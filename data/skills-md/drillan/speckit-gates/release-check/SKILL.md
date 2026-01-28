---
name: release-check
description: >
  Validates all artifacts are complete and consistent for release.
  Checks spec kit artifacts, documentation, versioning, and API docs.
  Run before creating a release to ensure nothing is missing.
version: 0.0.1
license: MIT
compatibility: Requires spec kit artifacts
metadata:
  author: drillan
  category: quality-gate
  repository: https://github.com/drillan/speckit-gates
---

# release-check

Validates release readiness before creating a release.

## Purpose

This skill validates that all artifacts are complete and consistent for release:

- **Spec kit artifacts**: spec.md, plan.md, tasks.md exist and are complete
- **Documentation**: README.md, CHANGELOG.md have required sections
- **Versioning**: Version numbers are consistent across package.json and CHANGELOG
- **API docs**: API documentation matches contract specifications

## Output

The skill outputs a **ReleaseChecklist** with:

- Overall readiness status (Ready/Not Ready)
- Individual check items with pass/fail/skip status
- Version consistency information
- Specific issues to address before release

## Usage

This is a manual skill - run it before creating a release:

```bash
npx skills run release-check
```

Or via AI agent:
```
User: Check if we're ready for release
```

## Exit Codes

| Code | Status | Meaning |
|------|--------|---------|
| 0 | Ready | All checks pass |
| 1 | Not Ready | Some checks failed |
| 3 | Error | Required files missing |

## Checks Performed

### Artifact Checks (FR-022)

| Check | Requirement |
|-------|-------------|
| spec.md exists | Required |
| plan.md exists | Required |
| tasks.md exists | Required |
| All tasks complete | Required |

### Documentation Checks (FR-023)

| Check | Requirement |
|-------|-------------|
| README.md exists | Required |
| README.md has usage section | Required |
| CHANGELOG.md exists | Required |
| CHANGELOG.md has unreleased section | Required |

### Version Checks (FR-026)

| Check | Requirement |
|-------|-------------|
| package.json version present | Optional |
| CHANGELOG.md version present | Optional |
| Versions match | If both present |

### API Checks (FR-025)

| Check | Requirement |
|-------|-------------|
| contracts/ exists | Optional |
| API docs exist if contracts | Required if contracts |
| Endpoints documented | Required if contracts |

## Checklist Output Format

```
## Release Checklist

**Status**: Ready to Release / Not Ready

### Artifacts
| Status | Check | Details |
|--------|-------|---------|
| [PASS] | spec.md exists | |
| [PASS] | plan.md exists | |
| [FAIL] | All tasks complete | 5 tasks remaining |

### Documentation
| Status | Check | Details |
|--------|-------|---------|
| [PASS] | README.md exists | |
| [SKIP] | API docs | No contracts/ directory |
```

## Recommendations

If release check fails:

1. Complete all remaining tasks in tasks.md
2. Ensure README.md has a usage section
3. Update CHANGELOG.md with release notes
4. Verify version numbers are consistent
5. Run release-check again to verify fixes
