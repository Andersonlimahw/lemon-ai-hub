#!/usr/bin/env bash

# Lemon AI Hub - Interactive Menu

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}=======================================${NC}"
echo -e "${GREEN}      🍋 Lemon AI Hub Menu 🍋          ${NC}"
echo -e "${BLUE}=======================================${NC}"
echo ""

# Ensure we have the repository cloned or are inside it
if [ -d "$PWD/plugins" ] && [ -d "$PWD/.git" ]; then
  REPO_ROOT="$PWD"
else
  REPO_ROOT="$HOME/.lemon-ai-hub"
  echo -e "${YELLOW}Not running inside the Lemon AI Hub repository.${NC}"
  echo -e "Setting up Lemon AI Hub at ${BLUE}$REPO_ROOT${NC}..."
  if [ ! -d "$REPO_ROOT" ]; then
    git clone https://github.com/Andersonlimahw/lemon-ai-hub.git "$REPO_ROOT"
  else
    git -C "$REPO_ROOT" pull
  fi
  echo ""
fi
REPO_PLUGINS_DIR="$REPO_ROOT/plugins"

echo "Select an option:"
echo "1) 🧩 Add Marketplace to Claude Code"
echo "2) 🔗 Setup Symlinks for All Agents"
echo "3) 🤖 Setup Symlink for a Specific Agent"
echo "4) 🔄 Update Marketplace Manifest (update_marketplace.py)"
echo "5) 🧹 Normalize Plugins Configs (normalize_plugins.py)"
echo "6) 🚪 Exit"
echo ""

read -p "Enter your choice [1-6]: " choice

case $choice in
  1)
    echo -e "\n${YELLOW}To add the Lemon AI Hub marketplace, you must run this inside Claude Code:${NC}"
    echo -e "${GREEN}/plugin marketplace add Andersonlimahw/lemon-ai-hub${NC}\n"
    ;;
  2)
    echo -e "\n${YELLOW}Setting up symlinks for all agents...${NC}"
    if [ -f "$REPO_ROOT/scripts/setup-symlinks.sh" ]; then
      bash "$REPO_ROOT/scripts/setup-symlinks.sh"
    else
      echo -e "${RED}Error: setup-symlinks.sh not found in $REPO_ROOT/scripts${NC}"
    fi
    ;;
  3)
    echo ""
    echo "Which agent do you want to configure?"
    echo "a) Claude Code (~/.claude/skills)"
    echo "b) Codex (~/.codex/skills)"
    echo "c) Gemini (~/.gemini/skills)"
    echo "d) OpenCode (~/.opencode/skills)"
    echo "e) Agy / Antigravity (~/.agy/skills)"
    read -p "Select agent [a-e]: " agent_choice
    
    case $agent_choice in
      a) TARGET="~/.claude/skills" ;;
      b) TARGET="~/.codex/skills" ;;
      c) TARGET="~/.gemini/skills" ;;
      d) TARGET="~/.opencode/skills" ;;
      e) TARGET="~/.agy/skills" ;;
      *) echo -e "${RED}Invalid choice.${NC}"; exit 1 ;;
    esac
    
    TARGET="${TARGET/#\~/$HOME}"
    echo -e "\n${YELLOW}Setting up symlink for: $TARGET${NC}"
    
    if [ -d "$TARGET" ] && [ ! -L "$TARGET" ]; then
      BACKUP="${TARGET}_bak_$(date +%s)"
      echo "Warning: Directory exists. Backing up to $BACKUP"
      mv "$TARGET" "$BACKUP"
    elif [ -L "$TARGET" ] || [ -e "$TARGET" ]; then
      rm -f "$TARGET"
    fi
    
    mkdir -p "$(dirname "$TARGET")"
    ln -s "$REPO_PLUGINS_DIR" "$TARGET"
    echo -e "${GREEN}Created: $TARGET -> $REPO_PLUGINS_DIR${NC}\n"
    ;;
  4)
    echo -e "\n${YELLOW}Updating marketplace manifest...${NC}"
    if command -v python3 >/dev/null 2>&1; then
      cd "$REPO_ROOT" && python3 scripts/update_marketplace.py
    else
      echo -e "${RED}Python 3 is required but not found.${NC}"
    fi
    ;;
  5)
    echo -e "\n${YELLOW}Normalizing plugin configs...${NC}"
    if command -v python3 >/dev/null 2>&1; then
      cd "$REPO_ROOT" && python3 scripts/normalize_plugins.py
    else
      echo -e "${RED}Python 3 is required but not found.${NC}"
    fi
    ;;
  6)
    echo "Exiting..."
    exit 0
    ;;
  *)
    echo -e "${RED}Invalid choice.${NC}"
    exit 1
    ;;
esac
