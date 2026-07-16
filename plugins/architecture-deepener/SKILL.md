---
name: architecture-deepener
description: Surface opportunities to deepen a codebase. Finds modules that are shallow (thin pass-throughs, anemic types, missing domain modeling) and proposes how to make them deep (rich domain types, co-located behavior, testable seams). Outputs a visual HTML report and then runs an interactive grilling loop that pressure-tests each opportunity. Use when the codebase feels "flat", domain logic leaks into controllers/UI, types carry no behavior, or AI agents struggle to navigate the module boundaries. Integrates with domain-modeling, codebase-design, and ADR workflows.
---

# Architecture Deepener

Turn shallow modules into deep ones. Make the codebase navigable for humans and AI agents alike.

Based on **improve-codebase-architecture** by Matt Pocock (https://github.com/mattpocock/skills).

## Core Idea: Shallow vs Deep Modules

A **shallow module** has a broad interface relative to the complexity it hides. It passes data through, delegates immediately, or carries no domain knowledge. It is a wiring artifact, not an abstraction.

A **deep module** has a narrow interface over a large implementation. It hides a hard decision behind a small surface, co-locates behavior with the data it owns, and gives callers something meaningful to say.

```
SHALLOW                          DEEP
┌──────────────────────┐         ┌──────────┐
│ interface (wide)     │         │ interface│
│  - validate()        │         │  - run() │
│  - transform()       │         └────┬─────┘
│  - persist()         │              │
│  - notify()          │              ▼
└──────────────────────┘         ┌──────────┐
  implementation (thin)          │ complex  │
  - return this.repo.save(x)     │ impl that│
                                 │ truly    │
                                 │ hides X  │
                                 └──────────┘
```

Deepening is not about adding code. It is about **moving** behavior to where the data lives, so the rest of the system can stay shallow.

## Quick Start

```
/architecture-deepener                        — analyze cwd, write report, start grilling
/architecture-deepener --dir src/domain       — scope to a directory
/architecture-deepener --report-only          — skip grilling, just emit HTML
/architecture-deepener --grill src/checkout   — skip exploration, grill a known module
```

## Three Phases

### Phase 1 — Explore (read-only)

Goal: build an evidence-backed map of shallowness across the target scope.

1. **Bound the scope.** Default: project root (respect `.gitignore`). Override with `--dir`.
2. **Enumerate modules.** A "module" is a file or cohesive directory that exports a unit (class, factory, service, component, route handler).
3. **For each module, collect signals:**
   - **Interface surface**: count exported members. Wide surface + thin body = shallow.
   - **Pass-through ratio**: how many functions just forward args to the next call (`return this.x.foo(...args)`).
   - **Anemic types**: types/interfaces that only declare shape and carry zero methods/functions.
   - **Domain logic in the wrong layer**: business rules living in controllers, UI components, or CLI handlers instead of domain modules.
   - **Primitive obsession at boundaries**: `string`, `number`, bare arrays used where a value object would carry meaning and invariants.
   - **AI-navigability**: can an agent jump to this module from a symptom ("where is the rule for X?") without reading 5 wiring files? Score 1-5.
4. **Classify** each module: `deep`, `balanced`, `shallow`, `anemic`, `leaky`.
5. **Rank** by deepening payoff = (impact of the hidden complexity) x (effort to move it). Prefer changes that unblock tests and AI navigation.
6. **Persist raw findings** to memory/context for the report phase. Do not emit prose yet.

Exit criteria: every module tagged, top 5-10 opportunities ranked with one-line rationale each.

### Phase 2 — HTML Report (artifact)

Goal: produce a single self-contained `architecture-deepener-report.html` that a human can scan in 60 seconds and an agent can cite.

Write the file with the native Write tool. The report MUST contain:

- **Header**: project name, scope, date, counts (modules scanned, shallow count, deep count).
- **Shallowness heatmap**: a table or grid where each row is a module, columns are the signals from Phase 1, cells are color-coded:
  - green = deep / healthy
  - yellow = balanced / watch
  - red = shallow / anemic / leaky
- **Top opportunities**: the ranked list with, for each:
  - module path
  - current shape (one sentence + the signal that proves it)
  - proposed deep shape (one sentence: what moves where)
  - payoff score + effort estimate (S/M/L)
  - testability delta: what becomes testable after the change that is not testable today
  - AI-navigability delta: what an agent can now locate directly
- **Before/After sketch**: an ASCII or `<svg>` diagram for the top 1-2 opportunities showing behavior moving from a controller/wiring layer into the domain module.
- **Integration notes**: explicit hooks into `domain-modeling`, `codebase-design`, and ADR workflows (see below).
- **Footer**: credit line — `Based on improve-codebase-architecture by Matt Pocock (https://github.com/mattpocock/skills)`.

Keep it dependency-free: inline `<style>`, no external scripts, no network calls. It must render by opening the file directly.

### Phase 3 — Grilling Loop (interactive)

Goal: pressure-test each top opportunity before anyone writes code. Do not trust the first proposal.

For each ranked opportunity, run this loop (max 3 rounds per item, then move on):

1. **State the proposal** in one sentence: "Move X behavior from A into B."
2. **Grill yourself** with these questions, in order. Answer each concretely with file paths and types, not vibes:
   - **What concrete bug or test-gap does this fix that exists today?** If you cannot name one, the change is speculative — demote it.
   - **Who are the callers, and what must they change?** Enumerate every import site. A "deepening" that ripples through 20 callers is usually wrong; a better intermediate step exists.
   - **What invariant does the deeper module enforce that nothing enforces today?** Name the rule. If there is no new invariant, you are moving code, not deepening it.
   - **Does this collapse or create a layer?** Deepening should remove a layer or a pass-through, not add scaffolding. If it adds a layer, justify why the indirection pays for itself.
   - **Can an AI agent now navigate to this module from a symptom without reading wiring files?** Give the symptom-to-module path. This is the AI-navigability test.
   - **What is the smallest version of this change that still delivers the invariant?** Cut scope until it hurts, then cut once more.
3. **Update the proposal** based on the answers. Common outcomes:
   - Proposal survives — promote to an actionable card.
   - Proposal shrinks — re-rank with the smaller scope.
   - Proposal dies — mark it `rejected: <reason>` in the report and move on. A kill is a successful outcome.
4. **Exit the loop** when the proposal is either promoted or killed. Never leave one lingering.

After all top items are processed, emit a final **action list**:
- `PROMOTE` items: module, invariant gained, smallest first step, estimated effort.
- `REJECTED` items: module, one-line reason.
- `DEFERRED` items: module, what needs to become true first (an ADR, a missing type, a test).

## Shallow vs Deep — Recognition Cheatsheet

| Signal | Shallow | Deep |
|--------|---------|------|
| Exports | Many, ad-hoc | Few, cohesive |
| Function bodies | `return this.x.foo(...)` | Encodes a domain rule |
| Types | Shape-only interfaces | Types with behavior / invariants |
| Where rules live | Controller / UI / CLI | Domain module |
| Tests | Need full stack to test | Unit-testable in isolation |
| AI navigation | "Where is the rule for X?" → 5 hops | Symptom → module in 1 hop |
| Change ripple | One rule change → N files | One rule change → 1 file |

## Integration

- **domain-modeling**: When an opportunity is "anemic type", hand to domain-modeling to design the rich type and its invariants before moving code.
- **codebase-design**: When an opportunity collapses or creates a layer, log it in the codebase-design record so the layering decision is explicit and reviewable.
- **ADRs**: Any `PROMOTE` item that changes a cross-cutting invariant or layering boundary gets a short ADR (Architecture Decision Record) capturing the before/after and the grilling answers. Do not let an invariant move silently.

## Guardrails

- **Read-only until Phase 3 ends.** Exploration and report never edit source.
- **No speculative generality.** If you cannot name the concrete bug, test-gap, or invariant gained, the change does not ship.
- **Smallest first step.** Every promoted item has a single smallest first step. Do not batch.
- **Kill is success.** A rejected opportunity that saves a team from a bad refactor is a win. Record it.
- **Effort honesty.** Do not label a 20-caller ripple as effort `S`. If the honest answer is `L`, say so and defer.

## Output Artifacts

| Artifact | Path | Phase |
|----------|------|-------|
| Raw findings map | in-memory / context store | 1 |
| Visual report | `architecture-deepener-report.html` (project root, or `--out <path>`) | 2 |
| Action list | appended to the report + echoed to chat | 3 |

## Credit

Based on **improve-codebase-architecture** by Matt Pocock (https://github.com/mattpocock/skills). The shallow/deep framing and the pressure-test-before-refactor discipline are adapted from that work.
