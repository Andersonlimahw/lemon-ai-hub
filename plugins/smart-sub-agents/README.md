# Smart Sub-Agents

Portable provider/model/effort routing for Claude Code, Codex, OpenCode, Antigravity, Gemini CLI, and lemon-code, plus a versioned **worker matrix** that installs tiered named workers into every harness.

The plugin keeps a curated, source-linked matrix in [`references/provider-matrix.json`](references/provider-matrix.json), resolves explicit routes, normalizes a small set of known aliases, and renders native or handoff artifacts without writing global configuration by default. It pairs with [`smart-dispatch`](../smart-dispatch/SKILL.md), which announces a `DISPATCH` budget contract and picks the cheapest worker that still fits the task.

## Worker matrix (named agents)

A tier x effort grid of named subagents is generated from the matrix and installed into each harness. Claude bodies are canonical; other harnesses render/symlink.

| Harness | Pattern | Example | Location |
| --- | --- | --- | --- |
| Claude (canonical) | `{haiku\|sonnet\|opus}_worker_{effort}` | `sonnet_worker_high` | `~/.claude/agents/` |
| Codex | `{luna\|terra\|sol}_worker_{effort}` | `luna_worker_max` | `~/.codex/agents/` |
| OpenCode Zen (free) | `zen_{family}_worker_{effort}` | `zen_sol_worker_max` | `~/.config/opencode/agents/` |
| OpenCode Go (subscription) | `go_{family}_worker_{effort}` | `go_luna_worker_high` | `~/.config/opencode/agents/` |
| Agy | symlink -> Claude workers + Codex-named aliases | `opus_worker_high` -> `~/.claude/agents/...` | `~/.agy/agents/` |

Every generated file carries the marker `managed-by: smart-sub-agents/worker-matrix` and the installer is idempotent: re-running it never duplicates managed workers and never deletes non-managed agents.

## Setup (hub + a maintainer machine)

Run from the repo root so the scripts resolve the catalog via a relative path:

```bash
cd "$(git rev-parse --show-toplevel)"   # lemon-ai-hub root

# 1) Validate the catalog (providers, models, harnesses, workerMatrix, taskRouting)
python3 plugins/smart-sub-agents/scripts/validate_catalog.py

# 2) Unit tests
python3 -m unittest discover -s plugins/smart-sub-agents/tests -p 'test_*.py' -v

# 3) Sync live OpenCode Zen/Go models against `opencode models` (dry report)
python3 plugins/smart-sub-agents/scripts/sync_provider_matrix.py

# 4) Optional: persist discovered/stale flags + bump the `updated` date
python3 plugins/smart-sub-agents/scripts/sync_provider_matrix.py --write

# 5) Install workers into local harness dirs (~/.claude|codex|config/opencode|agy/agents)
python3 plugins/smart-sub-agents/scripts/install_worker_matrix.py

# 6) Validate the installed files (frontmatter + managed marker per harness)
python3 plugins/smart-sub-agents/scripts/install_worker_matrix.py --validate-only
```

Tip: render artifacts into the repo without touching global config first, then copy the ones you want:

```bash
python3 plugins/smart-sub-agents/scripts/render_agents.py --harness all --profile balanced --output-dir .smart-sub-agents/generated
python3 plugins/smart-sub-agents/scripts/render_agents.py --harness opencode --provider deepseek --model deepseek-v4-flash --effort max --output-dir .smart-sub-agents/generated
```

## Sync (monthly / weekly drift)

The matrix is a curated snapshot, not a live provider API. Models are added, deprecated, and gain new effort options over time. Keep it current with a three-command cadence:

```bash
# 1) Report drift: newly observed OpenCode models are marked `discovered`,
#    models no longer live are marked `stale`. Nothing is written yet.
python3 plugins/smart-sub-agents/scripts/sync_provider_matrix.py

# 2) Promote or remove entries in references/provider-matrix.json by hand,
#    then persist the catalog and re-run the validator so it stays green:
python3 plugins/smart-sub-agents/scripts/sync_provider_matrix.py --write

# 3) Reinstall workers so harnesses reflect the promoted matrix:
python3 plugins/smart-sub-agents/scripts/install_worker_matrix.py
```

`discovered` models stay status `discovered` until a human moves them into `workerMatrix` / profiles. The syncer never auto-deletes and never invents a model ID the live catalog did not return. Re-validate after every matrix change.

## Where to read more

- [`SKILL.md`](SKILL.md) - routing protocol (`ROUTE-MAP v1`) and the install/sync commands.
- [`references/provider-matrix.md`](references/provider-matrix.md) - recommended routes, alias corrections, and the harness-vs-provider distinction.
- [`references/provider-matrix.json`](references/provider-matrix.json) - the verified catalog: providers, models, harnesses, `workerMatrix`, `taskRouting`, `aliases`.
- [`plugins/smart-dispatch/SKILL.md`](../smart-dispatch/SKILL.md) - task -> tier -> worker routing table and the mandatory `DISPATCH` budget contract.