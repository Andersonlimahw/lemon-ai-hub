---
name: "ai-workspace-orchestrator"
description: "ai-workspace-orchestrator plugin. Routes to its sub-skills: adversarial-setup-review, build-agent-orchestrator, context-handoff, setup-ai-workspace, workspace-contract, write-project-skill. Use when the task matches any of the capabilities listed below."
---
# ai-workspace-orchestrator

Entry point for the `ai-workspace-orchestrator` plugin. Pick the sub-skill that matches the task.

## Sub-skills

- **`adversarial-setup-review`** (`skills/adversarial-setup-review/SKILL.md`) — Principal-engineer adversarial review for AI workspace setup changes, agent/skill topology, AGENTS.md/CLAUDE.md contracts, and plugin marketplace registration. Use when reviewing a PR, diff, or setup plan for overengineering, missing verification, broken orchestration, stale instructions, or weak agent boundaries.
- **`build-agent-orchestrator`** (`skills/build-agent-orchestrator/SKILL.md`) — Design and create a project, workspace, or domain agent orchestrator with optional Spotify Squad-style subagents. Use when the user wants agents, subagents, a squad orchestrator, cross-repo coordination, or backend/frontend/mobile domain delegation.
- **`context-handoff`** (`skills/context-handoff/SKILL.md`) — Write compact handoff documents for AI workspace setup and agent orchestration work. Use when a session needs to transfer current decisions, suggested skills, open questions, and next actions to another agent or future session.
- **`setup-ai-workspace`** (`skills/setup-ai-workspace/SKILL.md`) — Interactive AI workspace setup wizard for projects, monorepos, workspaces, and product domains. Use when the user wants to configure AGENTS.md/CLAUDE.md, choose low/medium/high/max setup depth, create global or project skills, or design agent/subagent orchestration.
- **`workspace-contract`** (`skills/workspace-contract/SKILL.md`) — Create or update AGENTS.md and CLAUDE.md workspace contracts for AI coding agents. Use when the user wants project instructions, symlink strategy, orchestrator routing, skill maps, or monorepo/domain AI configuration files.
- **`write-project-skill`** (`skills/write-project-skill/SKILL.md`) — Create global or project-local agent skills with concise SKILL.md files, progressive disclosure, and optional deterministic scripts. Use when the user wants new skills for a project, workspace, domain, or global AI setup.
