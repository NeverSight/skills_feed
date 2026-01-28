---
name: hyva-ui-component
description: Apply Hyva UI template-based components to a Hyvä theme. This skill should be used when the user wants to add, install, or apply a Hyva UI component (such as header, footer, gallery, menu, minicart, etc.) to their Hyvä theme. It lists available non-CMS components and their variants, displays component README instructions, and copies component files to the theme directory.
---

# Hyva UI Component

Applies Hyva UI template-based (non-CMS) components to a Hyvä theme by copying files from `{hyva_ui_path}/components/` to `app/design/frontend/{Vendor}/{Theme}/`.

**Path variable:** `{hyva_ui_path}` = `vendor/hyva-themes/hyva-ui` (default) or user-provided custom path.

**Command execution:** For any commands that need to run inside the development environment (e.g., `bin/magento` commands), use the `hyva-exec-shell-cmd` skill to detect the environment and determine the appropriate command wrapper.

## Step 0: Verify Hyva UI Installation

```bash
ls vendor/hyva-themes/hyva-ui/components/ 2>/dev/null
```

**If NOT found**, offer options: (A) User provides custom extraction path, (B) `composer require --dev hyva-themes/hyva-ui`, (C) Download from https://hyva.io/my-account/my-downloads/

After install, refresh catalog: `<skill_path>/scripts/refresh_catalog.sh {hyva_ui_path} <skill_path>/references/components.md`

Where `<skill_path>` is the directory containing this SKILL.md file.

## Step 1: Identify Theme Path

Use the `hyva-theme-list` skill to find existing Hyvä themes. Filter the results to only include themes in `app/design/frontend/` (exclude vendor themes).

Prompt the user to select:
- **Existing Hyvä themes**: List themes returned by the script as options (e.g., `Example/winterWonderTheme`)
- **Create new theme**: Always include an option to create a new child theme

**If user selects "Create new theme":**
1. Use the `hyva-child-theme` skill to create the new theme first
2. Continue with the newly created theme path after the skill completes

**If user selects an existing theme:**
Continue with the selected theme path: `app/design/frontend/{Vendor}/{Theme}`

## Step 2: List or Select Component

If no component specified or user asks to list components, show **only the "Non-CMS Components (Template-Based)" section** from `references/components.md`.

**Do NOT list or mention:**
- CMS components (accordion, card, categories, error-page, generic-content, order-confirmation, shortcuts, testimonial, usp, product-data/C-highlights)
- Plugins (alpine-collapse, splidejs, sticky-header, tailwind-v3-design-tokens, tailwind-v4)

These are internal dependencies or require the CMS Tailwind JIT compiler and are not applicable for direct installation via this skill.

## Step 3: Show Variants

Variants: **A**=Basic, **B**=Enhanced, **C**=Advanced, **D**=Specialized. List with: `ls {hyva_ui_path}/components/{component}/`

## Step 4: Read Component README

Always read `{hyva_ui_path}/components/{component}/{variant}/README.md` before copying. Present to user: dependencies, configuration options, special requirements.

## Step 5: Copy Component Files

**Before copying**, check which destination files already exist to track created vs updated:

```bash
# List source files
find {hyva_ui_path}/components/{component}/{variant}/src -type f

# For each source file, check if destination exists
# e.g., for src/Magento_Catalog/templates/product/view/gallery.phtml
# check: {theme_path}/Magento_Catalog/templates/product/view/gallery.phtml
```

Track each file as either:
- **created**: Destination file did not exist before copy
- **updated**: Destination file already existed (will be overwritten)

Then copy:
```bash
cp -r {hyva_ui_path}/components/{component}/{variant}/src/* {theme_path}/
```

The `src/` directory contains Magento module folders (`Magento_Theme/`, `Magento_Catalog/`, etc.) that map directly to theme structure. For existing layout XML files, **merge** content rather than overwriting.

## Step 5.5: Add XML Configuration Options

Check if README contains XML configuration (look for `<var name="`, `etc/view.xml`).

**If found:**
1. Extract the first XML block containing `<var name=` elements with default values
2. Identify the module attribute (e.g., `module="Magento_Catalog"`)
3. Add to `{theme_path}/etc/view.xml`:
   - If file doesn't exist: Create with full `<view>` structure
   - If `<vars module="...">` exists: Add `<var>` elements inside it
   - If section missing: Add new `<vars module="...">` before `</view>`
4. Notify: "Added configuration options to `{theme_path}/etc/view.xml` with default values."

Preserve existing view.xml content and keep XML comments from README.

## Step 6: Handle Dependencies

Check README for dependencies and install them automatically (do not ask the user to select plugins):
- **Plugin dependencies:** Copy required files from `{hyva_ui_path}/plugins/{plugin}/src/` (e.g., splidejs for gallery/D-splide)
- **Component dependencies:** Apply dependent components first
- **External packages:** e.g., `composer require hyva-themes/magento2-hyva-payment-icons`

## Step 7: Ask to recompile styles

- **Rebuild Tailwind:** Always ask: "Do you need to recompile Tailwind CSS styles?" Never automatically build — an external tool may already be handling this. If the user wants to compile, use the `hyva-compile-tailwind-css` skill with the target theme.

## Step 8: Output Summary

After applying all changes, output a summary of modifications:

### 8.1: List Modified Files

Display all files that were created or modified during this component installation. Use the tracking from Step 5 to label each file correctly:

- **(created)**: File did not exist before and was newly created
- **(updated)**: File already existed and was overwritten

```
Modified files:
  - {theme_path}/Magento_Catalog/templates/product/view/gallery.phtml (updated)
  - {theme_path}/Magento_Theme/templates/html/header.phtml (created)
  - {theme_path}/etc/view.xml (updated)
```

### 8.2: XML Configuration Table

If XML configuration was added to `{theme_path}/etc/view.xml`, parse the XML block from the README and display a table of options:

```bash
# Extract the XML config block from README and parse it
php <skill_path>/scripts/parse_readme_xml.php --format=table < xml_block.txt
```

The table shows each option with columns:
- **Option**: The full option path without a common prefix (e.g., `magnifier.enable`)
- **Value**: The default value configured
- **Description**: Explanatory text from the XML comment

Example output (common prefix like `gallery.` is automatically stripped):
```
Option               | Value      | Description
---------------------+------------+---------------------------------------------------
nav                  | thumbs     | Gallery navigation style (false/thumbs/counter)
magnifier.enable     | false      | Turn on/off magnifier (true/false)
```

For markdown output (e.g., when creating documentation), use `--format=md`.

## Step 9: Final steps

1. **Review** copied templates for store-specific customization

## Quick Reference

```
{hyva_ui_path}/components/{component}/{variant}/
├── README.md       # Instructions
├── media/          # Preview images
└── src/            # Files to copy to theme
```

See `references/components.md` for the full component catalog (only show non-CMS section to users).

<!-- Copyright © Hyvä Themes https://hyva.io. All rights reserved. Licensed under OSL 3.0 -->
