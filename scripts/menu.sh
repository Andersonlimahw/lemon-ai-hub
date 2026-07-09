#!/usr/bin/env bash

# Lemon AI Hub - Interactive Menu

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}=======================================${NC}"
echo -e "${GREEN}      🍋 Lemon AI Hub Menu 🍋          ${NC}"
echo -e "${BLUE}=======================================${NC}"
echo ""
echo "Select an option:"
echo "1) 🧩 Add Marketplace to Claude Code"
echo "2) 🔗 Setup Symlinks for All Agents"
echo "3) 🤖 Setup Symlink for a Specific Agent"
echo "4) 🚪 Exit"
echo ""

read -p "Enter your choice [1-4]: " choice

case $choice in
  1)
    echo -e "${YELLOW}Running: /plugin marketplace add Andersonlimahw/lemon-ai-hub${NC}"
    echo "Note: You must run this command inside an active Claude Code session."
    echo "Please open Claude Code and paste:"
    echo -e "${GREEN}/plugin marketplace add Andersonlimahw/lemon-ai-hub${NC}"
    ;;
  2)
    echo -e "${YELLOW}Setting up symlinks for all agents...${NC}"
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    if [ -f "$SCRIPT_DIR/setup-symlinks.sh" ]; then
      bash "$SCRIPT_DIR/setup-symlinks.sh"
    else
      echo "Error: setup-symlinks.sh not found."
    fi
    ;;
  3)
    echo ""
    echo "Which agent do you want to configure?"
    echo "a) Claude Code"
    echo "b) Codex"
    echo "c) Gemini"
    echo "d) OpenCode"
    echo "e) Agy (Antigravity)"
    read -p "Select agent [a-e]: " agent_choice
    
    REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
    REPO_PLUGINS_DIR="$REPO_ROOT/plugins"
    
    case $agent_choice in
      a) TARGET="~/.claude/skills" ;;
      b) TARGET="~/.codex/skills" ;;
      c) TARGET="~/.gemini/skills" ;;
      d) TARGET="~/.opencode/skills" ;;
      e) TARGET="~/.agy/skills" ;;
      *) echo "Invalid choice."; exit 1 ;;
    esac
    
    TARGET="${TARGET/#\~/$HOME}"
    echo -e "${YELLOW}Setting up symlink for: $TARGET${NC}"
    
    if [ -d "$TARGET" ] && [ ! -L "$TARGET" ]; then
      BACKUP="${TARGET}_bak_$(date +%s)"
      echo "Warning: Directory exists. Backing up to $BACKUP"
      mv "$TARGET" "$BACKUP"
    elif [ -L "$TARGET" ] || [ -e "$TARGET" ]; then
      rm -f "$TARGET"
    fi
    
    mkdir -p "$(dirname "$TARGET")"
    ln -s "$REPO_PLUGINS_DIR" "$TARGET"
    echo -e "${GREEN}Created: $TARGET -> $REPO_PLUGINS_DIR${NC}"
    ;;
  4)
    echo "Exiting..."
    exit 0
    ;;
  *)
    echo "Invalid choice."
    exit 1
    ;;
esac
