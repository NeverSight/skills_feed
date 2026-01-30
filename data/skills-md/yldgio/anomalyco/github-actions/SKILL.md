---
name: github-actions
description: GitHub Actions workflow security, performance optimization, and best practices
---

## GitHub Actions Code Review Rules

### Security
- Pin actions to full commit SHA (not `@v1` or `@main`)
- Use minimal `permissions` block (principle of least privilege)
- Never echo secrets or use them in URLs
- Use `secrets.GITHUB_TOKEN` instead of PATs when possible
- Audit third-party actions before use

### Permissions
```yaml
permissions:
  contents: read  # Minimal by default
  # Add only what's needed:
  # pull-requests: write
  # issues: write
```

### Secrets
- Store secrets in repository/organization secrets
- Use environments for production secrets with approvals
- Don't pass secrets as command arguments (visible in logs)
- Mask sensitive output with `::add-mask::`

### Performance
- Use caching for dependencies (`actions/cache` or built-in)
- Run independent jobs in parallel
- Use `concurrency` to cancel redundant runs
- Consider self-hosted runners for heavy workloads

### Workflow Structure
- Use reusable workflows for common patterns
- Use composite actions for shared steps
- Set appropriate `timeout-minutes` to prevent hung jobs
- Use `if:` conditions to skip unnecessary jobs

### Triggers
- Be specific with `paths` and `branches` filters
- Use `workflow_dispatch` for manual triggers
- Consider `pull_request_target` security implications

### Common Anti-patterns
- Avoid `actions/checkout` with `persist-credentials: true` unless needed
- Avoid running on `push` to all branches
- Avoid hardcoding versions that need updates
