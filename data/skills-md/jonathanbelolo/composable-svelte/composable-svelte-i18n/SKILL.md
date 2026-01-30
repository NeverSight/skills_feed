---
name: composable-svelte-i18n
description: Internationalization (i18n) system for Composable Svelte. Use when implementing multi-language support, translations, date/number formatting, locale detection, or localizing applications. Covers translation loading, ICU MessageFormat, formatters (dates/numbers/currency), locale detection, SSR integration, and the i18n reducer.
---

# Composable Svelte Internationalization (i18n)

Complete i18n solution integrated with the Composable Architecture. Handles translations, formatting (dates, numbers, currency), locale detection, and works seamlessly with SSR/SSG.

---

## CRITICAL RULES

### Rule 1: i18n State Lives in Store

**Principle**: i18n state is part of your application state, integrated via the i18n reducer.

#### ✅ CORRECT - i18n in Store State
```typescript
import { createInitialI18nState, i18nReducer } from '@composable-svelte/core/i18n';

interface AppState {
  todos: Todo[];
  i18n: I18nState;  // ✅ i18n integrated with app state
}

type AppAction =
  | { type: 'addTodo'; text: string }
  | I18nAction;  // ✅ i18n actions part of app actions

const appReducer: Reducer<AppState, AppAction> = (state, action, deps) => {
  // Handle i18n actions
  if (typeof action.type === 'string' && action.type.startsWith('i18n/')) {
    const [newI18nState, i18nEffect] = i18nReducer(state.i18n, action as any, deps);
    return [
      { ...state, i18n: newI18nState },
      i18nEffect as Effect<AppAction>
    ];
  }

  // Handle other actions...
  return [state, Effect.none()];
};
```

#### ❌ WRONG - Separate i18n Store
```typescript
// ❌ Don't create a separate store for i18n
const i18nStore = createStore({
  initialState: i18nState,
  reducer: i18nReducer
});

const appStore = createStore({
  initialState: appState,
  reducer: appReducer
});
```

**WHY**: Single source of truth. i18n changes should flow through the same reducer pipeline as other state changes.

---

### Rule 2: Use Framework Formatters, Not Manual Formatting

**Principle**: The framework provides locale-aware formatters. Never manually format dates, numbers, or currency.

#### ✅ CORRECT - Framework Formatters
```svelte
<script lang="ts">
  import { createTranslator, createFormatters } from '@composable-svelte/core/i18n';

  const t = $derived(createTranslator($store.i18n, 'common'));
  const formatters = $derived(createFormatters($store.i18n));
</script>

<div>
  <p>{t('welcome', { name: 'Alice' })}</p>
  <p>{formatters.date(post.date)}</p>
  <p>{formatters.number(1234.56)}</p>
  <p>{formatters.currency(99.99, 'USD')}</p>
</div>
```

#### ❌ WRONG - Manual Formatting
```svelte
<!-- ❌ Don't manually format dates -->
<p>{new Date(post.date).toLocaleDateString()}</p>

<!-- ❌ Don't manually format numbers -->
<p>{price.toFixed(2)}</p>

<!-- ❌ Don't manually construct currency -->
<p>${price}</p>
```

**WHY**: Manual formatting doesn't respect locale conventions. Formatters automatically handle regional differences (e.g., "January 5, 2025" vs "5 janvier 2025", "1,234.56" vs "1 234,56").

---

## CORE CONCEPTS

### 1. Translation System

Use `createTranslator()` for accessing translations. It handles interpolation, ICU MessageFormat, and fallback chains automatically.

```svelte
<script lang="ts">
  import { createTranslator } from '@composable-svelte/core/i18n';

  const t = $derived(createTranslator($store.i18n, 'common'));
</script>

<div>
  <!-- Simple translation -->
  <h1>{t('app.title')}</h1>

  <!-- With interpolation -->
  <p>{t('welcome', { name: 'Alice' })}</p>

  <!-- ICU MessageFormat (pluralization) -->
  <p>{t('items', { count: 5 })}</p>
  <!-- Translation: "{count, plural, one {# item} other {# items}}" -->
  <!-- Output: "5 items" -->
</div>
```

**Translation File Example** (`locales/en/common.json`):
```json
{
  "app.title": "My Application",
  "welcome": "Welcome, {name}!",
  "items": "{count, plural, one {# item} other {# items}}",
  "greeting": "{gender, select, male {Hello Mr. {name}} female {Hello Ms. {name}} other {Hello {name}}}"
}
```

---

### 2. Formatters (Dates, Numbers, Currency)

Use `createFormatters()` to get locale-bound formatters. All formatters automatically use the current locale.

```svelte
<script lang="ts">
  import { createFormatters, DateFormats, NumberFormats } from '@composable-svelte/core/i18n';

  const formatters = $derived(createFormatters($store.i18n));
</script>

<div>
  <!-- Date formatting -->
  <p>{formatters.date(post.date)}</p>
  <!-- en: "January 5, 2025" -->
  <!-- fr: "5 janvier 2025" -->
  <!-- es: "5 de enero de 2025" -->

  <!-- Date with custom options -->
  <p>{formatters.date(post.date, DateFormats.short)}</p>
  <!-- en: "1/5/25" -->
  <!-- fr: "05/01/2025" -->

  <!-- Number formatting -->
  <p>{formatters.number(1234.56)}</p>
  <!-- en: "1,234.56" -->
  <!-- fr: "1 234,56" -->
  <!-- de: "1.234,56" -->

  <!-- Currency formatting -->
  <p>{formatters.currency(99.99, 'USD')}</p>
  <!-- en-US: "$99.99" -->
  <!-- fr: "99,99 $US" -->
  <!-- de: "99,99 $" -->

  <!-- Relative time -->
  <p>{formatters.relativeTime(yesterday)}</p>
  <!-- en: "yesterday" -->
  <!-- fr: "hier" -->
  <!-- es: "ayer" -->
</div>
```

**Available DateFormats**:
- `DateFormats.short` - "1/5/25"
- `DateFormats.medium` - "Jan 5, 2025"
- `DateFormats.long` - "January 5, 2025" (default)
- `DateFormats.full` - "Monday, January 5, 2025"

---

### 3. Locale Detection

The framework provides three locale detectors for different environments.

#### Browser (Client-Side)
```typescript
import { createBrowserLocaleDetector } from '@composable-svelte/core/i18n';

const localeDetector = createBrowserLocaleDetector({
  supportedLocales: ['en', 'fr', 'es'],
  defaultLocale: 'en',
  cookieName: 'locale',  // Optional: persist preference
  storageKey: 'user_locale'  // Optional: localStorage key
});

const locale = localeDetector.detect();
// Checks: 1. localStorage, 2. cookie, 3. navigator.language, 4. default
```

#### SSR (Server-Side Rendering)
```typescript
import { createSSRLocaleDetector } from '@composable-svelte/core/i18n';

// In your server handler
const localeDetector = createSSRLocaleDetector({
  supportedLocales: ['en', 'fr', 'es'],
  defaultLocale: 'en',
  url: request.url,  // For ?lang=fr query param
  cookies: request.headers.get('cookie') ?? '',
  acceptLanguage: request.headers.get('accept-language') ?? ''
});

const locale = localeDetector.detect();
// Checks: 1. URL (?lang=fr), 2. cookie, 3. Accept-Language, 4. default
```

#### SSG (Static Site Generation)
```typescript
import { createStaticLocaleDetector } from '@composable-svelte/core/i18n';

// For pre-rendering specific locale
const localeDetector = createStaticLocaleDetector('fr', ['en', 'fr', 'es']);
const locale = localeDetector.detect();  // Always returns 'fr'
```

---

### 4. Translation Loading

Three strategies for loading translations based on your use case.

#### Fetch Loader (Client-Side, Lazy Loading)
```typescript
import { FetchTranslationLoader } from '@composable-svelte/core/i18n';

const translationLoader = new FetchTranslationLoader({
  baseUrl: '/locales',  // Fetches from /locales/{locale}/{namespace}.json
  supportedLocales: ['en', 'fr', 'es']
});
```

**File Structure:**
```
public/
  locales/
    en/
      common.json
      products.json
    fr/
      common.json
      products.json
```

#### Bundled Loader (SSR, Build-Time)
```typescript
import { BundledTranslationLoader } from '@composable-svelte/core/i18n';

// Import translations at build time
import enCommon from '../locales/en/common.json';
import frCommon from '../locales/fr/common.json';

const translationLoader = new BundledTranslationLoader({
  bundles: {
    'en': { common: enCommon },
    'fr': { common: frCommon }
  }
});
```

#### Glob Loader (Vite-Specific, Auto-Discovery)
```typescript
import { createGlobLoader } from '@composable-svelte/core/i18n';

const translationLoader = createGlobLoader(
  import.meta.glob('/src/locales/*/*.json')
);
```

---

## COMPLETE SETUP EXAMPLES

### Client-Only Application

```typescript
// src/store.ts
import { createStore } from '@composable-svelte/core';
import {
  createInitialI18nState,
  i18nReducer,
  createBrowserLocaleDetector,
  FetchTranslationLoader,
  browserDOM
} from '@composable-svelte/core/i18n';

// Detect locale
const localeDetector = createBrowserLocaleDetector({
  supportedLocales: ['en', 'fr', 'es'],
  defaultLocale: 'en',
  storageKey: 'app_locale'
});

const initialLocale = localeDetector.detect();

// Initialize i18n state
const i18nState = createInitialI18nState(initialLocale, ['en', 'fr', 'es'], 'en');

const initialState: AppState = {
  todos: [],
  i18n: i18nState
};

// Create store with i18n dependencies
const store = createStore({
  initialState,
  reducer: appReducer,
  dependencies: {
    translationLoader: new FetchTranslationLoader({
      baseUrl: '/locales',
      supportedLocales: ['en', 'fr', 'es']
    }),
    localeDetector,
    storage: localStorage,
    dom: browserDOM
  }
});

// Load initial translations
store.dispatch({
  type: 'i18n/loadNamespace',
  namespace: 'common'
});
```

```svelte
<!-- src/App.svelte -->
<script lang="ts">
  import { createTranslator, createFormatters } from '@composable-svelte/core/i18n';

  const t = $derived(createTranslator($store.i18n, 'common'));
  const formatters = $derived(createFormatters($store.i18n));

  function switchLanguage(locale: string) {
    store.dispatch({
      type: 'i18n/setLocale',
      locale,
      preloadNamespaces: ['common']
    });
  }
</script>

<div>
  <h1>{t('app.title')}</h1>

  <select value={$store.i18n.currentLocale} onchange={(e) => switchLanguage(e.currentTarget.value)}>
    <option value="en">English</option>
    <option value="fr">Français</option>
    <option value="es">Español</option>
  </select>

  <p>{t('welcome', { name: 'User' })}</p>
  <p>{formatters.date(new Date())}</p>
</div>
```

---

### SSR Application

**Server Setup:**
```typescript
// src/server/index.ts
import { renderToHTML } from '@composable-svelte/core/ssr';
import {
  createInitialI18nState,
  BundledTranslationLoader,
  createSSRLocaleDetector,
  serverDOM
} from '@composable-svelte/core/i18n';

// Import translations
import enCommon from '../locales/en/common.json';
import frCommon from '../locales/fr/common.json';

app.get('*', async (request, reply) => {
  // Detect locale from request
  const localeDetector = createSSRLocaleDetector({
    supportedLocales: ['en', 'fr'],
    defaultLocale: 'en',
    url: request.url,
    cookies: request.headers.cookie ?? '',
    acceptLanguage: request.headers['accept-language'] ?? ''
  });

  const locale = localeDetector.detect();

  // Initialize i18n for this request
  const i18nState = createInitialI18nState(locale, ['en', 'fr'], 'en');

  const initialState: AppState = {
    todos: [],
    i18n: i18nState
  };

  // Render with i18n dependencies
  const html = await renderToHTML(App, {
    initialState,
    reducer: appReducer,
    dependencies: {
      translationLoader: new BundledTranslationLoader({
        bundles: {
          'en': { common: enCommon },
          'fr': { common: frCommon }
        }
      }),
      localeDetector,
      storage: new Map(),  // SSR-safe storage
      dom: serverDOM
    }
  });

  reply.type('text/html').send(html);
});
```

**Client Hydration:**
```typescript
// src/client/index.ts
import { hydrateStore } from '@composable-svelte/core/ssr';
import {
  FetchTranslationLoader,
  createBrowserLocaleDetector,
  browserDOM
} from '@composable-svelte/core/i18n';

const store = hydrateStore(
  document.getElementById('__COMPOSABLE_SVELTE_STATE__')!.textContent,
  {
    reducer: appReducer,
    dependencies: {
      translationLoader: new FetchTranslationLoader({
        baseUrl: '/locales',
        supportedLocales: ['en', 'fr']
      }),
      localeDetector: createBrowserLocaleDetector({
        supportedLocales: ['en', 'fr'],
        defaultLocale: 'en'
      }),
      storage: localStorage,
      dom: browserDOM
    }
  }
);
```

---

## ICU MessageFormat

The framework automatically detects and compiles ICU MessageFormat syntax for advanced translations.

### Pluralization
```json
{
  "items": "{count, plural, =0 {No items} one {# item} other {# items}}"
}
```

```typescript
t('items', { count: 0 });   // "No items"
t('items', { count: 1 });   // "1 item"
t('items', { count: 5 });   // "5 items"
```

### Selection (Gender, etc.)
```json
{
  "greeting": "{gender, select, male {Hello Mr. {name}} female {Hello Ms. {name}} other {Hello {name}}}"
}
```

```typescript
t('greeting', { gender: 'male', name: 'Smith' });    // "Hello Mr. Smith"
t('greeting', { gender: 'female', name: 'Johnson' }); // "Hello Ms. Johnson"
t('greeting', { gender: 'other', name: 'Taylor' });  // "Hello Taylor"
```

### Nested Plurals
```json
{
  "cart": "{itemCount, plural, one {You have # item} other {You have # items}} in {cartCount, plural, one {# cart} other {# carts}}"
}
```

```typescript
t('cart', { itemCount: 1, cartCount: 1 });  // "You have 1 item in 1 cart"
t('cart', { itemCount: 5, cartCount: 2 });  // "You have 5 items in 2 carts"
```

---

## COMMON PATTERNS

### Pattern 1: Language Switcher

```svelte
<script lang="ts">
  const availableLocales = $derived($store.i18n.availableLocales);
  const currentLocale = $derived($store.i18n.currentLocale);

  const languageNames: Record<string, string> = {
    en: 'English',
    fr: 'Français',
    es: 'Español'
  };

  function switchLanguage(locale: string) {
    store.dispatch({
      type: 'i18n/setLocale',
      locale,
      preloadNamespaces: ['common']  // Load common translations immediately
    });
  }
</script>

<div class="language-switcher">
  {#each availableLocales as locale}
    <button
      class:active={locale === currentLocale}
      onclick={() => switchLanguage(locale)}
    >
      {languageNames[locale]}
    </button>
  {/each}
</div>
```

### Pattern 2: Lazy Loading Namespaces

Load translations on-demand to reduce initial bundle size.

```typescript
// Load translations when user navigates to products page
function navigateToProducts() {
  store.dispatch({
    type: 'i18n/loadNamespace',
    namespace: 'products'
  });

  // Navigate after translations loaded (via effect)
  store.dispatch({
    type: 'navigate',
    destination: { type: 'products' }
  });
}
```

**In Reducer:**
```typescript
case 'i18n/namespaceLoaded': {
  // Translation loaded, safe to navigate
  if (action.namespace === 'products') {
    return [state, Effect.none()];
  }
  return [state, Effect.none()];
}
```

### Pattern 3: Formatted Lists

```svelte
<script lang="ts">
  const authors = ['Alice', 'Bob', 'Carol'];

  // The framework uses Intl.ListFormat automatically
  const formattedAuthors = $derived(
    new Intl.ListFormat($store.i18n.currentLocale, {
      style: 'long',
      type: 'conjunction'
    }).format(authors)
  );
</script>

<p>Authors: {formattedAuthors}</p>
<!-- en: "Authors: Alice, Bob, and Carol" -->
<!-- fr: "Authors: Alice, Bob et Carol" -->
<!-- es: "Authors: Alice, Bob y Carol" -->
```

---

## BEST PRACTICES

### 1. Organize Translation Files by Namespace

```
locales/
  en/
    common.json         # UI labels, buttons, navigation
    products.json       # Product-related translations
    errors.json         # Error messages
    validation.json     # Form validation messages
  fr/
    common.json
    products.json
    ...
```

**Benefits:**
- Lazy load translations per feature
- Easier maintenance
- Smaller initial bundle

### 2. Use Descriptive Keys

```json
{
  "nav.home": "Home",
  "nav.products": "Products",
  "products.addToCart": "Add to Cart",
  "products.outOfStock": "Out of Stock",
  "validation.required": "This field is required"
}
```

**WHY**: Namespaced keys make it clear where translations are used and prevent conflicts.

### 3. Provide Context in Plurals

```json
{
  "cart.items": "{count, plural, =0 {Your cart is empty} one {# item in cart} other {# items in cart}}"
}
```

**WHY**: The `=0` case lets you provide a more natural message than "0 items".

### 4. Keep Formatters as Derived Values

```svelte
<script lang="ts">
  // ✅ CORRECT - Reactive to locale changes
  const formatters = $derived(createFormatters($store.i18n));

  // ❌ WRONG - Won't update when locale changes
  const formatters = createFormatters($store.i18n);
</script>
```

### 5. Test with Multiple Locales

```typescript
import { TestStore } from '@composable-svelte/core/test';

test('displays localized date', async () => {
  const store = new TestStore({
    initialState: {
      post: { date: '2025-01-05' },
      i18n: createInitialI18nState('fr', ['en', 'fr'])
    },
    reducer: appReducer,
    dependencies: { /* ... */ }
  });

  const formatters = createFormatters(store.state.i18n);
  expect(formatters.date(store.state.post.date)).toBe('5 janvier 2025');
});
```

---

## COMMON GOTCHAS

### Gotcha 1: Not Awaiting Translation Load

```typescript
// ❌ WRONG - Translations not loaded yet
store.dispatch({ type: 'i18n/setLocale', locale: 'fr' });
const t = createTranslator(store.state.i18n, 'common');  // May not have French translations!

// ✅ CORRECT - Wait for load or preload
store.dispatch({
  type: 'i18n/setLocale',
  locale: 'fr',
  preloadNamespaces: ['common']  // Loads before completing
});
```

### Gotcha 2: Forgetting to Handle i18n Actions in Reducer

```typescript
// ❌ WRONG - i18n actions not handled
const appReducer: Reducer<AppState, AppAction> = (state, action, deps) => {
  switch (action.type) {
    case 'addTodo':
      return [/* ... */];
    // Missing i18n handling!
  }
};

// ✅ CORRECT - Handle i18n actions
const appReducer: Reducer<AppState, AppAction> = (state, action, deps) => {
  // Handle i18n actions first
  if (typeof action.type === 'string' && action.type.startsWith('i18n/')) {
    const [newI18nState, i18nEffect] = i18nReducer(state.i18n, action as any, deps);
    return [
      { ...state, i18n: newI18nState },
      i18nEffect as Effect<AppAction>
    ];
  }

  switch (action.type) {
    case 'addTodo':
      return [/* ... */];
  }
};
```

### Gotcha 3: Using Wrong Storage on Server

```typescript
// ❌ WRONG - localStorage doesn't exist on server
const deps = {
  storage: localStorage,  // Crashes in SSR!
  dom: serverDOM
};

// ✅ CORRECT - Use SSR-safe storage
const deps = {
  storage: new Map(),  // Or mock storage
  dom: serverDOM
};
```

### Gotcha 4: Not Binding Formatters to Locale

```typescript
// ❌ WRONG - Formatters created once, won't update
const formatters = createFormatters($store.i18n);

// ✅ CORRECT - Derived, updates when locale changes
const formatters = $derived(createFormatters($store.i18n));
```

---

## PERFORMANCE TIPS

### 1. Cache Formatters Per Locale

The framework already caches `Intl.DateTimeFormat` and `Intl.NumberFormat` instances. Creating formatters is cheap.

### 2. Lazy Load Namespaces

```typescript
// Load translations only when needed
store.dispatch({
  type: 'i18n/loadNamespace',
  namespace: 'products'
});
```

### 3. Use Bundled Loader for SSR

Bundled translations are faster than fetch on every request:
```typescript
const translationLoader = new BundledTranslationLoader({
  bundles: {
    'en': { common: enCommon },
    'fr': { common: frCommon }
  }
});
```

### 4. Preload Critical Namespaces

```typescript
store.dispatch({
  type: 'i18n/setLocale',
  locale: 'fr',
  preloadNamespaces: ['common', 'navigation']  // Load multiple at once
});
```

---

## SSR/SSG INTEGRATION

For complete SSR/SSG patterns, see the **composable-svelte-ssr** skill. Key points:

### SSR
- Server: Use `BundledTranslationLoader`, `createSSRLocaleDetector`, `serverDOM`
- Client: Use `FetchTranslationLoader`, `createBrowserLocaleDetector`, `browserDOM`
- State serializes automatically via `renderToHTML`

### SSG (Static Sites)
- Use `createStaticLocaleDetector` with fixed locale
- Generate separate HTML files per locale (`/en/`, `/fr/`, `/es/`)
- Language switcher uses links to pre-generated pages

**Example**: See `examples/ssr-server/src/build/ssg.ts` for complete SSG setup.

---

## TYPESCRIPT SUPPORT

All types are fully typed and exported:

```typescript
import type {
  I18nState,
  I18nAction,
  I18nDependencies,
  Translator,
  BoundFormatters,
  TranslationLoader,
  LocaleDetector
} from '@composable-svelte/core/i18n';
```

---

## TESTING

Use `TestStore` to test translations and locale switching:

```typescript
import { TestStore } from '@composable-svelte/core/test';
import { createTranslator } from '@composable-svelte/core/i18n';

test('switches locale', async () => {
  const store = new TestStore({
    initialState: {
      i18n: createInitialI18nState('en', ['en', 'fr'])
    },
    reducer: appReducer,
    dependencies: mockI18nDependencies
  });

  await store.send({ type: 'i18n/setLocale', locale: 'fr', preloadNamespaces: ['common'] });
  await store.receive({ type: 'i18n/namespaceLoaded', namespace: 'common' }, (state) => {
    expect(state.i18n.currentLocale).toBe('fr');
  });
});
```

---

## SUMMARY

**Core Principles:**
1. i18n state lives in your app store via `i18nReducer`
2. Use `createTranslator()` for translations, `createFormatters()` for dates/numbers/currency
3. Framework handles all locale-specific formatting automatically
4. ICU MessageFormat for pluralization and selection
5. Three loaders: Fetch (client), Bundled (SSR), Glob (Vite)
6. Three detectors: Browser, SSR, Static (SSG)

**Most Common Pattern:**
```svelte
<script lang="ts">
  import { createTranslator, createFormatters } from '@composable-svelte/core/i18n';

  const t = $derived(createTranslator($store.i18n, 'common'));
  const formatters = $derived(createFormatters($store.i18n));
</script>

<div>
  <h1>{t('app.title')}</h1>
  <p>{t('welcome', { name: user.name })}</p>
  <time>{formatters.date(post.date)}</time>
  <span>{formatters.currency(product.price, 'USD')}</span>
</div>
```

The i18n system is fully integrated with the Composable Architecture, providing a complete, type-safe, and performant solution for building multi-language applications.
