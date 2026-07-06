# computer-use-swiftui-loop

A generic Lemon AI Hub plugin that provides an agentic testing loop for macOS applications (such as SwiftUI or AppKit apps) using Computer Use. **Note: The Computer Use feature is currently exclusive to the Codex app.**

This plugin automates the UI and visual verification loop by navigating the app safely, taking screenshots, analyzing the accessibility tree (AX tree), logging findings, and deploying minimal fixes.

## Contents

- **skills/SKILL.md**: The primary skill that orchestrates the workflow.
- **agents/**:
  - `computer-use-swiftui-validator.md`: Subagent responsible for investigating the UI and logging reproducible issues.
  - `computer-use-fix-implementer.md`: Subagent responsible for mapping findings to views and applying surgical fixes.
- **templates/**:
  - `loop.md`: Standard execution plan to be customized per project.
  - `findings.md`: Empty template for logging visual bugs.
  - `evals.json`: Template for continuous evaluation of the loop.

## Usage

1. Copy the contents of `templates/` to your target repository (e.g. `docs/test-plans/computer-use-loop/`).
2. Run `/computer-use-swiftui-loop` or prompt an agent to validate the application.
3. Review the findings and explicitly approve fixes.
