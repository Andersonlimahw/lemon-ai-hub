---
name: "smart-handoff"
description: "Save a resumable handoff when a session's context/usage budget is nearly exhausted, so any AI runtime (Claude Code, Codex, Antigravity/Agy, OpenCode, Gemini CLI) can pick the work up with zero lost context. Use proactively when approaching ~90-95% context or usage limits."
---

# Smart Handoff

Runtime-agnostic protocol for pausing and resuming long-running AI coding sessions.

## Configuration

Add this plugin to your `plugin.json` or `.claude-plugin/marketplace.json`.

## Core Agents

- **handoff-writer**: Pauses and saves in-flight work safely.
- **handoff-resumer**: Verifies and resumes from a saved handoff.
