---
name: dependency-manager
description: Expert at package management and supply chain security. Use when managing dependencies, updating packages, resolving version conflicts, ensuring supply chain security, or auditing vulnerabilities in project dependencies.
---

# Dependency Manager

## Purpose
Provides expertise in package management, version resolution, and software supply chain security. Handles dependency updates, vulnerability auditing, and conflict resolution across multiple package ecosystems.

## When to Use
- Updating project dependencies
- Resolving version conflicts
- Auditing for security vulnerabilities
- Managing lockfiles and reproducibility
- Migrating between package managers
- Implementing dependency policies
- Reducing bundle size via dependency analysis

## Quick Start
**Invoke this skill when:**
- Updating project dependencies
- Resolving version conflicts
- Auditing for security vulnerabilities
- Managing lockfiles and reproducibility
- Implementing dependency policies

**Do NOT invoke when:**
- Building CI/CD pipelines (use devops-engineer)
- Publishing packages to registries (use build-engineer)
- Container image management (use kubernetes-specialist)
- Cloud infrastructure dependencies (use terraform-engineer)

## Decision Framework
```
Update Strategy:
├── Security patch → Update immediately
├── Bug fix (patch) → Update with tests
├── Minor version → Review changelog, test
├── Major version → Full compatibility review
└── Deprecated package → Find replacement

Ecosystem Tools:
├── Node.js → npm, yarn, pnpm
├── Python → pip, poetry, uv
├── Go → go mod
├── Rust → cargo
├── Java → Maven, Gradle
└── .NET → NuGet
```

## Core Workflows

### 1. Dependency Audit
1. Run package audit tool
2. Review vulnerability reports
3. Prioritize by severity (CVSS)
4. Check for available patches
5. Update or find alternatives
6. Verify fixes don't break app
7. Document remediation

### 2. Major Version Upgrade
1. Read changelog and migration guide
2. Check for breaking changes
3. Update in isolated branch
4. Run full test suite
5. Fix breaking changes
6. Review for deprecated APIs
7. Deploy to staging first

### 3. Lockfile Management
1. Ensure lockfile is committed
2. Use CI to verify lockfile matches
3. Regenerate on conflict resolution
4. Audit lockfile for tampering
5. Update lockfile atomically

## Best Practices
- Always use lockfiles for reproducibility
- Run security audits in CI/CD
- Pin exact versions in production
- Use renovate/dependabot for automation
- Audit transitive dependencies
- Minimize dependency count

## Anti-Patterns
| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| No lockfile | Non-reproducible builds | Commit lockfiles |
| Ignoring audits | Security vulnerabilities | Address all high/critical |
| Auto-merge updates | Breaking changes in prod | Test before merge |
| Too many deps | Large attack surface | Audit and minimize |
| Outdated deps | Missing security patches | Regular update cadence |
