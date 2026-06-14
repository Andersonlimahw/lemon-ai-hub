---
name: chaos-test
description: Chaos engineering scenarios for resilience testing. Designs fault injection experiments (network partitions, latency injection, dependency failures, disk pressure, memory leaks) and verifies circuit breakers, retries, and fallbacks work correctly. Use when building resilience features, verifying SLO under failure conditions, or preparing for production chaos days.
---

# Chaos Test

Deliberately break things to prove your system handles failure gracefully.

## Quick Start

```
/chaos-test design              — design experiments for this codebase
/chaos-test network-delay 500ms — inject network latency to dependencies
/chaos-test kill-dep <service>  — simulate dependency outage
/chaos-test memory-pressure     — simulate memory exhaustion
/chaos-test verify-circuit      — verify circuit breakers work
/chaos-test steady-state        — define and verify steady-state hypothesis
```

## Chaos Experiment Template

Every experiment follows this structure:

```
Hypothesis: "When [condition], the system will [expected behavior]"
Steady state: [metrics that define normal operation]
Method: [what you will break]
Rollback: [how to undo instantly]
Success: [what proves the hypothesis]
```

## Common Experiments

### 1. Dependency Outage
```
Hypothesis: When payment service is down, checkout shows friendly error
            and no charges occur (idempotent)
Steady state: checkout completion rate >95%, payment errors <0.1%
Method: Block traffic to payment service (iptables / TC / mock)
Rollback: Restore iptables rule
Success: - Users see "Payment temporarily unavailable, try again"
         - No partial charges in DB
         - Circuit breaker opens after 5 failures
         - Circuit closes after 30s (configurable)
```

### 2. High Latency Injection
```
Hypothesis: When DB queries take 2s, API still responds within 5s SLO
            (no cascade timeout)
Steady state: p95 API latency <500ms
Method: Add 2s delay to DB connection (tc netem or toxiproxy)
Rollback: Remove tc rule
Success: - API p95 latency <5s (degraded but within SLO)
         - No thread pool exhaustion
         - Timeouts propagate, not hang
```

### 3. Memory Pressure
```
Hypothesis: When JVM/Node heap reaches 85%, GC kicks in and
            service recovers without OOM crash
Steady state: Memory <70%, p99 latency <1s
Method: Allocate large in-memory object (stress-ng / custom script)
Rollback: Kill stress process
Success: - Memory returns to <70% after GC
         - No process crash
         - Error rate stays <1%
```

### 4. Pod/Process Kill
```
Hypothesis: Killing one pod causes zero user-visible errors
            (health check + rolling deploy pattern)
Steady state: HTTP 200 rate >99.9%
Method: kubectl delete pod [random pod from deployment]
Rollback: k8s auto-restarts; monitor for recovery
Success: - Kubernetes replaces pod in <30s
         - Zero HTTP errors during replacement
         - Load balancer removes unhealthy pod before kill
```

## Toxiproxy Setup (network fault injection)

```bash
# Install
brew install toxiproxy

# Proxy your DB connection
toxiproxy-cli create --listen localhost:5433 --upstream localhost:5432 db-proxy

# Inject 500ms latency
toxiproxy-cli toxic add db-proxy --type latency --attribute latency=500

# Inject 10% packet loss
toxiproxy-cli toxic add db-proxy --type bandwidth --attribute rate=100

# Simulate timeout
toxiproxy-cli toxic add db-proxy --type timeout --attribute timeout=0

# Remove all toxics (recovery)
toxiproxy-cli toxic remove db-proxy --toxicName latency_downstream
```

## Circuit Breaker Verification

```typescript
// What to verify
[ ] Circuit opens after N failures (default: 5)
[ ] Circuit stays open for M seconds (default: 30)
[ ] Circuit moves to HALF-OPEN after timeout
[ ] Single test request in HALF-OPEN state
[ ] Circuit closes on first success in HALF-OPEN
[ ] Fallback response is user-safe (not error 500)
[ ] Metrics track open/close transitions
```

## Steady State Definition

```yaml
steady_state:
  http_success_rate: ">= 99.5%"
  p95_latency_ms: "<= 500"
  error_rate: "<= 0.5%"
  active_users_session_count: ">= 90% of baseline"
  database_connection_pool: "<= 80% utilized"
```

## Chaos Calendar

Recommended schedule:
- Weekly: Kill a random pod in staging
- Monthly: Dependency outage simulation in staging  
- Quarterly: Game day — full chaos scenario with entire team
- Annually: DR drill — full region failover
