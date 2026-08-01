#!/usr/bin/env bash
# install.sh — Install error-fixer-loop hooks into every supported AI harness.
#
# Usage:
#   ./install.sh            # install into every harness present on this machine
#   ./install.sh claude     # Claude Code only
#   ./install.sh codex      # Codex CLI only
#   ./install.sh gemini     # Gemini CLI only
#   ./install.sh agy        # Agy / Antigravity only
#   ./install.sh opencode   # OpenCode only
#
# Claude, Codex, Gemini and Agy all consume the same POSIX shell hook and are
# installed from a single code path; only their config directory differs.
# OpenCode uses a TypeScript plugin instead, so it has its own installer.
#
# Idempotent: safe to run multiple times. Will not overwrite an existing
# hook that differs — it will print a warning and skip.

set -euo pipefail

PLUGIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OPENCODE_PLUGINS_DIR="${HOME}/.config/opencode/plugins"

# harness name -> config dir. Shell-hook harnesses only.
SHELL_HARNESSES="claude codex gemini agy"

harness_config_dir() {
  case "$1" in
    claude) echo "${HOME}/.claude" ;;
    codex)  echo "${HOME}/.codex" ;;
    gemini) echo "${HOME}/.gemini" ;;
    agy)    echo "${HOME}/.agy" ;;
    *)      return 1 ;;
  esac
}

target="${1:-all}"

# Installs the shell hook for one harness. Skips harnesses that are not
# installed on this machine so a partial setup is not treated as an error.
install_shell_harness() {
  local harness="$1"
  local config_dir
  config_dir="$(harness_config_dir "$harness")"

  if [ ! -d "$config_dir" ]; then
    echo "[install] SKIP: $harness not installed ($config_dir absent)"
    return 0
  fi

  local hooks_dir="${config_dir}/hooks"
  mkdir -p "$hooks_dir"
  local src="${PLUGIN_DIR}/hooks/error-fixer-loop-hook.sh"
  local dst="${hooks_dir}/error-fixer-loop-hook.sh"
  if [ -f "$dst" ] && ! cmp -s "$src" "$dst"; then
    echo "[install] WARN: $dst exists and differs. Skipping (review manually)." >&2
  else
    cp "$src" "$dst"
    chmod +x "$dst"
    echo "[install] $harness hook installed: $dst"
    echo "[install] Register it in ${config_dir}/settings.json under hooks.PostToolUse for tool=Bash"
  fi

  # Legacy cleanup: if the old error-fix-loop-hook.sh exists and is identical
  # to the new one, leave it; otherwise warn.
  local legacy="${hooks_dir}/error-fix-loop-hook.sh"
  if [ -f "$legacy" ]; then
    echo "[install] NOTE: legacy hook found at $legacy — consider removing after migration."
  fi
}

install_opencode() {
  if [ ! -d "${HOME}/.config/opencode" ] && [ ! -d "${HOME}/.opencode" ]; then
    echo "[install] SKIP: opencode not installed"
    return 0
  fi
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
  claude|codex|gemini|agy) install_shell_harness "$target" ;;
  opencode) install_opencode ;;
  all)
    for harness in $SHELL_HARNESSES; do
      install_shell_harness "$harness"
    done
    install_opencode
    ;;
  *) echo "usage: $0 [claude|codex|gemini|agy|opencode|all]" >&2; exit 2 ;;
esac
