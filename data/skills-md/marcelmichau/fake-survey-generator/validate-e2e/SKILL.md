---
name: validate-e2e
description: Validates features end-to-end using Playwright MCP to navigate the UI and verify feature behavior. Use this skill to confirm that implemented features work correctly in the running application from a user's perspective. Supports feature-aware happy-path validation tailored to the specific feature requirements.
---

# Validate E2E Skill

Use this skill to interactively validate that implemented features work correctly by navigating the UI and verifying expected behavior.

## What This Skill Does

1. Receives the UI endpoint URL from Aspire runtime (typically `https://localhost:3000`)
2. Receives feature context/requirements from the user or implementation notes
3. Uses Playwright MCP browser tools to navigate the UI
4. Executes feature-specific validation flows tailored to the requirements
5. Verifies UI state changes, element properties, API responses
6. Reports validation results (pass/fail per step) with evidence
7. Exits with failure if any assertions fail or expected behavior is not observed

## When to Use

- After Aspire runtime is healthy and running
- After builds and tests all pass
- To validate feature behavior matches requirements (happy-path workflows)
- To verify UI state changes and interactions work correctly
- To confirm API integration from the user's perspective

## How the Agent Should Use This Skill

### Step 1: Understand Feature Context

Before starting E2E validation, understand what feature is being validated. Examples:
- **Feature**: "Change survey creation button color to purple"
  - **Validation Flow**: Navigate to survey list page → verify button color is purple
  
- **Feature**: "Add user registration flow with Auth0"
  - **Validation Flow**: Navigate to login → register new user → verify user is authenticated
  
- **Feature**: "Create new survey with questions"
  - **Validation Flow**: Login → navigate to create survey → add title and questions → verify survey appears in list

### Step 2: Navigate to UI

Use Playwright MCP `navigate` tool to go to the UI endpoint:
```
Navigate to: https://localhost:3000
```

### Step 3: Execute Feature-Specific Happy-Path

Based on the feature being validated, execute appropriate steps:

#### Generic Happy-Path Flows

**User Registration Flow** (if feature involves user management):
1. Take page snapshot to see current UI
2. Click "Register" or "Sign Up" button
3. Fill in user registration form (email, name, etc.)
4. Submit form
5. Verify successful registration (redirect to home or dashboard, welcome message)

**Survey Creation Flow** (if feature involves survey creation):
1. Navigate to/login to application
2. Click "Create Survey" or "New Survey" button
3. Fill in survey title and description
4. Verify form validation works (try invalid inputs)
5. Submit form
6. Verify survey appears in survey list
7. Verify survey details load correctly

**Survey Completion Flow** (if feature involves completing surveys):
1. Navigate to available surveys
2. Click "Take Survey" or "Complete" button
3. Answer survey questions
4. Submit responses
5. Verify completion confirmation
6. Verify survey results/summary displayed

**Feature-Specific Validation**:
- For "purple button" feature: verify specific element has correct CSS color property
- For "API integration" feature: use Network tab inspection to verify API calls were made
- For "form validation" feature: test invalid inputs and verify error messages appear
- For "sorting/filtering" feature: apply sort/filter and verify results are correct order

### Step 4: Assert Expected State

For each validation step, use Playwright to verify:
- **Element Presence**: Element exists on page (`getByRole('button', { name: 'Create' })`)
- **Element Properties**: Check specific attributes (color, text content, disabled state)
- **Page Navigation**: Verify redirect/navigation happened (`currentURL` contains expected path)
- **Error Messages**: Verify error or success messages appear
- **List Content**: Verify items in lists match expected values

### Step 5: Report Results

Document findings:
- ✅ Pass: Step executed successfully, assertion verified
- ❌ Fail: Step failed, assertion not met (include details: expected vs. actual)
- ⚠️  Partial: Feature works but with caveats (e.g., layout issue but functionality OK)

## Example E2E Validation Scenarios

### Scenario 1: Change Button Color to Purple
```
Requirement: Make the "Create Survey" button purple
Validation:
1. Navigate to https://localhost:3000
2. Locate "Create Survey" button
3. Inspect button element for CSS color property
4. Verify color matches purple (e.g., rgb(128, 0, 128) or #800080)
Result: ✅ Button is purple OR ❌ Button is still blue
```

### Scenario 2: User Registration
```
Requirement: Add Auth0-based user registration
Validation:
1. Navigate to https://localhost:3000
2. Click "Sign Up" link
3. Fill registration form (email: test@example.com, name: Test User)
4. Submit form
5. Verify redirect to dashboard or home page
6. Verify user name displayed in UI
Result: ✅ Registration successful, user authenticated OR ❌ Registration failed
```

### Scenario 3: Create and List Surveys
```
Requirement: Allow users to create surveys and see them in list
Validation:
1. Navigate to https://localhost:3000 and authenticate
2. Click "Create Survey"
3. Fill form (title: "Test Survey", description: "Test Description")
4. Submit
5. Verify redirect to survey details or list page
6. Verify new survey appears in list with correct title
Result: ✅ Survey created and visible in list OR ❌ Survey not created/not visible
```

## Using Playwright MCP Tools

Key Playwright MCP tools available for this skill:

- **Navigate**: Go to URL
  ```
  mcp_playwright_browser_navigate(url: "https://localhost:3000")
  ```

- **Click**: Click an element
  ```
  mcp_playwright_browser_click(element: "Create Survey button", ref: "button[name='create']")
  ```

- **Fill Form**: Fill input fields
  ```
  mcp_playwright_browser_fill_form(fields: [{name: "Email", type: "textbox", ref: "input[type='email']", value: "test@example.com"}])
  ```

- **Evaluate**: Run JavaScript to inspect state
  ```
  mcp_playwright_browser_evaluate(function: "() => document.querySelector('button').textContent")
  ```

- **Take Snapshot**: Capture accessibility snapshot of page
  ```
  (Use activate_page_capture_tools to access screenshot tools)
  ```

- **Wait For**: Wait for text or UI to appear
  ```
  mcp_playwright_browser_wait_for(text: "Survey created successfully")
  ```

## Success Criteria

- All feature-specific validation steps execute without errors
- All assertions pass (elements exist, properties match, navigation works)
- No UI errors or broken state observed
- User can complete the intended workflow

## Failure Indicators

- Any assertion fails (element missing, property mismatch, navigation broken)
- JavaScript errors in browser console
- Unexpected navigation or state
- Error messages appearing where success expected
- Timeout waiting for expected elements/text

## Important Notes

- **Feature Context**: The specifics of what to validate depend on the feature requirements. Tailor the flow to the actual feature being implemented.
- **Authentication**: Some flows may require authentication. If starting from unauthenticated state, include login step if needed.
- **Timing**: Some operations take time (API calls, page loads). Use `wait_for` to wait for UI updates.
- **Browser State**: Each validation run starts fresh; previous state is not retained between runs.
- **Developer Certificates**: UI uses developer HTTPS certificates; browser will trust them (auto-configured).

## Cleanup

After E2E validation completes, manually stop Aspire:
```
Press Ctrl+C in the terminal running `aspire run`
```

## Next Steps

- If validation passes: Feature implementation is complete and validated ✅
- If validation fails: Report failures to user for debugging/fixing
