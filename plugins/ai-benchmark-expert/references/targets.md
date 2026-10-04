# Target command lines

Tested headless invocations. Each runs with `cwd` = the run's workdir; the
prompt goes to stdin unless the command uses `{prompt}` / `{prompt_file}`.

| Harness | `cmd` | `parse` | Notes |
|---------|-------|---------|-------|
| Claude Code | `claude -p --model {model} --output-format json --permission-mode bypassPermissions` | `claude-json` | Reports `total_cost_usd` and token usage. Add `"unset_env": ["ANTHROPIC_BASE_URL", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_MODEL"]` when your shell routes Claude Code through a gateway, so the run hits the intended provider. |
| Claude Code (judge, no tools) | `claude -p --model {model} --output-format json --tools ''` | `claude-json` | Judge only reads the prompt; tools disabled. |
| Codex | `codex exec --json --skip-git-repo-check --sandbox workspace-write -` | `codex-jsonl` | `-` reads the prompt from stdin. Add `-m <model>` to pin a model. Token usage from `turn.completed`; no dollar cost (subscription) unless `price` is set. |
| Gemini CLI | `gemini --skip-trust --yolo --output-format json -m {model} -p {prompt}` | `gemini-json` | `--skip-trust` is required in a fresh directory. Always pin `-m`: auto-routing can pick a model your plan has no quota for (seen: `gemini-3.1-pro`, free-tier limit 0) and the run fails. Tokens are summed across the router and main model. |
| Codex (note) | — | — | `--full-auto` was removed from `codex exec`; use `--sandbox workspace-write` so the agent can write in its workdir. |
| OpenCode | `opencode run --format json -m {model} {prompt}` | `opencode-json` | Works for any OpenCode provider (`minimax/MiniMax-M3`, `zai/glm-…`, `openrouter/…`). Reports cost at list price. |
| MiniMax via mm-run | `mm-run --tier balanced --dir {workdir} -- {prompt}` | `text` | Uses the minimax-subagents plugin backend; set `price` for cost. |
| Any API / script | `python3 my_client.py --model {model} < {prompt_file}` | `text` | Print the final answer to stdout. |

## Pinning model and reasoning effort

Put the model in `"model"` and reference `{model}` so the report shows it. Use
separate targets for the same model at different efforts (e.g. Codex
`-c model_reasoning_effort=high` vs `low`) — effort changes both quality and
cost, so it is a different contestant.

## Pricing

When a CLI reports tokens but not dollars, add `"price": {"input": <$ per
Mtok>, "output": <$ per Mtok>}`. Input tokens include cache reads/writes as
reported by the CLI, so list-price estimates are an upper bound when caching
discounts apply.
