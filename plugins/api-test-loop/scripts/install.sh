#!/usr/bin/env bash
# ============================================================================
# API Test Loop Plugin — Installation Script
# ============================================================================

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

PLUGIN_NAME="api-test-loop"
PLUGIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo -e "${CYAN}🔄 API Test Loop Installer${NC}"
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

    if [ -d "$HOME/.codex" ]; then
        targets+=("codex")
    fi

    if [ -d "$HOME/.agy" ]; then
        targets+=("agy")
    fi

    if [ -d "$HOME/.opencode" ]; then
        targets+=("opencode")
    fi

    echo "${targets[@]}"
}

# Install for a specific CLI
install_for_cli() {
    local cli_name="$1"
    local cli_home="$HOME/.$cli_name"
    local cli_plugins="$cli_home/plugins"
    local cli_skills="$cli_home/skills"
    local cli_agents="$cli_home/agents"

    echo -e "${MAGENTA}📦 Installing for ${cli_name}...${NC}"

    mkdir -p "$cli_plugins" "$cli_agents" "$cli_skills"

    # Link the plugin directory
    if [ -L "$cli_plugins/$PLUGIN_NAME" ]; then rm "$cli_plugins/$PLUGIN_NAME"; fi
    ln -sf "$PLUGIN_DIR" "$cli_plugins/$PLUGIN_NAME"

    # Link agents
    for agent_file in "$PLUGIN_DIR/agents/"*.md; do
        if [ -f "$agent_file" ]; then
            local basename=$(basename "$agent_file")
            if [ -L "$cli_agents/$basename" ]; then rm "$cli_agents/$basename"; fi
            ln -sf "$agent_file" "$cli_agents/$basename"
            echo -e "  ${GREEN}✓${NC} Agent linked: $basename"
        fi
    done

    # Link skill if needed
    if [ -f "$PLUGIN_DIR/SKILL.md" ]; then
        if [ -L "$cli_skills/$PLUGIN_NAME" ]; then rm "$cli_skills/$PLUGIN_NAME"; fi
        # Symlink the entire plugin folder under skills so the skill is auto-discovered
        ln -sf "$PLUGIN_DIR" "$cli_skills/$PLUGIN_NAME"
        echo -e "  ${GREEN}✓${NC} Skill linked: $PLUGIN_NAME"
    fi

    echo -e "  ${GREEN}✅ ${cli_name} installation complete${NC}"
}

echo -e "${YELLOW}Detecting installed AI CLIs...${NC}"
TARGETS=($(detect_cli))

if [ ${#TARGETS[@]} -eq 0 ]; then
    echo -e "${RED}❌ No supported AI CLI found (Claude, Gemini, Codex, Agy, OpenCode)${NC}"
    exit 1
fi

echo -e "${GREEN}Found: ${TARGETS[*]}${NC}"
echo ""

for target in "${TARGETS[@]}"; do
    install_for_cli "$target"
    echo ""
done

echo -e "${CYAN}══════════════════════════════════${NC}"
echo -e "${GREEN}🎉 Installation complete!${NC}"
echo ""
echo -e "${CYAN}Agents:${NC}"
echo -e "  🔴 api-validator — REST API Validation & security auditing"
echo -e "  🔵 api-fix-implementer — Surgical backend validation/safety repairs"
echo ""
echo -e "${YELLOW}Usage: Trigger @api-validator or run the api-test-loop skill!${NC}"
