---
name: shopify-built-for-shopify
description: Enforces Built for Shopify (BFS) quality standards during Shopify app development. Use when building, reviewing, or auditing Shopify apps for BFS compliance, or when the user mentions Built for Shopify, BFS, app quality, or app store requirements.
---

# Built for Shopify Guidelines

This skill enforces Shopify's Built for Shopify (BFS) quality standards during development to ensure apps meet the highest quality bar for the Shopify App Store.

Reference: https://shopify.dev/docs/apps/launch/built-for-shopify/requirements

## Quick Compliance Checklist

Use this checklist when reviewing code or building features:

```
BFS Compliance Review:
- [ ] App is embedded in Shopify admin (App Bridge)
- [ ] Uses session token authentication
- [ ] Primary workflows stay within Shopify admin
- [ ] No additional login/signup required
- [ ] Uses theme app extensions (not Asset API for writes)
- [ ] Meets Web Vitals targets (LCP ≤2.5s, CLS ≤0.1, INP ≤200ms)
- [ ] Uses Polaris components matching admin styling
- [ ] Mobile responsive design
- [ ] Uses nav menu (s-app-nav) and contextual save bar
- [ ] Error messages are red, contextual, and helpful
- [ ] No dark patterns or pressure tactics
- [ ] Premium features are disabled and labeled
- [ ] Promotional content is dismissible
```

## 1. Integration Requirements

### Embedding (MANDATORY)

Apps MUST be embedded in the Shopify admin:

```html
<!-- Add to <head> of every document -->
<script src="https://cdn.shopify.com/shopifycloud/app-bridge.js"></script>
```

```typescript
// Use session token authentication
import { authenticate } from "@shopify/shopify-app-remix/server";

export async function loader({ request }) {
  const { session } = await authenticate.admin(request);
  // ...
}
```

### Primary Workflows

All primary app workflows MUST be completable within the Shopify admin:
- No external website required for core functionality
- Third-party connection settings must be accessible in-app
- Simplified monitoring/reporting on app homepage

### Clean Installation

For storefront apps, use theme app extensions instead of Asset API:

```liquid
<!-- extensions/theme-extension/blocks/my-block.liquid -->
{% schema %}
{
  "name": "My App Block",
  "target": "section",
  "settings": []
}
{% endschema %}
```

**Do NOT** use Asset API to create, modify, or delete theme files (reading is allowed).

## 2. Performance Requirements

### Web Vitals Targets (75th percentile)

| Metric | Target | Description |
|--------|--------|-------------|
| LCP | ≤ 2.5s | Largest Contentful Paint |
| CLS | ≤ 0.1 | Cumulative Layout Shift |
| INP | ≤ 200ms | Interaction to Next Paint |

### Optimization Strategies

```typescript
// Lazy load heavy components
const HeavyChart = lazy(() => import('./HeavyChart'));

// Use React.memo for expensive renders
const ExpensiveList = memo(({ items }) => (
  // ...
));

// Avoid layout shifts with skeleton loaders
<Suspense fallback={<SkeletonPage />}>
  <AppContent />
</Suspense>
```

### Storefront Performance

- Must not reduce Lighthouse score by more than 10 points
- Checkout requests: p95 ≤ 500ms, failure rate ≤ 0.1%

## 3. Design Requirements

### Familiar (Match Shopify Admin)

Use Polaris web components to match admin styling:

```html
<!-- Use s-page for page structure -->
<s-page>
  <s-title-bar title="My Page">
    <s-button slot="primary-action">Save</s-button>
  </s-title-bar>
  
  <s-layout>
    <s-layout-section>
      <s-card>
        <s-text>Content in cards</s-text>
      </s-card>
    </s-layout-section>
  </s-layout>
</s-page>
```

**Rejection reasons to avoid:**
- Custom button colors (use Polaris defaults)
- Serif/script fonts
- Non-standard background colors
- Content not in card containers
- Poor contrast (must meet WCAG 2.1 AA)

### Navigation

Use App Bridge nav menu:

```html
<s-app-nav>
  <s-nav-item href="/dashboard" selected>Dashboard</s-nav-item>
  <s-nav-item href="/settings">Settings</s-nav-item>
</s-app-nav>
```

**Do NOT:**
- Create custom navigation menus
- Use emojis in nav items
- Have separate "Home" link (app name should link to home)

### Contextual Save Bar

Use for all form inputs:

```typescript
import { useAppBridge } from "@shopify/app-bridge-react";
import { SaveBar } from "@shopify/app-bridge/actions";

function SettingsForm() {
  const app = useAppBridge();
  
  const showSaveBar = () => {
    const saveBar = SaveBar.create(app, {
      saveAction: { disabled: false, loading: false },
      discardAction: { disabled: false, loading: false },
    });
    saveBar.dispatch(SaveBar.Action.SHOW);
  };
  // ...
}
```

### Modals

Use s-modal with proper slots:

```html
<s-modal heading="Confirm Action">
  <p>Modal content here</p>
  <s-button slot="secondary-action">Cancel</s-button>
  <s-button slot="primary-action" variant="primary">Confirm</s-button>
</s-modal>
```

### Mobile Responsiveness

- No horizontal scrolling on mobile
- Content must wrap/stack appropriately
- All content accessible (no hidden without expand mechanism)

## 4. Helpful UX Requirements

### Onboarding

- Concise, guiding merchants to completion
- Dismissible after completion
- No requirement to install additional apps
- Justify any merchant information requests

### Homepage

Must include:
- Theme block/embed status (if applicable)
- Relevant metrics/analytics
- Dynamic content (not just static links)

### Error Messages

```html
<!-- CORRECT: Red, contextual, persistent -->
<s-text-field 
  label="Email"
  error="Please enter a valid email address"
/>

<!-- WRONG: Using toast for errors -->
<!-- WRONG: Non-red error colors -->
<!-- WRONG: Top-of-page errors for field issues -->
```

## 5. User-Friendly Requirements (No Dark Patterns)

### Prohibited Practices

| Don't | Why |
|-------|-----|
| Countdown timers for upgrades | Pressures merchants |
| "No thanks, I prefer less sales" | Guilt/shame language |
| Auto-appearing modals/popovers | Distracts merchants |
| Guarantee outcomes ("increase sales 18%") | False claims |
| Review incentives ("5-star for Pro") | Manipulative |
| Non-dismissible promotions | Overwhelms merchants |
| Shopify-like icons/colors | Impersonation |

### Premium Features

```html
<!-- Features must be visually AND functionally disabled -->
<s-card>
  <s-text variant="headingMd">Advanced Analytics</s-text>
  <s-badge tone="info">Pro Plan</s-badge>
  <s-button disabled>View Analytics</s-button>
  <s-link url="/upgrade">Upgrade to unlock</s-link>
</s-card>
```

- Shopify Plus-only features must be hidden (not just disabled) for non-Plus merchants

## 6. Category-Specific Requirements

### If Building: Ads/Analytics/Affiliate Apps

```typescript
// MUST use Web Pixel extensions, NOT script tags
// extensions/web-pixel/src/index.ts
import { register } from "@shopify/web-pixels-extension";

register(({ analytics }) => {
  analytics.subscribe("page_viewed", (event) => {
    // Track event
  });
});
```

### If Building: Email/SMS Marketing Apps

- Sync customer data to/from Shopify
- Use Shopify segments via customer segment action extension
- Use visitors API for identifying store visitors

### If Building: Discount Apps

```graphql
# Use discount functions or native APIs
# Do NOT use draft orders for custom discounts
# Use discountRedeemCodeBulkAdd for multiple codes

mutation {
  discountRedeemCodeBulkAdd(
    discountId: "gid://shopify/DiscountCodeNode/123"
    codes: [{ code: "CODE1" }, { code: "CODE2" }]
  ) {
    bulkCreation {
      id
    }
  }
}
```

### If Building: Subscription Apps

- Use Selling Plan API, Subscription Contract API, Customer Payment Method API
- Use theme app blocks for product pages
- Display subscription info clearly (name, price, savings)
- Use Customer Account UI extensions for subscription management

### If Building: Fulfillment Apps

- Wait for merchant fulfillment requests before fulfilling
- Respond to fulfillment requests within 4 hours
- Respond to cancellation requests within 1 hour
- Add tracking info within 1 hour of fulfillment creation
- 99% completion rate, 99.9% callback success rate

### If Building: Returns Apps

Sync all return lifecycle events:
- returnCreate, reverseDeliveryCreateWithShipping
- reverseFulfillmentOrderDispose, returnLineItemRemoveFromReturn
- returnCancel, returnClose, refundCreate

## Code Review Checklist

When reviewing Shopify app code for BFS compliance:

```
Technical:
- [ ] App Bridge script in <head>
- [ ] Session token auth (no cookie auth)
- [ ] Theme app extensions (no Asset API writes)
- [ ] Web Pixel extensions (no script tags for tracking)
- [ ] Proper API usage for app category

UI/UX:
- [ ] Polaris components throughout
- [ ] s-app-nav for navigation
- [ ] Contextual save bar for forms
- [ ] s-modal with proper slots
- [ ] Responsive design
- [ ] WCAG 2.1 AA contrast

Content:
- [ ] No outcome guarantees
- [ ] No pressure tactics
- [ ] Dismissible promotional content
- [ ] Disabled + labeled premium features
- [ ] Clear error messages (red, contextual)
- [ ] Helpful onboarding
- [ ] Dynamic homepage content
```

## Resources

- [BFS Requirements](https://shopify.dev/docs/apps/launch/built-for-shopify/requirements)
- [App Bridge](https://shopify.dev/docs/api/app-bridge)
- [Polaris Web Components](https://shopify.dev/docs/api/app-home/polaris-web-components)
- [Theme App Extensions](https://shopify.dev/docs/apps/build/online-store/theme-app-extensions)
- [Web Pixels](https://shopify.dev/docs/apps/build/marketing-analytics/build-web-pixels)
