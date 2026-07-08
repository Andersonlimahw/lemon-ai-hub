# Expo / EAS Submit Checklist

Build + submit via EAS. Items marked `# APPROVAL` require explicit human confirmation before running.

## EAS Auth & Credentials
- [ ] `eas login` confirmed (whoami shows correct account)
- [ ] Apple App Store Connect API key or Apple ID credentials configured
- [ ] Credentials resolved (distribution cert + provisioning profile) — let EAS manage or explicit

## Build (Production)
- [ ] `eas.json` has `production` build profile (release channel, no dev client)
- [ ] `app.json`/`app.config` `ios.bundleIdentifier` set, non-placeholder
- [ ] Build version + build number incremented vs last release
- [ ] `EXPO_PUBLIC_*` envs set for production (mock flag OFF)
- [ ] Command (generate, do NOT auto-run):
  ```bash
  eas build --platform ios --profile production --non-interactive   # APPROVAL
  ```

## Submit
- [ ] `eas.json` submit profile points to `latest` production build
- [ ] `ascAppId` (App Store Connect app ID) configured if submitting programmatically
- [ ] Command (generate, do NOT auto-run):
  ```bash
  eas submit --platform ios --profile production --latest   # APPROVAL
  ```

## TestFlight Processing
- [ ] Build status "Processing" → "Ready" in App Store Connect (human-monitored)
- [ ] Add internal testers in TestFlight
- [ ] Run `checklists/testflight-smoke.md` on the TF build

## Pre-Submit Sanity
- [ ] `node scripts/validate-ios-release.mjs --project . --strict` passes
- [ ] Decision is GO / GO_WITH_WARNINGS (no open BLOCKER)
- [ ] Review Notes + metadata attached in App Store Connect
