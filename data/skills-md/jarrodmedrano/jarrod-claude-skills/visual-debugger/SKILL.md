---
name: visual-debugger
description: >
  Interactive visual debugging using Playwright browser automation. Use when asked to visually inspect
  websites/apps, test UI elements, verify button functionality, check responsive design, debug layout
  issues, monitor console errors, or perform any browser-based visual testing. Common triggers include
  requests to check if buttons work, verify page loading, test forms, inspect elements, debug pages,
  navigate to URLs and verify behavior, or any request involving visual browser inspection and testing.
---

# Visual Debugger

Interactive visual debugging tool using Playwright MCP browser automation to inspect, test, and debug web applications and websites.

## Core Capabilities

This skill enables:
1. **Element inspection** - Check visibility, rendering, and positioning of UI elements
2. **Interactive testing** - Click buttons, fill forms, test user flows
3. **Responsive design validation** - Test across viewport sizes
4. **Console monitoring** - Capture JavaScript errors and warnings
5. **Authentication support** - Handle login flows and authenticated sessions


## Prerequisites

Before using this skill, verify Playwright MCP tools are available:

1. Check if `mcp__playwright__browser_navigate` tool is available
2. If NOT available, the Playwright MCP server needs to be enabled:
   - Tell the user: "The Playwright MCP server is not currently enabled. To use visual debugging, please enable the Playwright plugin by running: `/plugins` and enabling 'playwright'"
   - STOP execution until the plugin is enabled
3. If available, proceed with testing

## Workflow


### 1. Initialize Browser Session

Always start by confirming the target and approach:

```
I'll use Playwright to visually debug [target]. Here's my approach:
1. Navigate to [URL]
2. [Specific actions to perform]
3. [What to verify/test]
4. Capture screenshots and console logs

Would you like me to proceed?
```

### 2. Navigation & Setup

Use `mcp__playwright__browser_navigate` to reach the target page:

```typescript
// Navigate to URL
mcp__playwright__browser_navigate({ url: "https://example.com/page" })

// Wait for key elements if needed
mcp__playwright__browser_wait_for({
  selector: "button#submit",
  timeout: 5000
})
```

For **authenticated pages**, handle login first:
1. Navigate to login page
2. Fill credentials using `browser_type` or `browser_fill_form`
3. Click submit with `browser_click`
4. Wait for redirect/dashboard

### 3. Visual Inspection & Testing

**Element Visibility:**
```typescript
// Take screenshot to verify rendering
mcp__playwright__browser_take_screenshot({
  selector: "#target-element",
  full_page: false
})

// Check element state via snapshot
mcp__playwright__browser_snapshot()
```

**Interactive Testing:**
```typescript
// Click button
mcp__playwright__browser_click({ selector: "button#submit" })

// Fill form field
mcp__playwright__browser_type({
  selector: "input#email",
  text: "test@example.com"
})

// Select dropdown option
mcp__playwright__browser_select_option({
  selector: "select#country",
  value: "US"
})
```

**Responsive Design:**
```typescript
// Test mobile viewport
mcp__playwright__browser_resize({
  width: 375,
  height: 667
})
mcp__playwright__browser_take_screenshot({ full_page: true })

// Test tablet
mcp__playwright__browser_resize({
  width: 768,
  height: 1024
})
mcp__playwright__browser_take_screenshot({ full_page: true })

// Test desktop
mcp__playwright__browser_resize({
  width: 1920,
  height: 1080
})
mcp__playwright__browser_take_screenshot({ full_page: true })
```

### 4. Console Monitoring

Capture JavaScript errors and warnings:

```typescript
// Get console messages
const messages = mcp__playwright__browser_console_messages()

// Analyze errors
// Filter for errors, warnings, and relevant logs
// Report findings with severity levels
```

### 5. Report Findings

After testing, provide a structured report:

```markdown
## Visual Debug Report: [Page/Feature Name]

### Actions Performed
- [List of steps taken]

### Findings

#### ✅ Working Correctly
- [Element/feature]: [Description]

#### ⚠️ Issues Found
- [Issue 1]: [Description, severity, screenshot reference]
- [Issue 2]: [Description, severity, screenshot reference]

#### 🔴 Console Errors
- [Error type]: [Message and impact]

### Screenshots
[Include relevant screenshots with captions]

### Recommendations
- [Actionable next steps]
```

## Common Debugging Patterns

### Button Functionality Test
```
1. Navigate to page
2. Locate button via selector
3. Take screenshot of button state (before)
4. Click button
5. Monitor console for errors
6. Take screenshot of result (after)
7. Verify expected behavior occurred
```

### Form Validation Test
```
1. Navigate to form page
2. Screenshot initial state
3. Fill fields (valid and invalid data)
4. Submit form
5. Capture validation messages
6. Check console for errors
7. Verify form behavior
```

### Responsive Layout Test
```
1. Navigate to page
2. For each viewport (mobile/tablet/desktop):
   - Resize browser
   - Take full-page screenshot
   - Check element positioning
   - Note any layout breaks
3. Compare across viewports
```

### Page Load Verification
```
1. Navigate to URL
2. Monitor console during load
3. Wait for key elements
4. Take screenshot when stable
5. Report load time and errors
6. Verify critical elements rendered
```

## Authentication Patterns

### Basic Login Flow
```typescript
// Navigate to login
mcp__playwright__browser_navigate({ url: "https://app.example.com/login" })

// Fill credentials
mcp__playwright__browser_type({
  selector: "input[name='email']",
  text: "user@example.com"
})
mcp__playwright__browser_type({
  selector: "input[name='password']",
  text: "password123"
})

// Submit
mcp__playwright__browser_click({ selector: "button[type='submit']" })

// Wait for redirect
mcp__playwright__browser_wait_for({
  selector: ".dashboard",
  timeout: 5000
})
```

**Security Note:** Never hardcode real credentials. Ask user for test credentials or use environment variables.

## Playwright MCP Tool Reference

**Navigation:**
- `browser_navigate` - Go to URL
- `browser_navigate_back` - Go back in history
- `browser_navigate_forward` - Go forward in history

**Interaction:**
- `browser_click` - Click element
- `browser_type` - Type text into input
- `browser_fill_form` - Fill multiple form fields
- `browser_select_option` - Select dropdown option
- `browser_hover` - Hover over element
- `browser_drag` - Drag and drop
- `browser_press_key` - Press keyboard key

**Inspection:**
- `browser_take_screenshot` - Capture screenshot (full page or element)
- `browser_snapshot` - Get DOM snapshot
- `browser_console_messages` - Get console logs
- `browser_evaluate` - Run JavaScript in browser context

**Waiting:**
- `browser_wait_for` - Wait for element/condition

**Viewport:**
- `browser_resize` - Change viewport size

**Tabs:**
- `browser_tab_list` - List open tabs
- `browser_tab_new` - Open new tab
- `browser_tab_select` - Switch to tab
- `browser_tab_close` - Close tab

**Browser:**
- `browser_install` - Install Playwright browsers
- `browser_close` - Close browser session

## Best Practices

**Always:**
- Confirm approach with user before starting
- Take screenshots as evidence
- Monitor console for errors
- Report findings clearly with severity levels
- Provide actionable recommendations

**Never:**
- Make destructive changes without confirmation
- Test on production without permission
- Hardcode real user credentials
- Ignore console errors
- Skip screenshot evidence

**Progressive Testing:**
1. Start simple (can page load?)
2. Add complexity (can elements be found?)
3. Test interactions (do buttons work?)
4. Verify behavior (is output correct?)
5. Check edge cases (responsive, errors)

## Troubleshooting

**Element not found:**
- Take screenshot to verify page state
- Check selector syntax
- Wait for dynamic content to load
- Inspect DOM snapshot for actual selectors

**Click not working:**
- Verify element is visible and enabled
- Check for overlaying elements
- Wait for animations to complete
- Try hovering before clicking

**Timeout errors:**
- Increase wait timeout for slow pages
- Check network requests for blocking resources
- Verify element selector is correct
- Consider page load vs. element appearance

## Reference Files

For detailed patterns and troubleshooting:
- **references/playwright-patterns.md** - Advanced Playwright usage patterns
- **references/common-issues.md** - Common visual bugs and diagnostic approaches
