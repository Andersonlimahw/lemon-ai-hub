#!/usr/bin/env python3
"""wtj.py — Worktree Janitor.

Discovers every git worktree left behind by AI coding agents (Claude Code,
Codex, Gemini CLI, Agy/Antigravity, OpenCode, Cursor, ...), classifies each one
by removal risk, removes only what the human approved, and renders a
self-contained HTML report with an undo script.

Subcommands
-----------
    wtj.py scan   [--json] [--report]          discover + classify (never mutates)
    wtj.py clean  --scan <scan.json> --select  remove approved worktrees
    wtj.py report --result <result.json>       (re)render the HTML report

Safety invariants
-----------------
1. The main worktree of a repository is NEVER removed.
2. The worktree the current shell runs from is NEVER removed.
3. Locked worktrees are NEVER removed.
4. Worktrees with uncommitted changes are classified `risky` and excluded from
   the default selection; they require an explicit `--include-dirty` scan.
5. `clean` only ever touches ids that were explicitly passed in `--select`.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import webbrowser
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_html import REASON_LABELS, human_bytes, render_report  # noqa: E402

VERSION = "1.0.0"

# Directories that never contain a repository we care about, and that are
# expensive to walk. Mirrors the hub-wide "never touch build artifacts" rule.
SKIP_DIRS = {
    "node_modules", ".venv", "venv", "dist", "build", "target", "Pods",
    ".gradle", "vendor", "__pycache__", ".next", "Library", ".Trash",
    ".cache", "DerivedData", ".npm", ".pnpm-store", ".terraform", "site-packages",
}

# Path segment -> harness that owns worktrees under it.
HARNESS_BY_SEGMENT = {
    ".claude": "Claude Code",
    ".codex": "Codex",
    ".agy": "Agy",
    ".antigravity": "Antigravity",
    ".gemini": "Gemini CLI",
    ".opencode": "OpenCode",
    ".cursor": "Cursor",
    ".aider": "Aider",
    ".windsurf": "Windsurf",
    ".continue": "Continue",
}

DEFAULT_BASES = ("main", "master", "develop", "trunk")
DEFAULT_ROOTS = ("~/Projects",)
DEFAULT_DEPTH = 5
DEFAULT_STALE_DAYS = 14
CONFIG_PATH = Path("~/.worktree-janitor.json").expanduser()
OUTPUT_ROOT = Path("~/.worktree-janitor/reports").expanduser()

RISK_ORDER = {"safe": 0, "review": 1, "risky": 2, "keep": 3, "protected": 4}

# Reasons that mean "this branch is reproducible from the base", and are
# therefore the only ones where `--delete-branch auto` removes the local branch.
BRANCH_DELETABLE_REASONS = ("merged", "upstream-gone", "no-unique-commits")


# --------------------------------------------------------------------------- #
# process helpers
# --------------------------------------------------------------------------- #

def run(cmd: list[str], cwd: str | None = None, timeout: int = 60) -> tuple[int, str, str]:
    """Run a command without a shell. Returns (returncode, stdout, stderr)."""
    try:
        proc = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return 124, "", f"timeout after {timeout}s: {' '.join(cmd)}"
    except OSError as exc:
        return 127, "", str(exc)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def git(args: list[str], cwd: str | None = None, timeout: int = 60) -> tuple[int, str, str]:
    return run(["git", *args], cwd=cwd, timeout=timeout)


def log(msg: str) -> None:
    print(msg, file=sys.stderr)


# --------------------------------------------------------------------------- #
# discovery
# --------------------------------------------------------------------------- #

def find_repos(roots: list[str], depth: int) -> list[Path]:
    """Find main git checkouts under `roots`, bounded by `depth` levels.

    Only directories holding a `.git` *directory* are main checkouts; a linked
    worktree holds a `.git` *file*, and is enumerated via its parent repo.
    Descent stops at a repository root so nested worktrees are not double
    counted.
    """
    repos: list[Path] = []
    seen: set[Path] = set()
    for raw_root in roots:
        root = Path(raw_root).expanduser()
        if not root.is_dir():
            continue
        base_depth = len(root.resolve().parts)
        for dirpath, dirnames, _ in os.walk(root.resolve(), followlinks=False):
            current = Path(dirpath)
            if len(current.parts) - base_depth >= depth:
                dirnames[:] = []
                continue
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            if (current / ".git").is_dir():
                resolved = current.resolve()
                if resolved not in seen:
                    seen.add(resolved)
                    repos.append(resolved)
                dirnames[:] = []
    return sorted(repos)


def list_worktrees(repo: Path) -> list[dict]:
    """Parse `git worktree list --porcelain` into one dict per worktree."""
    code, out, _ = git(["worktree", "list", "--porcelain"], cwd=str(repo))
    if code != 0:
        return []
    blocks: list[dict] = []
    current: dict = {}
    for line in out.splitlines():
        if not line.strip():
            if current:
                blocks.append(current)
                current = {}
            continue
        key, _, value = line.partition(" ")
        current[key] = value
    if current:
        blocks.append(current)
    return blocks


def resolve_base(repo: Path) -> tuple[str, str | None]:
    """Return (base_branch_name, comparable_ref) for the repository.

    The ref is None when no real base could be found. Comparing against `HEAD`
    as a fallback would mean "merged into whatever the main checkout happens to
    be parked on" — routinely a feature branch — so callers must treat an
    unresolved base as "cannot classify" rather than guessing.
    """
    code, out, _ = git(["symbolic-ref", "--quiet", "refs/remotes/origin/HEAD"], cwd=str(repo))
    if code == 0 and out.startswith("refs/remotes/origin/"):
        name = out[len("refs/remotes/origin/"):]
        return name, f"origin/{name}"
    for name in DEFAULT_BASES:
        if git(["rev-parse", "--verify", "--quiet", f"refs/remotes/origin/{name}"], cwd=str(repo))[0] == 0:
            return name, f"origin/{name}"
        if git(["rev-parse", "--verify", "--quiet", f"refs/heads/{name}"], cwd=str(repo))[0] == 0:
            return name, name
    return "(indeterminada)", None


def detect_harness(path: str) -> tuple[str | None, bool]:
    """Infer which AI harness owns a worktree path.

    Returns (harness_name_or_None, is_agent_managed).
    """
    parts = Path(path).parts
    for segment in parts:
        if segment in HARNESS_BY_SEGMENT:
            return HARNESS_BY_SEGMENT[segment], True
    if "worktrees" in parts or ".worktrees" in parts:
        return None, True
    return None, False


def dir_size_bytes(path: str) -> int:
    """Best-effort size. Cosmetic only — 0 on failure, never blocks a decision."""
    _, out, _ = run(["du", "-sk", path], timeout=120)
    match = re.match(r"^(\d+)", out)
    return int(match.group(1)) * 1024 if match else 0


def current_worktree() -> str | None:
    code, out, _ = git(["rev-parse", "--show-toplevel"])
    if code == 0 and out:
        return str(Path(out).resolve())
    return None


# --------------------------------------------------------------------------- #
# classification
# --------------------------------------------------------------------------- #

def expand_patterns(patterns: list[str]) -> list[str]:
    """`~` in a --protect glob must expand, or the pattern silently matches
    nothing — the failure mode is "protection did not apply", so it fails open."""
    return [os.path.expanduser(p) for p in patterns]


def matches_protect(path: str, patterns: list[str]) -> bool:
    """Match a glob against both the literal and the resolved path.

    `/tmp` vs `/private/tmp`, autofs and symlinked home dirs mean the porcelain
    path and the path the user typed the glob against may differ.
    """
    candidates = {path}
    try:
        candidates.add(str(Path(path).resolve()))
    except OSError:
        pass
    return any(fnmatch.fnmatch(c, p) for c in candidates for p in patterns)


def gather_facts(repo: Path, block: dict, base_name: str, base_ref: str | None, is_main: bool) -> dict:
    """Everything the classifier needs, read from disk and git. No policy here.

    Numbers that could not be measured stay `None` — never `0`. A git failure
    must not be indistinguishable from "this branch has no unique commits".
    """
    path = block.get("worktree", "")
    head = block.get("HEAD", "")
    branch_ref = block.get("branch", "")
    # Keep the full branch name: `refs/heads/feat/x` -> `feat/x`, not `x`.
    branch = branch_ref[len("refs/heads/"):] if branch_ref.startswith("refs/heads/") else (branch_ref or None)

    facts: dict = {
        "repoPath": str(repo),
        "repoName": repo.name,
        "path": path,
        "exists": bool(path) and Path(path).exists(),
        "branch": branch,
        "head": head,
        "baseBranch": base_name,
        "isMain": is_main,
        "locked": "locked" in block,
        "lockedReason": block.get("locked") or None,
        "prunable": "prunable" in block,
        "prunableReason": block.get("prunable") or None,
        "dirtyFiles": None,
        "ahead": None,
        "behind": None,
        "merged": None,
        "upstream": None,
        "upstreamGone": False,
        "lastCommit": None,
        "ageDays": None,
        "sizeBytes": 0,
    }
    facts["harness"], facts["agentManaged"] = detect_harness(path)

    # Protected and dead worktrees are classified from the porcelain block
    # alone; touching the filesystem for them is wasted work.
    if is_main or facts["locked"] or facts["prunable"] or not facts["exists"]:
        return facts

    facts["sizeBytes"] = dir_size_bytes(path)

    code, out, _ = git(["status", "--porcelain", "--untracked-files=normal"], cwd=path)
    if code == 0:
        facts["dirtyFiles"] = len(out.splitlines()) if out else 0

    code, out, _ = git(["log", "-1", "--format=%cI"], cwd=path)
    if code == 0 and out:
        facts["lastCommit"] = out
        try:
            facts["ageDays"] = (datetime.now(timezone.utc) - datetime.fromisoformat(out)).days
        except ValueError:
            pass

    if head and base_ref:
        code, _, _ = git(["merge-base", "--is-ancestor", head, base_ref], cwd=str(repo))
        if code in (0, 1):  # 1 = definitively not an ancestor; anything else = error
            facts["merged"] = code == 0
        code, out, _ = git(["rev-list", "--left-right", "--count", f"{base_ref}...{head}"], cwd=str(repo))
        numbers = out.split() if code == 0 else []
        if len(numbers) == 2:
            facts["behind"], facts["ahead"] = int(numbers[0]), int(numbers[1])

    if branch:
        # `|` is a legal refname character, so it cannot be the separator.
        # A newline is not legal in a refname, so `%0a` is unambiguous.
        code, out, _ = git(
            ["for-each-ref", "--format=%(upstream:short)%0a%(upstream:track)", f"refs/heads/{branch}"],
            cwd=str(repo),
        )
        lines = out.split("\n") if code == 0 else []
        if len(lines) == 2:
            facts["upstream"] = lines[0] or None
            facts["upstreamGone"] = bool(lines[0]) and lines[1].strip() == "[gone]"

    return facts


def classify(facts: dict, stale_days: int, include_dirty: bool,
             protect_patterns: list[str], here: str | None) -> dict:
    """Pure policy: facts in, (reason, risk, recommended, signals) out.

    Evaluation is sequential and stops at the first match. The order is the
    contract documented in references/criteria.md — safety before convenience.
    """
    path = facts["path"]
    signals: list[str] = []

    def verdict(reason: str, risk: str) -> dict:
        return {**facts, "reason": reason, "risk": risk, "signals": signals,
                "recommended": risk == "safe"}

    if facts["isMain"]:
        return verdict("main-worktree", "protected")
    if here and path:
        try:
            if str(Path(path).resolve()) == here:
                return verdict("current-session", "protected")
        except OSError:
            pass
    if matches_protect(path, protect_patterns):
        return verdict("protected", "protected")
    if facts["locked"]:
        return verdict("locked", "protected")
    if facts["prunable"]:
        signals.append("prunable")
        return verdict("prunable", "safe")
    if not facts["exists"]:
        # Directory is gone but git has not noticed. Could be an unmounted
        # volume rather than a dead worktree — never auto-recommend.
        return verdict("missing", "review")

    dirty = bool(facts["dirtyFiles"])
    if dirty:
        signals.append("dirty")
    if dirty and not include_dirty:
        return verdict("dirty", "risky")

    if facts["merged"]:
        signals.append("merged")
        reason, risk = "merged", "safe"
    elif facts["upstreamGone"]:
        signals.append("upstream-gone")
        reason, risk = "upstream-gone", "safe"
    elif facts["ahead"] is None or facts["merged"] is None:
        # git could not answer. Never let a measurement failure read as
        # "nothing unique here" and green-light a deletion.
        reason, risk = "unknown", "review"
    elif not facts["branch"] and facts["ahead"] == 0:
        reason, risk = "orphan-detached", "safe"
    elif facts["ahead"] == 0:
        reason, risk = "no-unique-commits", "safe"
    elif facts["ageDays"] is not None and facts["ageDays"] >= stale_days:
        reason, risk = "stale", "review"
    else:
        return verdict("active", "keep")

    # Uncommitted work is unrecoverable: never auto-recommend it.
    if dirty and risk == "safe":
        risk = "review"
    return verdict(reason, risk)


def build_scan(
    roots: list[str],
    depth: int,
    stale_days: int,
    include_dirty: bool,
    protect_patterns: list[str],
    quiet: bool = False,
) -> dict:
    here = current_worktree()
    protect_patterns = expand_patterns(protect_patterns)
    repos = find_repos(roots, depth)
    if not quiet:
        log(f"[wtj] {len(repos)} repositório(s) encontrado(s) em {', '.join(roots)}")

    items: list[dict] = []
    for repo in repos:
        blocks = list_worktrees(repo)
        if len(blocks) <= 1:
            continue
        base_name, base_ref = resolve_base(repo)
        for index, block in enumerate(blocks):
            if "bare" in block:
                continue
            facts = gather_facts(repo, block, base_name, base_ref, index == 0)
            items.append(classify(facts, stale_days, include_dirty, protect_patterns, here))

    # A --protect glob that matches nothing is almost always a typo, and its
    # failure mode is silent: the user believes a path is protected when it is not.
    for pattern in protect_patterns:
        if not any(matches_protect(i["path"], [pattern]) for i in items):
            log(f"[wtj] AVISO: o glob --protect {pattern!r} não casou com nenhuma worktree")

    items.sort(key=lambda i: (RISK_ORDER.get(i["risk"], 9), i["repoName"], i["path"]))
    for new_id, item in enumerate(items, start=1):
        item["id"] = new_id

    return {
        "version": VERSION,
        "mode": "preview",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "roots": roots,
        "depth": depth,
        "staleDays": stale_days,
        "includeDirty": include_dirty,
        "protect": protect_patterns,
        "reposScanned": len(repos),
        "items": items,
        "summary": summarize(items),
    }


def summarize(items: list[dict]) -> dict:
    by_risk: dict[str, int] = {}
    by_reason: dict[str, int] = {}
    by_repo: dict[str, dict] = {}
    by_harness: dict[str, int] = {}
    reclaimable = 0
    for item in items:
        by_risk[item["risk"]] = by_risk.get(item["risk"], 0) + 1
        by_reason[item["reason"]] = by_reason.get(item["reason"], 0) + 1
        harness = item.get("harness") or ("agente (genérico)" if item.get("agentManaged") else "humano")
        by_harness[harness] = by_harness.get(harness, 0) + 1
        bucket = by_repo.setdefault(item["repoName"], {"repoPath": item["repoPath"], "total": 0, "candidates": 0, "bytes": 0})
        bucket["total"] += 1
        if item["risk"] in ("safe", "review"):
            bucket["candidates"] += 1
            bucket["bytes"] += item.get("sizeBytes", 0)
        if item["risk"] == "safe":
            reclaimable += item.get("sizeBytes", 0)
    return {
        "total": len(items),
        "byRisk": by_risk,
        "byReason": by_reason,
        "byRepo": by_repo,
        "byHarness": by_harness,
        "reclaimableBytes": reclaimable,
        "candidates": by_risk.get("safe", 0) + by_risk.get("review", 0),
    }


# --------------------------------------------------------------------------- #
# cleaning
# --------------------------------------------------------------------------- #

def should_delete_branch(item: dict, policy: str) -> bool:
    if policy == "never" or not item.get("branch"):
        return False
    if policy == "always":
        return True
    if item["reason"] not in BRANCH_DELETABLE_REASONS:
        return False
    # `upstream-gone` catches squash-merges, but it is not proof of a merge: a
    # remote branch deleted without merging leaves commits that exist only here.
    # Keep the ref — the worktree still goes, and the commits stay reachable.
    if item["reason"] == "upstream-gone" and not item.get("merged") and (item.get("ahead") or 0) > 0:
        return False
    return True


def prune_one(repo: str, path: str) -> tuple[bool, str]:
    """Drop the administrative record of one dead worktree.

    `git worktree prune` is repo-wide: it would remove every prunable worktree
    in the repository, including ids the user did not select, and the report
    would then claim nothing outside the selection was touched. So the entry is
    located by its own `gitdir` file and removed on its own.
    """
    code, common, err = git(["rev-parse", "--path-format=absolute", "--git-common-dir"], cwd=repo)
    if code != 0:
        return False, err or "não foi possível localizar o git dir"
    admin_root = Path(common) / "worktrees"
    if not admin_root.is_dir():
        return False, "repositório não possui registros de worktree"

    target = str(Path(path))
    for entry in sorted(admin_root.iterdir()):
        gitdir_file = entry / "gitdir"
        try:
            recorded = gitdir_file.read_text(encoding="utf-8", errors="replace").strip()
        except OSError:
            continue
        # `gitdir` holds `<worktree>/.git`; older git wrote the worktree itself.
        if recorded == target or str(Path(recorded).parent) == target:
            try:
                shutil.rmtree(entry)
            except OSError as exc:
                return False, str(exc)
            return True, ""
    return False, f"nenhum registro administrativo aponta para {path}"


def revalidate(item: dict, here: str | None, protect_patterns: list[str]) -> str | None:
    """Re-check the safety invariants against live state, not against the scan.

    `scan` and `clean` are separate invocations; minutes and several agent turns
    can pass between them. Returns an error string when the classification no
    longer holds, or None when it is still safe to proceed.
    """
    path = item.get("path") or ""
    repo = item.get("repoPath") or ""

    if here and path:
        try:
            if str(Path(path).resolve()) == here:
                return "scan desatualizado: esta é a worktree da sessão atual"
        except OSError:
            pass
    if matches_protect(path, protect_patterns):
        return "protegida por --protect"

    for block in list_worktrees(Path(repo)):
        if block.get("worktree") != path:
            continue
        if "locked" in block:
            return "scan desatualizado: a worktree foi travada (git worktree lock)"
        if "prunable" in block:
            return None
        code, out, _ = git(["status", "--porcelain", "--untracked-files=normal"], cwd=path)
        if code == 0 and out and not item.get("dirtyFiles"):
            return (f"scan desatualizado: a worktree passou a ter {len(out.splitlines())} "
                    "alteração(ões) não commitada(s)")
        return None
    return "scan desatualizado: a worktree não está mais registrada no repositório"


def clean(scan_data: dict, selected_ids: list[int], branch_policy: str, force: bool) -> dict:
    by_id = {item["id"]: item for item in scan_data["items"]}
    protect_patterns = expand_patterns(scan_data.get("protect", []))
    here = current_worktree()
    results: list[dict] = []

    def record(item: dict | None, item_id: int, **fields) -> None:
        base = {k: item.get(k) for k in
                ("repoPath", "repoName", "path", "branch", "head", "risk", "reason", "sizeBytes")} if item else {}
        results.append({"id": item_id, **base, "undo": [], **fields})

    for item_id in selected_ids:
        item = by_id.get(item_id)
        if item is None:
            record(None, item_id, status="skipped", error="id inexistente no scan")
            continue
        if item["risk"] == "protected":
            record(item, item_id, status="skipped",
                   error=f"protegida ({REASON_LABELS.get(item['reason'], item['reason'])})")
            continue

        repo, path = item["repoPath"], item["path"]
        stale = revalidate(item, here, protect_patterns)
        if stale:
            record(item, item_id, status="skipped", error=stale)
            continue

        if item["prunable"] or not item["exists"]:
            ok, err = prune_one(repo, path)
            record(item, item_id, status="removed" if ok else "failed",
                   action="prune", error=None if ok else err)
            continue

        if item.get("dirtyFiles") and not force:
            record(item, item_id, status="skipped",
                   error="worktree com alterações não commitadas exige --force")
            continue

        args = ["worktree", "remove", path]
        if force:
            args.append("--force")
        code, _, err = git(args, cwd=repo)
        if code != 0:
            record(item, item_id, status="failed", action="remove",
                   error=err or "git worktree remove falhou")
            continue

        branch_deleted, branch_error, undo = False, None, []
        if should_delete_branch(item, branch_policy):
            bcode, _, berr = git(["branch", "-D", item["branch"]], cwd=repo)
            branch_deleted = bcode == 0
            branch_error = None if branch_deleted else berr
        if branch_deleted:
            undo.append(f"git -C {shlex.quote(repo)} branch {shlex.quote(item['branch'])} {item['head']}")
        undo.append(f"git -C {shlex.quote(repo)} worktree add {shlex.quote(path)} "
                    f"{shlex.quote(item['branch'] or item['head'])}")

        record(item, item_id, status="removed", action="remove", error=None,
               branchDeleted=branch_deleted, branchError=branch_error, undo=undo)

    removed = [r for r in results if r.get("status") == "removed"]
    return {
        "version": VERSION,
        "mode": "executed",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "roots": scan_data.get("roots", []),
        "staleDays": scan_data.get("staleDays"),
        "reposScanned": scan_data.get("reposScanned", 0),
        "branchPolicy": branch_policy,
        "selectedIds": selected_ids,
        "items": scan_data["items"],
        "results": results,
        "reclaimedBytes": sum(r.get("sizeBytes", 0) for r in removed),
        "removedCount": len(removed),
        "failedCount": len([r for r in results if r.get("status") == "failed"]),
        "skippedCount": len([r for r in results if r.get("status") == "skipped"]),
        "summary": scan_data.get("summary", {}),
    }


def shq(value: str) -> str:
    """Quote a value for safe paste into a POSIX shell."""
    return "'" + str(value).replace("'", "'\\''") + "'"


def write_undo_script(result: dict, path: Path) -> None:
    lines = [
        "#!/usr/bin/env bash",
        "# Worktree Janitor — undo script",
        f"# Gerado em {result['generatedAt']}",
        "#",
        "# ATENÇÃO: restaura branches e worktrees removidas, mas NÃO restaura",
        "# alterações não commitadas que existiam dentro da worktree.",
        "set -euo pipefail",
        "",
    ]
    commands = [cmd for r in result["results"] for cmd in (r.get("undo") or [])]
    if commands:
        lines.extend(commands)
    else:
        lines.append("echo 'Nada a desfazer.'")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    path.chmod(0o755)


# --------------------------------------------------------------------------- #
# output
# --------------------------------------------------------------------------- #

def print_table(scan_data: dict) -> None:
    items = scan_data["items"]
    if not items:
        print("Nenhuma worktree encontrada.")
        return
    buckets: dict[str, list[dict]] = {}
    for item in items:
        buckets.setdefault(item["repoName"], []).append(item)
    for repo_name in sorted(buckets):
        print(f"\n▌ {repo_name}  ({buckets[repo_name][0]['repoPath']})")
        for item in buckets[repo_name]:
            marker = {"safe": "✔", "review": "?", "risky": "!", "keep": "·", "protected": "🔒"}[item["risk"]]
            branch = item["branch"] or "(detached)"
            size = human_bytes(item["sizeBytes"]) if item["sizeBytes"] else "-"
            print(f"  [{item['id']:>3}] {marker} {item['risk']:<9} {branch:<38} {size:>9}  {REASON_LABELS.get(item['reason'], item['reason'])}")
            print(f"        {item['path']}")
    summary = scan_data["summary"]
    print(
        f"\nTotal: {summary['total']} worktrees · candidatas: {summary['candidates']} · "
        f"espaço recuperável (safe): {human_bytes(summary['reclaimableBytes'])}"
    )


def output_dir(explicit: str | None) -> Path:
    if explicit:
        target = Path(explicit).expanduser()
    else:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        target = OUTPUT_ROOT / stamp
    target.mkdir(parents=True, exist_ok=True)
    return target


def emit_report(data: dict, out_dir: Path, open_browser: bool) -> Path:
    report_path = out_dir / "report.html"
    report_path.write_text(render_report(data), encoding="utf-8")
    if open_browser:
        try:
            webbrowser.open(report_path.as_uri())
        except Exception as exc:  # pragma: no cover - environment dependent
            log(f"[wtj] não foi possível abrir o browser: {exc}")
    return report_path


def load_config() -> dict:
    if not CONFIG_PATH.is_file():
        return {}
    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        log(f"[wtj] config inválida em {CONFIG_PATH}: {exc}")
        return {}


def parse_selection(raw: str, items: list[dict]) -> list[int]:
    """Expand `--select` into concrete ids.

    Accepts `all`, `safe`, `review`, `none`, comma lists and `a-b` ranges.
    """
    raw = (raw or "").strip().lower()
    if raw in ("", "none"):
        return []
    if raw == "all":
        return [i["id"] for i in items if i["risk"] in ("safe", "review", "risky")]
    if raw in ("safe", "review", "risky"):
        return [i["id"] for i in items if i["risk"] == raw]
    ids: list[int] = []
    for token in raw.split(","):
        token = token.strip()
        if not token:
            continue
        if "-" in token:
            start, _, end = token.partition("-")
            try:
                ids.extend(range(int(start), int(end) + 1))
            except ValueError:
                raise SystemExit(f"seleção inválida: {token!r}")
        else:
            try:
                ids.append(int(token))
            except ValueError:
                raise SystemExit(f"seleção inválida: {token!r}")
    known = {i["id"] for i in items}
    unknown = [i for i in ids if i not in known]
    if unknown:
        raise SystemExit(f"ids inexistentes no scan: {unknown}")
    return sorted(dict.fromkeys(ids))


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def cmd_scan(args: argparse.Namespace) -> int:
    config = load_config()
    roots = args.root or config.get("roots") or list(DEFAULT_ROOTS)
    protect = (args.protect or []) + list(config.get("protect", []))
    stale_days = args.stale_days if args.stale_days is not None else config.get("staleDays", DEFAULT_STALE_DAYS)

    data = build_scan(roots, args.depth, stale_days, args.include_dirty, protect, quiet=args.json)
    out_dir = output_dir(args.out)
    scan_path = out_dir / "scan.json"
    scan_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    data["scanPath"] = str(scan_path)

    if args.report:
        report = emit_report(data, out_dir, args.open)
        data["reportPath"] = str(report)

    if args.json:
        print(json.dumps(data, ensure_ascii=False))
    else:
        print_table(data)
        print(f"\nscan salvo em: {scan_path}")
        if args.report:
            print(f"relatório: {data['reportPath']}")
    return 0


def cmd_clean(args: argparse.Namespace) -> int:
    scan_path = Path(args.scan).expanduser()
    if not scan_path.is_file():
        raise SystemExit(f"scan não encontrado: {scan_path}")
    scan_data = json.loads(scan_path.read_text(encoding="utf-8"))

    selected = parse_selection(args.select, scan_data["items"])
    if not selected:
        print("Nenhuma worktree selecionada — nada a fazer.")
        return 0
    if not args.yes:
        raise SystemExit("clean exige --yes (confirmação explícita do usuário).")

    result = clean(scan_data, selected, args.delete_branch, args.force)
    out_dir = output_dir(args.out or str(scan_path.parent))
    (out_dir / "result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    write_undo_script(result, out_dir / "undo.sh")
    report = emit_report(result, out_dir, args.open) if not args.no_report else None
    if report:
        result["reportPath"] = str(report)

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(
            f"removidas: {result['removedCount']} · falhas: {result['failedCount']} · "
            f"puladas: {result['skippedCount']} · espaço liberado: {human_bytes(result['reclaimedBytes'])}"
        )
        for entry in result["results"]:
            if entry.get("status") == "failed":
                print(f"  ✗ [{entry['id']}] {entry.get('path')}: {entry.get('error')}")
            elif entry.get("branchError"):
                print(f"  ⚠ [{entry['id']}] branch {entry.get('branch')} não removida: {entry['branchError']}")
        print(f"undo: {out_dir / 'undo.sh'}")
        if report:
            print(f"relatório: {report}")
    return 1 if result["failedCount"] else 0


def cmd_report(args: argparse.Namespace) -> int:
    source = Path(args.result).expanduser()
    if not source.is_file():
        raise SystemExit(f"arquivo não encontrado: {source}")
    data = json.loads(source.read_text(encoding="utf-8"))
    out_dir = output_dir(args.out or str(source.parent))
    report = emit_report(data, out_dir, args.open)
    print(report)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wtj.py", description="Worktree Janitor — limpeza auditável de worktrees de agentes de IA.")
    parser.add_argument("--version", action="version", version=VERSION)
    sub = parser.add_subparsers(dest="command", required=True)

    scan_parser = sub.add_parser("scan", help="descobre e classifica worktrees (read-only)")
    scan_parser.add_argument("--root", action="append", help="raiz de busca (repetível). Default: ~/Projects")
    scan_parser.add_argument("--depth", type=int, default=DEFAULT_DEPTH, help=f"profundidade máxima de busca (default {DEFAULT_DEPTH})")
    scan_parser.add_argument("--stale-days", type=int, default=None, help=f"idade em dias para marcar como stale (default {DEFAULT_STALE_DAYS})")
    scan_parser.add_argument("--include-dirty", action="store_true", help="classifica worktrees sujas além de 'risky'")
    scan_parser.add_argument("--protect", action="append", help="glob de caminho que nunca deve ser removido (repetível)")
    scan_parser.add_argument("--out", help="diretório de saída")
    scan_parser.add_argument("--report", action="store_true", help="renderiza o relatório HTML de pré-visualização")
    scan_parser.add_argument("--open", action="store_true", help="abre o relatório no browser")
    scan_parser.add_argument("--json", action="store_true", help="saída JSON")
    scan_parser.set_defaults(func=cmd_scan)

    clean_parser = sub.add_parser("clean", help="remove as worktrees aprovadas pelo usuário")
    clean_parser.add_argument("--scan", required=True, help="caminho do scan.json")
    clean_parser.add_argument("--select", required=True, help="ids (1,3,5 / 1-4), ou all|safe|review|risky|none")
    clean_parser.add_argument("--delete-branch", choices=["auto", "always", "never"], default="auto", help="política de remoção da branch local")
    clean_parser.add_argument("--force", action="store_true", help="força remoção mesmo com alterações locais")
    clean_parser.add_argument("--yes", action="store_true", help="confirmação explícita (obrigatória)")
    clean_parser.add_argument("--out", help="diretório de saída")
    clean_parser.add_argument("--no-report", action="store_true", help="não renderiza HTML")
    clean_parser.add_argument("--open", action="store_true", help="abre o relatório no browser")
    clean_parser.add_argument("--json", action="store_true", help="saída JSON")
    clean_parser.set_defaults(func=cmd_clean)

    report_parser = sub.add_parser("report", help="renderiza HTML a partir de scan.json ou result.json")
    report_parser.add_argument("--result", required=True, help="caminho do scan.json ou result.json")
    report_parser.add_argument("--out", help="diretório de saída")
    report_parser.add_argument("--open", action="store_true", help="abre o relatório no browser")
    report_parser.set_defaults(func=cmd_report)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
