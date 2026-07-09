---
name: Analytics
description: Endpoints for app analytics and performance reports.
---

# Analytics
Endpoints for app analytics and performance reports.

## Endpoints

### `GET /v1/analyticsReportInstances/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[analyticsReportInstances]` (query, optional): the fields to include for returned resources of type analyticsReportInstances

### `POST /v1/analyticsReportRequests`
**Summary**: No summary provided.

### `GET /v1/analyticsReportRequests/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[analyticsReportRequests]` (query, optional): the fields to include for returned resources of type analyticsReportRequests
- `fields[analyticsReports]` (query, optional): the fields to include for returned resources of type analyticsReports
- `include` (query, optional): comma-separated list of relationships to include
- `limit[reports]` (query, optional): maximum number of related reports returned (when they are included)

### `DELETE /v1/analyticsReportRequests/{id}`
**Summary**: No summary provided.

### `GET /v1/analyticsReportSegments/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[analyticsReportSegments]` (query, optional): the fields to include for returned resources of type analyticsReportSegments

### `GET /v1/analyticsReports/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[analyticsReports]` (query, optional): the fields to include for returned resources of type analyticsReports

### `GET /v1/analyticsReportInstances/{id}/relationships/segments`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/analyticsReportInstances/{id}/segments`
**Summary**: No summary provided.

**Parameters**:
- `fields[analyticsReportSegments]` (query, optional): the fields to include for returned resources of type analyticsReportSegments
- `limit` (query, optional): maximum resources per page

### `GET /v1/analyticsReportRequests/{id}/relationships/reports`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/analyticsReportRequests/{id}/reports`
**Summary**: No summary provided.

**Parameters**:
- `filter[name]` (query, optional): filter by attribute 'name'
- `filter[category]` (query, optional): filter by attribute 'category'
- `fields[analyticsReports]` (query, optional): the fields to include for returned resources of type analyticsReports
- `limit` (query, optional): maximum resources per page

### `GET /v1/analyticsReports/{id}/relationships/instances`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/analyticsReports/{id}/instances`
**Summary**: No summary provided.

**Parameters**:
- `filter[granularity]` (query, optional): filter by attribute 'granularity'
- `filter[processingDate]` (query, optional): filter by attribute 'processingDate'
- `fields[analyticsReportInstances]` (query, optional): the fields to include for returned resources of type analyticsReportInstances
- `limit` (query, optional): maximum resources per page

## Typical Workflows
Use these endpoints to automate analytics tasks within Apple Store Connect.

## Best Practices
- Always authenticate requests using your Apple Store Connect API key (JWT token).
- Handle rate limiting gracefully, as the Apple Store Connect API enforces quotas.
- When writing integrations, refer back to the exact schemas for precise payload construction.