---
name: purgetss
description: "PRIMARY SOURCE for PurgeTSS utility-first styling toolkit for Titanium/Alloy. Contains complete reference of 21,236+ utility classes, grid system, animations, and CLI tools. ALWAYS consult this skill FIRST for ANY PurgeTSS styling question before suggesting classes. CRITICAL: NEVER suggest Tailwind CSS classes - always verify in class-index.md first. Covers: (1) Project setup with utility-first styling, (2) Grid-based responsive layouts, (3) Declarative animations, (4) Dynamic components with $.UI.create(), (5) Icon Fonts and Color Palettes via CLI, (6) Advanced design rules in config.cjs, (7) Arbitrary values and platform modifiers. NOTE: PurgeTSS is an opinionated toolkit created by the author. This skill reflects personal styling preferences. Feel free to adapt to your needs."
---

# PurgeTSS Expert

Utility-first styling toolkit for Titanium/Alloy mobile apps.

## Table of Contents

- [PurgeTSS Expert](#purgetss-expert)
  - [Table of Contents](#table-of-contents)
  - [Core Workflow](#core-workflow)
  - [Project Structure](#project-structure)
    - [Understanding `app.tss` vs `_app.tss`](#understanding-apptss-vs-_apptss)
    - [Checking for Unused/Unsupported Classes](#checking-for-unusedunsupported-classes)
    - [How `tailwind.tss` Works](#how-tailwindtss-works)
  - [Quick Start](#quick-start)
  - [Critical Rules (Low Freedom)](#critical-rules-low-freedom)
    - [⭐ PREFER `$.UI.create()` for Dynamic Components](#-prefer-uicreate-for-dynamic-components)
    - [🚨 NEVER Create Manual .tss Files](#-never-create-manual-tss-files)
    - [🚨 NO FLEXBOX - Titanium Doesn't Support It](#-no-flexbox---titanium-doesnt-support-it)
    - [Other Mandatory Rules](#other-mandatory-rules)
  - [Common Anti-Patterns](#common-anti-patterns)
  - [Class Verification Workflow](#class-verification-workflow)
    - [Verification Steps](#verification-steps)
    - [What HAS Classes vs What DOESN'T](#what-has-classes-vs-what-doesnt)
  - [Reference Guides](#reference-guides)
    - [Essential References](#essential-references)
    - [Setup \& Configuration](#setup--configuration)
    - [Customization](#customization)
    - [Layout \& Styling](#layout--styling)
    - [Fonts \& Animations](#fonts--animations)
  - [Examples](#examples)
  - [Related Skills](#related-skills)

---

## Core Workflow

1. **Setup**: `purgetss create 'name'` or `purgetss init` for existing projects
2. **Build**: Write XML with utility classes → PurgeTSS auto-generates `app.tss`
3. **Configure**: Customize via `purgetss/config.cjs`

## Project Structure

```bash
./purgetss/
├─ fonts/              # Custom font files (.ttf, .otf)
├─ styles/
│  ├─ definitions.css  # For VS Code IntelliSense
│  └─ tailwind.tss     # All PurgeTSS utility classes
└─ config.cjs          # Theme configuration

./app/styles/
├─ app.tss             # AUTO-GENERATED - DO NOT EDIT DIRECTLY
└─ _app.tss            # YOUR CUSTOM STYLES (persists across runs)
```

### Understanding `app.tss` vs `_app.tss`

:::warning CRITICAL: app.tss IS AUTO-GENERATED
**`app.tss` is ALWAYS regenerated** every time the app compiles.

PurgeTSS scans ALL XMLs and Controllers for utility classes, then generates a fresh `app.tss` containing only the classes actually used.

**NEVER edit `app.tss` directly** - your changes WILL be overwritten on the next build.
:::

:::info THE `_app.tss` BACKUP FILE
On **first run**, PurgeTSS backs up your original `app.tss` to `_app.tss`.

**`_app.tss` is your custom styles file** - it persists across all PurgeTSS runs.

Every build, PurgeTSS:
1. Scans XMLs and Controllers for used classes
2. Regenerates `app.tss` from scratch
3. Copies `_app.tss` content into the generated `app.tss`

Better approach: define custom classes in `config.cjs` instead of `_app.tss`.
:::

### Checking for Unused/Unsupported Classes

:::danger ALWAYS CHECK `app.tss` FOR ERRORS
At the **end of every generated `app.tss`**, look for this section:

```tss
// Unused or unsupported classes
// .my-typo-class
// .non-existent-utility
```

**These are classes used in your XMLs or Controllers that have NO definition anywhere:**
- Not in `tailwind.tss` (generated from PurgeTSS utilities)
- Not in `_app.tss` (your custom styles)
- Not in any other `.tss` file in the `styles/` folder

**This means:**
1. You have a **typo** in your class name
2. You're using a class that **doesn't exist** in PurgeTSS
3. You need to **define the class** in `_app.tss` or `config.cjs`

**As part of any analysis, ALWAYS check the end of `app.tss` and report any unused/unsupported classes to the user!**
:::

### How `tailwind.tss` Works

:::info TAILWIND.TSS REGENERATION
`./purgetss/styles/tailwind.tss` contains ALL available PurgeTSS utility classes.

**It regenerates when `./purgetss/config.cjs` changes** - this is where you define:
- Custom colors
- Custom spacing scales
- Ti Element styles
- Any project-specific utilities

If a class appears in "Unused or unsupported classes" in `app.tss`, it means it's truly not defined anywhere - not even in your `config.cjs` customizations.
:::

## Quick Start

```bash
purgetss create 'MyApp' -d -v fa
# -d: Install dev dependencies (ESLint, Tailwind)
# -v: Copy icon fonts (fa, mi, ms, f7)
```

## Critical Rules (Low Freedom)

### ⭐ PREFER `$.UI.create()` for Dynamic Components

:::tip RECOMMENDED FOR DYNAMIC COMPONENTS
When creating components dynamically in Controllers, **use `$.UI.create()` instead of `Ti.UI.create()`** to get full PurgeTSS utility class support:

```javascript
// ✅ RECOMMENDED - Full PurgeTSS support
const view = $.UI.create('View', {
  classes: ['w-screen', 'h-auto', 'bg-white', 'rounded-lg']
})

// ❌ AVOID - No PurgeTSS classes
const view = Ti.UI.createView({
  width: Ti.UI.FILL,
  height: Ti.UI.SIZE,
  backgroundColor: '#ffffff',
  borderRadius: 8
})
```

See [Dynamic Component Creation](references/dynamic-component-creation.md) for complete guide.
:::

### 🚨 NEVER Create Manual .tss Files

:::danger DEFEATS PURPOSE OF PURGETSS
**PurgeTSS automatically generates ALL styles.**

- **DO NOT** create `app/styles/index.tss`, `login.tss`, or ANY manual `.tss` files
- **ONLY** use utility classes in XML views
- PurgeTSS parses XML → extracts used classes → generates clean `app.tss`
:::

### 🚨 NO FLEXBOX - Titanium Doesn't Support It

:::danger FLEXBOX CLASSES DO NOT EXIST
The following are **NOT supported**:
- ❌ `flex`, `flex-row`, `flex-col`
- ❌ `justify-between`, `justify-center`, `justify-start`, `justify-end`
- ❌ `items-center` for alignment (exists but sets `width/height: FILL`)

**Use Titanium layouts instead:**
- ✅ `horizontal` - Children left to right
- ✅ `vertical` - Children top to bottom
- ✅ Omit layout class - Defaults to `composite` (absolute positioning)
:::

### Other Mandatory Rules

- **NO `p-` padding classes**: Titanium does NOT support a native `padding` property on `View`, `Window`, `ScrollView`, or `TableView`. Always use **margins on children** (`m-`) to simulate internal spacing.
- **View defaults to `SIZE`**: Use `w-screen`/`h-screen` to fill space when needed.
- **`rounded-full`**: To get a perfect circle, use `rounded-full-XX` (where XX is the width/height of the square element).
- **`rounded-full-XX` includes size**: These classes already set `width`, `height`, and `borderRadius`. Do **not** add `w-XX h-XX`/`wh-XX` unless you need to override.
- **`m-xx` on FILL elements**: Adding `m-4` to a `w-screen` element pins it to all four edges (top, bottom, left, right). This will **stretch the component vertically** to fill the parent unless you explicitly add `h-auto` (`Ti.UI.SIZE`) to constrain it to its content.
- **`w-XX` + `h-XX` → `wh-XX`**: If both width and height use the same scale value, prefer a single `wh-XX` (order doesn't matter: `w-10 h-10` and `h-10 w-10` are equivalent).
- **Use `wh-` shortcuts**: PurgeTSS provides a complete scale of combined width/height utilities:
    - **Numeric Scale**: `wh-0` to `wh-96` (e.g., `wh-16` sets both to 64px).
    - **Fractions**: `wh-1/2`, `wh-3/4`, up to `wh-11/12` for proportional sizing.
    - **Special Values**: `wh-auto` (explicit `SIZE`), `wh-full` (`100%`), and `wh-screen` (`FILL`).
    - Using these instead of separate `w-` and `h-` classes improves XML readability and reduces generated TSS size.

:::tip LAYOUT TIP: EDGE PINNING
If using margins (`m-`) causes your `Label` or `Button` to stretch unexpectedly, it is due to Titanium's **Edge Pinning** rule (2 opposite pins = computed dimension). Use the `wh-auto` class to explicitly force `SIZE` behavior and prevent stretching.
:::

- **NEVER add `composite` class explicitly** - That's the default, use `horizontal`/`vertical` when needed
- **Arbitrary values use parentheses**: `w-(100px)`, `bg-(#ff0000)` - NO square brackets
- **`mode: 'all'` required** in `config.cjs` for Ti Elements styling
- **Classes use `kebab-case`**: `.my-class`, IDs use `camelCase`: `#myId`

## Common Anti-Patterns

**WRONG:**
```xml
<View class="flex-row justify-between">  <!-- Flexbox doesn't exist -->
<View class="p-4">  <!-- No padding on Views -->
<View class="composite">  <!-- Never add composite explicitly -->
```

**CORRECT:**
```xml
<View class="horizontal">
<View class="m-4">  <!-- Use margins on children -->
<View>  <!-- Omit layout = composite by default -->
```

**WRONG (Dynamic Components):**
```javascript
// Manual styling with Ti.UI.create()
const view = Ti.UI.createView({
  width: Ti.UI.FILL,
  backgroundColor: '#fff',
  borderRadius: 8
})
```

**CORRECT (Dynamic Components):**
```javascript
// PurgeTSS classes with $.UI.create()
const view = $.UI.create('View', {
  classes: ['w-screen', 'bg-white', 'rounded-lg']
})
```

## Class Verification Workflow

:::danger CRITICAL: VERIFY CLASSES BEFORE SUGGESTING
**NEVER guess or hallucinate classes based on Tailwind CSS knowledge!**

PurgeTSS shares naming with Tailwind CSS but has DIFFERENT classes for Titanium.
Always verify a class exists before suggesting it.
:::

### Verification Steps

1. **Check if it's a KNOWN anti-pattern**
   - See [PROHIBITED Classes](references/class-index.md#prohibited-tailwind-classes-that-do-not-exist)
   - Common mistakes: `flex-row`, `justify-between`, `p-4` on Views (p-* not supported on Views)

2. **Check the Class Index**
   - See [Class Index](references/class-index.md) for available patterns
   - Constant properties like `keyboard-type-*`, `return-key-type-*` have dedicated classes

3. **Search the project when unsure**
   ```bash
   # Search for a class pattern in the project's tailwind.tss
   grep -E "keyboard-type-" ./purgetss/styles/tailwind.tss
   grep -E "return-key-type-" ./purgetss/styles/tailwind.tss
   grep -E "^'bg-" ./purgetss/styles/tailwind.tss
   ```

4. **After making changes**
   - Check `app.tss` for "Unused or unsupported classes" section at the end
   - Report any typos or non-existent classes to the user

### What HAS Classes vs What DOESN'T

| Has Classes in PurgeTSS | Does NOT Have Classes                 |
| ----------------------- | ------------------------------------- |
| `keyboard-type-email`   | `hintText` (use attribute)            |
| `return-key-type-next`  | `passwordMask` (use attribute)        |
| `text-center`           | `autocorrect` (use attribute)         |
| `bg-blue-500`           | `autocapitalization` (use attribute)  |
| `w-screen`              | `flex-row` → use `horizontal`         |
| `wh-16`                 | `justify-between` → use margins       |
| `rounded-lg`            | `w-full` → use `w-screen`             |
| `m-4`, `gap-4`          | `p-4` on View → use `m-4` on children |

:::tip
When in doubt, prefer using the search command above to verify. It's better to spend 5 seconds verifying than suggesting a class that doesn't exist and will appear in the "unused classes" warning.
:::

## Reference Guides

Load these only when needed:

### Essential References
- **[Class Index](references/class-index.md)** - Quick patterns, prohibited classes, verification commands (LOAD FIRST when unsure about a class)
- **[Dynamic Component Creation](references/dynamic-component-creation.md)** - `$.UI.create()` and `Alloy.createStyle()` for creating components in Controllers (READ FIRST for dynamic components)

### Setup & Configuration
- [Installation & Setup](references/installation-setup.md) - First run, VS Code, LiveView
- [CLI Commands](references/cli-commands.md) - All `purgetss` commands

### Customization
- [Deep Customization](references/customization-deep-dive.md) - config.cjs, colors, spacing, Ti Elements
- [Custom Rules](references/custom-rules.md) - Styling Ti Elements, IDs, classes
- [Apply Directive](references/apply-directive.md) - Extracting utility combinations
- [Configurable Properties](references/configurable-properties.md) - All 80+ customizable properties

### Layout & Styling
- [Grid Layout System](references/grid-layout.md) - 12-column grid, responsive layouts
- [Smart Mappings](references/smart-mappings.md) - How gap, shadows, and grid work under the hood
- [Arbitrary Values](references/arbitrary-values.md) - Parentheses notation for custom values
- [Platform Modifiers](references/platform-modifiers.md) - ios:, android:, tablet:, handheld:
- [Opacity Modifier](references/opacity-modifier.md) - Color transparency with /50 syntax
- [Titanium Resets](references/titanium-resets.md) - Default styles for Ti elements

### Fonts & Animations
- [Icon Fonts](references/icon-fonts.md) - Font Awesome 7, Material Icons, custom icon libraries
- [Animation Component](references/animation-system.md) - Declarative `<Animation>` API

:::tip TEXT FONTS (Google Fonts, Roboto, etc.)
For text fonts, see [CLI Commands → build-fonts](references/cli-commands.md#purgetss-build-fonts-alias-bf).
:::

## Examples

For complete WRONG vs CORRECT examples including:
- Titanium layout patterns (horizontal, vertical, composite)
- Grid with percentages
- Gap usage
- Manual .tss anti-patterns
- Dynamic component creation with `$.UI.create()` and `Alloy.createStyle()`

See [EXAMPLES.md](references/EXAMPLES.md) and [Dynamic Component Creation](references/dynamic-component-creation.md)

## Related Skills

For tasks beyond styling, use these complementary skills:

| Task                                         | Use This Skill |
| -------------------------------------------- | -------------- |
| Project architecture, services, controllers  | `alloy-expert` |
| Complex UI components, ListViews, gestures   | `ti-ui`        |
| Alloy MVC concepts, data binding, TSS syntax | `alloy-guides` |
| Native features (camera, location, push)     | `ti-howtos`    |
