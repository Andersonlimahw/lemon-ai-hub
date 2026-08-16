#!/usr/bin/env python3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = PLUGIN_ROOT / "scripts" / "validate_catalog.py"
RENDERER = PLUGIN_ROOT / "scripts" / "render_agents.py"


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


if __name__ == "__main__":
    unittest.main()
