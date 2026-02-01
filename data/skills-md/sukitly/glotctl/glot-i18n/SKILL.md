---
name: glot-i18n
description: Fix i18n issues in Next.js + next-intl projects using glot MCP server. Use when user needs to fix hardcoded text, missing translation keys, sync translations across locales, or detect untranslated values.
compatibility: Requires glot MCP server configured
metadata:
  author: glot
  version: "1.0"
---

# Glot i18n Skill

This skill guides you through detecting and fixing internationalization (i18n) issues in Next.js projects using next-intl.

## Prerequisites

- **glot MCP server** must be configured and available
- Project should have a `.glotrc.json` configuration file (run `glot init` if missing)
- Project uses `next-intl` for translations

## When to Use This Skill

Activate this skill when:

- User asks to fix i18n, internationalization, or translation issues
- User mentions hardcoded text that should be translated
- User wants to find missing translation keys
- User needs to sync translations across multiple locales
- User mentions "glot" or asks to use glot tools

## Core Workflow

**IMPORTANT**: Follow this order to minimize rework!

```
1. scan_overview     → Understand the overall state
2. Fix hardcoded    → Replace text with t() calls, add keys to primary locale
3. Fix primary_missing → Add missing keys to primary locale
4. Fix replica_lag   → Sync keys to other locales
5. Fix untranslated  → Translate values that are identical to primary locale
```

Why this order matters:

- Fixing hardcoded issues may create new primary_missing issues
- Fixing primary_missing may create new replica_lag issues
- Replica_lag fixes may create new untranslated issues (if text is copied without translation)
- Following this order prevents duplicate work

## Available Tools

| Tool                   | Purpose                               | When to Use                           |
| ---------------------- | ------------------------------------- | ------------------------------------- |
| `get_config`           | Get project configuration             | First, to understand project setup    |
| `get_locales`          | List available locale files           | To see which languages are configured |
| `scan_overview`        | Get statistics of all issues          | Always start here to understand scope |
| `scan_hardcoded`       | List hardcoded text issues            | When fixing hardcoded text            |
| `scan_primary_missing` | List keys missing from primary locale | After fixing hardcoded issues         |
| `scan_replica_lag`     | List keys missing from other locales  | After fixing primary_missing          |
| `scan_untranslated`    | List values identical to primary locale | After fixing replica_lag (or anytime) |
| `add_translations`     | Add keys to locale files              | When adding new translation keys      |

## Step-by-Step: Fixing Hardcoded Text

### 1. Get Overview First

```
Call: scan_overview
Parameters: { "project_root_path": "<project_path>" }
```

Check the `hardcoded.total_count` to understand scope.

### 2. Get Detailed Hardcoded Issues

```
Call: scan_hardcoded
Parameters: { "project_root_path": "<project_path>", "limit": 20 }
```

Each item contains:

- `file_path`: The TSX/JSX file
- `line`, `col`: Location
- `text`: The hardcoded text found
- `source_line`: The actual source code line

### 3. For Each Issue, Determine the Key Name

Follow key naming conventions:

- Use **camelCase** for keys
- Organize by **component or page namespace**
- Be **descriptive but concise**

Examples:
| Text | Suggested Key |
|------|---------------|
| "Submit" | `common.submit` or `buttons.submit` |
| "Welcome to our app" | `homePage.hero.welcomeMessage` |
| "Enter your email" | `auth.emailPlaceholder` |
| "Loading..." | `common.loading` |

### 4. Modify the Source Code

Replace hardcoded text with `t()` calls:

**Before:**

```tsx
<button>Submit</button>
<input placeholder="Enter email" />
<p>Welcome to our app</p>
```

**After:**

```tsx
<button>{t("common.submit")}</button>
<input placeholder={t("auth.emailPlaceholder")} />
<p>{t("homePage.hero.welcomeMessage")}</p>
```

Ensure the component has `useTranslations` hook:

```tsx
import { useTranslations } from "next-intl";

export function MyComponent() {
  const t = useTranslations();
  // ... or with namespace:
  // const t = useTranslations("homePage");

  return <p>{t("hero.welcomeMessage")}</p>;
}
```

### 5. Add Keys to Locale Files

```
Call: add_translations
Parameters: {
  "project_root_path": "<project_path>",
  "translations": [
    {
      "locale": "en",
      "keys": {
        "common.submit": "Submit",
        "auth.emailPlaceholder": "Enter your email",
        "homePage.hero.welcomeMessage": "Welcome to our app"
      }
    }
  ]
}
```

Nested keys (e.g., `common.submit`) are automatically expanded to nested JSON structure.

### 6. Handle Pagination

If `pagination.has_more` is `true`, continue with next offset:

```
Call: scan_hardcoded
Parameters: { "project_root_path": "<project_path>", "limit": 20, "offset": 20 }
```

## Step-by-Step: Fixing Primary Missing Keys

After fixing hardcoded issues, some keys might be used in code but missing from locale files.

### 1. Scan for Missing Keys

```
Call: scan_primary_missing
Parameters: { "project_root_path": "<project_path>" }
```

Each item shows:

- `key`: The missing key name
- `file_path`: Where it's used
- `line`: Line number

### 2. Add Missing Keys

For each missing key, determine the appropriate translation value and add it:

```
Call: add_translations
Parameters: {
  "project_root_path": "<project_path>",
  "translations": [
    {
      "locale": "en",
      "keys": {
        "missingKey1": "Translation value 1",
        "missingKey2": "Translation value 2"
      }
    }
  ]
}
```

## Step-by-Step: Fixing Replica Lag

Keys that exist in primary locale but missing in other locales.

### 1. Scan for Replica Lag

```
Call: scan_replica_lag
Parameters: { "project_root_path": "<project_path>" }
```

Each item shows:

- `key`: The key name
- `value`: Value in primary locale
- `exists_in`: Primary locale code
- `missing_in`: Array of locales missing this key

### 2. Sync to Other Locales

**Option A**: Copy primary value (for same-language variants or as placeholder)

```
Call: add_translations
Parameters: {
  "project_root_path": "<project_path>",
  "translations": [
    { "locale": "de", "keys": { "common.submit": "Submit" } },
    { "locale": "fr", "keys": { "common.submit": "Submit" } }
  ]
}
```

**Option B**: Ask user for translations

If the user can provide translations, use their values. Otherwise, copy the primary value as a placeholder with a TODO comment in the code or a note to the user.

## Step-by-Step: Fixing Untranslated Values

Values that are identical to the primary locale may indicate text was copied without being translated.

### 1. Scan for Untranslated Values

```
Call: scan_untranslated
Parameters: { "project_root_path": "<project_path>" }
```

Each item shows:

- `key`: The translation key
- `value`: The value (same in both locales)
- `locale`: The non-primary locale with the issue
- `primary_locale`: The primary locale code

### 2. Translate the Values

For each untranslated key, provide the correct translation:

```
Call: add_translations
Parameters: {
  "project_root_path": "<project_path>",
  "translations": [
    { "locale": "de", "keys": { "common.submit": "Absenden" } },
    { "locale": "fr", "keys": { "common.submit": "Soumettre" } }
  ]
}
```

**Note**: Some values may intentionally be the same across locales (e.g., brand names, technical terms). Use your judgment or ask the user.

## Key Naming Conventions

### Namespace Structure

```
<area>.<section>.<element>
```

Examples:

- `common.buttons.submit` - Shared UI elements
- `auth.login.title` - Authentication pages
- `dashboard.sidebar.menuItem` - Dashboard specific
- `errors.validation.required` - Error messages

### Rules

1. **Use camelCase**: `welcomeMessage` not `welcome-message`
2. **Be specific**: `auth.loginButton` not just `login`
3. **Group by feature**: Keep related keys together
4. **Avoid deep nesting**: Max 3-4 levels

### Special Cases

**Plurals** (if using next-intl plural support):

```json
{
  "items": "{count, plural, =0 {No items} =1 {One item} other {# items}}"
}
```

**Variables**:

```json
{
  "greeting": "Hello, {name}!"
}
```

## Common Patterns

### JSX Text Content

```tsx
// Before
<h1>Welcome</h1>

// After
<h1>{t("page.welcome")}</h1>
```

### Attributes (placeholder, title, alt, aria-\*)

```tsx
// Before
<input placeholder="Search..." />
<img alt="User avatar" />

// After
<input placeholder={t("common.searchPlaceholder")} />
<img alt={t("common.userAvatar")} />
```

### Conditional Text

```tsx
// Before
{
  isLoading ? "Loading..." : "Submit";
}

// After
{
  isLoading ? t("common.loading") : t("common.submit");
}
```

### Template Literals

```tsx
// Before
<p>{`Welcome, ${userName}`}</p>

// After (using next-intl variables)
<p>{t("greeting", { name: userName })}</p>
// In JSON: "greeting": "Welcome, {name}"
```

## Important Notes

1. **Work in batches**: Fix 10-20 issues at a time, then verify
2. **Re-scan after fixes**: Run `scan_overview` again to verify progress
3. **Handle pagination**: Check `has_more` field and continue if needed
4. **Preserve formatting**: When modifying TSX, maintain existing code style
5. **Import hook**: Ensure `useTranslations` is imported in modified components
6. **Test after changes**: Recommend user runs the app to verify translations work

## Troubleshooting

### "Config file not found"

Run `glot init` in the project root to create `.glotrc.json`

### Keys not being detected

Check that `messages_dir` in config points to correct locale files directory

### Some text not detected as hardcoded

The text must contain at least one alphabetic character. Pure numbers/symbols are ignored.
