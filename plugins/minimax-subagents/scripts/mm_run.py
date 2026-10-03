#!/usr/bin/env python3
"""mm-run: run a MiniMax worker inline through OpenCode on the Token Plan subscription.

    mm-run [--tier budget|balanced|quality | --model ID | --agent NAME]
           [--effort low|medium|high|xhigh|max] [--dir PATH] [-f FILE]...
           [--] "self-contained prompt"        (or prompt on stdin)

--tier routes to the installed lean worker (mm_fast / mm_m3 / mm_flash
_worker_<effort>) when present, else to `-m minimax/<model>`. Prints only the
final answer (thinking blocks stripped) so the calling harness pays for as few
tokens as possible.

Exit codes: 0 ok · 2 usage · 3 preflight · 75 quota/rate window (fall back,
do not retry on MiniMax) · 124 timeout · 1 other failure.
Never reads, prints, or asks for keys: auth lives in the OpenCode provider.
"""

from __future__ import annotations

import argparse
import fcntl
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

PROVIDER = os.environ.get("MM_PROVIDER", "minimax")
TIER_MODELS = {
    "budget": os.environ.get("MM_MODEL_BUDGET", "MiniMax-M2.7-highspeed"),
    "balanced": os.environ.get("MM_MODEL_BALANCED", "MiniMax-M3"),
    "quality": os.environ.get("MM_MODEL_QUALITY", "MiniMax-M3.1-Flash-Preview"),
}
# Only models with "tunable thinking depth" accept an OpenCode --variant.
VARIANT_MODELS = {"MiniMax-M3.1-Flash-Preview"}
EFFORTS = ("low", "medium", "high", "xhigh", "max")
# Worker families installed by smart-sub-agents (lane "minimax").
TIER_FAMILIES = {"budget": "mm_fast", "balanced": "mm_m3", "quality": "mm_flash"}
DEFAULT_EFFORT = {"budget": "low", "balanced": "medium", "quality": "high"}
FALLBACKS = {
    "budget": "haiku_worker_low | opencode-go/deepseek-v4-flash",
    "balanced": "sonnet_worker_medium | opencode-go/glm-5.2",
    "quality": "opus_worker_high | opencode-go/deepseek-v4-pro",
}

EXIT_USAGE, EXIT_PREFLIGHT, EXIT_QUOTA, EXIT_TIMEOUT = 2, 3, 75, 124

# Matched against OpenCode diagnostics only, never against model text.
QUOTA_RE = re.compile(
    r"\b429\b|rate.?limit|usage limit|quota|insufficient (?:balance|credit)|too many requests|limit exceeded",
    re.IGNORECASE,
)
TRANSIENT_RE = re.compile(
    r"UnknownError|Unexpected server error|\b50[0234]\b|ECONNRESET|ETIMEDOUT|socket hang up|overloaded|fetch failed",
    re.IGNORECASE,
)
THINK_RE = re.compile(r"<think>.*?</think>\s*", re.DOTALL)


def log(message: str) -> None:
    print(f"[mm-run] {message}", file=sys.stderr)


def opencode_bin() -> str | None:
    return os.environ.get("MM_OPENCODE_BIN") or shutil.which("opencode")


def agent_dirs(project_dir: str) -> list[Path]:
    configured = os.environ.get("MM_AGENT_DIRS")
    if configured:
        return [Path(p).expanduser() for p in configured.split(os.pathsep) if p]
    project = Path(project_dir)
    return [
        project / ".opencode" / "agents",
        project / ".opencode" / "agent",
        Path.home() / ".config" / "opencode" / "agents",
        Path.home() / ".config" / "opencode" / "agent",
    ]


def worker_agent(tier: str, effort: str | None, project_dir: str) -> str | None:
    """Installed lean worker for a tier, effort clamped to the family's range.

    Lean workers allowlist core tools; the default `build` agent ships every
    MCP schema (~118k input tokens per call vs ~6.7k, measured 2026-10-03).
    """
    family = TIER_FAMILIES[tier]
    effort = effort or DEFAULT_EFFORT[tier]
    allowed = EFFORTS if tier == "quality" else EFFORTS[:3]
    if effort not in allowed:
        effort = allowed[-1]
    name = f"{family}_worker_{effort}"
    if any((d / f"{name}.md").is_file() for d in agent_dirs(project_dir)):
        return name
    return None


def resolve_route(args: argparse.Namespace) -> tuple[str | None, str | None, str]:
    """Return (model id or None when the agent decides, agent name, tier label)."""
    if args.model:
        model = args.model.split("/", 1)[1] if args.model.startswith(f"{PROVIDER}/") else args.model
        tier = next((t for t, m in TIER_MODELS.items() if m == model), "custom")
        return model, args.agent, tier
    if args.agent and not args.tier:
        tier = next((t for t, f in TIER_FAMILIES.items() if args.agent.startswith(f"{f}_")), "agent")
        return None, args.agent, tier
    tier = args.tier or "balanced"
    if args.agent:
        return TIER_MODELS[tier], args.agent, tier
    model_overridden = f"MM_MODEL_{tier.upper()}" in os.environ
    agent = None if args.no_agent or model_overridden else worker_agent(tier, args.effort, args.dir)
    if agent:
        return None, agent, tier
    return TIER_MODELS[tier], None, tier


FIXED_DEPTH_AGENTS = (f"{TIER_FAMILIES['budget']}_", f"{TIER_FAMILIES['balanced']}_")


def supports_variant(model: str | None, agent: str | None) -> bool:
    if model:
        return model in VARIANT_MODELS
    return bool(agent) and not agent.startswith(FIXED_DEPTH_AGENTS)


def build_command(binary: str, args: argparse.Namespace, model: str | None, agent: str | None, prompt: str) -> list[str]:
    cmd = [binary, "run", "--format", "json", "--dir", args.dir]
    if model:
        cmd += ["-m", f"{PROVIDER}/{model}"]
    if agent:
        cmd += ["--agent", agent]
    # Agents carry their own reasoningEffort; an explicit --effort still wins.
    if args.effort and supports_variant(model, agent):
        cmd += ["--variant", args.effort]
    for path in args.file or []:
        cmd += ["-f", path]
    if args.pure:
        cmd.append("--pure")
    return cmd + ["--", prompt]


def parse_events(stdout: str) -> tuple[str, list[str], dict]:
    """Collect final text parts (last write wins per part id) and diagnostics."""
    texts: dict[str, str] = {}
    order: list[str] = []
    diagnostics: list[str] = []
    tokens: dict = {}
    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            diagnostics.append(line)
            continue
        part = event.get("part") or {}
        if part.get("type") == "text":
            part_id = part.get("id") or str(len(order))
            if part_id not in texts:
                order.append(part_id)
            texts[part_id] = part.get("text") or ""
        elif part.get("tokens"):
            tokens = part["tokens"]
        elif event.get("type") == "error" or "error" in event:
            diagnostics.append(json.dumps(event.get("error", event))[:2000])
    return "\n".join(texts[i] for i in order).strip(), diagnostics, tokens


class Slot:
    """File-lock semaphore: caps concurrent MiniMax workers on one machine.

    Token Plan tiers are sized for 3-7 parallel agents; more parallel calls
    only trip the 5-hour rolling window sooner.
    """

    def __init__(self, limit: int, wait_seconds: int) -> None:
        self.limit = max(1, limit)
        self.wait_seconds = wait_seconds
        self.root: Path | None = None
        self.handle = None

    @staticmethod
    def candidate_roots() -> list[Path]:
        configured = os.environ.get("MM_STATE_DIR")
        if configured:
            return [Path(configured) / "slots"]
        # Sandboxed harnesses (Codex workspace-write) cannot write ~/.cache but
        # can write $TMPDIR; slots there only cap calls from the same sandbox.
        return [
            Path.home() / ".cache" / "minimax-subagents" / "slots",
            Path(tempfile.gettempdir()) / f"minimax-subagents-{os.getuid()}" / "slots",
        ]

    def __enter__(self) -> "Slot":
        for root in self.candidate_roots():
            try:
                root.mkdir(parents=True, exist_ok=True)
                open(root / "slot-0.lock", "a").close()
            except OSError:
                continue
            self.root = root
            break
        else:
            log("no writable state dir; running without the parallel cap")
            return self
        deadline = time.monotonic() + self.wait_seconds
        announced = False
        while True:
            for index in range(self.limit):
                handle = open(self.root / f"slot-{index}.lock", "w")
                try:
                    fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except OSError:
                    handle.close()
                    continue
                self.handle = handle
                return self
            if time.monotonic() > deadline:
                raise TimeoutError(f"no free MiniMax slot after {self.wait_seconds}s (limit {self.limit})")
            if not announced:
                log(f"waiting for a free slot (MM_MAX_PARALLEL={self.limit})")
                announced = True
            time.sleep(1)

    def __exit__(self, *_: object) -> None:
        if self.handle:
            fcntl.flock(self.handle, fcntl.LOCK_UN)
            self.handle.close()


def check(binary: str | None) -> int:
    if not binary:
        log("opencode not found on PATH (install: https://opencode.ai)")
        return EXIT_PREFLIGHT
    result = subprocess.run([binary, "models", PROVIDER], capture_output=True, text=True, check=False)
    available = {line.strip().split("/", 1)[-1] for line in result.stdout.splitlines() if "/" in line}
    missing = 0
    for tier, model in TIER_MODELS.items():
        ok = model in available
        missing += not ok
        print(f"{'OK     ' if ok else 'MISSING'} {tier:<8} {PROVIDER}/{model}")
    if missing:
        log(f"configure the '{PROVIDER}' provider in opencode.json with your Token Plan key (see SKILL.md)")
        return EXIT_PREFLIGHT
    return 0


def read_prompt(args: argparse.Namespace) -> str:
    prompt = " ".join(args.prompt).strip()
    if (not prompt or prompt == "-") and not sys.stdin.isatty():
        prompt = sys.stdin.read().strip()
    return prompt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    target = parser.add_mutually_exclusive_group()
    target.add_argument("--tier", choices=sorted(TIER_MODELS))
    target.add_argument("--model", help="MiniMax model id, e.g. MiniMax-M3 or minimax/MiniMax-M3")
    parser.add_argument("--agent", help="OpenCode agent, e.g. mm_flash_worker_high (must be mode: all)")
    parser.add_argument("--effort", choices=EFFORTS, help="thinking depth (MiniMax-M3.1-Flash-Preview only)")
    parser.add_argument("--no-agent", action="store_true", help="use -m with the default agent instead of a lean worker")
    parser.add_argument("--dir", default=os.getcwd(), help="project directory the worker runs in")
    parser.add_argument("-f", "--file", action="append", help="attach a file (repeatable)")
    parser.add_argument("--timeout", type=int, default=int(os.environ.get("MM_TIMEOUT", "1800")))
    parser.add_argument("--retries", type=int, default=1, help="retries on transient errors only")
    parser.add_argument("--max-parallel", type=int, default=int(os.environ.get("MM_MAX_PARALLEL", "3")))
    parser.add_argument("--thinking", action="store_true", help="keep <think> blocks in the output")
    parser.add_argument("--pure", action="store_true", help="run OpenCode without external plugins")
    parser.add_argument("--dry-run", action="store_true", help="print the OpenCode command and exit")
    parser.add_argument("--check", action="store_true", help="verify opencode and the MiniMax models")
    parser.add_argument("prompt", nargs="*")
    args = parser.parse_args(argv)

    binary = opencode_bin()
    if args.check:
        return check(binary)

    prompt = read_prompt(args)
    if not prompt:
        parser.print_usage(sys.stderr)
        log("missing prompt")
        return EXIT_USAGE
    model, agent, tier = resolve_route(args)
    if args.effort and not supports_variant(model, agent):
        log(f"--effort ignored: {model or agent} has no thinking-depth variants (budget contract only)")

    cmd = build_command(binary or "opencode", args, model, agent, prompt)
    if args.dry_run:
        print(" ".join(cmd[:-1] + ["<prompt>"]))
        return 0
    if not binary:
        log("opencode not found on PATH (install: https://opencode.ai)")
        return EXIT_PREFLIGHT

    label = agent or model
    attempts = max(0, args.retries) + 1
    try:
        with Slot(args.max_parallel, args.timeout):
            for attempt in range(1, attempts + 1):
                started = time.monotonic()
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=args.timeout, check=False)
                except subprocess.TimeoutExpired:
                    log(f"timeout after {args.timeout}s on {label}")
                    return EXIT_TIMEOUT
                text, diagnostics, tokens = parse_events(result.stdout)
                diagnostic_text = "\n".join(diagnostics + [result.stderr])
                elapsed = time.monotonic() - started
                if result.returncode == 0 and text:
                    if not args.thinking:
                        text = THINK_RE.sub("", text).strip()
                    print(text)
                    usage = f" in={tokens.get('input')} out={tokens.get('output')}" if tokens else ""
                    log(f"ok model={label} tier={tier} t={elapsed:.0f}s{usage}")
                    return 0
                if QUOTA_RE.search(diagnostic_text):
                    print(f"ROUTE-FALLBACK: minimax quota/rate window hit on {label}; use {FALLBACKS.get(tier, FALLBACKS['balanced'])}")
                    log("Token Plan uses 5-hour rolling and weekly windows; do not retry on MiniMax")
                    return EXIT_QUOTA
                if attempt < attempts and (TRANSIENT_RE.search(diagnostic_text) or (result.returncode == 0 and not text)):
                    log(f"transient failure on {label}, retry {attempt}/{attempts - 1}")
                    time.sleep(3 * attempt)
                    continue
                tail = "\n".join(diagnostic_text.strip().splitlines()[-20:])
                log(f"failed model={label} rc={result.returncode}\n{tail}")
                return result.returncode or 1
    except TimeoutError as exc:
        log(str(exc))
        return EXIT_TIMEOUT
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
