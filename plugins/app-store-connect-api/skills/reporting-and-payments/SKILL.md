---
name: Reporting, Payments and Financial Reports
description: Endpoints for downloading sales and financial reports.
---

# Reporting, Payments and Financial Reports
Endpoints for downloading sales and financial reports.

## Endpoints

### `GET /v1/financeReports`
**Summary**: No summary provided.

**Parameters**:
- `filter[vendorNumber]` (query, required): filter by attribute 'vendorNumber'
- `filter[reportType]` (query, required): filter by attribute 'reportType'
- `filter[regionCode]` (query, required): filter by attribute 'regionCode'
- `filter[reportDate]` (query, required): filter by attribute 'reportDate'

### `GET /v1/salesReports`
**Summary**: No summary provided.

**Parameters**:
- `filter[vendorNumber]` (query, required): filter by attribute 'vendorNumber'
- `filter[reportType]` (query, required): filter by attribute 'reportType'
- `filter[reportSubType]` (query, required): filter by attribute 'reportSubType'
- `filter[frequency]` (query, required): filter by attribute 'frequency'
- `filter[reportDate]` (query, optional): filter by attribute 'reportDate'
- `filter[version]` (query, optional): filter by attribute 'version'

## Typical Workflows
Use these endpoints to automate reporting, payments and financial reports tasks within Apple Store Connect.

## Best Practices
- Always authenticate requests using your Apple Store Connect API key (JWT token).
- Handle rate limiting gracefully, as the Apple Store Connect API enforces quotas.
- When writing integrations, refer back to the exact schemas for precise payload construction.