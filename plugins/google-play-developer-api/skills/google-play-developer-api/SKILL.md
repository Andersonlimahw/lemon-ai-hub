---
name: google-play-developer-api
description: Google Play Developer API knowledge base and automation expert. Use when interacting with or integrating the Google Play Developer API for publishing, in-app products, subscriptions, reviews, or reporting. Note that this skill provides the API knowledge (e.g. fastlane supply, googleapis endpoints) and differs from google-play-release-agent which is for release checklists and audits.
---

# Google Play Developer API

This skill contains the comprehensive knowledge for interacting with the Google Play Developer API. 
Unlike the `google-play-release-agent` which focuses on human-in-the-loop release audits, readiness checklists, and Data Safety validation, this skill focuses strictly on API integration, payload construction, and automation via direct endpoints or tools like `fastlane supply`.

## Core Domains

### 1. Publishing API
Automate the app distribution process.
- **Concepts:** Edits system (transactional changes bundled as a draft and committed).
- **Capabilities:** Upload APKs/AABs, manage tracks (production, closed, open, internal), update store listings (localized text, graphics).
- **Integration:** Often automated via `fastlane supply` (which uses the Publishing API under the hood) or raw REST calls to `androidpublisher.edits`.

### 2. Subscriptions & In-App Purchases (IAP)
Manage monetization items programmatically.
- **Subscriptions API:** Uses the `monetization.subscriptions` endpoints. Modern standard for configuring base plans, billing periods, pricing, and offers.
- **In-App Products API:** Uses the `inappproducts` endpoint for managing one-time purchase products.
- **Purchase Management:** APIs to verify user purchase states, and modify, defer, or cancel recurring subscriptions.

### 3. Reviews API
Manage user feedback.
- **Capabilities:** List app reviews, fetch individual review details, and programmatically reply to or update replies to reviews.
- **Note:** This API is for backend management. In-app prompting is handled via the Play Core Library.

### 4. Reporting API
Extract and automate analysis of app performance data.
- **Capabilities:** Access Android Vitals programmatically (crash rates, ANR rates, wake locks).
- **Use Cases:** Build internal dashboards, aggregate with business data, and integrate stability metrics directly into CI/CD pipelines.

## Implementation Details

When automating:
- **fastlane supply:** For standard publishing tasks (uploading builds, updating metadata), prefer `fastlane supply` over writing custom API calls, as it provides a robust, well-maintained wrapper around the Publishing API.
- **Raw `googleapis` Endpoints:** Use Google's Node.js `googleapis` SDK or raw REST calls for tasks not covered by Fastlane, such as specific Subscriptions lifecycle management or querying the Reporting API for Android Vitals.

Authentication always requires a Google Cloud Service Account linked to the Google Play Console with the necessary permissions.
