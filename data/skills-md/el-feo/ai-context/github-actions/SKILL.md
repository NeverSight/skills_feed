---
name: github-actions
description: Create, evaluate, and optimize GitHub Actions workflows and custom actions. Use when building CI/CD pipelines, creating workflow files, developing custom actions, troubleshooting workflow failures, performing security analysis, optimizing performance, or reviewing GitHub Actions best practices. Covers Ruby/Rails, TypeScript/Node.js, Heroku and Fly.io deployments.
---

<objective>
Enable creation, evaluation, and optimization of GitHub Actions workflows and custom actions with comprehensive coverage of CI/CD patterns, security best practices, performance optimization, and deployment strategies for Ruby/Rails and TypeScript projects to Heroku and Fly.io.
</objective>

<context>
GitHub Actions automates software workflows with event-driven CI/CD pipelines. Workflows are YAML files in `.github/workflows/` that define jobs, steps, and actions triggered by repository events.

**Latest Updates (2024-2025):**
- **November 2025**: Nested reusable workflows increased to 10 levels (was 4), total workflows to 50 (was 20)
- **November 2025**: M2-powered macOS runners with GPU acceleration (macos-latest-xlarge, macos-15-xlarge)
- **December 2024 - January 2025**: ubuntu-latest migrating from Ubuntu 22 to Ubuntu 24
- **February-March 2025**: Cache storage v1-v2 retirement - must use actions/cache@v4.0.0+

**Action Types:**
- **Workflow files**: CI/CD pipelines using existing actions (.github/workflows/*.yml)
- **Custom JavaScript actions**: Fast, cross-platform, use @actions/toolkit
- **Custom Docker actions**: Full environment control, specific tooling, slower startup
- **Composite actions**: Combine multiple steps into reusable units
</context>

<quick_start>
**Create a basic workflow:**

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Run tests
        run: npm test
```

**Ruby/Rails with RSpec:**

```yaml
- uses: ruby/setup-ruby@v1
  with:
    ruby-version: .ruby-version
    bundler-cache: true

- name: Setup database
  env:
    RAILS_ENV: test
  run: bin/rails db:setup

- name: Run tests
  run: bundle exec rspec
```

**TypeScript/Node.js:**

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'

- run: npm ci
- run: npm run build --if-present
- run: npm test
```

**Deploy to Fly.io:**

```yaml
- uses: superfly/flyctl-actions/setup-flyctl@master
- run: flyctl deploy --remote-only
  env:
    FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```
</quick_start>

<workflow>
**Creating Workflows:**

1. **Identify triggers**: push, pull_request, workflow_dispatch, schedule, etc.
2. **Define jobs**: Specify runner OS, steps, and dependencies
3. **Add security**: Set GITHUB_TOKEN permissions to read-only, pin actions to SHA
4. **Optimize performance**: Enable caching, use matrix builds for parallelization
5. **Test locally**: Use act or GitHub CLI to test before pushing

**Evaluating Workflows:**

1. **Security scan**: Check permissions, secrets exposure, action pinning, pull_request_target usage
2. **Performance analysis**: Identify slow steps, missing caches, parallelization opportunities
3. **Best practices review**: Validate naming, structure, error handling, documentation
4. **Troubleshooting**: Review logs, check dependencies, verify secrets/environment variables
</workflow>

<validation>
**Pre-deployment checks:**

- YAML syntax valid (use yamllint or GitHub's workflow validator)
- Required secrets configured in repository settings
- GITHUB_TOKEN permissions explicitly set to minimum required
- Actions pinned to specific SHA or trusted tags
- Caching configured for dependencies (bundler, npm, etc.)
- Matrix builds used for multiple versions/platforms
- Workflow triggers appropriate for use case

**Post-deployment monitoring:**

- First run completes successfully
- Execution time acceptable (check for optimization opportunities if >5 minutes)
- No secrets or credentials in logs
- Cache hit rate >80% after first run
</validation>

<security_checklist>
**Critical Security Patterns:**

1. **GITHUB_TOKEN permissions**: Always set to read-only by default
   ```yaml
   permissions:
     contents: read
   ```

2. **Pin actions to commit SHA** (most secure):
   ```yaml
   - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1
   ```

3. **Use OIDC for cloud deployments** (credential-less authentication):
   ```yaml
   permissions:
     id-token: write
     contents: read
   ```

4. **Avoid pull_request_target with untrusted code**:
   - Runs in base repository context with access to secrets
   - Never checkout PR code without approval workflow

5. **Environment secrets with required reviewers**:
   ```yaml
   jobs:
     deploy:
       environment: production
   ```

6. **Never log secrets**:
   - Use `::add-mask::` for dynamic values
   - Avoid `echo` or `print` statements with secret variables

7. **Audit action sources**:
   - Prefer verified creators (GitHub, major organizations)
   - Review action source code before using
   - Check for recent maintenance and security issues

See [references/security-checklist.md](references/security-checklist.md) for complete security guidelines.
</security_checklist>

<common_patterns>
**Conditional execution:**

```yaml
- name: Deploy to production
  if: github.ref == 'refs/heads/main' && github.event_name == 'push'
  run: ./deploy.sh
```

**Matrix builds:**

```yaml
strategy:
  matrix:
    ruby-version: ['3.1', '3.2', '3.3']
    os: [ubuntu-latest, macos-latest]
jobs:
  test:
    runs-on: ${{ matrix.os }}
```

**Reusable workflows:**

```yaml
# .github/workflows/reusable.yml
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying to ${{ inputs.environment }}"
```

```yaml
# .github/workflows/main.yml
jobs:
  call-reusable:
    uses: ./.github/workflows/reusable.yml
    with:
      environment: production
```

**Secrets in composite actions:**

```yaml
# Pass secrets explicitly - they're not inherited
- uses: ./.github/actions/my-action
  with:
    api-key: ${{ secrets.API_KEY }}
```

See [references/common-workflows.md](references/common-workflows.md) for Ruby/Rails, TypeScript, Heroku, and Fly.io patterns.
</common_patterns>

<anti_patterns>
**Avoid these mistakes:**

- **Running as root in Docker actions**: Use non-root user for security
- **Hardcoded secrets**: Always use GitHub Secrets
- **Overly broad permissions**: Set minimal required permissions
- **No caching**: Wastes time and resources on every run
- **Sequential jobs that could be parallel**: Use dependencies only when needed
- **Using `master` branch references**: Pin to tags or SHAs
- **Ignoring security alerts**: Review and address Dependabot alerts
- **No timeout-minutes**: Jobs can run for 6 hours by default
- **Checkout without depth control**: Use `fetch-depth: 0` only when needed
- **Manual apt-get installs**: Use setup actions when available
</anti_patterns>

<examples>
**Complete Rails CI/CD workflow:**

```yaml
name: Rails CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4

      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: .ruby-version
          bundler-cache: true

      - name: Setup database
        env:
          RAILS_ENV: test
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/test
        run: |
          bin/rails db:create
          bin/rails db:schema:load

      - name: Run tests
        env:
          RAILS_ENV: test
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/test
        run: bundle exec rspec

      - name: Run RuboCop
        run: bundle exec rubocop

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    environment: production

    steps:
      - uses: actions/checkout@v4

      - uses: superfly/flyctl-actions/setup-flyctl@master

      - run: flyctl deploy --remote-only
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

See [references/common-workflows.md](references/common-workflows.md) for more complete examples.
</examples>

<troubleshooting>
**Common issues and solutions:**

1. **"Resource not accessible by integration"**
   - Add required permissions to GITHUB_TOKEN
   - Check if job needs `contents: write` or `pull-requests: write`

2. **Cache not restoring**
   - Verify cache key matches between save and restore
   - Check if cache size exceeds 10GB limit
   - Ensure actions/cache@v4+ for new cache backend

3. **Secrets not available**
   - Verify secret is defined in repository/organization/environment settings
   - Check if job requires `environment` for environment secrets
   - Ensure secret name matches exactly (case-sensitive)

4. **Action fails to find command**
   - Ensure setup action runs before command usage
   - Check PATH modifications in previous steps
   - Verify runner OS matches requirements

5. **Timeout after 6 hours**
   - Add `timeout-minutes: 30` to jobs or steps
   - Investigate why job runs so long (missing cache, inefficient scripts)

See [references/troubleshooting.md](references/troubleshooting.md) for detailed debugging strategies.
</troubleshooting>

<performance_optimization>
**Key optimization strategies:**

1. **Dependency caching** (can reduce build times by 80%):
   - Ruby: Use `ruby/setup-ruby` with `bundler-cache: true`
   - Node.js: Use `actions/setup-node` with `cache: 'npm'`
   - Custom: Use `actions/cache@v4` with hash keys from lock files

2. **Parallelization**:
   - Use matrix builds for multiple versions/platforms
   - Split independent jobs to run concurrently
   - Avoid job dependencies unless actually required

3. **Selective triggers**:
   ```yaml
   on:
     push:
       paths:
         - 'src/**'
         - 'package.json'
   ```

4. **Concurrency control** (cancel outdated runs):
   ```yaml
   concurrency:
     group: ${{ github.workflow }}-${{ github.ref }}
     cancel-in-progress: true
   ```

5. **Self-hosted runners** for heavy workloads:
   - Persistent caching across runs
   - Faster than GitHub-hosted for large builds
   - More control over environment

See [references/performance-optimization.md](references/performance-optimization.md) for advanced techniques.
</performance_optimization>

<reference_guides>
For detailed information on specific topics:

- **[Workflow Syntax](references/workflow-syntax.md)**: Complete YAML reference, triggers, jobs, steps, expressions
- **[Custom Actions](references/custom-actions.md)**: Building JavaScript, Docker, and composite actions
- **[Security Checklist](references/security-checklist.md)**: Comprehensive security patterns and OIDC setup
- **[Performance Optimization](references/performance-optimization.md)**: Caching strategies, parallelization, profiling
- **[Common Workflows](references/common-workflows.md)**: Ruby/Rails, TypeScript, Heroku/Fly.io deployment templates
- **[Troubleshooting](references/troubleshooting.md)**: Debugging workflows, common errors, log analysis
- **[Evaluation Guide](references/evaluation-guide.md)**: Security analysis, performance review, best practices audit
</reference_guides>

<success_criteria>
**For workflow creation:**
- Workflow file is valid YAML with correct syntax
- Triggers appropriate for use case
- Jobs execute successfully with expected outputs
- Security best practices applied (permissions, pinned actions, no secrets in logs)
- Performance optimized (caching, parallelization where appropriate)
- Documentation included (comments explaining non-obvious steps)

**For workflow evaluation:**
- Security issues identified and prioritized
- Performance bottlenecks documented with recommendations
- Best practice violations noted with fixes
- Overall assessment: PASS/FAIL/NEEDS_IMPROVEMENT with specific action items
</success_criteria>
