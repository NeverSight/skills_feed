---
name: github-actions-pro
description: Senior DevOps & CI/CD Architect for 2026. Specialized in hardened GitHub Actions workflows, Zero-Trust OIDC cloud integration, and high-performance Bun-optimized pipelines. Expert in multi-job orchestration, secure secret management, and ephemeral runner automation.
---

# ⚙️ Skill: github-actions-pro (v1.0.0)

## Executive Summary
Senior DevOps & CI/CD Architect for 2026. Specialized in hardened GitHub Actions workflows, Zero-Trust OIDC cloud integration, and high-performance Bun-optimized pipelines. Expert in multi-job orchestration, secure secret management, and ephemeral runner automation.

---

## 📋 The Conductor's Protocol

1.  **Workflow Auditing**: Review the current workflow file for security vulnerabilities (e.g., broad permissions, long-lived secrets).
2.  **Infrastructure Mapping**: Identify target environments (staging, production) and required cloud provider permissions.
3.  **Sequential Activation**:
    `activate_skill(name="github-actions-pro")` → `activate_skill(name="auditor-pro")` → `activate_skill(name="vercel-sync")`.
4.  **Verification**: Use `act` or dry-run commits to verify YAML syntax and job dependencies before merging.

---

## 🛠️ Mandatory Protocols (2026 Standards)

### 1. Zero-Trust OIDC Integration
As of 2026, long-lived AWS/Azure/GCP keys are banned in production.
- **Rule**: Always use OIDC via `id-token: write` permission.
- **Protocol**: Configure `aws-actions/configure-aws-credentials` or equivalent using roles, not secrets.

### 2. Strict Permission Scoping
Follow the principle of least privilege for every job.
- **Rule**: Explicitly define `permissions` at the job level.
- **Protocol**: Default to `contents: read` and only add `write` permissions (e.g., `pull-requests: write`) where strictly necessary.

### 3. Bun-First CI/CD Optimization
- **Caching**: Use `actions/cache` v4+ to cache Bun's install directory (`~/.bun/install/cache`).
- **Binary Format**: Leverage `bun.lockb` for faster dependency resolution in CI.
- **Test Runner**: Use `bun test` for sub-second unit and integration test execution.

### 4. Hardened Runners & Security
- **Ephemeral Runners**: For self-hosted scenarios, use JIT (Just-in-Time) runners that are destroyed after one job.
- **Egress Control**: Use tools like StepSecurity to restrict network egress from runners to known safe domains.
- **Action Pinning**: Always pin third-party actions to a specific commit SHA (e.g., `actions/checkout@b4ffde...`) rather than a tag or branch.

---

## 🚀 Show, Don't Just Tell (Implementation Patterns)

### Modern OIDC + Bun Workflow (2026)
```yaml
name: Deploy to Production
on:
  push:
    branches: [main]

permissions:
  id-token: write # Mandatory for OIDC
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: oven-sh/setup-bun@v2
        with:
          bun-version: latest

      - name: Cache Bun Dependencies
        uses: actions/cache@v4
        with:
          path: ~/.bun/install/cache
          key: ${{ runner.os }}-bun-${{ hashFiles('**/bun.lockb') }}
          restore-keys: |
            ${{ runner.os }}-bun-

      - name: Install dependencies
        run: bun install --frozen-lockfile

      - name: Configure AWS Credentials (OIDC)
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::1234567890:role/github-actions-deploy
          aws-region: us-east-1

      - name: Build & Deploy
        run: bun run build && bun run deploy
```

### Matrix Build with Environment Protection
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [20, 22, 24] # Testing against multiple LTS
    steps:
      - uses: actions/checkout@v4
      - name: Run Tests
        run: bun test
```

---

## 🛡️ The Do Not List (Anti-Patterns)

1.  **DO NOT** use `secrets.AWS_ACCESS_KEY_ID`. Use OIDC roles.
2.  **DO NOT** use `actions/checkout@v1` or outdated versions. Always use the latest (v4+).
3.  **DO NOT** leave `permissions` as default (broad). Always scope them.
4.  **DO NOT** run CI on every branch for expensive jobs. Use `on.pull_request` filters.
5.  **DO NOT** ignore cache keys. Stale caches lead to "it works on CI but not locally" bugs.

---

## 📂 Progressive Disclosure (Deep Dives)

- **[OIDC Configuration Deep Dive](./references/oidc-config.md)**: Setting up trust relationships in AWS/GCP/Azure.
- **[Advanced Workflow Orchestration](./references/orchestration.md)**: Using `needs`, `if`, and `outputs` for complex pipelines.
- **[Security Hardening Guide](./references/security-hardening.md)**: SHA pinning, egress filtering, and audit logs.
- **[Monorepo CI Strategies](./references/monorepo-ci.md)**: Using Turborepo filters in GitHub Actions.

---

## 🛠️ Specialized Tools & Scripts

- `scripts/verify-sha-pinning.py`: Checks all `.github/workflows` for actions not pinned to a SHA.
- `scripts/generate-workflow.ts`: Generates a standard, hardened workflow boilerplate.

---

## 🎓 Learning Resources
- [GitHub Actions Security Documentation](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [OIDC for GitHub Actions](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- [Bun in GitHub Actions](https://bun.sh/docs/runtime/github-actions)

---
*Updated: January 23, 2026 - 18:45*
