---
name: minimax-subagents
description: Delegate work to MiniMax subagents and tiered workers on the M Plan / Token Plan subscription, inline through MiniMax Code (`mcode exec`, default) or OpenCode, from Claude Code, Codex, OpenCode, Antigravity (Agy) or Gemini CLI. Routes budget/balanced/quality tasks to MiniMax-M2.7-highspeed, MiniMax-M3 or MiniMax-M3.1-Flash-Preview with tunable thinking depth, via `mm-run` or the mm_fast/mm_m3/mm_flash workers. Use when the user asks to use MiniMax or mcode, offload coding/refactor/docs/long-context/multimodal work to a subscription model, run "opencode run -m minimax/...", or spread parallel workers without paying per token.
---

# MiniMax Subagents (subscription, inline via MiniMax Code or OpenCode)

MiniMax runs on a **flat subscription** (M Plan / Token Plan: 5-hour rolling +
weekly quota windows). Cost is quota, not dollars per token. Optimize for
**fewer input tokens per call** and **graceful fallback when a window closes**.

`mm-run` executes every call through one of two backends; other harnesses call
it **inline** with one shell command. No harness ever reads or prints a key.

| Backend | When | Auth | Input tokens / trivial call |
|---------|------|------|-----------------------------|
| `mcode` (default) | MiniMax Code installed and logged in | OAuth login, no key on disk | ~14k |
| `opencode` | `--backend opencode`, `MM_BACKEND=opencode`, mcode missing, or a non-`mm_*` agent | `minimax` provider key in OpenCode | ~7k (lean `mm_*` worker) |

`mcode exec` adds `--effort`, `--timeout`, structured JSON usage and the managed
model route. OpenCode wins on raw input tokens and on its MCP/plugin ecosystem.

## Route table

| Tier | Model (`minimax/…`) | Worker family | Efforts | Use for |
|------|--------------------|---------------|---------|---------|
| budget | `MiniMax-M2.7-highspeed` | `mm_fast_worker_<e>` | low · medium · high | docs, comments, changelogs, boilerplate, mechanical tests, lint fixes |
| balanced | `MiniMax-M3` | `mm_m3_worker_<e>` | low · medium · high | implementation, refactor, integration tests, 1M-context reads |
| quality | `MiniMax-M3.1-Flash-Preview` | `mm_flash_worker_<e>` | low · medium · high · xhigh · max | architecture, plans, root cause, multimodal, long-context reasoning |

- Only **M3.1-Flash-Preview** has tunable thinking depth (`mcode --effort` /
  OpenCode `--variant`). On M3 and M2.7 the effort is a budget contract only;
  `mcode` rejects `--effort` there, so `mm-run` never sends it.
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
mm-run --backend opencode --tier budget -- "…"   # force OpenCode
mm-run --check                               # verify both backends + models
```

What `mm-run` does for you:

1. Picks the backend (`--backend` > `MM_BACKEND` > `auto` = mcode when
   installed). `--agent mm_<family>_worker_<effort>` maps to the same model and
   effort on mcode; any other agent name runs on OpenCode.
2. mcode: `mcode exec --cwd <dir> --model minimax/<model> [--effort] --permission
   smart --output-format json` (`MM_MCODE_PERMISSION` overrides the policy).
   Quality tier defaults to `--effort high`.
3. OpenCode: `--tier` picks the **installed lean worker** and falls back to
   `-m minimax/<model>`. The default OpenCode agent ships every MCP tool
   schema: **~118k input tokens per call vs ~6.7k** (measured 2026-10-03).
   Never pass `--no-agent` unless you need MCP tools.
4. Strips `<think>` blocks from stdout (`--thinking` keeps them).
5. Retries **once** on transient errors (`UnknownError`, 5xx, resets). In
   auto mode, an mcode failure that is not quota/timeout gets **one** retry on
   the OpenCode backend (sandbox denials, local locks, crashes).
6. Caps concurrent MiniMax calls with a file-lock semaphore
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
workspace. Inside it, `mcode` 0.6.2 still fails on an internal migration lock
even with `~/.minimax*` writable, so `mm-run` (auto mode) retries once on
OpenCode, which works once its dirs are writable. Either approve the
escalation when Codex asks (mcode then runs normally), or start Codex with
these overrides (verified with `codex exec` on 2026-10-04; alias as `codex-mm`):

```bash
codex -s workspace-write \
  -c sandbox_workspace_write.network_access=true \
  -c "sandbox_workspace_write.writable_roots=[\"$HOME/.minimax\",\"$HOME/.minimax-code\",\"$HOME/.cache/minimax-subagents\",\"$HOME/.local/share/opencode\",\"$HOME/.local/state/opencode\",\"$HOME/.cache/opencode\",\"$HOME/.config/opencode\"]"
```

Set `MM_BACKEND=opencode` there to skip the doomed mcode attempt.

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

MiniMax Code (default backend, once). The installer lands in
`~/.minimax-code/bin/mcode`; `mm-run` finds it there even off PATH
(`MM_MCODE_BIN` overrides, `MM_MCODE_BIN=""` disables it):

```bash
curl -fsSL https://filecdn.minimax.chat/public/install.sh | bash   # review the script first
~/.minimax-code/bin/mcode login                                    # OAuth, no key on disk
```

OpenCode provider (fallback backend, once). Keep the key in the environment, not in the file:

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
