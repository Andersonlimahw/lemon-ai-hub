#!/usr/bin/env bash
# ============================================================================
# Agentic Value Loops Plugin — Installation Script
# ============================================================================

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

PLUGIN_NAME="agentic-value-loops"
PLUGIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo -e "${CYAN}🔄 Agentic Value Loops Installer${NC}"
echo -e "${CYAN}══════════════════════════════════${NC}"
echo ""

# Detect target CLI
detect_cli() {
    local targets=()

    if [ -d "$HOME/.claude" ]; then
        targets+=("claude")
    fi

    if [ -d "$HOME/.gemini" ]; then
        targets+=("gemini")
    fi

    echo "${targets[@]}"
}

# Install for Claude Code
install_claude() {
    local claude_plugins="$HOME/.claude/plugins"
    local claude_skills="$HOME/.claude/skills"
    local claude_agents="$HOME/.claude/agents"

    echo -e "${MAGENTA}📦 Installing for Claude Code...${NC}"

    mkdir -p "$claude_plugins" "$claude_agents" "$claude_skills"

    if [ -L "$claude_plugins/$PLUGIN_NAME" ]; then rm "$claude_plugins/$PLUGIN_NAME"; fi
    ln -sf "$PLUGIN_DIR" "$claude_plugins/$PLUGIN_NAME"

    for agent_file in "$PLUGIN_DIR/agents/"*.md; do
        if [ -f "$agent_file" ]; then
            local basename=$(basename "$agent_file")
            if [ -L "$claude_agents/$basename" ]; then rm "$claude_agents/$basename"; fi
            ln -sf "$agent_file" "$claude_agents/$basename"
            echo -e "  ${GREEN}✓${NC} Agent linked: $basename"
        fi
    done

    for skill_dir in "$PLUGIN_DIR/skills/"*/; do
        if [ -d "$skill_dir" ]; then
            local skill_name=$(basename "$skill_dir")
            if [ -L "$claude_skills/$skill_name" ]; then rm "$claude_skills/$skill_name"; fi
            ln -sf "$skill_dir" "$claude_skills/$skill_name"
            echo -e "  ${GREEN}✓${NC} Skill linked: $skill_name"
        fi
    done

    echo -e "  ${GREEN}✅ Claude Code installation complete${NC}"
}

# Install for Gemini CLI
install_gemini() {
    local gemini_config="$HOME/.gemini/config"
    local gemini_plugins="$gemini_config/plugins"
    local gemini_skills="$gemini_config/skills"

    echo -e "${MAGENTA}📦 Installing for Gemini CLI...${NC}"

    mkdir -p "$gemini_plugins" "$gemini_skills"

    if [ -L "$gemini_plugins/$PLUGIN_NAME" ]; then rm "$gemini_plugins/$PLUGIN_NAME"; fi
    ln -sf "$PLUGIN_DIR" "$gemini_plugins/$PLUGIN_NAME"

    for skill_dir in "$PLUGIN_DIR/skills/"*/; do
        if [ -d "$skill_dir" ]; then
            local skill_name=$(basename "$skill_dir")
            if [ -L "$gemini_skills/$skill_name" ]; then rm "$gemini_skills/$skill_name"; fi
            ln -sf "$skill_dir" "$gemini_skills/$skill_name"
            echo -e "  ${GREEN}✓${NC} Skill linked: $skill_name"
        fi
    done

    echo -e "  ${GREEN}✅ Gemini CLI installation complete${NC}"
}

echo -e "${YELLOW}Detecting installed AI CLIs...${NC}"
TARGETS=($(detect_cli))

if [ ${#TARGETS[@]} -eq 0 ]; then
    echo -e "${RED}❌ No supported AI CLI found (Claude Code or Gemini CLI)${NC}"
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

echo -e "${CYAN}══════════════════════════════════${NC}"
echo -e "${GREEN}🎉 Installation complete!${NC}"
echo ""
echo -e "${CYAN}Agent:${NC}"
echo -e "  🔄 loop-orchestrator — Maestro of Value Loops"
echo ""
echo -e "${YELLOW}Usage: Mention @loop-orchestrator in your prompt!${NC}"
