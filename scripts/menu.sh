#!/usr/bin/env bash

# Lemon AI Hub - Interactive Setup Menu

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}=======================================${NC}"
echo -e "${GREEN}      🍋 Lemon AI Hub Setup 🍋         ${NC}"
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

install_symlink() {
  local target="$1"
  local link_name="$2"

  echo -e "Setting up symlink: ${BLUE}$link_name${NC} -> ${YELLOW}$target${NC}"

  # If it exists and is a directory (not a symlink)
  if [ -d "$link_name" ] && [ ! -L "$link_name" ]; then
    local backup="${link_name}_bak_$(date +%s)"
    echo -e "${YELLOW}Warning: Directory $link_name exists. Backing up to $backup${NC}"
    mv "$link_name" "$backup"
  # If it's a broken symlink or already exists, remove it to recreate
  elif [ -L "$link_name" ] || [ -e "$link_name" ]; then
    rm -f "$link_name"
  fi

  # Ensure parent directory exists
  mkdir -p "$(dirname "$link_name")"

  # Create symlink
  ln -s "$target" "$link_name"
  echo -e "${GREEN}Created: $link_name${NC}"
}

run_installer() {
  echo -e "\n${GREEN}--- Installation Wizard ---${NC}"
  echo "Select Installation Scope:"
  echo "1) Global (User profile, e.g., ~/.claude/skills)"
  echo "2) Project (Current directory, e.g., ./.claude/skills)"
  read -p "Choice [1-2]: " scope_choice

  local base_dir
  if [ "$scope_choice" = "2" ]; then
    base_dir="$PWD"
    echo -e "${YELLOW}Scope: Project ($base_dir)${NC}"
  else
    base_dir="$HOME"
    echo -e "${YELLOW}Scope: Global ($base_dir)${NC}"
  fi

  echo ""
  echo "Select Target Agent(s):"
  echo "1) All Agents"
  echo "2) Claude Code"
  echo "3) Codex"
  echo "4) Gemini"
  echo "5) OpenCode"
  echo "6) Agy (Antigravity)"
  read -p "Choice [1-6]: " agent_choice

  echo ""
  case $agent_choice in
    1)
      install_symlink "$REPO_PLUGINS_DIR" "$base_dir/.claude/skills"
      install_symlink "$REPO_PLUGINS_DIR" "$base_dir/.codex/skills"
      install_symlink "$REPO_PLUGINS_DIR" "$base_dir/.gemini/skills"
      install_symlink "$REPO_PLUGINS_DIR" "$base_dir/.opencode/skills"
      install_symlink "$REPO_PLUGINS_DIR" "$base_dir/.agy/skills"
      ;;
    2) install_symlink "$REPO_PLUGINS_DIR" "$base_dir/.claude/skills" ;;
    3) install_symlink "$REPO_PLUGINS_DIR" "$base_dir/.codex/skills" ;;
    4) install_symlink "$REPO_PLUGINS_DIR" "$base_dir/.gemini/skills" ;;
    5) install_symlink "$REPO_PLUGINS_DIR" "$base_dir/.opencode/skills" ;;
    6) install_symlink "$REPO_PLUGINS_DIR" "$base_dir/.agy/skills" ;;
    *) echo -e "${RED}Invalid choice.${NC}"; return 1 ;;
  esac
  echo -e "${GREEN}Installation complete!${NC}\n"

  # Phase 3.5: per-harness agent frontmatter sync (same as setup-symlinks.sh).
  local SYNC_AGENTS="$REPO_ROOT/scripts/sync-agents.py"
  if [ -f "$SYNC_AGENTS" ]; then
    echo -e "${BLUE}=== Phase 3.5: Agent Frontmatter Sync ===${NC}"
    python3 "$SYNC_AGENTS" || echo -e "${YELLOW}WARNING: sync-agents.py failed. Run 'python3 $SYNC_AGENTS --verify' to inspect.${NC}" >&2
  fi
}

echo "Select an option:"
echo "1) 🚀 Install/Setup Symlinks (Interactive)"
echo "2) 🧩 Add Marketplace to Claude Code"
echo "3) 🔄 Update Marketplace Manifest (update_marketplace.py)"
echo "4) 🧹 Normalize Plugins Configs (normalize_plugins.py)"
echo "5) 🚪 Exit"
echo ""

read -p "Enter your choice [1-5]: " choice

case $choice in
  1)
    run_installer
    ;;
  2)
    echo -e "\n${YELLOW}To add the Lemon AI Hub marketplace, you must run this inside Claude Code:${NC}"
    echo -e "${GREEN}/plugin marketplace add Andersonlimahw/lemon-ai-hub${NC}\n"
    ;;
  3)
    echo -e "\n${YELLOW}Updating marketplace manifest...${NC}"
    if command -v python3 >/dev/null 2>&1; then
      cd "$REPO_ROOT" && python3 scripts/update_marketplace.py
    else
      echo -e "${RED}Python 3 is required but not found.${NC}"
    fi
    ;;
  4)
    echo -e "\n${YELLOW}Normalizing plugin configs...${NC}"
    if command -v python3 >/dev/null 2>&1; then
      cd "$REPO_ROOT" && python3 scripts/normalize_plugins.py
    else
      echo -e "${RED}Python 3 is required but not found.${NC}"
    fi
    ;;
  5)
    echo "Exiting..."
    exit 0
    ;;
  *)
    echo -e "${RED}Invalid choice.${NC}"
    exit 1
    ;;
esac
