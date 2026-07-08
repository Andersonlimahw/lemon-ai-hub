# iOS Release Report

> Auto-fill from the agent's audit outputs. The agent writes this; humans review.

**App:** <name>
**Bundle ID:** <com.example.app>
**Version / Build:** <x.y.z> / <n>
**Target:** Apple App Store (iOS)
**Decision:** <!-- GO | GO_WITH_WARNINGS | NO_GO -->
**Generated:** <ISO date>

---

## Summary
<2–4 sentences: overall readiness, headline risk, recommended action.>

## Build Readiness
- bundleIdentifier: <OK | MISSING>
- app.json/app.config: <OK | MISSING>
- eas.json production profile: <OK | MISSING>
- Build/version incremented: <OK | UNKNOWN>
- Mock flag off for prod: <OK | WARNING>
- Quality-gate scripts present: <OK | MISSING>

## App Store Metadata
- Description: <OK | MISSING>
- Keywords: <OK | MISSING>
- Release notes: <OK | MISSING>
- Review notes: <OK | MISSING>
- Screenshots: <OK | MISSING>
- Risky wording: <NONE | LIST>

## Privacy
- Privacy Policy URL: <OK | MISSING — BLOCKER>
- Terms URL: <OK | MISSING — BLOCKER>
- App Privacy labels: <DECLARED | NEEDS REVIEW>
- SDK data collection map: <attached>
- ATT prompt (if tracking): <OK | N/A | MISSING>
- Secrets committed: <NONE | DETECTED — BLOCKER>

## IAP / RevenueCat
- RC SDK present: <YES | NO>
- Public iOS key: <OK | MISSING>
- Products referenced vs configured: <CONSISTENT | DRIFT>
- Restore Purchases: <PRESENT | MISSING — BLOCKER>
- Paywall fallback: <OK | WARNING>
- Wording risk: <NONE | LIST>

## TestFlight
- Build submitted: <YES | PENDING>
- Processing status: <READY | PROCESSING | N/A>
- Smoke checklist: <PASSED | PENDING> (see TESTFLIGHT_SMOKE_CHECKLIST.md)

## Risks
| # | Severity | Area | Finding | Action |
| --- | --- | --- | --- | --- |
| 1 | BLOCKER/WARNING/INFO | <area> | <finding> | <action> |

## Required Manual Actions
1. <action — mark `# APPROVAL` if it touches submit/pay/publish/privacy>
2. ...

## Final Decision
<!-- GO / GO_WITH_WARNINGS / NO_GO + one-line rationale -->
<DECISION> — <rationale>
