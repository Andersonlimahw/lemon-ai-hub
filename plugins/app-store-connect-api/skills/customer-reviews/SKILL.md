---
name: Customer Reviews
description: Endpoints for reading and responding to customer reviews.
---

# Customer Reviews
Endpoints for reading and responding to customer reviews.

## Endpoints

### `POST /v1/customerReviewResponses`
**Summary**: No summary provided.

### `GET /v1/customerReviewResponses/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[customerReviewResponses]` (query, optional): the fields to include for returned resources of type customerReviewResponses
- `fields[customerReviews]` (query, optional): the fields to include for returned resources of type customerReviews
- `include` (query, optional): comma-separated list of relationships to include

### `DELETE /v1/customerReviewResponses/{id}`
**Summary**: No summary provided.

### `GET /v1/customerReviews/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[customerReviews]` (query, optional): the fields to include for returned resources of type customerReviews
- `fields[customerReviewResponses]` (query, optional): the fields to include for returned resources of type customerReviewResponses
- `fields[territories]` (query, optional): the fields to include for returned resources of type territories
- `include` (query, optional): comma-separated list of relationships to include

### `GET /v1/customerReviews/{id}/relationships/response`
**Summary**: No summary provided.

### `GET /v1/customerReviews/{id}/response`
**Summary**: No summary provided.

**Parameters**:
- `fields[customerReviewResponses]` (query, optional): the fields to include for returned resources of type customerReviewResponses
- `fields[customerReviews]` (query, optional): the fields to include for returned resources of type customerReviews
- `include` (query, optional): comma-separated list of relationships to include

## Typical Workflows
Use these endpoints to automate customer reviews tasks within Apple Store Connect.

## Best Practices
- Always authenticate requests using your Apple Store Connect API key (JWT token).
- Handle rate limiting gracefully, as the Apple Store Connect API enforces quotas.
- When writing integrations, refer back to the exact schemas for precise payload construction.