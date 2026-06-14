---
name: incident-center
description: Incident tracking, MTTR/MTTD metrics, and postmortem library. Manages the full incident lifecycle from declaration to postmortem close. Use when declaring a new incident, reviewing MTTR trends, searching for similar past incidents, or tracking open action items from postmortems.
---

# Incident Center Plugin

Full incident lifecycle. From alert to action items closed.

## Commands

```
/incident-center declare P1 "Checkout errors"   — open new incident
/incident-center status                          — list open incidents
/incident-center close INC-042                  — mark resolved
/incident-center postmortem INC-042             — generate postmortem template
/incident-center search "database timeout"      — find similar past incidents
/incident-center metrics                        — MTTR/MTTD/frequency report
/incident-center action-items                  — list all open follow-up tasks
```

## Incident Registry

```
OPEN INCIDENTS — 2026-06-14
=============================
INC-047  P1  Checkout 500 errors  44m open  IC: @dev  #inc-2026-06-14-checkout
INC-046  P2  Search latency >2s   2h open   IC: @ops  #inc-2026-06-14-search
```

## MTTR/MTTD Metrics

```
INCIDENT METRICS — Last 90 days
=================================
Total incidents: 23  (P0: 1, P1: 8, P2: 14)
MTTD (mean time to detect):  4.2 min  (target: <5 min) ✅
MTTR (mean time to resolve): 47 min   (target: <60 min) ✅
Recurrence rate: 22% (5 incidents were repeats)

TOP RECURRING ISSUES
  1. DB connection pool exhaustion — 3 incidents (add better pool monitoring)
  2. Payment API timeout — 2 incidents (circuit breaker threshold too high)
```

## Postmortem Search

`/incident-center search "memory leak"` searches past postmortems to find:
- Same root cause occurred before
- What was the fix last time
- Whether that action item was actually completed

Pairs with `/incident-runbook` skill for runbook generation.
