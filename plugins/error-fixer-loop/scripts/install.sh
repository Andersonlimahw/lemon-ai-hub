#!/usr/bin/env bash
# install.sh — Install error-fixer-loop hooks into Claude Code and OpenCode.
#
# Usage:
#   ./install.sh           # install both
#   ./install.sh claude    # Claude Code only
#   ./install.sh opencode  # OpenCode only
#
# Idempotent: safe to run multiple times. Will not overwrite an existing
# hook that differs — it will print a warning and skip.

set -euo pipefail

PLUGIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLAUDE_HOOKS_DIR="${HOME}/.claude/hooks"
OPENCODE_PLUGINS_DIR="${HOME}/.config/opencode/plugins"

target="${1:-all}"

install_claude() {
  mkdir -p "$CLAUDE_HOOKS_DIR"
  local src="${PLUGIN_DIR}/hooks/error-fixer-loop-hook.sh"
  local dst="${CLAUDE_HOOKS_DIR}/error-fixer-loop-hook.sh"
  if [ -f "$dst" ] && ! cmp -s "$src" "$dst"; then
    echo "[install] WARN: $dst exists and differs. Skipping (review manually)." >&2
  else
    cp "$src" "$dst"
    chmod +x "$dst"
    echo "[install] Claude hook installed: $dst"
    echo "[install] Register it in ~/.claude/settings.json under hooks.PostToolUse for tool=Bash"
  fi

  # Legacy cleanup: if the old error-fix-loop-hook.sh exists and is identical
  # to the new one, leave it; otherwise warn.
  local legacy="${CLAUDE_HOOKS_DIR}/error-fix-loop-hook.sh"
  if [ -f "$legacy" ]; then
    echo "[install] NOTE: legacy hook found at $legacy — consider removing after migration."
  fi
}

install_opencode() {
  mkdir -p "$OPENCODE_PLUGINS_DIR"
  local src="${PLUGIN_DIR}/hooks/error-fixer-loop.ts"
  local dst="${OPENCODE_PLUGINS_DIR}/error-fixer-loop.ts"
  if [ -f "$dst" ] && ! cmp -s "$src" "$dst"; then
    echo "[install] WARN: $dst exists and differs. Skipping (review manually)." >&2
  else
    cp "$src" "$dst"
    echo "[install] OpenCode plugin installed: $dst"
    echo "[install] OpenCode auto-discovers it on next session."
  fi

  local legacy="${OPENCODE_PLUGINS_DIR}/error-fix-loop.ts"
  if [ -f "$legacy" ]; then
    echo "[install] NOTE: legacy plugin found at $legacy — consider removing after migration."
  fi
}

case "$target" in
  claude)   install_claude ;;
  opencode) install_opencode ;;
  all)      install_claude; install_opencode ;;
  *) echo "usage: $0 [claude|opencode|all]" >&2; exit 2 ;;
esac
