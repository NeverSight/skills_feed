---
name: webapp-testing
description: Test local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.
---

# Webapp Testing

This is a toolkit for interacting with and testing local web applications using Playwright. It supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.

## Key Helper Scripts

- **`scripts/with_server.py`** - Manages server lifecycle (supports multiple servers)

⚠️ **Always run scripts with `--help` first** to see usage. DO NOT read the source until you try running the script first and find that a customized solution is absolutely necessary.

## Decision Tree: Choosing Your Approach

```
User task → Is it static HTML?
 ├─ Yes → Read HTML file directly to identify selectors
 │ ├─ Success → Write Playwright script using selectors
 │ └─ Fails/Incomplete → Treat as dynamic (below)
 │
 └─ No (dynamic webapp) → Is the server already running?
   ├─ No → Run: python scripts/with_server.py --help
   │ Then use the helper + write simplified Playwright script
   │
   └─ Yes → Reconnaissance-then-action:
     1. Navigate and wait for networkidle
     2. Take screenshot or inspect DOM
     3. Identify selectors from rendered state
     4. Execute actions with discovered selectors
```

## Example: Using with_server.py

### Single Server
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
```

### Multiple Servers
```bash
python scripts/with_server.py \
 --server "cd backend && python server.py" --port 3000 \
 --server "cd frontend && npm run dev" --port 5173 \
 -- python your_automation.py
```

### Automation Script Template
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # Always launch chromium in headless mode
    page = browser.new_page()
    page.goto('http://localhost:5173')  # Server already running and ready
    page.wait_for_load_state('networkidle')  # CRITICAL: Wait for JS to execute
    # ... your automation logic
    browser.close()
```

## Reconnaissance-Then-Action Pattern

1. **Inspect rendered DOM:**
   ```python
   page.screenshot(path='/tmp/inspect.png', full_page=True)
   content = page.content()
   page.locator('button').all()
   ```

2. **Identify selectors** from inspection results

3. **Execute actions** using discovered selectors

## Common Pitfall

❌ **Don't** inspect the DOM before waiting for `networkidle` on dynamic apps

✅ **Do** wait for `page.wait_for_load_state('networkidle')` before inspection

## Best Practices

- **Use bundled scripts as black boxes** - Use `--help` to see usage, then invoke directly without reading source
- Use `sync_playwright()` for synchronous scripts
- Always close the browser when done
- Use descriptive selectors: `text=`, `role=`, CSS selectors, or IDs
- Add appropriate waits: `page.wait_for_selector()` or `page.wait_for_timeout()`

## Reference Files

- **examples/** - Common patterns:
  - `element_discovery.py` - Discovering buttons, links, and inputs on a page
  - `static_html_automation.py` - Using file:// URLs for local HTML
  - `console_logging.py` - Capturing console logs during automation
