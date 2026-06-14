#!/usr/bin/env bash
# ============================================================================
# Spotify Squad Plugin — Installation Script
# Installs the spotify-squad plugin into your Claude Code / Gemini CLI config
# ============================================================================

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

PLUGIN_NAME="spotify-squad"
PLUGIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo -e "${CYAN}🎯 Spotify Squad Plugin Installer${NC}"
echo -e "${CYAN}══════════════════════════════════${NC}"
echo ""

# Detect target CLI
detect_cli() {
    local targets=()

    # Claude Code
    if [ -d "$HOME/.claude" ]; then
        targets+=("claude")
    fi

    # Gemini CLI
    if [ -d "$HOME/.gemini" ]; then
        targets+=("gemini")
    fi

    echo "${targets[@]}"
}

# Install for Claude Code
install_claude() {
    local claude_plugins="$HOME/.claude/plugins"
    local claude_skills="$HOME/.claude/skills"

    echo -e "${MAGENTA}📦 Installing for Claude Code...${NC}"

    # Create plugins directory
    mkdir -p "$claude_plugins"

    # Symlink plugin
    if [ -L "$claude_plugins/$PLUGIN_NAME" ]; then
        rm "$claude_plugins/$PLUGIN_NAME"
    fi
    ln -sf "$PLUGIN_DIR" "$claude_plugins/$PLUGIN_NAME"
    echo -e "  ${GREEN}✓${NC} Plugin linked: $claude_plugins/$PLUGIN_NAME"

    # Symlink agents to .claude/agents/ (Claude discovers agents there)
    local claude_agents="$HOME/.claude/agents"
    mkdir -p "$claude_agents"
    for agent_file in "$PLUGIN_DIR/agents/"*.md; do
        local basename=$(basename "$agent_file")
        if [ -L "$claude_agents/$basename" ]; then
            rm "$claude_agents/$basename"
        fi
        ln -sf "$agent_file" "$claude_agents/$basename"
        echo -e "  ${GREEN}✓${NC} Agent linked: $basename"
    done

    # Symlink skills
    mkdir -p "$claude_skills"
    for skill_dir in "$PLUGIN_DIR/skills/"*/; do
        local skill_name=$(basename "$skill_dir")
        if [ -L "$claude_skills/$skill_name" ]; then
            rm "$claude_skills/$skill_name"
        fi
        ln -sf "$skill_dir" "$claude_skills/$skill_name"
        echo -e "  ${GREEN}✓${NC} Skill linked: $skill_name"
    done

    echo -e "  ${GREEN}✅ Claude Code installation complete${NC}"
}

# Install for Gemini CLI
install_gemini() {
    local gemini_config="$HOME/.gemini/config"
    local gemini_plugins="$gemini_config/plugins"
    local gemini_skills="$gemini_config/skills"

    echo -e "${MAGENTA}📦 Installing for Gemini CLI...${NC}"

    # Create directories
    mkdir -p "$gemini_plugins"
    mkdir -p "$gemini_skills"

    # Symlink plugin
    if [ -L "$gemini_plugins/$PLUGIN_NAME" ]; then
        rm "$gemini_plugins/$PLUGIN_NAME"
    fi
    ln -sf "$PLUGIN_DIR" "$gemini_plugins/$PLUGIN_NAME"
    echo -e "  ${GREEN}✓${NC} Plugin linked: $gemini_plugins/$PLUGIN_NAME"

    # Symlink skills individually (Gemini discovers skills from config/skills/)
    for skill_dir in "$PLUGIN_DIR/skills/"*/; do
        local skill_name=$(basename "$skill_dir")
        if [ -L "$gemini_skills/$skill_name" ]; then
            rm "$gemini_skills/$skill_name"
        fi
        ln -sf "$skill_dir" "$gemini_skills/$skill_name"
        echo -e "  ${GREEN}✓${NC} Skill linked: $skill_name"
    done

    echo -e "  ${GREEN}✅ Gemini CLI installation complete${NC}"
}

# Main
echo -e "${YELLOW}Detecting installed AI CLIs...${NC}"
TARGETS=($(detect_cli))

if [ ${#TARGETS[@]} -eq 0 ]; then
    echo -e "${RED}❌ No supported AI CLI found (Claude Code or Gemini CLI)${NC}"
    echo -e "${YELLOW}Supported directories: ~/.claude/ or ~/.gemini/${NC}"
    exit 1
fi

echo -e "${GREEN}Found: ${TARGETS[*]}${NC}"
echo ""

for target in "${TARGETS[@]}"; do
    case "$target" in
        claude) install_claude ;;
        gemini) install_gemini ;;
    esac
    echo ""
done

# Summary
echo -e "${CYAN}══════════════════════════════════${NC}"
echo -e "${GREEN}🎉 Installation complete!${NC}"
echo ""
echo -e "${CYAN}Squad Agents:${NC}"
echo -e "  🎼 squad-orchestrator  — Tech Lead / Orchestrator"
echo -e "  ⚙️  backend-engineer    — Backend Engineer"
echo -e "  🎨 frontend-engineer   — Frontend Engineer"
echo -e "  📱 mobile-engineer     — Mobile Engineer"
echo -e "  🔍 ux-researcher       — UX Researcher"
echo -e "  🎨 ui-designer         — UI/Visual Designer"
echo -e "  📋 product-manager     — Product Manager"
echo -e "  🔄 scrum-master        — Scrum Master"
echo -e "  🚀 devops-engineer     — DevOps Engineer"
echo -e "  🧪 qa-engineer         — QA Engineer"
echo -e "  📊 data-engineer       — Data Engineer"
echo -e "  🛡️  security-engineer   — Security Engineer"
echo ""
echo -e "${YELLOW}Usage: Just mention squad roles in your prompts!${NC}"
echo -e "  Example: \"I need to build a new feature for user authentication\""
echo -e "  The squad-orchestrator will decompose and delegate."
