---
name: prompts-mobile-release
description: Ready-to-paste prompts for mobile release — App Store and Google Play go/no-go audits, App Store Connect automation, Play Console API, store listing optimization, and macOS/SwiftUI validation loops.
---

# Prompts — Mobile & Release

Recipes to get an app off the machine and into the store with an auditable decision. Release agents decide GO/NO_GO — they never submit or pay without human approval.

## R1 — iOS go/no-go

**Skills:** `apple-store-release-agent`
**When:** an Expo/RN iOS build is a release candidate; you want an audit before hitting submit.

```text
Run apple-store-release-agent on app <app>: audit the iOS build,
App Store metadata, App Privacy, TestFlight, IAP/RevenueCat, i18n
parity, screenshots, and review notes.
Success: GO / GO_WITH_WARNINGS / NO_GO decision with every blocker
listed, actionable, and owned; nothing submitted without my
approval.
```

## R2 — Android go/no-go + Play automation

**Skills:** `google-play-release-agent` + `google-play-developer-api`
**When:** an Android release; tracks, staged rollout, and listing via API.

```text
Run google-play-release-agent on app <app> for the go/no-go of
release <version>. Where automation fits (upload to track
<internal/closed/production>, rollout <X>%), use
google-play-developer-api and show me the steps before executing.
Success: auditable decision + rollout plan per track; no
irreversible action without confirmation.
```

## R3 — App Store Connect automation

**Skills:** `app-store-connect-api`
**When:** a repetitive App Store Connect task: TestFlight, IAP, provisioning, metadata, reports.

```text
Automate with app-store-connect-api: <task — e.g. distribute build
<n> to TestFlight group <group>, create IAP <product>, download
sales report for <period>>.
Success: operation executed with the API response as evidence;
credentials never in a log or in code.
```

## R4 — A listing that converts

**Skills:** `aso`
**When:** the app is live but installs are weak — audit the listing before buying traffic.

```text
Audit with aso the listing for <app> (<App Store/Play URL>):
keywords, title/subtitle, screenshots, conversion vs. competitors
<apps>.
Success: prioritized list of listing changes with an impact
hypothesis each; ready copy within character limits.
```

## See also

- `vercel-react-native-skills` — RN/Expo performance before release (track [prompts-vercel-react](../prompts-vercel-react/SKILL.md)).
- `computer-use-swiftui-loop` — visual validation loop for macOS/SwiftUI apps (Computer Use, Codex app only).
- `imagegen-frontend-mobile` — generate listing screenshots/artwork.
