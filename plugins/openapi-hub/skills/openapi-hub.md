---
name: openapi-hub
description: OpenAPI spec versioning, breaking change detection, and SDK publishing. Tracks spec versions, blocks PRs that introduce breaking API changes without a major version bump, and auto-publishes updated docs. Use when managing a public API, releasing a new API version, or detecting breaking changes in a PR.
---

# OpenAPI Hub Plugin

Spec versioning + breaking change gates + SDK publishing.

## Commands

```
/openapi-hub validate          — validate openapi.yaml against OpenAPI 3.1
/openapi-hub diff v1 v2        — detect breaking changes between versions
/openapi-hub publish           — publish docs to Redoc / GitHub Pages
/openapi-hub sdk ts            — regenerate TypeScript SDK from current spec
/openapi-hub changelog         — auto-generate API changelog from spec diff
/openapi-hub mock-server       — start Prism mock server from spec
```

## Breaking Change Detection

```
BREAKING CHANGES — v3.3.0 → v3.4.0
=====================================
❌ 2 breaking changes detected (requires major version bump)

  [BREAK] GET /products/{id} — removed field 'legacyId' from response
          → Clients depending on legacyId will break silently
          → Add to deprecated fields list and keep for v4.0.0

  [BREAK] POST /orders — 'couponCode' now required (was optional)
          → Clients not sending couponCode will get 422
          → Make it optional again OR bump to v4.0.0

⚠️ 3 non-breaking changes (safe to ship in v3.4.0)
  [ADD] GET /products — new optional query param 'featured'
  [ADD] User schema — new optional field 'avatarUrl'
  [DEP] POST /v1/auth/login — deprecated, use POST /v2/auth/login
```

## Spec Versioning

```
specs/
  openapi.yaml          ← current (auto-symlink to latest)
  openapi-v3.4.0.yaml
  openapi-v3.3.0.yaml
  openapi-v3.2.0.yaml
```

## CI Gate

```yaml
- name: Detect breaking API changes
  run: npx @redocly/cli lint openapi.yaml && npx oasdiff openapi-v3.3.0.yaml openapi.yaml --fail-on-breaking
```

Pairs with `/openapi-generate` skill for spec generation.
