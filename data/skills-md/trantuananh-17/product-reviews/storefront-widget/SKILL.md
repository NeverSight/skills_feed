---
name: storefront-widget
description: Use this skill when the user asks about "storefront widget", "scripttag", "customer-facing", "Preact", "bundle size", "lazy loading", "performance optimization", or any storefront frontend work. Provides Preact patterns for lightweight storefront widgets.
---

# Scripttag Development (Storefront Widget)

## Overview

The scripttag package contains **customer-facing storefront widgets** injected into merchant stores. Performance is **CRITICAL** - every KB and millisecond impacts merchant store speed and conversion rates.

---

## Architecture

### Tech Stack

| Technology | Purpose | Why |
|------------|---------|-----|
| **Preact** | UI library | 3KB vs React's 40KB+ |
| **preact-lazy** | Lazy loading | Lightweight lazy loader |
| **SCSS** | Styling | Scoped styles, minimal footprint |
| **Rspack** | Bundler | 10x faster than webpack |

> **Styling:** Always use custom SCSS/CSS. Avoid UI libraries - they add unnecessary bundle size.

---

## Directory Structure

```
packages/scripttag/
├── src/                      # Main widget entry
│   ├── index.js              # Main entry point
│   ├── loader.js             # Minimal loader script
│   ├── components/           # Shared components
│   ├── managers/             # API, Display managers
│   ├── helpers/              # Utility functions
│   └── styles/               # Global styles
├── [feature-name]/           # Feature-specific modules
│   ├── index.js              # Feature entry point
│   ├── components/           # Feature components
│   └── helpers/              # Feature helpers
└── rspack.config.js          # Build configuration
```

---

## Performance Rules (CRITICAL)

### 1. Minimal Loader Pattern

```javascript
// loader.js - Keep as small as possible (~2KB)
function loadScript() {
  const script = document.createElement('script');
  script.async = true;
  script.src = `${CDN_URL}/main.min.js`;
  document.head.appendChild(script);
}

// Load after page ready (non-blocking)
if (document.readyState === 'complete') {
  setTimeout(loadScript, 1);
} else {
  window.addEventListener('load', loadScript, false);
}
```

### 2. Lazy Loading Components

```javascript
import lazy from 'preact-lazy';

const HeavyComponent = lazy(() => import('./HeavyComponent'));
```

### 3. Tree Shaking

```javascript
// BAD: Import entire library
import * as utils from '@avada/utils';

// GOOD: Import only what you need
import {isEmpty} from '@avada/utils/lib/isEmpty';

// BAD: Barrel imports
import {formatDate, formatCurrency} from '../helpers';

// GOOD: Direct path imports
import formatDate from '../helpers/formatDate';
import formatCurrency from '../helpers/formatCurrency';
```

### 4. Bundle Size Limits

| Component | Target Size |
|-----------|-------------|
| Loader script | < 3KB gzipped |
| Main bundle | < 50KB gzipped |
| Feature chunk | < 30KB gzipped |
| Initial load total | < 60KB gzipped |

---

## Preact Patterns

### Use Preact Instead of React

```javascript
// Use preact directly
import {render} from 'preact';
import {useState, useEffect} from 'preact/hooks';

// Rspack aliases handle React compat:
// 'react' -> 'preact/compat'
// 'react-dom' -> 'preact/compat'
```

### Functional Components with Hooks

```javascript
import {useState, useEffect, useMemo, useCallback} from 'preact/hooks';

function Widget() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchData().then(setData);
  }, []);

  return data ? <Display data={data} /> : null;
}
```

---

## Styling (Recommended Approach)

### Custom SCSS (Preferred)

```scss
// Lightweight custom styles with BEM
.widget {
  &__button {
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    background: var(--primary-color);
    color: white;
    cursor: pointer;

    &:hover {
      opacity: 0.9;
    }

    &--secondary {
      background: transparent;
      border: 1px solid var(--primary-color);
      color: var(--primary-color);
    }
  }
}
```

### CSS Variables for Theming

```scss
:root {
  --primary-color: #{$primaryColor};
  --text-color: #{$textColor};
  --bg-color: #{$backgroundColor};
}

.card {
  background: var(--bg-color);
  color: var(--text-color);
}
```

---

## Window Data Pattern

Storefront widgets receive data via global window object:

```javascript
const {
  shop,           // Shop configuration
  customer,       // Current customer data
  settings,       // Widget settings
  translation,    // i18n translations
} = window.APP_DATA || {};

// Always destructure with defaults
const {items = [], config = {}} = settings || {};
```

---

## Development Commands

```bash
# Development with watch
npm run watch

# Production build
npm run build

# Analyze bundle size
npm run build:analyze

# Development build (unminified)
npm run build:dev
```

---

## Checklist

### Before Commit

```
- No barrel imports (use direct paths)
- Heavy components lazy loaded
- Dynamic imports for conditional features
- Tree-shaking friendly imports
- No console.log in production
- Custom SCSS with BEM naming
- No UI library dependencies
```

### Bundle Size Check

```
- Run build:analyze
- Loader < 3KB gzipped
- No unexpected large chunks
- No duplicate dependencies
- All imports use direct paths
```

### Performance

```
- Loads after document ready
- Non-blocking script loading
- Retry logic with backoff
- Performance tracking in place
- No synchronous heavy operations
```