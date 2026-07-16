---
name: skill-authoring
description: Reference for creating and editing skills well — the vocabulary and principles that make a skill predictable. Covers invocation, information hierarchy, granularity, steering, pruning, and failure modes.
disable-model-invocation: true
---

# Skill Authoring

A skill exists to wrangle determinism out of a stochastic system. **Predictability** — the agent taking the same _process_ every run, not producing the same output — is the root virtue; every lever below serves it.

**Bold terms** are defined in [`GLOSSARY.md`](GLOSSARY.md); look them up there for the full meaning.

> **Credits**: Based on [writing-great-skills](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-great-skills/SKILL.md) by Matt Pocock (https://github.com/mattpocock/skills). Adapted for the Lemon AI Hub plugin ecosystem.

## Invocation

Two choices, trading different costs:

- A **model-invoked** skill keeps a **description**, so the agent can fire it autonomously _and_ other skills can reach it (you can still type its name too). It contributes to **context load** — the description sits in the window every turn. Mechanics: omit `disable-model-invocation`, and write a model-facing description with rich trigger phrasing ("Use when the user wants…, mentions…").
- A **user-invoked** skill strips the description from the agent\'s reach: only you, typing its name, can invoke it — and no other skill can. Zero context load, but it spends **cognitive load**: _you_ are the index that must remember it exists. Mechanics: set `disable-model-invocation: true`; the `description` becomes human-facing — a one-line summary, trigger lists stripped.

Pick model-invocation only when the agent must reach the skill on its own, or another skill must. If it only ever fires by hand, make it user-invoked and pay no context load.

When user-invoked skills multiply past what you can remember, that piled-up cognitive load is cured by a **router skill**: one user-invoked skill that names the others and when to reach for each.

## Writing the description

A model-invoked **description** does two jobs — state what the skill is, and list the **branches** that should trigger it. Every word increases **context load**, so a description earns even harder pruning than the body:

- **Front-load the skill\'s leading word** — the description is where it does its invocation work.
- **One trigger per branch.** Synonyms that rename a single branch are **duplication** — "build features using TDD … asks for test-first development" is one branch written twice. Collapse them; keep only genuinely distinct branches.
- **Cut identity that\'s already in the body.** Keep the description to triggers, plus any "when another skill needs…" reach clause.

## Information hierarchy

A skill is built from two content types — **steps** and **reference** — that mix freely: a skill can be all steps, all reference, or both. The core decision is which to use and where each sits on the **information hierarchy**, a ladder ranked by how immediately the agent needs the material:

1. **In-skill step** — an ordered action in `SKILL.md`, the primary tier: what the agent does, in order. Each step ends on a **completion criterion**, the condition that tells the agent the work is done. Make it _checkable_ (can the agent tell done from not-done?) and, where it matters, _exhaustive_ ("every modified model accounted for").
2. **In-skill reference** — material the agent consults as needed, secondary to steps. Lives in the same file but is not a sequence; the agent dips in when a step demands it.
3. **Disclosed reference** — pulled out of `SKILL.md` behind a **context pointer** (a link or named callout). The agent only loads it when a step or branch needs it, keeping the top tier lean.

Move material _down_ the ladder (from in-skill step, to in-skill reference, to disclosed) until each tier carries only what its rank demands. The test for "is this a step or reference?" is _sequence_: if order matters, it\'s a step; if the agent consults it on demand, it\'s reference.

### Completion criteria drive legwork

A demanding completion criterion drives thorough **legwork** — the digging the agent does within the work — whether the skill has steps or not, since "every rule applied" binds flat reference just as "every step done" binds a sequence.

## Leading words

A **leading word** is the compact term that anchors a skill\'s invocation and its execution — the single word you would actually type. It does triple duty: it names the skill (so you can reach it), seeds the description\'s trigger phrasing, and concentrates what the skill _is_ in the fewest tokens.

- A weak leading word (_be thorough_ when the agent is already thorough-ish) is a **no-op** — it changes no behaviour.
- A strong leading word (_relentless_) shifts behaviour without changing technique.
- The leading word belongs at the front of the description: that is where invocation happens.

## Granularity

**Granularity** is how finely you divide skills, and each cut spends one of the two loads, so split only when the cut earns it. Two cuts:

- **By branch** — split when one **branch** of a skill grows distinct enough to deserve its own leading word and description. Lowers the **context load** of the parent (the branch\'s triggers move out of the parent\'s description) but adds cognitive load if the split becomes user-invoked.
- **By sequence** — split an ordered skill when later steps only matter after earlier ones finish, and the agent rushes to completion. Hiding post-completion steps behind a real context boundary (a user-invoked hand-off or a subagent dispatch) cures **premature completion**; an inline model-invoked call leaves the later steps in context and clears nothing.

## Steering

**Steering** is how a skill shapes the agent\'s runtime behaviour beyond the sequence of steps. Two disciplines:

- Keep each meaning in a **single source of truth**: one authoritative place, so changing the behaviour is a one-place edit.
- Prefer **positive** steering over **negation**. _Don\'t think of an elephant_ names the elephant and makes it more available, not less. State the target behaviour so the banned one is never spoken; keep a prohibition only as a hard guardrail you can\'t phrase positively, and even then pair it with what to do instead.

## Pruning

Pruning is the discipline that keeps a skill lean. Every line costs tokens and maintenance, so each must earn its place. The four pressures to cut against are the **failure modes** below.

Keep the **single source of truth**: one authoritative place per meaning. When two locations say the same thing, one is **duplication**.

## Failure modes

Use these to diagnose issues the user may be having with the skill.

- **Premature completion** — ending a step before it\'s genuinely done, attention slipping to _being done_. Defence, in order: sharpen the completion criterion first (cheap, local); only if it is irreducibly fuzzy _and_ you observe the rush, hide the post-completion steps by splitting (the sequence cut).
- **Duplication** — the same meaning in more than one place. Costs maintenance and tokens, and inflates a meaning\'s prominence on the ladder past its real rank.
- **Sediment** — stale layers that settle because adding feels safe and removing feels risky. The default fate of any skill without a pruning discipline.
- **Sprawl** — a skill simply too long, even when every line is live and unique. Hurts readability and maintainability and wastes tokens. The cure is the ladder: disclose **reference** behind pointers, and split by **branch** or sequence so each path carries only what it needs.
- **No-op** — a line the model already obeys by default, so you pay load to say nothing. The test: does it change behaviour versus the default? A weak leading word (_be thorough_ when the agent is already thorough-ish) is a no-op; the fix is a stronger word (_relentless_), not a different technique.
- **Negation** — steering by prohibition backfires: _don\'t think of an elephant_ names the elephant and makes it more available, not less. Prompt the **positive** — state the target behaviour so the banned one is never spoken; keep a prohibition only as a hard guardrail you can\'t phrase positively, and even then pair it with what to do instead.

## Completion criteria for this skill

When you finish editing or creating a skill, verify:

- Every **step** ends on a checkable **completion criterion**.
- No meaning lives in more than one place (**single source of truth**).
- The description, if present, is pruned to triggers plus reach clauses — no identity that the body already carries.
- The invocation choice (model- vs user-invoked) matches how the skill is actually reached.
- Each **leading word** is strong enough to change behaviour versus the default.
- No line is a **no-op** or **negation** that a positive phrasing could replace.
