#!/usr/bin/env python3
"""Install the worker agent matrix across Claude, Codex, OpenCode, and Agy.

Claude agents are canonical. Other harnesses get:
- Codex: native TOML with model + model_reasoning_effort
- OpenCode: adapted markdown (mode/permission/model provider prefix)
- Agy: symlink body to Claude when possible, else adapted markdown

Idempotent. Never deletes non-managed agents.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

from validate_catalog import validate

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = PLUGIN_ROOT / "references" / "provider-matrix.json"
MANAGED_MARKER = "managed-by: smart-sub-agents/worker-matrix"

HOME = Path.home()
HARNESS_DIRS = {
    "claude-code": HOME / ".claude" / "agents",
    "codex": HOME / ".codex" / "agents",
    "opencode": HOME / ".config" / "opencode" / "agents",
    "antigravity": HOME / ".agy" / "agents",
}

EFFORT_TOKEN_BUDGET = {
    "none": "1k-4k",
    "low": "2k-10k",
    "medium": "8k-35k",
    "high": "15k-60k",
    "xhigh": "25k-100k",
    "max": "40k-150k",
    "ultra": "60k-200k",
}

EFFORT_TIME_BUDGET = {
    "none": "1-3min",
    "low": "2-8min",
    "medium": "8-30min",
    "high": "15-60min",
    "xhigh": "20-90min",
    "max": "30-120min",
    "ultra": "45-180min",
}

TIER_COLOR = {
    "budget": "#22C55E",
    "balanced": "#3B82F6",
    "quality": "#A855F7",
}


def load_catalog(path: Path) -> dict:
    catalog = json.loads(path.read_text(encoding="utf-8"))
    errors = validate(catalog)
    if errors:
        raise ValueError("; ".join(errors))
    return catalog


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def worker_name(family_id: str, effort: str) -> str:
    return f"{slug(family_id)}_worker_{slug(effort)}"


def body_text(family: dict, effort: str, harness: str) -> str:
    tasks = ", ".join(family.get("tasks", []))
    token_budget = EFFORT_TOKEN_BUDGET.get(effort, "unknown")
    time_budget = EFFORT_TIME_BUDGET.get(effort, "unknown")
    return f"""# {family['id'].title()} Worker ({effort})

You are a **tiered worker subagent**. Stay inside the selected route.

## Route
- harness: `{harness}`
- provider: `{family['provider']}`
- model: `{family['model']}`
- effort: `{effort}`
- tier: `{family['tier']}`
- tasks: {tasks}

## Budget contract
- tokens: `{token_budget}`
- time: `{time_budget}`
- effort: `{effort}`
- escalate only after 2 failed validation attempts, then return ROUTE-ESCALATE with next tier.

## Protocol
1. Restate the task in one line and confirm it matches the allowed tasks above.
2. Prefer local CLI (`rtk`, lint, tsc, tests) before expanding scope.
3. Make surgical edits only. No drive-by refactors.
4. Verify with the cheapest command that proves success.
5. Return: changed files, verification command+result, residual risks.

## DO NOT
- Invent provider availability or credentials.
- Exceed the effort/token budget without explicit user approval.
- Touch unrelated files.
- Mark complete without verification evidence.
"""


def render_claude(name: str, family: dict, effort: str) -> str:
    tasks = ", ".join(family.get("tasks", []))
    return f"""---
name: {name}
description: >
  Worker {family['id']} @ {effort} effort ({family['tier']}).
  Use for: {tasks}.
  Model {family['model']}. Managed by smart-sub-agents worker matrix.
model: {family['model']}
effort: {effort}
color: "{TIER_COLOR.get(family['tier'], '#6B7280')}"
mode: subagent
# {MANAGED_MARKER}
---

{body_text(family, effort, 'claude-code')}
"""


def render_codex_toml(name: str, family: dict, effort: str) -> str:
    tasks = ", ".join(family.get("tasks", []))
    body = body_text(family, effort, "codex").replace('"""', "'''")
    return f'''name = "{name}"
description = "Worker {family['id']} @ {effort} ({family['tier']}). Tasks: {tasks}. Model {family['model']}."
model = "{family['model']}"
model_reasoning_effort = "{effort}"
sandbox_mode = "workspace-write"
# {MANAGED_MARKER}
developer_instructions = """
{body}
"""
'''


def render_opencode(name: str, family: dict, effort: str, lane: str | None = None) -> str:
    provider = family["provider"]
    model_ref = f"{provider}/{family['model']}"
    tasks = ", ".join(family.get("tasks", []))
    lane_note = f" lane={lane}" if lane else ""
    return f"""---
name: {name}
description: >
  Worker {family['id']} @ {effort} ({family['tier']}){lane_note}.
  Use for: {tasks}. Model {model_ref}.
mode: subagent
model: {model_ref}
temperature: 0.1
color: "{TIER_COLOR.get(family['tier'], '#6B7280')}"
permission:
  bash: allow
  read: allow
  edit: allow
  glob: allow
  grep: allow
  webfetch: deny
# {MANAGED_MARKER}
---

{body_text(family, effort, 'opencode')}
"""


def write_file(path: Path, content: str, dry_run: bool) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.is_symlink():
        if dry_run:
            return f"WOULD_REPLACE_SYMLINK {path}"
        path.unlink()
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return f"SKIP {path}"
    if dry_run:
        return f"WOULD_WRITE {path}"
    path.write_text(content, encoding="utf-8")
    return f"WRITE {path}"


def symlink_file(src: Path, dst: Path, dry_run: bool) -> str:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() or dst.is_symlink():
        if dst.is_symlink() and dst.resolve() == src.resolve():
            return f"SKIP_LINK {dst}"
        if dry_run:
            return f"WOULD_RELINK {dst} -> {src}"
        dst.unlink()
    if dry_run:
        return f"WOULD_LINK {dst} -> {src}"
    os.symlink(src, dst)
    return f"LINK {dst} -> {src}"


def install_claude(catalog: dict, dry_run: bool) -> list[str]:
    results: list[str] = []
    root = HARNESS_DIRS["claude-code"]
    matrix = catalog["workerMatrix"]["claude-code"]
    for family in matrix["families"]:
        for effort in family["efforts"]:
            name = worker_name(family["id"], effort)
            path = root / f"{name}.md"
            results.append(write_file(path, render_claude(name, family, effort), dry_run))
    return results


def install_codex(catalog: dict, dry_run: bool) -> list[str]:
    results: list[str] = []
    root = HARNESS_DIRS["codex"]
    matrix = catalog["workerMatrix"]["codex"]
    for family in matrix["families"]:
        for effort in family["efforts"]:
            name = worker_name(family["id"], effort)
            path = root / f"{name}.toml"
            results.append(write_file(path, render_codex_toml(name, family, effort), dry_run))
    return results


def install_opencode(catalog: dict, dry_run: bool) -> list[str]:
    results: list[str] = []
    root = HARNESS_DIRS["opencode"]
    lanes = catalog["workerMatrix"]["opencode"]["lanes"]
    for lane_id, lane in lanes.items():
        for family in lane["families"]:
            for effort in family["efforts"]:
                # names: go_luna_worker_high, zen_sol_worker_max
                name = worker_name(family["id"], effort)
                path = root / f"{name}.md"
                results.append(write_file(path, render_opencode(name, family, effort, lane=lane_id), dry_run))
    return results


def install_agy(catalog: dict, dry_run: bool) -> list[str]:
    """Agy consumes Claude canonical bodies via symlink when model-agnostic.

    Worker agents are model-specific, so Agy gets adapted markdown copies that
    mirror Claude content (same body) with Claude frontmatter kept for shared
    skills and a note that execution should prefer Claude/Codex native workers.
    """
    results: list[str] = []
    root = HARNESS_DIRS["antigravity"]
    claude_root = HARNESS_DIRS["claude-code"]
    # Symlink each Claude worker into Agy so body stays canonical.
    for family in catalog["workerMatrix"]["claude-code"]["families"]:
        for effort in family["efforts"]:
            name = worker_name(family["id"], effort)
            src = claude_root / f"{name}.md"
            dst = root / f"{name}.md"
            if not src.exists() and not dry_run:
                results.append(f"MISSING_CANONICAL {src}")
                continue
            results.append(symlink_file(src, dst, dry_run))
    # Also expose codex-named aliases as thin markdown pointers for discoverability.
    for family in catalog["workerMatrix"]["codex"]["families"]:
        for effort in family["efforts"]:
            name = worker_name(family["id"], effort)
            # Map codex family -> claude tier equivalent for body
            tier_map = {"luna": "haiku", "terra": "sonnet", "sol": "opus"}
            claude_family = tier_map[family["id"]]
            # clamp effort to claude family efforts
            claude_efforts = next(
                f["efforts"]
                for f in catalog["workerMatrix"]["claude-code"]["families"]
                if f["id"] == claude_family
            )
            mapped_effort = effort if effort in claude_efforts else claude_efforts[-1]
            src = claude_root / f"{worker_name(claude_family, mapped_effort)}.md"
            dst = root / f"{name}.md"
            content = f"""---
name: {name}
description: >
  Codex-named alias for {family['id']} @ {effort}. Body canonical from Claude
  {claude_family}_worker_{mapped_effort}. Prefer native Codex TOML worker when
  running under Codex.
# {MANAGED_MARKER}
---

See canonical Claude worker: `{src.name}`.
Harness note: Agy should load Claude-equivalent tier and keep budget discipline.
Provider target when delegated to Codex: `{family['provider']}/{family['model']}` effort `{effort}`.
"""
            results.append(write_file(dst, content, dry_run))
    return results


def symlink_canonical_specialists(dry_run: bool) -> list[str]:
    """Keep shared specialists pointing at Claude canonical files."""
    results: list[str] = []
    claude = HARNESS_DIRS["claude-code"]
    shared = [
        "git-master.md",
        "zai-specialist.md",
        "thermo-nuclear-review-subagent.md",
        "thermo-nuclear-code-quality-review-subagent.md",
    ]
    for harness, root in HARNESS_DIRS.items():
        if harness == "claude-code":
            continue
        for name in shared:
            src = claude / name
            if not src.exists():
                continue
            # OpenCode keeps adapted copies for frontmatter; only symlink body-identical harnesses.
            if harness == "opencode":
                continue
            dst = root / name
            results.append(symlink_file(src, dst, dry_run))
    return results


def validate_installed() -> list[str]:
    errors: list[str] = []
    # Claude frontmatter
    for path in HARNESS_DIRS["claude-code"].glob("*_worker_*.md"):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            errors.append(f"{path}: missing frontmatter")
            continue
        if "model:" not in text.split("---", 2)[1]:
            errors.append(f"{path}: missing model")
        if "effort:" not in text.split("---", 2)[1]:
            errors.append(f"{path}: missing effort")
        if MANAGED_MARKER not in text:
            errors.append(f"{path}: missing managed marker")
    # Codex toml
    for path in HARNESS_DIRS["codex"].glob("*_worker_*.toml"):
        text = path.read_text(encoding="utf-8")
        if 'model = "' not in text:
            errors.append(f"{path}: missing model")
        if "model_reasoning_effort" not in text:
            errors.append(f"{path}: missing model_reasoning_effort")
        if MANAGED_MARKER not in text:
            errors.append(f"{path}: missing managed marker")
    # OpenCode
    for path in HARNESS_DIRS["opencode"].glob("*_worker_*.md"):
        text = path.read_text(encoding="utf-8")
        fm = text.split("---", 2)[1] if text.startswith("---") else ""
        if "mode: subagent" not in fm:
            errors.append(f"{path}: missing mode: subagent")
        if "model:" not in fm:
            errors.append(f"{path}: missing model")
        if MANAGED_MARKER not in text:
            errors.append(f"{path}: missing managed marker")
    # Agy: validate managed codex-named aliases only. Symlinks point to Claude
    # canonical bodies (already validated above); non-managed files are skipped
    # so a user's manual worker file does not trigger a false positive.
    for path in HARNESS_DIRS["antigravity"].glob("*_worker_*.md"):
        if path.is_symlink():
            continue
        text = path.read_text(encoding="utf-8")
        if MANAGED_MARKER not in text:
            continue
        if not text.startswith("---"):
            errors.append(f"{path}: missing frontmatter")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--harness", choices=["all", "claude-code", "codex", "opencode", "antigravity"], default="all")
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()

    if args.validate_only:
        errors = validate_installed()
        if errors:
            for e in errors:
                print(f"ERROR: {e}", file=sys.stderr)
            return 1
        print("OK: installed worker matrix validates")
        return 0

    catalog = load_catalog(args.catalog)
    results: list[str] = []
    harnesses = (
        ["claude-code", "codex", "opencode", "antigravity"]
        if args.harness == "all"
        else [args.harness]
    )
    # Claude first so Agy can symlink.
    order = ["claude-code", "codex", "opencode", "antigravity"]
    for harness in order:
        if harness not in harnesses:
            continue
        if harness == "claude-code":
            results.extend(install_claude(catalog, args.dry_run))
        elif harness == "codex":
            results.extend(install_codex(catalog, args.dry_run))
        elif harness == "opencode":
            results.extend(install_opencode(catalog, args.dry_run))
        elif harness == "antigravity":
            results.extend(install_agy(catalog, args.dry_run))

    results.extend(symlink_canonical_specialists(args.dry_run))

    writes = sum(1 for r in results if r.startswith("WRITE") or r.startswith("LINK"))
    skips = sum(1 for r in results if r.startswith("SKIP"))
    for line in results:
        print(line)
    print(f"---\nsummary: writes/links={writes} skips={skips} total={len(results)} date={date.today().isoformat()}")

    if not args.dry_run:
        errors = validate_installed()
        if errors:
            for e in errors:
                print(f"ERROR: {e}", file=sys.stderr)
            return 1
        print("OK: validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
