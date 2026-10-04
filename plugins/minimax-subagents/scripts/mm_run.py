#!/usr/bin/env python3
"""mm-run: run a MiniMax worker inline on the subscription (MiniMax Code or OpenCode).

    mm-run [--tier budget|balanced|quality | --model ID | --agent NAME]
           [--effort low|medium|high|xhigh|max] [--backend auto|mcode|opencode]
           [--dir PATH] [-f FILE]... [--] "self-contained prompt"   (or stdin)

Backends:
  mcode    (default) `mcode exec` from MiniMax Code: OAuth login, no key on
           disk, ~14k input tokens per call.
  opencode `opencode run` with the lean mm_* workers (~7k input tokens) or
           `-m minimax/<model>`; needs the `minimax` provider configured.
  auto     mcode when installed, else opencode. Agents that are not mm_*
           workers always run on opencode.

--agent mm_<family>_worker_<effort> maps to the same model + effort on mcode.
Prints only the final answer (thinking blocks stripped).

Exit codes: 0 ok · 2 usage · 3 preflight · 75 quota/rate window (fall back,
do not retry on MiniMax) · 124 timeout · 1 other failure.
Never reads, prints, or asks for keys.
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
# Only models with "tunable thinking depth" accept an effort; both backends
# reject or ignore it elsewhere.
VARIANT_MODELS = {"MiniMax-M3.1-Flash-Preview"}
EFFORTS = ("low", "medium", "high", "xhigh", "max")
# Worker families installed by smart-sub-agents (lane "minimax").
TIER_FAMILIES = {"budget": "mm_fast", "balanced": "mm_m3", "quality": "mm_flash"}
DEFAULT_EFFORT = {"budget": "low", "balanced": "medium", "quality": "high"}
WORKER_RE = re.compile(r"^(mm_fast|mm_m3|mm_flash)_worker_(low|medium|high|xhigh|max)$")
FALLBACKS = {
    "budget": "haiku_worker_low | opencode-go/deepseek-v4-flash",
    "balanced": "sonnet_worker_medium | opencode-go/glm-5.2",
    "quality": "opus_worker_high | opencode-go/deepseek-v4-pro",
}

EXIT_USAGE, EXIT_PREFLIGHT, EXIT_QUOTA, EXIT_TIMEOUT = 2, 3, 75, 124

# Matched against backend diagnostics only, never against model text.
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


def mcode_bin() -> str | None:
    configured = os.environ.get("MM_MCODE_BIN")
    if configured is not None:
        return configured or None  # empty string disables mcode
    found = shutil.which("mcode")
    if found:
        return found
    default = Path.home() / ".minimax-code" / "bin" / "mcode"
    return str(default) if os.access(default, os.X_OK) else None


# --------------------------------------------------------------------------
# Route resolution
# --------------------------------------------------------------------------


class Route:
    def __init__(self, backend: str, tier: str, model: str | None, agent: str | None, effort: str | None) -> None:
        self.backend = backend
        self.tier = tier
        self.model = model
        self.agent = agent
        self.effort = effort

    @property
    def label(self) -> str:
        return self.agent or self.model or "?"


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


def clamp_effort(tier: str, effort: str | None) -> str:
    effort = effort or DEFAULT_EFFORT[tier]
    allowed = EFFORTS if tier == "quality" else EFFORTS[:3]
    return effort if effort in allowed else allowed[-1]


def worker_agent(tier: str, effort: str | None, project_dir: str) -> str | None:
    """Installed lean OpenCode worker for a tier, effort clamped to the family.

    Lean workers allowlist core tools; the default `build` agent ships every
    MCP schema (~118k input tokens per call vs ~6.7k, measured 2026-10-03).
    """
    name = f"{TIER_FAMILIES[tier]}_worker_{clamp_effort(tier, effort)}"
    if any((d / f"{name}.md").is_file() for d in agent_dirs(project_dir)):
        return name
    return None


def pick_backend(args: argparse.Namespace) -> str:
    choice = args.backend or os.environ.get("MM_BACKEND", "auto")
    if args.agent and not WORKER_RE.match(args.agent):
        if choice == "mcode":
            log(f"--agent {args.agent} is an OpenCode agent; using the opencode backend")
        return "opencode"
    if choice == "auto":
        return "mcode" if mcode_bin() else "opencode"
    return choice


def resolve_route(args: argparse.Namespace) -> Route:
    backend = pick_backend(args)
    worker = WORKER_RE.match(args.agent) if args.agent else None
    tier_of_family = {family: tier for tier, family in TIER_FAMILIES.items()}

    if args.model:
        model = args.model.split("/", 1)[1] if args.model.startswith(f"{PROVIDER}/") else args.model
        tier = next((t for t, m in TIER_MODELS.items() if m == model), "custom")
        agent = args.agent if backend == "opencode" else None
        return Route(backend, tier, model, agent, args.effort)

    if args.agent and not args.tier:
        if worker:
            tier = tier_of_family[worker.group(1)]
            if backend == "mcode":
                return Route(backend, tier, TIER_MODELS[tier], None, args.effort or worker.group(2))
            return Route(backend, tier, None, args.agent, args.effort)
        return Route(backend, "agent", None, args.agent, args.effort)

    tier = args.tier or "balanced"
    if backend == "mcode":
        return Route(backend, tier, TIER_MODELS[tier], None, clamp_effort(tier, args.effort))
    if args.agent:
        return Route(backend, tier, TIER_MODELS[tier], args.agent, args.effort)
    model_overridden = f"MM_MODEL_{tier.upper()}" in os.environ
    agent = None if args.no_agent or model_overridden else worker_agent(tier, args.effort, args.dir)
    if agent:
        return Route(backend, tier, None, agent, args.effort)
    return Route(backend, tier, TIER_MODELS[tier], None, args.effort)


FIXED_DEPTH_AGENTS = (f"{TIER_FAMILIES['budget']}_", f"{TIER_FAMILIES['balanced']}_")


def supports_effort(route: Route) -> bool:
    if route.model:
        return route.model in VARIANT_MODELS
    return bool(route.agent) and not route.agent.startswith(FIXED_DEPTH_AGENTS)


# --------------------------------------------------------------------------
# Backends
# --------------------------------------------------------------------------


def build_opencode(binary: str, args: argparse.Namespace, route: Route, prompt: str) -> list[str]:
    cmd = [binary, "run", "--format", "json", "--dir", args.dir]
    if route.model:
        cmd += ["-m", f"{PROVIDER}/{route.model}"]
    if route.agent:
        cmd += ["--agent", route.agent]
    # Agents carry their own reasoningEffort; an explicit --effort still wins.
    if args.effort and supports_effort(route):
        cmd += ["--variant", args.effort]
    for path in args.file or []:
        cmd += ["-f", path]
    if args.pure:
        cmd.append("--pure")
    return cmd + ["--", prompt]


def build_mcode(binary: str, args: argparse.Namespace, route: Route, prompt: str) -> list[str]:
    cmd = [
        binary, "exec",
        "--cwd", args.dir,
        "--output-format", "json",
        "--timeout", f"{args.timeout}s",
        "--model", f"{PROVIDER}/{route.model}",
        "--permission", os.environ.get("MM_MCODE_PERMISSION", "smart"),
    ]
    # mcode rejects --effort on models without tunable thinking depth.
    if route.effort and supports_effort(route):
        cmd += ["--effort", route.effort]
    for path in args.file or []:
        cmd += ["--file", path]
    return cmd + ["--", prompt]


class Outcome:
    def __init__(self, ok: bool, text: str, diagnostics: str, usage: str, timed_out: bool = False) -> None:
        self.ok = ok
        self.text = text
        self.diagnostics = diagnostics
        self.usage = usage
        self.timed_out = timed_out


def parse_opencode(result: subprocess.CompletedProcess) -> Outcome:
    """Collect final text parts (last write wins per part id) and diagnostics."""
    texts: dict[str, str] = {}
    order: list[str] = []
    diagnostics: list[str] = []
    tokens: dict = {}
    for line in result.stdout.splitlines():
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
    text = "\n".join(texts[i] for i in order).strip()
    usage = f" in={tokens.get('input')} out={tokens.get('output')}" if tokens else ""
    return Outcome(result.returncode == 0 and bool(text), text, "\n".join(diagnostics + [result.stderr]), usage)


def parse_mcode(result: subprocess.CompletedProcess) -> Outcome:
    """`mcode exec --output-format json` ends with one exec.result object."""
    final: dict = {}
    for line in reversed(result.stdout.splitlines()):
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "exec.result":
            final = event
            break
    status = final.get("status", "")
    error = final.get("error") or {}
    usage_data = final.get("usage") or {}
    usage = ""
    if usage_data:
        cached = usage_data.get("cacheReadTokens") or usage_data.get("cacheWriteTokens")
        usage = f" in={usage_data.get('inputTokens')} out={usage_data.get('outputTokens')}"
        usage += f" cache={cached}" if cached else ""
    text = (final.get("output") or "").strip()
    # Without an exec.result (crash, sandbox denial) the reason is on stdout.
    stdout_tail = "" if final else "\n".join(result.stdout.strip().splitlines()[-20:])
    diagnostics = "\n".join(filter(None, [json.dumps(error) if error else "", stdout_tail, result.stderr]))
    timed_out = status in {"timed_out", "timeout"} or "timed out" in str(error.get("message", "")).lower()
    return Outcome(result.returncode == 0 and status == "succeeded" and bool(text), text, diagnostics, usage, timed_out)


# --------------------------------------------------------------------------
# Concurrency cap
# --------------------------------------------------------------------------


class Slot:
    """File-lock semaphore: caps concurrent MiniMax workers on one machine.

    Subscription tiers are sized for 3-7 parallel agents; more parallel calls
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


# --------------------------------------------------------------------------
# Preflight
# --------------------------------------------------------------------------


def check_mcode(binary: str | None) -> bool:
    if not binary:
        print("MISSING mcode   MiniMax Code not installed (curl -fsSL https://filecdn.minimax.chat/public/install.sh | bash)")
        return False
    result = subprocess.run([binary, "provider", "list"], capture_output=True, text=True, check=False)
    active = [line.split()[1] if line.startswith("*") else line.split()[0]
              for line in result.stdout.splitlines() if "active" in line]
    if result.returncode != 0 or not active:
        print("MISSING mcode   no active provider (run: mcode login)")
        return False
    print(f"OK      mcode   provider={active[0]} ({binary})")
    return True


def check_opencode(binary: str | None) -> bool:
    if not binary:
        print("MISSING opencode not found on PATH (https://opencode.ai)")
        return False
    result = subprocess.run([binary, "models", PROVIDER], capture_output=True, text=True, check=False)
    available = {line.strip().split("/", 1)[-1] for line in result.stdout.splitlines() if "/" in line}
    ok = True
    for tier, model in TIER_MODELS.items():
        present = model in available
        ok &= present
        print(f"{'OK     ' if present else 'MISSING'} opencode {tier:<8} {PROVIDER}/{model}")
    return ok


def check(args: argparse.Namespace) -> int:
    default = pick_backend(args)
    print(f"default backend: {default}")
    mcode_ok = check_mcode(mcode_bin())
    opencode_ok = check_opencode(opencode_bin())
    if (default == "mcode" and mcode_ok) or (default == "opencode" and opencode_ok):
        return 0
    log("default backend not ready; see SKILL.md (Install / update)")
    return EXIT_PREFLIGHT


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------


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
    parser.add_argument("--agent", help="mm_<family>_worker_<effort>, or any OpenCode agent (mode: all)")
    parser.add_argument("--effort", choices=EFFORTS, help="thinking depth (MiniMax-M3.1-Flash-Preview only)")
    parser.add_argument("--backend", choices=("auto", "mcode", "opencode"), help="default: $MM_BACKEND or auto")
    parser.add_argument("--no-agent", action="store_true", help="opencode: use -m with the default agent")
    parser.add_argument("--dir", default=os.getcwd(), help="project directory the worker runs in")
    parser.add_argument("-f", "--file", action="append", help="attach a file (repeatable)")
    parser.add_argument("--timeout", type=int, default=int(os.environ.get("MM_TIMEOUT", "1800")))
    parser.add_argument("--retries", type=int, default=1, help="retries on transient errors only")
    parser.add_argument("--max-parallel", type=int, default=int(os.environ.get("MM_MAX_PARALLEL", "3")))
    parser.add_argument("--thinking", action="store_true", help="keep <think> blocks in the output")
    parser.add_argument("--pure", action="store_true", help="opencode: run without external plugins")
    parser.add_argument("--dry-run", action="store_true", help="print the backend command and exit")
    parser.add_argument("--check", action="store_true", help="verify both backends and the MiniMax models")
    parser.add_argument("prompt", nargs="*")
    args = parser.parse_args(argv)

    if args.check:
        return check(args)

    prompt = read_prompt(args)
    if not prompt:
        parser.print_usage(sys.stderr)
        log("missing prompt")
        return EXIT_USAGE

    route = resolve_route(args)
    if args.effort and not supports_effort(route):
        log(f"--effort ignored: {route.label} has no thinking-depth variants (budget contract only)")
    if args.dry_run:
        return execute(args, route, prompt)

    try:
        with Slot(args.max_parallel, args.timeout):
            code = execute(args, route, prompt)
            # An auto-selected mcode that breaks for infrastructure reasons
            # (sandbox denials, local locks, crashes) gets one OpenCode attempt.
            if code not in NO_BACKEND_FALLBACK and route.backend == "mcode" and backend_is_auto(args) and opencode_bin():
                log("mcode failed; retrying once on the opencode backend")
                args.backend = "opencode"
                code = execute(args, resolve_route(args), prompt)
            return code
    except TimeoutError as exc:
        log(str(exc))
        return EXIT_TIMEOUT


NO_BACKEND_FALLBACK = {0, EXIT_USAGE, EXIT_QUOTA, EXIT_TIMEOUT}


def backend_is_auto(args: argparse.Namespace) -> bool:
    return (args.backend or os.environ.get("MM_BACKEND", "auto")) == "auto"


def execute(args: argparse.Namespace, route: Route, prompt: str) -> int:
    if route.backend == "mcode":
        binary = mcode_bin()
        cmd = build_mcode(binary or "mcode", args, route, prompt)
        parse = parse_mcode
    else:
        binary = opencode_bin()
        cmd = build_opencode(binary or "opencode", args, route, prompt)
        parse = parse_opencode

    if args.dry_run:
        print(" ".join(cmd[:-1] + ["<prompt>"]))
        return 0
    if not binary:
        log(f"{route.backend} not found (run: mm-run --check)")
        return EXIT_PREFLIGHT

    attempts = max(0, args.retries) + 1
    shown_effort = route.effort if route.backend == "mcode" else args.effort
    effort_note = f" effort={shown_effort}" if shown_effort and supports_effort(route) else ""
    for attempt in range(1, attempts + 1):
        started = time.monotonic()
        try:
            # Backend gets --timeout too; this is the hard stop for hung starts.
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=args.timeout + 30, check=False)
        except subprocess.TimeoutExpired:
            log(f"timeout after {args.timeout}s on {route.label} ({route.backend})")
            return EXIT_TIMEOUT
        outcome = parse(result)
        elapsed = time.monotonic() - started
        if outcome.ok:
            text = outcome.text if args.thinking else THINK_RE.sub("", outcome.text).strip()
            print(text)
            log(f"ok backend={route.backend} model={route.label} tier={route.tier}{effort_note} "
                f"t={elapsed:.0f}s{outcome.usage}")
            return 0
        if QUOTA_RE.search(outcome.diagnostics):
            print(f"ROUTE-FALLBACK: minimax quota/rate window hit on {route.label}; "
                  f"use {FALLBACKS.get(route.tier, FALLBACKS['balanced'])}")
            log("subscription quota uses 5-hour rolling and weekly windows; do not retry on MiniMax")
            return EXIT_QUOTA
        if outcome.timed_out:
            log(f"timeout after {args.timeout}s on {route.label} ({route.backend})")
            return EXIT_TIMEOUT
        transient = TRANSIENT_RE.search(outcome.diagnostics) or (result.returncode == 0 and not outcome.text)
        if attempt < attempts and transient:
            log(f"transient failure on {route.label}, retry {attempt}/{attempts - 1}")
            time.sleep(3 * attempt)
            continue
        tail = "\n".join(outcome.diagnostics.strip().splitlines()[-20:])
        log(f"failed backend={route.backend} model={route.label} rc={result.returncode}\n{tail}")
        return result.returncode or 1
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
