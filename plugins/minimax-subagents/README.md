# minimax-subagents

MiniMax subagents and tiered workers on the **Token Plan subscription**, run
inline through OpenCode from any harness.

```bash
mm-run --tier quality --effort high -- "self-contained prompt"
```

| Piece | Path | What it does |
|-------|------|--------------|
| Skill | `SKILL.md` | Route table, per-harness calls, prompt contract, quota policy |
| CLI | `bin/mm-run` → `scripts/mm_run.py` | Tier/effort → lean worker or `-m`, strips thinking, retries transient errors once, exit 75 on quota, parallel cap |
| Agent | `agents/minimax-worker.md` | Claude Code / Agy relay that picks the tier and calls `mm-run` |
| Workers | `smart-sub-agents` lane `minimax` | `mm_fast_*`, `mm_m3_*`, `mm_flash_*` OpenCode agents + Claude/Agy bridges |
| Installer | `scripts/install.sh` | Links `mm-run`, skill symlinks, installs workers, runs `mm-run --check` |
| Reference | `references/models.md` | Models, endpoints, plan limits, measured token costs |

## Install

```bash
bash ~/Projects/IA/lemon-ai-hub/plugins/minimax-subagents/scripts/install.sh
claude plugin install minimax-subagents@lemon-ai-hub   # Claude Code skill + agent
```

Requires OpenCode with a `minimax` provider (see `SKILL.md`). Keys stay in the
OpenCode provider config or `MINIMAX_API_KEY`; nothing here reads them.

## Test

```bash
python3 -m unittest discover -s plugins/minimax-subagents/tests
```
