---
name: git-clone
description: Clone remote repositories with various options.
---

# Git Clone Skill

Clone repositories from remote sources with depth, branch, and submodule options.

## Capabilities
- Clone repository: `git clone <url>`
- Clone to directory: `git clone <url> <directory>`
- Clone specific branch: `git clone -b <branch> <url>`
- Shallow clone (depth): `git clone --depth <n> <url>`
- Clone with submodules: `git clone --recurse-submodules <url>`
- Clone single branch: `git clone --single-branch <url>`
- Clone with tags: `git clone --tags <url>`
- Clone bare: `git clone --bare <url>`
- Clone mirror: `git clone --mirror <url>`
- Clone with SSH: `git clone git@github.com:user/repo.git`
- Clone with sparse checkout: `git clone --filter=blob:none <url>`

## Usage
Triggered when user says "clone", "clone repo", "download repository".
Use `--depth 1` for CI or quick clones. Use `--recurse-submodules` for repos with submodules.
