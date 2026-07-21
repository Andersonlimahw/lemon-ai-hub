#!/usr/bin/env bash
# error-fixer-loop-hook.sh — Claude Code PostToolUse hook (Bash)
# Detects build/test/typecheck errors in bash output and reminds the agent
# to run the error-fixer-loop skill.
#
# Install (Claude Code):
#   Register in ~/.claude/settings.json:
#   {
#     "hooks": {
#       "PostToolUse": [
#         {
#           "matcher": "Bash",
#           "hooks": [
#             { "type": "command", "command": "~/.claude/hooks/error-fixer-loop-hook.sh" }
#           ]
#         }
#       ]
#     }
#   }
#
# Behavior:
#   - Reads JSON from stdin: { "tool_name": "...", "tool_response": { "output": "..." } }
#   - If tool is Bash AND output matches an error pattern, prints a one-line reminder to stdout.
#   - Always exits 0 (never blocks the tool).
#
# Source of truth: lemon-ai-hub/plugins/error-fixer-loop/hooks/error-fixer-loop-hook.sh
# Skill:           lemon-ai-hub/plugins/error-fixer-loop/SKILL.md

set -u

input="$(cat || true)"
[ -z "$input" ] && exit 0

# Fast path: not a Bash tool call.
printf '%s' "$input" | grep -q '"tool_name"[[:space:]]*:[[:space:]]*"Bash"' || exit 0

# Extract a sample of the tool output. We avoid jq to keep this hook
# dependency-free; sed is enough for a flat string field.
output="$(printf '%s' "$input" | sed -n 's/.*"output"[[:space:]]*:[[:space:]]*"\(.*\)"[,}].*/\1/p' | head -c 8192)"
if [ -z "$output" ]; then
  output="$(printf '%s' "$input" | sed -n 's/.*"stdout"[[:space:]]*:[[:space:]]*"\(.*\)"[,}].*/\1/p' | head -c 8192)"
fi
[ -z "$output" ] && exit 0

# Error patterns — keep in sync with hooks/error-fixer-loop.ts.
pattern='error TS[0-9]+|Unable to find a specification for|npm ERR!|BUILD FAILED|BUILD FAILURE|GRADLE.*FAILED|pod install.*fail|Cannot find module |Module not found:|Test Suites:.*[1-9][0-9]* failed|Tests:.*[1-9][0-9]* failed|NitroModules.*not found|jest.*FAIL |ModuleNotFoundError|ImportError|AssertionError|FAILED tests/|cannot find package|^FAIL[[:space:]]|undefined:|error\[E[0-9]+\]|panicked at|Compilation failure|> Task .* FAILED'

if printf '%s' "$output" | grep -Eiq "$pattern"; then
  printf '%s\n' '[EFL] Build/test error detected. Run error-fixer-loop: capture → root-cause → classify → minimal fix → test → lint/typecheck → persist rule (docs/rules or AGENTS.md) → audit with evidence.'
fi

exit 0
