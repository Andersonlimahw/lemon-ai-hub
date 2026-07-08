# RevenueCat / IAP Checklist

Validate IAP before App Review. BLOCKER items force NO_GO.

## Products
- [ ] All products created in App Store Connect (consumables, non-consumables, auto-renewable subs)
- [ ] Product IDs in code match App Store Connect exactly
- [ ] Agreements/Tax/Banking accepted in App Store Connect (else products won't serve)
- [ ] Products in "Ready to Submit" or approved state

## Offerings & Entitlements
- [ ] Current Offering configured in RevenueCat dashboard
- [ ] Entitlements mapped to products
- [ ] Packages attached to Offering
- [ ] Offering ID referenced in code matches dashboard

## Sandbox
- [ ] Sandbox tester account created in App Store Connect
- [ ] Sandbox purchase tested end-to-end on a TF build
- [ ] Restore Purchases tested after sandbox purchase
- [ ] Subscription renewal/cancellation flow verified in sandbox

## Restore Purchases — ⚠️ BLOCKER
- [ ] Restore path present in code (heuristic check)
- [ ] Restore button reachable from paywall + settings
- [ ] Restore handles "no purchases" gracefully

## Paywall & Fallback
- [ ] Paywall shows price, period, terms
- [ ] Subscription auto-renew terms disclosed near purchase
- [ ] Paywall has graceful fallback if offering/products fail to load
- [ ] No external payment links / web checkout — ⚠️ BLOCKER

## Webhook / Ledger (if backend-managed)
- [ ] RevenueCat webhook → backend verified
- [ ] Entitlement ledger idempotent (no double-grant)
- [ ] Refund/cancellation events handled

## Wording Risk — ⚠️ BLOCKER
- [ ] No "earn money / ganhe dinheiro / lucro / renda garantida / cashout / saque garantido"
- [ ] Virtual currency (coins) framed as non-monetary, non-withdrawable
- [ ] Subscription cancellation instructions reachable

## Public Keys
- [ ] `EXPO_PUBLIC_RC_IOS_KEY` present (public SDK key only)
- [ ] No secret RC API keys in client code
