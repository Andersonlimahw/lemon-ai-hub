# Jev / System One reference

Jev is TypeSafe's flagship System One model: state plus typed questions in; structured probabilistic judgments out. System One is intended for narrow machine-consumed decisions, not code generation or autonomous control flow.

Key semantics:

- `Choice`: selected declared option, full option distribution, derived confidence.
- `Score`: ordered-level expected score, distribution, legend, derived confidence.
- `Noul`: probability statement is true; no separate confidence field.
- Independent questions can share one state and run in one request. Compose answers in code.
- Typed/schema-correct output does not prove semantic correctness. Calibrate on representative data.

Provider-specific limits, aliases, pricing, and throughput change. Verify current model docs before implementation. Pin versions after calibration.

## Sources

- Full docs index/content: https://docs.typesafe.ai/llms-full.txt
- Introduction: https://docs.typesafe.ai/introduction
- System One: https://docs.typesafe.ai/concepts/system-one
- Building: https://docs.typesafe.ai/concepts/how-to-build-with-system-one
- State: https://docs.typesafe.ai/concepts/state
- Primitives: https://docs.typesafe.ai/primitives
- Confidence: https://docs.typesafe.ai/confidence
- Patterns: https://docs.typesafe.ai/patterns
- API: https://docs.typesafe.ai/api
- Models/limits/pricing: https://docs.typesafe.ai/models
- Claims and caveats: https://typesafe.ai/blog/introducing-system-one-models-and-jev
- Legal terms, including benchmark restrictions: https://typesafe.ai/legal/mca

TypeSafe names and claims belong to TypeSafe. This plugin extracts an architectural pattern and is not an official TypeSafe product.
