---
name: zoonk-translations
description: Work with internationalization using next-intl. Use when handling translations, i18n, getTranslations, useTranslations, translating content, or when the user needs to add or modify translations.
license: MIT
metadata:
  author: zoonk
  version: "1.0.0"
---

# Internationalization (i18n) Workflow

## Overview

This project uses `next-intl` for internationalization. Translations are stored in JSON message files.

## Key Functions

- **Server Components**: Use `getTranslations` (no locale needed)
- **Client Components**: Use `useTranslations`
- **Metadata/Server Actions**: Use `getTranslations` with locale parameter

## Critical Rules

### 1. No Dynamic Values in Translation Keys

**IMPORTANT**: The `t` function does NOT support dynamic values as keys.

```tsx
// BAD: Dynamic key - will NOT work
const category = getCategory();
t(category); // Error!
t(MYLABELS[category]);

// GOOD: String literals only
t("Arts courses");
t("Business courses");
t("Technology courses");
```

### 2. String Interpolation IS Supported

You CAN use string interpolation for dynamic values within translations:

```tsx
// GOOD: Interpolation with static key
t("Explore all {category} courses", { category: "arts" });
t("Welcome, {name}!", { name: user.name });
t("{count} items remaining", { count: 5 });
```

### 3. Don't Pass `t` Function Around

You can't pass the `t` function to other functions or components:

```tsx
// BAD: Passing t function
function myFunction(t, label) {
  return t(label);
}
myFunction(t, "Some label");

// GOOD: Call t directly
function myFunction(translatedLabel: string) {
  return translatedLabel;
}
myFunction(t("Some label"));
```

### 4. Locale Parameter Rules

```tsx
// Server Component - no locale needed
const t = await getTranslations();
t("Hello");

// generateMetadata - needs locale
export async function generateMetadata({ params }) {
  const { locale } = await params;
  const t = await getTranslations({ locale });
  return { title: t("Page Title") };
}
```

## Workflow for Adding Translations

1. **Add translation call in code**:

   ```tsx
   const t = await getTranslations();
   return <h1>{t("New page title")}</h1>;
   ```

2. **Add the key to message files**:

   Find JSON message files in your locales directory (e.g., `messages/en.json`, `messages/es.json`) and add the new key:

   ```json
   {
     "New page title": "New page title"
   }
   ```

3. **Translate for each locale**:

   ```json
   // messages/es.json
   {
     "New page title": "Nuevo título de página"
   }
   ```

## Common Patterns

### Conditional Text

```tsx
// Use separate translation keys
const status = isActive ? t("Active") : t("Inactive");
```

### Pluralization

```tsx
// Use ICU message format
t("items", { count: 5 }); // "5 items"
```

In your messages file:

```json
{
  "items": "{count, plural, =0 {No items} =1 {1 item} other {# items}}"
}
```

### Rich Text (with components)

```tsx
t.rich("Read our {link}", {
  link: (chunks) => <Link href="/terms">{chunks}</Link>,
});
```

In your messages file:

```json
{
  "Read our {link}": "Read our <link>terms of service</link>"
}
```

## File Structure

```
messages/
  en.json      # English translations
  es.json      # Spanish translations
  pt.json      # Portuguese translations
```

## Namespaces

For larger apps, organize translations by namespace:

```tsx
// Server Component
const t = await getTranslations("Dashboard");
t("welcome"); // Looks up "Dashboard.welcome"

// Client Component
const t = useTranslations("Dashboard");
t("welcome");
```

```json
{
  "Dashboard": {
    "welcome": "Welcome to your dashboard"
  }
}
```
