#!/usr/bin/env bash
# detect-error.sh — Standalone error-pattern detector.
# Reads stdin, exits 0 if a known build/test error pattern is found, 1 otherwise.
# Useful for wiring error-fixer-loop into arbitrary CI scripts, pre-push hooks,
# or other harnesses that don't support the native Claude/OpenCode plugin API.
#
# Usage:
#   npm test 2>&1 | ./detect-error.sh && echo "run error-fixer-loop"

set -u

input="$(cat || true)"
[ -z "$input" ] && exit 1

pattern='error TS[0-9]+|Unable to find a specification for|npm ERR!|BUILD FAILED|BUILD FAILURE|GRADLE.*FAILED|pod install.*fail|Cannot find module |Module not found:|Test Suites:.*[1-9][0-9]* failed|Tests:.*[1-9][0-9]* failed|NitroModules.*not found|jest.*FAIL |ModuleNotFoundError|ImportError|AssertionError|FAILED tests/|cannot find package|^FAIL[[:space:]]|undefined:|error\[E[0-9]+\]|panicked at|Compilation failure|> Task .* FAILED'

if printf '%s' "$input" | head -c 8192 | grep -Eiq "$pattern"; then
  exit 0
fi
exit 1
