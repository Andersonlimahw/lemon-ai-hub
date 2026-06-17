---
name: workspace-contract
description: Create or update AGENTS.md and CLAUDE.md workspace contracts for AI coding agents. Use when the user wants project instructions, symlink strategy, orchestrator routing, skill maps, or monorepo/domain AI configuration files.
---

# Workspace Contract

Goal: make the project readable to future agents in one load.

## Process

1. Read existing `AGENTS.md` and `CLAUDE.md` if present.
2. Decide canonical file:
   - Prefer `AGENTS.md` as canonical for multi-agent portability.
   - Use `CLAUDE.md` as a symlink to `AGENTS.md` when supported and requested.
   - Use a short pointer file when symlink support is unknown or unsafe.
3. Append or update a delimited AI workspace block. Preserve unrelated instructions.
4. Include only operational facts future agents need.
5. Verify links, symlink target, and absence of duplicated long blocks.

## Required Sections

- Project identity and topology.
- Domains and owning folders.
- Setup depth and scope.
- Skills map: name, scope, trigger, location.
- Agent map: orchestrator, subagents, delegation rules.
- Verification commands.
- Marketplace/plugin sync rules when the repo has `plugins/`.
- Handoff path and continuation protocol.

## Symlink Policy

Use this decision order:

1. If both files already contain meaningful content, preserve both and add cross-links.
2. If `AGENTS.md` is canonical and `CLAUDE.md` is absent, create `CLAUDE.md -> AGENTS.md` when the filesystem and user allow symlinks.
3. If symlink is unsafe, create a short `CLAUDE.md` pointer that references `AGENTS.md`.
4. Never replace user-authored instructions without preserving them.

## Minimal Block

```md
## AI Workspace

Depth: medium
Topology: monorepo
Canonical instructions: AGENTS.md

Skills:
- setup-ai-workspace: project setup and routing

Agents:
- workspace-orchestrator: cross-domain planning and delegation

Verification:
- Run repo tests or documented quality gates after edits.
```

## Rules

- No marketing prose.
- No duplicated long policy blocks.
- No stale file paths.
- If this repo's `plugins/` changes, update `.claude-plugin/marketplace.json` in the same change.
