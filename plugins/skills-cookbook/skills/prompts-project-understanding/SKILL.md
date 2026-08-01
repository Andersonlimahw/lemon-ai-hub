---
name: prompts-project-understanding
description: Ready-to-paste prompts to understand a codebase fast and cut cognitive load — architecture deep-dives, auto-generated wikis, guided learning paths, and spec grilling before implementation.
---

# Prompts — Understanding projects (less cognitive load)

Recipes to explain a project to you (or an agent) without drowning the context. Goal: reduce cognitive load and cognitive debt — you understand the system in layers, with navigable artifacts, instead of reading raw code.

## R1 — Architecture X-ray

**Skills:** `architecture-deepener`
**When:** the codebase feels "flat", domain logic leaked into controllers/UI, or you inherited a project.

```text
Run architecture-deepener on <path>.
I want: (1) the map of shallow vs. deep modules, (2) where domain
logic leaked into controllers/UI, (3) the top 3 highest-impact
opportunities to deepen the design, prioritized.
Success: report with opportunities I can validate by pointing to
file:line, ready to become backlog items.
```

## R2 — Living project wiki

**Skills:** `llm-wiki-curator` + `architecture-deepener`
**When:** onboarding a teammate or an agent; nobody wants to re-read the code for every question.

```text
Generate a navigable wiki of project <path> with llm-wiki-curator:
index, one page per relevant module, real links between pages. Run
architecture-deepener first to decide what deserves its own page
(deep modules) vs. a footnote.
Success: index.md + module pages with links that resolve; a
typical onboarding question answers in ≤2 clicks.
```

## R3 — Teach me the project

**Skills:** `teaching` + `learning-output-style`
**When:** you want to master an area of the repo over a few sessions, not just receive a dump.

```text
Build with teaching a learning plan for repo <repo> so I master
<area> in <N> sessions. Didactic format (learning-output-style):
each session with an objective, minimal reading (exact files), a
hands-on exercise in the repo itself, and a verifiable checkpoint.
Success: plan with N sessions; each checkpoint is a command or
change I run and verify myself.
```

## R4 — Grill the spec before coding

**Skills:** `doc-driven-grilling` + `task-interrogator`
**When:** before implementing a feature from a doc/spec — cheap to ask now, expensive to discover later.

```text
Before implementing <feature>, grill document <path> with
doc-driven-grilling: list ambiguities, undeclared assumptions, and
blocking questions, ranked by risk. Use task-interrogator to turn
what's left into tasks with acceptance criteria.
Success: list of gaps I can answer in one pass + tasks with
verifiable acceptance; no generic questions.
Note: the two skills overlap on the core grilling; here they run in
sequence with distinct roles (grilling+docs → tasks with
acceptance), never as parallel drivers.
```

## See also

- `session-handoff` — end of a long session: generate a handoff so the next session starts without re-exploring.
- `bug-diagnostics` — when the goal is understanding broken behavior, not the whole project.
- In this repo, `graphify query "<question>"` (project tooling, `graphify-out/`) answers codebase questions more cheaply than exploring files.
