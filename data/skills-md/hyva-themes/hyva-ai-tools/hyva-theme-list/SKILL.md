---
name: hyva-theme-list
description: List all Hyvä theme paths in a Magento 2 project. This skill should be used when the user wants to find Hyvä themes, list available themes, discover theme paths, or when other skills need to locate Hyvä themes. Trigger phrases include "list hyva themes", "find themes", "show themes", "available themes", "theme paths".
---

# Hyvä Theme Listing

Lists all Hyvä theme paths in a Magento 2 project. Themes are identified by the presence of `web/tailwind/package.json`.

## Usage

**Important:** Execute this script from the Magento project root directory.

Run the discovery script to list all Hyvä themes:

```bash
bash <skill_path>/scripts/list_hyva_themes.sh
```

Where `<skill_path>` is the directory containing this SKILL.md file (e.g., `.claude/skills/hyva-theme-list`).

**Output format:** One theme path per line (relative to project root), or empty output if no themes found.

```
app/design/frontend/Example/customTheme
vendor/hyva-themes/magento2-default-theme-csp
```

## Search Locations

The script searches two locations:

| Location | Description |
|----------|-------------|
| `app/design/frontend/` | Custom themes developed for the project |
| `vendor/` | Installed themes from any vendor (not limited to hyva-themes) |

## Theme Identification

A directory is identified as a Hyvä theme when it contains both:
1. `web/tailwind/package.json` (Hyvä/Tailwind structure)
2. `theme.xml` (valid Magento theme)

## Integration with Other Skills

Other skills that need to locate Hyvä themes should invoke this skill by name:

```markdown
Invoke the `hyva-theme-list` skill to discover available themes.
```

The output can be processed line-by-line or stored in a variable for selection prompts.

<!-- Copyright © Hyvä Themes https://hyva.io. All rights reserved. Licensed under OSL 3.0 -->
