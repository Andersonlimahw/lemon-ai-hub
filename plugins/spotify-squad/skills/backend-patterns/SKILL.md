---
name: backend-patterns
description: >
  Backend development patterns and best practices. Use for API design, database
  optimization, microservice architecture, authentication, caching strategies,
  and server-side implementation.
---

# Backend Patterns

You are the backend engineering expert. You apply proven server-side patterns for APIs, databases, security, and observability. Every recommendation must be concrete, with code examples and anti-patterns to avoid.

---

## 1. API Design

### REST Conventions

#### URL Structure

```
GET    /api/v1/users              → List users (paginated)
GET    /api/v1/users/:id          → Get single user
POST   /api/v1/users              → Create user
PATCH  /api/v1/users/:id          → Partial update
PUT    /api/v1/users/:id          → Full replace
DELETE /api/v1/users/:id          → Soft delete
```

#### Naming Rules

- **Plural nouns** for collections: `/users`, not `/user`.
- **Kebab-case** for multi-word: `/user-profiles`, not `/userProfiles`.
- **Nest for ownership**: `/users/:id/posts` (user's posts).
- **Max 2 levels deep**: `/users/:id/posts/:postId` — no deeper.
- **Query params for filtering**: `GET /users?role=admin&status=active`.

#### Response Envelope

```json
{
  "data": { ... },
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 142,
    "total_pages": 8
  },
  "links": {
    "self": "/api/v1/users?page=1",
    "next": "/api/v1/users?page=2",
    "prev": null
  }
}
```

#### HTTP Status Codes

| Code | Usage |
|------|-------|
| `200` | Success with body |
| `201` | Created — return created resource + `Location` header |
| `204` | Success, no body (DELETE, some PATCH) |
| `400` | Validation error — include field-level errors |
| `401` | Unauthenticated — token missing or expired |
| `403` | Unauthorized — valid token but insufficient permissions |
| `404` | Resource not found |
| `409` | Conflict — duplicate key, version mismatch |
| `422` | Unprocessable entity — business rule violation |
| `429` | Rate limited — include `Retry-After` header |
| `500` | Server error — log details, return generic message |

#### Pagination

Use cursor-based pagination for large datasets:

```json
{
  "data": [...],
  "meta": {
    "has_next": true,
    "cursor": "eyJpZCI6MTAwfQ=="
  }
}
```

Use offset-based only for small, stable datasets where random page access is needed.

### GraphQL Schema Design

#### Schema-First Approach

```graphql
type User {
  id: ID!
  email: String!
  displayName: String!
  avatar: String
  posts(first: Int = 10, after: String): PostConnection!
  createdAt: DateTime!
}

type PostConnection {
  edges: [PostEdge!]!
  pageInfo: PageInfo!
}

type PostEdge {
  node: Post!
  cursor: String!
}

input CreateUserInput {
  email: String!
  displayName: String!
  password: String!
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
}

type CreateUserPayload {
  user: User
  errors: [UserError!]!
}
```

#### GraphQL Rules

- Use **Relay-style connections** for lists (edges + pageInfo).
- **Input types** for mutations — never inline arguments.
- **Payload types** for mutations — always include an `errors` field.
- **DataLoader** for N+1 prevention — batch all database calls.
- Limit query **depth to 5** and **complexity scoring** to prevent abuse.
- Never expose internal IDs directly — use opaque, base64-encoded cursors.

### gRPC Proto Design

```protobuf
syntax = "proto3";
package user.v1;

service UserService {
  rpc GetUser(GetUserRequest) returns (GetUserResponse);
  rpc ListUsers(ListUsersRequest) returns (ListUsersResponse);
  rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
}

message GetUserRequest {
  string user_id = 1;
}

message GetUserResponse {
  User user = 1;
}

message User {
  string id = 1;
  string email = 2;
  string display_name = 3;
  google.protobuf.Timestamp created_at = 4;
}
```

#### gRPC Rules

- **Package versioning**: `package user.v1;` — version in package name.
- **Field numbers are forever** — never reuse deleted field numbers.
- Use `google.protobuf.Timestamp` for dates, not strings.
- Wrap responses in response messages — allows adding metadata later.
- Use **server streaming** for real-time feeds, **bidirectional** for chat.

---

## 2. Database Patterns

### Query Optimization

#### The Query Checklist

1. **EXPLAIN ANALYZE** every query touching >1000 rows.
2. **Select only needed columns** — never `SELECT *` in production.
3. **Avoid N+1** — use JOINs or batch queries.
4. **Parameterize everything** — never concatenate user input.
5. **Limit result sets** — always paginate.

#### Common Optimizations

```sql
-- BAD: Full table scan
SELECT * FROM orders WHERE YEAR(created_at) = 2024;

-- GOOD: Sargable query, uses index
SELECT id, total, status
FROM orders
WHERE created_at >= '2024-01-01'
  AND created_at < '2025-01-01';
```

### Indexing Strategy

| Pattern | Index Type |
|---------|-----------|
| Exact match (`WHERE status = 'active'`) | B-tree |
| Range query (`WHERE created_at > X`) | B-tree |
| Text search (`WHERE name ILIKE '%query%'`) | GIN / trigram |
| JSON field access | GIN |
| Geospatial | GiST / SP-GiST |
| Composite filters | Composite index (most selective first) |

#### Index Rules

- **Covering indexes** for read-heavy queries — include all selected columns.
- **Partial indexes** for filtered subsets: `CREATE INDEX idx_active ON users(email) WHERE status = 'active';`
- **Never index** columns with low cardinality unless combined with high-cardinality columns.
- **Monitor unused indexes** — they slow writes with zero benefit.
- **Composite index order matters**: `(a, b, c)` supports queries on `(a)`, `(a, b)`, `(a, b, c)` but NOT `(b, c)`.

### Migration Patterns

#### Safe Migration Rules

1. **Always reversible** — every `up` has a `down`.
2. **No breaking changes** — expand first, migrate data, then contract.
3. **Column additions**: Add with `DEFAULT NULL`, backfill in batches, then add constraints.
4. **Column removals**: Stop reading → deploy → stop writing → deploy → drop column.
5. **Rename = add new + copy + drop old** — never use `RENAME COLUMN` in production.
6. **Large table migrations**: Use `pt-online-schema-change` or `gh-ost` for MySQL, `pg_repack` for PostgreSQL.
7. **Lock timeouts**: Set `SET lock_timeout = '5s';` to avoid long table locks.

---

## 3. Authentication & Authorization

### JWT Pattern

```
Access Token:
- Short-lived (15 min)
- Stored in memory (never localStorage)
- Contains: sub, roles, permissions, exp, iat, jti

Refresh Token:
- Long-lived (7-30 days)
- Stored in httpOnly secure cookie
- Rotated on each use (one-time use)
- Stored server-side for revocation
```

#### JWT Checklist

- [ ] Use RS256 or ES256 (asymmetric) — never HS256 in distributed systems.
- [ ] Validate `iss`, `aud`, `exp`, `nbf` on every request.
- [ ] Include `jti` for token revocation.
- [ ] Short expiry (15 min max for access tokens).
- [ ] Refresh token rotation with reuse detection.
- [ ] Logout = revoke refresh token server-side.

### OAuth2 Flows

| Flow | Use Case |
|------|----------|
| Authorization Code + PKCE | SPAs, mobile apps, web apps |
| Client Credentials | Service-to-service |
| Device Code | Smart TVs, CLI tools |

**Never use** Implicit flow or Resource Owner Password — both are deprecated.

### RBAC (Role-Based Access Control)

```
Roles: admin, editor, viewer
Permissions: users:read, users:write, posts:read, posts:write, posts:delete

admin  → users:read, users:write, posts:read, posts:write, posts:delete
editor → posts:read, posts:write
viewer → posts:read
```

### ABAC (Attribute-Based Access Control)

Use when RBAC is too coarse. Evaluate policies based on:

- **Subject**: user role, department, clearance level
- **Resource**: owner, classification, status
- **Action**: read, write, delete
- **Context**: time, IP, device

```
ALLOW IF:
  subject.role == "editor"
  AND resource.owner_id == subject.id
  AND action IN ["read", "write"]
  AND context.time BETWEEN 09:00 AND 18:00
```

---

## 4. Caching Strategies

### Redis Patterns

#### Cache-Aside (Lazy Loading)

```
Read:
1. Check cache → hit? return cached.
2. Miss? Query DB → store in cache with TTL → return.

Write:
1. Write to DB.
2. Invalidate cache key.
```

#### Write-Through

```
Write:
1. Write to cache.
2. Cache writes to DB synchronously.

Read:
1. Always read from cache.
```

#### Cache Stampede Prevention

```
# Use probabilistic early expiration
actual_ttl = base_ttl - (random(0, ttl * 0.1))

# Or use locking
if cache.miss(key):
    if cache.setnx(lock_key, 1, ttl=5):
        result = db.query(...)
        cache.set(key, result, ttl=300)
        cache.del(lock_key)
    else:
        sleep(0.1)
        retry()
```

### Cache Key Design

```
# Pattern: {service}:{entity}:{id}:{variant}
user:profile:12345
user:profile:12345:minimal
feed:timeline:12345:page:1
config:feature-flags:v3
```

### Cache Invalidation Rules

- **TTL everything** — no key should live forever.
- **Invalidate on write** — delete or update the cached key.
- **Use versioned keys** for bulk invalidation: `v3:user:12345` → bump to `v4` to invalidate all.
- **Event-driven invalidation** for cross-service: publish `user.updated` → subscribers invalidate their caches.
- **Never cache errors** — or cache with very short TTL (5s) to prevent thundering herd.

### CDN Caching

```
# Static assets: aggressive caching
Cache-Control: public, max-age=31536000, immutable

# API responses: short cache with revalidation
Cache-Control: public, max-age=60, stale-while-revalidate=300

# Private data: no CDN caching
Cache-Control: private, no-store
```

---

## 5. Error Handling Patterns

### Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "email",
        "code": "INVALID_FORMAT",
        "message": "Must be a valid email address"
      }
    ],
    "request_id": "req_abc123",
    "docs_url": "https://api.example.com/docs/errors#VALIDATION_ERROR"
  }
}
```

### Error Code Taxonomy

```
AUTH_*          → Authentication/authorization errors
VALIDATION_*   → Input validation errors
NOT_FOUND_*    → Resource not found
CONFLICT_*     → State conflicts (duplicate, version mismatch)
RATE_LIMIT_*   → Rate limiting
INTERNAL_*     → Server errors (log full details, return generic)
DEPENDENCY_*   → External service failures
```

### Graceful Degradation

1. **Circuit Breaker**: After N failures to a dependency, stop calling it for X seconds.
2. **Fallback**: Return cached/stale data when the primary source is down.
3. **Bulkhead**: Isolate failure domains — one slow dependency shouldn't consume all threads.
4. **Timeout**: Every external call has a timeout. Default: 5s for HTTP, 2s for cache, 30s for DB.
5. **Retry with backoff**: `delay = base * 2^attempt + jitter` — max 3 retries.

---

## 6. Logging & Observability

### Structured Logging

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "info",
  "message": "User profile updated",
  "service": "user-service",
  "trace_id": "abc123",
  "span_id": "def456",
  "user_id": "usr_789",
  "duration_ms": 45,
  "fields": {
    "changed_fields": ["display_name", "avatar"],
    "ip": "192.168.1.1"
  }
}
```

### Logging Rules

- **Structured JSON** — never unstructured text in production.
- **Correlation IDs** — propagate `trace_id` across all services.
- **Log levels**: `debug` (dev only), `info` (business events), `warn` (recoverable issues), `error` (failures needing attention), `fatal` (process must exit).
- **Never log**: passwords, tokens, PII, credit card numbers, full request bodies with sensitive fields.
- **Always log**: request_id, user_id (hashed if needed), duration, status code, error codes.

### The Three Pillars

| Pillar | Tool Examples | Purpose |
|--------|--------------|---------|
| **Logs** | ELK, Loki, CloudWatch | What happened (events) |
| **Metrics** | Prometheus, Datadog, CloudWatch | How much / how often (aggregates) |
| **Traces** | Jaeger, Tempo, X-Ray | How requests flow (causality) |

### Key Metrics to Track

```
# RED Method (for services)
- Rate:    requests per second
- Errors:  error rate (%)
- Duration: latency percentiles (p50, p95, p99)

# USE Method (for resources)
- Utilization: CPU, memory, disk, connections
- Saturation: queue depth, thread pool usage
- Errors: resource errors (OOM, connection refused)
```

### Alerting Rules

- Alert on **symptoms** (error rate > 1%, p99 > 2s), not causes.
- Every alert must have a **runbook link**.
- **Page** for user-facing impact, **ticket** for everything else.
- Set **burn rate** alerts for SLO-based monitoring.

---

## 7. Testing Patterns

### Test Pyramid

```
        /  E2E  \        → Few, slow, expensive (critical paths only)
       / Contract \      → API contract validation between services
      / Integration \    → DB, cache, external service integration
     /    Unit Tests  \  → Many, fast, isolated (business logic)
```

### Unit Testing Rules

- Test **behavior**, not implementation.
- One assertion per test (logical, not literal).
- Use **factories** for test data, not fixtures.
- Mock at **boundaries** (DB, HTTP, file system), not internal classes.
- **Arrange-Act-Assert** structure for every test.

### Integration Testing

```
# Test real database interactions
- Use testcontainers or in-memory DB.
- Each test gets a clean database (transaction rollback or truncate).
- Test complex queries, joins, and constraints.
- Test migration up AND down.

# Test external service integration
- Use WireMock / MSW for HTTP service mocks.
- Test happy path, error responses, timeouts.
- Record/replay for deterministic tests.
```

### Contract Testing (Pact / Schema Validation)

```
# Consumer-driven contracts
1. Consumer (frontend) defines expected API shape.
2. Contract is shared with provider (backend).
3. Provider verifies its API satisfies the contract.
4. Both sides run contract tests in CI.

# Schema validation
- Validate request/response against OpenAPI spec.
- Fail CI if API response doesn't match schema.
```

---

## 8. Security Checklist (OWASP Top 10)

### Prevention Matrix

| Threat | Prevention |
|--------|-----------|
| **A01 Broken Access Control** | Deny by default. Validate permissions on every endpoint. Test IDOR (insecure direct object reference). |
| **A02 Cryptographic Failures** | TLS everywhere. AES-256 for data at rest. bcrypt/argon2 for passwords. Never roll your own crypto. |
| **A03 Injection** | Parameterized queries only. Input validation (allowlist, not blocklist). ORM with prepared statements. |
| **A04 Insecure Design** | Threat modeling. Abuse case testing. Rate limiting on sensitive endpoints. |
| **A05 Security Misconfiguration** | Disable debug in production. Remove default credentials. Security headers (HSTS, CSP, X-Frame-Options). |
| **A06 Vulnerable Components** | Automated dependency scanning (Snyk, Dependabot). Pin versions. Update regularly. |
| **A07 Auth Failures** | MFA for sensitive ops. Account lockout after N failures. Credential stuffing protection. |
| **A08 Data Integrity Failures** | Verify CI/CD pipeline integrity. Sign artifacts. Validate deserialization input. |
| **A09 Logging & Monitoring** | Log auth events, access control failures. Alert on anomalies. Retain logs 90+ days. |
| **A10 SSRF** | Allowlist outbound URLs. Block internal IP ranges. Validate and sanitize URLs. |

### Security Headers

```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
Content-Security-Policy: default-src 'self'; script-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

### Input Validation Rules

- **Validate on the server** — client validation is UX, not security.
- **Allowlist over blocklist** — define what IS valid, not what isn't.
- **Type coercion** — parse integers as integers, not strings.
- **Length limits** — every string field has a max length.
- **File uploads** — validate MIME type by content (magic bytes), not extension. Limit size. Scan for malware.
