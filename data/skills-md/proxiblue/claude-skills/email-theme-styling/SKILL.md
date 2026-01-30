---
name: email-theme-styling
description: Comprehensive guide for theming and styling Magento 2 transactional emails via theme files, including Hyvä-specific considerations, CSS inlining architecture, and template override patterns.
---

# Magento 2 Email Theme & Styling Skill

## Purpose
This skill provides comprehensive guidance on theming and styling Magento 2 transactional emails via theme files. It covers the full email rendering pipeline, CSS inlining architecture, template override patterns, Hyvä Email module integration, and the Tailwind-to-LESS compilation approach.

## When to Use This Skill
- Customizing the look and feel of transactional emails (order confirmation, account creation, etc.)
- Overriding email header/footer templates via the theme
- Adding custom CSS styles to emails
- Setting up a custom email logo
- Debugging email rendering or CSS inlining issues
- Understanding how Hyvä interacts with the email system
- Using Tailwind CSS as a source for email styles

---

## Architecture Overview

### Email Rendering Pipeline

```
1. Module defines template in email_templates.xml (e.g. sales_email_order_template)
       ↓
2. TransportBuilder triggers template rendering
       ↓
3. AbstractTemplate::getProcessedTemplate()
   - applyDesignConfig() → emulates store/theme context
   - addEmailVariables() → populates store data, template_styles
       ↓
4. Filter->filter(templateText) processes directives:
   - {{template config_path="design/email/header_template"}} → includes header
   - {{template config_path="design/email/footer_template"}} → includes footer
   - {{css file="css/email.css"}} → outputs CSS in <style> tag
   - {{inlinecss file="css/email-inline.css"}} → queues CSS for inlining
   - {{var variable}} → outputs variable values
   - {{trans "text"}} → translatable strings
   - {{layout handle="..."}} → renders layout blocks
       ↓
5. applyInlineCss() callback:
   - Loads compiled CSS via asset repository
   - Processes CSS placeholders (@base_url_path, @locale)
   - Passes HTML + CSS to Emogrifier (Pelago\Emogrifier\CssInliner)
   - Emogrifier converts CSS selectors to inline style="" attributes
       ↓
6. Final inlined HTML sent via SMTP transport (Symfony Mailer)
```

### Two-File CSS Strategy

Magento splits email CSS into two files because email clients like Gmail strip `<style>` tags:

| File | Purpose | Directive | Processing |
|------|---------|-----------|------------|
| `email-inline.css` (from `email-inline.less`) | Styles that CAN be inlined | `{{inlinecss file="css/email-inline.css"}}` | Emogrifier converts to `style=""` attributes |
| `email.css` (from `email.less`) | Styles that CANNOT be inlined | `{{css file="css/email.css"}}` | Placed in `<style>` tag (media queries, `:hover`, `@font-face`) |

The header template (`header.html`) contains both directives:
```html
<style type="text/css">
    {{var template_styles|raw}}
    {{css file="css/email.css"}}
</style>
<!-- ... later in the template ... -->
{{inlinecss file="css/email-inline.css"}}
```

### The `template_styles` Variable

Each email template can declare per-template styles in a `<!--@styles @-->` comment block at the top:
```html
<!--@styles
.custom-class { color: #333; }
@-->
```
These are injected into the `<style>` tag via `{{var template_styles|raw}}`.

---

## Hyvä Email Module

### Why It Exists

Hyvä replaces the Luma/Blank LESS-based frontend with TailwindCSS. This breaks the LESS file inheritance chain that Magento's email system depends on. The `hyva-themes/magento2-email-module` re-adds the necessary LESS files and creates a fallback specifically for email rendering.

**Module:** `Hyva_Email` (enabled in `app/etc/config.php`)
**Location:** `vendor/hyva-themes/magento2-email-module/src/`

### What It Does

1. **FallbackRulePlugin** - Adds the module's `view/frontend/web` directory to the design fallback so `email.less` and `email-inline.less` are found during static content deployment
2. **PackageFilePlugin** - Treats the module's static files as global scope for proper deployment

### What It Does NOT Do

- Does NOT provide custom email templates (uses default Magento templates)
- Does NOT change the CSS inlining mechanism (still uses Emogrifier)
- Does NOT use TailwindCSS for emails (uses LESS, same as Luma)

### LESS Files Provided

Located at `vendor/hyva-themes/magento2-email-module/src/view/frontend/web/css/`:

| File | Purpose |
|------|---------|
| `email.less` | Master non-inline styles import file |
| `email-inline.less` | Master inline styles import file |
| `email-fonts.less` | @font-face declarations |
| `source/_email-base.less` | Core email stylesheet (resets, layout, typography, tables, buttons) |
| `source/_email-extend.less` | Theme customization file (extend without copying _email-base) |
| `source/_email-variables.less` | Variable overrides for email-specific values |
| `source/_variables.less` | Local theme variable overrides |
| `source/_theme.less` | Global theme variable overrides |
| `source/_typography.less` | @font-face rule generation |

### LESS Import Chain (email-inline.less)

```less
@import 'source/lib/_lib.less';              // Global Magento UI library
@import 'source/lib/variables/_email.less';  // Global email variables
@import 'source/_theme.less';                // Global variable overrides
@import 'source/_variables.less';            // Local theme variables
@import 'source/_email-variables.less';      // Email-specific variables
@import 'source/_email-base.less';           // Core email styles
@import 'source/_email-extend.less';         // Theme customizations
//@magento_import 'source/_email.less';       // Module-specific email styles
```

### How Styles Get Split

`_email-base.less` contains all styles. The build splits them:
- Styles **inside** `.email-non-inline()` and `.media-width()` mixins → `email.css` (in `<style>` tag)
- Styles **outside** those mixins → `email-inline.css` (inlined by Emogrifier)

---

## Theme-Based Email Customization

### Directory Structure

```
app/design/frontend/Uptactics/nto/
├── Magento_Email/
│   ├── email/
│   │   ├── header.html              # Custom email header (wraps ALL emails)
│   │   └── footer.html              # Custom email footer
│   └── web/
│       └── logo_email.png           # Custom email logo
├── Magento_Sales/
│   └── email/
│       ├── order_new.html           # Custom new order email
│       ├── order_new_guest.html     # Custom new order for guests
│       ├── invoice_new.html         # Custom invoice email
│       ├── shipment_new.html        # Custom shipment email
│       └── creditmemo_new.html      # Custom credit memo email
├── Magento_Customer/
│   └── email/
│       ├── account_new.html         # Custom new account email
│       ├── password_new.html        # Custom new password email
│       └── password_reset_confirmation.html
├── Magento_Contact/
│   └── email/
│       └── submitted_form.html      # Custom contact form email
└── web/
    └── css/
        ├── email.less               # Override non-inline styles (optional)
        ├── email-inline.less        # Override inline styles (optional)
        └── source/
            ├── _email-extend.less   # Custom style overrides (recommended)
            ├── _email-variables.less # Custom variable overrides (recommended)
            └── _theme.less          # Global variable overrides
```

### Template Fallback Order

1. **Admin-configured templates** (database `email_template` table) - highest priority
2. **Current theme** (`app/design/frontend/Uptactics/nto/`)
3. **Parent theme** (`vendor/hyva-themes/magento2-default-theme/`)
4. **Hyvä Email module** (`vendor/hyva-themes/magento2-email-module/src/`)
5. **Module default** (`vendor/mage-os/module-*/view/frontend/email/`)

### Override Pattern

Copy the source file to your theme following this path convention:
```
vendor/mage-os/module-{name}/view/frontend/email/{filename}.html
                ↓
app/design/frontend/Uptactics/nto/Magento_{Name}/email/{filename}.html
```

For CSS overrides:
```
vendor/hyva-themes/magento2-email-module/src/view/frontend/web/css/source/_email-extend.less
                ↓
app/design/frontend/Uptactics/nto/web/css/source/_email-extend.less
```

### Common Templates to Override

| Template | Source Module | Source Path |
|----------|-------------|-------------|
| Header | `module-email` | `view/frontend/email/header.html` |
| Footer | `module-email` | `view/frontend/email/footer.html` |
| New Order | `module-sales` | `view/frontend/email/order_new.html` |
| New Order (Guest) | `module-sales` | `view/frontend/email/order_new_guest.html` |
| Invoice | `module-sales` | `view/frontend/email/invoice_new.html` |
| Shipment | `module-sales` | `view/frontend/email/shipment_new.html` |
| Credit Memo | `module-sales` | `view/frontend/email/creditmemo_new.html` |
| New Account | `module-customer` | `view/frontend/email/account_new.html` |
| Password Reset | `module-customer` | `view/frontend/email/password_reset_confirmation.html` |
| Contact Form | `module-contact` | `view/frontend/email/submitted_form.html` |
| Newsletter Sub | `module-newsletter` | `view/frontend/email/subscr_success.html` |

---

## CSS Customization Approaches

### Approach 1: LESS Variable Overrides (Simplest)

Create `app/design/frontend/Uptactics/nto/web/css/source/_email-variables.less`:
```less
// Brand colors
@email__background-color: #f5f5f5;
@email-body__background-color: #ffffff;
@email-body__width: 600px;

// Links
@link__color: #006bb4;
@link__text-decoration: underline;
@link__visited__color: #006bb4;

// Header
@email-header__background-color: #003366;

// Buttons
@button__background-color: #006bb4;
@button__border-color: #006bb4;
@button__color: #ffffff;

// Typography
@font-family__base: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
@font-size__base: 14px;
@heading__color: #333333;
```

### Approach 2: LESS Style Extensions (Moderate)

Create `app/design/frontend/Uptactics/nto/web/css/source/_email-extend.less`:
```less
@import url("@{baseUrl}css/email-fonts.css");

// Custom header styles
.email-header {
    background-color: @email-header__background-color;
}

// Custom button styles
.email-button {
    border-radius: 4px;
    text-transform: uppercase;
    font-weight: bold;
}

// Custom footer
.email-footer {
    border-top: 2px solid @border__color;
    padding-top: 20px;
}
```

### Approach 3: Tailwind-to-LESS Compilation (Advanced)

Use PostCSS to compile Tailwind `@apply` directives into LESS-compatible CSS.

#### Setup

Create `app/design/frontend/Uptactics/nto/web/tailwind/emails/postcss.config.js`:
```javascript
module.exports = {
    plugins: [
        require('postcss-import'),
        require('tailwindcss/nesting'),
        require('tailwindcss')({ config: './emails/tailwind.email.config.js' }),
    ]
}
```

Create `app/design/frontend/Uptactics/nto/web/tailwind/emails/tailwind.email.config.js`:
```javascript
const defaultConfig = require('../tailwind.config.js');

module.exports = {
    ...defaultConfig,
    corePlugins: {
        // CRITICAL: Disable opacity plugins - LESS cannot parse RGBA syntax
        backdropOpacity: false,
        backgroundOpacity: false,
        borderOpacity: false,
        divideOpacity: false,
        ringOpacity: false,
        textOpacity: false
    }
};
```

Create `app/design/frontend/Uptactics/nto/web/tailwind/theme/email.css`:
```css
.footer {
    @apply border-t-2 border-primary;
}

.email-header {
    @apply bg-primary text-white;
}

.btn-primary {
    @apply bg-primary text-white font-bold py-2 px-4 rounded;
}
```

Add build script to `app/design/frontend/Uptactics/nto/web/tailwind/package.json`:
```json
{
    "scripts": {
        "build-email": "npx postcss --config ./emails theme/email.css -o ../css/source/_theme.less"
    }
}
```

#### Build

```bash
cd app/design/frontend/Uptactics/nto/web/tailwind
npm run build-email
```

This outputs `web/css/source/_theme.less` with plain CSS (no Tailwind utilities), which Magento's LESS processor can consume.

**Known constraints:**
- LESS processor cannot parse RGBA syntax (disable opacity plugins)
- Some border utilities (`border-b`, `border-t`) may need explicit CSS fallbacks
- Background image URLs with LESS variables need single quotes: `url('@{baseDir}css/bg.svg')`

---

## Template Directives Reference

| Directive | Usage | Example |
|-----------|-------|---------|
| `{{var name}}` | Output escaped variable | `{{var order.increment_id}}` |
| `{{var name\|raw}}` | Output unescaped HTML | `{{var template_styles\|raw}}` |
| `{{var name\|nl2br}}` | Newlines to `<br>` | `{{var comment\|nl2br}}` |
| `{{trans "text"}}` | Translatable string | `{{trans "Thank you for your order."}}` |
| `{{trans "text %var" var=$val}}` | Translated with variable | `{{trans "Dear %name" name=$customer.name}}` |
| `{{template config_path="..."}}` | Include configured template | `{{template config_path="design/email/header_template"}}` |
| `{{layout handle="..." ...}}` | Render layout block | `{{layout handle="sales_email_order_items" order=$order}}` |
| `{{css file="..."}}` | CSS in `<style>` tag | `{{css file="css/email.css"}}` |
| `{{inlinecss file="..."}}` | CSS for Emogrifier inlining | `{{inlinecss file="css/email-inline.css"}}` |
| `{{depend condition}}` | Conditional block | `{{depend store_phone}}...{{/depend}}` |
| `{{if condition}}` | If/else branching | `{{if order.getIsNotVirtual()}}...{{/if}}` |

### Template Metadata Comments

Every email template starts with metadata:
```html
<!--@subject {{trans "Your %store_name order confirmation" store_name=$store.frontend_name}} @-->
<!--@vars {
"var order.increment_id":"Order ID",
"var order.created_at":"Order Date",
"var billing":"Billing Address HTML"
} @-->
<!--@styles
.custom-table { border: 1px solid #ccc; }
@-->
```

### Available Global Variables

| Variable | Description |
|----------|-------------|
| `$store` | Store object |
| `$store.frontend_name` | Store display name |
| `$store_email` | Support email address |
| `$store_phone` | Store phone number |
| `$store_hours` | Business hours |
| `$logo_url` | Email logo image URL |
| `$logo_alt` | Logo alt text |
| `$logo_width` | Logo width |
| `$logo_height` | Logo height |
| `$template_styles` | Per-template CSS styles |

---

## Emogrifier CSS Inlining

### How It Works

1. `email-inline.less` compiled to `email-inline.css`
2. `{{inlinecss}}` directive loads the compiled CSS
3. Emogrifier receives full HTML + CSS string
4. CSS selectors matched against DOM elements
5. Matched properties written as inline `style=""` attributes
6. Modified HTML returned

### Supported CSS Selectors

- ID selectors (`#id`)
- Class selectors (`.class`)
- Type selectors (`table`, `td`, `p`)
- Descendant selectors (`table td`)
- Child selectors (`table > tr`)
- Adjacent sibling (`h1 + p`)
- Attribute selectors (`[attr]`, `[attr=value]`)

### Unsupported (Must Go in email.css)

- Pseudo-classes (`:hover`, `:first-child`, `:nth-child`)
- Pseudo-elements (`::before`, `::after`)
- Universal selector (`*`)
- Media queries (`@media`)
- `@font-face` declarations
- CSS animations/transitions

---

## HTML Best Practices for Email

### Layout Rules

- Use **table-based layouts** (`<table>`, `<tr>`, `<td>`) - not `<div>` with CSS
- Use **HTML4** elements - many clients don't support HTML5
- Set explicit `width` on tables/images via HTML attribute AND CSS
- Use `cellpadding`, `cellspacing`, `border` attributes on tables
- Avoid `position`, `float`, `flexbox`, `grid`
- Use `align` attribute for centering (not `margin: 0 auto` alone)

### CSS Rules

- Use **CSS2 properties** only - avoid shadows, animations, CSS3
- Use specific properties: `padding-top` not `padding` shorthand
- Use full 6-digit hex colors: `#FFFFFF` not `#FFF`
- Use standard system fonts: Arial, Verdana, Georgia
- Design buttons at minimum **44x44px** for mobile touch targets
- Keep email width at **600px** maximum

### Responsive Design

- Place media queries in `.media-width()` mixins (outputs to `email.css`)
- Use percentage widths for fluid layouts within the 600px container
- Minimum font size 14px for body text
- Test across: Gmail (web/app), Outlook (desktop/web), Apple Mail, Yahoo Mail

---

## Email Logo Customization

### Via Theme File

Place logo at:
```
app/design/frontend/Uptactics/nto/Magento_Email/web/logo_email.png
```

### Via Admin Panel

Navigate to: **Content > Design > Configuration > [Store View] > Transactional Emails**
- Upload logo image (JPG, GIF, PNG; max 2MB)
- Set alt text, width, height

### Retina Support

Provide image at 3x display size. For 200x100px display, upload 600x300px image and set:
- Logo Width: 200
- Logo Height: 100

---

## Build & Deployment

### Compile Email CSS

```bash
# Deploy static content (includes email CSS compilation)
ddev exec bin/magento setup:static-content:deploy -f --area=frontend --theme Uptactics/nto

# Or use composer script
ddev exec composer build-static

# Verify compiled output exists
ls -la pub/static/frontend/Uptactics/nto/en_US/css/email*.css
```

### Clear Caches After Changes

```bash
# Clear view preprocessed (required for LESS changes)
ddev exec rm -rf var/view_preprocessed/*

# Clear static content
ddev exec rm -rf pub/static/frontend/Uptactics/nto/*

# Flush Magento cache
ddev exec bin/magento cache:flush

# Redeploy static content
ddev exec bin/magento setup:static-content:deploy -f --area=frontend --theme Uptactics/nto
```

### Full Email Style Rebuild

```bash
ddev exec rm -rf var/view_preprocessed/* pub/static/frontend/Uptactics/nto/*
ddev exec bin/magento cache:flush
ddev exec bin/magento setup:static-content:deploy -f --area=frontend --theme Uptactics/nto
```

---

## Verifying Email Changes via Mailpit

**IMPORTANT:** Every email styling change MUST be visually verified via Mailpit before considering the change complete. This is a mandatory step in the workflow.

### Mailpit Access

DDEV runs Mailpit internally to capture all outgoing emails. No emails leave the local environment.

- **Browser UI:** `https://ntotank.ddev.site:8443/mailpit/`
- **API Base URL:** `http://127.0.0.1:8025/mailpit/api/v1/`

### Mailpit API Reference

All API calls use the base URL `http://127.0.0.1:8025/mailpit/api/v1/`.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/messages` | GET | List all messages (paginated). Returns `total`, `count`, `messages[]` |
| `/message/{ID}` | GET | Get full message metadata (From, To, Subject, HTML, Text, Size, etc.) |
| `/message/{ID}/html` | GET | Get rendered HTML body only (for visual inspection) |
| `/messages` | DELETE | Delete all messages |
| `/search?query={query}` | GET | Search messages by subject, from, to, or content |

### Verification Workflow

After making any email template or CSS change, follow this process:

#### Step 1: Rebuild and Clear Caches

```bash
ddev exec rm -rf var/view_preprocessed/* pub/static/frontend/Uptactics/nto/*
ddev exec bin/magento cache:flush
ddev exec bin/magento setup:static-content:deploy -f --area=frontend --theme Uptactics/nto
```

#### Step 2: Trigger a Test Email

Place a test order or trigger the relevant transactional email from the admin panel. For order emails, use the admin to create a test order or resend an existing order confirmation.

#### Step 3: Check Mailpit for the Email

```bash
# List all captured emails
curl -s http://127.0.0.1:8025/mailpit/api/v1/messages | python3 -m json.tool

# Get the most recent email's ID and subject
curl -s http://127.0.0.1:8025/mailpit/api/v1/messages | python3 -c "
import sys, json
data = json.load(sys.stdin)
for msg in data['messages']:
    print(f'ID: {msg[\"ID\"]}')
    print(f'Subject: {msg[\"Subject\"]}')
    print(f'From: {msg[\"From\"][\"Name\"]} <{msg[\"From\"][\"Address\"]}>')
    print(f'To: {msg[\"To\"][0][\"Name\"]} <{msg[\"To\"][0][\"Address\"]}>')
    print(f'Date: {msg[\"Created\"]}')
    print('---')
"
```

#### Step 4: Inspect the Email HTML

```bash
# Get full message details (includes HTML, Text, metadata)
curl -s http://127.0.0.1:8025/mailpit/api/v1/message/{MESSAGE_ID} | python3 -m json.tool

# Get just the rendered HTML (for saving/viewing)
curl -s http://127.0.0.1:8025/mailpit/api/v1/message/{MESSAGE_ID}/html > /tmp/email_preview.html
```

#### Step 5: Visual Verification

Open Mailpit in the browser to visually confirm styling:
```
https://ntotank.ddev.site:8443/mailpit/
```

Click on the email to view the rendered HTML. Mailpit displays the email as it would appear in a mail client. Check:
- Logo renders correctly with proper dimensions
- Brand colors are applied (header, buttons, links)
- Typography is consistent (font family, sizes, weights)
- Table layouts are properly structured (order items, totals, addresses)
- Footer content is present and styled
- Responsive layout works (Mailpit supports viewport toggling)

#### Step 6: Verify CSS Inlining

To confirm Emogrifier is properly inlining styles, inspect the raw HTML:

```bash
# Check that inline style attributes are present on elements
curl -s http://127.0.0.1:8025/mailpit/api/v1/message/{MESSAGE_ID}/html | grep -o 'style="[^"]*"' | head -20

# Check for <style> tag content (non-inline styles like media queries)
curl -s http://127.0.0.1:8025/mailpit/api/v1/message/{MESSAGE_ID}/html | grep -oP '<style[^>]*>.*?</style>' | head -5
```

**What to look for:**
- `style=""` attributes on `<body>`, `<table>`, `<td>`, `<p>`, `<a>`, `<h1>`-`<h6>` elements confirm inlining is working
- `<style>` tag should contain media queries and `:hover`/`:visited`/`:active` pseudo-class rules
- No unstyled elements that should have brand colors/fonts applied

### Quick Verification Checklist

After every email style change, confirm ALL of the following:

- [ ] Email captured in Mailpit (check message list)
- [ ] Logo image loads correctly (not broken image icon)
- [ ] Brand colors visible in header area
- [ ] Link colors match brand (not default blue)
- [ ] Button styles applied (background color, text color, border radius)
- [ ] Table layout for order items is properly aligned
- [ ] Totals section (subtotal, shipping, grand total) is formatted
- [ ] Footer text and contact info present
- [ ] Inline `style` attributes present on HTML elements (Emogrifier working)
- [ ] Media queries present in `<style>` tag (responsive styles)

### Admin Preview (Alternative)

Navigate to: **Marketing > Communications > Email Templates**
1. Create a new template (or load default)
2. Click "Preview Template" to see rendered output

Note: Admin preview does NOT process `{{inlinecss}}` or `{{css}}` directives. Mailpit shows the actual rendered email as sent, making it the definitive verification method.

### Cross-Client Testing (Production)

For production readiness, additionally test on these priority clients:
1. **Gmail** (web + mobile app) - strips `<style>` tags, inline only
2. **Outlook** (desktop) - uses Word rendering engine, limited CSS
3. **Apple Mail** (iOS/macOS) - best CSS support
4. **Yahoo Mail** - strips some styles
5. Use **Litmus** or **Email on Acid** for comprehensive cross-client testing

---

## Strict Mode Restrictions (Magento 2.4+)

Custom email templates **cannot** call methods directly on objects. Only scalar values and DataObject `getData()` access are allowed.

### Forbidden (Will Break)

```
{{var order.getCustomerName()}}
{{var subscriber.getConfirmationLink()}}
```

### Allowed

```
{{var order_data.customer_name}}
{{var subscriber_data.confirmation_link}}
```

### Check Compatibility

```bash
ddev exec bin/magento dev:email:override-compatibility-check
ddev exec bin/magento dev:email:newsletter-compatibility-check
```

---

## Troubleshooting

### "LESS file is empty" Error

```
CSS inlining error: Compilation from source: LESS file is empty: frontend/.../css/email-inline.less
```

**Cause:** Hyvä theme doesn't have LESS files in its inheritance chain.
**Fix:** Ensure `Hyva_Email` module is enabled:
```bash
ddev exec bin/magento module:status Hyva_Email
ddev exec bin/magento module:enable Hyva_Email
ddev exec bin/magento setup:upgrade
```

### Styles Not Appearing in Emails

1. Clear preprocessed files: `ddev exec rm -rf var/view_preprocessed/*`
2. Clear static content: `ddev exec rm -rf pub/static/frontend/Uptactics/nto/*`
3. Redeploy: `ddev exec bin/magento setup:static-content:deploy -f --area=frontend`
4. Flush cache: `ddev exec bin/magento cache:flush`
5. Verify compiled CSS exists: `ls pub/static/frontend/Uptactics/nto/en_US/css/email*.css`

### Emogrifier Not Inlining Styles

- Verify selectors are supported (no pseudo-classes, no `*`)
- Check that styles are in `email-inline.less`, not `email.less`
- Ensure HTML elements have matching classes/IDs
- In developer mode, Emogrifier outputs debug info

### Template Overrides Not Loading

1. Verify file path matches convention: `Magento_{ModuleName}/email/{filename}.html`
2. Check file permissions are readable
3. Run `ddev exec bin/magento cache:flush`
4. Check if admin has a custom template configured (database overrides take priority)

---

## Key File Locations

### Core Engine
- `vendor/mage-os/module-email/Model/AbstractTemplate.php` - Template loading & processing
- `vendor/mage-os/module-email/Model/Template/Filter.php` - Directive processing (1,145 lines)
- `vendor/mage-os/framework/Css/PreProcessor/Adapter/CssInliner.php` - Emogrifier wrapper

### Hyvä Email Module
- `vendor/hyva-themes/magento2-email-module/src/view/frontend/web/css/` - LESS source files
- `vendor/hyva-themes/magento2-email-module/src/Plugin/FallbackRulePlugin.php` - Design fallback
- `vendor/hyva-themes/magento2-email-module/src/Plugin/PackageFilePlugin.php` - Static deployment

### Default Templates
- `vendor/mage-os/module-email/view/frontend/email/header.html` - Email header
- `vendor/mage-os/module-email/view/frontend/email/footer.html` - Email footer
- `vendor/mage-os/module-sales/view/frontend/email/` - All sales email templates (16 templates)
- `vendor/mage-os/module-customer/view/frontend/email/` - Customer email templates
- `vendor/mage-os/module-contact/view/frontend/email/` - Contact form template

### Template Registration
- `vendor/mage-os/module-email/etc/email_templates.xml` - Header/footer template IDs
- `vendor/mage-os/module-sales/etc/email_templates.xml` - Sales template IDs (16 templates)
- `vendor/mage-os/module-customer/etc/email_templates.xml` - Customer template IDs

### Compiled Output
- `pub/static/frontend/Uptactics/nto/en_US/css/email.css` - Non-inline styles
- `pub/static/frontend/Uptactics/nto/en_US/css/email-inline.css` - Inline styles
- `pub/static/frontend/Uptactics/nto/en_US/css/email-fonts.css` - Font declarations

### Admin Configuration
- **Content > Design > Configuration > Transactional Emails** - Logo, header/footer template selection
- **Marketing > Communications > Email Templates** - Create/edit custom templates
- **Stores > Configuration > Sales > Sales Emails** - Enable/disable specific email types

---

## References

- [Adobe Commerce - Email Templates](https://developer.adobe.com/commerce/frontend-core/guide/templates/email)
- [Adobe Commerce - Email Template Migration (Strict Mode)](https://developer.adobe.com/commerce/frontend-core/guide/templates/email-migration/)
- [Hyvä Docs - Styling Emails](https://docs.hyva.io/hyva-themes/building-your-theme/styling-emails.html)
- [Hyvä Docs - Styling Emails with Tailwind CSS](https://docs.hyva.io/hyva-themes/building-your-theme/styling-emails-with-tailwind.html)
- [GitHub - hyva-themes/magento2-email-module](https://github.com/hyva-themes/magento2-email-module)
- [Emogrifier Library](https://github.com/MyIntervals/emogrifier)
