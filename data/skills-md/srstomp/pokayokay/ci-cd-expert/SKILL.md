---
name: ci-cd-expert
description: Create, review, debug, and optimize CI/CD pipelines across platforms. Covers GitHub Actions, GitLab CI, CircleCI, Azure DevOps, and Bitbucket Pipelines. Use this skill when creating new pipelines, debugging failing builds, implementing deployment strategies (blue-green, canary, rolling), reviewing pipelines for security and efficiency, or optimizing build times. Triggers on "ci", "cd", "pipeline", "deployment", "github actions", "gitlab ci", "workflow", "build failing", "deploy to staging/production".
---

# CI/CD Expert

Create, debug, and optimize CI/CD pipelines.

## Platform Selection

| Platform | Best For | Key Strength |
|----------|----------|--------------|
| **GitHub Actions** | GitHub-hosted repos, open source | Native GitHub integration, marketplace |
| **GitLab CI** | GitLab repos, self-hosted | Built-in registry, Auto DevOps |
| **CircleCI** | Complex workflows, speed | Parallelism, orbs ecosystem |
| **Azure DevOps** | Microsoft/enterprise, multi-repo | Azure integration, YAML templates |
| **Bitbucket** | Atlassian stack, Jira integration | Pipes marketplace, deployments |

**Quick pick:**
- GitHub repo? → GitHub Actions
- GitLab repo? → GitLab CI
- Need extreme parallelism? → CircleCI
- Azure/Microsoft shop? → Azure DevOps
- Using Jira/Confluence? → Bitbucket Pipelines

## Core Workflows

### 1. Pipeline Creation

```
Requirements → Platform Selection → Structure → Implementation → Validation
```

**Steps:**
1. Identify triggers (push, PR, schedule, manual)
2. Define stages (build, test, deploy)
3. Map environments (dev, staging, prod)
4. Configure secrets and variables
5. Set up caching strategy
6. Implement deployment gates

**Minimal viable pipeline:**
```yaml
# Every pipeline needs these elements
triggers:        # When to run
stages:          # What to run (in order)
  - build        # Compile/bundle
  - test         # Validate
  - deploy       # Ship (optional)
caching:         # Speed optimization
environment:     # Secrets/variables
```

### 2. Pipeline Review

**Review checklist (in order of priority):**

1. **Security**
   - [ ] Secrets not hardcoded
   - [ ] Minimal permissions (least privilege)
   - [ ] Dependencies pinned (no `@latest`)
   - [ ] Untrusted input sanitized

2. **Reliability**
   - [ ] Idempotent steps
   - [ ] Explicit failure handling
   - [ ] Timeouts configured
   - [ ] Retry logic for flaky steps

3. **Efficiency**
   - [ ] Caching implemented
   - [ ] Parallelization where possible
   - [ ] Conditional execution (skip unchanged)
   - [ ] Resource sizing appropriate

4. **Maintainability**
   - [ ] DRY (reusable workflows/templates)
   - [ ] Clear naming conventions
   - [ ] Comments on non-obvious logic

### 3. Pipeline Debugging

**Diagnostic framework:**

```
Symptom → Category → Platform-specific fix
```

**Common failure categories:**

| Symptom | Likely Cause | First Check |
|---------|--------------|-------------|
| "Command not found" | Missing dependency | Environment setup |
| "Permission denied" | File/secret access | Permissions config |
| "Connection refused" | Service not ready | Health checks, wait |
| "Out of memory" | Resource limits | Runner sizing |
| "Timeout exceeded" | Slow step or deadlock | Step isolation |
| "Exit code 1" | Script failure | Run locally first |

**Debug approach:**
1. Read the full error (scroll up!)
2. Identify which step failed
3. Check if it works locally
4. Add debug output (`set -x`, verbose flags)
5. Check platform-specific logs

### 4. Deployment Strategy Selection

```
                     Risk Tolerance
                          ↑
                    Low   │   High
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
 Slow   │   Blue-Green    │    Rolling      │  Fast
        │   (safest)      │   (balanced)    │
        │                 │                 │
        ├─────────────────┼─────────────────┤
        │                 │                 │
        │    Canary       │   Direct        │
        │   (measured)    │   (fastest)     │
        │                 │                 │
        └─────────────────┴─────────────────┘
                     Rollback Speed →
```

**Decision guide:**

| Strategy | Use When | Avoid When |
|----------|----------|------------|
| **Blue-Green** | Zero downtime critical, simple rollback needed | Limited infrastructure budget |
| **Canary** | Need to validate with real traffic, gradual rollout | Urgent hotfix, no traffic splitting |
| **Rolling** | Large clusters, cost-conscious | Stateful apps, breaking changes |
| **Direct** | Dev/test environments, low risk | Production, user-facing services |

### 5. Build Optimization

**Optimization priority:**
1. Caching (highest impact)
2. Parallelization
3. Conditional execution
4. Resource sizing
5. Image optimization

**Caching hierarchy:**
```
Dependencies (npm, pip) → Build artifacts → Docker layers → Test fixtures
       ↑                        ↑                ↑              ↑
   Always cache          If build slow     If using Docker   If tests slow
```

**Cache key strategies:**
```yaml
# Dependencies - hash lockfile
key: deps-${{ hashFiles('package-lock.json') }}

# Build artifacts - hash source
key: build-${{ hashFiles('src/**') }}

# Combined - hash both
key: ${{ runner.os }}-${{ hashFiles('**/lockfiles') }}
```

## Common Patterns

### Secret Management

```yaml
# ✅ Good: Environment variables
env:
  API_KEY: ${{ secrets.API_KEY }}

# ❌ Bad: Inline secrets
run: curl -H "Authorization: hardcoded-secret"
```

**Secret rotation checklist:**
- [ ] Secrets stored in platform secret store
- [ ] Secrets scoped to minimum required (repo/org/env)
- [ ] Rotation procedure documented
- [ ] No secrets in logs (mask sensitive output)

### Environment Progression

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│   Dev   │ →  │Staging  │ →  │   QA    │ →  │  Prod   │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
  Auto          Auto          Manual          Manual
  deploy        deploy        approval        approval
```

### Artifact Management

```yaml
# Upload
- name: Upload build
  uses: actions/upload-artifact@v4
  with:
    name: dist
    path: dist/
    retention-days: 7

# Download (later job)
- name: Download build
  uses: actions/download-artifact@v4
  with:
    name: dist
```

### Matrix Builds

```yaml
# Test across multiple versions
strategy:
  matrix:
    node: [18, 20, 22]
    os: [ubuntu-latest, macos-latest]
  fail-fast: false  # Continue other jobs if one fails
```

## Anti-Patterns

### ❌ Secrets in Logs
```yaml
# BAD
run: echo "Deploying with key $API_KEY"

# GOOD
run: echo "Deploying..." && deploy --key "$API_KEY"
```

### ❌ No Caching
```yaml
# BAD: Downloads deps every run
- run: npm install

# GOOD: Cache node_modules
- uses: actions/cache@v4
  with:
    path: node_modules
    key: ${{ hashFiles('package-lock.json') }}
- run: npm ci
```

### ❌ Mutable Tags
```yaml
# BAD: Could change anytime
uses: actions/checkout@master

# GOOD: Pinned version
uses: actions/checkout@v4
```

### ❌ Overly Broad Triggers
```yaml
# BAD: Runs on every push to every branch
on: push

# GOOD: Specific triggers
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
```

### ❌ Sequential When Parallel Works
```yaml
# BAD: 15 min total
jobs:
  lint:
    ...
  test:
    needs: lint  # Waits for lint
    ...

# GOOD: 10 min total (parallel)
jobs:
  lint:
    ...
  test:
    ...  # Runs alongside lint
```

## Troubleshooting Quick Reference

| Error Pattern | Platform | Solution |
|---------------|----------|----------|
| `EACCES: permission denied` | All | `chmod +x script.sh` or check file ownership |
| `rate limit exceeded` | GitHub | Use `GITHUB_TOKEN`, implement backoff |
| `no space left on device` | All | Clean workspace, use smaller runner |
| `SSL certificate problem` | All | Update CA certs, check proxy settings |
| `container not found` | Docker-based | Check registry auth, image exists |
| `workflow not triggered` | GitHub | Check trigger conditions, branch patterns |
| `job timeout` | All | Increase timeout, optimize slow steps |

## Integration Points

**With version control:**
- Branch protection rules
- Required status checks
- Auto-merge on success

**With deployment targets:**
- Cloud providers (AWS, GCP, Azure)
- Container registries (Docker Hub, ECR, GCR)
- Kubernetes clusters
- Serverless (Lambda, Cloud Functions)

**With monitoring:**
- Build metrics (duration, success rate)
- Deployment tracking
- Error alerting (Slack, PagerDuty)

## Skill Usage

**Creating a pipeline:**
1. Identify platform from repo hosting
2. Read platform-specific reference
3. Follow creation workflow above
4. Validate with platform's linter

**Debugging a failure:**
1. Categorize the error (table above)
2. Read debugging-guide.md for detailed steps
3. Check platform-specific quirks

**Implementing deployments:**
1. Choose strategy using decision guide
2. Read deployment-strategies.md
3. Implement with platform-specific syntax

**Security audit:**
1. Use review checklist above
2. Read security-checklist.md for comprehensive review
3. Generate ohno tasks for findings

---

**References:**
- [references/github-actions.md](references/github-actions.md) — GitHub Actions syntax, patterns, marketplace actions
- [references/gitlab-ci.md](references/gitlab-ci.md) — GitLab CI syntax, Auto DevOps, runners
- [references/circleci.md](references/circleci.md) — CircleCI orbs, parallelism, caching
- [references/azure-devops.md](references/azure-devops.md) — Azure Pipelines, templates, stages
- [references/bitbucket-pipelines.md](references/bitbucket-pipelines.md) — Bitbucket Pipelines, pipes, deployments
- [references/deployment-strategies.md](references/deployment-strategies.md) — Blue-green, canary, rolling implementations
- [references/debugging-guide.md](references/debugging-guide.md) — Platform-specific debugging techniques
- [references/security-checklist.md](references/security-checklist.md) — OWASP CI/CD security, supply chain
