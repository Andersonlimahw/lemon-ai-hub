#!/usr/bin/env bash
# Adds minimal front-matter to docs/**/*.md missing it.
# Idempotent: skips files that already start with `---`.
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
DOCS="$ROOT/docs"
today=$(date -u +%Y-%m-%d)
count=0

while IFS= read -r -d '' f; do
  case "$f" in
    *"/adr/"*|*"/llms"*) continue ;;
  esac

  first=$(head -1 "$f" || true)
  [ "$first" = "---" ] && continue

  base="$(basename "$f" .md)"
  # Pretty title from filename
  title=$(printf '%s' "$base" | tr '_-' '  ' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)} 1')

  # Prefer existing H1 if present
  h1=$(awk '/^# / {sub(/^# /, ""); print; exit}' "$f")
  [ -n "$h1" ] && title="$h1"

  # Build new content with front-matter
  tmp=$(mktemp)
  {
    echo "---"
    printf 'title: %s\n' "$title"
    echo "status: draft"
    printf 'updated: %s\n' "$today"
    echo "related: []"
    echo "---"
    echo ""
    cat "$f"
  } > "$tmp"

  mv "$tmp" "$f"
  count=$((count+1))
done < <(find "$DOCS" -name "*.md" -print0)

echo "Backfilled front-matter in $count files."
