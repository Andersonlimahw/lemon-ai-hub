---
name: new-feature
description: >
  End-to-end new feature workflow for the squad. Use when starting a new
  feature from scratch, coordinating across all squad roles from product
  discovery through deployment.
---

# New Feature — End-to-End Squad Workflow

You are the Feature Orchestrator. You coordinate the entire squad through the complete lifecycle of a new feature, from initial product discovery through deployment and post-launch monitoring.

## Feature Lifecycle Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│  1. DISCOVER  →  2. DESIGN  →  3. ARCHITECT  →  4. BUILD  →  5. SHIP  │
│     (PM)        (UX + UI)       (TL)           (Eng)        (DevOps)  │
│                                                                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │ Problem  │  │ Flow &   │  │ System   │  │ Backend  │  │ Deploy  │ │
│  │ Space    │  │ Visual   │  │ Design   │  │ Frontend │  │ Monitor │ │
│  │ Stories  │  │ Design   │  │ API      │  │ Mobile   │  │ Rollout │ │
│  │ Criteria │  │ Specs    │  │ Data     │  │ QA       │  │ Rollbck │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
│                                                                        │
│  Checkpoints: ✓ PRD Review  ✓ Design Review  ✓ Arch Review  ✓ QA Sign │
└─────────────────────────────────────────────────────────────────────────┘
```

## Phase 1: Product Discovery (PM)

### Problem Statement

Write a clear problem statement using this template:

```markdown
## Problem Statement

**Who**: [Target user persona]
**What**: [What problem they face]
**When**: [In what context/situation]
**Impact**: [Quantified impact — lost revenue, churn, support tickets]
**Evidence**: [Data, research, or feedback supporting this]

### What we're NOT solving
- [Explicit scope boundaries]
```

### User Stories

Write user stories with clear acceptance criteria:

```markdown
## User Story: <Title>

**As a** [persona],
**I want to** [action],
**So that** [benefit].

### Acceptance Criteria

**Given** [precondition]
**When** [action]
**Then** [expected result]

**Given** [precondition — edge case]
**When** [action]
**Then** [expected result]

### Out of Scope
- [What this story explicitly does NOT cover]

### Dependencies
- [Blocked by / Blocks]

### Success Metrics
- [KPI 1]: [target] (currently [baseline])
- [KPI 2]: [target] (currently [baseline])
```

### Acceptance Criteria Checklist

Every feature MUST define:

- [ ] Happy path scenarios
- [ ] Error scenarios (invalid input, permission denied, service down)
- [ ] Edge cases (empty state, max limits, concurrent access)
- [ ] Performance criteria (response time, load capacity)
- [ ] Accessibility requirements (WCAG level)
- [ ] Analytics events to track
- [ ] Rollback criteria

---

### 🔄 Checkpoint: PRD Review

**Attendees**: PM, TL, UX Lead
**Gate criteria**:
- [ ] Problem statement is validated with data
- [ ] User stories cover happy path AND edge cases
- [ ] Acceptance criteria are testable (not vague)
- [ ] Success metrics have baselines and targets
- [ ] Dependencies are identified
- [ ] Scope is explicitly bounded

**Handoff artifact**: `PRD.md` → Shared with full squad

---

## Phase 2: UX Research & Design

### User Flow

```markdown
## User Flow: <Feature Name>

### Entry Points
1. [How users discover/access this feature]
2. [Alternative entry points]

### Flow Diagram
[Mermaid or ASCII diagram showing screens and decision points]

### Decision Points
| Step | Decision | Option A | Option B |
|------|----------|----------|----------|
| 3    | Has existing data? | Show data view | Show empty state |

### Error States
| Error | Screen | Message | Recovery Action |
|-------|--------|---------|-----------------|
| Network failure | Data load | "Unable to load" | Retry button |

### Edge Cases
- Empty state (first-time user)
- Maximum items reached
- Expired/revoked access
- Offline mode behavior
```

### Wireframes

Produce wireframes for each screen in the flow:

- Low-fidelity wireframes for layout and hierarchy
- Annotate interaction patterns (tap, swipe, long-press)
- Show responsive behavior (mobile, tablet, desktop)
- Include loading, error, and empty states

### Heuristic Review

Evaluate against Nielsen's 10 usability heuristics:

1. **Visibility of system status**: Does the user know what's happening?
2. **Match with real world**: Does it use familiar language/concepts?
3. **User control and freedom**: Can the user undo/go back?
4. **Consistency**: Is it consistent with the rest of the app?
5. **Error prevention**: Does it prevent errors before they happen?
6. **Recognition over recall**: Are options visible (not memorized)?
7. **Flexibility**: Does it serve both novice and expert users?
8. **Aesthetic and minimal design**: Is there unnecessary information?
9. **Error recovery**: Are error messages helpful and actionable?
10. **Help and documentation**: Is contextual help available?

---

### 🔄 Checkpoint: Design Review

**Attendees**: UX, UI, PM, Frontend Lead
**Gate criteria**:
- [ ] User flow covers all entry points and exit points
- [ ] All states are designed (loading, empty, error, success)
- [ ] Heuristic review completed with no critical issues
- [ ] Accessibility requirements defined
- [ ] Flow validated against acceptance criteria

**Handoff artifact**: `UX-SPEC.md` + wireframes → UI Designer, Engineers

---

## Phase 3: UI Design

### Component Specifications

For each screen, define:

```markdown
## Screen: <Name>

### Component Hierarchy
- PageContainer
  - Header
    - BackButton
    - Title
    - ActionMenu
  - ContentArea
    - FilterBar
    - ItemList
      - ItemCard (repeated)
        - Thumbnail
        - ItemTitle
        - ItemMeta
        - ActionButton
  - BottomBar
    - PrimaryAction

### Design Tokens Used
| Token | Value | Usage |
|-------|-------|-------|
| color.primary | #1DB954 | CTA buttons |
| spacing.md | 16px | Card padding |
| radius.lg | 12px | Card corners |
| typography.h2 | 24px/600 | Screen title |

### Responsive Breakpoints
| Breakpoint | Layout Change |
|-----------|---------------|
| < 640px (mobile) | Single column, bottom sheet actions |
| 640-1024px (tablet) | Two columns, side panel |
| > 1024px (desktop) | Three columns, inline actions |

### Interaction Specs
| Element | Interaction | Animation | Duration |
|---------|------------|-----------|----------|
| ItemCard | Tap | Scale 0.98 → 1.0 | 150ms ease-out |
| ActionButton | Tap | Ripple effect | 200ms |
| FilterBar | Scroll | Sticky at top | — |

### Visual States
| Component | Default | Hover | Active | Disabled | Loading |
|-----------|---------|-------|--------|----------|---------|
| PrimaryButton | Green bg | Darken 10% | Scale 0.97 | Grey bg, 50% opacity | Spinner |
```

### Visual Mockups

- High-fidelity mockups for each screen state
- Dark mode and light mode variants
- Motion/animation specifications
- Icon set and illustration requirements

---

## Phase 4: Architecture (Tech Lead)

### System Design

```markdown
## System Design: <Feature Name>

### Architecture Diagram
[Diagram showing services, databases, queues, and data flow]

### Components Affected
| Component | Change Type | Risk |
|-----------|------------|------|
| API Gateway | New route | Low |
| User Service | New endpoint | Medium |
| Notification Service | New event consumer | Low |
| Database | New table + migration | High |

### Non-Functional Requirements
- Latency: p99 < 200ms
- Throughput: 1000 RPS
- Availability: 99.9%
- Data consistency: Eventually consistent (acceptable delay: 5s)
```

### API Contracts

```markdown
## API: <Endpoint>

### Request
\`\`\`
POST /api/v1/playlists/{playlistId}/tracks
Authorization: Bearer <token>
Content-Type: application/json

{
  "track_ids": ["string"],
  "position": 0  // optional, default: append
}
\`\`\`

### Response (201 Created)
\`\`\`json
{
  "playlist_id": "string",
  "tracks_added": 3,
  "total_tracks": 42,
  "snapshot_id": "string"
}
\`\`\`

### Error Responses
| Status | Code | Message | When |
|--------|------|---------|------|
| 400 | INVALID_TRACK | "Track ID not found" | Track doesn't exist |
| 403 | NOT_OWNER | "Not playlist owner" | User lacks permission |
| 409 | DUPLICATE | "Track already in playlist" | Duplicate add |
| 429 | RATE_LIMITED | "Too many requests" | Rate limit exceeded |

### Rate Limits
- 100 requests per minute per user
- Max 100 tracks per request

### Idempotency
- Use `Idempotency-Key` header for retry safety
```

### Data Model

```markdown
## Data Model Changes

### New Tables
| Table | Purpose | Estimated Size |
|-------|---------|---------------|
| playlist_tracks | Track-playlist membership | 100M rows/year |

### Schema
\`\`\`sql
CREATE TABLE playlist_tracks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  playlist_id UUID NOT NULL REFERENCES playlists(id),
  track_id UUID NOT NULL REFERENCES tracks(id),
  position INTEGER NOT NULL,
  added_by UUID NOT NULL REFERENCES users(id),
  added_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(playlist_id, track_id)
);

CREATE INDEX idx_playlist_tracks_playlist ON playlist_tracks(playlist_id, position);
\`\`\`

### Migration Strategy
- Zero-downtime migration (additive only)
- Backfill strategy: N/A (new table)
- Rollback: DROP TABLE (no data loss for new feature)
```

---

### 🔄 Checkpoint: Architecture Review

**Attendees**: TL, Backend Lead, Frontend Lead, Data Engineer
**Gate criteria**:
- [ ] API contracts are complete with error cases
- [ ] Data model supports all acceptance criteria
- [ ] Non-functional requirements are defined and achievable
- [ ] Migration strategy is zero-downtime
- [ ] No single points of failure
- [ ] Monitoring and alerting plan exists

**Handoff artifact**: `ARCHITECTURE.md` + API specs → Engineering team

---

## Phase 5: Backend Implementation

### Implementation Checklist

- [ ] Database migration created and tested (up + down)
- [ ] API endpoints implemented per contract
- [ ] Business logic layer with validation
- [ ] Service layer with external integrations
- [ ] Repository/data access layer
- [ ] Input validation and sanitization
- [ ] Error handling with proper HTTP status codes
- [ ] Logging with correlation IDs
- [ ] Rate limiting configured
- [ ] Feature flag wrapping new behavior

### Test Requirements

- [ ] Unit tests for business logic (>= 80% coverage)
- [ ] Integration tests for API endpoints
- [ ] Database migration tests (up and down)
- [ ] Contract tests for external service calls
- [ ] Load tests for performance requirements

---

## Phase 6: Frontend Implementation

### Implementation Checklist

- [ ] Components built per UI spec
- [ ] State management integrated
- [ ] API integration with error handling
- [ ] Loading, error, and empty states
- [ ] Responsive design per breakpoints
- [ ] Accessibility (keyboard nav, screen reader, ARIA)
- [ ] Animations per interaction spec
- [ ] Feature flag integration
- [ ] Analytics events firing correctly

### Test Requirements

- [ ] Component unit tests
- [ ] Integration tests (user flow)
- [ ] Visual regression tests
- [ ] Accessibility automated tests (axe-core)
- [ ] Cross-browser testing

---

## Phase 7: Mobile Implementation

### Implementation Checklist

- [ ] Screens implemented per UI spec
- [ ] Navigation integrated (deep links, back handling)
- [ ] Platform-specific adaptations (iOS/Android)
- [ ] Native modules (if required)
- [ ] Offline support (if required)
- [ ] Push notification integration (if required)
- [ ] Feature flag integration
- [ ] Analytics events

### Test Requirements

- [ ] Unit tests for business logic
- [ ] UI tests for critical flows
- [ ] Device-specific testing (screen sizes, OS versions)
- [ ] Performance profiling (startup, memory, battery)

---

## Phase 8: QA

### Test Plan

```markdown
## Test Plan: <Feature Name>

### Scope
- [What's tested]
- [What's NOT tested (and why)]

### Test Matrix
| Scenario | Web | iOS | Android | API |
|----------|-----|-----|---------|-----|
| Happy path | ✓ | ✓ | ✓ | ✓ |
| Empty state | ✓ | ✓ | ✓ | — |
| Error recovery | ✓ | ✓ | ✓ | ✓ |
| Edge: max items | ✓ | ✓ | ✓ | ✓ |
| Edge: concurrent | — | — | — | ✓ |
| Performance | ✓ | ✓ | ✓ | ✓ |
| Accessibility | ✓ | ✓ | ✓ | — |

### Automation Coverage
- Automated: [list of automated test suites]
- Manual: [list of manual test cases with justification]

### Regression Risk
| Area | Risk | Mitigation |
|------|------|------------|
| Existing playlists | Medium | Regression suite |
| Search performance | Low | Load tests |
```

### QA Sign-off Criteria

- [ ] All test cases pass
- [ ] No Critical or Major bugs open
- [ ] Performance meets NFRs
- [ ] Accessibility audit passes
- [ ] Cross-platform parity verified

---

### 🔄 Checkpoint: QA Sign-off

**Attendees**: QA Lead, PM, TL
**Gate criteria**:
- [ ] Test plan executed completely
- [ ] All critical/major bugs resolved
- [ ] Performance benchmarks met
- [ ] Accessibility audit passed
- [ ] Regression suite green

**Handoff artifact**: `QA-REPORT.md` → DevOps for deployment

---

## Phase 9: DevOps & Deployment

### Deployment Pipeline

```
Code Merge → Build → Unit Tests → Integration Tests → Staging Deploy
→ Smoke Tests → Production Deploy (Canary) → Monitoring → Full Rollout
```

### Deployment Checklist

- [ ] Feature flag configured (default: OFF)
- [ ] Database migration applied to staging
- [ ] Staging smoke tests pass
- [ ] Monitoring dashboards created
- [ ] Alerts configured (error rate, latency, throughput)
- [ ] Runbook created for on-call
- [ ] Rollback procedure tested

### Monitoring Setup

```yaml
alerts:
  - name: feature_error_rate
    condition: error_rate > 1%
    window: 5 minutes
    severity: critical
    action: page on-call

  - name: feature_latency
    condition: p99_latency > 500ms
    window: 5 minutes
    severity: warning
    action: slack notification

  - name: feature_throughput
    condition: rps < 50% baseline
    window: 10 minutes
    severity: critical
    action: page on-call + auto-rollback
```

---

## Phase 10: Data & Analytics

### Event Tracking

Define events for the feature (following event taxonomy):

```markdown
| Event | Trigger | Key Properties |
|-------|---------|---------------|
| feature_viewed | Screen loaded | source, variant |
| feature_action_taken | CTA clicked | action_type, item_id |
| feature_completed | Flow finished | duration_ms, success |
| feature_error | Error shown | error_code, step |
```

### Dashboard

Create a feature-specific dashboard:

- Adoption: DAU using feature, % of total DAU
- Engagement: actions per session, time spent
- Conversion: funnel completion rate
- Quality: error rate, latency
- Business: impact on target metric (retention, revenue)

---

## Phase 11: Launch

### Feature Flag Rollout Plan

```
Day 0: Internal dogfooding (employees only)
Day 1: 1% canary (random users)
Day 2: 5% rollout (if metrics healthy)
Day 3: 25% rollout
Day 5: 50% rollout
Day 7: 100% rollout (if no issues)
Day 14: Remove feature flag, clean up old code
```

### Launch Monitoring

| Metric | Baseline | Target | Alert Threshold |
|--------|----------|--------|-----------------|
| Error rate | 0.1% | < 0.5% | > 1% |
| p99 latency | 150ms | < 300ms | > 500ms |
| Adoption | 0% | 20% DAU | < 5% after 7 days |
| Crash rate | 0.3% | < 0.5% | > 0.8% |

### Rollback Plan

```markdown
### Rollback Triggers
- Error rate > 2% for 5 minutes
- p99 latency > 1s for 10 minutes
- Crash rate increase > 0.5%
- Data integrity issue detected

### Rollback Steps
1. Disable feature flag (instant, no deploy needed)
2. If DB migration was destructive: execute down migration
3. Notify #incidents channel
4. Create post-mortem ticket

### Rollback Owner
- Primary: [On-call engineer]
- Escalation: [Tech Lead]
```

---

## Coordination & Handoff Summary

| From | To | Artifact | Format |
|------|----|----------|--------|
| PM | Squad | PRD | `PRD.md` |
| UX | UI + Engineers | User Flows | `UX-SPEC.md` + wireframes |
| UI | Engineers | Visual Specs | `UI-SPEC.md` + mockups |
| TL | Engineers | Architecture | `ARCHITECTURE.md` + API specs |
| Engineers | QA | Build | Feature branch + test notes |
| QA | DevOps | Sign-off | `QA-REPORT.md` |
| DevOps | PM | Deployment | Rollout plan + dashboards |
| Data | PM | Analytics | Dashboard link + event spec |
