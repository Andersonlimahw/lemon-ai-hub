---
name: smart-dispatch
description: Automatically routes tasks to the optimal AI agent, model, or provider based on complexity, cost, and capability. Optionally combines with smart-sub-agents to pin harness, provider, model, and effort through an explicit combine_smart_subagents parameter. Use when implementing features, fixing bugs, or any multi-step development work. Triggers on "implement", "build", "create", "fix", "add feature", "develop", or when the user asks to do any coding task.
---

# Smart Agent & Model Dispatch (Pro Edition)

## Stage input — consume the EXEC-MAP contract if present

If an `EXEC-MAP v1` block from `senior-prompt-engineer` is in context, **consume it instead of re-deriving complexity:**
- `EXEC-MAP.effort` seeds the tier (trivial/low → Tier 0; medium/high → Tier 1).
- `EXEC-MAP.models` is the per-phase routing intent (`plan`→Opus/quality, `impl`→Sonnet/balanced, `mechanical`→Haiku/budget); honor it unless validation proves it wrong.
- `EXEC-MAP.executor` picks the provider/CLI; map model tiers to that CLI's tiers.
- `EXEC-MAP.mcp` lists tools to wire up.
Treat the map as a starting routing decision, not gospel — escalation rules (Tier 1) still override it when validation keeps failing. With no EXEC-MAP, derive routing from the request as usual.

## Optional combination parameter: `combine_smart_subagents`

When `smart-sub-agents` is installed, support this parameter in the dispatch request:

```text
combine_smart_subagents: ask | always | never
```

The default is `ask`, but ask only when the task has explicit provider/model/effort requirements, needs more than one provider/harness, or would materially benefit from isolated parallel subagents. Use this exact question once:

> Combine this dispatch with `smart-sub-agents` to pin the harness, provider, model, and effort and render a subagent configuration? (yes/no)

- `yes` or `always`: invoke `smart-sub-agents`, consume its `ROUTE-MAP v1`, and preserve its explicit route unless validation proves it unavailable.
- `no` or `never`: continue with the normal smart-dispatch matrix and do not ask again for the same task.
- If the user already supplied `combine_smart_subagents`, honor it without asking.

The combined route must log both the requested and effective `harness/provider/model/effort`. A provider fallback is visible and auditable; STOP/Ctrl+C or an explicit cancellation must not retry or fall back.

If `smart-sub-agents` is unavailable, state that fact and continue with the standard dispatch table. Do not recreate its catalog inside this skill.

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

| Tier | Claude worker | Codex worker | OpenCode Zen | OpenCode Go | Gemini |
|------|---------------|--------------|--------------|-------------|--------|
| **budget** | `haiku_worker_{low\|medium\|high}` | `luna_worker_{low…max}` | `zen_flash_*` / `zen_luna_*` | `go_luna_*` / `go_flash_*` | Flash-Lite |
| **balanced** | `sonnet_worker_{low…xhigh}` | `terra_worker_{low…max}` | `zen_terra_*` / `zen_grok_*` | `go_grok_*` / `go_glm_*` / `go_kimi_*` | Flash |
| **quality** | `opus_worker_{low…max}` | `sol_worker_{low…max}` | `zen_sol_*` / `zen_opus_*` | `go_pro_*` / `go_qwen_max_*` | Pro |

Use named workers when the harness supports custom agents. Prefer the **cheapest worker that still fits the task**. Codex: **Luna** mechanical, **Terra** implementation, **Sol** architecture/root-cause. Claude: **Haiku / Sonnet / Opus**. OpenCode: prefer **Go** lane when subscribed; else **Zen free**.

### Budget contract (mandatory on every dispatch)

Announce before work:

```text
DISPATCH
worker: <name>
tier: budget|balanced|quality
effort: low|medium|high|xhigh|max
tokens: <range from taskRouting>
time: <range from taskRouting>
verify: <command>
```

Source of truth: `plugins/smart-sub-agents/references/provider-matrix.json` → `taskRouting` + `workerMatrix`.
Refresh models: `python3 plugins/smart-sub-agents/scripts/sync_provider_matrix.py --write`
Reinstall workers: `python3 plugins/smart-sub-agents/scripts/install_worker_matrix.py`

| Task type | Tier | Default worker (Claude / Codex) | Tokens | Time |
|-----------|------|----------------------------------|--------|------|
| Docs, comments, changelogs, summaries, translations | budget | `haiku_worker_low` / `luna_worker_low` | 2k–8k | 1–5min |
| Test writing — mechanical / known pattern | budget | `haiku_worker_low` / `luna_worker_low` | 3k–12k | 3–10min |
| Lint / typecheck / format fixes | local CLI → budget | Tier 0 first, then haiku/luna | 1k–6k | 1–5min |
| Boilerplate / scaffolding | budget | `haiku_worker_medium` / `luna_worker_medium` | 2k–10k | 2–8min |
| Implementation, refactor | balanced | `sonnet_worker_medium` / `terra_worker_medium` | 8k–40k | 10–40min |
| Multi-step agentic | balanced | `sonnet_worker_high` / `terra_worker_high` | 15k–60k | 15–60min |
| Test design — integration/e2e strategy | balanced | `sonnet_worker_medium` / `terra_worker_medium` | 6k–25k | 8–25min |
| Plan, architecture, security audit, migration | quality | `opus_worker_high` / `sol_worker_high` | 15k–80k | 15–90min |
| Root-cause / hard debug | quality | `opus_worker_xhigh` / `sol_worker_xhigh` | 20k–100k | 20–90min |

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
| **Complex Logic / Math** | Codex Sol | Highest-reasoning Codex subagent tier for algorithms and root cause. |
| **Agentic Chains / Auth** | Claude Sonnet 4.6+ | Best tool-use and multi-step autonomy. |
| **Deep Plan / Architecture** | Codex Sol or Claude Opus 4.8 / Fable 5 | Use Sol for codebase-grounded decisions; use Opus/Fable for cross-domain synthesis. |
| **Open Source / Docs** | OpenCode | Deep integration with community patterns. |

---

## Rules

- **Announce & Verify**: Always say what you are doing and how you will verify it.
- **Token Economy**: Prefer Gemini Flash for context-heavy reads but simple edits.
- **Fail Fast**: Don't loop on cheap models. Escalate early.
- **Local First**: CLI tools > AI Agents for mechanical fixes.
