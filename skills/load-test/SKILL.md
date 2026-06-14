---
name: load-test
description: Load testing setup, execution, and analysis with k6, Artillery, or Locust. Generates test scripts, defines VU ramp-up scenarios, interprets p99 latency and error rate results, and suggests infrastructure fixes. Use when user wants to load test an API, check throughput limits, validate SLO headroom, or diagnose performance under traffic.
---

# Load Test

Design, run, and analyze load tests. Find your system's breaking point before users do.

## Quick Start

```
/load-test scaffold           — generate k6 script from OpenAPI spec or cURL examples
/load-test run <script>       — execute + stream metrics
/load-test analyze <results>  — interpret results, flag SLO violations
/load-test soak 30m           — run soak test (low VU, long duration)
/load-test spike              — spike test (sudden burst, check recovery)
```

## Test Scenarios

| Scenario | Goal | Duration |
|----------|------|----------|
| **Smoke** | Verify script works at 1 VU | 1 min |
| **Load** | Simulate expected peak traffic | 30 min |
| **Stress** | Find breaking point | Ramp to failure |
| **Soak** | Detect memory leaks, slow drift | 2–8 hours |
| **Spike** | Instant 10× traffic burst | 1 min burst |
| **Breakpoint** | Binary search for max TPS | Auto |

## Workflow

Claude will:
1. Infer endpoints from OpenAPI spec / cURL samples / route files
2. Generate parameterized k6 or Artillery script
3. Define realistic VU ramp (warm up → peak → cool down)
4. Add SLO thresholds (p95 < 500ms, error rate < 1%)
5. Run test (or provide `docker run` command)
6. Parse JSON results → surface p50/p95/p99/max + error breakdown
7. Recommend: cache headers, DB indexes, connection pool size, rate limits

## k6 Script Template

```javascript
import http from 'k6/http'
import { check, sleep } from 'k6'
import { Rate } from 'k6/metrics'

const errorRate = new Rate('errors')

export const options = {
  stages: [
    { duration: '2m', target: 50 },   // ramp up
    { duration: '5m', target: 50 },   // sustain peak
    { duration: '2m', target: 0 },    // ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
    errors: ['rate<0.01'],
  },
}

export default function () {
  const res = http.get('https://api.example.com/products')
  check(res, { 'status 200': (r) => r.status === 200 })
  errorRate.add(res.status !== 200)
  sleep(1)
}
```

## Artillery Script Template

```yaml
config:
  target: "https://api.example.com"
  phases:
    - duration: 60
      arrivalRate: 10
      name: Warm up
    - duration: 300
      arrivalRate: 50
      name: Peak load

scenarios:
  - name: "Browse products"
    flow:
      - get:
          url: "/products"
          expect:
            - statusCode: 200
            - maxResponseTime: 500
```

## Results Interpretation

```
/load-test analyze results.json

LOAD TEST RESULTS — 2026-06-14
================================
Duration: 9m  |  VUs peak: 50  |  Total requests: 12,430

LATENCY
  p50:  42ms   ✅
  p95:  380ms  ✅ (threshold: <500ms)
  p99:  1,240ms ❌ (threshold: <1000ms)
  max:  4,800ms ❌

ERROR RATE: 2.3% ❌ (threshold: <1%)
  404 Not Found:    0.1%
  502 Bad Gateway:  1.8%  ← upstream timeout
  503 Unavailable:  0.4%

BOTTLENECKS IDENTIFIED
  → DB query P99 800ms on /products?filter=... — add composite index
  → Upstream timeout at 2.2× peak — increase ALB timeout or add circuit breaker
  → Memory grows 15MB/min during soak — suspect connection leak in pool

RECOMMENDATIONS
  1. Add index: CREATE INDEX ON products(category_id, created_at DESC)
  2. Set keepAlive timeout > ALB idle timeout (current: 60s, ALB: 120s)
  3. Limit connection pool max to CPUs × 2 (not unlimited)
```

## SLO Thresholds Reference

| Tier | p95 | p99 | Error Rate |
|------|-----|-----|-----------|
| Real-time (chat, trading) | <100ms | <250ms | <0.01% |
| Interactive (API, web) | <300ms | <800ms | <0.1% |
| Batch (reports, exports) | <2s | <5s | <1% |
