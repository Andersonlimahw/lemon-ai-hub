---
id: <run-id>-<NN>
severity: P0 | P1 | P2 | P3        # P0 security/data-loss · P1 broken core flow · P2 degraded UX · P3 polish
type: bug | inconsistency | improvement | security | a11y
screen: <route>
owner_doc: ${OWNER_DOCS_ROOT}/<x>/index.md
status: open                        # open → triaged → planned → fixed → verified
found_at: <ISO date>
run: <run-id>
---

# <Title — one line, action-oriented>

## Summary
<2–3 lines: what's wrong and why it matters to the user/business.>

## Steps to reproduce
1. Go to <url>
2. <action>
3. <observe>

## Expected vs Actual
- **Expected** (per `owner_doc`): <...>
- **Actual:** <...>

## Evidence
- Screenshot / GIF: <path or "captured in session">
- Console: <relevant error, verbatim>
- Network: <failing request: method, path, status>

## Suggested fix (hypothesis)
<engineering lens — where it likely lives in the codebase; the triage agent refines this with /graphify.>

## Lens
<which expert lens flagged it: QA | Product | Engineering | Security>
