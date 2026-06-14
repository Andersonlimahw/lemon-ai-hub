#!/usr/bin/env bash
# inject.sh - Injects Lemon AI Hub standards (Karpathy style) into the current project.
set -euo pipefail

HUB_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TARGET_AGENTS="AGENTS.md"
TARGET_CLAUDE="CLAUDE.md"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=== Lemon AI Hub: Injecting Karpathy Guidelines ===${NC}"

inject_file() {
  local src="$1"
  local dest="$2"
  
  if [ ! -f "$src" ]; then
    echo "Error: Source $src not found."
    return 1
  fi

  if [ -f "$dest" ]; then
    echo "Updating existing $dest..."
    # We prepend our standards and keep a marker
    if grep -q "Lemon AI Hub: Karpathy Standards" "$dest"; then
      echo "Standards already present in $dest. Updating content..."
      # Surgical replacement could be complex, for now we overwrite with Hub version 
      # but ideally we'd merge. Given the goal: replace/force standard.
      cat "$src" > "$dest"
    else
      echo "Backing up original $dest..."
      cp "$dest" "${dest}.bak_$(date +%s)"
      cat "$src" > "$dest"
    fi
  else
    echo "Creating new $dest..."
    cat "$src" > "$dest"
  fi
  echo -e "${GREEN}✔ $dest updated.${NC}"
}

inject_file "$HUB_ROOT/AGENTS.md" "$TARGET_AGENTS"
inject_file "$HUB_ROOT/CLAUDE.md" "$TARGET_CLAUDE"

echo -e "${BLUE}=== Injection Complete! ===${NC}"
echo "Your AI agent will now follow Andrej Karpathy's surgical coding style."
