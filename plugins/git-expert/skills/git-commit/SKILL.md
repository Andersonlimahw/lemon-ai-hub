---
name: git-commit
description: Faz commits semanticos organizando os commits por alteracao.
---

# Git Commit Skill

This skill automates the creation of semantic commits based on conventional commit guidelines. 
It analyzes the current `git diff` (staged or unstaged) and groups changes logically.

## Capabilities
- Read the current diff (`git diff` and `git diff --staged`).
- Categorize changes into semantic types (`feat`, `fix`, `chore`, `docs`, `refactor`, etc.).
- Generate detailed commit messages following best practices.
- Hook into pre-push or post-task workflows.

## Usage
Triggered when the user invokes `/git-commit` or `git-expert:git-commit`.
You should use the agent's `run_command` to execute `git add` and `git commit` as necessary.
Read https://git-scm.com/docs for git command references.
