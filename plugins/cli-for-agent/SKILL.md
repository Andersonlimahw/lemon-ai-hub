---
name: cli-for-agents
description: Design or review CLIs so coding agents can run them reliably: non-interactive flags, layered --help with examples, stdin/pipelines, fast actionable errors, idempotency, dry-run, and predictable structure. Use when building a CLI, adding commands, writing --help, or when the user mentions agent-friendly CLIs.
---

# CLI for Agents

Human-oriented CLIs often block agents: interactive prompts, huge upfront docs, and help text without copy-pasteable examples. Prefer patterns that work headlessly and compose in pipelines.

## Non-interactive First

Every input should be expressible as a flag. Do not require arrow keys, menus, or timed prompts. If flags are missing, fall back to interactive — not the other way.

**Bad:** `mycli deploy` → `? Which environment? (use arrow keys)`
**Good:** `mycli deploy --env staging`

## Discoverability Without Dumping Context

Agents discover subcommands incrementally: `mycli`, then `mycli deploy --help`. Do not print the entire manual on every run.

## `--help` That Works

Every subcommand has `--help`. Every `--help` includes **Examples** with real invocations.

```
Options:
  --env     Target environment (staging, production)
  --tag     Image tag (default: latest)
  --force   Skip confirmation

Examples:
  mycli deploy --env staging
  mycli deploy --env production --tag v1.2.3
```

## Stdin, Flags, and Pipelines

Accept stdin where it makes sense. Avoid odd positional ordering. Support chaining.

## Fail Fast With Actionable Errors

On missing required flags: exit immediately with a clear message and a correct example invocation.

```
Error: No image tag specified.
  mycli deploy --env staging --tag <image-tag>
```

## Idempotency

Agents retry often. The same successful command run twice should be safe (no-op or explicit "already done").

## Destructive Actions

Add `--dry-run` so agents can preview plans. Offer `--yes` / `--force` to skip confirmations.

## Predictable Structure

Use consistent patterns: `resource` + `verb`. If `mycli service list` exists, `mycli deploy list` should follow the same shape.

## Success Output

Return machine-useful data on success: IDs, URLs, durations.

```
deployed v1.2.3 to staging
url: https://staging.myapp.com
deploy_id: dep_abc123
```
