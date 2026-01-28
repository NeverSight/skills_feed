---
name: hyva-cms-component
description: Create custom Hyvä CMS component. This skill should be used when the user wants to create a new Hyvä CMS component, build a Hyvä component, or needs help with components.json and PHTML templates for Hyvä CMS. Trigger phrases include "create hyva cms component", "add cms component", "new hyva component", "build page hyva cms element", "custom cms element".
---

# Hyvä CMS Component Creator

## Overview

This skill guides the interactive creation of custom Hyvä CMS components for Magento 2. It supports creating components in new or existing modules, with field presets for common patterns and automatic setup:upgrade execution.

**Command execution:** For commands that need to run inside the development environment (e.g., `bin/magento`), use the `hyva-exec-shell-cmd` skill to detect the environment and determine the appropriate command wrapper.

## Workflow

### Step 1: Module Selection

If not already specified in the prompt, ask the user where to create the component:

**Option A: New Module**

Ask for both values (do not assume defaults without asking):
1. **Vendor name** (e.g., `Acme`) - Required, no default. Do not suggest a Vendor name, prompt for user input.
2. **Module name** - Suggest `CmsComponents` as default so user can press Enter to accept

Then use the `hyva-create-module` skill with:
  - `dependencies`: `["Hyva_CmsBase"]`
  - `composer_require`: `{"hyva-themes/commerce-module-cms": "^1.0"}`

**Option B: Existing Module**
- Request the module path (can be in `app/code/`, `vendor/`, or custom location)
- Verify the module has `Hyva_CmsBase` as a dependency in `etc/module.xml`. If not present, add it.
- Verify the module has `hyva-themes/commerce-module-cms` as a dependency in `composer.json`. If not present, add it.

### Step 2: Component Details

Gather component information:

1. **Component name** (snake_case, e.g., `feature_card`)
2. **Label** (display name in editor, e.g., "Feature Card")
3. **Category** (Layout, Elements, Media, Content, or Other)
4. **Icon** - Automatically select an appropriate icon:

   **Step 4a: Identify icons already in use**
   Use the `hyva-cms-components-dump` skill to dump all current CMS components. Extract all `icon` values from the output to build a list of icons already in use by existing components.

   **Step 4b: Find available lucide icons**
   List the SVG files in `vendor/hyva-themes/magento2-theme-module/src/view/base/web/svg/lucide/` to get the full set of available icons.

   **Step 4c: Select the best fitting icon**
   From the available lucide icons that are NOT already in use by another component:
   - Choose the icon whose name best matches the purpose/meaning of the new component
   - Consider semantic meaning (e.g., `shopping-cart.svg` for cart-related, `image.svg` for image-related, `layout-grid.svg` for grid layouts)
   - Format the selected icon as `Hyva_Theme::svg/lucide/[icon-name].svg`

   If no suitable unused icon can be found, or if the lucide directory doesn't exist, leave the `icon` property unset.

### Step 3: Field Selection

Offer field presets or custom field creation. See `references/field-types.md` "Field Presets" section for available presets (Basic Card, Image Card, CTA Block, Text Block, Feature Item, Testimonial, Accordion Item) or allow custom field definition.

For custom fields, iterate through each field asking:
1. Field name (snake_case)
2. Field type (see `references/field-types.md`)
3. Label
4. Default value (optional)
5. Required? (yes/no)
6. Any additional attributes

### Step 4: Variant Support

Ask if the component needs template variants:

- If **yes**: Gather variant names and labels (e.g., default, compact, wide). See `references/variant-support.md` for configuration details.
- If **no**: Use single template

### Step 5: Generate Files

Create the required files:

#### For New Modules

The `hyva-create-module` skill creates the base module structure. Then add the CMS-specific directories:

```
app/code/[Vendor]/[Module]/
├── registration.php          # Created by hyva-create-module
├── composer.json             # Created by hyva-create-module
├── etc/
│   ├── module.xml            # Created by hyva-create-module
│   └── hyva_cms/
│       └── components.json   # Create this
└── view/
    └── frontend/
        └── templates/
            └── elements/
                └── [component-name].phtml (or [component-name]/ for variants)
```

#### For Existing Modules

Create or update:
- `etc/hyva_cms/components.json` (merge with existing if present)
- `view/frontend/templates/elements/[component-name].phtml`

### Step 6: Run Setup

After creating files, run `bin/magento setup:upgrade` using the appropriate command wrapper detected by the `hyva-exec-shell-cmd` skill.

## File Generation Details

### components.json Structure

```json
{
    "[component_name]": {
        "label": "[Label]",
        "category": "[Category]",
        "template": "[Vendor]_[Module]::elements/[component-name].phtml",
        "content": {
            // Generated fields
        },
        "design": {
            "includes": [
                "Hyva_CmsBase::etc/hyva_cms/default_design.json",
                "Hyva_CmsBase::etc/hyva_cms/default_design_typography.json"
            ]
        },
        "advanced": {
            "includes": [
                "Hyva_CmsBase::etc/hyva_cms/default_advanced.json"
            ]
        }
    }
}
```

### Valid Component Properties

**IMPORTANT:** Only specific properties are allowed at the component level. See `references/component-schema.md` for the complete schema reference.

Key properties: `label` (required), `category`, `template`, `icon`, `children`, `require_parent`, `content`, `design`, `advanced`, `disabled`, `custom_properties`.

**Invalid properties that will cause schema errors:**
- `hidden` - Does not exist. Use `require_parent: true` for child-only components, or `disabled: true`
- Any property not listed in the schema reference

### Child-Only Components

For components that should only be used as children of other components (like list items), use `require_parent: true`:

```json
{
    "my_list_item": {
        "label": "My List Item",
        "category": "Elements",
        "require_parent": true,
        "template": false,
        "content": {
            "title": {"type": "text", "label": "Title"}
        }
    },
    "my_list": {
        "label": "My List",
        "category": "Elements",
        "template": "Vendor_Module::elements/my-list.phtml",
        "children": {
            "config": {
                "accepts": ["my_list_item"]
            }
        }
    }
}
```

When `template: false`, the parent component renders the child data directly (NOT using `$block->createChildHtml()`). See "Rendering Children with template: false" below.

### PHTML Template Structure

Every template must start with this header:

```php
<?php
declare(strict_types=1);

use Hyva\CmsLiveviewEditor\Block\Element;
use Hyva\Theme\Model\ViewModelRegistry;
use Magento\Framework\Escaper;

/** @var Element $block */
/** @var Escaper $escaper */
/** @var ViewModelRegistry $viewModels */
```

Additional requirements:
1. `$block->getEditorAttrs()` on root element
2. `$block->getEditorAttrs('field_name')` on editable elements
3. Proper escaping with `$escaper->escapeHtml()` and `$escaper->escapeHtmlAttr()`

### Template Patterns by Field Type

**Text fields:**
```php
$title = $block->getData('title');
// In template:
<?php if ($title): ?>
    <h2 <?= /** @noEscape */ $block->getEditorAttrs('title') ?>>
        <?= $escaper->escapeHtml($title) ?>
    </h2>
<?php endif; ?>
```

**Richtext/HTML fields:**
```php
$content = $block->getData('content');
// In template (no escaping for richtext):
<?php if ($content): ?>
    <div <?= /** @noEscape */ $block->getEditorAttrs('content') ?>>
        <?= /** @noEscape */ $content ?>
    </div>
<?php endif; ?>
```

**Image fields:**

Use the `hyva-render-media-image` skill for rendering images. It provides the complete API reference and code patterns for the `\Hyva\Theme\ViewModel\Media` view model.

Add these imports when rendering images:

```php
// Additional imports for templates with images:
use Hyva\Theme\ViewModel\Media;

/** @var Media $mediaViewModel */
$mediaViewModel = $viewModels->require(Media::class);
```

The data from `$block->getData('image')` can be passed directly to `getResponsivePictureHtml()`:

```php
$image = $block->getData('image');

// In template:
<?php if ($image): ?>
    <?= /** @noEscape */ $mediaViewModel->getResponsivePictureHtml(
        $image,
        ['class' => 'w-full h-auto', 'loading' => 'lazy']
    ) ?>
<?php endif; ?>
```

For responsive images with separate desktop and mobile sources, see the `hyva-render-media-image` skill.

**Link fields:**
```php
$link = $block->getData('link');
$linkData = $link ? $block->getLinkData($link) : null;
// In template:
<?php if ($linkData): ?>
    <a href="<?= $escaper->escapeUrl($linkData['url']) ?>"
       <?php if (!empty($linkData['target'])): ?>target="<?= $escaper->escapeHtmlAttr($linkData['target']) ?>"<?php endif; ?>>
        <?= $escaper->escapeHtml($linkData['title'] ?: 'Read more') ?>
    </a>
<?php endif; ?>
```

**Boolean fields:**
```php
$showTitle = (bool) $block->getData('show_title');
// In template:
<?php if ($showTitle && $title): ?>
    <!-- title markup -->
<?php endif; ?>
```

**Select fields:**
```php
$style = $block->getData('style') ?: 'default';
$styleClasses = match($style) {
    'primary' => 'bg-blue-600 text-white',
    'secondary' => 'bg-gray-200 text-gray-800',
    default => 'bg-white text-gray-600'
};
```

**Children fields (with their own templates):**

When child components have their own templates (default behavior), use `$block->createChildHtml()`:

```php
$children = $block->getData('children') ?: [];
// In template:
<?php foreach ($children as $index => $child): ?>
    <?= /** @noEscape */ $block->createChildHtml($child, 'child-' . $index) ?>
<?php endforeach; ?>
```

**Rendering Children with `template: false`:**

When child components have `"template": false`, the parent component renders them directly. Child data is **flat** - field values are directly on the child array, NOT nested under a `content` key.

```php
$children = $block->getData('children') ?: [];

// In template - iterate and access child data directly:
<?php foreach ($children as $elementData): ?>
    <?php
    // Access fields directly on $elementData (NOT $elementData['content']['field'])
    $image = $elementData['image'] ?? null;
    $title = $elementData['title'] ?? '';
    $description = $elementData['description'] ?? '';

    // Each child has a 'uid' for editor attributes
    $childUid = $elementData['uid'];
    ?>
    <div <?= /** @noEscape */ $block->getEditorAttrs('', $childUid) ?>>
        <?php if (!empty($image['src'])): ?>
            <?php // For image rendering patterns, see the hyva-render-media-image skill ?>
            <?= /** @noEscape */ $mediaViewModel->getResponsivePictureHtml(
                [$block->getResponsiveImageData($image)],
                ['alt' => $image['alt'] ?? '', 'class' => 'w-full h-auto', 'loading' => 'lazy']
            ) ?>
        <?php endif; ?>
        <p <?= /** @noEscape */ $block->getEditorAttrs('title', $childUid) ?>>
            <?= $escaper->escapeHtml($title) ?>
        </p>
    </div>
<?php endforeach; ?>
```

**Key points for `template: false` children:**
- Child field data is flat: use `$elementData['field_name']`, NOT `$elementData['content']['field_name']`
- Each child has a `uid` property for editor attributes
- Use `$block->getEditorAttrs('field_name', $childUid)` to enable live editing of child fields
- Use `$block->getEditorAttrs('', $childUid)` on the child's root element
- For images, check `!empty($image['src'])` and use `$block->getResponsiveImageData($image)` to process the image data
- For advanced image rendering patterns (responsive breakpoints, etc.), see the `hyva-render-media-image` skill

## Resources

### references/example-component.md

Complete end-to-end example showing a Feature Card component with:
- Full `components.json` definition
- Matching PHTML template with all field types
- Supporting module files (registration.php, module.xml, composer.json)
- Directory structure overview

Read this file when you need a reference for how all the pieces fit together.

### references/component-schema.md

Complete schema reference for component declarations, auto-generated from the Hyvä CMS JSON schema. Includes:
- Valid component-level properties
- Field declaration properties
- All field types
- Validation attributes

Read this file when validating component structure or when encountering schema validation errors.

Run `scripts/update_component_schema.php` after Hyvä CMS updates to regenerate.

### references/field-types.md

Complete reference for all supported field types including:
- Field configuration syntax
- All available field types with examples
- Validation attributes
- Conditional visibility (show_if/hide_if)
- Field presets for common patterns

Read this file when generating field configurations.

### references/variant-support.md

Guide for implementing template variants including:
- Directory structure for variant templates
- Variant field configuration in components.json
- Template implementation patterns
- Common variant patterns and best practices

Read this file when the user wants multiple layout options for a component.

### references/troubleshooting.md

Solutions for common issues including:
- Schema validation errors
- Component not visible in editor
- Template not rendering
- Live editor not working
- Image display issues
- Fallbacks when dependent skills are unavailable

Read this file when encountering errors during component creation or testing.

### scripts/update_component_schema.php

PHP script that reads the Hyvä CMS JSON schema files and regenerates `references/component-schema.md`. Run after upgrading `hyva-themes/commerce-module-cms` to ensure documentation stays current.

### assets/templates/component/template.phtml.tpl

Base PHTML structure for CMS components.

Placeholders:
- `{{CONTENT_FIELDS}}` - PHP variable declarations
- `{{TEMPLATE_BODY}}` - HTML template content

## Important Guidelines

1. **Always use `getEditorAttrs()`** on the root element and on each editable field element
2. **Never use `<script>` tags** in templates - use Alpine.js via `alpine:init` event
3. **Escape all user content** with appropriate escaper methods
4. **Use meaningful default values** for better merchant experience
5. **Include design/advanced sections** via includes for consistency
6. **Validate component names** are snake_case with only lowercase letters, numbers, and underscores

<!-- Copyright © Hyvä Themes https://hyva.io. All rights reserved. Licensed under OSL 3.0 -->
