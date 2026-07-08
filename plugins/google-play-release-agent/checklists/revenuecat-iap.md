# RevenueCat / IAP Checklist

## Products
- [ ] Every product ID in code exists in Play Console
- [ ] Base plans created (auto-renewing / one-time as needed)
- [ ] Offers configured (intro/free trial if applicable)
- [ ] Entitlements mapped in RevenueCat dashboard

## Connection
- [ ] Android package connected to RevenueCat
- [ ] Play Console service account key linked to RevenueCat
- [ ] Public Android SDK key in `EXPO_PUBLIC_RC_ANDROID_KEY`

## Flows
- [ ] Purchase flow works on a clean install
- [ ] **Restore purchases** works (required by Play)
- [ ] Paywall fallback shown if offering fails to load
- [ ] Entitlement granted after purchase
- [ ] Entitlement revoked after refund/cancel

## Testing
- [ ] Sandbox / test purchase completed
- [ ] License testers added in Play Console
- [ ] Subscription lifecycle tested (renew, cancel, grace period)

## Wording
- [ ] No gambling/betting/money-guarantee language in paywall
- [ ] Virtual currency (e.g. Soccer Coins) framed as in-app only, no real-money payout
- [ ] Prices pulled from Play (not hardcoded)
- [ ] Terms of purchase clear

## Operations
- [ ] Webhook / ledger reconciles transactions
- [ ] Refund handling tested
