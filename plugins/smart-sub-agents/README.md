# Smart Sub-Agents

Portable provider/model/effort routing for Claude Code, Codex, OpenCode, Antigravity, Gemini CLI, and lemon-code.

The plugin keeps a curated, source-linked matrix in [`references/provider-matrix.json`](references/provider-matrix.json), resolves explicit routes, normalizes a small set of known aliases, and renders native or handoff artifacts without writing global configuration by default.

```bash
python3 scripts/validate_catalog.py
python3 scripts/render_agents.py --harness all --profile balanced --output-dir .smart-sub-agents/generated
python3 -m unittest discover -s tests -p 'test_*.py'
```

See [`SKILL.md`](SKILL.md) for the routing protocol and [`references/provider-matrix.md`](references/provider-matrix.md) for the provider/harness distinction and current recommendations.
