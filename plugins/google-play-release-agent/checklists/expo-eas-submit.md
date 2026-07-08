# Expo / EAS Submit Checklist (Android)

## Setup
- [ ] EAS CLI logged in (`eas login`)
- [ ] Android credentials configured (keystore / Play signing)
- [ ] Keystore managed by EAS or supplied securely
- [ ] Play Console service account key available (gitignored)

## Build
- [ ] `eas build --platform android --profile production`
- [ ] Output is `.aab` (not `.apk`)
- [ ] `EXPO_PUBLIC_USE_MOCK=false` in production profile
- [ ] versionCode incremented
- [ ] Package name matches Play Console app

## Submit
- [ ] `eas submit --platform android`
- [ ] Track selected (internal → closed → production, never skip to prod)
- [ ] Service account key path set in `eas.json` submit
- [ ] Submission completes without error

## Verify
- [ ] Build appears in Play Console internal track
- [ ] Install works from internal track
- [ ] No signing mismatch warnings
