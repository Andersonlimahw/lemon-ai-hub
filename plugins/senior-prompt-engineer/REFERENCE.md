# Senior Prompt Engineer — Reference

Depth for the 6-step protocol in [SKILL.md](SKILL.md). Source of truth for techniques: Anthropic prompt-library + docs (https://code.claude.com/docs/en/prompt-library, https://docs.claude.com/en/docs/build-with-claude/prompt-engineering).

---

## Prompt skeleton

The canonical block order. Omit a block only if truly irrelevant; never reorder.

```md
# Role / Context
You are <role> working in <repo/domain>. <relevant constraints of the environment>.

# Task
<single imperative objective>.

# Inputs
- <file path / artifact> — <what it is>
- <data / API / fixture>

# Constraints
- Scope: touch only <X>. Do NOT modify <Y>.
- Style: match existing conventions in <file>.
- <perf / security / compat limits>

# Plan
1. <step> → verify: <observable check>
2. <step> → verify: <check>
3. <step> → verify: <check>

# Output contract
- Deliverable: <exact artifact>.
- Format: <md / diff / json / code>.
- Location: <path>.
- Definition of done: <verifiable condition>.

# Examples            # optional, only when it disambiguates
<one good input→output shape>

# Feedback — DO
- <positive guardrail>

# Feedback — DO NOT
- <specific anti-pattern for THIS task>

# Execution Map
Agents: <...> | Skills: <...> | Models: <...>
Effort: <trivial|low|medium|high> | Time: <~range> | Tokens: <~range> | MCP/Tools: <...>
```

---

## Techniques (Anthropic prompt-library, ranked by leverage)

Apply the ones that fit; cite them implicitly through structure, not by naming them in the output.

1. **Be clear & direct** — explicit > implicit. Spell out what a smart contractor with no context would need. Vague verbs become measurable checks.
2. **Multishot (examples)** — 1–3 examples beat paragraphs of description. Wrap each in tags, show input→output. Use when format/shape matters. One well-chosen example > five rules.
3. **Let it think (CoT)** — for analysis/ambiguous tasks, instruct a brief reasoning pass before the answer. Skip for mechanical tasks (wastes tokens).
4. **XML / section tags** — delimit role, inputs, constraints, examples so the model parses structure unambiguously. Markdown headers work in Claude Code prompts.
5. **System vs user split** — durable role/constraints in system position; the specific task in user position. For Claude Code prompts, the "Role/Context" block plays the system role.
6. **Prefill / output contract** — pin the exact output shape (start token, format, file). Removes preamble drift.
7. **Constrain scope (surgical)** — every changed line must trace to the request. The DO-NOT block enforces this.
8. **Decompose long tasks** — chain numbered steps each with a verify check, instead of one mega-instruction. Enables independent looping.
9. **Assign a role** — a precise persona sharpens tone and judgment ("senior staff engineer reviewing for prod").
10. **Name the failure modes** — pre-empt known LLM mistakes (over-engineering, speculative abstractions, touching adjacent code) directly in DO-NOT.

---

## Boilerplate autocomplete

**Gate:** only fire when step-2 probe returns real signal. The output is a *pre-filled scaffold*, never a fabricated one.

When context is found, fill blanks from the repo:
- Paths/scripts from `package.json`, `Makefile`, `AGENTS.md`, `CLAUDE.md`.
- Stack & conventions from manifests + config (tsconfig, pyproject, go.mod, etc.).
- Test/build/lint commands → wire them into the `→ verify:` checks.
- Domain language from README / existing code.

When context is absent or thin:
- Emit NO scaffold. Instead ask, e.g.:
  > "Not enough repo context. To build the prompt I need: (1) stack/language, (2) target files, (3) definition of done. Can you provide them?"
- Proceed only with user-supplied facts. Inventing a fake stack is forbidden.

---

## Execution Map

> Emit it as the canonical **`EXEC-MAP v1`** fenced block (see SKILL.md step 5). It is a **contract** the routers parse: `skills-selector` reads `intent`+`skills`, `smart-dispatch` reads `effort`+`models`. The tables below are how you *fill* each field — not a second format.

### Agent / subagent routing
| Situation | Recommendation |
|-----------|----------------|
| Single linear task | `inline` — no subagent |
| Broad fan-out search across many files | `Explore` (read-only) |
| Independent multi-step build that can run unattended | `general-purpose` agent or `smart-dispatch` route |
| Architecture/plan before code | `Plan` agent / `gsd:plan-phase` |
| Verification of a Claude SDK app | `agent-sdk-verifier-*` |
Only recommend an agent when the task genuinely parallelizes or needs isolation. Default = inline.

### Skill chaining (Claude Code)
Common ordered chains to suggest in the Execution Map:
- Code work: `skills-selector → smart-dispatch → (domain skill) → git-commit`
- Git op: `git-commit` / `git-pr-create` (narrow beats `git-master`)
- New skill/MCP: `write-a-skill` / `mcp-builder`
- Bug: `auto-fix → systematic-debugging` (escalate) / `diagnose`
- UI: `ui-polisher` (small) vs `frontend-design` / `ui-ux-pro-max` (heavy, needs explicit signal)
Cap suggestions at what the task needs; don't list the whole catalog.

### Model routing
| Phase / task shape | Model | Why |
|--------------------|-------|-----|
| Architecture, ambiguous specs, multi-constraint reasoning, security review | **Opus** (`claude-opus-4-8`) | Deepest reasoning, best at tradeoffs/edge cases |
| Bulk feature implementation, refactors, standard tests | **Sonnet** (`claude-sonnet-4-6`) | Strong code, faster/cheaper than Opus |
| Mechanical edits, lint/format fixes, boilerplate, i18n, simple codegen | **Haiku** (`claude-haiku-4-5`) | Cheapest, fast, sufficient for deterministic work |
Rationale line is mandatory next to each pick. If the executor is a non-Claude CLI (Gemini/Codex/OpenCode/Antigravity/lemon-code), map to its closest tier and note the substitution. Mark unknowns `TBD`.

### Estimation (effort / time / tokens) — mandatory in Execution Map
Heuristic, not promises. Calibrate to the refined plan:

| Effort | Shape | Time | Tokens |
|--------|-------|------|--------|
| trivial | 1 file, mechanical edit, no ambiguity | <5 min | <3k |
| low | 1–2 files, clear path, few verify steps | ~5–15 min | ~3k–10k |
| medium | several files, some design choices, tests | ~15–45 min | ~10k–40k |
| high | cross-module/architecture, ambiguity, fan-out | ~45 min+ | ~40k+ |

Rules: count plan steps × files touched × ambiguity. Add ~30% tokens if subagents fan out (cold context per spawn). State as a **range**, prefix `~`. If genuinely unknown, write `TBD` — never a fake precise number.

### Per-CLI execution notes (executor-aware)
The skeleton + techniques are CLI-agnostic. Only the Execution Map's agent/skill names differ:

| CLI | Skills dir | Has skills-selector / smart-dispatch | Notes |
|-----|------------|--------------------------------------|-------|
| Claude Code | `~/.claude/skills/<n>/SKILL.md` | yes | full agent catalog (Explore/Plan/general-purpose/gsd:*) |
| Codex | `~/.codex/skills/<n>/SKILL.md` | yes | map agents → Codex runtime; models → GPT tier |
| Gemini | `~/.gemini/skills/<n>/SKILL.md` | yes (subset) | models → Gemini tier; agents mostly `inline` |
| OpenCode | `~/.opencode/skills/<n>/SKILL.md` | yes | provider-agnostic; name model by configured provider |
| Antigravity (agy) | `~/.antigravity/skills/<n>/SKILL.md` | yes | Gemini-based; agents mostly `inline` |
| lemon-code (lemon) | `~/.lemoncode/skills/<n>.md` (flat) | smart-dispatch-planner | open-source models (Qwen/Ollama); name local model |

If the target CLI lacks a skill/agent you'd suggest, downgrade to `inline` or `TBD` — never name a tool the executor can't load.

---

## Quality checklist (run before delivering)
- [ ] Output is a prompt, not task execution.
- [ ] All 9 skeleton blocks present (or justified omission).
- [ ] DO-NOT block is task-specific, not generic.
- [ ] Every plan step has a `→ verify:` check.
- [ ] No fabricated repo context; gaps surfaced as questions or `TBD`.
- [ ] Model/agent/skill map is honest (`TBD` over wrong guess) and executor-aware.
- [ ] Effort + Time + Token estimate present in Execution Map.
- [ ] Triviality gate checked (skipped refino if request was trivial/clear).
- [ ] Probe used `rtk` and stayed cheap (no large `cat` into context).
- [ ] Changelog of improvements appended.
- [ ] User's language + domain terms preserved.
