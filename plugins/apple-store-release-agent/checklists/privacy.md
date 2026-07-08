# App Privacy Readiness Checklist

Apple App Privacy ("Privacy Nutrition Labels") + legal links. BLOCKER items force NO_GO.

## Legal URLs — ⚠️ BLOCKER
- [ ] Privacy Policy URL present and reachable (https)
- [ ] Terms of Service URL present and reachable (https)
- [ ] Both URLs open in-app or via in-app browser (not forced out of app)

## Data Collection — map each SDK
For each detected SDK, confirm data types + purposes declared in App Store Connect:

- [ ] **Firebase Auth** → Contact Info / Identifiers (email, user ID)
- [ ] **Firestore / Storage** → User Content (photos, user-generated content)
- [ ] **Firebase Analytics** → Usage Data (product interaction, diagnostics)
- [ ] **Crashlytics** → Diagnostics (crash data, performance)
- [ ] **RevenueCat** → Purchases (transaction history)
- [ ] **Notifications (APNs/Messaging)** → Identifiers (device ID)
- [ ] **Location** → Location (precise/coarse) + clear in-app purpose
- [ ] **Camera** → Photos/Videos (if used)
- [ ] **Photo Library** → Photos/Videos (if used)

> **Suggestion only.** The agent never auto-declares labels. Confirm against Apple's data-type taxonomy and the SDK's real behavior.

## Permissions (infoPlist usage strings)
- [ ] Every requested permission has a clear `NSXxxUsageDescription`
- [ ] Permission strings explain **why** (not just "we need it")

## Tracking (ATT)
- [ ] If any tracking SDK present → ATT prompt configured
- [ ] `NSUserTrackingUsageDescription` present and clear
- [ ] Tracking purpose declared in App Privacy

## Account Deletion — ⚠️ BLOCKER
- [ ] In-app deletion offered (matches signup)
- [ ] Deletion behavior documented in Privacy Policy

## Data Retention
- [ ] Retention periods documented in Privacy Policy
- [ ] No indefinite retention without justification

## Secrets Hygiene — ⚠️ BLOCKER
- [ ] No `.env*`, `GoogleService-Info.plist`, or service-account keys committed
- [ ] Public envs (`EXPO_PUBLIC_*`) reviewed — only non-secret values
- [ ] No tokens/keys in source, screenshots, or metadata
