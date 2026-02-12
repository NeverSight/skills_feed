---
name: review-security
description: "Review code for security: injection, sensitive data, authentication and authorization, dependencies and CVEs, configuration and secrets, and crypto. Cognitive-only atomic skill; output is a findings list."
tags: [eng-standards, security]
related_skills: [review-diff, review-codebase, review-sql, review-code]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
---

# Skill: Review Security

## Purpose

Review code for **security** concerns only. Do not define scope (diff vs codebase) or perform language/framework/architecture analysis; those are separate atomic skills. Emit a **findings list** in the standard format for aggregation. Focus on injection (SQL, command, template), sensitive data and logging, authentication and authorization, dependencies and CVEs, configuration and secrets, and cryptography and hashing.

---

## Use Cases

- **Orchestrated review**: Used as a cognitive step when [review-code](../review-code/SKILL.md) runs scope → language → framework → library → cognitive.
- **Security-focused review**: When the user wants only security dimensions checked (e.g. before release or audit).
- **Compliance or audit**: As a repeatable security checklist output for documentation.

**When to use**: When the task includes security review. Scope and code scope are determined by the caller or user.

---

## Behavior

### Scope of this skill

- **Analyze**: Security dimensions in the **given code scope** (files or diff provided by the caller). Do not decide scope; accept the code range as input.
- **Do not**: Perform scope selection, language/framework conventions, or architecture review. Focus only on security.

### Review checklist (security dimension only)

1. **Injection**: SQL injection (parameterization, raw queries); command injection (shell, exec); template injection (user-controlled templates); path traversal; LDAP/XML injection where relevant.
2. **Sensitive data and logging**: Secrets, tokens, or PII in logs or error messages; sensitive data in URLs or client-side storage; exposure in responses or caches.
3. **Authentication and authorization**: Missing or weak authentication; broken access control (IDOR, privilege escalation); session handling and CSRF; permission checks on every sensitive operation.
4. **Dependencies and CVEs**: Known vulnerable dependencies (versions, advisories); unpinned or overly broad version ranges; supply-chain and integrity.
5. **Configuration and secrets**: Hardcoded secrets; secrets in config files or environment; secure default configuration; feature flags and debug mode in production.
6. **Cryptography and hashing**: Weak or deprecated algorithms (e.g. MD5, SHA1 for security); inappropriate use of encryption; key management and storage; password hashing (e.g. bcrypt, Argon2).

### Tone and references

- **Professional and technical**: Reference specific locations (file:line). Emit findings with Location, Category, Severity, Title, Description, Suggestion. Use severity critical for clear vulnerabilities.

---

## Input & Output

### Input

- **Code scope**: Files or directories (or diff) already selected by the user or scope skill. This skill does not decide scope; it reviews the provided code for security only.

### Output

- Emit zero or more **findings** in the format defined in **Appendix: Output contract**.
- Category for this skill is **cognitive-security**.

---

## Restrictions

- **Do not** perform scope selection, language, framework, or architecture review. Stay within security dimensions.
- **Do not** give conclusions without specific locations or actionable suggestions.
- **Do not** assume deployment or network topology unless stated; focus on code and configuration in scope.

---

## Self-Check

- [ ] Was only the security dimension reviewed (no scope/language/architecture)?
- [ ] Are injection, sensitive data, authz, dependencies, config/secrets, and crypto covered where relevant?
- [ ] Is each finding emitted with Location, Category=cognitive-security, Severity, Title, Description, and optional Suggestion?
- [ ] Are critical issues clearly marked and actionable?

---

## Examples

### Example 1: Hardcoded secret

- **Input**: API key or password in source code.
- **Expected**: Emit a critical finding; suggest environment variable or secret manager; reference the line. Category = cognitive-security.

### Example 2: SQL built from user input

- **Input**: Query string built with concatenation of user-controlled input.
- **Expected**: Emit a critical finding for SQL injection; suggest parameterized queries. Category = cognitive-security.

### Edge case: False positive

- **Input**: Placeholder like "changeme" or "TODO" in config, not used in production.
- **Expected**: Emit a minor/suggestion finding to remove or replace before production; do not mark as critical if context indicates non-production. If unclear, ask user or emit as suggestion.

---

## Appendix: Output contract

Each finding MUST follow the standard findings format:

| Element | Requirement |
| :--- | :--- |
| **Location** | `path/to/file.ext` (optional line or range). |
| **Category** | `cognitive-security`. |
| **Severity** | `critical` \| `major` \| `minor` \| `suggestion`. |
| **Title** | Short one-line summary. |
| **Description** | 1–3 sentences. |
| **Suggestion** | Concrete fix or improvement (optional). |

Example:

```markdown
- **Location**: `config/app.yml:7`
- **Category**: cognitive-security
- **Severity**: critical
- **Title**: API key hardcoded in configuration
- **Description**: Secret is committed to repo and may be exposed in logs or backups.
- **Suggestion**: Move to environment variable or secret manager; add to .gitignore if local override.
```
