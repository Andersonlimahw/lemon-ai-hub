# Android Permissions Checklist

## Declared permissions
- [ ] List every declared permission (manifest + app.json)
- [ ] Each maps to a real, visible feature
- [ ] No permissions declared "just in case"

## Runtime permission UX
- [ ] Pre-prompt rationale shown (why we need it)
- [ ] Graceful denial path (feature disabled, not crash)
- [ ] Re-prompt via settings if permanently denied

## Permission purpose
- [ ] CAMERA — capture feature
- [ ] RECORD_AUDIO — voice feature
- [ ] LOCATION — map / nearby / tagging
- [ ] NOTIFICATIONS (Android 13+) — push
- [ ] MEDIA (Android 13+) — photo picker

## Sensitive / high-scrutiny
- [ ] ACCESS_BACKGROUND_LOCATION — strong justification or remove
- [ ] READ_CONTACTS — core feature or remove
- [ ] MANAGE_EXTERNAL_STORAGE — remove (use scoped storage)
- [ ] QUERY_ALL_PACKAGES — approved use case or remove
- [ ] SEND_SMS / READ_SMS — PAY policy or remove
- [ ] AD_ID — declare in Data Safety

## Cleanup
- [ ] No deprecated READ/WRITE_EXTERNAL_STORAGE (Android 13+)
- [ ] No unused permissions detected
- [ ] No permissions with no runtime UI where required

## Policy
- [ ] No permission combination that triggers high-risk review (e.g. SMS + contacts)
- [ ] Permissions align with Data Safety declarations
