---
name: prompts-apis-clis
description: Ready-to-paste prompts for API and CLI tooling — OpenAPI specs from code, Postman collections, agent-friendly CLI design, generated CLIs from specs, and wrapping external CLIs for token savings.
---

# Prompts — APIs & CLIs

Receitas para a camada de contrato: specs, collections e CLIs que humanos E agentes conseguem operar. Escolha de gerador: `cli-creator` (CLI composável a partir de API/spec, foco Codex) × `cli-generator` (CLI Bun completa a partir de SPEC) — sobreposição, escolha pelo runtime alvo.

## R1 — Spec-first: OpenAPI + Postman

**Skills:** `openapi-generate` + `postman-generator`
**Quando:** API sem contrato formal, ou contrato desatualizado do código.

```text
Gere com openapi-generate a spec OpenAPI 3 das rotas de <path>
(schemas de request/response reais, exemplos). Depois gere com
postman-generator a collection com um request por endpoint e
environment <envs>.
Sucesso: spec valida sem erro; collection roda contra <base-url>
com os exemplos passando; nenhuma rota do código fora da spec.
```

## R2 — CLI amigável para agentes

**Skills:** `cli-for-agent` + `cli-generator`
**Quando:** criar (ou revisar) uma CLI que agentes de IA vão operar sem babysitting.

```text
Crie com cli-generator a CLI de <API/spec> e aplique cli-for-agent
como rubrica: flags non-interactive, --help em camadas com
exemplos, stdin/pipes, erros acionáveis, --dry-run, JSON estável
na saída.
Sucesso: agente consegue descobrir e executar qualquer comando só
pelo --help; saída parseável; nenhum prompt interativo obrigatório.
```

## R3 — Envelopar CLI externo (economia de tokens)

**Skills:** `cli-wrapper`
**Quando:** o harness vai chamar um CLI desconhecido/verboso repetidamente.

```text
Envelope o CLI <cli> com cli-wrapper: capture --help, gere o
digest compacto de subcomandos/flags, valide invocações e
pós-processe a saída. Registre as métricas de economia.
Sucesso: /cli-wrapper list mostra <cli> com digest; invocação via
wrapper retorna o mesmo resultado do raw com fração dos tokens.
```

## R4 — Loop de validação da API

Contrato pronto → valide o comportamento real com `api-test-loop` + `verification-before-completion` — receita completa na trilha [prompts-feedback-loops](../prompts-feedback-loops/SKILL.md) (R1).

## Veja também

- `openapi-hub` — gestão contínua de múltiplas specs (vs `openapi-generate` pontual — não usar como drivers do mesmo passe).
- `agent-sdk-dev` — quando o consumidor da API é um agente construído no Claude Agent SDK.
- `supabase` / `firebase-expert` — backends gerenciados por trás da API (trilha [prompts-data-backend](../prompts-data-backend/SKILL.md)).
