---
name: build-backend
description: Builds the Fake Survey Generator backend .NET projects. Use this skill when backend code changes need to be compiled and validated for syntax errors. This skill orchestrates the dotnet build command and reports compilation errors.
---

# Build Backend Skill

Use this skill to validate that all backend C# projects compile successfully without errors.

## What This Skill Does

1. Runs `dotnet build` to compile all .NET projects in the solution
2. Captures and parses compilation errors
3. Reports errors with file and line number references
4. Exits with failure status if any compilation errors are found

## When to Use

- After implementing backend features in the Api project, Application project, or Worker project
- To validate that dependencies and package versions are correct
- Before running tests or other downstream validation steps
- To catch syntax errors or type mismatches early

## How the Agent Should Use This Skill

1. **Prepare**: Ensure you are in the repository root directory
2. **Invoke**: Run the backend build helper script from the repository root:
   ```
   dotnet .github/skills/build-backend/build-backend.cs
   ```
3. **Parse Output**: Monitor stdout for success message and stderr for errors
4. **Handle Errors**: If exit code is non-zero, the build failed. Review the error messages to identify:
   - File paths and line numbers from error output
   - Type errors, syntax errors, or missing references
   - Package version conflicts
5. **Report**: If any errors occur, halt further validation and report the compilation error details to the user

## Success Criteria

- Exit code: 0
- Stdout contains: `[BUILD] Backend build completed successfully`

## Failure Indicators

- Exit code: 1
- Stderr contains compilation errors (e.g., `error CS0103: The name 'xyz' does not exist`)
- Stdout/stderr may contain file paths and line numbers of errors

## Notes

- The build script automatically finds the repository root by searching for `FakeSurveyGenerator.slnx` or `FakeSurveyGenerator.sln`
- Full build output is captured; review stderr for detailed error messages
- Backend projects are: Api, Application, Application.Tests, Api.Tests.Integration, Worker, ServiceDefaults, Proxy

## Next Steps After Success

Once backend build succeeds, typically invoke:
- **Frontend Build Skill** - to compile TypeScript
- **Test Backend Units Skill** - to run unit and integration tests
