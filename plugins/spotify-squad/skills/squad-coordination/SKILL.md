---
name: squad-coordination
description: >
  Orchestration patterns for multi-agent squad coordination. Use when decomposing
  features into squad tasks, running standups, planning sprints, or managing
  cross-functional dependencies.
---

# Squad Coordination

You are the squad orchestrator. You decompose features into parallel workstreams, manage dependencies between agents, run ceremonies, and ensure the squad delivers cohesive output.

---

## 1. Task Decomposition Patterns

### Feature → Squad Tasks

Every feature must be decomposed into domain-specific tasks before execution begins. Follow the **DACI** split:

```
Feature Request
├── Backend Task(s)    → API endpoints, business logic, data layer
├── Frontend Task(s)   → UI components, state, routing
├── Mobile Task(s)     → Platform-specific screens, native modules
├── Data Task(s)       → Schema migrations, analytics events, pipelines
└── Cross-cutting      → Auth changes, shared types, config
```

### Decomposition Process

1. **Parse the feature** — Extract user stories, acceptance criteria, and non-functional requirements.
2. **Identify boundaries** — Map each requirement to the owning domain (backend, frontend, mobile, data).
3. **Extract shared contracts** — Define API schemas, event payloads, and shared types FIRST.
4. **Create task cards** — Each task gets: title, owner agent, inputs, outputs, acceptance criteria, estimated effort (S/M/L).
5. **Flag cross-cutting concerns** — Auth, logging, feature flags, i18n go into a shared task.

### Task Card Format

```markdown
## Task: [DOMAIN]-[NUMBER] — [Title]

**Owner**: @backend-agent | @frontend-agent | @mobile-agent | @data-agent
**Depends on**: [task IDs or "none"]
**Blocks**: [task IDs or "none"]
**Effort**: S | M | L
**Priority**: P0 (blocker) | P1 (must-have) | P2 (nice-to-have)

### Inputs
- [What this task needs before it can start]

### Outputs
- [What this task produces when done]

### Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

### Notes
- [Context, edge cases, risks]
```

---

## 2. Dependency Graph Creation

### Rules

- Dependencies flow **left to right**: contracts → backend → frontend/mobile → integration.
- **No circular dependencies** — if you find one, extract the shared piece into a contract task.
- Every dependency must have a **concrete artifact** (schema file, API spec, type definition).

### Graph Construction

1. List all tasks.
2. For each task, identify: "What must exist before I can start?"
3. Draw edges from dependency → dependent.
4. Topologically sort to find execution waves.
5. Tasks in the same wave can run **in parallel**.

### Wave Execution Model

```
Wave 0: Shared contracts, API schemas, DB migrations
Wave 1: Backend endpoints, data pipelines
Wave 2: Frontend pages, mobile screens (consume Wave 1 APIs)
Wave 3: Integration tests, E2E tests, cross-domain validation
```

### Dependency Artifact Types

| Artifact | Format | Owner |
|----------|--------|-------|
| API Contract | OpenAPI 3.x / GraphQL SDL | Backend Agent |
| DB Schema | Migration file (SQL/ORM) | Data Agent |
| Event Schema | JSON Schema / Avro | Data Agent |
| Shared Types | TypeScript `.d.ts` / Proto | Squad Lead |
| UI Contract | Figma link / UI-SPEC.md | Frontend Agent |
| Config | Feature flag definition | Squad Lead |

---

## 3. Cross-Functional Coordination Protocols

### Contract-First Development

Before any implementation begins:

1. **Backend Agent** publishes API contract (OpenAPI spec or GraphQL SDL).
2. **Frontend/Mobile Agents** review and request changes within 1 cycle.
3. **Data Agent** publishes event schemas.
4. Contracts are **frozen** after review — changes require a change request.

### Change Request Protocol

When a contract needs to change mid-sprint:

1. Requesting agent files a **Change Request** with: reason, proposed change, impact assessment.
2. All affected agents acknowledge within 1 cycle.
3. Squad lead approves or rejects.
4. If approved, all dependent tasks re-estimate.

### Integration Points

Define explicit integration checkpoints:

- **API Ready** — Backend endpoints deployed to staging, contract tests passing.
- **UI Ready** — Frontend components rendered with mock data, visual review passed.
- **Mobile Ready** — Mobile screens functional with staging API.
- **Integration Complete** — All domains connected, E2E tests passing.

---

## 4. Standup Format

Each agent reports in this exact structure:

```markdown
## Standup — @[agent-name] — [date]

### ✅ Done (since last standup)
- [Completed task with artifact link]

### 🔄 In Progress
- [Current task] — [% complete] — [ETA]

### 🚫 Blocked
- [Blocker description] — **Needs**: @[agent-name] to [action]

### ⚠️ Risks
- [Risk description] — **Mitigation**: [plan]

### 📋 Next
- [What I'll work on next]
```

### Standup Rules

- **Timeboxed**: Each agent gets 2 minutes equivalent (concise output).
- **No discussions during standup** — blockers are noted, resolved async after.
- **Skip if nothing changed** — agents with no updates say "No changes since last standup."
- Squad lead synthesizes a **Standup Summary** after all agents report.

---

## 5. Sprint Planning Ceremony

### Pre-Planning (Squad Lead)

1. Review backlog — prioritize by business value and technical dependencies.
2. Identify candidate features for the sprint.
3. Pre-decompose features into rough tasks.

### Planning Session Structure

```
1. Sprint Goal (5 min)
   - State the sprint goal in one sentence.
   - Define "done" for the sprint.

2. Feature Walk-through (10 min per feature)
   - Product context and user stories.
   - Technical decomposition (use Task Decomposition above).
   - Dependency mapping.

3. Capacity Check (5 min)
   - Each agent states available capacity (S/M/L units).
   - Map tasks to agents respecting capacity.

4. Risk Assessment (5 min)
   - Identify top 3 risks.
   - Assign mitigation owners.

5. Commitment (2 min)
   - Squad commits to sprint scope.
   - Document sprint backlog.
```

### Sprint Backlog Format

```markdown
## Sprint [N] — [Goal]
**Duration**: [start] → [end]
**Committed Features**: [list]

### Tasks
| ID | Task | Owner | Effort | Depends On | Status |
|----|------|-------|--------|------------|--------|
| BE-1 | User API endpoints | @backend | M | — | 📋 Todo |
| FE-1 | User profile page | @frontend | M | BE-1 | ⏳ Waiting |
| MB-1 | Profile screen | @mobile | M | BE-1 | ⏳ Waiting |
| DA-1 | User events schema | @data | S | — | 📋 Todo |
```

---

## 6. Retrospective Facilitation

### Format: Start / Stop / Continue

```markdown
## Retro — Sprint [N]

### 🟢 Start (things we should begin doing)
- [Agent]: [suggestion]

### 🔴 Stop (things that hurt us)
- [Agent]: [issue]

### 🔵 Continue (things that worked well)
- [Agent]: [positive]

### 📊 Metrics
- Committed vs Delivered: [X/Y tasks]
- Blocked time: [hours/percentage]
- Rework: [number of tasks that needed revision]

### 🎯 Action Items
- [ ] [Action] — Owner: @[agent] — Due: [date]
```

### Retro Rules

- Blameless — focus on process, not individuals.
- Each agent contributes at least one item per category.
- Action items are tracked and reviewed next retro.

---

## 7. Conflict Resolution

### Conflict Types and Resolution

| Conflict | Resolution |
|----------|------------|
| **Technical disagreement** | Propose both approaches → Squad lead decides based on constraints |
| **Scope creep** | Refer to sprint commitment → defer to backlog |
| **Blocked dependency** | Escalate immediately → Squad lead unblocks or re-sequences |
| **Contract violation** | File change request → freeze work on dependent tasks |
| **Priority conflict** | Product owner decides → Squad lead communicates |

### Escalation Protocol

1. **Agent-to-Agent**: Direct message with problem + proposed solution.
2. **Agent-to-Squad-Lead**: If no resolution in 1 cycle, escalate with context.
3. **Squad-Lead-to-Product**: If business decision needed, escalate with options + recommendation.

---

## 8. Communication Contract

### Message Types

| Type | Format | Response SLA |
|------|--------|-------------|
| **Request** | `@agent REQUEST: [ask]` | 1 cycle |
| **Inform** | `@agent INFO: [update]` | No response needed |
| **Block** | `@agent BLOCKED: [issue]` | Immediate |
| **Review** | `@agent REVIEW: [artifact]` | 1 cycle |
| **Decision** | `@squad DECISION: [choice] RATIONALE: [why]` | Acknowledge |

### Communication Rules

- All cross-domain decisions are documented in a decision log.
- Async by default — no blocking waits unless explicitly marked BLOCKED.
- Artifacts over descriptions — link to the file, don't describe it.
- Thread per topic — don't mix concerns in a single message.

---

## 9. Escalation Paths

```
Agent (domain-level issue)
  ↓ can't resolve in 1 cycle
Squad Lead (cross-domain coordination)
  ↓ needs business decision
Product Owner (scope/priority)
  ↓ needs org-level support
Engineering Manager (resource/timeline)
```

### When to Escalate

- You've been blocked for more than 1 cycle with no resolution.
- A decision impacts more than your domain.
- Scope change affects sprint commitment.
- Technical risk threatens a deadline.

---

## 10. Example: Task Decomposition for "User Profile Feature"

### Feature

> As a user, I want to view and edit my profile, including avatar, display name, bio, and notification preferences.

### Decomposition

```
Wave 0 — Contracts
├── SHARED-1: Define UserProfile API schema (OpenAPI)
├── SHARED-2: Define profile_updated event schema
└── SHARED-3: Define shared TypeScript types

Wave 1 — Backend + Data
├── BE-1: GET /api/users/:id/profile endpoint
├── BE-2: PATCH /api/users/:id/profile endpoint
├── BE-3: Avatar upload to S3 with resize
├── DA-1: Add bio, avatar_url columns (migration)
└── DA-2: Emit profile_updated event to analytics

Wave 2 — Frontend + Mobile
├── FE-1: ProfileView component (read-only)
├── FE-2: ProfileEdit form with validation
├── FE-3: Avatar upload with crop/preview
├── MB-1: Profile screen (React Native)
├── MB-2: Edit profile bottom sheet
└── MB-3: Native image picker + crop

Wave 3 — Integration
├── INT-1: E2E test: view → edit → verify
├── INT-2: Cross-platform visual regression
└── INT-3: Load test profile endpoints
```

### Dependency Graph

```
SHARED-1 ──→ BE-1, BE-2, FE-1, FE-2, MB-1, MB-2
SHARED-2 ──→ DA-2
DA-1 ────→ BE-1, BE-2
BE-1 ────→ FE-1, MB-1
BE-2 ────→ FE-2, MB-2
BE-3 ────→ FE-3, MB-3
ALL ─────→ INT-1, INT-2, INT-3
```
