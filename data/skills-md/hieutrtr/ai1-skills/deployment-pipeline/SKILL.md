---
name: deployment-pipeline
description: >-
  Deployment procedures and CI/CD pipeline configuration for Python/React projects. Use
  when deploying to staging or production, creating CI/CD pipelines with GitHub Actions,
  troubleshooting deployment failures, or planning rollbacks. Covers pipeline stages
  (build/test/staging/production), environment promotion, pre-deployment validation,
  health checks, canary deployment, rollback procedures, and GitHub Actions workflows.
  Does NOT cover Docker image building (use docker-best-practices) or incident response
  (use incident-response).
license: MIT
compatibility: 'GitHub Actions, Docker, Python 3.12+, React 18+'
metadata:
  author: platform-team
  version: '1.0.0'
  sdlc-phase: deployment
allowed-tools: Read Edit Write Bash(docker:*) Bash(gh:*) Bash(git:*)
context: fork
---

# Deployment Pipeline

## When to Use

Activate this skill when:
- Setting up or modifying CI/CD pipelines with GitHub Actions
- Deploying application changes to staging or production environments
- Planning environment promotion strategies (dev -> staging -> production)
- Implementing pre-deployment validation gates
- Configuring health checks and smoke tests for deployed services
- Planning or executing rollback procedures after a failed deployment
- Setting up canary or blue-green deployment strategies
- Troubleshooting deployment failures or pipeline errors

Do NOT use this skill for:
- Building or optimizing Docker images (use `docker-best-practices`)
- Responding to production incidents (use `incident-response`)
- Setting up monitoring or alerting (use `monitoring-setup`)
- Infrastructure provisioning (Terraform, CloudFormation)

## Instructions

### Pipeline Stages Overview

Every deployment follows a strict four-stage pipeline. No stage may be skipped.

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────────┐
│  BUILD   │───>│   TEST   │───>│ STAGING  │───>│  PRODUCTION  │
│          │    │          │    │          │    │              │
│ • Lint   │    │ • Unit   │    │ • Deploy │    │ • Canary 10% │
│ • Build  │    │ • Integ  │    │ • Smoke  │    │ • Monitor    │
│ • Image  │    │ • E2E    │    │ • QA     │    │ • Full 100%  │
└──────────┘    └──────────┘    └──────────┘    └──────────────┘
     Gate:           Gate:           Gate:            Gate:
  Build pass     Tests pass     Smoke pass      Health checks
  No lint err    Coverage ≥80%  Manual approve  Error rate <1%
```

### Stage 1: Build

Build stage validates code quality and produces deployable artifacts.

**Steps:**
1. **Lint and format check** -- Run `ruff check` and `ruff format --check` for Python, `eslint` and `prettier --check` for React
2. **Type check** -- Run `mypy` for Python, `tsc --noEmit` for TypeScript
3. **Build artifacts** -- Build Python wheel/sdist, build React production bundle
4. **Build Docker images** -- Tag with git SHA and branch name

**Gate criteria:** All checks pass, images build successfully.

```yaml
# GitHub Actions build stage
build:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Lint Python
      run: ruff check src/ && ruff format --check src/
    - name: Type check Python
      run: mypy src/
    - name: Build backend image
      run: docker build -t app-backend:${{ github.sha }} -f Dockerfile.backend .
    - name: Build frontend
      run: npm ci && npm run build
    - name: Build frontend image
      run: docker build -t app-frontend:${{ github.sha }} -f Dockerfile.frontend .
```

### Stage 2: Test

Run the full test suite. Never skip tests for "urgent" deployments.

**Steps:**
1. **Unit tests** -- `pytest tests/unit/ -v --cov=src --cov-report=xml`
2. **Integration tests** -- `pytest tests/integration/ -v` (requires test database)
3. **Frontend tests** -- `npm test -- --coverage`
4. **E2E tests** -- `npx playwright test` against a test environment
5. **Security scan** -- `pip-audit` for Python, `npm audit` for Node

**Gate criteria:** All tests pass, coverage >= 80%, no critical vulnerabilities.

```yaml
# GitHub Actions test stage
test:
  needs: build
  runs-on: ubuntu-latest
  services:
    postgres:
      image: postgres:16
      env:
        POSTGRES_DB: testdb
        POSTGRES_PASSWORD: testpass
      ports: ['5432:5432']
    redis:
      image: redis:7-alpine
      ports: ['6379:6379']
  steps:
    - uses: actions/checkout@v4
    - name: Run unit tests
      run: pytest tests/unit/ -v --cov=src --cov-report=xml
    - name: Run integration tests
      run: pytest tests/integration/ -v
      env:
        DATABASE_URL: postgresql://postgres:testpass@localhost:5432/testdb
    - name: Check coverage threshold
      run: coverage report --fail-under=80
```

### Stage 3: Staging Deployment

Deploy to staging environment for validation before production.

**Pre-deployment checklist:**
- [ ] All tests pass in CI
- [ ] Database migrations tested with `scripts/migration-dry-run.sh`
- [ ] Environment variables verified for staging
- [ ] Feature flags configured appropriately
- [ ] Dependent services verified available

**Steps:**
1. **Run migration dry-run** -- Validate Alembic migrations against staging DB clone
2. **Deploy to staging** -- Push images, apply migrations, restart services
3. **Run smoke tests** -- Execute `scripts/smoke-test.sh` against staging URL
4. **Run health checks** -- Execute `scripts/health-check.py` for all endpoints
5. **Manual QA** -- Team verifies critical user flows

**Gate criteria:** Smoke tests pass, health checks green, QA sign-off.

### Stage 4: Production Deployment

Production deployment uses canary strategy to minimize risk.

**Canary deployment steps:**
1. **Deploy canary (10% traffic)** -- Route 10% of traffic to new version
2. **Monitor for 10 minutes** -- Watch error rates, latency, resource usage
3. **Evaluate canary** -- If error rate < 1% and p99 latency within 20% of baseline, proceed
4. **Ramp to 50%** -- Increase traffic to 50%, monitor for 5 minutes
5. **Full rollout (100%)** -- Complete the deployment
6. **Post-deployment smoke tests** -- Run full smoke test suite

```
Canary Timeline:
  0 min    10 min   15 min   20 min
  |--------|--------|--------|
  10%      Check    50%      100%
  Deploy   Metrics  Ramp     Full
           OK?      Up       Rollout
           |
           No -> Rollback immediately
```

**Automatic rollback triggers:**
- Error rate exceeds 5% during canary
- p99 latency increases by more than 50%
- Health check failures on canary instances
- Memory usage exceeds 90% threshold

### Pre-Deployment Validation

Run these validations before any deployment. Use `scripts/deploy.sh --validate-only` for a dry run.

**Backend validation:**
```bash
# Verify migrations are consistent
alembic check

# Verify no pending migrations
alembic heads --verbose

# Test migration against staging clone
./skills/deployment-pipeline/scripts/migration-dry-run.sh \
  --db-url "$STAGING_DB_URL" \
  --output-dir ./deploy-validation/

# Verify all dependencies are pinned
pip-compile --dry-run requirements.in
```

**Frontend validation:**
```bash
# Verify build succeeds
npm run build

# Check bundle size limits
npx bundlesize

# Verify environment variables are set
node -e "const vars = ['REACT_APP_API_URL']; vars.forEach(v => { if(!process.env[v]) throw new Error(v + ' not set') })"
```

### Environment Promotion

Strict rules govern how changes move between environments.

| Aspect | Development | Staging | Production |
|--------|-------------|---------|------------|
| Deploy trigger | Push to `main` | Manual or auto after tests | Manual approval required |
| Database | Local PostgreSQL | Staging PostgreSQL | Production PostgreSQL (RDS) |
| Secrets | `.env` file | GitHub Secrets | AWS Secrets Manager |
| Log level | DEBUG | INFO | WARNING |
| Feature flags | All enabled | Per-feature | Gradual rollout |
| SSL | Self-signed | ACM cert | ACM cert |
| Replicas | 1 | 2 | 3+ (auto-scaled) |

**Promotion rules:**
1. Code must pass ALL gates in the previous stage
2. Database migrations must be backward-compatible (no column drops without migration window)
3. Environment variables must be configured BEFORE deployment
4. Feature flags must be set to correct state BEFORE deployment
5. Rollback plan must be documented BEFORE production deployment

### Health Checks

Every service exposes health check endpoints. The deployment pipeline validates these after every deployment.

**Required health check endpoints:**

```python
# FastAPI health check endpoints
@router.get("/health")
async def health():
    """Basic liveness check -- returns 200 if process is running."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@router.get("/health/ready")
async def readiness(db: AsyncSession = Depends(get_db)):
    """Readiness check -- verifies all dependencies are accessible."""
    checks = {}
    # Database
    try:
        await db.execute(text("SELECT 1"))
        checks["database"] = "ok"
    except Exception as e:
        checks["database"] = f"error: {str(e)}"
    # Redis
    try:
        await redis.ping()
        checks["redis"] = "ok"
    except Exception as e:
        checks["redis"] = f"error: {str(e)}"

    all_ok = all(v == "ok" for v in checks.values())
    return JSONResponse(
        status_code=200 if all_ok else 503,
        content={"status": "ready" if all_ok else "not_ready", "checks": checks}
    )
```

**Health check strategy during deployment:**

```
After deploy:
  Wait 10s -> Check /health (liveness)
  Wait 5s  -> Check /health/ready (readiness)
  Wait 5s  -> Check /health/ready again (stability)
  All pass -> Deployment successful
  Any fail -> Trigger rollback
```

Use `scripts/health-check.py` for automated health validation:
```bash
python scripts/health-check.py \
  --url https://staging.example.com \
  --retries 3 \
  --timeout 30 \
  --output-dir ./health-results/
```

### Rollback Procedure

When a deployment fails, follow this rollback procedure immediately. See `references/rollback-runbook.md` for the full step-by-step guide.

**Automated rollback (preferred):**
```bash
# Roll back to previous version
./skills/deployment-pipeline/scripts/deploy.sh \
  --rollback \
  --version "$PREVIOUS_VERSION" \
  --output-dir ./rollback-results/
```

**Rollback decision matrix:**

| Signal | Action | Timeline |
|--------|--------|----------|
| Error rate > 5% | Automatic rollback | Immediate |
| p99 latency > 2x baseline | Automatic rollback | Immediate |
| Health check failures | Automatic rollback | After 2 retries |
| User-reported issues | Manual rollback decision | Within 15 minutes |
| Data inconsistency | Stop traffic, investigate | Immediate |

**Database rollback considerations:**
- Forward-only migrations are preferred; avoid `alembic downgrade` in production
- If migration must be reversed, use a new forward migration to undo changes
- Never drop columns or tables in the same release that removes code references
- Use a two-phase approach: Phase 1 deploys new code (backward compatible), Phase 2 removes old columns

### GitHub Actions CI/CD

The full CI/CD pipeline is defined in `.github/workflows/deploy.yml`. See `references/github-actions-template.yml` for the complete template.

**Key workflow features:**
- **Matrix testing** -- Test against Python 3.12 and 3.13
- **Caching** -- Cache pip, npm, and Docker layers for faster builds
- **Concurrency** -- Cancel in-progress deployments when new commits arrive
- **Environment protection** -- Require manual approval for production
- **Secrets management** -- Use GitHub environment secrets per stage

```yaml
# Key sections of the workflow
on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        type: choice
        options: [staging, production]

concurrency:
  group: deploy-${{ github.ref }}
  cancel-in-progress: true

jobs:
  build:    # Stage 1
  test:     # Stage 2 (needs: build)
  staging:  # Stage 3 (needs: test)
  production:  # Stage 4 (needs: staging, manual approval)
```

### Canary Deployment

Canary deployment routes a small percentage of traffic to the new version before full rollout.

**Implementation with Docker and Nginx:**

```nginx
# nginx canary configuration
upstream backend {
    server backend-stable:8000 weight=9;   # 90% to stable
    server backend-canary:8000 weight=1;   # 10% to canary
}
```

**Canary evaluation criteria:**

```python
# Canary health evaluation
def evaluate_canary(metrics: dict) -> bool:
    """Return True if canary is healthy enough to proceed."""
    checks = [
        metrics["error_rate"] < 0.01,           # < 1% error rate
        metrics["p99_latency_ms"] < 500,         # p99 under 500ms
        metrics["memory_usage_pct"] < 85,        # Memory under 85%
        metrics["cpu_usage_pct"] < 75,           # CPU under 75%
        metrics["successful_health_checks"] >= 3, # 3+ consecutive passes
    ]
    return all(checks)
```

**Canary monitoring checklist:**
- [ ] Error rate compared to baseline (must be within 1%)
- [ ] Latency percentiles (p50, p95, p99) compared to baseline
- [ ] Resource utilization (CPU, memory) within thresholds
- [ ] No increase in log error volume
- [ ] Health check endpoints responding correctly
- [ ] No degradation in dependent service metrics

### Deployment Scripts

The following scripts automate deployment tasks:

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/deploy.sh` | Main deployment orchestration | `./scripts/deploy.sh --env staging --output-dir ./results/` |
| `scripts/smoke-test.sh` | Post-deployment smoke tests | `./scripts/smoke-test.sh --url https://staging.example.com --output-dir ./results/` |
| `scripts/health-check.py` | Health endpoint validation | `python scripts/health-check.py --url https://staging.example.com --output-dir ./results/` |
| `scripts/migration-dry-run.sh` | Test migrations safely | `./scripts/migration-dry-run.sh --db-url $DB_URL --output-dir ./results/` |

### Quick Reference

**Deploy to staging:**
```bash
./skills/deployment-pipeline/scripts/deploy.sh \
  --env staging \
  --version $(git rev-parse --short HEAD) \
  --output-dir ./deploy-results/
```

**Deploy to production (with canary):**
```bash
./skills/deployment-pipeline/scripts/deploy.sh \
  --env production \
  --version $(git rev-parse --short HEAD) \
  --canary \
  --output-dir ./deploy-results/
```

**Run smoke tests:**
```bash
./skills/deployment-pipeline/scripts/smoke-test.sh \
  --url https://staging.example.com \
  --output-dir ./smoke-results/
```

**Emergency rollback:**
```bash
./skills/deployment-pipeline/scripts/deploy.sh \
  --rollback \
  --env production \
  --version $PREVIOUS_SHA \
  --output-dir ./rollback-results/
```
