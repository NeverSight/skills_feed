---
name: "Web Design Builder"
description: "Create and refactor HTML5/JavaScript web designs from specifications or descriptions. Generates complete, accessible, responsive web designs with modern frameworks. Automatically verifies designs using Playwright MCP for accessibility and functionality testing. Use this skill when users ask to create web designs, mockups, landing pages, web applications, or refactor existing HTML/CSS/JS designs."
---

# Web Design Builder

This skill creates professional HTML5/JavaScript web designs from specifications, with automatic accessibility and functionality verification using Playwright MCP.

## When to Use This Skill

Activate this skill when the user requests:
- Create a web design from a specification or description
- Build a landing page, website, or web application
- Create a design mockup or prototype
- Refactor or improve existing HTML/CSS/JavaScript code
- Build responsive web interfaces
- Create component libraries or design systems
- Generate accessible web designs with WCAG compliance

## Core Workflow

### Phase 1: Requirements Gathering

When a user requests a web design, start by understanding their needs:

1. **Clarify the Design Scope**
   - What type of design? (landing page, dashboard, form, etc.)
   - Target audience and use case
   - Required features and functionality
   - Content and copy (provided or placeholder?)
   - Brand colors, fonts, or design system
   - Responsive requirements (mobile-first?)

2. **Technical Preferences**
   - Framework preference:
     - **Vanilla HTML/CSS/JS** (simple, no dependencies)
     - **Tailwind CSS** (utility-first, recommended for rapid development)
     - **React** (component-based, for complex interactions)
     - **Vue** (progressive framework)
     - **Alpine.js** (lightweight reactivity)
   - Browser support requirements
   - Accessibility requirements (WCAG level)
   - Performance constraints

3. **Check Playwright MCP Availability**

   **IMPORTANT**: Before starting the design process, check if Playwright MCP is available:

   ```javascript
   // Check if mcp__playwright tools are available
   // Look for tools like: mcp__playwright__navigate, mcp__playwright__screenshot, etc.
   ```

   **If Playwright MCP is NOT available:**
   - Inform the user: "Playwright MCP is not installed. Design verification will be skipped."
   - Provide installation instructions (see MCP Setup section below)
   - Continue with design generation but skip verification phase
   - Mark this clearly in the output

   **If Playwright MCP IS available:**
   - Inform the user: "Playwright MCP detected. Design will be automatically verified."
   - Include verification in the workflow

### Phase 2: Design Generation

#### Step 1: Create Design Mockup

Generate a complete HTML/CSS/JS mockup including:

**HTML Structure:**
- Semantic HTML5 elements
- Proper heading hierarchy (h1 → h6)
- ARIA landmarks (header, nav, main, aside, footer)
- Accessible form labels and inputs
- Alt text for images
- Unique page title

**CSS Styling:**
- Responsive design (mobile-first)
- CSS Grid or Flexbox for layouts
- Custom properties (CSS variables) for theming
- Smooth transitions and animations
- Print styles (if applicable)
- Dark mode support (optional)

**JavaScript Functionality:**
- Progressive enhancement
- Accessible interactions (keyboard support)
- Form validation
- Dynamic content loading
- Event handling
- Error handling

**Accessibility Features:**
- WCAG 2.1 Level AA compliance minimum
- Keyboard navigation support
- Focus indicators
- Screen reader friendly
- Color contrast compliance (4.5:1 minimum)
- Skip links
- ARIA attributes where needed

**Example Output Structure:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Title</title>
  <style>
    /* Modern CSS with custom properties */
    :root {
      --primary-color: #0066cc;
      --text-color: #1a1a1a;
      --bg-color: #ffffff;
      --spacing: 1rem;
    }

    /* Reset and base styles */
    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      line-height: 1.6;
      color: var(--text-color);
      background: var(--bg-color);
    }

    /* Responsive layout */
    @media (max-width: 768px) {
      /* Mobile styles */
    }
  </style>
</head>
<body>
  <!-- Accessible skip link -->
  <a href="#main-content" class="skip-link">Skip to main content</a>

  <!-- Semantic structure -->
  <header role="banner">
    <nav aria-label="Main navigation">
      <!-- Navigation -->
    </nav>
  </header>

  <main id="main-content" role="main">
    <!-- Main content -->
  </main>

  <footer role="contentinfo">
    <!-- Footer -->
  </footer>

  <script>
    // Progressive enhancement JavaScript
    (function() {
      'use strict';

      // Feature detection
      if (!('querySelector' in document)) return;

      // Your JavaScript here
    })();
  </script>
</body>
</html>
```

#### Step 2: Save Design to File

Save the generated design to a file:

```javascript
// Recommended file structure
project-name/
  index.html         // Main HTML file
  styles.css         // Separate CSS (if needed)
  script.js          // Separate JS (if needed)
  assets/
    images/          // Image assets
    fonts/           // Custom fonts
```

Use the Write tool to create the file:
- Save to user's current directory or ask for preferred location
- Use descriptive filename (e.g., `landing-page.html`, `dashboard.html`)
- Create single-file HTML for mockups (CSS/JS inline)
- Create separate files for production builds

### Phase 3: Design Verification (ONLY if Playwright MCP is available)

**IMPORTANT**: Only execute this phase if Playwright MCP was detected in Phase 1.

#### Step 1: Launch Browser and Load Design

Use Playwright MCP to open the design:

```javascript
// Navigate to the local HTML file
await mcp__playwright__navigate({
  url: 'file:///path/to/design.html'
});
```

#### Step 2: Accessibility Testing

Run comprehensive accessibility checks:

1. **Automated Accessibility Scan**
   - Check for WCAG violations
   - Verify color contrast ratios
   - Check heading hierarchy
   - Verify ARIA attributes
   - Check form labels
   - Verify alt text on images

2. **Keyboard Navigation Test**
   - Tab through all interactive elements
   - Verify focus indicators are visible
   - Check tab order is logical
   - Test Escape key behavior (modals, dropdowns)
   - Verify no keyboard traps

3. **Screen Reader Compatibility**
   - Check ARIA landmarks
   - Verify semantic HTML usage
   - Check dynamic content announcements
   - Verify form error messages

#### Step 3: Visual Testing

Capture screenshots and verify layout:

```javascript
// Take full-page screenshot
await mcp__playwright__screenshot({
  fullPage: true,
  path: 'design-screenshot.png'
});

// Test responsive breakpoints
const breakpoints = [
  { width: 375, height: 667, name: 'mobile' },
  { width: 768, height: 1024, name: 'tablet' },
  { width: 1440, height: 900, name: 'desktop' }
];

for (const bp of breakpoints) {
  await mcp__playwright__setViewportSize({
    width: bp.width,
    height: bp.height
  });

  await mcp__playwright__screenshot({
    path: `design-${bp.name}.png`
  });
}
```

#### Step 4: Functionality Testing

Test interactive elements:

1. **Form Validation**
   - Test required fields
   - Test input validation
   - Test error messages
   - Test success states

2. **Interactive Components**
   - Test buttons and links
   - Test modals and dialogs
   - Test dropdowns and menus
   - Test tabs and accordions
   - Test carousels and sliders

3. **JavaScript Functionality**
   - Verify event handlers work
   - Test dynamic content loading
   - Check console for errors
   - Verify progressive enhancement

#### Step 5: Performance Check

Evaluate performance metrics:

1. **Load Time**
   - Measure page load time
   - Check resource loading
   - Identify bottlenecks

2. **Resource Optimization**
   - Check CSS file size
   - Check JavaScript file size
   - Verify image optimization
   - Check for unused CSS/JS

### Phase 4: Verification Report

Generate a comprehensive report:

```markdown
# Design Verification Report

## Overview
- **Design Type**: [Landing Page / Dashboard / etc.]
- **Framework**: [Vanilla / Tailwind / React / etc.]
- **Verification Date**: [Date]
- **Playwright MCP**: [Available / Not Available]

## Accessibility Compliance

### WCAG 2.1 Level AA
✅ **PASSED**: Color contrast (4.5:1 minimum)
✅ **PASSED**: Keyboard navigation
✅ **PASSED**: Semantic HTML structure
⚠️  **WARNING**: Missing alt text on 2 images
❌ **FAILED**: Form missing associated labels

### Issues Found
1. **HIGH**: Form input #email missing label
   - Location: Line 45
   - Fix: Add `<label for="email">Email</label>`

2. **MEDIUM**: Image missing alt text
   - Location: Line 78
   - Fix: Add `alt="Description of image"`

## Visual Testing

### Responsive Breakpoints
✅ **Mobile (375px)**: Layout renders correctly
✅ **Tablet (768px)**: Layout renders correctly
✅ **Desktop (1440px)**: Layout renders correctly

### Screenshots
- [x] Full page screenshot saved
- [x] Mobile screenshot saved
- [x] Tablet screenshot saved
- [x] Desktop screenshot saved

## Functionality Testing

### Interactive Elements
✅ Navigation menu works
✅ Form submission works
✅ Modal opens and closes
⚠️  Focus not returned to trigger after modal close

### JavaScript
✅ No console errors
✅ Event handlers working
✅ Progressive enhancement implemented

## Performance

### Metrics
- **Page Load Time**: 1.2s
- **Total File Size**: 45KB
- **CSS Size**: 12KB
- **JavaScript Size**: 8KB

### Optimization Opportunities
- Consider minifying CSS (potential 30% reduction)
- Lazy load images below the fold
- Consider code splitting for JavaScript

## Recommendations

### High Priority
1. Fix form label associations
2. Add missing alt text to images
3. Implement focus management for modal

### Medium Priority
1. Minify CSS and JavaScript for production
2. Add loading states for dynamic content
3. Implement error boundaries for JavaScript

### Low Priority
1. Add dark mode support
2. Enhance animations with reduced motion support
3. Add print styles

## Next Steps

1. Review and fix high-priority issues
2. Re-run verification after fixes
3. Test with actual screen readers
4. Conduct user testing
5. Deploy to staging environment
```

### Phase 5: Iteration and Refinement

Based on verification results:

1. **Fix Critical Issues**
   - Address all accessibility violations
   - Fix broken functionality
   - Resolve layout issues

2. **Apply Improvements**
   - Implement recommended optimizations
   - Enhance visual design based on feedback
   - Refine interactions and animations

3. **Re-verify**
   - Run verification again after fixes
   - Ensure all issues are resolved
   - Generate updated report

4. **Deliver Final Design**
   - Provide clean, production-ready code
   - Include documentation
   - Provide deployment instructions
   - Share verification report

## Design Patterns & Best Practices

### Responsive Design

**Mobile-First Approach:**
```css
/* Base styles for mobile */
.container {
  padding: 1rem;
}

/* Tablet and up */
@media (min-width: 768px) {
  .container {
    padding: 2rem;
    max-width: 960px;
    margin: 0 auto;
  }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .container {
    padding: 3rem;
    max-width: 1200px;
  }
}
```

### Accessible Forms

```html
<form class="contact-form">
  <div class="form-field">
    <label for="name">
      Name <span aria-label="required">*</span>
    </label>
    <input
      type="text"
      id="name"
      name="name"
      required
      aria-required="true"
      aria-describedby="name-error"
    />
    <span id="name-error" class="error" role="alert" hidden>
      Please enter your name
    </span>
  </div>
</form>
```

### Interactive Components

**Accessible Modal:**
```javascript
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  const lastFocused = document.activeElement;

  modal.hidden = false;
  modal.setAttribute('aria-modal', 'true');

  // Focus first focusable element
  const firstFocusable = modal.querySelector('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
  firstFocusable?.focus();

  // Store last focused for return
  modal.dataset.lastFocused = lastFocused;

  // Trap focus
  trapFocus(modal);
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  modal.hidden = true;

  // Return focus
  const lastFocused = document.querySelector(`[data-last-focused="${modal.id}"]`);
  lastFocused?.focus();
}
```

## Framework-Specific Guidelines

### Tailwind CSS

**Pros:**
- Rapid development
- Consistent design system
- Built-in responsive utilities
- Excellent for prototyping

**Setup:**
```html
<script src="https://cdn.tailwindcss.com"></script>
<script>
  tailwind.config = {
    theme: {
      extend: {
        colors: {
          primary: '#0066cc',
        }
      }
    }
  }
</script>
```

**Example:**
```html
<div class="container mx-auto px-4">
  <h1 class="text-4xl font-bold text-gray-900 mb-4">
    Welcome
  </h1>
  <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
    Click Me
  </button>
</div>
```

### React

**Pros:**
- Component reusability
- Virtual DOM performance
- Large ecosystem
- Great for SPAs

**Example:**
```jsx
function DesignComponent() {
  const [isOpen, setIsOpen] = React.useState(false);

  return (
    <div className="container">
      <button
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
      >
        Toggle
      </button>
      {isOpen && (
        <div className="content">
          Content here
        </div>
      )}
    </div>
  );
}
```

### Alpine.js

**Pros:**
- Lightweight (15KB)
- Declarative syntax
- No build step needed
- Good for progressive enhancement

**Example:**
```html
<div x-data="{ open: false }">
  <button @click="open = !open" :aria-expanded="open">
    Toggle
  </button>
  <div x-show="open" x-transition>
    Content here
  </div>
</div>
```

## MCP Setup Instructions

If Playwright MCP is not available, provide these instructions to the user:

### Installing Playwright MCP

**Option 1: Via NPM (Recommended)**
```bash
# Install Playwright MCP server
npm install -g @playwright/mcp-server

# Configure in Claude Code
claude code mcp add playwright
```

**Option 2: Manual Setup**

1. Create MCP configuration file:
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp-server"],
      "env": {}
    }
  }
}
```

2. Restart Claude Code

**Verification:**
After installation, verify Playwright MCP is working:
```bash
# Check MCP servers
claude code mcp list
```

You should see `playwright` in the list of available MCP servers.

## Communication Style

When working with users:

1. **Clarify Requirements First**
   - Ask about design goals and constraints
   - Understand technical requirements
   - Confirm framework preferences

2. **Provide Context**
   - Explain design decisions
   - Justify framework choices
   - Describe accessibility considerations

3. **Show Progress**
   - Inform when generating design
   - Update during verification (if MCP available)
   - Share findings incrementally

4. **Be Actionable**
   - Provide specific fixes for issues
   - Include code examples
   - Offer alternatives when appropriate

5. **Handle MCP Unavailability Gracefully**
   - Clearly state when verification is skipped
   - Provide manual testing guidance
   - Offer installation instructions

## Deliverables

At the end of the design process, provide:

1. **Complete Design Files**
   - HTML, CSS, JavaScript files
   - Assets (if any)
   - README with setup instructions

2. **Verification Report** (if MCP available)
   - Accessibility compliance results
   - Visual testing screenshots
   - Functionality test results
   - Performance metrics
   - Prioritized recommendations

3. **Documentation**
   - Component usage guide
   - Customization instructions
   - Browser support information
   - Deployment guidelines

4. **Next Steps**
   - Suggested improvements
   - Testing recommendations
   - Production checklist

## Example Workflow

**User Request:**
> "Create a landing page for a SaaS product with a hero section, features, pricing, and contact form."

**Your Response:**

1. **Clarify Requirements:**
   - "I'll create a modern SaaS landing page. A few questions:
     - Do you have brand colors or should I use a professional default palette?
     - Framework preference? I recommend Tailwind CSS for rapid development.
     - Any specific features to highlight?
     - Contact form fields needed?"

2. **Check Playwright MCP:**
   - "Checking for Playwright MCP... Not detected. Design verification will be skipped. Would you like installation instructions?"

3. **Generate Design:**
   - Create complete HTML/CSS/JS file
   - Include hero, features, pricing, contact form
   - Make it responsive and accessible
   - Save to `saas-landing-page.html`

4. **Manual Verification Guide** (since MCP not available):
   - Provide checklist for manual testing
   - Share accessibility testing tools
   - Suggest browser testing approach

5. **Deliver:**
   - Share complete design file
   - Provide customization guide
   - Offer iteration if needed

Remember: The goal is to create beautiful, accessible, functional web designs that work for all users, with automatic verification when possible!
