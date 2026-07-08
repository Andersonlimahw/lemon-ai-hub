# API Test Loop Execution Plan

## Objective
Validate local backend API endpoints using HTTP requests (`curl`), verify conformance to RESTful best practices, validate robust error handling and input validation gates, audit common security vulnerabilities, and apply surgical presentation/middleware layer fixes.

## Standard Scenarios

### 1. REST Path & Method Mapping
- Nouns over verbs for resource endpoints (e.g. `/users` instead of `/getUsers`).
- Pluralization naming consistency.
- Correct mapping of HTTP methods (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS).

### 2. Input Validation Gates
- Validate endpoint behaviors under malformed JSON, empty payloads, missing required headers, wrong data types, or out-of-range bounds.
- Ensure validation failures return `400 Bad Request` or `422 Unprocessable Entity` with clean error fields, instead of a server crash or `500 Internal Server Error`.

### 3. Response Format & Envelope
- Consistent JSON output structure.
- HTTP status codes match operation outcome (e.g. `201 Created` for creations, `204 No Content` for empty deletes, `404 Not Found` for missing resources).
- Error payloads follow a standardized dictionary format.

### 4. API Security Audit
- Authentication bypass validation (can protected routes be queried without tokens?).
- IDOR checks (does altering resource IDs in path/body allow unauthorized data fetch?).
- SQL Injection and path traversal probes.
- Missing rate-limit checks (response headers like `X-RateLimit-*`).
- Absence of security headers (e.g., `X-Frame-Options`, `Content-Security-Policy`, `Strict-Transport-Security`).

### 5. Performance & Caching
- Response latency under typical payload constraints.
- Correct use of `Cache-Control` or `ETag` headers for read operations.

## Execution Steps

1. **Setup**: Identify the project's local port, backend startup command, and environment variables.
2. **Scan**: Discover route definitions in routers, controllers, or OpenAPI specifications.
3. **Probe**: Execute `curl -i` requests for standard CRUD operations and boundary conditions.
4. **Log**: Record discovered anomalies in `findings.md`.
5. **Fix**: Map the issue to the controller, middleware, or validation schema, and apply a minimal, surgical fix.
6. **Verify**: Run the local test suite and re-execute curl command to prove resolution.
7. **Reflect**: Close finding status as `fixed` and commitConventional Commits.

## Blocked Actions (Require Confirmation)

- Dropping, truncating, or deleting database tables or cache clusters.
- Changing shared database models or migration scripts that would break other microservices or systems.
- Committing credentials, environment keys, or private certificates.
- Disabling global authorization handlers or CORS constraints.
