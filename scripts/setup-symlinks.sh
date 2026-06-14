#!/usr/bin/env bash

# setup-symlinks.sh - Configure sharing of skills across agents
# This script creates symlinks from agent home directories to this repository's skills/ folder.
# Supported agents: Claude Code, Codex, Codex App, Gemini, Agy, OpenCode.

set -euo pipefail

# Get the absolute path of the repository's skills directory
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_SKILLS_DIR="$REPO_ROOT/skills"

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

echo "=== Lemon AI Hub: Multi-Agent Symlink Setup ==="

# 1. Claude Code
setup_symlink "$REPO_SKILLS_DIR" "~/.claude/skills"

# 2. Codex & Codex App
setup_symlink "$REPO_SKILLS_DIR" "~/.codex/skills"

# 3. Gemini
setup_symlink "$REPO_SKILLS_DIR" "~/.gemini/skills"

# 4. Agy (Antigravity)
setup_symlink "$REPO_SKILLS_DIR" "~/.agy/skills"

# 5. OpenCode
setup_symlink "$REPO_SKILLS_DIR" "~/.opencode/skills"

echo "=== All symlinks configured successfully! ==="
echo "Skills from $REPO_SKILLS_DIR are now available in all agents."
