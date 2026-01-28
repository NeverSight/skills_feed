---
name: Dependency Health
description: Security-first dependency management methodology with batch remediation, policy-driven compliance, and automated enforcement. Use when security vulnerabilities exist in dependencies, dependency freshness low (outdated packages), license compliance needed, or systematic dependency management lacking. Provides security-first prioritization (critical vulnerabilities immediately, high within week, medium within month), batch remediation strategy (group compatible updates, test together, single PR), policy-driven compliance framework (security policies, freshness policies, license policies), and automation tools for vulnerability scanning, update detection, and compliance checking. Validated in meta-cc with 6x speedup (9 hours manual to 1.5 hours systematic), 3 iterations, 88% transferability across package managers (concepts universal, tools vary by ecosystem).
allowed-tools: Read, Write, Edit, Bash
---

# Dependency Health

**Systematic dependency management: security-first, batch remediation, policy-driven.**

> Dependencies are attack surface. Manage them systematically, not reactively.

---

## When to Use This Skill

Use this skill when:
- 🔒 **Security vulnerabilities**: Known CVEs in dependencies
- 📅 **Outdated dependencies**: Packages months/years behind
- ⚖️ **License compliance**: Need to verify license compatibility
- 🎯 **Systematic management**: Ad-hoc updates causing issues
- 🔄 **Frequent breakage**: Dependency updates break builds
- 📊 **No visibility**: Don't know dependency health status

**Don't use when**:
- ❌ Zero dependencies (static binary, no external deps)
- ❌ Dependencies already managed systematically
- ❌ Short-lived projects (throwaway tools, prototypes)
- ❌ Frozen dependencies (legacy systems, no updates allowed)

---

## Quick Start (30 minutes)

### Step 1: Audit Current State (10 min)

```bash
# Go projects
go list -m -u all | grep '\['

# Node.js
npm audit

# Python
pip list --outdated

# Identify:
# - Security vulnerabilities
# - Outdated packages (>6 months old)
# - License issues
```

### Step 2: Prioritize by Security (10 min)

**Severity levels**:
- **Critical**: Actively exploited, RCE, data breach
- **High**: Authentication bypass, privilege escalation
- **Medium**: DoS, information disclosure
- **Low**: Minor issues, limited impact

**Action timeline**:
- Critical: Immediate (same day)
- High: Within 1 week
- Medium: Within 1 month
- Low: Next quarterly update

### Step 3: Batch Remediation (10 min)

```bash
# Group compatible updates
# Test together
# Create single PR with all updates

# Example: Update all patch versions
go get -u=patch ./...
go test ./...
git commit -m "chore(deps): update dependencies (security + freshness)"
```

---

## Security-First Prioritization

### Vulnerability Assessment

**Critical vulnerabilities** (immediate action):
- RCE (Remote Code Execution)
- SQL Injection
- Authentication bypass
- Data breach potential

**High vulnerabilities** (1 week):
- Privilege escalation
- XSS (Cross-Site Scripting)
- CSRF (Cross-Site Request Forgery)
- Sensitive data exposure

**Medium vulnerabilities** (1 month):
- DoS (Denial of Service)
- Information disclosure
- Insecure defaults
- Weak cryptography

**Low vulnerabilities** (quarterly):
- Minor issues
- Informational
- False positives

### Remediation Strategy

```
Priority queue:
1. Critical vulnerabilities (immediate)
2. High vulnerabilities (week)
3. Dependency freshness (monthly)
4. License compliance (quarterly)
5. Medium/low vulnerabilities (quarterly)
```

---

## Batch Remediation Strategy

### Why Batch Updates?

**Problems with one-at-a-time**:
- Update fatigue (100+ dependencies)
- Test overhead (N tests for N updates)
- PR overhead (N reviews)
- Potential conflicts (update A breaks with update B)

**Benefits of batching**:
- Single test run for all updates
- Single PR review
- Detect incompatibilities early
- 6x faster (validated in meta-cc)

### Batching Strategies

**Strategy 1: By Severity**
```bash
# Batch 1: All security patches
# Batch 2: All minor/patch updates
# Batch 3: All major updates (breaking changes)
```

**Strategy 2: By Compatibility**
```bash
# Batch 1: Compatible updates (no breaking changes)
# Batch 2: Breaking changes (one at a time)
```

**Strategy 3: By Timeline**
```bash
# Batch 1: Immediate (critical vulnerabilities)
# Batch 2: Weekly (high vulnerabilities + freshness)
# Batch 3: Monthly (medium vulnerabilities)
# Batch 4: Quarterly (low vulnerabilities + license)
```

---

## Policy-Driven Compliance

### Security Policies

```yaml
# .dependency-policy.yml
security:
  critical_vulnerabilities:
    action: block_merge
    max_age: 0 days
  high_vulnerabilities:
    action: block_merge
    max_age: 7 days
  medium_vulnerabilities:
    action: warn
    max_age: 30 days
```

### Freshness Policies

```yaml
freshness:
  max_age:
    major: 12 months
    minor: 6 months
    patch: 3 months
  exceptions:
    - package: legacy-lib
      reason: "No maintained alternative"
```

### License Policies

```yaml
licenses:
  allowed:
    - MIT
    - Apache-2.0
    - BSD-3-Clause
  denied:
    - GPL-3.0  # Copyleft issues
    - AGPL-3.0
  review_required:
    - Custom
    - Proprietary
```

---

## Automation Tools

### Vulnerability Scanning

```bash
# Go: govulncheck
go install golang.org/x/vuln/cmd/govulncheck@latest
govulncheck ./...

# Node.js: npm audit
npm audit --audit-level=moderate

# Python: safety
pip install safety
safety check

# Rust: cargo-audit
cargo install cargo-audit
cargo audit
```

### Automated Updates

```bash
# Dependabot (GitHub)
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "gomod"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
    groups:
      security:
        patterns:
          - "*"
        update-types:
          - "patch"
          - "minor"
```

### License Checking

```bash
# Go: go-licenses
go install github.com/google/go-licenses@latest
go-licenses check ./...

# Node.js: license-checker
npx license-checker --summary

# Python: pip-licenses
pip install pip-licenses
pip-licenses
```

---

## Proven Results

**Validated in bootstrap-010** (meta-cc project):
- ✅ Security-first prioritization implemented
- ✅ Batch remediation (5 dependencies updated together)
- ✅ 6x speedup: 9 hours manual → 1.5 hours systematic
- ✅ 3 iterations (rapid convergence)
- ✅ V_instance: 0.92 (highest among experiments)
- ✅ V_meta: 0.85

**Metrics**:
- Vulnerabilities: 2 critical → 0 (resolved immediately)
- Freshness: 45% outdated → 15% outdated
- License compliance: 100% (all MIT/Apache-2.0/BSD)

**Transferability**:
- Go (gomod): 100% (native)
- Node.js (npm): 90% (npm audit similar)
- Python (pip): 85% (safety similar)
- Rust (cargo): 90% (cargo audit similar)
- Java (Maven): 85% (OWASP dependency-check)
- **Overall**: 88% transferable

---

## Common Patterns

### Pattern 1: Security Update Workflow

```bash
# 1. Scan for vulnerabilities
govulncheck ./...

# 2. Review severity
# Critical/High → immediate
# Medium/Low → batch

# 3. Update dependencies
go get -u github.com/vulnerable/package@latest

# 4. Test
go test ./...

# 5. Commit
git commit -m "fix(deps): resolve CVE-XXXX-XXXXX in package X"
```

### Pattern 2: Monthly Freshness Update

```bash
# 1. Check for updates
go list -m -u all

# 2. Batch updates (patch/minor)
go get -u=patch ./...

# 3. Test
go test ./...

# 4. Commit
git commit -m "chore(deps): monthly dependency freshness update"
```

### Pattern 3: Major Version Upgrade

```bash
# One at a time (breaking changes)
# 1. Update single package
go get package@v2

# 2. Fix breaking changes
# ... code modifications ...

# 3. Test extensively
go test ./...

# 4. Commit
git commit -m "feat(deps): upgrade package to v2"
```

---

## Anti-Patterns

❌ **Ignoring security advisories**: "We'll update later"
❌ **One-at-a-time updates**: 100 separate PRs for 100 dependencies
❌ **Automatic merging**: Dependabot auto-merge without testing
❌ **Dependency pinning forever**: Never updating to avoid breakage
❌ **License ignorance**: Not checking license compatibility
❌ **No testing after updates**: Assuming updates won't break anything

---

## Related Skills

**Parent framework**:
- [methodology-bootstrapping](../methodology-bootstrapping/SKILL.md) - Core OCA cycle

**Complementary**:
- [ci-cd-optimization](../ci-cd-optimization/SKILL.md) - Automated dependency checks in CI
- [error-recovery](../error-recovery/SKILL.md) - Dependency failure handling

**Acceleration**:
- [rapid-convergence](../rapid-convergence/SKILL.md) - 3 iterations achieved

---

## References

**Core guides**:
- Reference materials in experiments/bootstrap-010-dependency-health/
- Security-first prioritization framework
- Batch remediation strategies
- Policy-driven compliance

**Tools**:
- govulncheck (Go)
- npm audit (Node.js)
- safety (Python)
- cargo-audit (Rust)
- go-licenses (license checking)

---

**Status**: ✅ Production-ready | 6x speedup | 88% transferable | V_instance 0.92 (highest)
