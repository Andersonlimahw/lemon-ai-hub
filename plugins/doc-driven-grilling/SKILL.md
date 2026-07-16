---
name: doc-driven-grilling
description: Interrogatório implacável para planos e designs que cria documentação (CONTEXT.md/glossário, ADRs) durante o processo, enquanto grilla. Combina grilling de decisão com domain-modeling — desafia a linguagem vaga contra o glossário existente, stress-testa cenários concretos, e captura termos e decisões inline conforme cristalizam. Use when user wants to stress-test a plan against their project's language and documented decisions, mentions "grill me", "grilling", or needs to sharpen terminology while deciding.
disable-model-invocation: true
---

# Doc-Driven Grilling

Interrogatório implacável que cria documentação enquanto grilla. Cada termo resolvido vai para o glossário; cada decisão irreversível vira ADR — capturados no momento, não em lote.

Integração: `/grilling` (interrogatório de decisão) + `/domain-modeling` (modelagem de domínio e glossário).

---

## O fluxo

<what-to-do>

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing.

If a question can be answered by exploring the codebase, explore the codebase instead.

</what-to-do>

---

## Domain awareness

During codebase exploration, also look for existing documentation.

### File structure

Most repos have a single context:

```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If a `CONTEXT-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each one lives:

```
/
├── CONTEXT-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── CONTEXT.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── CONTEXT.md
│       └── docs/adr/
```

Create files lazily — only when you have something to write. If no `CONTEXT.md` exists, create one when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is needed.

---

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `CONTEXT.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account' — do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"

### Update CONTEXT.md inline

When a term is resolved, update `CONTEXT.md` right there. Don't batch these up — capture them as they happen. Use the format in [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md).

Don't couple `CONTEXT.md` to implementation details. Only include terms that are meaningful to domain experts.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).

---

## Integration: /grilling + /domain-modeling

This skill unifies two workflows:

- **`/grilling`** — relentless one-question-at-a-time interview that walks the decision tree, resolving dependencies one-by-one. Each question comes with a recommended answer.
- **`/domain-modeling`** — canonical glossary (CONTEXT.md), ADRs, context maps, and relationship modeling. Terms are captured the moment they're resolved, not batched.

The differentiator: documentation is a **byproduct** of grilling, not a separate phase. Every ambiguity surfaced becomes a glossary entry; every irreversible trade-off becomes an ADR. The session leaves behind a documented domain model even if the plan changes.

---

## Credits

Based on **grill-with-docs** by Matt Pocock (https://github.com/mattpocock/skills). Adapted and extended for the lemon-ai-hub plugin ecosystem.
