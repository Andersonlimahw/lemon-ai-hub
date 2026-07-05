---
name: claude-cli
description: >
  Wrapped access to Claude Code CLI. Captures claude --help, caches subcommands,
  validates flags against pre-built digest, post-processes output for minimal token
  consumption. Use for ANY Claude Code CLI invocation from this or other harnesses.
  Saves ~85% tokens vs raw claude help/output.
---

# Claude Code CLI Wrapper

Wrapped Claude Code CLI access. Digest-driven, token-optimized.

## Commands

```
/claude-cli invoke <args>    — run claude command with validated flags
/claude-cli explain <cmd>     — show what a claude subcommand does
/claude-cli audit             — token savings report
/claude-cli wrap              — rebuild digest from live claude --help
```

## Token Savings

Claude Code CLI has extensive help output (~5KB+). Digest = ~400 bytes. 92% savings.

| Phase | Raw | Wrapped |
|-------|-----|---------|
| Discovery | 5.2KB | 0.4KB |
| Invocation | variable | filtered + deduped |
| Flag validation | trial/error | first-try via digest |

## Common Patterns

```
/claude-cli invoke --version
/claude-cli invoke config list
/claude-cli invoke mcp list
/claude-cli invoke plugin list
```

## Digest Location

`.claude/cli-wrappers/claude.json` — auto-refreshed on `/claude-cli wrap`
