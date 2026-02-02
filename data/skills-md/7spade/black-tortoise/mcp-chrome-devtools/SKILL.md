---
name: mcp-chrome-devtools
description: Use the Chrome DevTools MCP server (io.github.ChromeDevTools/chrome-devtools-mcp) for browser automation, navigation, form interaction, and UI flow validation in Chrome; use when testing Black-Tortoise Angular application UI behavior and user flows.
---

# MCP Skill: Chrome DevTools MCP (Browser Automation)

## Scope
Use the MCP server configured as `io.github.ChromeDevTools/chrome-devtools-mcp` in `.vscode/mcp.json` and `.codex/mcp.json` to run browser automation tasks (navigation, form filling, clicking, screenshots, console monitoring) during testing and validation.

## Preconditions
- Ensure `.vscode/mcp.json` and `.codex/mcp.json` contain `io.github.ChromeDevTools/chrome-devtools-mcp` server configuration.
- Ensure the Black-Tortoise app is running locally (typically `pnpm start` on http://localhost:4200).
- Chrome browser should be available on the system.

## Operating Rules
- Prefer semantic selectors: `data-testid`, `role`, `aria-label`, `id`, or stable class names.
- Avoid brittle selectors based on dynamic classes or deep DOM paths.
- Always wait for page load and element visibility before interaction.
- Capture screenshots for evidence and debugging.
- Monitor console errors/warnings during automation.
- Use explicit waits instead of fixed delays.

## Core Capabilities

### 1. Navigation
- Navigate to URLs (absolute or relative)
- Handle page transitions and redirects
- Wait for page load completion
- Verify URL changes

### 2. Form Interaction
- Fill text inputs
- Click buttons and links
- Select dropdowns
- Submit forms
- Handle input validation

### 3. Element Interaction
- Click elements
- Type into fields
- Check element visibility
- Read element text/attributes
- Wait for elements

### 4. Verification
- Assert element presence
- Verify text content
- Check URL patterns
- Validate page state
- Inspect DOM structure

### 5. Debugging & Evidence
- Capture full-page screenshots
- Take element screenshots
- Monitor console logs
- Record network activity
- Inspect page metrics

## Typical Workflows

### 1. Application Startup & Navigation
```
1. Start the application: pnpm start
2. Wait for server to be ready
3. Navigate to http://localhost:4200/
4. Verify landing page loads
5. Capture initial state screenshot
```

### 2. Login Flow
```
1. Navigate to /auth/login
2. Wait for login form to appear
3. Fill email field with test credentials
4. Fill password field with test credentials
5. Click login button
6. Wait for navigation to complete
7. Verify successful login (e.g., URL change, user menu visible)
8. Capture post-login screenshot
```

### 3. Workspace Navigation
```
1. From authenticated state
2. Navigate to /workspace
3. Wait for workspace content to load
4. Verify workspace UI elements
5. Check for console errors
6. Capture workspace screenshot
```

### 4. Full User Flow Test
```
1. Start app (pnpm start)
2. Navigate to home (http://localhost:4200/)
3. Navigate to login (/auth/login)
4. Perform login (demo@test.com / 123123)
5. Navigate to workspace (/workspace)
6. Verify complete flow
7. Capture evidence at each step
```

## Common Selectors for Black-Tortoise

### Login Page
- Email input: `input[type="email"]`, `#email`, `[data-testid="email-input"]`
- Password input: `input[type="password"]`, `#password`, `[data-testid="password-input"]`
- Login button: `button[type="submit"]`, `[data-testid="login-button"]`

### Navigation
- Home link: `[routerLink="/"]`, `a[href="/"]`
- Workspace link: `[routerLink="/workspace"]`, `a[href="/workspace"]`
- User menu: `[data-testid="user-menu"]`, `.user-menu`

### Common Elements
- Main content: `main`, `[role="main"]`
- Navigation bar: `nav`, `[role="navigation"]`
- Error messages: `.error-message`, `[role="alert"]`
- Loading indicators: `.loading`, `[data-testid="loading"]`

## Test Credentials

### Demo Account
- **Email**: demo@test.com
- **Password**: 123123

⚠️ **Security Note**: These are test credentials for local development only. Never use in production or commit to public repositories.

## Error Handling

### Common Issues & Solutions

1. **Element not found**
   - Solution: Add explicit wait with timeout
   - Use `waitForSelector` before interaction
   - Verify selector is correct

2. **Page load timeout**
   - Solution: Increase timeout duration
   - Check if app is running (`pnpm start`)
   - Verify network connectivity

3. **Form submission fails**
   - Solution: Verify field values are filled
   - Check form validation rules
   - Monitor console for errors

4. **Navigation not completing**
   - Solution: Wait for URL pattern match
   - Check for redirects
   - Verify route guards are satisfied

## Best Practices

1. **Always verify app is running** - Check http://localhost:4200 is accessible
2. **Use explicit waits** - Wait for specific conditions, not fixed delays
3. **Capture evidence** - Take screenshots at critical points
4. **Monitor console** - Check for errors and warnings
5. **Handle errors gracefully** - Add try-catch blocks with screenshots
6. **Clean state** - Start each test from a known state
7. **Incremental testing** - Test one flow at a time
8. **Use data-testid** - Prefer stable test identifiers

## Prompt Templates

### Basic Navigation Test
```
Use chrome-devtools-mcp to:
1. Navigate to http://localhost:4200/
2. Verify the page title contains "Black-Tortoise"
3. Take a screenshot
4. Check console for errors
```

### Login Flow Test
```
Use chrome-devtools-mcp to:
1. Navigate to http://localhost:4200/auth/login
2. Fill email field with "demo@test.com"
3. Fill password field with "123123"
4. Click login button
5. Wait for navigation to complete
6. Verify URL is /workspace or /dashboard
7. Take screenshot of logged-in state
```

### Full User Journey
```
Use chrome-devtools-mcp to test the complete user flow:
1. Start at http://localhost:4200/
2. Navigate to login page
3. Login with demo@test.com / 123123
4. Navigate to workspace
5. Verify all steps complete successfully
6. Capture screenshots at each major step
7. Report any console errors
```

## Related Skills

- `.github/skills/webapp-testing` - General web testing patterns
- `.github/skills/mcp-playwright` - Alternative Playwright MCP approach
- `.github/skills/e2e-playwright` - E2E test organization

## Related Instructions

- `64-quality-testing-copilot-instructions.md` - Testing standards
- `72-angular-accessibility-copilot-instructions.md` - Accessibility testing

## Limitations

- Requires Chrome browser installed
- Local server must be running
- Cannot test authentication flows requiring external OAuth
- May have timing issues with very slow networks
- Screenshot storage needs disk space management

## Version
- chrome-devtools-mcp: 0.15.0
- Compatible with: Black-Tortoise Angular 20+ application
- Last updated: 2026-02-01
