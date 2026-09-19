---
name: prompts-meta-harness
description: Ready-to-paste prompts for extending and operating the AI harness itself — prompt refinement, skill selection, decision-native routing, portable subagents, authoring skills and plugins, hooks, migration, and token economy.
---

# Prompts — Meta-harness (extending the hub itself)

Recipes to run the hub's decision-native pipeline, create skills/plugins, automate the harness with hooks, orchestrate portable subagents, and save tokens. Generator choice: `skill-creator` (guided new skill) × `create-plugin` / `plugin-creator` / `plugin-generator` (overlapping plugin generators) — pick ONE generator per artifact; in this repo, follow the canonical layout validated by `scripts/validate_plugins.py`.

## R1 — Create a new skill

**Skills:** `skill-creator` + `skill-authoring`
**When:** one of your recurring flows deserves to become a reusable skill.

```text
Create with skill-creator the skill <name> that <capability>.
Apply skill-authoring: description with explicit triggers ("Use
when..."), lean body, multishot examples only where they
disambiguate. Expected trigger: <phrases that should activate it>.
Success: SKILL.md with valid frontmatter; the trigger phrases
activate the skill in testing; no instruction redundant with the
harness.
```

## R2 — Automate with hooks

**Skills:** `hookify`
**When:** "whenever X happens, do Y" — behavior that needs to live in the harness, not in memory.

```text
Create with hookify a hook that <behavior — e.g. run the linter
after every Edit on *.ts; block commit if validate_plugins.py
fails>. Event: <PreToolUse/PostToolUse/SessionStart/...>.
Success: hook registered in settings.json; trigger demonstrated
with one positive and one negative case; easy to disable.
```

## R3 — Multi-agent orchestration

**Skills:** `orchestrate` + `subagent-driven-development`
**When:** fan-out work (many files/fronts) that a single session can't hold.

```text
Orchestrate <work> with orchestrate: break it into independent
subtasks, one subagent per front with a model/effort matched to
that front's complexity (subagent-driven-development), and a final
integration + review pass.
Success: every subagent with a verifiable deliverable; integration
with no conflicts; cost/model per subagent justified in one line.
```

## R4 — Migrate/mirror to another harness

**Skills:** `migrate-to-codex` + `opencode-subagent`
**When:** porting skills/flows from Claude Code to Codex/OpenCode, or delegating between CLIs.

```text
Migrate <skill/flow> to <Codex/OpenCode> with migrate-to-codex: map
what's portable, adjust frontmatter/paths per harness, and keep
Claude Code as the canonical source (symlinks). For a one-off
delegation, use opencode-subagent.
Success: skill visible and functional in the target harness;
single source preserved (no divergent fork).
```

## R5 — Token economy

**Skills:** `token-saver` + `caveman`
**When:** sessions blowing through context or cost; responses too verbose.

```text
Apply token-saver on session/project <target>: identify the
biggest consumers (CLI outputs, re-read files, verbosity) and
propose cuts. Turn on caveman <lite|full|ultra> for response
compression.
Success: estimated savings per source with a number; technical
content preserved (no code information lost).
```

## R6 — Turn an ambiguous request into an executable contract

**Skills:** `senior-prompt-engineer`
**When:** the request is multi-step or underspecified and downstream routing needs one authoritative interpretation.

```text
Use senior-prompt-engineer to refine this request without executing
it: <request>. Resolve the expected artifact, constraints, explicit
non-goals, and verification checks. Emit the definitive prompt plus
EXEC-MAP v1 using only declared intent/executor values. Preserve the
decision envelope: router, router_mode, router_confidence, and
router_fallback.
Success: one unambiguous prompt and one schema-valid EXEC-MAP; every
implementation step has a verification check; unknown facts are
asked before the map instead of encoded as invalid enum values.
```

## R7 — Select the smallest adequate skill set

**Skills:** `skills-selector`
**When:** a refined request or `EXEC-MAP v1` exists and you want bounded, auditable skill activation.

```text
Use skills-selector on this request: <request or EXEC-MAP v1>.
Consume the existing map instead of reclassifying it. Select at most
two skills, reject unavailable or overlapping candidates, and
preserve router, router_mode, router_confidence, and router_fallback
losslessly in the selection block.
Success: exactly one SKILLS block; MAP is consumed when supplied;
every selected identifier exists; no heavy skill lacks an explicit
task signal.
```

## R8 — Route by cost, confidence, and validation

**Skills:** `smart-dispatch`
**When:** implementation needs the cheapest adequate worker with an explicit escalation path.

```text
Use smart-dispatch for <task>. Start from <EXEC-MAP v1 or task
description>, choose the cheapest tier likely to pass <validation
command>, and record requested versus effective route. Use the
static route when scoring adds no value. If a typed scorer is
enabled, use <shadow|advisory|enforce>; an explicit user route wins,
uncertainty fails open to balanced, and the safety floor applies
last.
Success: one DISPATCH block with worker, tier, effort, decision
envelope, budget, and verification command; escalation occurs only
after validation failure or a declared safety requirement.
```

## R9 — Pin a portable subagent route

**Skills:** `smart-sub-agents`
**When:** delegation must name the harness, provider, model, effort, and auditable fallback behavior.

```text
Use smart-sub-agents to route <task> on <harness> through
<provider/model> at <effort>. Validate the exact route against the
provider matrix and map effort to the provider-native control.
Keep provider_fallback separate from router_fallback and do not
retry after explicit cancellation.
Success: one valid ROUTE-MAP v1; requested and effective route are
visible; unsupported model IDs fail closed; no credentials are read
or written.
```

## R10 — Combine cost-aware dispatch with a pinned subagent

**Skills:** `smart-dispatch` + `smart-sub-agents`
**When:** dispatch policy should choose the tier while a portable route pins the actual executor.

```text
Dispatch <task> with smart-dispatch and
combine_smart_subagents: always. Use smart-sub-agents to resolve
<harness/provider/model/effort>, then return its ROUTE-MAP v1 to the
dispatcher. Preserve the canonical decision envelope end to end;
keep provider outage fallback distinct from router uncertainty.
Verify with <command> and escalate only if that validation fails.
Success: ROUTE-MAP and DISPATCH agree on the effective route; both
fallback reasons remain auditable; <command> passes.
```

## See also

- `senior-prompt-engineer` → `skills-selector` → `smart-dispatch` — the hub's standard pipeline; recipes R6–R8 show each contract boundary.
- `smart-sub-agents` — optional portable executor routing; use alone (R9) or with `smart-dispatch` (R10).
- `ai-workspace-orchestrator` — build an agent workspace from scratch (contract + adversarial setup review).
- `agentic-value-loops` — continuous value loops (docs, maintenance, security) running as routine.
- `cli-wrapper` — wrap external CLIs (track [prompts-apis-clis](../prompts-apis-clis/SKILL.md) R3).
- `agent-sdk-dev` — build programmatic agents on the Claude Agent SDK.
- `skill-installer` — install external skills into the local harness.
