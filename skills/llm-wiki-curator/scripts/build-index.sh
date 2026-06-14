#!/usr/bin/env bash
# Builds docs/llms.txt — flat LLM-friendly index per llmstxt.org.
# Karpathy-style: flat, link-rich, machine-parseable.
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
DOCS="$ROOT/docs"
OUT="$DOCS/llms.txt"

if [ ! -d "$DOCS" ]; then
  echo "error: $DOCS not found" >&2
  exit 1
fi

extract_title() {
  local f="$1"
  local t
  t=$(awk '/^title:/ {sub(/^title:[[:space:]]*/, ""); gsub(/^"|"$/, ""); print; exit}' "$f")
  if [ -z "$t" ]; then
    t=$(awk '/^# / {sub(/^# /, ""); print; exit}' "$f")
  fi
  [ -z "$t" ] && t="$(basename "$f" .md)"
  printf '%s' "$t"
}

extract_desc() {
  local f="$1"
  awk '
    /^---$/ { fm = !fm; next }
    fm { next }
    /^#/ { next }
    /^[[:space:]]*$/ { next }
    { gsub(/^[[:space:]]+|[[:space:]]+$/, ""); print; exit }
  ' "$f" | cut -c1-160
}

{
  echo "# AI Marketplace"
  echo ""
  echo "> Centralized workspace to share custom AI Skills and Plugins across Claude Code, Codex, OpenCode, and Antigravity (Agy)."
  echo ""
  echo "Last generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo ""

  # Top-level docs first
  echo "## Overview"
  echo ""
  find "$DOCS" -maxdepth 1 -name "*.md" -not -name "llms*.md" | sort | while read -r f; do
    rel="${f#"$ROOT/"}"
    title=$(extract_title "$f")
    desc=$(extract_desc "$f")
    if [ -n "$desc" ]; then
      echo "- [$title]($rel): $desc"
    else
      echo "- [$title]($rel)"
    fi
  done
  echo ""

  # Subdirectories
  find "$DOCS" -mindepth 1 -maxdepth 1 -type d | sort | while read -r dir; do
    name="$(basename "$dir")"
    pretty=$(echo "$name" | tr '_-' '  ' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)} 1')
    has_md=$(find "$dir" -name "*.md" | head -1)
    [ -z "$has_md" ] && continue

    echo "## $pretty"
    echo ""
    find "$dir" -name "*.md" | sort | while read -r f; do
      rel="${f#"$ROOT/"}"
      title=$(extract_title "$f")
      desc=$(extract_desc "$f")
      if [ -n "$desc" ]; then
        echo "- [$title]($rel): $desc"
      else
        echo "- [$title]($rel)"
      fi
    done
    echo ""
  done
} > "$OUT"

count=$(grep -c '^- \[' "$OUT" || true)
echo "docs/llms.txt regenerated — $count entries indexed"
