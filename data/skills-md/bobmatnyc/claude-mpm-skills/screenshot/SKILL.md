---
name: screenshot
description: "Visual verification workflow for UI changes to accelerate code review and catch ..."
version: 1.0.0
tags: []
progressive_disclosure:
  entry_point:
    summary: "Visual verification workflow for UI changes to accelerate code review and catch ..."
    when_to_use: "When working with screenshot or related functionality."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
---
# Screenshot-Based UI Verification

Visual verification workflow for UI changes to accelerate code review and catch responsive design issues early.

## When to Use This Skill

Use this skill when:
- Making any UI changes (components, styling, layout)
- Implementing responsive design
- Creating pull requests with visual changes
- Want to demonstrate UI behavior without reviewers running code locally
- Need to document visual state before/after bug fixes

## Why Screenshot Verification Matters

### Benefits
- **Faster Reviews**: Reviewers see changes instantly without local setup
- **Documents Design**: Creates visual record of design decisions
- **Visual Changelog**: Historical record of UI evolution
- **Catches Responsive Issues**: Early detection of mobile/tablet problems
- **Reduces Communication**: Less back-and-forth about visual changes
- **Quality Gate**: Forces conscious review of visual output

### Problems It Solves
- ❌ "I can't reproduce the layout issue locally"
- ❌ "What does this look like on mobile?"
- ❌ "Is this the intended design?"
- ❌ "How does this compare to the old version?"
- ✅ All answered with screenshots in PR

## Required Screenshots

For any PR that changes UI, capture all three viewport sizes:

### 1. Desktop View (1920x1080)
- Full page screenshot
- Key component close-ups if needed
- Before and after comparisons (for fixes/refactors)
- Different states (default, hover, active, error, loading)

### 2. Tablet View (768x1024)
- Portrait orientation
- Verify responsive breakpoints
- Touch interaction targets visible
- Menu/navigation in tablet mode

### 3. Mobile View (375x667)
- Portrait orientation (iPhone 8/SE size - common minimum)
- Touch target sizes visible (minimum 44x44px)
- Scrolling behavior documented
- Mobile menu states

## How to Capture Screenshots

### Browser DevTools Method

**Chrome/Edge DevTools**:
1. Open DevTools (F12 or Cmd+Option+I)
2. Toggle device toolbar (Cmd+Shift+M or Ctrl+Shift+M)
3. Select device preset or custom dimensions:
   - Desktop: 1920 x 1080
   - Tablet: 768 x 1024
   - Mobile: 375 x 667
4. Capture screenshot:
   - Full page: Cmd+Shift+P → "Capture full size screenshot"
   - Viewport only: Cmd+Shift+P → "Capture screenshot"

**Firefox DevTools**:
1. Open DevTools (F12)
2. Toggle Responsive Design Mode (Cmd+Option+M)
3. Set dimensions
4. Click screenshot icon in toolbar

### CLI Screenshot Tools

**Using Playwright** (recommended for CI):
```javascript
// screenshot.js
const { chromium } = require('playwright');

async function captureScreenshots(url) {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  await page.goto(url);

  // Desktop
  await page.setViewportSize({ width: 1920, height: 1080 });
  await page.screenshot({
    path: 'screenshots/desktop.png',
    fullPage: true
  });

  // Tablet
  await page.setViewportSize({ width: 768, height: 1024 });
  await page.screenshot({
    path: 'screenshots/tablet.png',
    fullPage: true
  });

  // Mobile
  await page.setViewportSize({ width: 375, height: 667 });
  await page.screenshot({
    path: 'screenshots/mobile.png',
    fullPage: true
  });

  await browser.close();
}

captureScreenshots('http://localhost:3000');
```

Run: `node screenshot.js`

**Using Puppeteer**:
```javascript
// screenshot.js
const puppeteer = require('puppeteer');

async function captureScreenshots(url) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  await page.goto(url, { waitUntil: 'networkidle2' });

  // Desktop
  await page.setViewport({ width: 1920, height: 1080 });
  await page.screenshot({
    path: 'screenshots/desktop.png',
    fullPage: true
  });

  // Tablet
  await page.setViewport({ width: 768, height: 1024 });
  await page.screenshot({
    path: 'screenshots/tablet.png',
    fullPage: true
  });

  // Mobile
  await page.setViewport({ width: 375, height: 667 });
  await page.screenshot({
    path: 'screenshots/mobile.png',
    fullPage: true
  });

  await browser.close();
}

captureScreenshots('http://localhost:3000');
```

## PR Description Template

Use this template to document visual changes:

```markdown
## Visual Changes

### Desktop (1920x1080)
![Desktop view](./screenshots/desktop.png)

**Key changes**:
- Updated header navigation layout
- Improved spacing between sections
- Added hover states to buttons

### Tablet (768x1024)
![Tablet view](./screenshots/tablet.png)

**Key changes**:
- Stacked layout for sidebar
- Touch-friendly button sizes (48x48px)
- Adjusted typography for readability

### Mobile (375x667)
![Mobile view](./screenshots/mobile.png)

**Key changes**:
- Hamburger menu replaces horizontal nav
- Single column layout
- Bottom sticky CTA button

### Before/After Comparison

#### Before (Bug)
![Before fix](./screenshots/before-mobile.png)

**Issue**: Text overflowing container on mobile

#### After (Fixed)
![After fix](./screenshots/after-mobile.png)

**Fix**: Applied word-wrap and max-width constraints

### Interaction States

#### Default State
![Default](./screenshots/state-default.png)

#### Hover State
![Hover](./screenshots/state-hover.png)

#### Active/Selected State
![Active](./screenshots/state-active.png)

#### Error State
![Error](./screenshots/state-error.png)

#### Loading State
![Loading](./screenshots/state-loading.png)

## Responsive Design Notes
- Breakpoints: 768px (tablet), 375px (mobile)
- All touch targets > 44x44px
- Text remains readable at all sizes (min 16px body)
- No horizontal scrolling on any viewport
- Images scale proportionally

## Accessibility Checks
- [ ] Keyboard navigation works
- [ ] Focus states visible
- [ ] Color contrast meets WCAG AA (4.5:1)
- [ ] Alt text on images
- [ ] ARIA labels where needed
```

## Automated Screenshot Testing

### Using Playwright Test

```javascript
// tests/visual.spec.js
const { test, expect } = require('@playwright/test');

test.describe('Visual Regression', () => {
  test('homepage looks correct on desktop', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.setViewportSize({ width: 1920, height: 1080 });
    await expect(page).toHaveScreenshot('homepage-desktop.png');
  });

  test('homepage looks correct on mobile', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.setViewportSize({ width: 375, height: 667 });
    await expect(page).toHaveScreenshot('homepage-mobile.png');
  });
});
```

Run: `npx playwright test --update-snapshots` (first time to generate baselines)

### Using Storybook + Chromatic

For component-level visual testing:

1. **Setup Storybook**:
```javascript
// Button.stories.jsx
export default {
  title: 'Components/Button',
  component: Button,
};

export const Primary = () => <Button variant="primary">Click me</Button>;
export const Secondary = () => <Button variant="secondary">Click me</Button>;
```

2. **Integrate Chromatic**:
```bash
npm install --save-dev chromatic
npx chromatic --project-token=<token>
```

3. **CI Integration** (GitHub Actions):
```yaml
# .github/workflows/chromatic.yml
name: Chromatic
on: push
jobs:
  chromatic:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npx chromatic --project-token=${{ secrets.CHROMATIC_TOKEN }}
```

## Screenshot Checklist

Before submitting PR with UI changes:

### Capture Requirements
- [ ] Desktop screenshot (1920x1080) captured
- [ ] Tablet screenshot (768x1024) captured
- [ ] Mobile screenshot (375x667) captured
- [ ] All screenshots uploaded to PR
- [ ] Before/after comparison included (for bug fixes)

### Quality Checks
- [ ] Screenshots show full page (not cut off)
- [ ] No localhost URLs visible in screenshots
- [ ] No sensitive data in screenshots (PII, keys, etc.)
- [ ] Screenshots are clear and readable
- [ ] File names are descriptive (e.g., `desktop-homepage.png`)

### Documentation
- [ ] Key changes listed for each viewport
- [ ] Responsive behavior described
- [ ] Accessibility notes included
- [ ] Interaction states documented (if applicable)

## Common Issues and Solutions

### Issue: Screenshots Too Large
**Problem**: Screenshots are 5MB+ and slow to load in PR
**Solution**: Compress images before uploading
```bash
# Using ImageMagick
convert input.png -quality 85 output.png

# Using pngquant
pngquant input.png --output output.png
```

### Issue: Dynamic Content Changes Between Screenshots
**Problem**: Timestamps, random data make screenshots inconsistent
**Solution**: Mock data or freeze time in tests
```javascript
// Mock Date
const mockDate = new Date('2025-01-01T00:00:00Z');
jest.useFakeTimers();
jest.setSystemTime(mockDate);

// Or in Playwright
await page.addInitScript(() => {
  Date.now = () => 1704067200000; // Fixed timestamp
});
```

### Issue: Screenshot Diffs Show Font Rendering Differences
**Problem**: Same code renders differently on different OS
**Solution**: Use Docker for consistent environment
```dockerfile
FROM mcr.microsoft.com/playwright:v1.40.0-jammy
WORKDIR /app
COPY . .
RUN npm ci
CMD ["npm", "run", "screenshot"]
```

## Screenshot Organization

### Directory Structure
```
screenshots/
├── desktop/
│   ├── homepage.png
│   ├── product-list.png
│   └── checkout.png
├── tablet/
│   ├── homepage.png
│   ├── product-list.png
│   └── checkout.png
└── mobile/
    ├── homepage.png
    ├── product-list.png
    └── checkout.png
```

### Naming Convention
- Use descriptive names: `desktop-homepage-logged-in.png`
- Include state if relevant: `mobile-form-error-state.png`
- Version comparisons: `before-header-fix.png`, `after-header-fix.png`

## Integration with CI/CD

### GitHub Actions Example
```yaml
name: Visual Testing
on: pull_request

jobs:
  screenshots:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Build app
        run: npm run build

      - name: Start app
        run: npm start &

      - name: Wait for app
        run: npx wait-on http://localhost:3000

      - name: Capture screenshots
        run: node scripts/screenshot.js

      - name: Upload screenshots
        uses: actions/upload-artifact@v4
        with:
          name: screenshots
          path: screenshots/
```

## Best Practices

### Do's
- ✅ Capture all three viewport sizes
- ✅ Include before/after for bug fixes
- ✅ Document interaction states (hover, active, error)
- ✅ Compress large images
- ✅ Use descriptive file names
- ✅ Annotate screenshots with key changes

### Don'ts
- ❌ Skip mobile screenshots ("desktop only" is rare)
- ❌ Upload screenshots with sensitive data
- ❌ Use random viewport sizes (stick to standards)
- ❌ Forget to document responsive breakpoints
- ❌ Rely solely on screenshots (still need code review)

## Related Skills

- `universal-verification-pre-merge` - Pre-merge verification checklist
- `universal-testing-webapp-testing` - Web application testing patterns
- `toolchains-javascript-testing-playwright` - Playwright testing framework
- `universal-debugging-verification-before-completion` - Verification workflows
