---
name: prompts-meta-harness
description: Ready-to-paste prompts for extending and operating the AI harness itself — authoring skills and plugins, hooks, multi-agent orchestration, cross-harness migration, and token economy.
---

# Prompts — Meta-harness (extending the hub itself)

Recipes to create skills/plugins, automate the harness with hooks, orchestrate subagents, and save tokens. Generator choice: `skill-creator` (guided new skill) × `create-plugin` / `plugin-creator` / `plugin-generator` (overlapping plugin generators) — pick ONE generator per artifact; in this repo, follow the canonical layout validated by `scripts/validate_plugins.py`.

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

## See also

- `senior-prompt-engineer` → `skills-selector` → `smart-dispatch` — the hub's standard pipeline; refine before routing.
- `ai-workspace-orchestrator` — build an agent workspace from scratch (contract + adversarial setup review).
- `agentic-value-loops` — continuous value loops (docs, maintenance, security) running as routine.
- `cli-wrapper` — wrap external CLIs (track [prompts-apis-clis](../prompts-apis-clis/SKILL.md) R3).
- `agent-sdk-dev` — build programmatic agents on the Claude Agent SDK.
- `skill-installer` — install external skills into the local harness.
