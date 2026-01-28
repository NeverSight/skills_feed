---
name: webpage-screenshotter
description: High-resolution Playwright-based screenshot capture skill that takes full-page screenshots of any URL with optimized settings for quality and reliability
tools: Read, Write, Bash
model: inherit
thinking:
  type: enabled
  budget_tokens: 5000
max_turns: 3
max_budget: 0.05
---

# Screenshotter Skill

## Description
A high-resolution Playwright-based screenshot capture skill that takes full-page screenshots of any URL with optimized settings for quality and reliability.

## Features
- High-resolution viewport (1920x1080)
- Full-page screenshot capture
- Timeout error handling
- Page reload for stability
- Base64 encoding of screenshot data
- Extended timeout (120 seconds) for slow-loading pages

## Configuration
- **Viewport**: 1920x1080 pixels
- **Device Scale Factor**: 0.5
- **Timeout**: 120 seconds
- **Wait Strategy**: domcontentloaded
- **Screenshot Type**: Full page

## Wait Strategies

Choose the appropriate wait strategy based on your needs:

- **`domcontentloaded`** (default): Fast, waits for HTML to parse. Good for most pages.
- **`load`**: Waits for all resources (images, stylesheets). More reliable but slower.
- **`networkidle`**: Waits until no network activity for 500ms. Best for dynamic content.

## Python Implementation

```python
import asyncio
import base64
from playwright.async_api import async_playwright
import playwright._impl._api_types

async def get_screenshot(url):
    """
    Capture a full-page screenshot of a given URL using Playwright.
    
    Args:
        url (str): The URL to capture
        
    Returns:
        str: Base64-encoded screenshot data
    """
    print('in get_screenshot_func_remote', url)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1920, "height": 1080, "device_scale_factor": 0.5})
        
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=120000)
        except playwright._impl._api_types.TimeoutError:
            print(f"TimeoutError: Failed to load {url} within the specified timeout.")
            await asyncio.sleep(2)
        
        # Reload page for stability
        await page.reload(wait_until='domcontentloaded')
        
        # Capture full-page screenshot
        await page.screenshot(path="screenshot.png", full_page=True)
        await browser.close()
        
        # Read and encode screenshot
        data = open("screenshot.png", "rb").read()
        print('screenshot done,', len(data))
        encoded_data = base64.b64encode(data).decode('utf-8')
        base64_image_data = f"data:image/png;base64,{encoded_data}"
        print("Screenshot of size %d bytes" % len(data))
        
        return encoded_data
```

## Usage Example

```python
import asyncio

# Basic usage
async def main():
    url = "https://example.com"
    screenshot_data = await get_screenshot(url)
    print(f"Screenshot captured and encoded: {len(screenshot_data)} characters")

# Run the async function
asyncio.run(main())
```

## Advanced Usage

### Save to Custom Path

```python
async def get_screenshot_custom_path(url, output_path="screenshot.png"):
    """
    Capture screenshot with custom output path.
    """
    print('in get_screenshot_func_remote', url)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1920, "height": 1080, "device_scale_factor": 0.5})
        
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=120000)
        except playwright._impl._api_types.TimeoutError:
            print(f"TimeoutError: Failed to load {url} within the specified timeout.")
            await asyncio.sleep(2)
        
        await page.reload(wait_until='domcontentloaded')
        await page.screenshot(path=output_path, full_page=True)
        await browser.close()
        
        data = open(output_path, "rb").read()
        print('screenshot done,', len(data))
        encoded_data = base64.b64encode(data).decode('utf-8')
        print("Screenshot of size %d bytes" % len(data))
        
        return encoded_data
```

### Batch Screenshots

```python
async def capture_multiple_screenshots(urls):
    """
    Capture screenshots of multiple URLs.
    
    Args:
        urls (list): List of URLs to capture
        
    Returns:
        dict: Dictionary mapping URLs to their base64-encoded screenshots
    """
    results = {}
    
    for url in urls:
        try:
            screenshot_data = await get_screenshot(url)
            results[url] = screenshot_data
        except Exception as e:
            print(f"Error capturing {url}: {e}")
            results[url] = None
    
    return results

# Usage
urls = ["https://example.com", "https://another-site.com"]
results = asyncio.run(capture_multiple_screenshots(urls))
```

### Wait for Full Page Load

```python
async def get_screenshot_full_load(url):
    """Wait for all resources to load before screenshot."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1920, "height": 1080, "device_scale_factor": 0.5})
        
        # Wait for complete load including all resources
        await page.goto(url, wait_until="load", timeout=120000)
        
        await page.screenshot(path="screenshot.png", full_page=True)
        await browser.close()
        
        data = open("screenshot.png", "rb").read()
        return base64.b64encode(data).decode('utf-8')
```

### Wait for Network Idle (Dynamic Content)

```python
async def get_screenshot_network_idle(url):
    """Wait for network to be idle - best for JavaScript-heavy sites."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1920, "height": 1080, "device_scale_factor": 0.5})
        
        # Wait for network idle (no requests for 500ms)
        await page.goto(url, wait_until="networkidle", timeout=120000)
        
        # Optional: wait for specific element
        await page.wait_for_selector("body", state="visible")
        
        await page.screenshot(path="screenshot.png", full_page=True)
        await browser.close()
        
        data = open("screenshot.png", "rb").read()
        return base64.b64encode(data).decode('utf-8')
```

## Cloudflare Bypass

For sites protected by Cloudflare, standard Playwright sessions are often detected. Use these techniques to bypass detection:

### Installation

**Node.js (JavaScript):**
```bash
npm install playwright-extra playwright-extra-plugin-stealth
```

**Python:**
```bash
pip install playwright playwright-stealth
```

### Stealth Mode Setup (JavaScript)

```javascript
const { chromium } = require('playwright-extra');
const stealth = require('puppeteer-extra-plugin-stealth')();

// CRITICAL: Must use stealth plugin BEFORE launching browser
chromium.use(stealth);

// Launch with stealth enabled
const browser = await chromium.launch({ 
  headless: false // Headed mode reduces detection
});
```

### Browser Fingerprint Randomization

Randomize viewport, user-agent, locale, and timezone to avoid fingerprinting:

```javascript
const context = await browser.newContext({
  viewport: {
    width: 1280 + Math.floor(Math.random() * 100), // Randomize
    height: 720 + Math.floor(Math.random() * 100)
  },
  userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
  locale: 'en-US',
  timezoneId: 'America/New_York'
});
```

### Persistent Sessions

Reuse cookies and localStorage to appear as returning user:

```javascript
const userDataDir = './session-profile';

const browser = await chromium.launchPersistentContext(userDataDir, {
  headless: false,
  args: ['--start-maximized']
});
```

### Proxy Rotation

Rotate proxies to distribute requests and avoid IP-based blocking:

```javascript
const browser = await chromium.launch({
  headless: false,
  args: [
    '--proxy-server=http://username:password@proxy-ip:port'
  ]
});
```

### CAPTCHA Detection

```javascript
// Check for CAPTCHA iframe
const isCaptchaPresent = await page.$('iframe[src*="captcha"]');

if (isCaptchaPresent) {
  console.log('CAPTCHA detected – solve or switch proxy');
}
```

### CAPTCHA Solving (Optional)

For reCAPTCHA, use 2Captcha service:

```javascript
const RecaptchaPlugin = require('@extra/recaptcha');

chromium.use(
  RecaptchaPlugin({
    provider: {
      id: '2captcha',
      token: 'YOUR_2CAPTCHA_API_KEY'
    },
    visualFeedback: true
  })
);

await page.solveRecaptchas();
```

### Session Cookie Management

Save and restore cookies for continuity:

```javascript
// Save cookies after successful scrape
const cookies = await context.cookies();
fs.writeFileSync('./cookies.json', JSON.stringify(cookies, null, 2));

// Restore cookies on next run
const savedCookies = JSON.parse(fs.readFileSync('./cookies.json'));
await context.addCookies(savedCookies);
```

### Complete Cloudflare Bypass Example

```javascript
const { chromium } = require('playwright-extra');
const stealth = require('puppeteer-extra-plugin-stealth')();
const fs = require('fs');

chromium.use(stealth);

async function screenshotWithCloudflareBypass(url, proxy = null) {
  const args = proxy ? [`--proxy-server=${proxy}`] : [];
  
  const browser = await chromium.launch({
    headless: false,
    args: args
  });

  const context = await browser.newContext({
    viewport: {
      width: 1280 + Math.floor(Math.random() * 100),
      height: 720 + Math.floor(Math.random() * 100)
    },
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    locale: 'en-US',
    timezoneId: 'America/New_York'
  });

  const page = await context.newPage();

  // Load page and wait for Cloudflare checks
  await page.goto(url, { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(5000); // Let Cloudflare finish background checks

  // Check for CAPTCHA
  const captchaPresent = await page.$('iframe[src*="captcha"]');
  if (captchaPresent) {
    console.log('CAPTCHA detected');
    // Handle CAPTCHA or switch proxy
  }

  // Capture screenshot
  await page.screenshot({ path: "screenshot.png", fullPage: true });

  // Save cookies for next visit
  const cookies = await context.cookies();
  fs.writeFileSync('./cookies.json', JSON.stringify(cookies, null, 2));

  await browser.close();
}
```

### Best Practices

1. **Use headed mode** (`headless: false`) - reduces detection
2. **Rotate proxies** - avoid IP-based blocking
3. **Randomize fingerprints** - viewport, user-agent, timezone
4. **Persist sessions** - reuse cookies to appear as returning user
5. **Wait for Cloudflare** - add delays for background JS checks
6. **Monitor CAPTCHAs** - detect and handle challenges
7. **Limit reuse** - don't reuse same proxy/UA combo too often

## Dependencies

**Python:**
```bash
pip install playwright
playwright install chromium
```

**Node.js (with Cloudflare bypass):**
```bash
npm install playwright-extra playwright-extra-plugin-stealth
```

## Error Handling

The skill includes robust error handling for:
- **Timeout errors**: Gracefully handles pages that don't load within 120 seconds
- **Network failures**: Continues execution even if initial page load fails
- **Browser crashes**: Ensures browser is properly closed even on errors

## Performance Notes

- The viewport is set to 1920x1080 with a device scale factor of 0.5, resulting in effective 960x540 rendering
- Full-page screenshots may take longer for very long pages
- The page reload step ensures dynamic content is fully loaded
- Screenshots are saved temporarily as PNG files before being base64-encoded

## Use Cases

- Automated website monitoring
- Visual regression testing
- Web scraping with visual confirmation
- Documentation generation
- Archiving web pages
- Quality assurance workflows

