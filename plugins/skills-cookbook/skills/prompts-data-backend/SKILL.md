---
name: prompts-data-backend
description: Ready-to-paste prompts for data and backend — Supabase with Postgres best practices, Firebase operations, database advisory, and production incident response.
---

# Prompts — Data & Backend

Recipes for the data layer and managed-backend operations.

## R1 — Well-modeled Supabase

**Skills:** `supabase` + `supabase-postgres-best-practices`
**When:** a new or reworked Supabase schema; RLS, indexes, and Postgres modeling.

```text
Model <domain> in Supabase with the supabase skill, applying
supabase-postgres-best-practices: correct types, constraints,
justified indexes, RLS per role <roles>.
Success: ready migration SQL + RLS policy tested with one allowed
and one denied case per role; EXPLAIN on the main queries shows no
full scan.
```

## R2 — Firebase operations

**Skills:** `firebase-expert`
**When:** Firestore/Auth/Functions/Hosting — modeling, rules, logs, or deploy.

```text
Use firebase-expert on <project>: <task — e.g. review Firestore
security rules for <collections>, diagnose function <name> from
logs, structure collection <data> for read pattern <pattern>>.
Success: change applied with rules/queries validated (simulator or
emulator) and evidence of clean logs.
```

## R3 — Continuous database monitoring

**Skills:** `db-advisor`
**When:** the database grows with nobody watching; you want recurring health reports, not discovering the problem during an incident.

```text
Set up db-advisor to monitor <database/project>: recurring health
reports covering degrading queries, unused indexes, growth of
tables <tables>, and connections.
Success: first report generated with ≥1 prioritized action per
section; cadence defined and scheduled.
```

## R4 — Production incident

**Skills:** `incident-runbook` + `incident-center`
**When:** something broke (or nearly did); response now, prevention after.

```text
Incident: <symptom/alert>. Follow incident-runbook: triage,
mitigation, communication, evidence. Then log with incident-center
the blameless postmortem with preventive actions.
Success: mitigation applied with a recorded timeline; postmortem
with ≥2 preventive actions, each with an owner and a deadline.
```

## See also

- `db-index-advisor` — one-shot index fix per specific query (track [prompts-engineering-quality](../prompts-engineering-quality/SKILL.md) R3); with `db-advisor` the hub-wide rule applies: one-shot × continuous, one driver per pass.
- `api-test-loop` — validate the API exposing this data.
- `load-test` / `chaos-test` — prove the data layer can survive production.
