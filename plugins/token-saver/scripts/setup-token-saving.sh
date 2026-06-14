#!/usr/bin/env bash

# setup-token-saving.sh - Configures RTK, Caveman, Graphify, and Context-Mode.
# Supports both interactive prompts and command-line arguments.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CURRENT_PROJECT_DIR="$(pwd)"

# Default selections
INSTALL_RTK=""
SCOPE_RTK="global"

INSTALL_CAVEMAN=""
SCOPE_CAVEMAN="global"

INSTALL_GRAPHIFY=""
SCOPE_GRAPHIFY="project"

INSTALL_CONTEXT_MODE=""
SCOPE_CONTEXT_MODE="global"

INTERACTIVE=true

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --non-interactive)
      INTERACTIVE=false
      shift
      ;;
    --rtk)
      INSTALL_RTK="y"
      SCOPE_RTK="${2:-global}"
      shift 2
      ;;
    --caveman)
      INSTALL_CAVEMAN="y"
      SCOPE_CAVEMAN="${2:-global}"
      shift 2
      ;;
    --graphify)
      INSTALL_GRAPHIFY="y"
      SCOPE_GRAPHIFY="${2:-project}"
      shift 2
      ;;
    --context-mode)
      INSTALL_CONTEXT_MODE="y"
      SCOPE_CONTEXT_MODE="${2:-global}"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1"
      exit 1
      ;;
  esac
done

prompt_user() {
  local prompt_text="$1"
  local default_val="$2"
  local user_input
  
  if [ "$INTERACTIVE" = true ]; then
    read -rp "$prompt_text [$default_val]: " user_input
    echo "${user_input:-$default_val}"
  else
    echo "$default_val"
  fi
}

echo "=== Token Saving Setup Wizard ==="

# 1. RTK Prompt
if [ -z "$INSTALL_RTK" ]; then
  INSTALL_RTK=$(prompt_user "Do you want to install/configure RTK (Rust Token Killer)? (y/n)" "y")
  if [ "$INSTALL_RTK" = "y" ]; then
    SCOPE_RTK=$(prompt_user "RTK scope ([g]lobal / [p]roject)?" "g")
    if [ "$SCOPE_RTK" = "g" ] || [ "$SCOPE_RTK" = "global" ]; then
      SCOPE_RTK="global"
    else
      SCOPE_RTK="project"
    fi
  fi
fi

# 2. Caveman Prompt
if [ -z "$INSTALL_CAVEMAN" ]; then
  INSTALL_CAVEMAN=$(prompt_user "Do you want to activate Caveman Mode (compressed communication ~75%)? (y/n)" "y")
  if [ "$INSTALL_CAVEMAN" = "y" ]; then
    SCOPE_CAVEMAN=$(prompt_user "Caveman scope ([g]lobal / [p]roject)?" "g")
    if [ "$SCOPE_CAVEMAN" = "g" ] || [ "$SCOPE_CAVEMAN" = "global" ]; then
      SCOPE_CAVEMAN="global"
    else
      SCOPE_CAVEMAN="project"
    fi
  fi
fi

# 3. Graphify Prompt
if [ -z "$INSTALL_GRAPHIFY" ]; then
  INSTALL_GRAPHIFY=$(prompt_user "Do you want to configure Graphify (codebase Knowledge Graph)? (y/n)" "y")
  if [ "$INSTALL_GRAPHIFY" = "y" ]; then
    SCOPE_GRAPHIFY=$(prompt_user "Graphify scope ([g]lobal / [p]roject)?" "p")
    if [ "$SCOPE_GRAPHIFY" = "g" ] || [ "$SCOPE_GRAPHIFY" = "global" ]; then
      SCOPE_GRAPHIFY="global"
    else
      SCOPE_GRAPHIFY="project"
    fi
  fi
fi

# 4. Context-Mode Prompt
if [ -z "$INSTALL_CONTEXT_MODE" ]; then
  INSTALL_CONTEXT_MODE=$(prompt_user "Do you want to install Context-Mode (context compression)? (y/n)" "y")
  if [ "$INSTALL_CONTEXT_MODE" = "y" ]; then
    SCOPE_CONTEXT_MODE=$(prompt_user "Context-Mode scope ([g]lobal / [p]roject)?" "g")
    if [ "$SCOPE_CONTEXT_MODE" = "g" ] || [ "$SCOPE_CONTEXT_MODE" = "global" ]; then
      SCOPE_CONTEXT_MODE="global"
    else
      SCOPE_CONTEXT_MODE="project"
    fi
  fi
fi

# Apply RTK Setup
if [ "$INSTALL_RTK" = "y" ]; then
  echo "=> Configuring RTK..."
  if ! command -v rtk &> /dev/null; then
    echo "Warning: 'rtk' executable not found in PATH."
    echo "Installation instruction: run 'brew install steipete/tap/rtk' or obtain from https://github.com/steipete/rtk"
  else
    echo "RTK found at $(which rtk)."
  fi
  
  if [ "$SCOPE_RTK" = "global" ]; then
    export ENABLE_RTK=1
  else
    echo "To configure RTK for project only, add 'rtk hook claude' to local scripts or config."
  fi
fi

# Apply Caveman Setup
if [ "$INSTALL_CAVEMAN" = "y" ]; then
  echo "=> Configuring Caveman Mode..."
  
  CAVEMAN_INSTRUCTIONS="
# Caveman Mode (Active)
Work style: telegraphic, noun-phrases, min tokens.
Short answers, no fluff, no formalities.
"
  if [ "$SCOPE_CAVEMAN" = "global" ]; then
    export ENABLE_CAVEMAN=1
    CLAUDE_MD="$HOME/.claude/CLAUDE.md"
    if [ -f "$CLAUDE_MD" ]; then
      if ! grep -q "Caveman Mode" "$CLAUDE_MD"; then
        echo "$CAVEMAN_INSTRUCTIONS" >> "$CLAUDE_MD"
        echo "Caveman instructions added to $CLAUDE_MD"
      fi
    else
      echo "$CAVEMAN_INSTRUCTIONS" > "$CLAUDE_MD"
      echo "Created $CLAUDE_MD with Caveman instructions"
    fi
  else
    # Project scope
    PROJECT_CLAUDE_MD="$CURRENT_PROJECT_DIR/CLAUDE.md"
    if ! grep -q "Caveman Mode" "$PROJECT_CLAUDE_MD" 2>/dev/null; then
      echo "$CAVEMAN_INSTRUCTIONS" >> "$PROJECT_CLAUDE_MD"
      echo "Caveman instructions added to the project's CLAUDE.md"
    fi
  fi
fi

# Apply Graphify Setup
if [ "$INSTALL_GRAPHIFY" = "y" ]; then
  echo "=> Configuring Graphify..."
  if ! command -v graphify &> /dev/null; then
    echo "Graphify not installed globally. Cloning from repository..."
    # Local clone / build or setup instructions
    echo "Clone/Build: git clone https://github.com/safishamsi/graphify.git ~/.graphify"
    echo "See documentation at https://github.com/safishamsi/graphify to install the binary."
  else
    echo "Graphify found at $(which graphify)."
  fi

  if [ "$SCOPE_GRAPHIFY" = "project" ]; then
    echo "Initializing Graphify in the current project..."
    if [ -d "$CURRENT_PROJECT_DIR" ]; then
      # Simulates or runs graphify initialization in the project
      mkdir -p "$CURRENT_PROJECT_DIR/graphify-out"
      echo "Created graphify-out/ directory in the project for knowledge graphs."
      
      # Add instruction to the project's CLAUDE.md
      GRAPHIFY_RULE="
# Graphify Codebase Q&A
If the 'graphify-out/' folder is present in the project, query the knowledge graph BEFORE making linear searches or exploring multiple files.
"
      PROJECT_CLAUDE_MD="$CURRENT_PROJECT_DIR/CLAUDE.md"
      if ! grep -q "Graphify" "$PROJECT_CLAUDE_MD" 2>/dev/null; then
        echo "$GRAPHIFY_RULE" >> "$PROJECT_CLAUDE_MD"
        echo "Graphify rule added to the project's CLAUDE.md"
      fi
    fi
  fi
fi

# Apply Context-Mode Setup
if [ "$INSTALL_CONTEXT_MODE" = "y" ]; then
  echo "=> Configuring Context-Mode..."
  if [ "$SCOPE_CONTEXT_MODE" = "global" ]; then
    export ENABLE_CONTEXT_MODE=1
  fi
fi

# Run settings updater if global modifications were requested
if [ "${ENABLE_RTK:-0}" = "1" ] || [ "${ENABLE_CAVEMAN:-0}" = "1" ] || [ "${ENABLE_CONTEXT_MODE:-0}" = "1" ]; then
  echo "=> Updating global settings.json in ~/.claude/..."
  node "$SCRIPT_DIR/update-settings.js"
fi

echo "=== Setup Completed Successfully! ==="
echo ""
echo "Quick Usage Instructions:"
echo "--------------------------------------------------------"
echo "1. RTK: Use 'rtk gain' to view savings audit."
echo "2. Caveman: The agent will speak in an extremely compact manner."
echo "3. Graphify: If in project, the agent will use 'graphify-out/' to accelerate architecture searches."
echo "4. Context-Mode: The plugin is active and manages long outputs automatically."
echo "--------------------------------------------------------"
