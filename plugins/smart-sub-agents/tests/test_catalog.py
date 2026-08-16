#!/usr/bin/env python3
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PLUGIN_ROOT / "scripts"
VALIDATOR = SCRIPTS_DIR / "validate_catalog.py"
RENDERER = SCRIPTS_DIR / "render_agents.py"
INSTALLER = SCRIPTS_DIR / "install_worker_matrix.py"
SYNCER = SCRIPTS_DIR / "sync_provider_matrix.py"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class SmartSubAgentsCatalogTests(unittest.TestCase):
    def run_cli(self, script: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(script), *args], capture_output=True, text=True, check=False)

    def test_catalog_is_valid(self) -> None:
        result = self.run_cli(VALIDATOR)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertRegex(result.stdout, r"\d+ providers")
        self.assertIn("harnesses", result.stdout)

    def test_sol_route_renders(self) -> None:
        result = self.run_cli(RENDERER, "--harness", "codex", "--provider", "openai", "--model", "gpt-5.6-sol", "--effort", "xhigh")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('model = "gpt-5.6-sol"', result.stdout)
        self.assertIn('model_reasoning_effort = "xhigh"', result.stdout)

    def test_alias_normalizes_lunce_to_luna(self) -> None:
        result = self.run_cli(RENDERER, "--harness", "codex", "--model", "gpt-5.6 lunce", "--effort", "low")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('model = "gpt-5.6-luna"', result.stdout)

    def test_deepseek_route_keeps_thinking_mapping(self) -> None:
        result = self.run_cli(RENDERER, "--harness", "opencode", "--provider", "deepseek", "--model", "deepseek-v4-flash", "--effort", "max")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("deepseek/deepseek-v4-flash", result.stdout)
        self.assertIn("thinking=true", result.stdout)

    def test_user_examples_normalize_harness_and_provider_aliases(self) -> None:
        examples = (
            (("--harness", "codex", "--provider", "openai", "--model", "l 5.6 lunce", "--effort", "max"), "gpt-5.6-luna"),
            (("--harness", "opencode", "--provider", "opencode", "--model", "kimi k3", "--effort", "low"), "moonshotai/kimi-k2"),
            (("--harness", "claude-code", "--provider", "anthropic", "--model", "Opus %", "--effort", "medium"), "claude-opus-5"),
            (("--harness", "opencode", "--provider", "deepseek api", "--model", "deepseek v4 flash", "--effort", "max"), "deepseek/deepseek-v4-flash"),
            (("--harness", "opencode", "--provider", "google", "--model", "Gemini 3.5 Pro", "--effort", "high"), "google/gemini-2.5-pro"),
        )
        for arguments, expected in examples:
            with self.subTest(expected=expected):
                result = self.run_cli(RENDERER, *arguments)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(expected, result.stdout)

    def test_all_harnesses_render_to_output_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.run_cli(RENDERER, "--harness", "all", "--profile", "balanced", "--output-dir", temp_dir)
            self.assertEqual(result.returncode, 0, result.stderr)
            for harness in ("claude-code", "codex", "opencode", "antigravity", "gemini-cli", "lemon-code"):
                self.assertTrue((Path(temp_dir) / harness).exists(), harness)

    def test_unknown_model_fails_closed(self) -> None:
        result = self.run_cli(RENDERER, "--harness", "opencode", "--provider", "openai", "--model", "gpt-5.6-lunce")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unknown model", result.stderr)


class InstallHelperTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        sys.path.insert(0, str(SCRIPTS_DIR))
        cls.installer = _load_module("install_worker_matrix", INSTALLER)

    def test_slug_normalizes_punctuation(self) -> None:
        self.assertEqual(self.installer.slug("Go Luna #1!"), "go_luna_1")

    def test_worker_name_format(self) -> None:
        self.assertEqual(self.installer.worker_name("go_luna", "high"), "go_luna_worker_high")

    def test_load_catalog_fails_closed_on_invalid_matrix(self) -> None:
        bad = {
            "schemaVersion": 99,
            "updated": "not-a-date",
            "efforts": [],
            "harnesses": {},
            "providers": [],
        }
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(bad, f)
            catalog_path = Path(f.name)
        try:
            with self.assertRaises(ValueError):
                self.installer.load_catalog(catalog_path)
        finally:
            catalog_path.unlink(missing_ok=True)


class SyncHelperTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        sys.path.insert(0, str(SCRIPTS_DIR))
        cls.syncer = _load_module("sync_provider_matrix", SYNCER)

    def test_tier_guess_minimax_is_balanced(self) -> None:
        self.assertEqual(self.syncer.tier_guess("minimax-m3"), "balanced")

    def test_tier_guess_flash_is_budget(self) -> None:
        self.assertEqual(self.syncer.tier_guess("gemini-3.6-flash"), "budget")

    def test_tier_guess_sol_is_quality(self) -> None:
        self.assertEqual(self.syncer.tier_guess("gpt-5.6-sol"), "quality")


if __name__ == "__main__":
    unittest.main()
