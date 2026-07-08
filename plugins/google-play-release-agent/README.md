# Google Play Release Agent

AI release agent for the Google Play Store. **Prepares, audits, reports — never publishes.**

Built for the first target app **Vai ter fut** (React Native + Expo + Firebase + RevenueCat, i18n PT/EN/ES), but generic with presets for this stack.

## What it does

- **Build readiness**: `app.json`/`app.config.*`, `eas.json`, `android.package`, `versionCode`/`versionName`, AAB output, mock flag, quality-gate scripts.
- **Play Console metadata**: short/full description, release notes, screenshots, risky-term scan.
- **Data Safety Form**: detects SDKs (Firebase, RevenueCat, Analytics, Crashlytics…) and produces a review checklist. **Never auto-fills.**
- **Android permissions**: manifest + `app.json` permissions; sensitive/unused detection with expected justification.
- **i18n parity** (PT/EN/ES): missing/orphan keys, obvious hardcoded strings.
- **RevenueCat / IAP**: public RC keys, products in code vs metadata, restore, paywall fallback, wording risk.
- **Policy-risk copy**: classifies LOW/MEDIUM/HIGH and suggests safer wording.
- **GO / NO-GO**: final decision with all blockers listed.

## Install

This plugin ships with the [Lemon AI Hub](https://github.com/Andersonlimahw/lemon-ai-hub) marketplace:

```text
/plugin marketplace add Andersonlimahw/lemon-ai-hub
/plugin install google-play-release-agent@lemon-ai-hub
```

## Use

```
/google-play-release-agent
/google-play-release-agent go-no-go
/google-play-release-agent data-safety
/google-play-release-agent release-notes
```

Or in plain language:

> "Use google-play-release-agent para auditar meu app Android antes da Google Play."
> "Valide RevenueCat, Data Safety e permissões antes do review."
> "Crie release notes para o Google Play Console."
> "Prepare meu app para internal testing."

## Scripts

Each script is a standalone Node.js ESM (`.mjs`), zero heavy dependencies. Run directly:

```bash
node scripts/validate-android-release.mjs [--project <path>] [--output <path>] [--strict] [--json]
```

| Script | Validates |
| --- | --- |
| `validate-android-release.mjs` | Expo/EAS config, package, versionCode, AAB, quality gates, mock flag |
| `validate-play-store-metadata.mjs` | Store listing + risky-term scan |
| `validate-data-safety-readiness.mjs` | Detected SDKs vs privacy docs (suggest only) |
| `validate-android-permissions.mjs` | Manifest + app.json permissions, sensitive/unused |
| `validate-i18n-parity.mjs` | PT/EN/ES key parity, hardcoded strings |
| `validate-revenuecat-iap.mjs` | RC keys, products, restore, paywall fallback |
| `validate-no-policy-risk-copy.mjs` | LOW/MEDIUM/HIGH copy classification |

## Outputs

Reports written to project root: `ANDROID_RELEASE_REPORT.md`, `GOOGLE_PLAY_REVIEW_RISK_REPORT.md`, `DATA_SAFETY_READINESS_REPORT.md`, `ANDROID_PERMISSIONS_REPORT.md`, `REVENUECAT_IAP_ANDROID_REPORT.md`, `INTERNAL_TESTING_CHECKLIST.md`, `PLAY_STORE_RELEASE_NOTES.md`, `ANDROID_RELEASE_GO_NOGO.md`.

## Safety

The agent never publishes, rolls out, changes prices, or edits Data Safety / App Content without explicit human approval. See `SKILL.md` → Security policy.

## License

MIT © Anderson Lima
