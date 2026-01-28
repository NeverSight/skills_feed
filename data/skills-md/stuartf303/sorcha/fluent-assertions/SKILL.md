---
name: fluent-assertions
description: |
  Creates readable test assertions with FluentAssertions library.
  Use when: writing unit tests, integration tests, verifying object state, testing exceptions, asserting collections
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, mcp__context7__resolve-library-id, mcp__context7__query-docs
---

# FluentAssertions Skill

FluentAssertions provides a fluent interface for writing test assertions in C#. The Sorcha codebase uses it across 1,100+ tests with xUnit. All assertions follow the `subject.Should().BeX()` pattern.

## Quick Start

### Basic Value Assertions

```csharp
// Strings
wallet.Address.Should().NotBeNullOrEmpty();
blueprint.Title.Should().Be("Purchase Order");
error.Message.Should().Contain("validation");

// Numbers
blueprint.Version.Should().Be(5);
result.Count.Should().BeGreaterThan(0).And.BeLessThan(100);

// Booleans
result.IsSuccess.Should().BeTrue();
validation.IsValid.Should().BeFalse();
```

### Exception Testing

```csharp
// Sync exception testing
builder.Invoking(b => b.Build())
    .Should().Throw<InvalidOperationException>()
    .WithMessage("*title*");  // Wildcard matching

// Async exception testing
await Assert.ThrowsAsync<InvalidOperationException>(async () =>
    await _walletManager.CreateWalletAsync("Test", null!, "user1", "tenant1"));
```

### Collection Assertions

```csharp
blueprint.Participants.Should().HaveCount(2);
blueprint.Actions.Should().NotBeEmpty();
events.Should().ContainSingle(e => e is WalletCreatedEvent);
wallets.Should().AllSatisfy(w => w.Owner.Should().Be(owner));
docket.TransactionIds.Should().ContainInOrder("tx1", "tx2", "tx3");
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Should() | Entry point for all assertions | `value.Should().Be(expected)` |
| And | Chain multiple assertions | `.NotBeNull().And.HaveCount(2)` |
| Which/WhoseValue | Access nested values | `.ContainKey("x").WhoseValue.Should().Be("y")` |
| Invoking | Test sync exceptions | `obj.Invoking(x => x.Method())` |
| Awaiting | Test async exceptions | `obj.Awaiting(x => x.MethodAsync())` |

## Common Patterns

### Object Property Assertions

```csharp
wallet.Should().NotBeNull();
wallet.Name.Should().Be("Test Wallet");
wallet.Status.Should().Be(WalletStatus.Active);
wallet.Metadata.Should().ContainKey("environment").WhoseValue.Should().Be("production");
```

### Time-Based Assertions

```csharp
docket.TimeStamp.Should().BeCloseTo(DateTime.UtcNow, TimeSpan.FromSeconds(1));
blueprint.UpdatedAt.Should().BeOnOrAfter(beforeBuild).And.BeOnOrBefore(afterBuild);
```

### Validation Result Assertions

```csharp
result.Validation.IsValid.Should().BeTrue();
result.Errors.Should().BeEmpty();

// Or for failures
result.Success.Should().BeFalse();
result.Validation.Errors.Should().NotBeEmpty();
result.Errors.Should().Contain(e => e.Contains("validation"));
```

## See Also

- [patterns](references/patterns.md)
- [workflows](references/workflows.md)

## Related Skills

- See the **xunit** skill for test framework patterns
- See the **moq** skill for mocking dependencies in tests

## Documentation Resources

> Fetch latest FluentAssertions documentation with Context7.

**How to use Context7:**
1. Use `mcp__context7__resolve-library-id` to search for "fluent-assertions"
2. **Prefer website documentation** (IDs starting with `/websites/`) over source code repositories when available
3. Query with `mcp__context7__query-docs` using the resolved library ID

**Library ID:** `/fluentassertions/fluentassertions`

**Recommended Queries:**
- "FluentAssertions basic assertions Should Be"
- "FluentAssertions collection assertions HaveCount Contain"
- "FluentAssertions exception testing ThrowAsync"
- "FluentAssertions object equivalence BeEquivalentTo"