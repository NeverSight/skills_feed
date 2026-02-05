---
name: optimizely-web
description: Optimizely Web (snippet-based) patterns
---

# Optimizely Web

## Overview

This skill covers Optimizely Web (snippet-based) patterns for client-side experimentation.

## Snippet Integration

### Basic Setup

```html
<!-- Add before closing </head> tag -->
<script src="https://cdn.optimizely.com/js/PROJECT_ID.js"></script>
```

### Async Loading (Recommended)

```html
<script async src="https://cdn.optimizely.com/js/PROJECT_ID.js"></script>
```

## Anti-Flicker Handling

### CSS-Based Anti-Flicker

```html
<style>
  /* Hide content until Optimizely activates */
  .optimizely-pending {
    opacity: 0 !important;
  }
</style>
<script>
  document.documentElement.classList.add('optimizely-pending');

  window.optimizely = window.optimizely || [];
  window.optimizely.push({
    type: 'addListener',
    filter: { type: 'lifecycle', name: 'activated' },
    handler: function() {
      document.documentElement.classList.remove('optimizely-pending');
    }
  });

  // Fallback timeout
  setTimeout(function() {
    document.documentElement.classList.remove('optimizely-pending');
  }, 3000);
</script>
```

## Custom JavaScript

### Activate Experiment

```javascript
window.optimizely = window.optimizely || [];
window.optimizely.push(['activate', 'experiment_id']);
```

### Track Event

```javascript
window.optimizely.push({
  type: 'event',
  eventName: 'purchase_completed',
  tags: {
    revenue: 9900,
    currency: 'USD'
  }
});
```

### Get Variation

```javascript
var state = window.optimizely.get('state');
var experimentId = 'EXPERIMENT_ID';
var variationId = state.getVariationMap()[experimentId];
```

### Check Feature Flag

```javascript
var state = window.optimizely.get('state');
var isEnabled = state.getDecisionString({
  campaignId: 'CAMPAIGN_ID',
  experimentId: 'EXPERIMENT_ID'
});
```

## Page Targeting

### URL Targeting Helpers

```javascript
// Custom activation for SPA
window.optimizely.push({
  type: 'activate'
});

// After route change
function onRouteChange(newPath) {
  window.optimizely.push({
    type: 'page',
    pageName: newPath
  });
}
```

## Custom Attributes

### Set Visitor Attributes

```javascript
window.optimizely.push({
  type: 'user',
  attributes: {
    membershipTier: 'premium',
    country: 'US',
    isLoggedIn: true
  }
});
```

## Best Practices

1. **Use async loading** to prevent blocking
2. **Implement anti-flicker** for visual experiments
3. **Track meaningful events** not page views
4. **Use activation listeners** for SPAs
5. **Set visitor attributes** early for targeting
