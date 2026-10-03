#!/usr/bin/env bash
# Install minimax-subagents across harnesses. Idempotent; never touches keys.
#   bash install.sh            install / update
#   bash install.sh --dry-run  show what would change
set -euo pipefail

PLUGIN_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HUB_PLUGINS="$(dirname "$PLUGIN_DIR")"
DRY=0
[ "${1:-}" = "--dry-run" ] && DRY=1

run() { if [ "$DRY" = 1 ]; then echo "DRY: $*"; else "$@"; fi; }

# 1. mm-run on PATH for every harness shell.
run mkdir -p "$HOME/.local/bin"
run ln -sfn "$PLUGIN_DIR/bin/mm-run" "$HOME/.local/bin/mm-run"
echo "LINK ~/.local/bin/mm-run -> $PLUGIN_DIR/bin/mm-run"

# 2. Skill into curated skill dirs. A dir that resolves to ANY hub plugins/
# (this clone or another checkout) already sees the plugin; linking there
# would drop a stray symlink into that hub's working tree.
for dir in "$HOME/.config/opencode/skills" "$HOME/.gemini/skills" "$HOME/.gemini/config/skills" \
           "$HOME/.agy/skills" "$HOME/.antigravity/skills" "$HOME/.codex/skills" "$HOME/.agents/skills"; do
  [ -d "$dir" ] || continue
  resolved="$(cd -P "$dir" && pwd)"
  if [ -f "$resolved/smart-sub-agents/plugin.json" ]; then
    echo "SKIP $dir (resolves to a hub plugins/ dir: $resolved)"
    continue
  fi
  target="$dir/minimax-subagents"
  if [ -e "$target" ] && [ ! -L "$target" ]; then
    echo "KEEP $target (real directory, not managed)"
    continue
  fi
  run ln -sfn "$PLUGIN_DIR" "$target"
  echo "LINK $target"
done

# 3. Worker lane: OpenCode mm_* agents + Claude/Agy bridges (smart-sub-agents).
installer="$HUB_PLUGINS/smart-sub-agents/scripts/install_worker_matrix.py"
if [ -f "$installer" ]; then
  if [ "$DRY" = 1 ]; then
    python3 "$installer" --dry-run | grep -E "mm_|summary" || true
  else
    python3 "$installer" | grep -E "mm_|summary|OK|ERROR" || true
  fi
else
  echo "WARN: $installer not found; workers not installed (mm-run falls back to -m)"
fi

# 4. Preflight (does not read keys).
if [ "$DRY" = 0 ]; then
  "$PLUGIN_DIR/bin/mm-run" --check || echo "WARN: configure the OpenCode 'minimax' provider (see SKILL.md)"
fi

# 5. Codex sandbox note: not written automatically, it widens the sandbox.
if command -v codex >/dev/null 2>&1; then
  echo "NOTE Codex: run mm-run outside workspace-write or start Codex with the"
  echo "     network_access + writable_roots overrides from SKILL.md (Codex sandbox section)."
fi
