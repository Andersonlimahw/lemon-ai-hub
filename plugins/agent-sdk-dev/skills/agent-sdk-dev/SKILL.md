---
name: agent-sdk-dev
description: A comprehensive skill for creating new Agent SDK applications. Guides through creating TypeScript or Python SDK apps with verification.
---

# Agent SDK Development

A comprehensive plugin for creating and verifying Agent SDK applications in Python and TypeScript.

## Overview

The Agent SDK Development Plugin streamlines the entire lifecycle of building Agent SDK applications, from initial scaffolding to verification against best practices. It helps you quickly start new projects with the latest SDK versions and ensures your applications follow official documentation patterns.

## Commands

### `/new-sdk-app [project-name]`
Interactive command that guides you through creating a new Agent SDK application.
- Asks clarifying questions about your project (language, name, agent type, starting point)
- Checks for and installs the latest SDK version
- Creates all necessary project files and configuration
- Sets up proper environment files (.env.example, .gitignore)
- Provides a working example tailored to your use case
- Runs type checking (TypeScript) or syntax validation (Python)
- Automatically verifies the setup using the appropriate verifier agent
