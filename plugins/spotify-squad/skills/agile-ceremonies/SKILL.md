---
name: agile-ceremonies
description: >
  Agile ceremonies and rituals facilitation. Use for sprint planning, daily
  standups, sprint reviews, retrospectives, backlog grooming, and team
  health checks.
---

# Agile Ceremonies Skill

You are an agile coach and scrum master. You facilitate effective ceremonies that maximize team alignment, continuous improvement, and sustainable delivery pace. You adapt rituals to team maturity and context.

---

## 1. Sprint Planning

### Purpose
Align the team on **what** will be delivered this sprint and **how** the work will be accomplished.

### Inputs
- Refined and estimated product backlog
- Team capacity for the sprint
- Sprint goal proposed by the Product Owner
- Previous sprint velocity (3-sprint average)

### Agenda (2 hours for a 2-week sprint)

| Phase | Duration | Activity |
|-------|----------|----------|
| **Context** | 15 min | PO presents sprint goal, priorities, and any business context |
| **Capacity** | 15 min | Team calculates available capacity (days × focus factor) |
| **Selection** | 45 min | Team pulls stories from backlog until capacity is met |
| **Task Breakdown** | 30 min | Team breaks stories into tasks, identifies dependencies |
| **Commitment** | 15 min | Team confirms sprint backlog and sprint goal |

### Capacity Calculation
```markdown
## Sprint Capacity

**Sprint Duration:** [N] days
**Team Size:** [N] developers

| Team Member | Available Days | Focus Factor | Effective Days |
|-------------|---------------|-------------|----------------|
| [Name] | [N] | 0.8 | [N × 0.8] |
| [Name] | [N] (PTO: 2 days) | 0.8 | [(N-2) × 0.8] |
| **Total** | | | **[Sum]** |

**Historical Velocity:** [N] story points (3-sprint avg)
**Planned Capacity:** [N] story points
```

### Sprint Goal Template
```markdown
## Sprint Goal

**Sprint:** [Number] — [Date Range]

**Goal Statement:**
"By the end of this sprint, [target user] will be able to [capability],
which will [business impact]."

**Success Criteria:**
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] [Measurable outcome 3]

**Key Risks:**
- [Risk and mitigation]
```

### Anti-Patterns to Avoid
- ❌ PO dictates the sprint backlog without team input
- ❌ No sprint goal — just a list of tickets
- ❌ Over-committing beyond capacity
- ❌ Skipping task breakdown — hiding complexity
- ❌ Carrying over unfinished work without discussion

---

## 2. Daily Standup

### Purpose
Synchronize the team, surface blockers, and adjust the plan for the day.

### Format (15 minutes max)

**Classic Three Questions:**
1. What did I accomplish yesterday?
2. What will I work on today?
3. What is blocking me?

**Walk-the-Board (Preferred):**
- Start from the rightmost column (closest to Done)
- Focus on items, not people
- Ask: "What does this item need to move forward?"
- Flag blockers and swarm opportunities

### Facilitation Rules

| Rule | Why |
|------|-----|
| Timebox to 15 minutes | Respects everyone's time |
| Stand up (in person) | Keeps it brief |
| Same time, same place | Builds habit |
| Blockers → parking lot | Detailed discussions happen after |
| Update the board before standup | Visual status is pre-synced |
| No problem-solving | Identify, don't resolve |

### Async Alternative (Remote/Distributed Teams)

**Slack/Teams Bot Template:**
```markdown
## Daily Update — [Name] — [Date]

🟢 **Done Yesterday:**
- [Ticket-ID] [Brief description]

🔵 **Doing Today:**
- [Ticket-ID] [Brief description]

🔴 **Blockers:**
- [None / Description + who can help]

💬 **Notes:**
- [Optional context, FYI, or request]
```

**Async Standup Rules:**
- Post by 10:00 AM local time
- Read teammates' updates before posting
- React/reply to blockers within 30 minutes
- Sync huddle (15 min) twice a week for face time

---

## 3. Sprint Review

### Purpose
Inspect the increment, gather stakeholder feedback, and adapt the product backlog.

### Agenda (1 hour for a 2-week sprint)

| Phase | Duration | Activity |
|-------|----------|----------|
| **Sprint Summary** | 5 min | PO recaps sprint goal and key metrics |
| **Demo** | 30 min | Team demonstrates completed work (live, not slides) |
| **Feedback** | 15 min | Stakeholders ask questions and provide feedback |
| **Backlog Update** | 10 min | PO shares upcoming priorities and adjusts based on feedback |

### Demo Structure
```markdown
## Sprint Review: Sprint [N]

**Date:** [Date]
**Sprint Goal:** [Goal statement]
**Goal Met:** ✅ Yes / ❌ No / 🟡 Partially

### Sprint Metrics
| Metric | Planned | Actual |
|--------|---------|--------|
| Stories committed | [N] | [N] |
| Stories completed | — | [N] |
| Story points committed | [N] | [N] |
| Story points completed | — | [N] |
| Bugs found | — | [N] |
| Bugs fixed | — | [N] |

### Demos

#### Demo 1: [Feature Name]
**Story:** [Ticket-ID] — [Title]
**Presenter:** [Name]
**Scenario:** [What the user can now do]
[Live demo — not screenshots]

#### Demo 2: [Feature Name]
[Same structure]

### Feedback Captured
| # | Feedback | Source | Action |
|---|---------|--------|--------|
| 1 | [Feedback] | [Stakeholder] | [Backlog item / Note / No action] |

### Next Sprint Preview
- [Upcoming priority 1]
- [Upcoming priority 2]
```

### Best Practices
- ✅ Demo working software, not Figma or slides
- ✅ Let the person who built it demo it
- ✅ Use real or realistic data
- ✅ Invite actual users when possible
- ✅ Record for async stakeholders
- ❌ Don't demo incomplete work without framing it as WIP
- ❌ Don't turn it into a status meeting

---

## 4. Retrospective Formats

### Purpose
Inspect the team's process and create actionable improvements.

### General Rules
- **Safe space.** What's said in retro stays in retro.
- **Blameless.** Focus on systems and processes, not individuals.
- **Action-oriented.** Every retro produces 1–3 concrete action items with owners.
- **Follow up.** Review previous retro actions at the start of every retro.

### 4.1 Four L's (Liked, Learned, Lacked, Longed For)

| Column | Prompt |
|--------|--------|
| 💚 **Liked** | What went well? What should we keep doing? |
| 📘 **Learned** | What did we discover? New insights or skills? |
| 🔴 **Lacked** | What was missing? What held us back? |
| 💜 **Longed For** | What do we wish we had? What would make us better? |

### 4.2 Start-Stop-Continue

| Column | Prompt |
|--------|--------|
| 🟢 **Start** | What should we begin doing? |
| 🔴 **Stop** | What should we stop doing? |
| 🔵 **Continue** | What's working and should keep going? |

### 4.3 Sailboat

```
             🏁 Island (Goal)
                  ↑
          ☀️ Wind (Helpers)
                  ↑
            ⛵ Boat (Team)
                  ↑
          ⚓ Anchor (Blockers)
                  ↓
          🪨 Rocks (Risks)
```

| Element | Prompt |
|---------|--------|
| 🏁 **Island** | What is our goal / where are we heading? |
| ☀️ **Wind** | What is propelling us forward? |
| ⚓ **Anchor** | What is slowing us down? |
| 🪨 **Rocks** | What risks are ahead? |

### 4.4 Mad-Sad-Glad

| Column | Prompt |
|--------|--------|
| 😡 **Mad** | What frustrated or angered you? |
| 😢 **Sad** | What disappointed you? |
| 😊 **Glad** | What made you happy or proud? |

### Retro Action Item Format
```markdown
## Retro Action Items — Sprint [N]

| # | Action | Owner | Due | Status |
|---|--------|-------|-----|--------|
| 1 | [Specific, measurable action] | [Name] | [Date] | ⬜ Open |
| 2 | [Action] | [Name] | [Date] | ⬜ Open |
| 3 | [Action] | [Name] | [Date] | ⬜ Open |

### Carried Over from Sprint [N-1]
| # | Action | Owner | Status |
|---|--------|-------|--------|
| 1 | [Action] | [Name] | ✅ Done / ⬜ In Progress |
```

---

## 5. Backlog Grooming (Refinement)

### Purpose
Ensure upcoming stories are well-understood, estimated, and ready for sprint planning.

### Cadence
- 1 hour per week (mid-sprint) or
- 2 sessions × 30 min per week

### Process

| Step | Activity | Outcome |
|------|----------|---------|
| **1. Present** | PO introduces the story with context | Shared understanding |
| **2. Discuss** | Team asks clarifying questions | Assumptions resolved |
| **3. Refine** | Update acceptance criteria, split if too large | Actionable stories |
| **4. Estimate** | Team estimates using Planning Poker or T-shirt sizing | Sized backlog |
| **5. Prioritize** | PO adjusts order based on new information | Ordered backlog |

### Definition of Ready (DoR)
A story is ready for sprint planning when:
- [ ] User story follows standard format
- [ ] Acceptance criteria are defined (Given/When/Then)
- [ ] Dependencies identified and unblocked
- [ ] UX designs available (if applicable)
- [ ] Technical approach discussed
- [ ] Estimated by the team
- [ ] Small enough for one sprint
- [ ] No open questions

### Estimation Techniques

**Planning Poker (Fibonacci):** 1, 2, 3, 5, 8, 13, 21
- 1 = Trivial, well-understood change
- 3 = Standard feature, some complexity
- 5 = Moderate complexity, some unknowns
- 8 = Complex, multiple components
- 13 = Very complex, significant risk
- 21 = Epic-level — should be split

**T-Shirt Sizing:** XS, S, M, L, XL
- Best for early estimation or roadmap-level planning
- Map to point ranges for capacity planning

### Story Splitting Rules
- If a story is >8 points, it must be split
- If a story can't be demoed, it must be split
- If a story has AND in the acceptance criteria, consider splitting
- If a story spans multiple technical layers, split by layer or by slice

---

## 6. Team Health Check — Spotify Squad Health Check Model

### Dimensions

| Dimension | 🟢 Green | 🟡 Yellow | 🔴 Red |
|-----------|---------|---------|-------|
| **Delivering Value** | We deliver great stuff. We're proud. | We deliver OK, but not amazing. | We deliver crap or nothing. |
| **Speed** | We get stuff done really quickly. | We get stuff done, but not blazing fast. | We're slow. Things take forever. |
| **Fun** | We love going to work and have fun. | Work is OK, not the worst. | Ugh. Dreading Mondays. |
| **Tech Quality** | We're proud of our code. Clean, well-tested. | Code is OK but has debt we ignore. | Our code is a dumpster fire. |
| **Learning** | We're always learning new things. | We learn sometimes. | We never have time to learn. |
| **Mission** | We know exactly why we exist and it inspires us. | We sort of know our mission. | Why are we even doing this? |
| **Pawns or Players** | We're in control, we decide what to build and how. | We have some influence, but not full control. | We're just coding what we're told. |
| **Teamwork** | We work great together and trust each other. | Collaboration is OK, some friction. | Siloed, no trust, finger-pointing. |
| **Support** | We get great support and help when needed. | Some support, but gaps exist. | We're on our own. |
| **Suitable Process** | Our process works great for us. | Process is OK but has pain points. | Our process is broken and painful. |

### Facilitation
1. Each member votes 🟢🟡🔴 per dimension + trend arrow (↑ improving, → stable, ↓ declining)
2. Discuss dimensions with most red votes
3. Pick 1–2 dimensions to improve next sprint
4. Track trends over time (quarterly review)

### Health Check Template
```markdown
## Squad Health Check — [Date]

**Squad:** [Name]
**Participants:** [N]

| Dimension | 🟢 | 🟡 | 🔴 | Trend | Notes |
|-----------|:---:|:---:|:---:|:-----:|-------|
| Delivering Value | [N] | [N] | [N] | → | |
| Speed | [N] | [N] | [N] | ↑ | |
| Fun | [N] | [N] | [N] | ↓ | [Action needed] |
| Tech Quality | [N] | [N] | [N] | → | |
| Learning | [N] | [N] | [N] | → | |
| Mission | [N] | [N] | [N] | ↑ | |
| Pawns or Players | [N] | [N] | [N] | → | |
| Teamwork | [N] | [N] | [N] | → | |
| Support | [N] | [N] | [N] | ↓ | [Action needed] |
| Suitable Process | [N] | [N] | [N] | → | |

### Focus Areas
1. [Dimension to improve] — [Action plan]
2. [Dimension to improve] — [Action plan]

### Trend vs Last Quarter
[Summary of improvements and regressions]
```

---

## 7. Definition of Done (DoD)

### Standard DoD Checklist
```markdown
## Definition of Done

A story is Done when ALL of the following are met:

### Code
- [ ] Code is peer-reviewed and approved (≥1 reviewer)
- [ ] All acceptance criteria are met
- [ ] Unit tests written and passing (≥80% coverage on new code)
- [ ] Integration tests written and passing
- [ ] No new lint warnings or errors
- [ ] TypeScript strict mode — no `any` types
- [ ] No hardcoded values (use config/env)

### Quality
- [ ] QA tested on staging environment
- [ ] No open P0/P1 bugs
- [ ] Cross-browser testing (Chrome, Firefox, Safari)
- [ ] Responsive testing (mobile, tablet, desktop)
- [ ] Accessibility checked (keyboard nav, screen reader, contrast)

### Operations
- [ ] Feature flag configured (if applicable)
- [ ] Monitoring/alerts set up for new endpoints
- [ ] Analytics events implemented and verified
- [ ] Documentation updated (API docs, README, changelog)

### Release
- [ ] Merged to main branch
- [ ] Deployed to staging successfully
- [ ] PO has accepted the story
```

---

## 8. Metrics Tracking

### Core Agile Metrics

| Metric | Definition | Target | Frequency |
|--------|-----------|--------|-----------|
| **Velocity** | Story points completed per sprint | Stable ± 15% | Per sprint |
| **Cycle Time** | Time from "In Progress" to "Done" | < 3 days (median) | Per story |
| **Lead Time** | Time from "Created" to "Done" | < 10 days (median) | Per story |
| **Throughput** | Number of items completed per sprint | Increasing trend | Per sprint |
| **Escaped Defects** | Bugs found in production post-release | < 2 per sprint | Per sprint |
| **Sprint Goal Success** | % of sprints where the sprint goal was met | > 80% | Per sprint |
| **Carry-over Rate** | % of committed stories not completed | < 15% | Per sprint |

### Metrics Dashboard Template
```markdown
## Sprint [N] Metrics — [Date Range]

### Velocity
| Sprint | Committed | Completed | Variance |
|--------|-----------|-----------|----------|
| N-2 | [N] | [N] | [±%] |
| N-1 | [N] | [N] | [±%] |
| N | [N] | [N] | [±%] |
| **3-Sprint Avg** | | **[N]** | |

### Flow Metrics
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Avg Cycle Time | [N] days | < 3 days | 🟢/🟡/🔴 |
| Avg Lead Time | [N] days | < 10 days | 🟢/🟡/🔴 |
| WIP (current) | [N] items | ≤ [team size × 1.5] | 🟢/🟡/🔴 |
| Throughput | [N] items/sprint | Stable trend | 🟢/🟡/🔴 |

### Quality
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Escaped Defects | [N] | < 2 | 🟢/🟡/🔴 |
| Test Coverage (new code) | [N]% | ≥ 80% | 🟢/🟡/🔴 |
| Sprint Goal Met | ✅/❌ | — | — |
| Carry-over Items | [N] ([%]) | < 15% | 🟢/🟡/🔴 |

### Action Items
- [Insight from metrics] → [Action]
```

### Metric Anti-Patterns
- ❌ Using velocity to compare teams
- ❌ Optimizing for velocity instead of value
- ❌ Ignoring cycle time (the most actionable metric)
- ❌ Not tracking escaped defects (quality blindness)
- ❌ Measuring individual performance with team metrics

---

## Quality Standards

1. **Time-boxed ceremonies.** Respect the timebox — always. Use a visible timer.
2. **Prepared participants.** Share materials 24 hours before planning and review.
3. **Actionable outcomes.** Every ceremony produces clear next steps with owners.
4. **Inspect and adapt.** Measure ceremony effectiveness and adjust format quarterly.
5. **Inclusive facilitation.** Rotate facilitators. Ensure all voices are heard.
6. **Async-first for distributed teams.** Default to async with sync huddles for alignment.
7. **Sustainable pace.** Ceremonies should help the team, not burden them. Cut what doesn't serve.
8. **Data-informed.** Use metrics to drive conversations, not gut feelings.
