---
name: maestri-workspace
description: Create new Maestri workspaces and floors from the command line, optionally cloning an existing workspace as a starting point. Use when the user asks to provision, spin up, or scaffold a new workspace, project environment, or isolated floor.
user-invocable: true
---

# Maestri Workspace Provisioning

Workspaces are standalone canvases, each rooted in its own project directory — isolation *between* projects. Floors are levels inside one workspace, optionally backed by a git-isolated clone of its repository — isolation *within* a project. Use these commands to provision either without leaving the terminal, e.g. to set up a ready-to-work environment for a brand-new project the user just scaffolded.

These commands require **Maestro Mode** on your terminal. If a command returns "This terminal is not the Maestro", the user must toggle Maestro on your terminal in the canvas to unlock them.

## Scope & safety

- Creation and filing are additive and reversible. There are deliberately **no delete or rename commands** — anything destructive stays in the UI, on explicit user action.
- Creation is always silent: nothing changes on the user's screen. The new workspace or floor simply appears in the sidebar, ready when the user opens it.
- The target directory must already exist — create the folder (and `git init` if wanted) before calling `workspace create`.

## Commands

### `maestri workspace create "Name" --dir PATH [--from "Source Workspace"] [--group "Group"] [--folder "Folder"]`

Creates a new workspace rooted at PATH.

- `--from "Source Workspace"` — clone an existing workspace as the starting point: its full canvas layout (terminals, notes, file trees, floors, connections) is deep-copied, and every path under the source's working directory is retargeted onto PATH. Terminals start fresh — no scrollback, nothing running — and boot when the user first opens the workspace. Paths pointing outside the source's directory are kept as-is.
- `--group "Group"` — file the workspace under a sidebar group, creating the group if it doesn't exist yet.
- `--folder "Folder"` — file the workspace inside a sidebar folder. Alone, the folder is matched anywhere in the sidebar (created at the sidebar root when missing); with `--group`, the folder lives inside that group; with `--root`, only folders at the sidebar root are matched. If a bare folder name matches more than one folder, the command asks you to add `--group` or `--root` to disambiguate.
- Without `--from`, the workspace starts with an empty canvas.

The user's "template" is just a normal workspace — suggest they keep one laid out the way they like and clone it by name:

```
maestri workspace create "Acme Churn Analysis" --dir ~/Work/acme-churn --from "Data Project Template" --group "Data Projects"
maestri workspace create "Q3 Report" --dir ~/Work/q3 --group "Data Projects" --folder "Reports"
```

### `maestri workspace move "Name" --group "Group" | --folder "Folder" | --root`

Refiles an existing workspace in the sidebar. Same destination rules as `create`: groups and folders are created when missing, `--group` + `--folder` scopes the folder to that group, `--root` + `--folder` scopes it to the sidebar root, and `--root` alone moves the workspace out of any group or folder. This only reorganizes the sidebar — the workspace itself is untouched.

```
maestri workspace move "Acme Churn Analysis" --folder "Archive 2026"
maestri workspace move "Q3 Report" --folder "Reports" --root
maestri workspace move "Scratch" --root
```

### `maestri workspace list`

Prints the sidebar hierarchy exactly as the user sees it — Pinned first, then the root workspaces and folders in order, then each group with its folders — with every workspace's directory and floor count, marking the one your terminal lives in. Empty groups and folders are listed too, so the output doubles as a map of valid filing destinations. Run it before `create` or `move` to pick a free name, the exact `--from` source, and where the workspace should live.

### `maestri floor create "Name" [--branch NAME] [--existing-branch] [--no-git] [--copy-ground]`

Adds a floor to **your own workspace**. By default the floor gets git isolation when the workspace supports it (a git repository on an APFS volume): a copy-on-write clone of the project on its own branch, so work there can't disturb the ground floor. When the workspace can't support isolation, a plain floor is created instead and the response says so.

- `--branch NAME` — branch for the isolated clone (default: a slug of the floor name). Fails if the branch already exists.
- `--existing-branch` — check out an existing branch instead of creating one.
- `--no-git` — skip isolation and share the ground directory.
- `--copy-ground` — start the floor with a copy of the ground floor's canvas layout.

```
maestri floor create "Refactor Auth" --branch refactor-auth
maestri floor create "Scratch" --no-git
```

Landing a floor's work (merging its branch back) is done by the user in the UI — there is no CLI command for it.

After creating an isolated floor you can staff it without leaving your own floor: `maestri recruit "Name" --floor "Refactor Auth" --role "..."` (from the maestri-manager skill) spawns an agent there, working inside the floor's clone, still wired to you for `ask`/`check`.

### `maestri floor list`

Lists the ground floor and every floor of your workspace with branch, clone path, and node count.