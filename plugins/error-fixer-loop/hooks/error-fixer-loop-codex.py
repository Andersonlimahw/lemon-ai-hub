#!/usr/bin/env python3
"""error-fixer-loop-codex.py — Codex-compatible PostToolUse hook (Bash).

Reads hook JSON from stdin (Codex CLI schema or Claude Code schema),
scans tool output for build/test/typecheck error patterns and, ONLY when
an error is detected, prints a JSON payload Codex accepts:

    {"hookSpecificOutput": {"hookEventName": "PostToolUse",
                            "additionalContext": "..."}}

When no error is detected it prints NOTHING and exits 0. Printing
plain text (like the Claude-format error-fixer-loop-hook.sh does) makes
Codex report "hook returned invalid post-tool-use JSON output" on
every Bash call -- this script is the fix for that.

Do NOT register hooks/error-fixer-loop-hook.sh in ~/.codex/hooks.json.
Register this file instead, e.g.:

    "/usr/bin/python3 ~/.codex/hooks/error-fixer-loop-codex.py"

Always exits 0 (never blocks the tool).

Source of truth: lemon-ai-hub/plugins/error-fixer-loop/hooks/error-fixer-loop-codex.py
Skill:           lemon-ai-hub/plugins/error-fixer-loop/SKILL.md
"""
import json
import re
import sys

PATTERN = re.compile(
    r"error TS[0-9]+|Unable to find a specification for|npm ERR!|"
    r"BUILD FAILED|BUILD FAILURE|GRADLE.*FAILED|pod install.*fail|"
    r"Cannot find module |Module not found:|"
    r"Test Suites:.*[1-9][0-9]* failed|Tests:.*[1-9][0-9]* failed|"
    r"NitroModules.*not found|jest.*FAIL |ModuleNotFoundError|ImportError|"
    r"AssertionError|FAILED tests/|cannot find package|^FAIL[ \t]|"
    r"undefined:|error\[E[0-9]+\]|panicked at|Compilation failure|"
    r"> Task .* FAILED|OperationFailure|requires authentication",
    re.IGNORECASE | re.DOTALL,
)


def collect_text(data):
    """Gather candidate output strings from known hook schemas."""
    texts = []
    if isinstance(data, dict):
        # Claude Code schema
        resp = data.get("tool_response")
        if isinstance(resp, dict):
            for key in ("output", "stdout", "stderr"):
                val = resp.get(key)
                if isinstance(val, str) and val:
                    texts.append(val)
        elif isinstance(resp, str) and resp:
            texts.append(resp)
        # Codex CLI schema variants
        for key in ("tool_output", "output", "stdout", "stderr", "result"):
            val = data.get(key)
            if isinstance(val, str) and val:
                texts.append(val)
            elif isinstance(val, dict):
                for sub in ("output", "stdout", "stderr", "text"):
                    sval = val.get(sub)
                    if isinstance(sval, str) and sval:
                        texts.append(sval)
    return texts


def main():
    try:
        raw = sys.stdin.read()
    except Exception:
        return 0
    if not raw.strip():
        return 0
    try:
        data = json.loads(raw)
    except Exception:
        return 0

    texts = collect_text(data)
    sample = "\n".join(texts)[:8192]
    if not sample:
        return 0
    if PATTERN.search(sample):
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": (
                    "[EFL] Build/test error detected. Run error-fixer-loop: "
                    "capture -> root-cause -> classify -> minimal fix -> test "
                    "-> lint/typecheck -> persist rule."
                ),
            }
        }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
