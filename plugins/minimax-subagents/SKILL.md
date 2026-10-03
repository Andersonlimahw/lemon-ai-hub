---
name: minimax-subagents
description: Delegate work to MiniMax subagents and tiered workers on the Token Plan subscription, inline through OpenCode, from Claude Code, Codex, OpenCode, Antigravity (Agy) or Gemini CLI. Routes budget/balanced/quality tasks to MiniMax-M2.7-highspeed, MiniMax-M3 or MiniMax-M3.1-Flash-Preview with tunable thinking depth, via `mm-run` or the mm_fast/mm_m3/mm_flash workers. Use when the user asks to use MiniMax, offload coding/refactor/docs/long-context/multimodal work to a subscription model, run "opencode run -m minimax/...", or spread parallel workers without paying per token.
---

# MiniMax Subagents (Token Plan, inline via OpenCode)

MiniMax runs on a **flat Token Plan subscription** (5-hour rolling + weekly
quota windows). Cost is quota, not dollars per token. Optimize for **fewer
input tokens per call** and **graceful fallback when a window closes**.

OpenCode is the execution harness: it holds the `minimax` provider and the
subscription key. Every other harness calls it **inline** with one shell
command. No harness ever reads or prints the key.

## Route table

| Tier | Model (`minimax/…`) | Worker family | Efforts | Use for |
|------|--------------------|---------------|---------|---------|
| budget | `MiniMax-M2.7-highspeed` | `mm_fast_worker_<e>` | low · medium · high | docs, comments, changelogs, boilerplate, mechanical tests, lint fixes |
| balanced | `MiniMax-M3` | `mm_m3_worker_<e>` | low · medium · high | implementation, refactor, integration tests, 1M-context reads |
| quality | `MiniMax-M3.1-Flash-Preview` | `mm_flash_worker_<e>` | low · medium · high · xhigh · max | architecture, plans, root cause, multimodal, long-context reasoning |

- Only **M3.1-Flash-Preview** has tunable thinking depth (`reasoningEffort` /
  OpenCode `--variant`). On M3 and M2.7 the effort is a budget contract only.
- M3.1-Flash-Preview is available only on the Token Plan (M Plan) and MiniMax
  Code. Source: <https://platform.minimax.io/docs/guides/models-intro>.
- Safety floor: security audits, production incidents, destructive ops and
  legal/medical/financial work stay on the `quality` tier at `high`+ effort
  and get a review from a second model before merge.

## Call it

`mm-run` is the single entry point (`bin/mm-run` → `scripts/mm_run.py`):

```bash
mm-run --tier quality --effort high -- "self-contained prompt"
mm-run --tier budget -- "write the CHANGELOG entry for <diff summary>"
mm-run --agent mm_m3_worker_medium --dir "$PWD" -f src/app.ts -- "refactor …"
git diff | mm-run --tier balanced -- -      # prompt from stdin
mm-run --check                               # verify opencode + models
```

What `mm-run` does for you:

1. `--tier` picks the **installed lean worker** (`mm_<family>_worker_<effort>`,
   default effort low/medium/high per tier) and falls back to
   `-m minimax/<model>` when workers are not installed.
2. Lean workers allowlist core tools only. The default OpenCode agent ships
   every MCP tool schema: **~118k input tokens per call vs ~6.7k** measured on
   2026-10-03. Never pass `--no-agent` unless you need MCP tools.
3. Strips `<think>` blocks from stdout (`--thinking` keeps them).
4. Retries **once** on transient errors (`UnknownError`, 5xx, resets).
5. Caps concurrent MiniMax calls with a file-lock semaphore
   (`MM_MAX_PARALLEL`, default 3; Plus ≈3-4 agents, Max ≈4-5, Ultra ≈6-7).

Exit codes: `0` ok · `2` usage · `3` preflight · `75` quota window hit
(stdout starts with `ROUTE-FALLBACK:`) · `124` timeout · `1` other.

`124` with no output usually means OpenCode hung at start-up (`init`), most
often a broken dependency install in the project's own `.opencode/` dir. Run
`opencode run --print-logs -m minimax/MiniMax-M3 -- hi` there to confirm, and
keep `--timeout` on (default 1800 s, `MM_TIMEOUT`).

## Per harness

| Harness | Cheapest path | Parallel / background path |
|---------|---------------|----------------------------|
| Claude Code | Bash: `mm-run --tier … -- "…"` | Agent tool → bridge `mm_flash_worker_high` (Haiku relay) or `minimax-subagents:minimax-worker` |
| OpenCode | `@mm_m3_worker_medium` or the `task` tool inside a session | `opencode run --agent mm_flash_worker_max -- "…"` (workers are `mode: all`) |
| Codex | shell `mm-run …` outside the sandbox: approve the escalation, or run with the `minimax` profile below | several `mm-run` calls in parallel; the semaphore keeps quota safe |
| Antigravity (Agy) | shell `mm-run …` | bridge agents symlinked into `~/.agy/agents` |
| Gemini CLI | `run_shell_command`: `mm-run …` | parallel shell calls |

**Codex sandbox.** `workspace-write` blocks network and writes outside the
workspace, and OpenCode must write `~/.local/share/opencode`. Either approve
the escalation when Codex asks, or start Codex with these overrides (verified
with `codex exec` on 2026-10-03; put them in a shell alias such as `codex-mm`):

```bash
codex -s workspace-write \
  -c sandbox_workspace_write.network_access=true \
  -c "sandbox_workspace_write.writable_roots=[\"$HOME/.local/share/opencode\",\"$HOME/.local/state/opencode\",\"$HOME/.cache/opencode\",\"$HOME/.cache/minimax-subagents\",\"$HOME/.config/opencode\"]"
```

If a hook forces an `rtk` prefix on shell commands, call `rtk proxy mm-run …`.

Your own direct form still works and is the baseline the wrapper builds on:
`opencode run -m minimax/MiniMax-M3.1-Flash-Preview --variant high "prompt"`.

## Prompt contract

The worker sees nothing of the caller's conversation. Every prompt states:
goal · files/paths · constraints (style, no drive-by refactors) · acceptance
check (exact command) · output format (changed files + verification result).
Attach files with `-f` instead of pasting them.

## Quota policy

- `75` / `ROUTE-FALLBACK` → **do not retry on MiniMax**. Route the same task
  to the printed fallback: budget → `haiku_worker_low` or
  `opencode-go/deepseek-v4-flash`; balanced → `sonnet_worker_medium` or
  `opencode-go/glm-5.2`; quality → `opus_worker_high` or
  `opencode-go/deepseek-v4-pro`.
- Prefer `budget`/`balanced` for volume; spend `mm_flash` at `xhigh`/`max`
  only on hard reasoning. Batch small edits into one call.
- Use `--dir` so the worker's tools resolve paths in the right project.

## Install / update (one shot, idempotent)

```bash
bash ~/Projects/IA/lemon-ai-hub/plugins/minimax-subagents/scripts/install.sh
```

Links `mm-run` into `~/.local/bin`, links this skill into the curated skill
dirs (OpenCode, Gemini, Agy, `.agents`), installs the `minimax` worker lane
(OpenCode agents + Claude/Agy bridges) through
`smart-sub-agents/scripts/install_worker_matrix.py`, then runs `mm-run --check`.
Claude Code gets the skill and `minimax-worker` agent from the `lemon-ai-hub`
marketplace (`claude plugin install minimax-subagents@lemon-ai-hub`).

OpenCode provider (once). Keep the key in the environment, not in the file:

```jsonc
"provider": {
  "minimax": {
    "npm": "@ai-sdk/openai-compatible",
    "name": "MiniMax",
    "options": { "baseURL": "https://api.minimax.io/v1", "apiKey": "{env:MINIMAX_API_KEY}" },
    "models": { "MiniMax-M3.1-Flash-Preview": { "reasoning": true }, "MiniMax-M3": {}, "MiniMax-M2.7-highspeed": {} }
  }
}
```

Full model limits and variants: `references/models.md`.

## DO NOT

- Print, read, echo, or commit the subscription key (`sk-cp-…`).
- Retry after exit `75`, or raise `MM_MAX_PARALLEL` past the plan's agent count.
- Use `--no-agent` for routine work (17× more input tokens).
- Mark delegated work done without the worker's verification evidence.
