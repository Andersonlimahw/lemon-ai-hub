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

echo "=== All symlinks configured successfully! ==="
