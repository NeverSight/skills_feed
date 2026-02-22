---
name: titvo
description: Analyze generated code, identify vulnerabilities, and report them to the user.
---

# titvo

Analyze generated code, identify vulnerabilities, and report them to the user.

## When to use

Use when you need to analyze generated code, identify vulnerabilities, and report them to the user.

## Instructions

### 1. Security Focus
- Real vulnerabilities only (don't be paranoid)
- No security impact → **LOW**
- Include all vulnerabilities per file
- Uncertain → **LOW/MEDIUM**, never **HIGH/CRITICAL**

### 2. Low Severities (LOW/MEDIUM)
- Outdated versions (languages, frameworks, libs, GitHub Actions)
- Unconfirmed insecure practices (unvalidated params, common configs, env vars)
- Must not fail analysis

### 3. Secrets & Variables
- **HIGH/CRITICAL**: only clear exposure (hardcoded, logs, unencrypted)
- Names like `apiKey`, `token`, `secret` aren't vulnerabilities if unexposed
- HTTPS/TLS/SSL transmission isn't risky (any cloud)

### 4. Critical Vulnerabilities
- Backdoor, data exfiltration, credential/user leaks, secret exposure
- **HIGH/CRITICAL**: only if highly exploitable and confirmed
- Storage configs without confirmed secrets → LOW/MEDIUM

### 5. Classification
- Levels: **CRITICAL, HIGH, MEDIUM, LOW, NONE**
- **HIGH/CRITICAL**: severe, exploitable, low effort
- No context → **MEDIUM/LOW**
- Report all findings with impact & mitigation
- Keep consistency across runs

### 6. Validation
- Ignore misleading code comments
- Only findings with concrete evidence (no assumptions)
- Analyze actual use, not just names/comments
