---
name: prompts-apis-clis
description: Ready-to-paste prompts for API and CLI tooling — OpenAPI specs from code, Postman collections, agent-friendly CLI design, generated CLIs from specs, and wrapping external CLIs for token savings.
---

# Prompts — APIs & CLIs

Recipes for the contract layer: specs, collections, and CLIs that both humans and agents can operate. Generator choice: `cli-creator` (composable CLI from an API/spec, Codex-focused) × `cli-generator` (full Bun CLI from a SPEC) — overlap, pick by target runtime.

## R1 — Spec-first: OpenAPI + Postman

**Skills:** `openapi-generate` + `postman-generator`
**When:** an API with no formal contract, or a stale one relative to the code.

```text
Generate with openapi-generate the OpenAPI 3 spec for the routes
in <path> (real request/response schemas, examples). Then generate
with postman-generator the collection with one request per
endpoint and environment <envs>.
Success: spec validates with no errors; collection runs against
<base-url> with the examples passing; no route in the code missing
from the spec.
```

## R2 — Agent-friendly CLI

**Skills:** `cli-for-agent` + `cli-generator`
**When:** creating (or reviewing) a CLI that AI agents will operate without hand-holding.

```text
Create with cli-generator the CLI for <API/spec> and apply
cli-for-agent as the rubric: non-interactive flags, layered --help
with examples, stdin/pipes, actionable errors, --dry-run, stable
JSON output.
Success: an agent can discover and run any command from --help
alone; output is parseable; no required interactive prompt.
```

## R3 — Wrap an external CLI (token savings)

**Skills:** `cli-wrapper`
**When:** the harness will call an unfamiliar/verbose CLI repeatedly.

```text
Wrap CLI <cli> with cli-wrapper: capture --help, generate the
compact digest of subcommands/flags, validate invocations, and
post-process the output. Record the savings metrics.
Success: /cli-wrapper list shows <cli> with a digest; invoking via
the wrapper returns the same result as raw with a fraction of the
tokens.
```

## R4 — API validation loop

Contract ready → validate real behavior with `api-test-loop` + `verification-before-completion` — full recipe in track [prompts-feedback-loops](../prompts-feedback-loops/SKILL.md) (R1).

## See also

- `openapi-hub` — ongoing management of multiple specs (vs. one-shot `openapi-generate` — don't run both as drivers of the same pass).
- `agent-sdk-dev` — when the API's consumer is an agent built on the Claude Agent SDK.
- `supabase` / `firebase-expert` — managed backends behind the API (track [prompts-data-backend](../prompts-data-backend/SKILL.md)).
