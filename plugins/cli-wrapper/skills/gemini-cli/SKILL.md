---
name: gemini-cli
description: >
  Wrapped access to Gemini CLI. Captures gemini --help, caches subcommands,
  validates flags, post-processes output. Use for ANY Gemini CLI invocation
  from Claude Code or other harnesses. Saves ~85% tokens vs raw gemini output.
---

# Gemini CLI Wrapper

Wrapped Gemini CLI access. Digest-driven, token-optimized.

## Commands

```
/gemini-cli invoke <args>    — run gemini command with validated flags
/gemini-cli explain <cmd>    — show what a gemini subcommand does
/gemini-cli audit            — token savings report
/gemini-cli wrap             — rebuild digest from live gemini --help
```

## Token Savings

Gemini CLI help output ~4KB+. Digest = ~350 bytes. 91% savings.

| Phase | Raw | Wrapped |
|-------|-----|---------|
| Discovery | 4.1KB | 0.35KB |
| Invocation | variable | filtered + deduped |
| Flag validation | trial/error | first-try via digest |

## Common Patterns

```
/gemini-cli invoke --version
/gemini-cli invoke config list
/gemini-cli invoke extensions list
/gemini-cli invoke agent run <name>
```

## Digest Location

`.claude/cli-wrappers/gemini.json` — auto-refreshed on `/gemini-cli wrap`

## Cross-Harness

When Claude Code delegates to Gemini CLI, always use this wrapper.
The wrapper agent `gemini-cli` handles the full delegation lifecycle.
