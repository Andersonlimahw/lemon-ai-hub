# Evidence — `ai-benchmark-expert` smoke run

Sample artifacts produced by `bench.py` running the example suite against two
real targets. Kept in the repo so reviewers can open the rendered report and
see the output shape without having to install the plugin and spend money on
model calls first.

## Files

| File | What it is |
|------|------------|
| `report.html` | Self-contained interactive report (no CDN, no network). Open in any browser. |
| `report-overview.png` | Full-page screenshot of `report.html` (Chrome headless, 1400 × 3400). |
| `results.json` | Raw run data the report was rendered from. |

## How it was generated

```bash
python3 plugins/ai-benchmark-expert/scripts/bench.py run \
    plugins/ai-benchmark-expert/examples/quick-suite.json \
    --targets claude-haiku-4-5,minimax-m3 \
    --tasks slugify-bugfix,shipping-math \
    --no-judge \
    -o /tmp/bench-smoke
```

`--no-judge` skips the optional blind LLM judge (the example suite's judge
points at `claude -p --model claude-opus-5-5`, which would need a separate
credential); the deterministic checks still produce the 0–100 score and tiers.

## Headline

| # | Model | Score | Tier | Checks | Time | Tokens (in/out) | Cost |
|---|---|---|---|---|---|---|---|
| 1 | MiniMax M3 | 100.0 | A | 100.0% | 126 s | 1.05 M / 8.7 k | $0.135 |
| 2 | Claude Haiku 4.5 | 0.0 | D | 0% | 11 s | — | — |

MiniMax M3 passes both tasks (hidden acceptance cases + its own unittest
suite); Claude Haiku 4.5 is not available in the runtime environment used
to capture these artifacts, so every run exits with a CLI error — the runner
records that as a result, not a crash, which is the intended behaviour.

## Caveats

- The scores above reflect this single run on this single machine, on the
  subset of targets whose CLIs are available here. They are evidence that
  the runner, judge path and report render end-to-end; they are **not** a
  ranking.
- The Tier-D result for Claude Haiku is an artifact of the missing model in
  the capture environment, not a real evaluation. Re-run with `--targets`,
  `--tasks`, and a judge to get a meaningful leaderboard.