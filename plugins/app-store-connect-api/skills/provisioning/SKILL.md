---
name: Provisioning
description: Endpoints for managing certificates, devices, profiles, and bundle IDs.
---

# Provisioning
Endpoints for managing certificates, devices, profiles, and bundle IDs.

## Endpoints

### `GET /v1/bundleIds`
**Summary**: No summary provided.

**Parameters**:
- `filter[name]` (query, optional): filter by attribute 'name'
- `filter[platform]` (query, optional): filter by attribute 'platform'
- `filter[identifier]` (query, optional): filter by attribute 'identifier'
- `filter[seedId]` (query, optional): filter by attribute 'seedId'
- `filter[id]` (query, optional): filter by id(s)
- `sort` (query, optional): comma-separated list of sort expressions; resources will be sorted as specified
- `fields[bundleIds]` (query, optional): the fields to include for returned resources of type bundleIds
- `fields[profiles]` (query, optional): the fields to include for returned resources of type profiles
- `fields[bundleIdCapabilities]` (query, optional): the fields to include for returned resources of type bundleIdCapabilities
- `fields[apps]` (query, optional): the fields to include for returned resources of type apps
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[bundleIdCapabilities]` (query, optional): maximum number of related bundleIdCapabilities returned (when they are included)
- `limit[profiles]` (query, optional): maximum number of related profiles returned (when they are included)

### `POST /v1/bundleIds`
**Summary**: No summary provided.

### `GET /v1/bundleIds/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[bundleIds]` (query, optional): the fields to include for returned resources of type bundleIds
- `fields[profiles]` (query, optional): the fields to include for returned resources of type profiles
- `fields[bundleIdCapabilities]` (query, optional): the fields to include for returned resources of type bundleIdCapabilities
- `fields[apps]` (query, optional): the fields to include for returned resources of type apps
- `include` (query, optional): comma-separated list of relationships to include
- `limit[bundleIdCapabilities]` (query, optional): maximum number of related bundleIdCapabilities returned (when they are included)
- `limit[profiles]` (query, optional): maximum number of related profiles returned (when they are included)

### `PATCH /v1/bundleIds/{id}`
**Summary**: No summary provided.

### `DELETE /v1/bundleIds/{id}`
**Summary**: No summary provided.

### `GET /v1/certificates`
**Summary**: No summary provided.

**Parameters**:
- `filter[displayName]` (query, optional): filter by attribute 'displayName'
- `filter[certificateType]` (query, optional): filter by attribute 'certificateType'
- `filter[serialNumber]` (query, optional): filter by attribute 'serialNumber'
- `filter[id]` (query, optional): filter by id(s)
- `sort` (query, optional): comma-separated list of sort expressions; resources will be sorted as specified
- `fields[certificates]` (query, optional): the fields to include for returned resources of type certificates
- `fields[passTypeIds]` (query, optional): the fields to include for returned resources of type passTypeIds
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include

### `POST /v1/certificates`
**Summary**: No summary provided.

### `GET /v1/certificates/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[certificates]` (query, optional): the fields to include for returned resources of type certificates
- `fields[passTypeIds]` (query, optional): the fields to include for returned resources of type passTypeIds
- `include` (query, optional): comma-separated list of relationships to include

### `PATCH /v1/certificates/{id}`
**Summary**: No summary provided.

### `DELETE /v1/certificates/{id}`
**Summary**: No summary provided.

### `GET /v1/devices`
**Summary**: No summary provided.

**Parameters**:
- `filter[name]` (query, optional): filter by attribute 'name'
- `filter[platform]` (query, optional): filter by attribute 'platform'
- `filter[udid]` (query, optional): filter by attribute 'udid'
- `filter[status]` (query, optional): filter by attribute 'status'
- `filter[id]` (query, optional): filter by id(s)
- `sort` (query, optional): comma-separated list of sort expressions; resources will be sorted as specified
- `fields[devices]` (query, optional): the fields to include for returned resources of type devices
- `limit` (query, optional): maximum resources per page

### `POST /v1/devices`
**Summary**: No summary provided.

### `GET /v1/devices/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[devices]` (query, optional): the fields to include for returned resources of type devices

### `PATCH /v1/devices/{id}`
**Summary**: No summary provided.

### `GET /v1/profiles`
**Summary**: No summary provided.

**Parameters**:
- `filter[name]` (query, optional): filter by attribute 'name'
- `filter[profileType]` (query, optional): filter by attribute 'profileType'
- `filter[profileState]` (query, optional): filter by attribute 'profileState'
- `filter[id]` (query, optional): filter by id(s)
- `sort` (query, optional): comma-separated list of sort expressions; resources will be sorted as specified
- `fields[profiles]` (query, optional): the fields to include for returned resources of type profiles
- `fields[bundleIds]` (query, optional): the fields to include for returned resources of type bundleIds
- `fields[devices]` (query, optional): the fields to include for returned resources of type devices
- `fields[certificates]` (query, optional): the fields to include for returned resources of type certificates
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[certificates]` (query, optional): maximum number of related certificates returned (when they are included)
- `limit[devices]` (query, optional): maximum number of related devices returned (when they are included)

### `POST /v1/profiles`
**Summary**: No summary provided.

### `GET /v1/profiles/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[profiles]` (query, optional): the fields to include for returned resources of type profiles
- `fields[bundleIds]` (query, optional): the fields to include for returned resources of type bundleIds
- `fields[devices]` (query, optional): the fields to include for returned resources of type devices
- `fields[certificates]` (query, optional): the fields to include for returned resources of type certificates
- `include` (query, optional): comma-separated list of relationships to include
- `limit[certificates]` (query, optional): maximum number of related certificates returned (when they are included)
- `limit[devices]` (query, optional): maximum number of related devices returned (when they are included)

### `DELETE /v1/profiles/{id}`
**Summary**: No summary provided.

### `GET /v1/bundleIds/{id}/relationships/app`
**Summary**: No summary provided.

### `GET /v1/bundleIds/{id}/app`
**Summary**: No summary provided.

**Parameters**:
- `fields[apps]` (query, optional): the fields to include for returned resources of type apps

### `GET /v1/bundleIds/{id}/relationships/bundleIdCapabilities`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/bundleIds/{id}/bundleIdCapabilities`
**Summary**: No summary provided.

**Parameters**:
- `fields[bundleIdCapabilities]` (query, optional): the fields to include for returned resources of type bundleIdCapabilities
- `limit` (query, optional): maximum resources per page

### `GET /v1/bundleIds/{id}/relationships/profiles`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/bundleIds/{id}/profiles`
**Summary**: No summary provided.

**Parameters**:
- `fields[profiles]` (query, optional): the fields to include for returned resources of type profiles
- `limit` (query, optional): maximum resources per page

### `GET /v1/certificates/{id}/relationships/passTypeId`
**Summary**: No summary provided.

### `GET /v1/certificates/{id}/passTypeId`
**Summary**: No summary provided.

**Parameters**:
- `fields[passTypeIds]` (query, optional): the fields to include for returned resources of type passTypeIds
- `fields[certificates]` (query, optional): the fields to include for returned resources of type certificates
- `include` (query, optional): comma-separated list of relationships to include
- `limit[certificates]` (query, optional): maximum number of related certificates returned (when they are included)

### `GET /v1/profiles/{id}/relationships/bundleId`
**Summary**: No summary provided.

### `GET /v1/profiles/{id}/bundleId`
**Summary**: No summary provided.

**Parameters**:
- `fields[bundleIds]` (query, optional): the fields to include for returned resources of type bundleIds

### `GET /v1/profiles/{id}/relationships/certificates`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/profiles/{id}/certificates`
**Summary**: No summary provided.

**Parameters**:
- `fields[certificates]` (query, optional): the fields to include for returned resources of type certificates
- `limit` (query, optional): maximum resources per page

### `GET /v1/profiles/{id}/relationships/devices`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/profiles/{id}/devices`
**Summary**: No summary provided.

**Parameters**:
- `fields[devices]` (query, optional): the fields to include for returned resources of type devices
- `limit` (query, optional): maximum resources per page

## Typical Workflows
Use these endpoints to automate provisioning tasks within Apple Store Connect.

## Best Practices
- Always authenticate requests using your Apple Store Connect API key (JWT token).
- Handle rate limiting gracefully, as the Apple Store Connect API enforces quotas.
- When writing integrations, refer back to the exact schemas for precise payload construction.