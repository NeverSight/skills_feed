---
name: test-frontend-units
description: Executes frontend component unit tests for the Fake Survey Generator React application using Vitest. This skill validates that React components are properly tested and that existing tests continue to pass. Reports test failures and code coverage metrics.
---

# Test Frontend Units Skill

Use this skill to run unit tests for React components to validate that features are properly tested and components function as expected.

## What This Skill Does

1. Runs `npm test -- --run` from the `src/client/frontend` directory
2. Executes Vitest test suite including:
   - `src/components/CreateSurvey.test.tsx` (15 tests - survey creation form)
   - `src/components/GetSurvey.test.tsx` (17 tests - survey fetching and display)
   - `src/components/MySurveys.test.tsx` (18 tests - user surveys listing)
3. Tests run in jsdom environment simulating browser APIs
4. Includes Auth0 authentication mocking and testing utilities
5. Collects test results including:
   - Total tests run, passed, failed, skipped
   - Failed test names and error details
   - Test execution time per file
6. Reports failures with specific test names and assertion errors
7. Exits with failure status if any tests fail

## Test Framework & Environment

- **Framework**: Vitest v4.0.17
- **Environment**: jsdom (browser API simulation)
- **Testing Library**: @testing-library/react with @testing-library/user-event
- **Auth Mocking**: Auth0 useAuth0 hook mocked in test setup
- **Utilities**: Custom test utilities with render wrapper for consistent test setup

## When to Use

- After implementing new React component features to ensure they're covered by tests
- Before deploying frontend changes to validate no regressions
- To check component functionality and user interactions
- After modifying existing components to ensure tests still pass
- To verify form handling, API integration, and state management
- During feature development to validate component behavior

## How the Agent Should Use This Skill

1. **Prepare**: Navigate to repository root
2. **Invoke**: Run tests from repository root:
   ```
   cd src/client/frontend && npm test -- --run
   ```
   - The `--run` flag executes tests once and exits (non-watch mode)
   - Tests execute with jsdom environment for browser API simulation
3. **Parse Output**: Monitor stdout and stderr for:
   - Test file summary (e.g., "Test Files  3 passed (3)")
   - Test count summary (e.g., "Tests  50 passed (50)")
   - Individual test execution times
   - Failed test names and assertion errors
   - Error details and stack traces if failures occur
4. **Handle Failures**: If any tests fail:
   - Extract failed test names and file locations
   - Review assertion errors or exception messages
   - Report specific failures to user with context
   - Halt further validation (don't proceed to Aspire/E2E)
5. **Report Success**: Include test count and execution time in report

## Success Criteria

- Exit code: 0
- All tests pass (output shows `failed: 0` or similar)
- No error output to stderr indicating test execution issues
- Output shows "Test Files X passed (X)" with all files passing
- Vitest runs and completes successfully
- Tests complete in reasonable time (under 5 seconds)

## Failure Indicators

- Exit code: 1 or non-zero
- Stdout contains failed test counts (e.g., `failed: 2`)
- Individual test failure messages with names and assertion details
- Console errors from test setup or mocking issues
- Timeout errors in async tests
- Import or type errors in test files

## Test Files & Components

### CreateSurvey.test.tsx
- **Component**: CreateSurvey (survey creation form)
- **Tests**: 15 test cases
- **Coverage**:
  - Form rendering and input fields
  - Adding/removing survey options
  - Form validation and submission
  - Error handling and success messages
  - State management and form reset
- **Key Tests**:
  - Renders form with correct fields
  - Updates input values on user type
  - Adds/removes options from survey
  - Submits form with correct API payload
  - Shows error/success messages

### GetSurvey.test.tsx
- **Component**: GetSurvey (survey fetching and display)
- **Tests**: 17 test cases
- **Coverage**:
  - Survey fetching by ID
  - Form submission for manual fetch
  - Survey result display
  - Error state handling (404, network errors)
  - Loading indicators
  - Component updates on prop changes
- **Key Tests**:
  - Auto-fetches survey when ID prop changes
  - Displays survey data and result breakdown
  - Shows error messages for failed requests
  - Handles 404 and network errors gracefully
  - Updates input values on user interaction

### MySurveys.test.tsx
- **Component**: MySurveys (user surveys listing)
- **Tests**: 18 test cases
- **Coverage**:
  - Fetching user's surveys
  - Displaying surveys in table format
  - Loading skeletons during fetch
  - Empty state when no surveys exist
  - Error handling and error messages
  - User interactions (clicking buttons, rapid clicks)
  - Multiple successive fetches
- **Key Tests**:
  - Renders survey list with correct data
  - Shows loading skeleton while fetching
  - Shows empty state when no surveys
  - Handles API errors gracefully
  - Fetches surveys when button clicked

## Common Test Patterns Used

```typescript
// Component rendering test
render(<ComponentName />);
expect(screen.getByRole("heading", { name: /title/i })).toBeInTheDocument();

// Form interaction test with userEvent
const input = screen.getByPlaceholderText("placeholder");
await user.type(input, "value");
expect(input).toHaveValue("value");

// Async API test with mock
const mockApiCall = vi.fn().mockResolvedValue({ok: true, json: async () => data});
vi.mocked(hooks.useApiCall).mockReturnValue({apiCall: mockApiCall});
await user.click(button);
await waitFor(() => expect(mockApiCall).toHaveBeenCalled());

// Error handling test
mockApiCall.mockRejectedValue(new Error("Network error"));
// ... trigger component action
await waitFor(() => expect(screen.getByText("Network error")).toBeInTheDocument());
```

## Test Setup & Infrastructure

- **vitest.config.ts**: Configures jsdom environment, global APIs, setup files
- **src/test/setup.ts**: Auth0 useAuth0 hook mock, window.matchMedia mock
- **src/test/test-utils.tsx**: Custom render function with testing utilities wrapper
- **Mock Data**: Realistic survey and user data structures matching API types

## Notes

- Tests are located in `src/client/frontend/src/components/` directory
- All tests use jsdom for browser API simulation (window, document, etc.)
- Auth0 authentication is mocked so tests don't require real tokens
- Tests use userEvent for realistic user interaction simulation
- Custom hooks (useApiCall, useSurveyFetch) are mocked via vi.mocked()
- Tests include loading states, error states, and empty states
- Current test suite: **50 tests passing** (100% success rate)
- Run with `npm test -- --ui` for interactive Vitest UI dashboard
- Run with `npm test -- --coverage` to generate coverage report
- Test execution time: ~1.5-2 seconds for full suite

## Common Issues & Troubleshooting

| Issue                             | Cause                               | Solution                                                                      |
| --------------------------------- | ----------------------------------- | ----------------------------------------------------------------------------- |
| "Unable to find an element" error | Selector doesn't match any elements | Use more specific selectors (getByRole, getByLabelText) or use screen.debug() |
| Timeout in waitFor                | Async operation not completing      | Check mock setup, increase timeout, verify component updates state            |
| Import errors in tests            | Wrong import paths                  | Use relative paths from test file location (e.g., `../test/test-utils`)       |
| Type errors with mocks            | Mock return type mismatch           | Ensure mock data matches component prop types                                 |
| Auth0 not mocked                  | Setup.ts not loading                | Verify vitest.config.ts has correct setupFiles path                           |

## Next Steps After Success

Once all frontend unit tests pass, typically invoke:
- **Validate Aspire Runtime Skill** - to start the full application environment
- **Validate E2E Skill** - to run end-to-end acceptance tests and verify features work in running application

## Dependencies

Run these from `src/client/frontend` directory once:
```bash
npm install
```

Installed packages:
- `vitest` - test runner
- `@testing-library/react` - component testing utilities
- `@testing-library/user-event` - realistic user interaction simulation
- `@testing-library/jest-dom` - custom matchers
- `@vitest/ui` - interactive test dashboard
- `jsdom` - browser environment simulation

## References

- Test files: `src/client/frontend/src/components/*.test.tsx`
- Vitest docs: https://vitest.dev/
- Testing Library docs: https://testing-library.com/docs/react-testing-library/intro
- Test utilities: `src/client/frontend/src/test/`
