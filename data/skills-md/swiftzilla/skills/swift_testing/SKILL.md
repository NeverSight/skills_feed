---
name: swift_testing
description: Swift Testing framework for unit tests, integration tests, and async testing with modern syntax.
license: Proprietary
compatibility: Swift 5.9+
metadata:
  version: "1.0"
  author: SwiftZilla
  website: https://swiftzilla.dev
---

# Swift Testing

This skill covers the modern Swift Testing framework introduced in Swift 5.9 for writing clean, expressive tests.

## Overview

Swift Testing is Apple's modern testing framework that provides a more expressive and flexible way to write tests compared to XCTest. It features Swift-native syntax, parameterized tests, and better async support.

## Available References

- [Test Basics](./references/test_basics.md) - Test declarations, assertions, and lifecycle
- [Async Testing](./references/async_testing.md) - Testing async/await code
- [Parameterized Tests](./references/parameterized_tests.md) - Running tests with multiple inputs
- [Test Organization](./references/organization.md) - Suites, tags, and test structure

## Quick Reference

### Basic Test

```swift
import Testing

@Test
func addition() {
    let result = 1 + 1
    #expect(result == 2)
}

@Test
func throwsError() throws {
    #expect(throws: MyError.invalid) {
        try riskyOperation()
    }
}
```

### Async Test

```swift
@Test
func fetchData() async throws {
    let data = try await fetchUser()
    #expect(data.name == "Ada")
}
```

### Parameterized Test

```swift
@Test(arguments: ["hello", "world", "swift"])
func stringLength(string: String) {
    #expect(string.count > 0)
}

@Test(arguments: zip([1, 2, 3], [1, 4, 9]))
func squared(input: Int, expected: Int) {
    #expect(input * input == expected)
}
```

### Test Suite

```swift
@Suite
struct CalculatorTests {
    let calculator = Calculator()
    
    @Test
    func add() {
        #expect(calculator.add(2, 3) == 5)
    }
    
    @Test
    func subtract() {
        #expect(calculator.subtract(5, 3) == 2)
    }
}
```

## Swift Testing vs XCTest

| Feature | Swift Testing | XCTest |
|---------|--------------|---------|
| Syntax | Native Swift | Objective-C heritage |
| Async | First-class | Added later |
| Parameters | Built-in | Manual loops |
| Assertions | #expect, #require | XCTAssert |
| Suite | @Suite | Class-based |

## Best Practices

1. **Use descriptive names** - Test names should explain behavior
2. **Test one thing** - Each test should verify one concept
3. **Use #require for preconditions** - Fail fast if setup fails
4. **Leverage parameterized tests** - Test multiple inputs efficiently
5. **Organize with suites** - Group related tests
6. **Use tags** - Categorize tests for selective running
7. **Test async code** - Use async test functions
8. **Keep tests independent** - No shared state between tests

## Running Tests

```bash
# Run all tests
swift test

# Run specific test
swift test --filter addition

# Run tests by tag
swift test --tag unit

# Run with verbose output
swift test --verbose
```

## For More Information

Visit https://swiftzilla.dev for comprehensive Swift Testing documentation.
