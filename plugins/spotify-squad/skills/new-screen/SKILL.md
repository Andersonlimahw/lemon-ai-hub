---
name: new-screen
description: >
  New screen/page creation workflow. Use when adding a new screen or page
  to web or mobile application, coordinating between UX, UI, frontend,
  and mobile engineers.
---

# New Screen — Screen/Page Creation Workflow

You are the Screen Coordinator. You guide the creation of a new screen or page from initial UX positioning through implementation and QA verification, ensuring consistency and quality across platforms.

## Screen Creation Pipeline

```
UX Flow Position → UI Visual Design → Frontend Build → Mobile Build → QA Verify
      │                   │                  │               │            │
      ▼                   ▼                  ▼               ▼            ▼
  Where does it     How does it        React/Vue         Swift/Kotlin   Tests &
  fit in the app?   look & feel?       components        screens        a11y
```

## Phase 1: UX — User Flow Position

### Information Architecture

Define where this screen lives in the application hierarchy:

```markdown
## Screen Position: <Screen Name>

### Navigation Path
Home → Library → Playlists → **[New Screen]**

### Sitemap Position
\`\`\`
App Root
├── Home
├── Search
├── Library
│   ├── Playlists
│   │   ├── Playlist Detail
│   │   └── **[New Screen]** ← HERE
│   ├── Albums
│   └── Artists
└── Settings
\`\`\`

### Entry Points
| # | Source | Trigger | Context Passed |
|---|--------|---------|---------------|
| 1 | Playlist Detail | "Edit" button tap | playlist_id |
| 2 | Deep link | URL scheme | playlist_id via URL |
| 3 | Push notification | Notification tap | playlist_id + action |

### Exit Points
| # | Destination | Trigger | Data Returned |
|---|-------------|---------|---------------|
| 1 | Playlist Detail | Save success | updated_playlist |
| 2 | Playlist Detail | Back/Cancel | none |
| 3 | Error screen | Unrecoverable error | error_context |
```

### Wireframe Specification

```markdown
## Wireframe: <Screen Name>

### Layout Zones
\`\`\`
┌─────────────────────────────────┐
│         HEADER ZONE             │
│  [← Back]  [Title]  [Action]   │
├─────────────────────────────────┤
│                                 │
│         CONTENT ZONE            │
│                                 │
│  [Primary content area]        │
│  [Scrollable if needed]        │
│                                 │
├─────────────────────────────────┤
│         FOOTER ZONE             │
│  [Primary CTA]                  │
└─────────────────────────────────┘
\`\`\`

### Content Priority (top to bottom)
1. [Most important element — what the user came here for]
2. [Supporting information]
3. [Secondary actions]
4. [Tertiary information]

### Screen States
| State | Description | Key Elements |
|-------|------------|-------------|
| Loading | Data being fetched | Skeleton placeholders |
| Empty | No data available | Illustration + CTA |
| Populated | Normal with data | Full content layout |
| Error | Failed to load | Error message + retry |
| Partial | Some data loaded | Mixed content + retry for failed sections |

### User Interactions
| Element | Gesture | Result |
|---------|---------|--------|
| Back button | Tap | Navigate back (with unsaved changes prompt) |
| List item | Tap | Open detail |
| List item | Long press | Show context menu |
| Content area | Pull down | Refresh data |
| Content area | Scroll | Load more (pagination) |
```

### User Flow Diagram

```markdown
## Flow: <Screen Name>

### Happy Path
\`\`\`mermaid
flowchart TD
    A[Entry Point] --> B{Data Available?}
    B -->|Yes| C[Show Content]
    B -->|No| D[Show Empty State]
    C --> E[User Interaction]
    E --> F{Action Success?}
    F -->|Yes| G[Show Success + Navigate]
    F -->|No| H[Show Error + Retry]
    D --> I[CTA: Create/Add]
    I --> E
\`\`\`

### Error Recovery Flow
\`\`\`mermaid
flowchart TD
    A[Error Occurs] --> B{Error Type}
    B -->|Network| C[Show Retry Banner]
    B -->|Auth| D[Redirect to Login]
    B -->|Not Found| E[Show 404 State]
    B -->|Server| F[Show Generic Error]
    C --> G[User Taps Retry]
    G --> H{Success?}
    H -->|Yes| I[Show Content]
    H -->|No| C
\`\`\`
```

---

## Phase 2: UI — Visual Design

### Visual Design Specification

```markdown
## Visual Spec: <Screen Name>

### Design Tokens Used

#### Colors
| Token | Value | Usage |
|-------|-------|-------|
| color.bg.primary | #121212 | Screen background |
| color.bg.secondary | #1E1E1E | Card background |
| color.text.primary | #FFFFFF | Headings, body text |
| color.text.secondary | #B3B3B3 | Metadata, captions |
| color.accent.primary | #1DB954 | CTA buttons, links |
| color.error | #E74C3C | Error states |
| color.warning | #F39C12 | Warning banners |

#### Typography
| Token | Size | Weight | Line Height | Usage |
|-------|------|--------|-------------|-------|
| type.h1 | 28px | 700 | 34px | Screen title |
| type.h2 | 22px | 600 | 28px | Section headers |
| type.body | 16px | 400 | 22px | Body text |
| type.caption | 12px | 400 | 16px | Metadata |
| type.button | 14px | 600 | 20px | Button labels |

#### Spacing
| Token | Value | Usage |
|-------|-------|-------|
| space.xs | 4px | Inline element gaps |
| space.sm | 8px | Related element spacing |
| space.md | 16px | Section internal padding |
| space.lg | 24px | Section separation |
| space.xl | 32px | Major section breaks |

#### Elevation & Borders
| Token | Value | Usage |
|-------|-------|-------|
| shadow.sm | 0 1px 3px rgba(0,0,0,0.2) | Cards |
| shadow.md | 0 4px 12px rgba(0,0,0,0.3) | Modals, dropdowns |
| radius.sm | 4px | Buttons, inputs |
| radius.md | 8px | Cards |
| radius.lg | 16px | Bottom sheets |
| radius.full | 50% | Avatars |
```

### Responsive Breakpoints

```markdown
### Breakpoint Behavior

| Breakpoint | Width | Layout Changes |
|-----------|-------|---------------|
| Mobile (xs) | < 480px | Single column, full-width cards, bottom sheet modals |
| Mobile (sm) | 480-639px | Single column, slight padding increase |
| Tablet (md) | 640-1023px | Two columns, side-by-side content, modal dialogs |
| Desktop (lg) | 1024-1439px | Three columns, sidebar navigation visible |
| Desktop (xl) | ≥ 1440px | Max content width 1200px, centered |

### Per-Breakpoint Wireframes
\`\`\`
Mobile (< 480px)          Tablet (640-1023px)       Desktop (≥ 1024px)
┌──────────────┐          ┌────────────────────┐    ┌─────────────────────────┐
│   Header     │          │  Header            │    │ Sidebar │ Header        │
├──────────────┤          ├──────────┬─────────┤    ├─────────┼───────────────┤
│              │          │          │         │    │         │               │
│  Content     │          │ Content  │ Detail  │    │  Nav    │   Content     │
│  (stacked)   │          │ (list)   │ (panel) │    │         │   (grid)      │
│              │          │          │         │    │         │               │
├──────────────┤          ├──────────┴─────────┤    │         │               │
│  Bottom CTA  │          │  Footer CTA        │    │         │               │
└──────────────┘          └────────────────────┘    └─────────┴───────────────┘
\`\`\`
```

### Component Visual Specs

```markdown
### Component: <ComponentName>

**Variants**: default | active | disabled | loading | error

| Property | Default | Active | Disabled | Loading |
|----------|---------|--------|----------|---------|
| Background | bg.secondary | accent.primary | bg.secondary | bg.secondary |
| Text Color | text.primary | white | text.secondary | text.secondary |
| Opacity | 1 | 1 | 0.5 | 0.7 |
| Border | none | none | none | none |
| Cursor | pointer | pointer | not-allowed | wait |

**Animations**:
| Trigger | Property | From | To | Duration | Easing |
|---------|----------|------|-----|----------|--------|
| Hover | background | default | lighten(10%) | 150ms | ease-out |
| Press | transform | scale(1) | scale(0.97) | 100ms | ease-in |
| Enter | opacity | 0 | 1 | 200ms | ease-out |
| Exit | opacity | 1 | 0 | 150ms | ease-in |
```

### Dark Mode / Light Mode

```markdown
| Token | Dark Mode | Light Mode |
|-------|-----------|------------|
| bg.primary | #121212 | #FFFFFF |
| bg.secondary | #1E1E1E | #F5F5F5 |
| text.primary | #FFFFFF | #191414 |
| text.secondary | #B3B3B3 | #535353 |
| border.default | #333333 | #E0E0E0 |
```

---

## Phase 3: Frontend — Component Implementation

### Component Hierarchy

```markdown
## Component Tree: <ScreenName>

\`\`\`
<ScreenNamePage>                    # Route-level component
├── <PageHeader>                    # Shared header component
│   ├── <BackButton />
│   ├── <PageTitle title={...} />
│   └── <HeaderActions>
│       └── <IconButton icon="more" />
├── <ContentContainer>              # Scrollable content area
│   ├── <SectionHeader title={...} />
│   ├── <ItemList>                  # Virtualized list
│   │   └── <ItemCard>             # Repeated
│   │       ├── <Thumbnail />
│   │       ├── <ItemInfo>
│   │       │   ├── <ItemTitle />
│   │       │   └── <ItemMeta />
│   │       └── <ItemActions />
│   └── <LoadMoreTrigger />         # Intersection observer
├── <ErrorBoundary>                 # Error catching wrapper
│   └── <ErrorFallback />
└── <BottomBar>                     # Fixed bottom bar
    └── <PrimaryButton />
\`\`\`
```

### State Requirements

```markdown
## State: <ScreenName>

### Local State (Component)
| State | Type | Initial | Managed By |
|-------|------|---------|-----------|
| isRefreshing | boolean | false | ContentContainer |
| selectedItems | string[] | [] | ItemList |
| filterValue | string | '' | FilterBar |

### Global State (Store)
| State | Type | Source | Cache TTL |
|-------|------|--------|-----------|
| items | Item[] | API: GET /items | 5 min |
| userPrefs | UserPrefs | API: GET /prefs | 30 min |

### Derived State
| State | Derivation |
|-------|-----------|
| filteredItems | items.filter(i => matches(i, filterValue)) |
| hasSelection | selectedItems.length > 0 |
| canSubmit | filteredItems.length > 0 && !isSubmitting |

### Data Fetching
| Query | Endpoint | Trigger | Error Handling |
|-------|----------|---------|---------------|
| useItems | GET /api/items | Mount + pull-refresh | Toast + retry |
| useUpdateItem | PUT /api/items/:id | User action | Inline error |
```

### Route Setup

```markdown
## Routing: <ScreenName>

### Route Definition
| Property | Value |
|----------|-------|
| Path | /library/playlists/:playlistId/edit |
| Component | PlaylistEditPage |
| Auth Required | Yes |
| Layout | MainLayout |
| Preload | items query |

### URL Parameters
| Param | Type | Required | Validation |
|-------|------|----------|-----------|
| playlistId | UUID | Yes | UUID format |

### Query Parameters
| Param | Type | Default | Purpose |
|-------|------|---------|---------|
| tab | string | 'details' | Active tab |
| sort | string | 'recent' | Sort order |

### Navigation Guards
- Redirect to /login if not authenticated
- Show 404 if playlist not found
- Show permission denied if not owner
- Prompt "unsaved changes" on navigate away
```

---

## Phase 4: Mobile — Platform-Specific Implementation

### Platform Adaptations

```markdown
## Mobile Adaptations: <ScreenName>

### iOS-Specific
| Aspect | Implementation |
|--------|---------------|
| Navigation | UINavigationController push |
| Back gesture | Swipe from left edge |
| Haptics | Light impact on selection |
| Safe areas | Respect notch + home indicator |
| Dynamic Type | Support accessibility text sizes |
| Context menu | Long press with preview |

### Android-Specific
| Aspect | Implementation |
|--------|---------------|
| Navigation | Fragment via Navigation Component |
| Back gesture | System back + predictive back animation |
| Material You | Dynamic color from wallpaper |
| Edge-to-edge | Draw behind status bar + nav bar |
| Font scaling | Support up to 200% |
| Context menu | Long press with popup menu |

### Cross-Platform Consistency
| Element | iOS | Android | Rationale |
|---------|-----|---------|-----------|
| Primary CTA | Bottom floating | Bottom floating | Consistency |
| Pull to refresh | Native UIRefreshControl | SwipeRefreshLayout | Platform native |
| Loading | Custom skeleton | Custom skeleton | Brand consistency |
| Transitions | Push from right | Shared element | Platform convention |
```

### Navigation Integration

```markdown
### Deep Link Support
| Link | Screen | Parameters |
|------|--------|-----------|
| app://playlist/{id}/edit | PlaylistEdit | playlistId |
| https://app.example.com/playlist/{id} | PlaylistDetail | playlistId |

### Navigation Stack Behavior
| Entry Point | Stack |
|-------------|-------|
| Tab navigation | Tab → List → Detail → **Edit** |
| Deep link | **Edit** (single screen, back → Home) |
| Notification | **Edit** (synthetic back stack: Home → List → Detail → Edit) |

### Transition Animations
| Direction | iOS | Android |
|-----------|-----|---------|
| Forward | Slide from right (push) | Shared element / fade |
| Backward | Slide to right (pop) | Shared element / fade reverse |
| Modal | Slide from bottom | Slide from bottom |
```

---

## Phase 5: QA — Screen-Specific Testing

### Screen Test Cases

```markdown
## Test Cases: <ScreenName>

### Functional Tests
| # | Scenario | Steps | Expected Result | Priority |
|---|----------|-------|-----------------|----------|
| 1 | Load with data | Navigate to screen | Content displayed correctly | P0 |
| 2 | Load empty | Navigate with no data | Empty state shown with CTA | P0 |
| 3 | Load error | Simulate network failure | Error state with retry | P0 |
| 4 | Pull to refresh | Pull down on content | Data refreshes, spinner shows | P1 |
| 5 | Pagination | Scroll to bottom | Next page loads seamlessly | P1 |
| 6 | Back navigation | Tap back button | Returns to previous screen | P0 |
| 7 | Deep link entry | Open via deep link | Screen loads with correct data | P1 |
| 8 | Orientation change | Rotate device | Layout adapts, no data loss | P2 |
| 9 | Background/foreground | Switch apps and return | State preserved | P1 |
| 10 | Low memory | Simulate memory warning | Screen recovers gracefully | P2 |
```

### Accessibility Checklist

```markdown
### Accessibility: <ScreenName>

#### Screen Reader
- [ ] All elements have accessible labels
- [ ] Reading order matches visual order
- [ ] Decorative images marked as decorative (role="presentation")
- [ ] Dynamic content changes announced (aria-live or accessibility announcement)
- [ ] Custom components have correct roles (button, heading, list)

#### Keyboard Navigation (Web)
- [ ] All interactive elements are focusable
- [ ] Focus order is logical (top-to-bottom, left-to-right)
- [ ] Focus is visible (outline or highlight)
- [ ] Modal traps focus correctly
- [ ] Escape closes modals/dropdowns
- [ ] No keyboard traps

#### Touch Targets (Mobile)
- [ ] All tap targets ≥ 44x44pt (iOS) / 48x48dp (Android)
- [ ] Adequate spacing between targets (≥ 8px)
- [ ] Swipe gestures have button alternatives

#### Visual
- [ ] Color contrast ratio ≥ 4.5:1 for normal text
- [ ] Color contrast ratio ≥ 3:1 for large text
- [ ] Information not conveyed by color alone
- [ ] Text scales properly with system font size
- [ ] Animations can be reduced (prefers-reduced-motion)

#### Content
- [ ] Error messages are descriptive and actionable
- [ ] Form labels are properly associated
- [ ] Required fields are indicated
- [ ] Timeout warnings are provided
```

### Cross-Platform Test Matrix

```markdown
| Test | Chrome | Safari | Firefox | iOS Safari | Android Chrome |
|------|--------|--------|---------|------------|----------------|
| Render | ✓ | ✓ | ✓ | ✓ | ✓ |
| Interactions | ✓ | ✓ | ✓ | ✓ | ✓ |
| Responsive | ✓ | ✓ | ✓ | ✓ | ✓ |
| Accessibility | ✓ | ✓ | ✓ | ✓ | ✓ |
| Performance | ✓ | ✓ | ✓ | ✓ | ✓ |
```

---

## Screen Specification Template

Use this template to create a complete screen specification document:

```markdown
# Screen Specification: <Screen Name>

## Overview
- **Purpose**: [What this screen does]
- **User story**: [Link to user story]
- **Entry points**: [How users reach this screen]
- **Platform**: Web | iOS | Android | All

## UX
### Navigation Position
[Sitemap position and navigation path]

### User Flow
[Mermaid diagram of the flow]

### Screen States
[Table of all states: loading, empty, populated, error]

## UI
### Visual Design
[Link to Figma/mockup]

### Design Tokens
[Table of tokens used]

### Responsive Behavior
[Breakpoint table]

### Component Specs
[Detailed component specifications]

## Frontend
### Component Tree
[Hierarchy diagram]

### State Management
[Local, global, and derived state]

### Route Configuration
[Path, params, guards]

### API Integration
[Endpoints, caching, error handling]

## Mobile
### Platform Adaptations
[iOS/Android specific behavior]

### Navigation
[Deep links, stack behavior, transitions]

## QA
### Test Cases
[Prioritized test scenarios]

### Accessibility Checklist
[a11y verification items]

## Analytics
### Events
| Event | Trigger | Properties |
|-------|---------|-----------|
| screen_viewed | Screen mount | screen_name, source |
| screen_action | User interaction | action_type, target |
```
