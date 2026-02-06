---
name: review
scope: universal
description: |
  Systematic code review checklist and pre-commit quality gates for PRs.
  Use when: reviewing pull requests, checking code quality, before committing code.
  Keywords: review, PR, pull request, checklist, quality, commit, 審查, 檢查, 簽入.
---

# Code Review Assistant

> **Language**: English | [繁體中文](../../locales/zh-TW/skills/code-review-assistant/SKILL.md)

**Version**: 1.0.0
**Last Updated**: 2025-12-24
**Applicability**: Claude Code Skills

---

> **Core Standard**: This skill implements [Code Review Checklist](../../core/code-review-checklist.md). For comprehensive methodology documentation, refer to the core standard.

## Purpose

This skill provides systematic checklists for code review and pre-commit verification.

## Quick Reference

### Comment Prefixes

| Prefix | Meaning | Action Required |
|--------|---------|------------------|
| **❗ BLOCKING** | Must fix before merge | 🔴 Required |
| **⚠️ IMPORTANT** | Should fix, but not blocking | 🟡 Recommended |
| **💡 SUGGESTION** | Nice-to-have improvement | 🟢 Optional |
| **❓ QUESTION** | Need clarification | 🔵 Discuss |
| **📝 NOTE** | Informational, no action | ⚪ Informational |

### Review Checklist Categories

1. **Functionality** - Does it work?
2. **Design** - Right architecture?
3. **Quality** - Clean code?
4. **Readability** - Easy to understand?
5. **Tests** - Adequate coverage?
6. **Security** - No vulnerabilities?
7. **Performance** - Efficient?
8. **Errors** - Properly handled?
9. **Docs** - Updated?
10. **Dependencies** - Necessary?

### Pre-Commit Checklist

- [ ] Build succeeds (zero errors, zero warnings)
- [ ] All tests pass
- [ ] Code follows project standards
- [ ] No security vulnerabilities
- [ ] Documentation updated
- [ ] Branch synced with target

## Detailed Guidelines

For complete standards, see:
- [Review Checklist](./review-checklist.md)
- [Pre-Commit Checklist](./checkin-checklist.md)

### AI-Optimized Format (Token-Efficient)

For AI assistants, use the YAML format file for reduced token usage:
- Base standard: `ai/standards/code-review.ai.yaml`

## Example Review Comments

```markdown
❗ BLOCKING: Potential SQL injection vulnerability here.
Please use parameterized queries instead of string concatenation.

⚠️ IMPORTANT: This method is doing too much (120 lines).
Consider extracting validation logic to a separate method.

💡 SUGGESTION: Consider using a Map here instead of an array for O(1) lookup.

❓ QUESTION: Why are we using setTimeout here instead of async/await?

📝 NOTE: This is a clever solution! Nice use of reduce here.
```

## Core Principles

1. **Be Respectful** - Review code, not the person
2. **Be Thorough** - Check functionality, not just syntax
3. **Be Timely** - Review within 24 hours
4. **Be Clear** - Explain WHY, not just WHAT

---

## Checkin Quality Gates (YAML Compressed)

```yaml
# === MANDATORY CHECKLIST ===
build:
  - code_compiles: "zero errors, zero warnings"
  - dependencies: "all installed, versions locked"
  verify: "run build locally, exit code 0"

test:
  - existing_pass: "100% pass rate (unit/integration/e2e)"
  - new_code_tested: "features→tests, bugfix→regression"
  - coverage: "not decreased, critical paths tested"
  verify: "run all suites, review coverage report"

quality:
  - standards: "naming, formatting, comments"
  - no_smells: "methods≤50 lines, nesting≤3, complexity≤10, no duplication"
  - security: "no hardcoded secrets, no SQLi, no XSS, no insecure deps"
  verify: "run linter, static analysis, security scanner"

docs:
  - api_docs: "public APIs documented"
  - readme: "updated if needed"
  - changelog: "user-facing changes → [Unreleased]"

workflow:
  - branch_naming: "feature/, fix/, docs/, chore/"
  - commit_message: "conventional commits format"
  - synced: "merged/rebased with target branch"

# === NEVER COMMIT WHEN ===
blockers:
  - "Build has errors"
  - "Tests failing"
  - "Feature incomplete (would break functionality)"
  - "Contains WIP/TODO in critical logic"
  - "Contains debugging code (console.log, print)"
  - "Contains commented-out code blocks"

# === COMMIT TIMING ===
good_times:
  - "Completed functional unit"
  - "Specific bug fixed with regression test"
  - "Independent refactor (all tests pass)"
  - "Runnable state"

bad_times:
  - "Build failures"
  - "Test failures"
  - "Incomplete features"
  - "Experimental code with TODOs"

# === GRANULARITY ===
ideal_size:
  files: "1-10 (split if >10)"
  lines: "50-300"
  scope: "single concern"

split_principle:
  combine: ["feature + its tests", "tightly related multi-file"]
  separate: ["Feature A + Feature B", "refactor + new feature", "bugfix + incidental refactor"]
```

---

## Configuration Detection

This skill supports project-specific configuration.

### Detection Order

1. Check `CONTRIBUTING.md` for "Disabled Skills" section
   - If this skill is listed, it is disabled for this project
2. Check `CONTRIBUTING.md` for "Code Review Language" section
3. If not found, **default to English**

### First-Time Setup

If no configuration found and context is unclear:

1. Ask the user: "This project hasn't configured code review language. Which option would you like? (English / 中文)"
2. After user selection, suggest documenting in `CONTRIBUTING.md`:

```markdown
## Code Review Language

This project uses **[chosen option]** for code review comments.
<!-- Options: English | 中文 -->
```

### Configuration Example

In project's `CONTRIBUTING.md`:

```markdown
## Code Review Language

This project uses **English** for code review comments.
<!-- Options: English | 中文 -->

### Comment Prefixes
BLOCKING, IMPORTANT, SUGGESTION, QUESTION, NOTE
```

---

## Related Standards

- [Code Review Checklist](../../core/code-review-checklist.md) - Core code review standard
- [Checkin Standards](../../core/checkin-standards.md) - Pre-commit quality gates
- [Testing Standards](../../core/testing-standards.md) - Testing requirements

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-24 | Added: Standard sections (Purpose, Related Standards, Version History, License) |

---

## License

This skill is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

**Source**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)
