# Decision-native routing

Use this reference when a probability scorer will choose worker tier, effort, or delegation shape. This is a model-agnostic architecture pattern, not a dependency on any named service or repository. The static provider matrix remains the executor catalog and fail-open path.

## Core pattern

```text
shared task state + runtime criteria + declared options
        -> typed option scores
        -> calibrated policy clamps
        -> executor worker
        -> validation outcome
        -> calibration data
```

Prefer decision-native scoring over asking a chat model to generate prose or JSON that software immediately parses into a branch. Constrain every decision to declared semantic options. A scorer must never invent a provider, model, effort, or action outside the supplied catalog.

For multiple decisions over the same task state, compute or cache the shared prefix once and evaluate independent criteria as suffixes. Batch independent criteria when execution supports it. Do not repeat the entire transcript for every routing question.

## Prompt and skill-router application

The same shape applies before execution, not only to worker selection:

```text
request + confirmed context + available catalog
        -> intent / ambiguity / risk / candidate / budget questions
        -> policy clamps and confidence gate
        -> prompt, skill selection, or worker route
        -> validation outcome
```

For prompt refinement, the action is a definitive prompt plus `EXEC-MAP v1`.
For skill selection, the action is the bounded `SKILLS` block. Neither stage should
ask a text model to invent a route and then parse its prose as authority. Keep the
static catalog as the fail-open path; use numeric confidence only when a scorer has
been calibrated on the same task family and phase.

## Typed score contract

Score these independent questions together:

- `tier`: `budget | balanced | quality`
- `effort`: an effort supported by the selected executor
- `risk`: `routine | consequential | safety-critical`
- `tool_complexity`: `none | bounded | agentic`
- `delegation`: `inline | one-worker | parallel-workers`
- `route_fit`: probability that the route meets the task's quality target

Keep state dense and bounded: objective, phase, affected surface, available routes, validation command, recent failures, and context size. Do not send secrets, raw environment values, full logs, or an unbounded transcript.

Every stage preserves this decision envelope without renaming or dropping fields:

```text
router: heuristic|typed-scorer
router_mode: heuristic|shadow|advisory|enforce
router_confidence: 0.00-1.00|unavailable
router_fallback: ask|static-catalog|balanced|none
```

Provider outage routing is a separate `provider_fallback`; it must never overwrite the reason a decision router failed open.

## Policy order

1. Bypass learned scoring for deterministic local work and tiny obvious tasks.
2. Accept scores only when their schema is valid, the route exists, latency stays within budget, and confidence clears a locally calibrated threshold.
3. Apply an explicit user route when present; it overrides the scorer's preference.
4. Without an explicit route, fail open to `balanced` on uncertainty or scorer failure.
5. Apply safety floors as the final monotonic lower bound; they may raise, but never lower, the effective route.
6. Escalate to `quality` only when an explicit route, risk floor, or failed validation warrants it.
7. Verify the executor result. Typed output prevents invalid options, not semantically wrong decisions.

## Rollout and calibration

Use `shadow -> advisory -> enforce`:

- `shadow`: record the proposed route while serving the static route.
- `advisory`: expose the recommendation; the orchestrator decides.
- `enforce`: apply it subject to policy clamps and fail-open behavior.

Evaluate per task family and phase. Track validation pass rate, regret against a stronger route, tokens or credits, end-to-end latency including scoring, fallback rate, and calibration error. Recalibrate when models, prompts, workloads, or task distributions change.

The matrix's `0.70` gate is a placeholder, not a universal optimum. Raw softmax over allowed options is conditional on those options and is not automatically calibrated operational confidence.

## Research basis

- OpenJEV demonstrates runtime-defined typed options, generation-free logit readout, shared-prefix reuse, parallel suffix evaluation, pinned revisions, prompt hashes, and row-level auditing: <https://github.com/TheoLeeCJ/openjev>
- Its method explicitly separates valid typed output from semantic correctness and warns that option-token softmax is not calibrated confidence: <https://github.com/TheoLeeCJ/openjev/blob/master/docs/METHOD.md>
- FrugalGPT establishes learned cascades for cost/quality trade-offs: <https://arxiv.org/abs/2305.05176>
- RouteLLM learns strong-vs-weak routing from preference data: <https://arxiv.org/abs/2406.18665>
- UCCI argues for calibration before thresholding and documents distribution-shift limits: <https://arxiv.org/abs/2605.18796>

OpenJEV is research evidence for the pattern, not a runtime dependency. Its reported speedups are hardware- and implementation-specific, and its faster shared-state paths recorded small argmax changes versus fresh scoring. Reproduce locally before relying on equivalent performance or stability.

- TypeSafe's launch article describes the broader System One pattern: structured
  decisions, probabilities, parallel independent questions, and workflow-level
  evaluation rather than unconstrained text generation: <https://typesafe.ai/blog/introducing-system-one-models-and-jev>
- The TypeSafe state and quickstart docs make the state/questions/typed-answer
  boundary concrete: <https://docs.typesafe.ai/concepts/state> and <https://docs.typesafe.ai/introduction/quickstart>
- LangChain's harness examples apply the pattern to model routing and tool-risk
  gating while keeping the LLM responsible for open-ended work: <https://www.langchain.com/blog/building-a-harness-with-jev>
- The practical use-case catalog emphasizes the same input → question → answer →
  action shape and confidence-gated automation: <https://uditgoenka.medium.com/how-to-use-typesafe-ai-jev-e9f1306300be>
