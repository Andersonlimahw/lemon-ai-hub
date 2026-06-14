---
name: incident-runbook
description: Incident response runbooks, on-call workflows, and postmortem templates. Generates severity-tiered runbooks, communication templates, timeline reconstruction, and blameless postmortem docs. Use when user is in an incident, doing on-call prep, writing a postmortem, or building incident response playbooks.
---

# Incident Runbook

Structured incident response — from first alert to blameless postmortem.

## Quick Start

```
/incident-runbook new <service>     — create runbook for a service
/incident-runbook triage            — immediate triage checklist
/incident-runbook postmortem        — generate postmortem from timeline
/incident-runbook comms             — draft stakeholder communication
/incident-runbook playbook <error>  — generate playbook for specific error type
```

## Severity Matrix

| Sev | Criteria | Response Time | Who |
|-----|----------|---------------|-----|
| **P0** | Prod down, data loss, security breach | 5 min | IC + Eng lead + CTO |
| **P1** | Core feature degraded, >10% users affected | 15 min | IC + On-call |
| **P2** | Non-critical feature degraded, workaround exists | 1 hour | On-call |
| **P3** | Minor issue, low user impact | Next business day | Team |

## Immediate Response (First 15 Minutes)

```
[ ] 1. Acknowledge alert (prevents duplicate paging)
[ ] 2. Assess severity → declare P0/P1/P2/P3
[ ] 3. P0/P1: Open incident Slack channel #inc-YYYY-MM-DD-<slug>
[ ] 4. Assign Incident Commander (IC) — single decision owner
[ ] 5. Start timeline doc (incident log)
[ ] 6. Notify stakeholders (template below)
[ ] 7. Do NOT start fixing until you understand the blast radius
```

## Stakeholder Communication Templates

### Initial (within 5 min of P0/P1)
```
🔴 INCIDENT DECLARED — P[0/1]
Service: [service name]
Impact: [what users can't do]
Status: Investigating
IC: @[name]
Channel: #inc-[slug]
Next update: in 15 min
```

### Update (every 15–30 min)
```
🟡 INCIDENT UPDATE — P[0/1] — [HH:MM]
Status: [Investigating / Identified / Fixing / Monitoring]
Impact: [current user impact]
Root cause hypothesis: [best theory]
Actions taken: [what you did]
Next update: in [X] min
```

### Resolution
```
✅ INCIDENT RESOLVED — P[0/1] — [HH:MM]
Duration: [X hours Y min]
Impact: [X users affected, Y% of traffic]
Root cause: [brief]
Fix applied: [what was done]
Postmortem: [link] — due [date]
```

## Triage Checklist

```
TRIAGE — [service] — [timestamp]
=====================================
[ ] Is the service responding? (curl / health endpoint)
[ ] Is it all users or a subset? (region / customer / feature)
[ ] When did it start? (check deploy history, cron jobs, traffic spike)
[ ] What changed recently? (git log, infra changes, dependency updates)
[ ] Is the database healthy? (query time, connections, replication lag)
[ ] Is a dependency degraded? (check status pages, upstream errors)
[ ] Are error rates spiking or flat-lining?
[ ] Is it a traffic spike or a code regression?
```

## Runbook Template (per service)

```markdown
# Runbook: [Service Name]

## Contacts
- On-call: @[team-pagerduty-rotation]
- Escalation: @[eng-lead] → @[cto]
- External: [vendor support link]

## Dashboards
- [Grafana link]
- [Datadog link]
- [Log query link]

## Common Alerts and Fixes

### Alert: High Error Rate (>1%)
1. Check recent deploys: `git log --since="2 hours ago"`
2. Check DB: `SELECT * FROM pg_stat_activity WHERE state='active'`
3. Rollback if code change: `kubectl rollout undo deploy/[service]`

### Alert: High Latency (p99 > 1s)
1. Check DB slow queries
2. Check Redis hit rate
3. Check external API timeouts

### Rollback Procedure
```bash
# Kubernetes
kubectl rollout undo deployment/[service]
kubectl rollout status deployment/[service]

# Vercel
vercel rollback [deployment-url]

# Railway / Render
# Use dashboard instant rollback button
```
```

## Blameless Postmortem Template

```markdown
# Postmortem: [Incident Title]
**Date:** YYYY-MM-DD  |  **Severity:** P[0/1]  |  **Duration:** Xh Ymin
**Authors:** @[names]  |  **Review date:** [date + 7 days]

## Summary
[2–3 sentence description of what happened, impact, and resolution]

## Impact
- Users affected: ~X (Y% of total)
- Duration: HH:MM–HH:MM UTC
- Revenue impact: $X (if applicable)

## Timeline (UTC)
| Time | Event |
|------|-------|
| 14:32 | Alert fired: error rate >5% |
| 14:35 | On-call acknowledged |
| 14:41 | Identified bad deploy at 14:20 |
| 14:45 | Rollback initiated |
| 14:52 | Error rate normalized |
| 15:10 | Declared resolved |

## Root Cause
[Technical root cause. What failed and why.]

## Contributing Factors
- [Factor 1: e.g., no canary deployment]
- [Factor 2: e.g., alert threshold too high]

## What Went Well
- [e.g., fast detection via synthetic monitoring]

## Action Items
| Action | Owner | Due |
|--------|-------|-----|
| Add canary deploy step to CI | @dev | 2026-06-21 |
| Lower error rate alert to 0.5% | @ops | 2026-06-17 |
```
