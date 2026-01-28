---
name: moq
description: |
  Mocks dependencies in unit tests using Moq framework.
  Use when: writing unit tests, creating test doubles for interfaces, verifying method calls, mocking async operations
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, mcp__context7__resolve-library-id, mcp__context7__query-docs
---

# Moq Skill

Moq provides type-safe mocking for .NET unit tests. Sorcha uses Moq extensively across 30+ test projects to isolate components and verify interactions. The codebase favors constructor injection with mocks stored as `private readonly` fields.

## Quick Start

### Basic Mock Setup

```csharp
public class WalletManagerTests
{
    private readonly Mock<ICryptoModule> _mockCryptoModule;
    private readonly Mock<IHashProvider> _mockHashProvider;

    public WalletManagerTests()
    {
        _mockCryptoModule = new Mock<ICryptoModule>();
        _mockHashProvider = new Mock<IHashProvider>();
    }
}
```

### Async Method Mock

```csharp
_mockCryptoModule
    .Setup(x => x.GenerateKeySetAsync(
        It.IsAny<WalletNetworks>(),
        It.IsAny<byte[]>(),
        It.IsAny<CancellationToken>()))
    .ReturnsAsync(CryptoResult<KeySet>.Success(keySet));
```

### Verification

```csharp
_mockRegisterManager.Verify(
    m => m.CreateRegisterAsync("Test Register", "tenant-123", false, true, It.IsAny<CancellationToken>()),
    Times.Once);
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| `Mock<T>` | Create mock instance | `new Mock<IService>()` |
| `.Object` | Get mock instance | `_mock.Object` |
| `Mock.Of<T>()` | Quick mock for simple deps | `Mock.Of<ILogger<T>>()` |
| `Setup()` | Configure behavior | `.Setup(x => x.Method())` |
| `ReturnsAsync()` | Async return value | `.ReturnsAsync(result)` |
| `Callback()` | Capture arguments | `.Callback<T>((arg) => captured = arg)` |
| `Verify()` | Assert method called | `.Verify(x => x.Method(), Times.Once)` |
| `It.IsAny<T>()` | Match any argument | `It.IsAny<string>()` |
| `It.Is<T>()` | Match with predicate | `It.Is<T>(x => x.Id == 1)` |

## Common Patterns

### Logger Mock (Quick)

**When:** You need a logger but don't care about verifying logs.

```csharp
var service = new WalletManager(Mock.Of<ILogger<WalletManager>>());
```

### Options Pattern Mock

**When:** Injecting `IOptions<T>` dependencies.

```csharp
var mockConfig = new Mock<IOptions<PeerServiceConfiguration>>();
mockConfig.Setup(x => x.Value).Returns(new PeerServiceConfiguration { Enabled = true });
```

## See Also

- [patterns](references/patterns.md) - Detailed setup and verification patterns
- [workflows](references/workflows.md) - Test writing workflows and integration testing

## Related Skills

- See the **xunit** skill for test framework patterns
- See the **fluent-assertions** skill for assertion syntax
- See the **entity-framework** skill for mocking DbContext

## Documentation Resources

> Fetch latest Moq documentation with Context7.

**How to use Context7:**
1. Use `mcp__context7__resolve-library-id` to search for "moq"
2. Query with `mcp__context7__query-docs` using the resolved library ID

**Library ID:** `/devlooped/moq`

**Recommended Queries:**
- "moq setup verify async methods"
- "moq callbacks parameter capture"
- "moq argument matching It.Is"