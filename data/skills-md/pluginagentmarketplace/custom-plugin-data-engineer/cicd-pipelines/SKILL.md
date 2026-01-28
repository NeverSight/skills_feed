---
name: cicd-pipelines
description: GitHub Actions, GitLab CI, Jenkins, and automated deployment pipelines
sasmp_version: "1.3.0"
bonded_agent: 03-devops-engineer
bond_type: PRIMARY_BOND
skill_version: "2.0.0"
last_updated: "2025-01"
complexity: intermediate
estimated_mastery_hours: 80
prerequisites: [git-version-control, containerization]
unlocks: [cloud-platforms, mlops]
---

# CI/CD Pipelines

Production CI/CD with GitHub Actions, testing automation, and deployment strategies.

## Quick Start

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run linting
        run: ruff check .

      - name: Run type checking
        run: mypy src/

      - name: Run tests
        run: pytest tests/ --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: coverage.xml
```

## Core Concepts

### 1. Complete CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy Pipeline

on:
  push:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt && pytest

  build:
    needs: test
    runs-on: ubuntu-latest
    outputs:
      image_tag: ${{ steps.meta.outputs.tags }}
    steps:
      - uses: actions/checkout@v4

      - name: Log in to registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix=
            type=ref,event=branch

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Deploy to staging
        run: |
          kubectl set image deployment/app \
            app=${{ needs.build.outputs.image_tag }}

  deploy-production:
    needs: [build, deploy-staging]
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy to production
        run: |
          kubectl set image deployment/app \
            app=${{ needs.build.outputs.image_tag }}
```

### 2. Matrix Testing

```yaml
jobs:
  test:
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
        os: [ubuntu-latest, macos-latest]
        database: [postgres, mysql]
        exclude:
          - os: macos-latest
            database: mysql
    runs-on: ${{ matrix.os }}
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pytest --db=${{ matrix.database }}
```

### 3. Reusable Workflows

```yaml
# .github/workflows/python-ci.yml (reusable)
name: Python CI

on:
  workflow_call:
    inputs:
      python-version:
        required: false
        type: string
        default: '3.12'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ inputs.python-version }}
      - run: pip install -r requirements.txt && pytest

# Usage in another workflow
jobs:
  ci:
    uses: ./.github/workflows/python-ci.yml
    with:
      python-version: '3.11'
```

### 4. Deployment Strategies

```yaml
# Blue-Green Deployment
deploy:
  steps:
    - name: Deploy to green
      run: |
        kubectl apply -f k8s/deployment-green.yaml
        kubectl rollout status deployment/app-green

    - name: Run smoke tests
      run: ./scripts/smoke-test.sh $GREEN_URL

    - name: Switch traffic
      run: |
        kubectl patch service app \
          -p '{"spec":{"selector":{"version":"green"}}}'

    - name: Cleanup blue
      run: kubectl delete deployment app-blue

# Canary Deployment
deploy-canary:
  steps:
    - name: Deploy canary (10%)
      run: |
        kubectl apply -f k8s/deployment-canary.yaml
        kubectl scale deployment/app-canary --replicas=1
        kubectl scale deployment/app-stable --replicas=9

    - name: Monitor canary
      run: ./scripts/monitor-canary.sh --duration=30m

    - name: Promote or rollback
      run: |
        if [ "$CANARY_SUCCESS" == "true" ]; then
          kubectl scale deployment/app-canary --replicas=10
          kubectl scale deployment/app-stable --replicas=0
        else
          kubectl delete deployment/app-canary
        fi
```

## Tools & Technologies

| Tool | Purpose | Version (2025) |
|------|---------|----------------|
| **GitHub Actions** | CI/CD platform | Latest |
| **GitLab CI** | CI/CD platform | 16+ |
| **ArgoCD** | GitOps for K8s | 2.10+ |
| **Terraform** | Infrastructure | 1.6+ |
| **act** | Local testing | 0.2+ |

## Troubleshooting Guide

| Issue | Symptoms | Root Cause | Fix |
|-------|----------|------------|-----|
| **Workflow Not Running** | No job triggered | Wrong trigger config | Check `on:` section |
| **Secret Not Available** | Empty variable | Missing secret | Add in repo settings |
| **Slow Builds** | Long duration | No caching | Add cache steps |
| **Flaky Tests** | Random failures | Race conditions | Fix tests, add retries |

## Best Practices

```yaml
# ✅ DO: Cache dependencies
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}

# ✅ DO: Use environments for deployments
environment: production

# ✅ DO: Pin action versions
- uses: actions/checkout@v4  # Not @main

# ✅ DO: Add timeouts
jobs:
  test:
    timeout-minutes: 10

# ❌ DON'T: Store secrets in code
# ❌ DON'T: Skip tests for faster deployments
```

## Resources

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [GitLab CI Docs](https://docs.gitlab.com/ee/ci/)
- [ArgoCD Docs](https://argo-cd.readthedocs.io/)

---

**Skill Certification Checklist:**
- [ ] Can create CI pipelines with testing
- [ ] Can build and push Docker images
- [ ] Can deploy to Kubernetes
- [ ] Can implement deployment strategies
- [ ] Can create reusable workflows
