# Computer Use macOS UI Validation Loop

## Objective

Validate the real UI of the macOS application with Computer Use (Note: Computer Use is currently exclusive to the Codex app), save reproducible findings, and apply surgical fixes only in View or UI Store/ViewModel layers.

## Standard Scenarios

1. Main application window layout and stability.
2. Sidebar and navigation lists.
3. Detail panes and main content areas.
4. Settings and configuration modals.

## Execution Steps

1. Capture a screenshot and the accessibility tree of the target macOS application.
2. Check layout for: truncated text, overlapping controls, missing accessibility labels, empty states.
3. Check navigation safety: alternate between views, use search inputs, toggle sidebars.
4. Record findings in `findings.md`.
5. Map the finding to the likely SwiftUI/AppKit source file or ViewModel.
6. Apply a minimal patch in the presentation layer.
7. Verify the fix using local build tools (e.g., `swift build` and `swift test`).
8. Reopen/re-capture with Computer Use to confirm the visual finding is fixed.

## Blocked Actions (Require Confirmation)

- Removing projects, documents, or artifacts.
- Running destructive background tasks or real agents.
- Creating commits, pushes, or PRs via the UI.
- Altering credentials, permissions, keys, or system settings.
