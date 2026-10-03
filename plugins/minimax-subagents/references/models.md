# MiniMax models for subagent routing

Checked 2026-10-03 against <https://platform.minimax.io/docs/guides/models-intro>
and the live `opencode models minimax` list.

| Model id (`minimax/…`) | Tier | Context | Thinking depth | Notes |
|------------------------|------|---------|----------------|-------|
| `MiniMax-M3.1-Flash-Preview` | quality | 1M | tunable: low · medium · high · xhigh · max | Frontier multimodal coding. Token Plan (M Plan) and MiniMax Code only. |
| `MiniMax-M3` | balanced | 1M | fixed | Frontier multimodal coding. |
| `MiniMax-M2.7` | balanced | — | fixed | Real-world engineering, office delivery. Not in a worker family; use `--model`. |
| `MiniMax-M2.7-highspeed` | budget | — | fixed | Same quality as M2.7, much faster inference. |
| `MiniMax-M2.5`, `-M2.5-highspeed`, `-M2.1`, `-M2` | legacy | — | fixed | Avoid for new routes. |

## Endpoints

| Protocol | Base URL | Used by |
|----------|----------|---------|
| OpenAI-compatible | `https://api.minimax.io/v1` | OpenCode provider `minimax` (`@ai-sdk/openai-compatible`) |
| Anthropic-compatible | `https://api.minimax.io/anthropic` | Claude Code style tools (`ANTHROPIC_BASE_URL`), whole session only |

Claude Code can only point a **whole session** at MiniMax (via
`ANTHROPIC_BASE_URL`); a single subagent cannot switch provider. That is why
this plugin runs MiniMax through OpenCode inline and keeps Claude Code on
Anthropic.

## Token Plan

- Flat subscription: Plus $22 · Max $55 · Ultra $132 per month.
- Quota: 5-hour rolling window + weekly window; unused quota does not carry over.
- Sized for 3-4 (Plus), 4-5 (Max), 6-7 (Ultra) concurrent agents → `MM_MAX_PARALLEL`.
- When a window closes: wait, use purchased credits, upgrade, or switch the key
  to pay-as-you-go. `mm-run` returns exit `75` so callers fall back instead.

## Measured on this setup (2026-10-03, OpenCode 1.18.34)

| Route | Input tokens for "Reply OK" | Wall time |
|-------|-----------------------------|-----------|
| `-m minimax/MiniMax-M2.7-highspeed` (default `build` agent, all MCP tools) | ~118k | ~10 s |
| lean worker (`tools: "*": false` + core allowlist, `mode: all`) | ~4.2k-6.7k | ~4 s |

- `opencode run --agent X` ignores agents declared `mode: subagent` and falls
  back to the default agent; inline workers must be `mode: all`.
- `--variant` on a model without variants is silently ignored.
- A project with its own `.opencode/` directory makes OpenCode install that
  directory's dependencies at start-up; a broken install there hangs at
  `init` before any model call. Keep `--timeout` on (default 1800 s) and run
  from a clean project root.
