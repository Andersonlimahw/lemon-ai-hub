---
name: codex-cli
description: >
  Wrapped access to Codex CLI (OpenAI). Captures codex --help, caches subcommands,
  validates flags, post-processes output. Use for ANY Codex CLI invocation from
  Claude Code or other harnesses. Saves ~85% tokens vs raw codex output.
---

# Codex CLI Wrapper

Wrapped Codex CLI access. Digest-driven, token-optimized.

## Commands

```
/codex-cli invoke <args>    — run codex command with validated flags
/codex-cli explain <cmd>    — show what a codex subcommand does
/codex-cli audit            — token savings report
/codex-cli wrap             — rebuild digest from live codex --help
```

## Token Savings

Codex CLI help output ~5KB+. Digest = ~400 bytes. 92% savings.

| Phase | Raw | Wrapped |
|-------|-----|---------|
| Discovery | 5.0KB | 0.4KB |
| Invocation | variable | filtered + deduped |
| Flag validation | trial/error | first-try via digest |

## Common Patterns

```
/codex-cli invoke --version
/codex-cli invoke config list
/codex-cli invoke agent run <name>
/codex-cli invoke plugin list
```

## Digest Location

`.claude/cli-wrappers/codex.json` — auto-refreshed on `/codex-cli wrap`

## Cross-Harness

When Claude Code delegates to Codex CLI, always use this wrapper.
The wrapper agent `codex-cli` handles the full delegation lifecycle.
