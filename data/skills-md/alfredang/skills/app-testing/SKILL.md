---
name: app-testing
description: Test app functionality and mobile responsiveness on localhost or remote live sites using Playwright MCP. Navigates pages, clicks buttons, fills forms, checks content, validates UI behavior, and tests mobile-friendliness across device viewports. Use when running "test app", "test my site", "test the app", "test mobile", or any functional/responsive testing task.
---

# App Testing

Test application functionality and mobile responsiveness on localhost or remote live sites using Playwright MCP browser automation. Navigates pages, interacts with elements, validates content, tests mobile-friendliness across device viewports, and reports results.

## Command
`/test-app` or `test-app`

## Navigate
Testing & QA

## Keywords
test app, test site, test my app, test my site, test localhost, test live site, functional test, ui test, smoke test, e2e test, end to end test, test buttons, test forms, test navigation, test links, playwright test, browser test, test functionality, qa test, test page, test deployed site, test production, verify app, check app works, test-app, test mobile, mobile friendly, responsive test, mobile view, mobile responsiveness, test on phone, mobile testing, responsive design test, viewport test

## Description
Uses Playwright MCP to launch a browser, navigate to your app (localhost or remote URL), and systematically test functionality and mobile responsiveness. Takes snapshots to understand page structure, interacts with elements (clicks, types, selects), validates expected behavior, resizes the browser to mobile/tablet viewports to verify responsive design, and generates a test report with pass/fail results and screenshots of failures.

## Execution
This skill runs using **Claude Code with subscription plan**. Requires the Playwright MCP server to be configured and available. All browser interactions use Playwright MCP tools (browser_navigate, browser_snapshot, browser_click, browser_type, etc.).

## Response
I'll test your app's functionality using Playwright MCP!

The workflow includes:

| Step | Description |
|------|-------------|
| **Discover** | Determine target URL (localhost or remote) |
| **Snapshot** | Take accessibility snapshot to understand page structure |
| **Plan** | Identify testable elements and user flows |
| **Execute** | Run through test scenarios interacting with the app |
| **Validate** | Check expected outcomes after each interaction |
| **Mobile** | Test responsiveness across mobile and tablet viewports |
| **Report** | Generate test summary with pass/fail results |

## Instructions

When executing `/test-app`, follow this workflow:

### Phase 0: Determine Target URL

The user may provide a URL directly or you need to detect it:

1. **If user provides a URL** (e.g., `test-app https://mysite.com` or `test-app localhost:3000`):
   - Use the provided URL directly
   - If just a domain without protocol, prepend `https://`
   - If `localhost` without port, try common ports: 3000, 5173, 8080, 8000, 4321

2. **If no URL provided**, auto-detect:
   - Check for running localhost servers by scanning common ports:
     ```bash
     for port in 3000 5173 8080 8000 4321 8501 5000 9292; do
       lsof -ti:$port >/dev/null 2>&1 && echo "Found server on port $port"
     done
     ```
   - If exactly one server is found, use it
   - If multiple servers found, ask the user which one to test
   - If no server found, check for a deployed URL:
     - Look for `vercel.json`, `.vercel/project.json` for Vercel deployments
     - Look for `CNAME` file or `.github/workflows` for GitHub Pages
     - Check `package.json` for `homepage` field
   - If nothing found, ask the user for the URL

3. **Validate the target is reachable:**
   ```bash
   curl -s -o /dev/null -w "%{http_code}" <URL> 2>/dev/null
   ```
   - If the response is not 2xx or 3xx, inform the user the target is unreachable
   - For localhost, ensure the server is running first (suggest `/start-app` if not)

### Phase 1: Initial Page Load & Snapshot

Navigate to the target URL and capture the initial state:

1. **Navigate to the app:**
   Use `browser_navigate` to open the target URL.

2. **Take accessibility snapshot:**
   Use `browser_snapshot` to get the full page structure. This returns a structured representation of all interactive elements, text content, links, buttons, forms, and navigation.

3. **Take a screenshot for visual reference:**
   Use `browser_take_screenshot` to capture the initial visual state.

4. **Analyze the page structure:**
   From the snapshot, identify:
   - Navigation menus and links
   - Buttons and interactive elements
   - Forms and input fields
   - Main content areas
   - Dynamic elements (dropdowns, modals, tabs)
   - Error messages or broken elements

### Phase 2: Plan Test Scenarios

Based on the page snapshot, plan test scenarios organized by priority:

#### 2.1 Critical Path Tests (always run)
- **Page loads successfully** — no error states, main content renders
- **Navigation works** — all nav links are clickable and lead to valid pages
- **No console errors** — check `browser_console_messages` for errors
- **No broken network requests** — check `browser_network_requests` for failed calls

#### 2.2 Interactive Element Tests
- **Buttons** — click each visible button and verify expected behavior
- **Links** — verify internal links navigate correctly, external links exist
- **Forms** — fill in form fields and submit, verify validation messages
- **Dropdowns/Selects** — open and select options
- **Tabs/Accordions** — toggle and verify content changes
- **Modals/Dialogs** — trigger and verify they open/close properly

#### 2.3 Content Validation Tests
- **Text content** — verify headings, paragraphs, and labels are present
- **Images** — verify images load (no broken image indicators)
- **Lists/Tables** — verify data renders correctly
- **Dynamic content** — verify content loads after API calls

#### 2.4 User Flow Tests (if applicable)
Identify common user flows based on the app type:
- **Auth apps** — login/signup/logout flow
- **E-commerce** — browse/add to cart/checkout flow
- **Forms** — fill/validate/submit flow
- **Dashboards** — navigate between views, filter/sort data
- **Landing pages** — CTA buttons, anchor links, contact forms

### Phase 3: Execute Tests

Run each test scenario using Playwright MCP tools. For each test:

1. **Snapshot before action** — use `browser_snapshot` to understand current state
2. **Perform the action** — use the appropriate Playwright MCP tool:
   - `browser_click` — for buttons, links, tabs
   - `browser_type` — for text inputs
   - `browser_fill_form` — for multiple form fields
   - `browser_select_option` — for dropdowns
   - `browser_press_key` — for keyboard interactions (Enter, Escape, Tab)
   - `browser_hover` — for hover states and tooltips
   - `browser_navigate` — for direct URL navigation
   - `browser_navigate_back` — to return to previous page
3. **Snapshot after action** — use `browser_snapshot` to verify the result
4. **Validate** — check that the expected outcome occurred:
   - Element appeared/disappeared
   - Text changed
   - Page navigated
   - Form submitted successfully
   - Error message displayed for invalid input
5. **Screenshot on failure** — if a test fails, use `browser_take_screenshot` to capture the failure state

#### Test Execution Rules
- **Wait for dynamic content** — use `browser_wait_for` when expecting async changes
- **Handle dialogs** — use `browser_handle_dialog` if alerts/confirms appear
- **Check console** — periodically use `browser_console_messages` to catch JS errors
- **Check network** — use `browser_network_requests` to catch failed API calls
- **Navigate back** — after testing a sub-page, navigate back to continue testing
- **Use tabs** — use `browser_tabs` to manage multiple pages if needed

### Phase 4: Multi-Page Testing

If the app has multiple pages/routes:

1. **Collect all navigation links** from the snapshot
2. **Visit each page** and run Phase 1 (snapshot + basic validation) on each
3. **Test cross-page flows** (e.g., add to cart on page A, verify cart on page B)
4. **Test browser back/forward** navigation

For single-page apps (SPAs):
- Test client-side routing by clicking nav elements
- Verify URL changes in the browser
- Test deep linking by navigating directly to routes

### Phase 5: Mobile Responsiveness Testing

After desktop testing, resize the browser to test mobile-friendliness across common device viewports. This phase ensures the app works well on phones and tablets.

#### 5.1 Define Test Viewports

Test at these standard device sizes (width x height):

| Device | Width | Height | Category |
|--------|-------|--------|----------|
| iPhone SE | 375 | 667 | Small phone |
| iPhone 14 / 15 | 390 | 844 | Standard phone |
| iPhone 14 Pro Max | 430 | 932 | Large phone |
| iPad Mini | 768 | 1024 | Small tablet |
| iPad Air / Pro | 820 | 1180 | Standard tablet |

**At minimum, always test these 3 viewports:**
1. **Small phone** (375×667) — catches tight layout issues
2. **Standard phone** (390×844) — most common mobile device
3. **Tablet** (768×1024) — catches tablet breakpoint issues

#### 5.2 Mobile Test Execution

For **each viewport**, perform the following:

1. **Resize the browser:**
   Use `browser_resize` to set the viewport dimensions:
   ```
   browser_resize(width: 375, height: 667)  // iPhone SE
   ```

2. **Navigate to the main page:**
   Use `browser_navigate` to reload the app at the target URL (ensures fresh responsive layout).

3. **Take a screenshot:**
   Use `browser_take_screenshot` to capture the mobile layout for visual reference.

4. **Take an accessibility snapshot:**
   Use `browser_snapshot` to get the page structure at this viewport size.

5. **Check for mobile layout issues:**
   - **Horizontal overflow** — look for horizontal scrollbars or content extending beyond the viewport. Use `browser_evaluate` to check:
     ```javascript
     () => document.documentElement.scrollWidth > document.documentElement.clientWidth
     ```
   - **Viewport meta tag** — verify the page has a proper viewport meta tag. Use `browser_evaluate`:
     ```javascript
     () => {
       const meta = document.querySelector('meta[name="viewport"]');
       return meta ? meta.getAttribute('content') : 'MISSING';
     }
     ```
   - **Touch target sizes** — verify buttons and links are at least 44x44px for tap accessibility. Use `browser_evaluate`:
     ```javascript
     () => {
       const issues = [];
       document.querySelectorAll('a, button, [role="button"], input, select, textarea').forEach(el => {
         const rect = el.getBoundingClientRect();
         if (rect.width > 0 && rect.height > 0 && (rect.width < 44 || rect.height < 44)) {
           issues.push({ tag: el.tagName, text: el.textContent?.slice(0, 30), width: Math.round(rect.width), height: Math.round(rect.height) });
         }
       });
       return issues.length > 0 ? issues : 'ALL PASS';
     }
     ```
   - **Text readability** — check that body font size is at least 16px (prevents auto-zoom on iOS). Use `browser_evaluate`:
     ```javascript
     () => {
       const body = document.body;
       const fontSize = parseFloat(window.getComputedStyle(body).fontSize);
       const inputs = document.querySelectorAll('input, textarea, select');
       const smallInputs = [];
       inputs.forEach(el => {
         const size = parseFloat(window.getComputedStyle(el).fontSize);
         if (size < 16) smallInputs.push({ tag: el.tagName, type: el.type, fontSize: size });
       });
       return { bodyFontSize: fontSize, inputsBelow16px: smallInputs.length > 0 ? smallInputs : 'NONE' };
     }
     ```

6. **Test mobile navigation:**
   - **Hamburger menu** — look for a hamburger/menu icon button in the snapshot. If found:
     - Click it with `browser_click`
     - Snapshot to verify the mobile nav menu opens
     - Verify all navigation links are visible and clickable
     - Click each nav link to verify it works
     - Verify the menu can be closed (click hamburger again, click outside, or press Escape)
   - **Sticky/fixed headers** — scroll down and verify header stays visible if sticky. Use `browser_evaluate`:
     ```javascript
     () => {
       window.scrollTo(0, 500);
       const header = document.querySelector('header, nav, [role="banner"]');
       if (!header) return 'NO HEADER FOUND';
       const rect = header.getBoundingClientRect();
       return { isVisible: rect.top >= 0 && rect.bottom <= window.innerHeight, top: rect.top };
     }
     ```
   - **Bottom navigation** — if a mobile bottom nav exists, verify it stays fixed at bottom

7. **Test mobile-specific interactions:**
   - **Scroll behavior** — use `browser_evaluate` to scroll and verify smooth scrolling works:
     ```javascript
     () => { window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' }); return 'scrolled to bottom'; }
     ```
   - **Forms on mobile** — verify form fields are usable (not hidden behind keyboard, proper input types)
   - **Modals/overlays** — if tested in desktop phase, re-test that modals fit within mobile viewport
   - **Images** — verify images scale down and don't overflow the viewport
   - **Tables** — check if tables have horizontal scroll wrappers or responsive alternatives

8. **Test content stacking:**
   - Verify multi-column layouts properly stack to single-column on mobile
   - Check that sidebars collapse or move below main content
   - Verify cards/grid items reflow properly

#### 5.3 Responsive Breakpoint Transitions

After testing individual viewports, test the transition between breakpoints:

1. Start at desktop (1280×800) with `browser_resize`
2. Step down through breakpoints:
   - 1024×768 (small desktop / landscape tablet)
   - 768×1024 (tablet portrait)
   - 390×844 (phone)
3. At each step, take a snapshot and screenshot to verify:
   - Layout transitions smoothly (no broken intermediate states)
   - Navigation switches between desktop and mobile modes at an appropriate breakpoint
   - Content remains accessible at every width

#### 5.4 Restore Desktop Viewport

After mobile testing, restore the browser to desktop size:
```
browser_resize(width: 1280, height: 800)
```

### Phase 6: Generate Test Report

After all tests complete, generate a structured report:

```
## Test Report

**Target:** <URL>
**Date:** <current date/time>
**Total Tests:** <count>
**Passed:** <count>  |  **Failed:** <count>  |  **Skipped:** <count>

### Results

| # | Test | Status | Details |
|---|------|--------|---------|
| 1 | Page loads successfully | PASS | Main content rendered in <X>ms |
| 2 | Navigation - Home link | PASS | Navigated to / |
| 3 | Navigation - About link | PASS | Navigated to /about |
| 4 | Login form submission | FAIL | Expected redirect, got validation error |
| 5 | Contact form - empty submit | PASS | Validation messages displayed |
| ... | ... | ... | ... |

### Failures

#### Test 4: Login form submission
- **Action:** Filled email/password and clicked Submit
- **Expected:** Redirect to dashboard
- **Actual:** Validation error "Invalid credentials"
- **Screenshot:** [captured]

### Console Errors
- [error] Failed to load resource: /api/users (404)
- [warning] React: Each child in a list should have a unique "key" prop

### Network Issues
- GET /api/users → 404 Not Found
- POST /api/login → 500 Internal Server Error

### Mobile Responsiveness

| Viewport | Status | Issues |
|----------|--------|--------|
| iPhone SE (375×667) | PASS/FAIL | Details |
| iPhone 14 (390×844) | PASS/FAIL | Details |
| iPad Mini (768×1024) | PASS/FAIL | Details |

#### Mobile Issues Found
- **Horizontal overflow** on iPhone SE — content extends 40px beyond viewport
- **Touch targets too small** — 3 buttons under 44px height on mobile nav
- **Missing viewport meta tag** — page does not have `<meta name="viewport">`
- **Input font size < 16px** — email input has 14px font (causes iOS auto-zoom)
- **Hamburger menu not functional** — menu icon present but click has no effect

### Recommendations
- Fix the /api/users endpoint returning 404
- Add proper error handling for login failures
- Add alt text to images on the homepage
- Add `<meta name="viewport" content="width=device-width, initial-scale=1">` if missing
- Increase touch target sizes to minimum 44×44px
- Set input font sizes to at least 16px to prevent iOS auto-zoom
- Add responsive breakpoints for mobile layouts
```

### Phase 7: Cleanup

After testing:
1. Close the browser with `browser_close`
2. Display the test report to the user
3. If failures were found, offer to:
   - Investigate specific failures in more detail
   - Re-run failed tests after fixes
   - Take additional screenshots

## Advanced Usage

### Testing with Arguments

Users can pass specific test targets:

- `/test-app` — auto-detect URL, run all tests
- `/test-app http://localhost:3000` — test specific localhost
- `/test-app https://mysite.com` — test remote site
- `/test-app https://mysite.com/login` — test specific page
- `/test-app --forms` — focus on form testing
- `/test-app --nav` — focus on navigation testing
- `/test-app --a11y` — focus on accessibility checks
- `/test-app --mobile` — focus on mobile responsiveness testing only
- `/test-app --responsive` — run full responsive test across all viewports

### Testing Remote vs Local

**Localhost testing:**
- Can test with hot-reload (changes reflect immediately)
- Can test authenticated flows with test credentials
- Can test API endpoints directly

**Remote/live site testing:**
- Tests the deployed production build
- Validates CDN, SSL, and production configs
- Can catch deployment-specific issues
- Respects rate limits and avoids destructive actions (no form submissions with real data unless explicitly requested)

## Capabilities

- Navigate to any localhost or remote URL via Playwright MCP
- Take accessibility snapshots to understand full page structure
- Click buttons, links, tabs, and any interactive elements
- Fill and submit forms with test data
- Validate page content, navigation, and UI behavior
- Capture screenshots for visual verification and failure documentation
- Check browser console for JavaScript errors
- Monitor network requests for failed API calls
- Test multi-page flows and SPA client-side routing
- Handle browser dialogs (alerts, confirms, prompts)
- **Test mobile responsiveness** by resizing to phone/tablet viewports (iPhone SE, iPhone 14, iPad Mini, etc.)
- **Detect mobile layout issues** — horizontal overflow, small touch targets, missing viewport meta, font size issues
- **Test mobile navigation** — hamburger menus, sticky headers, bottom nav bars
- **Verify responsive breakpoint transitions** — layout changes smoothly from desktop to mobile
- Generate structured test reports with pass/fail results including mobile responsiveness section

## Notes

- This skill requires Playwright MCP to be configured in Claude Code
- For localhost testing, ensure the app is running first (use `/start-app` if needed)
- The skill does NOT modify any application code — it only reads and interacts via the browser
- Remote site testing avoids destructive actions by default (no real purchases, account deletions, etc.)
- Form testing uses obviously fake test data (e.g., test@example.com, "Test User")
- Screenshots are captured for failures to help debug issues
- Console and network errors are always checked even if not explicitly requested
