---
name: agy-cli
description: >
  Wrapped access to Agy CLI (Antigravity). Captures agy --help, caches subcommands,
  validates flags, post-processes output. Use for ANY Agy CLI invocation from
  Claude Code or other harnesses. Saves ~85% tokens vs raw agy output.
---

# Agy CLI Wrapper (Antigravity)

Wrapped Agy (Antigravity) CLI access. Digest-driven, token-optimized.

## Commands

```
/agy-cli invoke <args>    — run agy command with validated flags
/agy-cli explain <cmd>    — show what an agy subcommand does
/agy-cli audit            — token savings report
/agy-cli wrap             — rebuild digest from live agy --help
```

## Token Savings

Agy CLI help output ~3KB+. Digest = ~300 bytes. 90% savings.

| Phase | Raw | Wrapped |
|-------|-----|---------|
| Discovery | 3.0KB | 0.3KB |
| Invocation | variable | filtered + deduped |
| Flag validation | trial/error | first-try via digest |

## Common Patterns

```
/agy-cli invoke --version
/agy-cli invoke config list
/agy-cli invoke agent run <name>
```

## Digest Location

`.claude/cli-wrappers/agy.json` — auto-refreshed on `/agy-cli wrap`

## Cross-Harness

When Claude Code delegates to Agy, always use this wrapper.
The wrapper agent `agy-cli` handles the full delegation lifecycle.
