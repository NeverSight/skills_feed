---
name: security-scanner
description: Scan codebase for security vulnerabilities including secrets, insecure
  dependencies, and unsafe code patterns. Use when performing automated security scans.
allowed-tools: Read, Grep, Glob, Bash
---

# Security Scanner Skill

## Purpose

This skill provides automated security scanning of codebases to identify vulnerabilities, hardcoded secrets, insecure dependencies, and unsafe coding patterns.

## When to Use

- Starting security assessment of a codebase
- Pre-commit security checks
- CI/CD pipeline security validation
- Dependency vulnerability scanning
- Secret detection in code
- Static security analysis

## Scanning Workflow

### 1. Secret Detection

**Scan for Hardcoded Secrets:**

```bash
# Using grep patterns for common secrets
grep -r -i "password\s*=\s*['\"]" src/ --include="*.py" --include="*.js"
grep -r -i "api_key\s*=\s*['\"]" src/ --include="*.py" --include="*.js"
grep -r -i "secret\s*=\s*['\"]" src/ --include="*.py" --include="*.js"
grep -r -i "token\s*=\s*['\"]" src/ --include="*.py" --include="*.js"

# AWS credentials
grep -r "AKIA[0-9A-Z]{16}" src/
grep -r "aws_secret_access_key" src/

# Private keys
grep -r "BEGIN.*PRIVATE KEY" src/

# Database connection strings
grep -r "postgresql://.*:.*@" src/
grep -r "mysql://.*:.*@" src/
grep -r "mongodb://.*:.*@" src/
```

**Use Dedicated Secret Scanners:**

```bash
# Gitleaks (if available)
gitleaks detect --source . --report-format json --report-path gitleaks-report.json

# Trufflehog (if available)
trufflehog filesystem . --json > trufflehog-report.json

# Git-secrets (if available)
git secrets --scan
```

**Secrets to Look For:**
- API keys (AWS, Google Cloud, Azure, etc.)
- Database passwords
- Authentication tokens
- Private keys (SSH, TLS, etc.)
- OAuth secrets
- Encryption keys
- Service account credentials
- Third-party service keys (Stripe, Twilio, etc.)

**Deliverable:** List of files containing potential secrets with line numbers

---

### 2. Dependency Vulnerability Scanning

**Python Dependencies:**

```bash
# Using pip-audit (recommended)
pip-audit --desc --format json > pip-audit-report.json

# Using safety
safety check --json > safety-report.json

# Check for outdated packages
pip list --outdated --format json
```

**Node.js Dependencies:**

```bash
# NPM audit
npm audit --json > npm-audit-report.json

# Yarn audit
yarn audit --json > yarn-audit-report.json
```

**General Container/Filesystem Scanning:**

```bash
# Trivy (multi-language)
trivy filesystem . --format json --output trivy-report.json

# Check specific files
trivy filesystem requirements.txt
trivy filesystem package.json
```

**Dependency Checks:**
- Known CVEs in dependencies
- Outdated packages with security patches
- Unmaintained packages
- License compliance issues
- Transitive dependency vulnerabilities

**Deliverable:** Vulnerability report with CVE IDs, severity scores, and affected packages

---

### 3. Insecure Code Pattern Detection

**SQL Injection Vulnerabilities:**

```bash
# Python - Look for string concatenation in SQL queries
grep -r "execute.*%.*" src/ --include="*.py"
grep -r "execute.*\+.*" src/ --include="*.py"
grep -r "cursor.execute.*format" src/ --include="*.py"

# Look for string formatting in SQL
grep -r "SELECT.*{" src/ --include="*.py"
grep -r "INSERT.*{" src/ --include="*.py"
grep -r "UPDATE.*{" src/ --include="*.py"
grep -r "DELETE.*{" src/ --include="*.py"
```

**Command Injection:**

```bash
# Python - subprocess with shell=True
grep -r "subprocess.*shell=True" src/ --include="*.py"
grep -r "os.system" src/ --include="*.py"
grep -r "os.popen" src/ --include="*.py"

# Node.js - child_process exec
grep -r "child_process.*exec" src/ --include="*.js"
grep -r "\.exec(" src/ --include="*.js"
```

**Path Traversal:**

```bash
# Unsanitized file paths
grep -r "open(.*request\." src/ --include="*.py"
grep -r "os.path.join(.*request\." src/ --include="*.py"
grep -r "readFile(.*req\." src/ --include="*.js"
```

**Insecure Deserialization:**

```bash
# Python pickle
grep -r "pickle.loads" src/ --include="*.py"
grep -r "cPickle.loads" src/ --include="*.py"

# YAML load (unsafe)
grep -r "yaml.load(" src/ --include="*.py"

# Node.js eval
grep -r "eval(" src/ --include="*.js"
```

**Cross-Site Scripting (XSS):**

```bash
# HTML rendering without escaping
grep -r "\.innerHTML" src/ --include="*.js" --include="*.jsx"
grep -r "dangerouslySetInnerHTML" src/ --include="*.jsx" --include="*.tsx"

# Python templates without autoescape
grep -r "autoescape=False" src/ --include="*.py"
```

**Weak Cryptography:**

```bash
# MD5, SHA1 usage
grep -r "hashlib.md5" src/ --include="*.py"
grep -r "hashlib.sha1" src/ --include="*.py"
grep -r "crypto.createHash('md5')" src/ --include="*.js"

# Weak random
grep -r "random.random(" src/ --include="*.py"
grep -r "Math.random(" src/ --include="*.js"
```

**Deliverable:** List of insecure code patterns with file locations and severity

---

### 4. Authentication & Authorization Issues

**Missing Authentication:**

```bash
# Python Flask routes without auth decorators
grep -r "@app.route" src/ --include="*.py" -A 1 | grep -v "@login_required" | grep -v "@auth_required"

# Express routes without middleware
grep -r "app.get\|app.post" src/ --include="*.js" -A 1
```

**Hardcoded Credentials:**

```bash
# Default passwords
grep -r "password.*=.*['\"]admin['\"]" src/
grep -r "password.*=.*['\"]password['\"]" src/
grep -r "password.*=.*['\"]123456['\"]" src/

# Default tokens
grep -r "token.*=.*['\"]test['\"]" src/
```

**Session Management:**

```bash
# Insecure session configuration
grep -r "SESSION_COOKIE_SECURE.*False" src/ --include="*.py"
grep -r "SESSION_COOKIE_HTTPONLY.*False" src/ --include="*.py"
grep -r "SESSION_COOKIE_SAMESITE.*None" src/ --include="*.py"
```

**Deliverable:** Authentication and authorization gaps with recommendations

---

### 5. Static Analysis with Automated Tools

**Python - Bandit:**

```bash
# Run bandit for Python security issues
bandit -r src/ -f json -o bandit-report.json

# With specific tests
bandit -r src/ -f json --severity-level medium

# Show only high severity
bandit -r src/ -ll
```

**Multi-language - Semgrep:**

```bash
# Auto-detect and scan
semgrep --config=auto . --json > semgrep-report.json

# OWASP Top 10 rules
semgrep --config=p/owasp-top-ten . --json

# Security audit
semgrep --config=p/security-audit . --json

# Python-specific
semgrep --config=p/python . --json
```

**JavaScript - ESLint Security:**

```bash
# With security plugin
eslint src/ --format json > eslint-report.json

# With security-specific rules
eslint src/ --plugin security --format json
```

**Deliverable:** Automated tool reports with findings categorized by severity

---

### 6. Configuration Security

**Environment Files:**

```bash
# Check for committed .env files
find . -name ".env" -o -name ".env.*" | grep -v ".env.example"

# Check .gitignore
grep -q "\.env" .gitignore || echo "WARNING: .env not in .gitignore"
```

**Security Headers:**

```bash
# Check for security header configuration
grep -r "X-Frame-Options" src/ config/
grep -r "Content-Security-Policy" src/ config/
grep -r "X-Content-Type-Options" src/ config/
grep -r "Strict-Transport-Security" src/ config/
```

**CORS Configuration:**

```bash
# Overly permissive CORS
grep -r "Access-Control-Allow-Origin.*\*" src/ config/
grep -r "cors().*origin:.*\*" src/ --include="*.js"
```

**Deliverable:** Configuration security issues and recommendations

---

## Scanning Output Format

Create a security scan report:

```markdown
# Security Scan Report

**Date**: [YYYY-MM-DD]
**Scan Scope**: [path/to/code]
**Scanner Version**: [tool versions]

## Summary

- **Critical Issues**: [count]
- **High Issues**: [count]
- **Medium Issues**: [count]
- **Low Issues**: [count]
- **Informational**: [count]

## Critical Issues

### [Issue Title]

**File**: [path/to/file:line]
**Category**: [Secret/Injection/etc.]
**Severity**: Critical

**Description**: [What was found]

**Evidence**:
```
[code snippet]
```

**Recommendation**: [How to fix]

---

## High Issues

[Similar format]

## Medium Issues

[Similar format]

## Low Issues

[Similar format]

## Tool Reports

### Dependency Scan (pip-audit)
- Vulnerable packages: [count]
- CVEs found: [list]

### Secret Detection (gitleaks)
- Secrets found: [count]
- Types: [API keys, passwords, etc.]

### Static Analysis (bandit)
- Issues found: [count]
- Most common: [issue type]

## Recommendations

### Immediate Actions (Critical/High)
1. [Action 1]
2. [Action 2]

### Short-term (Medium)
1. [Action 1]

### Long-term (Low)
1. [Action 1]

## False Positives

[List any false positives to ignore in future scans]
```

---

## Best Practices

**Secret Scanning:**
- Always scan before committing code
- Check git history for past secrets
- Use pre-commit hooks for automated scanning
- Never commit .env files
- Use secret management tools (Vault, AWS Secrets Manager)

**Dependency Scanning:**
- Scan before adding new dependencies
- Keep dependencies updated
- Monitor for new vulnerabilities
- Use lock files (requirements.txt, package-lock.json)
- Consider dependency pinning

**Code Pattern Detection:**
- Focus on user input handling
- Check all database queries
- Review file operations
- Validate all external inputs
- Sanitize all outputs

**Automated Tools:**
- Run multiple tools for better coverage
- Configure tools with project-specific rules
- Integrate into CI/CD pipeline
- Review and triage findings
- Track false positives

---

## Supporting Scripts

**Quick Scan Script** (`scripts/quick-security-scan.sh`):

```bash
#!/bin/bash
# Quick security scan

echo "Running security scans..."

# Secret detection
echo "1. Scanning for secrets..."
gitleaks detect --no-git || echo "Gitleaks not available"

# Dependency check
echo "2. Checking dependencies..."
if [ -f requirements.txt ]; then
    pip-audit || echo "pip-audit not available"
fi

# Static analysis
echo "3. Running static analysis..."
if [ -d src ]; then
    bandit -r src/ -ll || echo "Bandit not available"
fi

echo "Scan complete!"
```

---

## Integration with Security Assessment

**Input**: Codebase to scan
**Process**: Automated scanning with multiple tools
**Output**: Security scan report with findings
**Next Step**: Vulnerability assessment for detailed analysis

---

## Tools Installation

**Python Security Tools:**

```bash
pip install pip-audit safety bandit
```

**Secret Scanners:**

```bash
# Gitleaks (via binary release)
# See: https://github.com/gitleaks/gitleaks/releases

# Trufflehog
pip install truffleHog
```

**Multi-language:**

```bash
# Semgrep
pip install semgrep

# Trivy (via binary release)
# See: https://github.com/aquasecurity/trivy/releases
```

---

## Scan Frequency

- **Pre-commit**: Secret detection
- **Daily**: Dependency scanning
- **Weekly**: Full static analysis
- **Before PR**: Complete security scan
- **Before release**: Comprehensive assessment

---

## Remember

- **Automate everything**: Use tools, don't scan manually
- **Multiple tools**: Each catches different issues
- **Triage findings**: Not all findings are exploitable
- **Fix high severity first**: Prioritize by risk
- **Track over time**: Monitor security trends
- **Update tools**: Keep scanners current
- **Document exceptions**: Log false positives

Your goal is to identify security issues early and comprehensively through automated scanning.