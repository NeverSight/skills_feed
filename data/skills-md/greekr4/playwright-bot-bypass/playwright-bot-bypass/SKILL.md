---
name: playwright-bot-bypass
description: This skill should be used when the user asks to "bypass bot detection", "avoid CAPTCHA", "stealth browser automation", "undetected playwright", "bypass Google bot check", "rebrowser-playwright", or needs to automate websites that detect and block bots.
version: 1.0.0
---

# Playwright Bot Bypass

Bypass bot detection systems using rebrowser-playwright with stealth techniques. This approach successfully passes bot detection tests like bot.sannysoft.com and enables automation on sites with aggressive bot protection (Google, Cloudflare, etc.).

## Why Standard Playwright Gets Detected

Standard Playwright/Puppeteer exposes several automation signatures:

| Detection Point | Standard Playwright | This Solution |
|-----------------|---------------------|---------------|
| WebDriver property | `navigator.webdriver = true` | Removed |
| WebGL Renderer | SwiftShader (software) | Real GPU (Apple M2, etc.) |
| User Agent | Contains "HeadlessChrome" | Clean Chrome UA |
| Chrome runtime | Missing properties | Complete chrome.runtime |

## Quick Start

### 1. Install Dependencies

```bash
npm install rebrowser-playwright
```

### 2. Basic Stealth Script

```javascript
import { chromium } from 'rebrowser-playwright';

const browser = await chromium.launch({
  headless: false,
  channel: 'chrome'  // Use real Chrome browser
});

const context = await browser.newContext();

// Remove WebDriver property
await context.addInitScript(() => {
  delete Object.getPrototypeOf(navigator).webdriver;
});

const page = await context.newPage();
await page.goto('https://example.com');
```

## Key Components

### rebrowser-playwright

Drop-in replacement for playwright that patches automation detection:

- Uses real GPU instead of SwiftShader
- Removes HeadlessChrome from User Agent
- Patches various fingerprinting vectors

### addInitScript for WebDriver

The `navigator.webdriver` property is the most common detection method:

```javascript
await context.addInitScript(() => {
  delete Object.getPrototypeOf(navigator).webdriver;
});
```

### Real Chrome Browser

Always use `channel: 'chrome'` to launch the user's installed Chrome:

```javascript
chromium.launch({
  headless: false,
  channel: 'chrome'
});
```

## Complete Example

See `examples/stealth-google-search.mjs` for a complete working example that:

1. Bypasses bot detection
2. Performs Google search
3. Captures results

## Testing Bot Detection

Verify bypass effectiveness at https://bot.sannysoft.com:

```bash
node scripts/bot-detection-test.mjs
```

All items should show green (passed).

## Scripts

- **`scripts/bot-detection-test.mjs`** - Test bot detection status
- **`scripts/stealth-template.mjs`** - Reusable stealth browser template

## Examples

- **`examples/stealth-google-search.mjs`** - Google search without CAPTCHA
- **`examples/ab-test.mjs`** - Compare detected vs stealth side-by-side

## Limitations

- Requires `headless: false` (headed mode)
- Needs real Chrome installed (`channel: 'chrome'`)
- Some sites may still detect based on behavior patterns
- Does not bypass CAPTCHAs, only prevents triggering them

## Python Support

### playwright-stealth (Limited)

**Python `playwright-stealth` cannot fully bypass bot detection.**

| Environment | bot.sannysoft.com | Google Search |
|-------------|-------------------|---------------|
| Node.js rebrowser-playwright | ✅ Pass | ✅ Works |
| Python playwright-stealth | ✅ Pass | ❌ CAPTCHA |

**Why?**
- `rebrowser-playwright`: Chromium binary-level patch → uses real GPU
- `playwright-stealth`: JavaScript-level patch only → SwiftShader exposed

### undetected-chromedriver (Recommended for Python)

**`undetected-chromedriver` fully bypasses bot detection in Python!**

| Library | bot.sannysoft.com | Google Search |
|---------|-------------------|---------------|
| playwright-stealth | ✅ Pass | ❌ CAPTCHA |
| **undetected-chromedriver** | ✅ Pass | ✅ **Works!** |

#### Installation

```bash
pip install undetected-chromedriver
```

#### Usage

```python
import undetected_chromedriver as uc

# Specify your Chrome version
driver = uc.Chrome(version_main=144)

driver.get("https://www.google.com")
search_box = driver.find_element("name", "q")
search_box.send_keys("your search query")
search_box.submit()
```

#### Key Points

- Uses Selenium WebDriver API (not Playwright)
- Automatically patches ChromeDriver to avoid detection
- Requires specifying `version_main` matching your Chrome version
- Check Chrome version: `chrome://version`

### Alternative: Subprocess

For Electron/Node.js apps, call Node.js script from Python:

```python
import subprocess
result = subprocess.run(['node', 'stealth-script.mjs', query], capture_output=True)
```

## Troubleshooting

### Still Getting Detected?

1. Ensure using `rebrowser-playwright`, not `playwright`
2. Verify `channel: 'chrome'` is set
3. Check `addInitScript` runs before navigation
4. Try adding delays between actions (human-like behavior)

### Browser Not Opening?

```bash
# Verify Chrome is installed
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version
```

### WebGL Still Shows SwiftShader?

This happens with regular playwright. Confirm import is from `rebrowser-playwright`:

```javascript
// Correct
import { chromium } from 'rebrowser-playwright';

// Wrong - will be detected
import { chromium } from 'playwright';
```
