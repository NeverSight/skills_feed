---
name: browser-testing
description: Automated browser testing, interaction automation, and form testing. Use when the user needs to test web pages, automate browser interactions, fill forms, test validation, run multi-step wizards, or test login/signup flows.
allowed-tools: Bash(browser-devtools-cli:*)
---

# Browser Testing Skill

Automated browser testing, interaction automation, and form testing using Browser DevTools CLI.

## When to Use

This skill activates when:
- User asks to test a web page or application
- User wants to automate browser interactions
- User needs to verify UI behavior
- User wants to automate form submission
- User needs to test form validation
- User mentions multi-step forms or wizards
- User wants to test login/signup flows

## Capabilities

### Navigation
```bash
browser-devtools-cli navigation go-to --url "https://example.com"
browser-devtools-cli navigation go-back
browser-devtools-cli navigation go-forward
browser-devtools-cli navigation reload
```

### Interaction
```bash
browser-devtools-cli interaction click --selector "#button"
browser-devtools-cli interaction fill --selector "#input" --value "text"
browser-devtools-cli interaction select --selector "#dropdown" --value "option"
browser-devtools-cli interaction hover --selector "#element"
browser-devtools-cli interaction press-key --key "Enter"
browser-devtools-cli interaction scroll --mode bottom
browser-devtools-cli interaction drag --source-selector "#drag" --target-selector "#drop"
```

### Content Capture
```bash
browser-devtools-cli content take-screenshot --name "screenshot"
browser-devtools-cli content get-as-html
browser-devtools-cli content get-as-text
browser-devtools-cli content save-as-pdf --name "page"
```

### Synchronization
```bash
browser-devtools-cli sync wait-for-network-idle
```

### Mocking & Stubbing
```bash
browser-devtools-cli stub mock-http-response --pattern "**/api/**" --response '{"status":200}'
browser-devtools-cli stub intercept-http-request --pattern "**/api/**" --modifications '{"headers":{}}'
browser-devtools-cli stub list
browser-devtools-cli stub clear --all
```

### Code Execution
```bash
browser-devtools-cli run js-in-browser --script "document.title"
browser-devtools-cli run js-in-sandbox --code "return await page.title()"
```

## Basic Testing Workflow

1. **Navigate**: Go to the page under test
2. **Wait**: Ensure page is fully loaded
3. **Interact**: Click, fill, scroll as needed
4. **Verify**: Check page state, take screenshots
5. **Document**: Report results

## Form Automation Patterns

### Basic Form Fill

```bash
# Fill text input
browser-devtools-cli interaction fill \
  --selector "#email" \
  --value "test@example.com"

# Fill password
browser-devtools-cli interaction fill \
  --selector "#password" \
  --value "SecurePass123"

# Click submit
browser-devtools-cli interaction click \
  --selector "button[type=submit]"
```

### Select Dropdown

```bash
browser-devtools-cli interaction select \
  --selector "#country" \
  --value "US"
```

### Checkbox/Radio

```bash
# Check checkbox
browser-devtools-cli interaction click \
  --selector "#terms-checkbox"

# Select radio option
browser-devtools-cli interaction click \
  --selector "input[name=plan][value=premium]"
```

### Multi-Step Wizard

```bash
SESSION="--session-id wizard-test"

# Step 1: Personal Info
browser-devtools-cli $SESSION interaction fill --selector "#name" --value "John Doe"
browser-devtools-cli $SESSION interaction fill --selector "#email" --value "john@example.com"
browser-devtools-cli $SESSION interaction click --selector "#next-step"

# Wait for step 2
browser-devtools-cli $SESSION sync wait-for-network-idle

# Step 2: Address
browser-devtools-cli $SESSION interaction fill --selector "#address" --value "123 Main St"
browser-devtools-cli $SESSION interaction select --selector "#state" --value "CA"
browser-devtools-cli $SESSION interaction click --selector "#next-step"

# Step 3: Confirm
browser-devtools-cli $SESSION sync wait-for-network-idle
browser-devtools-cli $SESSION interaction click --selector "#submit"
```

## Validation Testing

### Test Required Fields

```bash
# Submit empty form
browser-devtools-cli interaction click --selector "button[type=submit]"

# Check for error messages
browser-devtools-cli content get-as-text --selector ".error-message"
```

### Test Invalid Input

```bash
# Invalid email
browser-devtools-cli interaction fill --selector "#email" --value "not-an-email"
browser-devtools-cli interaction click --selector "button[type=submit]"

# Check validation error
browser-devtools-cli content get-as-html --selector ".email-error"
```

## Session-Based Testing

```bash
SESSION="--session-id my-test"

# Navigate
browser-devtools-cli $SESSION navigation go-to --url "https://example.com"

# Interact
browser-devtools-cli $SESSION interaction click --selector ".login-btn"
browser-devtools-cli $SESSION interaction fill --selector "#email" --value "test@example.com"

# Verify
browser-devtools-cli $SESSION content take-screenshot --name "after-login"

# Cleanup
browser-devtools-cli session delete my-test
```

## Best Practices

1. **Use sessions** for multi-step flows
2. **Wait for network idle** after navigation and actions
3. **Take screenshots** after important actions for verification
4. **Use specific selectors** to avoid wrong elements
5. **Test empty submission** first for validation testing
6. **Clear fields** before filling (use `interaction fill` which clears first)
7. **Handle dynamic fields** with wait strategies
8. **Screenshot after errors** for documentation
