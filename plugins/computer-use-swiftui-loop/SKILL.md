---
name: computer-use-swiftui-loop
description: Executes a continuous validation loop for macOS apps using Computer Use (Note: Computer Use is currently exclusive to the Codex app), recording layout/accessibility findings and applying/verifying small SwiftUI/UI fixes.
---

# computer-use-swiftui-loop

This skill guides the automated or manual testing and visual bug-fixing loop for native macOS applications (such as SwiftUI/AppKit apps) using Computer Use. **Note: The Computer Use feature is currently exclusive to the Codex app.**

## Triggers
- Request to validate a macOS app visual layout using Computer Use.
- Visual bug fixes, truncation, clipping, alignment, or accessibility tree issues in the running app's window.
- Execution of the continuous validation cycle: `capture -> inspect -> log finding -> apply minimal fix -> build/test -> revalidate`.

## Loop Process

1. **Visual & Accessibility Capture**:
   - Run the target macOS application.
   - Take screenshots and query the application's accessibility tree (AX tree) using Computer Use tools to verify elements are correctly laid out and labeled.
   
2. **Layout & Design Audit**:
   - Inspect the interface for layout loops, truncated labels (e.g., `Button Lab...`), overlapping controls, or controls lacking descriptive accessibility info.
   
3. **Log Findings**:
   - Record findings in the designated findings file (e.g., `docs/test-plans/computer-use-loop/findings.md`).
   - Use the standard format:
     - `CU-SWIFTUI-XXX - Title`
     - Status: `open` or `fixed`
     - Severity: `low` / `medium` / `high`
     - Evidence, Steps to reproduce, Observed, Expected, Likely file, Rules violated, Fix details, and Verification commands.

4. **Apply Fix**:
   - Perform surgical, minimal changes to SwiftUI Views, ViewModels, or Stores.
   - Preserve responsive layouts. Add fallbacks (e.g., symbol with help text if space is tight) or capabilities checks instead of breaking API contracts.

5. **Technical Verification**:
   - Compile the project using build commands (e.g., `swift build`).
   - Run UI compile canaries or tests (e.g., `swift test --filter ViewCompileCanaryTests`).

6. **Revalidate Visual State**:
   - Launch the updated app and recapture its UI to verify the fix works, updating the status of the logged finding to `fixed`.

## Guardrails
- **Explicit Confirmation**: Never perform destructive actions or workflow state changes (e.g., clicking `Delete`, `Remove`, `Run`, `Commit`, `Push`, or `PR`) without explicit confirmation from the user.
- **Contract Integrity**: Do not change RPC contracts, databases, or core logic to solve purely visual presentation issues. Implement UI-level state checks or store guards.
