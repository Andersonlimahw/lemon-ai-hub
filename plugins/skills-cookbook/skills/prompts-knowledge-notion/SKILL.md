---
name: prompts-knowledge-notion
description: Ready-to-paste prompts for knowledge workflows — capturing decisions into Notion, meeting intelligence, research documentation, spec-to-implementation, and cross-session learning persistence.
---

# Prompts — Knowledge & Notion

Recipes to turn volatile conversation into persistent knowledge — in Notion and across harness sessions. Complements track [prompts-project-understanding](../prompts-project-understanding/SKILL.md): that one helps you understand; this one helps you record and reuse.

## R1 — Capture decisions and knowledge

**Skills:** `notion-knowledge-capture`
**When:** the session/discussion produced decisions that can't die in the chat.

```text
Capture with notion-knowledge-capture the decisions from this
session/thread about <topic> into page/database <destination>:
decision, context, discarded alternatives, and follow-ups with an
owner.
Success: page created with traceable decisions; follow-ups as
actionable items; no raw transcript dump.
```

## R2 — Meeting intelligence

**Skills:** `notion-meeting-intelligence`
**When:** meeting notes need to become actions, not archaeology.

```text
Process with notion-meeting-intelligence the notes from meeting
<meeting/page>: extract decisions, owned actions with deadlines,
and open points; cross-reference against prior meetings in series
<series>.
Success: summary with assigned actions; recurring open points
flagged; link to the sources.
```

## R3 — Documented research

**Skills:** `notion-research-documentation`
**When:** research (technical or market) needs an auditable trail of sources.

```text
Document with notion-research-documentation the research on
<question>: structure question → sources → findings → synthesis →
recommendation, in database <destination>.
Success: every finding linked to a source; synthesis kept separate
from opinion; recommendation with stated confidence.
```

## R4 — Notion spec → implementation

**Skills:** `notion-spec-to-implementation` + `doc-driven-grilling`
**When:** the spec lives in Notion and will become code.

```text
Pull spec <Notion page> with notion-spec-to-implementation and
grill it first with doc-driven-grilling: ambiguities and
assumptions first, then the implementation plan with per-step
verification.
Success: spec gaps answered or logged; plan with "→ verify:" per
step; spec→code traceability per item.
```

## R5 — Learning that survives the session

**Skills:** `continual-learning` + `session-handoff`
**When:** lessons and context need to carry across sessions/compactions.

```text
Persist with continual-learning the lessons from this session on
<topic> (mistakes made, patterns that worked). Generate with
session-handoff the handoff for the next session to continue
without re-exploring.
Success: lessons queryable in the next session; handoff with
state, decisions, and next steps in ≤1 page.
```

## See also

- `teaching-workspace` — structured study environment; `teaching` builds the plan (track [prompts-project-understanding](../prompts-project-understanding/SKILL.md) R3).
- `llm-wiki-curator` — wiki of the code; Notion holds the rest of the knowledge.
- `writing-guidelines` — writing standard for everything these recipes produce.
