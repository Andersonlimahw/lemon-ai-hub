---
name: opencode-subagent
description: >
  Cross-harness skill that teaches Claude Code, Codex (OpenAI), and Antigravity
  (Agy) how to use OpenCode as a subagent. Covers delegation triggers, task
  formatting, provider routing, result handling, and the complete protocol
  for efficient subagent orchestration.
---

# OpenCode — Cross-Harness Subagent Skill

Teach **Claude Code**, **Codex**, and **Antigravity (Agy)** to delegate work to
OpenCode efficiently. OpenCode is a standalone AI coding harness with its own
provider system, plugin architecture, and MCP/ACP support. Use it as a
specialist subagent for tasks your current harness handles poorly.

## Why OpenCode as Subagent

OpenCode excels where other harnesses fall short:

| Capability | OpenCode | Notes |
|------------|----------|-------|
| Any provider/model | Yes | Opus, Sonnet, Haiku, GLM, GPT, Claude, Gemini, Ollama |
| ACP (Agent Client Protocol) | Native | Run headless servers, attach remotely |
| Plugin system | Yes | Install any plugin from npm or local |
| Autonomous mode | `--auto` | Complete approval-free execution |
| Session management | `--continue`, `--fork`, `--session` | Resume/interrupt workflows |
| Remote attach | `opencode attach <url>` | Connect to headless opencode servers |
| MCP servers | Native | Full Model Context Protocol support |
| Mini mode | `--mini` | Lightweight TUI for constrained envs |
| Token tracking | `opencode stats` | Per-session cost analytics |
| Export/Import | `opencode export/import` | Share sessions across machines |

## When to Delegate

Use **opencode subagent** when:

1. **Provider flexibility**: Task needs a specific model (GLM, GPT, Opus) not available on your current harness
2. **Parallel execution**: Fan out multiple independent tasks to separate opencode instances
3. **Specialized plugins**: Task needs an opencode plugin not available in your ecosystem
4. **Remote execution**: Task must run on a remote machine or CI/CD via ACP
5. **Session isolation**: Task should not pollute your current session context
6. **Cost tracking**: Need per-task token/cost accounting via `opencode stats`

## How to Invoke

### From Claude Code

```bash
# Simple task
opencode run "refactor src/utils.ts to use async/await"

# Autonomous (no prompts)
opencode run "fix all TypeScript errors in src/" --auto

# With specific model
opencode run "audit bundle size" -m anthropic:claude-opus-4

# Continue previous session
opencode run "now optimize further" --continue

# Run headless server + attach
opencode serve --port 3001 &
opencode attach http://localhost:3001
```

### From Codex (OpenAI CLI)

```bash
# Basic delegation
opencode run "add unit tests for the auth module" --auto

# With session tracking
SESSION=$(opencode run "migrate database schema" --auto --print-logs 2>&1 | grep session.id | grep -oP 'ses_\w+')
echo "Task running in session: $SESSION"

# Export results
opencode export $SESSION > migration-results.json
```

### From Antigravity (Agy CLI)

```bash
# Drop-in delegation
agy exec -- opencode run "deploy to staging" --auto

# Or direct
opencode run "run performance benchmarks" -m openai:gpt-4o --auto
```

## Task Formatting Best Practices

### 1. Self-Contained Prompts

Include all context — OpenCode has no access to your current session:

```bash
# BAD — lacks context
opencode run "fix the bug in auth.ts" --auto

# GOOD — self-contained
opencode run "
  File: src/auth.ts (lines 42-67)
  Bug: JWT token refresh throws 'invalid signature' 
  when the token has < 5min expiry.
  Expected: Token should refresh silently.
  Fix the validateToken function to check expiry before signature.
" --auto
```

### 2. Use `--continue` for Multi-Step

```bash
opencode run "step 1: scaffold the component" --auto
STATUS=$?
if [ $STATUS -eq 0 ]; then
  opencode run "step 2: add styles and tests" --auto --continue
fi
```

### 3. Fan-Out Pattern (Parallel)

```bash
# Launch parallel tasks
opencode run "task A: API docs" --auto &
PID1=$!
opencode run "task B: client SDK" --auto &
PID2=$!
opencode run "task C: examples" --auto &
PID3=$!

# Wait for all
wait $PID1 $PID2 $PID3
echo "All parallel tasks complete"
```

### 4. Remote ACP Pattern

```bash
# On remote server
opencode serve --port 3001 --hostname 0.0.0.0 &

# On local machine
opencode attach http://remote-server:3001
```

### 5. Provider Routing via Models

Use OpenCode's multi-provider to route each task to the best model:

```bash
# Budget work → cheap model
opencode run "format all files" -m openai:gpt-4o-mini --auto

# Complex reasoning → quality model
opencode run "design auth architecture" -m anthropic:claude-opus-4 --auto

# Balanced → mid-tier
opencode run "implement CRUD endpoints" -m openai:gpt-4o --auto
```

## Result Handling

### Capture Output

```bash
# Capture to variable
RESULT=$(opencode run "analyze package.json dependencies" --auto --print-logs 2>&1)
echo "$RESULT" | grep -v "^timestamp="  # Strip logs, show AI output only

# Capture to file
opencode run "generate migration SQL" --auto > migration-output.txt
```

### Check Exit Code

```bash
opencode run "validate all schemas" --auto
if [ $? -eq 0 ]; then
  echo "Validation passed"
else
  echo "Validation failed — check session output"
fi
```

### Export Session for Review

```bash
# After task completes
opencode export <session-id> > task-report.json

# Parse results
cat task-report.json | jq '.messages[-1].content' 
```

## Agent Definitions for Each Harness

### Claude Code Agent

Place in `~/.claude/agents/opencode-subagent.md`:

```yaml
---
name: opencode-subagent
description: >
  Delegates work to OpenCode CLI. Use when a task needs a specific provider,
  plugin, or autonomous execution that Claude Code doesn't handle well.
  Triggers on "delegate to opencode", "opencode run", "open code subagent".
color: "#F97316"
mode: subagent
permission:
  bash: allow
  read: allow
---
```

### Codex Plugin

Place in `.codex-plugin/agents/opencode-subagent.json`:

```json
{
  "name": "opencode-subagent",
  "description": "Delegates work to OpenCode CLI from Codex. Use for autonomous task execution, multi-provider routing, or headless ACP operations.",
  "triggers": ["delegate to opencode", "opencode run"]
}
```

### Agy Agent

Place in `~/.agy/agents/opencode-subagent.yaml`:

```yaml
name: opencode-subagent
description: |
  Delegates work to OpenCode CLI from Antigravity.
  Use for parallel task execution, remote ACP, or provider-specific work.
```

## Protocol Summary

```
┌──────────────┐     opencode run "<task>"     ┌──────────────┐
│              │ ──────────────────────────────> │              │
│   Claude /   │                                 │   OpenCode   │
│   Codex /    │ <────────────────────────────── │              │
│    Agy       │   session output + exit code    │              │
└──────────────┘                                 └──────────────┘
     │                                                  │
     │ 3. Process Results                      2. Execute Task
     │    - Parse output                              │
     │    - Check exit code                    - Auto mode
     │    - Export if needed                  - Any provider
     │    - Log metrics                       - Isolated session
     │                                         - MCP/ACP if needed
```

## Testing the Setup

```bash
# Quick smoke test
opencode run "respond only with 'opencode subagent OK'" --auto

# Full delegation test
opencode run "
  Create a hello.txt file with content 'Hello from OpenCode subagent'
  Then read it back to confirm.
" --auto --print-logs 2>&1 | tail -5

# Provider routing test
opencode run "echo 'model test'" -m openai:gpt-4o-mini --auto

# Session persistence test
opencode run "create a note" --auto
opencode run "now read the note back" --auto --continue
```

## Requirements

- OpenCode CLI installed and in `$PATH`
- At least one provider configured (`opencode providers`)
- For remote ACP: network access to target server
