---
name: gtm-testing
description: Comprehensive GTM tracking testing and validation including automated Playwright headless testing, browser console testing, GTM Preview mode validation, and GA4 DebugView verification. Use when users need to "test GTM tracking", "validate dataLayer events", "debug GTM", "check if tracking works", "automated tracking tests", "run tracking tests without opening browser", or troubleshoot tracking issues. Prioritises automated testing over manual when possible.
---

# GTM Testing - Validation & Debugging

Guide users through comprehensive testing of GTM tracking implementation. Prefers automated headless testing over manual steps wherever possible.

## Testing Philosophy

Four-tier validation approach, ordered by automation level:

- **Tier 0 (Automated)**: Playwright headless tests (no browser needed, fully automated)
- **Tier 1 (Manual)**: Browser Console dataLayer verification
- **Tier 2 (Manual)**: GTM Preview Mode tag firing verification
- **Tier 3 (Manual)**: GA4 DebugView end-to-end verification

**Always start with Tier 0** if the user asks "can you do it yourself" or wants automated testing. Fall back to manual tiers only for GTM container and GA4 validation, which require a browser session.

---

## Tier 0: Automated Playwright Testing (Preferred)

Run this tier first. It requires no browser interaction from the user and can be run entirely by Claude.

### Prerequisites Check

```bash
# Check if Playwright is installed
npx playwright --version

# If not installed as a project dependency:
npm install --save-dev playwright
npx playwright install chromium

# Check if dev server is running
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000
# If not running, start it:
# npm run dev
```

### Core Helper: captureDataLayerEvents

This helper intercepts all `dataLayer.push()` calls during an action and returns the captured events. Use it in every test.

```javascript
async function captureDataLayerEvents(page, action) {
  await page.evaluate(() => {
    window.__testEvents = [];
    const original = window.dataLayer.push.bind(window.dataLayer);
    window.dataLayer.push = function (...args) {
      window.__testEvents.push(args[0]);
      return original(...args);
    };
  });

  await action();
  await page.waitForTimeout(300);

  return await page.evaluate(() => window.__testEvents || []);
}
```

### Key Patterns for Common Element Types

**Next.js Link components (navigation, course buttons):**
Do NOT use `page.click()` — it triggers navigation before the onClick handler fires. Use `dispatchEvent` instead:
```javascript
await page.evaluate(() => {
  const btn = document.querySelector('a.js-module_nav');
  if (btn) btn.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
});
await page.waitForTimeout(400);
```

**Outbound links (href to external domains):**
Block the navigation so the page stays loaded while the event fires:
```javascript
await page.route('**github.com**', route => route.abort());
// Then use dispatchEvent as above
```

**Regular buttons and internal actions:**
Standard click works fine:
```javascript
await page.locator('#element-id').click({ force: true });
```

### Test Script Template

Create `scripts/test-tracking.js` in the project root:

```javascript
const { chromium } = require('playwright');

const BASE_URL = 'http://localhost:3000';
const results = { passed: [], failed: [], warnings: [] };

function pass(test, detail = '') {
  results.passed.push({ test, detail });
  console.log(`  PASS  ${test}${detail ? ' - ' + detail : ''}`);
}
function fail(test, detail = '') {
  results.failed.push({ test, detail });
  console.log(`  FAIL  ${test}${detail ? ' - ' + detail : ''}`);
}
function warn(test, detail = '') {
  results.warnings.push({ test, detail });
  console.log(`  WARN  ${test}${detail ? ' - ' + detail : ''}`);
}

async function captureDataLayerEvents(page, action) {
  await page.evaluate(() => {
    window.__testEvents = [];
    const original = window.dataLayer.push.bind(window.dataLayer);
    window.dataLayer.push = function (...args) {
      window.__testEvents.push(args[0]);
      return original(...args);
    };
  });
  await action();
  await page.waitForTimeout(300);
  return await page.evaluate(() => window.__testEvents || []);
}

async function runTests() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();

  console.log('\n=== GTM dataLayer Event Tests ===\n');

  // TEST: dataLayer initialisation
  console.log('Test: dataLayer initialisation');
  {
    const page = await context.newPage();
    await page.goto(BASE_URL, { waitUntil: 'networkidle' });
    const hasDataLayer = await page.evaluate(() => Array.isArray(window.dataLayer));
    hasDataLayer ? pass('dataLayer initialised') : fail('dataLayer not found');
    const gtmEvent = await page.evaluate(() => window.dataLayer.find(e => e['gtm.start']));
    gtmEvent ? pass('GTM bootstrap event present') : fail('GTM bootstrap event missing - container may not be installed');
    await page.close();
  }

  // TEST: cta_click event
  // Adjust selector to match your actual element ID
  console.log('\nTest: cta_click event');
  {
    const page = await context.newPage();
    await page.goto(BASE_URL, { waitUntil: 'networkidle' });
    const events = await captureDataLayerEvents(page, async () => {
      const el = await page.$('#your-cta-id');
      if (el) await page.evaluate(el => el.dispatchEvent(new MouseEvent('click', { bubbles: true })), el);
    });
    const e = events.find(e => e.event === 'cta_click');
    e ? pass('cta_click fired', `location=${e.cta_location}`) : fail('cta_click did not fire');
    await page.close();
  }

  // Add more tests following the same pattern...

  // RESULTS
  await browser.close();
  console.log('\n=== RESULTS ===');
  console.log(`  Passed:   ${results.passed.length}`);
  console.log(`  Failed:   ${results.failed.length}`);
  console.log(`  Warnings: ${results.warnings.length}`);
  if (results.failed.length > 0) {
    console.log('\nFailed:');
    results.failed.forEach(f => console.log(`  - ${f.test}: ${f.detail}`));
  }
  process.exit(results.failed.length > 0 ? 1 : 0);
}

runTests().catch(err => { console.error('Fatal:', err.message); process.exit(1); });
```

### Finding Correct Element Selectors

Before writing tests, always inspect what's actually rendered. Use this discovery script:

```javascript
// Add to test script or run as a separate debug script
const page = await context.newPage();
await page.goto(`${BASE_URL}/your-page`, { waitUntil: 'networkidle' });

const tracked = await page.evaluate(() => {
  return Array.from(document.querySelectorAll('[id], .js-track, [data-track]')).map(el => ({
    id: el.id,
    tag: el.tagName,
    class: el.className,
    text: el.textContent.trim().substring(0, 40),
    href: el.getAttribute('href'),
  }));
});
console.log(JSON.stringify(tracked, null, 2));
```

### Validating GTM Container Configuration via API

Before running browser tests, verify the GTM container itself is correctly configured. This catches orphaned trigger references and missing measurement IDs.

```javascript
// scripts/audit-gtm-coverage.js
// Uses googleapis + gtm-credentials.json + gtm-token.json + gtm-config.json

// Critical checks:
// 1. Base GA4 config tag (googtag) - must fire on Page View trigger
//    If firingTriggerId references a non-existent trigger, NO pages are tracked
// 2. GA4 event tags (gaawe) - must have measurementIdOverride set
//    Parameter key is "measurementIdOverride" NOT "measurementId"
// 3. All triggers must be used by at least one tag
// 4. All tags must have at least one firing trigger
```

**Critical GTM API bug to watch for:** The `gaawe` (GA4 Event) tag type uses `measurementIdOverride` and `eventSettingsTable` (not `measurementId` or `eventParameters`). The correct parameter structure is:

```javascript
// CORRECT structure for gaawe tags via API
{
  type: 'gaawe',
  parameter: [
    { type: 'boolean', key: 'sendEcommerceData', value: 'false' },
    { type: 'template', key: 'eventName', value: 'your_event_name' },
    { type: 'template', key: 'measurementIdOverride', value: 'G-XXXXXXXXXX' },
    {
      type: 'list',
      key: 'eventSettingsTable',
      list: [
        {
          type: 'map',
          map: [
            { type: 'template', key: 'parameter', value: 'param_name' },
            { type: 'template', key: 'parameterValue', value: '{{DL - Variable Name}}' },
          ],
        },
      ],
    },
  ],
}
```

### Running and Interpreting Results

```bash
node scripts/test-tracking.js
```

Exit code `0` = all tests passed. Exit code `1` = failures exist.

**Result types:**
- `PASS` - Event fired with correct parameters
- `FAIL` - Event did not fire, or required element not found
- `WARN` - Component has tracking code but is not rendered on any page yet (not a bug)

**Common failure causes and fixes:**

| Failure | Cause | Fix |
|---------|-------|-----|
| `dataLayer not found` | GTM snippet missing from `<head>` | Add GTM container snippet to layout |
| Event didn't fire | Element uses wrong selector in test | Use discovery script to find real ID/class |
| Event fired but page unloaded | Clicking a Next.js `<Link>` | Use `dispatchEvent` not `page.click()` |
| Outbound click not captured | Page navigated away before capture | Use `page.route()` to block external navigation |
| No events on page load | GTM base tag has orphaned trigger reference | Fix via GTM API or UI - re-assign to Page View trigger |

---

## Tier 1: Browser Console Testing (Manual)

Use when you want to manually verify events while interacting with the site.

### Step 1: Check dataLayer Exists

```javascript
window.dataLayer
// Expected: [...] array
// If undefined: GTM not installed
```

### Step 2: Monitor dataLayer in Real-Time

```javascript
const _push = window.dataLayer.push.bind(window.dataLayer);
window.dataLayer.push = function(...args) {
  console.log('%c dataLayer.push', 'background:#222;color:#0f0;padding:2px 6px', args[0]);
  return _push(...args);
};
// Now every push is logged in green
```

### Step 3: Test Each Event

Click elements one at a time and verify the console output matches expected:

```
Expected for cta_click:
{
  event: "cta_click",
  cta_location: "hero",
  cta_type: "primary",
  cta_text: "Start Course",
  cta_destination: "/claude-code"
}
```

### Validation Checklist - Tier 1

- [ ] `window.dataLayer` is an array
- [ ] GTM bootstrap event (`gtm.start`) present
- [ ] Each event fires with correct `event` name
- [ ] All required parameters present and non-empty
- [ ] No duplicate events on single click
- [ ] No JavaScript errors in console

---

## Tier 2: GTM Preview Mode (Manual)

Confirms the GTM container receives events and fires tags. Requires GTM UI access.

### Setup

1. Go to [tagmanager.google.com](https://tagmanager.google.com)
2. Select container
3. Click **Preview**
4. Enter site URL, click **Connect**
5. A debug panel appears at the bottom of your site

### What to Verify

For each event, the Preview panel should show:

```
Event fired: "cta_click"
  Triggers: CE - CTA Click  [FIRED]
  Tags:      GA4 - CTA Click [FIRED]
```

Click a fired tag to verify:
- `measurementIdOverride` has the correct GA4 ID
- All event parameters are populated (not empty `{{DL - ...}}` strings)

### Validation Checklist - Tier 2

- [ ] Preview mode connects successfully
- [ ] GA4 Configuration tag fires on page load (not orphaned)
- [ ] Each custom event appears in the event list
- [ ] Correct trigger fires for each event
- [ ] Correct tag fires for each trigger
- [ ] Tag parameters show resolved values (not unresolved variable references)
- [ ] No tags firing unexpectedly

---

## Tier 3: GA4 DebugView (Manual)

Confirms events reach GA4 with correct parameters. Requires GA4 property access.

### Enable Debug Mode

Option A - URL parameter: append `?debug_mode=true` to the page URL

Option B - Chrome extension: install **Google Analytics Debugger**, enable it

### Open DebugView

GA4 > Admin > Property > DebugView

Events appear in real time as you interact with the site.

### What to Verify

- Event name appears (e.g., `cta_click`)
- All parameters visible with correct values
- `page_view` event fires on every page navigation
- Event count increments on repeated actions

### Validation Checklist - Tier 3

- [ ] `page_view` events firing on all pages
- [ ] Custom events appear within 1-3 seconds of firing
- [ ] All event parameters visible and correctly valued
- [ ] Events attributed to correct page paths
- [ ] No unexpected events

---

## Common Issues Reference

| Issue | Tier Found | Cause | Fix |
|-------|-----------|-------|-----|
| `dataLayer` undefined | 1 | GTM snippet missing | Add GTM snippet to `<head>` |
| Event fires, trigger doesn't | 2 | Event name mismatch (case-sensitive) | Confirm trigger uses `{{_event}}` equals exact event name |
| Trigger fires, tag doesn't | 2 | Orphaned trigger or misconfigured tag | Check tag has valid firing trigger assigned |
| Page View tag never fires | 2 | Orphaned trigger reference on base tag | Re-assign base tag to a valid Page View trigger |
| Parameters show as `{{DL - X}}` | 2 | Data Layer Variable not created | Create DLV with correct dataLayer key name |
| Events in Preview, not DebugView | 3 | Wrong GA4 property or debug mode off | Verify Measurement ID matches, enable debug mode |
| Parameters missing in GA4 | 3 | Not mapped in tag's eventSettingsTable | Add parameter mapping in GTM tag config |

---

## Full Workflow

```
1. Run Tier 0 (automated)
   PASS → proceed to publish GTM
   FAIL → fix code or GTM config, re-run

2. Run Tier 1 (console) — optional manual spot-check
   PASS → proceed
   FAIL → fix before Tier 2

3. Run Tier 2 (GTM Preview)
   PASS → proceed
   FAIL → fix GTM tags/triggers/variables

4. Run Tier 3 (GA4 DebugView)
   PASS → publish GTM container
   FAIL → fix GA4 config or parameter mappings

5. Publish GTM → GTM UI > Submit > Publish version
6. Disable debug mode in production
7. Monitor GA4 Reports > Engagement > Events
```

---

## References

- `references/debugging-guide.md` - Extended issue diagnosis
- `references/test-checklist.md` - Printable checklist template
- `examples/sample.md` - Example test run output showing PASS/FAIL/WARN format and common failure fixes
- Related skills: `gtm-implementation`, `gtm-analytics-audit`, `gtm-reporting`
