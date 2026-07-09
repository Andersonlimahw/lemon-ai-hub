---
name: Power and Performance
description: Endpoints for fetching diagnostic signatures and performance metrics.
---

# Power and Performance
Endpoints for fetching diagnostic signatures and performance metrics.

## Endpoints

### `GET /v1/diagnosticSignatures/{id}/logs`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

## Typical Workflows
Use these endpoints to automate power and performance tasks within Apple Store Connect.

## Best Practices
- Always authenticate requests using your Apple Store Connect API key (JWT token).
- Handle rate limiting gracefully, as the Apple Store Connect API enforces quotas.
- When writing integrations, refer back to the exact schemas for precise payload construction.