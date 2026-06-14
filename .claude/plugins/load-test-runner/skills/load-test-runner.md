---
name: load-test-runner
description: Load test suite management and regression detection. Maintains a library of k6/Artillery scripts, runs them on schedule or pre-release, compares results to baseline, and alerts on p99 regressions. Use when setting up pre-release performance gates or tracking latency trends across versions.
---

# Load Test Runner Plugin

Performance baselines, regression detection, nightly tests.

## Commands

```
/load-test-runner init          — scaffold load test suite for this project
/load-test-runner run smoke     — quick smoke test (1 VU, 1 min)
/load-test-runner run peak      — peak load test vs SLO
/load-test-runner run soak      — 2h soak test (detect memory leaks)
/load-test-runner baseline      — save current results as new baseline
/load-test-runner compare       — compare last run vs baseline
/load-test-runner schedule      — set up nightly test cron
```

## Test Suite Structure

```
load-tests/
  smoke.js          — 1 VU, 1 min, verify script works
  peak.js           — 50 VUs, 30 min, simulates peak traffic
  soak.js           — 10 VUs, 2 hours, memory leak detection
  spike.js          — ramp 0→500 in 30s, check recovery
  baselines/
    v3.2.0.json     — performance baseline per release
    v3.3.0.json
```

## Regression Detection

```
REGRESSION ALERT — v3.4.0 vs v3.3.0
=======================================
❌ p99 latency regression detected

Endpoint       v3.3.0   v3.4.0   Change
/api/products    280ms    890ms   +218%  ← REGRESSION
/api/checkout    450ms    460ms    +2%   ✅
/api/users       120ms    115ms    -4%   ✅ (improved)

Root cause suggestion:
  New query in ProductService.findByCategory() introduced in commit c1f9823
  → Run /db-index-advisor to find missing index
```

## Nightly Schedule (cron)

```bash
# Runs every night at 2am against staging
0 2 * * * cd ~/app && k6 run load-tests/soak.js --out json=results/$(date +%Y%m%d).json
```

Pairs with `/load-test` skill for test design and script generation.
