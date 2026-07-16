# Glossary — Skill Authoring

The domain model for what makes a skill great. A skill exists to wrangle determinism out of a stochastic system; the root virtue is **Predictability**, and every term below is a lever on it. This is the disclosed reference for [`skill-authoring`](SKILL.md).

The terms are grouped by axis: **Invocation** (how a skill is reached), **Information Hierarchy** (how its content is arranged), **Steering** (how the agent\'s runtime behaviour is shaped), and **Pruning** (how it is kept lean). Each **failure mode** lives beside the lever that cures it, tagged _failure mode_.

**Bold terms** in any definition are themselves defined in this glossary; find them by their heading.

> **Credits**: Adapted from the [writing-great-skills GLOSSARY](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-great-skills/GLOSSARY.md) by Matt Pocock.

## Predictability

The degree to which a skill makes the agent behave the same _way_ on every run — the same process, not the same output (a brainstorming skill should _predictably_ diverge; its tokens vary, its behaviour doesn\'t). The root virtue every other term serves — cost and maintainability are symptoms of it, not rivals.

_Avoid_: consistency, reliability, robustness, output-determinism

## Invocation

How a skill is reached — and the two loads you pay for the choice.

### Model-Invoked

A skill that keeps its **description** field, so the agent can see it and fire it autonomously — and the human can still type its name, so model-invocation always _includes_ user reach. There is no model-only state: a description only ever _adds_ agent discovery, never removes the human\'s. Pays a permanent **context load** on every turn in exchange for that discoverability. Reachable by other skills, because the description that makes it agent-discoverable makes it invocable. A model-invoked skill whose content is all **reference** is also one home for shared reference: another skill can invoke it, so reference needed by several skills lives in one place. Pick model-invocation only when the agent must reach the skill on its own; if it never fires except by hand, drop the description and pay no context load.

_Avoid_: ability, tool, capability

### User-Invoked

A skill with its **description** stripped — invisible to the agent and reachable only by the human typing its name (user-_only_, where **model-invoked** is user-_and-agent_). Trades agent-discoverability for zero **context load**. Because it has no description, nothing but the human can reach it: no other skill can fire it.

_Avoid_: procedure, workflow, command

### Description

The skill\'s machine-readable trigger, and the one **context pointer** a **model-invoked** skill is forced to keep loaded at all times. Its mere presence _is_ the invocation axis: keep it and the skill is model-invoked (and reachable by other skills); delete it and the skill is **user-invoked**, reachable only by the human. The source of a model-invoked skill\'s **context load**.

_Avoid_: frontmatter, summary

### Context Pointer

A reference held in the agent\'s context that names some out-of-context material and encodes the condition for reaching it. The **description** is the top-level context pointer; a link to **disclosed reference** is another. Each pointer costs **context load** proportional to its size, so pointers should be compact and trigger-dense.

### Context Load

The permanent token cost a **model-invoked** skill pays every turn, because its **description** (a **context pointer**) must sit in the window for the agent to discover and fire it. The budget every pruning decision protects: if a description doesn\'t earn its context load, the skill should be **user-invoked**.

### Cognitive Load

The cost a **user-invoked** skill pays: the human must remember the skill exists and when to reach for it, because nothing else indexes it. The counterpart to **context load** — you pay one or the other. Cured at scale by a **router skill**.

### Router Skill

A **user-invoked** skill that names other user-invoked skills and when to reach for each, acting as a human-facing index. Cures the **cognitive load** that piles up when user-invoked skills multiply past what one person can remember.

### Leading Word

The compact term that anchors a skill\'s invocation and execution — the single word you would actually type to reach or summarise the skill. Does triple duty: names the skill, seeds the **description**\'s trigger phrasing, and concentrates what the skill _is_ in the fewest tokens. A weak leading word that the model already obeys is a **no-op**; a strong one (_relentless_ over _be thorough_) shifts behaviour without changing technique.

## Information Hierarchy

How a skill\'s content is arranged — the ladder ranked by how immediately the agent needs each piece.

### Steps

Ordered actions in `SKILL.md`, the primary tier of the **information hierarchy**. Each step ends on a **completion criterion**. Use steps when _sequence_ matters: the order of actions is itself the instruction.

### Reference

Material the agent consults as needed, not a sequence. Can sit in-skill (secondary tier) or be **disclosed** behind a **context pointer** (third tier). Use reference when the agent dips in on demand rather than executing top-to-bottom.

### Completion Criterion

The condition that tells the agent a **step** is done. The defence against **premature completion**. Must be _checkable_ (the agent can tell done from not-done) and, where it matters, _exhaustive_ ("every modified model accounted for"). A fuzzy criterion is the necessary condition for rushing; a sharp one resists the pull no matter how many later steps are visible.

### Legwork

The digging the agent does _within_ a step or across **reference** to actually do the work. Driven by a demanding **completion criterion**: "every rule applied" binds flat reference just as "every step done" binds a sequence. Thin legwork is one failure mode; **premature completion** is another — a step can run to full completion with thin legwork, or quit early with thorough intent.

### Information Hierarchy

The ladder ranking content by how immediately the agent needs it:

- **Steps** — in-file, primary
- **Reference**, in-file — secondary
- **Reference**, disclosed — behind a **context pointer**

Move material _down_ the ladder until each tier carries only what its rank demands.

## Granularity

How finely you divide skills — and each cut spends one of the two loads.

### Granularity

How finely you divide skills. Each split spends either **context load** (if the split stays model-invoked) or **cognitive load** (if it becomes user-invoked), so split only when the cut earns it. Two cuts: **by branch** and **by sequence**.

### Branch

A distinct trigger path within a skill. One **branch** per meaningfully different way the skill fires. Splitting by branch lowers the parent\'s **context load** when a branch grows its own **leading word** and trigger phrasing.

### By Branch

A granularity cut: split a skill when one **branch** grows distinct enough to deserve its own **leading word** and **description**. Moves that branch\'s triggers out of the parent\'s description, lowering the parent\'s **context load** — but adds **cognitive load** if the split becomes user-invoked.

### By Sequence

A granularity cut: split an ordered skill when later **steps** only matter after earlier ones finish, and the agent rushes to completion. Hiding post-completion steps behind a real context boundary (a user-invoked hand-off or a subagent dispatch) cures **premature completion**. An inline model-invoked call leaves the later steps in context and clears nothing — the split must cross a real boundary to work.

## Steering

How a skill shapes the agent\'s runtime behaviour beyond the sequence of steps.

### Steering

The discipline of shaping runtime behaviour. Two core moves: keep a **single source of truth**, and prefer **positive** phrasing over **negation**.

### Single Source of Truth

One authoritative place per meaning, so changing behaviour is a one-place edit. The cure for **duplication**. When two locations say the same thing, one is duplication.

### Positive

Steering by naming the target behaviour so the banned one is never spoken. The counterpart to **negation**: _don\'t think of an elephant_ makes the elephant more available, not less. Keep a prohibition only as a hard guardrail you can\'t phrase positively, and even then pair it with what to do instead.

### Negation

_Failure mode._ Steering by prohibition — _don\'t think of an elephant_ — which names the banned thing and makes it more available, not less. The cure is the **positive**: state the target behaviour so the banned one is never spoken.

## Pruning

How a skill is kept lean — every line costs tokens and maintenance.

### Pruning

The discipline of cutting lines that don\'t earn their place. Each line must justify its token and maintenance cost or leave. The four pressures to cut against are the **failure modes**: premature completion, duplication, sediment, sprawl, no-op, negation.

### Relevance

The property of a line still mattering to the skill\'s current behaviour. Lost slowly to **sediment** — stale layers that settle because adding feels safe and removing feels risky.

## Failure Modes

The named anti-patterns. Each lives beside the lever that cures it.

### Premature Completion

_Failure mode._ Ending the current **step** before it is genuinely done, because the agent\'s attention slips to _being done_ rather than to the work. A tug-of-war between visible post-completion steps (the pull forward) and the **completion criterion**\'s clarity (the resistance). Defence, in order: sharpen the criterion first (cheap, local); only if it is irreducibly fuzzy _and_ you observe the rush, hide the later steps by splitting **by sequence** across a real context boundary.

### Duplication

_Failure mode._ The same meaning in more than one place. Costs maintenance and tokens, and inflates a meaning\'s prominence on the **information hierarchy** past its real rank. The cure is the **single source of truth**.

### Sediment

_Failure mode._ Layers of old content that settle in a skill and are never cleared, because adding feels safe and removing feels risky — so stale and irrelevant lines accumulate. The default fate of any skill without a **pruning** discipline; the slow erosion of **relevance**, as opposed to **duplication**\'s repeated meaning.

### Sprawl

_Failure mode._ A skill simply too long, even when every line is live and unique. Hurts readability and maintainability and wastes tokens. The cure is the **information hierarchy**: disclose **reference** behind **context pointers**, and split **by branch** or **by sequence** so each path carries only what it needs.

### No-Op

_Failure mode._ A line the model already obeys by default, so you pay load to say nothing. The test: does it change behaviour versus the default? A weak **leading word** (_be thorough_ when the agent is already thorough-ish) is a no-op; the fix is a stronger word (_relentless_), not a different technique.
