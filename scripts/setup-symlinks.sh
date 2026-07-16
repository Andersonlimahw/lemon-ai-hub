#!/usr/bin/env bash

# setup-symlinks.sh - Configure sharing of skills across agents
# This script creates symlinks from agent home directories to this repository's plugins/ folder.
# Supported agents: Claude Code, Codex, Codex App, Gemini, Agy, OpenCode.
#
# Phase 3.5: after directory symlinks, sync agent frontmatter per-harness via
# scripts/sync-agents.py. Raw symlinks for `agents/` would feed Claude-format
# frontmatter to OpenCode/Agy/Gemini and break them (e.g. `tools:` is deprecated
# in OpenCode v1.1.1, `name:` is treated as a label, missing `description:` is
# a hard error). The sync emits per-harness materialized files with strict
# schema validation and fail-loud warnings for invalid keys.

set -euo pipefail

# Get the absolute path of the repository's plugins directory
if [ -d "$PWD/plugins" ] && [ -d "$PWD/.git" ]; then
  # Running from within a local clone
  REPO_ROOT="$PWD"
else
  # Running via curl or outside the repo
  REPO_ROOT="$HOME/.lemon-ai-hub"
  echo "Setting up Lemon AI Hub at $REPO_ROOT..."
  if [ ! -d "$REPO_ROOT" ]; then
    git clone https://github.com/Andersonlimahw/lemon-ai-hub.git "$REPO_ROOT"
  else
    git -C "$REPO_ROOT" pull
  fi
fi
REPO_PLUGINS_DIR="$REPO_ROOT/plugins"
SYNC_AGENTS="$REPO_ROOT/scripts/sync-agents.py"

install_symlink() {
  local target="$1"
  local link_name="$2"

  echo "Setting up symlink: $link_name -> $target"

  link_name="${link_name/#\~/$HOME}"

  if [ -d "$link_name" ] && [ ! -L "$link_name" ]; then
    local backup="${link_name}_bak_$(date +%s)"
    echo "Warning: Directory $link_name exists. Backing up to $backup"
    mv "$link_name" "$backup"
  elif [ -L "$link_name" ] || [ -e "$link_name" ]; then
    rm -f "$link_name"
  fi

  mkdir -p "$(dirname "$link_name")"
  ln -s "$target" "$link_name"
  echo "Created: $link_name"
}

echo "=== Lemon AI Hub: Headless Symlink Setup ==="
echo "Scope: Global (~/)"
echo "Target: All Supported Agents"

install_symlink "$REPO_PLUGINS_DIR" "~/.claude/skills"
install_symlink "$REPO_PLUGINS_DIR" "~/.codex/skills"
install_symlink "$REPO_PLUGINS_DIR" "~/.gemini/skills"
install_symlink "$REPO_PLUGINS_DIR" "~/.agy/skills"
install_symlink "$REPO_PLUGINS_DIR" "~/.opencode/skills"

# Phase 3.5: per-harness agent frontmatter sync.
# Materializes transformed copies of plugins/cli-wrapper/agents/*.md into each
# harness's agents/ dir with the correct schema (drops `name` for OpenCode,
# drops `tools`, validates permission keys, emits Codex .toml sidecar).
if [ -f "$SYNC_AGENTS" ]; then
  echo ""
  echo "=== Phase 3.5: Agent Frontmatter Sync ==="
  if python3 "$SYNC_AGENTS"; then
    echo "Agent frontmatter synced across all harnesses."
  else
    echo "WARNING: sync-agents.py reported errors. Run 'python3 $SYNC_AGENTS --verify' to inspect." >&2
  fi
else
  echo "WARNING: $SYNC_AGENTS not found. Skipping per-harness agent sync." >&2
fi

echo "=== All symlinks configured successfully! ==="
