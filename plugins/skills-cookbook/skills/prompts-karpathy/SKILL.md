---
name: prompts-karpathy
description: Ready-to-paste prompts for the Karpathy method — behavioral guidelines while coding, the full recipe for medium/large work, review against the four principles, and the autonomous optimization loop.
---

# Prompts — Karpathy method

The trio `karpathy-guidelines` (behavioral principles), `karpathy-recipe` (recipe for medium/large work), and `karpathy-loop` (autonomous optimization cycles). Complementary, not redundant: guidelines apply always; recipe structures large work; loop chases a metric.

## R1 — Guidelines on any implementation

**Skills:** `karpathy-guidelines`
**When:** any non-trivial code — the default to cut classic LLM mistakes.

```text
Implement <feature/fix> in <path> applying karpathy-guidelines:
state assumptions before coding (ask if one is structural), the
minimum code that solves it, surgical changes (no "improving"
neighboring code), and a numbered plan with "→ verify:" per step.
Success: every line of the diff traces to the request; every
verify ran with evidence.
```

## R2 — Full recipe for medium/large work

**Skills:** `karpathy-recipe` + `verification-before-completion`
**When:** a feature/refactor that spans several files or sessions.

```text
Structure <work> with karpathy-recipe: break it into stages with a
verifiable criterion each, execute stage by stage, and close each
one with verification-before-completion before moving on.
Success: plan with stages + verification; no stage marked complete
without the check having run; final diff with no extra scope.
```

## R3 — Review against the four principles

**Skills:** `karpathy-guidelines` + `code-review-expert`
**When:** reviewing a diff/PR looking for the vices the guidelines prevent.

```text
Review the diff of <branch/PR> with code-review-expert using
karpathy-guidelines as the rubric: (1) hidden assumptions,
(2) speculative complexity/premature abstraction, (3) non-surgical
changes outside scope, (4) weak or unverified success criteria.
Success: every finding mapped to a principle, with file:line and a
1-sentence fix.
```

## R4 — Autonomous metric loop

**Skills:** `karpathy-loop`
**When:** an objective metric to optimize in cycles. Full recipe in track [prompts-feedback-loops](../prompts-feedback-loops/SKILL.md) (R4) — one loop driver at a time.

## See also

- `verification-before-completion` — universal "is this actually done?" gate.
- `continual-learning` — persist lessons from the cycles across sessions.
