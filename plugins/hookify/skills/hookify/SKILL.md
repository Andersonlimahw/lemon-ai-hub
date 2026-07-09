---
name: hookify
description: Easily create custom hooks to prevent unwanted behaviors by analyzing conversation patterns or from explicit instructions. Use when the user asks to create a hook, warn about a command, or block a specific behavior.
---

# Hookify

Easily create custom hooks to prevent unwanted behaviors by analyzing conversation patterns or from explicit instructions.

## Overview

The hookify skill makes it simple to create hooks without editing complex JSON files. Instead, you create lightweight markdown configuration files that define patterns to watch for and messages to show when those patterns match.

**Key features:**
- 🎯 Analyze conversations to find unwanted behaviors automatically
- 📝 Simple markdown configuration files with YAML frontmatter
- 🔍 Regex pattern matching for powerful rules
- 🚀 No coding required - just describe the behavior
- 🔄 Easy enable/disable without restarting

## How to use

When the user asks to hook or warn about something (e.g., "Warn me when I use rm -rf commands" or "Don't use console.log in TypeScript files"):

1. Create a markdown rule file in the appropriate rules directory (e.g., `.claude/hookify.[name].local.md` or `.gemini/rules/hookify.[name].md`).

### Rule Configuration Format

#### Simple Rule (Single Pattern)

Create a file like `.claude/hookify.dangerous-rm.local.md`:
```markdown
---
name: block-dangerous-rm
enabled: true
event: bash
pattern: rm\s+-rf
action: block
---

⚠️ **Dangerous rm command detected!**

This command could delete important files. Please:
- Verify the path is correct
- Consider using a safer approach
- Make sure you have backups
```

**Action field:**
- `warn`: Shows warning but allows operation (default)
- `block`: Prevents operation from executing

#### Advanced Rule (Multiple Conditions)

```markdown
---
name: warn-sensitive-files
enabled: true
event: file
action: warn
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.env$|credentials|secrets
  - field: new_text
    operator: contains
    pattern: KEY
---

🔐 **Sensitive file edit detected!**

Ensure credentials are not hardcoded and file is in .gitignore.
```

## Event Types

- **`bash`**: Triggers on Bash tool commands
- **`file`**: Triggers on Edit, Write, MultiEdit tools
- **`stop`**: Triggers when the agent wants to stop
- **`prompt`**: Triggers on user prompt submission
- **`all`**: Triggers on all events
