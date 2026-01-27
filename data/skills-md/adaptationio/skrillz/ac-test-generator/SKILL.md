---
name: ac-test-generator
description: Generate tests for features using TDD approach. Use when creating test files, generating test cases, implementing RED phase of TDD, or scaffolding test infrastructure.
---

# AC Test Generator

Generate test files and test cases following TDD principles.

## Purpose

Implements the RED phase of TDD by generating failing tests before implementation, ensuring all features have comprehensive test coverage.

## Quick Start

```python
from scripts.test_generator import TestGenerator

generator = TestGenerator(project_dir)
tests = await generator.generate_for_feature(feature)
await generator.write_test_file(tests)
```

## Generated Test Structure

```python
# tests/test_auth_001.py
"""Tests for feature auth-001: User can register"""

import pytest
from app.auth import register_user

class TestUserRegistration:
    """Test suite for user registration."""

    def test_valid_registration_creates_user(self):
        """Valid registration creates user in database."""
        # Arrange
        email = "test@example.com"
        password = "SecurePass123!"

        # Act
        result = register_user(email, password)

        # Assert
        assert result.success
        assert result.user.email == email

    def test_duplicate_email_returns_error(self):
        """Duplicate email registration returns error."""
        # Arrange - create existing user
        # Act - try to register same email
        # Assert - error returned
        pass

    def test_weak_password_rejected(self):
        """Weak password is rejected with message."""
        pass
```

## Test Types

### Unit Tests
- Test individual functions
- Mock dependencies
- Fast execution
- High coverage

### Integration Tests
- Test component interactions
- Real dependencies
- Database transactions
- API endpoints

### E2E Tests
- Full user workflows
- Browser automation
- Real environment
- Acceptance criteria

## Configuration

```json
{
  "test_framework": "pytest",
  "coverage_target": 80,
  "test_patterns": {
    "unit": "tests/unit/",
    "integration": "tests/integration/",
    "e2e": "tests/e2e/"
  },
  "fixtures": "tests/fixtures/"
}
```

## Workflow

1. **Analyze**: Read feature and test cases
2. **Scaffold**: Create test file structure
3. **Generate**: Write test functions
4. **Validate**: Ensure tests fail (RED)
5. **Report**: Output test locations

## TDD Integration

```
RED   → ac-test-generator creates failing tests
GREEN → Claude implements minimum code to pass
REFACTOR → Code cleaned while tests pass
```

## API Reference

See `scripts/test_generator.py` for full implementation.
