#!/usr/bin/env bash

# setup-symlinks.sh - Configure sharing of skills across agents
# This script creates symlinks from agent home directories to this repository's plugins/ folder.
# Supported agents: Claude Code, Codex, Codex App, Gemini, Agy, OpenCode.

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

setup_symlink() {
  local target="$1"
  local link_name="$2"

  echo "Setting up symlink: $link_name -> $target"

  # Resolve ~ to $HOME
  link_name="${link_name/#\~/$HOME}"

  # If it exists and is a directory (not a symlink)
  if [ -d "$link_name" ] && [ ! -L "$link_name" ]; then
    local backup="${link_name}_bak_$(date +%s)"
    echo "Warning: Directory $link_name exists. Backing up to $backup"
    mv "$link_name" "$backup"
  # If it's a broken symlink or already exists, remove it to recreate
  elif [ -L "$link_name" ] || [ -e "$link_name" ]; then
    rm -f "$link_name"
  fi

  # Ensure parent directory exists
  mkdir -p "$(dirname "$link_name")"

  # Create symlink
  ln -s "$target" "$link_name"
  echo "Created: $link_name"
}

echo "=== Lemon AI Hub: Multi-Agent Symlink Setup (Plugins-based) ==="

# 1. Claude Code
setup_symlink "$REPO_PLUGINS_DIR" "~/.claude/skills"

# 2. Codex & Codex App
setup_symlink "$REPO_PLUGINS_DIR" "~/.codex/skills"

# 3. Gemini
setup_symlink "$REPO_PLUGINS_DIR" "~/.gemini/skills"

# 4. Agy (Antigravity)
setup_symlink "$REPO_PLUGINS_DIR" "~/.agy/skills"

# 5. OpenCode
setup_symlink "$REPO_PLUGINS_DIR" "~/.opencode/skills"

echo "=== All symlinks configured successfully! ==="
echo "Tools from $REPO_PLUGINS_DIR are now available in all agents."
