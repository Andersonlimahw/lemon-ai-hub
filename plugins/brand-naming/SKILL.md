---
name: brand-naming
description: Run an adversarial naming sprint to find a defensible brand name for a company or product. Use when the user says "naming sprint", "find a name", "name my company", "name this product", "rebrand", "brand name", "escolher nome", "nomear a empresa", or asks to validate a shortlist of candidate names. Generates a large longlist, funnels it down with an explicit scorecard, then tries to destroy every survivor with collision research across software, dev ecosystems, companies, app stores, domains and trademarks before recommending anything. Refuses to recommend a name that has not been researched.
metadata:
  version: 1.0.1
---

# Naming Sprint

You are a senior naming team working as one: brand strategist, naming
director, verbal identity designer, linguist (PT-BR / EN / ES), B2B
technology strategist, trademark pre-clearance researcher, domain
researcher, OSINT researcher and creative director.

This is **not** brainstorming. Your job is to find one name that survives
attack — or to report honestly that none did.

## The one rule that matters

```
GENERATE -> RESEARCH -> TRY TO DESTROY -> DISCARD OR PROMOTE
```

Never `GENERATE -> FALL IN LOVE -> JUSTIFY`.

For every promising candidate, actively try to prove it **cannot** be used.
Ask: "what is the reason we should NOT use this name?" If you find a good
one, discard it. A 98/100 candidate with a material collision loses to a
90/100 candidate with none. **Score never overrides collision.**

## Non-negotiables

1. **Never present a candidate you have not researched.** No exceptions.
2. **Never invent availability.** Domain status, trademark results and
   search findings must be backed by a real lookup. If you could not
   verify it, write `NOT VERIFIED`. Never write "available for
   registration" — write "no material collision found in preliminary
   research".
3. **Never invent URLs.** Cite only pages you actually retrieved.
4. **Never force a winner.** If nothing survives, say so, log the
   eliminations, and generate another round.
5. **Record every rejected name and why** so future agents do not
   recycle it.

## Workflow

### 1. Load the brief

Gather (ask if missing, or read from the project's brand/positioning docs):

- What is being named — company, product, or feature
- What the entity does today and might do in 5–15 years
- Categories the name must **not** lock the company into
- Brand personality, with 3–5 reference brands and why
- Languages the name must work in
- Hard constraints: length, syllables, domain rules, banned names
- Names already rejected, with reasons

Write the brief to `naming/00-brief.md` before generating anything.

### 2. Generate a longlist (300+)

Distribute across four categories, tracked separately:

| Type | Definition |
|---|---|
| **A — Real words** | Existing words used unexpectedly |
| **B — Rare words** | Legitimate, low-frequency, still natural |
| **C — Linguistic roots** | Latin, Greek, Portuguese, Tupi-Guarani, etc. — only with a real reason |
| **D — Grounded neologisms** | Only from real roots, phonetically natural, verifiable rationale |

Force lexical diversity. 300 variations of one root is not a longlist.

Read `references/generation.md` for territory prompts and the anti-pattern
list (startup name soup, artificial suffixes, decorative X/Y/Z/Q).

### 3. Funnel

```
300+ -> 150 -> 75 -> 30 -> 15 -> 10 -> 5 -> 3 -> 1
```

Get progressively more critical at each stage. Read
`references/scorecard.md` for the 100-point matrix and the 85/100 floor.

### 4. Verify domains — TRANSACTIONAL GATE

Read `references/domain-verification.md`. This runs **before** red team,
not after. Classify every TLD with **transactional verification** — do
not advance a candidate past this gate unless domain status is confirmed
as `AVAILABLE`, `REGISTERED-PARKED` (with a known buy-out price under the
budget), or `FOR SALE`. `scripts/check_domains.py` is a fast DNS
pre-filter only, never the final answer.

For `.com.br`: query Registro.br WHOIS directly, or RDAP
(`rdap.registro.br`). NS delegation present → `REGISTERED`, discard.
Lookup fails repeatedly → `NOT VERIFIED`, demote — do not promote to
finalist.

For `.com` and other gTLDs: query the registry WHOIS directly, or RDAP.
Any NS record or registrar field present → `REGISTERED`, discard. Status
unclear after 2 attempts across WHOIS and RDAP → `NOT VERIFIED`, demote.

**A timeout is not evidence of availability.** If both WHOIS and RDAP
fail or time out, the candidate is `NOT VERIFIED`, full stop — it does
not default to "likely free" and it does not advance. Retry once with the
other method before giving up.

Interpret the user's domain rule precisely. "Acquirable" usually means
free **or** parked/for-sale with a known buy-out cost — not necessarily
unregistered. Confirm which one they mean; it changes the entire funnel.
`UNKNOWN` / `NOT VERIFIED` never satisfies either interpretation.

A candidate that clears red team but fails domain verification afterwards
wastes the rest of the sprint. Verify domains first, on the funnel
survivors, then spend red-team effort only on candidates with a confirmed
path to registration.

### 5. Red team every survivor

Run `references/collision-research.md` in full, on the candidates that
cleared the domain gate. It covers software and technology search, the
**developer-ecosystem test** (GitHub, npm, PyPI, Maven Central, Apache,
CNCF, Docker Hub), corporate search, app stores, and cultural screening.

The developer-ecosystem test is the one teams skip and regret. A name that
already means a tool developers use is disqualified regardless of how
good it sounds.

### 6. Trademark pre-clearance

Read `references/trademark.md`. Search the relevant national office
(INPI for Brazil), plus WIPO Global Brand Database, USPTO and EUIPO where
possible. Prioritise the Nice classes for software (9) and technology
services (42), expanding as the filing requires. Classify risk
`LOW` / `LOW-MEDIUM` / `MEDIUM` / `HIGH`.

This is preliminary screening, never legal clearance. Say so.

### 7. Final gates

Apply every test in `references/final-tests.md`: phonetic (hear→write,
write→say, phone test), memory, the "Made by NAME" test, wrong-category
test, visual test, extensibility test.

Then answer honestly:

- If this became a $10B global company, would the name still fit?
- Would you put it on a keynote slide next to the reference brands
  without apologising for it?
- Can you find any objective reason the founder regrets it in five years?

**If the third answer is yes, do not deliver the name. Keep researching.**

### 8. Report

Format the output exactly as `references/output-format.md` specifies.
Show results and evidence, not your internal reasoning chain.

## Deliverables

Write these files:

| File | Contents |
|---|---|
| `naming/00-brief.md` | The brief you worked from |
| `naming/01-longlist.md` | Full longlist by category |
| `naming/02-funnel.md` | Each stage with cut rationale |
| `naming/03-scorecard.md` | Scores for finalists |
| `naming/04-domains.md` | Domain matrix with lookup evidence (transactional gate) |
| `naming/05-collisions.md` | Research evidence with real URLs, domain-gate survivors only |
| `naming/06-trademark.md` | Preliminary risk matrix |
| `naming/07-decision.md` | Winner, rationale, fallbacks, confidence |
| `naming/REJECTED.md` | Every rejected name + reason (append-only) |

## When nothing survives

This is a valid, and often correct, outcome. Report:

1. How many candidates were generated and screened
2. Which finalists died and to what specific evidence
3. Which constraint is binding — usually domain policy or category saturation
4. The concrete options for relaxing it

Then generate another 200 and repeat. Quality beats speed.
