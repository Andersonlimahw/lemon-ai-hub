---
name: openapi-generate
description: Generate OpenAPI 3.1 specs from existing code (routes, controllers, types, Zod/Joi schemas), or generate code from an existing spec. Produces valid openapi.yaml, typed client SDKs, mock servers, and Postman collections. Use when documenting an API, onboarding clients, generating typed SDKs, or migrating to spec-first development.
---

# OpenAPI Generate

Code → spec → SDK → mocks. Full API documentation lifecycle.

## Quick Start

```
/openapi-generate                    — generate spec from codebase routes
/openapi-generate --from spec        — generate code/SDK from openapi.yaml
/openapi-generate --sdk typescript   — generate TypeScript client SDK
/openapi-generate --mock             — generate mock server from spec
/openapi-generate --postman          — export Postman collection
/openapi-generate --validate         — validate existing openapi.yaml
```

## Directions

### Code → Spec (most common)
Claude reads your route files, controllers, and type definitions, then produces a complete `openapi.yaml`.

### Spec → Code (spec-first)
Claude reads an existing `openapi.yaml` and generates:
- TypeScript types / Zod schemas
- Route handlers (Express / Fastify / NestJS / Next.js)
- Typed client SDK
- Test fixtures

## Workflow — Code to Spec

Claude will:
1. Discover route files (Express `router.get`, NestJS `@Get`, Next.js `route.ts`, etc.)
2. Extract path params, query params, request body, response shapes
3. Infer types from TypeScript / Zod / Joi / Prisma schema
4. Generate `openapi.yaml` with examples
5. Add `$ref` components to avoid duplication
6. Validate with `@redocly/cli lint`

## Generated Spec Example

```yaml
openapi: 3.1.0
info:
  title: Products API
  version: 1.0.0

paths:
  /products:
    get:
      summary: List products
      operationId: listProducts
      parameters:
        - name: category
          in: query
          schema:
            type: string
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProductList'
        '400':
          $ref: '#/components/responses/BadRequest'

  /products/{id}:
    get:
      summary: Get product by ID
      operationId: getProduct
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Product'
        '404':
          $ref: '#/components/responses/NotFound'

components:
  schemas:
    Product:
      type: object
      required: [id, name, price]
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
        price:
          type: number
          format: float
        category:
          type: string
```

## SDK Generation

```bash
# TypeScript (via openapi-typescript)
/openapi-generate --sdk typescript
# → generates: src/types/api.ts (fully typed)

# Typed fetch client (openapi-fetch)
/openapi-generate --sdk typescript-fetch
# → generates: src/lib/api-client.ts

# Python (via openapi-python-client)
/openapi-generate --sdk python
```

### TypeScript SDK Example

```typescript
import createClient from 'openapi-fetch'
import type { paths } from './types/api'

const client = createClient<paths>({ baseUrl: 'https://api.example.com' })

// Fully typed — autocomplete on params + response
const { data, error } = await client.GET('/products/{id}', {
  params: { path: { id: '123' } },
})
// data.name is typed as string
```

## Mock Server

```bash
/openapi-generate --mock
# Generates: mock-server/ (uses Prism)
# Run: npx @stoplight/prism-cli mock openapi.yaml
# → Serves realistic mocks from examples in spec
```

## Validation

```
OPENAPI VALIDATION — openapi.yaml
====================================
❌ 3 errors | ⚠️ 7 warnings

ERRORS
  [E1] /paths/~1orders~1{id}/put — requestBody is required but not defined
  [E2] /components/schemas/User — 'email' format should be 'email' not 'string'
  [E3] Missing operationId on GET /users

WARNINGS
  [W1] No examples defined for 5 schemas (reduces mock quality)
  [W2] Missing 401/403 responses on authenticated endpoints
```

## Frameworks Supported

| Framework | Route Discovery |
|-----------|----------------|
| Express / Fastify | `router.get/post/put/delete` |
| NestJS | `@Get`, `@Post`, `@Controller` decorators |
| Next.js App Router | `route.ts` export handlers |
| FastAPI (Python) | `@app.get`, `@app.post` |
| Django REST | ViewSet + `urlpatterns` |
| Hono | `app.get/post` |
