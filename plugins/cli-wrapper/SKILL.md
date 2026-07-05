---
name: cli-wrapper
description: >
  Wraps any external CLI so the AI harness can invoke it without context bloat.
  Captures --help output, documents every subcommand/flag in a compact digest,
  saves token metrics (raw vs wrapped), and exposes a standardized interface
  (invoke, explain, audit). Use before calling an unfamiliar CLI or when the
  harness needs to interact with a CLI repeatedly.
---

# CLI Wrapper — Multi-Harness Ecosystem

Bridge between AI harness and external CLIs. Captures, documents, optimizes.
**Claude Code = single source of truth. Other CLIs = symlinks.**

## Ecosystem

```
claude (canonical) ← symlinks → codex, agy, opencode, gemini
```

All wrapper skills/agents live in Claude's space. Other harnesses access via symlink.
Setup one command: `/cli-wrapper:cli-wrapper-setup`

## Why

Raw CLI help output floods context. A single `docker --help` = ~3KB. Wrapped digest = ~300 bytes. 10x savings per invocation. Multiply by every CLI the harness calls.

## Quick Start

```
/cli-wrapper:cli-wrapper-setup              — one-shot ecosystem setup (symlinks, configs, verify)
/cli-wrapper:cli-wrapper-setup --verify     — audit existing setup
/cli-wrapper wrap <cli-name>                — capture CLI help + build digest
/cli-wrapper invoke <cli-name> <args>       — run command, return compact output
/cli-wrapper audit <cli-name>               — show token savings for this CLI
/cli-wrapper audit all                      — ecosystem-wide savings report
/cli-wrapper list                           — list all wrapped CLIs
/cli-wrapper unwrap <cli-name>              — remove wrapper, restore raw access
```

### CLI-Specific Wrappers

Each major AI CLI has its own dedicated wrapper skill + agent:

```
/claude-cli invoke|explain|audit|wrap      — Claude Code CLI
/gemini-cli invoke|explain|audit|wrap      — Gemini CLI
/codex-cli invoke|explain|audit|wrap       — Codex CLI (OpenAI)
/opencode-cli invoke|explain|audit|wrap    — OpenCode CLI
/agy-cli invoke|explain|audit|wrap         — Agy CLI (Antigravity)
```

These auto-delegate to the respective wrapper agent for complex operations.

## Workflow

### 1. Wrap a CLI (discovery)

Claude will:
1. Run `<cli> --help` (and `<cli> <subcommand> --help` recursively)
2. Parse flag types, defaults, required vs optional
3. Build a compact digest — only what the harness needs to know
4. Save digest to `.claude/cli-wrappers/<cli-name>.json`
5. Report token savings: raw vs wrapped

### 2. Invoke via wrapper

Instead of raw CLI calls, the harness uses the wrapper interface:

```
/cli-wrapper invoke docker ps --filter status=running
```

The wrapper:
1. Validates flags against the digest (catches typos early)
2. Runs the command
3. Post-processes output (dedup, truncate, format)
4. Returns only essential output to context
5. Logs token metrics

### 3. Audit savings

```
/cli-wrapper audit docker
```

Returns:
```
CLI WRAPPER AUDIT — docker
===========================
Wrapped:    2026-06-15
Commands:   27 subcommands indexed
Help size:  3.2KB raw → 0.3KB digest (90% savings)
Invocations: 12
Tokens saved: ~18,400
Avg savings:  ~1,533 tokens/call
```

## Digest Format

Each wrapped CLI produces a machine-readable digest:

```json
{
  "name": "docker",
  "version": "27.3.1",
  "wrapped_at": "2026-06-15T10:30:00Z",
  "subcommands": {
    "ps": {
      "description": "List containers",
      "flags": {
        "--all": { "type": "bool", "description": "Show all containers" },
        "--filter": { "type": "string", "description": "Filter output", "repeatable": true },
        "--format": { "type": "string", "description": "Go template" },
        "--quiet": { "type": "bool", "description": "Only IDs" }
      }
    },
    "build": {
      "description": "Build image from Dockerfile",
      "flags": {
        "--tag": { "type": "string", "description": "Name:tag", "repeatable": true },
        "--file": { "type": "string", "description": "Dockerfile path" },
        "--build-arg": { "type": "string", "description": "Build-time var", "repeatable": true },
        "--no-cache": { "type": "bool", "description": "Don't use cache" },
        "--platform": { "type": "string", "description": "Target platform" }
      }
    }
  },
  "global_flags": {
    "--config": { "type": "string", "description": "Config file location" },
    "--context": { "type": "string", "description": "Docker context" },
    "--debug": { "type": "bool", "description": "Debug mode" },
    "--host": { "type": "string", "description": "Daemon socket" },
    "--log-level": { "type": "string", "description": "Log level", "choices": ["debug", "info", "warn", "error"] }
  },
  "stats": {
    "help_raw_bytes": 3247,
    "digest_bytes": 312,
    "savings_pct": 90.4
  }
}
```

## Token Savings — How It Works

| Phase | Without Wrapper | With Wrapper |
|-------|----------------|-------------|
| Discovery | Run `cmd --help` each session → 3KB tokens | Load digest → 0.3KB tokens |
| Validation | Harness guesses flags → retries | Digest validates → first try |
| Output | Raw output → possibly 10KB+ | Post-processed → essential only |
| Documentation | Harness re-discovers each time | Digest persists across sessions |

## Supported CLI Patterns

Works with any CLI that supports `--help`:
- **Posix-style**: `command --help`, `command subcommand --help`
- **Subcommand trees**: `git`, `docker`, `kubectl`, `aws`, `gcloud`
- **Single-binary tools**: `ffmpeg`, `curl`, `jq`, `gh`
- **Node/npm tools**: `npx`, `pnpm`, `bun`

## Post-Processing Rules

To minimize context bloat, the wrapper applies:
1. **Dedup**: remove repeated lines (stack traces, warnings)
2. **Truncate**: cap output at 500 lines by default (`--max-lines` overrides)
3. **Filter**: strip ANSI escape codes, progress bars, spinners
4. **Summarize**: for known CLIs, extract structured summary (e.g., `docker ps` → table of container names + status only)

## Files

- `.claude/cli-wrappers/<name>.json` — digest (machine-readable)
- `.claude/cli-wrappers/<name>.md` — human-readable reference (optional)

## Example Session

```
User: /cli-wrapper wrap gh
Claude:
  Running gh --help … 2.1KB
  Running gh issue --help … 1.8KB
  Running gh pr --help … 2.4KB
  Running gh repo --help … 1.6KB

  ✓ gh wrapped — 4 subcommands, 47 flags indexed
  Digest: 0.4KB (94% savings vs 7.9KB raw)
  Saved to .claude/cli-wrappers/gh.json

User: /cli-wrapper invoke gh issue list --state open --limit 5
Claude: [validates flags ✓] [runs command] [output: 5 issues, compact table]
  Tokens used: 142 (vs ~800 raw — 82% savings)
```
