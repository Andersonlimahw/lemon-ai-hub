# App Store Review Notes

<!-- Paste into App Store Connect → App Information → "Notes for Reviewer".
     Keep concise, factual, and reviewer-friendly. -->

## App Summary
<!-- 2–4 sentences: what the app does, primary use case. -->
App: <NAME>. Category: <CATEGORY>. Platform: iOS.
<NAME> is a <one-line purpose, e.g. amateur football match organizer>. Users can <key actions>.

## Demo Account (login-gated)
- Email: `reviewer+<app>@example.com`
- Password: `<PASSWORD>`
- Notes: account is pre-populated with sample data for testing.

## How to Test (key flows)
1. Launch the app → log in with the demo account.
2. <Primary flow, e.g. Create a match / join a group>.
3. Open Settings → <Account> → verify flows below.

## In-App Purchases (Sandbox)
- This app uses Apple IAP via RevenueCat.
- Sandbox tester: `<sandbox-tester@email.com>` (configured in App Store Connect).
- Products to test:
  - `<product_id_1>` — <description, e.g. Pro monthly subscription>
  - `<product_id_2>` — <description, e.g. Soccer Coins pack>
- Restore Purchases is available in Settings → <Account>.

## Account Deletion
- Path: Settings → Account → Delete Account.
- Deletion removes the account and associated user data per our Privacy Policy.

## Feature Flags / Special Config
- <Flag>: <value the reviewer should see> (e.g. mock data is OFF in this build).
- <Any backend env the reviewer should know about>.

## Sign-in Methods
- Email/password, <Sign in with Apple / Google> where applicable.
- Sign in with Apple is offered wherever other third-party sign-in is offered.

## Support Contact
- Email: <support@email>
- Privacy Policy: <https://...>
- Terms of Service: <https://...>
