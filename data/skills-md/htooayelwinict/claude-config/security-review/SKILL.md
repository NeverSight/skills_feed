---
name: security-review
description: |
  Audit code for security vulnerabilities using OWASP Top 10 guidelines. Use for security audits, pre-deployment
  checks, authentication reviews, or when checking for XSS, SQL injection, CSRF, or authorization issues. EXCLUSIVE to security-expert agent.
allowed-tools: Read, Grep, Glob, Bash, mcp_gemini-bridge, mcp_open-bridge, mcp_codex-bridge, mcp_context7, mcp_web-search-prime
---
# Security Review

**Exclusive to:** `security-expert` agent

## MCP Helpers (Brain + Memory + Web)

### 🧠 Gemini-Bridge — Security Analysis
```
mcp_gemini-bridge_consult_gemini(query="Security audit this code for OWASP vulnerabilities: [code snippet]", directory=".")
```

### 🌉 Open-Bridge — Alternative Security Analysis
```
mcp_open-bridge_consult_gemini(query="Security audit this code for OWASP vulnerabilities: [code snippet]", directory=".")
```

### 💻 Codex-Bridge — Code Security Review
```
mcp_codex-bridge_consult_codex(query="Find security vulnerabilities in: [code]", directory=".")
```

### 📚 Context7 (Memory) — Up-to-Date Docs

Lookup security patterns and vulnerability mitigations:
```
mcp_context7_resolve-library-id(libraryName="laravel", query="csrf protection")
mcp_context7_query-docs(libraryId="/laravel/docs", query="authentication security")
```

### 🌐 Web Search — CVE and Vulnerability Lookup
```
mcp_web-search-prime_search(query="[package name] CVE vulnerability 2025")
```

## Validation Loop (MANDATORY)

Every security review MUST run these dependency checks:
```bash
composer audit            # Check PHP vulnerabilities
npm audit                 # Check JS vulnerabilities
php artisan route:list --compact  # Verify route middleware
```

Report any vulnerabilities found as Critical findings.

## Instructions

1. Run `git diff` to identify changed files
2. Scan for security vulnerabilities using checklist below
3. Check authentication and authorization patterns
4. Review input validation and sanitization
5. Report findings by severity (Critical → Warning → Suggestion)

## OWASP Top 10 Checklist

| # | Vulnerability | Laravel Check | React Check |
|---|---------------|---------------|-------------|
| A01 | Broken Access Control | Policies, Gates | Route guards |
| A02 | Cryptographic Failures | `Hash::make`, `encrypt` | No secrets in client |
| A03 | Injection | Eloquent, query builder | No `dangerouslySetInnerHTML` |
| A04 | Insecure Design | Business logic review | Component security |
| A05 | Security Misconfiguration | `.env` settings | Build config |
| A06 | Vulnerable Components | `composer audit` | `npm audit` |
| A07 | Auth Failures | Rate limiting, sessions | Token handling |
| A08 | Data Integrity | CSRF, mass assignment | Form validation |
| A09 | Logging Failures | Security event logs | Error boundaries |
| A10 | SSRF | URL validation | API call validation |

## Laravel Security Checks

```php
// Mass Assignment
$fillable = ['name', 'email'];  // ✅ Whitelist
$guarded = ['id', 'is_admin'];  // ✅ Blacklist

// SQL Injection Prevention
User::where('email', $email)->first();  // ✅ Safe
DB::raw("SELECT * FROM users WHERE email = '$email'");  // ❌ Dangerous

// CSRF
@csrf  // ✅ In forms
```

## React Security Checks

```tsx
// XSS Prevention
<div>{userInput}</div>  // ✅ Auto-escaped
<div dangerouslySetInnerHTML={{__html: userInput}} />  // ❌ XSS risk

// No secrets in client
const API_KEY = process.env.NEXT_PUBLIC_API_KEY;  // ⚠️ Visible to users
```

## Audit Commands

```bash
composer audit          # PHP vulnerabilities
npm audit               # JS vulnerabilities
php artisan route:list  # Check route middleware
```

## Examples
- "Security review this PR"
- "Check for OWASP vulnerabilities"
- "Audit authentication flow"
