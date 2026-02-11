---
name: security-audit-owasp-top-10
description: "Performs comprehensive security audit of any codebase against OWASP Top 10 2025. Use when user asks for OWASP audit, OWASP Top 10 review, OWASP security check, or wants to audit code against OWASP categories. Do not trigger for PR review, npm/pip audit, SOC2 compliance, general security questions, or threat modeling."
---

# OWASP Top 10 2025 Security Audit

## Goal

Systematic codebase audit against the OWASP Top 10 2025 framework. Produces a structured severity-rated report with evidence-backed findings. Emphasizes semantic code understanding over regex pattern matching — grep patterns are starting points, real analysis happens by reading and reasoning about code context.

## When to use

- "Run an OWASP audit on this codebase"
- "Check for OWASP Top 10 vulnerabilities"
- "Security audit against OWASP 2025"
- "Audit A01 and A03 only"
- "Check this repo for common vulnerabilities"
- "OWASP security review"

## When not to use

- PR code review (use review skill)
- `npm audit` / `pip audit` / dependency scanning only
- SOC2 / ISO 27001 compliance checks (use drata-api skill)
- General security questions without audit intent
- Threat modeling (use security-threat-model skill)
- Single-file code review

## Inputs

- Codebase accessible via Glob/Grep/Read
- Optional: specific OWASP categories (e.g. "A01 and A03 only")
- Optional: focus areas or known concerns

## Outputs

- Markdown report inline (write to file only if user requests)
- Executive summary table
- Per-category findings with severity/confidence/evidence/remediation
- Summary statistics and next steps

## Workflow

### Phase 1: Reconnaissance

Classify the project before auditing. Use Glob/Read on key files:

```
Glob: package.json, requirements.txt, go.mod, Cargo.toml, *.tf, *.csproj, pom.xml
Glob: Dockerfile*, docker-compose*, .github/workflows/*
Glob: **/routes/*, **/api/*, **/controllers/*, **/handlers/*
Read: README.md (first 100 lines), main entry points
```

Determine:
- **Project type**: web-app | api | iac | library | cli | mobile | monorepo
- **Languages/frameworks**: e.g. Node/Express, Python/Django, Go/Gin, Terraform/AWS
- **Deployment model**: serverless, containers, VMs, static hosting
- **Data sensitivity signals**: auth, PII, payments, healthcare, crypto

### Phase 2: Relevance Filtering

Use project type to set audit depth per category. Prevents nonsensical checks (e.g. SQL injection on Terraform).

| Category | web-app | api | iac | library | cli | mobile |
|----------|---------|-----|-----|---------|-----|--------|
| A01 Broken Access Control | Full | Full | Full | Light | Light | Full |
| A02 Security Misconfiguration | Full | Full | Full | Light | Light | Full |
| A03 Supply Chain Failures | Full | Full | Light | Full | Full | Full |
| A04 Cryptographic Failures | Full | Full | Light | Full | Light | Full |
| A05 Injection | Full | Full | Skip | Light | Full | Full |
| A06 Insecure Design | Full | Full | Light | Light | Light | Full |
| A07 Authentication Failures | Full | Full | Skip | Light | Skip | Full |
| A08 Data Integrity Failures | Full | Full | Light | Full | Light | Full |
| A09 Logging & Alerting | Full | Full | Light | Light | Light | Full |
| A10 Exceptional Conditions | Full | Full | Light | Full | Full | Full |

- **Full**: run all grep patterns + semantic analysis
- **Light**: grep patterns only, flag but don't deep-dive
- **Skip**: mention as not applicable in report, move on

### Phase 3: Evidence Gathering

For each relevant category, run Grep/Glob patterns from `CATEGORIES.md`. Use parallel tool calls for independent categories. Collect file paths and matching lines as evidence.

### Phase 4: Semantic Analysis

For each flagged file/pattern:
1. Read surrounding code context (not just matched line)
2. Determine if finding is true positive or false positive
3. Check for existing mitigations (guards, validators, middleware)
4. Assign severity: Critical / High / Medium / Low
5. Assign confidence: High / Medium / Low
6. Note specific remediation

**Severity criteria:**
- **Critical**: exploitable without authentication, leads to data breach or RCE
- **High**: exploitable with low-privilege access, significant data exposure
- **Medium**: requires specific conditions, limited exposure
- **Low**: defense-in-depth issue, minimal direct impact

### Phase 5: Report Generation

Use this template:

```markdown
# OWASP Top 10 2025 Security Audit Report

**Project**: <name>
**Type**: <project-type> | **Languages**: <langs> | **Date**: <date>
**Scope**: <full audit | partial: categories listed>

## Executive Summary

| Severity | Count |
|----------|-------|
| Critical | N |
| High     | N |
| Medium   | N |
| Low      | N |
| Info     | N |

<1-3 sentence summary of key findings and overall posture>

## Findings

### A0X: <Category Name> — <PASS | FINDINGS | N/A>

> Relevance: Full | Light | Skip

#### Finding X.1: <title>
- **Severity**: Critical | High | Medium | Low
- **Confidence**: High | Medium | Low
- **Location**: `path/to/file:line`
- **Evidence**: <code snippet or pattern match>
- **Issue**: <what's wrong and why it matters>
- **Remediation**: <specific fix>

(repeat per finding)

---

## Summary Table

| Category | Status | Critical | High | Medium | Low |
|----------|--------|----------|------|--------|-----|
| A01 | ... | ... | ... | ... | ... |
(all 10 categories)

## Methodology

- Automated pattern matching via Grep/Glob
- Semantic code analysis of flagged locations
- False positive filtering based on code context
- Project-type relevance filtering applied

## Next Steps

1. <prioritized remediation actions>
2. <recommended tooling or processes>
3. <categories needing deeper manual review>
```

## Partial Audit Support

When user requests specific categories (e.g. "audit A01 and A03 only"):
1. Skip Phase 2 (relevance filtering)
2. Minimal Phase 1 — detect language/framework only
3. Run only requested categories through Phases 3-5
4. Report covers only requested categories, notes others as out-of-scope

## Decision Points

- **Large codebase (>500 files)**: Focus on entry points, auth boundaries, and config files. Note coverage limitations in report.
- **Monorepo**: Run Phase 1 per sub-project. Produce per-project section or single unified report based on user preference.
- **No findings**: Report as clean audit with methodology notes. Don't fabricate issues.

## Validation Checklist

- [ ] All 10 categories addressed (or noted as N/A/out-of-scope)
- [ ] Every finding has severity + confidence + location + evidence + remediation
- [ ] False positives filtered (not just raw grep output)
- [ ] Project type correctly identified and relevance matrix applied
- [ ] Report uses consistent severity definitions
- [ ] Executive summary accurately reflects findings

## References

- Category details, grep patterns, semantic checks: `CATEGORIES.md`
- Evaluation prompts: `EVALUATIONS.md`
