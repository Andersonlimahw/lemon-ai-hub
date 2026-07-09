---
name: orchestrate
description: Fan a large task out across parallel AI agents. Planners scope and publish tasks, workers execute, and a script reconciles the tree from disk. Use when explicitly invoking /orchestrate with a large goal that benefits from parallel decomposition.
---

# Orchestrate

Fan out a large task across parallel agents. Workers don't talk to each other — they hand results up through structured handoffs.

## Core Principles

1. **Planners own scopes and publish tasks.** They do no coding. Writing plans, reading handoffs, and deciding what's next are planner work.
2. **Planners don't know who picks up their tasks.** The script routes each task to an agent.
3. **Workers are isolated.** One task, one clone of the repo, no channel to other agents. One handoff when done.
4. **Subplanners are recursive planners.** A planner publishes a "subplan this slice" task; the subplanner fully owns that slice.
5. **Continuous motion via handoffs.** No "finished" state until the planner decides to stop publishing.
6. **Propagation, not synchronization.** No cross-talk between siblings. No shared state between levels.

## Node Types

| Node | Runs Loop? | Scope | Output |
|------|-----------|-------|--------|
| Planner | yes | Entire user goal | User-facing message + optional PR |
| Subplanner | yes | One slice of parent scope | Handoff to parent |
| Worker | no | One concrete task | Handoff to spawning planner |
| Verifier | no | Acceptance criteria | Verdict handoff |

## Workflow

1. User invokes with a goal description.
2. Root planner decomposes goal into tasks.
3. Workers execute isolated tasks, return handoffs.
4. Planner reads handoffs, publishes next tasks or completes.
5. Subplanners handle complex slices recursively.
