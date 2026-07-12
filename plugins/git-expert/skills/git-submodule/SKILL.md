---
name: git-submodule
description: Manage git submodules for nested repositories.
---

# Git Submodule Skill

Add, update, remove, and manage submodules in a repository.

## Capabilities
- Add submodule: `git submodule add <url> <path>`
- Init submodules: `git submodule init`
- Update submodules: `git submodule update`
- Init and update: `git submodule update --init`
- Recursive: `git submodule update --init --recursive`
- Clone with submodules: `git clone --recurse-submodules <url>`
- List submodules: `git submodule status`
- Show diff: `git diff --submodule`
- Deinit submodule: `git submodule deinit <path>`
- Remove submodule: `git submodule deinit <path>` && `git rm <path>`
- Update to latest: `git submodule update --remote`
- Foreach command: `git submodule foreach '<command>'`

## Usage
Triggered when user says "submodule", "add submodule", "update submodules", "clone with submodules".
After cloning a repo with submodules, always run `git submodule update --init --recursive`.
