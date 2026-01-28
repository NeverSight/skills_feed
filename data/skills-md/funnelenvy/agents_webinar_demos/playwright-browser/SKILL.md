---
name: playwright-browser
description: Use when capturing screenshots, automating browser interactions, or scraping web content. Covers Playwright Python API for page navigation, screenshots, element selection, form filling, and waiting strategies.
---

# Playwright Browser Automation

Use this skill for capturing screenshots, web scraping, form automation, and browser-based testing.

## Quick Start

The project's venv has Playwright installed. Always use the venv Python:

```bash
# Run Playwright scripts
.venv/bin/python scripts/my_playwright_script.py

# Install browsers if needed (one-time)
.venv/bin/playwright install chromium
```

## Screenshot Capture

### Basic Screenshot

```python
#!/Users/arun/dev/agents_webinar/.venv/bin/python
from playwright.sync_api import sync_playwright

def capture_screenshot(url: str, output_path: str) -> str:
    """Capture a screenshot of a webpage.

    Args:
        url: URL to capture
        output_path: Path to save PNG file

    Returns:
        Path to saved screenshot
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1280, 'height': 800})
        page.goto(url, wait_until='networkidle')
        page.screenshot(path=output_path)
        browser.close()
    return output_path

# Usage
capture_screenshot('https://example.com', 'screenshot.png')
```

### Full Page Screenshot

```python
def capture_full_page(url: str, output_path: str) -> str:
    """Capture full-page screenshot (scrolls entire page)."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1280, 'height': 800})
        page.goto(url, wait_until='networkidle')
        page.screenshot(path=output_path, full_page=True)
        browser.close()
    return output_path
```

### Above-the-Fold Screenshot

```python
def capture_above_fold(url: str, output_path: str, width: int = 1280, height: int = 800) -> str:
    """Capture only the visible viewport (above-the-fold content)."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': width, 'height': height})
        page.goto(url, wait_until='networkidle')
        # Viewport screenshot (not full_page)
        page.screenshot(path=output_path, full_page=False)
        browser.close()
    return output_path
```

### Element Screenshot

```python
def capture_element(url: str, selector: str, output_path: str) -> str:
    """Capture screenshot of a specific element."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until='networkidle')
        element = page.locator(selector)
        element.screenshot(path=output_path)
        browser.close()
    return output_path

# Usage
capture_element('https://example.com', 'header.hero', 'hero_section.png')
```

## Async API (Recommended for Multiple Pages)

```python
#!/Users/arun/dev/agents_webinar/.venv/bin/python
import asyncio
from playwright.async_api import async_playwright

async def capture_multiple_pages(urls: list[str], output_dir: str) -> list[str]:
    """Capture screenshots of multiple pages concurrently."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()

        async def capture_one(url: str) -> str:
            page = await browser.new_page(viewport={'width': 1280, 'height': 800})
            await page.goto(url, wait_until='networkidle')
            filename = url.replace('https://', '').replace('/', '_') + '.png'
            path = f"{output_dir}/{filename}"
            await page.screenshot(path=path)
            await page.close()
            return path

        results = await asyncio.gather(*[capture_one(url) for url in urls])
        await browser.close()
    return results

# Usage
asyncio.run(capture_multiple_pages([
    'https://example.com',
    'https://example.com/pricing',
    'https://example.com/about'
], 'screenshots'))
```

## Wait Strategies

### Wait Until Options

```python
# 'load' - Wait for load event (default)
page.goto(url, wait_until='load')

# 'domcontentloaded' - Wait for DOMContentLoaded
page.goto(url, wait_until='domcontentloaded')

# 'networkidle' - Wait until no network requests for 500ms (RECOMMENDED)
page.goto(url, wait_until='networkidle')

# 'commit' - Wait for first byte of response
page.goto(url, wait_until='commit')
```

### Wait for Specific Elements

```python
# Wait for element to be visible
page.wait_for_selector('.hero-cta', state='visible')

# Wait for element to be hidden
page.wait_for_selector('.loading-spinner', state='hidden')

# Wait with timeout
page.wait_for_selector('.lazy-loaded-content', timeout=10000)  # 10 seconds
```

### Wait for Network Idle After Interaction

```python
# Click and wait for network to settle
page.click('button.load-more')
page.wait_for_load_state('networkidle')

# Then capture
page.screenshot(path='after_load_more.png')
```

## Element Selection

### Locator Strategies

```python
# CSS selector (most common)
page.locator('button.cta')
page.locator('#signup-form')
page.locator('[data-testid="hero-section"]')

# Text content
page.locator('text=Sign Up Now')
page.get_by_text('Get Started')

# Role-based (accessibility)
page.get_by_role('button', name='Submit')
page.get_by_role('link', name='Pricing')

# Label (forms)
page.get_by_label('Email address')

# Placeholder
page.get_by_placeholder('Enter your email')

# Chained selectors
page.locator('form').locator('button[type="submit"]')
```

### Extract Text Content

```python
def extract_page_content(url: str) -> dict:
    """Extract key text content from a page."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until='networkidle')

        content = {
            'title': page.title(),
            'h1': page.locator('h1').first.text_content() if page.locator('h1').count() > 0 else None,
            'meta_description': page.locator('meta[name="description"]').get_attribute('content'),
            'cta_buttons': [btn.text_content() for btn in page.locator('a.cta, button.cta').all()],
        }

        browser.close()
    return content
```

## Form Automation

### Fill and Submit Form

```python
def fill_form(url: str, form_data: dict) -> str:
    """Fill out a form and capture result."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until='networkidle')

        # Fill text fields
        page.fill('input[name="email"]', form_data['email'])
        page.fill('input[name="company"]', form_data['company'])

        # Select dropdown
        page.select_option('select[name="country"]', form_data['country'])

        # Check checkbox
        page.check('input[name="agree_terms"]')

        # Click submit
        page.click('button[type="submit"]')

        # Wait for navigation/result
        page.wait_for_load_state('networkidle')

        # Capture result
        page.screenshot(path='form_result.png')
        browser.close()
    return 'form_result.png'
```

## Mobile Screenshots

```python
from playwright.sync_api import sync_playwright

def capture_mobile(url: str, output_path: str) -> str:
    """Capture screenshot with mobile viewport."""
    with sync_playwright() as p:
        # Use iPhone 12 device profile
        iphone = p.devices['iPhone 12']
        browser = p.chromium.launch()
        context = browser.new_context(**iphone)
        page = context.new_page()
        page.goto(url, wait_until='networkidle')
        page.screenshot(path=output_path)
        browser.close()
    return output_path

# Available device profiles include:
# 'iPhone 12', 'iPhone 12 Pro Max', 'iPhone SE'
# 'iPad Pro', 'iPad Mini'
# 'Pixel 5', 'Galaxy S9+'
# 'Desktop Chrome', 'Desktop Firefox', 'Desktop Safari'
```

## PDF Generation

```python
def generate_pdf(url: str, output_path: str) -> str:
    """Generate PDF from webpage (Chromium only)."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until='networkidle')
        page.pdf(
            path=output_path,
            format='A4',
            print_background=True,
            margin={'top': '1cm', 'bottom': '1cm', 'left': '1cm', 'right': '1cm'}
        )
        browser.close()
    return output_path
```

## Error Handling

```python
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

def safe_capture(url: str, output_path: str, timeout: int = 30000) -> dict:
    """Capture with comprehensive error handling."""
    result = {'success': False, 'path': None, 'error': None}

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={'width': 1280, 'height': 800})

            response = page.goto(url, wait_until='networkidle', timeout=timeout)

            if response and response.status >= 400:
                result['error'] = f"HTTP {response.status}"
            else:
                page.screenshot(path=output_path)
                result['success'] = True
                result['path'] = output_path

            browser.close()

    except PlaywrightTimeout:
        result['error'] = f"Timeout after {timeout}ms"
    except Exception as e:
        result['error'] = str(e)

    return result
```

## Performance Tips

### 1. Reuse Browser Instance

```python
# Bad: Launch browser for each page
for url in urls:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        page.screenshot(...)
        browser.close()

# Good: Reuse browser
with sync_playwright() as p:
    browser = p.chromium.launch()
    for url in urls:
        page = browser.new_page()
        page.goto(url)
        page.screenshot(...)
        page.close()  # Close page, not browser
    browser.close()
```

### 2. Disable Unnecessary Resources

```python
def fast_capture(url: str, output_path: str) -> str:
    """Fast capture by blocking non-essential resources."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()

        # Block images, fonts, stylesheets for faster load
        context.route('**/*.{png,jpg,jpeg,gif,svg,woff,woff2,ttf}',
                     lambda route: route.abort())

        page = context.new_page()
        page.goto(url, wait_until='domcontentloaded')
        page.screenshot(path=output_path)
        browser.close()
    return output_path
```

### 3. Headless vs Headed Mode

```python
# Headless (default, faster, no UI)
browser = p.chromium.launch(headless=True)

# Headed (shows browser, useful for debugging)
browser = p.chromium.launch(headless=False)

# Slow motion (for demos)
browser = p.chromium.launch(headless=False, slow_mo=500)  # 500ms between actions
```

## CRO Analysis Pattern (Demo 6)

```python
#!/Users/arun/dev/agents_webinar/.venv/bin/python
"""Capture landing page for CRO analysis."""

from playwright.sync_api import sync_playwright
import json

def capture_for_cro_analysis(url: str, output_dir: str) -> dict:
    """Capture screenshots and metadata for CRO analysis.

    Returns dict with paths to:
    - above_fold.png: What users see first
    - full_page.png: Complete page
    - metadata.json: Page info (title, CTAs, etc.)
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()

        # Desktop viewport
        page = browser.new_page(viewport={'width': 1280, 'height': 800})
        page.goto(url, wait_until='networkidle')

        # Above-the-fold
        above_fold_path = f"{output_dir}/above_fold.png"
        page.screenshot(path=above_fold_path, full_page=False)

        # Full page
        full_page_path = f"{output_dir}/full_page.png"
        page.screenshot(path=full_page_path, full_page=True)

        # Extract metadata
        metadata = {
            'url': url,
            'title': page.title(),
            'h1': page.locator('h1').first.text_content() if page.locator('h1').count() > 0 else None,
            'cta_count': page.locator('a.cta, button.cta, [class*="cta"], [class*="btn-primary"]').count(),
            'form_count': page.locator('form').count(),
            'image_count': page.locator('img').count(),
        }

        metadata_path = f"{output_dir}/metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

        browser.close()

    return {
        'above_fold': above_fold_path,
        'full_page': full_page_path,
        'metadata': metadata_path
    }

if __name__ == '__main__':
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else 'https://www.reform.app/done-for-you-forms'
    output_dir = sys.argv[2] if len(sys.argv) > 2 else 'demos/06-vision-audit/outputs'

    result = capture_for_cro_analysis(url, output_dir)
    print(f"Captured: {result}")
```

## Troubleshooting

### "Browser not found"

```bash
# Install Chromium browser
.venv/bin/playwright install chromium

# Or install all browsers
.venv/bin/playwright install
```

### "Timeout waiting for page"

```python
# Increase timeout
page.goto(url, timeout=60000)  # 60 seconds

# Or use less strict wait
page.goto(url, wait_until='domcontentloaded')  # Faster than 'networkidle'
```

### "Element not found"

```python
# Check if element exists first
if page.locator('.cta-button').count() > 0:
    page.locator('.cta-button').click()
else:
    print("CTA button not found")
```

### SSL/Certificate Errors

```python
# Ignore HTTPS errors (use cautiously)
context = browser.new_context(ignore_https_errors=True)
```

## Quick Reference

**Screenshot types:**
- `page.screenshot(path='file.png')` - Viewport only
- `page.screenshot(path='file.png', full_page=True)` - Full scrollable page
- `element.screenshot(path='file.png')` - Specific element

**Wait strategies:**
- `wait_until='networkidle'` - Most reliable for dynamic pages
- `wait_until='domcontentloaded'` - Faster, for static pages
- `page.wait_for_selector('.class')` - Wait for specific element

**Viewport sizes:**
- Desktop: 1280x800 or 1920x1080
- Tablet: 768x1024
- Mobile: Use `p.devices['iPhone 12']`

**Best practices:**
1. Always use `with sync_playwright()` context manager
2. Use `wait_until='networkidle'` for JS-heavy pages
3. Close pages/browsers to free resources
4. Handle timeouts gracefully
5. Use async API for multiple concurrent captures
