---
name: form-attribution
description: Implement the Form Attribution library on websites to capture UTM parameters, ad click IDs, referrer data, and other marketing attribution automatically. Use when the user needs to (1) add marketing attribution tracking to a website, (2) configure form attribution for specific use cases like cross-subdomain tracking or CRM integration, (3) troubleshoot form attribution issues, or (4) implement platform-specific patterns for Webflow, HubSpot, WordPress, or other select platforms.
license: MIT
metadata:
  author: "[Ben Sabic](https://bensabic.ca)"
  role: "Fractional CTO"
  version: "1.0.0"
---

# Form Attribution

A lightweight, zero-dependency script that automatically captures marketing attribution data and injects it into forms as hidden fields.

| Resource   | Link/URL                                                                                   |
|------------|-------------------------------------------------------------------------------------------|
| **CDN URL**| `https://cdn.jsdelivr.net/npm/form-attribution@latest/dist/script.min.js`                 |
| **Docs**   | [https://form-attribution.flashbrew.digital/docs](https://form-attribution.flashbrew.digital/docs) |
| **GitHub** | [https://github.com/Flash-Brew-Digital/form-attribution](https://github.com/Flash-Brew-Digital/form-attribution) |

## Basic Implementation

Add before the closing `</body>` tag:

```html
<script src="https://cdn.jsdelivr.net/npm/form-attribution@latest/dist/script.min.js" defer></script>
```

The script automatically captures UTM parameters, stores them in sessionStorage, and injects hidden fields into all forms.

## Configuration Options

Configure via data attributes on the script tag:

| Attribute | Default | Description |
|-----------|---------|-------------|
| `data-storage` | `sessionStorage` | `sessionStorage`, `localStorage`, or `cookie` |
| `data-field-prefix` | `""` | Prefix for hidden field names (e.g., `attr_`) |
| `data-extra-params` | `""` | Additional URL parameters to capture (comma-separated) |
| `data-exclude-forms` | `""` | CSS selector for forms to exclude |
| `data-click-ids` | `false` | Capture ad platform click IDs (gclid, fbclid, etc.) |
| `data-debug` | `false` | Enable debug panel overlay |
| `data-privacy` | `true` | Respect GPC/DNT privacy signals |
| `data-storage-key` | `form_attribution_data` | Custom storage key name |

**Cookie-specific options** (when `data-storage="cookie"`):

| Attribute | Default | Description |
|-----------|---------|-------------|
| `data-cookie-domain` | `""` | Cookie domain (e.g., `.example.com`) |
| `data-cookie-path` | `/` | Cookie path |
| `data-cookie-expires` | `30` | Expiration in days |
| `data-cookie-samesite` | `lax` | `lax`, `strict`, or `none` |

## What Gets Captured

**URL Parameters (default):** `utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content`, `utm_id`, `ref`

**Metadata (automatic):** `landing_page`, `current_page`, `referrer_url`, `first_touch_timestamp`

**Click IDs (when `data-click-ids="true"`):** `gclid` (Google), `fbclid` (Meta), `msclkid` (Microsoft), `ttclid` (TikTok), `li_fat_id` (LinkedIn), `twclid` (Twitter/X)

## Common Configurations

**With ad click ID tracking:**
```html
<script src="https://cdn.jsdelivr.net/npm/form-attribution@latest/dist/script.min.js"
  data-click-ids="true" defer></script>
```

**Cross-subdomain tracking (cookies):**
```html
<script src="https://cdn.jsdelivr.net/npm/form-attribution@latest/dist/script.min.js"
  data-storage="cookie"
  data-cookie-domain=".example.com"
  data-cookie-expires="90"
  data-click-ids="true" defer></script>
```

**CRM field prefix:**
```html
<script src="https://cdn.jsdelivr.net/npm/form-attribution@latest/dist/script.min.js"
  data-field-prefix="lead_"
  data-click-ids="true" defer></script>
```

**Exclude forms (e.g., search, login):**
```html
<script src="https://cdn.jsdelivr.net/npm/form-attribution@latest/dist/script.min.js"
  data-exclude-forms=".no-track, #login-form, [data-no-attribution]" defer></script>
```

## JavaScript API

The library exposes a global `FormAttribution` object:

```javascript
FormAttribution.getData();              // Get all captured data
FormAttribution.getParam('utm_source'); // Get specific parameter
FormAttribution.getForms();             // Get tracked forms
FormAttribution.clear();                // Clear stored data
FormAttribution.refresh();              // Re-inject into forms
```

## Privacy

Respects Global Privacy Control (GPC) and Do Not Track (DNT) by default. When detected, no data is captured. Override with `data-privacy="false"`.

## References (references/*)

### Platform-Specific Patterns

For implementation patterns specific to Webflow, HubSpot, WordPress, Marketo, and certain other platforms, see [references/platforms.md](references/platforms.md).

### FAQ

For common questions about compatibility, privacy, performance, and customization, see [references/faq.md](references/faq.md).