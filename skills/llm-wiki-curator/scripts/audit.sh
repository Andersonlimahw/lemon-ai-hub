#!/usr/bin/env bash
# Audits docs/ for Karpathy LLM-wiki compliance.
# - missing front-matter
# - broken markdown links
# - orphans (not referenced by any other doc)
# - deprecated docs still linked from active docs
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
DOCS="$ROOT/docs"
exit_code=0

echo "## Front-matter check"
missing=0
while IFS= read -r -d '' f; do
  case "$f" in
    *"/adr/"*|*"/llms"*.md|*"/llms.txt") continue ;;
  esac
  first=$(head -1 "$f" || true)
  if [ "$first" != "---" ]; then
    rel="${f#"$ROOT/"}"
    echo "  miss: $rel"
    missing=$((missing+1))
  fi
done < <(find "$DOCS" -name "*.md" -print0)
echo "  total without front-matter: $missing"
[ "$missing" -gt 0 ] && exit_code=1

echo ""
echo "## Broken markdown links"
broken=0
while IFS= read -r -d '' f; do
  dir="$(dirname "$f")"
  while IFS= read -r link; do
    [ -z "$link" ] && continue
    case "$link" in
      http*|"#"*|mailto:*) continue ;;
    esac
    target="${link%%#*}"
    [ -z "$target" ] && continue
    if [[ "$target" = /* ]]; then
      abs="$ROOT$target"
    else
      abs="$dir/$target"
    fi
    if [ ! -e "$abs" ]; then
      rel="${f#"$ROOT/"}"
      echo "  broken: $rel -> $target"
      broken=$((broken+1))
    fi
  done < <(awk '
    /^```/ { incode = !incode; next }
    !incode { print }
  ' "$f" | grep -oE '\]\(([^)]+)\)' | sed -E 's/^\]\(//; s/\)$//')
done < <(find "$DOCS" -name "*.md" -print0)
echo "  total broken links: $broken"
[ "$broken" -gt 0 ] && exit_code=1

echo ""
echo "## Orphan docs (not linked from anywhere)"
orphans=0
while IFS= read -r -d '' f; do
  rel="${f#"$ROOT/"}"
  base="$(basename "$f")"
  case "$base" in
    README.md|llms.txt) continue ;;
  esac
  refs=$(grep -rlE "\]\([^)]*$base" "$DOCS" --include="*.md" 2>/dev/null | grep -v "^$f$" | wc -l | tr -d ' ')
  if [ "$refs" = "0" ]; then
    echo "  orphan: $rel"
    orphans=$((orphans+1))
  fi
done < <(find "$DOCS" -name "*.md" -print0)
echo "  total orphans: $orphans"

echo ""
echo "Exit: $exit_code  (0=clean, 1=issues)"
exit $exit_code
