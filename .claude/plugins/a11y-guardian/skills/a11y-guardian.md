---
name: a11y-guardian
description: Continuous accessibility monitoring. Runs WCAG 2.1 audit on every PR, blocks merge on CRITICAL violations, and posts inline PR comments with fixes. Use when setting up CI accessibility gates or reviewing PR for a11y regressions.
---

# A11y Guardian

CI/CD accessibility gate. Block regressions. Fix inline.

## Commands

```
/a11y-guardian setup       — configure CI hook (GitHub Actions / pre-commit)
/a11y-guardian pr          — audit current git diff for a11y regressions
/a11y-guardian baseline    — snapshot current a11y score as baseline
/a11y-guardian compare     — compare current score vs baseline
```

## CI Configuration

```yaml
# .github/workflows/a11y.yml
name: Accessibility Audit
on: [pull_request]
jobs:
  a11y:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npx axe-cli http://localhost:3000 --exit
```

## Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit
changed_tsx=$(git diff --cached --name-only | grep '\.tsx\?$')
if [ -n "$changed_tsx" ]; then
  echo "Running a11y check on changed components..."
  npx eslint $changed_tsx --plugin jsx-a11y --rule 'jsx-a11y/alt-text: error'
fi
```

## Integration with a11y-audit skill

This plugin provides CI/CD infrastructure.
Use `/a11y-audit` for deep interactive audits.
Use `/a11y-guardian setup` to enforce audit in CI.
