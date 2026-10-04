#!/usr/bin/env python3
"""mm_run.py mcode backend (default) against fake `mcode` / `opencode` binaries."""

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

FAKE_MCODE = textwrap.dedent(
    """\
    #!/usr/bin/env python3
    import json, os, sys
    from pathlib import Path
    state = Path(os.environ["FAKE_STATE"])
    with open(state / "mcode.jsonl", "a") as f:
        f.write(json.dumps(sys.argv[1:]) + "\\n")
    calls = len((state / "mcode.jsonl").read_text().splitlines())
    mode = os.environ.get("FAKE_MODE", "ok")
    if sys.argv[1:3] == ["provider", "list"]:
        print("* minimax_oauth\\tactive\\tmanaged login" if mode != "no-login" else "  minimax_api\\tenabled\\tno key")
        sys.exit(0)
    def result(status, **extra):
        print(json.dumps({"type": "exec.result", "status": status, **extra}))
    usage = {"inputTokens": 14000, "outputTokens": 3, "cacheReadTokens": 1500}
    if mode == "ok":
        print("progress line that is not json")
        result("succeeded", output="<think>hidden</think>\\nMCODE-DONE", usage=usage)
    elif mode == "quota":
        result("failed", error={"category": "runtime", "message": "429 usage limit exceeded for this window"})
        sys.stderr.write("mcode exec failed: usage limit\\n")
        sys.exit(4)
    elif mode == "transient-once":
        if calls == 1:
            result("failed", error={"category": "runtime", "message": "Unexpected server error"})
            sys.exit(4)
        result("succeeded", output="RECOVERED", usage=usage)
    elif mode == "bad-model":
        result("failed", error={"category": "runtime", "message": "Model is not available", "retryable": True})
        sys.exit(4)
    elif mode == "timeout":
        result("timed_out", error={"message": "Run timed out after 30s"})
        sys.exit(4)
    """
)

FAKE_OPENCODE = textwrap.dedent(
    """\
    #!/usr/bin/env python3
    import json, os, sys
    from pathlib import Path
    state = Path(os.environ["FAKE_STATE"])
    with open(state / "opencode.jsonl", "a") as f:
        f.write(json.dumps(sys.argv[1:]) + "\\n")
    if sys.argv[1] == "models":
        for m in ("MiniMax-M2.7-highspeed", "MiniMax-M3", "MiniMax-M3.1-Flash-Preview"):
            print(f"minimax/{m}")
        sys.exit(0)
    print(json.dumps({"type": "text", "part": {"id": "p1", "type": "text", "text": "OPENCODE-DONE"}}))
    """
)


def executable(path: Path, body: str) -> Path:
    path.write_text(body)
    path.chmod(path.stat().st_mode | stat.S_IEXEC)
    return path


class McodeBackendTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.mcode = executable(root / "mcode", FAKE_MCODE)
        self.opencode = executable(root / "opencode", FAKE_OPENCODE)
        self.state = root / "state"
        self.state.mkdir()
        self.agents = root / "agents"
        self.agents.mkdir()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_mm(self, *args: str, mode: str = "ok", extra_env=None):
        env = {
            **{k: v for k, v in os.environ.items() if not k.startswith("MM_")},
            "MM_MCODE_BIN": str(self.mcode),
            "MM_OPENCODE_BIN": str(self.opencode),
            "MM_AGENT_DIRS": str(self.agents),
            "MM_STATE_DIR": str(self.state / "mm"),
            "FAKE_STATE": str(self.state),
            "FAKE_MODE": mode,
            **(extra_env or {}),
        }
        return subprocess.run([sys.executable, str(MM_RUN), *args], capture_output=True, text=True, env=env, check=False)

    def calls(self, backend: str) -> list[list[str]]:
        path = self.state / f"{backend}.jsonl"
        return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

    def flag(self, argv: list[str], name: str) -> str:
        return argv[argv.index(name) + 1]

    def test_mcode_is_the_default_backend(self) -> None:
        result = self.run_mm("--tier", "quality", "--", "do it")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "MCODE-DONE")
        self.assertNotIn("hidden", result.stdout)
        self.assertIn("backend=mcode", result.stderr)
        argv = self.calls("mcode")[0]
        self.assertEqual(argv[0], "exec")
        self.assertEqual(self.flag(argv, "--model"), "minimax/MiniMax-M3.1-Flash-Preview")
        self.assertEqual(self.flag(argv, "--effort"), "high")  # quality default depth
        self.assertEqual(self.flag(argv, "--output-format"), "json")
        self.assertEqual(self.flag(argv, "--permission"), "smart")
        self.assertEqual(argv[-2:], ["--", "do it"])
        self.assertEqual(self.calls("opencode"), [])

    def test_fixed_depth_models_get_no_effort_flag(self) -> None:
        for tier, model in (("budget", "MiniMax-M2.7-highspeed"), ("balanced", "MiniMax-M3")):
            with self.subTest(tier=tier):
                self.run_mm("--tier", tier, "--effort", "max", "x")
                argv = self.calls("mcode")[-1]
                self.assertEqual(self.flag(argv, "--model"), f"minimax/{model}")
                self.assertNotIn("--effort", argv)

    def test_worker_agent_name_maps_to_model_and_effort(self) -> None:
        result = self.run_mm("--agent", "mm_flash_worker_xhigh", "--dir", "/tmp", "-f", "a.py", "x")
        self.assertEqual(result.returncode, 0, result.stderr)
        argv = self.calls("mcode")[0]
        self.assertEqual(self.flag(argv, "--model"), "minimax/MiniMax-M3.1-Flash-Preview")
        self.assertEqual(self.flag(argv, "--effort"), "xhigh")
        self.assertEqual(self.flag(argv, "--cwd"), "/tmp")
        self.assertEqual(self.flag(argv, "--file"), "a.py")
        self.assertNotIn("--agent", argv)

    def test_non_worker_agent_runs_on_opencode(self) -> None:
        result = self.run_mm("--agent", "my_custom_agent", "x")
        self.assertEqual(result.stdout.strip(), "OPENCODE-DONE")
        self.assertEqual(self.calls("mcode"), [])
        self.assertEqual(self.flag(self.calls("opencode")[0], "--agent"), "my_custom_agent")

    def test_backend_flag_and_env_force_opencode(self) -> None:
        self.run_mm("--backend", "opencode", "x")
        self.run_mm("x", extra_env={"MM_BACKEND": "opencode"})
        self.assertEqual(len(self.calls("opencode")), 2)
        self.assertEqual(self.calls("mcode"), [])

    def test_auto_falls_back_to_opencode_without_mcode(self) -> None:
        result = self.run_mm("x", extra_env={"MM_MCODE_BIN": ""})
        self.assertEqual(result.stdout.strip(), "OPENCODE-DONE")
        self.assertIn("backend=opencode", result.stderr)

    def test_quota_exits_75_without_retry(self) -> None:
        result = self.run_mm("--tier", "balanced", "x", mode="quota")
        self.assertEqual(result.returncode, 75)
        self.assertIn("ROUTE-FALLBACK", result.stdout)
        self.assertIn("sonnet_worker_medium", result.stdout)
        self.assertEqual(len(self.calls("mcode")), 1)

    def test_transient_failure_retries_once(self) -> None:
        result = self.run_mm("x", mode="transient-once")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "RECOVERED")
        self.assertEqual(len(self.calls("mcode")), 2)

    def test_explicit_mcode_hard_failure_keeps_exit_code(self) -> None:
        result = self.run_mm("--backend", "mcode", "x", mode="bad-model")
        self.assertEqual(result.returncode, 4)
        self.assertEqual(len(self.calls("mcode")), 1)
        self.assertEqual(self.calls("opencode"), [])
        self.assertIn("not available", result.stderr)

    def test_auto_mcode_infra_failure_falls_back_to_opencode_once(self) -> None:
        """Regression: in Codex's sandbox mcode fails on a local lock; auto mode recovers."""
        self.install_agent("mm_flash_worker_high")
        result = self.run_mm("--tier", "quality", "x", mode="bad-model")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "OPENCODE-DONE")
        self.assertIn("retrying once on the opencode backend", result.stderr)
        self.assertEqual(len(self.calls("mcode")), 1)
        self.assertEqual(self.flag(self.calls("opencode")[0], "--agent"), "mm_flash_worker_high")

    def test_quota_and_timeout_never_switch_backend(self) -> None:
        self.assertEqual(self.run_mm("x", mode="quota").returncode, 75)
        self.assertEqual(self.run_mm("x", mode="timeout").returncode, 124)
        self.assertEqual(self.calls("opencode"), [])

    def install_agent(self, name: str) -> None:
        (self.agents / f"{name}.md").write_text("---\nmode: all\n---\n")

    def test_check_reports_both_backends(self) -> None:
        result = self.run_mm("--check")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("default backend: mcode", result.stdout)
        self.assertIn("provider=minimax_oauth", result.stdout)
        self.assertIn("OK      opencode quality", result.stdout)
        self.assertEqual(self.run_mm("--check", mode="no-login").returncode, 3)

    def test_dry_run_shows_mcode_command(self) -> None:
        result = self.run_mm("--dry-run", "--tier", "budget", "x")
        self.assertIn("exec --cwd", result.stdout)
        self.assertEqual(self.calls("mcode"), [])


if __name__ == "__main__":
    unittest.main()
