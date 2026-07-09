---
name: Users and Roles
description: Endpoints for managing App Store Connect users and invitations.
---

# Users and Roles
Endpoints for managing App Store Connect users and invitations.

## Endpoints

### `GET /v1/userInvitations`
**Summary**: No summary provided.

**Parameters**:
- `filter[email]` (query, optional): filter by attribute 'email'
- `filter[roles]` (query, optional): filter by attribute 'roles'
- `filter[visibleApps]` (query, optional): filter by id(s) of related 'visibleApps'
- `sort` (query, optional): comma-separated list of sort expressions; resources will be sorted as specified
- `fields[userInvitations]` (query, optional): the fields to include for returned resources of type userInvitations
- `fields[apps]` (query, optional): the fields to include for returned resources of type apps
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[visibleApps]` (query, optional): maximum number of related visibleApps returned (when they are included)

### `POST /v1/userInvitations`
**Summary**: No summary provided.

### `GET /v1/userInvitations/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[userInvitations]` (query, optional): the fields to include for returned resources of type userInvitations
- `fields[apps]` (query, optional): the fields to include for returned resources of type apps
- `include` (query, optional): comma-separated list of relationships to include
- `limit[visibleApps]` (query, optional): maximum number of related visibleApps returned (when they are included)

### `DELETE /v1/userInvitations/{id}`
**Summary**: No summary provided.

### `GET /v1/users`
**Summary**: No summary provided.

**Parameters**:
- `filter[username]` (query, optional): filter by attribute 'username'
- `filter[roles]` (query, optional): filter by attribute 'roles'
- `filter[visibleApps]` (query, optional): filter by id(s) of related 'visibleApps'
- `sort` (query, optional): comma-separated list of sort expressions; resources will be sorted as specified
- `fields[users]` (query, optional): the fields to include for returned resources of type users
- `fields[apps]` (query, optional): the fields to include for returned resources of type apps
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[visibleApps]` (query, optional): maximum number of related visibleApps returned (when they are included)

### `GET /v1/users/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[users]` (query, optional): the fields to include for returned resources of type users
- `fields[apps]` (query, optional): the fields to include for returned resources of type apps
- `include` (query, optional): comma-separated list of relationships to include
- `limit[visibleApps]` (query, optional): maximum number of related visibleApps returned (when they are included)

### `PATCH /v1/users/{id}`
**Summary**: No summary provided.

### `DELETE /v1/users/{id}`
**Summary**: No summary provided.

### `GET /v1/userInvitations/{id}/relationships/visibleApps`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/userInvitations/{id}/visibleApps`
**Summary**: No summary provided.

**Parameters**:
- `fields[apps]` (query, optional): the fields to include for returned resources of type apps
- `limit` (query, optional): maximum resources per page

### `GET /v1/users/{id}/relationships/visibleApps`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `POST /v1/users/{id}/relationships/visibleApps`
**Summary**: No summary provided.

### `PATCH /v1/users/{id}/relationships/visibleApps`
**Summary**: No summary provided.

### `DELETE /v1/users/{id}/relationships/visibleApps`
**Summary**: No summary provided.

### `GET /v1/users/{id}/visibleApps`
**Summary**: No summary provided.

**Parameters**:
- `fields[apps]` (query, optional): the fields to include for returned resources of type apps
- `limit` (query, optional): maximum resources per page

## Typical Workflows
Use these endpoints to automate users and roles tasks within Apple Store Connect.

## Best Practices
- Always authenticate requests using your Apple Store Connect API key (JWT token).
- Handle rate limiting gracefully, as the Apple Store Connect API enforces quotas.
- When writing integrations, refer back to the exact schemas for precise payload construction.