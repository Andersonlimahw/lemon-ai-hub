---
name: loop-invariants
description: >
  Universal rules and invariants that every Agentic Value Loop must follow.
---

# Loop Invariants

A loop is only "good" if every iteration satisfies **all** of these invariants.

1. **Single increment of real value**: Avoid scope creep; ship something a user notices. (Phase 0 value hypothesis).
2. **Spec before code (SDD)**: No code without a `PLAN.md`. (Phase 1).
3. **Eval defined up front**: Define success before building.
4. **Surgical diff**: Touch only what the request needs.
5. **100% codebase-rule adherence**: Follow Repository Pattern, clean architecture, specific guardrails.
6. **Quality gate green**: `npm run version:validate` MUST exit 0. No exceptions.
7. **PR open + CI green**: Nothing is "done" until CI says so.
8. **Learning captured**: Never repeat a fixed error. Update `ITERATION_LOG.md`.
9. **Automate the second time**: Extract reusable assets so the loop compounds, never repeats toil (Create Skills, Subagents, Scripts).
