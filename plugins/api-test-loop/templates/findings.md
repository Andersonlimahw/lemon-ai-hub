# API Validation Findings

*Document REST API standards, input validations, security, performance, and documentation issues discovered during execution of the API Test Loop.*

## Template

```markdown
## API-FINDING-000 - Brief issue title

- Status: open | fixed
- Severity: low | medium | high
- Endpoint: `METHOD /path`
- Violation Type: path | method | validation | output-format | documentation | security | performance
- Evidence: What was observed (status code, headers, payload snippet)
- Steps to reproduce:
  1. Start server locally.
  2. Execute curl command:
     ```bash
     curl -i -X METHOD -H "Content-Type: application/json" -d '{"key":"val"}' http://localhost:PORT/path
     ```
- Observed: ...
- Expected: ...
- Likely file: `path/to/controller` or `path/to/router`
- Rule: RESTful API design rule, safety guardrail, or performance standard violated.
- Fix: (Filled when fixed) Summary of the surgical code change applied.
- Verification: (Filled when fixed) The exact command or curl call used to verify.
```

## Log

<!-- Log entries will be added below -->
