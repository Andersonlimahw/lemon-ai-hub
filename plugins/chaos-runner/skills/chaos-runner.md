---
name: chaos-runner
description: Chaos experiment orchestration and scheduling. Runs predefined chaos scenarios (latency injection, pod kill, dependency outage), records results, and tracks resilience score over time. Use when scheduling a game day, setting up weekly chaos tests, or verifying that a new circuit breaker works under fault conditions.
---

# Chaos Runner Plugin

Scheduled fault injection. Automated resilience scoring.

## Commands

```
/chaos-runner run <experiment>   — execute a named experiment
/chaos-runner schedule weekly    — schedule weekly chaos (random pod kill)
/chaos-runner history            — show past experiment results
/chaos-runner score              — current resilience score (0-100)
/chaos-runner game-day           — orchestrate a full game day session
```

## Experiment Library

Pre-built experiments (run by name):

| Name | What It Does |
|------|-------------|
| `pod-kill` | Kills a random pod from target deployment |
| `db-latency-500ms` | Adds 500ms to all DB connections via toxiproxy |
| `api-timeout` | Makes payment API time out after 3s |
| `disk-pressure` | Fills disk to 90% on one node |
| `memory-hog` | Allocates 80% of available heap |
| `network-partition` | Blocks all traffic between service A and B |

## Game Day Orchestration

```
/chaos-runner game-day

Phase 1 — Baseline (10 min)
  → Measure: p95 latency, error rate, uptime
  → Confirm steady state

Phase 2 — Experiment (30 min)
  → Run: db-latency-500ms
  → Monitor: circuit breakers, fallbacks, error messages

Phase 3 — Recovery (10 min)
  → Remove fault
  → Confirm return to steady state

Phase 4 — Report
  → Resilience score: 78/100
  → Failed: circuit breaker opened too slowly (12s, target <5s)
  → Action item: reduce CB threshold from 10 failures to 5
```

## Resilience Score

```
RESILIENCE SCORE — 2026-06-14
================================
Total: 78/100

Detection speed:   85/100  (alert in 2min, target <3min) ✅
Recovery speed:    70/100  (recovered in 4min, target <2min) ⚠️
Blast radius:      90/100  (only /checkout affected, not /browse) ✅
User experience:   65/100  (users saw 500 instead of fallback message) ❌
Circuit breaker:   80/100  (opened correctly, but closed too fast) ⚠️
```

Pairs with `/chaos-test` skill for experiment design.
