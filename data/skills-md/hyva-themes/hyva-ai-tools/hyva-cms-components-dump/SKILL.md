---
name: hyva-cms-components-dump
description: Dump all Hyvä CMS components from active modules. This skill should be used when the user wants to list all CMS components, view available components, debug component configurations, or see the merged components.json output. Trigger phrases include "list cms components", "dump components", "show all components", "view cms components", "components.json dump".
---

# Hyvä CMS Component Dump

Locates all `components.json` files from Hyvä CMS modules and outputs a merged JSON object containing all component definitions from active modules.

## Usage

**Important:** Execute this script from the Magento project root directory.

Run the dump script:

```bash
php <skill_path>/scripts/dump_cms_components.php
```

Where `<skill_path>` is the directory containing this SKILL.md file (e.g., `.claude/skills/hyva-cms-components-dump`).

**Output format:** A single JSON object containing all merged CMS component definitions.

## How It Works

1. **Reads module configuration** from `app/etc/config.php` to get the ordered list of modules
2. **Filters active modules** - only modules with value `1` are included (disabled modules are skipped)
3. **Locates components.json files** in:
   - `app/code/{Vendor}/{Module}/etc/hyva_cms/components.json`
   - `vendor/{vendor-name}/{package-name}/*/etc/hyva_cms/components.json`
4. **Maps paths to module names** by reading each module's `etc/module.xml`
5. **Merges JSON objects** in module load order as declared in `config.php`
6. **Outputs the result** as formatted JSON

## Module Load Order

Components are merged in the exact order modules appear in `app/etc/config.php`. Later modules can override components from earlier modules by using the same component key.

## Example Output

```json
{
    "text_block": {
        "label": "Text Block",
        "category": "Content",
        "template": "Hyva_CmsBase::elements/text-block.phtml",
        ...
    },
    "feature_card": {
        "label": "Feature Card",
        "category": "Elements",
        "template": "Custom_Module::elements/feature-card.phtml",
        ...
    }
}
```

## Integration with Other Skills

This skill can be used to:
- Debug which components are available in the CMS editor
- Verify component registration after creating new components
- Check for component name conflicts between modules
- Export component definitions for documentation

<!-- Copyright © Hyvä Themes https://hyva.io. All rights reserved. Licensed under OSL 3.0 -->
