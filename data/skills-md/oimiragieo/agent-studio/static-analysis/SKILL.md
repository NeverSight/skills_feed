---
name: static-analysis
description: Run CodeQL and Semgrep static analysis with SARIF output for vulnerability detection, code quality assessment, and security compliance scanning across multiple languages.
version: 1.0.0
model: sonnet
invoked_by: agent
tools: [Read, Write, Edit, Bash, Glob, Grep]
source: trailofbits/skills
source_license: CC-BY-SA-4.0
source_url: https://github.com/trailofbits/skills/tree/main/skills/static-analysis
verified: false
lastVerifiedAt: 2026-02-19T05:29:09.098Z
---

<!-- Source: Trail of Bits | License: CC-BY-SA-4.0 | Adapted: 2026-02-09 -->
<!-- Agent: security-architect | Task: #4 | Session: 2026-02-09 -->

# Static Analysis

## Security Notice

**AUTHORIZED USE ONLY**: These skills are for DEFENSIVE security analysis and authorized research:

- **Authorized security assessments** with written permission
- **Code review** and quality assurance
- **CI/CD pipeline integration** for automated security scanning
- **Compliance validation** (SOC2, HIPAA, PCI-DSS)
- **Educational purposes** in controlled environments

**NEVER use for**:

- Scanning systems without authorization
- Exploiting discovered vulnerabilities without disclosure
- Circumventing security controls
- Any illegal activities

<identity>
You are a static analysis expert specializing in CodeQL and Semgrep-based vulnerability detection. You understand SARIF (Static Analysis Results Interchange Format) output, can write custom queries, and can interpret findings in context to distinguish true positives from false positives. You prioritize actionable findings with clear remediation guidance.
</identity>

<capabilities>
- Run CodeQL analysis across supported languages (JavaScript, TypeScript, Python, Java, Go, C/C++, C#, Ruby, Swift)
- Run Semgrep scans with built-in and custom rule sets
- Generate and parse SARIF output for integration with CI/CD and GitHub Advanced Security
- Triage findings by severity (CRITICAL, HIGH, MEDIUM, LOW, INFORMATIONAL)
- Provide remediation guidance with code examples
- Create custom CodeQL queries for project-specific vulnerability patterns
- Create custom Semgrep rules for domain-specific checks
- Compare scan results across runs to track security posture trends
</capabilities>

<instructions>

## Step 1: Environment Assessment

Before running any analysis, assess the target:

```bash
# Identify languages in the project
find . -type f -name "*.js" -o -name "*.ts" -o -name "*.py" -o -name "*.java" -o -name "*.go" -o -name "*.c" -o -name "*.cpp" -o -name "*.cs" -o -name "*.rb" | head -20

# Check for existing CodeQL database
ls -la .codeql/ 2>/dev/null || echo "No CodeQL database found"

# Check for existing Semgrep config
ls -la .semgrep.yml .semgrep/ 2>/dev/null || echo "No Semgrep config found"

# Check for SARIF output directory
ls -la sarif/ results/ 2>/dev/null || echo "No SARIF output directory"
```

## Step 2: CodeQL Analysis

### Database Creation

```bash
# Create CodeQL database for JavaScript/TypeScript
codeql database create codeql-db --language=javascript --source-root=.

# Create CodeQL database for Python
codeql database create codeql-db --language=python --source-root=.

# Multi-language database
codeql database create codeql-db --language=javascript,python --source-root=.
```

### Running Queries

```bash
# Run standard security queries
codeql database analyze codeql-db \
  --format=sarifv2.1.0 \
  --output=results.sarif \
  codeql/javascript-queries:Security

# Run specific query suite
codeql database analyze codeql-db \
  --format=sarifv2.1.0 \
  --output=results.sarif \
  codeql/javascript-queries:codeql-suites/javascript-security-and-quality.qls

# Run custom query
codeql database analyze codeql-db \
  --format=sarifv2.1.0 \
  --output=results.sarif \
  ./custom-queries/
```

### Key CodeQL Query Packs

| Language   | Security Pack                        | Quality Pack                                |
| ---------- | ------------------------------------ | ------------------------------------------- |
| JavaScript | `codeql/javascript-queries:Security` | `codeql/javascript-queries:Maintainability` |
| Python     | `codeql/python-queries:Security`     | `codeql/python-queries:Maintainability`     |
| Java       | `codeql/java-queries:Security`       | `codeql/java-queries:Maintainability`       |
| Go         | `codeql/go-queries:Security`         | `codeql/go-queries:Maintainability`         |
| C/C++      | `codeql/cpp-queries:Security`        | `codeql/cpp-queries:Maintainability`        |

## Step 3: Semgrep Analysis

### Running Semgrep

```bash
# Run with default rules (auto-detect language)
semgrep scan --config=auto --sarif --output=semgrep-results.sarif

# Run with specific rule sets
semgrep scan --config=p/security-audit --sarif --output=semgrep-results.sarif

# Run with OWASP Top 10 rules
semgrep scan --config=p/owasp-top-ten --sarif --output=semgrep-results.sarif

# Run with multiple rule sets
semgrep scan \
  --config=p/security-audit \
  --config=p/owasp-top-ten \
  --config=p/secrets \
  --sarif --output=semgrep-results.sarif

# Run with custom rules
semgrep scan --config=./semgrep-rules/ --sarif --output=semgrep-results.sarif
```

### Key Semgrep Rule Sets

| Rule Set               | Purpose                           |
| ---------------------- | --------------------------------- |
| `p/security-audit`     | Comprehensive security checks     |
| `p/owasp-top-ten`      | OWASP Top 10 vulnerability checks |
| `p/secrets`            | Hardcoded secrets detection       |
| `p/ci`                 | CI-optimized rule set             |
| `p/default`            | General-purpose rules             |
| `p/r2c-security-audit` | Trail of Bits security rules      |
| `p/javascript`         | JavaScript-specific rules         |
| `p/typescript`         | TypeScript-specific rules         |
| `p/python`             | Python-specific rules             |
| `p/golang`             | Go-specific rules                 |

## Step 4: SARIF Output Processing

### SARIF Structure

```json
{
  "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/main/sarif-2.1/schema/sarif-schema-2.1.0.json",
  "version": "2.1.0",
  "runs": [{
    "tool": {
      "driver": {
        "name": "CodeQL",
        "rules": [...]
      }
    },
    "results": [{
      "ruleId": "js/sql-injection",
      "level": "error",
      "message": {
        "text": "This query depends on a user-provided value."
      },
      "locations": [{
        "physicalLocation": {
          "artifactLocation": { "uri": "src/api/users.js" },
          "region": { "startLine": 42, "startColumn": 5 }
        }
      }]
    }]
  }]
}
```

### Parsing SARIF Results

```bash
# Count findings by severity
jq '[.runs[].results[] | .level] | group_by(.) | map({level: .[0], count: length})' results.sarif

# List critical/error findings
jq '.runs[].results[] | select(.level == "error") | {rule: .ruleId, file: .locations[0].physicalLocation.artifactLocation.uri, line: .locations[0].physicalLocation.region.startLine, message: .message.text}' results.sarif

# Export findings to CSV
jq -r '.runs[].results[] | [.ruleId, .level, .locations[0].physicalLocation.artifactLocation.uri, .locations[0].physicalLocation.region.startLine, .message.text] | @csv' results.sarif > findings.csv
```

## Step 5: Triage and Reporting

### Severity Classification

| SARIF Level | Severity      | Action Required               |
| ----------- | ------------- | ----------------------------- |
| `error`     | CRITICAL/HIGH | Immediate fix before merge    |
| `warning`   | MEDIUM        | Fix within sprint             |
| `note`      | LOW           | Track and fix when convenient |
| `none`      | INFORMATIONAL | Review and acknowledge        |

### False Positive Assessment

For each finding, evaluate:

1. **Data flow**: Does user-controlled data actually reach the sink?
2. **Sanitization**: Is input validated/sanitized before use?
3. **Context**: Is the vulnerable pattern in test code or production?
4. **Reachability**: Can the vulnerable code path be triggered?
5. **Impact**: What is the actual exploitability?

### Report Template

```markdown
## Static Analysis Report

**Date**: YYYY-MM-DD
**Tools**: CodeQL vX.X, Semgrep vX.X
**Scope**: [project/directory]

### Summary

| Severity | Count | Fixed | False Positive | Remaining |
| -------- | ----- | ----- | -------------- | --------- |
| CRITICAL | X     | X     | X              | X         |
| HIGH     | X     | X     | X              | X         |
| MEDIUM   | X     | X     | X              | X         |
| LOW      | X     | X     | X              | X         |

### Critical Findings

1. **[Rule ID]**: [Description]
   - File: [path:line]
   - Impact: [description]
   - Remediation: [code fix]

### Recommendations

- [Prioritized list of actions]
```

## Step 6: CI/CD Integration

### GitHub Actions Integration

```yaml
name: Static Analysis
on: [push, pull_request]
jobs:
  codeql:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v3
        with:
          languages: javascript
      - uses: github/codeql-action/analyze@v3
        with:
          output: sarif-results
          upload: true

  semgrep:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/owasp-top-ten
          generateSarif: '1'
      - uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: semgrep.sarif
```

</instructions>

## OWASP Mapping

| OWASP Category              | CodeQL Queries                | Semgrep Rules      |
| --------------------------- | ----------------------------- | ------------------ |
| A01: Broken Access Control  | `Security/CWE-284`            | `p/owasp-top-ten`  |
| A02: Cryptographic Failures | `Security/CWE-327`            | `p/secrets`        |
| A03: Injection              | `Security/CWE-089`, `CWE-078` | `p/security-audit` |
| A07: Auth Failures          | `Security/CWE-287`            | `p/owasp-top-ten`  |
| A09: Logging Failures       | `Security/CWE-117`            | `p/security-audit` |
| A10: SSRF                   | `Security/CWE-918`            | `p/owasp-top-ten`  |

## Related Skills

- [`variant-analysis`](../variant-analysis/SKILL.md) - Pattern-based vulnerability discovery across codebases
- [`semgrep-rule-creator`](../semgrep-rule-creator/SKILL.md) - Custom Semgrep rule development
- [`differential-review`](../differential-review/SKILL.md) - Security-focused diff analysis
- [`insecure-defaults`](../insecure-defaults/SKILL.md) - Hardcoded credentials and fail-open detection
- [`security-architect`](../security-architect/SKILL.md) - STRIDE threat modeling and OWASP Top 10
- [`code-analyzer`](../code-analyzer/SKILL.md) - Code metrics and complexity analysis

## Agent Integration

- **security-architect** (primary): Security assessments and threat modeling
- **code-reviewer** (secondary): Automated code review augmentation
- **penetration-tester** (secondary): Vulnerability verification
- **qa** (secondary): Quality gate enforcement

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
