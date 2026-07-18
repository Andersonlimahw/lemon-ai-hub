#!/usr/bin/env python3
"""sync-agents.py — Retrocompatible agent frontmatter synchronizer.

Reads canonical agent files from `plugins/cli-wrapper/agents/*.md` and emits
per-harness copies with the correct YAML frontmatter schema for each target
AI harness. Single source of truth = canonical .md files.

Harnesses supported:
  - claude   (Claude Code):    name, description, color, mode, permission
  - codex    (Codex CLI):      .md (same as claude) + .toml sidecar
  - gemini   (Gemini CLI):     name, description, color, mode, permission
  - agy      (Antigravity):    name, description, color, mode, permission
  - opencode (OpenCode):       description, mode, color, permission
                               (NO `name` — file name IS the agent name)

Why this exists:
  The previous setup created raw symlinks from `~/.{harness}/agents/` to
  Claude-format files. OpenCode then rejected the `tools:` key (deprecated
  v1.1.1), and `name:` is treated as a label rather than identity. Some
  scripts attempted to "fix" this by uppercasing `tools` to `Tools` and
  pluralizing `color` to `colors` — both invalid. This script enforces a
  strict per-harness schema with fail-loud warnings.

Usage:
  sync-agents.py                apply transforms (default)
  sync-agents.py --dry-run      preview, no writes
  sync-agents.py --verify       read-only check, exit 1 on drift
  sync-agents.py --harness X    restrict to one harness
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent
CANONICAL_DIR = REPO_ROOT / "plugins" / "cli-wrapper" / "agents"

# Per-harness: (config_dir, top-level keys allowed, file extension, sidecar?)
# file_name_in_target = file_name_in_canonical (lowercase stem)
HARNESSES: dict[str, dict] = {
    "claude": {
        "config_dir": "~/.claude",
        "agents_subdir": "agents",
        "allowed_top_keys": {"name", "description", "color", "mode", "permission", "tools"},
        "drops": set(),
        "sidecar": None,
    },
    "codex": {
        "config_dir": "~/.codex",
        "agents_subdir": "agents",
        "allowed_top_keys": {"name", "description", "color", "mode", "permission"},
        "drops": set(),
        "sidecar": "toml",
    },
    "gemini": {
        "config_dir": "~/.gemini",
        "agents_subdir": "agents",
        "allowed_top_keys": {"name", "description", "color", "mode", "permission"},
        "drops": set(),
        "sidecar": None,
    },
    "agy": {
        "config_dir": "~/.agy",
        "agents_subdir": "agents",
        "allowed_top_keys": {"name", "description", "color", "mode", "permission"},
        "drops": set(),
        "sidecar": None,
    },
    "opencode": {
        "config_dir": "~/.opencode",
        "agents_subdir": "agents",
        "allowed_top_keys": {"description", "color", "mode", "permission"},
        "drops": {"name"},  # file name = agent name in OpenCode
        "sidecar": None,
    },
}

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Parse simple YAML frontmatter (only top-level scalars + nested `permission:` block)."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    raw, body = m.group(1), m.group(2)
    fm: dict[str, str] = {}
    current_key: str | None = None
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  ") and current_key:
            fm[current_key] += "\n" + line
            continue
        if ":" in line:
            k, _, v = line.partition(":")
            k, v = k.strip(), v.strip()
            if v == "":
                fm[k] = ""
                current_key = k
            else:
                fm[k] = v
                current_key = None
    return fm, body


def render_frontmatter(fm: dict[str, str]) -> str:
    out = ["---"]
    for k, v in fm.items():
        if "\n" in v:
            out.append(f"{k}:")
            for sub in v.splitlines():
                if sub.strip():
                    out.append(sub)
        else:
            out.append(f"{k}: {v}")
    out.append("---")
    return "\n".join(out) + "\n"


def extract_prompt_block(body: str) -> str:
    """For Codex .toml: capture the first XML-like role block as developer_instructions."""
    m = re.search(r"(<role>.*?</role>)", body, re.DOTALL)
    return m.group(1).strip() if m else body.strip()


def transform_for_harness(fm: dict[str, str], body: str, harness: str) -> tuple[str, str | None]:
    """Return (md_text, optional_sidecar_text) for the target harness."""
    spec = HARNESSES[harness]
    out: dict[str, str] = {}
    dropped: list[str] = []
    for k, v in fm.items():
        if k in spec["drops"]:
            dropped.append(k)
            continue
        if k not in spec["allowed_top_keys"]:
            dropped.append(k)
            continue
        out[k] = v
    if dropped:
        print(f"  [warn] {harness}: dropped invalid keys {dropped}", file=sys.stderr)
    md = render_frontmatter(out) + "\n" + body.lstrip()
    sidecar: str | None = None
    if spec["sidecar"] == "toml":
        name = out.get("name") or Path(CANONICAL_DIR / "unknown").stem
        description = out.get("description", "").replace('"', '\\"')
        prompt = extract_prompt_block(body).replace("'''", "\\'\\'\\'")
        sidecar = (
            f'name = "{name}"\n'
            f'description = "{description}"\n'
            f'sandbox_mode = "workspace-write"\n'
            f"developer_instructions = '''{prompt}'''\n"
        )
    return md, sidecar


def home(p: str) -> Path:
    return Path(os.path.expanduser(p))


def iter_canonical() -> Iterable[Path]:
    if not CANONICAL_DIR.is_dir():
        return []
    return sorted(p for p in CANONICAL_DIR.glob("*.md") if p.is_file())


def sync_one(src: Path, harness: str, dry_run: bool) -> list[str]:
    spec = HARNESSES[harness]
    target_dir = home(spec["config_dir"]) / spec["agents_subdir"]
    target_md = target_dir / src.name
    target_sidecar: Path | None = None
    if spec["sidecar"] == "toml":
        target_sidecar = target_dir / f"{src.stem}.toml"
    text = src.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)
    md_out, sidecar_out = transform_for_harness(fm, body, harness)
    actions: list[str] = []
    if dry_run:
        actions.append(f"DRY {target_md}")
        if target_sidecar:
            actions.append(f"DRY {target_sidecar}")
        return actions
    target_dir.mkdir(parents=True, exist_ok=True)
    md_needs_write = (
        not target_md.exists()
        or target_md.is_symlink()
        or target_md.read_text(encoding="utf-8") != md_out
    )
    if md_needs_write:
        if target_md.is_symlink() or target_md.exists():
            target_md.unlink()
        target_md.write_text(md_out, encoding="utf-8")
        actions.append(f"WROTE  {target_md}")
    else:
        actions.append(f"OK     {target_md}")
    if target_sidecar and sidecar_out is not None:
        sc_needs_write = (
            not target_sidecar.exists()
            or target_sidecar.is_symlink()
            or target_sidecar.read_text(encoding="utf-8") != sidecar_out
        )
        if sc_needs_write:
            if target_sidecar.is_symlink() or target_sidecar.exists():
                target_sidecar.unlink()
            target_sidecar.write_text(sidecar_out, encoding="utf-8")
            actions.append(f"WROTE  {target_sidecar}")
        else:
            actions.append(f"OK     {target_sidecar}")
    return actions


def verify_one(src: Path, harness: str) -> list[str]:
    spec = HARNESSES[harness]
    target_dir = home(spec["config_dir"]) / spec["agents_subdir"]
    target_md = target_dir / src.name
    text = src.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)
    md_out, sidecar_out = transform_for_harness(fm, body, harness)
    drifts: list[str] = []
    if not target_md.exists():
        drifts.append(f"MISSING {target_md}")
    elif target_md.is_symlink():
        drifts.append(f"SYMLINK {target_md} (expected materialized file)")
    elif target_md.read_text(encoding="utf-8") != md_out:
        drifts.append(f"DRIFT {target_md}")
    if spec["sidecar"] == "toml" and sidecar_out is not None:
        sc = target_dir / f"{src.stem}.toml"
        if not sc.exists():
            drifts.append(f"MISSING {sc}")
        elif sc.read_text(encoding="utf-8") != sidecar_out:
            drifts.append(f"DRIFT {sc}")
    return drifts


def main() -> int:
    ap = argparse.ArgumentParser(description="Sync agent frontmatter across AI harnesses.")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--harness", choices=list(HARNESSES))
    args = ap.parse_args()

    if not CANONICAL_DIR.is_dir():
        print(f"canonical dir not found: {CANONICAL_DIR}", file=sys.stderr)
        return 2

    harnesses = [args.harness] if args.harness else list(HARNESSES)
    canonicals = list(iter_canonical())
    if not canonicals:
        print(f"no canonical agents in {CANONICAL_DIR}", file=sys.stderr)
        return 2

    print(f"canonical: {len(canonicals)} agent(s) in {CANONICAL_DIR}")
    print(f"target:    {', '.join(harnesses)}")

    all_drifts: list[str] = []
    for h in harnesses:
        print(f"\n[{h}]")
        for src in canonicals:
            if args.verify:
                drifts = verify_one(src, h)
                if drifts:
                    for d in drifts:
                        print(f"  ✗ {d}")
                        all_drifts.append(d)
                else:
                    print(f"  ✓ {src.name}")
            else:
                actions = sync_one(src, h, args.dry_run)
                for a in actions:
                    print(f"  {a}")

    if args.verify:
        if all_drifts:
            print(f"\nFAILED: {len(all_drifts)} drift(s) detected.", file=sys.stderr)
            return 1
        print("\nOK: all harnesses in sync with canonical.")
        return 0
    print("\nDONE." if not args.dry_run else "\nDRY-RUN: no changes written.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
