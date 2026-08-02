---
name: smart-sub-agents
description: Creates and routes portable subagents by harness, provider, model, and effort. Use when a task needs explicit model selection, multi-provider delegation, dynamic effort, parallel subagents, or configuration for Claude Code, Codex, OpenCode, Antigravity, Gemini CLI, or lemon-code.
---

# Smart Sub-Agents

Use this skill to turn a vague delegation request into a reproducible route:

```yaml
harness: opencode
provider: deepseek
model: deepseek-v4-flash
effort: max
```

The source of truth is [`references/provider-matrix.json`](references/provider-matrix.json). It separates two concepts that are often incorrectly mixed:

- **Harness**: the tool that owns the subagent (`claude-code`, `codex`, `opencode`, `antigravity`, `gemini-cli`, or `lemon-code`).
- **Provider/model**: the model service and model ID used by that harness (`anthropic/claude-opus-5`, `openai/gpt-5.6`, and so on).

## Routing protocol

1. Select the harness that can actually execute the work. Use `opencode` when the requested provider is not native to the current harness.
2. Select a profile: `budget`, `balanced`, `quality`, or `research`.
3. Apply explicit `provider`, `model`, and `effort` overrides. Explicit values win over profile defaults.
4. Validate the exact model ID against the matrix. Never silently replace an unavailable model with a similarly named one.
5. Map the normalized effort to the provider's native control. If the provider only supports a boolean thinking switch or model-specific variants, record that limitation in the route.
6. Emit one `ROUTE-MAP v1` block and, when requested, render the harness-specific subagent configuration.

Recommended profile defaults:

| Profile | Effort | Use for |
| --- | --- | --- |
| `budget` | `low` | Formatting, bounded checks, repetitive work |
| `balanced` | `medium` | Normal implementation and integration |
| `quality` | `high` | Architecture, security, difficult debugging |
| `research` | `max` | Long-horizon research or adversarial synthesis |

`max` is a quality/cost choice, not a promise that every provider accepts a literal `max` request parameter. The renderer preserves the requested level and exposes the effective native mapping.

## Normalizing the examples

The following common inputs are normalized only when the catalog has an explicit alias:

| Input | Canonical route |
| --- | --- |
| `openai / gpt-5.6 lunce` | `openai / gpt-5.6-luna` |
| `opencode / kimi k3` | `moonshotai / kimi-k2` (Kimi K3 is not in the verified matrix) |
| `anthropic / Opus %` | `anthropic / claude-opus-5` |
| `deepseek api / deepseek v4 flash` | `deepseek / deepseek-v4-flash` |
| `google / Gemini 3.5 Pro` | `google / gemini-2.5-pro` or `google / gemini-3.1-pro-preview` |

These are corrections, not fuzzy guesses. If an alias is not listed, ask for the exact provider/model ID or run the catalog validator before routing.

## Harness configuration

Use the local renderer to generate artifacts without mutating global configuration:

```bash
python3 plugins/smart-sub-agents/scripts/validate_catalog.py
python3 plugins/smart-sub-agents/scripts/render_agents.py \
  --harness opencode \
  --provider deepseek \
  --model deepseek-v4-flash \
  --effort max \
  --output-dir .smart-sub-agents/generated
```

To create one route for every supported harness using a profile:

```bash
python3 plugins/smart-sub-agents/scripts/render_agents.py \
  --harness all --profile balanced --output-dir .smart-sub-agents/generated
```

The renderer is deliberately non-destructive. Inspect generated files before copying them to `~/.claude/agents/`, `~/.codex/agents/`, `~/.config/opencode/agents/`, or another harness-specific location. API keys are never read or written by this skill.

Native behavior covered by the renderer:

- **Claude Code**: Markdown subagents with `model` and `effort`; native provider is Anthropic.
- **Codex**: TOML custom agents with `model` and `model_reasoning_effort`; native provider is OpenAI.
- **OpenCode**: `opencode.json` agent entries using `provider/model`; it can route across the matrix, but effort options remain model/provider-specific.
- **Antigravity/Gemini CLI**: JSON handoff manifests because the managed agent surface does not expose the same local custom-agent file contract.
- **lemon-code**: JSON route manifest for its provider-agnostic dispatcher.

## Contract returned to smart-dispatch

When this skill is combined with `smart-dispatch`, return exactly one route contract for the selected subagent:

```text
ROUTE-MAP v1
harness: opencode
provider: deepseek
model: deepseek-v4-flash
effort: max
native_effort: thinking=true
fallback: openrouter/auto
reason: quality-first coding route with DeepSeek V4 Flash thinking mode
```

Do not add secrets, invent provider support, or fall back after an explicit cancellation. A fallback is only a declared route for a provider outage or unavailable model and must be visible to the caller.

## Refresh policy

The matrix is a curated snapshot, not a live provider API. Check the linked official documentation before production rollout and update `updated` plus the affected source URL when a model is added, deprecated, renamed, or changes effort semantics. Run the validator and tests after every matrix change.
