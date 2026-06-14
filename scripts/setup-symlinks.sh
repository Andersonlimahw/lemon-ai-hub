#!/usr/bin/env bash

# setup-symlinks.sh - Configure sharing of skills across agents
# Primary target: ~/.claude/skills points to this repository's skills directory.
# Other agents (.codex, .opencode, .agy) point to ~/.claude/skills.

set -euo pipefail

REPO_SKILLS_DIR="/Users/andersonlimadev/Projects/IA/lemon-ai-hub/skills"

setup_symlink() {
  local target="$1"
  local link_name="$2"

  echo "Setting up symlink: $link_name -> $target"

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
  echo "Created: $link_name -> $(readlink "$link_name")"
}

echo "=== Lemon AI Hub: Setting up Agent Symlinks ==="

# 1. Point ~/.claude/skills to our repository skills directory
setup_symlink "$REPO_SKILLS_DIR" "$HOME/.claude/skills"

# 2. Point other agents' skills to ~/.claude/skills
setup_symlink "$HOME/.claude/skills" "$HOME/.codex/skills"
setup_symlink "$HOME/.claude/skills" "$HOME/.opencode/skills"
setup_symlink "$HOME/.claude/skills" "$HOME/.agy/skills"

echo "=== Symlinks configured successfully! ==="
