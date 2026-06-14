# 🎯 Spotify Squad Plugin

**AI-Native Squad — Spotify-model autonomous engineering team**

Este plugin transforma o seu CLI (Claude Code, Gemini CLI, etc.) em uma squad de engenharia completa baseada no modelo do Spotify, seguindo as diretrizes do livro **[AI Native Developer](https://andersonlimahw.github.io/ebook-ai-native-developer/)**.

A squad é composta por 12 agentes especialistas, liderados por um orquestrador (Tech Lead), todos compartilhando o mesmo contexto de projeto, mas operando isoladamente (em "subagents") para manter o uso de tokens e a clareza perfeitos.

## 🌟 Visão Geral

- **12 Agentes Especializados**: De UX a DevSecOps.
- **16 Skills Avançadas**: Conhecimento progressivo (Progressive Disclosure) para manter o contexto leve.
- **Orquestração Inteligente**: O `squad-orchestrator` recebe sua demanda ("Crie uma tela de login"), quebra em tarefas, e delega para os agentes certos.
- **Qualidade Assegurada**: Todos os agentes possuem diretrizes claras (quality gates, testes obrigatórios e revisão adversária).

## 🚀 Instalação

```bash
# Na raiz do seu repositório lemon-ai-hub:
./plugins/spotify-squad/scripts/install.sh
```

## 👥 A Squad

| Agente | Papel | Quando usar |
|--------|-------|-------------|
| `@squad-orchestrator` | Tech Lead / Orquestrador | Quando você tiver uma funcionalidade inteira para implementar (delegação automática). |
| `@product-manager` | Product Manager | Para criar PRDs, User Stories e priorizar tarefas. |
| `@ux-researcher` | UX Researcher | Para validar fluxos, acessibilidade (Nielsen) e jornada do usuário. |
| `@ui-designer` | UI/Visual Designer | Para criar design tokens, specs de UI e paletas. |
| `@frontend-engineer` | Frontend Engineer | Para implementar UI (React/Vue), estado e integrações (Next.js). |
| `@backend-engineer` | Backend Engineer | Para implementar APIs, microserviços e lógica de servidor. |
| `@mobile-engineer` | Mobile Engineer | Para implementar apps nativos ou cross-platform (React Native/Flutter). |
| `@data-engineer` | Data Engineer | Para pipelines, analytics, banco de dados (BigQuery/Snowflake). |
| `@devops-engineer` | DevOps Engineer | Para pipelines de CI/CD, Docker, Kubernetes, Terraform e AWS/GCP. |
| `@qa-engineer` | QA Engineer | Para automação de testes (Cypress/Playwright), E2E e test plans. |
| `@security-engineer` | DevSecOps / Security | Para audits de segurança, threat modeling e secure coding. |
| `@scrum-master` | Scrum Master | Para plannings, dailies, retrospectivas e facilitação do board. |

## 🛠️ Como usar (Exemplos)

Apenas mencione os agentes no seu prompt para ativá-los, ou simplesmente peça para o orquestrador montar a solução completa:

> **"Quero criar uma funcionalidade de exportação de relatórios em CSV."**
> *(O `squad-orchestrator` vai assumir o controle, criar o plano com o `product-manager`, delegar a API para o `backend-engineer`, a tela para o `frontend-engineer` e os testes para o `qa-engineer`.)*

> **"Me ajude a planejar a próxima sprint."**
> *(O `scrum-master` assume, puxa tickets, avalia complexidade e levanta dependências.)*

> **"Revise a segurança dessa implementação de login."**
> *(O `qa-engineer` e o `backend-engineer` vão carregar a skill de `adversary-review` para quebrar sua implementação.)*

## 📚 Skills Incluídas

As skills ensinam *como* fazer. Elas são carregadas sob demanda:
- `agile-ceremonies`
- `adversary-review`
- `new-feature`
- `new-repository`
- `frontend-patterns`, `backend-patterns`, `mobile-patterns`, `devops-pipeline`, `data-pipeline`, `secure-coding-patterns`...

## 🏗️ Padrões Arquiteturais

Baseado no Ebook "AI Native Developer", utilizamos:
- **Plan-Execute-Verify Loop**: Nenhuma feature passa sem verificação.
- **Context Isolation**: Subagentes possuem janela de contexto limpa, reportando apenas o necessário.
- **Token Economy**: "Lazy loading" de instruções extensas (Skills).
