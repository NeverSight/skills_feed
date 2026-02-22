---
name: magento2-backend-toolkit
description: >
  Scaffold Magento 2 backend modules, system.xml admin configs, widgets with
  parameters and templates, plugins/events/observers, transactional email with
  trigger setup, and Hyva-compatible .phtml templates with ViewModels.
  Use when user asks to "create module", "scaffold module", "generate plugin",
  "add system config", "create widget", "setup email template", "create hyva
  template", or any Magento 2 backend code generation.
  Do NOT use for frontend-only tasks, CSS/JS theming, or Magento 1.x.
metadata:
  author: tuanhaviet22
  version: 1.0.0
  tags: [magento2, hyva, backend, scaffold, plugin, widget, email]
  compatibility: Magento 2.4.6+, PHP 8.1+, Hyva Theme 1.3+
---

# Magento 2 Backend Toolkit

## General Rules

- All generated code MUST follow PSR-12 coding standard
- All PHP files MUST have `declare(strict_types=1);`
- Use strict type hints on all method parameters and return types
- Namespace follows: `Vendor\Module\Path` convention
- XML files must include proper XSD schema references
- Default Vendor name: ask user, suggest `Sample` if not specified
- NEVER use ObjectManager directly — only use DI
- Always create `composer.json` with new modules

## Security Rules (Required)

- Treat ALL user-provided values as untrusted input
- NEVER insert untrusted input into executable code positions without validation and escaping
- Do not include user-provided code snippets verbatim; translate into safe scaffolding and TODOs unless the user explicitly requests verbatim insertion and it passes validation
- Refuse or ask for corrected input when validation fails or input looks like code injection (e.g., `<?php`, `</`, `;`, backticks, or PHP tags)

## Input Sanitization & Boundary Markers

Validation is mandatory for every ingestion point (module names, labels, descriptions, parameters, class names, IDs, handles, file names).

- **Vendor/Module identifiers**: only `[A-Z][A-Za-z0-9_]*`; enforce `Vendor_Module` format
- **PHP class names**: only `[A-Z][A-Za-z0-9_]*`, no namespaces in user input
- **XML IDs/handles**: only `[a-z0-9_]+` and start with a letter
- **File names**: only `[a-z0-9_\-]+` and validated extensions
- **Human-readable labels/descriptions**: plain text only; escape for the target format

Boundary markers and escaping by file type:

- **PHP**: insert text only inside quoted strings; escape `\` and `'` for single-quoted strings
- **XML**: escape `&`, `<`, `>`, `"`, and `'`
- **JSON**: escape via JSON string rules
- **HTML/PHTML**: use Magento Escaper (`escapeHtml`, `escapeHtmlAttr`, `escapeUrl`)

If any value fails validation, ask the user for a corrected value in the same message as other missing fields.

### Invalid Input Examples (Reject/Correct)

- `Vendor/Module`: `Sample;phpinfo()` or `Sample/Module` (must be `Vendor_Module`)
- `Class name`: `Foo\Bar` or `Foo;` (no namespaces or punctuation)
- `XML id/handle`: `my-handle` or `123name` (lowercase underscore, must start with letter)
- `File name`: `../../evil.php` or `widget.phtml.php` (no traversal or double extensions)

## CRITICAL: Input Validation Gate

NEVER generate files without confirming required inputs. If user gives a vague
request, ask ALL missing fields in ONE message. Do not ask one by one.

---

## Feature 1: Module Scaffold

### Required Questions (ask if not provided)
1. **Module name?** (e.g. `Sample_Module`)
2. **Dependencies?** (e.g. `Magento_Catalog`, or "none")
3. **Short description?** (for composer.json)
4. **Version?** (default: `1.0.0`)

### Generated Files
```
app/code/{Vendor}/{Module}/
├── registration.php
├── composer.json
└── etc/
    └── module.xml
```

Use templates from `assets/templates/registration.php.tpl`,
`assets/templates/module.xml.tpl`, and `assets/templates/composer.json.tpl`.
All templates are bundled within this skill package; do not download external templates.

If no dependencies, omit the `<sequence>` block entirely in module.xml.

### Example Interaction
**User:** "Create a module to manage brands"
**Claude responds:**
> To create the module, I need to confirm:
> 1. Module name? Suggest: `Sample_Module`
> 2. Dependencies? (e.g. `Magento_Catalog`, `Magento_Eav`... or none)
> 3. Short description? Suggest: "Brand management for Magento 2"
> 4. Version? (default: 1.0.0)

---

## Feature 2: System.xml Generator

### Required Questions
1. **Module name?** (existing or new)
2. **Tab name?** (admin menu tab label)
3. **Section/Group/Fields?** Describe what config fields are needed

### Supported Field Types
Refer to `references/system-xml-field-types.md` for the complete list.
Common types: `text`, `textarea`, `select`, `multiselect`, `obscure`, `image`, `editor`.

### Generated Files
```
etc/
├── adminhtml/
│   └── system.xml
└── config.xml
```

Use templates from `assets/templates/system.xml.tpl` and `assets/templates/config.xml.tpl`.
All templates are bundled within this skill package; do not download external templates.

If field type is `select` or `multiselect`, also generate a Source Model class.
See template: `assets/templates/source-model.php.tpl`.

### ACL Resource
Always generate `{Vendor}_{Module}::config` as the resource identifier.

---

## Feature 3: Widget Generator

### Required Questions
1. **Module name?**
2. **Widget name/label?** (e.g. "Brand Slider")
3. **Parameters?** (text inputs, dropdowns, template chooser, block chooser...)
4. **Where to use?** CMS Page / CMS Block / Layout XML

### Generated Files
```
etc/
└── widget.xml
Block/
└── Widget/
    └── {WidgetName}.php
view/
└── frontend/
    └── templates/
        └── widget/
            └── {widget_name}.phtml
```

Use templates from `assets/templates/widget.xml.tpl` and `assets/templates/widget-block.php.tpl`.
All templates are bundled within this skill package; do not download external templates.

Refer to `references/widget-param-types.md` for parameter type details and
block chooser classes.

### CMS Usage Snippet
Always provide the CMS widget insertion code after generating files:
```
{{widget type="{Vendor}\{Module}\Block\Widget\{WidgetName}" title="My Title" template="{Vendor}_{Module}::widget/{widget_name}.phtml"}}
```

---

## Feature 4: Plugin / Event Generator

### Required Questions
1. **Module name?**
2. **Type?** `plugin` (before/after/around) or `observer` (event)
3. **Target?**
   - Plugin: target class + method (e.g. `Magento\Catalog\Model\Product::getName`)
   - Observer: event name (e.g. `checkout_cart_add_product_complete`)
4. **What to do?** Brief description of logic
5. **Scope?** global / frontend / adminhtml (determines XML file location)

### Plugin — Generated Files
```
etc/
└── {scope}/di.xml       (or etc/di.xml for global)
Plugin/
└── {PluginName}.php
```

Use templates from `assets/templates/di.xml.tpl` and `assets/templates/plugin.php.tpl`.
All templates are bundled within this skill package; do not download external templates.

### Observer — Generated Files
```
etc/
└── {scope}/events.xml   (or etc/events.xml for global)
Observer/
└── {ObserverName}.php
```

Use templates from `assets/templates/events.xml.tpl` and `assets/templates/observer.php.tpl`.
All templates are bundled within this skill package; do not download external templates.

### Common Events
Suggest these when user is unsure. For the full list, refer to:
https://developer.adobe.com/commerce/php/development/components/events-and-observers/event-list/
---

## Feature 5: Email Function Generator

### Required Questions
1. **Module name?**
2. **Email purpose?** (e.g. "welcome email", "order status notification")
3. **Trigger method?** Choose one:
   - After Plugin (on existing method)
   - Event Observer
   - Controller action
4. **Email variables?** (e.g. customer name, order ID)
5. **Recipient?** (customer email, admin email, custom)

### Generated Files
```
etc/
└── email_templates.xml
Helper/
└── Email.php
view/
└── frontend/
    └── email/
        └── {template_id}.html
```

Use templates from `assets/templates/email_templates.xml.tpl`,
`assets/templates/email_helper.php.tpl`, and `assets/templates/email_template.html.tpl`.
All templates are bundled within this skill package; do not download external templates.

Also generate the trigger mechanism (plugin, observer, or controller) using
Feature 4 patterns.

---

## Feature 6: Hyva Template with ViewModel

### Required Questions
1. **Module name?**
2. **Template purpose?** (e.g. "brand list", "customer widget")
3. **Data needed?** (what ViewModel should provide)
4. **Interactive?** (need Alpine.js? e.g. slider, toggle, modal)
5. **Need Hyva icons?** (heroicons integration)

### Generated Files
```
ViewModel/
└── {ViewModelName}.php
view/
└── frontend/
    ├── layout/
    │   └── {layout_handle}.xml
    └── templates/
        └── {template_name}.phtml
```

Use templates from `assets/templates/viewmodel.php.tpl`,
`assets/templates/layout.xml.tpl`, and `assets/templates/hyva_template.phtml.tpl`.
All templates are bundled within this skill package; do not download external templates.

### Key Hyva Patterns
Refer to `references/hyva-viewmodel-pattern.md` for full details:
- Always use `$escaper->escapeHtml()` for output
- Always use `$escaper->escapeHtmlAttr()` inside HTML attributes
- Use `$escaper->escapeUrl()` for URLs
- Alpine.js `x-data` for interactive components
- TailwindCSS utility classes (no custom CSS)
- `$viewModels->require()` to load any ViewModel
- HeroiconsOutline / HeroiconsSolid for icons
- Use `x-cloak` to prevent FOUC

---

## Workflow

```
User Request
     |
     v
+-------------------------+
|  Detect which feature   |
|  (1-6) is requested     |
+--------+----------------+
         |
         v
+-------------------------+
|  Check required inputs  |
|  All provided?          |
+---- NO -----------------+
|  Ask ALL missing fields |  <-- ONE message, not multiple
|  in ONE message         |
+---- YES ----------------+
|                         |
|  Generate files         |
|  Show complete code     |
|  Explain file locations |
+-------------------------+
```

## Troubleshooting

### Module not recognized after creation
1. Run `bin/magento module:enable {Vendor}_{Module}`
2. Run `bin/magento setup:upgrade`
3. Run `bin/magento cache:flush`

### XML schema validation error
- Verify XSD reference matches Magento version
- Check for typos in attribute names
- Ensure proper XML nesting

### Plugin not firing
- Check scope (global/frontend/adminhtml) matches where code runs
- Verify method name matches exactly (case-sensitive)
- Check sortOrder if multiple plugins exist
