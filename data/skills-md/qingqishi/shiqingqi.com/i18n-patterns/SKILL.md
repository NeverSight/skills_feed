---
name: i18n-patterns
description: Internationalization (i18n) patterns for server and client components using getTranslations and useTranslations. Use when working with translations, locales, multilingual content, translation files, TranslationContextProvider, locale switching, or when the user mentions i18n, translations, getTranslations, useTranslations, or translation.json files.
---

# Internationalization Patterns

## Overview

This project supports internationalization (i18n) with separate patterns for server and client components.

## Supported Locales

Routes use the `[locale]` parameter to support:

- `en` - English
- `zh` - Chinese

## Routing

### URL Structure

All routes include the locale parameter:

```
/en/about
/zh/about
```

### Generating Localized URLs

Use `getLocalePath()` to create locale-aware URLs:

```tsx
import { getLocalePath } from "@/utils/locale";

// Current locale: "en"
const aboutPath = getLocalePath("/about"); // Returns "/en/about"

// Switching locale
const zhAboutPath = getLocalePath("/about", "zh"); // Returns "/zh/about"
```

## Translation File Structure

### Server Component Translations

Location: `translations.json` files in component and route folders

```
src/
  components/
    Header/
      translations.json
  app/
    [locale]/
      about/
        translations.json
```

Example `translations.json`:

```json
{
  "en": {
    "title": "About Us",
    "description": "Learn more about our company"
  },
  "zh": {
    "title": "关于我们",
    "description": "了解更多关于我们公司的信息"
  }
}
```

### Client Component Translations

Location: `[ComponentName].translations.json` (component-specific for tree shaking)

```
src/
  components/
    Button/
      Button.tsx
      Button.translations.json
```

Example `Button.translations.json`:

```json
{
  "en": {
    "submit": "Submit",
    "cancel": "Cancel"
  },
  "zh": {
    "submit": "提交",
    "cancel": "取消"
  }
}
```

Component-specific translation files enable tree shaking.

## Server Components

Server components use the `getTranslations` utility to obtain translated texts.

```tsx
import { getTranslations } from "@/utils/translations";

async function ServerComponent({ params }) {
  const t = await getTranslations(params.locale);

  return (
    <div>
      <h1>{t.title}</h1>
      <p>{t.description}</p>
    </div>
  );
}
```

Use `getTranslations(locale)` - async function that returns translation object.

## Client Components

Client components use the `useTranslations()` hook which reads translations from context.

```tsx
"use client";
import { useTranslations } from "@/hooks/useTranslations";

function ClientComponent() {
  const t = useTranslations();

  return <button>{t.submit}</button>;
}
```

### Providing Translations to Client Components

A server component parent must render `<TranslationContextProvider />` with the translation content.

```tsx
// Server component (parent)
import { TranslationContextProvider } from "@/contexts/TranslationContext";
import buttonTranslations from "@/components/Button/Button.translations.json";
import ClientComponent from "./ClientComponent";

async function ServerParent({ params }) {
  const locale = params.locale;

  return (
    <TranslationContextProvider translations={buttonTranslations[locale]}>
      <ClientComponent />
    </TranslationContextProvider>
  );
}
```

Server component parent must provide `<TranslationContextProvider />` with component-specific translations imported from JSON.

## Complete Example

### Scenario: Button component with translations

**1. Translation file** (`Button.translations.json`):

```json
{
  "en": {
    "submit": "Submit",
    "cancel": "Cancel",
    "loading": "Loading..."
  },
  "zh": {
    "submit": "提交",
    "cancel": "取消",
    "loading": "加载中..."
  }
}
```

**2. Client component** (`Button.tsx`):

```tsx
"use client";
import { useTranslations } from "@/hooks/useTranslations";

export function Button({ isLoading, onSubmit, onCancel }) {
  const t = useTranslations();

  return (
    <div>
      <button onClick={onSubmit} disabled={isLoading}>
        {isLoading ? t.loading : t.submit}
      </button>
      <button onClick={onCancel}>{t.cancel}</button>
    </div>
  );
}
```

**3. Server component parent** (`Form.tsx`):

```tsx
import { TranslationContextProvider } from "@/contexts/TranslationContext";
import buttonTranslations from "@/components/Button/Button.translations.json";
import { Button } from "@/components/Button/Button";

export async function Form({ params }) {
  const locale = params.locale;

  return (
    <TranslationContextProvider translations={buttonTranslations[locale]}>
      <Button onSubmit={...} onCancel={...} />
    </TranslationContextProvider>
  );
}
```

## Pattern Summary

### Server Components

```
Server Component → getTranslations(locale) → translations.json → Rendered text
```

### Client Components

```
Server Parent → Import translations.json → TranslationContextProvider
    ↓
Client Component → useTranslations() hook → Rendered text
```

## Best Practices

1. **File naming**: `translations.json` for server components, `[ComponentName].translations.json` for client components
2. **Context provider**: Always wrap client components with `TranslationContextProvider`
3. **Locale parameter**: Pass `params.locale` from route params

## Common Patterns

### Locale Switching Link

```tsx
import { getLocalePath } from "@/utils/locale";

<a href={getLocalePath("/current-route", "zh")}>Switch to Chinese</a>;
```

### Conditional Translation

```tsx
const t = useTranslations();

<div>{user.isPremium ? t.premiumMessage : t.freeMessage}</div>;
```

### Translation with Variables

```tsx
// In translations.json
{
  "en": {
    "greeting": "Hello, {name}!"
  }
}

// In component
const message = t.greeting.replace("{name}", userName);
```

## Common Mistakes

❌ Using `getTranslations()` in client components (use `useTranslations()` hook)
❌ Missing `TranslationContextProvider` wrapper for client components
❌ Hardcoding locale strings (use `params.locale`)
❌ Creating monolithic translation files (split by component)
