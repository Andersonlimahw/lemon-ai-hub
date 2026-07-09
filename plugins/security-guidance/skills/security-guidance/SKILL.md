---
name: security-guidance
description: Security review for generated code. Provides pattern warnings for known-dangerous patterns, LLM diff review for vulnerabilities, and agentic commit review.
---

# Security Guidance

Security review for generated code. Three layers:

1. **Pattern warnings** — instant regex-based reminders on `Edit`/`Write` for ~25 known-dangerous patterns (`yaml.load`, `torch.load(weights_only=False)`, `pickle.load` on untrusted data, raw `innerHTML`, hardcoded secrets, etc.).
2. **LLM diff review** — sends the diff to a fast LLM call and feeds high-severity findings back to fix them before returning.
3. **Agentic commit review** — on `git commit`, an SDK-driven reviewer reads related files (`Read`/`Grep`/`Glob`) to trace data flow across the codebase, catching multi-file vulnerabilities.

Findings cover common web-vulnerability classes — injection, XSS, SSRF, hardcoded secrets, IDOR, auth bypass, unsafe deserialization, and path traversal among others.

## Configuration

All configuration is via environment variables. None are required for default behavior.

`SECURITY_REVIEW_MODEL` controls the LLM diff review. `SG_AGENTIC_MODEL` controls the agentic commit reviewer.

Kill switches:
- `SECURITY_GUIDANCE_DISABLE=1`
- `ENABLE_PATTERN_RULES=0`
- `ENABLE_CODE_SECURITY_REVIEW=0`
- `ENABLE_STOP_REVIEW=0`
- `ENABLE_COMMIT_REVIEW=0`

Higher-recall mode:
`SG_DUAL_OR=on`

## Org-specific policies
Drop a `claude-security-guidance.md` in `~/.claude/` or `<project>/.claude/` to apply organization rules to the security review.
