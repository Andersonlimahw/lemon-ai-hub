# <Project Name> AI Workspace

## Topology

- Depth: <low|medium|high|max>
- Scope: <project|global|both>
- Shape: <single-project|monorepo|multi-repo-domain>
- Domains: <backend, frontend, mobile, data, infra, docs, security>

## Skills

- `<skill-name>`: <scope and trigger>

## Agents

- `workspace-orchestrator`: owns cross-domain planning, delegation, and synthesis.
- `<domain-agent>`: owns <domain>.

## Routing

1. Use project evidence before asking setup questions.
2. Ask one unresolved decision at a time.
3. Delegate domain work to the matching specialist agent.
4. Verify each changed domain with its documented command.
5. Run `adversarial-setup-review` before merging durable instruction changes.

## Handoff

Write compact handoffs to the configured temp or project handoff path. Reference artifacts by path instead of duplicating them.
