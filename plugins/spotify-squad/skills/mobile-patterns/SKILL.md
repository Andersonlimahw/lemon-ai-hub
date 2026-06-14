---
name: mobile-patterns
description: >
  Mobile development patterns and best practices. Use for cross-platform architecture, native module integration, navigation, offline-first, push notifications, and app store deployment.
---

# Mobile Patterns

## 1. Cross-Platform Architecture
- **Shared Core**: Maximize business logic sharing between platforms using cross-platform frameworks (React Native, Flutter) or KMM (Kotlin Multiplatform Mobile).
- **Platform-Specific UI**: Respect platform conventions (iOS Cupertino vs Android Material) when appropriate, using platform-specific file extensions or conditional rendering.

## 2. Navigation Patterns
- **Stack Navigation**: Push new screens onto the stack and pop them off to go back.
- **Tab Navigation**: Provide quick access to top-level views.
- **Drawer Navigation**: Use a hidden side menu for secondary navigation.
- **Deep Linking**: Configure URLs that navigate directly to specific content within the app.

## 3. Native Module Integration
- **Bridging**: Write custom native code (Java/Kotlin or Objective-C/Swift) and expose it to JavaScript/Dart.
- **Turbo Modules / JSI**: (React Native) Use direct C++ integration for high-performance synchronous calls.
- **Platform Channels**: (Flutter) Communicate between Dart and native code securely.

## 4. Offline-First
- **Local Database**: Use SQLite, WatermelonDB, or Realm to persist data locally.
- **Sync Strategies**: Implement optimistic UI updates and background sync queues.
- **Conflict Resolution**: Handle data conflicts between local edits and remote server state.

## 5. Push Notifications
- **FCM / APNs**: Configure Firebase Cloud Messaging for Android and Apple Push Notification service for iOS.
- **Rich Notifications**: Include images, action buttons, and custom payloads in notifications.
- **Badge Management**: Keep the app icon badge count in sync with unread notifications.

## 6. Performance
- **FPS Monitoring**: Aim for 60fps (or 120fps) for smooth animations and interactions.
- **Memory Management**: Profile memory usage to avoid OOM (Out Of Memory) crashes, especially with image-heavy views.
- **Startup Time**: Optimize app load time by deferring non-critical initializations.

## 7. App Store & Deployment
- **Metadata**: Prepare compelling descriptions, keywords, and release notes.
- **Screenshots**: Generate localized, high-resolution screenshots for all required device sizes.
- **Versioning**: Follow semantic versioning and increment build numbers automatically.

## 8. CI/CD
- **Fastlane**: Automate beta deployments, releases, and screenshots.
- **EAS (Expo Application Services)**: Manage builds and OTA (Over The Air) updates for React Native.
- **Code Signing**: Manage provisioning profiles and keystores securely.
- **TestFlight / Play Console**: Distribute beta builds to testers and manage the release tracks.
