---
name: hyva-compile-tailwind-css
description: Compile Tailwind CSS for Hyvä themes in Magento 2. This skill should be used when the user wants to build styles, generate CSS, compile Tailwind, run Tailwind, or create production/development stylesheets for a Hyvä theme. Triggers on phrases like "compile tailwind", "build styles", "generate css", "run tailwind", "build css", or "npm build for theme".
---

# Compile Tailwind CSS for Hyvä Themes

Compiles Tailwind CSS for Hyvä themes in Magento 2. Handles both production builds and development watch mode.

## Step 1: Detect Environment & Set Command Wrapper

Use the `hyva-exec-shell-cmd` skill to detect the environment and determine the appropriate command wrapper. All npm commands below show the core command; wrap them according to the detected environment.

## Step 2: Identify Theme

If no theme path provided, invoke the `hyva-theme-list` skill to discover available themes. Filter the results to only include themes in `app/design/frontend/` by default. Themes in `vendor/hyva-themes/` require explicit user request.

**If no themes found:** Inform the user that no Hyvä themes with Tailwind configuration were found in `app/design/frontend/`. Ask if they want to check `vendor/hyva-themes/` instead, or if they need to create a child theme first using the `hyva-child-theme` skill.

## Step 3: Install Dependencies & Build

**Default to production build** unless user explicitly requests "watch", "watch mode", or "live reload".

```bash
# Install deps only if node_modules missing
if [ ! -d "<theme-path>/web/tailwind/node_modules" ]; then
  cd <theme-path>/web/tailwind && npm ci
fi

# Production build (default)
cd <theme-path>/web/tailwind && npm run build

# OR watch mode (only if explicitly requested)
cd <theme-path>/web/tailwind && npm run watch
```

## Step 4: Verify Output

Compiled CSS location: `<theme-path>/web/css/styles.css`

Confirm the file was updated by checking its modification time.

## Troubleshooting

- **Missing node_modules:** Run `npm ci`
- **Outdated styles:** Clear browser cache; in production mode run `bin/magento setup:static-content:deploy`

<!-- Copyright © Hyvä Themes https://hyva.io. All rights reserved. Licensed under OSL 3.0 -->
