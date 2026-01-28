---
name: build-frontend
description: Builds the Fake Survey Generator React frontend with Vite and TypeScript. Use this skill when frontend code changes need to be compiled and validated for TypeScript errors. This skill orchestrates the npm build command and reports build errors.
---

# Build Frontend Skill

Use this skill to validate that all frontend TypeScript and React components compile successfully without errors.

## What This Skill Does

1. Runs `npm run build` in `src/client/frontend/`
2. Validates TypeScript compilation via `tsc` type checking
3. Bundles React application with Vite
4. Captures and parses build errors
5. Reports errors with file and line number references
6. Exits with failure status if any build errors are found

## When to Use

- After implementing or modifying React components
- After updating frontend TypeScript types or interfaces
- To validate that TypeScript compilation succeeds
- Before running E2E validation against the UI
- To ensure Vite bundling produces valid output

## How the Agent Should Use This Skill

1. **Prepare**: Ensure you are in the repository root directory
2. **Invoke**: Run the frontend build helper script from the repository root:
   ```
   dotnet .github/skills/build-frontend/build-frontend.cs
   ```
3. **Parse Output**: Monitor stdout for success message and stderr for errors
4. **Handle Errors**: If exit code is non-zero, the build failed. Review the error messages to identify:
   - TypeScript compilation errors (e.g., type mismatches, missing properties)
   - Import/export issues
   - React component rendering errors
   - Vite bundling failures
5. **Report**: If any errors occur, halt further validation and report the build error details to the user

## Success Criteria

- Exit code: 0
- Stdout contains: `[BUILD] Frontend build completed successfully`

## Failure Indicators

- Exit code: 1
- Stderr contains TypeScript or build errors
- Error messages may reference file paths, line numbers, and error codes (e.g., `TS7006`)

## Notes

- The build script automatically finds the repository root by searching for `FakeSurveyGenerator.slnx` or `FakeSurveyGenerator.sln`
- Frontend directory is located at `src/client/frontend/`
- Build process includes TypeScript type checking (`npm run build` runs both `tsc` check and Vite bundling)
- The script automatically runs `npm ci` if `node_modules` directory is missing, ensuring dependencies are installed before building
- On Windows, the script uses `cmd.exe /c npm` to reliably invoke npm, avoiding PATH resolution issues

## Next Steps After Success

Once frontend build succeeds, typically invoke:
- **Validate Aspire Runtime Skill** - to start the application and UI server
- **Validate E2E Skill** - to run interactive UI tests with Playwright MCP
