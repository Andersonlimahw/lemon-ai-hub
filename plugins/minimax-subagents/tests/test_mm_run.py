#!/usr/bin/env python3
"""mm_run.py contract tests against a fake `opencode` binary (no network, no keys)."""

import json
import os
import stat
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
MM_RUN = PLUGIN_ROOT / "scripts" / "mm_run.py"
SHIM = PLUGIN_ROOT / "bin" / "mm-run"

FAKE_OPENCODE = textwrap.dedent(
    """\
    #!/usr/bin/env python3
    import json, os, sys
    from pathlib import Path
    state = Path(os.environ["FAKE_STATE"])
    with open(state / "argv.jsonl", "a") as f:
        f.write(json.dumps(sys.argv[1:]) + "\\n")
    calls = len((state / "argv.jsonl").read_text().splitlines())
    mode = os.environ.get("FAKE_MODE", "ok")
    if sys.argv[1] == "models":
        for m in ("MiniMax-M2.7-highspeed", "MiniMax-M3", "MiniMax-M3.1-Flash-Preview"):
            if mode == "models-missing" and m == "MiniMax-M3":
                continue
            print(f"minimax/{m}")
        sys.exit(0)
    def text(t):
        print(json.dumps({"type": "text", "part": {"id": "p1", "type": "text", "text": t}}))
    def finish():
        print(json.dumps({"type": "step_finish", "part": {"type": "step-finish", "tokens": {"input": 10, "output": 2}}}))
    if mode == "ok":
        text("<think>\\nsecret reasoning\\n</think>\\n\\nDONE")
        finish()
    elif mode == "quota":
        sys.stderr.write('Error: {"name":"APIError","data":{"message":"429 usage limit exceeded"}}\\n')
        sys.exit(1)
    elif mode == "transient-once":
        if calls == 1:
            sys.stderr.write('Error: {"name":"UnknownError","data":{"message":"Unexpected server error"}}\\n')
            sys.exit(1)
        text("RECOVERED")
        finish()
    elif mode == "model-says-quota":
        text("The word quota and 429 appear in my answer, that is fine.")
        finish()
    elif mode == "hard-fail":
        sys.stderr.write("Error: invalid configuration\\n")
        sys.exit(1)
    """
)


class MmRunTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.fake = root / "opencode"
        self.fake.write_text(FAKE_OPENCODE)
        self.fake.chmod(self.fake.stat().st_mode | stat.S_IEXEC)
        self.state = root / "state"
        self.state.mkdir()
        # Hermetic: never see the machine's real ~/.config/opencode/agents.
        self.agents = root / "agents"
        self.agents.mkdir()

    def install_agent(self, name: str) -> None:
        (self.agents / f"{name}.md").write_text("---\nmode: all\n---\n")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_mm(self, *args: str, mode: str = "ok", stdin: str | None = None, exe=None, extra_env=None):
        env = {
            **{k: v for k, v in os.environ.items() if not k.startswith("MM_")},
            "MM_OPENCODE_BIN": str(self.fake),
            "FAKE_STATE": str(self.state),
            "FAKE_MODE": mode,
            "MM_STATE_DIR": str(self.state / "mm"),
            "MM_AGENT_DIRS": str(self.agents),
            **(extra_env or {}),
        }
        env = {k: v for k, v in env.items() if v is not None}
        command = [str(exe)] if exe else [sys.executable, str(MM_RUN)]
        return subprocess.run(command + list(args), capture_output=True, text=True, env=env, input=stdin, check=False)

    def calls(self) -> list[list[str]]:
        path = self.state / "argv.jsonl"
        return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

    def test_strips_thinking_and_prints_only_answer(self) -> None:
        result = self.run_mm("--tier", "quality", "--effort", "high", "--", "do it")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "DONE")
        self.assertNotIn("secret reasoning", result.stdout)
        argv = self.calls()[0]
        self.assertIn("minimax/MiniMax-M3.1-Flash-Preview", argv)
        self.assertEqual(argv[argv.index("--variant") + 1], "high")
        self.assertEqual(argv[-2:], ["--", "do it"])

    def test_thinking_flag_keeps_reasoning(self) -> None:
        result = self.run_mm("--thinking", "x")
        self.assertIn("secret reasoning", result.stdout)

    def test_variant_only_for_tunable_model(self) -> None:
        result = self.run_mm("--tier", "balanced", "--effort", "max", "x")
        self.assertEqual(result.returncode, 0, result.stderr)
        argv = self.calls()[0]
        self.assertIn("minimax/MiniMax-M3", argv)
        self.assertNotIn("--variant", argv)
        self.assertIn("--effort ignored", result.stderr)

    def test_default_tier_is_balanced(self) -> None:
        self.run_mm("x")
        self.assertIn("minimax/MiniMax-M3", self.calls()[0])

    def test_agent_route_lets_agent_pick_model(self) -> None:
        self.run_mm("--agent", "mm_flash_worker_high", "x")
        argv = self.calls()[0]
        self.assertEqual(argv[argv.index("--agent") + 1], "mm_flash_worker_high")
        self.assertNotIn("-m", argv)

    def test_tier_prefers_installed_lean_worker(self) -> None:
        self.install_agent("mm_flash_worker_high")
        result = self.run_mm("--tier", "quality", "x")
        self.assertEqual(result.returncode, 0, result.stderr)
        argv = self.calls()[0]
        self.assertEqual(argv[argv.index("--agent") + 1], "mm_flash_worker_high")
        self.assertNotIn("-m", argv)
        self.assertNotIn("--variant", argv)

    def test_lean_worker_effort_is_clamped_for_fixed_depth_family(self) -> None:
        self.install_agent("mm_m3_worker_high")
        result = self.run_mm("--tier", "balanced", "--effort", "max", "x")
        argv = self.calls()[0]
        self.assertEqual(argv[argv.index("--agent") + 1], "mm_m3_worker_high")
        self.assertNotIn("--variant", argv)
        self.assertIn("--effort ignored", result.stderr)

    def test_flash_worker_passes_explicit_effort_as_variant(self) -> None:
        self.install_agent("mm_flash_worker_xhigh")
        self.run_mm("--tier", "quality", "--effort", "xhigh", "x")
        argv = self.calls()[0]
        self.assertEqual(argv[argv.index("--agent") + 1], "mm_flash_worker_xhigh")
        self.assertEqual(argv[argv.index("--variant") + 1], "xhigh")

    def test_no_agent_and_model_override_bypass_workers(self) -> None:
        self.install_agent("mm_m3_worker_medium")
        self.run_mm("--no-agent", "x")
        self.run_mm("x", extra_env={"MM_MODEL_BALANCED": "MiniMax-M2.7"})
        first, second = self.calls()
        self.assertNotIn("--agent", first)
        self.assertIn("minimax/MiniMax-M3", first)
        self.assertIn("minimax/MiniMax-M2.7", second)

    def test_quota_exits_75_with_fallback_and_no_retry(self) -> None:
        result = self.run_mm("--tier", "quality", "x", mode="quota")
        self.assertEqual(result.returncode, 75)
        self.assertIn("ROUTE-FALLBACK", result.stdout)
        self.assertIn("opus_worker_high", result.stdout)
        self.assertEqual(len(self.calls()), 1)

    def test_transient_error_retries_once(self) -> None:
        result = self.run_mm("x", mode="transient-once")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "RECOVERED")
        self.assertEqual(len(self.calls()), 2)

    def test_quota_words_in_model_text_are_not_a_quota_error(self) -> None:
        result = self.run_mm("x", mode="model-says-quota")
        self.assertEqual(result.returncode, 0)

    def test_hard_failure_is_not_retried(self) -> None:
        result = self.run_mm("x", mode="hard-fail")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(len(self.calls()), 1)
        self.assertIn("invalid configuration", result.stderr)

    def test_prompt_from_stdin(self) -> None:
        result = self.run_mm(stdin="from stdin")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.calls()[0][-1], "from stdin")

    def test_missing_prompt_is_usage_error(self) -> None:
        result = self.run_mm(stdin="")
        self.assertEqual(result.returncode, 2)

    def test_check_reports_missing_models(self) -> None:
        self.assertEqual(self.run_mm("--check").returncode, 0)
        result = self.run_mm("--check", mode="models-missing")
        self.assertEqual(result.returncode, 3)
        self.assertIn("MISSING", result.stdout)

    def test_dry_run_does_not_call_opencode(self) -> None:
        result = self.run_mm("--dry-run", "--tier", "budget", "x")
        self.assertEqual(result.returncode, 0)
        self.assertIn("minimax/MiniMax-M2.7-highspeed", result.stdout)
        self.assertEqual(self.calls(), [])

    def test_sandboxed_home_falls_back_to_tmpdir_slots(self) -> None:
        """Regression: Codex workspace-write cannot write ~/.cache; mm-run crashed."""
        home = Path(self.tmp.name) / "ro-home"
        home.mkdir()
        home.chmod(0o500)
        tmpdir = Path(self.tmp.name) / "tmpdir"
        tmpdir.mkdir()
        try:
            result = self.run_mm("x", extra_env={"MM_STATE_DIR": None, "HOME": str(home), "TMPDIR": str(tmpdir)})
        finally:
            home.chmod(0o700)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "DONE")
        self.assertTrue(list(tmpdir.glob("minimax-subagents-*/slots/slot-0.lock")))

    def test_no_writable_state_dir_fails_open(self) -> None:
        locked = Path(self.tmp.name) / "locked"
        locked.mkdir()
        locked.chmod(0o500)
        try:
            result = self.run_mm("x", extra_env={"MM_STATE_DIR": str(locked / "state")})
        finally:
            locked.chmod(0o700)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("without the parallel cap", result.stderr)

    def test_shim_resolves_through_symlink(self) -> None:
        link = Path(self.tmp.name) / "mm-run"
        link.symlink_to(SHIM)
        result = self.run_mm("x", exe=link)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "DONE")


if __name__ == "__main__":
    unittest.main()
