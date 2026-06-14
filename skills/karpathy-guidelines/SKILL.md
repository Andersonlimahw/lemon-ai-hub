---
name: karpathy-guidelines
description: >
  Injects Lemon AI Hub's standard AGENTS.md and CLAUDE.md guidelines into the current workspace.
  Enforces Andrej Karpathy's surgical coding style, simplicity, and goal-driven execution.
---

# Karpathy Guidelines

This skill injects the high-engineering standards of the Lemon AI Hub into your project. It ensures that any AI agent working on this codebase follows the **Andrej Karpathy surgical coding style**.

## Purpose

- **AGENTS.md**: Standardizes behavioral guidelines (Think before coding, Simplicity first, Surgical changes, Goal-driven execution).
- **CLAUDE.md**: Configures session setup rules and entry points for the active agent.

## Usage

Use this skill when you want to:
- Initialize a new project with professional AI-native guidelines.
- Update an existing project to match the Lemon.dev engineering philosophy.
- Fix "vibe coding" issues by enforcing structured reasoning and minimal changes.

## Commands

Run the injection script from your terminal:

```bash
# From the root of your project
bash ~/.claude/skills/karpathy-guidelines/scripts/inject.sh
```

> **Note:** The script will backup your existing `AGENTS.md` or `CLAUDE.md` if they don't already contain the Lemon AI Hub marker.

## Philosophy

Following Karpathy's recipe means:
1. **Understand first:** No implementation without explicit assumptions.
2. **Minimize noise:** Change only the lines that need changing.
3. **Verify always:** Every task must have a verifiable success criterion.
