---
name: test-audit
description: Audit test suites (unit, integration, feature/E2E) for correctness, quality, and best practices. Use when the user wants to review, audit, validate, or improve tests in any programming language or framework (Jest, pytest, RSpec, JUnit, PHPUnit, etc.). Triggers on requests like "audit my tests", "review test quality", "check my test coverage", "are my tests good", or any request to evaluate test effectiveness.
license: MIT
metadata:
  version: "1.0.0"
---

# Test Suite Audit

Audit tests for correctness, quality, and adherence to best practices.

## Step 1: Clarify Scope

**Always ask the user before proceeding:**

> Would you like me to audit:
> 1. **A specific file** — Provide the path to the test file
> 2. **Only changed files** — I'll audit tests in the diff against `main` (new or modified tests)
> 3. **The entire project** — I'll scan for all test files in the codebase
>
> Which would you prefer?

Wait for the user's response before continuing.

## Step 2: Gather Context

Identify:
- **Language and framework** — Jest, pytest, RSpec, JUnit, PHPUnit, etc.
- **Test type** — unit, integration, or feature/E2E
- **Code under test** — locate and review if available
- **Project conventions** — infer from existing tests, config, or docs

Use the project's conventions and tooling to locate test files:

| Framework | Test Location | Config | Naming Pattern |
|-----------|---------------|--------|----------------|
| **Jest** | `__tests__/`, `*.test.js` | `jest.config.js` | `*.test.js`, `*.spec.js` |
| **Vitest** | `__tests__/`, `*.test.ts` | `vitest.config.ts` | `*.test.ts`, `*.spec.ts` |
| **Mocha** | `test/` | `.mocharc.js`, `mocha.opts` | `*.test.js`, `*.spec.js` |
| **Go** | Same as source | `go.mod` | `*_test.go` |
| **Rust** | `src/`, `tests/` | `Cargo.toml` | `mod tests`, `tests/*.rs` |
| **JUnit/Java** | `src/test/java/` | `pom.xml`, `build.gradle` | `*Test.java`, `*Tests.java` |
| **C# (xUnit/NUnit)** | `*.Tests/` project | `*.csproj` | `*Tests.cs`, `*Test.cs` |
| **PHP (PHPUnit)** | `tests/` | `phpunit.xml` | `*Test.php` |
| **Laravel** | `tests/Unit/`, `tests/Feature/` | `phpunit.xml` | `*Test.php` |
| **Symfony** | `tests/` | `phpunit.xml.dist` | `*Test.php` |
| **Ruby (RSpec)** | `spec/` | `.rspec`, `spec_helper.rb` | `*_spec.rb` |
| **Rails** | `spec/` or `test/` | `.rspec`, `rails_helper.rb` | `*_spec.rb`, `*_test.rb` |
| **Django** | `tests/`, `*/tests.py` | `pytest.ini`, `setup.cfg` | `test_*.py`, `*_test.py` |

Also check for:
- Package manager scripts (`composer test`, `bundle exec rspec`, `python manage.py test`)
- CI configuration files for test commands

## Step 3: Apply Audit Criteria

See `references/audit-criteria.md` for the complete checklist covering:
- Test validity
- Assertion quality
- Test isolation
- Naming and structure (including AAA enforcement)
- Coverage quality
- Maintainability
- Framework conventions

## Step 4: Report Findings

For each issue:

```
### [HIGH | MEDIUM | LOW] Issue Title

**File**: `path/to/test_file.ext`
**Test**: `test name`
**Lines**: X–Y

**Problem**: What's wrong

**Current**:
[code snippet]

**Fix**:
[corrected code]

**Why**: One-sentence rationale
```

## Step 5: Summarize

Conclude with:

1. **Critical issues** — false positives, tests that verify nothing
2. **Quality issues** — weak assertions, missing edge cases
3. **Style issues** — naming, organization, minor fixes
4. **Overall health** — one paragraph assessment
5. **Top 3–5 priorities** — highest-impact improvements
