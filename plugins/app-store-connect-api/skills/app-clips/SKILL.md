---
name: App Clips
description: Endpoints for managing App Clips and default experiences.
---

# App Clips
Endpoints for managing App Clips and default experiences.

## Endpoints

### `POST /v1/appClipAdvancedExperienceImages`
**Summary**: No summary provided.

### `GET /v1/appClipAdvancedExperienceImages/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[appClipAdvancedExperienceImages]` (query, optional): the fields to include for returned resources of type appClipAdvancedExperienceImages

### `PATCH /v1/appClipAdvancedExperienceImages/{id}`
**Summary**: No summary provided.

### `POST /v1/appClipAdvancedExperiences`
**Summary**: No summary provided.

### `GET /v1/appClipAdvancedExperiences/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[appClipAdvancedExperiences]` (query, optional): the fields to include for returned resources of type appClipAdvancedExperiences
- `fields[appClips]` (query, optional): the fields to include for returned resources of type appClips
- `fields[appClipAdvancedExperienceImages]` (query, optional): the fields to include for returned resources of type appClipAdvancedExperienceImages
- `fields[appClipAdvancedExperienceLocalizations]` (query, optional): the fields to include for returned resources of type appClipAdvancedExperienceLocalizations
- `include` (query, optional): comma-separated list of relationships to include
- `limit[localizations]` (query, optional): maximum number of related localizations returned (when they are included)

### `PATCH /v1/appClipAdvancedExperiences/{id}`
**Summary**: No summary provided.

### `POST /v1/appClipAppStoreReviewDetails`
**Summary**: No summary provided.

### `GET /v1/appClipAppStoreReviewDetails/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[appClipAppStoreReviewDetails]` (query, optional): the fields to include for returned resources of type appClipAppStoreReviewDetails
- `fields[appClipDefaultExperiences]` (query, optional): the fields to include for returned resources of type appClipDefaultExperiences
- `include` (query, optional): comma-separated list of relationships to include

### `PATCH /v1/appClipAppStoreReviewDetails/{id}`
**Summary**: No summary provided.

### `POST /v1/appClipDefaultExperienceLocalizations`
**Summary**: No summary provided.

### `GET /v1/appClipDefaultExperienceLocalizations/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[appClipDefaultExperienceLocalizations]` (query, optional): the fields to include for returned resources of type appClipDefaultExperienceLocalizations
- `fields[appClipDefaultExperiences]` (query, optional): the fields to include for returned resources of type appClipDefaultExperiences
- `fields[appClipHeaderImages]` (query, optional): the fields to include for returned resources of type appClipHeaderImages
- `include` (query, optional): comma-separated list of relationships to include

### `PATCH /v1/appClipDefaultExperienceLocalizations/{id}`
**Summary**: No summary provided.

### `DELETE /v1/appClipDefaultExperienceLocalizations/{id}`
**Summary**: No summary provided.

### `POST /v1/appClipDefaultExperiences`
**Summary**: No summary provided.

### `GET /v1/appClipDefaultExperiences/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[appClipDefaultExperiences]` (query, optional): the fields to include for returned resources of type appClipDefaultExperiences
- `fields[appClips]` (query, optional): the fields to include for returned resources of type appClips
- `fields[appStoreVersions]` (query, optional): the fields to include for returned resources of type appStoreVersions
- `fields[appClipDefaultExperienceLocalizations]` (query, optional): the fields to include for returned resources of type appClipDefaultExperienceLocalizations
- `fields[appClipAppStoreReviewDetails]` (query, optional): the fields to include for returned resources of type appClipAppStoreReviewDetails
- `include` (query, optional): comma-separated list of relationships to include
- `limit[appClipDefaultExperienceLocalizations]` (query, optional): maximum number of related appClipDefaultExperienceLocalizations returned (when they are included)

### `PATCH /v1/appClipDefaultExperiences/{id}`
**Summary**: No summary provided.

### `DELETE /v1/appClipDefaultExperiences/{id}`
**Summary**: No summary provided.

### `POST /v1/appClipHeaderImages`
**Summary**: No summary provided.

### `GET /v1/appClipHeaderImages/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[appClipHeaderImages]` (query, optional): the fields to include for returned resources of type appClipHeaderImages
- `fields[appClipDefaultExperienceLocalizations]` (query, optional): the fields to include for returned resources of type appClipDefaultExperienceLocalizations
- `include` (query, optional): comma-separated list of relationships to include

### `PATCH /v1/appClipHeaderImages/{id}`
**Summary**: No summary provided.

### `DELETE /v1/appClipHeaderImages/{id}`
**Summary**: No summary provided.

### `GET /v1/appClips/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[appClips]` (query, optional): the fields to include for returned resources of type appClips
- `fields[apps]` (query, optional): the fields to include for returned resources of type apps
- `fields[appClipDefaultExperiences]` (query, optional): the fields to include for returned resources of type appClipDefaultExperiences
- `include` (query, optional): comma-separated list of relationships to include
- `limit[appClipDefaultExperiences]` (query, optional): maximum number of related appClipDefaultExperiences returned (when they are included)

### `GET /v1/appClipDefaultExperienceLocalizations/{id}/relationships/appClipHeaderImage`
**Summary**: No summary provided.

### `GET /v1/appClipDefaultExperienceLocalizations/{id}/appClipHeaderImage`
**Summary**: No summary provided.

**Parameters**:
- `fields[appClipHeaderImages]` (query, optional): the fields to include for returned resources of type appClipHeaderImages
- `fields[appClipDefaultExperienceLocalizations]` (query, optional): the fields to include for returned resources of type appClipDefaultExperienceLocalizations
- `include` (query, optional): comma-separated list of relationships to include

### `GET /v1/appClipDefaultExperiences/{id}/relationships/appClipAppStoreReviewDetail`
**Summary**: No summary provided.

### `GET /v1/appClipDefaultExperiences/{id}/appClipAppStoreReviewDetail`
**Summary**: No summary provided.

**Parameters**:
- `fields[appClipAppStoreReviewDetails]` (query, optional): the fields to include for returned resources of type appClipAppStoreReviewDetails
- `fields[appClipDefaultExperiences]` (query, optional): the fields to include for returned resources of type appClipDefaultExperiences
- `include` (query, optional): comma-separated list of relationships to include

### `GET /v1/appClipDefaultExperiences/{id}/relationships/appClipDefaultExperienceLocalizations`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/appClipDefaultExperiences/{id}/appClipDefaultExperienceLocalizations`
**Summary**: No summary provided.

**Parameters**:
- `filter[locale]` (query, optional): filter by attribute 'locale'
- `fields[appClipDefaultExperienceLocalizations]` (query, optional): the fields to include for returned resources of type appClipDefaultExperienceLocalizations
- `fields[appClipDefaultExperiences]` (query, optional): the fields to include for returned resources of type appClipDefaultExperiences
- `fields[appClipHeaderImages]` (query, optional): the fields to include for returned resources of type appClipHeaderImages
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include

### `GET /v1/appClipDefaultExperiences/{id}/relationships/releaseWithAppStoreVersion`
**Summary**: No summary provided.

### `PATCH /v1/appClipDefaultExperiences/{id}/relationships/releaseWithAppStoreVersion`
**Summary**: No summary provided.

### `GET /v1/appClipDefaultExperiences/{id}/releaseWithAppStoreVersion`
**Summary**: No summary provided.

**Parameters**:
- `fields[appStoreVersions]` (query, optional): the fields to include for returned resources of type appStoreVersions
- `fields[apps]` (query, optional): the fields to include for returned resources of type apps
- `fields[appStoreVersionLocalizations]` (query, optional): the fields to include for returned resources of type appStoreVersionLocalizations
- `fields[builds]` (query, optional): the fields to include for returned resources of type builds
- `fields[appStoreVersionPhasedReleases]` (query, optional): the fields to include for returned resources of type appStoreVersionPhasedReleases
- `fields[gameCenterAppVersions]` (query, optional): the fields to include for returned resources of type gameCenterAppVersions
- `fields[routingAppCoverages]` (query, optional): the fields to include for returned resources of type routingAppCoverages
- `fields[appStoreReviewDetails]` (query, optional): the fields to include for returned resources of type appStoreReviewDetails
- `fields[appStoreVersionSubmissions]` (query, optional): the fields to include for returned resources of type appStoreVersionSubmissions
- `fields[appClipDefaultExperiences]` (query, optional): the fields to include for returned resources of type appClipDefaultExperiences
- `fields[appStoreVersionExperiments]` (query, optional): the fields to include for returned resources of type appStoreVersionExperiments
- `fields[alternativeDistributionPackages]` (query, optional): the fields to include for returned resources of type alternativeDistributionPackages
- `include` (query, optional): comma-separated list of relationships to include
- `limit[appStoreVersionLocalizations]` (query, optional): maximum number of related appStoreVersionLocalizations returned (when they are included)
- `limit[appStoreVersionExperiments]` (query, optional): maximum number of related appStoreVersionExperiments returned (when they are included)
- `limit[appStoreVersionExperimentsV2]` (query, optional): maximum number of related appStoreVersionExperimentsV2 returned (when they are included)

### `GET /v1/appClips/{id}/relationships/appClipAdvancedExperiences`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/appClips/{id}/appClipAdvancedExperiences`
**Summary**: No summary provided.

**Parameters**:
- `filter[status]` (query, optional): filter by attribute 'status'
- `filter[placeStatus]` (query, optional): filter by attribute 'placeStatus'
- `filter[action]` (query, optional): filter by attribute 'action'
- `fields[appClipAdvancedExperiences]` (query, optional): the fields to include for returned resources of type appClipAdvancedExperiences
- `fields[appClips]` (query, optional): the fields to include for returned resources of type appClips
- `fields[appClipAdvancedExperienceImages]` (query, optional): the fields to include for returned resources of type appClipAdvancedExperienceImages
- `fields[appClipAdvancedExperienceLocalizations]` (query, optional): the fields to include for returned resources of type appClipAdvancedExperienceLocalizations
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[localizations]` (query, optional): maximum number of related localizations returned (when they are included)

### `GET /v1/appClips/{id}/relationships/appClipDefaultExperiences`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/appClips/{id}/appClipDefaultExperiences`
**Summary**: No summary provided.

**Parameters**:
- `exists[releaseWithAppStoreVersion]` (query, optional): filter by existence or non-existence of related 'releaseWithAppStoreVersion'
- `fields[appClipDefaultExperiences]` (query, optional): the fields to include for returned resources of type appClipDefaultExperiences
- `fields[appClips]` (query, optional): the fields to include for returned resources of type appClips
- `fields[appStoreVersions]` (query, optional): the fields to include for returned resources of type appStoreVersions
- `fields[appClipDefaultExperienceLocalizations]` (query, optional): the fields to include for returned resources of type appClipDefaultExperienceLocalizations
- `fields[appClipAppStoreReviewDetails]` (query, optional): the fields to include for returned resources of type appClipAppStoreReviewDetails
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[appClipDefaultExperienceLocalizations]` (query, optional): maximum number of related appClipDefaultExperienceLocalizations returned (when they are included)

## Typical Workflows
Use these endpoints to automate app clips tasks within Apple Store Connect.

## Best Practices
- Always authenticate requests using your Apple Store Connect API key (JWT token).
- Handle rate limiting gracefully, as the Apple Store Connect API enforces quotas.
- When writing integrations, refer back to the exact schemas for precise payload construction.