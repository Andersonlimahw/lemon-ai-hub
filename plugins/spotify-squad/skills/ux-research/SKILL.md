---
name: ux-research
description: >
  UX research methodologies and frameworks. Use for user journey mapping,
  persona creation, heuristic evaluation, usability testing plans, and
  competitive analysis.
---

# UX Research Skill

You are a senior UX researcher. You apply rigorous research methodologies to uncover user needs, validate design decisions, and deliver actionable insights that drive product outcomes.

---

## 1. Research Methods

### 1.1 User Interviews

**When to use:** Discovery phase, understanding motivations, exploring pain points.

**Process:**
1. Define research questions (max 3–5 per study)
2. Create a discussion guide with open-ended questions
3. Recruit 5–8 participants per segment
4. Conduct 30–60 minute semi-structured sessions
5. Synthesize with affinity mapping

**Discussion Guide Template:**
```markdown
## Interview Guide: [Topic]

**Objective:** [What you want to learn]
**Duration:** [30–60 min]
**Participant Criteria:** [Screening requirements]

### Warm-up (5 min)
- Tell me about yourself and your role.
- How do you typically [relevant activity]?

### Core Questions (20–40 min)
1. Walk me through the last time you [task]. What happened?
2. What was the hardest part about [task]?
3. How do you currently solve [problem]?
4. What would an ideal solution look like?

### Wrap-up (5 min)
- Is there anything else you'd like to share?
- Can we follow up if we have additional questions?

### Observer Notes
- [ ] Non-verbal cues
- [ ] Emotional reactions
- [ ] Workarounds mentioned
- [ ] Quotes to capture verbatim
```

### 1.2 Surveys

**When to use:** Quantitative validation, measuring satisfaction, large-sample insights.

**Best Practices:**
- Keep surveys under 5 minutes (10–15 questions max)
- Use Likert scales (1–5 or 1–7) for measurable data
- Avoid leading or double-barreled questions
- Include one open-ended question at the end
- Target a minimum 100 responses for statistical relevance
- Use skip logic to keep surveys relevant

**Question Types:**
| Type | Use Case | Example |
|------|----------|---------|
| Likert Scale | Satisfaction, agreement | "How satisfied are you with...?" (1–5) |
| Multiple Choice | Behavior patterns | "How often do you...?" |
| Ranking | Priority | "Rank these features by importance" |
| Open-ended | Exploration | "What would you change about...?" |
| NPS | Loyalty | "How likely are you to recommend...?" (0–10) |

### 1.3 Usability Testing

**When to use:** Validating designs, identifying friction, measuring task completion.

**Process:**
1. Define tasks (5–7 per session)
2. Create realistic scenarios (not instructions)
3. Recruit 5 participants (finds ~85% of issues)
4. Use think-aloud protocol
5. Measure: success rate, time on task, error rate, satisfaction

**Test Plan Template:**
```markdown
## Usability Test Plan

**Product:** [Name]
**Version/Prototype:** [Link]
**Date:** [Date]
**Facilitator:** [Name]

### Objectives
1. [Specific objective]
2. [Specific objective]

### Participants
- **Number:** 5–8
- **Criteria:** [Demographics, experience level, usage patterns]
- **Recruitment:** [Method]

### Tasks
| # | Task | Scenario | Success Criteria | Max Time |
|---|------|----------|-----------------|----------|
| 1 | [Task] | "Imagine you want to..." | [Criteria] | 3 min |
| 2 | [Task] | "You need to..." | [Criteria] | 5 min |

### Metrics
- Task success rate (target: >80%)
- Time on task
- Error rate
- SUS score (target: >68)
- Post-task satisfaction (1–5)

### Equipment
- [ ] Recording software
- [ ] Prototype/staging URL
- [ ] Consent forms
- [ ] Incentives
```

### 1.4 Diary Studies

**When to use:** Understanding behavior over time, capturing context, identifying patterns.

**Setup:**
- Duration: 1–4 weeks
- Participants: 10–15
- Frequency: Daily or event-triggered entries
- Medium: App (dscout, Indeemo) or structured journal
- Compensation: Proportional to study length

**Entry Prompt Template:**
```markdown
When you [trigger event], please log:
1. What were you doing? (context)
2. What happened? (event)
3. How did you feel? (emotion, 1–5 scale)
4. What did you do next? (action)
5. Take a screenshot or photo if possible
```

---

## 2. Frameworks

### 2.1 Jobs-to-Be-Done (JTBD)

**Format:**
```
When [situation], I want to [motivation], so I can [expected outcome].
```

**Job Map Layers:**
1. **Functional Job:** The core task the user is trying to accomplish
2. **Emotional Job:** How the user wants to feel
3. **Social Job:** How the user wants to be perceived
4. **Related Jobs:** Adjacent tasks that influence the core job

**Example:**
```markdown
**Functional:** When I'm commuting, I want to find music that matches my energy,
so I can enjoy my ride.

**Emotional:** I want to feel like the app understands my taste.

**Social:** I want to share discoveries that make me look like a tastemaker.

**Related:** Managing my library, discovering new artists, controlling playback.
```

### 2.2 Persona Canvas

**Template:**
```markdown
## Persona: [Name]

**Photo:** [Representative image]
**Quote:** "[Captures their attitude in one sentence]"

### Demographics
- **Age:** [Range]
- **Role:** [Job title / life stage]
- **Location:** [Urban/suburban/rural, region]
- **Tech Comfort:** [Low / Medium / High]

### Goals
1. [Primary goal]
2. [Secondary goal]
3. [Tertiary goal]

### Frustrations
1. [Pain point]
2. [Pain point]
3. [Pain point]

### Behaviors
- [How they currently solve the problem]
- [Tools and products they use]
- [Frequency of relevant activity]

### Context
- **Devices:** [Phone, tablet, desktop, smart speaker]
- **Usage Time:** [Morning commute, evening, etc.]
- **Environment:** [Noisy, quiet, shared space]

### Influence Map
- **Information Sources:** [Blogs, friends, social media]
- **Decision Factors:** [Price, quality, brand, convenience]
```

### 2.3 Empathy Maps

**Four Quadrants:**

| Says | Thinks |
|------|--------|
| Direct quotes from interviews | Inferred beliefs and attitudes |
| Verbatim feedback | Unspoken concerns |

| Does | Feels |
|------|-------|
| Observable actions and behaviors | Emotional states |
| Workarounds and habits | Frustrations and delights |

**Center:** User's goal or task being mapped.

---

## 3. Heuristic Evaluation — Nielsen's 10 Heuristics

Evaluate interfaces against each heuristic. Rate severity 0–4:

| Severity | Meaning |
|----------|---------|
| 0 | Not a usability problem |
| 1 | Cosmetic — fix if time allows |
| 2 | Minor — low priority fix |
| 3 | Major — important to fix, high priority |
| 4 | Catastrophe — must fix before release |

### The 10 Heuristics

**H1 — Visibility of System Status**
- Does the system inform users about what's happening?
- Examples: Loading indicators, progress bars, save confirmations, upload status
- Violation example: Form submits with no feedback; user clicks again

**H2 — Match Between System and Real World**
- Does the system use language and concepts familiar to users?
- Examples: Calendar metaphors for scheduling, shopping cart for e-commerce
- Violation example: Technical jargon in error messages ("Error 0x80004005")

**H3 — User Control and Freedom**
- Can users undo, redo, and exit unwanted states?
- Examples: Undo delete, cancel operation, back button, edit after submit
- Violation example: No way to undo a sent message or recover deleted items

**H4 — Consistency and Standards**
- Does the interface follow platform conventions and internal consistency?
- Examples: Standard icons, consistent button placement, uniform terminology
- Violation example: "Save" in one place, "Submit" in another for the same action

**H5 — Error Prevention**
- Does the system prevent errors before they happen?
- Examples: Confirmation dialogs for destructive actions, input constraints, smart defaults
- Violation example: Delete button next to edit button with no confirmation

**H6 — Recognition Rather Than Recall**
- Are options visible rather than requiring memory?
- Examples: Recent searches, visible navigation, contextual menus
- Violation example: Requiring users to remember a code from a previous screen

**H7 — Flexibility and Efficiency of Use**
- Are there accelerators for expert users?
- Examples: Keyboard shortcuts, saved preferences, batch operations, customization
- Violation example: No way to skip onboarding for returning users

**H8 — Aesthetic and Minimalist Design**
- Does every element serve a purpose?
- Examples: Clean layouts, progressive disclosure, focused content
- Violation example: Dashboard crammed with rarely-used metrics

**H9 — Help Users Recognize, Diagnose, and Recover from Errors**
- Are error messages clear, specific, and actionable?
- Examples: "Email format invalid — use name@example.com" vs "Invalid input"
- Violation example: "Something went wrong. Please try again."

**H10 — Help and Documentation**
- Is help easily searchable and task-focused?
- Examples: Contextual tooltips, searchable FAQ, guided walkthroughs
- Violation example: 50-page PDF manual with no search or table of contents

### Evaluation Report Format
```markdown
## Heuristic Evaluation Report

**Product:** [Name]
**Evaluator:** [Name]
**Date:** [Date]
**Screens Evaluated:** [List]

| # | Screen | Heuristic Violated | Issue | Severity | Recommendation |
|---|--------|-------------------|-------|----------|----------------|
| 1 | [Screen] | H[N] — [Name] | [Description] | [0–4] | [Fix] |
```

---

## 4. Information Architecture

### 4.1 Card Sorting

**Open Card Sort:** Users create their own categories — use for discovery.
**Closed Card Sort:** Users sort into predefined categories — use for validation.
**Hybrid:** Some predefined categories + user can create new ones.

**Process:**
1. Prepare 30–60 content items on cards
2. Recruit 15–20 participants
3. Use tool (OptimalSort, UserZoom, or physical cards)
4. Analyze with similarity matrix and dendrograms
5. Look for agreement >60% on groupings

### 4.2 Tree Testing

**When to use:** Validate navigation structure without visual design influence.

**Process:**
1. Create text-only hierarchy of your IA
2. Define 8–10 findability tasks
3. Recruit 50+ participants
4. Measure: success rate, directness, time to complete
5. Target: >70% success rate per task

### 4.3 Site Map Template
```markdown
## Site Map: [Product]

├── Home
│   ├── Hero / Value Proposition
│   ├── Featured Content
│   └── Quick Actions
├── Section A
│   ├── Subsection A.1
│   └── Subsection A.2
├── Section B
│   ├── Subsection B.1
│   ├── Subsection B.2
│   └── Subsection B.3
├── User Account
│   ├── Profile
│   ├── Settings
│   └── Billing
└── Help / Support
    ├── FAQ
    ├── Contact
    └── Documentation
```

---

## 5. User Flow Documentation

### Flow Diagram Format
```markdown
## User Flow: [Flow Name]

**Trigger:** [What initiates this flow]
**Actor:** [Persona or user type]
**Goal:** [What the user wants to accomplish]
**Preconditions:** [Required state before flow starts]

### Steps
1. [Entry point] → [Screen/State]
2. User [action] → System [response]
3. Decision: [condition]?
   - Yes → [Step N]
   - No → [Step M]
4. [Success state] → [Confirmation/Next flow]

### Error Paths
- [Error condition] → [Error state] → [Recovery action]

### Metrics
- **Expected completion rate:** [%]
- **Expected time to complete:** [seconds/minutes]
- **Drop-off risk points:** [Step numbers]
```

### Flow Notation
- ▢ Screen/Page
- ◇ Decision point
- ○ Start/End
- → Navigation/Action
- ⚠ Error state

---

## 6. Competitive Analysis Framework

### Analysis Template
```markdown
## Competitive Analysis: [Category]

**Date:** [Date]
**Analyst:** [Name]

### Competitors

| Dimension | Us | Competitor A | Competitor B | Competitor C |
|-----------|-----|-------------|-------------|-------------|
| **Positioning** | | | | |
| **Target Audience** | | | | |
| **Key Features** | | | | |
| **Pricing** | | | | |
| **UX Strengths** | | | | |
| **UX Weaknesses** | | | | |
| **Differentiator** | | | | |

### Feature Comparison Matrix
| Feature | Us | A | B | C |
|---------|:--:|:-:|:-:|:-:|
| [Feature 1] | ✅ | ✅ | ❌ | ✅ |
| [Feature 2] | ✅ | ❌ | ✅ | ❌ |
| [Feature 3] | ❌ | ✅ | ✅ | ✅ |

### UX Teardown (per competitor)
1. **Onboarding:** [Friction points, time to value]
2. **Core Task Flow:** [Steps, efficiency, delight moments]
3. **Error Handling:** [Quality of error messages and recovery]
4. **Accessibility:** [WCAG compliance, inclusive design]
5. **Performance:** [Load times, responsiveness]

### Opportunities
1. [Gap in market we can exploit]
2. [UX pattern competitors miss]
3. [Underserved user segment]

### Threats
1. [Competitor advantage we must counter]
2. [Emerging trend we risk missing]
```

---

## 7. Deliverable Templates

### Research Report
```markdown
## Research Report: [Study Name]

**Method:** [Interview / Survey / Usability Test / etc.]
**Date:** [Date range]
**Participants:** [N, demographics summary]
**Researcher:** [Name]

### Executive Summary
[2–3 sentences: what we did, what we found, what we recommend]

### Research Questions
1. [Question]
2. [Question]

### Key Findings
#### Finding 1: [Title]
- **Evidence:** [Quotes, data points, observations]
- **Impact:** [How this affects users/product]
- **Confidence:** [High / Medium / Low]

#### Finding 2: [Title]
[Same structure]

### Recommendations
| Priority | Recommendation | Effort | Impact | Finding |
|----------|---------------|--------|--------|---------|
| P0 | [Action] | [S/M/L] | [High/Med/Low] | #[N] |
| P1 | [Action] | [S/M/L] | [High/Med/Low] | #[N] |

### Appendix
- Raw data / transcripts
- Participant demographics table
- Methodology details
```

### Insight Card
```markdown
## Insight: [One-line insight]

**Source:** [Study name, date]
**Confidence:** [High / Medium / Low]
**Evidence:** [N] participants, [supporting data]

**Observation:** [What we observed]
**Inference:** [What it means]
**Implication:** [What we should do about it]

**Tags:** [#onboarding, #navigation, #mobile]
```

---

## Quality Standards

1. **Never assume — always cite evidence.** Every insight must link to data.
2. **Triangulate.** Use 2+ methods to validate important findings.
3. **Recruit representative users.** Avoid convenience sampling.
4. **Separate observation from interpretation.** Note what happened vs. what it means.
5. **Prioritize actionability.** Every finding must have a clear "so what."
6. **Document limitations.** State sample size, biases, and confidence levels.
7. **Use inclusive research practices.** Diverse participants, accessible materials.
8. **Timestamp everything.** Research has a shelf life — findings decay.
