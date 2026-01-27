---
name: mobile-emulation
description: Mobile device emulation and responsive testing with Playwright. Use when testing mobile layouts, touch interactions, device-specific features, or responsive breakpoints.
version: 1.0.0
tags: [testing, mobile, responsive, emulation, devices, playwright]
---

# Mobile Emulation Testing with Playwright

Test responsive designs and mobile-specific features using Playwright's device emulation capabilities.

## Quick Start

```typescript
import { test, expect, devices } from '@playwright/test';

test.use(devices['iPhone 14']);

test('mobile navigation works', async ({ page }) => {
  await page.goto('/');

  // Mobile menu should be visible
  await page.getByRole('button', { name: 'Menu' }).click();
  await expect(page.getByRole('navigation')).toBeVisible();
});
```

## Configuration

### Project-Based Device Testing

**playwright.config.ts:**
```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  projects: [
    // Desktop browsers
    {
      name: 'Desktop Chrome',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'Desktop Firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'Desktop Safari',
      use: { ...devices['Desktop Safari'] },
    },

    // Mobile devices
    {
      name: 'iPhone 14',
      use: { ...devices['iPhone 14'] },
    },
    {
      name: 'iPhone 14 Pro Max',
      use: { ...devices['iPhone 14 Pro Max'] },
    },
    {
      name: 'Pixel 7',
      use: { ...devices['Pixel 7'] },
    },
    {
      name: 'Galaxy S23',
      use: { ...devices['Galaxy S III'] },  // Closest available
    },

    // Tablets
    {
      name: 'iPad Pro',
      use: { ...devices['iPad Pro 11'] },
    },
    {
      name: 'iPad Mini',
      use: { ...devices['iPad Mini'] },
    },
  ],
});
```

### Custom Device Configuration

```typescript
{
  name: 'Custom Mobile',
  use: {
    viewport: { width: 390, height: 844 },
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)...',
    deviceScaleFactor: 3,
    isMobile: true,
    hasTouch: true,
    defaultBrowserType: 'webkit',
  },
},
```

## Available Devices

### Popular Devices

```typescript
import { devices } from '@playwright/test';

// iPhones
devices['iPhone 14']
devices['iPhone 14 Plus']
devices['iPhone 14 Pro']
devices['iPhone 14 Pro Max']
devices['iPhone 13']
devices['iPhone 12']
devices['iPhone SE']

// Android Phones
devices['Pixel 7']
devices['Pixel 5']
devices['Galaxy S III']
devices['Galaxy S5']
devices['Galaxy Note 3']
devices['Nexus 5']

// Tablets
devices['iPad Pro 11']
devices['iPad Pro 11 landscape']
devices['iPad Mini']
devices['iPad (gen 7)']
devices['Galaxy Tab S4']

// Desktop
devices['Desktop Chrome']
devices['Desktop Firefox']
devices['Desktop Safari']
devices['Desktop Edge']
```

### List All Devices

```typescript
import { devices } from '@playwright/test';

console.log(Object.keys(devices));
// Outputs all available device names
```

## Responsive Breakpoint Testing

### Test Multiple Viewports

```typescript
const breakpoints = [
  { name: 'mobile', width: 375, height: 667 },
  { name: 'tablet', width: 768, height: 1024 },
  { name: 'desktop', width: 1280, height: 720 },
  { name: 'wide', width: 1920, height: 1080 },
];

for (const bp of breakpoints) {
  test(`layout at ${bp.name}`, async ({ page }) => {
    await page.setViewportSize({ width: bp.width, height: bp.height });
    await page.goto('/');
    await expect(page).toHaveScreenshot(`layout-${bp.name}.png`);
  });
}
```

### Dynamic Viewport Changes

```typescript
test('responsive navigation', async ({ page }) => {
  await page.goto('/');

  // Desktop - horizontal nav
  await page.setViewportSize({ width: 1280, height: 720 });
  await expect(page.locator('.desktop-nav')).toBeVisible();
  await expect(page.locator('.mobile-menu-button')).not.toBeVisible();

  // Tablet - may show hamburger
  await page.setViewportSize({ width: 768, height: 1024 });

  // Mobile - hamburger menu
  await page.setViewportSize({ width: 375, height: 667 });
  await expect(page.locator('.desktop-nav')).not.toBeVisible();
  await expect(page.locator('.mobile-menu-button')).toBeVisible();
});
```

## Touch Interactions

### Tap

```typescript
test('tap interaction', async ({ page }) => {
  await page.goto('/');

  // Tap is equivalent to click on touch devices
  await page.getByRole('button').tap();
});
```

### Swipe

```typescript
test('swipe carousel', async ({ page }) => {
  await page.goto('/gallery');

  const carousel = page.locator('.carousel');
  const box = await carousel.boundingBox();

  if (box) {
    // Swipe left
    await page.mouse.move(box.x + box.width - 50, box.y + box.height / 2);
    await page.mouse.down();
    await page.mouse.move(box.x + 50, box.y + box.height / 2, { steps: 10 });
    await page.mouse.up();
  }

  await expect(page.locator('.slide-2')).toBeVisible();
});
```

### Pinch to Zoom

```typescript
test('pinch to zoom map', async ({ page }) => {
  await page.goto('/map');

  const map = page.locator('#map');
  const box = await map.boundingBox();

  if (box) {
    const centerX = box.x + box.width / 2;
    const centerY = box.y + box.height / 2;

    // Simulate pinch out (zoom in)
    await page.touchscreen.tap(centerX, centerY);
    // Note: Multi-touch pinch requires custom implementation
  }
});
```

### Long Press

```typescript
test('long press context menu', async ({ page }) => {
  await page.goto('/');

  const element = page.locator('.long-press-target');
  const box = await element.boundingBox();

  if (box) {
    await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
    await page.mouse.down();
    await page.waitForTimeout(1000);  // Hold for 1 second
    await page.mouse.up();
  }

  await expect(page.locator('.context-menu')).toBeVisible();
});
```

## Orientation Testing

### Portrait vs Landscape

```typescript
test('orientation change', async ({ page }) => {
  // Portrait
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/video');
  await expect(page.locator('.video-container')).toHaveCSS('width', '390px');

  // Landscape
  await page.setViewportSize({ width: 844, height: 390 });
  await expect(page.locator('.video-container')).toHaveCSS('width', '844px');
});
```

### Using Device Landscape Variants

```typescript
test.use(devices['iPad Pro 11 landscape']);

test('tablet landscape layout', async ({ page }) => {
  await page.goto('/dashboard');

  // Sidebar should be visible in landscape
  await expect(page.locator('.sidebar')).toBeVisible();
});
```

## Geolocation Testing

```typescript
test.use({
  geolocation: { latitude: 40.7128, longitude: -74.0060 },  // NYC
  permissions: ['geolocation'],
});

test('shows nearby locations', async ({ page }) => {
  await page.goto('/locations');

  await page.getByRole('button', { name: 'Find Nearby' }).click();

  await expect(page.getByText('New York')).toBeVisible();
});
```

### Change Location During Test

```typescript
test('location change', async ({ page, context }) => {
  await context.setGeolocation({ latitude: 51.5074, longitude: -0.1278 });  // London
  await page.goto('/weather');
  await expect(page.getByText('London')).toBeVisible();

  await context.setGeolocation({ latitude: 35.6762, longitude: 139.6503 });  // Tokyo
  await page.reload();
  await expect(page.getByText('Tokyo')).toBeVisible();
});
```

## Network Conditions

### Slow 3G

```typescript
test('works on slow network', async ({ page, context }) => {
  // Emulate slow 3G
  const client = await context.newCDPSession(page);
  await client.send('Network.emulateNetworkConditions', {
    offline: false,
    downloadThroughput: (500 * 1024) / 8,  // 500kb/s
    uploadThroughput: (500 * 1024) / 8,
    latency: 400,  // 400ms
  });

  await page.goto('/');

  // Should show skeleton loaders
  await expect(page.locator('.skeleton')).toBeVisible();

  // Eventually loads
  await expect(page.locator('.content')).toBeVisible({ timeout: 30000 });
});
```

### Offline Mode

```typescript
test('offline functionality', async ({ page, context }) => {
  await page.goto('/');

  // Cache page, then go offline
  await context.setOffline(true);

  await page.reload();

  // Should show offline message or cached content
  await expect(page.getByText(/offline/i)).toBeVisible();
});
```

## Device-Specific Features

### Notch/Safe Areas

```typescript
test('respects safe areas', async ({ page }) => {
  // iPhone with notch
  test.use(devices['iPhone 14 Pro']);

  await page.goto('/');

  // Header should account for notch
  const header = page.locator('header');
  const paddingTop = await header.evaluate(el =>
    window.getComputedStyle(el).paddingTop
  );

  // Should have safe area inset
  expect(parseInt(paddingTop)).toBeGreaterThan(20);
});
```

### Dark Mode

```typescript
test.use({
  colorScheme: 'dark',
});

test('dark mode styling', async ({ page }) => {
  await page.goto('/');

  const body = page.locator('body');
  const bgColor = await body.evaluate(el =>
    window.getComputedStyle(el).backgroundColor
  );

  // Should have dark background
  expect(bgColor).toBe('rgb(0, 0, 0)');  // or dark color
});
```

### Reduced Motion

```typescript
test.use({
  reducedMotion: 'reduce',
});

test('respects reduced motion', async ({ page }) => {
  await page.goto('/');

  const animated = page.locator('.animated-element');
  const animationDuration = await animated.evaluate(el =>
    window.getComputedStyle(el).animationDuration
  );

  // Should have no animation
  expect(animationDuration).toBe('0s');
});
```

## Visual Regression Across Devices

```typescript
const testDevices = [
  'iPhone 14',
  'Pixel 7',
  'iPad Pro 11',
  'Desktop Chrome',
];

for (const deviceName of testDevices) {
  test.describe(`Visual: ${deviceName}`, () => {
    test.use(devices[deviceName]);

    test('homepage', async ({ page }) => {
      await page.goto('/');
      await expect(page).toHaveScreenshot(`homepage-${deviceName}.png`);
    });

    test('product page', async ({ page }) => {
      await page.goto('/products/1');
      await expect(page).toHaveScreenshot(`product-${deviceName}.png`);
    });
  });
}
```

## Best Practices

1. **Test real devices too** - Emulation is good but not perfect
2. **Cover major breakpoints** - 375px, 768px, 1024px, 1280px minimum
3. **Test both orientations** - Portrait and landscape
4. **Test touch vs click** - Some interactions differ
5. **Test slow networks** - Mobile users often have poor connectivity
6. **Test safe areas** - Account for notches, home indicators

## References

- `references/device-list.md` - Complete device list with specs
- `references/touch-patterns.md` - Touch gesture implementations
