---
name: async-patterns
description: Async and concurrency pattern advisor for JavaScript/TypeScript, Python, Go, and Rust. Identifies race conditions, missing error handling in promise chains, N+1 async anti-patterns, unbounded parallelism, and missing cancellation. Recommends correct patterns: Promise.all, p-limit, AbortController, AsyncLocalStorage, worker threads. Use when async code has bugs, timeouts, or memory leaks.
---

# Async Patterns

Correct async code is hard. This skill finds the bugs and shows the fix.

## Quick Start

```
/async-patterns                   — audit current codebase async patterns
/async-patterns --file src/api.ts — analyze single file
/async-patterns --race-conditions — focus on race condition detection
/async-patterns --fix             — apply safe pattern upgrades
```

## Common Anti-Patterns and Fixes

### 1. Sequential instead of parallel (N+1 async)
```typescript
// ❌ 100 users × 50ms each = 5,000ms
for (const userId of userIds) {
  const user = await db.user.findById(userId)
  users.push(user)
}

// ✅ all in parallel = ~50ms
const users = await Promise.all(userIds.map(id => db.user.findById(id)))

// ✅ with concurrency limit (avoid overwhelming DB)
import pLimit from 'p-limit'
const limit = pLimit(10)
const users = await Promise.all(userIds.map(id => limit(() => db.user.findById(id))))
```

### 2. Swallowed promise rejections
```typescript
// ❌ fire and forget — errors silently disappear
sendEmail(user).catch(() => {}) // hiding the error
doSomething() // no await, no catch

// ✅ explicit non-critical handling
sendEmail(user).catch(err => logger.warn('Email failed, non-critical', { err }))

// ✅ or make it explicit you don't care (and document why)
void sendAnalytics(event) // non-critical telemetry, intentional fire-and-forget
```

### 3. Missing AbortController (uncancellable fetches)
```typescript
// ❌ fetch keeps running even if component unmounts / request times out
useEffect(() => {
  fetch('/api/data').then(r => r.json()).then(setData)
}, [])

// ✅ cancellable with timeout
useEffect(() => {
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), 5000)

  fetch('/api/data', { signal: controller.signal })
    .then(r => r.json())
    .then(setData)
    .catch(err => { if (err.name !== 'AbortError') setError(err) })
    .finally(() => clearTimeout(timer))

  return () => controller.abort()
}, [])
```

### 4. Race condition in state updates
```typescript
// ❌ if user types fast, older response can overwrite newer one
const [data, setData] = useState(null)
async function search(query: string) {
  const result = await fetch(`/api/search?q=${query}`)
  setData(await result.json()) // stale response can arrive last
}

// ✅ ignore stale responses with version counter
const requestId = useRef(0)
async function search(query: string) {
  const id = ++requestId.current
  const result = await fetch(`/api/search?q=${query}`)
  if (id === requestId.current) setData(await result.json())
}
```

### 5. Unbound parallelism (memory/connection exhaustion)
```typescript
// ❌ spawns 10,000 concurrent DB connections
await Promise.all(records.map(r => processRecord(r)))

// ✅ bounded concurrency
import pLimit from 'p-limit'
const limit = pLimit(20)
await Promise.all(records.map(r => limit(() => processRecord(r))))
```

### 6. Missing error boundary in Promise.all
```typescript
// ❌ one failure rejects all — you lose partial results
const [users, orders, products] = await Promise.all([
  getUsers(),
  getOrders(),
  getProducts(),
])

// ✅ use Promise.allSettled when partial results are acceptable
const results = await Promise.allSettled([getUsers(), getOrders(), getProducts()])
const [users, orders, products] = results.map(r =>
  r.status === 'fulfilled' ? r.value : null
)
```

### 7. Mutex for shared mutable state (Node.js)
```typescript
// ❌ two concurrent requests can read same balance, both deduct, overdraft
async function deductBalance(userId: string, amount: number) {
  const user = await db.user.findById(userId)
  if (user.balance < amount) throw new Error('Insufficient funds')
  await db.user.update(userId, { balance: user.balance - amount })
}

// ✅ database-level atomic update
await db.user.updateMany({
  where: { id: userId, balance: { gte: amount } },
  data: { balance: { decrement: amount } },
})
// Check affected count — 0 means insufficient funds
```

### 8. Context propagation (AsyncLocalStorage)
```typescript
// Share request context across async calls without prop drilling
import { AsyncLocalStorage } from 'async_hooks'

const requestContext = new AsyncLocalStorage<{ requestId: string; userId: string }>()

// Middleware
app.use((req, res, next) => {
  requestContext.run({ requestId: req.id, userId: req.user?.id }, next)
})

// Anywhere in the call chain
function logEvent(event: string) {
  const ctx = requestContext.getStore()
  logger.info(event, { requestId: ctx?.requestId })
}
```

## Audit Output

```
ASYNC AUDIT — 2026-06-14
==========================
Files analyzed: 34  |  Issues: 12

CRITICAL
  [C1] src/api/reports.ts:45 — UNBOUNDED PARALLELISM
       Promise.all over reportIds (up to 5,000 items)
       → Wrap with pLimit(20)

  [C2] src/hooks/useSearch.ts:23 — RACE CONDITION
       Stale response can overwrite latest result
       → Add requestId counter or use AbortController

HIGH
  [H1] src/workers/emailQueue.ts — SWALLOWED REJECTION
       sendEmail().catch(() => {}) — errors lost silently
       → Log and retry or push to dead-letter queue

MEDIUM
  [M1] src/api/users.ts:67 — SEQUENTIAL N+1
       for...await loop over 50 users
       → Promise.all with pLimit(10)
```
