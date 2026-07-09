---
name: app-store-connect-expert
description: Expert agent for the Apple Store Connect API. Use when the user asks questions about the App Store Connect API or needs to automate tasks involving TestFlight, In-App Purchases, Provisioning, App Metadata, Reporting, or Game Center.
---

# Apple Store Connect API Expert

This skill acts as the entry point and overarching knowledge base for the Apple Store Connect API.
It is composed of multiple specialized skills that cover the specific domains of the API:

- **App Management & Metadata**: Managing app versions, screenshots, localizations, and app reviews.
- **TestFlight & Provisioning**: Managing beta testers, build deployments, profiles, and certificates.
- **Monetization**: In-app purchases, Subscriptions, and Pricing.
- **Reporting & Analytics**: Sales, Financial reports, and app analytics.
- **Game Center & App Clips**: Managing achievements, leaderboards, and App Clip experiences.
- **Users & Customer Reviews**: Managing team roles and responding to user reviews.

## Capabilities
When tasked with an App Store Connect API operation, refer to the corresponding domain skill to access detailed endpoint paths, required parameters, and best practices.

## OpenAPI Reference
The agent derives its knowledge from the official App Store Connect OpenAPI specification. Always ensure requests match the expected payload structure defined in the `openapi.oas.json`.
