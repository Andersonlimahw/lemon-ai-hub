---
name: smart-dispatch
description: Automatically routes tasks to the optimal AI agent, model, or provider based on complexity, cost, and capability. Use when implementing features, fixing bugs, or any multi-step development work. Triggers on "implement", "build", "create", "fix", "add feature", "develop", or when the user asks to do any coding task.
---

# Smart Agent & Model Dispatch (Pro Edition)

## Stage input — consume the EXEC-MAP contract if present

If an `EXEC-MAP v1` block from `senior-prompt-engineer` is in context, **consume it instead of re-deriving complexity:**
- `EXEC-MAP.effort` seeds the tier (trivial/low → Tier 0; medium/high → Tier 1).
- `EXEC-MAP.models` is the per-phase routing intent (`plan`→Opus/quality, `impl`→Sonnet/balanced, `mechanical`→Haiku/budget); honor it unless validation proves it wrong.
- `EXEC-MAP.executor` picks the provider/CLI; map model tiers to that CLI's tiers.
- `EXEC-MAP.mcp` lists tools to wire up.
Treat the map as a starting routing decision, not gospel — escalation rules (Tier 1) still override it when validation keeps failing. With no EXEC-MAP, derive routing from the request as usual.

## Tier 0 — Automated Boilerplate & Verification (RTK Bypass)

### 0.1 Local-First Rule
Before dispatching to an AI agent for Tier 0 tasks, attempt to solve it using local CLI tools.
- **Lint**: Run `npm run lint --fix` or `eslint --fix`.
- **Formatting**: Run `prettier --write`.
- **Typecheck**: Run `tsc` and check if errors are trivial.

### 0.2 RTK Bypass Dispatch (The "Hammer")
If local tools fail or aren't enough, use **Gemini-Flash YOLO** via RTK.
- **Lint/Typecheck/I18n/Tests**: Route to `rtk gemini --yolo`.

### 0.3 Verification Mandate
Any agent dispatched in YOLO/Bypass mode **MUST** execute the relevant validation command before completion.
- If it fixed types, it **must** run `tsc --noEmit`.
- If it fixed lint, it **must** run `npm run lint`.
- If it fixed tests, it **must** run `npm run test <file>`.

---

## Tier 1 — Escalation & Intelligence Mapping

### 1.0 Task-Type → Model Routing (default table)

Always pick the **cheapest tier that passes validation**; escalate per 1.1. Tiers map per provider:

| Tier | Claude | Codex | Gemini |
|------|--------|-------|--------|
| **budget** | Haiku 4.5 | gpt low/mini reasoning | Flash |
| **balanced** | Sonnet 4.6 | gpt medium reasoning | Pro |
| **quality** | Opus 4.8 / Fable 5 | gpt high reasoning | Pro (max thinking) |

| Task type | Tier | Notes |
|-----------|------|-------|
| Docs, comments, changelogs, summaries, translations | budget | Haiku-class is enough; never burn Opus here |
| Test writing — mechanical / known pattern | budget | Verify with test run (0.3 mandate) |
| Lint / typecheck / format fixes | local CLI → budget | Tier 0 rules apply first |
| Implementation, refactor, multi-step agentic | balanced | Sonnet-class default for code |
| Test design — integration/e2e strategy | balanced | Strategy needs reasoning; writing the cases can drop to budget |
| Plan, architecture, root-cause, security audit, migration | quality | Opus-class; deep reasoning pays for itself |

EXEC-MAP's `models: {plan, impl, mechanical}` maps 1:1 to quality/balanced/budget rows above.

### 1.1 Auto-Escalation Policy
If a Tier 0 agent fails to resolve the issue (validation still fails) after **2 attempts**, the dispatcher MUST:
1. Stop using the "cheap" model.
2. Escalate the task to a Tier 1 model (Claude Sonnet or Gemini Pro).
3. Notify the user: "Escalating to [Model] due to persistent validation failures."

### 1.2 Capability Matrix
| Domain | Best Platform | Reason |
|--------|---------------|--------|
| **Multimodal / UI screenshots** | Gemini Pro (latest) | Best image/screenshot interpretation. |
| **Complex Logic / Math** | Codex (gpt high reasoning) | Superior reasoning for algorithms. |
| **Agentic Chains / Auth** | Claude Sonnet 4.6+ | Best tool-use and multi-step autonomy. |
| **Deep Plan / Architecture** | Claude Opus 4.8 / Fable 5 | Strongest long-horizon reasoning. |
| **Open Source / Docs** | OpenCode | Deep integration with community patterns. |

---

## Rules

- **Announce & Verify**: Always say what you are doing and how you will verify it.
- **Token Economy**: Prefer Gemini Flash for context-heavy reads but simple edits.
- **Fail Fast**: Don't loop on cheap models. Escalate early.
- **Local First**: CLI tools > AI Agents for mechanical fixes.

