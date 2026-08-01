#!/usr/bin/env python3
"""normalize_plugins.py — Bring every plugin to the canonical cross-harness layout.

Companion to scripts/validate_plugins.py: the validator states the contract,
this script repairs violations of it. Run normalize -> validate -> update
marketplace.

Canonical layout (see validate_plugins.py for the full rationale):

    plugins/<name>/
    |-- plugin.json              marketplace metadata (Claude Code)
    |-- SKILL.md                 root skill, discovered by every harness
    `-- skills/<sub>/SKILL.md    sub-skills, one directory per skill

Repairs performed
-----------------
FLAT_SKILL_FILE       skills/<n>.md            -> skills/<n>/SKILL.md
NO_ROOT_SKILL         promote the sole sub-skill to the plugin root SKILL.md
                      (or synthesize an index that points at the sub-skills)
NO_PLUGIN_JSON        generate plugin.json from the root SKILL.md frontmatter
SKILL_NAME_MISMATCH   rewrite frontmatter `name` to match the directory
SKILL_NAME_NOT_SLUG   slugify frontmatter `name`
SKILL_NO_FRONTMATTER  synthesize frontmatter from the first H1 + first prose
                      paragraph

This also subsumes the previous behaviour of this script: every plugin.json
gets the standard author block, an MIT license and the base keywords.

Every repair is idempotent: running twice changes nothing the second time.

Usage
-----
    normalize_plugins.py --dry-run     preview every change, write nothing
    normalize_plugins.py               apply
    normalize_plugins.py --plugin X    restrict to one plugin
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGINS_DIR = REPO_ROOT / "plugins"

EXCLUDED = {".system"}

AUTHOR = {"name": "Anderson Lima", "url": "https://andersonlimahw.github.io"}
DEFAULT_VERSION = "1.0.0"
DEFAULT_LICENSE = "MIT"
BASE_KEYWORDS = ["skill", "lemon-ai-hub"]

SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


class Changes:
    def __init__(self, dry_run: bool) -> None:
        self.dry_run = dry_run
        self.entries: list[str] = []

    def record(self, message: str) -> None:
        self.entries.append(message)
        prefix = "[dry-run]" if self.dry_run else "[apply]  "
        print(f"{prefix} {message}")


def slugify(value: str) -> str:
    value = value.strip().strip("\"'")
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return re.sub(r"-{2,}", "-", value)


def split_frontmatter(text: str) -> tuple[str | None, str]:
    """Return (frontmatter_block, body). frontmatter_block excludes the fences."""
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end < 0:
        return None, text
    block = text[4:end]
    body = text[end + 4 :]
    if body.startswith("\n"):
        body = body[1:]
    return block, body


def parse_frontmatter(block: str) -> dict[str, str]:
    data: dict[str, str] = {}
    key: str | None = None
    for line in block.split("\n"):
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            key = match.group(1)
            data[key] = match.group(2).strip()
        elif key and line.strip():
            data[key] = f"{data[key]} {line.strip()}".strip()
    return data


def yaml_quote(value: str) -> str:
    """Emit a double-quoted YAML scalar, escaping embedded quotes."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def render_frontmatter(data: dict[str, str], original_block: str | None) -> str:
    """Rewrite `name` and `description`, preserving any other original lines."""
    lines = [
        f"name: {yaml_quote(data['name'])}",
        f"description: {yaml_quote(data['description'])}",
    ]
    if original_block:
        # Carry over keys we do not manage (license, metadata, allowed-tools...).
        managed = {"name", "description"}
        keep: list[str] = []
        current_key: str | None = None
        for line in original_block.split("\n"):
            match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
            if match:
                current_key = match.group(1)
                if current_key not in managed:
                    keep.append(line)
            elif current_key and current_key not in managed and line.strip():
                keep.append(line)
        lines.extend(keep)
    return "---\n" + "\n".join(lines) + "\n---\n"


def derive_from_body(body: str, fallback_name: str) -> tuple[str, str]:
    """Infer (name, description) for a SKILL.md that has no frontmatter."""
    heading = ""
    paragraph: list[str] = []
    for line in body.split("\n"):
        stripped = line.strip()
        if not heading and stripped.startswith("# "):
            heading = stripped[2:].strip()
            continue
        if heading:
            if not stripped:
                if paragraph:
                    break
                continue
            if stripped.startswith("#"):
                break
            paragraph.append(re.sub(r"[*_`]", "", stripped))
    name = slugify(heading) or fallback_name
    if not SLUG_RE.match(name):
        name = fallback_name
    description = " ".join(paragraph).strip()
    if not description:
        description = f"{heading or fallback_name} skill."
    return name, description


def write(path: Path, content: str, changes: Changes) -> None:
    if not changes.dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def git_mv(src: Path, dst: Path, changes: Changes) -> None:
    """Move a tracked file, preferring `git mv` so history follows the rename."""
    if changes.dry_run:
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["git", "mv", str(src.relative_to(REPO_ROOT)), str(dst.relative_to(REPO_ROOT))],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        # Untracked file (git mv refuses); a plain move is correct there.
        shutil.move(str(src), str(dst))


# ---------------------------------------------------------------------------
# Repairs
# ---------------------------------------------------------------------------


def fix_flat_skills(plugin_dir: Path, changes: Changes) -> dict[str, Path]:
    """skills/<n>.md -> skills/<n>/SKILL.md (no harness discovers the flat form).

    Returns the sub-skills this call materialized, keyed by sub-skill name. In
    dry-run the move does not happen, so later steps would wrongly conclude the
    plugin has no sub-skill to promote; the returned map lets them see it.
    """
    materialized: dict[str, Path] = {}
    skills_dir = plugin_dir / "skills"
    if not skills_dir.is_dir():
        return materialized
    for entry in sorted(skills_dir.iterdir()):
        if not entry.is_file() or entry.suffix != ".md" or entry.name == "SKILL.md":
            continue
        target = skills_dir / entry.stem / "SKILL.md"
        if target.exists():
            continue
        changes.record(
            f"{plugin_dir.name}: skills/{entry.name} -> skills/{entry.stem}/SKILL.md"
        )
        # Record the source path: in dry-run it is where the content still lives.
        materialized[entry.stem] = entry if changes.dry_run else target
        git_mv(entry, target, changes)
    return materialized


def fix_skill_frontmatter(
    skill_path: Path, expected_name: str, plugin: str, changes: Changes
) -> None:
    """Force frontmatter `name` to the slug of its containing directory."""
    text = skill_path.read_text(encoding="utf-8")
    block, body = split_frontmatter(text)

    if block is None:
        _, description = derive_from_body(body, expected_name)
        changes.record(
            f"{plugin}: {skill_path.relative_to(REPO_ROOT)} synthesized frontmatter "
            f"(name={expected_name})"
        )
        content = render_frontmatter(
            {"name": expected_name, "description": description}, None
        )
        write(skill_path, content + body, changes)
        return

    data = parse_frontmatter(block)
    current_name = data.get("name", "").strip().strip("\"'")
    description = data.get("description", "").strip().strip("\"'")

    needs_name_fix = current_name != expected_name
    needs_desc_fix = not description
    if not (needs_name_fix or needs_desc_fix):
        return

    if needs_desc_fix:
        _, description = derive_from_body(body, expected_name)
        changes.record(
            f"{plugin}: {skill_path.relative_to(REPO_ROOT)} description synthesized"
        )
    if needs_name_fix:
        changes.record(
            f"{plugin}: {skill_path.relative_to(REPO_ROOT)} name "
            f'"{current_name}" -> "{expected_name}"'
        )

    new_block = render_frontmatter(
        {"name": expected_name, "description": description}, block
    )
    write(skill_path, new_block + body, changes)


def ensure_root_skill(
    plugin_dir: Path, changes: Changes, materialized: dict[str, Path] | None = None
) -> None:
    """Guarantee plugins/<name>/SKILL.md exists — the cross-harness entry point."""
    root_skill = plugin_dir / "SKILL.md"
    if root_skill.exists():
        return

    plugin = plugin_dir.name
    skills_dir = plugin_dir / "skills"

    # name -> path of the SKILL.md holding the content right now.
    sources: dict[str, Path] = dict(materialized or {})
    if skills_dir.is_dir():
        for entry in sorted(skills_dir.iterdir()):
            if entry.is_dir() and (entry / "SKILL.md").exists():
                sources.setdefault(entry.name, entry / "SKILL.md")
    sub_skills = sorted(sources.items())

    if not sub_skills:
        changes.record(
            f"{plugin}: SKIPPED — no root SKILL.md and no sub-skills to derive one from"
        )
        return

    if len(sub_skills) == 1:
        # A single sub-skill is the plugin. Promote it so non-Claude harnesses
        # see it, and leave the sub-skill in place for Claude Code namespacing.
        sub_name, source = sub_skills[0]
        block, body = split_frontmatter(source.read_text(encoding="utf-8"))
        data = parse_frontmatter(block) if block else {}
        description = data.get("description", "").strip().strip("\"'")
        if not description:
            _, description = derive_from_body(body, plugin)
        changes.record(f"{plugin}: promoted skills/{sub_name}/SKILL.md -> SKILL.md")
        content = render_frontmatter({"name": plugin, "description": description}, block)
        write(root_skill, content + body, changes)
        return

    # Several sub-skills: the root becomes an index that routes to them.
    entries = []
    for sub_name, source in sub_skills:
        block, body = split_frontmatter(source.read_text(encoding="utf-8"))
        data = parse_frontmatter(block) if block else {}
        desc = data.get("description", "").strip().strip("\"'")
        if not desc:
            _, desc = derive_from_body(body, sub_name)
        entries.append((sub_name, desc))

    description = (
        f"{plugin} plugin. Routes to its sub-skills: "
        + ", ".join(name for name, _ in entries)
        + ". Use when the task matches any of the capabilities listed below."
    )
    lines = [
        f"# {plugin}",
        "",
        f"Entry point for the `{plugin}` plugin. Pick the sub-skill that matches the task.",
        "",
        "## Sub-skills",
        "",
    ]
    for name, desc in entries:
        lines.append(f"- **`{name}`** (`skills/{name}/SKILL.md`) — {desc}")
    lines.append("")
    changes.record(f"{plugin}: generated index SKILL.md for {len(entries)} sub-skills")
    content = render_frontmatter({"name": plugin, "description": description}, None)
    write(root_skill, content + "\n".join(lines), changes)


def ensure_plugin_json(plugin_dir: Path, changes: Changes) -> None:
    """Generate or repair plugin.json from the root SKILL.md frontmatter."""
    plugin = plugin_dir.name
    plugin_json = plugin_dir / "plugin.json"
    root_skill = plugin_dir / "SKILL.md"

    description = ""
    if root_skill.exists():
        block, body = split_frontmatter(root_skill.read_text(encoding="utf-8"))
        data = parse_frontmatter(block) if block else {}
        description = data.get("description", "").strip().strip("\"'")
        if not description:
            _, description = derive_from_body(body, plugin)

    if plugin_json.exists():
        try:
            existing = json.loads(plugin_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            changes.record(f"{plugin}: plugin.json is invalid JSON — regenerating")
            existing = {}
    else:
        existing = None

    data = dict(existing or {})
    before = json.dumps(data, sort_keys=True)

    data["name"] = plugin
    data.setdefault("version", DEFAULT_VERSION)
    if not data.get("description"):
        data["description"] = description
    data["author"] = AUTHOR
    data["license"] = DEFAULT_LICENSE
    keywords = data.get("keywords") or []
    for keyword in reversed(BASE_KEYWORDS):
        if keyword not in keywords:
            keywords.insert(0, keyword)
    if plugin not in keywords:
        keywords.append(plugin)
    data["keywords"] = keywords

    # Stable key order keeps diffs readable across runs.
    ordered = {
        "name": data["name"],
        "version": data["version"],
        "description": data["description"],
        "author": data["author"],
        "license": data["license"],
        "keywords": data["keywords"],
    }
    for key, value in data.items():
        if key not in ordered:
            ordered[key] = value

    if existing is None:
        changes.record(f"{plugin}: created plugin.json")
    elif json.dumps(ordered, sort_keys=True) != before:
        changes.record(f"{plugin}: updated plugin.json")
    else:
        return

    write(plugin_json, json.dumps(ordered, indent=2, ensure_ascii=False) + "\n", changes)


def normalize_plugin(plugin_dir: Path, changes: Changes) -> None:
    plugin = plugin_dir.name

    # Order matters: flat files become sub-skills, a root skill is derived from
    # the sub-skills, frontmatter is repaired, then plugin.json reads the
    # repaired root frontmatter.
    materialized = fix_flat_skills(plugin_dir, changes)
    ensure_root_skill(plugin_dir, changes, materialized)

    root_skill = plugin_dir / "SKILL.md"
    if root_skill.exists():
        fix_skill_frontmatter(root_skill, plugin, plugin, changes)

    skills_dir = plugin_dir / "skills"
    if skills_dir.is_dir():
        for sub in sorted(skills_dir.iterdir()):
            if sub.is_dir() and (sub / "SKILL.md").exists():
                fix_skill_frontmatter(sub / "SKILL.md", slugify(sub.name), plugin, changes)

    ensure_plugin_json(plugin_dir, changes)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--dry-run", action="store_true", help="preview changes, write nothing")
    parser.add_argument("--plugin", help="restrict normalization to a single plugin")
    args = parser.parse_args()

    plugin_dirs = sorted(
        d
        for d in PLUGINS_DIR.iterdir()
        if d.is_dir() and d.name not in EXCLUDED and not d.name.startswith(".")
    )
    if args.plugin:
        plugin_dirs = [d for d in plugin_dirs if d.name == args.plugin]
        if not plugin_dirs:
            print(f"No such plugin: {args.plugin}", file=sys.stderr)
            return 2

    changes = Changes(args.dry_run)
    for plugin_dir in plugin_dirs:
        normalize_plugin(plugin_dir, changes)

    print(f"\n{len(plugin_dirs)} plugins processed — {len(changes.entries)} changes")
    if args.dry_run:
        print("Dry run: nothing written. Re-run without --dry-run to apply.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
