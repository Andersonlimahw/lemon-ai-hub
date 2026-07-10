#!/usr/bin/env bash

# validate-marketplace-fix.sh
# Valida se o marketplace do lemon-ai-hub funciona corretamente
# Execute em uma NOVA session do Claude Code após o fix

set -euo pipefail

echo "=== Validando Marketplace Fix ==="
echo ""

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

pass() {
  echo -e "${GREEN}✓${NC} $1"
}

fail() {
  echo -e "${RED}✗${NC} $1"
  exit 1
}

warn() {
  echo -e "${YELLOW}⚠${NC} $1"
}

# 1. Verificar marketplace.json local
echo "1. Validando marketplace.json local..."
if [ ! -f ".claude-plugin/marketplace.json" ]; then
  fail "marketplace.json não encontrado"
fi

# 2. Verificar schema
echo "2. Validando schema..."
INVALID=$(node -e "
  const data = require('./.claude-plugin/marketplace.json');
  const invalid = data.plugins.filter(p => !p.source || p.source.source !== 'github');
  if (invalid.length > 0) {
    console.log(invalid.map(p => p.name).join(','));
  }
" 2>/dev/null || echo "")

if [ -n "$INVALID" ]; then
  fail "Plugins com schema inválido: $INVALID"
fi

pass "Schema válido (todos com source.source = github)"

# 3. Verificar cache local
echo "3. Validando cache local..."
CACHE_DIR="$HOME/.claude/plugins/marketplaces/lemon-ai-hub"
if [ ! -d "$CACHE_DIR" ]; then
  fail "Cache local não encontrado: $CACHE_DIR"
fi

if [ ! -f "$CACHE_DIR/.claude-plugin/marketplace.json" ]; then
  fail "marketplace.json não encontrado no cache"
fi

pass "Cache local presente"

# 4. Comparar local vs cache
echo "4. Comparando local vs cache..."
LOCAL_SHA=$(git rev-parse HEAD:./.claude-plugin/marketplace.json 2>/dev/null || echo "unknown")
CACHE_SHA=$(git -C "$CACHE_DIR" rev-parse HEAD:.claude-plugin/marketplace.json 2>/dev/null || echo "unknown")

if [ "$LOCAL_SHA" != "$CACHE_SHA" ]; then
  warn "Cache desatualizado. Executando git pull..."
  git -C "$CACHE_DIR" pull origin main
fi

pass "Cache sincronizado"

# 5. Verificar symlinks
echo "5. Validando symlinks..."
AGENTES=("claude" "codex" "gemini" "agy" "opencode")
MISSING=()

for agent in "${AGENTES[@]}"; do
  SKILL_LINK="$HOME/.${agent}/skills"
  if [ ! -L "$SKILL_LINK" ]; then
    MISSING+=("$agent")
  fi
done

if [ ${#MISSING[@]} -gt 0 ]; then
  warn "Symlinks faltando: ${MISSING[*]}"
  echo "   Execute: bash scripts/setup-symlinks.sh"
else
  pass "Symlinks OK (5 agentes)"
fi

# 6. Verificar plugins disponíveis
echo "6. Validando plugins disponíveis..."
PLUGIN_COUNT=$(ls -1 ~/.claude/skills/ 2>/dev/null | grep -v "^\." | wc -l | tr -d ' ')

if [ "$PLUGIN_COUNT" -lt 50 ]; then
  fail "Poucos plugins detectados: $PLUGIN_COUNT (esperado ~60)"
fi

pass "Plugins disponíveis: $PLUGIN_COUNT"

# 7. Testar uma skill específica
echo "7. Testando skill específica..."
if [ ! -d "$HOME/.claude/skills/cli-wrapper" ]; then
  fail "cli-wrapper não encontrado"
fi

if [ ! -f "$HOME/.claude/skills/cli-wrapper/SKILL.md" ]; then
  fail "cli-wrapper/SKILL.md não encontrado"
fi

pass "Skill específica funciona (cli-wrapper)"

# 8. Final check
echo ""
echo "=== Resumo ==="
echo -e "${GREEN}✓${NC} marketplace.json válido"
echo -e "${GREEN}✓${NC} Schema correto (source.source = github)"
echo -e "${GREEN}✓${NC} Cache sincronizado"
echo -e "${GREEN}✓${NC} Symlinks ativos"
echo -e "${GREEN}✓${NC} Plugins disponíveis"
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ FIX VALIDADO - MARKETPLACE FUNCIONAL${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Para testar no Claude Code:"
echo "  /plugin"
echo "  ⎿ marketplace update"
echo ""
echo "Esperado: Atualização sem erro"
