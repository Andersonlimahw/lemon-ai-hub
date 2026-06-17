---
name: build-agent-orchestrator
description: Design and create a project, workspace, or domain agent orchestrator with optional Spotify Squad-style subagents. Use when the user wants agents, subagents, a squad orchestrator, cross-repo coordination, or backend/frontend/mobile domain delegation.
---

# Build Agent Orchestrator

Goal: create a minimal manager-worker agent topology that matches the real project shape.

## Process

1. Inspect topology:
   - Single app, monorepo/workspace, multi-repo domain, or mixed.
   - Present domains: backend, frontend, mobile, data, infra, QA, security, product, design.
   - Existing `plugins/spotify-squad`, `agents/`, `.claude/agents`, or project agent folders.
2. Recommend agent scope:
   - Project-local for repo-specific orchestration.
   - Global only for reusable specialist agents.
   - Hybrid when a global specialist needs project routing rules.
3. Choose topology:
   - Single project: one orchestrator, optional specialists.
   - Monorepo: one root orchestrator, one specialist per app/domain boundary.
   - Multi-repo domain: one domain orchestrator plus per-repo contracts pointing back to it.
4. Reuse `spotify-squad` when it fits. Create smaller local agents when the full squad would be overkill.
5. Write agent files only for real boundaries.
6. Update `AGENTS.md`/`CLAUDE.md` routing rules.
7. Verify frontmatter, names, and examples.

## Orchestrator Contract

The orchestrator must define:

- Domain map.
- Delegation rules.
- Parallel workstream policy.
- Inputs each subagent receives.
- Output format each subagent returns.
- Integration and verification gate.
- Escalation path when domains conflict.

## Recommended Agent Set

- Backend present: `backend-engineer`.
- Frontend present: `frontend-engineer`.
- Mobile present: `mobile-engineer`.
- Data present: `data-engineer`.
- Infrastructure present: `devops-engineer`.
- Security-sensitive domain: `security-engineer`.
- Product/design ambiguity: `product-manager`, `ux-researcher`, or `ui-designer`.
- Cross-domain work: `workspace-orchestrator`.

## Rules

- Ask one question at a time if topology cannot be inferred.
- Do not create all Spotify Squad agents by default.
- Prefer `model: inherit` unless the agent has a clear reason to override.
- Include 2-4 trigger examples in each agent description.
- Keep tools least-privilege when the target harness supports tool restrictions.
- Treat agents as autonomous workers; use skills for reusable knowledge.
