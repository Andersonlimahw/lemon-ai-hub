# 🔄 Agentic Value Loops Plugin

**Repeatable, agent-driven workflows that keep projects improving with quality held constant.**

Este plugin transforma automações documentadas em **Value Loops** executáveis. Um loop é uma iteração repetível que, a cada passagem, entrega um incremento de valor real de usuário, validado por um "quality gate" inegociável.

## 🌟 Visão Geral

- **Loop Orchestrator (`@loop-orchestrator`)**: O maestro que garante que cada iteração de qualquer loop passe pelas 7 fases obrigatórias (Idea → Plan → Implement → Test → Gate → Ship → Reflect).
- **Skills de Loops**: 
  - `feature-development-loop`
  - `maintenance-security-loop`
  - `documentation-sync-loop`
  - `ai-tuning-loop`
- **Invariantes**: Nenhuma iteração é completada sem respeitar as regras do `loop-invariants`.

## 🚀 Instalação

```bash
# Na raiz do seu repositório ai-marketplace:
./plugins/agentic-value-loops/scripts/install.sh
```

## 🛠️ Como usar (Exemplos)

Basta chamar o `@loop-orchestrator` e dizer qual loop você quer executar:

> **"Inicie o feature development loop para criar um sistema de notificações em tempo real."**
> *(O orquestrador carregará a skill de feature-development, aplicará os invariants e guiará por todas as 7 fases, extraindo os subagents necessários).*

> **"Rode o loop semanal de maintenance and security."**
> *(O orquestrador vai auditar o npm, criar o plano para atualização das dependências (SD Lite), atualizar e passar pelo quality gate).*

> **"Houve drift na documentação. Inicie o documentation sync loop."**
> *(Verificará git logs, rodará o llm-wiki-curator e sincronizará docs com código).*

## 🏗️ Princípios

1. **Spec before code**: O plano (`PLAN.md`) sempre precede a implementação.
2. **One quality gate**: `npm run version:validate` deve passar.
3. **Automate the second time**: Cada iteração extrai assets reutilizáveis (script, skill, subagent ou MCP).
