---
name: "teaching"
description: "Plan and review a learning journey: build a personalized learning roadmap with milestones and practice checkpoints, or run a retrospective over progress already made. Use when the user wants to learn a technology or concept over time and asks for a study plan, learning path, roadmap, curriculum, 'how do I learn X', 'where do I start with X', or wants to review what they have learned, identify blockers, and adjust the plan. For interactive hands-on coding instruction during a task, use learning-output-style instead. For a stateful workspace with missions and lesson artifacts, use teaching-workspace."
---
# teaching

Entry point for the `teaching` plugin. Two sub-skills, picked by where the user is in the loop.

## Sub-skills

| Sub-skill | Use when |
|---|---|
| **`create-learning-path`** (`skills/create-learning-path/SKILL.md`) | The user is starting out and needs a roadmap: milestones, ordering, practice checkpoints. |
| **`run-learning-retrospective`** (`skills/run-learning-retrospective/SKILL.md`) | The user has already been learning and needs to evaluate progress, surface blockers, and adjust the plan. |

Read the sub-skill file before acting — this page only routes.

## Related skills

- **`learning-output-style`** — hands-on: hands the keyboard back to the user at decision points while coding.
- **`teaching-workspace`** — stateful: missions, HTML lessons, and learning records persisted in a workspace.
- **`continual-learning`** — passive: mines transcripts to keep `AGENTS.md` current.
