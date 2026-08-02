# Provider and harness matrix

Snapshot date: 2026-08-02. Model availability, IDs, pricing, and effort controls change; verify the linked provider documentation before production rollout.

## Recommended routes

| Workload | Harness | Provider | Model | Effort | Native control |
| --- | --- | --- | --- | --- | --- |
| Fast bounded worker | Codex | OpenAI | `gpt-5.6-luna` | low | `model_reasoning_effort` |
| Normal implementation | Codex | OpenAI | `gpt-5.6-terra` | medium | `model_reasoning_effort` |
| Complex implementation/review | Claude Code | Anthropic | `claude-opus-5` | high | `effort` |
| Long-horizon research | Claude Code | Anthropic | `claude-fable-5` | max | adaptive effort |
| Low-cost coding | OpenCode | DeepSeek | `deepseek-v4-flash` | high/max | thinking mode |
| Balanced multimodal work | OpenCode | Google | `gemini-3.6-flash` | medium | model-specific thinking config |
| Deep multimodal reasoning | OpenCode | Google | `gemini-3.1-pro-preview` | high | model-specific thinking config |
| Cross-provider fallback | OpenCode/lemon-code | OpenRouter | `openrouter/auto` | medium/high | selected model-specific |
| Managed browser/code agent | Antigravity | Google | `antigravity-agent-preview` | high/max | managed surface |

## Corrections to the example names

The requested examples contain shorthand or names that are not in the verified matrix. Use the canonical values below:

| User input | Canonical value | Why |
| --- | --- | --- |
| `l 5.6 lunce` | `gpt-5.6-luna` | `l...` and `lunce` are not model IDs; Luna is the documented OpenAI efficiency tier. |
| `kimi k3` | `moonshotai/kimi-k2` | OpenCode's current provider docs list Kimi K2; Kimi K3 is not asserted here. |
| `Opus %` | `claude-opus-5` | `%` is not an Anthropic model suffix. |
| `deepseek v4 flash` | `deepseek/deepseek-v4-flash` | Exact DeepSeek API model ID. |
| `Gemini 3.5 Pro` | `google/gemini-2.5-pro` or `google/gemini-3.1-pro-preview` | The current Google catalog lists Gemini 2.5 Pro and Gemini 3.1 Pro Preview, not Gemini 3.5 Pro. |

## Harness versus provider

Claude Code, Codex, OpenCode, Antigravity, Gemini CLI, and lemon-code are execution harnesses. Anthropic, OpenAI, Google, DeepSeek, Moonshot AI, Qwen, Z.AI, and OpenRouter are providers or gateways. A harness/provider pair is valid only when the harness can load the provider or can delegate to a cross-provider harness such as OpenCode.

| Harness | Native configuration | Provider scope | Effort caveat |
| --- | --- | --- | --- |
| Claude Code | `~/.claude/agents/*.md` | Anthropic model aliases/IDs | `effort` is native for supported Claude models. |
| Codex | `~/.codex/agents/*.toml` or `.codex/agents/*.toml` | OpenAI model IDs | `model_reasoning_effort` is explicit and model-dependent. |
| OpenCode | `opencode.json` agent entries or `~/.config/opencode/agents/*.md` | 75+ providers and local models | Use `/models` and `/variants`; do not assume `low/high/max` exists for every model. |
| Antigravity | Managed agent surface | Google managed agent models | Renderer emits a handoff manifest; no unsupported local agent file is invented. |
| Gemini CLI | CLI/project instructions and model selection | Google Gemini | Model-specific thinking controls vary. |
| lemon-code | Runtime route manifest | Provider-agnostic | The runtime owns final adapter semantics. |

## Sources

- [OpenAI model guidance](https://developers.openai.com/api/docs/guides/latest-model) and [Codex subagents](https://developers.openai.com/codex/subagents)
- [Anthropic model overview](https://platform.claude.com/docs/en/about-claude/models/overview) and [Claude Code subagents](https://code.claude.com/docs/en/sub-agents)
- [Google Gemini models](https://ai.google.dev/gemini-api/docs/models)
- [DeepSeek models and pricing](https://api-docs.deepseek.com/quick_start/pricing)
- [OpenCode models](https://opencode.ai/docs/models), [providers](https://opencode.ai/docs/providers), and [agents](https://opencode.ai/docs/agents)
- [OpenRouter Auto Router](https://openrouter.ai/docs/guides/routing/routers/auto-router)
