---
name: dev-test
description: Automated testing after implementation using Playwright
version: 1.0.0
---

# /dev-test - Implementation Testing

> **Skill Awareness**: See `skills/_registry.md` for all available skills.
> - **After**: `/dev-coding` implementation complete
> - **Auto-triggered**: By `/dev-coding` after implementation
> - **If fails**: Loop back to fix, then re-test

Automated testing using Playwright to verify implementation works correctly.

## When to Use

- After completing feature implementation
- After fixing bugs
- Before code review
- Before committing changes

## Usage

```
/dev-test                         # Test current implementation
/dev-test UC-AUTH-001             # Test specific use case
/dev-test --url http://...        # Test specific URL
/dev-test --fix                   # Auto-fix issues found
```

## What It Tests

| Check | Method | Catches |
|-------|--------|---------|
| Console Errors | `browser_console_messages` | JS errors, React errors, warnings |
| Network Failures | `browser_network_requests` | API 4xx/5xx, failed fetches, timeouts |
| Visual State | `browser_snapshot` | Render errors, missing elements |
| Interactions | `browser_click`, `browser_type` | Form failures, broken buttons |

## Expected Outcome

Test report showing whether implementation works correctly.

**Report includes:**
- Overall status (Pass/Fail + issue count)
- Issues found (critical/warning with location + suggested fix)
- Test steps executed (which passed/failed)
- Suggested fixes or next actions

## Success Criteria

- No console errors during user flows
- No network failures (API 4xx/5xx)
- Expected elements render correctly
- User interactions work as expected
- Happy path completes successfully
- All acceptance criteria from spec verified

## What to Test

**From UC spec:**
- Expected user flows (happy path)
- Required inputs and outputs
- Acceptance criteria
- Error scenarios (if specified)

**From recent changes:**
- Modified components/endpoints
- New functionality added

## Error Detection

| Check | What It Catches |
|-------|----------------|
| Console Errors | JS errors, React errors, warnings, unhandled promises |
| Network Failures | API 4xx/5xx, failed fetches, timeouts |
| Visual State | Render errors, missing elements, wrong state |
| Interactions | Form failures, broken buttons, navigation issues |

**Error categories:**
- 🔴 **Critical:** Breaks functionality, must fix
- 🟡 **Warning:** Should fix, not blocking

## Test Approach

**1. Prepare:**
- Identify what to test (from spec + recent changes)
- Determine test URL (from spec or default: http://localhost:3000)
- Verify dev server running (prompt if not)

**2. Execute User Flows:**
- Navigate to page
- Capture initial state (check page loads, no immediate errors)
- Execute happy path (fill forms, click buttons, navigate)
- Wait for expected results
- Capture final state

**3. Collect Errors:**
- Console messages (errors, warnings)
- Network requests (find failures)
- Visual issues (missing elements)

**4. Report:**
- Status (pass/fail + count)
- Issues with severity, location, suggested fix
- Test steps executed (which passed/failed)

**5. Fix Loop (if --fix):**
- For each issue: read file, identify fix, apply fix, re-test
- Continue until fixed or max iterations (3) or needs user input
- Re-run full test to verify

## Test Patterns

Available as reference in original SKILL.md:
- Form submission
- Navigation flow
- API response validation
- Error state testing

Use Playwright MCP tools to interact with browser.

## Test Patterns

### Form Submission

```typescript
// 1. Fill form
await browser_fill_form({
  fields: [
    { name: 'Email', type: 'textbox', ref: 'input-email', value: 'test@test.com' },
    { name: 'Password', type: 'textbox', ref: 'input-password', value: 'password123' }
  ]
});

// 2. Submit and wait
await browser_click({ element: 'Submit button', ref: 'btn-submit' });
await browser_wait_for({ text: 'Success' });

// 3. Check for errors
const errors = await browser_console_messages({ level: 'error' });
```

### Navigation Flow

```typescript
// 1. Start at page A
await browser_navigate({ url: '/dashboard' });

// 2. Click to page B
await browser_click({ element: 'Settings link', ref: 'nav-settings' });
await browser_wait_for({ text: 'Settings' });

// 3. Verify correct page
const snapshot = await browser_snapshot({});
// Check snapshot contains expected elements
```

### API Response Validation

```typescript
// 1. Trigger API call (via form submit or button)
await browser_click({ element: 'Load data', ref: 'btn-load' });
await browser_wait_for({ time: 2 });

// 2. Check network requests
const requests = await browser_network_requests({});

// 3. Find the API call
const apiCall = requests.find(r => r.url.includes('/api/data'));

// 4. Validate
if (apiCall.status >= 400) {
  // Report error
}
```

### Error State Testing

```typescript
// Test error handling by submitting invalid data
await browser_type({
  element: 'email',
  ref: 'input-email',
  text: 'invalid-email'  // No @ symbol
});

await browser_click({ element: 'Submit', ref: 'btn-submit' });

// Verify error message appears
const snapshot = await browser_snapshot({});
// Check for validation error in snapshot
```

## Test Data

Use predictable test data:

```typescript
const TEST_DATA = {
  validEmail: 'test@example.com',
  validPassword: 'Test123!@#',
  invalidEmail: 'not-an-email',
  shortPassword: '123',
};
```

For existing data, check spec or use API to fetch valid IDs.

## Common Issues & Solutions

### Issue: Page Not Loading

```
Symptom: Navigation fails or times out
Check:
1. Is dev server running? (npm run dev)
2. Correct port? (3000, 3001, etc.)
3. Any build errors?
```

### Issue: Element Not Found

```
Symptom: Click/type fails with "element not found"
Check:
1. Take snapshot to see current state
2. Is element conditionally rendered?
3. Has ref changed since snapshot?
4. Is page still loading?
```

### Issue: Intermittent Failures

```
Symptom: Test passes sometimes, fails sometimes
Check:
1. Add wait_for before interactions
2. Check for race conditions
3. Increase timeout for slow APIs
```

## Integration with /dev-coding

When `/dev-coding` completes:

```markdown
## Implementation Complete

Backend: ✓ API endpoints created
Frontend: ✓ Components built

**Next Step**: Running /dev-test to verify...

[Auto-triggers /dev-test]
```

If tests fail, `/dev-test` can:
1. Report issues for manual fix
2. Auto-fix with `--fix` flag
3. Re-run until passing

## Tools Used

| Tool | Purpose |
|------|---------|
| `mcp__playwright__browser_navigate` | Go to test URL |
| `mcp__playwright__browser_snapshot` | Capture page state |
| `mcp__playwright__browser_type` | Fill form inputs |
| `mcp__playwright__browser_click` | Click buttons/links |
| `mcp__playwright__browser_wait_for` | Wait for elements/time |
| `mcp__playwright__browser_console_messages` | Get JS errors |
| `mcp__playwright__browser_network_requests` | Get API responses |
| `Read` | Read spec for expected behavior |
| `Edit` | Fix issues (with --fix) |

## Output Locations

Test reports are informational and displayed inline. No files created unless requested.

For saved reports:
```
plans/features/{feature}/test-reports/
└── {date}-{UC-ID}.md
```
