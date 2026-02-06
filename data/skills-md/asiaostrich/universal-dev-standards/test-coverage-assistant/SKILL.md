---
name: coverage
scope: partial
description: |
  Evaluate test completeness using the 8 dimensions framework.
  Use when: writing tests, reviewing test coverage, ensuring test quality.
  Keywords: test coverage, completeness, dimensions, 8 dimensions, test quality, AI test quality, 測試覆蓋, 測試完整性, 八維度.
---

# Test Coverage Assistant

> **Language**: English | [繁體中文](../../locales/zh-TW/skills/test-coverage-assistant/SKILL.md)

**Version**: 1.1.0
**Last Updated**: 2026-01-25
**Applicability**: Claude Code Skills

---

## Purpose

This skill helps evaluate and improve test completeness using the 8 dimensions framework, ensuring comprehensive test coverage for each feature.

## Quick Reference

### The 8 Dimensions

```
┌─────────────────────────────────────────────────────────────┐
│              Test Completeness = 8 Dimensions                │
├─────────────────────────────────────────────────────────────┤
│  1. Happy Path        Normal expected behavior              │
│  2. Boundary          Min/max values, limits                │
│  3. Error Handling    Invalid input, exceptions             │
│  4. Authorization     Role-based access control             │
│  5. State Changes     Before/after verification             │
│  6. Validation        Format, business rules                │
│  7. Integration       Real query verification               │
│  8. AI Generation     AI-generated test quality (NEW)       │
└─────────────────────────────────────────────────────────────┘
```

### Dimension Summary Table

| # | Dimension | What to Test | Key Question |
|---|-----------|--------------|--------------|
| 1 | **Happy Path** | Valid input → expected output | Does the normal flow work? |
| 2 | **Boundary** | Min/max values, limits | What happens at edges? |
| 3 | **Error Handling** | Invalid input, not found | How do errors behave? |
| 4 | **Authorization** | Role permissions | Who can do what? |
| 5 | **State Changes** | Before/after states | Did the state change correctly? |
| 6 | **Validation** | Format, business rules | Is input validated? |
| 7 | **Integration** | Real DB/API calls | Does the query really work? |
| 8 | **AI Generation** | AI-generated test quality | Are AI tests meaningful? |

### When to Apply Each Dimension

| Feature Type | Required Dimensions |
|--------------|---------------------|
| CRUD API | 1, 2, 3, 4, 6, 7, 8* |
| Query/Search | 1, 2, 3, 4, 7, 8* |
| State Machine | 1, 3, 4, 5, 6, 8* |
| Validation Logic | 1, 2, 3, 6, 8* |
| Background Job | 1, 3, 5, 8* |
| External Integration | 1, 3, 7, 8* |

*Dimension 8 (AI Generation Quality) applies when tests are AI-generated

## Test Design Checklist

Use this checklist for each feature:

```
Feature: ___________________

□ Happy Path
  □ Valid input produces expected success
  □ Correct data is returned/created
  □ Side effects occur as expected

□ Boundary Conditions
  □ Minimum valid value
  □ Maximum valid value
  □ Empty collection
  □ Single item collection
  □ Large collection (if applicable)

□ Error Handling
  □ Invalid input format
  □ Missing required fields
  □ Duplicate/conflict scenarios
  □ Not found scenarios
  □ External service failure (if applicable)

□ Authorization
  □ Each permitted role tested
  □ Each denied role tested
  □ Unauthenticated access tested
  □ Cross-boundary access tested

□ State Changes
  □ Initial state verified
  □ Final state verified
  □ All valid state transitions tested

□ Validation
  □ Format validation (email, phone, etc.)
  □ Business rule validation
  □ Cross-field validation

□ Integration (if UT uses wildcards)
  □ Query predicates verified
  □ Entity relationships verified
  □ Pagination verified
  □ Sorting/filtering verified

□ AI Generation Quality (if AI-generated)
  □ Tests verify meaningful behavior
  □ Assertions are specific (not just "not null")
  □ Tests are independent and self-contained
  □ Mutation score > 80% (if evaluated)
```

## Detailed Guidelines

For complete standards, see:
- [Test Completeness Dimensions](../../core/test-completeness-dimensions.md)
- [Testing Standards](../../core/testing-standards.md)

### AI-Optimized Format (Token-Efficient)

For AI assistants, use the YAML format files for reduced token usage:
- Base standard: `ai/standards/test-completeness-dimensions.ai.yaml`

## Examples

### 1. Happy Path

```csharp
[Fact]
public async Task CreateUser_WithValidData_ReturnsSuccess()
{
    // Arrange
    var request = new CreateUserRequest
    {
        Username = "newuser",
        Email = "user@example.com"
    };

    // Act
    var result = await _service.CreateUserAsync(request);

    // Assert
    result.Success.Should().BeTrue();
    result.Data.Username.Should().Be("newuser");
}
```

### 2. Boundary

```csharp
[Theory]
[InlineData(0, false)]      // Below minimum
[InlineData(1, true)]       // Minimum valid
[InlineData(100, true)]     // Maximum valid
[InlineData(101, false)]    // Above maximum
public void ValidateQuantity_BoundaryValues_ReturnsExpected(
    int quantity, bool expected)
{
    var result = _validator.IsValidQuantity(quantity);
    result.Should().Be(expected);
}
```

### 4. Authorization

```csharp
[Fact]
public async Task DeleteUser_AsAdmin_Succeeds()
{
    var adminContext = CreateContext(role: "Admin");
    var result = await _service.DeleteUserAsync(userId, adminContext);
    result.Success.Should().BeTrue();
}

[Fact]
public async Task DeleteUser_AsMember_ReturnsForbidden()
{
    var memberContext = CreateContext(role: "Member");
    var result = await _service.DeleteUserAsync(userId, memberContext);
    result.ErrorCode.Should().Be("FORBIDDEN");
}
```

### 5. State Changes

```csharp
[Fact]
public async Task DisableUser_UpdatesStateCorrectly()
{
    // Arrange
    var user = await CreateEnabledUser();
    user.IsEnabled.Should().BeTrue();  // Verify initial state

    // Act
    await _service.DisableUserAsync(user.Id);

    // Assert
    var updatedUser = await _repository.GetByIdAsync(user.Id);
    updatedUser.IsEnabled.Should().BeFalse();  // Verify final state
}
```

## Authorization Matrix Template

Create a matrix for each feature:

| Operation | Admin | Manager | Member | Guest |
|-----------|-------|---------|--------|-------|
| Create | ✅ | ✅ | ❌ | ❌ |
| Read All | ✅ | ⚠️ Scoped | ❌ | ❌ |
| Update | ✅ | ⚠️ Own dept | ❌ | ❌ |
| Delete | ✅ | ❌ | ❌ | ❌ |

Each cell should have a corresponding test case.

## Anti-Patterns to Avoid

- ❌ Testing only happy path
- ❌ Missing authorization tests for multi-role systems
- ❌ Not verifying state changes
- ❌ Using wildcards in UT without corresponding IT
- ❌ Same values for ID and business identifier in test data
- ❌ Testing implementation details instead of behavior
- ❌ Accepting AI-generated tests without review
- ❌ Assuming high line coverage means effective tests

---

## Configuration Detection

This skill supports project-specific configuration.

### Detection Order

1. Check `CONTRIBUTING.md` for "Testing Standards" section
2. Check for existing test patterns in the codebase
3. If not found, **default to all 8 dimensions** (dimension 8 only when tests are AI-generated)

### First-Time Setup

If no configuration found:

1. Suggest: "This project hasn't configured test completeness requirements. Would you like to customize which dimensions are required?"
2. Suggest documenting in `CONTRIBUTING.md`:

```markdown
## Test Completeness

We use the 8 Dimensions framework for test coverage.

### Required Dimensions by Feature Type
- API endpoints: All 8 dimensions (8 only when AI-generated)
- Utility functions: Dimensions 1, 2, 3, 6, 8*
- Background jobs: Dimensions 1, 3, 5, 8*

*Dimension 8 applies when tests are AI-generated
```

---

## Related Standards

- [Test Completeness Dimensions](../../core/test-completeness-dimensions.md)
- [Testing Standards](../../core/testing-standards.md)
- [Testing Guide](../testing-guide/SKILL.md)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | 2026-01-25 | Updated: 7 dimensions → 8 dimensions (added AI Generation Quality) |
| 1.0.0 | 2025-12-30 | Initial release |

---

## License

This skill is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

**Source**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)
