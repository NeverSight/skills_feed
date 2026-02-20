---
name: test-first
description: >-
  Guide for Test-First (Test-Driven) Development. Focuses on writing tests before 
  implementation, ensuring comprehensive coverage and clear requirements. 
  Covers test design, edge cases, and the Arrange-Act-Assert structure.
---

# Test-First Development Skill

Test-First Development (TDD) ensures that code is written to satisfy specific, predefined requirements, leading to higher quality and better design.

## TDD Workflow

1. **Red**: Write a failing test for a small piece of functionality.
2. **Green**: Write the minimum amount of code required to make the test pass.
3. **Refactor**: Clean up the code while ensuring the tests remain green.

## Test Design Principles

### 1. Comprehensive Coverage
- **Normal Cases**: Test the expected "happy path" behavior.
- **Boundary Values**: Test inputs at the edges of valid ranges (e.g., 0, max_int, empty strings).
- **Edge Cases**: Test unusual or extreme conditions (e.g., network timeout, disk full, null values).
- **Error Handling**: Verify that the system fails gracefully and returns appropriate error messages.

### 2. Structure (Arrange-Act-Assert)
Follow the AAA pattern for clear and maintainable tests:
- **Arrange**: Set up the necessary preconditions and inputs.
- **Act**: Execute the function or method being tested.
- **Assert**: Verify that the outcome matches the expectation.

## Best Practices

- **One Assertion per Test**: Aim to test a single concept per test case.
- **Descriptive Naming**: Name tests clearly (e.g., `test_should_reject_invalid_api_key`).
- **Independence**: Ensure tests do not depend on each other or on a specific execution order.
- **Fast Execution**: Keep unit tests fast to encourage frequent execution.
