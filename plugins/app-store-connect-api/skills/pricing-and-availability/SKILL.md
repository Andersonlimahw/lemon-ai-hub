---
name: Pricing and Availability
description: Endpoints for app price schedules and territories.
---

# Pricing and Availability
Endpoints for app price schedules and territories.

## Endpoints

### `POST /v1/appPriceSchedules`
**Summary**: No summary provided.

### `GET /v1/appPriceSchedules/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[appPriceSchedules]` (query, optional): the fields to include for returned resources of type appPriceSchedules
- `fields[apps]` (query, optional): the fields to include for returned resources of type apps
- `fields[territories]` (query, optional): the fields to include for returned resources of type territories
- `fields[appPrices]` (query, optional): the fields to include for returned resources of type appPrices
- `include` (query, optional): comma-separated list of relationships to include
- `limit[automaticPrices]` (query, optional): maximum number of related automaticPrices returned (when they are included)
- `limit[manualPrices]` (query, optional): maximum number of related manualPrices returned (when they are included)

### `GET /v1/territories`
**Summary**: No summary provided.

**Parameters**:
- `fields[territories]` (query, optional): the fields to include for returned resources of type territories
- `limit` (query, optional): maximum resources per page

### `GET /v1/appPriceSchedules/{id}/relationships/automaticPrices`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/appPriceSchedules/{id}/automaticPrices`
**Summary**: No summary provided.

**Parameters**:
- `filter[startDate]` (query, optional): filter by attribute 'startDate'
- `filter[endDate]` (query, optional): filter by attribute 'endDate'
- `filter[territory]` (query, optional): filter by id(s) of related 'territory'
- `fields[appPrices]` (query, optional): the fields to include for returned resources of type appPrices
- `fields[appPricePoints]` (query, optional): the fields to include for returned resources of type appPricePoints
- `fields[territories]` (query, optional): the fields to include for returned resources of type territories
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include

### `GET /v1/appPriceSchedules/{id}/relationships/baseTerritory`
**Summary**: No summary provided.

### `GET /v1/appPriceSchedules/{id}/baseTerritory`
**Summary**: No summary provided.

**Parameters**:
- `fields[territories]` (query, optional): the fields to include for returned resources of type territories

### `GET /v1/appPriceSchedules/{id}/relationships/manualPrices`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/appPriceSchedules/{id}/manualPrices`
**Summary**: No summary provided.

**Parameters**:
- `filter[startDate]` (query, optional): filter by attribute 'startDate'
- `filter[endDate]` (query, optional): filter by attribute 'endDate'
- `filter[territory]` (query, optional): filter by id(s) of related 'territory'
- `fields[appPrices]` (query, optional): the fields to include for returned resources of type appPrices
- `fields[appPricePoints]` (query, optional): the fields to include for returned resources of type appPricePoints
- `fields[territories]` (query, optional): the fields to include for returned resources of type territories
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include

## Typical Workflows
Use these endpoints to automate pricing and availability tasks within Apple Store Connect.

## Best Practices
- Always authenticate requests using your Apple Store Connect API key (JWT token).
- Handle rate limiting gracefully, as the Apple Store Connect API enforces quotas.
- When writing integrations, refer back to the exact schemas for precise payload construction.