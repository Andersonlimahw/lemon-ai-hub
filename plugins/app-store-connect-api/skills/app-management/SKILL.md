---
name: App Management
description: Endpoints for managing apps, app infos, and app store versions in Apple Store Connect.
---

# App Management
Endpoints for managing apps, app infos, and app store versions in Apple Store Connect.

## Endpoints

### `GET /v1/appInfos/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[appInfos]` (query, optional): the fields to include for returned resources of type appInfos
- `fields[apps]` (query, optional): the fields to include for returned resources of type apps
- `fields[ageRatingDeclarations]` (query, optional): the fields to include for returned resources of type ageRatingDeclarations
- `fields[appInfoLocalizations]` (query, optional): the fields to include for returned resources of type appInfoLocalizations
- `fields[appCategories]` (query, optional): the fields to include for returned resources of type appCategories
- `include` (query, optional): comma-separated list of relationships to include
- `limit[appInfoLocalizations]` (query, optional): maximum number of related appInfoLocalizations returned (when they are included)

### `PATCH /v1/appInfos/{id}`
**Summary**: No summary provided.

### `POST /v1/appStoreVersions`
**Summary**: No summary provided.

### `GET /v1/appStoreVersions/{id}`
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
- `limit[appStoreVersionExperiments]` (query, optional): maximum number of related appStoreVersionExperiments returned (when they are included)
- `limit[appStoreVersionExperimentsV2]` (query, optional): maximum number of related appStoreVersionExperimentsV2 returned (when they are included)
- `limit[appStoreVersionLocalizations]` (query, optional): maximum number of related appStoreVersionLocalizations returned (when they are included)

### `PATCH /v1/appStoreVersions/{id}`
**Summary**: No summary provided.

### `DELETE /v1/appStoreVersions/{id}`
**Summary**: No summary provided.

### `GET /v1/apps`
**Summary**: No summary provided.

**Parameters**:
- `filter[name]` (query, optional): filter by attribute 'name'
- `filter[bundleId]` (query, optional): filter by attribute 'bundleId'
- `filter[sku]` (query, optional): filter by attribute 'sku'
- `filter[appStoreVersions.appStoreState]` (query, optional): filter by attribute 'appStoreVersions.appStoreState'
- `filter[appStoreVersions.platform]` (query, optional): filter by attribute 'appStoreVersions.platform'
- `filter[appStoreVersions.appVersionState]` (query, optional): filter by attribute 'appStoreVersions.appVersionState'
- `filter[reviewSubmissions.state]` (query, optional): filter by attribute 'reviewSubmissions.state'
- `filter[reviewSubmissions.platform]` (query, optional): filter by attribute 'reviewSubmissions.platform'
- `filter[appStoreVersions]` (query, optional): filter by id(s) of related 'appStoreVersions'
- `filter[id]` (query, optional): filter by id(s)
- `exists[gameCenterEnabledVersions]` (query, optional): filter by existence or non-existence of related 'gameCenterEnabledVersions'
- `sort` (query, optional): comma-separated list of sort expressions; resources will be sorted as specified
- `fields[apps]` (query, optional): the fields to include for returned resources of type apps
- `fields[appEncryptionDeclarations]` (query, optional): the fields to include for returned resources of type appEncryptionDeclarations
- `fields[buildIcons]` (query, optional): the fields to include for returned resources of type buildIcons
- `fields[ciProducts]` (query, optional): the fields to include for returned resources of type ciProducts
- `fields[betaGroups]` (query, optional): the fields to include for returned resources of type betaGroups
- `fields[appStoreVersions]` (query, optional): the fields to include for returned resources of type appStoreVersions
- `fields[preReleaseVersions]` (query, optional): the fields to include for returned resources of type preReleaseVersions
- `fields[betaAppLocalizations]` (query, optional): the fields to include for returned resources of type betaAppLocalizations
- `fields[builds]` (query, optional): the fields to include for returned resources of type builds
- `fields[betaLicenseAgreements]` (query, optional): the fields to include for returned resources of type betaLicenseAgreements
- `fields[betaAppReviewDetails]` (query, optional): the fields to include for returned resources of type betaAppReviewDetails
- `fields[appInfos]` (query, optional): the fields to include for returned resources of type appInfos
- `fields[appClips]` (query, optional): the fields to include for returned resources of type appClips
- `fields[endUserLicenseAgreements]` (query, optional): the fields to include for returned resources of type endUserLicenseAgreements
- `fields[inAppPurchases]` (query, optional): the fields to include for returned resources of type inAppPurchases
- `fields[subscriptionGroups]` (query, optional): the fields to include for returned resources of type subscriptionGroups
- `fields[gameCenterEnabledVersions]` (query, optional): the fields to include for returned resources of type gameCenterEnabledVersions
- `fields[appCustomProductPages]` (query, optional): the fields to include for returned resources of type appCustomProductPages
- `fields[promotedPurchases]` (query, optional): the fields to include for returned resources of type promotedPurchases
- `fields[appEvents]` (query, optional): the fields to include for returned resources of type appEvents
- `fields[reviewSubmissions]` (query, optional): the fields to include for returned resources of type reviewSubmissions
- `fields[subscriptionGracePeriods]` (query, optional): the fields to include for returned resources of type subscriptionGracePeriods
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[appStoreVersionExperiments]` (query, optional): the fields to include for returned resources of type appStoreVersionExperiments
- `fields[androidToIosAppMappingDetails]` (query, optional): the fields to include for returned resources of type androidToIosAppMappingDetails
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[androidToIosAppMappingDetails]` (query, optional): maximum number of related androidToIosAppMappingDetails returned (when they are included)
- `limit[appClips]` (query, optional): maximum number of related appClips returned (when they are included)
- `limit[appCustomProductPages]` (query, optional): maximum number of related appCustomProductPages returned (when they are included)
- `limit[appEncryptionDeclarations]` (query, optional): maximum number of related appEncryptionDeclarations returned (when they are included)
- `limit[appEvents]` (query, optional): maximum number of related appEvents returned (when they are included)
- `limit[appInfos]` (query, optional): maximum number of related appInfos returned (when they are included)
- `limit[appStoreVersionExperimentsV2]` (query, optional): maximum number of related appStoreVersionExperimentsV2 returned (when they are included)
- `limit[appStoreVersions]` (query, optional): maximum number of related appStoreVersions returned (when they are included)
- `limit[betaAppLocalizations]` (query, optional): maximum number of related betaAppLocalizations returned (when they are included)
- `limit[betaGroups]` (query, optional): maximum number of related betaGroups returned (when they are included)
- `limit[builds]` (query, optional): maximum number of related builds returned (when they are included)
- `limit[gameCenterEnabledVersions]` (query, optional): maximum number of related gameCenterEnabledVersions returned (when they are included)
- `limit[inAppPurchases]` (query, optional): maximum number of related inAppPurchases returned (when they are included)
- `limit[inAppPurchasesV2]` (query, optional): maximum number of related inAppPurchasesV2 returned (when they are included)
- `limit[preReleaseVersions]` (query, optional): maximum number of related preReleaseVersions returned (when they are included)
- `limit[promotedPurchases]` (query, optional): maximum number of related promotedPurchases returned (when they are included)
- `limit[reviewSubmissions]` (query, optional): maximum number of related reviewSubmissions returned (when they are included)
- `limit[subscriptionGroups]` (query, optional): maximum number of related subscriptionGroups returned (when they are included)

### `GET /v1/apps/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[apps]` (query, optional): the fields to include for returned resources of type apps
- `fields[appEncryptionDeclarations]` (query, optional): the fields to include for returned resources of type appEncryptionDeclarations
- `fields[buildIcons]` (query, optional): the fields to include for returned resources of type buildIcons
- `fields[ciProducts]` (query, optional): the fields to include for returned resources of type ciProducts
- `fields[betaGroups]` (query, optional): the fields to include for returned resources of type betaGroups
- `fields[appStoreVersions]` (query, optional): the fields to include for returned resources of type appStoreVersions
- `fields[preReleaseVersions]` (query, optional): the fields to include for returned resources of type preReleaseVersions
- `fields[betaAppLocalizations]` (query, optional): the fields to include for returned resources of type betaAppLocalizations
- `fields[builds]` (query, optional): the fields to include for returned resources of type builds
- `fields[betaLicenseAgreements]` (query, optional): the fields to include for returned resources of type betaLicenseAgreements
- `fields[betaAppReviewDetails]` (query, optional): the fields to include for returned resources of type betaAppReviewDetails
- `fields[appInfos]` (query, optional): the fields to include for returned resources of type appInfos
- `fields[appClips]` (query, optional): the fields to include for returned resources of type appClips
- `fields[endUserLicenseAgreements]` (query, optional): the fields to include for returned resources of type endUserLicenseAgreements
- `fields[inAppPurchases]` (query, optional): the fields to include for returned resources of type inAppPurchases
- `fields[subscriptionGroups]` (query, optional): the fields to include for returned resources of type subscriptionGroups
- `fields[gameCenterEnabledVersions]` (query, optional): the fields to include for returned resources of type gameCenterEnabledVersions
- `fields[appCustomProductPages]` (query, optional): the fields to include for returned resources of type appCustomProductPages
- `fields[promotedPurchases]` (query, optional): the fields to include for returned resources of type promotedPurchases
- `fields[appEvents]` (query, optional): the fields to include for returned resources of type appEvents
- `fields[reviewSubmissions]` (query, optional): the fields to include for returned resources of type reviewSubmissions
- `fields[subscriptionGracePeriods]` (query, optional): the fields to include for returned resources of type subscriptionGracePeriods
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[appStoreVersionExperiments]` (query, optional): the fields to include for returned resources of type appStoreVersionExperiments
- `fields[androidToIosAppMappingDetails]` (query, optional): the fields to include for returned resources of type androidToIosAppMappingDetails
- `include` (query, optional): comma-separated list of relationships to include
- `limit[androidToIosAppMappingDetails]` (query, optional): maximum number of related androidToIosAppMappingDetails returned (when they are included)
- `limit[appClips]` (query, optional): maximum number of related appClips returned (when they are included)
- `limit[appCustomProductPages]` (query, optional): maximum number of related appCustomProductPages returned (when they are included)
- `limit[appEncryptionDeclarations]` (query, optional): maximum number of related appEncryptionDeclarations returned (when they are included)
- `limit[appEvents]` (query, optional): maximum number of related appEvents returned (when they are included)
- `limit[appInfos]` (query, optional): maximum number of related appInfos returned (when they are included)
- `limit[appStoreVersionExperimentsV2]` (query, optional): maximum number of related appStoreVersionExperimentsV2 returned (when they are included)
- `limit[appStoreVersions]` (query, optional): maximum number of related appStoreVersions returned (when they are included)
- `limit[betaAppLocalizations]` (query, optional): maximum number of related betaAppLocalizations returned (when they are included)
- `limit[betaGroups]` (query, optional): maximum number of related betaGroups returned (when they are included)
- `limit[builds]` (query, optional): maximum number of related builds returned (when they are included)
- `limit[gameCenterEnabledVersions]` (query, optional): maximum number of related gameCenterEnabledVersions returned (when they are included)
- `limit[inAppPurchases]` (query, optional): maximum number of related inAppPurchases returned (when they are included)
- `limit[inAppPurchasesV2]` (query, optional): maximum number of related inAppPurchasesV2 returned (when they are included)
- `limit[preReleaseVersions]` (query, optional): maximum number of related preReleaseVersions returned (when they are included)
- `limit[promotedPurchases]` (query, optional): maximum number of related promotedPurchases returned (when they are included)
- `limit[reviewSubmissions]` (query, optional): maximum number of related reviewSubmissions returned (when they are included)
- `limit[subscriptionGroups]` (query, optional): maximum number of related subscriptionGroups returned (when they are included)

### `PATCH /v1/apps/{id}`
**Summary**: No summary provided.

### `GET /v1/reviewSubmissions`
**Summary**: No summary provided.

**Parameters**:
- `filter[platform]` (query, optional): filter by attribute 'platform'
- `filter[state]` (query, optional): filter by attribute 'state'
- `filter[app]` (query, required): filter by id(s) of related 'app'
- `fields[reviewSubmissions]` (query, optional): the fields to include for returned resources of type reviewSubmissions
- `fields[apps]` (query, optional): the fields to include for returned resources of type apps
- `fields[reviewSubmissionItems]` (query, optional): the fields to include for returned resources of type reviewSubmissionItems
- `fields[appStoreVersions]` (query, optional): the fields to include for returned resources of type appStoreVersions
- `fields[actors]` (query, optional): the fields to include for returned resources of type actors
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[items]` (query, optional): maximum number of related items returned (when they are included)

### `POST /v1/reviewSubmissions`
**Summary**: No summary provided.

### `GET /v1/reviewSubmissions/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[reviewSubmissions]` (query, optional): the fields to include for returned resources of type reviewSubmissions
- `fields[apps]` (query, optional): the fields to include for returned resources of type apps
- `fields[reviewSubmissionItems]` (query, optional): the fields to include for returned resources of type reviewSubmissionItems
- `fields[appStoreVersions]` (query, optional): the fields to include for returned resources of type appStoreVersions
- `fields[actors]` (query, optional): the fields to include for returned resources of type actors
- `include` (query, optional): comma-separated list of relationships to include
- `limit[items]` (query, optional): maximum number of related items returned (when they are included)

### `PATCH /v1/reviewSubmissions/{id}`
**Summary**: No summary provided.

### `GET /v1/appInfos/{id}/relationships/ageRatingDeclaration`
**Summary**: No summary provided.

### `GET /v1/appInfos/{id}/ageRatingDeclaration`
**Summary**: No summary provided.

**Parameters**:
- `fields[ageRatingDeclarations]` (query, optional): the fields to include for returned resources of type ageRatingDeclarations

### `GET /v1/appInfos/{id}/relationships/appInfoLocalizations`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/appInfos/{id}/appInfoLocalizations`
**Summary**: No summary provided.

**Parameters**:
- `filter[locale]` (query, optional): filter by attribute 'locale'
- `fields[appInfoLocalizations]` (query, optional): the fields to include for returned resources of type appInfoLocalizations
- `fields[appInfos]` (query, optional): the fields to include for returned resources of type appInfos
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include

### `GET /v1/appInfos/{id}/relationships/primaryCategory`
**Summary**: No summary provided.

### `GET /v1/appInfos/{id}/primaryCategory`
**Summary**: No summary provided.

**Parameters**:
- `fields[appCategories]` (query, optional): the fields to include for returned resources of type appCategories
- `include` (query, optional): comma-separated list of relationships to include
- `limit[subcategories]` (query, optional): maximum number of related subcategories returned (when they are included)

### `GET /v1/appInfos/{id}/relationships/primarySubcategoryOne`
**Summary**: No summary provided.

### `GET /v1/appInfos/{id}/primarySubcategoryOne`
**Summary**: No summary provided.

**Parameters**:
- `fields[appCategories]` (query, optional): the fields to include for returned resources of type appCategories
- `include` (query, optional): comma-separated list of relationships to include
- `limit[subcategories]` (query, optional): maximum number of related subcategories returned (when they are included)

### `GET /v1/appInfos/{id}/relationships/primarySubcategoryTwo`
**Summary**: No summary provided.

### `GET /v1/appInfos/{id}/primarySubcategoryTwo`
**Summary**: No summary provided.

**Parameters**:
- `fields[appCategories]` (query, optional): the fields to include for returned resources of type appCategories
- `include` (query, optional): comma-separated list of relationships to include
- `limit[subcategories]` (query, optional): maximum number of related subcategories returned (when they are included)

### `GET /v1/appInfos/{id}/relationships/secondaryCategory`
**Summary**: No summary provided.

### `GET /v1/appInfos/{id}/secondaryCategory`
**Summary**: No summary provided.

**Parameters**:
- `fields[appCategories]` (query, optional): the fields to include for returned resources of type appCategories
- `include` (query, optional): comma-separated list of relationships to include
- `limit[subcategories]` (query, optional): maximum number of related subcategories returned (when they are included)

### `GET /v1/appInfos/{id}/relationships/secondarySubcategoryOne`
**Summary**: No summary provided.

### `GET /v1/appInfos/{id}/secondarySubcategoryOne`
**Summary**: No summary provided.

**Parameters**:
- `fields[appCategories]` (query, optional): the fields to include for returned resources of type appCategories
- `include` (query, optional): comma-separated list of relationships to include
- `limit[subcategories]` (query, optional): maximum number of related subcategories returned (when they are included)

### `GET /v1/appInfos/{id}/relationships/secondarySubcategoryTwo`
**Summary**: No summary provided.

### `GET /v1/appInfos/{id}/secondarySubcategoryTwo`
**Summary**: No summary provided.

**Parameters**:
- `fields[appCategories]` (query, optional): the fields to include for returned resources of type appCategories
- `include` (query, optional): comma-separated list of relationships to include
- `limit[subcategories]` (query, optional): maximum number of related subcategories returned (when they are included)

### `GET /v1/appInfos/{id}/relationships/territoryAgeRatings`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/appInfos/{id}/territoryAgeRatings`
**Summary**: No summary provided.

**Parameters**:
- `fields[territoryAgeRatings]` (query, optional): the fields to include for returned resources of type territoryAgeRatings
- `fields[territories]` (query, optional): the fields to include for returned resources of type territories
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include

### `GET /v1/appStoreVersions/{id}/relationships/alternativeDistributionPackage`
**Summary**: No summary provided.

### `GET /v1/appStoreVersions/{id}/alternativeDistributionPackage`
**Summary**: No summary provided.

**Parameters**:
- `fields[alternativeDistributionPackages]` (query, optional): the fields to include for returned resources of type alternativeDistributionPackages
- `fields[alternativeDistributionPackageVersions]` (query, optional): the fields to include for returned resources of type alternativeDistributionPackageVersions
- `include` (query, optional): comma-separated list of relationships to include
- `limit[versions]` (query, optional): maximum number of related versions returned (when they are included)

### `GET /v1/appStoreVersions/{id}/relationships/appClipDefaultExperience`
**Summary**: No summary provided.

### `PATCH /v1/appStoreVersions/{id}/relationships/appClipDefaultExperience`
**Summary**: No summary provided.

### `GET /v1/appStoreVersions/{id}/appClipDefaultExperience`
**Summary**: No summary provided.

**Parameters**:
- `fields[appClipDefaultExperiences]` (query, optional): the fields to include for returned resources of type appClipDefaultExperiences
- `fields[appClips]` (query, optional): the fields to include for returned resources of type appClips
- `fields[appStoreVersions]` (query, optional): the fields to include for returned resources of type appStoreVersions
- `fields[appClipDefaultExperienceLocalizations]` (query, optional): the fields to include for returned resources of type appClipDefaultExperienceLocalizations
- `fields[appClipAppStoreReviewDetails]` (query, optional): the fields to include for returned resources of type appClipAppStoreReviewDetails
- `include` (query, optional): comma-separated list of relationships to include
- `limit[appClipDefaultExperienceLocalizations]` (query, optional): maximum number of related appClipDefaultExperienceLocalizations returned (when they are included)

### `GET /v1/appStoreVersions/{id}/relationships/appStoreReviewDetail`
**Summary**: No summary provided.

### `GET /v1/appStoreVersions/{id}/appStoreReviewDetail`
**Summary**: No summary provided.

**Parameters**:
- `fields[appStoreReviewDetails]` (query, optional): the fields to include for returned resources of type appStoreReviewDetails
- `fields[appStoreVersions]` (query, optional): the fields to include for returned resources of type appStoreVersions
- `fields[appStoreReviewAttachments]` (query, optional): the fields to include for returned resources of type appStoreReviewAttachments
- `include` (query, optional): comma-separated list of relationships to include
- `limit[appStoreReviewAttachments]` (query, optional): maximum number of related appStoreReviewAttachments returned (when they are included)

### `GET /v1/appStoreVersions/{id}/relationships/appStoreVersionExperiments`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/appStoreVersions/{id}/appStoreVersionExperiments`
**Summary**: No summary provided.

**Parameters**:
- `filter[state]` (query, optional): filter by attribute 'state'
- `fields[appStoreVersionExperiments]` (query, optional): the fields to include for returned resources of type appStoreVersionExperiments
- `fields[appStoreVersions]` (query, optional): the fields to include for returned resources of type appStoreVersions
- `fields[appStoreVersionExperimentTreatments]` (query, optional): the fields to include for returned resources of type appStoreVersionExperimentTreatments
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[appStoreVersionExperimentTreatments]` (query, optional): maximum number of related appStoreVersionExperimentTreatments returned (when they are included)

### `GET /v1/appStoreVersions/{id}/relationships/appStoreVersionExperimentsV2`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/appStoreVersions/{id}/appStoreVersionExperimentsV2`
**Summary**: No summary provided.

**Parameters**:
- `filter[state]` (query, optional): filter by attribute 'state'
- `fields[appStoreVersionExperiments]` (query, optional): the fields to include for returned resources of type appStoreVersionExperiments
- `fields[apps]` (query, optional): the fields to include for returned resources of type apps
- `fields[appStoreVersions]` (query, optional): the fields to include for returned resources of type appStoreVersions
- `fields[appStoreVersionExperimentTreatments]` (query, optional): the fields to include for returned resources of type appStoreVersionExperimentTreatments
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[controlVersions]` (query, optional): maximum number of related controlVersions returned (when they are included)
- `limit[appStoreVersionExperimentTreatments]` (query, optional): maximum number of related appStoreVersionExperimentTreatments returned (when they are included)

### `GET /v1/appStoreVersions/{id}/relationships/appStoreVersionLocalizations`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/appStoreVersions/{id}/appStoreVersionLocalizations`
**Summary**: No summary provided.

**Parameters**:
- `filter[locale]` (query, optional): filter by attribute 'locale'
- `fields[appStoreVersionLocalizations]` (query, optional): the fields to include for returned resources of type appStoreVersionLocalizations
- `fields[appStoreVersions]` (query, optional): the fields to include for returned resources of type appStoreVersions
- `fields[appScreenshotSets]` (query, optional): the fields to include for returned resources of type appScreenshotSets
- `fields[appPreviewSets]` (query, optional): the fields to include for returned resources of type appPreviewSets
- `fields[appKeywords]` (query, optional): the fields to include for returned resources of type appKeywords
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[appScreenshotSets]` (query, optional): maximum number of related appScreenshotSets returned (when they are included)
- `limit[appPreviewSets]` (query, optional): maximum number of related appPreviewSets returned (when they are included)
- `limit[searchKeywords]` (query, optional): maximum number of related searchKeywords returned (when they are included)

### `GET /v1/appStoreVersions/{id}/relationships/appStoreVersionPhasedRelease`
**Summary**: No summary provided.

### `GET /v1/appStoreVersions/{id}/appStoreVersionPhasedRelease`
**Summary**: No summary provided.

**Parameters**:
- `fields[appStoreVersionPhasedReleases]` (query, optional): the fields to include for returned resources of type appStoreVersionPhasedReleases

### `GET /v1/appStoreVersions/{id}/relationships/appStoreVersionSubmission`
**Summary**: No summary provided.

### `GET /v1/appStoreVersions/{id}/appStoreVersionSubmission`
**Summary**: No summary provided.

**Parameters**:
- `fields[appStoreVersionSubmissions]` (query, optional): the fields to include for returned resources of type appStoreVersionSubmissions
- `fields[appStoreVersions]` (query, optional): the fields to include for returned resources of type appStoreVersions
- `include` (query, optional): comma-separated list of relationships to include

### `GET /v1/appStoreVersions/{id}/relationships/build`
**Summary**: No summary provided.

### `PATCH /v1/appStoreVersions/{id}/relationships/build`
**Summary**: No summary provided.

### `GET /v1/appStoreVersions/{id}/build`
**Summary**: No summary provided.

**Parameters**:
- `fields[builds]` (query, optional): the fields to include for returned resources of type builds

### `GET /v1/appStoreVersions/{id}/relationships/customerReviews`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/appStoreVersions/{id}/customerReviews`
**Summary**: No summary provided.

**Parameters**:
- `filter[territory]` (query, optional): filter by attribute 'territory'
- `filter[rating]` (query, optional): filter by attribute 'rating'
- `filter[reviewTerritory]` (query, optional): filter by id(s) of related 'reviewTerritory'
- `exists[publishedResponse]` (query, optional): filter by publishedResponse
- `sort` (query, optional): comma-separated list of sort expressions; resources will be sorted as specified
- `fields[customerReviews]` (query, optional): the fields to include for returned resources of type customerReviews
- `fields[customerReviewResponses]` (query, optional): the fields to include for returned resources of type customerReviewResponses
- `fields[territories]` (query, optional): the fields to include for returned resources of type territories
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include

### `GET /v1/appStoreVersions/{id}/relationships/gameCenterAppVersion`
**Summary**: No summary provided.

### `GET /v1/appStoreVersions/{id}/gameCenterAppVersion`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterAppVersions]` (query, optional): the fields to include for returned resources of type gameCenterAppVersions
- `fields[appStoreVersions]` (query, optional): the fields to include for returned resources of type appStoreVersions
- `include` (query, optional): comma-separated list of relationships to include
- `limit[compatibilityVersions]` (query, optional): maximum number of related compatibilityVersions returned (when they are included)

### `GET /v1/appStoreVersions/{id}/relationships/routingAppCoverage`
**Summary**: No summary provided.

### `GET /v1/appStoreVersions/{id}/routingAppCoverage`
**Summary**: No summary provided.

**Parameters**:
- `fields[routingAppCoverages]` (query, optional): the fields to include for returned resources of type routingAppCoverages
- `fields[appStoreVersions]` (query, optional): the fields to include for returned resources of type appStoreVersions
- `include` (query, optional): comma-separated list of relationships to include

### `GET /v1/apps/{id}/relationships/accessibilityDeclarations`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/accessibilityDeclarations`
**Summary**: No summary provided.

**Parameters**:
- `filter[deviceFamily]` (query, optional): filter by attribute 'deviceFamily'
- `filter[state]` (query, optional): filter by attribute 'state'
- `fields[accessibilityDeclarations]` (query, optional): the fields to include for returned resources of type accessibilityDeclarations
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/relationships/alternativeDistributionKey`
**Summary**: No summary provided.

### `GET /v1/apps/{id}/alternativeDistributionKey`
**Summary**: No summary provided.

**Parameters**:
- `fields[alternativeDistributionKeys]` (query, optional): the fields to include for returned resources of type alternativeDistributionKeys

### `GET /v1/apps/{id}/relationships/analyticsReportRequests`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/analyticsReportRequests`
**Summary**: No summary provided.

**Parameters**:
- `filter[accessType]` (query, optional): filter by attribute 'accessType'
- `fields[analyticsReportRequests]` (query, optional): the fields to include for returned resources of type analyticsReportRequests
- `fields[analyticsReports]` (query, optional): the fields to include for returned resources of type analyticsReports
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[reports]` (query, optional): maximum number of related reports returned (when they are included)

### `GET /v1/apps/{id}/relationships/androidToIosAppMappingDetails`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/androidToIosAppMappingDetails`
**Summary**: No summary provided.

**Parameters**:
- `fields[androidToIosAppMappingDetails]` (query, optional): the fields to include for returned resources of type androidToIosAppMappingDetails
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/relationships/appAvailabilityV2`
**Summary**: No summary provided.

### `GET /v1/apps/{id}/appAvailabilityV2`
**Summary**: No summary provided.

**Parameters**:
- `fields[appAvailabilities]` (query, optional): the fields to include for returned resources of type appAvailabilities
- `fields[territoryAvailabilities]` (query, optional): the fields to include for returned resources of type territoryAvailabilities
- `include` (query, optional): comma-separated list of relationships to include
- `limit[territoryAvailabilities]` (query, optional): maximum number of related territoryAvailabilities returned (when they are included)

### `GET /v1/apps/{id}/relationships/appClips`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/appClips`
**Summary**: No summary provided.

**Parameters**:
- `filter[bundleId]` (query, optional): filter by attribute 'bundleId'
- `fields[appClips]` (query, optional): the fields to include for returned resources of type appClips
- `fields[apps]` (query, optional): the fields to include for returned resources of type apps
- `fields[appClipDefaultExperiences]` (query, optional): the fields to include for returned resources of type appClipDefaultExperiences
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[appClipDefaultExperiences]` (query, optional): maximum number of related appClipDefaultExperiences returned (when they are included)

### `GET /v1/apps/{id}/relationships/appCustomProductPages`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/appCustomProductPages`
**Summary**: No summary provided.

**Parameters**:
- `filter[visible]` (query, optional): filter by attribute 'visible'
- `fields[appCustomProductPages]` (query, optional): the fields to include for returned resources of type appCustomProductPages
- `fields[apps]` (query, optional): the fields to include for returned resources of type apps
- `fields[appCustomProductPageVersions]` (query, optional): the fields to include for returned resources of type appCustomProductPageVersions
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[appCustomProductPageVersions]` (query, optional): maximum number of related appCustomProductPageVersions returned (when they are included)

### `GET /v1/apps/{id}/relationships/appEncryptionDeclarations`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/appEncryptionDeclarations`
**Summary**: No summary provided.

**Parameters**:
- `filter[platform]` (query, optional): filter by attribute 'platform'
- `filter[builds]` (query, optional): filter by id(s) of related 'builds'
- `fields[appEncryptionDeclarations]` (query, optional): the fields to include for returned resources of type appEncryptionDeclarations
- `fields[apps]` (query, optional): the fields to include for returned resources of type apps
- `fields[builds]` (query, optional): the fields to include for returned resources of type builds
- `fields[appEncryptionDeclarationDocuments]` (query, optional): the fields to include for returned resources of type appEncryptionDeclarationDocuments
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[builds]` (query, optional): maximum number of related builds returned (when they are included)

### `GET /v1/apps/{id}/relationships/appEvents`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/appEvents`
**Summary**: No summary provided.

**Parameters**:
- `filter[eventState]` (query, optional): filter by attribute 'eventState'
- `filter[id]` (query, optional): filter by id(s)
- `fields[appEvents]` (query, optional): the fields to include for returned resources of type appEvents
- `fields[appEventLocalizations]` (query, optional): the fields to include for returned resources of type appEventLocalizations
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[localizations]` (query, optional): maximum number of related localizations returned (when they are included)

### `GET /v1/apps/{id}/relationships/appInfos`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/appInfos`
**Summary**: No summary provided.

**Parameters**:
- `fields[appInfos]` (query, optional): the fields to include for returned resources of type appInfos
- `fields[apps]` (query, optional): the fields to include for returned resources of type apps
- `fields[ageRatingDeclarations]` (query, optional): the fields to include for returned resources of type ageRatingDeclarations
- `fields[appInfoLocalizations]` (query, optional): the fields to include for returned resources of type appInfoLocalizations
- `fields[appCategories]` (query, optional): the fields to include for returned resources of type appCategories
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[appInfoLocalizations]` (query, optional): maximum number of related appInfoLocalizations returned (when they are included)

### `GET /v1/apps/{id}/relationships/appPricePoints`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/appPricePoints`
**Summary**: No summary provided.

**Parameters**:
- `filter[territory]` (query, optional): filter by id(s) of related 'territory'
- `fields[appPricePoints]` (query, optional): the fields to include for returned resources of type appPricePoints
- `fields[apps]` (query, optional): the fields to include for returned resources of type apps
- `fields[territories]` (query, optional): the fields to include for returned resources of type territories
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include

### `GET /v1/apps/{id}/relationships/appPriceSchedule`
**Summary**: No summary provided.

### `GET /v1/apps/{id}/appPriceSchedule`
**Summary**: No summary provided.

**Parameters**:
- `fields[appPriceSchedules]` (query, optional): the fields to include for returned resources of type appPriceSchedules
- `fields[apps]` (query, optional): the fields to include for returned resources of type apps
- `fields[territories]` (query, optional): the fields to include for returned resources of type territories
- `fields[appPrices]` (query, optional): the fields to include for returned resources of type appPrices
- `include` (query, optional): comma-separated list of relationships to include
- `limit[manualPrices]` (query, optional): maximum number of related manualPrices returned (when they are included)
- `limit[automaticPrices]` (query, optional): maximum number of related automaticPrices returned (when they are included)

### `GET /v1/apps/{id}/relationships/appStoreVersionExperimentsV2`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/appStoreVersionExperimentsV2`
**Summary**: No summary provided.

**Parameters**:
- `filter[state]` (query, optional): filter by attribute 'state'
- `fields[appStoreVersionExperiments]` (query, optional): the fields to include for returned resources of type appStoreVersionExperiments
- `fields[apps]` (query, optional): the fields to include for returned resources of type apps
- `fields[appStoreVersions]` (query, optional): the fields to include for returned resources of type appStoreVersions
- `fields[appStoreVersionExperimentTreatments]` (query, optional): the fields to include for returned resources of type appStoreVersionExperimentTreatments
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[controlVersions]` (query, optional): maximum number of related controlVersions returned (when they are included)
- `limit[appStoreVersionExperimentTreatments]` (query, optional): maximum number of related appStoreVersionExperimentTreatments returned (when they are included)

### `GET /v1/apps/{id}/relationships/appStoreVersions`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/appStoreVersions`
**Summary**: No summary provided.

**Parameters**:
- `filter[platform]` (query, optional): filter by attribute 'platform'
- `filter[versionString]` (query, optional): filter by attribute 'versionString'
- `filter[appStoreState]` (query, optional): filter by attribute 'appStoreState'
- `filter[appVersionState]` (query, optional): filter by attribute 'appVersionState'
- `filter[id]` (query, optional): filter by id(s)
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
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[appStoreVersionLocalizations]` (query, optional): maximum number of related appStoreVersionLocalizations returned (when they are included)
- `limit[appStoreVersionExperiments]` (query, optional): maximum number of related appStoreVersionExperiments returned (when they are included)
- `limit[appStoreVersionExperimentsV2]` (query, optional): maximum number of related appStoreVersionExperimentsV2 returned (when they are included)

### `GET /v1/apps/{id}/relationships/appTags`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/appTags`
**Summary**: No summary provided.

**Parameters**:
- `filter[visibleInAppStore]` (query, optional): filter by attribute 'visibleInAppStore'
- `sort` (query, optional): comma-separated list of sort expressions; resources will be sorted as specified
- `fields[appTags]` (query, optional): the fields to include for returned resources of type appTags
- `fields[territories]` (query, optional): the fields to include for returned resources of type territories
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[territories]` (query, optional): maximum number of related territories returned (when they are included)

### `GET /v1/apps/{id}/relationships/backgroundAssets`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/backgroundAssets`
**Summary**: No summary provided.

**Parameters**:
- `filter[archived]` (query, optional): filter by attribute 'archived'
- `filter[assetPackIdentifier]` (query, optional): filter by attribute 'assetPackIdentifier'
- `filter[versions.locale]` (query, optional): filter by attribute 'versions.locale'
- `filter[versions.platforms]` (query, optional): filter by attribute 'versions.platforms'
- `sort` (query, optional): comma-separated list of sort expressions; resources will be sorted as specified
- `fields[backgroundAssets]` (query, optional): the fields to include for returned resources of type backgroundAssets
- `fields[apps]` (query, optional): the fields to include for returned resources of type apps
- `fields[backgroundAssetVersions]` (query, optional): the fields to include for returned resources of type backgroundAssetVersions
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include

### `GET /v1/apps/{id}/relationships/betaAppLocalizations`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/betaAppLocalizations`
**Summary**: No summary provided.

**Parameters**:
- `fields[betaAppLocalizations]` (query, optional): the fields to include for returned resources of type betaAppLocalizations
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/relationships/betaAppReviewDetail`
**Summary**: No summary provided.

### `GET /v1/apps/{id}/betaAppReviewDetail`
**Summary**: No summary provided.

**Parameters**:
- `fields[betaAppReviewDetails]` (query, optional): the fields to include for returned resources of type betaAppReviewDetails

### `GET /v1/apps/{id}/relationships/betaFeedbackCrashSubmissions`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/betaFeedbackCrashSubmissions`
**Summary**: No summary provided.

**Parameters**:
- `filter[deviceModel]` (query, optional): filter by attribute 'deviceModel'
- `filter[osVersion]` (query, optional): filter by attribute 'osVersion'
- `filter[appPlatform]` (query, optional): filter by attribute 'appPlatform'
- `filter[devicePlatform]` (query, optional): filter by attribute 'devicePlatform'
- `filter[build]` (query, optional): filter by id(s) of related 'build'
- `filter[build.preReleaseVersion]` (query, optional): filter by id(s) of related 'build.preReleaseVersion'
- `filter[tester]` (query, optional): filter by id(s) of related 'tester'
- `sort` (query, optional): comma-separated list of sort expressions; resources will be sorted as specified
- `fields[betaFeedbackCrashSubmissions]` (query, optional): the fields to include for returned resources of type betaFeedbackCrashSubmissions
- `fields[builds]` (query, optional): the fields to include for returned resources of type builds
- `fields[betaTesters]` (query, optional): the fields to include for returned resources of type betaTesters
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include

### `GET /v1/apps/{id}/relationships/betaFeedbackScreenshotSubmissions`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/betaFeedbackScreenshotSubmissions`
**Summary**: No summary provided.

**Parameters**:
- `filter[deviceModel]` (query, optional): filter by attribute 'deviceModel'
- `filter[osVersion]` (query, optional): filter by attribute 'osVersion'
- `filter[appPlatform]` (query, optional): filter by attribute 'appPlatform'
- `filter[devicePlatform]` (query, optional): filter by attribute 'devicePlatform'
- `filter[build]` (query, optional): filter by id(s) of related 'build'
- `filter[build.preReleaseVersion]` (query, optional): filter by id(s) of related 'build.preReleaseVersion'
- `filter[tester]` (query, optional): filter by id(s) of related 'tester'
- `sort` (query, optional): comma-separated list of sort expressions; resources will be sorted as specified
- `fields[betaFeedbackScreenshotSubmissions]` (query, optional): the fields to include for returned resources of type betaFeedbackScreenshotSubmissions
- `fields[builds]` (query, optional): the fields to include for returned resources of type builds
- `fields[betaTesters]` (query, optional): the fields to include for returned resources of type betaTesters
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include

### `GET /v1/apps/{id}/relationships/betaGroups`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/betaGroups`
**Summary**: No summary provided.

**Parameters**:
- `fields[betaGroups]` (query, optional): the fields to include for returned resources of type betaGroups
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/relationships/betaLicenseAgreement`
**Summary**: No summary provided.

### `GET /v1/apps/{id}/betaLicenseAgreement`
**Summary**: No summary provided.

**Parameters**:
- `fields[betaLicenseAgreements]` (query, optional): the fields to include for returned resources of type betaLicenseAgreements

### `DELETE /v1/apps/{id}/relationships/betaTesters`
**Summary**: No summary provided.

### `GET /v1/apps/{id}/relationships/buildUploads`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/buildUploads`
**Summary**: No summary provided.

**Parameters**:
- `filter[cfBundleShortVersionString]` (query, optional): filter by attribute 'cfBundleShortVersionString'
- `filter[cfBundleVersion]` (query, optional): filter by attribute 'cfBundleVersion'
- `filter[platform]` (query, optional): filter by attribute 'platform'
- `filter[state]` (query, optional): filter by state
- `sort` (query, optional): comma-separated list of sort expressions; resources will be sorted as specified
- `fields[buildUploads]` (query, optional): the fields to include for returned resources of type buildUploads
- `fields[builds]` (query, optional): the fields to include for returned resources of type builds
- `fields[buildUploadFiles]` (query, optional): the fields to include for returned resources of type buildUploadFiles
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include

### `GET /v1/apps/{id}/relationships/builds`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/builds`
**Summary**: No summary provided.

**Parameters**:
- `fields[builds]` (query, optional): the fields to include for returned resources of type builds
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/relationships/ciProduct`
**Summary**: No summary provided.

### `GET /v1/apps/{id}/ciProduct`
**Summary**: No summary provided.

**Parameters**:
- `fields[ciProducts]` (query, optional): the fields to include for returned resources of type ciProducts
- `fields[apps]` (query, optional): the fields to include for returned resources of type apps
- `fields[bundleIds]` (query, optional): the fields to include for returned resources of type bundleIds
- `fields[scmRepositories]` (query, optional): the fields to include for returned resources of type scmRepositories
- `include` (query, optional): comma-separated list of relationships to include
- `limit[primaryRepositories]` (query, optional): maximum number of related primaryRepositories returned (when they are included)

### `GET /v1/apps/{id}/customerReviewSummarizations`
**Summary**: No summary provided.

**Parameters**:
- `filter[platform]` (query, required): filter by attribute 'platform'
- `filter[territory]` (query, optional): filter by id(s) of related 'territory'
- `fields[customerReviewSummarizations]` (query, optional): the fields to include for returned resources of type customerReviewSummarizations
- `fields[territories]` (query, optional): the fields to include for returned resources of type territories
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include

### `GET /v1/apps/{id}/relationships/customerReviews`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/customerReviews`
**Summary**: No summary provided.

**Parameters**:
- `filter[territory]` (query, optional): filter by attribute 'territory'
- `filter[rating]` (query, optional): filter by attribute 'rating'
- `filter[reviewTerritory]` (query, optional): filter by id(s) of related 'reviewTerritory'
- `exists[publishedResponse]` (query, optional): filter by publishedResponse
- `sort` (query, optional): comma-separated list of sort expressions; resources will be sorted as specified
- `fields[customerReviews]` (query, optional): the fields to include for returned resources of type customerReviews
- `fields[customerReviewResponses]` (query, optional): the fields to include for returned resources of type customerReviewResponses
- `fields[territories]` (query, optional): the fields to include for returned resources of type territories
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include

### `GET /v1/apps/{id}/relationships/endUserLicenseAgreement`
**Summary**: No summary provided.

### `GET /v1/apps/{id}/endUserLicenseAgreement`
**Summary**: No summary provided.

**Parameters**:
- `fields[endUserLicenseAgreements]` (query, optional): the fields to include for returned resources of type endUserLicenseAgreements

### `GET /v1/apps/{id}/relationships/gameCenterDetail`
**Summary**: No summary provided.

### `GET /v1/apps/{id}/gameCenterDetail`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[apps]` (query, optional): the fields to include for returned resources of type apps
- `fields[gameCenterAppVersions]` (query, optional): the fields to include for returned resources of type gameCenterAppVersions
- `fields[gameCenterGroups]` (query, optional): the fields to include for returned resources of type gameCenterGroups
- `fields[gameCenterLeaderboards]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboards
- `fields[gameCenterLeaderboardSets]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSets
- `fields[gameCenterAchievements]` (query, optional): the fields to include for returned resources of type gameCenterAchievements
- `fields[gameCenterActivities]` (query, optional): the fields to include for returned resources of type gameCenterActivities
- `fields[gameCenterChallenges]` (query, optional): the fields to include for returned resources of type gameCenterChallenges
- `fields[gameCenterAchievementReleases]` (query, optional): the fields to include for returned resources of type gameCenterAchievementReleases
- `fields[gameCenterActivityVersionReleases]` (query, optional): the fields to include for returned resources of type gameCenterActivityVersionReleases
- `fields[gameCenterChallengeVersionReleases]` (query, optional): the fields to include for returned resources of type gameCenterChallengeVersionReleases
- `fields[gameCenterLeaderboardReleases]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardReleases
- `fields[gameCenterLeaderboardSetReleases]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSetReleases
- `fields[appStoreVersions]` (query, optional): the fields to include for returned resources of type appStoreVersions
- `include` (query, optional): comma-separated list of relationships to include
- `limit[gameCenterAppVersions]` (query, optional): maximum number of related gameCenterAppVersions returned (when they are included)
- `limit[gameCenterLeaderboards]` (query, optional): maximum number of related gameCenterLeaderboards returned (when they are included)
- `limit[gameCenterLeaderboardsV2]` (query, optional): maximum number of related gameCenterLeaderboardsV2 returned (when they are included)
- `limit[gameCenterLeaderboardSets]` (query, optional): maximum number of related gameCenterLeaderboardSets returned (when they are included)
- `limit[gameCenterLeaderboardSetsV2]` (query, optional): maximum number of related gameCenterLeaderboardSetsV2 returned (when they are included)
- `limit[gameCenterAchievements]` (query, optional): maximum number of related gameCenterAchievements returned (when they are included)
- `limit[gameCenterAchievementsV2]` (query, optional): maximum number of related gameCenterAchievementsV2 returned (when they are included)
- `limit[gameCenterActivities]` (query, optional): maximum number of related gameCenterActivities returned (when they are included)
- `limit[gameCenterChallenges]` (query, optional): maximum number of related gameCenterChallenges returned (when they are included)
- `limit[achievementReleases]` (query, optional): maximum number of related achievementReleases returned (when they are included)
- `limit[activityReleases]` (query, optional): maximum number of related activityReleases returned (when they are included)
- `limit[challengeReleases]` (query, optional): maximum number of related challengeReleases returned (when they are included)
- `limit[leaderboardReleases]` (query, optional): maximum number of related leaderboardReleases returned (when they are included)
- `limit[leaderboardSetReleases]` (query, optional): maximum number of related leaderboardSetReleases returned (when they are included)
- `limit[challengesMinimumPlatformVersions]` (query, optional): maximum number of related challengesMinimumPlatformVersions returned (when they are included)

### `GET /v1/apps/{id}/relationships/gameCenterEnabledVersions`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/gameCenterEnabledVersions`
**Summary**: No summary provided.

**Parameters**:
- `filter[platform]` (query, optional): filter by attribute 'platform'
- `filter[versionString]` (query, optional): filter by attribute 'versionString'
- `filter[id]` (query, optional): filter by id(s)
- `sort` (query, optional): comma-separated list of sort expressions; resources will be sorted as specified
- `fields[gameCenterEnabledVersions]` (query, optional): the fields to include for returned resources of type gameCenterEnabledVersions
- `fields[apps]` (query, optional): the fields to include for returned resources of type apps
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[compatibleVersions]` (query, optional): maximum number of related compatibleVersions returned (when they are included)

### `GET /v1/apps/{id}/relationships/inAppPurchases`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/inAppPurchases`
**Summary**: No summary provided.

**Parameters**:
- `filter[inAppPurchaseType]` (query, optional): filter by attribute 'inAppPurchaseType'
- `filter[canBeSubmitted]` (query, optional): filter by canBeSubmitted
- `sort` (query, optional): comma-separated list of sort expressions; resources will be sorted as specified
- `fields[inAppPurchases]` (query, optional): the fields to include for returned resources of type inAppPurchases
- `fields[apps]` (query, optional): the fields to include for returned resources of type apps
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[apps]` (query, optional): maximum number of related apps returned (when they are included)

### `GET /v1/apps/{id}/relationships/inAppPurchasesV2`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/inAppPurchasesV2`
**Summary**: No summary provided.

**Parameters**:
- `filter[productId]` (query, optional): filter by attribute 'productId'
- `filter[name]` (query, optional): filter by attribute 'name'
- `filter[state]` (query, optional): filter by attribute 'state'
- `filter[inAppPurchaseType]` (query, optional): filter by attribute 'inAppPurchaseType'
- `sort` (query, optional): comma-separated list of sort expressions; resources will be sorted as specified
- `fields[inAppPurchases]` (query, optional): the fields to include for returned resources of type inAppPurchases
- `fields[inAppPurchaseLocalizations]` (query, optional): the fields to include for returned resources of type inAppPurchaseLocalizations
- `fields[inAppPurchaseContents]` (query, optional): the fields to include for returned resources of type inAppPurchaseContents
- `fields[inAppPurchaseAppStoreReviewScreenshots]` (query, optional): the fields to include for returned resources of type inAppPurchaseAppStoreReviewScreenshots
- `fields[promotedPurchases]` (query, optional): the fields to include for returned resources of type promotedPurchases
- `fields[inAppPurchasePriceSchedules]` (query, optional): the fields to include for returned resources of type inAppPurchasePriceSchedules
- `fields[inAppPurchaseAvailabilities]` (query, optional): the fields to include for returned resources of type inAppPurchaseAvailabilities
- `fields[inAppPurchaseImages]` (query, optional): the fields to include for returned resources of type inAppPurchaseImages
- `fields[inAppPurchaseOfferCodes]` (query, optional): the fields to include for returned resources of type inAppPurchaseOfferCodes
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[inAppPurchaseLocalizations]` (query, optional): maximum number of related inAppPurchaseLocalizations returned (when they are included)
- `limit[images]` (query, optional): maximum number of related images returned (when they are included)
- `limit[offerCodes]` (query, optional): maximum number of related offerCodes returned (when they are included)

### `GET /v1/apps/{id}/relationships/marketplaceSearchDetail`
**Summary**: No summary provided.

### `GET /v1/apps/{id}/marketplaceSearchDetail`
**Summary**: No summary provided.

**Parameters**:
- `fields[marketplaceSearchDetails]` (query, optional): the fields to include for returned resources of type marketplaceSearchDetails

### `GET /v1/apps/{id}/perfPowerMetrics`
**Summary**: No summary provided.

**Parameters**:
- `filter[platform]` (query, optional): filter by attribute 'platform'
- `filter[metricType]` (query, optional): filter by attribute 'metricType'
- `filter[deviceType]` (query, optional): filter by attribute 'deviceType'

### `GET /v1/apps/{id}/relationships/preReleaseVersions`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/preReleaseVersions`
**Summary**: No summary provided.

**Parameters**:
- `fields[preReleaseVersions]` (query, optional): the fields to include for returned resources of type preReleaseVersions
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/relationships/promotedPurchases`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `PATCH /v1/apps/{id}/relationships/promotedPurchases`
**Summary**: No summary provided.

### `GET /v1/apps/{id}/promotedPurchases`
**Summary**: No summary provided.

**Parameters**:
- `fields[promotedPurchases]` (query, optional): the fields to include for returned resources of type promotedPurchases
- `fields[inAppPurchases]` (query, optional): the fields to include for returned resources of type inAppPurchases
- `fields[subscriptions]` (query, optional): the fields to include for returned resources of type subscriptions
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include

### `GET /v1/apps/{id}/relationships/reviewSubmissions`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/reviewSubmissions`
**Summary**: No summary provided.

**Parameters**:
- `filter[platform]` (query, optional): filter by attribute 'platform'
- `filter[state]` (query, optional): filter by attribute 'state'
- `fields[reviewSubmissions]` (query, optional): the fields to include for returned resources of type reviewSubmissions
- `fields[apps]` (query, optional): the fields to include for returned resources of type apps
- `fields[reviewSubmissionItems]` (query, optional): the fields to include for returned resources of type reviewSubmissionItems
- `fields[appStoreVersions]` (query, optional): the fields to include for returned resources of type appStoreVersions
- `fields[actors]` (query, optional): the fields to include for returned resources of type actors
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[items]` (query, optional): maximum number of related items returned (when they are included)

### `GET /v1/apps/{id}/relationships/searchKeywords`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/searchKeywords`
**Summary**: No summary provided.

**Parameters**:
- `filter[platform]` (query, optional): filter by platform
- `filter[locale]` (query, optional): filter by locale
- `fields[appKeywords]` (query, optional): the fields to include for returned resources of type appKeywords
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/relationships/subscriptionGracePeriod`
**Summary**: No summary provided.

### `GET /v1/apps/{id}/subscriptionGracePeriod`
**Summary**: No summary provided.

**Parameters**:
- `fields[subscriptionGracePeriods]` (query, optional): the fields to include for returned resources of type subscriptionGracePeriods

### `GET /v1/apps/{id}/relationships/subscriptionGroups`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/subscriptionGroups`
**Summary**: No summary provided.

**Parameters**:
- `filter[referenceName]` (query, optional): filter by attribute 'referenceName'
- `filter[subscriptions.state]` (query, optional): filter by attribute 'subscriptions.state'
- `sort` (query, optional): comma-separated list of sort expressions; resources will be sorted as specified
- `fields[subscriptionGroups]` (query, optional): the fields to include for returned resources of type subscriptionGroups
- `fields[subscriptions]` (query, optional): the fields to include for returned resources of type subscriptions
- `fields[subscriptionGroupLocalizations]` (query, optional): the fields to include for returned resources of type subscriptionGroupLocalizations
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[subscriptions]` (query, optional): maximum number of related subscriptions returned (when they are included)
- `limit[subscriptionGroupLocalizations]` (query, optional): maximum number of related subscriptionGroupLocalizations returned (when they are included)

### `GET /v1/apps/{id}/relationships/webhooks`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/apps/{id}/webhooks`
**Summary**: No summary provided.

**Parameters**:
- `fields[webhooks]` (query, optional): the fields to include for returned resources of type webhooks
- `fields[apps]` (query, optional): the fields to include for returned resources of type apps
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include

### `GET /v1/reviewSubmissions/{id}/relationships/items`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/reviewSubmissions/{id}/items`
**Summary**: No summary provided.

**Parameters**:
- `fields[reviewSubmissionItems]` (query, optional): the fields to include for returned resources of type reviewSubmissionItems
- `fields[appStoreVersions]` (query, optional): the fields to include for returned resources of type appStoreVersions
- `fields[appCustomProductPageVersions]` (query, optional): the fields to include for returned resources of type appCustomProductPageVersions
- `fields[appStoreVersionExperiments]` (query, optional): the fields to include for returned resources of type appStoreVersionExperiments
- `fields[appEvents]` (query, optional): the fields to include for returned resources of type appEvents
- `fields[backgroundAssetVersions]` (query, optional): the fields to include for returned resources of type backgroundAssetVersions
- `fields[gameCenterAchievementVersions]` (query, optional): the fields to include for returned resources of type gameCenterAchievementVersions
- `fields[gameCenterActivityVersions]` (query, optional): the fields to include for returned resources of type gameCenterActivityVersions
- `fields[gameCenterChallengeVersions]` (query, optional): the fields to include for returned resources of type gameCenterChallengeVersions
- `fields[gameCenterLeaderboardSetVersions]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSetVersions
- `fields[gameCenterLeaderboardVersions]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardVersions
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include

### `GET /v1/apps/{id}/metrics/betaTesterUsages`
**Summary**: No summary provided.

**Parameters**:
- `period` (query, optional): the duration of the reporting period
- `groupBy` (query, optional): the dimension by which to group the results
- `filter[betaTesters]` (query, optional): filter by 'betaTesters' relationship dimension
- `limit` (query, optional): maximum number of groups to return per page

## Typical Workflows
Use these endpoints to automate app management tasks within Apple Store Connect.

## Best Practices
- Always authenticate requests using your Apple Store Connect API key (JWT token).
- Handle rate limiting gracefully, as the Apple Store Connect API enforces quotas.
- When writing integrations, refer back to the exact schemas for precise payload construction.