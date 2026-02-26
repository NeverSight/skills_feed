---
name: playwright-debugging
description: Use when Playwright scripts fail, tests are flaky, selectors stop working, or timeouts occur - provides systematic debugging approach for browser automation issues
user-invocable: false
---

# Playwright Debugging

## Overview

Browser automation failures fall into predictable categories. This skill provides a systematic approach to diagnose and fix issues quickly.

## When to Use

- Scripts that worked before now fail
- Intermittent test failures (flakiness)
- "Element not found" errors
- Timeout errors
- Unexpected behavior in automation
- Elements not interactable

**When NOT to use:**
- Writing new automation (use playwright-patterns skill)
- API or backend debugging

## Quick Reference

| Problem | First Action |
|---------|-------------|
| Timeout on locator | Run with `--ui` mode, check element state with `.count()`, `.isVisible()` |
| Flaky test (passes sometimes) | Replace `waitForTimeout()` with condition-based waits |
| "Element not visible" | Check computed styles, wait for overlays to disappear |
| Works locally, fails CI | Use `waitForLoadState('networkidle')`, increase timeout |
| Element not clickable | Check if covered by overlay, wait for animations to complete |
| Stale element | Re-query after navigation instead of storing locator |

## Diagnostic Framework

### 1. Reproduce and Isolate

**First step: Can you reproduce it?**

```javascript
// Run single test to isolate issue
npx playwright test path/to/test.spec.js

// Run with headed mode to observe
npx playwright test --headed

// Run with slow motion
npx playwright test --headed --slow-mo=1000
```

**Questions to answer:**
- Does it fail consistently or intermittently?
- Does it fail in all browsers or just one?
- Does it fail in headed and headless mode?
- Did something change recently (site update, code change)?

### 2. Add Visibility

**Use UI Mode for interactive debugging:**

```bash
# Best for local development - provides time-travel debugging
npx playwright test --ui
```

UI Mode gives you:
- Visual timeline of all actions
- Watch mode for re-running on file changes
- Network and console tabs
- Time-travel through test execution

**Use Inspector to step through tests:**

```bash
# Step through test execution with live browser
npx playwright test --debug
```

Inspector allows:
- Stepping through actions one at a time
- Picking locators directly from the browser
- Editing selectors live and seeing results
- Viewing actionability logs

**Take screenshots at failure point:**

```javascript
// Before failing action
await page.screenshot({ path: 'before-action.png', fullPage: true });

// Try action
try {
  await page.click('.button');
} catch (error) {
  await page.screenshot({ path: 'after-error.png', fullPage: true });
  throw error;
}
```

**Enable verbose logging:**

```bash
# API-level debugging
DEBUG=pw:api npx playwright test

# Browser DevTools with playwright object
PWDEBUG=console npx playwright test
```

With `PWDEBUG=console`, you get DevTools access to:
```javascript
// In browser console
playwright.$('.selector')      // Query with Playwright engine
playwright.$$('selector')      // Get all matches
playwright.inspect('selector') // Highlight in Elements panel
playwright.locator('selector') // Create locator
```

**Use trace viewer:**

```javascript
// Record trace
await context.tracing.start({ screenshots: true, snapshots: true });
// ... your test code
await context.tracing.stop({ path: 'trace.zip' });

// View trace
npx playwright show-trace trace.zip
```

**Organize traces with test steps:**

```javascript
// Group actions in trace viewer
await test.step('Login', async () => {
  await page.fill('input[name="username"]', 'user');
  await page.click('button[type="submit"]');
});

await test.step('Navigate to dashboard', async () => {
  await page.click('a[href="/dashboard"]');
});
```

**Add descriptions to locators for clarity:**

```javascript
// Descriptions appear in trace viewer and reports
const submitButton = page.locator('#submit').describe('Submit button');
await submitButton.click();
```

**VS Code debugging:**

Install the Playwright VS Code extension for:
- Live debugging with breakpoints in VS Code
- Locator highlighting in browser while editing
- "Show Browser" option for real-time feedback
- Right-click "Debug Test" on any test

This integrates debugging directly into your editor workflow.

### 3. Inspect Element State

**Check if element exists:**

```javascript
const element = page.locator('.button');

// Does it exist in DOM?
const count = await element.count();
console.log(`Found ${count} elements`);

// Is it visible?
const isVisible = await element.isVisible();
console.log(`Visible: ${isVisible}`);

// Is it enabled?
const isEnabled = await element.isEnabled();
console.log(`Enabled: ${isEnabled}`);

// Get all attributes
const attrs = await element.evaluate(el => ({
  classes: el.className,
  id: el.id,
  display: window.getComputedStyle(el).display,
  visibility: window.getComputedStyle(el).visibility,
  opacity: window.getComputedStyle(el).opacity
}));
console.log(attrs);
```

### 4. Verify Selector

**Test selector in browser console:**

```javascript
// Use page.evaluate to test selector
const found = await page.evaluate(() => {
  const el = document.querySelector('.button');
  return el ? {
    text: el.textContent,
    visible: el.offsetParent !== null,
    enabled: !el.disabled
  } : null;
});
console.log('Selector test:', found);
```

**Check for multiple matches:**

```javascript
// Are there multiple elements?
const all = await page.locator('.button').all();
console.log(`Found ${all.length} matching elements`);

// Get text of all matches
const texts = await page.locator('.button').allTextContents();
console.log('All matching texts:', texts);
```

## Common Issues and Fixes

### Issue: Element Not Found

**Causes:**
- Selector is wrong
- Element hasn't loaded yet
- Element is in iframe
- Element is dynamically created

**Debug steps:**

```javascript
// 1. Check if selector exists at all
const exists = await page.locator('.button').count() > 0;
console.log('Element exists:', exists);

// 2. Wait for element explicitly (modern approach)
await page.locator('.button').waitFor({ timeout: 10000 });
// Or let auto-waiting handle it:
await page.locator('.button').click();

// 3. Check if in iframe
const frame = page.frameLocator('iframe');
await frame.locator('.button').click();

// 4. Dump all matching elements
const all = await page.evaluate(() => {
  return Array.from(document.querySelectorAll('button')).map(el => ({
    text: el.textContent,
    classes: el.className,
    id: el.id
  }));
});
console.log('All buttons on page:', all);
```

### Issue: Element Not Visible/Clickable

**Causes:**
- Element is hidden (CSS: display:none, visibility:hidden)
- Element is covered by another element
- Element is outside viewport
- Element hasn't finished animating

**Debug steps:**

```javascript
// 1. Check computed styles
const styles = await page.locator('.button').evaluate(el => ({
  display: window.getComputedStyle(el).display,
  visibility: window.getComputedStyle(el).visibility,
  opacity: window.getComputedStyle(el).opacity,
  zIndex: window.getComputedStyle(el).zIndex
}));
console.log('Element styles:', styles);

// 2. Scroll into view
await page.locator('.button').scrollIntoViewIfNeeded();

// 3. Wait for element to be stable (not animating)
await expect(page.locator('.button')).toBeVisible();
await page.waitForTimeout(100); // Brief wait for animation

// 4. Force click if needed (last resort)
await page.locator('.button').click({ force: true });
```

### Issue: Timing/Race Conditions

**Causes:**
- Network requests not complete
- JavaScript still executing
- Animations in progress
- Dynamic content loading

**Debug steps:**

```javascript
// 1. Wait for network to be idle
await page.goto('https://example.com');
await page.waitForLoadState('networkidle');

// 2. Wait for specific network request
await page.waitForResponse(resp =>
  resp.url().includes('/api/data') && resp.status() === 200
);

// 3. Wait for JavaScript condition
await page.waitForFunction(() =>
  window.dataLoaded === true
);

// 4. Wait for element count to stabilize
await expect(page.locator('.item')).toHaveCount(10);
```

### Issue: Stale Element Reference

**Causes:**
- Page refreshed or navigated
- Element was removed and re-added to DOM
- Dynamic content replaced element

**Fix:**

```javascript
// DON'T store element handles across navigation
const button = page.locator('.button'); // BAD: might become stale
await page.goto('/other-page');
await button.click(); // ERROR: stale

// DO re-query after navigation
await page.goto('/other-page');
await page.locator('.button').click(); // GOOD: fresh query
```

### Issue: Form Submission Not Working

**Causes:**
- JavaScript validation preventing submit
- Event listeners not attached yet
- Form action not set correctly

**Debug steps:**

```javascript
// 1. Verify form state before submit
const formState = await page.evaluate(() => {
  const form = document.querySelector('form');
  return {
    action: form?.action,
    method: form?.method,
    valid: form?.checkValidity()
  };
});
console.log('Form state:', formState);

// 2. Trigger form events manually
await page.fill('input[name="email"]', 'test@example.com');
await page.dispatchEvent('input[name="email"]', 'blur');

// 3. Use form.submit() instead of clicking button
await page.evaluate(() => document.querySelector('form').submit());
```

## Common Mistakes

| Mistake | Why It's Wrong | Right Approach |
|---------|---------------|----------------|
| Adding `waitForTimeout(5000)` | Masks timing issues, makes tests slower, unreliable | Use condition-based waits: `expect().toBeVisible()` |
| Force-clicking without understanding why | Bypasses Playwright's actionability checks | Diagnose WHY element isn't clickable, fix root cause |
| Not using modern debugging tools | Slower diagnosis, guessing at issues | Start with `--ui` or `--debug` for visual debugging |
| Testing only in headed mode | Hides timing issues that appear in CI | Always test in headless mode too |
| Using brittle selectors | Breaks when HTML structure changes | Use role-based or data-testid selectors |
| Skipping trace viewer | Miss detailed timeline of what happened | Enable tracing for failing tests |

## Debugging Checklist

When automation fails, check in this order:

1. ☐ Can I reproduce the failure consistently?
2. ☐ Does it fail in headed mode with slow motion?
3. ☐ Have I taken screenshots before/after the failure?
4. ☐ Does the selector actually match an element?
5. ☐ Is the element visible and enabled?
6. ☐ Is the element in an iframe?
7. ☐ Have I waited for page load to complete?
8. ☐ Is there dynamic content that needs time to load?
9. ☐ Are there network requests still in flight?
10. ☐ Have I checked browser console for JavaScript errors?

## Debugging Tools Reference

| Tool | Command | Use When |
|------|---------|----------|
| UI Mode | `--ui` | Time-travel debugging with visual timeline (best for local dev) |
| Inspector | `--debug` | Step through test execution, pick locators live |
| Headed mode | `--headed` | Need to see browser |
| Slow motion | `--slow-mo=1000` | Actions too fast to observe |
| Debug mode | `PWDEBUG=1` | Open Inspector (older approach, prefer --debug) |
| Console debug | `PWDEBUG=console` | Access browser DevTools with playwright object |
| Trace viewer | `show-trace trace.zip` | Need full timeline analysis |
| Screenshot | `page.screenshot()` | Need visual evidence |
| Console logs | `DEBUG=pw:api` | Need API call details |
| Pause | `await page.pause()` | Need to inspect manually |

## Flakiness Patterns

### Flaky: Works 80% of the time

**Likely cause:** Race condition

**Fix:**
```javascript
// Replace arbitrary waits
await page.waitForTimeout(2000); // BAD

// With condition-based waits
await expect(page.locator('.result')).toBeVisible(); // GOOD
```

### Flaky: Fails on CI but works locally

**Likely cause:** Timing differences

**Fix:**
```javascript
// Increase default timeout for CI
test.setTimeout(60000);
page.setDefaultTimeout(30000);

// Wait for network idle
await page.waitForLoadState('networkidle');
```

### Flaky: Fails with "element not clickable"

**Likely cause:** Overlapping elements or animations

**Fix:**
```javascript
// Wait for element to be actionable
await expect(page.locator('.button')).toBeVisible();
await expect(page.locator('.button')).toBeEnabled();

// Or wait for overlay to disappear
await expect(page.locator('.loading-overlay')).not.toBeVisible();
```

## Remember

**Debugging priorities:**
1. Reproduce the issue reliably
2. Add visibility (screenshots, logs, traces)
3. Verify element state and selector
4. Check timing and waits
5. Test in different modes (headed, browsers)

**Auto-waiting advantages:**
Playwright automatically waits for elements to be:
- Attached to DOM
- Visible
- Enabled and stable
- Not covered by overlays

Most actions (click, fill, etc.) include auto-waiting. Explicit waits are only needed for complex conditions.

Most Playwright issues are timing-related. Replace arbitrary timeouts with condition-based waits. When in doubt, slow down and observe in headed mode with `--ui` or `--debug`.
