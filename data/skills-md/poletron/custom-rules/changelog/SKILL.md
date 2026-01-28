---
name: changelog
description: >
  Guidelines for maintaining changelogs based on Keep a Changelog format.
  Trigger: When writing or updating CHANGELOG.md files.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with changelog"

## When to Use

Use this skill when:
- Creating or updating CHANGELOG.md
- Documenting version releases
- Following semantic versioning
- Writing user-facing change descriptions

---

## Critical Patterns

### Structure (REQUIRED)

```markdown
# Changelog

All notable changes will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- New features

### Changed
- Changes to existing functionality

### Fixed
- Bug fixes

## [1.2.0] - 2024-01-15

### Added
- Multi-language support ([#123](link))
```

### Change Types (REQUIRED)

```
Added      → New features, endpoints, options
Changed    → Changes to existing functionality
Deprecated → Features planned for removal
Removed    → Deleted features
Fixed      → Bug fixes
Security   → Vulnerability patches
```

---

## Decision Tree

```
New feature?               → Added
Behavior change?           → Changed
Bug fix?                   → Fixed
Security patch?            → Security
Will be removed?           → Deprecated
Already removed?           → Removed
```

---

## Code Examples

### Good Entry

```markdown
### Added
- Email notifications for order status changes with customizable templates
- Batch processing support for up to 1000 items per request

### Fixed
- Race condition in payment processing that could cause duplicate charges
- Memory leak when uploading files larger than 100MB
```

### Bad Entry

```markdown
### Added
- New feature (too vague)
- Updated stuff (unclear)

### Fixed
- Fixed bug (which bug?)
```

---

## Best Practices

- Update changelog with every PR
- Write from the user's perspective
- Include issue/PR numbers for reference
- Date entries in ISO format (YYYY-MM-DD)
- Keep unreleased changes at the top
