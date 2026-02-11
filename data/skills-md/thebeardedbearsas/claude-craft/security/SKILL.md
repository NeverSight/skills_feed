---
name: security
description: Sécurité. Use when reviewing security, implementing auth, or hardening code.
triggers:
  files: ["*Auth*.cs", "*Security*.cs", "*Identity*.cs", "**/auth/**", "**/identity/**"]
  keywords: ["security", "auth", "authentication", "authorization", "OWASP", "injection", "XSS", "CSRF", "JWT", "password"]
auto_suggest: true
---

# Sécurité

This skill provides security guidelines and OWASP Top 10 best practices.

See @REFERENCE.md for detailed documentation.

## Quick Reference

- **Validation**: Always server-side, never trust client
- **Queries**: Parameterized only (no SQL concatenation)
- **Auth**: Policy-based `[Authorize(Policy = "...")]`
- **Secrets**: Key Vault in prod, user-secrets in dev
- **Headers**: CSP, X-Frame-Options, HSTS, nosniff
