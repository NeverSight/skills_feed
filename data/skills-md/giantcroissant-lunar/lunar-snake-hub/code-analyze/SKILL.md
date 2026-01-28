---
name: code-analyze
version: 0.1.0
kind: cli
description: Run static analysis, security scans, and dependency checks on .NET code. Use when task involves code quality, security audits, or vulnerability detection.
inputs:
  analysis_type: [static, security, dependencies, all]
  project_path: string
  severity_filter: [error, warning, suggestion, all]
contracts:
  success: 'Analysis completes with findings report; exit code 0'
  failure: 'Non-zero exit code or tool execution errors'
---

# Code Analysis Skill (Entry Map)

> **Goal:** Guide agent to the exact analysis procedure needed.

## Quick Start (Pick One)

- **Run static code analysis** → `references/static-analysis.md`
- **Scan for security issues** → `references/security-scan.md`
- **Check dependency vulnerabilities** → `references/dependency-check.md`

## When to Use

- Enforce code quality standards and best practices
- Detect potential bugs and code smells
- Identify security vulnerabilities in code
- Check for vulnerable dependencies
- Run automated code reviews

**NOT for:** building (dotnet-build), testing (dotnet-test), or formatting (code-format)

## Inputs & Outputs

**Inputs:** `analysis_type` (static/security/dependencies/all), `project_path` (default: ./dotnet/PigeonPea.sln), `severity_filter` (error/warning/suggestion)

**Outputs:** `analysis_report` (findings with file/line), `exit_code` (0=clean, 1=issues), `metrics` (violations by severity)

**Guardrails:** Analyze only, never modify code, report all findings with context, fail on critical issues

## Navigation

**1. Static Code Analysis** → [`references/static-analysis.md`](references/static-analysis.md)

- Roslyn analyzers, StyleCop, code quality rules, best practices

**2. Security Scanning** → [`references/security-scan.md`](references/security-scan.md)

- Secret detection (gitleaks, detect-secrets), security analyzers, vulnerability patterns

**3. Dependency Vulnerability Check** → [`references/dependency-check.md`](references/dependency-check.md)

- NuGet package vulnerabilities, outdated dependencies, CVE detection

## Common Patterns

### Quick Analysis (All Checks)

```bash
cd ./dotnet
dotnet build PigeonPea.sln /p:TreatWarningsAsErrors=true
dotnet list package --vulnerable
```

### Static Analysis Only

```bash
cd ./dotnet
dotnet build PigeonPea.sln /p:RunAnalyzers=true /warnaserror
```

### Security Scan (Pre-commit)

```bash
pre-commit run gitleaks --all-files
pre-commit run detect-secrets --all-files
```

### Dependency Check

```bash
cd ./dotnet
dotnet list package --vulnerable --include-transitive
dotnet list package --outdated
```

### Full Analysis Suite

```bash
# Run from repository root
.agent/skills/code-analyze/scripts/analyze.sh --all
```

### Analysis with Specific Severity

```bash
cd ./dotnet
# Errors only
dotnet build PigeonPea.sln /p:TreatWarningsAsErrors=false

# Warnings as errors
dotnet build PigeonPea.sln /p:TreatWarningsAsErrors=true
```

## Troubleshooting

**No analyzers found:** Verify Roslyn analyzers enabled. See `references/static-analysis.md`.

**Too many warnings:** Filter by severity or add suppressions. See `references/static-analysis.md`.

**False positives:** Use `.editorconfig` or suppressions. See `references/static-analysis.md`.

**Secrets not detected:** Check `.gitleaksignore` and `.secrets.baseline`. See `references/security-scan.md`.

**Dependency scan fails:** Network issues or package restore needed. See `references/dependency-check.md`.

## Success Indicators

**Static Analysis:**

```
Build succeeded.
    0 Warning(s)
    0 Error(s)
```

**Security Scan:**

```
gitleaks................Passed
detect-secrets...........Passed
```

**Dependency Check:**

```
No vulnerable packages found.
```

## Integration

**Before commit:** Run security scans (gitleaks, detect-secrets)
**After build:** Run static analysis (Roslyn, StyleCop)
**Regular checks:** Run dependency vulnerability checks

**CI/CD Integration:** Include all analysis in build pipeline, fail on critical issues

## Related

- [`./dotnet/ARCHITECTURE.md`](../../../dotnet/ARCHITECTURE.md) - Project structure
- [`.pre-commit-config.yaml`](../../../.pre-commit-config.yaml) - Pre-commit hooks
- [`.editorconfig`](../../../.editorconfig) - Code style rules
- [`dotnet-build`](../dotnet-build/SKILL.md) - Build skill
