---
name: gh-copilot
description: Manage GitHub Copilot tasks via gh CLI.
---

# GitHub Copilot Skill

Use GitHub Copilot from the command line for AI-assisted tasks.

## Capabilities
- Explain command: `gh copilot explain "<natural language question>"`
- Suggest command: `gh copilot suggest "<task description>"`
- Evaluate command: Pipe or pass command suggestions through copilot for verification
- Agent mode: `gh copilot --agent` or `gh copilot` interactive mode
- Ask about gh: `gh copilot explain "how do I list all open issues"`

## Usage
Triggered when user says "copilot", "gh copilot", "explain command", "suggest command", "how do I use gh".
Use `explain` to understand what a command does before running it.
Use `suggest` when unsure what gh command to use for a task.
