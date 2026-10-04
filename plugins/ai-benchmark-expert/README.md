# ai-benchmark-expert

Give the **same task** to many providers and models, score what each one
actually produced, and share the result as **one interactive HTML file**.

```bash
python3 scripts/bench.py run examples/quick-suite.json --dry-run   # command matrix, spends nothing
python3 scripts/bench.py run examples/quick-suite.json -o /tmp/bench/quick
open /tmp/bench/quick/report.html
```

| Piece | Path | What it does |
|-------|------|--------------|
| Skill | `SKILL.md` | Workflow, suite format, scoring, guardrails |
| Runner | `scripts/bench.py` | Runs targets × tasks × repeats in isolated git workdirs, parses usage from Claude/Codex/Gemini/OpenCode JSON, runs hidden checks, blind judge, aggregates, writes `results.json` + `report.html`; `--dry-run`, `--resume`, `--targets`, `--tasks`, `--repeat`, `--parallel` |
| Report | `scripts/report.py` + `assets/report-template.html` | Self-contained report: verdict, leaderboard with tiers and ±sd, quality-vs-cost/time/tokens Pareto, efficiency bars, rubric/task heatmap, sortable table, per-run evidence, methodology, light/dark, Markdown/link/JSON/PDF sharing |
| Agent | `agents/ai-benchmark-runner.md` | Delegates the full loop (preflight → run → leaderboard + caveats) |
| Example | `examples/quick-suite.json` | 3 tasks (greenfield code, fixture bug fix, arithmetic reasoning) × 5 targets (Claude Haiku, Claude Sonnet, Codex, Gemini, MiniMax M3) with hidden checks |
| References | `references/methodology.md`, `references/targets.md` | Rubric, scoring, statistics, sources; tested CLI command lines |
| Tests | `tests/test_bench.py` | Offline end-to-end with fake targets and judge: `python3 -m unittest discover -s tests` |

Requirements: Python 3.9+ (stdlib only), `git`, and the CLIs you benchmark,
already authenticated. The report needs no network.

Scoring follows public benchmarks (akitaonrails' LLM coding benchmark,
BenchLM, Open LLM Leaderboard, SWE-bench, Aider, Artificial Analysis, LMArena):
deterministic checks + blind 8-dimension rubric → 0–100 → tiers A/B/C/D, with
time, tokens and cost reported beside the score instead of folded into it.
