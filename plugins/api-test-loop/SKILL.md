---
name: api-test-loop
description: Executes a continuous validation loop for backend REST APIs using CURL commands. Records findings (REST standards, path, HTTP verbs, inputs, outputs, documentation, security gaps, performance) and applies minimal surgical fixes in routers, controllers, validation schemas, or middleware.
---

# api-test-loop

This skill guides the automated or manual testing and security/design bug-fixing loop for backend API applications using CURL and shell operations.

## Triggers
- Request to validate backend APIs, verify RESTful routing, or test endpoint security.
- Discovery of API bugs (e.g. 500 status codes, input validations failing, unauthenticated endpoint access, performance bottlenecks, non-standard outputs).
- Execution of the continuous validation cycle: `discover -> curl probe -> inspect -> log finding -> apply minimal fix -> build/test -> revalidate`.

## Loop Process

### 1. API Discovery & Spec Scan
- Locate the API code, router definitions, controllers, and validation schemas (e.g., Zod, Joi, class-validator, marshmallow, Pydantic, Go structs, Rust Serde).
- Locate API documentation (e.g., `openapi.yaml`, Swagger json, postman collection) to establish expectations.
- **verify:** route mappings and environment configuration (port, local URL) are identified.

### 2. PLAN (Spec-Driven Design)
- Write `docs/test-plans/api-test-loop/loop.md` outlining target API scenarios.
- List test cases for each route: valid payloads, boundary/empty payloads, invalid types, and unauthorized requests.
- **verify:** test inputs are defined before making requests.

### 3. PROBE (Execute Requests)
- Start the backend server locally if not already running (or identify its port).
- Execute HTTP requests using `curl` commands. Use `-i` or `-v` flag to output headers and response payload.
- Save execution logs or command snippets for documentation.
- **verify:** curl command receives a response (even if an error code).

### 4. AUDIT & LOG
- Inspect headers and payload returned.
- Check against REST best practices:
  - **Path**: Is the URI path noun-based, singular/plural consistent, lowercase, and representing resource hierarchies correctly?
  - **Method**: Is the correct HTTP method used (e.g., GET for read, POST for create, PUT/PATCH for update, DELETE for remove)?
  - **Input Validation**: Does the endpoint handle bad input correctly? (e.g. returning `400 Bad Request` or `422 Unprocessable Entity` with details, instead of crash/`500 Internal Server Error`).
  - **Output Format**: Is JSON returned with standard keys? Are errors formatted consistently (e.g. `{ "error": "message", "details": [...] }`)?
  - **Documentation**: Does the behavior match the Swagger/OpenAPI spec?
  - **Security Gaps**: Can endpoints be accessed without auth headers? Are IDs guessable (IDOR)? Does input sanitizer check for SQL Injection, path traversal, XSS? Are CORS and security headers (`X-Frame-Options`, `Content-Security-Policy`) correct? Is there basic rate-limiting?
  - **Performance**: Check the `X-Runtime` or latency. Is Cache-Control used when reading static resources?
- Log issues to `docs/test-plans/api-test-loop/findings.md` using the unified finding format.
- **verify:** finding ID `API-FINDING-XXX` contains concrete steps to reproduce with a curl command.

### 5. APPLY FIX
- Modify the backend source code (routes, controllers, middleware, validators) surgically.
- Focus on the presentation, routing, validation, or security filter layers.
- Avoid modifying core database schemas, migrations, or database models unless required.
- **verify:** code edits are minimal, target the root cause, and follow the language's clean coding idioms.

### 6. TECHNICAL VERIFICATION
- Build the backend project (e.g. `npm run build`, `cargo build`, `go build`, `mvn compile`).
- Run the local unit or integration tests (e.g. `npm test`, `go test`, `pytest`).
- Re-run the reproducing `curl` command. Check that status codes and output now conform.
- **verify:** local tests are green, and the specific curl reproduction yields the expected valid behavior.

### 7. REVALIDATE & CLOSE
- Update the findings log status to `fixed`.
- Record the minimal patch details and the exact verification command used.
- Reflect on any systemic improvements or reusable code helpers that can be extracted.

## Guardrails
- **Destructive operations**: Never drop databases, delete tables, or clear cache stores without explicit confirmation from the user.
- **Contract Safety**: Do not modify external contract definitions (RPC, GraphQL, public webhooks) that would break upstream services. Focus fixes on endpoint validation or HTTP-level sanitation.
- **Stack Agnostic**: Apply correct patterns matching the stack used (e.g. proper Go middleware, Express error handler, Spring boot `@RestControllerAdvice`, NestJS pipes).
