---
name: medusa-security
description: >-
  AI-first security scanning with Medusa. 3,000+ detection patterns covering AI/ML, agents, MCP,
  RAG, prompt injection, and traditional SAST vulnerabilities. Wraps Medusa CLI with SARIF/JSON
  parsing, structured finding output, OWASP mapping, and remediation guidance.
version: 1.0.0
category: security
model: sonnet
invoked_by: agent
user_invocable: true
tools: [Read, Write, Edit, Bash, Glob, Grep]
agents: [security-architect, penetration-tester, code-reviewer]
tags: [security, sast, ai-security, mcp-security, prompt-injection, vulnerability-scanning]
best_practices:
  - Run full scan before release for comprehensive coverage
  - Use ai-only mode for rapid AI/LLM-focused checks
  - Use quick mode during development for changed-files-only scanning
  - Always review CRITICAL and HIGH findings before deployment
  - Use --fail-on high in CI/CD pipelines
error_handling: graceful
streaming: supported
verified: false
lastVerifiedAt: 2026-02-19T05:29:09.098Z
---

# Medusa Security Skill

## Identity

AI-first security scanner integration skill. Leverages Medusa's 76 scanners and 3,000+ detection
patterns for comprehensive security analysis including AI/ML-specific vulnerability detection.

## Capabilities

1. **Full Scan** — All 76 scanners, comprehensive security analysis
2. **AI-Only Scan** — Prompt injection, MCP security, agent security, RAG security
3. **Quick Scan** — Git-changed files only for rapid development feedback
4. **Targeted Scan** — Specific scanner categories (mcp, secrets, prompt-injection, etc.)
5. **SARIF Output Parsing** — Standard SARIF v2.1.0 structured findings
6. **JSON Output Parsing** — Medusa-native JSON format
7. **OWASP Mapping** — Maps findings to OWASP Agentic AI (ASI01-10) and OWASP Top 10 (A01-10)
8. **Remediation Guidance** — Links findings to agent-studio skills and agents
9. **CI/CD Integration** — Fail-on thresholds, SARIF upload for GitHub Code Scanning

## Prerequisites

```
Python 3.10+
pip install medusa-security
```

Check installation: `python -m medusa --version`

## Workflow: Full Security Scan

```bash
# Step 1: Verify installation
python -m medusa --version

# Step 2: Run scan
medusa scan . --format sarif --fail-on high

# Step 3: Parse output (use scripts/main.cjs)
node .claude/skills/medusa-security/scripts/main.cjs --mode full --target .

# Step 4: Review findings by severity
# CRITICAL → immediate fix required
# HIGH → fix before release
# MEDIUM → fix in next sprint
# LOW → track and address
```

## Workflow: AI-Only Scan

```bash
medusa scan . --format sarif --ai-only
```

Scans only: prompt injection (800+ patterns), MCP security (400+ patterns), agent security
(500+ patterns), RAG security (300+ patterns).

## Workflow: Quick Scan (Development)

```bash
medusa scan . --format sarif --quick
```

Only scans git-changed files. Use during development for rapid feedback.

## Workflow: Targeted Scan

```bash
# MCP security only
medusa scan . --format sarif --scanners mcp-server,mcp-config

# Secrets only
medusa scan . --format sarif --scanners secrets,gitleaks,env

# AI context files only
medusa scan . --format sarif --scanners ai-context
```

## Output Processing

The skill uses helper scripts located at `.claude/skills/medusa-security/scripts/`:

| Script                  | Purpose                                         |
| ----------------------- | ----------------------------------------------- |
| `sarif-parser.cjs`      | Parses SARIF v2.1.0 output                      |
| `json-parser.cjs`       | Parses Medusa JSON output                       |
| `finding-formatter.cjs` | Formats findings with OWASP mapping             |
| `main.cjs`              | Orchestrates the full pipeline                  |
| `cli-wrapper.cjs`       | Wraps Medusa CLI invocation                     |
| `security-review.cjs`   | Deterministic report writer (no Glob recursion) |

### Using the Pipeline

```bash
# Full scan with structured output
node .claude/skills/medusa-security/scripts/main.cjs --mode full --target .

# AI-only scan
node .claude/skills/medusa-security/scripts/main.cjs --mode ai-only --target .

# Quick scan (git-changed files)
node .claude/skills/medusa-security/scripts/main.cjs --mode quick --target .
```

### Deterministic Security Review (Recommended in Claude sessions)

Use this when you need the final security review report and want to avoid recursive `Glob` timeouts:

```bash
node .claude/skills/medusa-security/scripts/security-review.cjs
```

This writes:

`/.claude/context/reports/security-review-medusa-scan-2026-02-17.md`

and performs fixed-path checks on:

- `.claude/hooks/`
- `.claude/lib/`
- `.claude/skills/medusa-security/scripts/`
- `.claude/CLAUDE.md`

### Important Runtime Guardrail

- Avoid recursive glob patterns like `.claude/skills/medusa-security/**/*` in long sessions.
- Prefer direct file reads and deterministic script entry points.

## OWASP Mapping

Findings are automatically mapped to:

- **OWASP Agentic AI Top 10** (ASI01-10): Goal Hijacking, Tool Misuse, Context Poisoning, etc.
- **OWASP Top 10** (A01-10): Broken Access Control, Injection, Cryptographic Failures, etc.

## Severity Triage

| Severity | Action             | Timeline         |
| -------- | ------------------ | ---------------- |
| CRITICAL | Immediate fix      | Before any merge |
| HIGH     | Fix before release | Same sprint      |
| MEDIUM   | Fix in next sprint | Next cycle       |
| LOW      | Track and address  | Backlog          |

## Agent Integration

| Agent                | Usage                                                       |
| -------------------- | ----------------------------------------------------------- |
| `security-architect` | Primary consumer. Use for comprehensive security reviews.   |
| `penetration-tester` | Use for targeted vulnerability scanning with authorization. |
| `code-reviewer`      | Use AI-only scan as part of code review workflow.           |

## CI/CD Integration

```yaml
# GitHub Actions example
- name: Security Scan
  run: |
    pip install medusa-security
    medusa scan . --format sarif --fail-on high -o reports/
- name: Upload SARIF
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: reports/medusa-results.sarif
```

## Memory Protocol

After scanning:

- Record new vulnerability patterns in `patterns.json`
- Log significant findings in `issues.md`
- Track scan history for trend analysis
- Use `recordGotcha()` for recurring false positives

```javascript
const manager = require('.claude/lib/memory/memory-manager.cjs');

manager.recordGotcha({
  text: 'False positive: medusa flags X pattern in Y context',
  area: 'security-scanning',
});

manager.recordPattern({
  text: 'Prompt injection found in CLAUDE.md context files',
  area: 'ai-security',
});
```

## Related Skills

- `security-architect` — Threat modeling and OWASP analysis
- `static-analysis` — CodeQL and Semgrep SARIF analysis
- `semgrep-rule-creator` — Create custom Semgrep rules
- `insecure-defaults` — Detect hardcoded credentials
- `variant-analysis` — Discover vulnerability variants
