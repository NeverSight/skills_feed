---
name: xunit
description: |
  Writes unit tests with xUnit framework across 30 test projects.
  Use when: writing new tests, adding test coverage, creating integration tests, setting up test fixtures, or debugging test failures.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, mcp__context7__resolve-library-id, mcp__context7__query-docs
---

# xUnit Skill

xUnit 2.9.3 is the testing framework for all 30 test projects in Sorcha. Tests use **FluentAssertions** for readable assertions and **Moq** for mocking. All tests follow strict `MethodName_Scenario_ExpectedBehavior` naming.

## Quick Start

### Unit Test Structure

```csharp
// SPDX-License-Identifier: MIT
// Copyright (c) 2025 Sorcha Contributors

public class WalletManagerTests
{
    private readonly Mock<IRepository<Wallet>> _mockRepository;
    private readonly WalletManager _sut;

    public WalletManagerTests()
    {
        _mockRepository = new Mock<IRepository<Wallet>>();
        _sut = new WalletManager(_mockRepository.Object);
    }

    [Fact]
    public async Task CreateAsync_ValidWallet_ReturnsSuccess()
    {
        // Arrange
        var wallet = new Wallet { Name = "Test" };
        _mockRepository.Setup(r => r.AddAsync(wallet)).ReturnsAsync(wallet);

        // Act
        var result = await _sut.CreateAsync(wallet);

        // Assert
        result.IsSuccess.Should().BeTrue();
        result.Value.Should().Be(wallet);
    }
}
```

### Theory with InlineData

```csharp
[Theory]
[InlineData(12)]
[InlineData(15)]
[InlineData(18)]
[InlineData(21)]
[InlineData(24)]
public void GenerateMnemonic_ValidWordCount_ReturnsCorrectLength(int wordCount)
{
    var result = _keyManager.GenerateMnemonic(wordCount);

    result.IsSuccess.Should().BeTrue();
    result.Value!.Split(' ').Should().HaveCount(wordCount);
}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| `[Fact]` | Single test case | `[Fact] public void Method_Test() {}` |
| `[Theory]` | Parameterized tests | `[Theory] [InlineData(1)] public void Method(int x) {}` |
| `IClassFixture<T>` | Per-class shared state | `class Tests : IClassFixture<DbFixture>` |
| `ICollectionFixture<T>` | Cross-class shared state | `[Collection("Db")] class Tests` |
| `IAsyncLifetime` | Async setup/teardown | `Task InitializeAsync()`, `Task DisposeAsync()` |

## Common Patterns

### Exception Testing

```csharp
[Fact]
public void Constructor_NullRepository_ThrowsArgumentNullException()
{
    var act = () => new WalletManager(null!);

    act.Should().Throw<ArgumentNullException>()
        .WithParameterName("repository");
}

[Fact]
public async Task ProcessAsync_InvalidData_ThrowsWithMessage()
{
    var exception = await Assert.ThrowsAsync<InvalidOperationException>(
        () => _processor.ProcessAsync(invalidContext));

    exception.Message.Should().Contain("validation failed");
}
```

### Async Test Pattern

```csharp
[Fact]
public async Task ExecuteAsync_ValidBlueprint_CompletesSuccessfully()
{
    // Arrange
    var blueprint = CreateTestBlueprint();

    // Act
    var result = await _engine.ExecuteAsync(blueprint);

    // Assert
    result.Success.Should().BeTrue();
    result.ProcessedData.Should().ContainKey("output");
}
```

## See Also

- [patterns](references/patterns.md) - Test patterns and anti-patterns
- [workflows](references/workflows.md) - Test workflows and fixtures

## Related Skills

- See the **fluent-assertions** skill for assertion patterns
- See the **moq** skill for mocking dependencies
- See the **entity-framework** skill for database testing with InMemory provider
- See the **postgresql** skill for Testcontainers integration tests

## Documentation Resources

> Fetch latest xUnit documentation with Context7.

**How to use Context7:**
1. Use `mcp__context7__resolve-library-id` to search for "xunit"
2. Query with `mcp__context7__query-docs` using the resolved library ID

**Library ID:** `/xunit/xunit.net` _(875 code snippets, High reputation)_

**Recommended Queries:**
- "xUnit Theory InlineData patterns"
- "IClassFixture ICollectionFixture shared context"
- "IAsyncLifetime async setup teardown"
- "xUnit parallel test execution configuration"