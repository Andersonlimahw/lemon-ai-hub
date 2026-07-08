# Apple Review Checklist

Walk this checklist before any submission. Items marked ⚠️ BLOCKER force NO_GO if failed.

## App Completeness
- [ ] App launches without crash on cold start
- [ ] All primary flows functional (no "coming soon", no dead buttons)
- [ ] No placeholder/lorem-ipsum content visible to users
- [ ] No debug/staging menus reachable in prod build
- [ ] `EXPO_PUBLIC_USE_MOCK` is NOT `true` in production env

## Metadata Accuracy
- [ ] Description matches shipping functionality
- [ ] Keywords relevant, no competitor trademarks, no spam
- [ ] Screenshots from the **shipping** build, correct device sizes
- [ ] App category + age rating correct
- [ ] No forbidden wording (aposta, betting, gambling, cashout garantido, ganhe dinheiro, lucro, renda garantida, saque garantido) — ⚠️ BLOCKER

## Login & Demo Account
- [ ] Demo account credentials provided in Review Notes — ⚠️ BLOCKER (login-gated apps)
- [ ] Demo account has enough data/state to exercise main flows
- [ ] Third-party login (Sign in with Apple/Google) configured and documented

## Account Deletion — ⚠️ BLOCKER (if signup exists)
- [ ] In-app account deletion reachable from settings
- [ ] Deletion explains data retention/erasure behavior
- [ ] Deletion path tested end-to-end

## IAP / Subscriptions
- [ ] All purchasable items use Apple IAP (no external payment links) — ⚠️ BLOCKER
- [ ] Restore Purchases reachable and functional — ⚠️ BLOCKER
- [ ] Subscription terms + auto-renew disclosed near purchase
- [ ] Virtual currency framed as non-monetary (no cash/withdraw wording) — ⚠️ BLOCKER

## Privacy & Legal
- [ ] Privacy Policy URL reachable — ⚠️ BLOCKER
- [ ] Terms of Service URL reachable — ⚠️ BLOCKER
- [ ] App Privacy labels declared in App Store Connect
- [ ] ATT prompt present if tracking SDKs used

## Stability
- [ ] No known crashes on key devices (iPhone + iPad if universal)
- [ ] Offline / poor-network states handled gracefully
- [ ] No ANR / infinite spinners on main flows

## Review Notes
- [ ] APP_STORE_REVIEW_NOTES.md populated (see templates/review-notes.md)
- [ ] Special configurations flagged for reviewer (feature flags, env)

## Final
- [ ] Build version incremented vs last App Store version
- [ ] Decision is GO or GO_WITH_WARNINGS (no open BLOCKER)
