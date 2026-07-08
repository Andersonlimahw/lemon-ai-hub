# Data Safety Checklist

Google Play Data Safety Form. **Review against detected SDKs — do not auto-fill.**

## Policy URL
- [ ] Privacy Policy URL live and reachable
- [ ] Privacy Policy describes each data type collected

## Data collection
- [ ] Personal info (name, email, phone) declared only if collected
- [ ] Financial info (purchase history) declared if IAP
- [ ] Health/fitness — N/A or declared
- [ ] Messages — N/A or declared
- [ ] Photos/videos — declared if camera/storage
- [ ] Audio files — declared if mic
- [ ] Files/docs — N/A or declared
- [ ] Calendar — N/A or declared
- [ ] Contacts — declared if contacts permission
- [ ] App activity (taps, history) — declared if analytics
- [ ] Web browsing — N/A or declared
- [ ] App info/performance — declared if crash/diagnostic
- [ ] Device/other IDs — declared if push token / advertising ID

## Data sharing
- [ ] Data shared with third parties declared (Firebase, RevenueCat, etc.)
- [ ] Each shared type has a recipient + purpose

## Security
- [ ] "Data encrypted in transit" checked ONLY if TLS enforced end-to-end
- [ ] Data deletion / account deletion declared where applicable

## SDK-driven disclosures
- [ ] Firebase Auth → personal info
- [ ] Firestore / Storage → user-generated content
- [ ] Firebase Analytics → app activity
- [ ] Crashlytics → diagnostics (crash logs)
- [ ] RevenueCat → purchase history
- [ ] Push notifications → device/other IDs (token)
- [ ] Location SDK → location
- [ ] Camera → photos/videos
- [ ] Advertising SDK → advertising ID

## Sign-off
- [ ] Human reviewed every declaration against actual app behavior
- [ ] Never reduced a declaration without technical evidence
