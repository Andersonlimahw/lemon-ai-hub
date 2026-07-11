---
name: git-expert
description: Expert git plugin containing multiple skills for advanced version control, semantic commits, and bisect automation.
---

# Git Expert Plugin

This plugin provides a suite of advanced Git skills for autonomous agents to use when managing version control.
It follows the multi-skill architecture.

## Available Skills

- **git-bisect-ai**: AI-guided git bisect for finding the exact commit that introduced a bug or regression. Automates the binary search, interprets test results, and identifies the responsible code change with full context.
- **git-commit**: Generates high-quality semantic commits based on the diff. Organizes commits by task and ensures they follow conventional commit standards. Can be integrated with hooks.

## Usage

Use the specific skills when you need advanced git operations.
Example: `/git-commit <prompt>` to trigger semantic commit generation.
