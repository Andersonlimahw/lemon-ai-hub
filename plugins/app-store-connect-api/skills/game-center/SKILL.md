---
name: Game Center
description: Endpoints for managing Game Center leaderboards, achievements, and matchmaking.
---

# Game Center
Endpoints for managing Game Center leaderboards, achievements, and matchmaking.

## Endpoints

### `POST /v1/gameCenterAchievementImages`
**Summary**: No summary provided.

### `GET /v1/gameCenterAchievementImages/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterAchievementImages]` (query, optional): the fields to include for returned resources of type gameCenterAchievementImages
- `fields[gameCenterAchievementLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterAchievementLocalizations
- `include` (query, optional): comma-separated list of relationships to include

### `PATCH /v1/gameCenterAchievementImages/{id}`
**Summary**: No summary provided.

### `DELETE /v1/gameCenterAchievementImages/{id}`
**Summary**: No summary provided.

### `POST /v1/gameCenterAchievementLocalizations`
**Summary**: No summary provided.

### `GET /v1/gameCenterAchievementLocalizations/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterAchievementLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterAchievementLocalizations
- `fields[gameCenterAchievements]` (query, optional): the fields to include for returned resources of type gameCenterAchievements
- `fields[gameCenterAchievementImages]` (query, optional): the fields to include for returned resources of type gameCenterAchievementImages
- `include` (query, optional): comma-separated list of relationships to include

### `PATCH /v1/gameCenterAchievementLocalizations/{id}`
**Summary**: No summary provided.

### `DELETE /v1/gameCenterAchievementLocalizations/{id}`
**Summary**: No summary provided.

### `POST /v1/gameCenterAchievementReleases`
**Summary**: No summary provided.

### `GET /v1/gameCenterAchievementReleases/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterAchievementReleases]` (query, optional): the fields to include for returned resources of type gameCenterAchievementReleases
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterAchievements]` (query, optional): the fields to include for returned resources of type gameCenterAchievements
- `include` (query, optional): comma-separated list of relationships to include

### `DELETE /v1/gameCenterAchievementReleases/{id}`
**Summary**: No summary provided.

### `POST /v1/gameCenterAchievements`
**Summary**: No summary provided.

### `GET /v1/gameCenterAchievements/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterAchievements]` (query, optional): the fields to include for returned resources of type gameCenterAchievements
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterGroups]` (query, optional): the fields to include for returned resources of type gameCenterGroups
- `fields[gameCenterAchievementLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterAchievementLocalizations
- `fields[gameCenterAchievementReleases]` (query, optional): the fields to include for returned resources of type gameCenterAchievementReleases
- `fields[gameCenterActivities]` (query, optional): the fields to include for returned resources of type gameCenterActivities
- `include` (query, optional): comma-separated list of relationships to include
- `limit[localizations]` (query, optional): maximum number of related localizations returned (when they are included)
- `limit[releases]` (query, optional): maximum number of related releases returned (when they are included)

### `PATCH /v1/gameCenterAchievements/{id}`
**Summary**: No summary provided.

### `DELETE /v1/gameCenterAchievements/{id}`
**Summary**: No summary provided.

### `POST /v1/gameCenterActivities`
**Summary**: No summary provided.

### `GET /v1/gameCenterActivities/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterActivities]` (query, optional): the fields to include for returned resources of type gameCenterActivities
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterGroups]` (query, optional): the fields to include for returned resources of type gameCenterGroups
- `fields[gameCenterAchievements]` (query, optional): the fields to include for returned resources of type gameCenterAchievements
- `fields[gameCenterLeaderboards]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboards
- `fields[gameCenterActivityVersions]` (query, optional): the fields to include for returned resources of type gameCenterActivityVersions
- `include` (query, optional): comma-separated list of relationships to include
- `limit[achievements]` (query, optional): maximum number of related achievements returned (when they are included)
- `limit[achievementsV2]` (query, optional): maximum number of related achievementsV2 returned (when they are included)
- `limit[leaderboards]` (query, optional): maximum number of related leaderboards returned (when they are included)
- `limit[leaderboardsV2]` (query, optional): maximum number of related leaderboardsV2 returned (when they are included)
- `limit[versions]` (query, optional): maximum number of related versions returned (when they are included)

### `PATCH /v1/gameCenterActivities/{id}`
**Summary**: No summary provided.

### `DELETE /v1/gameCenterActivities/{id}`
**Summary**: No summary provided.

### `POST /v1/gameCenterActivityImages`
**Summary**: No summary provided.

### `GET /v1/gameCenterActivityImages/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterActivityImages]` (query, optional): the fields to include for returned resources of type gameCenterActivityImages

### `PATCH /v1/gameCenterActivityImages/{id}`
**Summary**: No summary provided.

### `DELETE /v1/gameCenterActivityImages/{id}`
**Summary**: No summary provided.

### `POST /v1/gameCenterActivityLocalizations`
**Summary**: No summary provided.

### `GET /v1/gameCenterActivityLocalizations/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterActivityLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterActivityLocalizations
- `fields[gameCenterActivityVersions]` (query, optional): the fields to include for returned resources of type gameCenterActivityVersions
- `fields[gameCenterActivityImages]` (query, optional): the fields to include for returned resources of type gameCenterActivityImages
- `include` (query, optional): comma-separated list of relationships to include

### `PATCH /v1/gameCenterActivityLocalizations/{id}`
**Summary**: No summary provided.

### `DELETE /v1/gameCenterActivityLocalizations/{id}`
**Summary**: No summary provided.

### `POST /v1/gameCenterActivityVersionReleases`
**Summary**: No summary provided.

### `GET /v1/gameCenterActivityVersionReleases/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterActivityVersionReleases]` (query, optional): the fields to include for returned resources of type gameCenterActivityVersionReleases
- `fields[gameCenterActivityVersions]` (query, optional): the fields to include for returned resources of type gameCenterActivityVersions
- `include` (query, optional): comma-separated list of relationships to include

### `DELETE /v1/gameCenterActivityVersionReleases/{id}`
**Summary**: No summary provided.

### `POST /v1/gameCenterActivityVersions`
**Summary**: No summary provided.

### `GET /v1/gameCenterActivityVersions/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterActivityVersions]` (query, optional): the fields to include for returned resources of type gameCenterActivityVersions
- `fields[gameCenterActivities]` (query, optional): the fields to include for returned resources of type gameCenterActivities
- `fields[gameCenterActivityLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterActivityLocalizations
- `fields[gameCenterActivityImages]` (query, optional): the fields to include for returned resources of type gameCenterActivityImages
- `fields[gameCenterActivityVersionReleases]` (query, optional): the fields to include for returned resources of type gameCenterActivityVersionReleases
- `include` (query, optional): comma-separated list of relationships to include
- `limit[localizations]` (query, optional): maximum number of related localizations returned (when they are included)
- `limit[releases]` (query, optional): maximum number of related releases returned (when they are included)

### `PATCH /v1/gameCenterActivityVersions/{id}`
**Summary**: No summary provided.

### `POST /v1/gameCenterAppVersions`
**Summary**: No summary provided.

### `GET /v1/gameCenterAppVersions/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterAppVersions]` (query, optional): the fields to include for returned resources of type gameCenterAppVersions
- `fields[appStoreVersions]` (query, optional): the fields to include for returned resources of type appStoreVersions
- `include` (query, optional): comma-separated list of relationships to include
- `limit[compatibilityVersions]` (query, optional): maximum number of related compatibilityVersions returned (when they are included)

### `PATCH /v1/gameCenterAppVersions/{id}`
**Summary**: No summary provided.

### `POST /v1/gameCenterChallengeImages`
**Summary**: No summary provided.

### `GET /v1/gameCenterChallengeImages/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterChallengeImages]` (query, optional): the fields to include for returned resources of type gameCenterChallengeImages

### `PATCH /v1/gameCenterChallengeImages/{id}`
**Summary**: No summary provided.

### `DELETE /v1/gameCenterChallengeImages/{id}`
**Summary**: No summary provided.

### `POST /v1/gameCenterChallengeLocalizations`
**Summary**: No summary provided.

### `GET /v1/gameCenterChallengeLocalizations/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterChallengeLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterChallengeLocalizations
- `fields[gameCenterChallengeVersions]` (query, optional): the fields to include for returned resources of type gameCenterChallengeVersions
- `fields[gameCenterChallengeImages]` (query, optional): the fields to include for returned resources of type gameCenterChallengeImages
- `include` (query, optional): comma-separated list of relationships to include

### `PATCH /v1/gameCenterChallengeLocalizations/{id}`
**Summary**: No summary provided.

### `DELETE /v1/gameCenterChallengeLocalizations/{id}`
**Summary**: No summary provided.

### `POST /v1/gameCenterChallengeVersionReleases`
**Summary**: No summary provided.

### `GET /v1/gameCenterChallengeVersionReleases/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterChallengeVersionReleases]` (query, optional): the fields to include for returned resources of type gameCenterChallengeVersionReleases
- `fields[gameCenterChallengeVersions]` (query, optional): the fields to include for returned resources of type gameCenterChallengeVersions
- `include` (query, optional): comma-separated list of relationships to include

### `DELETE /v1/gameCenterChallengeVersionReleases/{id}`
**Summary**: No summary provided.

### `POST /v1/gameCenterChallengeVersions`
**Summary**: No summary provided.

### `GET /v1/gameCenterChallengeVersions/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterChallengeVersions]` (query, optional): the fields to include for returned resources of type gameCenterChallengeVersions
- `fields[gameCenterChallenges]` (query, optional): the fields to include for returned resources of type gameCenterChallenges
- `fields[gameCenterChallengeLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterChallengeLocalizations
- `fields[gameCenterChallengeVersionReleases]` (query, optional): the fields to include for returned resources of type gameCenterChallengeVersionReleases
- `fields[gameCenterChallengeImages]` (query, optional): the fields to include for returned resources of type gameCenterChallengeImages
- `include` (query, optional): comma-separated list of relationships to include
- `limit[localizations]` (query, optional): maximum number of related localizations returned (when they are included)
- `limit[releases]` (query, optional): maximum number of related releases returned (when they are included)

### `POST /v1/gameCenterChallenges`
**Summary**: No summary provided.

### `GET /v1/gameCenterChallenges/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterChallenges]` (query, optional): the fields to include for returned resources of type gameCenterChallenges
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterGroups]` (query, optional): the fields to include for returned resources of type gameCenterGroups
- `fields[gameCenterChallengeVersions]` (query, optional): the fields to include for returned resources of type gameCenterChallengeVersions
- `fields[gameCenterLeaderboards]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboards
- `include` (query, optional): comma-separated list of relationships to include
- `limit[versions]` (query, optional): maximum number of related versions returned (when they are included)

### `PATCH /v1/gameCenterChallenges/{id}`
**Summary**: No summary provided.

### `DELETE /v1/gameCenterChallenges/{id}`
**Summary**: No summary provided.

### `POST /v1/gameCenterDetails`
**Summary**: No summary provided.

### `GET /v1/gameCenterDetails/{id}`
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
- `limit[achievementReleases]` (query, optional): maximum number of related achievementReleases returned (when they are included)
- `limit[activityReleases]` (query, optional): maximum number of related activityReleases returned (when they are included)
- `limit[challengeReleases]` (query, optional): maximum number of related challengeReleases returned (when they are included)
- `limit[challengesMinimumPlatformVersions]` (query, optional): maximum number of related challengesMinimumPlatformVersions returned (when they are included)
- `limit[gameCenterAchievements]` (query, optional): maximum number of related gameCenterAchievements returned (when they are included)
- `limit[gameCenterAchievementsV2]` (query, optional): maximum number of related gameCenterAchievementsV2 returned (when they are included)
- `limit[gameCenterActivities]` (query, optional): maximum number of related gameCenterActivities returned (when they are included)
- `limit[gameCenterAppVersions]` (query, optional): maximum number of related gameCenterAppVersions returned (when they are included)
- `limit[gameCenterChallenges]` (query, optional): maximum number of related gameCenterChallenges returned (when they are included)
- `limit[gameCenterLeaderboardSets]` (query, optional): maximum number of related gameCenterLeaderboardSets returned (when they are included)
- `limit[gameCenterLeaderboardSetsV2]` (query, optional): maximum number of related gameCenterLeaderboardSetsV2 returned (when they are included)
- `limit[gameCenterLeaderboards]` (query, optional): maximum number of related gameCenterLeaderboards returned (when they are included)
- `limit[gameCenterLeaderboardsV2]` (query, optional): maximum number of related gameCenterLeaderboardsV2 returned (when they are included)
- `limit[leaderboardReleases]` (query, optional): maximum number of related leaderboardReleases returned (when they are included)
- `limit[leaderboardSetReleases]` (query, optional): maximum number of related leaderboardSetReleases returned (when they are included)

### `PATCH /v1/gameCenterDetails/{id}`
**Summary**: No summary provided.

### `GET /v1/gameCenterGroups`
**Summary**: No summary provided.

**Parameters**:
- `filter[gameCenterDetails]` (query, optional): filter by id(s) of related 'gameCenterDetails'
- `fields[gameCenterGroups]` (query, optional): the fields to include for returned resources of type gameCenterGroups
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterLeaderboards]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboards
- `fields[gameCenterLeaderboardSets]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSets
- `fields[gameCenterAchievements]` (query, optional): the fields to include for returned resources of type gameCenterAchievements
- `fields[gameCenterActivities]` (query, optional): the fields to include for returned resources of type gameCenterActivities
- `fields[gameCenterChallenges]` (query, optional): the fields to include for returned resources of type gameCenterChallenges
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[gameCenterAchievements]` (query, optional): maximum number of related gameCenterAchievements returned (when they are included)
- `limit[gameCenterAchievementsV2]` (query, optional): maximum number of related gameCenterAchievementsV2 returned (when they are included)
- `limit[gameCenterActivities]` (query, optional): maximum number of related gameCenterActivities returned (when they are included)
- `limit[gameCenterChallenges]` (query, optional): maximum number of related gameCenterChallenges returned (when they are included)
- `limit[gameCenterDetails]` (query, optional): maximum number of related gameCenterDetails returned (when they are included)
- `limit[gameCenterLeaderboardSets]` (query, optional): maximum number of related gameCenterLeaderboardSets returned (when they are included)
- `limit[gameCenterLeaderboardSetsV2]` (query, optional): maximum number of related gameCenterLeaderboardSetsV2 returned (when they are included)
- `limit[gameCenterLeaderboards]` (query, optional): maximum number of related gameCenterLeaderboards returned (when they are included)
- `limit[gameCenterLeaderboardsV2]` (query, optional): maximum number of related gameCenterLeaderboardsV2 returned (when they are included)

### `POST /v1/gameCenterGroups`
**Summary**: No summary provided.

### `GET /v1/gameCenterGroups/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterGroups]` (query, optional): the fields to include for returned resources of type gameCenterGroups
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterLeaderboards]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboards
- `fields[gameCenterLeaderboardSets]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSets
- `fields[gameCenterAchievements]` (query, optional): the fields to include for returned resources of type gameCenterAchievements
- `fields[gameCenterActivities]` (query, optional): the fields to include for returned resources of type gameCenterActivities
- `fields[gameCenterChallenges]` (query, optional): the fields to include for returned resources of type gameCenterChallenges
- `include` (query, optional): comma-separated list of relationships to include
- `limit[gameCenterAchievements]` (query, optional): maximum number of related gameCenterAchievements returned (when they are included)
- `limit[gameCenterAchievementsV2]` (query, optional): maximum number of related gameCenterAchievementsV2 returned (when they are included)
- `limit[gameCenterActivities]` (query, optional): maximum number of related gameCenterActivities returned (when they are included)
- `limit[gameCenterChallenges]` (query, optional): maximum number of related gameCenterChallenges returned (when they are included)
- `limit[gameCenterDetails]` (query, optional): maximum number of related gameCenterDetails returned (when they are included)
- `limit[gameCenterLeaderboardSets]` (query, optional): maximum number of related gameCenterLeaderboardSets returned (when they are included)
- `limit[gameCenterLeaderboardSetsV2]` (query, optional): maximum number of related gameCenterLeaderboardSetsV2 returned (when they are included)
- `limit[gameCenterLeaderboards]` (query, optional): maximum number of related gameCenterLeaderboards returned (when they are included)
- `limit[gameCenterLeaderboardsV2]` (query, optional): maximum number of related gameCenterLeaderboardsV2 returned (when they are included)

### `PATCH /v1/gameCenterGroups/{id}`
**Summary**: No summary provided.

### `DELETE /v1/gameCenterGroups/{id}`
**Summary**: No summary provided.

### `POST /v1/gameCenterLeaderboardEntrySubmissions`
**Summary**: No summary provided.

### `POST /v1/gameCenterLeaderboardImages`
**Summary**: No summary provided.

### `GET /v1/gameCenterLeaderboardImages/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterLeaderboardImages]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardImages
- `fields[gameCenterLeaderboardLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardLocalizations
- `include` (query, optional): comma-separated list of relationships to include

### `PATCH /v1/gameCenterLeaderboardImages/{id}`
**Summary**: No summary provided.

### `DELETE /v1/gameCenterLeaderboardImages/{id}`
**Summary**: No summary provided.

### `POST /v1/gameCenterLeaderboardLocalizations`
**Summary**: No summary provided.

### `GET /v1/gameCenterLeaderboardLocalizations/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterLeaderboardLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardLocalizations
- `fields[gameCenterLeaderboards]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboards
- `fields[gameCenterLeaderboardImages]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardImages
- `include` (query, optional): comma-separated list of relationships to include

### `PATCH /v1/gameCenterLeaderboardLocalizations/{id}`
**Summary**: No summary provided.

### `DELETE /v1/gameCenterLeaderboardLocalizations/{id}`
**Summary**: No summary provided.

### `POST /v1/gameCenterLeaderboardReleases`
**Summary**: No summary provided.

### `GET /v1/gameCenterLeaderboardReleases/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterLeaderboardReleases]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardReleases
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterLeaderboards]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboards
- `include` (query, optional): comma-separated list of relationships to include

### `DELETE /v1/gameCenterLeaderboardReleases/{id}`
**Summary**: No summary provided.

### `POST /v1/gameCenterLeaderboardSetImages`
**Summary**: No summary provided.

### `GET /v1/gameCenterLeaderboardSetImages/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterLeaderboardSetImages]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSetImages
- `fields[gameCenterLeaderboardSetLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSetLocalizations
- `include` (query, optional): comma-separated list of relationships to include

### `PATCH /v1/gameCenterLeaderboardSetImages/{id}`
**Summary**: No summary provided.

### `DELETE /v1/gameCenterLeaderboardSetImages/{id}`
**Summary**: No summary provided.

### `POST /v1/gameCenterLeaderboardSetLocalizations`
**Summary**: No summary provided.

### `GET /v1/gameCenterLeaderboardSetLocalizations/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterLeaderboardSetLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSetLocalizations
- `fields[gameCenterLeaderboardSets]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSets
- `fields[gameCenterLeaderboardSetImages]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSetImages
- `include` (query, optional): comma-separated list of relationships to include

### `PATCH /v1/gameCenterLeaderboardSetLocalizations/{id}`
**Summary**: No summary provided.

### `DELETE /v1/gameCenterLeaderboardSetLocalizations/{id}`
**Summary**: No summary provided.

### `GET /v1/gameCenterLeaderboardSetMemberLocalizations`
**Summary**: No summary provided.

**Parameters**:
- `filter[gameCenterLeaderboardSet]` (query, required): filter by id(s) of related 'gameCenterLeaderboardSet'
- `filter[gameCenterLeaderboard]` (query, required): filter by id(s) of related 'gameCenterLeaderboard'
- `fields[gameCenterLeaderboardSetMemberLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSetMemberLocalizations
- `fields[gameCenterLeaderboardSets]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSets
- `fields[gameCenterLeaderboards]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboards
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include

### `POST /v1/gameCenterLeaderboardSetMemberLocalizations`
**Summary**: No summary provided.

### `PATCH /v1/gameCenterLeaderboardSetMemberLocalizations/{id}`
**Summary**: No summary provided.

### `DELETE /v1/gameCenterLeaderboardSetMemberLocalizations/{id}`
**Summary**: No summary provided.

### `POST /v1/gameCenterLeaderboardSetReleases`
**Summary**: No summary provided.

### `GET /v1/gameCenterLeaderboardSetReleases/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterLeaderboardSetReleases]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSetReleases
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterLeaderboardSets]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSets
- `include` (query, optional): comma-separated list of relationships to include

### `DELETE /v1/gameCenterLeaderboardSetReleases/{id}`
**Summary**: No summary provided.

### `POST /v1/gameCenterLeaderboardSets`
**Summary**: No summary provided.

### `GET /v1/gameCenterLeaderboardSets/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterLeaderboardSets]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSets
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterGroups]` (query, optional): the fields to include for returned resources of type gameCenterGroups
- `fields[gameCenterLeaderboardSetLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSetLocalizations
- `fields[gameCenterLeaderboards]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboards
- `fields[gameCenterLeaderboardSetReleases]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSetReleases
- `include` (query, optional): comma-separated list of relationships to include
- `limit[gameCenterLeaderboards]` (query, optional): maximum number of related gameCenterLeaderboards returned (when they are included)
- `limit[localizations]` (query, optional): maximum number of related localizations returned (when they are included)
- `limit[releases]` (query, optional): maximum number of related releases returned (when they are included)

### `PATCH /v1/gameCenterLeaderboardSets/{id}`
**Summary**: No summary provided.

### `DELETE /v1/gameCenterLeaderboardSets/{id}`
**Summary**: No summary provided.

### `POST /v1/gameCenterLeaderboards`
**Summary**: No summary provided.

### `GET /v1/gameCenterLeaderboards/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterLeaderboards]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboards
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterGroups]` (query, optional): the fields to include for returned resources of type gameCenterGroups
- `fields[gameCenterLeaderboardSets]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSets
- `fields[gameCenterLeaderboardLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardLocalizations
- `fields[gameCenterLeaderboardReleases]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardReleases
- `fields[gameCenterActivities]` (query, optional): the fields to include for returned resources of type gameCenterActivities
- `fields[gameCenterChallenges]` (query, optional): the fields to include for returned resources of type gameCenterChallenges
- `include` (query, optional): comma-separated list of relationships to include
- `limit[gameCenterLeaderboardSets]` (query, optional): maximum number of related gameCenterLeaderboardSets returned (when they are included)
- `limit[localizations]` (query, optional): maximum number of related localizations returned (when they are included)
- `limit[releases]` (query, optional): maximum number of related releases returned (when they are included)

### `PATCH /v1/gameCenterLeaderboards/{id}`
**Summary**: No summary provided.

### `DELETE /v1/gameCenterLeaderboards/{id}`
**Summary**: No summary provided.

### `GET /v1/gameCenterMatchmakingQueues`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterMatchmakingQueues]` (query, optional): the fields to include for returned resources of type gameCenterMatchmakingQueues
- `fields[gameCenterMatchmakingRuleSets]` (query, optional): the fields to include for returned resources of type gameCenterMatchmakingRuleSets
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include

### `POST /v1/gameCenterMatchmakingQueues`
**Summary**: No summary provided.

### `GET /v1/gameCenterMatchmakingQueues/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterMatchmakingQueues]` (query, optional): the fields to include for returned resources of type gameCenterMatchmakingQueues
- `fields[gameCenterMatchmakingRuleSets]` (query, optional): the fields to include for returned resources of type gameCenterMatchmakingRuleSets
- `include` (query, optional): comma-separated list of relationships to include

### `PATCH /v1/gameCenterMatchmakingQueues/{id}`
**Summary**: No summary provided.

### `DELETE /v1/gameCenterMatchmakingQueues/{id}`
**Summary**: No summary provided.

### `POST /v1/gameCenterMatchmakingRuleSetTests`
**Summary**: No summary provided.

### `GET /v1/gameCenterMatchmakingRuleSets`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterMatchmakingRuleSets]` (query, optional): the fields to include for returned resources of type gameCenterMatchmakingRuleSets
- `fields[gameCenterMatchmakingTeams]` (query, optional): the fields to include for returned resources of type gameCenterMatchmakingTeams
- `fields[gameCenterMatchmakingRules]` (query, optional): the fields to include for returned resources of type gameCenterMatchmakingRules
- `fields[gameCenterMatchmakingQueues]` (query, optional): the fields to include for returned resources of type gameCenterMatchmakingQueues
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[matchmakingQueues]` (query, optional): maximum number of related matchmakingQueues returned (when they are included)
- `limit[rules]` (query, optional): maximum number of related rules returned (when they are included)
- `limit[teams]` (query, optional): maximum number of related teams returned (when they are included)

### `POST /v1/gameCenterMatchmakingRuleSets`
**Summary**: No summary provided.

### `GET /v1/gameCenterMatchmakingRuleSets/{id}`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterMatchmakingRuleSets]` (query, optional): the fields to include for returned resources of type gameCenterMatchmakingRuleSets
- `fields[gameCenterMatchmakingTeams]` (query, optional): the fields to include for returned resources of type gameCenterMatchmakingTeams
- `fields[gameCenterMatchmakingRules]` (query, optional): the fields to include for returned resources of type gameCenterMatchmakingRules
- `fields[gameCenterMatchmakingQueues]` (query, optional): the fields to include for returned resources of type gameCenterMatchmakingQueues
- `include` (query, optional): comma-separated list of relationships to include
- `limit[matchmakingQueues]` (query, optional): maximum number of related matchmakingQueues returned (when they are included)
- `limit[rules]` (query, optional): maximum number of related rules returned (when they are included)
- `limit[teams]` (query, optional): maximum number of related teams returned (when they are included)

### `PATCH /v1/gameCenterMatchmakingRuleSets/{id}`
**Summary**: No summary provided.

### `DELETE /v1/gameCenterMatchmakingRuleSets/{id}`
**Summary**: No summary provided.

### `POST /v1/gameCenterMatchmakingRules`
**Summary**: No summary provided.

### `PATCH /v1/gameCenterMatchmakingRules/{id}`
**Summary**: No summary provided.

### `DELETE /v1/gameCenterMatchmakingRules/{id}`
**Summary**: No summary provided.

### `POST /v1/gameCenterMatchmakingTeams`
**Summary**: No summary provided.

### `PATCH /v1/gameCenterMatchmakingTeams/{id}`
**Summary**: No summary provided.

### `DELETE /v1/gameCenterMatchmakingTeams/{id}`
**Summary**: No summary provided.

### `POST /v1/gameCenterPlayerAchievementSubmissions`
**Summary**: No summary provided.

### `GET /v1/gameCenterAchievementLocalizations/{id}/relationships/gameCenterAchievement`
**Summary**: No summary provided.

### `GET /v1/gameCenterAchievementLocalizations/{id}/gameCenterAchievement`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterAchievements]` (query, optional): the fields to include for returned resources of type gameCenterAchievements
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterGroups]` (query, optional): the fields to include for returned resources of type gameCenterGroups
- `fields[gameCenterAchievementLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterAchievementLocalizations
- `fields[gameCenterAchievementReleases]` (query, optional): the fields to include for returned resources of type gameCenterAchievementReleases
- `fields[gameCenterActivities]` (query, optional): the fields to include for returned resources of type gameCenterActivities
- `include` (query, optional): comma-separated list of relationships to include
- `limit[localizations]` (query, optional): maximum number of related localizations returned (when they are included)
- `limit[releases]` (query, optional): maximum number of related releases returned (when they are included)

### `GET /v1/gameCenterAchievementLocalizations/{id}/relationships/gameCenterAchievementImage`
**Summary**: No summary provided.

### `GET /v1/gameCenterAchievementLocalizations/{id}/gameCenterAchievementImage`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterAchievementImages]` (query, optional): the fields to include for returned resources of type gameCenterAchievementImages
- `fields[gameCenterAchievementLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterAchievementLocalizations
- `include` (query, optional): comma-separated list of relationships to include

### `PATCH /v1/gameCenterAchievements/{id}/relationships/activity`
**Summary**: No summary provided.

### `GET /v1/gameCenterAchievements/{id}/relationships/groupAchievement`
**Summary**: No summary provided.

### `PATCH /v1/gameCenterAchievements/{id}/relationships/groupAchievement`
**Summary**: No summary provided.

### `GET /v1/gameCenterAchievements/{id}/groupAchievement`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterAchievements]` (query, optional): the fields to include for returned resources of type gameCenterAchievements
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterGroups]` (query, optional): the fields to include for returned resources of type gameCenterGroups
- `fields[gameCenterAchievementLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterAchievementLocalizations
- `fields[gameCenterAchievementReleases]` (query, optional): the fields to include for returned resources of type gameCenterAchievementReleases
- `fields[gameCenterActivities]` (query, optional): the fields to include for returned resources of type gameCenterActivities
- `include` (query, optional): comma-separated list of relationships to include
- `limit[localizations]` (query, optional): maximum number of related localizations returned (when they are included)
- `limit[releases]` (query, optional): maximum number of related releases returned (when they are included)

### `GET /v1/gameCenterAchievements/{id}/relationships/localizations`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/gameCenterAchievements/{id}/localizations`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterAchievementLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterAchievementLocalizations
- `fields[gameCenterAchievements]` (query, optional): the fields to include for returned resources of type gameCenterAchievements
- `fields[gameCenterAchievementImages]` (query, optional): the fields to include for returned resources of type gameCenterAchievementImages
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include

### `GET /v1/gameCenterAchievements/{id}/relationships/releases`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/gameCenterAchievements/{id}/releases`
**Summary**: No summary provided.

**Parameters**:
- `filter[live]` (query, optional): filter by attribute 'live'
- `filter[gameCenterDetail]` (query, optional): filter by id(s) of related 'gameCenterDetail'
- `fields[gameCenterAchievementReleases]` (query, optional): the fields to include for returned resources of type gameCenterAchievementReleases
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterAchievements]` (query, optional): the fields to include for returned resources of type gameCenterAchievements
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include

### `POST /v1/gameCenterActivities/{id}/relationships/achievements`
**Summary**: No summary provided.

### `DELETE /v1/gameCenterActivities/{id}/relationships/achievements`
**Summary**: No summary provided.

### `POST /v1/gameCenterActivities/{id}/relationships/achievementsV2`
**Summary**: No summary provided.

### `DELETE /v1/gameCenterActivities/{id}/relationships/achievementsV2`
**Summary**: No summary provided.

### `POST /v1/gameCenterActivities/{id}/relationships/leaderboards`
**Summary**: No summary provided.

### `DELETE /v1/gameCenterActivities/{id}/relationships/leaderboards`
**Summary**: No summary provided.

### `POST /v1/gameCenterActivities/{id}/relationships/leaderboardsV2`
**Summary**: No summary provided.

### `DELETE /v1/gameCenterActivities/{id}/relationships/leaderboardsV2`
**Summary**: No summary provided.

### `GET /v1/gameCenterActivities/{id}/relationships/versions`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/gameCenterActivities/{id}/versions`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterActivityVersions]` (query, optional): the fields to include for returned resources of type gameCenterActivityVersions
- `fields[gameCenterActivities]` (query, optional): the fields to include for returned resources of type gameCenterActivities
- `fields[gameCenterActivityLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterActivityLocalizations
- `fields[gameCenterActivityImages]` (query, optional): the fields to include for returned resources of type gameCenterActivityImages
- `fields[gameCenterActivityVersionReleases]` (query, optional): the fields to include for returned resources of type gameCenterActivityVersionReleases
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[localizations]` (query, optional): maximum number of related localizations returned (when they are included)
- `limit[releases]` (query, optional): maximum number of related releases returned (when they are included)

### `GET /v1/gameCenterActivityLocalizations/{id}/relationships/image`
**Summary**: No summary provided.

### `GET /v1/gameCenterActivityLocalizations/{id}/image`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterActivityImages]` (query, optional): the fields to include for returned resources of type gameCenterActivityImages

### `GET /v1/gameCenterActivityVersions/{id}/relationships/defaultImage`
**Summary**: No summary provided.

### `GET /v1/gameCenterActivityVersions/{id}/defaultImage`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterActivityImages]` (query, optional): the fields to include for returned resources of type gameCenterActivityImages

### `GET /v1/gameCenterActivityVersions/{id}/relationships/localizations`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/gameCenterActivityVersions/{id}/localizations`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterActivityLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterActivityLocalizations
- `fields[gameCenterActivityVersions]` (query, optional): the fields to include for returned resources of type gameCenterActivityVersions
- `fields[gameCenterActivityImages]` (query, optional): the fields to include for returned resources of type gameCenterActivityImages
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include

### `GET /v1/gameCenterAppVersions/{id}/relationships/appStoreVersion`
**Summary**: No summary provided.

### `GET /v1/gameCenterAppVersions/{id}/appStoreVersion`
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

### `GET /v1/gameCenterAppVersions/{id}/relationships/compatibilityVersions`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `POST /v1/gameCenterAppVersions/{id}/relationships/compatibilityVersions`
**Summary**: No summary provided.

### `DELETE /v1/gameCenterAppVersions/{id}/relationships/compatibilityVersions`
**Summary**: No summary provided.

### `GET /v1/gameCenterAppVersions/{id}/compatibilityVersions`
**Summary**: No summary provided.

**Parameters**:
- `filter[enabled]` (query, optional): filter by attribute 'enabled'
- `fields[gameCenterAppVersions]` (query, optional): the fields to include for returned resources of type gameCenterAppVersions
- `fields[appStoreVersions]` (query, optional): the fields to include for returned resources of type appStoreVersions
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[compatibilityVersions]` (query, optional): maximum number of related compatibilityVersions returned (when they are included)

### `GET /v1/gameCenterChallengeLocalizations/{id}/relationships/image`
**Summary**: No summary provided.

### `GET /v1/gameCenterChallengeLocalizations/{id}/image`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterChallengeImages]` (query, optional): the fields to include for returned resources of type gameCenterChallengeImages

### `GET /v1/gameCenterChallengeVersions/{id}/relationships/defaultImage`
**Summary**: No summary provided.

### `GET /v1/gameCenterChallengeVersions/{id}/defaultImage`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterChallengeImages]` (query, optional): the fields to include for returned resources of type gameCenterChallengeImages

### `GET /v1/gameCenterChallengeVersions/{id}/relationships/localizations`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/gameCenterChallengeVersions/{id}/localizations`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterChallengeLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterChallengeLocalizations
- `fields[gameCenterChallengeVersions]` (query, optional): the fields to include for returned resources of type gameCenterChallengeVersions
- `fields[gameCenterChallengeImages]` (query, optional): the fields to include for returned resources of type gameCenterChallengeImages
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include

### `PATCH /v1/gameCenterChallenges/{id}/relationships/leaderboard`
**Summary**: No summary provided.

### `PATCH /v1/gameCenterChallenges/{id}/relationships/leaderboardV2`
**Summary**: No summary provided.

### `GET /v1/gameCenterChallenges/{id}/relationships/versions`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/gameCenterChallenges/{id}/versions`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterChallengeVersions]` (query, optional): the fields to include for returned resources of type gameCenterChallengeVersions
- `fields[gameCenterChallenges]` (query, optional): the fields to include for returned resources of type gameCenterChallenges
- `fields[gameCenterChallengeLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterChallengeLocalizations
- `fields[gameCenterChallengeVersionReleases]` (query, optional): the fields to include for returned resources of type gameCenterChallengeVersionReleases
- `fields[gameCenterChallengeImages]` (query, optional): the fields to include for returned resources of type gameCenterChallengeImages
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[localizations]` (query, optional): maximum number of related localizations returned (when they are included)
- `limit[releases]` (query, optional): maximum number of related releases returned (when they are included)

### `GET /v1/gameCenterDetails/{id}/relationships/achievementReleases`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/gameCenterDetails/{id}/achievementReleases`
**Summary**: No summary provided.

**Parameters**:
- `filter[live]` (query, optional): filter by attribute 'live'
- `filter[gameCenterAchievement]` (query, optional): filter by id(s) of related 'gameCenterAchievement'
- `fields[gameCenterAchievementReleases]` (query, optional): the fields to include for returned resources of type gameCenterAchievementReleases
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterAchievements]` (query, optional): the fields to include for returned resources of type gameCenterAchievements
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include

### `GET /v1/gameCenterDetails/{id}/relationships/activityReleases`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/gameCenterDetails/{id}/activityReleases`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterActivityVersionReleases]` (query, optional): the fields to include for returned resources of type gameCenterActivityVersionReleases
- `fields[gameCenterActivityVersions]` (query, optional): the fields to include for returned resources of type gameCenterActivityVersions
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include

### `GET /v1/gameCenterDetails/{id}/relationships/challengeReleases`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/gameCenterDetails/{id}/challengeReleases`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterChallengeVersionReleases]` (query, optional): the fields to include for returned resources of type gameCenterChallengeVersionReleases
- `fields[gameCenterChallengeVersions]` (query, optional): the fields to include for returned resources of type gameCenterChallengeVersions
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include

### `PATCH /v1/gameCenterDetails/{id}/relationships/challengesMinimumPlatformVersions`
**Summary**: No summary provided.

### `GET /v1/gameCenterDetails/{id}/relationships/gameCenterAchievements`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `PATCH /v1/gameCenterDetails/{id}/relationships/gameCenterAchievements`
**Summary**: No summary provided.

### `GET /v1/gameCenterDetails/{id}/gameCenterAchievements`
**Summary**: No summary provided.

**Parameters**:
- `filter[referenceName]` (query, optional): filter by attribute 'referenceName'
- `filter[archived]` (query, optional): filter by attribute 'archived'
- `filter[id]` (query, optional): filter by id(s)
- `fields[gameCenterAchievements]` (query, optional): the fields to include for returned resources of type gameCenterAchievements
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterGroups]` (query, optional): the fields to include for returned resources of type gameCenterGroups
- `fields[gameCenterAchievementLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterAchievementLocalizations
- `fields[gameCenterAchievementReleases]` (query, optional): the fields to include for returned resources of type gameCenterAchievementReleases
- `fields[gameCenterActivities]` (query, optional): the fields to include for returned resources of type gameCenterActivities
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[localizations]` (query, optional): maximum number of related localizations returned (when they are included)
- `limit[releases]` (query, optional): maximum number of related releases returned (when they are included)

### `GET /v1/gameCenterDetails/{id}/relationships/gameCenterAchievementsV2`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `PATCH /v1/gameCenterDetails/{id}/relationships/gameCenterAchievementsV2`
**Summary**: No summary provided.

### `GET /v1/gameCenterDetails/{id}/gameCenterAchievementsV2`
**Summary**: No summary provided.

**Parameters**:
- `filter[referenceName]` (query, optional): filter by attribute 'referenceName'
- `filter[archived]` (query, optional): filter by attribute 'archived'
- `filter[id]` (query, optional): filter by id(s)
- `fields[gameCenterAchievements]` (query, optional): the fields to include for returned resources of type gameCenterAchievements
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterGroups]` (query, optional): the fields to include for returned resources of type gameCenterGroups
- `fields[gameCenterActivities]` (query, optional): the fields to include for returned resources of type gameCenterActivities
- `fields[gameCenterAchievementVersions]` (query, optional): the fields to include for returned resources of type gameCenterAchievementVersions
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[versions]` (query, optional): maximum number of related versions returned (when they are included)

### `GET /v1/gameCenterDetails/{id}/relationships/gameCenterActivities`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/gameCenterDetails/{id}/gameCenterActivities`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterActivities]` (query, optional): the fields to include for returned resources of type gameCenterActivities
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterGroups]` (query, optional): the fields to include for returned resources of type gameCenterGroups
- `fields[gameCenterAchievements]` (query, optional): the fields to include for returned resources of type gameCenterAchievements
- `fields[gameCenterLeaderboards]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboards
- `fields[gameCenterActivityVersions]` (query, optional): the fields to include for returned resources of type gameCenterActivityVersions
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[achievements]` (query, optional): maximum number of related achievements returned (when they are included)
- `limit[achievementsV2]` (query, optional): maximum number of related achievementsV2 returned (when they are included)
- `limit[leaderboards]` (query, optional): maximum number of related leaderboards returned (when they are included)
- `limit[leaderboardsV2]` (query, optional): maximum number of related leaderboardsV2 returned (when they are included)
- `limit[versions]` (query, optional): maximum number of related versions returned (when they are included)

### `GET /v1/gameCenterDetails/{id}/relationships/gameCenterAppVersions`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/gameCenterDetails/{id}/gameCenterAppVersions`
**Summary**: No summary provided.

**Parameters**:
- `filter[enabled]` (query, optional): filter by attribute 'enabled'
- `fields[gameCenterAppVersions]` (query, optional): the fields to include for returned resources of type gameCenterAppVersions
- `fields[appStoreVersions]` (query, optional): the fields to include for returned resources of type appStoreVersions
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[compatibilityVersions]` (query, optional): maximum number of related compatibilityVersions returned (when they are included)

### `GET /v1/gameCenterDetails/{id}/relationships/gameCenterChallenges`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/gameCenterDetails/{id}/gameCenterChallenges`
**Summary**: No summary provided.

**Parameters**:
- `filter[referenceName]` (query, optional): filter by attribute 'referenceName'
- `filter[archived]` (query, optional): filter by attribute 'archived'
- `filter[id]` (query, optional): filter by id(s)
- `fields[gameCenterChallenges]` (query, optional): the fields to include for returned resources of type gameCenterChallenges
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterGroups]` (query, optional): the fields to include for returned resources of type gameCenterGroups
- `fields[gameCenterChallengeVersions]` (query, optional): the fields to include for returned resources of type gameCenterChallengeVersions
- `fields[gameCenterLeaderboards]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboards
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[versions]` (query, optional): maximum number of related versions returned (when they are included)

### `GET /v1/gameCenterDetails/{id}/relationships/gameCenterGroup`
**Summary**: No summary provided.

### `GET /v1/gameCenterDetails/{id}/gameCenterGroup`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterGroups]` (query, optional): the fields to include for returned resources of type gameCenterGroups
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterLeaderboards]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboards
- `fields[gameCenterLeaderboardSets]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSets
- `fields[gameCenterAchievements]` (query, optional): the fields to include for returned resources of type gameCenterAchievements
- `fields[gameCenterActivities]` (query, optional): the fields to include for returned resources of type gameCenterActivities
- `fields[gameCenterChallenges]` (query, optional): the fields to include for returned resources of type gameCenterChallenges
- `include` (query, optional): comma-separated list of relationships to include
- `limit[gameCenterDetails]` (query, optional): maximum number of related gameCenterDetails returned (when they are included)
- `limit[gameCenterLeaderboards]` (query, optional): maximum number of related gameCenterLeaderboards returned (when they are included)
- `limit[gameCenterLeaderboardsV2]` (query, optional): maximum number of related gameCenterLeaderboardsV2 returned (when they are included)
- `limit[gameCenterLeaderboardSets]` (query, optional): maximum number of related gameCenterLeaderboardSets returned (when they are included)
- `limit[gameCenterLeaderboardSetsV2]` (query, optional): maximum number of related gameCenterLeaderboardSetsV2 returned (when they are included)
- `limit[gameCenterAchievements]` (query, optional): maximum number of related gameCenterAchievements returned (when they are included)
- `limit[gameCenterAchievementsV2]` (query, optional): maximum number of related gameCenterAchievementsV2 returned (when they are included)
- `limit[gameCenterActivities]` (query, optional): maximum number of related gameCenterActivities returned (when they are included)
- `limit[gameCenterChallenges]` (query, optional): maximum number of related gameCenterChallenges returned (when they are included)

### `GET /v1/gameCenterDetails/{id}/relationships/gameCenterLeaderboardSets`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `PATCH /v1/gameCenterDetails/{id}/relationships/gameCenterLeaderboardSets`
**Summary**: No summary provided.

### `GET /v1/gameCenterDetails/{id}/gameCenterLeaderboardSets`
**Summary**: No summary provided.

**Parameters**:
- `filter[referenceName]` (query, optional): filter by attribute 'referenceName'
- `filter[id]` (query, optional): filter by id(s)
- `fields[gameCenterLeaderboardSets]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSets
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterGroups]` (query, optional): the fields to include for returned resources of type gameCenterGroups
- `fields[gameCenterLeaderboardSetLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSetLocalizations
- `fields[gameCenterLeaderboards]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboards
- `fields[gameCenterLeaderboardSetReleases]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSetReleases
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[localizations]` (query, optional): maximum number of related localizations returned (when they are included)
- `limit[gameCenterLeaderboards]` (query, optional): maximum number of related gameCenterLeaderboards returned (when they are included)
- `limit[releases]` (query, optional): maximum number of related releases returned (when they are included)

### `GET /v1/gameCenterDetails/{id}/relationships/gameCenterLeaderboardSetsV2`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `PATCH /v1/gameCenterDetails/{id}/relationships/gameCenterLeaderboardSetsV2`
**Summary**: No summary provided.

### `GET /v1/gameCenterDetails/{id}/gameCenterLeaderboardSetsV2`
**Summary**: No summary provided.

**Parameters**:
- `filter[referenceName]` (query, optional): filter by attribute 'referenceName'
- `filter[id]` (query, optional): filter by id(s)
- `fields[gameCenterLeaderboardSets]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSets
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterGroups]` (query, optional): the fields to include for returned resources of type gameCenterGroups
- `fields[gameCenterLeaderboards]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboards
- `fields[gameCenterLeaderboardSetVersions]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSetVersions
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[gameCenterLeaderboards]` (query, optional): maximum number of related gameCenterLeaderboards returned (when they are included)
- `limit[versions]` (query, optional): maximum number of related versions returned (when they are included)

### `GET /v1/gameCenterDetails/{id}/relationships/gameCenterLeaderboards`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `PATCH /v1/gameCenterDetails/{id}/relationships/gameCenterLeaderboards`
**Summary**: No summary provided.

### `GET /v1/gameCenterDetails/{id}/gameCenterLeaderboards`
**Summary**: No summary provided.

**Parameters**:
- `filter[referenceName]` (query, optional): filter by attribute 'referenceName'
- `filter[archived]` (query, optional): filter by attribute 'archived'
- `filter[id]` (query, optional): filter by id(s)
- `fields[gameCenterLeaderboards]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboards
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterGroups]` (query, optional): the fields to include for returned resources of type gameCenterGroups
- `fields[gameCenterLeaderboardSets]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSets
- `fields[gameCenterLeaderboardLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardLocalizations
- `fields[gameCenterLeaderboardReleases]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardReleases
- `fields[gameCenterActivities]` (query, optional): the fields to include for returned resources of type gameCenterActivities
- `fields[gameCenterChallenges]` (query, optional): the fields to include for returned resources of type gameCenterChallenges
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[gameCenterLeaderboardSets]` (query, optional): maximum number of related gameCenterLeaderboardSets returned (when they are included)
- `limit[localizations]` (query, optional): maximum number of related localizations returned (when they are included)
- `limit[releases]` (query, optional): maximum number of related releases returned (when they are included)

### `GET /v1/gameCenterDetails/{id}/relationships/gameCenterLeaderboardsV2`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `PATCH /v1/gameCenterDetails/{id}/relationships/gameCenterLeaderboardsV2`
**Summary**: No summary provided.

### `GET /v1/gameCenterDetails/{id}/gameCenterLeaderboardsV2`
**Summary**: No summary provided.

**Parameters**:
- `filter[referenceName]` (query, optional): filter by attribute 'referenceName'
- `filter[archived]` (query, optional): filter by attribute 'archived'
- `filter[id]` (query, optional): filter by id(s)
- `fields[gameCenterLeaderboards]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboards
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterGroups]` (query, optional): the fields to include for returned resources of type gameCenterGroups
- `fields[gameCenterLeaderboardSets]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSets
- `fields[gameCenterActivities]` (query, optional): the fields to include for returned resources of type gameCenterActivities
- `fields[gameCenterChallenges]` (query, optional): the fields to include for returned resources of type gameCenterChallenges
- `fields[gameCenterLeaderboardVersions]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardVersions
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[gameCenterLeaderboardSets]` (query, optional): maximum number of related gameCenterLeaderboardSets returned (when they are included)
- `limit[versions]` (query, optional): maximum number of related versions returned (when they are included)

### `GET /v1/gameCenterDetails/{id}/relationships/leaderboardReleases`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/gameCenterDetails/{id}/leaderboardReleases`
**Summary**: No summary provided.

**Parameters**:
- `filter[live]` (query, optional): filter by attribute 'live'
- `filter[gameCenterLeaderboard]` (query, optional): filter by id(s) of related 'gameCenterLeaderboard'
- `fields[gameCenterLeaderboardReleases]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardReleases
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterLeaderboards]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboards
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include

### `GET /v1/gameCenterDetails/{id}/relationships/leaderboardSetReleases`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/gameCenterDetails/{id}/leaderboardSetReleases`
**Summary**: No summary provided.

**Parameters**:
- `filter[live]` (query, optional): filter by attribute 'live'
- `filter[gameCenterLeaderboardSet]` (query, optional): filter by id(s) of related 'gameCenterLeaderboardSet'
- `fields[gameCenterLeaderboardSetReleases]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSetReleases
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterLeaderboardSets]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSets
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include

### `GET /v1/gameCenterEnabledVersions/{id}/relationships/compatibleVersions`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `POST /v1/gameCenterEnabledVersions/{id}/relationships/compatibleVersions`
**Summary**: No summary provided.

### `PATCH /v1/gameCenterEnabledVersions/{id}/relationships/compatibleVersions`
**Summary**: No summary provided.

### `DELETE /v1/gameCenterEnabledVersions/{id}/relationships/compatibleVersions`
**Summary**: No summary provided.

### `GET /v1/gameCenterEnabledVersions/{id}/compatibleVersions`
**Summary**: No summary provided.

**Parameters**:
- `filter[platform]` (query, optional): filter by attribute 'platform'
- `filter[versionString]` (query, optional): filter by attribute 'versionString'
- `filter[app]` (query, optional): filter by id(s) of related 'app'
- `filter[id]` (query, optional): filter by id(s)
- `sort` (query, optional): comma-separated list of sort expressions; resources will be sorted as specified
- `fields[gameCenterEnabledVersions]` (query, optional): the fields to include for returned resources of type gameCenterEnabledVersions
- `fields[apps]` (query, optional): the fields to include for returned resources of type apps
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[compatibleVersions]` (query, optional): maximum number of related compatibleVersions returned (when they are included)

### `GET /v1/gameCenterGroups/{id}/relationships/gameCenterAchievements`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `PATCH /v1/gameCenterGroups/{id}/relationships/gameCenterAchievements`
**Summary**: No summary provided.

### `GET /v1/gameCenterGroups/{id}/gameCenterAchievements`
**Summary**: No summary provided.

**Parameters**:
- `filter[referenceName]` (query, optional): filter by attribute 'referenceName'
- `filter[archived]` (query, optional): filter by attribute 'archived'
- `filter[id]` (query, optional): filter by id(s)
- `fields[gameCenterAchievements]` (query, optional): the fields to include for returned resources of type gameCenterAchievements
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterGroups]` (query, optional): the fields to include for returned resources of type gameCenterGroups
- `fields[gameCenterAchievementLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterAchievementLocalizations
- `fields[gameCenterAchievementReleases]` (query, optional): the fields to include for returned resources of type gameCenterAchievementReleases
- `fields[gameCenterActivities]` (query, optional): the fields to include for returned resources of type gameCenterActivities
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[localizations]` (query, optional): maximum number of related localizations returned (when they are included)
- `limit[releases]` (query, optional): maximum number of related releases returned (when they are included)

### `GET /v1/gameCenterGroups/{id}/relationships/gameCenterAchievementsV2`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `PATCH /v1/gameCenterGroups/{id}/relationships/gameCenterAchievementsV2`
**Summary**: No summary provided.

### `GET /v1/gameCenterGroups/{id}/gameCenterAchievementsV2`
**Summary**: No summary provided.

**Parameters**:
- `filter[referenceName]` (query, optional): filter by attribute 'referenceName'
- `filter[archived]` (query, optional): filter by attribute 'archived'
- `filter[id]` (query, optional): filter by id(s)
- `fields[gameCenterAchievements]` (query, optional): the fields to include for returned resources of type gameCenterAchievements
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterGroups]` (query, optional): the fields to include for returned resources of type gameCenterGroups
- `fields[gameCenterActivities]` (query, optional): the fields to include for returned resources of type gameCenterActivities
- `fields[gameCenterAchievementVersions]` (query, optional): the fields to include for returned resources of type gameCenterAchievementVersions
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[versions]` (query, optional): maximum number of related versions returned (when they are included)

### `GET /v1/gameCenterGroups/{id}/relationships/gameCenterActivities`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/gameCenterGroups/{id}/gameCenterActivities`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterActivities]` (query, optional): the fields to include for returned resources of type gameCenterActivities
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterGroups]` (query, optional): the fields to include for returned resources of type gameCenterGroups
- `fields[gameCenterAchievements]` (query, optional): the fields to include for returned resources of type gameCenterAchievements
- `fields[gameCenterLeaderboards]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboards
- `fields[gameCenterActivityVersions]` (query, optional): the fields to include for returned resources of type gameCenterActivityVersions
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[achievements]` (query, optional): maximum number of related achievements returned (when they are included)
- `limit[achievementsV2]` (query, optional): maximum number of related achievementsV2 returned (when they are included)
- `limit[leaderboards]` (query, optional): maximum number of related leaderboards returned (when they are included)
- `limit[leaderboardsV2]` (query, optional): maximum number of related leaderboardsV2 returned (when they are included)
- `limit[versions]` (query, optional): maximum number of related versions returned (when they are included)

### `GET /v1/gameCenterGroups/{id}/relationships/gameCenterChallenges`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/gameCenterGroups/{id}/gameCenterChallenges`
**Summary**: No summary provided.

**Parameters**:
- `filter[referenceName]` (query, optional): filter by attribute 'referenceName'
- `filter[archived]` (query, optional): filter by attribute 'archived'
- `filter[id]` (query, optional): filter by id(s)
- `fields[gameCenterChallenges]` (query, optional): the fields to include for returned resources of type gameCenterChallenges
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterGroups]` (query, optional): the fields to include for returned resources of type gameCenterGroups
- `fields[gameCenterChallengeVersions]` (query, optional): the fields to include for returned resources of type gameCenterChallengeVersions
- `fields[gameCenterLeaderboards]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboards
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[versions]` (query, optional): maximum number of related versions returned (when they are included)

### `GET /v1/gameCenterGroups/{id}/relationships/gameCenterDetails`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/gameCenterGroups/{id}/gameCenterDetails`
**Summary**: No summary provided.

**Parameters**:
- `filter[gameCenterAppVersions.enabled]` (query, optional): filter by attribute 'gameCenterAppVersions.enabled'
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
- `limit` (query, optional): maximum resources per page
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

### `GET /v1/gameCenterGroups/{id}/relationships/gameCenterLeaderboardSets`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `PATCH /v1/gameCenterGroups/{id}/relationships/gameCenterLeaderboardSets`
**Summary**: No summary provided.

### `GET /v1/gameCenterGroups/{id}/gameCenterLeaderboardSets`
**Summary**: No summary provided.

**Parameters**:
- `filter[referenceName]` (query, optional): filter by attribute 'referenceName'
- `filter[id]` (query, optional): filter by id(s)
- `fields[gameCenterLeaderboardSets]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSets
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterGroups]` (query, optional): the fields to include for returned resources of type gameCenterGroups
- `fields[gameCenterLeaderboardSetLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSetLocalizations
- `fields[gameCenterLeaderboards]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboards
- `fields[gameCenterLeaderboardSetReleases]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSetReleases
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[localizations]` (query, optional): maximum number of related localizations returned (when they are included)
- `limit[gameCenterLeaderboards]` (query, optional): maximum number of related gameCenterLeaderboards returned (when they are included)
- `limit[releases]` (query, optional): maximum number of related releases returned (when they are included)

### `GET /v1/gameCenterGroups/{id}/relationships/gameCenterLeaderboardSetsV2`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `PATCH /v1/gameCenterGroups/{id}/relationships/gameCenterLeaderboardSetsV2`
**Summary**: No summary provided.

### `GET /v1/gameCenterGroups/{id}/gameCenterLeaderboardSetsV2`
**Summary**: No summary provided.

**Parameters**:
- `filter[referenceName]` (query, optional): filter by attribute 'referenceName'
- `filter[id]` (query, optional): filter by id(s)
- `fields[gameCenterLeaderboardSets]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSets
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterGroups]` (query, optional): the fields to include for returned resources of type gameCenterGroups
- `fields[gameCenterLeaderboards]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboards
- `fields[gameCenterLeaderboardSetVersions]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSetVersions
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[gameCenterLeaderboards]` (query, optional): maximum number of related gameCenterLeaderboards returned (when they are included)
- `limit[versions]` (query, optional): maximum number of related versions returned (when they are included)

### `GET /v1/gameCenterGroups/{id}/relationships/gameCenterLeaderboards`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `PATCH /v1/gameCenterGroups/{id}/relationships/gameCenterLeaderboards`
**Summary**: No summary provided.

### `GET /v1/gameCenterGroups/{id}/gameCenterLeaderboards`
**Summary**: No summary provided.

**Parameters**:
- `filter[referenceName]` (query, optional): filter by attribute 'referenceName'
- `filter[archived]` (query, optional): filter by attribute 'archived'
- `filter[id]` (query, optional): filter by id(s)
- `fields[gameCenterLeaderboards]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboards
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterGroups]` (query, optional): the fields to include for returned resources of type gameCenterGroups
- `fields[gameCenterLeaderboardSets]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSets
- `fields[gameCenterLeaderboardLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardLocalizations
- `fields[gameCenterLeaderboardReleases]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardReleases
- `fields[gameCenterActivities]` (query, optional): the fields to include for returned resources of type gameCenterActivities
- `fields[gameCenterChallenges]` (query, optional): the fields to include for returned resources of type gameCenterChallenges
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[gameCenterLeaderboardSets]` (query, optional): maximum number of related gameCenterLeaderboardSets returned (when they are included)
- `limit[localizations]` (query, optional): maximum number of related localizations returned (when they are included)
- `limit[releases]` (query, optional): maximum number of related releases returned (when they are included)

### `GET /v1/gameCenterGroups/{id}/relationships/gameCenterLeaderboardsV2`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `PATCH /v1/gameCenterGroups/{id}/relationships/gameCenterLeaderboardsV2`
**Summary**: No summary provided.

### `GET /v1/gameCenterGroups/{id}/gameCenterLeaderboardsV2`
**Summary**: No summary provided.

**Parameters**:
- `filter[referenceName]` (query, optional): filter by attribute 'referenceName'
- `filter[archived]` (query, optional): filter by attribute 'archived'
- `filter[id]` (query, optional): filter by id(s)
- `fields[gameCenterLeaderboards]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboards
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterGroups]` (query, optional): the fields to include for returned resources of type gameCenterGroups
- `fields[gameCenterLeaderboardSets]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSets
- `fields[gameCenterActivities]` (query, optional): the fields to include for returned resources of type gameCenterActivities
- `fields[gameCenterChallenges]` (query, optional): the fields to include for returned resources of type gameCenterChallenges
- `fields[gameCenterLeaderboardVersions]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardVersions
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[gameCenterLeaderboardSets]` (query, optional): maximum number of related gameCenterLeaderboardSets returned (when they are included)
- `limit[versions]` (query, optional): maximum number of related versions returned (when they are included)

### `GET /v1/gameCenterLeaderboardLocalizations/{id}/relationships/gameCenterLeaderboardImage`
**Summary**: No summary provided.

### `GET /v1/gameCenterLeaderboardLocalizations/{id}/gameCenterLeaderboardImage`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterLeaderboardImages]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardImages
- `fields[gameCenterLeaderboardLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardLocalizations
- `include` (query, optional): comma-separated list of relationships to include

### `GET /v1/gameCenterLeaderboardSetLocalizations/{id}/relationships/gameCenterLeaderboardSetImage`
**Summary**: No summary provided.

### `GET /v1/gameCenterLeaderboardSetLocalizations/{id}/gameCenterLeaderboardSetImage`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterLeaderboardSetImages]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSetImages
- `fields[gameCenterLeaderboardSetLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSetLocalizations
- `include` (query, optional): comma-separated list of relationships to include

### `GET /v1/gameCenterLeaderboardSetMemberLocalizations/{id}/relationships/gameCenterLeaderboard`
**Summary**: No summary provided.

### `GET /v1/gameCenterLeaderboardSetMemberLocalizations/{id}/gameCenterLeaderboard`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterLeaderboards]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboards
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterGroups]` (query, optional): the fields to include for returned resources of type gameCenterGroups
- `fields[gameCenterLeaderboardSets]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSets
- `fields[gameCenterLeaderboardLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardLocalizations
- `fields[gameCenterLeaderboardReleases]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardReleases
- `fields[gameCenterActivities]` (query, optional): the fields to include for returned resources of type gameCenterActivities
- `fields[gameCenterChallenges]` (query, optional): the fields to include for returned resources of type gameCenterChallenges
- `include` (query, optional): comma-separated list of relationships to include
- `limit[gameCenterLeaderboardSets]` (query, optional): maximum number of related gameCenterLeaderboardSets returned (when they are included)
- `limit[localizations]` (query, optional): maximum number of related localizations returned (when they are included)
- `limit[releases]` (query, optional): maximum number of related releases returned (when they are included)

### `GET /v1/gameCenterLeaderboardSetMemberLocalizations/{id}/relationships/gameCenterLeaderboardSet`
**Summary**: No summary provided.

### `GET /v1/gameCenterLeaderboardSetMemberLocalizations/{id}/gameCenterLeaderboardSet`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterLeaderboardSets]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSets
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterGroups]` (query, optional): the fields to include for returned resources of type gameCenterGroups
- `fields[gameCenterLeaderboardSetLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSetLocalizations
- `fields[gameCenterLeaderboards]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboards
- `fields[gameCenterLeaderboardSetReleases]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSetReleases
- `include` (query, optional): comma-separated list of relationships to include
- `limit[localizations]` (query, optional): maximum number of related localizations returned (when they are included)
- `limit[gameCenterLeaderboards]` (query, optional): maximum number of related gameCenterLeaderboards returned (when they are included)
- `limit[releases]` (query, optional): maximum number of related releases returned (when they are included)

### `GET /v1/gameCenterLeaderboardSets/{id}/relationships/gameCenterLeaderboards`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `POST /v1/gameCenterLeaderboardSets/{id}/relationships/gameCenterLeaderboards`
**Summary**: No summary provided.

### `PATCH /v1/gameCenterLeaderboardSets/{id}/relationships/gameCenterLeaderboards`
**Summary**: No summary provided.

### `DELETE /v1/gameCenterLeaderboardSets/{id}/relationships/gameCenterLeaderboards`
**Summary**: No summary provided.

### `GET /v1/gameCenterLeaderboardSets/{id}/gameCenterLeaderboards`
**Summary**: No summary provided.

**Parameters**:
- `filter[referenceName]` (query, optional): filter by attribute 'referenceName'
- `filter[archived]` (query, optional): filter by attribute 'archived'
- `filter[id]` (query, optional): filter by id(s)
- `fields[gameCenterLeaderboards]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboards
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterGroups]` (query, optional): the fields to include for returned resources of type gameCenterGroups
- `fields[gameCenterLeaderboardSets]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSets
- `fields[gameCenterLeaderboardLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardLocalizations
- `fields[gameCenterLeaderboardReleases]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardReleases
- `fields[gameCenterActivities]` (query, optional): the fields to include for returned resources of type gameCenterActivities
- `fields[gameCenterChallenges]` (query, optional): the fields to include for returned resources of type gameCenterChallenges
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include
- `limit[gameCenterLeaderboardSets]` (query, optional): maximum number of related gameCenterLeaderboardSets returned (when they are included)
- `limit[localizations]` (query, optional): maximum number of related localizations returned (when they are included)
- `limit[releases]` (query, optional): maximum number of related releases returned (when they are included)

### `GET /v1/gameCenterLeaderboardSets/{id}/relationships/groupLeaderboardSet`
**Summary**: No summary provided.

### `PATCH /v1/gameCenterLeaderboardSets/{id}/relationships/groupLeaderboardSet`
**Summary**: No summary provided.

### `GET /v1/gameCenterLeaderboardSets/{id}/groupLeaderboardSet`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterLeaderboardSets]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSets
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterGroups]` (query, optional): the fields to include for returned resources of type gameCenterGroups
- `fields[gameCenterLeaderboardSetLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSetLocalizations
- `fields[gameCenterLeaderboards]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboards
- `fields[gameCenterLeaderboardSetReleases]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSetReleases
- `include` (query, optional): comma-separated list of relationships to include
- `limit[localizations]` (query, optional): maximum number of related localizations returned (when they are included)
- `limit[gameCenterLeaderboards]` (query, optional): maximum number of related gameCenterLeaderboards returned (when they are included)
- `limit[releases]` (query, optional): maximum number of related releases returned (when they are included)

### `GET /v1/gameCenterLeaderboardSets/{id}/relationships/localizations`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/gameCenterLeaderboardSets/{id}/localizations`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterLeaderboardSetLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSetLocalizations
- `fields[gameCenterLeaderboardSets]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSets
- `fields[gameCenterLeaderboardSetImages]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSetImages
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include

### `GET /v1/gameCenterLeaderboardSets/{id}/relationships/releases`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/gameCenterLeaderboardSets/{id}/releases`
**Summary**: No summary provided.

**Parameters**:
- `filter[live]` (query, optional): filter by attribute 'live'
- `filter[gameCenterDetail]` (query, optional): filter by id(s) of related 'gameCenterDetail'
- `fields[gameCenterLeaderboardSetReleases]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSetReleases
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterLeaderboardSets]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSets
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include

### `PATCH /v1/gameCenterLeaderboards/{id}/relationships/activity`
**Summary**: No summary provided.

### `PATCH /v1/gameCenterLeaderboards/{id}/relationships/challenge`
**Summary**: No summary provided.

### `GET /v1/gameCenterLeaderboards/{id}/relationships/groupLeaderboard`
**Summary**: No summary provided.

### `PATCH /v1/gameCenterLeaderboards/{id}/relationships/groupLeaderboard`
**Summary**: No summary provided.

### `GET /v1/gameCenterLeaderboards/{id}/groupLeaderboard`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterLeaderboards]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboards
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterGroups]` (query, optional): the fields to include for returned resources of type gameCenterGroups
- `fields[gameCenterLeaderboardSets]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardSets
- `fields[gameCenterLeaderboardLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardLocalizations
- `fields[gameCenterLeaderboardReleases]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardReleases
- `fields[gameCenterActivities]` (query, optional): the fields to include for returned resources of type gameCenterActivities
- `fields[gameCenterChallenges]` (query, optional): the fields to include for returned resources of type gameCenterChallenges
- `include` (query, optional): comma-separated list of relationships to include
- `limit[gameCenterLeaderboardSets]` (query, optional): maximum number of related gameCenterLeaderboardSets returned (when they are included)
- `limit[localizations]` (query, optional): maximum number of related localizations returned (when they are included)
- `limit[releases]` (query, optional): maximum number of related releases returned (when they are included)

### `GET /v1/gameCenterLeaderboards/{id}/relationships/localizations`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/gameCenterLeaderboards/{id}/localizations`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterLeaderboardLocalizations]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardLocalizations
- `fields[gameCenterLeaderboards]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboards
- `fields[gameCenterLeaderboardImages]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardImages
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include

### `GET /v1/gameCenterLeaderboards/{id}/relationships/releases`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/gameCenterLeaderboards/{id}/releases`
**Summary**: No summary provided.

**Parameters**:
- `filter[live]` (query, optional): filter by attribute 'live'
- `filter[gameCenterDetail]` (query, optional): filter by id(s) of related 'gameCenterDetail'
- `fields[gameCenterLeaderboardReleases]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboardReleases
- `fields[gameCenterDetails]` (query, optional): the fields to include for returned resources of type gameCenterDetails
- `fields[gameCenterLeaderboards]` (query, optional): the fields to include for returned resources of type gameCenterLeaderboards
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include

### `GET /v1/gameCenterMatchmakingRuleSets/{id}/relationships/matchmakingQueues`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/gameCenterMatchmakingRuleSets/{id}/matchmakingQueues`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterMatchmakingQueues]` (query, optional): the fields to include for returned resources of type gameCenterMatchmakingQueues
- `fields[gameCenterMatchmakingRuleSets]` (query, optional): the fields to include for returned resources of type gameCenterMatchmakingRuleSets
- `limit` (query, optional): maximum resources per page
- `include` (query, optional): comma-separated list of relationships to include

### `GET /v1/gameCenterMatchmakingRuleSets/{id}/relationships/rules`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/gameCenterMatchmakingRuleSets/{id}/rules`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterMatchmakingRules]` (query, optional): the fields to include for returned resources of type gameCenterMatchmakingRules
- `limit` (query, optional): maximum resources per page

### `GET /v1/gameCenterMatchmakingRuleSets/{id}/relationships/teams`
**Summary**: No summary provided.

**Parameters**:
- `limit` (query, optional): maximum resources per page

### `GET /v1/gameCenterMatchmakingRuleSets/{id}/teams`
**Summary**: No summary provided.

**Parameters**:
- `fields[gameCenterMatchmakingTeams]` (query, optional): the fields to include for returned resources of type gameCenterMatchmakingTeams
- `limit` (query, optional): maximum resources per page

### `GET /v1/gameCenterDetails/{id}/metrics/classicMatchmakingRequests`
**Summary**: No summary provided.

**Parameters**:
- `granularity` (query, required): the granularity of the per-group dataset
- `groupBy` (query, optional): the dimension by which to group the results
- `filter[result]` (query, optional): filter by 'result' attribute dimension
- `sort` (query, optional): comma-separated list of sort expressions; metrics will be sorted as specified
- `limit` (query, optional): maximum number of groups to return per page

### `GET /v1/gameCenterDetails/{id}/metrics/ruleBasedMatchmakingRequests`
**Summary**: No summary provided.

**Parameters**:
- `granularity` (query, required): the granularity of the per-group dataset
- `groupBy` (query, optional): the dimension by which to group the results
- `filter[result]` (query, optional): filter by 'result' attribute dimension
- `sort` (query, optional): comma-separated list of sort expressions; metrics will be sorted as specified
- `limit` (query, optional): maximum number of groups to return per page

### `GET /v1/gameCenterMatchmakingQueues/{id}/metrics/experimentMatchmakingQueueSizes`
**Summary**: No summary provided.

**Parameters**:
- `granularity` (query, required): the granularity of the per-group dataset
- `sort` (query, optional): comma-separated list of sort expressions; metrics will be sorted as specified
- `limit` (query, optional): maximum number of groups to return per page

### `GET /v1/gameCenterMatchmakingQueues/{id}/metrics/experimentMatchmakingRequests`
**Summary**: No summary provided.

**Parameters**:
- `granularity` (query, required): the granularity of the per-group dataset
- `groupBy` (query, optional): the dimension by which to group the results
- `filter[result]` (query, optional): filter by 'result' attribute dimension
- `filter[gameCenterDetail]` (query, optional): filter by 'gameCenterDetail' relationship dimension
- `sort` (query, optional): comma-separated list of sort expressions; metrics will be sorted as specified
- `limit` (query, optional): maximum number of groups to return per page

### `GET /v1/gameCenterMatchmakingQueues/{id}/metrics/matchmakingQueueSizes`
**Summary**: No summary provided.

**Parameters**:
- `granularity` (query, required): the granularity of the per-group dataset
- `sort` (query, optional): comma-separated list of sort expressions; metrics will be sorted as specified
- `limit` (query, optional): maximum number of groups to return per page

### `GET /v1/gameCenterMatchmakingQueues/{id}/metrics/matchmakingRequests`
**Summary**: No summary provided.

**Parameters**:
- `granularity` (query, required): the granularity of the per-group dataset
- `groupBy` (query, optional): the dimension by which to group the results
- `filter[result]` (query, optional): filter by 'result' attribute dimension
- `filter[gameCenterDetail]` (query, optional): filter by 'gameCenterDetail' relationship dimension
- `sort` (query, optional): comma-separated list of sort expressions; metrics will be sorted as specified
- `limit` (query, optional): maximum number of groups to return per page

### `GET /v1/gameCenterMatchmakingQueues/{id}/metrics/matchmakingSessions`
**Summary**: No summary provided.

**Parameters**:
- `granularity` (query, required): the granularity of the per-group dataset
- `sort` (query, optional): comma-separated list of sort expressions; metrics will be sorted as specified
- `limit` (query, optional): maximum number of groups to return per page

### `GET /v1/gameCenterMatchmakingRules/{id}/metrics/matchmakingBooleanRuleResults`
**Summary**: No summary provided.

**Parameters**:
- `granularity` (query, required): the granularity of the per-group dataset
- `groupBy` (query, optional): the dimension by which to group the results
- `filter[result]` (query, optional): filter by 'result' attribute dimension
- `filter[gameCenterMatchmakingQueue]` (query, optional): filter by 'gameCenterMatchmakingQueue' relationship dimension
- `sort` (query, optional): comma-separated list of sort expressions; metrics will be sorted as specified
- `limit` (query, optional): maximum number of groups to return per page

### `GET /v1/gameCenterMatchmakingRules/{id}/metrics/matchmakingNumberRuleResults`
**Summary**: No summary provided.

**Parameters**:
- `granularity` (query, required): the granularity of the per-group dataset
- `groupBy` (query, optional): the dimension by which to group the results
- `filter[gameCenterMatchmakingQueue]` (query, optional): filter by 'gameCenterMatchmakingQueue' relationship dimension
- `sort` (query, optional): comma-separated list of sort expressions; metrics will be sorted as specified
- `limit` (query, optional): maximum number of groups to return per page

### `GET /v1/gameCenterMatchmakingRules/{id}/metrics/matchmakingRuleErrors`
**Summary**: No summary provided.

**Parameters**:
- `granularity` (query, required): the granularity of the per-group dataset
- `groupBy` (query, optional): the dimension by which to group the results
- `filter[gameCenterMatchmakingQueue]` (query, optional): filter by 'gameCenterMatchmakingQueue' relationship dimension
- `sort` (query, optional): comma-separated list of sort expressions; metrics will be sorted as specified
- `limit` (query, optional): maximum number of groups to return per page

## Typical Workflows
Use these endpoints to automate game center tasks within Apple Store Connect.

## Best Practices
- Always authenticate requests using your Apple Store Connect API key (JWT token).
- Handle rate limiting gracefully, as the Apple Store Connect API enforces quotas.
- When writing integrations, refer back to the exact schemas for precise payload construction.