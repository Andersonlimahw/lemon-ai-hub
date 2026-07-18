---
name: maestri-routines
description: Manage scheduled routines on the Maestri canvas (recurring commands and reminders). Use to schedule a command or recurring prompt for an agent, automate a timed task, set a reminder, or list/edit/remove routines.
user-invocable: true
---

# Maestri Routines

Routines are scheduled commands that fire into a terminal on the canvas on a cron-like schedule — or fire as a desktop reminder with no terminal target. Use the `maestri routine` commands to create, inspect, modify, and remove them.

These commands require **Maestro Mode** on your terminal. If a command returns "This terminal is not the Maestro", the user must toggle Maestro on your terminal in the canvas to unlock them.

You can only see and manage routines in the current workspace.

## Scope & safety

- **`delete` is destructive.** Only delete a routine when the user explicitly asks. Never delete one on your own initiative, even to tidy up.
- Always run `maestri routine list` first to get exact names and short ids.

## Commands

### `maestri routine list`
Lists every routine in your workspace with its short id, schedule, target, status, and next fire time.

### `maestri routine show "Name"`
Full detail for one routine, including the command and any pre-run script.

### `maestri routine create "Name" --command "..." <schedule> [options]`
Schedules a new routine. A name, a `--command`, and exactly one schedule are required. The command can be a shell command or a prompt to an AI agent.

**Schedule (pick exactly one):**
- `--every 30m` — interval. Accepts `45s`, `30m`, `2h`, `1h30m` (a bare number means minutes).
- `--daily 09:00` — every day at a 24-hour time.
- `--weekly mon,wed,fri@09:00` — chosen weekdays at a time. Days: mon, tue, wed, thu, fri, sat, sun.
- `--once "2026-06-20 15:00"` — a single time (`yyyy-MM-dd HH:mm`).

**Target (optional):**
- *(omit)* — fires the command into **your own terminal**. This is the default: a recurring task for yourself.
- `--terminal "Name"` — fires into another terminal in your workspace. Run `maestri list` to see names.
- `--reminder` — no terminal target; fires a desktop notification with the command text instead.

**Options:**
- `--count N` — stop after N fires. `--until "2026-07-01"` — stop on a date. (Default: repeat forever.)
- `--pre-run "shell script"` — runs before each fire (must exit 0, or the fire is skipped). To feed its stdout into the command, put the literal placeholder `{{output}}` in your `--command` where the output should go — that token is replaced with the script's stdout at fire time. **Without `{{output}}` in the command, the script still runs but its output is not inserted.** Available env vars: `$MAESTRI_WORKSPACE_NAME`, `$MAESTRI_WORKSPACE_DIR`, `$MAESTRI_ROUTINE_NAME`, `$MAESTRI_TERMINAL_NAME`.

```
maestri routine create "Daily digest" --command "Summarize today's commits:\n\n{{output}}" --daily 18:00 --pre-run "git log --since=midnight --oneline"
```
- `--no-skip-if-busy` — fire even if the target terminal is mid-task (by default a fire is skipped while the terminal is busy).
- `--no-notify` — don't post a notification when it fires.
- `--disabled` — create it paused.

```
maestri routine create "Nightly audit" --command "Run npm audit and summarize new CVEs" --daily 02:00 --terminal "Backend"
maestri routine create "Hourly self-check" --command "Re-read the plan and report progress" --every 1h
maestri routine create "Standup" --command "Time for standup" --weekly mon,tue,wed,thu,fri@09:00 --reminder
```

### `maestri routine edit "Name" [--name "New"] [--command ...] [schedule] [options]`
Changes only the fields you pass. Use `--name` to rename. Changing the schedule resets the routine's fire counters.

### `maestri routine enable "Name"` / `maestri routine disable "Name"`
Resumes or pauses a routine without otherwise editing it.

### `maestri routine run "Name"`
Fires a routine once, right now, regardless of its schedule — useful to test it. If the target terminal isn't running, the fire is skipped.

### `maestri routine delete "Name"`
Removes a routine from the canvas. **Destructive — only on an explicit user request.**

## Disambiguating duplicates

If two routines share a name, the commands return a list of matches with short ids. Re-run with `--id <prefix>` to pick one:

```
maestri routine edit "Audit" --id a1b2c3 --daily 03:00
```