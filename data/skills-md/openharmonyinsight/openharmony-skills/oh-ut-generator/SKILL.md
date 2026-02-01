---
name: oh-ut-generator
description: |
  Generate OpenHarmony C++ unit tests following HWTEST_F framework conventions.
  Supports Mock strategies, BUILD.gn configuration, NDK/NAPI interfaces,
  and maintains 75%+ coverage requirements with strict code style consistency.
  Use when generating unit tests for OpenHarmony C++ source files.
---

# OpenHarmony Unit Test Generator

## Overview

Generate comprehensive C++ unit tests for OpenHarmony code following HWTEST_F framework conventions.

## Key Features

- **Automatic Test Generation**: Create test cases for normal/exception/boundary scenarios
- **Mock Object Support**: Mock class creation and EXPECT_CALL/ON_CALL setup
- **BUILD.gn Configuration**: Automatic dependency matching with source files
- **Coverage Optimization**: 75% minimum coverage, targeting 85%+
- **Code Style Consistency**: Maintains consistency with existing test patterns (>=70% threshold)
- **NDK/NAPI Support**: Special handling for NDK interfaces (7088+ OH_xxx) and NAPI functions (302+ napi_xxx)
- **CJSON Testing**: Complete support for CJSON library testing patterns

## Usage

Invoke this skill when you need to generate unit tests for OpenHarmony C++ source files.

### Supported Scenarios

1. **Single File Testing**: Generate tests for all functions in a source file
2. **Specific Function Testing**: Generate tests for a specific function only
3. **Test File Extension**: Append new test cases to existing test files
4. **Mock Generation**: Automatically create mock classes for dependencies

## Critical Requirements

### Test Implementation Completeness

- **Complete Implementation Only**: Every test case must have complete implementation
- **No Comments-Only Tests**: Forbidden to generate tests with only comments or empty bodies
- **Mock Usage**: If Mock objects are created, they must be used with EXPECT_CALL/ON_CALL
- **Branch-Assertion Correspondence**: Branch assertions must match branch logic exactly

### Coverage Requirements

- **Minimum**: 75% branch and line coverage (mandatory)
- **Target**: 85% branch and line coverage (goal)
- **Scope**: Boundary conditions, exception paths, normal paths, all conditional branches

### Code Style Consistency

When existing test files exist:
- **Smart Pointer Type**: Must match existing code (sptr/wptr vs std::shared_ptr)
- **Mock Usage**: Must match existing Mock patterns
- **Assertion Style**: Must match existing assertion preferences (EXPECT_ vs ASSERT_)
- **Test Structure**: Must match existing test fixtures and naming patterns

**Consistency Threshold**: >=70% for important scenarios

### Security Coding

- **Memory Management**: Match original function's smart pointer usage pattern
- **Variable Initialization**: All variables must be initialized
- **Boundary Checks**: Required before array/container access
- **Null Pointer Checks**: Required before pointer dereference
- **Return Value Checks**: Required for critical functions

## Framework Specifications

### HWTEST_F Framework

```cpp
// Test fixture structure
class YourServiceTest : public testing::Test {
public:
    static void SetUpTestCase(void);
    static void TearDownTestCase(void);
    void SetUp();
    void TearDown();
    std::shared_ptr<YourService> instance_;
};

// Test case format
HWTEST_F(TestClassName, TestCaseName_001, TestSize.Level1)
```

### Test Case Naming

- `_001`: Normal scenario
- `_002`: Exception scenario
- `_003`: Boundary scenario
- `_004+`: Other special scenarios

### Object Management

```cpp
// Standard smart pointers
SetUp(): instance_ = std::make_shared<YourService>();
TearDown(): instance_ = nullptr;

// OpenHarmony sptr/wptr
SetUp(): instance_ = MakeSptr<YourService>(); // or instance_ = new YourService();
TearDown(): instance_ = nullptr;
```

### Mock Usage

```cpp
auto mock = std::make_shared<MockClass>();
EXPECT_CALL(*mock, Method()).WillOnce(Return(value));
```

### Assertions

```cpp
ASSERT_NE(instance_, nullptr);  // Must check
EXPECT_EQ(result, expected);
EXPECT_TRUE(condition);
```

## NDK Interface Testing

For NDK interfaces (OH_xxx), follow these requirements:

1. **Resource Lifecycle**: Create/Destroy pairing is mandatory
2. **Test Structure**: Normal path (001), Exception path (002), Boundary (003)
3. **Return Value Verification**: Test all error codes
4. **Parameter Validation**: Test null pointers, invalid values, boundaries

## CJSON Testing

For CJSON library operations:

1. **Parse Tests**: Normal, null pointer, invalid JSON
2. **Get Item Tests**: Normal get, non-existent item, type checks
3. **Create Tests**: Object, array, value creation
4. **Memory Management**: All cJSON objects must be deleted

## BUILD.gn Requirements

### ohos_unittest Target

```gn
ohos_unittest("{CamelCase}Test") {
    module_out_path = "subsystem/module"
    branch_protector_ret = "pac_ret"
    sanitize = {
        integer_overflow = true
        cfi = true
        cfi_cross_dso = true
        debug = false
    }
    sources = ["test_file.cpp"]  # Alphabetically sorted
    include_dirs = ["//include/path"]
    deps = [":source_target"]
    external_deps = [
        "hilog:libhilog",
        "c_utils:utils",
        "googletest:gtest_main"
    ]
    defines = ["private=public"]
}
```

### Configuration Matching

The system automatically extracts source file's BUILD.gn configuration:
- **deps**: Must include all source target dependencies
- **external_deps**: Must include all external dependencies
- **include_dirs**: Must include all include directories
- **defines**: Must match source defines (add private=public if needed)

## Reference Files

Detailed specifications are available in the `references/` directory:

- **framework-specs.md**: HWTEST_F framework conventions and test patterns
- **mock-strategies.md**: Mock object creation and usage strategies
- **coverage-requirements.md**: Coverage metrics and optimization strategies
- **build-gn-rules.md**: BUILD.gn configuration and dependency matching
- **assertion-standards.md**: Assertion methods and branch correspondence
- **code-style-consistency.md**: Consistency requirements with existing tests
- **smart-pointer-usage.md**: sptr/wptr vs standard smart pointer usage
- **ndk-napi-testing.md**: NDK/NAPI interface testing specifications
- **cjson-testing.md**: CJSON library testing patterns
- **security-coding.md**: Memory management and secure coding requirements

## Examples

See the `examples/` directory for:
- **basic-test-example.cpp**: Basic test structure and patterns
- **mock-test-example.cpp**: Mock object usage examples
- **ndk-test-example.cpp**: NDK interface testing examples
