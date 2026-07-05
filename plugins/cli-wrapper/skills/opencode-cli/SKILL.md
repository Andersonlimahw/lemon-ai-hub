---
name: opencode-cli
description: >
  Wrapped access to OpenCode CLI. Captures opencode --help, caches subcommands,
  validates flags, post-processes output. Use for ANY OpenCode CLI invocation
  from Claude Code or other harnesses. Saves ~85% tokens vs raw opencode output.
---

# OpenCode CLI Wrapper

Wrapped OpenCode CLI access. Digest-driven, token-optimized.

## Commands

```
/opencode-cli invoke <args>   — run opencode command with validated flags
/opencode-cli explain <cmd>   — show what an opencode subcommand does
/opencode-cli audit           — token savings report
/opencode-cli wrap            — rebuild digest from live opencode --help
```

## Token Savings

OpenCode CLI help output ~3KB+. Digest = ~300 bytes. 90% savings.

| Phase | Raw | Wrapped |
|-------|-----|---------|
| Discovery | 3.2KB | 0.3KB |
| Invocation | variable | filtered + deduped |
| Flag validation | trial/error | first-try via digest |

## Common Patterns

```
/opencode-cli invoke --version
/opencode-cli invoke config list
/opencode-cli invoke run <prompt>
```

## Digest Location

`.claude/cli-wrappers/opencode.json` — auto-refreshed on `/opencode-cli wrap`

## Cross-Harness

When Claude Code delegates to OpenCode, always use this wrapper.
The wrapper agent `opencode-cli` handles the full delegation lifecycle.
