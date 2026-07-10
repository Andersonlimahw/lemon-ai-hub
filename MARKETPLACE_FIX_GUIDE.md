# Guide: Validação do Marketplace Fix

## Contexto
Erro: `Marketplace configuration file is corrupted: lemon-ai-hub.source.source: Invalid input`

## Fix Aplicado
✅ Atualizado `marketplace.json` com schema correto (`source.source = github`)
✅ Commit e push para GitHub
✅ Cache local atualizado

## Validação Requerida (NOVA SESSION)

### Passo 1: Abrir NOVA Session do Claude Code
```bash
# Fechar completamente Claude Code
# Abrir nova session
claude
```

### Passo 2: Atualizar Marketplace
Na nova session, execute:
```
/plugin
⎿ marketplace update
```

### Passo 3: Verificar Resultado
**ESPERADO:** Marketplace atualiza sem erro
```
✓ lemon-ai-hub updated successfully
```

**ERRO (se ainda ocorrer):**
```
⎿  Marketplace configuration file is corrupted: lemon-ai-hub.source.source: Invalid input
```

### Passo 4: Validar Plugins Disponíveis
```
/marketplace list lemon-ai-hub
```

Deve mostrar todos os 60 plugins.

## Validações Já Concluídas

### ✅ Schema Validation
```bash
cd ~/.claude/plugins/marketplaces/lemon-ai-hub/.claude-plugin
node -e "const data = require('./marketplace.json'); console.log('✓ Válido:', data.plugins.length, 'plugins');"
```
Resultado: ✓ Todos os 60 plugins têm `source.source = github`

### ✅ Symlinks (Todos os Agentes)
```bash
for agent in claude codex gemini agy opencode; do
  link="$HOME/.${agent}/skills"
  if [ -L "$link" ]; then
    echo "✓ $agent: $(readlink $link)"
  fi
done
```
Resultado: ✓ Todos apontam para `/Users/andersonlimadev/Projects/IA/lemon-ai-hub/plugins`

### ✅ Skills por Agente
```bash
ls ~/.claude/skills/ | wc -l      # 60
ls ~/.codex/skills/ | wc -l       # 60
ls ~/.opencode/skills/ | wc -l    # 60
ls ~/.agy/skills/ | wc -l         # 60
```
Resultado: ✓ Todos têm acesso aos 60 plugins

### ✅ Scripts Syntax
```bash
bash -n scripts/setup-symlinks.sh
bash -n scripts/menu.sh
python3 -m py_compile scripts/*.py
```
Resultado: ✓ Sintaxe válida em todos

## Comandos de Diagnóstico

Se o erro persistir na nova session:

### 1. Verificar Cache Local
```bash
cd ~/.claude/plugins/marketplaces/lemon-ai-hub
git status
git log -1 --oneline
cat .claude-plugin/marketplace.json | jq '.plugins[0].source'
```

### 2. Limpar Cache e Reinstalar
```bash
rm -rf ~/.claude/plugins/marketplaces/lemon-ai-hub
# Reinstalar via marketplace
```

### 3. Verificar Schema Manualmente
```bash
cd ~/.claude/plugins/marketplaces/lemon-ai-hub/.claude-plugin
jq '.plugins[] | select(.source.source != "github") | .name' marketplace.json
```
Esperado: (vazio - nenhum plugin com source incorreto)

## Status Checklist

- [x] marketplace.json corrigido
- [x] Push para GitHub
- [x] Cache local atualizado
- [x] Schema validado (60/60 plugins)
- [x] Symlinks funcionando (5 agentes)
- [x] Scripts validados
- [ ] **TESTE EM NOVA SESSION** ← PENDENTE

## Próximo Passo

**USUÁRIO DEVE:**
1. Fechar completamente Claude Code
2. Abrir nova session
3. Executar `/plugin marketplace update`
4. Reportar resultado

Se funcionar → ✅ FIX CONFIRMADO
Se falhar → 🔄 Loop continua com nova investigação
