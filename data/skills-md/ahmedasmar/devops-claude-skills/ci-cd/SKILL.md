---
name: ci-cd
description: CI/CD pipeline design, optimization, DevSecOps security scanning, and troubleshooting. Use for creating workflows, debugging pipeline failures, implementing SAST/DAST/SCA, optimizing build performance, implementing caching strategies, setting up deployments, securing pipelines with OIDC/secrets management, and troubleshooting common issues across GitHub Actions, GitLab CI, and other platforms.
---

# CI/CD Pipelines

Comprehensive guide for CI/CD pipeline design, optimization, security, and troubleshooting across GitHub Actions, GitLab CI, and other platforms.

## When to Use This Skill

Use this skill when:
- Creating new CI/CD workflows or pipelines
- Debugging pipeline failures or flaky tests
- Optimizing slow builds or test suites
- Implementing caching strategies
- Setting up deployment workflows
- Securing pipelines (secrets, OIDC, supply chain)
- Implementing DevSecOps security scanning (SAST, DAST, SCA)
- Troubleshooting platform-specific issues
- Analyzing pipeline performance
- Implementing matrix builds or test sharding
- Configuring multi-environment deployments

## Core Workflows

### 1. Creating a New Pipeline

**Decision tree:**
```
What are you building?
├── Node.js/Frontend → GitHub: templates/github-actions/node-ci.yml | GitLab: templates/gitlab-ci/node-ci.yml
├── Python → GitHub: templates/github-actions/python-ci.yml | GitLab: templates/gitlab-ci/python-ci.yml
├── Go → GitHub: templates/github-actions/go-ci.yml | GitLab: templates/gitlab-ci/go-ci.yml
├── Docker Image → GitHub: templates/github-actions/docker-build.yml | GitLab: templates/gitlab-ci/docker-build.yml
├── Other → Follow the pipeline design pattern below
```

**Basic pipeline structure:**
```yaml
# 1. Fast feedback (lint, format) - <1 min
# 2. Unit tests - 1-5 min
# 3. Integration tests - 5-15 min
# 4. Build artifacts
# 5. E2E tests (optional, main branch only) - 15-30 min
# 6. Deploy (with approval gates)
```

**Key principles:**
- Fail fast: Run cheap validation first
- Parallelize: Remove unnecessary job dependencies
- Cache dependencies: Use `actions/cache` or GitLab cache
- Use artifacts: Build once, deploy many times

See [best_practices.md](references/best_practices.md) for comprehensive pipeline design patterns.

### 2. Optimizing Pipeline Performance

**Quick wins checklist:**
- [ ] Add dependency caching (50-90% faster builds)
- [ ] Remove unnecessary `needs` dependencies
- [ ] Add path filters to skip unnecessary runs
- [ ] Use `npm ci` instead of `npm install`
- [ ] Add job timeouts to prevent hung builds
- [ ] Enable concurrency cancellation for duplicate runs

**Analyze existing pipeline:**
```bash
# Use the pipeline analyzer script
python3 scripts/pipeline_analyzer.py --platform github --workflow .github/workflows/ci.yml
```

**Common optimizations:**
- **Slow tests:** Shard tests with matrix builds
- **Repeated dependency installs:** Add caching
- **Sequential jobs:** Parallelize with proper `needs`
- **Full test suite on every PR:** Use path filters or test impact analysis

See [optimization.md](references/optimization.md) for detailed caching strategies, parallelization techniques, and performance tuning.

### 3. Securing Your Pipeline

**Essential security checklist:**
- [ ] Use OIDC instead of static credentials
- [ ] Pin actions/includes to commit SHAs
- [ ] Use minimal permissions
- [ ] Enable secret scanning
- [ ] Add vulnerability scanning (dependencies, containers)
- [ ] Implement branch protection
- [ ] Separate test from deploy workflows

**Quick setup - OIDC authentication:**

**GitHub Actions → AWS:**
```yaml
permissions:
  id-token: write
  contents: read

steps:
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::123456789:role/GitHubActionsRole
      aws-region: us-east-1
```

**Secrets management:**
- Store in platform secret stores (GitHub Secrets, GitLab CI/CD Variables)
- Mark as "masked" in GitLab
- Use environment-specific secrets
- Rotate regularly (every 90 days)
- Never log secrets

See [security.md](references/security.md) for comprehensive security patterns, supply chain security, and secrets management.

### 4. Troubleshooting Pipeline Failures

**Systematic approach:**

**Step 1: Check pipeline health**
```bash
python3 scripts/ci_health.py --platform github --repo owner/repo
```

**Step 2: Identify the failure type**

| Error Pattern | Common Cause | Quick Fix |
|---------------|--------------|-----------|
| "Module not found" | Missing dependency or cache issue | Clear cache, run `npm ci` |
| "Timeout" | Job taking too long | Add caching, increase timeout |
| "Permission denied" | Missing permissions | Add to `permissions:` block |
| "Cannot connect to Docker daemon" | Docker not available | Use correct runner or DinD |
| Intermittent failures | Flaky tests or race conditions | Add retries, fix timing issues |

**Step 3: Enable debug logging**

GitHub Actions:
```yaml
# Add repository secrets:
# ACTIONS_RUNNER_DEBUG = true
# ACTIONS_STEP_DEBUG = true
```

GitLab CI:
```yaml
variables:
  CI_DEBUG_TRACE: "true"
```

**Step 4: Reproduce locally**
```bash
# GitHub Actions - use act
act -j build

# Or Docker
docker run -it ubuntu:latest bash
# Then manually run the failing steps
```

See [troubleshooting.md](references/troubleshooting.md) for comprehensive issue diagnosis, platform-specific problems, and solutions.

### 5. Implementing Deployment Workflows

**Deployment pattern selection:**

| Pattern | Use Case | Complexity | Risk |
|---------|----------|------------|------|
| Direct | Simple apps, low traffic | Low | Medium |
| Blue-Green | Zero downtime required | Medium | Low |
| Canary | Gradual rollout, monitoring | High | Very Low |
| Rolling | Kubernetes, containers | Medium | Low |

**Basic deployment structure:**
```yaml
deploy:
  needs: [build, test]
  if: github.ref == 'refs/heads/main'
  environment:
    name: production
    url: https://example.com
  steps:
    - name: Download artifacts
    - name: Deploy
    - name: Health check
    - name: Rollback on failure
```

**Multi-environment setup:**
- **Development:** Auto-deploy on develop branch
- **Staging:** Auto-deploy on main, requires passing tests
- **Production:** Manual approval required, smoke tests mandatory

See [best_practices.md](references/best_practices.md#deployment-strategies) for detailed deployment patterns and environment management.

### 6. Implementing DevSecOps Security Scanning

**Security scanning types:**

| Scan Type | Purpose | When to Run | Speed | Tools |
|-----------|---------|-------------|-------|-------|
| Secret Scanning | Find exposed credentials | Every commit | Fast (<1 min) | TruffleHog, Gitleaks |
| SAST | Find code vulnerabilities | Every commit | Medium (5-15 min) | CodeQL, Semgrep, Bandit, Gosec |
| SCA | Find dependency vulnerabilities | Every commit | Fast (1-5 min) | npm audit, pip-audit, Snyk |
| Container Scanning | Find image vulnerabilities | After build | Medium (5-10 min) | Trivy, Grype |
| DAST | Find runtime vulnerabilities | Scheduled/main only | Slow (15-60 min) | OWASP ZAP |

**Quick setup - Add security to existing pipeline:**

**GitHub Actions:**
```yaml
jobs:
  # Add before build job
  secret-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: trufflesecurity/trufflehog@main
      - uses: gitleaks/gitleaks-action@v2

  sast:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v3
        with:
          languages: javascript  # or python, go
      - uses: github/codeql-action/analyze@v3

  build:
    needs: [secret-scan, sast]  # Add dependencies
```

**GitLab CI:**
```yaml
stages:
  - security  # Add before other stages
  - build
  - test

# Secret scanning
secret-scan:
  stage: security
  image: trufflesecurity/trufflehog:latest
  script:
    - trufflehog filesystem . --json --fail

# SAST
sast:semgrep:
  stage: security
  image: returntocorp/semgrep
  script:
    - semgrep scan --config=auto .

# Use GitLab templates
include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Dependency-Scanning.gitlab-ci.yml
```

**Comprehensive security pipeline templates:**
- **GitHub Actions:** `templates/github-actions/security-scan.yml` - Complete DevSecOps pipeline with all scanning stages
- **GitLab CI:** `templates/gitlab-ci/security-scan.yml` - Complete DevSecOps pipeline with GitLab security templates

**Security gate pattern:**

Add a security gate job that evaluates all security scan results and fails the pipeline if critical issues are found:

```yaml
security-gate:
  needs: [secret-scan, sast, sca, container-scan]
  script:
    # Check for critical vulnerabilities
    # Parse JSON reports and evaluate thresholds
    # Fail if critical issues found
```

**Language-specific security tools:**

- **Node.js:** CodeQL, Semgrep, npm audit, eslint-plugin-security
- **Python:** CodeQL, Semgrep, Bandit, pip-audit, Safety
- **Go:** CodeQL, Semgrep, Gosec, govulncheck

All language-specific templates now include security scanning stages. See:
- `templates/github-actions/node-ci.yml`
- `templates/github-actions/python-ci.yml`
- `templates/github-actions/go-ci.yml`
- `templates/gitlab-ci/node-ci.yml`
- `templates/gitlab-ci/python-ci.yml`
- `templates/gitlab-ci/go-ci.yml`

See [devsecops.md](references/devsecops.md) for comprehensive DevSecOps guide covering all security scanning types, tool comparisons, and implementation patterns.

## Quick Reference Commands

### GitHub Actions

```bash
# List workflows
gh workflow list

# View recent runs
gh run list --limit 20

# View specific run
gh run view <run-id>

# Re-run failed jobs
gh run rerun <run-id> --failed

# Download logs
gh run view <run-id> --log > logs.txt

# Trigger workflow manually
gh workflow run ci.yml

# Check workflow status
gh run watch
```

### GitLab CI

```bash
# View pipelines
gl project-pipelines list

# Pipeline status
gl project-pipeline get <pipeline-id>

# Retry failed jobs
gl project-pipeline retry <pipeline-id>

# Cancel pipeline
gl project-pipeline cancel <pipeline-id>

# Download artifacts
gl project-job artifacts <job-id>
```

## Platform-Specific Patterns

### GitHub Actions

**Reusable workflows:**
```yaml
# .github/workflows/reusable-test.yml
on:
  workflow_call:
    inputs:
      node-version:
        required: true
        type: string

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
```

**Call from another workflow:**
```yaml
jobs:
  test:
    uses: ./.github/workflows/reusable-test.yml
    with:
      node-version: '20'
```

### GitLab CI

**Templates with extends:**
```yaml
.test_template:
  image: node:20
  before_script:
    - npm ci

unit-test:
  extends: .test_template
  script:
    - npm run test:unit

integration-test:
  extends: .test_template
  script:
    - npm run test:integration
```

**DAG pipelines with needs:**
```yaml
build:
  stage: build

test:unit:
  stage: test
  needs: [build]

test:integration:
  stage: test
  needs: [build]

deploy:
  stage: deploy
  needs: [test:unit, test:integration]
```

## Diagnostic Scripts

### Pipeline Analyzer

Analyzes workflow configuration for optimization opportunities:

```bash
# GitHub Actions
python3 scripts/pipeline_analyzer.py --platform github --workflow .github/workflows/ci.yml

# GitLab CI
python3 scripts/pipeline_analyzer.py --platform gitlab --config .gitlab-ci.yml
```

**Identifies:**
- Missing caching opportunities
- Unnecessary sequential execution
- Outdated action versions
- Unused artifacts
- Overly broad triggers

### CI Health Checker

Checks pipeline status and identifies issues:

```bash
# GitHub Actions
python3 scripts/ci_health.py --platform github --repo owner/repo --limit 20

# GitLab CI
python3 scripts/ci_health.py --platform gitlab --project-id 12345 --token $GITLAB_TOKEN
```

**Provides:**
- Success/failure rates
- Recent failure patterns
- Workflow-specific insights
- Actionable recommendations

## Reference Documentation

For deep-dive information on specific topics:

- **[best_practices.md](references/best_practices.md)** - Pipeline design, testing strategies, deployment patterns, dependency management, artifact handling, platform-specific patterns
- **[security.md](references/security.md)** - Secrets management, OIDC authentication, supply chain security, access control, vulnerability scanning, secure pipeline patterns
- **[devsecops.md](references/devsecops.md)** - Comprehensive DevSecOps guide: SAST (CodeQL, Semgrep, Bandit, Gosec), DAST (OWASP ZAP), SCA (npm audit, pip-audit, Snyk), container security (Trivy, Grype, SBOM), secret scanning (TruffleHog, Gitleaks), security gates, license compliance
- **[optimization.md](references/optimization.md)** - Caching strategies (dependencies, Docker layers, build artifacts), parallelization techniques, test splitting, build optimization, resource management
- **[troubleshooting.md](references/troubleshooting.md)** - Common issues (workflow not triggering, flaky tests, timeouts, dependency errors), Docker problems, authentication issues, platform-specific debugging

## Templates

Starter templates for common use cases:

### GitHub Actions
- **`assets/templates/github-actions/node-ci.yml`** - Complete Node.js CI/CD with security scanning, caching, matrix testing, and multi-environment deployment
- **`assets/templates/github-actions/python-ci.yml`** - Python pipeline with security scanning, pytest, coverage, PyPI deployment
- **`assets/templates/github-actions/go-ci.yml`** - Go pipeline with security scanning, multi-platform builds, benchmarks, integration tests
- **`assets/templates/github-actions/docker-build.yml`** - Docker build with multi-platform support, security scanning, SBOM generation, and signing
- **`assets/templates/github-actions/security-scan.yml`** - Comprehensive DevSecOps pipeline with SAST, DAST, SCA, container scanning, and security gates

### GitLab CI
- **`assets/templates/gitlab-ci/node-ci.yml`** - GitLab CI pipeline with security scanning, parallel execution, services, and deployment stages
- **`assets/templates/gitlab-ci/python-ci.yml`** - Python pipeline with security scanning, parallel testing, Docker builds, PyPI and Cloud Run deployment
- **`assets/templates/gitlab-ci/go-ci.yml`** - Go pipeline with security scanning, multi-platform builds, benchmarks, Kubernetes deployment
- **`assets/templates/gitlab-ci/docker-build.yml`** - Docker build with DinD, multi-arch, Container Registry, security scanning
- **`assets/templates/gitlab-ci/security-scan.yml`** - Comprehensive DevSecOps pipeline with SAST, DAST, SCA, container scanning, GitLab security templates, and security gates

## Common Patterns

### Caching Dependencies

**GitHub Actions:**
```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
- run: npm ci
```

**GitLab CI:**
```yaml
cache:
  key:
    files:
      - package-lock.json
  paths:
    - node_modules/
```

### Matrix Builds

**GitHub Actions:**
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, macos-latest]
    node: [18, 20, 22]
  fail-fast: false
```

**GitLab CI:**
```yaml
test:
  parallel:
    matrix:
      - NODE_VERSION: ['18', '20', '22']
```

### Conditional Execution

**GitHub Actions:**
```yaml
- name: Deploy
  if: github.ref == 'refs/heads/main' && github.event_name == 'push'
```

**GitLab CI:**
```yaml
deploy:
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
      when: manual
```

## Best Practices Summary

**Performance:**
- Enable dependency caching
- Parallelize independent jobs
- Add path filters to reduce unnecessary runs
- Use matrix builds for cross-platform testing

**Security:**
- Use OIDC for cloud authentication
- Pin actions to commit SHAs
- Enable secret scanning and vulnerability checks
- Apply principle of least privilege

**Reliability:**
- Add timeouts to prevent hung jobs
- Implement retry logic for flaky operations
- Use health checks after deployments
- Enable concurrency cancellation

**Maintainability:**
- Use reusable workflows/templates
- Document non-obvious decisions
- Keep workflows DRY with extends/includes
- Regular dependency updates

## Getting Started

1. **New pipeline:** Start with a template from `assets/templates/`
2. **Add security scanning:** Use DevSecOps templates or add security stages to existing pipelines (see workflow 6 above)
3. **Optimize existing:** Run `scripts/pipeline_analyzer.py`
4. **Debug issues:** Check `references/troubleshooting.md`
5. **Improve security:** Review `references/security.md` and `references/devsecops.md` checklists
6. **Speed up builds:** See `references/optimization.md`
