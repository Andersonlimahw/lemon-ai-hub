---
name: context-handoff
description: Write compact handoff documents for AI workspace setup and agent orchestration work. Use when a session needs to transfer current decisions, suggested skills, open questions, and next actions to another agent or future session.
---

# Context Handoff

Goal: let a fresh agent continue without rereading the whole conversation.

## Process

1. Save to the OS temp directory by default, not the current workspace.
2. If the user requests a project artifact, save under the documented project handoff path.
3. Reference existing PRDs, plans, diffs, commits, and docs by path or URL instead of duplicating them.
4. Redact secrets, tokens, passwords, private keys, and personal data.
5. Include suggested skills and agents for the next session.

## Handoff Format

```md
# Handoff: <topic>

## Current Goal
<one paragraph>

## Decisions
- <decision>

## Files And Evidence
- <path or URL>: <why it matters>

## Suggested Skills
- <skill>: <when to invoke>

## Suggested Agents
- <agent>: <workstream>

## Next Actions
1. <action>

## Open Questions
- <question, if any>
```

## Rules

- Keep it compact.
- Do not duplicate content already stored in authoritative artifacts.
- Prefer paths and URLs over pasted content.
- Include enough verification state for a fresh agent to trust what is done.
