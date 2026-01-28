---
name: browser-automation
description: Guide for browser automation and testing using the browser_subagent tool. Use this skill when users need to interact with web pages, test user flows, scrape dynamic content, automate form submissions, capture screenshots, verify UI changes, or record browser sessions. Supports clicking, typing, navigation, scrolling, waiting for elements, and all standard browser interactions with automatic video recording.
license: Complete terms in LICENSE.txt
---

# Browser Automation

This skill provides comprehensive guidance for browser automation using the `browser_subagent` tool.

## Overview

The `browser_subagent` enables autonomous browser control with automatic session recording. All interactions are captured as WebP videos saved to the artifacts directory.

## Core Capabilities

1. **Navigation** - Open URLs, navigate pages, handle redirects
2. **Interaction** - Click, type, scroll, hover, drag-and-drop
3. **Extraction** - Read DOM content, capture screenshots, scrape data
4. **Verification** - Test user flows, validate UI changes
5. **Recording** - Automatic video capture of all sessions

## When to Use

Use `browser_subagent` (vs `read_url_content`) when:

- JavaScript execution is required
- User interaction is needed (forms, clicks, navigation)
- Authentication or session state is required
- Dynamic content loads after page render
- Visual verification or screenshots are needed
- Recording demonstrations or tutorials

Use `read_url_content` for static HTML content where JavaScript isn't needed.

## Tool Parameters

### TaskName (required)
Human-readable title for the browser task.
- Should be properly capitalized
- Example: "Testing Login Flow", "Scraping Product Data"
- Avoid URLs or technical jargon

### Task (required)
Detailed instructions for the browser subagent. Be explicit about:
- What to do
- When to stop
- What information to return

**Critical**: The subagent is autonomous and one-shot. Provide comprehensive instructions upfront.

### RecordingName (required)
Filename for the video recording.
- All lowercase with underscores
- Maximum 3 words
- Describes what the recording contains
- Example: `login_flow_demo`, `checkout_process`

## Best Practices

### 1. Clear Task Instructions

**Bad**: "Check the website"
```
Task: Go to example.com and check it
```

**Good**: Specific, with clear completion criteria
```
Task: Navigate to https://example.com, wait for the page to fully load, 
verify that the main heading contains "Welcome", capture a screenshot of 
the page, then return the page title and the text content of the main 
heading.
```

### 2. Return Conditions

Always specify what the subagent should return:

```
Task: Navigate to the product page at https://shop.example.com/products/123
and extract the following data:
- Product title
- Price
- Availability status
- Number of reviews

Return this information in a structured format when complete.
```

### 3. Error Handling

Instruct the subagent how to handle failures:

```
Task: Attempt to log in to https://app.example.com with username "testuser" 
and password "testpass123". If login succeeds, navigate to the dashboard 
and return the user's display name. If login fails, capture a screenshot 
of the error message and return the error text.
```

### 4. Wait Conditions

Specify wait conditions for dynamic content:

```
Task: Navigate to https://example.com/search, type "widgets" into the 
search box, click the search button, and wait until the results list 
appears (look for element with class "search-results"). Once results load, 
count the number of result items and return that count.
```

### 5. Multi-Step Flows

Break down complex flows into clear steps:

```
Task: Complete the following checkout flow:
1. Navigate to https://shop.example.com
2. Click "Add to Cart" on the first product
3. Click the cart icon in the top right
4. Click "Proceed to Checkout"
5. Fill in the shipping form with test data
6. Capture a screenshot of the order summary
7. Return the total price shown on the order summary
```

## Common Patterns

### Authentication Testing

```
TaskName: "Testing User Login"
Task: Navigate to https://app.example.com/login, enter "user@example.com" 
in the email field, enter "password123" in the password field, click the 
"Sign In" button, wait for navigation to complete. If login succeeds and 
you see a dashboard, return "Login successful". If there's an error message, 
return the error text.
RecordingName: login_test
```

### Data Scraping

```
TaskName: "Scraping Product Listings"
Task: Navigate to https://shop.example.com/products, wait for all product 
cards to load, then extract the title and price from each product card. 
Return a list of products with their titles and prices. If pagination 
exists, only scrape the first page.
RecordingName: product_scrape
```

### Form Submission

```
TaskName: "Submitting Contact Form"
Task: Navigate to https://example.com/contact, fill in the form with:
- Name: "Test User"
- Email: "test@example.com"
- Message: "This is a test message"
Then click the submit button and wait for the confirmation message. 
Return the confirmation message text.
RecordingName: contact_form
```

### Screenshot Capture

```
TaskName: "Capturing Homepage Design"
Task: Navigate to https://example.com, wait for complete page load including 
all images, scroll to show the full page layout, capture a full-page 
screenshot, and return confirmation that the screenshot was saved.
RecordingName: homepage_capture
```

### UI Verification

```
TaskName: "Verifying Responsive Layout"
Task: Navigate to https://example.com, resize the browser window to mobile 
width (375px), capture a screenshot, then resize to desktop width (1920px), 
capture another screenshot. Return the dimensions used and confirm both 
screenshots were captured.
RecordingName: responsive_check
```

## Element Selectors

The browser subagent can find elements using:
- CSS selectors
- Text content
- ARIA labels
- Position/proximity
- Visual descriptions

Be specific when describing elements:

**Good**:
- "Click the blue 'Submit' button at the bottom of the form"
- "Type into the input field labeled 'Email Address'"
- "Click the first product card in the grid"

**Avoid**:
- "Click the button" (which button?)
- "Fill in the field" (which field?)

## Waiting Strategies

### Wait for Navigation
```
After clicking "Submit", wait for the page to navigate to the success page.
```

### Wait for Elements
```
Wait until the spinner disappears and the results table is visible.
```

### Wait for Content
```
Wait until the product count shows a number greater than 0.
```

### Fixed Delays (use sparingly)
```
Wait 3 seconds for animations to complete.
```

## Recording Best Practices

### Naming Convention
- Use lowercase with underscores
- Be descriptive but concise
- Maximum 3 words
- Examples:
  - `login_flow`
  - `checkout_test`
  - `nav_demo`
  - `form_submit`

### Recording Purpose
Recordings are automatically saved and useful for:
- Debugging failed automation
- Demonstrating user flows
- Documenting test results
- Creating tutorials
- Reviewing UI behavior

## Advanced Techniques

### Session State
The browser maintains state during a single subagent execution:
- Cookies persist across navigation
- Login sessions remain active
- Form data can carry forward

### Multiple Tabs
If needed, the subagent can work with multiple tabs:
```
Task: Open https://example.com in the current tab, then open a new tab 
and navigate to https://example.com/compare. Switch between tabs to 
compare data from both pages.
```

### File Downloads
```
Task: Navigate to https://example.com/downloads, click the "Download Report" 
button, wait for the download to complete, and return confirmation.
```

### Iframes
```
Task: Navigate to https://example.com, locate the embedded iframe 
containing the video player, switch context to that iframe, then click 
the play button.
```

## Error Recovery

If the browser tool encounters issues:
1. The subagent will report what went wrong
2. Read the error message carefully
3. Adjust your Task instructions
4. Try again with more specific instructions or wait conditions

Common issues:
- Element not found: Be more specific about element description
- Timeout: Add explicit wait conditions or increase wait time
- Navigation failed: Check URL validity, network issues

## Performance Tips

1. **Be Specific**: Clear selectors are faster than vague descriptions
2. **Minimize Waits**: Only wait when necessary; don't add arbitrary delays
3. **Single Purpose**: One task per browser_subagent call
4. **Return Fast**: Return as soon as the required information is collected

## Examples

See `examples/` directory for complete working examples:
- `examples/login_test.md` - Authentication flow
- `examples/form_automation.md` - Form submission
- `examples/data_extraction.md` - Web scraping
- `examples/ui_testing.md` - Visual verification

## Limitations

- Each subagent call is independent (no session sharing between calls)
- Cannot execute arbitrary JavaScript (but can interact with page elements)
- Video recordings use system resources (keep sessions focused)
- Some sites may block automation (CAPTCHA, bot detection)

## Integration with Workflows

Browser automation pairs well with:
- **Testing workflows**: Automate E2E tests
- **Data collection**: Scrape and process information
- **Documentation**: Record user flows automatically
- **Verification**: Validate deployments

## When NOT to Use

Avoid browser automation when:
- Static HTML scraping is sufficient → use `read_url_content`
- API endpoints are available → use direct API calls
- File processing is needed → use file manipulation tools
- The task requires human judgment (CAPTCHA, visual verification)
