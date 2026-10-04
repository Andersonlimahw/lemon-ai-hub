# Benchmark methodology

What makes a benchmark worth sharing, distilled from public leaderboards and
applied by `scripts/bench.py`.

## Lessons taken from the references

| Source | What it does well | How this plugin applies it |
|--------|-------------------|----------------------------|
| [akitaonrails — LLM coding benchmark](https://akitaonrails.com/en/2026/06/01/llm-benchmarks-grok-4-3-minimax-m3-opus-4-8/) · [repo](https://github.com/akitaonrails/llm-coding-benchmark) | One fixed prompt for every model, an agent builds a real project unattended, 8-dimension 0–100 rubric, A/B/C/D tiers, time and cost reported next to the score, failures (DNF, leaked secrets) count against the model | Identical prompt + fixture per target, isolated workdir, weighted 8-dim rubric, same tier cut-offs, time/tokens/cost per run, timeouts score 0 |
| [BenchLM](https://benchlm.ai/) | Overall = normalised weighted average of category averages; confidence shown apart from score; harder, less saturated evals weigh more | Rubric weights, per-task breakdown (heatmap), ± from repeats kept apart from the score; write discriminating tasks, drop saturated ones |
| [Open LLM Leaderboard — Big Benchmarks Collection](https://huggingface.co/collections/open-llm-leaderboard/the-big-benchmarks-collection) | Reproducible harness, fixed prompts/few-shot, published configs and raw outputs | `results.json` keeps every run's answer, checks and judge notes; CLI versions recorded; suite file is the config |
| [SWE-bench](https://www.swebench.com/) | Real repo + hidden tests decide pass/fail; the model never sees the tests | Fixtures + hidden checks via `$BENCH_SUITE_DIR`, executed after the run |
| [Aider polyglot leaderboard](https://aider.chat/docs/leaderboards/) | Pass rate with cost per run and edit-format compliance | Checks pass-rate column, cost per suite, instruction-following dimension |
| [Artificial Analysis](https://artificialanalysis.ai/) | Quality vs price vs speed plotted, not folded into one number | Quality-vs-cost/time/tokens scatter with Pareto frontier |
| [LMArena](https://lmarena.ai/) | Blind evaluation removes brand bias | Judge sees an anonymous submission, never the model name |

## Rubric (default, 100 points)

| Dimension | Weight | Question the judge answers |
|-----------|-------:|----------------------------|
| Correctness | 25 | Does it work and do what was asked, without bugs? |
| Completeness | 15 | All requested parts delivered, nothing stubbed? |
| Instruction following | 15 | Every explicit constraint respected (stack, format, scope, no extras)? |
| Code quality | 10 | Readable, idiomatic, well structured, no dead code? |
| Tests & verification | 10 | Meaningful tests or evidence of verification? |
| Robustness | 10 | Edge cases, validation, error handling? |
| Security & hygiene | 10 | No leaked secrets, unsafe calls, risky defaults? |
| Clarity | 5 | Clear final answer/docs, honest about limits? |

Each dimension is scored 0–10; judge score = Σ(score × weight) / Σweight × 10.
Override with a suite-level `rubric` when the domain differs (e.g. writing,
data extraction), keeping 6–10 dimensions with explicit descriptions.

## Scoring

- **Run score** = `w_checks × pass_rate×100 + w_judge × judge`, weights
  normalised over the parts present (default 0.6 / 0.4). No checks and no
  judge → 100 if the CLI exited 0, else 0. **Timeout → 0.**
- **Model score** = mean run score in scope (all tasks or one task).
- **Spread** = sd of per-repeat means when `repeat > 1`. Gaps inside the
  larger spread are ties; the report says so.
- **Tiers:** A ≥ 80 (ship as is) · B ≥ 60 (usable, needs patching) · C ≥ 40
  (major gaps) · D < 40 (unusable).
- **Efficiency is never folded into quality.** Time, tokens and cost are
  reported per model and plotted against score; the Pareto frontier marks
  models nobody beats on both axes.

## Designing tasks that discriminate

1. **Precise spec, hidden tests.** State every rule the checks will enforce;
   never test unstated behaviour. Ambiguous cases measure luck.
2. **Mix task types:** greenfield code, bug fix in a fixture, reasoning with a
   single verifiable answer (`ANSWER: <x>` + `grep` on `$BENCH_ANSWER`).
3. **Avoid saturation and contamination:** famous puzzles and katas are in
   training data. Change numbers, names and constraints.
4. **One check per behaviour family** (acceptance cases, the model's own tests,
   lint/format if it matters) so partial credit is visible.
5. **Agentic tasks** (create/edit files) need the target's write permissions
   enabled; Q&A tasks should say "do not create files".

## Statistics and fairness

- LLM output varies. Use `repeat ≥ 3` before publishing gaps under ~5 points.
- Same timeout, same fixture, same prompt for all; record CLI versions.
- Harness overhead (system prompt, tool schemas) counts in tokens and cost —
  that is what users pay — but note it when comparing raw model efficiency.
- Subscription plans (Claude Max, ChatGPT, MiniMax Token Plan) bill quota, not
  dollars; CLI-reported cost is list price.
- LLM judges prefer their own family and longer answers. Use a judge outside
  the providers under test when possible, keep the judge prompt strict, and
  rely on deterministic checks for the bulk of the score.
