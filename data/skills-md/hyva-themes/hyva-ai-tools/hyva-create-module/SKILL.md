---
name: hyva-create-module
description: Create a new Magento 2 module in app/code/. This skill should be used when the user wants to create a module, scaffold a new module, generate module boilerplate, or set up a custom module. It handles registration.php, composer.json, module.xml generation with configurable dependencies. Trigger phrases include "create module", "new module", "scaffold module", "generate module".
---

# Create Magento 2 Module

This utility skill creates new Magento 2 modules in `app/code/`. It is designed to be called by other skills that need module scaffolding.

**Command execution:** For commands that need to run inside the development environment (e.g., `bin/magento`), use the `hyva-exec-shell-cmd` skill to detect the environment and determine the appropriate command wrapper.

## Parameters

When invoking this skill, the calling skill should provide:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `vendor` | Yes | Vendor name in PascalCase (e.g., `Acme`) |
| `module` | Yes | Module name in PascalCase (e.g., `CustomFeature`) |
| `description` | No | Module description for composer.json (default: "[Vendor] [Module] module") |
| `dependencies` | No | Array of module dependencies for `<sequence>` in module.xml |
| `composer_require` | No | Object of composer requirements (package: version) |

## Workflow

### Step 1: Validate Input

- Verify vendor name is PascalCase (starts with uppercase, alphanumeric only)
- Verify module name is PascalCase
- Check that `app/code/{Vendor}/{Module}` does not already exist

### Step 2: Create Directory Structure

```
app/code/{Vendor}/{Module}/
├── registration.php
├── composer.json
└── etc/
    └── module.xml
```

### Step 3: Generate Files

#### registration.php

Use template `assets/templates/registration.php.tpl`:
- Replace `{{VENDOR}}` with vendor name
- Replace `{{MODULE}}` with module name

#### composer.json

Use template `assets/templates/composer.json.tpl`:
- Replace `{{VENDOR}}` with vendor name (PascalCase)
- Replace `{{MODULE}}` with module name (PascalCase)
- Replace `{{vendor_kebabcase}}` with kebab-case, hyphenated vendor name
- Replace `{{module_kebabcase}}` with kebab-case, hyphenated module name
- Replace `{{DESCRIPTION}}` with description
- Add entries from `composer_require` parameter to the `require` section

#### module.xml

Use template `assets/templates/module.xml.tpl`:
- Replace `{{VENDOR}}` with PascalCase vendor name
- Replace `{{MODULE}}` with PascalCase module name
- Replace `{{SEQUENCE}}` with `<sequence>` block containing dependencies, or empty string if none

### Step 4: Run Setup (Optional)

If the calling skill requests it, run `bin/magento setup:upgrade` using the `hyva-exec-shell-cmd` skill for the appropriate wrapper.

## Error Handling

Abort module creation and report the error to the calling skill when:

| Condition | Action |
|-----------|--------|
| Vendor name not PascalCase | Report: "Invalid vendor name '{name}': must start with uppercase letter and contain only alphanumeric characters" |
| Module name not PascalCase | Report: "Invalid module name '{name}': must start with uppercase letter and contain only alphanumeric characters" |
| Directory already exists | Report: "Module already exists at app/code/{Vendor}/{Module}" |
| Cannot create directory | Report: "Failed to create directory app/code/{Vendor}/{Module}: {error}" |
| Cannot write file | Report: "Failed to write {filename}: {error}" |

If `hyva-exec-shell-cmd` skill is unavailable when Step 4 is requested, skip the setup:upgrade step and report: "Skipped setup:upgrade - hyva-exec-shell-cmd skill not available. Run manually: bin/magento setup:upgrade"

## Template Placeholders

| Placeholder            | Description | Example |
|------------------------|-------------|---------|
| `{{VENDOR}}`           | Vendor name (PascalCase) | `Acme` |
| `{{MODULE}}`           | Module name (PascalCase) | `CustomFeature` |
| `{{vendor_kebabcase}}` | Vendor name (kebab-case, split on capitals) | `acme` |
| `{{module_kebabcase}}` | Module name (kebab-case, split on capitals) | `custom-feature` |
| `{{DESCRIPTION}}`      | Module description | `Acme CustomFeature module` |
| `{{SEQUENCE}}`         | Module sequence XML or empty | `<sequence><module name="Magento_Catalog"/></sequence>` |

### PascalCase to kebab-case Conversion

Convert module names by inserting a hyphen before each capital letter and lowercasing:

| PascalCase | kebab-case |
|------------|------------|
| `CustomFeature` | `custom-feature` |
| `ShoppingCartGraphQl` | `shopping-cart-graph-ql` |
| `CmsComponents` | `cms-components` |
| `MyModule` | `my-module` |

## Usage by Other Skills

Skills should reference this skill for module creation:

```
To create the module, use the `hyva-create-module` skill with:
- vendor: "Acme"
- module: "CmsComponents"
- dependencies: ["Hyva_CmsBase"]
- composer_require: {"hyva-themes/commerce-module-cms": "*"}
```

## Example Output

For vendor `Acme`, module `CmsComponents`, with `Hyva_CmsBase` dependency:

**app/code/Acme/CmsComponents/registration.php:**
```php
<?php
declare(strict_types=1);

use Magento\Framework\Component\ComponentRegistrar;

ComponentRegistrar::register(ComponentRegistrar::MODULE, 'Acme_CmsComponents', __DIR__);
```

**app/code/Acme/CmsComponents/composer.json:**
```json
{
    "name": "acme/module-cms-components",
    "description": "Acme CmsComponents module",
    "type": "magento2-module",
    "require": {
        "php": ">=8.1",
        "hyva-themes/commerce-module-cms": "*"
    },
    "autoload": {
        "files": ["registration.php"],
        "psr-4": {
            "Acme\\CmsComponents\\": ""
        }
    }
}
```

**app/code/Acme/CmsComponents/etc/module.xml:**
```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework:Module/etc/module.xsd">
    <module name="Acme_CmsComponents">
        <sequence>
            <module name="Hyva_CmsBase"/>
        </sequence>
    </module>
</config>
```

<!-- Copyright © Hyvä Themes https://hyva.io. All rights reserved. Licensed under OSL 3.0 -->
