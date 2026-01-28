---
name: test-backend-units
description: Executes backend unit tests and integration tests for the Fake Survey Generator project using TUnit framework. This skill validates that implemented features are covered by tests and that existing tests continue to pass. Reports test failures and code coverage metrics.
---

# Test Backend Units Skill

Use this skill to run unit and integration tests (excluding acceptance tests) to validate that features are properly tested.

## What This Skill Does

1. Runs `dotnet test` with a filter to exclude acceptance tests (which require Aspire runtime to be running)
2. Includes test projects:
   - `FakeSurveyGenerator.Application.Tests` (unit tests for business logic)
   - `FakeSurveyGenerator.Api.Tests.Integration` (integration tests with real SQL Server & Redis via Testcontainers)
3. Excludes test projects:
   - `FakeSurveyGenerator.Acceptance.Tests` (E2E tests requiring Aspire runtime - validated separately via E2E skill)
4. Collects test results including:
   - Total tests run, passed, failed, skipped
   - Failed test names and error details
   - Code coverage metrics
5. Reports failures with specific test names and assertion errors
6. Exits with failure status if any tests fail

## Filter Rationale

Acceptance tests are excluded because they require the Aspire orchestration environment to be running. They are validated separately via the **validate-e2e skill** after Aspire runtime is started. This separation allows:
- Faster feedback cycle (unit + integration tests run in ~20 seconds)
- Clean separation of concerns (logic tests vs. E2E validation)
- Avoiding timeout issues when running acceptance tests without Aspire infrastructure

## When to Use

- After implementing new feature logic to ensure it's covered by tests
- Before deploying changes to validate no regressions
- To check code coverage metrics
- To verify that test infrastructure (databases, Redis) works correctly
- To ensure integration tests pass with real dependencies

## How the Agent Should Use This Skill

1. **Prepare**: Ensure backend build succeeded first via Build Backend Skill
2. **Invoke**: Run tests from repository root with the treenode filter to exclude acceptance tests:
   ```
   dotnet test --treenode-filter "/(*Tests*)&(!*Acceptance*)/*/*/*" --ignore-exit-code 8
   ```
   - The filter `--treenode-filter "/(*Tests*)&(!*Acceptance*)/*/*/*"` includes all test projects EXCEPT those with "Acceptance" in the name
   - The flag `--ignore-exit-code 8` treats exit code 8 (partial pass - when some test projects have zero tests) as success, since acceptance tests are filtered out
3. **Parse Output**: Monitor stdout and stderr for:
   - Test run summary (total tests, passed/failed counts)
   - Failed test names (format: `NameSpace.TestClass.TestMethod`)
   - Error details and stack traces
   - Code coverage percentage per project
4. **Handle Failures**: If any tests fail:
   - Extract failed test names
   - Review assertion errors or exception messages
   - Report specific failures to user with context
   - Halt further validation
5. **Report Coverage**: Include code coverage metrics from output

## Success Criteria

- Exit code: 0 (or 8 when ignoring filtered-out test projects)
- All executed tests pass (output shows `failed: 0` or similar)
- No error output to stderr indicating test execution issues
- Filter successfully excludes acceptance tests from execution
- Only Application.Tests and Api.Tests.Integration run

## Failure Indicators

- Exit code: 1 or higher (when not using --ignore-exit-code 8)
- Stdout contains failed test counts (e.g., `failed: 3`)
- Individual test failure messages with names and error details
- May show timeout errors if integration test containers fail to start

## Test Projects Reference

### FakeSurveyGenerator.Application.Tests
- **Type**: Unit tests
- **Framework**: TUnit
- **Coverage**: Business logic, domain models, application services
- **Mocking**: NSubstitute for dependencies
- **Test Data**: AutoFixture for fixtures

### FakeSurveyGenerator.Api.Tests.Integration
- **Type**: Integration tests
- **Framework**: TUnit + Testcontainers
- **Coverage**: API endpoints, database operations, cache interactions
- **Real Dependencies**: SQL Server (via Testcontainers), Redis (via Testcontainers)
- **DB Cleanup**: Respawn for test isolation

## Common Test Patterns

- Arrange-Act-Assert structure
- Async/await for async test methods
- Test class naming: `{ComponentUnderTest}Tests`
- Test method naming: `{Method}_GivenCondition_ExpectedBehavior`

## Notes

- Tests are located in `src/server/` directory alongside source code
- TrxReport format is used for reporting
- CodeCoverage analysis is enabled on build
- **Treenode Filter**: `--treenode-filter "/(*Tests*)&(!*Acceptance*)/*/*/*"` excludes acceptance tests (same as CI/CD pipeline in `.azdo/pipelines/azure-dev.yml`)
- **Exit Code Handling**: Use `--ignore-exit-code 8` to treat exit code 8 (partial pass due to filtered-out projects) as success
- Run with `-v n` for detailed output if needed: `dotnet test --treenode-filter "/(*Tests*)&(!*Acceptance*)/*/*/*" --ignore-exit-code 8 -v n`
- Some integration tests require Docker to be running (for Testcontainers)
- Acceptance tests are run separately via the **validate-e2e skill** after Aspire runtime is started

## Next Steps After Success

Once all tests pass, typically invoke:
- **Validate Aspire Runtime Skill** - to start the running application
- **Validate E2E Skill** - to run acceptance tests and interactive UI validation
