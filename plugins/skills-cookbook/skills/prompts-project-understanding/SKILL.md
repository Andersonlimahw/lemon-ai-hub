---
name: prompts-project-understanding
description: Ready-to-paste prompts to understand a codebase fast and cut cognitive load — architecture deep-dives, auto-generated wikis, guided learning paths, and spec grilling before implementation.
---

# Prompts — Entender projetos (menos carga cognitiva)

Receitas para explicar um projeto a você (ou a um agente) sem afogar o contexto. Objetivo: reduzir carga cognitiva e débito cognitivo — você entende o sistema em camadas, com artefatos navegáveis, em vez de ler código cru.

## R1 — Raio-X de arquitetura

**Skills:** `architecture-deepener`
**Quando:** o codebase parece "raso", lógica de domínio vazou para controllers/UI, ou você herdou um projeto.

```text
Use a skill architecture-deepener no diretório <path>.
Quero: (1) o mapa de módulos rasos vs profundos, (2) onde a lógica de
domínio vazou para controllers/UI, (3) as 3 oportunidades de maior
impacto para aprofundar o design, priorizadas.
Sucesso: relatório com oportunidades que eu consiga validar apontando
arquivo:linha, pronto para virar backlog.
```

## R2 — Wiki viva do projeto

**Skills:** `llm-wiki-curator` + `architecture-deepener`
**Quando:** onboarding de time ou de agente; ninguém quer reler o código a cada dúvida.

```text
Gere uma wiki navegável do projeto <path> com llm-wiki-curator:
índice, uma página por módulo relevante, links reais entre páginas.
Use architecture-deepener antes para decidir o que merece página
própria (módulos profundos) e o que é só nota de rodapé.
Sucesso: index.md + páginas por módulo com links que resolvem;
uma pergunta típica de onboarding se responde em ≤2 cliques.
```

## R3 — Me ensina o projeto

**Skills:** `teaching` + `learning-output-style`
**Quando:** você quer dominar uma área do repo em algumas sessões, não só receber um dump.

```text
Monte com a skill teaching um plano de aprendizado do repo <repo>
para eu dominar <área> em <N> sessões. Formato didático
(learning-output-style): cada sessão com objetivo, leitura mínima
(arquivos exatos), exercício prático no próprio repo e checkpoint
verificável.
Sucesso: plano com N sessões; cada checkpoint é um comando ou
mudança que eu executo e confiro sozinho.
```

## R4 — Interrogatório de spec antes de codar

**Skills:** `doc-driven-grilling` + `task-interrogator`
**Quando:** antes de implementar uma feature a partir de um doc/spec — barato perguntar agora, caro descobrir depois.
**Nota:** as duas skills se sobrepõem no grilling; aqui entram em sequência com papéis distintos (grilling+docs → tarefas com aceite), nunca como drivers paralelos.

```text
Antes de implementar <feature>, grile o documento <path> com
doc-driven-grilling: liste ambiguidades, assunções não declaradas
e perguntas bloqueantes, em ordem de risco. Use task-interrogator
para transformar o que sobrar em tarefas com critério de aceite.
Sucesso: lista de gaps que eu respondo em uma passada + tarefas
com aceite verificável; nenhuma pergunta genérica.
```

## Veja também

- `session-handoff` — fim de sessão longa: gere um handoff para a próxima sessão começar sem re-explorar.
- `bug-diagnostics` — quando o objetivo é entender um comportamento quebrado, não o projeto inteiro.
- Neste repo, `graphify query "<pergunta>"` (ferramenta do projeto, `graphify-out/`) responde perguntas de codebase mais barato que explorar arquivos.
