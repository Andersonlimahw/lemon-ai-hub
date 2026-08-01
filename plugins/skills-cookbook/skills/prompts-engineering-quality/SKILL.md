---
name: prompts-engineering-quality
description: Ready-to-paste prompts for engineering quality — PR review with semantic commits, async-pattern audits, database indexing, security threat modeling, resilience/load testing, and i18n sync.
---

# Prompts — Qualidade de engenharia

Receitas transversais de qualidade. Padrão do hub que vale para a trilha inteira: muitos pares vêm em dupla **pontual × contínuo** (`async-patterns`×`async-advisor`, `bundle-analyzer`×`bundle-watch`, `load-test`×`load-test-runner`, `chaos-test`×`chaos-runner`, `a11y-audit`×`a11y-guardian`). Use o pontual para investigar/fixar agora; o contínuo como gate de CI. Nunca os dois como driver do mesmo passe.

## R1 — Review de PR completo

**Skills:** `code-review-expert` + `pr-review-canvas` + `commit-quality`
**Quando:** PR relevante precisa de review estruturado, não de "LGTM".

```text
Revise o PR <número/branch> com code-review-expert; renderize os
findings com pr-review-canvas (comentários inline por
arquivo:linha). Cheque a higiene dos commits com commit-quality
(mensagens semânticas, escopo por commit).
Sucesso: findings com severidade + fix sugerido cada; commits fora
do padrão listados com mensagem corrigida proposta.
```

## R2 — Auditoria de async

**Skills:** `async-patterns`
**Quando:** timeouts, race conditions, memory leaks ou paralelismo sem limite em código async.

```text
Audite <path> com async-patterns: races, promises sem tratamento
de erro, N+1 async, paralelismo sem limite, cancelamento ausente.
Para cada finding, o padrão correto (Promise.all, p-limit,
AbortController...) com o diff.
Sucesso: cada finding com reprodução plausível + fix aplicável;
depois estabilize com async-advisor como gate de CI (não junto).
```

## R3 — Índices e queries de banco

**Skills:** `db-index-advisor` + `supabase-postgres-best-practices`
**Quando:** queries lentas, full scans, ou dúvida de modelagem em Postgres.

```text
Analise as queries lentas de <app/schema> com db-index-advisor:
proponha índices com justificativa por query. Se Postgres/Supabase,
aplique supabase-postgres-best-practices na modelagem e RLS.
Sucesso: EXPLAIN ANALYZE antes/depois por query otimizada; nenhum
índice proposto sem query que o use.
```

## R4 — Threat model de feature

**Skills:** `security-threat-model` + `security-best-practices` + `security-ownership-map`
**Quando:** feature nova toca auth, dados sensíveis ou superfície externa.

```text
Faça o threat model de <feature> com security-threat-model
(atores, superfícies, STRIDE). Valide mitigações contra
security-best-practices e mapeie donos por área com
security-ownership-map.
Sucesso: tabela ameaça → mitigação → dono; toda ameaça HIGH com
mitigação concreta ou risco aceito por escrito.
```

## R5 — Resiliência sob carga e falha

**Skills:** `load-test` + `chaos-test`
**Quando:** antes de produção ou de um pico previsto; validar SLO sob falha.

```text
Desenhe com load-test o teste de carga de <serviço> (perfil
<RPS/duração>) e com chaos-test os experimentos de falha (latência
injetada, dependência fora, disco cheio) sobre <dependências>.
Verifique circuit breakers, retries e fallbacks.
Sucesso: relatório com SLO alvo vs medido por cenário; cada
mecanismo de resiliência disparado ao menos uma vez com evidência.
```

## R6 — i18n sincronizado

**Skills:** `i18n-audit` + `i18n-sync`
**Quando:** locales divergentes, chaves órfãs, ou idioma novo entrando.

```text
Audite os locales de <projeto> com i18n-audit (chaves faltando,
órfãs, hardcoded strings) e sincronize com i18n-sync mantendo
locales/{lang}.json com estrutura idêntica.
Sucesso: diff de chaves zerado entre idiomas; teste no idioma
<alvo> passando; nenhuma string hardcoded nas telas <telas>.
```

## Veja também

- `git-expert` (`/git-commit`, bisect) e `gh-expert` — fluxo git/GitHub por trás de todo review.
- `feature-purge` — remover feature inteira sem deixar código morto; `finishing-a-development-branch` — fechar branch com qualidade.
- `incident-runbook` + `incident-center` — quando a qualidade falhou em produção.
- `code-smell` (pontual) / `code-smell-detector` (contínuo) — cheiro de código nas duas cadências.
