# CLAUDE.md
<!-- Lemon AI Hub: Karpathy Standards -->
Single source of truth: `@AGENTS.md`

Read on start a new session:

1. `@AGENTS.md`
2. `@README.md`

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).

## 🔌 CLI Wrapper Ecosystem

This project IS the canonical source for the `cli-wrapper` plugin — the multi-harness CLI wrapper ecosystem. Claude Code = single source of truth. Other CLIs (Codex, Gemini, Agy, OpenCode) access via symlink.

**When developing in this repo**: prefer wrapped CLI access.
- `/cli-wrapper:cli-wrapper-setup` — one-shot ecosystem setup
- `/cli-wrapper wrap <cli>` — wrap a new CLI
- `/cli-wrapper list` — all wrapped CLIs + stats
- `/cli-wrapper audit all` — ecosystem-wide savings

**Plugin structure** (this project):
```
plugins/cli-wrapper/        ← CANONICAL SOURCE (git)
├── SKILL.md                ← main skill
├── plugin.json             ← v2.0.0
├── skills/                 ← sub-skills (cli-wrapper-setup, *-cli wrappers)
├── agents/                 ← wrapper agents (one per CLI)
└── templates/              ← symlink-map.json + config templates
```

**Global symlinks** (created by cli-wrapper-setup):
- `~/.claude/skills/cli-wrapper/` → this project's `plugins/cli-wrapper/`
- Other CLIs resolve via existing `skills → ~/.claude/skills` dir symlink
- Gemini: individual symlinks per sub-skill (no dir-level symlink)

- Use the  and  plugins for git workflows. Prefer  for semantic commits.
