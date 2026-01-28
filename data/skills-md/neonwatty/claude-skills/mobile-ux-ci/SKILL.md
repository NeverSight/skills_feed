---
name: mobile-ux-ci
description: Generates Playwright tests that detect iOS/mobile UX anti-patterns in CI. Use this when the user wants to add automated UX pattern checks for web apps targeting mobile/iOS. Creates tests that FAIL when hamburger menus, FABs, small touch targets, or other anti-patterns are detected.
---

# Mobile UX CI Skill

You are a senior QA engineer specializing in mobile UX quality. Your job is to create automated Playwright tests that detect iOS/mobile UX anti-patterns and fail CI when they're found.

**The Problem This Solves:**
Most E2E tests verify that features *work*, not that they *should exist*. A hamburger menu test might verify "does the menu open?" but never asks "should there be a hamburger menu at all?" This skill creates tests that enforce UX standards.

## Task List Integration

**CRITICAL:** This skill uses Claude Code's task list system for progress tracking and session recovery. You MUST use TaskCreate, TaskUpdate, and TaskList tools throughout execution.

### Why Task Lists Matter Here
- **Anti-pattern tracking:** User sees "3 critical, 5 warning, 2 info anti-patterns detected"
- **Session recovery:** If interrupted during app exploration, resume that phase
- **Severity decisions:** Track which anti-patterns user chose to enforce vs allow
- **CI integration status:** Track Playwright setup and workflow creation

### Task Hierarchy
```
[Main Task] "Generate Mobile UX CI Tests"
  └── [Infra Task] "Assess: testing infrastructure"
  └── [App Task] "Explore: app structure and routes"
  └── [Generate Task] "Generate: UX pattern tests"
      └── [Pattern Task] "Pattern: hamburger menu (critical)"
      └── [Pattern Task] "Pattern: small touch targets (critical)"
      └── [Pattern Task] "Pattern: FAB detected (critical)"
  └── [CI Task] "CI: workflow integration"
```

### Session Recovery Check
**At the start of this skill, always check for existing tasks:**
```
1. Call TaskList to check for existing UX CI tasks
2. If a "Generate Mobile UX CI Tests" task exists with status in_progress:
   - Check its metadata for current phase
   - Resume from that phase
3. If pattern tasks exist with severity decisions:
   - Use those decisions for test generation
4. If no tasks exist, proceed with fresh execution
```

## When to Use This Skill

Use this skill when:
- User wants to add mobile UX checks to CI
- User says "add UX pattern tests", "detect anti-patterns", "iOS UX CI checks"
- User wants to prevent mobile UX regressions
- User is building a PWA or web app targeting iOS/mobile

## Process

### Phase 1: Assess Current Testing Infrastructure [DELEGATE TO AGENT]

**Create the main task:**
```
TaskCreate:
- subject: "Generate Mobile UX CI Tests"
- description: |
    Create Playwright tests to detect iOS/mobile UX anti-patterns.
    Tests will FAIL CI when anti-patterns are found.
- activeForm: "Assessing testing infrastructure"

TaskUpdate:
- taskId: [main task ID]
- status: "in_progress"
```

**Create infrastructure assessment task:**
```
TaskCreate:
- subject: "Assess: testing infrastructure"
- description: |
    Exploring codebase for Playwright setup and existing tests.
    Delegating to Explore agent.
- activeForm: "Assessing infrastructure"

TaskUpdate:
- taskId: [infra task ID]
- status: "in_progress"
```

**Purpose:** Explore the codebase to understand the current testing setup. Delegate this to an Explore agent to save context.

**Use the Task tool to spawn an Explore agent:**

```
Task tool parameters:
- subagent_type: "Explore"
- model: "sonnet"
- prompt: |
    You are assessing a project's testing infrastructure for mobile UX CI tests.

    ## What to Find

    1. **Playwright Configuration**
       - Search for `playwright.config.ts` or `playwright.config.js`
       - Check `package.json` for `@playwright/test` dependency
       - Note the Playwright version if installed

    2. **Existing E2E Tests**
       - Look in `e2e/`, `tests/`, `__tests__/`, or similar directories
       - Count existing test files
       - Note any mobile-specific test files

    3. **Mobile Testing Setup**
       - Check Playwright config for mobile viewport projects
       - Search for existing mobile test files (`*mobile*`, `*ios*`)
       - Look for device emulation settings

    4. **Test Utilities**
       - Find test helper files (`test-utils.ts`, `helpers.ts`)
       - Note any existing page object patterns
       - Find authentication/setup utilities

    ## Return Format

    ```
    ## Testing Infrastructure Report

    ### Playwright Status
    - Installed: [Yes/No]
    - Version: [version or N/A]
    - Config file: [path or N/A]

    ### Existing Tests
    - Test directory: [path]
    - Test file count: [count]
    - Mobile-specific tests: [count or None]

    ### Mobile Configuration
    - Mobile viewports configured: [Yes/No]
    - Device presets: [list or None]

    ### Test Utilities
    - Helper files: [list or None]
    - Page objects: [Yes/No]
    - Auth utilities: [Yes/No]

    ### Recommendation
    - [Add to existing / Create new / Needs Playwright setup]
    ```
```

**After agent returns:** Update task with findings:
```
TaskUpdate:
- taskId: [infra task ID]
- status: "completed"
- metadata: {
    "playwrightInstalled": true/false,
    "playwrightVersion": "[version or N/A]",
    "configFile": "[path or N/A]",
    "testDirectory": "[path]",
    "existingTestCount": [count],
    "mobileTestsExist": true/false,
    "recommendation": "add_to_existing|create_new|needs_setup"
  }
```

Based on the infrastructure report, ask the user their goal:
- **Add to existing**: Add UX pattern tests to existing Playwright setup
- **Create new**: Set up Playwright and add UX pattern tests
- **Audit only**: Generate a report of current anti-patterns without creating tests

**Store user's choice in main task metadata:**
```
TaskUpdate:
- taskId: [main task ID]
- metadata: {"userGoal": "add_to_existing|create_new|audit_only"}
```

### Phase 2: Understand the App [DELEGATE TO AGENT]

**Create app exploration task:**
```
TaskCreate:
- subject: "Explore: app structure and routes"
- description: |
    Exploring app to identify pages needing UX pattern testing.
    Delegating to Explore agent.
- activeForm: "Exploring app structure"

TaskUpdate:
- taskId: [app task ID]
- status: "in_progress"
```

**Purpose:** Explore the app's structure to identify what pages/routes need UX pattern testing. Delegate this to an Explore agent to save context.

**Use the Task tool to spawn an Explore agent:**

```
Task tool parameters:
- subagent_type: "Explore"
- model: "sonnet"
- prompt: |
    You are exploring a web application to identify pages that need mobile UX testing.

    ## What to Find

    1. **Routes and Pages**
       - Find all routes (React Router, Next.js pages, Vue Router, etc.)
       - List all user-facing pages
       - Note the base URL (likely localhost:5173 or similar)

    2. **Entry Points**
       - How does a user enter the app? (login, onboarding, direct access)
       - Is authentication required?
       - What's the first page users see?

    3. **Key Screens to Test**
       - Navigation screens (where nav patterns matter most)
       - Form screens (where touch targets matter)
       - List/table screens (where scrolling matters)
       - Modal/dialog screens (where presentation matters)

    4. **Existing Test Patterns**
       - Look for test utilities already mentioned in Phase 1
       - Find any app-specific selectors (data-testid patterns)
       - Note authentication helpers if they exist

    ## Return Format

    ```
    ## App Structure Report

    ### Base URL
    - Development: [URL]

    ### Entry Flow
    - Auth required: [Yes/No]
    - Entry point: [page/route]
    - First user screen: [page name]

    ### Pages to Test (prioritized)
    | Page | Route | Why Test |
    |------|-------|----------|
    | Home | / | Primary navigation visible |
    | Dashboard | /dashboard | Contains lists, buttons |
    | Settings | /settings | Form inputs, toggles |

    ### Navigation Pattern
    - Primary nav type: [tab bar / sidebar / hamburger / etc.]
    - Location: [top / bottom / left]

    ### Selector Patterns
    - data-testid usage: [Yes/No]
    - Common patterns: [list]
    ```
```

**After agent returns:** Update task with findings:
```
TaskUpdate:
- taskId: [app task ID]
- status: "completed"
- metadata: {
    "baseUrl": "[URL]",
    "authRequired": true/false,
    "entryPoint": "[route]",
    "pagesToTest": ["Home", "Dashboard", "Settings", ...],
    "primaryNavType": "tab_bar|sidebar|hamburger|other",
    "dataTestidUsage": true/false
  }
```

Use the app structure report to determine which pages to include in the UX pattern tests and how to set up test navigation.

### Phase 3: Generate UX Pattern Tests

**Create generate task:**
```
TaskCreate:
- subject: "Generate: UX pattern tests"
- description: |
    Generating Playwright tests for mobile UX anti-patterns.
    Will create tests for navigation, touch targets, components, and layout.
- activeForm: "Generating UX pattern tests"

TaskUpdate:
- taskId: [generate task ID]
- status: "in_progress"
```

**Create a task for each anti-pattern category detected:**
```
TaskCreate:
- subject: "Pattern: [pattern name] ([severity])"
- description: |
    Anti-pattern: [description]
    Severity: critical|warning|info
    Test: [what the test checks]
    User decision: [enforce|allow|pending]
- activeForm: "Checking [pattern name]"
```

Example pattern tasks:
```
TaskCreate:
- subject: "Pattern: hamburger menu (critical)"
- description: |
    Anti-pattern: Hamburger menu for primary navigation
    Severity: critical (should fail CI)
    iOS apps use tab bars, not hamburger menus.
    Test: Detect .hamburger-btn, [class*="hamburger"]
- activeForm: "Checking hamburger menu"
```

Create a `mobile-ux-patterns.spec.ts` file with tests for:

#### Navigation Anti-Patterns
| Anti-Pattern | Why It's Wrong | What to Test |
|--------------|---------------|--------------|
| Hamburger menu | iOS uses tab bars | `.hamburger-btn`, `[class*="hamburger"]` |
| Floating Action Button (FAB) | Material Design, not iOS | `.fab`, `[class*="floating-action"]` |
| Breadcrumb navigation | iOS uses back button | `.breadcrumb`, `[class*="breadcrumb"]` |
| Nested drawer menus | iOS prefers flat navigation | `.drawer`, `[class*="drawer"]` |

#### Touch Target Issues
| Issue | Standard | What to Test |
|-------|----------|--------------|
| Small buttons | iOS: 44x44pt, WCAG: 24x24px | `boundingBox()` on all `button, a, [role="button"]` |
| Targets too close | 8px minimum spacing | Measure distance between interactive elements |

#### Component Anti-Patterns
| Anti-Pattern | iOS Alternative | What to Test |
|--------------|-----------------|--------------|
| Native `<select>` | iOS picker wheels | `select:visible` count |
| Checkboxes | Toggle switches | `input[type="checkbox"]` count |
| Material snackbars | iOS alerts/banners | `.snackbar`, `[class*="snackbar"]` |
| Heavy shadows | Subtle iOS shadows | `[class*="elevation"]`, `.shadow-xl` |

#### Layout Issues
| Issue | What to Test |
|-------|--------------|
| Horizontal overflow | `body.scrollWidth > html.clientWidth` |
| Missing viewport meta | `meta[name="viewport"]` existence |
| No safe area insets | CSS `env(safe-area-inset-*)` usage |

#### Text & Selection
| Issue | What to Test |
|-------|--------------|
| UI text selectable | `user-select` CSS property |
| Font too small | Font sizes below 14px |

#### Interaction Issues
| Issue | What to Test |
|-------|--------------|
| Hover-dependent UI | Elements with opacity:0 and hover classes |
| Double-tap zoom | `touch-action: manipulation` |
| Canvas gesture conflicts | `touch-action: none` on canvas |

### Phase 4: Test File Template

**Update generate task with pattern counts:**
```
TaskUpdate:
- taskId: [generate task ID]
- metadata: {
    "criticalPatterns": [count],
    "warningPatterns": [count],
    "infoPatterns": [count],
    "totalTests": [count]
  }
```

Generate a test file following this structure:

```typescript
/**
 * Mobile UX Anti-Pattern Tests
 *
 * These tests FAIL when iOS/mobile UX anti-patterns are detected.
 * Reference: Apple HIG, Material Design vs iOS differences
 */

import { test, expect, Page } from '@playwright/test';

// Viewport sizes
const IPHONE_14 = { width: 393, height: 852 };

// Apple's minimum touch target
const IOS_MIN_TOUCH_TARGET = 44;

// Helper to enter the app (customize per project)
async function enterApp(page: Page) {
  await page.goto('/');
  // Add app-specific setup here
}

test.describe('Navigation Anti-Patterns', () => {
  test('ANTI-PATTERN: Hamburger menu should not exist', async ({ page }) => {
    await page.setViewportSize(IPHONE_14);
    await enterApp(page);

    const hamburger = page.locator('.hamburger-btn, [class*="hamburger"]').first();
    const isVisible = await hamburger.isVisible().catch(() => false);

    expect(isVisible, 'iOS anti-pattern: Hamburger menu detected').toBe(false);
  });

  // ... more navigation tests
});

test.describe('Touch Target Sizes', () => {
  test('All interactive elements meet iOS 44pt minimum', async ({ page }) => {
    await page.setViewportSize(IPHONE_14);
    await enterApp(page);

    const buttons = await page.locator('button:visible').all();
    const violations: string[] = [];

    for (const btn of buttons) {
      const box = await btn.boundingBox();
      if (box && (box.width < IOS_MIN_TOUCH_TARGET || box.height < IOS_MIN_TOUCH_TARGET)) {
        violations.push(`Button ${box.width}x${box.height}px`);
      }
    }

    expect(violations.length, `${violations.length} touch targets too small`).toBe(0);
  });
});

// ... more test categories
```

### Phase 5: CI Integration

**Mark generate task completed:**
```
TaskUpdate:
- taskId: [generate task ID]
- status: "completed"
- metadata: {
    "testFile": "e2e/mobile-ux-patterns.spec.ts",
    "testsGenerated": [count]
  }
```

**Create CI integration task:**
```
TaskCreate:
- subject: "CI: workflow integration"
- description: |
    Setting up CI workflow to run mobile UX pattern tests.
    Adding to existing workflow or creating new one.
- activeForm: "Setting up CI workflow"

TaskUpdate:
- taskId: [ci task ID]
- status: "in_progress"
```

Ensure tests run in CI by:

1. Adding to existing Playwright CI workflow
2. Or creating new workflow:

```yaml
name: Mobile UX Checks

on: [push, pull_request]

jobs:
  mobile-ux:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npx playwright install chromium
      - run: npm run dev &
      - run: npx playwright test mobile-ux-patterns.spec.ts
```

### Phase 6: Review with User

**Mark CI task completed:**
```
TaskUpdate:
- taskId: [ci task ID]
- status: "completed"
- metadata: {
    "workflowFile": "[path or 'added_to_existing']",
    "ciConfigured": true
  }
```

**Mark all pattern tasks with user decisions:**
For each pattern task, update with user's severity decision:
```
TaskUpdate:
- taskId: [pattern task ID]
- status: "completed"
- metadata: {"userDecision": "enforce|allow|warning_only"}
```

**Mark main task completed:**
```
TaskUpdate:
- taskId: [main task ID]
- status: "completed"
- metadata: {
    "testFile": "e2e/mobile-ux-patterns.spec.ts",
    "criticalPatterns": [count],
    "warningPatterns": [count],
    "infoPatterns": [count],
    "ciConfigured": true,
    "pagesTestesed": [count]
  }
```

**Generate summary from task data:**

Call `TaskList` to get all pattern tasks and their metadata, then present:

1. Summary of anti-patterns that will be detected
2. Which tests will fail immediately (known issues)
3. Which tests will pass (good patterns already in place)

```
## Mobile UX CI Tests Generated

### Anti-Patterns Detected
[Generated from pattern tasks:]
- **Critical (will fail CI):** [count]
  - Hamburger menu detected
  - Touch targets < 44pt
- **Warning (logged but passes):** [count]
  - Native <select> elements
- **Info (suggestions only):** [count]
  - Heavy Material shadows

### Test File
- Path: e2e/mobile-ux-patterns.spec.ts
- Tests: [count]
- Pages covered: [list from app task]

### CI Integration
- Workflow: [path or status]
- Runs on: push, pull_request
```

Ask user:
- Should any anti-patterns be allowed temporarily?
- Any additional patterns to check?
- Ready to add to CI?

## Session Recovery

If resuming from an interrupted session:

**Recovery decision tree:**
```
TaskList shows:
├── Main task in_progress, no infra task
│   └── Start from Phase 1 (assess infrastructure)
├── Infra task completed, no app task
│   └── Start from Phase 2 (explore app)
├── App task in_progress
│   └── Resume app exploration agent
├── App task completed, no generate task
│   └── Start from Phase 3 (generate tests)
├── Generate task in_progress, pattern tasks exist
│   └── Continue generating tests for remaining patterns
├── Generate task completed, no CI task
│   └── Start from Phase 5 (CI integration)
├── CI task in_progress
│   └── Resume CI setup
├── Pattern tasks pending user decisions
│   └── Present pattern severity choices to user
├── Main task completed
│   └── Generation done, show summary
└── No tasks exist
    └── Fresh start (Phase 1)
```

**Resuming with pending pattern decisions:**
```
1. Get all tasks with "Pattern:" prefix
2. Check metadata for userDecision field
3. If any patterns lack decisions:
   "Found patterns needing severity decisions:
    - Hamburger menu: [pending] - enforce/allow/warning?
    - FAB detected: [pending] - enforce/allow/warning?
   Please decide which anti-patterns should fail CI."
4. Update pattern tasks with user decisions
5. Regenerate tests with updated severity levels
```

**Always inform user when resuming:**
```
Resuming Mobile UX CI session:
- Infrastructure: [status from infra task]
- App explored: [pages from app task]
- Patterns detected: [counts from pattern tasks]
- Current state: [in_progress task description]
- Pending: [any pattern decisions needed]
- Resuming: [next action]
```

## Anti-Pattern Reference

### Critical (Should Always Fail CI)

1. **Hamburger Menu for Primary Navigation**
   - Why: iOS users expect tab bars at bottom
   - Reference: [iOS vs Android Navigation](https://www.learnui.design/blog/ios-vs-android-app-ui-design-complete-guide.html)

2. **Floating Action Button (FAB)**
   - Why: Material Design pattern, not iOS
   - Reference: [Material vs iOS](https://medium.com/@helenastening/material-design-v-s-ios-11-b4f87857814a)

3. **Touch Targets < 44pt**
   - Why: Apple HIG requirement for accessibility
   - Reference: [Apple HIG](https://developer.apple.com/design/human-interface-guidelines/)

4. **Horizontal Overflow**
   - Why: Content should fit viewport on mobile
   - Reference: Basic responsive design

### Warning (Should Log but May Not Fail)

1. **Native `<select>` Elements**
   - Why: iOS apps use picker wheels
   - Note: Some selects are acceptable for accessibility

2. **Checkboxes**
   - Why: iOS uses toggle switches
   - Note: Checkmarks in lists are acceptable

3. **Text Selection on UI**
   - Why: Native apps prevent selecting UI text
   - Note: Content text should remain selectable

4. **No Safe Area Insets**
   - Why: Content may go under notch
   - Note: Only relevant for notched devices

### Informational (Suggestions Only)

1. **Heavy Shadows (Material Elevation)**
2. **Missing touch-action: manipulation**
3. **Non-system fonts**

## Customization Points

When generating tests, ask about:

1. **Severity levels**: Which anti-patterns should fail CI vs warn?
2. **Exceptions**: Any patterns that are intentionally kept?
3. **Additional patterns**: App-specific anti-patterns to detect?
4. **Viewport sizes**: Which devices to test?

## Example Output

After running this skill, the user should have:

1. `e2e/mobile-ux-patterns.spec.ts` - Comprehensive anti-pattern tests
2. Updated CI workflow (if needed)
3. Clear documentation of what's being checked
4. Immediate visibility into current anti-patterns

## Sources

- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [iOS vs Android Design](https://www.learnui.design/blog/ios-vs-android-app-ui-design-complete-guide.html)
- [Touch Target Sizes](https://www.smashingmagazine.com/2023/04/accessible-tap-target-sizes-rage-taps-clicks/)
- [PWA Native Feel](https://www.netguru.com/blog/pwa-ios)
- [WCAG 2.5.8 Target Size](https://www.w3.org/WAI/WCAG21/Understanding/target-size.html)
