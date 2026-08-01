---
name: prompts-data-backend
description: Ready-to-paste prompts for data and backend — Supabase with Postgres best practices, Firebase operations, database advisory, and production incident response.
---

# Prompts — Dados & Backend

Receitas para a camada de dados e operação de backend gerenciado.

## R1 — Supabase bem modelado

**Skills:** `supabase` + `supabase-postgres-best-practices`
**Quando:** schema novo ou reforma em Supabase; RLS, índices e modelagem Postgres.

```text
Modele <domínio> no Supabase com a skill supabase, aplicando
supabase-postgres-best-practices: tipos corretos, constraints,
índices justificados, RLS por papel <papéis>.
Sucesso: migration SQL pronta + política RLS testada com um caso
permitido e um negado por papel; EXPLAIN das queries principais
sem full scan.
```

## R2 — Operação Firebase

**Skills:** `firebase-expert`
**Quando:** Firestore/Auth/Functions/Hosting — modelagem, rules, logs ou deploy.

```text
Use firebase-expert em <projeto>: <tarefa — ex.: revisar security
rules do Firestore para <coleções>, diagnosticar a function
<nome> pelos logs, estruturar a coleção <dado> para o padrão de
leitura <padrão>>.
Sucesso: mudança aplicada com rules/queries validadas (simulador
ou emulador) e evidência de logs limpos.
```

## R3 — Monitoramento contínuo do banco

**Skills:** `db-advisor`
**Quando:** o banco cresce sem ninguém olhando; você quer relatórios de saúde recorrentes, não descobrir o problema no incidente.

```text
Configure db-advisor para monitorar <banco/projeto>: relatórios
recorrentes de saúde cobrindo queries degradando, índices não
usados, crescimento de tabelas <tabelas> e conexões.
Sucesso: primeiro relatório gerado com ≥1 ação priorizada por
seção; cadência definida e agendada.
```

## R4 — Incidente em produção

**Skills:** `incident-runbook` + `incident-center`
**Quando:** algo caiu (ou quase); resposta agora e prevenção depois.

```text
Incidente: <sintoma/alerta>. Siga incident-runbook: triagem,
mitigação, comunicação, evidências. Depois registre em
incident-center o postmortem sem culpados com ações preventivas.
Sucesso: mitigação aplicada com timeline registrada; postmortem
com ≥2 ações preventivas com dono e prazo.
```

## Veja também

- `db-index-advisor` — fix pontual de índice por query (trilha [prompts-engineering-quality](../prompts-engineering-quality/SKILL.md) R3); com `db-advisor` vale a regra geral do hub: pontual × contínuo, um driver por passe.
- `api-test-loop` — validar a API que expõe esses dados.
- `load-test` / `chaos-test` — provar que a camada de dados aguenta produção.
