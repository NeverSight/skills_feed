---
name: versioning
description: Use when releasing, tagging, or bumping versions. Defines semver rules and keeps package.json/pyproject.toml synced with git tags.
---

# Versioning

Semantic versioning rules and workflow for consistent releases.

## Semver Rules

Format: `MAJOR.MINOR.PATCH` (e.g., `1.4.2`)

| Bump | When | Examples |
|------|------|----------|
| **MAJOR** | Breaking changes | API removed, incompatible changes, major rewrites |
| **MINOR** | New features (backward compatible) | New endpoint, new option, new capability |
| **PATCH** | Bug fixes (backward compatible) | Fix crash, fix typo, fix edge case |

### Decision Tree

```
Is it a breaking change?
├── Yes → MAJOR
└── No → Does it add new functionality?
    ├── Yes → MINOR
    └── No → PATCH
```

### What Counts as Breaking?

**MAJOR (breaking):**
- Removing a public function/endpoint
- Changing function signature (required params)
- Changing return type
- Renaming exports
- Dropping support for runtime/dependency

**MINOR (feature):**
- Adding new function/endpoint
- Adding optional parameter
- New configuration option
- Performance improvement with no API change

**PATCH (fix):**
- Bug fix
- Documentation fix
- Internal refactor (no API change)
- Dependency update (non-breaking)

## Version Sync Workflow

**Keep these in sync:**
1. `package.json` version (JS/TS projects)
2. `pyproject.toml` version (Python projects)
3. Git tag

### Release Workflow

```bash
# 1. Update version in manifest
# package.json: "version": "1.2.0"
# OR pyproject.toml: version = "1.2.0"

# 2. Commit the version bump
git add package.json  # or pyproject.toml
git commit -m "chore: bump version to 1.2.0"

# 3. Tag the commit
git tag -a v1.2.0 -m "Release 1.2.0: [brief description]"

# 4. Push with tags
git push && git push --tags
```

### Pre-release Versions

For work-in-progress releases:
- `1.2.0-alpha.1` - Early testing
- `1.2.0-beta.1` - Feature complete, testing
- `1.2.0-rc.1` - Release candidate

## Common Mistakes

| Mistake | Correct |
|---------|---------|
| Bumping MAJOR for new feature | MINOR (if backward compatible) |
| Bumping PATCH for new option | MINOR (it's new functionality) |
| Forgetting to tag | Always tag after version bump |
| Tag without version update | Update manifest first, then tag |
| Inconsistent tag format | Always use `v` prefix: `v1.2.0` |

## Quick Reference

```bash
# Check current version
node -p "require('./package.json').version"
# or
grep version pyproject.toml

# List tags
git tag -l

# See what changed since last tag
git log $(git describe --tags --abbrev=0)..HEAD --oneline
```
