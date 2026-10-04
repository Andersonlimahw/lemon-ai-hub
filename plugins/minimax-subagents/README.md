# minimax-subagents

MiniMax subagents and tiered workers on the **M Plan / Token Plan
subscription**, run inline from any harness through MiniMax Code (`mcode exec`,
default backend) or OpenCode (fallback / `--backend opencode`).

```bash
mm-run --tier quality --effort high -- "self-contained prompt"
```

| Piece | Path | What it does |
|-------|------|--------------|
| Skill | `SKILL.md` | Route table, per-harness calls, prompt contract, quota policy |
| CLI | `bin/mm-run` → `scripts/mm_run.py` | Backend `mcode` (default) or `opencode`; tier/effort → model or lean worker, strips thinking, retries transient errors once, one OpenCode retry when mcode breaks, exit 75 on quota, parallel cap |
| Agent | `agents/minimax-worker.md` | Claude Code / Agy relay that picks the tier and calls `mm-run` |
| Workers | `smart-sub-agents` lane `minimax` | `mm_fast_*`, `mm_m3_*`, `mm_flash_*` OpenCode agents + Claude/Agy bridges |
| Installer | `scripts/install.sh` | Links `mm-run`, skill symlinks, installs workers, runs `mm-run --check` |
| Reference | `references/models.md` | Models, endpoints, plan limits, measured token costs |

## Install

```bash
bash ~/Projects/IA/lemon-ai-hub/plugins/minimax-subagents/scripts/install.sh
claude plugin install minimax-subagents@lemon-ai-hub   # Claude Code skill + agent
```

Default backend: MiniMax Code logged in (`~/.minimax-code/bin/mcode login`).
Fallback backend: OpenCode with a `minimax` provider (see `SKILL.md`). Auth
stays in mcode's OAuth store or the OpenCode provider; nothing here reads it.

## Test

```bash
python3 -m unittest discover -s plugins/minimax-subagents/tests
```
