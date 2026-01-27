---
name: performance-testing
description: Performance testing with Lighthouse and Web Vitals integration in Playwright. Use when measuring page load times, Core Web Vitals, Lighthouse audits, or performance budgets.
version: 1.0.0
tags: [testing, performance, lighthouse, web-vitals, metrics, playwright]
---

# Performance Testing with Lighthouse & Web Vitals

Measure and enforce performance standards using Lighthouse audits and Core Web Vitals within Playwright tests.

## Quick Start

```typescript
import { test, expect } from '@playwright/test';
import { playAudit } from 'playwright-lighthouse';

test('homepage meets performance budget', async ({ page }) => {
  await page.goto('/');

  const audit = await playAudit({
    page,
    thresholds: {
      performance: 90,
      accessibility: 90,
      'best-practices': 90,
      seo: 90,
    },
  });

  expect(audit.lhr.categories.performance.score * 100).toBeGreaterThanOrEqual(90);
});
```

## Installation

```bash
npm install -D playwright-lighthouse lighthouse
```

## Lighthouse Integration

### Basic Audit

```typescript
import { test, expect } from '@playwright/test';
import { playAudit } from 'playwright-lighthouse';

test('run lighthouse audit', async ({ page }) => {
  await page.goto('/');

  const audit = await playAudit({
    page,
    port: 9222,  // Chrome debug port
  });

  console.log('Performance:', audit.lhr.categories.performance.score * 100);
  console.log('Accessibility:', audit.lhr.categories.accessibility.score * 100);
  console.log('Best Practices:', audit.lhr.categories['best-practices'].score * 100);
  console.log('SEO:', audit.lhr.categories.seo.score * 100);
});
```

### With Thresholds

```typescript
test('enforce performance budgets', async ({ page }) => {
  await page.goto('/');

  const audit = await playAudit({
    page,
    thresholds: {
      performance: 85,
      accessibility: 90,
      'best-practices': 85,
      seo: 80,
    },
  });

  // Test fails if any threshold is not met
});
```

### Mobile vs Desktop

```typescript
test('mobile performance', async ({ page }) => {
  await page.goto('/');

  const audit = await playAudit({
    page,
    config: {
      extends: 'lighthouse:default',
      settings: {
        formFactor: 'mobile',
        throttling: {
          rttMs: 150,
          throughputKbps: 1638.4,
          cpuSlowdownMultiplier: 4,
        },
        screenEmulation: {
          mobile: true,
          width: 375,
          height: 667,
          deviceScaleFactor: 2,
        },
      },
    },
  });
});

test('desktop performance', async ({ page }) => {
  await page.goto('/');

  const audit = await playAudit({
    page,
    config: {
      extends: 'lighthouse:default',
      settings: {
        formFactor: 'desktop',
        throttling: {
          rttMs: 40,
          throughputKbps: 10240,
          cpuSlowdownMultiplier: 1,
        },
        screenEmulation: {
          mobile: false,
          width: 1350,
          height: 940,
          deviceScaleFactor: 1,
        },
      },
    },
  });
});
```

## Core Web Vitals

### Measure Web Vitals

```typescript
import { test, expect } from '@playwright/test';

test('measure Core Web Vitals', async ({ page }) => {
  // Inject web-vitals library
  await page.addInitScript(() => {
    window.webVitals = {
      LCP: null,
      FID: null,
      CLS: null,
      FCP: null,
      TTFB: null,
    };
  });

  await page.goto('/');

  // Wait for metrics to be collected
  await page.waitForTimeout(3000);

  // Get LCP
  const lcp = await page.evaluate(() => {
    return new Promise(resolve => {
      new PerformanceObserver((list) => {
        const entries = list.getEntries();
        resolve(entries[entries.length - 1].startTime);
      }).observe({ type: 'largest-contentful-paint', buffered: true });
    });
  });

  // Get CLS
  const cls = await page.evaluate(() => {
    return new Promise(resolve => {
      let clsValue = 0;
      new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (!entry.hadRecentInput) {
            clsValue += entry.value;
          }
        }
        resolve(clsValue);
      }).observe({ type: 'layout-shift', buffered: true });
      setTimeout(() => resolve(clsValue), 1000);
    });
  });

  console.log('LCP:', lcp, 'ms');
  console.log('CLS:', cls);

  // Assert thresholds
  expect(lcp).toBeLessThan(2500);  // Good LCP < 2.5s
  expect(cls).toBeLessThan(0.1);   // Good CLS < 0.1
});
```

### Web Vitals Library Integration

```typescript
test('web vitals with library', async ({ page }) => {
  await page.addInitScript({
    content: `
      import { onLCP, onFID, onCLS, onFCP, onTTFB } from 'web-vitals';

      window.webVitalsResults = {};

      onLCP(metric => window.webVitalsResults.LCP = metric.value);
      onFID(metric => window.webVitalsResults.FID = metric.value);
      onCLS(metric => window.webVitalsResults.CLS = metric.value);
      onFCP(metric => window.webVitalsResults.FCP = metric.value);
      onTTFB(metric => window.webVitalsResults.TTFB = metric.value);
    `
  });

  await page.goto('/');

  // Interact to trigger FID
  await page.click('body');
  await page.waitForTimeout(2000);

  const vitals = await page.evaluate(() => window.webVitalsResults);

  console.log('Web Vitals:', vitals);
});
```

## Performance Timing API

### Navigation Timing

```typescript
test('page load timing', async ({ page }) => {
  await page.goto('/');

  const timing = await page.evaluate(() => {
    const perf = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
    return {
      dns: perf.domainLookupEnd - perf.domainLookupStart,
      tcp: perf.connectEnd - perf.connectStart,
      ttfb: perf.responseStart - perf.requestStart,
      download: perf.responseEnd - perf.responseStart,
      domInteractive: perf.domInteractive - perf.fetchStart,
      domComplete: perf.domComplete - perf.fetchStart,
      loadComplete: perf.loadEventEnd - perf.fetchStart,
    };
  });

  console.log('Performance Timing:', timing);

  expect(timing.ttfb).toBeLessThan(600);
  expect(timing.domInteractive).toBeLessThan(3000);
  expect(timing.loadComplete).toBeLessThan(5000);
});
```

### Resource Timing

```typescript
test('resource loading', async ({ page }) => {
  await page.goto('/');

  const resources = await page.evaluate(() => {
    return performance.getEntriesByType('resource').map(r => ({
      name: r.name,
      type: (r as PerformanceResourceTiming).initiatorType,
      duration: r.duration,
      size: (r as PerformanceResourceTiming).transferSize,
    }));
  });

  // Find slow resources
  const slowResources = resources.filter(r => r.duration > 1000);
  console.log('Slow resources:', slowResources);

  // Find large resources
  const largeResources = resources.filter(r => r.size > 100000);
  console.log('Large resources:', largeResources);
});
```

## Performance Budgets

### Define Budgets

```typescript
const performanceBudgets = {
  // Page load
  ttfb: 600,           // Time to first byte < 600ms
  fcp: 1800,           // First contentful paint < 1.8s
  lcp: 2500,           // Largest contentful paint < 2.5s
  tti: 3800,           // Time to interactive < 3.8s

  // Interactivity
  fid: 100,            // First input delay < 100ms
  cls: 0.1,            // Cumulative layout shift < 0.1

  // Resources
  totalSize: 1000000,  // Total page size < 1MB
  jsSize: 300000,      // JavaScript < 300KB
  cssSize: 100000,     // CSS < 100KB
  imageSize: 500000,   // Images < 500KB

  // Requests
  totalRequests: 50,   // Total requests < 50
  jsRequests: 10,      // JS files < 10
};

test('check performance budgets', async ({ page }) => {
  await page.goto('/');

  // Get resource sizes
  const resources = await page.evaluate(() => {
    const entries = performance.getEntriesByType('resource') as PerformanceResourceTiming[];
    return {
      total: entries.reduce((sum, r) => sum + r.transferSize, 0),
      js: entries.filter(r => r.name.endsWith('.js')).reduce((sum, r) => sum + r.transferSize, 0),
      css: entries.filter(r => r.name.endsWith('.css')).reduce((sum, r) => sum + r.transferSize, 0),
      images: entries.filter(r => r.initiatorType === 'img').reduce((sum, r) => sum + r.transferSize, 0),
      requests: entries.length,
    };
  });

  expect(resources.total).toBeLessThan(performanceBudgets.totalSize);
  expect(resources.js).toBeLessThan(performanceBudgets.jsSize);
  expect(resources.requests).toBeLessThan(performanceBudgets.totalRequests);
});
```

## Network Throttling

### Simulate Slow Connections

```typescript
test('performance on 3G', async ({ page, context }) => {
  const client = await context.newCDPSession(page);

  // Simulate slow 3G
  await client.send('Network.emulateNetworkConditions', {
    offline: false,
    downloadThroughput: (400 * 1024) / 8,  // 400 Kbps
    uploadThroughput: (400 * 1024) / 8,
    latency: 400,
  });

  const startTime = Date.now();
  await page.goto('/');
  const loadTime = Date.now() - startTime;

  console.log('Load time on 3G:', loadTime, 'ms');

  // Should still be usable on slow connections
  expect(loadTime).toBeLessThan(10000);
});
```

### CPU Throttling

```typescript
test('performance on slow CPU', async ({ page, context }) => {
  const client = await context.newCDPSession(page);

  // 4x CPU slowdown
  await client.send('Emulation.setCPUThrottlingRate', { rate: 4 });

  await page.goto('/');

  // Measure interaction responsiveness
  const startTime = Date.now();
  await page.click('.interactive-element');
  await page.waitForSelector('.result');
  const responseTime = Date.now() - startTime;

  expect(responseTime).toBeLessThan(500);
});
```

## Reporting

### Generate HTML Report

```typescript
import { playAudit } from 'playwright-lighthouse';
import fs from 'fs';

test('generate performance report', async ({ page }) => {
  await page.goto('/');

  const audit = await playAudit({
    page,
    thresholds: { performance: 80 },
  });

  // Save HTML report
  fs.writeFileSync(
    'lighthouse-report.html',
    audit.report
  );

  // Save JSON for further analysis
  fs.writeFileSync(
    'lighthouse-report.json',
    JSON.stringify(audit.lhr, null, 2)
  );
});
```

### Track Metrics Over Time

```typescript
interface PerformanceMetrics {
  date: string;
  url: string;
  lcp: number;
  fcp: number;
  cls: number;
  performance: number;
}

test('track performance metrics', async ({ page }) => {
  await page.goto('/');

  const audit = await playAudit({ page });

  const metrics: PerformanceMetrics = {
    date: new Date().toISOString(),
    url: page.url(),
    lcp: audit.lhr.audits['largest-contentful-paint'].numericValue,
    fcp: audit.lhr.audits['first-contentful-paint'].numericValue,
    cls: audit.lhr.audits['cumulative-layout-shift'].numericValue,
    performance: audit.lhr.categories.performance.score * 100,
  };

  // Append to metrics file
  const metricsFile = 'performance-history.json';
  const history = fs.existsSync(metricsFile)
    ? JSON.parse(fs.readFileSync(metricsFile, 'utf8'))
    : [];

  history.push(metrics);
  fs.writeFileSync(metricsFile, JSON.stringify(history, null, 2));
});
```

## CI Integration

### GitHub Actions

```yaml
name: Performance Tests

on: [push, pull_request]

jobs:
  performance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright
        run: npx playwright install --with-deps chromium

      - name: Start app
        run: npm run start &

      - name: Wait for app
        run: npx wait-on http://localhost:3000

      - name: Run performance tests
        run: npx playwright test --grep @performance

      - name: Upload Lighthouse report
        uses: actions/upload-artifact@v4
        with:
          name: lighthouse-report
          path: lighthouse-report.html
```

## Best Practices

1. **Test on realistic conditions** - Use network/CPU throttling
2. **Test multiple pages** - Home, product, checkout, etc.
3. **Track over time** - Compare against baselines
4. **Set budgets early** - Prevent regression
5. **Test mobile performance** - Often worse than desktop
6. **Cache and repeat** - Run multiple times for consistency

## References

- `references/web-vitals-guide.md` - Understanding Core Web Vitals
- `references/lighthouse-config.md` - Custom Lighthouse configurations
