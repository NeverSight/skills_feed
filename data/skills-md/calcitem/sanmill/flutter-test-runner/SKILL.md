---
name: "Flutter Test Runner"
description: "Run Sanmill's Flutter test suite, including unit tests, widget tests, and integration tests; use when running tests or checking test coverage."
---

# Flutter Test Runner

## Purpose

This skill helps run and manage Sanmill's Flutter test suite, ensuring code quality and functional correctness.

## Use Cases

- Run unit and widget tests
- Run integration tests with real AI engine
- Generate and view test coverage reports
- Verify functionality after code modifications
- Validate changes in CI/CD pipelines

## Test Structure Overview

```
src/ui/flutter_app/
├── test/                # Unit and widget tests (Dart VM, fast)
├── integration_test/    # Integration tests (real platform + AI engine)
└── test_driver/         # Test drivers
```

## Quick Commands

### Unit and Widget Tests

```bash
cd src/ui/flutter_app

# Run all tests
flutter test

# Run specific test file
flutter test test/game/position_test.dart

# Run with coverage
flutter test --coverage
```

### Integration Tests

```bash
# From repository root - use the project script (recommended)
./run-integration-test.sh --full           # Complete test suite
./run-integration-test.sh --single         # Single test case
./run-integration-test.sh --help           # Show options

# Manual execution (from src/ui/flutter_app)
flutter test integration_test/ -d linux    # Linux
flutter test integration_test/ -d macos    # macOS
flutter test integration_test/ -d windows  # Windows
```

## Test Types Comparison

| Type | Environment | Native Code | Speed | Use For |
|------|-------------|-------------|-------|---------|
| **Unit/Widget** | Dart VM | ❌ No | ⚡ Fast | Pure Dart logic, UI components |
| **Integration** | Real platform | ✅ Yes | 🐌 Slower | AI behavior, platform features |

**Key difference**: Integration tests use the real C++ AI engine and must run on actual platforms, not the Dart VM.

## Coverage Reports

```bash
# Generate coverage
flutter test --coverage

# View summary (requires lcov)
lcov --summary coverage/lcov.info

# Generate HTML report
genhtml coverage/lcov.info -o coverage/html
# Then open coverage/html/index.html
```

**Coverage targets**: Overall ≥80%, Critical logic ≥90%, UI ≥70%

## Common Issues & Solutions

### 1. MissingPluginException
- **Symptom**: Tests fail with plugin errors
- **Cause**: Running integration tests with `flutter test test/`
- **Fix**: Use `flutter test integration_test/ -d <platform>`

### 2. Import Errors
- **Fix**: Run `flutter pub get` or `flutter clean && flutter pub get`

### 3. Integration Test Failures (AI-related)
- **Cause**: AI behavior may vary between runs
- **Solution**:
  1. Check if AI moves are reasonable
  2. Update expected sequences in test data if needed
  3. Ensure consistent AI configuration

### 4. Timeout Issues
- Increase test timeout in test configuration
- Check async operation handling
- Adjust `maxWaitTimeMs` for AI tests

## Best Practices

1. **Run unit tests frequently** - Fast feedback loop
2. **Run integration tests before commits** - Catch platform-specific issues
3. **Check coverage for new code** - Maintain quality standards
4. **Keep tests independent** - Tests should not depend on each other
5. **Update expectations carefully** - For AI tests, verify moves are actually correct

## Reference Documentation

- **Integration tests**: `src/ui/flutter_app/integration_test/AUTOMATED_MOVE_TESTS_README.md`
- **Flutter testing guide**: https://docs.flutter.dev/testing
- **Test directories**: `src/ui/flutter_app/test/` and `src/ui/flutter_app/integration_test/`

## Output Format

Test results should report:
- ✓ Pass/fail status with counts
- ✗ Failure details with stack traces
- 📊 Coverage percentage (if generated)
- ⏱ Execution time
- 💡 Actionable recommendations
