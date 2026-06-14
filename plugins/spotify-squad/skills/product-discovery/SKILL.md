---
name: product-discovery
description: >
  Product discovery and PRD creation. Use for writing PRDs, defining user
  stories, setting OKRs, feature prioritization, and product strategy.
---

# Product Discovery Skill

You are a senior product manager. You drive product discovery with structured frameworks, write clear PRDs, define measurable outcomes, and align stakeholders around user-centric solutions.

---

## 1. PRD Template

```markdown
# PRD: [Feature Name]

**Author:** [Name]
**Status:** [Draft | In Review | Approved | In Development | Shipped]
**Version:** [1.0]
**Created:** [Date]
**Last Updated:** [Date]
**Stakeholders:** [Names, roles]
**Squad:** [Squad name]

---

## 1. Problem Statement

### Problem
[Describe the problem in 2–3 sentences. Focus on the user pain, not the solution.]

### Evidence
- [Data point: metric, research finding, or support ticket trend]
- [Data point]
- [Data point]

### Impact of Not Solving
[What happens if we don't address this? Quantify where possible.]

### Who Is Affected
[User segments, personas, or cohorts impacted]

---

## 2. Goals & Success Metrics

### Objective
[One-sentence statement of what success looks like]

### Key Results
| Metric | Current | Target | Measurement Method |
|--------|---------|--------|--------------------|
| [Metric] | [Baseline] | [Goal] | [How we measure] |
| [Metric] | [Baseline] | [Goal] | [How we measure] |
| [Metric] | [Baseline] | [Goal] | [How we measure] |

### Counter-Metrics (Guardrails)
[Metrics that should NOT degrade as a result of this work]
| Guardrail Metric | Acceptable Range |
|-----------------|-----------------|
| [Metric] | [Not below X] |

---

## 3. User Stories

[See Section 2 below for format details]

| # | User Story | Priority | Effort |
|---|-----------|----------|--------|
| US-1 | As a [user], I want [action] so that [benefit] | Must Have | M |
| US-2 | As a [user], I want [action] so that [benefit] | Must Have | S |
| US-3 | As a [user], I want [action] so that [benefit] | Should Have | L |

---

## 4. Acceptance Criteria

[See Section 3 below for Given/When/Then format]

---

## 5. Non-Functional Requirements

| Category | Requirement |
|----------|------------|
| **Performance** | Page loads in <2s on 3G; API response <200ms p95 |
| **Scalability** | Must support 10K concurrent users |
| **Security** | Data encrypted at rest and in transit; RBAC enforced |
| **Accessibility** | WCAG 2.1 AA compliant |
| **Localization** | Support for EN, PT-BR, ES initially |
| **Analytics** | Events tracked for [key actions] |
| **Backward Compatibility** | API v1 must remain functional for 6 months |

---

## 6. Solution Design

### Proposed Solution
[High-level description of the approach — what, not how]

### User Flow
[Link to flow diagram or embed key steps]

### Wireframes / Mockups
[Link to Figma or embed key screens]

### Alternatives Considered
| Option | Pros | Cons | Why Not Chosen |
|--------|------|------|---------------|
| [Option A] | [Pros] | [Cons] | [Reason] |
| [Option B] | [Pros] | [Cons] | [Reason] |

---

## 7. Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|-----------|
| [Risk] | High/Med/Low | High/Med/Low | [Plan] |
| [Risk] | High/Med/Low | High/Med/Low | [Plan] |

### Dependencies
- [External team or service dependency]
- [Third-party integration]

### Assumptions
- [Assumption we're making that could be wrong]
- [Assumption]

---

## 8. Timeline & Milestones

| Phase | Scope | Duration | Target Date |
|-------|-------|----------|-------------|
| Discovery | Research, validation | 1 week | [Date] |
| Design | UI/UX, prototype | 1 week | [Date] |
| Development | Build, unit tests | 2 weeks | [Date] |
| QA | Testing, bug fixes | 1 week | [Date] |
| Launch | Staged rollout | 1 week | [Date] |

---

## 9. Launch Plan

### Rollout Strategy
- [ ] Feature flag: [flag name]
- [ ] Internal dogfood → Beta (5%) → GA (100%)
- [ ] Rollback criteria: [metric threshold]

### Communication
- [ ] Changelog entry
- [ ] In-app notification / tooltip
- [ ] Help center article
- [ ] Email announcement (if needed)

---

## 10. Appendix

- Research links
- Technical design doc
- Related PRDs
- Meeting notes
```

---

## 2. User Story Format

### Standard Format
```
As a [user role/persona],
I want to [action/capability],
so that [benefit/outcome].
```

### Writing Rules

1. **User-centric.** The actor is always a user role, never a system.
2. **Independent.** Each story is self-contained and deliverable alone.
3. **Negotiable.** Stories are conversation starters, not contracts.
4. **Valuable.** Every story delivers user or business value.
5. **Estimable.** The team can estimate effort.
6. **Small.** Completable within one sprint.
7. **Testable.** Has clear acceptance criteria.

### INVEST Checklist
- **I**ndependent — Can be developed in any order
- **N**egotiable — Details can be discussed
- **V**aluable — Delivers value to users
- **E**stimable — Team can size it
- **S**mall — Fits in a sprint
- **T**estable — Has clear pass/fail criteria

### Story Splitting Strategies

| Strategy | When to Use | Example |
|----------|-------------|---------|
| **By workflow step** | Multi-step process | "Search" → "Filter" → "Sort" |
| **By data variation** | Different input types | "Upload image" → "Upload video" |
| **By operation** | CRUD operations | "Create item" → "Edit item" → "Delete item" |
| **By role** | Different permissions | "Viewer can..." → "Editor can..." → "Admin can..." |
| **By platform** | Cross-platform | "On mobile..." → "On desktop..." |
| **Happy path / edge case** | Complex logic | "Login succeeds" → "Login fails (wrong password)" |

---

## 3. Acceptance Criteria — Given/When/Then

### Format
```gherkin
Given [precondition / initial context]
When [action / trigger event]
Then [expected outcome / observable result]
```

### Examples
```gherkin
# Happy Path
Given I am a logged-in user on the playlist page
When I click "Add Song" and search for "Bohemian Rhapsody"
Then the song appears in my playlist and a success toast is shown

# Edge Case
Given I am a free-tier user
When I try to download a song for offline playback
Then I see an upsell modal prompting me to upgrade to Premium

# Error Case
Given I am on the signup form
When I submit with an already-registered email
Then I see an inline error: "This email is already associated with an account"
And the email field is highlighted in red

# Boundary
Given a playlist contains 10,000 songs (maximum)
When I try to add another song
Then I see a message: "Playlist limit reached. Remove a song to add a new one."
```

### Rules for Good Acceptance Criteria

1. **Specific.** No ambiguity — state exact values, messages, and behaviors.
2. **Testable.** A QA engineer can verify pass/fail without interpretation.
3. **Complete.** Cover happy path, error paths, edge cases, and boundaries.
4. **Behavior-focused.** Describe what happens, not how it's implemented.
5. **Measurable.** Include performance criteria where applicable.

---

## 4. Prioritization Frameworks

### 4.1 RICE Scoring

| Factor | Definition | Scale |
|--------|-----------|-------|
| **R**each | How many users will this impact per quarter? | Number of users |
| **I**mpact | How much will this move the target metric? | 3 = Massive, 2 = High, 1 = Medium, 0.5 = Low, 0.25 = Minimal |
| **C**onfidence | How confident are we in our estimates? | 100% = High, 80% = Medium, 50% = Low |
| **E**ffort | How many person-months of work? | Number (smaller = better) |

**Formula:**
```
RICE Score = (Reach × Impact × Confidence) / Effort
```

**Example:**
| Feature | Reach | Impact | Confidence | Effort | RICE Score |
|---------|-------|--------|------------|--------|------------|
| Smart Shuffle | 50,000 | 2 | 80% | 3 | 26,667 |
| Lyrics Display | 100,000 | 1 | 90% | 2 | 45,000 |
| Social Playlists | 20,000 | 3 | 50% | 6 | 5,000 |

### 4.2 MoSCoW

| Category | Meaning | Guideline |
|----------|---------|-----------|
| **Must Have** | Critical — release cannot ship without it | ~60% of effort |
| **Should Have** | Important but not critical — painful to leave out | ~20% of effort |
| **Could Have** | Desirable — nice-to-have, low impact if excluded | ~15% of effort |
| **Won't Have (this time)** | Explicitly out of scope for this release | ~5% (documented) |

### 4.3 Kano Model

| Category | Absent | Present | Strategy |
|----------|--------|---------|----------|
| **Must-be** (Basic) | Dissatisfied | Neutral | Must include — no delight, but absence causes frustration |
| **One-dimensional** (Performance) | Dissatisfied | Satisfied | More is better — linear relationship |
| **Attractive** (Delight) | Neutral | Delighted | Differentiator — unexpected value |
| **Indifferent** | Neutral | Neutral | Skip — no impact either way |
| **Reverse** | Satisfied | Dissatisfied | Avoid — actively unwanted |

**Classification Survey Questions:**
1. "How would you feel if [feature] were present?" (Functional)
2. "How would you feel if [feature] were absent?" (Dysfunctional)

---

## 5. OKR Framework

### Format
```markdown
## Objective: [Qualitative, inspirational goal]

**Owner:** [Name]
**Time Period:** [Q1 2025 / H1 2025]

### Key Results

| # | Key Result | Baseline | Target | Current | Status |
|---|-----------|----------|--------|---------|--------|
| KR1 | [Measurable outcome] | [N] | [N] | [N] | 🟡 On Track |
| KR2 | [Measurable outcome] | [N] | [N] | [N] | 🟢 Ahead |
| KR3 | [Measurable outcome] | [N] | [N] | [N] | 🔴 At Risk |

### Initiatives (outputs that drive key results)
- [ ] [Initiative 1] → Supports KR1
- [ ] [Initiative 2] → Supports KR1, KR2
- [ ] [Initiative 3] → Supports KR3
```

### OKR Writing Rules

1. **Objectives** are qualitative, ambitious, and time-bound.
2. **Key Results** are quantitative, measurable, and outcome-based (not output-based).
3. Aim for 3–5 Key Results per Objective.
4. KRs should be a stretch — 70% achievement = good.
5. Avoid vanity metrics — measure outcomes that matter.

**❌ Bad KR:** "Launch the new onboarding flow" (output, not outcome)
**✅ Good KR:** "Increase Day-7 retention from 35% to 50%"

---

## 6. Opportunity Solution Trees

### Structure
```
             [Desired Outcome]
                    │
        ┌───────────┼───────────┐
   [Opportunity]  [Opportunity]  [Opportunity]
        │              │              │
    ┌───┴───┐     ┌────┴────┐    ┌───┴───┐
 [Sol A] [Sol B] [Sol C] [Sol D] [Sol E] [Sol F]
    │       │       │       │       │       │
 [Exp]   [Exp]   [Exp]   [Exp]   [Exp]   [Exp]
```

**Layers:**
1. **Desired Outcome:** The measurable business/product outcome (from OKRs)
2. **Opportunities:** User needs, pain points, or desires (from research)
3. **Solutions:** Possible ways to address each opportunity
4. **Experiments:** Fastest way to test each solution assumption

### Process
1. Start with a clear outcome (KR from OKRs)
2. Map opportunities from user research (interviews, data, support tickets)
3. Brainstorm multiple solutions per opportunity (avoid single-solution bias)
4. Design small experiments to test riskiest assumptions first
5. Let evidence guide which branch to pursue

---

## 7. Go-to-Market Checklist

```markdown
## GTM Checklist: [Feature Name]

### Pre-Launch
- [ ] PRD approved and shared with all stakeholders
- [ ] Feature flag created and tested
- [ ] Analytics events implemented and validated
- [ ] Monitoring and alerts configured
- [ ] Rollback plan documented and tested
- [ ] Help center article drafted
- [ ] Support team briefed and FAQs prepared
- [ ] Legal/compliance review (if applicable)
- [ ] Localization complete for target markets

### Launch Day
- [ ] Feature flag enabled for beta cohort ([N]%)
- [ ] Metrics dashboard live and monitored
- [ ] On-call engineer assigned
- [ ] PM monitoring support channels

### Post-Launch (Week 1)
- [ ] Daily metric check against success criteria
- [ ] Bug triage — no P0/P1 open issues
- [ ] User feedback collection (in-app survey, interviews)
- [ ] Expand rollout to [N]% if metrics are green

### Post-Launch (Week 2–4)
- [ ] Full rollout (100%) or rollback decision
- [ ] Retrospective conducted
- [ ] PRD updated with actual results vs. targets
- [ ] Learnings documented and shared
- [ ] Next iteration scoped (if needed)
```

---

## 8. Stakeholder Communication Templates

### Status Update (Weekly)
```markdown
## [Feature] Weekly Update — [Date]

### Status: 🟢 On Track / 🟡 At Risk / 🔴 Blocked

### Progress This Week
- [Accomplishment 1]
- [Accomplishment 2]

### Planned Next Week
- [Plan 1]
- [Plan 2]

### Risks & Blockers
| Issue | Owner | ETA | Help Needed |
|-------|-------|-----|------------|
| [Issue] | [Name] | [Date] | [Yes/No — what?] |

### Metrics
| Metric | Target | Current | Trend |
|--------|--------|---------|-------|
| [Metric] | [N] | [N] | ↑/↓/→ |

### Decisions Needed
1. [Decision needed from stakeholder X]
```

### Decision Document (RFC)
```markdown
## RFC: [Decision Title]

**Author:** [Name]
**Date:** [Date]
**Decision Deadline:** [Date]
**Approvers:** [Names]

### Context
[Background and why this decision is needed now]

### Options

#### Option A: [Name]
- **Description:** [What this option entails]
- **Pros:** [Benefits]
- **Cons:** [Drawbacks]
- **Effort:** [T-shirt size]
- **Risk:** [High/Med/Low]

#### Option B: [Name]
[Same structure]

#### Option C: [Name]
[Same structure]

### Recommendation
[Which option and why]

### Decision
**Chosen:** [Option] — [Date]
**Rationale:** [Summary of why]
**Dissenting Views:** [Any disagreements noted for the record]
```

---

## Quality Standards

1. **Evidence-driven.** Every decision must link to data, research, or validated assumptions.
2. **Outcome-focused.** Measure results, not output. Ship outcomes, not features.
3. **User-centric.** Every PRD starts with a user problem, never a solution.
4. **Iterative.** Prefer small experiments over big bets. Reduce risk incrementally.
5. **Transparent.** Document trade-offs, rejected alternatives, and decision rationale.
6. **Time-boxed.** Discovery has deadlines. Avoid analysis paralysis.
7. **Collaborative.** Include engineering, design, and data in discovery — not just handoff.
8. **Living documents.** PRDs are updated as you learn — they reflect reality, not just intent.
