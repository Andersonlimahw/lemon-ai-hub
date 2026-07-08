# 🔄 API Test Loop Plugin

**Repeatable, agent-driven testing loop that validates backend REST APIs via CURL and ships verified security, reliability, and design fixes.**

This plugin translates manual endpoint testing into a repeatable, structured **API Validation Loop**. Rather than navigating through a UI, this loop interacts directly with backend endpoints using HTTP requests (`curl`), verifying RESTful best practices, validating input/output schemas, checking for security vulnerabilities, and applying surgical backend fixes.

## 🌟 Overview

- **API Validator (`@api-validator`)**: Probes endpoints, validates input constraints, reviews error formats, scans for security gaps, checks performance headers, and logs issues into a unified `findings.md` file.
- **API Fix Implementer (`@api-fix-implementer`)**: Applies minimal, surgical patches to routes, controllers, middleware, or validation schemas to address findings.
- **Loop Skill (`api-test-loop`)**: Guides the 7-phase validation cycle.
- **Invariants**: No iteration is complete without passing validation checks, ensuring Zero-Regression backend upgrades.

## 🚀 Installation

```bash
# In the root of your lemon-ai-hub workspace:
./plugins/api-test-loop/scripts/install.sh
```

## 🛠️ How to Use (Examples)

Mention the appropriate agent or trigger the skill in your prompt:

> **"Valide as APIs de autenticação e registro de usuários do projeto local usando o api-test-loop."**
> *(The orchestrator triggers `@api-validator` to inspect the routes/controllers, execute probing curls, and write findings to `docs/test-plans/api-test-loop/findings.md`)*

> **"Implemente correções para as brechas de segurança listadas no findings de API."**
> *(The orchestrator triggers `@api-fix-implementer` to edit backend controllers/middleware to fix validation constraints or missing authorization guards)*

## 🏗️ 7-Phase Loop Process

1. **Discovery & Spec Scan**: Locate the backend codebase, route registries, schemas, and OpenAPI/Swagger documentation.
2. **PLAN**: Outline the endpoints to test, target inputs, boundaries, and validation scenarios.
3. **PROBE (IMPLEMENT)**: Run `curl` commands to test the endpoints with valid, boundary, and malicious payloads.
4. **AUDIT & LOG**: Review responses. Verify HTTP methods, status codes, error payload format, security headers, rate limiting, and performance. Save findings to `findings.md`.
5. **FIX (GATE)**: Apply minimal, surgical corrections directly targeting the root cause of the findings.
6. **VERIFY**: Run backend tests (`npm run test`, `cargo test`, `go test`, etc.) and re-execute target `curl` probes to confirm the fix.
7. **REFLECT**: Log findings as `fixed`, update the iteration log, and commit Conventional Commits atomically.

## 📐 RESTful & Security Invariants Checked

- **Path & Method**: Proper noun-based paths, correct HTTP verbs (GET, POST, PUT, DELETE, PATCH).
- **Validation Gates**: Correct status codes (400 Bad Request for bad inputs instead of 500 Internal Server Error).
- **Output Formats**: Standardized JSON response envelopes and readable error structures.
- **Security Guardrails**: Protection against IDOR (Insecure Direct Object Reference), Auth bypass, SQL injection, missing rate limiting, CORS misconfigurations, and sensitive data leakage.
- **Performance Constraints**: Low response latency, proper usage of headers (e.g. Cache-Control, ETag).
