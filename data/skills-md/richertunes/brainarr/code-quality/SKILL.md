---
name: code-quality
description: Enforce code quality standards, test coverage, and static analysis. Use when working with code coverage thresholds, mutation testing, linting, code formatting, or quality gates. Maintains high code quality standards through automation.
---

# Code Quality Enforcer

## Current Quality Infrastructure
- ✅ **Test Coverage**: Collected with Coverlet (31% baseline)
- ✅ **Mutation Testing**: Stryker.NET weekly runs
- ✅ **Code Formatting**: .NET format enforcement in CI
- ✅ **Static Analysis**: .NET analyzers enabled
- ✅ **Pre-commit Hooks**: Format and lint checks

## Expertise Areas

### 1. Coverage Enforcement
- Set minimum coverage thresholds
- Fail builds on coverage regression
- Track coverage trends over time
- Identify uncovered critical paths

### 2. Mutation Testing
- Validate test effectiveness with Stryker.NET
- Identify weak tests that pass but don't validate logic
- Improve test quality through mutation analysis
- Weekly automated mutation test runs

### 3. Static Analysis
- CodeQL security scanning
- .NET analyzers and Roslyn
- Custom analyzer rules
- Complexity metrics tracking

### 4. Code Formatting
- Consistent style with .NET format
- EditorConfig enforcement
- Pre-commit format validation
- CI format verification

### 5. Quality Gates
- Fail builds on quality regression
- Enforce coverage thresholds
- Block PRs with quality issues
- Quality trend dashboards

## Enhancement Opportunities
1. **Increase Coverage**: From 31% baseline to 50%+
2. **SonarCloud Integration**: Code smells and tech debt
3. **Complexity Metrics**: Track cyclomatic complexity
4. **Performance Regression**: Detect performance degradation
5. **Quality Dashboards**: Visualize quality trends

## Related Skills
- `security-compliance` - Security is quality
- `integration-testing` - Quality through testing

## Examples

### Example 1: Enforce Coverage Threshold
**User**: "Fail builds if coverage drops below 31%"
**Action**: Add coverage enforcement to test workflow, fail on regression

### Example 2: Run Mutation Tests
**User**: "Run Stryker mutation testing"
**Action**: Execute Stryker, review mutation score, identify weak tests, improve coverage

### Example 3: Quality Dashboard
**User**: "Create quality metrics dashboard"
**Action**: Integrate CodeCov, add badges to README, visualize trends
