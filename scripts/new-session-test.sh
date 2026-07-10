#!/usr/bin/env bash

# new-session-test.sh
# Execute em UMA NOVA SESSION do Claude Code para validar o marketplace fix
# Instruções:
# 1. Feche COMPLETAMENTE Claude Code
# 2. Abra NOVA session
# 3. Execute: bash scripts/new-session-test.sh

set -euo pipefail

echo "=========================================="
echo "MARKETPLACE FIX - NOVA SESSION TEST"
echo "=========================================="
echo ""
echo "Esta é uma NOVA session do Claude Code?"
echo ""
select yn in "Sim - ACABEI de abrir esta session" "Não - Esta é a mesma session"; do
    case $yn in
        Sim )
            echo "✓ Prosseguindo com validação..."
            break
            ;;
        Não )
            echo "❌ ERRO: Execute em uma NOVA session!"
            echo ""
            echo "Passos corretos:"
            echo "1. Feche COMPLETAMENTE Claude Code"
            echo "2. Abra NOVA session"
            echo "3. Execute: bash scripts/new-session-test.sh"
            exit 1
            ;;
    esac
done

echo ""
echo "=== Validando Marketplace Fix ==="
echo ""

# Cores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

pass() {
  echo -e "${GREEN}✓${NC} $1"
}

fail() {
  echo -e "${RED}✗${NC} $1"
  echo ""
  echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "${RED}❌ FIX FALHOU - CONTINUE O LOOP${NC}"
  echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  exit 1
}

# 1. Verificar se é realmente uma nova session
echo "1. Verificando se é nova session..."
SESSION_START=$(ps -p $$ -o lstart= 2>/dev/null || echo "unknown")
NOW=$(date +"%Y-%m-%d %H:%M:%S")
echo "   Session start: $SESSION_START"
echo "   Current time: $NOW"
echo ""

# 2. Verificar marketplace.json
echo "2. Validando marketplace.json..."
if [ ! -f ".claude-plugin/marketplace.json" ]; then
  fail "marketplace.json não encontrado"
fi

# 3. Verificar schema
echo "3. Validando schema..."
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

# 4. Verificar cache
echo "4. Validando cache..."
CACHE_DIR="$HOME/.claude/plugins/marketplaces/lemon-ai-hub"
if [ ! -d "$CACHE_DIR" ]; then
  fail "Cache não encontrado"
fi

if [ ! -f "$CACHE_DIR/.claude-plugin/marketplace.json" ]; then
  fail "marketplace.json não encontrado no cache"
fi

pass "Cache presente"

# 5. Verificar se cache está atualizado
echo "5. Comparando local vs cache..."
cd "$CACHE_DIR"
git fetch origin &>/dev/null
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u})

if [ "$LOCAL" != "$REMOTE" ]; then
  echo "   Cache desatualizado. Atualizando..."
  git pull origin main
fi

cd - >/dev/null
pass "Cache sincronizado"

# 6. Verificar symlinks
echo "6. Validando symlinks..."
SYMLINKS_OK=true
for agent in claude codex gemini agy opencode; do
  LINK="$HOME/.${agent}/skills"
  if [ ! -L "$LINK" ]; then
    echo "   ✗ $agent: symlink não existe"
    SYMLINKS_OK=false
  fi
done

if [ "$SYMLINKS_OK" = false ]; then
  fail "Symlinks faltando. Execute: bash scripts/setup-symlinks.sh"
fi

pass "Symlinks OK (5 agentes)"

# 7. Verificar plugins disponíveis
echo "7. Verificando plugins..."
PLUGIN_COUNT=$(ls -1 ~/.claude/skills/ 2>/dev/null | grep -v "^\." | wc -l | tr -d ' ')

if [ "$PLUGIN_COUNT" -lt 50 ]; then
  fail "Poucos plugins: $PLUGIN_COUNT (esperado ~60)"
fi

pass "Plugins disponíveis: $PLUGIN_COUNT"

# 8. TESTE FINAL - Tentar atualizar marketplace
echo ""
echo "8. TESTE FINAL - Atualizar marketplace..."
echo ""
echo -e "${BLUE}Instruções:${NC}"
echo "1. Execute no Claude Code (nesta NOVA session):"
echo "   /plugin"
echo "   ⎿ marketplace update"
echo ""
echo "2. Se funcionar sem erro: ${GREEN}✓ FIX CONFIRMADO${NC}"
echo "   Se der erro: ${RED}✗ FIX FALHOU${NC} - continue o loop"
echo ""
echo -e "${YELLOW}Pressione ENTER após testar...${NC}"
read

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ VALIDAÇÃO AUTOMÁTICA COMPLETA${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Próximo passo: Testar /plugin marketplace update"
echo ""
echo "Se funcionar → ✅ LOOP COMPLETO"
echo "Se falhar → 🔄 CONTINUE LOOP"
echo ""
