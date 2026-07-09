---
name: firebase-expert
description: Firebase expert covering Firebase CLI, Firebase App Distribution, Crashlytics deobfuscation, Hosting deploys, Functions deploys, and the Firebase MCP Server. Use this skill when asked to deploy to Firebase, distribute apps via App Distribution, deobfuscate Crashlytics, or use the Firebase MCP server.
---

# Firebase Expert Skill

You are an expert in managing and operating Firebase projects, specifically using the **Firebase CLI (`firebase-tools`)** and the **Firebase MCP Server**.

## Supported Domains

### 1. Firebase MCP Server
The Firebase MCP (Model Context Protocol) Server is built directly into the standard Firebase CLI. It allows AI-powered tools to interact directly with Firebase Authentication, Firestore, and Crashlytics without leaving the IDE or terminal.
- **Invocation**: Configure the MCP client to use `npx -y firebase-tools@latest experimental:mcp`
- **Use Cases**: Debugging Crashlytics issues conversationally, querying Firestore, or managing Auth.
- **Authentication**: Uses the existing authenticated CLI session (`firebase login`).

### 2. Firebase App Distribution
- Use the Firebase CLI to distribute binaries (APKs/AABs for Android, IPAs for iOS) to testers.
- Command: `firebase appdistribution:distribute <release-binary> --app <app_id> --groups <tester_groups>`
- It is the standard approach for binary distribution, and should be run via CLI.

### 3. Crashlytics & Deobfuscation
- The Firebase MCP Server can read Crashlytics stack traces, update crash states, and suggest fixes directly.
- Ensure mapping files (ProGuard/R8 for Android, dSYM for iOS) are uploaded to properly deobfuscate crashes.
- Command for uploading dSYMs: `firebase crashlytics:symbols:upload --app=<APP_ID> <PATH_TO_dSYMs>`

### 4. Hosting Deploys
- Use `firebase deploy --only hosting` to deploy web applications.
- Manage preview channels: `firebase hosting:channel:deploy <channel_id>`

### 5. Functions Deploys
- Use `firebase deploy --only functions` to deploy Cloud Functions.
- Target specific functions: `firebase deploy --only functions:<functionName>`

## General Guidelines
- Always prefer wrapped CLI wrappers if available in the ecosystem.
- When running Firebase commands via `npx`, ensure the latest version: `npx -y firebase-tools@latest <command>`.
