---
name: unit-testing
description: Write comprehensive unit tests for code. Use when asked to (1) write tests for new or existing code, (2) add unit tests, (3) test a function/module/class, (4) verify code still works after changes, (5) create test coverage, or when phrases like "write tests", "add tests", "test this", "make sure this works" appear. Supports Python, JavaScript, R, Rust, Go, C++, SQL, Bash, Ansible, Kubernetes/Kustomize, Docker, and Docker Compose.
---

# Unit Testing Skill

Write comprehensive unit tests with full coverage: happy paths, edge cases, and error conditions.

## Core Principles

1. **Test behavior, not implementation** - Tests verify what code does, not how
2. **One assertion concept per test** - Each test validates a single logical behavior
3. **Arrange-Act-Assert structure** - Setup, execute, verify
4. **Descriptive test names** - Name describes scenario and expected outcome
5. **Independent tests** - No test depends on another's state or execution order
6. **Fast tests** - Mock expensive operations (network, disk, databases) unless integration testing

## Workflow

### 0. MANDATORY: Use context7 Before Writing Tests

**CRITICAL**: Before writing ANY tests, use context7 to look up current testing framework documentation and best practices.

**Always use context7 to verify:**
- Testing framework APIs (Jest, Vitest, pytest, etc.)
- Assertion syntax and available matchers
- Mocking/stubbing patterns
- Testing library utilities (React Testing Library, etc.)
- Framework-specific best practices

**Process:**
1. Identify testing framework and libraries in use
2. Use `context7 resolve <framework>` for each
3. Query relevant topics: assertions, mocking, async testing, etc.
4. Review docs before writing test code

**Example:**
```
context7 resolve vitest
context7 get-library-docs --library vitest --topic "mocking"
context7 resolve @testing-library/react
context7 get-library-docs --library @testing-library/react --topic "async"
```

### Workflow Steps

1. **Use context7 for testing framework docs** - Look up current API and patterns
2. **Analyze the code** - Identify public interfaces, dependencies, edge cases, error conditions
3. **Determine test scope** - Unit tests for functions/classes, integration tests for interactions
4. **Check existing structure** - Follow project's existing test organization patterns
5. **Select appropriate framework** - See language-specific references below
6. **Write comprehensive tests** covering:
   - Happy path (expected inputs produce expected outputs)
   - Edge cases (empty inputs, boundaries, null/None values)
   - Error conditions (invalid inputs, exceptions, failure modes)
   - State changes (side effects, mutations)

## context7 Usage by Language/Framework

Before writing tests, use context7 to look up documentation for:

| Language/Framework | context7 Libraries to Query |
|-------------------|----------------------------|
| JavaScript/React | `react`, `vitest` or `jest`, `@testing-library/react` |
| Python | `pytest`, relevant libraries being tested |
| R | `testthat`, `tidyverse` |
| Rust | `rust` (built-in testing) |
| Go | `go` (testing package) |
| C++ | `googletest` or `gtest` |
| Node.js/Express | `express`, `supertest`, `jest` |

**Common topics to query:**
- "mocking", "assertions", "async testing", "setup teardown"
- "matchers", "fixtures", "test coverage", "integration tests"

## Language References

Select the appropriate reference based on the code being tested:

| Language/Tool | Reference | Framework |
|---------------|-----------|-----------|
| Python | [python.md](references/python.md) | pytest |
| JavaScript | [javascript.md](references/javascript.md) | Jest / Vitest |
| R | [r.md](references/r.md) | testthat |
| Rust | [rust.md](references/rust.md) | built-in #[test] |
| Go | [go.md](references/go.md) | testing + testify |
| C++ | [cpp.md](references/cpp.md) | Google Test |
| SQL (PostgreSQL) | [sql.md](references/sql.md) | pgTAP |
| Bash | [bash.md](references/bash.md) | bats-core |
| Ansible | [ansible.md](references/ansible.md) | Molecule + ansible-lint |
| Kubernetes/Kustomize | [kubernetes.md](references/kubernetes.md) | kubeconform + conftest |
| Docker | [docker.md](references/docker.md) | hadolint + container-structure-test |

## Test Organization

Follow each language's conventions. When a project has existing tests, match their structure.

## Mocking Strategy

Mock external dependencies based on context:
- **Always mock**: Network calls, external APIs, system time
- **Consider mocking**: Databases (use test DB or mock based on test type), file system
- **Rarely mock**: Pure functions, data transformations

## Coverage Targets

Aim for comprehensive coverage:
- All public functions/methods
- All code branches (if/else, match arms, error handlers)
- Boundary conditions
- Error handling paths

## REMINDER: Always Use context7

**Before writing any test code:**
1. Use context7 to look up the testing framework's current API
2. Verify assertion syntax and available matchers
3. Check mocking/stubbing best practices
4. Review async testing patterns if needed

**Never write tests from memory alone** - always verify with current documentation using context7.
