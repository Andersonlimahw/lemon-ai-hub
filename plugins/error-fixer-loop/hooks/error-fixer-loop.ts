// error-fixer-loop.ts — OpenCode plugin
// Detects build/test/typecheck errors in bash tool output and appends a
// reminder to run the error-fixer-loop skill.
//
// Install (OpenCode):
//   Symlink or copy this file to ~/.config/opencode/plugins/error-fixer-loop.ts
//   OpenCode auto-discovers plugins in that directory.
//
// Behavior:
//   - Listens on `tool.execute.after` for the `bash` tool.
//   - Scans the output against ERROR_PATTERNS.
//   - On match, appends a one-line reminder to the tool result so the agent
//     sees it in-context (more reliable than a toast or a /tmp marker).
//   - Never blocks, never throws, never mutates the exit code.
//
// Source of truth: lemon-ai-hub/plugins/error-fixer-loop/hooks/error-fixer-loop.ts
// Skill:           lemon-ai-hub/plugins/error-fixer-loop/SKILL.md
// Legacy:          ~/.claude/hooks/error-fix-loop-hook.sh (superseded)

import type { Plugin } from "@opencode-ai/plugin"

// Keep in sync with hooks/error-fixer-loop-hook.sh
const ERROR_PATTERNS: RegExp[] = [
  /\berror TS[0-9]+\b/i, // TypeScript
  /Unable to find a specification for/i, // CocoaPods / SPM
  /npm ERR!/,
  /BUILD FAILED/,
  /BUILD FAILURE/,
  /GRADLE.*FAILED/i,
  /pod install.*fail/i,
  /Cannot find module /,
  /Module not found:/,
  /Test Suites:.*[1-9][0-9]* failed/,
  /Tests:.*[1-9][0-9]* failed/,
  /NitroModules.*not found/i,
  /jest.*FAIL /,
  /ModuleNotFoundError/,
  /ImportError/,
  /AssertionError/,
  /FAILED tests\//,
  /cannot find package/,
  /^FAIL\s+\S+/m,
  /undefined:\s*\w+/, // Go
  /error\[E[0-9]+\]/, // Rust
  /panicked at/, // Rust
  /Compilation failure/,
  /> Task .* FAILED/, // Gradle
]

const REMINDER =
  "\n\n[EFL] Build/test error detected. Run error-fixer-loop: capture → root-cause → classify → minimal fix → test → lint/typecheck → persist rule (docs/rules or AGENTS.md) → audit with evidence."

function detectError(output: string): boolean {
  if (!output) return false
  const sample = output.slice(0, 8192)
  return ERROR_PATTERNS.some((p) => p.test(sample))
}

function extractOutput(raw: unknown): string {
  if (typeof raw === "string") return raw
  if (!raw || typeof raw !== "object") return ""
  const o = raw as Record<string, unknown>
  const candidates = [
    o.output,
    o.stdout,
    (o.metadata as Record<string, unknown> | undefined)?.output,
    (o.result as Record<string, unknown> | undefined)?.output,
  ]
  for (const c of candidates) {
    if (typeof c === "string" && c.length > 0) return c
  }
  return ""
}

export const ErrorFixerLoopPlugin: Plugin = async () => {
  return {
    "tool.execute.after": async (
      input: { tool?: string },
      output: { output?: string; stdout?: string; metadata?: { output?: string } },
    ) => {
      // Only inspect shell-like tools.
      const tool = (input?.tool ?? "").toLowerCase()
      if (tool !== "bash" && tool !== "shell" && tool !== "sh") return

      const text = extractOutput(output)
      if (!detectError(text)) return

      // Best-effort in-context reminder. Different providers expose the tool
      // result in different shapes; we try the common ones and give up quietly.
      try {
        if (typeof output.output === "string") output.output += REMINDER
        else if (typeof output.stdout === "string") output.stdout += REMINDER
        else if (output.metadata && typeof output.metadata.output === "string") {
          output.metadata.output += REMINDER
        }
      } catch {
        // Never break the tool flow.
      }
    },
  }
}

export default ErrorFixerLoopPlugin
