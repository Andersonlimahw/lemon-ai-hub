#!/usr/bin/env bash

# detect-marketplace-load.sh
# Detecta se o marketplace foi carregado corretamente pelo Claude Code
# Execute em uma NOVA session antes de testar /plugin marketplace update

echo "=== Marketplace Load Detection ==="
echo ""

# Verificar se Claude Code consegue ler o marketplace.json
CACHE_MARKETPLACE="$HOME/.claude/plugins/marketplaces/lemon-ai-hub/.claude-plugin/marketplace.json"

if [ ! -f "$CACHE_MARKETPLACE" ]; then
  echo "✗ Cache marketplace.json não encontrado"
  exit 1
fi

# Validar que o JSON é válido e tem o schema correto
echo "1. Validando JSON..."
if ! node -e "JSON.parse(require('fs').readFileSync('$CACHE_MARKETPLACE', 'utf8'))" 2>/dev/null; then
  echo "✗ JSON inválido"
  exit 1
fi
echo "✓ JSON válido"

echo "2. Validando schema..."
INVALID=$(node -e "
  const data = require('$CACHE_MARKETPLACE');
  const invalid = data.plugins.filter(p => !p.source || p.source.source !== 'github');
  console.log(invalid.length > 0 ? 'INVALID' : 'OK');
" 2>/dev/null || echo "ERROR")

if [ "$INVALID" != "OK" ]; then
  echo "✗ Schema inválido"
  exit 1
fi
echo "✓ Schema correto"

echo "3. Contando plugins..."
COUNT=$(node -e "console.log(require('$CACHE_MARKETPLACE').plugins.length)" 2>/dev/null || echo "0")
if [ "$COUNT" -lt 50 ]; then
  echo "✗ Poucos plugins: $COUNT"
  exit 1
fi
echo "✓ Plugins: $COUNT"

echo ""
echo "=== Pronto para Testar ==="
echo ""
echo "Execute no Claude Code:"
echo "  /plugin"
echo "  ⎿ marketplace update"
echo ""
echo "Esperado: Atualização sem erro"
echo "Se der erro 'Invalid input', o fix falhou."
echo ""
echo "Log de execução:"
echo "  ~/.claude/plugins/marketplaces/lemon-ai-hub/.git/logs/HEAD"
