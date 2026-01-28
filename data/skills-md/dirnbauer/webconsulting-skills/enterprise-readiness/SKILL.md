---
name: enterprise-readiness
description: Assess and enhance software projects for enterprise-grade security, quality, and automation. Aligned with OpenSSF Scorecard, SLSA, and S2C2F.
version: 1.0.0
triggers:
  - enterprise
  - openssf
  - slsa
  - security
  - scorecard
  - supply chain
  - badge
---

# Enterprise Readiness Assessment

Assess and enhance software projects for enterprise-grade security, quality, and automation.

## When to Use

- Evaluating projects for production/enterprise readiness
- Implementing supply chain security (SLSA, signing, SBOMs)
- Hardening CI/CD pipelines
- Establishing quality gates
- Pursuing OpenSSF Best Practices Badge (Passing/Silver/Gold)

## Assessment Workflow

1. **Discovery**: Identify platform (GitHub/GitLab), languages, existing CI/CD
2. **Scoring**: Apply checklists based on stack
3. **Badge Assessment**: Check OpenSSF criteria status
4. **Gap Analysis**: List missing controls by severity
5. **Implementation**: Apply fixes using templates

## Scoring System

### Base Score (0-100 points)

| Category | Max Points | Focus Areas |
|----------|------------|-------------|
| Universal Controls | 60 | License, SECURITY.md, branch protection, CI |
| Platform-Specific | 40 | GitHub/GitLab specific features |
| Language-Specific | 20 | Go, PHP, JS specific tooling |

### Severity Levels

| Level | Impact | Priority |
|-------|--------|----------|
| Critical | Security vulnerability, compliance blocker | Immediate |
| High | Major quality issue, missing automation | This sprint |
| Medium | Best practice gap, technical debt | This quarter |
| Low | Nice-to-have improvement | Backlog |

## Universal Controls Checklist (60 pts)

### Repository Basics (15 pts)
- [ ] `LICENSE` file present (SPDX identifier)
- [ ] `README.md` with project description
- [ ] `CONTRIBUTING.md` with contribution guidelines
- [ ] `CODE_OF_CONDUCT.md` (Contributor Covenant)
- [ ] `SECURITY.md` with vulnerability reporting process

### Branch Protection (15 pts)
- [ ] Default branch protected
- [ ] Require pull request reviews (1+ reviewers)
- [ ] Require status checks before merging
- [ ] Require signed commits (GPG/SSH)
- [ ] No force pushes to protected branches

### CI/CD Pipeline (15 pts)
- [ ] Automated tests on every PR
- [ ] Linting and static analysis
- [ ] Dependency vulnerability scanning
- [ ] Build verification
- [ ] Coverage reporting

### Security Practices (15 pts)
- [ ] Dependabot or Renovate enabled
- [ ] Secret scanning enabled
- [ ] CodeQL or similar SAST
- [ ] No secrets in repository
- [ ] Signed releases

## GitHub-Specific Controls (40 pts)

### Security Features
- [ ] Secret scanning enabled
- [ ] Push protection enabled
- [ ] Dependabot security updates
- [ ] CodeQL analysis
- [ ] Private vulnerability reporting

### Actions Security
- [ ] Actions pinned by SHA (not tag)
- [ ] Minimal permissions (least privilege)
- [ ] No `pull_request_target` with untrusted input
- [ ] GITHUB_TOKEN scoped appropriately

### Example: Secure Action Reference

```yaml
# ❌ INSECURE - Tag can be moved
- uses: actions/checkout@v4

# ✅ SECURE - SHA-pinned with version comment
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1
```

## OpenSSF Best Practices Badge

### Passing Level Requirements

| Criterion | Requirement |
|-----------|-------------|
| Basics | LICENSE, documentation, build instructions |
| Change Control | Version control, unique versioning |
| Reporting | Public issue tracker, vulnerability reporting |
| Quality | Working build, automated tests |
| Security | No unaddressed vulnerabilities, secure development |

### Silver Level Requirements

All Passing criteria plus:
- [ ] DCO or CLA for contributions
- [ ] Detailed documentation (ARCHITECTURE.md)
- [ ] Code review required for changes
- [ ] 80%+ statement coverage
- [ ] Test policy documented

### Gold Level Requirements

All Silver criteria plus:
- [ ] Multiple security-knowledgeable reviewers
- [ ] Dynamic analysis (fuzzing)
- [ ] 80%+ branch coverage
- [ ] Security audit completed
- [ ] Reproducible builds

## SLSA Framework

### SLSA Levels

| Level | Requirements |
|-------|--------------|
| SLSA 1 | Documented build process |
| SLSA 2 | Hosted build, signed provenance |
| SLSA 3 | Hardened builds, non-falsifiable provenance |
| SLSA 4 | Two-person review, hermetic builds |

### GitHub Actions SLSA Provenance

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

permissions:
  contents: write
  id-token: write
  attestations: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1
      
      - name: Build
        run: make build
        
      - name: Generate SLSA Provenance
        uses: slsa-framework/slsa-github-generator/.github/workflows/generator_generic_slsa3.yml@v1.9.0
        with:
          base64-subjects: ${{ steps.hash.outputs.hashes }}
```

## Signed Releases

### Cosign (Containers)

```bash
# Sign container image
cosign sign --key cosign.key myregistry/myimage:v1.0.0

# Verify signature
cosign verify --key cosign.pub myregistry/myimage:v1.0.0
```

### GPG (Git Tags)

```bash
# Sign tag
git tag -s v1.0.0 -m "Release v1.0.0"

# Verify tag
git tag -v v1.0.0
```

## Software Bill of Materials (SBOM)

### Generate SBOM

```bash
# Using Syft
syft packages . -o spdx-json > sbom.spdx.json

# Using CycloneDX for PHP
composer require --dev cyclonedx/cyclonedx-php-composer
composer make-bom
```

### SBOM in CI

```yaml
- name: Generate SBOM
  uses: anchore/sbom-action@v0
  with:
    artifact-name: sbom.spdx.json
```

## Security Hardening

### Content Security

```yaml
# _headers or .htaccess
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

### Input Validation

```php
// ✅ SECURE - Validate and sanitize all input
$email = filter_var($input, FILTER_VALIDATE_EMAIL);
if ($email === false) {
    throw new ValidationException('Invalid email');
}
```

## CI Workflow Templates

### OpenSSF Scorecard

```yaml
# .github/workflows/scorecard.yml
name: OpenSSF Scorecard

on:
  schedule:
    - cron: '0 0 * * 0'
  push:
    branches: [main]

permissions:
  security-events: write
  id-token: write

jobs:
  analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1
        with:
          persist-credentials: false
          
      - uses: ossf/scorecard-action@v2.3.1
        with:
          results_file: results.sarif
          results_format: sarif
          publish_results: true
```

### Dependency Review

```yaml
# .github/workflows/dependency-review.yml
name: Dependency Review

on: pull_request

permissions:
  contents: read
  pull-requests: write

jobs:
  dependency-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1
      - uses: actions/dependency-review-action@v4
        with:
          fail-on-severity: high
          deny-licenses: GPL-3.0, AGPL-3.0
```

## Score Interpretation

| Score | Grade | Status |
|-------|-------|--------|
| 90-100+ | A | Enterprise Ready |
| 80-89 | B | Production Ready |
| 70-79 | C | Development Ready |
| 60-69 | D | Basic |
| <60 | F | Not Ready |

## Critical Rules

- **NEVER** interpolate `${{ github.event.* }}` in `run:` blocks (script injection)
- **NEVER** guess action versions - fetch from GitHub API or documentation
- **ALWAYS** use SHA pins for actions with version comments
- **ALWAYS** verify commit hashes against official tags
- **NEVER** store secrets in code or commit history

## Resources

- [OpenSSF Scorecard](https://securityscorecards.dev/)
- [Best Practices Badge](https://www.bestpractices.dev/)
- [SLSA Framework](https://slsa.dev/)
- [S2C2F](https://github.com/ossf/s2c2f)
- [Sigstore](https://sigstore.dev/)

---

## Credits & Attribution

This skill is based on the excellent work by
**[Netresearch DTT GmbH](https://www.netresearch.de/)**.

Original repository: https://github.com/netresearch/enterprise-readiness-skill

**Copyright (c) Netresearch DTT GmbH** - Methodology and best practices  
Adapted by webconsulting.at for this skill collection
