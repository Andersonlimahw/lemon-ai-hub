---
name: db-advisor
description: Automated database query monitoring and N+1 detection. Analyzes ORM query logs, detects repeated queries (N+1 pattern), suggests eager loading or batching fixes, and tracks query count per request. Use when adding DB monitoring, investigating slow endpoints, or reviewing ORM query patterns in a PR.
---

# DB Advisor Plugin

Continuous query monitoring. N+1 caught before production.

## Commands

```
/db-advisor monitor              — enable query logging for current session
/db-advisor n+1                  — detect N+1 patterns in ORM logs
/db-advisor slow-queries         — list queries slower than 100ms
/db-advisor explain <query>      — run EXPLAIN ANALYZE on a query
/db-advisor health               — overall DB health report
/db-advisor weekly-report        — generate markdown health report
```

## N+1 Detection

Automatically detects patterns like:
```
SELECT * FROM users WHERE id = 1    ─┐
SELECT * FROM users WHERE id = 2     │ N+1 detected
SELECT * FROM users WHERE id = 3     │ 50 identical queries
...                                  ─┘
```

Suggests fix:
```typescript
// ❌ N+1 — 1 query per order
const orders = await prisma.order.findMany()
for (const order of orders) {
  const user = await prisma.user.findUnique({ where: { id: order.userId } })
}

// ✅ eager load — 1 query total
const orders = await prisma.order.findMany({
  include: { user: true }
})
```

## Health Report

```
DB HEALTH — 2026-06-14
========================
Connections: 28/50 (56%) ✅
Slow queries (>100ms): 14 this hour ⚠️
  Slowest: SELECT * FROM events (avg 820ms) — add index on event_type
N+1 patterns: 3 detected in last hour
  /api/products endpoint: 48 user queries per request → use include
Table bloat: orders_archive 4.2 GB (87% dead rows) — run VACUUM ANALYZE
Replication lag: 0ms ✅
```

Pairs with `/db-index-advisor` skill for index optimization.
