---
name: release-readiness-checklist
description: Interactive release readiness checklist with semantic versioning guidance. Use when preparing a software release, cutting a version, deploying to production, or when user asks about release preparation. Triggers on phrases like "prepare release", "release checklist", "ready to release", "cut a version", "version bump", or "/release-readiness-checklist".
---

# Release Readiness Checklist

Conduct an interactive release readiness review, walking through each checklist category and producing a markdown summary at the end.

## Workflow

1. **Detect build system** - Check for Makefile and available targets
2. **Determine version** - Analyze changes to recommend semantic version bump
3. **Walk through checklist** - Review each category interactively with the user
4. **Generate summary** - Output markdown checklist with status and action items

## Step 0: Detect Build System

Check if the project has a Makefile or Justfile with standard targets:

```bash
# List Makefile targets
make -qp 2>/dev/null | grep -E "^[a-zA-Z_-]+:" | cut -d: -f1 | sort -u

# List Justfile recipes
just --list 2>/dev/null
```

Common targets/recipes to look for: `build`, `test`, `lint`, `format`, `check`, `audit`, `clean`

**If Makefile or Justfile exists with these targets, prefer them over language-specific commands throughout the checklist:**

| Task | Makefile | Justfile | Fallback |
| ---- | -------- | -------- | -------- |
| Lint | `make lint` | `just lint` | `npm run lint`, `ruff check` |
| Test | `make test` | `just test` | `pytest`, `npm test` |
| Build | `make build` | `just build` | `npm run build`, `cargo build` |
| Format | `make format` | `just format` | `prettier`, `black` |
| Audit | `make audit` | `just audit` | `npm audit`, `pip-audit` |

## Step 1: Determine Version Type

Analyze the changes since the last release to recommend a version bump:

```
MAJOR (X.0.0) - Breaking changes
├── API contract changes (removed/renamed endpoints, changed request/response schemas)
├── Database schema changes requiring migration
├── Removed or renamed public interfaces/exports
├── Changed default behaviors that could break existing integrations
└── Dependency upgrades with breaking changes that surface to users

MINOR (x.Y.0) - New features, backward-compatible
├── New API endpoints or features
├── New optional parameters or configuration
├── Deprecations (without removal)
├── Performance improvements
└── New dependencies that don't affect public API

PATCH (x.y.Z) - Bug fixes, backward-compatible
├── Bug fixes
├── Security patches
├── Documentation updates
├── Internal refactoring (no behavior change)
└── Dependency updates (non-breaking)
```

Examine recent commits, changelog entries, or ask the user about changes to determine the appropriate version bump.

## Step 2: Interactive Checklist Review

Walk through each category below. For each item:
- Ask the user for status (done, not applicable, needs work)
- Offer to help resolve blockers
- Track items that need attention

### Categories

**Code Quality**
- [ ] All code changes reviewed and approved
- [ ] No TODO/FIXME comments blocking release
- [ ] No debug code or console statements in production paths
- [ ] Linting passes with no errors
- [ ] Type checking passes (if applicable)

**Testing**
- [ ] All tests pass
- [ ] Test coverage meets project threshold
- [ ] Critical paths have integration tests
- [ ] Manual testing completed for new features
- [ ] Regression testing for bug fixes

**Documentation**
- [ ] CHANGELOG updated with all notable changes
- [ ] README updated if features/setup changed
- [ ] API documentation reflects changes
- [ ] Migration guide written (for breaking changes)

**Security**
- [ ] No secrets or credentials in codebase
- [ ] Git history scanned for exposed secrets (see references/secrets-scanning.md)
- [ ] Dependencies scanned for vulnerabilities
- [ ] Security-sensitive changes reviewed
- [ ] Authentication/authorization changes tested

**Versioning**
- [ ] Version bumped according to semver (see references/semver.md)
- [ ] Version consistent across all package files
- [ ] Git tag prepared (not pushed)
- [ ] Previous version tagged and accessible

**CI/CD**
- [ ] All CI checks pass on release branch
- [ ] Pipeline configuration follows best practices (see references/ci-cd-best-practices.md)
- [ ] Build artifacts generated successfully
- [ ] Deployment pipeline tested in staging
- [ ] Rollback procedure documented and tested

**Release Artifacts**
- [ ] Release notes drafted
- [ ] Changelog entry finalized
- [ ] Distribution packages built
- [ ] Checksums/signatures generated (if applicable)

**Operational Readiness**
- [ ] Monitoring and alerting configured
- [ ] Rollback plan documented
- [ ] On-call team notified
- [ ] Communication plan ready (announcements, notifications)

See references/checklist-details.md for detailed explanations of each item.

## Step 3: Generate Summary

After completing the review, output a markdown summary:

```markdown
# Release Readiness Report

**Project:** [name]
**Proposed Version:** [X.Y.Z]
**Date:** [YYYY-MM-DD]
**Status:** [Ready / Blocked]

## Version Determination
[Explanation of why this version number was chosen based on semver]

## Checklist Summary

| Category | Status | Blockers |
|----------|--------|----------|
| Code Quality | ✅/⚠️/❌ | [issues] |
| Testing | ✅/⚠️/❌ | [issues] |
| Documentation | ✅/⚠️/❌ | [issues] |
| Security | ✅/⚠️/❌ | [issues] |
| Versioning | ✅/⚠️/❌ | [issues] |
| CI/CD | ✅/⚠️/❌ | [issues] |
| Release Artifacts | ✅/⚠️/❌ | [issues] |
| Operational Readiness | ✅/⚠️/❌ | [issues] |

## Action Items
- [ ] [Blocking items that must be resolved]
- [ ] [Recommended items to address]

## Approval
- [ ] Release approved by: _______________
- [ ] Release date/time: _______________
```

## Resources

- **references/semver.md** - Semantic versioning rules and examples
- **references/checklist-details.md** - Detailed explanations for each checklist item
- **references/secrets-scanning.md** - Guide to scanning for exposed secrets in git history
- **references/ci-cd-best-practices.md** - GitHub Actions and GitLab CI pipeline best practices
