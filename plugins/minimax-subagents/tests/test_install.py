#!/usr/bin/env python3
"""install.sh against a throwaway HOME (no network, no real harness dirs)."""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
INSTALL = PLUGIN_ROOT / "scripts" / "install.sh"


class InstallTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name) / "home"
        self.home.mkdir()
        # A second hub checkout whose plugins/ a harness links wholesale.
        self.other_hub = Path(self.tmp.name) / "other-hub" / "plugins"
        (self.other_hub / "smart-sub-agents").mkdir(parents=True)
        (self.other_hub / "smart-sub-agents" / "plugin.json").write_text("{}")
        (self.home / ".gemini").mkdir()
        (self.home / ".gemini" / "skills").symlink_to(self.other_hub)
        # A curated per-skill dir that should get a link. Real curated dirs
        # already hold per-skill symlinks into the hub (incl. smart-sub-agents).
        curated = self.home / ".config" / "opencode" / "skills"
        curated.mkdir(parents=True)
        (curated / "smart-sub-agents").symlink_to(self.other_hub / "smart-sub-agents")
        # A stale link from an earlier install (other checkout) gets repointed.
        (curated / "minimax-subagents").symlink_to(Path(self.tmp.name) / "old-clone" / "minimax-subagents")
        fake = Path(self.tmp.name) / "opencode"
        fake.write_text("#!/bin/sh\nexit 0\n")
        fake.chmod(0o755)
        env = {k: v for k, v in os.environ.items() if not k.startswith("MM_")}
        self.env = {**env, "HOME": str(self.home), "MM_OPENCODE_BIN": str(fake)}

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_never_links_into_a_wholesale_hub_dir(self) -> None:
        """Regression: ~/.gemini/skills -> <live hub>/plugins got a stray symlink."""
        result = subprocess.run(["bash", str(INSTALL)], capture_output=True, text=True, env=self.env, check=False)
        self.assertFalse((self.other_hub / "minimax-subagents").exists(), result.stdout)
        self.assertIn("resolves to a hub plugins/ dir", result.stdout)
        curated = self.home / ".config" / "opencode" / "skills" / "minimax-subagents"
        self.assertTrue(curated.is_symlink())
        self.assertEqual(curated.resolve(), PLUGIN_ROOT.resolve())
        self.assertTrue((self.home / ".local" / "bin" / "mm-run").is_symlink())
        self.assertTrue((self.home / ".config" / "opencode" / "agents" / "mm_flash_worker_high.md").is_file())
        self.assertTrue((self.home / ".claude" / "agents" / "mm_m3_worker_medium.md").is_file())

    def test_dry_run_writes_nothing(self) -> None:
        result = subprocess.run(["bash", str(INSTALL), "--dry-run"], capture_output=True, text=True, env=self.env, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.home / ".local" / "bin" / "mm-run").exists())
        self.assertFalse((self.home / ".config" / "opencode" / "skills" / "minimax-subagents").exists())


if __name__ == "__main__":
    unittest.main()
