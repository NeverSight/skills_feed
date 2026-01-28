---
name: dotnet-test
version: 0.1.0
kind: cli
description: Run .NET tests using dotnet CLI. Use when task involves executing unit tests, generating code coverage reports, or running benchmarks.
inputs:
  target: [all, project, specific]
  configuration: [Debug, Release]
  coverage: ['true', 'false']
  project_path: string
contracts:
  success: 'Tests pass with zero failures; coverage data generated if requested'
  failure: 'Non-zero exit code, test failures, or coverage generation errors'
---

# .NET Test Skill (Entry Map)

> **Goal:** Guide agent to the exact testing procedure needed.

## Quick Start (Pick One)

- **Run unit tests** → `references/run-unit-tests.md`
- **Generate coverage report** → `references/generate-coverage.md`
- **Run benchmarks** → `references/run-benchmarks.md`

## When to Use

- Execute unit tests (xUnit, NUnit)
- Generate code coverage reports with coverlet
- Run performance benchmarks with BenchmarkDotNet
- Validate code changes with test suites
- Measure test execution time

**NOT for:** building code (dotnet-build), formatting (code-format), or static analysis (code-analyze)

## Inputs & Outputs

**Inputs:** `target` (all/project/specific), `configuration` (Debug/Release), `coverage` (true/false), `project_path` (default: all test projects)

**Outputs:** Test results (pass/fail counts), coverage reports (if requested), benchmark results, exit code (0=success)

**Guardrails:** Operate in ./dotnet only, report failures clearly, never skip tests without permission

## Navigation

**1. Run Unit Tests** → [`references/run-unit-tests.md`](references/run-unit-tests.md)

- Run all tests, run specific project tests, troubleshoot test failures

**2. Generate Coverage Report** → [`references/generate-coverage.md`](references/generate-coverage.md)

- Collect coverage data, generate reports (HTML/Cobertura), analyze coverage metrics

**3. Run Benchmarks** → [`references/run-benchmarks.md`](references/run-benchmarks.md)

- Execute performance benchmarks, compare results, optimize based on data

## Common Patterns

### Run All Tests (Quick)

```bash
cd ./dotnet
dotnet test
```

### Run Tests with Verbose Output

```bash
cd ./dotnet
dotnet test --verbosity normal
```

### Run Specific Test Project

```bash
cd ./dotnet
dotnet test console-app.Tests/PigeonPea.Console.Tests.csproj
```

### Run Tests with Coverage

```bash
cd ./dotnet
dotnet test --collect:"XPlat Code Coverage"
```

### Run Tests and Generate Coverage Report

```bash
cd ./dotnet
dotnet test --collect:"XPlat Code Coverage" --results-directory ./TestResults
# Coverage file: ./TestResults/{guid}/coverage.cobertura.xml
```

### Filter Tests by Name

```bash
cd ./dotnet
dotnet test --filter "FullyQualifiedName~FrameTests"
```

### Filter Tests by Category

```bash
cd ./dotnet
dotnet test --filter "Category=Unit"
```

### Run Tests in Release Configuration

```bash
cd ./dotnet
dotnet test --configuration Release
```

### Run Benchmarks

```bash
cd ./dotnet/benchmarks
dotnet run -c Release
```

## Troubleshooting

**Tests fail:** Check test output for assertion failures. See `references/run-unit-tests.md` for debugging.

**Coverage not generated:** Ensure coverlet.collector is installed. See `references/generate-coverage.md`.

**Benchmarks fail to run:** Use Release configuration. See `references/run-benchmarks.md`.

**Slow test execution:** Filter tests, run in parallel, or use `--no-build` after building.

**Test discovery fails:** Check project references, ensure test framework packages are installed.

## Success Indicators

```
Passed!  - Failed:     0, Passed:    42, Skipped:     0, Total:    42
```

Test artifacts in: `./dotnet/TestResults/`

Coverage report in: `./dotnet/TestResults/coverage.cobertura.xml`

## Integration

**Before testing:** dotnet-build (ensure code is built)
**After testing:** code-analyze (static analysis), code-review (quality checks)

## Test Frameworks

This repository uses:

- **xUnit** for unit tests (console-app.Tests, shared-app.Tests, windows-app.Tests)
- **coverlet.collector** for code coverage
- **BenchmarkDotNet** for performance benchmarks

## Related

- [`./dotnet/README.md`](../../../dotnet/README.md) - Project structure
- [`./dotnet/ARCHITECTURE.md`](../../../dotnet/ARCHITECTURE.md) - Architecture
- [`.pre-commit-config.yaml`](../../../.pre-commit-config.yaml) - Pre-commit hooks
- [`dotnet-build` skill](../dotnet-build/SKILL.md) - Build skill
