---
name: db-index-advisor
description: Database index optimization advisor for PostgreSQL, MySQL, and SQLite. Analyzes slow queries, missing indexes, unused indexes, and over-indexed tables. Generates CREATE INDEX statements with EXPLAIN ANALYZE estimates. Use when queries are slow, p99 DB latency spikes, or when reviewing a new schema.
---

# DB Index Advisor

Find slow queries. Add the right indexes. Drop the useless ones.

## Quick Start

```
/db-index-advisor                     — analyze current ORM queries + schema
/db-index-advisor --slow-log          — parse slow query log
/db-index-advisor --query "SELECT..." — analyze specific query
/db-index-advisor --table orders      — focus on one table
/db-index-advisor --unused            — find indexes that cost writes but never help reads
```

## Workflow

Claude will:
1. Read schema (migration files / ORM models / schema.prisma)
2. Read query patterns (repository files, ORM queries, raw SQL)
3. Identify sequential scans on large tables
4. Generate `EXPLAIN (ANALYZE, BUFFERS)` commands
5. Suggest indexes ranked by estimated impact
6. Flag redundant and unused indexes
7. Warn about index maintenance cost on write-heavy tables

## Common Index Patterns

### Single column (equality)
```sql
-- Query: WHERE user_id = $1
CREATE INDEX idx_orders_user_id ON orders(user_id);
```

### Composite (equality + sort)
```sql
-- Query: WHERE user_id = $1 ORDER BY created_at DESC
-- ❌ Two separate indexes won't help as much
-- ✅ Composite covers both
CREATE INDEX idx_orders_user_created
  ON orders(user_id, created_at DESC);
```

### Partial index (filter on subset)
```sql
-- Query: WHERE status = 'pending' AND created_at > NOW() - INTERVAL '7 days'
-- Full index on status wastes space (99% rows are 'completed')
CREATE INDEX idx_orders_pending
  ON orders(created_at DESC)
  WHERE status = 'pending';
```

### Covering index (avoid heap fetch)
```sql
-- Query: SELECT id, total FROM orders WHERE user_id = $1
-- Covering index returns result from index alone (no table lookup)
CREATE INDEX idx_orders_user_covering
  ON orders(user_id) INCLUDE (id, total);
```

### Full-text search
```sql
-- Query: WHERE description ILIKE '%payment%'
-- ❌ ILIKE uses sequential scan
-- ✅ GIN index for full-text
CREATE INDEX idx_products_search
  ON products USING gin(to_tsvector('english', description));
-- Query becomes:
-- WHERE to_tsvector('english', description) @@ plainto_tsquery('payment')
```

### JSON/JSONB field
```sql
-- Query: WHERE metadata->>'plan' = 'pro'
CREATE INDEX idx_users_plan
  ON users((metadata->>'plan'));
```

## Output Format

```
DB INDEX ANALYSIS — 2026-06-14
================================
Schema: PostgreSQL 15  |  Tables analyzed: 12  |  Queries analyzed: 34

CRITICAL — Sequential scans on large tables
  [C1] orders table (2.1M rows)
       Query: SELECT * FROM orders WHERE user_id = $1 ORDER BY created_at DESC
       Cost: seq_scan ~480ms → with index ~1.2ms (400× faster)
       → CREATE INDEX idx_orders_user_created ON orders(user_id, created_at DESC);

  [C2] events table (8.4M rows)
       Query: WHERE type = 'click' AND session_id = $1
       Cost: seq_scan ~1,800ms → with partial index ~3ms
       → CREATE INDEX idx_events_click_session
           ON events(session_id)
           WHERE type = 'click';

HIGH — Missing FK indexes (causes slow JOINs)
  [H1] order_items.product_id — no index, causes nested loop on every JOIN

MEDIUM — Redundant indexes (waste write performance)
  [M1] idx_orders_user + idx_orders_user_id — duplicate; drop idx_orders_user

LOW — Unused indexes (last used > 30 days ago per pg_stat_user_indexes)
  [L1] idx_users_phone — 0 scans in 90 days; created 2024-01 for SMS feature
  [L2] idx_products_legacy_sku — 0 scans; SKU format changed

GENERATED SQL
  -- Apply in this order (low-risk first):
  CREATE INDEX CONCURRENTLY idx_orders_user_created ON orders(user_id, created_at DESC);
  CREATE INDEX CONCURRENTLY idx_order_items_product_id ON order_items(product_id);
  DROP INDEX CONCURRENTLY idx_users_phone;
```

## Safety Rules

- Always use `CREATE INDEX CONCURRENTLY` on live tables (no table lock)
- Add indexes during low-traffic windows for very large tables
- Monitor `pg_stat_progress_create_index` during creation
- `EXPLAIN ANALYZE` before + after to confirm improvement
- Don't index columns with <10 distinct values (e.g., boolean, status with 2 values)
- Every index slows INSERT/UPDATE/DELETE — don't over-index write-heavy tables

## Prisma / TypeORM / Drizzle Integration

```typescript
// Prisma — add index to schema.prisma
model Order {
  @@index([userId, createdAt(sort: Desc)])
}

// TypeORM
@Index(['userId', 'createdAt'])
@Entity()
class Order { ... }

// Drizzle
const orders = pgTable('orders', { ... }, (table) => ({
  userCreatedIdx: index('idx_orders_user_created')
    .on(table.userId, table.createdAt),
}))
```
