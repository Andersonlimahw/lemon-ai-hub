---
name: "agentic-value-loops"
description: "agentic-value-loops plugin. Routes to its sub-skills: ai-tuning-loop, documentation-sync-loop, feature-development-loop, loop-invariants, maintenance-security-loop. Use when the task matches any of the capabilities listed below."
---
# agentic-value-loops

Entry point for the `agentic-value-loops` plugin. Pick the sub-skill that matches the task.

## Sub-skills

- **`ai-tuning-loop`** (`skills/ai-tuning-loop/SKILL.md`) — > AI Tuning Loop. Goal: raise chat answer quality for one agent + category per iteration.
- **`documentation-sync-loop`** (`skills/documentation-sync-loop/SKILL.md`) — > Documentation Sync Loop. Goal: keep docs truthful — no drift between code and the docs/guardrails that agents rely on.
- **`feature-development-loop`** (`skills/feature-development-loop/SKILL.md`) — > Feature Development Loop. Goal: ship one new user-facing feature per iteration, fully behind the quality gate.
- **`loop-invariants`** (`skills/loop-invariants/SKILL.md`) — > Universal rules and invariants that every Agentic Value Loop must follow.
- **`maintenance-security-loop`** (`skills/maintenance-security-loop/SKILL.md`) — > Maintenance & Security Loop. Goal: keep dependencies current and the app free of known vulnerabilities — one safe batch per iteration.
