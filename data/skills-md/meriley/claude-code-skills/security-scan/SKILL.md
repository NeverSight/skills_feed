---
name: security-scan
description: ⚠️ MANDATORY - Automatically invoked by safe-commit. Performs comprehensive security scanning before commits. Checks for secrets (API keys, passwords, tokens), dependency vulnerabilities, code injection risks, and authentication issues. MUST pass before any commit. NEVER run security scans manually.
version: 1.0.1
---

# Security Scan Skill

## ⚠️ MANDATORY SKILL - AUTO-INVOKED BY SAFE-COMMIT

## Purpose

Comprehensive security verification to ensure no secrets, vulnerabilities, or security issues are committed to the repository.

**CRITICAL:** This skill is automatically invoked by safe-commit. NEVER run security scans manually.

## 🚫 NEVER DO THIS

- ❌ Running `grep` for secrets manually before commit
- ❌ Running `npm audit` or `go mod audit` manually before commit
- ❌ Checking for security issues outside of this skill during commit workflow

**Let safe-commit invoke this skill automatically. Manual security scanning before commit is REDUNDANT and FORBIDDEN.**

---

## ⚠️ SKILL GUARD - READ BEFORE RUNNING SECURITY SCANS MANUALLY

**Before using Bash/Grep tools for security checks, answer these questions:**

### ❓ Are you about to run `grep` to search for secrets/API keys?

→ **STOP.** Are you doing this before commit? If YES, use safe-commit instead (it invokes this skill).

### ❓ Are you about to run `npm audit` or `go mod audit`?

→ **STOP.** Are you doing this before commit? If YES, use safe-commit instead (it invokes this skill).

### ❓ Are you checking for secrets, passwords, or tokens in code?

→ **STOP.** Are you doing this before commit? If YES, use safe-commit instead (it invokes this skill).

### ❓ Are you scanning for dependency vulnerabilities?

→ **STOP.** Are you doing this before commit? If YES, use safe-commit instead (it invokes this skill).

### ❓ Are you verifying security before committing?

→ **STOP.** Invoke safe-commit skill (it will invoke this skill automatically).

**IF YOU RUN SECURITY SCANS MANUALLY BEFORE COMMIT, YOU ARE CREATING REDUNDANCY AND WASTING TIME.**

When to run security scans manually:

- ✅ When adding new dependencies (outside commit flow)
- ✅ After modifying auth/security code (during development)
- ✅ When user explicitly requests security review

When NOT to run security scans manually:

- ❌ Before commit (use safe-commit instead)
- ❌ As part of commit workflow (use safe-commit instead)

**Safe-commit invokes this skill automatically. Don't duplicate the work.**

---

## Security Checklist

### 1. Secrets Scanning

**Step 1.1: Scan for Common Secret Patterns**

```bash
grep -r -E "(api_key|API_KEY|apikey|APIKEY)" . --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=vendor
```

**Step 1.2: Scan for Passwords and Tokens**

```bash
grep -r -E "(password|PASSWORD|secret|SECRET|token|TOKEN|bearer|BEARER)" . --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=vendor
```

**Step 1.3: Scan for Private Keys**

```bash
grep -r -E "(private_key|PRIVATE_KEY|-----BEGIN.*PRIVATE KEY-----)" . --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=vendor
```

**Step 1.4: Scan for Database Credentials**

```bash
grep -r -E "(db_password|DB_PASSWORD|database_url|DATABASE_URL|connection_string)" . --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=vendor
```

**Step 1.5: Check Common Secret Files**
Check if these files exist and are in .gitignore:

- `.env`
- `.env.local`
- `.env.production`
- `credentials.json`
- `secrets.yaml`
- `config/secrets.yml`
- `*.pem`
- `*.key`

**Action on Match:**

- **HALT** if secrets found in files to be committed
- Verify matches are false positives (test fixtures, documentation)
- If real secrets: MUST remove before proceeding
- Update .gitignore to prevent future commits
- Suggest using environment variables or secret management tools

### 2. Dependency Vulnerability Scanning

**Step 2.1: Detect Project Type**
Identify language/framework by checking for:

- `package.json` → Node.js/npm
- `go.mod` → Go
- `requirements.txt` or `Pipfile` → Python
- `Cargo.toml` → Rust
- `pom.xml` or `build.gradle` → Java

**Step 2.2: Run Language-Specific Audit**

For **Node.js**:

```bash
npm audit --audit-level=moderate
```

For **Go**:

```bash
go list -json -m all | nancy sleuth  # If nancy is installed
# OR
go list -json -m all > go.list && docker run --rm -v $(pwd):/src sonatypecommunity/nancy:latest sleuth --path /src/go.list
```

For **Python**:

```bash
pip-audit  # If pip-audit is installed
# OR
safety check  # If safety is installed
```

For **Rust**:

```bash
cargo audit
```

**Action on Vulnerabilities:**

- **HALT** on HIGH or CRITICAL vulnerabilities
- Report vulnerability details to user
- Suggest update commands
- Allow MEDIUM/LOW with user acknowledgment

### 3. Code Injection Risk Scanning

**Step 3.1: SQL Injection Patterns**

```bash
grep -r -E "(exec|execute|query|prepare).*\+|string.*concat.*query|fmt\.Sprintf.*query" . --include="*.go" --include="*.py" --include="*.js" --include="*.ts"
```

**Step 3.2: Command Injection Patterns**

```bash
grep -r -E "exec.*user|system.*user|os\.system.*\+|subprocess.*shell=True" . --include="*.py" --include="*.go" --include="*.js" --include="*.ts"
```

**Step 3.3: XSS Patterns (for web projects)**

```bash
grep -r -E "innerHTML.*\+|dangerouslySetInnerHTML|document\.write.*\+" . --include="*.js" --include="*.jsx" --include="*.ts" --include="*.tsx"
```

**Action on Match:**

- Review each match for proper input validation
- Verify parameterized queries are used (SQL)
- Check for proper escaping/sanitization
- Flag suspicious patterns to user for review

### 4. Authentication & Authorization Checks

**Step 4.1: Check for Hardcoded Credentials**

```bash
grep -r -E "(username|user).*=.*['\"].*['\"]" . --include="*.go" --include="*.py" --include="*.js" --include="*.ts" | grep -v "test" | grep -v "example"
```

**Step 4.2: Check for Weak Cryptography**

```bash
grep -r -E "(md5|MD5|sha1|SHA1|DES|ECB)" . --include="*.go" --include="*.py" --include="*.js" --include="*.ts"
```

**Step 4.3: Check for Insecure Random**

```bash
grep -r -E "(math\.random|Math\.random|rand\.Seed\(time)" . --include="*.go" --include="*.py" --include="*.js" --include="*.ts"
```

**Action on Match:**

- Verify cryptographic operations use strong algorithms
- Recommend SHA-256+ for hashing
- Recommend crypto/rand for security-sensitive random numbers
- Flag weak crypto as CRITICAL issues

### 5. Data Exposure Checks

**Step 5.1: Check for Debug/Verbose Logging**

```bash
git diff --cached | grep -E "console\.log|fmt\.Println|print\(|logger\.debug" | grep -v "//.*console\|#.*print"
```

**Step 5.2: Check for TODO Security Comments**

```bash
grep -r -E "TODO.*security|FIXME.*security|XXX.*security" . --exclude-dir=.git
```

**Action on Match:**

- Verify no sensitive data in debug statements
- Ensure debug logging disabled in production
- Flag unresolved security TODOs

## Reporting

### Success Report Format

```
✅ Security Scan PASSED

Checks Performed:
- Secrets scanning: No secrets detected
- Dependency audit: No critical vulnerabilities
- Code injection: No suspicious patterns
- Authentication: No hardcoded credentials
- Data exposure: No sensitive data in logs

Safe to proceed with commit.
```

### Failure Report Format

```
❌ Security Scan FAILED

CRITICAL Issues Found:
1. [SECRETS] API key detected in config/settings.py:42
   - Pattern: "api_key = 'sk_live_abc123'"
   - Action: Remove from code, use environment variables

2. [VULNERABILITY] lodash@4.17.19 has prototype pollution (CVE-2020-8203)
   - Severity: HIGH
   - Action: Run 'npm update lodash' to upgrade

CANNOT PROCEED until issues are resolved.

Suggestions:
- Move secrets to .env file and add to .gitignore
- Run: npm audit fix
- Review authentication code in auth/handlers.go:156
```

## Integration with Other Skills

This skill is invoked by:

- **`safe-commit`** - Before committing changes
- **`create-pr`** - Before creating pull requests

## Best Practices

1. **Never skip** - Security scanning is mandatory, not optional
2. **Be thorough** - Better to flag false positives than miss real issues
3. **Educate** - Explain WHY each issue is a problem
4. **Suggest fixes** - Provide concrete remediation steps
5. **Document exceptions** - If allowing a flagged pattern, document why

## Common False Positives

- Test fixtures containing example secrets
- Documentation with placeholder values
- Variable names containing "password" (e.g., `hasPasswordField`)
- Comment references to security concepts

**How to handle:**

- Verify context of each match
- If false positive: document and proceed
- If uncertain: flag to user for review

## Emergency Override

If user explicitly states "I have reviewed and approved these security findings", you may proceed with:

1. Document the user's explicit approval
2. List what was approved in commit message
3. Suggest creating follow-up ticket for remediation
