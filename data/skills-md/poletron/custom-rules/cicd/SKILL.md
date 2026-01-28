---
name: cicd
description: >
  CI/CD pipeline patterns for automated testing and deployment.
  Trigger: When configuring CI/CD pipelines.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with cicd"

## When to Use

Use this skill when:
- Setting up GitHub Actions workflows
- Configuring automated testing
- Implementing deployment pipelines
- Managing release processes

---

## Critical Patterns

### Pipeline Structure (REQUIRED)

```yaml
# ✅ ALWAYS: Clear stages
name: CI/CD Pipeline

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
      - name: Run tests
        run: npm test

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Build
        run: npm run build

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        run: ./deploy.sh
```

### Secrets Management (REQUIRED)

```yaml
# ✅ ALWAYS: Use GitHub Secrets
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
  API_KEY: ${{ secrets.API_KEY }}

# ❌ NEVER: Hardcode secrets
env:
  API_KEY: "sk-1234567890"
```

### Caching (RECOMMENDED)

```yaml
# ✅ Cache dependencies for faster builds
- name: Cache node modules
  uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

---

## Decision Tree

```
Need fast builds?          → Add caching
Need matrix testing?       → Use strategy.matrix
Need manual approval?      → Use environment protection
Need artifacts?            → Use upload-artifact
Need notifications?        → Add Slack/Discord step
```

---

## Code Examples

### Matrix Strategy

```yaml
jobs:
  test:
    strategy:
      matrix:
        node-version: [18, 20]
        os: [ubuntu-latest, windows-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
```

### Docker Build and Push

```yaml
- name: Build and push Docker image
  uses: docker/build-push-action@v5
  with:
    context: .
    push: true
    tags: |
      myregistry/myapp:${{ github.sha }}
      myregistry/myapp:latest
```

---

## Commands

```bash
# Local testing with act
act -j test

# GitHub CLI
gh run list
gh run view <run-id>
gh run watch
```
