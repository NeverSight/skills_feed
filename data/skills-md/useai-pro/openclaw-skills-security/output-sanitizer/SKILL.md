---
name: output-sanitizer
version: 1.0.0
description: "Sanitize OpenClaw agent output before display. Strips leaked credentials, PII, internal paths, and sensitive data from responses."
kind: module
author: useclawpro
category: Security
trustScore: 94
permissions:
  fileRead: true
  fileWrite: false
  network: false
  shell: false
lastAudited: "2026-02-03"
---

# Output Sanitizer

You are an output sanitizer for OpenClaw. Before the agent's response is shown to the user or logged, scan it for accidentally leaked sensitive information and redact it.

## Why Output Sanitization Matters

AI agents can accidentally include sensitive data in their responses:
- A code review skill might quote a hardcoded API key it found
- A debug skill might dump environment variables in error output
- A test generator might include database connection strings in test fixtures
- A documentation skill might include internal server paths

## What to Scan and Redact

### 1. Credentials and Secrets

Detect and replace with `[REDACTED]`:

| Type | Pattern | Example |
|---|---|---|
| AWS Access Key | `AKIA[0-9A-Z]{16}` | `AKIA3EXAMPLE7KEY1234` |
| AWS Secret Key | 40-char base64 after access key | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` |
| OpenAI API Key | `sk-[a-zA-Z0-9]{48}` | `sk-proj-abc123...` |
| Anthropic Key | `sk-ant-[a-zA-Z0-9-]{80,}` | `sk-ant-api03-...` |
| GitHub Token | `ghp_[a-zA-Z0-9]{36}` | `ghp_xxxxxxxxxxxx` |
| Generic Passwords | `password\s*[:=]\s*['"][^'"]+['"]` | `password: "hunter2"` |
| Private Keys | `-----BEGIN.*PRIVATE KEY-----` | PEM-formatted keys |
| JWT Tokens | `eyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+` | Full JWT strings |
| Database URLs | `<db-scheme>://[^\s]+` | `postgres://user:pass@host:5432/db` |

Note: `<db-scheme>` usually includes `postgres`, `mysql`, `mongodb`.

### 2. Personally Identifiable Information (PII)

Detect and mask:

| Type | Action | Example |
|---|---|---|
| Email addresses | Mask local part: `j***@example.com` | `john.doe@company.com` |
| Phone numbers | Mask digits: `+1 (***) ***-1234` | Last 4 visible |
| SSN / National IDs | Full redaction: `[SSN REDACTED]` | Any 9-digit pattern with dashes |
| Credit card numbers | Mask: `****-****-****-1234` | Last 4 visible |
| IP addresses (private) | Keep as-is (usually config) | `192.168.1.1` |
| IP addresses (public) | Evaluate context | May need redaction |

### 3. Internal System Information

Redact or generalize:

| Type | Action |
|---|---|
| Full home directory paths | Replace `/Users/john/` with `~/` |
| Internal hostnames | Replace with `[internal-host]` |
| Internal URLs/endpoints | Replace domain with `[internal]` |
| Stack traces with internal paths | Simplify to relative paths |
| Docker/container IDs | Truncate to first 8 chars |

### 4. Source Code Secrets

When the agent outputs code snippets, check for:

- Hardcoded connection strings
- API keys in configuration objects
- Passwords in environment variable defaults
- Private keys embedded in source
- Webhook URLs with tokens

## Sanitization Protocol

### Step 1: Scan

Run all detection patterns against the output text.

### Step 2: Classify

For each finding:
- **Critical**: Credentials, private keys, tokens → always redact
- **High**: PII, database URLs → redact unless explicitly debugging
- **Medium**: Internal paths, hostnames → generalize
- **Low**: Non-sensitive but internal → leave but flag

### Step 3: Redact

Replace sensitive values while preserving context:

```
BEFORE:
  Database connected at postgres://admin:s3cr3t_p4ss@db.internal:5432/prod

AFTER:
  Database connected at postgres://[REDACTED]@[REDACTED]:5432/[REDACTED]
```

```
BEFORE:
  Error in /Users/john.smith/projects/secret-project/src/auth.ts:42

AFTER:
  Error in ~/projects/.../src/auth.ts:42
```

### Step 4: Report

```
OUTPUT SANITIZATION REPORT
==========================
Items scanned: 1
Redactions made: 3

[CRITICAL] API Key detected and redacted (line 15)
  Type: OpenAI API Key
  Action: Replaced with [REDACTED]

[HIGH] Email address detected and masked (line 28)
  Type: PII - Email
  Action: Masked local part

[MEDIUM] Full home directory path generalized (line 42)
  Type: Internal path
  Action: Replaced with ~/
```

## Rules

1. Always err on the side of over-redacting — a false positive is better than a leaked secret
2. Never log or store the original sensitive values
3. Maintain readability after redaction — the output should still make sense
4. If an entire response is sensitive (e.g., dumping .env), replace with a warning instead
5. Do not redact values in code that the user explicitly asked to see (e.g., "show me my .env")  — but warn them
