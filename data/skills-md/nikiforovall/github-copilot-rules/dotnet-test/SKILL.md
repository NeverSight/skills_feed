---
name: dotnet-test
description: This skill should be used when running .NET tests selectively with a build-first, test-targeted workflow. Use it for running tests with xUnit focus.
allowed-tools: Bash(dotnet build:*), Bash(dotnet test:*), Read, Grep, Glob
---

# .NET Test Runner

Run .NET tests selectively using a build-first, test-targeted workflow optimized for development speed.

## Core Workflow

Follow this workflow to run tests efficiently:

### Step 1: Build Solution First

Build the entire solution with minimal output to catch compile errors early:

```bash
dotnet build -p:WarningLevel=0 /clp:ErrorsOnly --verbosity minimal
```

### Step 2: Run Specific Project Tests

Run tests for the specific test project with `--no-build` to skip redundant compilation:

```bash
dotnet test path/to/project --no-build --verbosity minimal
```

### Step 3: Filter When Targeting Specific Tests

Narrow down to specific tests using filter expressions:

```bash
# By method name using FullyQualifiedName (recommended)
dotnet test --no-build --filter "FullyQualifiedName~MyTestMethod"

# By class name using FullyQualifiedName (recommended)
dotnet test --no-build --filter "FullyQualifiedName~MyTestClass"

# By parameter values in Theory tests (xUnit)
dotnet test --no-build --filter "DisplayName~paramValue"

# Combined filters
dotnet test --no-build --filter "FullyQualifiedName~Create|FullyQualifiedName~Update"
```

**Note**: Properties `Name~` and `ClassName=` may not work reliably. Use `FullyQualifiedName~` instead.

## Quick Reference

### Commands

| Command                                                              | Purpose                              |
| -------------------------------------------------------------------- | ------------------------------------ |
| `dotnet build -p:WarningLevel=0 /clp:ErrorsOnly --verbosity minimal` | Build solution with minimal output   |
| `dotnet test path/to/Tests.csproj --no-build`                        | Run project tests (skip build)       |
| `dotnet test --no-build --logger "console;verbosity=detailed"`       | Show ITestOutputHelper output        |
| `dotnet test --no-build --filter "..."`                              | Run filtered tests                   |
| `dotnet test --no-build --list-tests`                                | List available tests without running |

### Filter Operators

| Operator | Meaning          | Example                                                        |
| -------- | ---------------- | -------------------------------------------------------------- |
| `=`      | Exact match      | `ClassName=MyTests`                                            |
| `!=`     | Not equal        | `Name!=SkipThis`                                               |
| `~`      | Contains         | `Name~Create`                                                  |
| `!~`     | Does not contain | `Name!~Integration`                                            |
| `\|`     | OR               | `Name~Test1\|Name~Test2` (note '\|' is an escape for markdown) |
| `&`      | AND              | `Name~User&Category=Unit`                                      |

### xUnit Filter Properties

| Property             | Description                                    | Reliability  | Example                                                |
| -------------------- | ---------------------------------------------- | ------------ | ------------------------------------------------------ |
| `FullyQualifiedName` | Full test name with namespace                  | ✅ Reliable   | `FullyQualifiedName~MyNamespace.MyClass`               |
| `DisplayName`        | Test display name (includes Theory parameters) | ✅ Reliable   | `DisplayName~My_Test_Name` or `DisplayName~paramValue` |
| `Name`               | Method name                                    | ⚠️ Unreliable | Use `FullyQualifiedName~` instead                      |
| `ClassName`          | Class name                                     | ⚠️ Unreliable | Use `FullyQualifiedName~` instead                      |
| `Category`           | Trait category                                 | ✅ Reliable   | `Category=Unit`                                        |

**When to use DisplayName**: Essential for filtering Theory tests by their parameter values. xUnit includes all parameter values in the DisplayName (e.g., `MyTest(username: "admin", age: 30)`), making it ideal for running specific test cases. See [references/theory-parameter-filtering.md](references/theory-parameter-filtering.md) for detailed guidance.

### Common Filter Patterns

```bash
# Run tests containing "Create" in method name
dotnet test --no-build --filter "FullyQualifiedName~Create"

# Run tests in a specific class
dotnet test --no-build --filter "FullyQualifiedName~UserServiceTests"

# Run tests matching namespace pattern
dotnet test --no-build --filter "FullyQualifiedName~MyApp.Tests.Unit"

# Run Theory tests with specific parameter value
dotnet test --no-build --filter "DisplayName~admin_user"

# Run tests with specific trait
dotnet test --no-build --filter "Category=Integration"

# Exclude slow tests
dotnet test --no-build --filter "Category!=Slow"

# Combined: class AND parameter value (Theory tests)
dotnet test --no-build --filter "FullyQualifiedName~OrderTests&DisplayName~USD"

# Multiple parameter values (OR condition)
dotnet test --no-build --filter "DisplayName~EUR|DisplayName~GBP"
```

### ITestOutputHelper Output

To see output from xUnit's `ITestOutputHelper`, use the console logger with detailed verbosity:

```bash
dotnet test --no-build --logger "console;verbosity=detailed"
```

### Reducing Output Noise

Verbosity levels for `dotnet test`:

| Level      | Flag      | Description                     |
| ---------- | --------- | ------------------------------- |
| quiet      | `-v q`    | Minimal output (pass/fail only) |
| minimal    | `-v m`    | Clean summary, no test output   |
| normal     | `-v n`    | Default, shows discovered tests |
| detailed   | `-v d`    | Shows more details              |
| diagnostic | `-v diag` | Most verbose                    |

To see test output, use grep to filter out discovery messages (for xUnit):

```bash
dotnet test --no-build --logger "console;verbosity=detailed" 2>&1 | grep -v "Discovered \[execution\]"
```

## Framework Differences

This skill focuses on **xUnit**. For MSTest or NUnit, filter property names differ:

| Property       | xUnit       | MSTest         | NUnit       |
| -------------- | ----------- | -------------- | ----------- |
| Method name    | `Name`      | `Name`         | `Name`      |
| Class name     | `ClassName` | `ClassName`    | `ClassName` |
| Category/Trait | `Category`  | `TestCategory` | `Category`  |
| Priority       | -           | `Priority`     | `Priority`  |

## Progressive Disclosure

For advanced scenarios, load additional references:

- **references/theory-parameter-filtering.md** - Filtering xUnit Theory tests by parameter values (string, numeric, boolean, etc.)
- **references/blame-mode.md** - Debugging test crashes and hangs with `--blame`
- **references/parallel-execution.md** - Controlling parallel test execution

Load these references when:

- Working with xUnit Theory tests and need to filter by specific parameter values
- Tests are crashing or hanging unexpectedly
- Diagnosing test isolation issues
- Optimizing test run performance

## When to Use This Skill

Invoke when the user needs to:

- Run targeted tests during development
- Filter tests by method or class name
- Filter xUnit Theory tests by specific parameter values (e.g., run only admin user test cases)
- Understand test output and filtering options
- Debug failing or hanging tests
