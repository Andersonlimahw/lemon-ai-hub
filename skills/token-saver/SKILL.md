---
name: token-saver
description: "Configura ferramentas de economia de tokens (rtk, caveman, graphify, context-mode) globalmente ou por projeto. Permite auditar e calcular o token saving obtido."
---

# token-saver

Esta skill guia e realiza a instalação e configuração de ferramentas otimizadas para redução do consumo de tokens (input/output) e compactação de contexto em LLMs de coding (Claude Code, Codex, OpenCode, Agy).

As ferramentas configuráveis são:
1. **rtk (Rust Token Killer)**: Proxy de comandos CLI que filtra outputs redundantes de builds, lints, testes e git, gerando economia de 60-90% em operações locais.
2. **caveman**: Modo de comunicação ultra-comprimida que reduz ~75% do consumo de output tokens ao falar em estilo telegráfico (sem verbos de ligação ou formalidades) sem perder precisão técnica.
3. **graphify**: Mapeamento do codebase em grafo de conhecimento estruturado (knowledge graph). Permite que a LLM consulte relações entre arquivos e god nodes sem varrer ou ler arquivos cruzados de forma linear.
4. **context-mode**: MCP/Plugin que intercepta outputs gigantes de ferramentas (APIs, logs longos, dumps) e armazena em uma base local FTS5, retornando apenas resumos compactados para a janela de contexto.

---

## Como Calcular o Token Saving de Cada Ferramenta

1. **rtk**:
   - Comando: `rtk gain`
   - O que mostra: Relatório de tokens economizados em comandos interceptados.
   - Comando com histórico: `rtk gain --history`

2. **caveman**:
   - Cálculo: Compara a quantidade de caracteres/tokens gerados em modo normal vs modo caveman. 
   - Exemplo: Uma resposta de 400 tokens cai para ~100 tokens. O saving típico é de **~75%** em output tokens.

3. **graphify**:
   - Economia: Reduz o consumo de input tokens em buscas no codebase. 
   - Em vez de ler 10 arquivos relacionados via grep/search (ex: 20k-50k tokens), a LLM faz uma busca direta no grafo em `graphify-out/` consumindo menos de 1k tokens.

4. **context-mode**:
   - Economia: Evita estouro do contexto em dumps de console/logs.
   - Um log de build de 50k tokens é resumido para 1k tokens na janela ativa, mantendo o log completo pesquisável via base SQLite local. Economia típica de **90-98%** em logs e outputs extensos.

---

## Fluxo de Execução da Skill

Quando esta skill for ativada:

1. **Perguntar ao Usuário (Iterativo)**:
   Perguntar para cada ferramenta se o usuário deseja instalar/configurar, e o escopo da instalação:
   - **rtk**: Instalar? [y/n] -> Escopo: [g]lobal ou [p]rojeto?
   - **caveman**: Instalar/Ativar? [y/n] -> Escopo: [g]lobal ou [p]rojeto?
   - **graphify**: Instalar/Configurar? [y/n] -> Escopo: [g]lobal ou [p]rojeto?
   - **context-mode**: Instalar/Configurar? [y/n] -> Escopo: [g]lobal ou [p]rojeto?

2. **Executar o Script de Setup**:
   Rodar o script auxiliar `skills/token-saver/scripts/setup-token-saving.sh` (com BypassSandbox quando necessário) para realizar as ações conforme a seleção do usuário.

3. **Confirmar e Ensinar**:
   Exibir um resumo do que foi configurado e as instruções rápidas de uso (cheat-sheet de comandos) de cada ferramenta ativada.
