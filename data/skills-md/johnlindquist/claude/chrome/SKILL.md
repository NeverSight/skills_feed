---
name: chrome
description: Browser automation using Puppeteer or Playwright. Use for web testing, screenshots, form filling, and automated browser interactions.
---

# Chrome Automation

Automate browser interactions using Puppeteer or Playwright.

## Prerequisites

```bash
# Puppeteer
npm install puppeteer

# Or Playwright
npm install playwright
npx playwright install chromium
```

## Puppeteer Quick Start

### Basic Script

```javascript
// script.js
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto('https://example.com');
  await page.screenshot({ path: 'screenshot.png' });
  await browser.close();
})();
```

Run: `node script.js`

### With Visible Browser

```javascript
const browser = await puppeteer.launch({
  headless: false,
  slowMo: 50,  // Slow down operations
});
```

## Playwright Quick Start

### Basic Script

```javascript
// script.js
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('https://example.com');
  await page.screenshot({ path: 'screenshot.png' });
  await browser.close();
})();
```

## Common Operations

### Navigation

```javascript
// Go to URL
await page.goto('https://example.com');

// Wait for navigation
await page.goto('https://example.com', { waitUntil: 'networkidle0' });

// Go back/forward
await page.goBack();
await page.goForward();

// Reload
await page.reload();
```

### Screenshots

```javascript
// Full page
await page.screenshot({ path: 'full.png', fullPage: true });

// Specific element
const element = await page.$('#header');
await element.screenshot({ path: 'header.png' });

// With options
await page.screenshot({
  path: 'screenshot.png',
  type: 'png',
  quality: 90,  // For jpeg
  clip: { x: 0, y: 0, width: 800, height: 600 }
});
```

### Click Actions

```javascript
// Click element
await page.click('#button');
await page.click('button.submit');

// Double click
await page.dblclick('#item');

// Right click
await page.click('#element', { button: 'right' });

// Click and wait for navigation
await Promise.all([
  page.waitForNavigation(),
  page.click('a.link')
]);
```

### Form Filling

```javascript
// Type text
await page.type('#email', 'user@example.com');

// Clear and type
await page.fill('#email', 'user@example.com');  // Playwright
await page.$eval('#email', el => el.value = '');  // Puppeteer clear
await page.type('#email', 'user@example.com');

// Select dropdown
await page.select('#country', 'US');

// Checkbox
await page.check('#agree');  // Playwright
await page.click('#agree');  // Puppeteer

// File upload
await page.setInputFiles('#file', '/path/to/file.pdf');  // Playwright
const input = await page.$('#file');
await input.uploadFile('/path/to/file.pdf');  // Puppeteer
```

### Waiting

```javascript
// Wait for selector
await page.waitForSelector('#loaded');

// Wait for text
await page.waitForFunction(() =>
  document.body.textContent.includes('Success')
);

// Wait for navigation
await page.waitForNavigation();

// Wait for network idle
await page.waitForLoadState('networkidle');  // Playwright

// Explicit wait
await page.waitForTimeout(1000);  // Not recommended for production
```

### Extract Data

```javascript
// Get text content
const text = await page.textContent('#element');
const text = await page.$eval('#element', el => el.textContent);

// Get attribute
const href = await page.getAttribute('a', 'href');
const href = await page.$eval('a', el => el.href);

// Get multiple elements
const items = await page.$$eval('.item', els =>
  els.map(el => el.textContent)
);

// Get page content
const html = await page.content();
```

### Evaluate JavaScript

```javascript
// Run in browser context
const result = await page.evaluate(() => {
  return document.title;
});

// With arguments
const text = await page.evaluate((selector) => {
  return document.querySelector(selector).textContent;
}, '#element');
```

## Testing Patterns

### Login Flow

```javascript
async function login(page, username, password) {
  await page.goto('https://app.example.com/login');
  await page.fill('#username', username);
  await page.fill('#password', password);
  await page.click('button[type="submit"]');
  await page.waitForSelector('#dashboard');
}
```

### Form Submission Test

```javascript
async function testForm(page) {
  await page.goto('https://example.com/form');

  // Fill form
  await page.fill('#name', 'Test User');
  await page.fill('#email', 'test@example.com');
  await page.select('#country', 'US');
  await page.check('#agree');

  // Submit
  await page.click('button[type="submit"]');

  // Verify success
  await page.waitForSelector('.success-message');
  const message = await page.textContent('.success-message');
  console.assert(message.includes('Thank you'));
}
```

### Visual Regression

```javascript
// Take baseline
await page.screenshot({ path: 'baseline.png', fullPage: true });

// Later, compare
await page.screenshot({ path: 'current.png', fullPage: true });
// Use image comparison tool
```

## Device Emulation

```javascript
// Puppeteer
const iPhone = puppeteer.devices['iPhone 12'];
await page.emulate(iPhone);

// Playwright
const iPhone = playwright.devices['iPhone 12'];
const context = await browser.newContext({ ...iPhone });

// Manual viewport
await page.setViewportSize({ width: 375, height: 812 });
```

## Network

```javascript
// Intercept requests (Playwright)
await page.route('**/api/*', route => {
  route.fulfill({ status: 200, body: JSON.stringify({ mocked: true }) });
});

// Block resources
await page.route('**/*.{png,jpg,jpeg}', route => route.abort());

// Monitor requests
page.on('request', req => console.log(req.url()));
page.on('response', res => console.log(res.status(), res.url()));
```

## Best Practices

1. **Use explicit waits** - Not timeouts
2. **Handle errors** - try/catch important
3. **Close browsers** - Always clean up
4. **Use headless for CI** - Faster, no display needed
5. **Test selectors** - Prefer data-testid
6. **Screenshot on failure** - Debug easier
7. **Reuse contexts** - Faster than new browsers
