---
name: ai-benchmark-expert
description: Benchmark LLMs by giving the SAME task to multiple providers and models as headless CLI subagents (Claude Code, Codex, Gemini CLI, OpenCode/MiniMax, mm-run or any command), scoring each with hidden deterministic checks plus a blind LLM judge on a weighted 8-dimension rubric, and publishing one self-contained interactive HTML report (leaderboard + tiers, quality-vs-cost Pareto, efficiency, rubric heatmap, sortable table, per-run evidence, methodology). Use when the user asks to benchmark, compare, rank or evaluate models/providers/subagents on a task, "which model is best for X", "run the same prompt on several models", "LLM leaderboard", "eval report", or wants a shareable benchmark HTML.
---

# AI Benchmark Expert

Same task → many models → evidence → one shareable report.

`scripts/bench.py` runs every **target** (a provider/model behind a headless
CLI) on every **task** in its own isolated git workdir, executes hidden
**checks** there, optionally asks a **blind judge** to score the anonymised
output on a rubric, then writes `results.json` and a single-file
`report.html` (no CDN, no network — attach it to a PR, mail it, host it).

Methodology is modelled on public benchmarks — read
[`references/methodology.md`](references/methodology.md) before designing a
suite or interpreting close results.

## Workflow

1. **Frame the question.** What decision will the benchmark inform (pick a
   default coding model? a cheap subagent tier? a provider for long context)?
   That picks the tasks. A benchmark answers *this suite*, not "best model".
2. **Write the suite** (`suite.json`). Start from
   [`examples/quick-suite.json`](examples/quick-suite.json). Each task needs a
   precise prompt and at least one deterministic check; checks are what make
   the score honest. Put acceptance scripts **outside** the workdir (use
   `$BENCH_SUITE_DIR`) so models cannot read or edit them.
3. **Pick targets.** One entry per provider/model. Use
   [`references/targets.md`](references/targets.md) for tested command lines
   (permissions flags, JSON output parsers, env isolation).
4. **Dry run** — prints the exact command matrix, spends nothing:
   `python3 scripts/bench.py run suite.json --dry-run`
5. **Run.** `python3 scripts/bench.py run suite.json -o <out> --parallel 4`
   (add `--repeat 3` before trusting gaps under ~5 points; `--resume` after an
   interruption reuses finished runs).
6. **Read and share.** Open `<out>/report.html`. Use *Copy summary* (Markdown
   table) for PRs/Slack, *Copy link* for a filtered view, *Data* for
   `results.json`, *PDF* to print. Re-render after editing results:
   `python3 scripts/report.py <out>/results.json`.

`bench.py summary <out>/results.json` prints the leaderboard as Markdown.

## Suite format (essentials)

```json
{
  "name": "…", "description": "…", "repeat": 1, "parallel": 4, "timeout": 900,
  "weights": {"checks": 0.6, "judge": 0.4},
  "judge": {"label": "…", "model": "…", "cmd": "claude -p --model … --output-format json --tools ''", "parse": "claude-json"},
  "rubric": [ {"id": "correctness", "label": "Correctness", "weight": 25, "desc": "…"} ],
  "tasks": [
    {"id": "t1", "title": "…", "category": "coding", "prompt": "…", "fixture": "fixtures/t1",
     "timeout": 600, "judge": true,
     "checks": [{"name": "hidden tests", "cmd": "python3 \"$BENCH_SUITE_DIR/checks/t1.py\"", "timeout": 120}]}
  ],
  "targets": [
    {"id": "sonnet", "label": "Claude Sonnet 5", "provider": "anthropic", "harness": "claude code",
     "model": "claude-sonnet-5", "cmd": "claude -p --model {model} --output-format json --permission-mode bypassPermissions",
     "parse": "claude-json", "unset_env": ["ANTHROPIC_BASE_URL"], "env": {}, "price": {"input": 3, "output": 15},
     "version_cmd": "claude --version", "timeout": 900}
  ]
}
```

- **Placeholders in `cmd`:** `{prompt}` (shell-quoted text), `{prompt_file}`,
  `{workdir}`, `{model}`. With neither prompt placeholder the prompt goes to
  **stdin**. The command runs with `cwd` = the run's workdir.
- **`parse`:** `claude-json`, `codex-jsonl`, `gemini-json`, `opencode-json`
  or `text`. Parsers extract the final answer, tokens and reported cost;
  `<think>` blocks are stripped. `price` ($/Mtok) fills cost when the CLI
  reports tokens but not dollars.
- **Check env:** `BENCH_ANSWER` (file with the final answer — for Q&A tasks),
  `BENCH_WORKDIR`, `BENCH_SUITE_DIR`. Exit code 0 = pass.
- **`rubric`** defaults to the 8-dimension, 100-point rubric in
  `references/methodology.md`; `"judge": false` on a task skips judging (pure
  answer-checking tasks).

## Scoring (what the report shows)

Run score = `checks × pass-rate + judge × judge score` (weights normalised;
a missing part drops out; timeout = 0). Model score = mean of its runs;
with `repeat > 1`, ± is the sd of per-repeat means. Tiers: **A ≥ 80,
B ≥ 60, C ≥ 40, D < 40**. Cost and tokens are reported, never folded into the
quality score — the Pareto chart shows the trade-off instead.

## Subagents inside a harness

Every target already *is* a subagent: a headless CLI session with its own
context and tools. To benchmark Claude Code's own workers, point targets at
`claude -p --model …`, Codex at `codex exec`, MiniMax lanes at `mm-run --tier …
-- {prompt}` or `opencode run -m minimax/…`. The `ai-benchmark-runner` agent
wraps the whole loop (suite → dry run → run → summary) for delegation.

## Guardrails

- **Isolation:** each run gets a fresh `git init` workdir under `--out`
  (default: system temp dir, outside any repo). Agents run with permissive
  flags there — never point `--out` at a real project.
- **Fairness:** same prompt, same fixture, same timeout for everyone; record
  CLI versions (`version_cmd`); never hand-edit outputs. Report failures and
  timeouts as results, not noise.
- **Judge bias:** the judge never sees the model name, but LLM judges favour
  their own family. Prefer a judge from a provider not under test, or run a
  second judge and compare.
- **Secrets:** checks and judge read only the workdir; do not put keys in
  fixtures. Inspect `stderr.txt` before sharing artifacts.
- **Cost:** a full agentic run can cost dollars per target. Dry-run first,
  start with `--targets` / `--tasks` subsets.

## Files

| Path | Purpose |
|------|---------|
| `scripts/bench.py` | runner, parsers, judge, scoring (stdlib only) |
| `scripts/report.py` | `results.json` → self-contained `report.html` |
| `assets/report-template.html` | report UI (inline SVG charts, light/dark, a11y) |
| `examples/quick-suite.json` | 3-task suite across 5 providers, with hidden checks |
| `references/methodology.md` | rubric, scoring, statistics, sources |
| `references/targets.md` | tested CLI command lines per provider |
| `agents/ai-benchmark-runner.md` | delegate the full loop to a subagent |
| `tests/test_bench.py` | offline tests (`python3 -m unittest discover -s tests`) |
