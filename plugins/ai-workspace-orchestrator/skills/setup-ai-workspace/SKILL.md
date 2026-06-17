---
name: setup-ai-workspace
description: Interactive AI workspace setup wizard for projects, monorepos, workspaces, and product domains. Use when the user wants to configure AGENTS.md/CLAUDE.md, choose low/medium/high/max setup depth, create global or project skills, or design agent/subagent orchestration.
---

# Setup AI Workspace

Goal: create the smallest useful AI operating layer for the current project or domain.

## Process

1. Inspect first:
   - Existing `AGENTS.md`, `CLAUDE.md`, `.codex/`, `.claude/`, `plugins/`, workspace manifests, app folders, package boundaries, and docs.
   - If the answer is in the codebase, use it instead of asking.
2. Ask one question at a time only when the decision cannot be inferred.
3. For every question, include a recommended answer and one-sentence reason.
4. Produce a setup profile before writing files.
5. If the user asked to apply the setup, write files surgically and verify them.

## Required Questions

Ask in this order unless already answered:

1. Depth: `low`, `medium`, `high`, or `max`.
2. Scope: current project, global user setup, or both.
3. Topology: single project, monorepo/workspace, multi-repo domain, or unknown.
4. Domains present: backend, frontend, mobile, data, infra, design, product, docs, security.
5. Skills: none, project-local, global, or both.
6. Agents: none, project-local, global, reuse `spotify-squad`, or hybrid.
7. Contract files: canonical `AGENTS.md`, `CLAUDE.md` symlink, pointer file, or preserve existing split.
8. Handoff: no handoff, temp handoff, or project handoff artifact.

## Depth Matrix

- `low`: root `AGENTS.md`/`CLAUDE.md`, setup profile, basic verification.
- `medium`: low plus project skills, routing rules, quality gates.
- `high`: medium plus orchestrator agent, domain subagents, skill map.
- `max`: high plus cross-repo/domain map, handoff loop, review loop, refinement cadence.

## Output Contract

Return:

1. `Setup Profile`: depth, scope, topology, domains.
2. `Artifacts`: files to create/update, with global vs project placement.
3. `Skill Plan`: skill names, triggers, scope, why each exists.
4. `Agent Plan`: orchestrator, subagents, delegation model.
5. `Contract Plan`: AGENTS/CLAUDE strategy and symlink/pointer decision.
6. `Verification`: exact checks to prove setup is complete.

## Rules

- Do not create speculative agents or skills.
- Prefer project-local skills for repo conventions and global skills for reusable workflows.
- For monorepos, create one root orchestrator that delegates to app/domain agents.
- For separate backend/frontend/mobile repos in one domain, create one domain orchestrator and link each repo contract back to it.
- Preserve existing instructions; append a delimited block instead of rewriting unrelated content.
- If a symlink is requested but unsupported or risky, create a short pointer file and explain the tradeoff.
