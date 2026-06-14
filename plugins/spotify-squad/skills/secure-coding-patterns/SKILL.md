---
name: secure-coding-patterns
description: >
  Secure coding patterns and DevSecOps best practices. Use for threat modeling, secret management, secure authentication, OWASP Top 10 prevention, and security compliance.
---

# Secure Coding Patterns & DevSecOps

## 1. Authentication & Authorization
- **MFA / 2FA**: Always support multi-factor authentication.
- **Tokens**: Use short-lived JWTs and secure HttpOnly, SameSite cookies for session management.
- **RBAC / ABAC**: Implement Role-Based or Attribute-Based Access Control enforcing the Principle of Least Privilege.

## 2. Input Validation & Sanitization
- **Trust No Input**: Validate all input on the server-side against a strict schema (e.g., Zod, Joi).
- **Sanitization**: Encode output to prevent XSS (Cross-Site Scripting).
- **SQL Injection Prevention**: Always use parameterized queries or ORMs. Never concatenate strings to build SQL queries.

## 3. Data Protection
- **Encryption at Rest**: Encrypt sensitive data in the database (e.g., AES-256).
- **Encryption in Transit**: Enforce TLS 1.2+ for all communications.
- **Hashing**: Use strong, salted hashing algorithms (Argon2, bcrypt) for passwords.

## 4. Secret Management
- Never hardcode secrets in source code.
- Use environment variables or dedicated secret vaults (HashiCorp Vault, AWS Secrets Manager).
- Scan repositories for leaked secrets (e.g., GitGuardian, detect-secrets).

## 5. DevSecOps & CI/CD Integration
- **SAST** (Static Application Security Testing): Analyze source code for vulnerabilities during the build.
- **DAST** (Dynamic Application Security Testing): Test the running application for vulnerabilities.
- **SCA** (Software Composition Analysis): Scan open-source dependencies for known CVEs.

## 6. Threat Modeling
- Use frameworks like STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) during the design phase.
