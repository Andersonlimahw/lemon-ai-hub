---
name: gh-release
description: Manage GitHub releases via gh CLI.
---

# GitHub Release Skill

Create, list, view, edit, delete, and download releases and assets.

## Capabilities
- Create release: `gh release create <tag> --title "<title>" --notes "<notes>" --target <branch>`
- Create with assets: `gh release create <tag> <file1> <file2> --title "<title>"`
- Create draft: `gh release create <tag> --draft`
- Create prerelease: `gh release create <tag> --prerelease`
- Generate notes: `gh release create <tag> --generate-notes`
- Latest: `gh release create <tag> --latest`
- List releases: `gh release list --limit <n>`
- View release: `gh release view <tag> --json <fields>`
- Edit release: `gh release edit <tag> --title "<title>" --notes "<notes>" --draft --prerelease --latest`
- Delete release: `gh release delete <tag>`
- Delete tag: `gh release delete <tag> --yes && git push --delete origin <tag>`
- Download asset: `gh release download <tag> --pattern "<pattern>" --dir "<dir>"`
- Upload asset: `gh release upload <tag> <file> --clobber`
- Verify asset: `gh release verify <tag>`
- View release in browser: `gh release view <tag> --web`

## Usage
Triggered when user says "release", "create release", "publish release", "list releases".
Use `--generate-notes` for auto-generated changelog from commits since last release.
