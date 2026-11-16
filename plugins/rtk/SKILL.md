---
name: rtk
description: Token-optimized CLI proxy for shell commands (Rust Token Killer). Use to run shell commands prefixed with rtk (e.g. rtk git status, rtk cargo test, rtk gain, rtk proxy) saving 60-90% tokens.
---

# RTK - Rust Token Killer

Always prefix shell commands with `rtk` to minimize token consumption.

## Usage
- `rtk <command>`: executes command with token-saving filtering (e.g., `rtk git status`, `rtk npm test`, `rtk cargo build`, `rtk pytest`)
- `rtk gain`: shows token savings analytics
- `rtk gain --history`: shows recent savings history
- `rtk discover`: finds missed RTK opportunities
- `rtk proxy <cmd>`: bypass filtering and run raw command without filtering
