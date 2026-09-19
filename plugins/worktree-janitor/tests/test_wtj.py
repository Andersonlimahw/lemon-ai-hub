#!/usr/bin/env python3
"""Tests for Worktree Janitor. Run: python3 -m unittest discover -s tests"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import wtj  # noqa: E402
from render_html import render_report  # noqa: E402


def run_git(args: list[str], cwd: str) -> str:
    proc = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True)
    return proc.stdout.strip()


def build_fixture(root: Path) -> Path:
    """Create a repo whose worktrees cover every classification branch."""
    repo = root / "demo"
    repo.mkdir(parents=True)
    env = {"GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null"}
    os.environ.update(env)
    run_git(["init", "-q", "-b", "main", "."], str(repo))
    run_git(["config", "user.email", "t@t.io"], str(repo))
    run_git(["config", "user.name", "T"], str(repo))
    (repo / "a.txt").write_text("hi", encoding="utf-8")
    run_git(["add", "."], str(repo))
    run_git(["commit", "-qm", "init"], str(repo))

    # merged: branch pointing at the base commit
    run_git(["branch", "feat/merged"], str(repo))
    run_git(["worktree", "add", "-q", ".claude/worktrees/merged", "feat/merged"], str(repo))

    # active: branch with a unique, recent commit
    run_git(["worktree", "add", "-q", "-b", "feat/active", ".claude/worktrees/active"], str(repo))
    active = repo / ".claude/worktrees/active"
    (active / "b.txt").write_text("x", encoding="utf-8")
    run_git(["add", "."], str(active))
    run_git(["commit", "-qm", "work"], str(active))

    # dirty: unique commit + uncommitted change
    run_git(["worktree", "add", "-q", "-b", "feat/dirty", ".codex/worktrees/dirty"], str(repo))
    dirty = repo / ".codex/worktrees/dirty"
    (dirty / "c.txt").write_text("y", encoding="utf-8")
    run_git(["add", "."], str(dirty))
    run_git(["commit", "-qm", "work2"], str(dirty))
    (dirty / "c.txt").write_text("y-changed", encoding="utf-8")

    # prunable: directory deleted behind git's back
    run_git(["worktree", "add", "-q", "-b", "feat/gone", ".gemini/worktrees/gone"], str(repo))
    subprocess.run(["rm", "-rf", str(repo / ".gemini/worktrees/gone")], check=True)

    return repo


class ScanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.tmp.name)
        cls.repo = build_fixture(cls.root)
        cls.scan = wtj.build_scan([str(cls.root)], depth=4, stale_days=14,
                                  include_dirty=False, protect_patterns=[], quiet=True)
        cls.by_branch = {i["branch"]: i for i in cls.scan["items"]}

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tmp.cleanup()

    def test_finds_every_worktree(self) -> None:
        self.assertEqual(self.scan["summary"]["total"], 5)
        self.assertEqual(self.scan["reposScanned"], 1)

    def test_branch_names_with_slash_are_preserved(self) -> None:
        self.assertIn("feat/merged", self.by_branch)
        self.assertIn("feat/dirty", self.by_branch)

    def test_main_worktree_is_protected(self) -> None:
        main = self.by_branch["main"]
        self.assertEqual(main["risk"], "protected")
        self.assertEqual(main["reason"], "main-worktree")
        self.assertFalse(main["recommended"])

    def test_merged_branch_is_safe(self) -> None:
        item = self.by_branch["feat/merged"]
        self.assertEqual(item["risk"], "safe")
        self.assertEqual(item["reason"], "merged")
        self.assertTrue(item["recommended"])

    def test_prunable_worktree_is_safe(self) -> None:
        item = self.by_branch["feat/gone"]
        self.assertEqual(item["reason"], "prunable")
        self.assertEqual(item["risk"], "safe")
        self.assertFalse(item["exists"])

    def test_dirty_worktree_is_risky_and_not_recommended(self) -> None:
        item = self.by_branch["feat/dirty"]
        self.assertEqual(item["risk"], "risky")
        self.assertEqual(item["reason"], "dirty")
        self.assertGreater(item["dirtyFiles"], 0)
        self.assertFalse(item["recommended"])

    def test_active_worktree_is_kept(self) -> None:
        item = self.by_branch["feat/active"]
        self.assertEqual(item["risk"], "keep")
        self.assertEqual(item["reason"], "active")
        self.assertGreaterEqual(item["ahead"], 1)

    def test_harness_detection(self) -> None:
        self.assertEqual(self.by_branch["feat/merged"]["harness"], "Claude Code")
        self.assertEqual(self.by_branch["feat/dirty"]["harness"], "Codex")
        self.assertEqual(self.by_branch["feat/gone"]["harness"], "Gemini CLI")

    def test_summary_counts_only_safe_as_reclaimable(self) -> None:
        summary = self.scan["summary"]
        self.assertEqual(summary["byRisk"]["safe"], 2)
        self.assertEqual(summary["byRisk"]["risky"], 1)
        self.assertEqual(summary["candidates"], 2)

    def test_report_is_self_contained(self) -> None:
        html = render_report(self.scan)
        self.assertEqual(re.findall(r"__[A-Z_]+__", html), [])
        self.assertEqual(re.findall(r'(?:src|href)="(?!#)[^"]+"', html), [])
        self.assertEqual(html.count('<tr data-risk'), 5)


class SelectionTests(unittest.TestCase):
    items = [
        {"id": 1, "risk": "safe"},
        {"id": 2, "risk": "review"},
        {"id": 3, "risk": "risky"},
        {"id": 4, "risk": "protected"},
        {"id": 5, "risk": "keep"},
    ]

    def test_keywords(self) -> None:
        self.assertEqual(wtj.parse_selection("safe", self.items), [1])
        self.assertEqual(wtj.parse_selection("all", self.items), [1, 2, 3])
        self.assertEqual(wtj.parse_selection("none", self.items), [])
        self.assertEqual(wtj.parse_selection("", self.items), [])

    def test_explicit_ids_and_ranges(self) -> None:
        self.assertEqual(wtj.parse_selection("1,3", self.items), [1, 3])
        self.assertEqual(wtj.parse_selection("1-3", self.items), [1, 2, 3])
        self.assertEqual(wtj.parse_selection("3,1,3", self.items), [1, 3])

    def test_unknown_id_is_rejected(self) -> None:
        with self.assertRaises(SystemExit):
            wtj.parse_selection("99", self.items)

    def test_garbage_is_rejected(self) -> None:
        with self.assertRaises(SystemExit):
            wtj.parse_selection("abc", self.items)


class CleanTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.repo = build_fixture(self.root)
        self.scan = wtj.build_scan([str(self.root)], depth=4, stale_days=14,
                                   include_dirty=False, protect_patterns=[], quiet=True)
        self.by_branch = {i["branch"]: i for i in self.scan["items"]}

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def worktree_paths(self) -> list[str]:
        out = run_git(["worktree", "list", "--porcelain"], str(self.repo))
        return [line.split(" ", 1)[1] for line in out.splitlines() if line.startswith("worktree ")]

    def test_clean_safe_removes_only_safe_items(self) -> None:
        ids = wtj.parse_selection("safe", self.scan["items"])
        result = wtj.clean(self.scan, ids, branch_policy="auto", force=False)
        self.assertEqual(result["removedCount"], 2)
        self.assertEqual(result["failedCount"], 0)
        remaining = self.worktree_paths()
        self.assertEqual(len(remaining), 3)  # main + active + dirty
        self.assertTrue(any("active" in p for p in remaining))
        self.assertTrue(any("dirty" in p for p in remaining))

    def test_merged_branch_is_deleted_prunable_branch_is_kept(self) -> None:
        ids = wtj.parse_selection("safe", self.scan["items"])
        wtj.clean(self.scan, ids, branch_policy="auto", force=False)
        branches = run_git(["branch", "--format=%(refname:short)"], str(self.repo)).splitlines()
        self.assertNotIn("feat/merged", branches)
        self.assertIn("feat/gone", branches)

    def test_never_policy_keeps_branches(self) -> None:
        ids = [self.by_branch["feat/merged"]["id"]]
        wtj.clean(self.scan, ids, branch_policy="never", force=False)
        branches = run_git(["branch", "--format=%(refname:short)"], str(self.repo)).splitlines()
        self.assertIn("feat/merged", branches)

    def test_protected_item_is_skipped_even_when_selected(self) -> None:
        main_id = self.by_branch["main"]["id"]
        result = wtj.clean(self.scan, [main_id], branch_policy="auto", force=False)
        self.assertEqual(result["removedCount"], 0)
        self.assertEqual(result["skippedCount"], 1)
        self.assertIn("protegida", result["results"][0]["error"])
        self.assertTrue(Path(self.repo / ".git").exists())

    def test_undo_script_restores_branch_and_worktree(self) -> None:
        ids = [self.by_branch["feat/merged"]["id"]]
        result = wtj.clean(self.scan, ids, branch_policy="auto", force=False)
        undo = self.root / "undo.sh"
        wtj.write_undo_script(result, undo)
        self.assertTrue(os.access(undo, os.X_OK))
        subprocess.run(["bash", str(undo)], check=True, capture_output=True)
        branches = run_git(["branch", "--format=%(refname:short)"], str(self.repo)).splitlines()
        self.assertIn("feat/merged", branches)
        self.assertTrue(any("merged" in p for p in self.worktree_paths()))

    def test_dirty_worktree_requires_explicit_selection(self) -> None:
        dirty_id = self.by_branch["feat/dirty"]["id"]
        self.assertNotIn(dirty_id, wtj.parse_selection("safe", self.scan["items"]))
        result = wtj.clean(self.scan, [dirty_id], branch_policy="auto", force=True)
        self.assertEqual(result["removedCount"], 1)

    def test_executed_report_renders(self) -> None:
        ids = wtj.parse_selection("safe", self.scan["items"])
        result = wtj.clean(self.scan, ids, branch_policy="auto", force=False)
        html = render_report(result)
        self.assertEqual(re.findall(r"__[A-Z_]+__", html), [])
        self.assertIn("Desfazer", html)
        self.assertIn("Removida", html)


class ShellQuotingTests(unittest.TestCase):
    def test_single_quotes_are_escaped(self) -> None:
        self.assertEqual(wtj.shq("/tmp/it's here"), "'/tmp/it'\\''s here'")

    def test_spaces_survive_a_shell_round_trip(self) -> None:
        path = "/tmp/a b/c'd"
        out = subprocess.run(["bash", "-c", f"printf %s {wtj.shq(path)}"],
                             capture_output=True, text=True, check=True).stdout
        self.assertEqual(out, path)


class HumanBytesTests(unittest.TestCase):
    def test_scales(self) -> None:
        self.assertEqual(wtj.human_bytes(0), "0 B")
        self.assertEqual(wtj.human_bytes(512), "512 B")
        self.assertEqual(wtj.human_bytes(2048), "2.0 KB")
        self.assertEqual(wtj.human_bytes(5 * 1024 ** 3), "5.0 GB")


if __name__ == "__main__":
    unittest.main()
