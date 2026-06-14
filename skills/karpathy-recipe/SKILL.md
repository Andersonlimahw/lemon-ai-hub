---
name: karpathy-recipe
description: Applies Karpathy's "A Recipe for Training Neural Networks" adapted to software engineering. Forces a minimum runnable baseline before optimizing, one knob at a time, with verifiable eval at the beginning. Use when implementing a new feature, doing a non-trivial refactor, integrating an external service, or when the user says "implement X from scratch", "how to start feature Y", "recipe", "incremental approach", "baseline first".
---

# karpathy-recipe

Translation of [Recipe for Training Neural Networks](https://karpathy.github.io/2019/04/25/recipe/) to product features. Principle: **be paranoid, go slow, visualize everything**.

## Mandatory Flow

### 1. Become one with the data
Before coding, read real data from the domain:
- For a financial feature: 10 real transactions from `extratos_exemplo/` or from `financial_transactions` in staging
- For AI: 5 examples of expected input/output from the user
- List known edge cases (memory, ADRs, past issues) — do not invent them

Output: 1 paragraph in the PR `## Data I looked at` with links/IDs.

### 2. Set up end-to-end skeleton + dumb baseline
Implement the **complete path** with trivial logic first:
- Server action returns a fixed mock
- Repository returns `[]`
- UI uses hardcoded data

Validate that the entire pipeline runs (request → action → repo → DB → UI) before any real logic. **Do not optimize anything yet.**

### 3. Overfit the simplest case
Next: make it work on **1 real input**, ignoring edge cases. Mock externals (Stripe, Belvo, OpenAI). Confirm expected logs/output.

### 4. Add one knob at a time
Add features in order (validation → real DB → external API → caching → optimization). After each knob:
- run `rtk npm test`
- run `rtk tsc --noEmit`
- atomic commit (semantic) — each commit must pass green

If something breaks: **revert the knob**, do not stack fixes.

### 5. Define eval up front
Before merging, write:
- 1 unit test (happy path)
- 1 integration test (with real fixtures when possible — see memory: "integration tests must hit a real database")
- `## Eval` criteria in the feature doc: "done when X is measurable"

### 6. Regularize / harden
**Only now** add: rate limit, error boundary, retry, Sentry observability, i18n keys, extra RLS. Not before.

## Forbidden Anti-patterns

- Starting optimization before the baseline is running
- Adding two knobs in the same commit
- "I will add a try/catch just in case" without a reproduced error
- Caching before having performance measurements
- Generic abstractions (factory, strategy) without 3 real callsites

## Expected Output when this skill is active

Codex responds with a mini-plan:
```
Recipe plan:
1. Data: <source of 5-10 real examples>
2. Skeleton: <files to create with mocks>
3. Overfit: <1 case to make work>
4. Ordered knobs: [...]
5. Eval: <test + measurable criteria>
```

And asks for confirmation before coding.

## Related
- [[surgical-reviewer]] — reviewer that validates these principles in a PR
- [[eval-harness-builder]] — agent that generates tests for step 5
- [[andrej-karpathy-skills:karpathy-guidelines]] — base behavioral guidelines
