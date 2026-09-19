# Typed decision model background

Typed decision engineering separates probabilistic judgment from deterministic software behavior. Applications provide bounded state and named questions; a provider returns structured answers; runtime validation and code-owned policy decide whether to act, escalate, request review, or stop safely.

## Neutral primitives

- `choice`: select one declared option and, when available, preserve the full option distribution.
- `score`: evaluate ordered descriptive levels and preserve score/distribution metadata.
- `noul`: estimate whether one statement is true on `[0,1]`; values near `0.5` indicate uncertainty, not medium intensity.

These labels are internal contract terms. Adapters may map them to JSON Schema structured output, tool/function calling, a classifier, or another provider-specific interface.

## Architectural rules

1. Code owns deterministic rules, permissions, control flow, arithmetic, and side effects.
2. Each model question asks one narrow semantic judgment.
3. Independent questions may share minimal state and execute together; dependent questions wait for required evidence.
4. Static types do not validate network data. Validate structure and cross-field semantics at runtime.
5. Probability and confidence are routing inputs, not proof of truth or authorization.
6. Version models, schemas, thresholds, evaluation sets, tokenizers, and price snapshots.
7. Benchmark only comparable paired cases; preserve evidence labels and provider publication restrictions.

## Independence statement

This project is independently authored, provider-neutral open-source software. It is not sponsored, endorsed, certified, or affiliated with any model or platform vendor. Third-party products may be integrated only through adapters and remain subject to their own licenses, terms, and trademarks.
