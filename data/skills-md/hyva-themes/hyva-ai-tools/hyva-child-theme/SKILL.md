---
name: hyva-child-theme
description: Create a Hyvä child theme in a Magento 2 project. This skill should be used when the user wants to create a new Hyvä child theme, set up a custom theme based on Hyvä, or initialize a new frontend theme directory structure. Trigger phrases include "create hyva child theme", "new hyva theme", "setup child theme", "create custom theme", "initialize theme".
---

# Hyvä Child Theme Creator

This skill creates a complete Hyvä child theme with the proper directory structure, configuration files, and Tailwind CSS build setup.

**Command execution:** For commands that need to run inside the development environment (e.g., `bin/magento`), use the `hyva-exec-shell-cmd` skill to detect the environment and determine the appropriate command wrapper.

## Workflow

### Step 1: Gather Theme Information

Prompt the user to provide the following information:

**Vendor Name**: The vendor/company namespace (e.g., "Acme", "MyCompany")
- Must be PascalCase
- Used in composer package name and directory structure
- If there are existing Vendor name folders in app/design/frontend or app/code/ offer those in lower case as suggestions

**Theme Name**: The name of the theme (e.g., "customTheme", "StoreTheme")
- Must be PascalCase or camelCase
- Used in theme registration and directory name
- Must not be present as a subdirectory in app/design/frontend 

### Step 2: Detect Parent Theme

If the user has specified a parent theme, use that. The parent can be:
- A Hyvä default theme: `Hyva/default-csp` or `Hyva/default`
- An existing Hyvä child theme: `{Vendor}/{ThemeName}` from `app/design/frontend/`

If the user has NOT specified a parent theme, discover available options by invoking the `hyva-theme-list` skill to find all Hyvä themes in the project.

Present the user with options to select a parent theme:
- **Hyvä default themes**: `Hyva/default-csp` (if installed) or `Hyva/default`
- **Existing Hyvä child themes**: List themes returned by the skill as `{Vendor}/{ThemeName}`

**Parent theme paths for later steps:**
- Hyvä default themes: `vendor/hyva-themes/magento2-default-theme-csp` or `vendor/hyva-themes/magento2-default-theme`
- Child themes: `app/design/frontend/{Vendor}/{ThemeName}`

### Step 3: Create Theme Directory Structure

Create the theme directory at `app/design/frontend/<Vendor>/<themeName>/` with:

```
app/design/frontend/<Vendor>/<themeName>/
├── registration.php
├── theme.xml
├── composer.json
└── web/
    └── tailwind/
        └── (copied from parent theme)
```

### Step 4: Create Configuration Files

#### registration.php

```php
<?php
declare(strict_types=1);

use Magento\Framework\Component\ComponentRegistrar;

ComponentRegistrar::register( ComponentRegistrar::THEME, 'frontend/<Vendor>/<themeName>', __DIR__);
```

#### theme.xml

```xml
<?xml version="1.0"?>
<theme xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:noNamespaceSchemaLocation="urn:magento:framework:Config/etc/theme.xsd">
    <title>Example Store Theme</title>
    <parent>Hyva/default-csp</parent>
</theme>
```

**Title formatting:** Split PascalCase theme names into separate words (e.g., `StoreTheme` → `Store Theme`). The title should read as `<Vendor> <Theme Name Words>` (e.g., `Example/StoreTheme` → `Example Store Theme`).

Adjust `<parent>` to match the selected parent theme:
- `Hyva/default-csp` or `Hyva/default` for Hyvä default themes
- `{ParentVendor}/{ParentThemeName}` for child theme parents (e.g., `Example/baseTheme`)

#### composer.json

```json
{
    "name": "<vendor-lowercase>/<package-name>",
    "description": "Example Store Theme based on Hyvä",
    "type": "magento2-theme",
    "license": "proprietary",
    "require": {
        "hyva-themes/magento2-default-theme-csp": "*"
    },
    "autoload": {
        "files": [
            "registration.php"
        ]
    }
}
```

**Package name rules:**
- Convert `<ThemeName>` to kebab-case (e.g., `StoreTheme` → `store-theme`)
- Append `-theme` suffix only if the theme name doesn't already end with "theme"
- Examples:
  - `StoreTheme` → `store-theme` (already ends with "theme", no suffix added)
  - `CustomStore` → `custom-store-theme` (suffix added)
  - `myTheme` → `my-theme` (already ends with "theme", no suffix added)

Adjust the `require` dependency to match the parent theme:
- For Hyvä default themes: `hyva-themes/magento2-default-theme-csp` or `hyva-themes/magento2-default-theme`
- For child theme parents: Use the parent's composer package name (from its `composer.json`), or omit if the parent theme is not a composer package

### Step 5: Copy and Configure Tailwind

Create the web directory and copy the tailwind folder from the parent theme, excluding `node_modules` (copied node_modules contain broken symlinks and must be installed fresh):

```bash
mkdir -p app/design/frontend/<Vendor>/<ThemeName>/web
rsync -a --exclude='node_modules' <parent_theme_path>/web/tailwind app/design/frontend/<Vendor>/<ThemeName>/web/
```

Where `<parent_theme_path>` is:
- `vendor/hyva-themes/magento2-default-theme-csp` for Hyvä default-csp
- `vendor/hyva-themes/magento2-default-theme` for Hyvä default
- `app/design/frontend/{ParentVendor}/{ParentTheme}` for child theme parents

Update `web/tailwind/hyva.config.json` to include the parent theme path(s) in Tailwind content scanning.

**For Hyvä default theme parent:**
```json
{
    "tailwind": {
        "include": [
            { "src": "vendor/hyva-themes/magento2-default-theme-csp" }
        ]
    }
}
```

**For child theme parent:** Include both the immediate parent AND the root Hyvä theme to ensure all template classes are scanned:
```json
{
    "tailwind": {
        "include": [
            { "src": "app/design/frontend/{ParentVendor}/{ParentTheme}" },
            { "src": "vendor/hyva-themes/magento2-default-theme-csp" }
        ]
    }
}
```

If the child theme parent already has additional includes in its `hyva.config.json`, copy those to maintain the full inheritance chain.

### Step 6: Install Dependencies and Build CSS

Use the `hyva-compile-tailwind-css` skill to install dependencies and build CSS for the newly created theme at `app/design/frontend/<Vendor>/<ThemeName>/`.

### Step 7: Enable the Theme

Inform the user they can enable the theme via:

1. Magento Admin: Content > Design > Configuration
2. Or via CLI: `bin/magento config:set design/theme/theme_id <theme_id>`

Run setup upgrade to register the theme:

```bash
bin/magento setup:upgrade
bin/magento cache:flush
```

## Troubleshooting

### No Hyvä themes found (Step 2)
**Cause**: Hyvä theme packages not installed in the project.
**Solution**: Install Hyvä themes via Composer: `composer require hyva-themes/magento2-default-theme` or `hyva-themes/magento2-default-theme-csp`.

### Parent theme path doesn't exist (Step 5)
**Cause**: The selected parent theme directory is missing or path is incorrect.
**Solution**: Verify the parent theme exists before running rsync. Check that Composer packages are properly installed with `composer install`.

### Tailwind folder missing in parent (Step 5)
**Cause**: The parent theme doesn't have a `web/tailwind` directory (possible with very old or custom themes).
**Solution**: Fall back to copying the tailwind folder from `vendor/hyva-themes/magento2-default-theme-csp/web/tailwind` instead.

### npm install fails (Step 6)
**Cause**: Node version mismatch, network issues, or corrupted package-lock.json.
**Solution**:
- Check Node version (requires Node 16+): `node --version`
- Delete `node_modules` and `package-lock.json`, then retry `npm install`

### npm build fails (Step 6)
**Cause**: Invalid paths in `hyva.config.json` or missing purge targets.
**Solution**:
- Verify all paths in `hyva.config.json` exist in the project
- Check for JSON syntax errors in the config file
- Ensure parent theme paths are correct

## Output

After successful creation, provide a summary:

- Theme location: `app/design/frontend/<Vendor>/<ThemeName>/`
- Parent theme: The selected parent (e.g., `Hyva/default-csp`, `Hyva/default`, or `{Vendor}/{ThemeName}`)
- Next steps for customization:
  - Override templates by creating matching paths
  - Customize Tailwind in `web/tailwind/tailwind-source.css`
  - Run `npm run watch` for development
  - Run `npm run build` before deployment

<!-- Copyright © Hyvä Themes https://hyva.io. All rights reserved. Licensed under OSL 3.0 -->
