---
name: pstack
description: "Rigorous agent workflows and engineering principles by Lauren Tan (@poteto): fearless parallelism, poteto-mode with 23 playbooks, 24 engineering principles, multi-model panels, verification, and unslop quality gates."
---

# pstack — Rigorous Agent Workflows & Engineering Principles

Created by Lauren Tan ([@poteto](https://x.com/poteto)) from Meta, Netflix, and Cursor. Designed to eliminate AI slop, encourage deep engineering before code generation, and enable fearless agent parallelism.

## Core Entrypoints

- `poteto-mode`: Primary execution engine. Classifies requests into one of 23 rigorous engineering playbooks and drives execution step-by-step with structured verification.
- `poteto-help`: Interactive guide to pick the best skill, playbook, or principle for your current task.
- `setup-pstack`: Configures multi-model routing tiers, panel allocations, and reasoning budgets.

## 23 Engineering Playbooks (`poteto-mode`)

1. **investigation**: Read-only codebase interrogation ("how does X work", "why was Y built this way").
2. **bug-fix**: Reproduce defect, isolate root cause, and fix with executable runtime evidence.
3. **perf-issue**: Profile, measure, and optimize against an established baseline.
4. **hillclimb**: Scientific metric improvement looping hypotheses with before/after benchmarks.
5. **runtime-forensics**: Live defect diagnostics (memory leaks, CPU spin, UI glitch) via instrumentation.
6. **trace-forensics**: Profiling artifact analysis (cpuprofiles, traces, heap snapshots).
7. **feature**: Contract-first behavioral changes built from clear data shapes.
8. **refactoring**: Behavior-preserving structural cleanup with regression tests.
9. **prototype**: Cheap throwaway spikes to validate design choices before implementation.
10. **visual-parity**: Pixel-exact UI equivalence between implementations.
11. **authoring-a-skill**: Authoring or updating clean, discoverable agent skills.
12. **eval**: Blinded behavioral evaluation of skill or prompt iterations.
13. **babysit**: Drive PRs to merge-ready (CI fixes, merge conflicts, review threads).
14. **shipping**: Stack verification and clean landing via GitHub/origin.
15. **autonomous-run**: Long-running unattended task execution with checkpoints.
16. **orchestrate**: Standing multi-day coordinator decomposing tasks across fleets.
17. **autopilot-full**: Independent PRs driven to merged with parallel verifiers.
18. **autopilot-stack**: Stacking dependent PRs safely without auto-merge.
19. **session-pickup**: Clean resumption of in-flight work from prior agents.
20. **pause-safely**: Safe suspension of work with context preservation.
21. **multi-phase-plan**: Multi-phase architectural migrations across stacked PRs.
22. **worktree-cleanup**: Pruning merged or stale worktrees and simulator state.
23. **opening-a-pr**: Conventional commit titles and briefing-style PR bodies.

## 24 Engineering Principles

- `principle-attack-the-premise`: Re-examine foundational assumptions when multiple fixes fail.
- `principle-boundary-discipline`: Concentrate validation, sanitization, and error handling at boundaries.
- `principle-build-the-lever`: Build tools, scripts, and fixtures instead of manual bulk edits.
- `principle-encode-lessons-in-structure`: Turn lessons into types, linters, and architectural constraints.
- `principle-exhaust-the-design-space`: Enumerate and weigh architectural alternatives before choosing.
- `principle-experience-first`: Prioritize user experience over developer or implementation convenience.
- `principle-explain-the-number`: Validate metrics and understand variance before optimizing them.
- `principle-fix-root-causes`: Trace defects back to source; never patch superficial symptoms.
- `principle-foundational-thinking`: Establish core types and invariant models before logic.
- `principle-guard-the-context-window`: Protect context from bloat, huge diffs, and log dumps.
- `principle-laziness-protocol`: Resist speculative abstractions and premature generality.
- `principle-make-operations-idempotent`: Design operations to be safely repeatable across crashes.
- `principle-migrate-callers-then-delete-legacy-apis`: Migrate callers cleanly before removing legacy APIs.
- `principle-minimize-reader-load`: Keep code direct and readable; reduce layers of indirection.
- `principle-model-the-domain`: Represent domain entities with rich, precise data structures.
- `principle-never-block-on-the-human`: Proceed autonomously on reversible decisions.
- `principle-outcome-oriented-execution`: Focus on tangible verified outcomes, not busywork.
- `principle-prove-it-works`: Require objective executable proof before declaring completion.
- `principle-redesign-from-first-principles`: Step back and design cleanly when requirements shift.
- `principle-separate-before-serializing-shared-state`: Avoid concurrent state contention.
- `principle-sequence-verifiable-units`: Break work into minimal independently verifiable slices.
- `principle-subtract-before-you-add`: Delete dead code and excess complexity before adding new logic.
- `principle-test-behavior-not-implementation`: Assert observable contracts, never internal wiring.
- `principle-type-system-discipline`: Use strong static types to make invalid states unrepresentable.

## Verification & Architecture Tools

- `architect`: Design module boundaries, types, and signatures before writing code.
- `arena`: Spawn parallel candidate implementations and graft the strongest components.
- `blast-radius`: Calculate full downstream impact and dependency risks of a change.
- `figure-it-out`: Build custom execution playbooks when no standard playbook fits.
- `statechart`: Formal system modeling with TLA+ and statecharts.
- `unslop`: Strip AI tells, sycophancy, unnecessary comments, and filler.
- `interrogate`: Adversarial multi-model review to identify blind spots.
- `correct`: Find recurring agent errors in a codebase and eliminate them structurally.
- `no-comments`: Remove obvious, low-value AI comments with Comment Sicko.
- `benchmark-checklist`: Rigorous performance measurement validation checklist.
- `recall`: Reconstruct recent working context from chat history and state.
- `reflect`: Parallel review subagents to extract durable lessons.
- `show-me-your-work`: Auditable TSV decision logging for long tasks.
- `teach`: Plain-language technical explanations using Diátaxis and Feynman techniques.
- `typescript-best-practices`: Clean, type-safe TypeScript patterns.
- `technical-writing`: Clear, structured developer documentation.
- `create-verification-skill` & `maintain-verification-skill`: User-level behavioral verification loops.
- `create-formal-verification-skill` & `maintain-formal-verification-skill`: Formal verification for mission-critical logic.
