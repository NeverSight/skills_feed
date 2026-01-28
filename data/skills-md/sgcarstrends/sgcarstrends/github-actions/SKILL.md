---
name: github-actions
description: Create and maintain GitHub Actions workflows for CI/CD, testing, deployment, and automation. Use when setting up pipelines, automating tasks, or configuring continuous integration.
allowed-tools: Read, Edit, Write, Bash, Grep, Glob
---

# GitHub Actions Skill

This skill helps you create and maintain GitHub Actions workflows for continuous integration and deployment.

## When to Use This Skill

- Setting up CI/CD pipelines
- Automating tests and builds
- Configuring deployment workflows
- Creating release automation
- Running scheduled jobs
- Automating dependency updates
- Setting up code quality checks

## Workflow Structure

```
.github/
├── workflows/
│   ├── test.yml              # Run tests on PR/push
│   ├── deploy-staging.yml    # Deploy to staging
│   ├── deploy-prod.yml       # Deploy to production
│   ├── release.yml           # Create releases
│   ├── security.yml          # Security audits
│   └── cron-jobs.yml         # Scheduled tasks
├── actions/
│   └── setup/                # Reusable actions
│       └── action.yml
└── dependabot.yml            # Dependency updates
```

## Basic Workflow

### Test Workflow

```yaml
# .github/workflows/test.yml
name: Test

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup pnpm
        uses: pnpm/action-setup@v2

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "pnpm"

      - name: Install dependencies
        run: pnpm install

      - name: Run linter
        run: pnpm biome check .

      - name: Type check
        run: pnpm tsc --noEmit

      - name: Run tests
        run: pnpm test

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info
```

## Deployment Workflows

### Deploy to Staging

```yaml
# .github/workflows/deploy-staging.yml
name: Deploy to Staging

on:
  push:
    branches: [develop]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.sgcarstrends.com

    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "pnpm"

      - name: Install dependencies
        run: pnpm install

      - name: Run tests
        run: pnpm test

      - name: Build
        run: pnpm build

      - name: Deploy API
        run: pnpm -F @sgcarstrends/api deploy:staging
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

      - name: Deploy Web
        run: pnpm -F @sgcarstrends/web deploy:staging
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

      - name: Run migrations
        run: pnpm db:migrate
        env:
          DATABASE_URL: ${{ secrets.STAGING_DATABASE_URL }}

      - name: Notify Slack
        if: always()
        uses: slackapi/slack-github-action@v1
        with:
          webhook-url: ${{ secrets.SLACK_WEBHOOK_URL }}
          payload: |
            {
              "text": "Staging deployment ${{ job.status }}"
            }
```

### Deploy to Production

```yaml
# .github/workflows/deploy-prod.yml
name: Deploy to Production

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      confirm:
        description: "Type 'deploy' to confirm"
        required: true

jobs:
  confirm:
    if: github.event_name == 'workflow_dispatch'
    runs-on: ubuntu-latest
    steps:
      - name: Confirm deployment
        run: |
          if [ "${{ github.event.inputs.confirm }}" != "deploy" ]; then
            echo "Deployment not confirmed"
            exit 1
          fi

  deploy:
    needs: [confirm]
    if: always() && (needs.confirm.result == 'success' || github.event_name == 'push')
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://sgcarstrends.com

    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "pnpm"

      - name: Install dependencies
        run: pnpm install

      - name: Run tests
        run: pnpm test

      - name: Run security audit
        run: pnpm audit --audit-level=high

      - name: Build
        run: pnpm build

      - name: Deploy API
        run: pnpm -F @sgcarstrends/api deploy:prod
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

      - name: Deploy Web
        run: pnpm -F @sgcarstrends/web deploy:prod
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

      - name: Run migrations
        run: pnpm db:migrate
        env:
          DATABASE_URL: ${{ secrets.PRODUCTION_DATABASE_URL }}

      - name: Create deployment
        uses: chrnorm/deployment-action@v2
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          environment: production
          state: success

      - name: Notify team
        if: always()
        uses: slackapi/slack-github-action@v1
        with:
          webhook-url: ${{ secrets.SLACK_WEBHOOK_URL }}
          payload: |
            {
              "text": "🚀 Production deployment ${{ job.status }}",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*Production Deployment*\nStatus: ${{ job.status }}\nCommit: ${{ github.sha }}\nAuthor: ${{ github.actor }}"
                  }
                }
              ]
            }
```

## Release Workflow

### Automated Release

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    branches: [main]

permissions:
  contents: write
  issues: write
  pull-requests: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          persist-credentials: false

      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "pnpm"

      - name: Install dependencies
        run: pnpm install

      - name: Release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
        run: npx semantic-release

      - name: Get new version
        id: version
        run: |
          VERSION=$(node -p "require('./package.json').version")
          echo "version=$VERSION" >> $GITHUB_OUTPUT

      - name: Create GitHub Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: v${{ steps.version.outputs.version }}
          release_name: Release v${{ steps.version.outputs.version }}
          draft: false
          prerelease: false
```

## Reusable Workflows

### Shared Setup Action

```yaml
# .github/actions/setup/action.yml
name: "Setup Project"
description: "Setup Node.js, pnpm, and install dependencies"

inputs:
  node-version:
    description: "Node.js version"
    required: false
    default: "20"

runs:
  using: "composite"
  steps:
    - name: Setup pnpm
      uses: pnpm/action-setup@v2
      with:
        version: 8

    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
        cache: "pnpm"

    - name: Install dependencies
      shell: bash
      run: pnpm install --frozen-lockfile

    - name: Cache Turbo
      uses: actions/cache@v3
      with:
        path: .turbo
        key: ${{ runner.os }}-turbo-${{ github.sha }}
        restore-keys: |
          ${{ runner.os }}-turbo-
```

### Use Reusable Workflow

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup project
        uses: ./.github/actions/setup

      - name: Run tests
        run: pnpm test
```

## Matrix Strategy

### Test Multiple Versions

```yaml
name: Test Matrix

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node: [18, 20, 21]
        exclude:
          - os: windows-latest
            node: 18

    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
          cache: "pnpm"

      - run: pnpm install
      - run: pnpm test
```

## Conditional Execution

### Run Jobs Conditionally

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-api:
    if: contains(github.event.head_commit.message, '[deploy-api]')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pnpm -F @sgcarstrends/api deploy:prod

  deploy-web:
    if: contains(github.event.head_commit.message, '[deploy-web]')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pnpm -F @sgcarstrends/web deploy:prod

  deploy-all:
    if: |
      !contains(github.event.head_commit.message, '[deploy-api]') &&
      !contains(github.event.head_commit.message, '[deploy-web]')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pnpm deploy:prod
```

## Caching

### Cache Dependencies

```yaml
- name: Cache pnpm store
  uses: actions/cache@v3
  with:
    path: ~/.pnpm-store
    key: ${{ runner.os }}-pnpm-${{ hashFiles('**/pnpm-lock.yaml') }}
    restore-keys: |
      ${{ runner.os }}-pnpm-

- name: Cache Turbo
  uses: actions/cache@v3
  with:
    path: .turbo
    key: ${{ runner.os }}-turbo-${{ github.sha }}
    restore-keys: |
      ${{ runner.os }}-turbo-

- name: Cache Next.js
  uses: actions/cache@v3
  with:
    path: apps/web/.next/cache
    key: ${{ runner.os }}-nextjs-${{ hashFiles('**/pnpm-lock.yaml') }}
```

## Secrets Management

### Using Secrets

```yaml
- name: Deploy
  env:
    AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
    AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
    REDIS_URL: ${{ secrets.REDIS_URL }}
  run: pnpm deploy:prod
```

### Environment-Specific Secrets

```yaml
jobs:
  deploy:
    environment: production
    steps:
      - name: Deploy
        env:
          DATABASE_URL: ${{ secrets.PRODUCTION_DATABASE_URL }}
        run: pnpm deploy:prod
```

## Scheduled Workflows

### Cron Jobs

```yaml
# .github/workflows/cron-jobs.yml
name: Scheduled Jobs

on:
  schedule:
    # Run every day at 2 AM UTC
    - cron: "0 2 * * *"
  workflow_dispatch:

jobs:
  update-data:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup

      - name: Update car data
        run: pnpm -F @sgcarstrends/api run-workflow update-car-data
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
          LTA_API_KEY: ${{ secrets.LTA_API_KEY }}

  cleanup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup

      - name: Clean old data
        run: pnpm -F @sgcarstrends/api run-script cleanup-old-data
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

## Notifications

### Slack Notifications

```yaml
- name: Notify Slack on success
  if: success()
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK_URL }}
    payload: |
      {
        "text": "✅ Deployment successful",
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*Deployment Successful*\nCommit: ${{ github.sha }}\nAuthor: ${{ github.actor }}"
            }
          }
        ]
      }

- name: Notify Slack on failure
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK_URL }}
    payload: |
      {
        "text": "❌ Deployment failed",
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*Deployment Failed*\nCommit: ${{ github.sha }}\nAuthor: ${{ github.actor }}\nWorkflow: ${{ github.workflow }}"
            }
          }
        ]
      }
```

## Artifacts

### Upload and Download

```yaml
# Upload artifacts
- name: Upload build artifacts
  uses: actions/upload-artifact@v3
  with:
    name: build-output
    path: |
      dist/
      .next/
    retention-days: 7

# Download artifacts in another job
- name: Download build artifacts
  uses: actions/download-artifact@v3
  with:
    name: build-output
```

## Best Practices

### 1. Use Specific Versions

```yaml
# ❌ Using latest
- uses: actions/checkout@latest

# ✅ Using specific version
- uses: actions/checkout@v4
```

### 2. Pin Action Versions

```yaml
# ✅ Good: Pinned to major version
- uses: actions/checkout@v4
- uses: actions/setup-node@v4

# ✅ Better: Pinned to commit SHA (most secure)
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # v4.1.1
```

### 3. Use Concurrency Controls

```yaml
name: Deploy

on:
  push:
    branches: [main]

concurrency:
  group: deploy-${{ github.ref }}
  cancel-in-progress: false  # Don't cancel in-progress deployments
```

### 4. Fail Fast

```yaml
jobs:
  test:
    strategy:
      fail-fast: true  # Stop all jobs if one fails
      matrix:
        node: [18, 20, 21]
```

## Troubleshooting

### Workflow Not Triggering

```yaml
# Issue: Workflow not running
# Solution: Check triggers and permissions

on:
  push:
    branches: [main]  # Ensure branch name matches
  pull_request:
    branches: [main]

permissions:
  contents: read
  pull-requests: write
```

### Secret Not Found

```yaml
# Issue: Secret not available
# Solution: Check secret name and environment

- name: Deploy
  environment: production  # Ensure environment exists
  env:
    SECRET: ${{ secrets.MY_SECRET }}  # Check secret name
```

### Cache Not Working

```yaml
# Issue: Cache not restoring
# Solution: Verify cache key

- uses: actions/cache@v3
  with:
    path: ~/.pnpm-store
    key: ${{ runner.os }}-pnpm-${{ hashFiles('**/pnpm-lock.yaml') }}
    # Ensure lockfile exists and path is correct
```

## References

- GitHub Actions Documentation: https://docs.github.com/en/actions
- Workflow Syntax: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions
- Actions Marketplace: https://github.com/marketplace?type=actions
- Related files:
  - `.github/workflows/` - Workflow files
  - Root CLAUDE.md - CI/CD guidelines

## Best Practices Summary

1. **Pin Versions**: Use specific action versions
2. **Cache Dependencies**: Cache pnpm, Turbo, Next.js
3. **Parallel Jobs**: Run independent jobs in parallel
4. **Fail Fast**: Stop on first failure in matrix
5. **Secrets Management**: Use GitHub Secrets for sensitive data
6. **Notifications**: Alert team on deployment status
7. **Reusable Workflows**: Share common setup steps
8. **Environment Protection**: Use environment rules for production
