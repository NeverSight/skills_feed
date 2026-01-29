---
name: design-tokens
description: Expert in design tokens using the DTCG specification. Use this skill when users ask about design tokens, DTCG format, token validation, formatting, transformation, color spaces (sRGB, Display P3, OKLCH), references and aliasing, resolvers, theming with modifiers/contexts, multi-platform design systems, accessibility, or working with tools like jq, jsonata, and terrazzo. Helps with token file creation, resolver configuration, structure, naming conventions, and best practices.
---

# Design Tokens Expert

Expert guidance for working with design tokens following the Design Tokens Community Group (DTCG) specification.

## Quick Reference

| Topic | Reference |
|-------|-----------|
| Token types, structure, validation | [reference/format.md](reference/format.md) |
| Color spaces, components, alpha, **common mistakes** | [reference/color.md](reference/color.md) |
| Sets, modifiers, resolution order | [reference/resolver.md](reference/resolver.md) |
| jq, JSONata, **Figma export**, **Terrazzo config** | [reference/tools.md](reference/tools.md) |
| Common patterns and examples | [examples/use-cases.md](examples/use-cases.md) |

**Getting Started:** See [Getting Started Guides](#getting-started-guides) for step-by-step workflows.

## Specification Sources

Based on the latest DTCG Draft Community Group Reports:
- [Format Module](https://www.designtokens.org/tr/drafts/format/)
- [Color Module](https://www.designtokens.org/tr/drafts/color/)
- [Resolver Module](https://www.designtokens.org/tr/drafts/resolver/)

## Core Concepts

### Token Structure

A token is a JSON object with `$value`. Special properties use `$` prefix:

```json
{
  "brand-blue": {
    "$type": "color",
    "$value": {
      "colorSpace": "srgb",
      "components": [0.15, 0.39, 0.92],
      "hex": "#2563eb"
    },
    "$description": "Primary brand color"
  }
}
```

### Token Types

**Atomic:** color, dimension, fontFamily, fontWeight, duration, cubicBezier, number

**Composite:** strokeStyle, border, shadow, gradient, typography, transition

See [reference/format.md](reference/format.md) for complete type definitions.

### Color Format

Colors use structured objects (not hex strings):

```json
{
  "$type": "color",
  "$value": {
    "colorSpace": "srgb",
    "components": [1, 0, 0.5],
    "alpha": 0.8,
    "hex": "#ff0080"
  }
}
```

Supported spaces: srgb, display-p3, oklch, oklab, hsl, hwb, lab, lch, and more. See [reference/color.md](reference/color.md).

### References (Aliasing)

**Two syntaxes supported:**

1. **Curly braces** - Token-level references: `"{path.to.token}"`
2. **JSON Pointer (`$ref`)** - Property-level access: `{"$ref": "#/path/to/$value/property"}`

Token reference example:
```json
{
  "color": {
    "primary": {"$type": "color", "$value": {"colorSpace": "srgb", "components": [0, 0.4, 0.8]}}
  },
  "button": {
    "background": {"$type": "color", "$value": "{color.primary}"}
  }
}
```

JSON Pointer example (accessing array elements):
```json
{
  "blue": {
    "$type": "color",
    "$value": {"colorSpace": "okhsl", "components": [0.733, 0.8, 0.5]}
  },
  "blue-hue": {
    "$type": "number",
    "$ref": "#/blue/$value/components/0"
  }
}
```

See [reference/format.md](reference/format.md) for complete reference syntax details.

### Groups and Type Inheritance

Groups organize tokens. `$type` on a group applies to all children:

```json
{
  "spacing": {
    "$type": "dimension",
    "sm": {"$value": {"value": 8, "unit": "px"}},
    "md": {"$value": {"value": 16, "unit": "px"}},
    "lg": {"$value": {"value": 24, "unit": "px"}}
  }
}
```

### Resolvers for Theming

Resolvers manage tokens across contexts (themes, platforms, densities):

```json
{
  "name": "my-system",
  "version": "2025.10",
  "sets": {
    "core": {"sources": [{"$ref": "tokens/base.json"}]}
  },
  "modifiers": {
    "theme": {
      "contexts": {
        "light": [{"$ref": "themes/light.json"}],
        "dark": [{"$ref": "themes/dark.json"}]
      },
      "default": "light"
    }
  },
  "resolutionOrder": [
    {"$ref": "#/sets/core"},
    {"$ref": "#/modifiers/theme"}
  ]
}
```

See [reference/resolver.md](reference/resolver.md) for complete documentation.

## Getting Started Guides

### Quick Start: Convert CSS Variables to DTCG

**Starting point:** Existing CSS custom properties
```css
:root {
  --color-primary: #2563eb;
  --color-background: #ffffff;
  --spacing-sm: 8px;
  --spacing-md: 16px;
}
```

**Step 1:** Create primitives.tokens.json
```json
{
  "color": {
    "primitive": {
      "$type": "color",
      "blue-500": {
        "$value": { "colorSpace": "srgb", "components": [0.145, 0.388, 0.922], "hex": "#2563eb" }
      },
      "white": {
        "$value": { "colorSpace": "srgb", "components": [1, 1, 1], "hex": "#ffffff" }
      }
    }
  },
  "spacing": {
    "$type": "dimension",
    "scale": {
      "sm": { "$value": { "value": 8, "unit": "px" } },
      "md": { "$value": { "value": 16, "unit": "px" } }
    }
  }
}
```

**Step 2:** Create semantic.tokens.json with references
```json
{
  "color": {
    "interactive": {
      "$type": "color",
      "primary": { "$value": "{color.primitive.blue-500}" }
    },
    "background": {
      "$type": "color",
      "page": { "$value": "{color.primitive.white}" }
    }
  },
  "spacing": {
    "$type": "dimension",
    "component": {
      "padding": { "$value": "{spacing.scale.sm}" },
      "gap": { "$value": "{spacing.scale.md}" }
    }
  }
}
```

**Conversion tips:**
- RGB hex to sRGB: divide each channel by 255 (e.g., `37/255 = 0.145`)
- Keep hex as fallback in the `hex` property
- Create semantic layer for purpose-driven naming

---

### Quick Start: Set Up Terrazzo with Dark Mode

**Step 1:** Install dependencies
```bash
npm install -D @terrazzo/cli @terrazzo/plugin-css
```

**Step 2:** Create token files with mode extensions

tokens/themes/light.tokens.json:
```json
{
  "$extensions": { "mode": "light" },
  "color": {
    "background": {
      "$type": "color",
      "page": { "$value": { "colorSpace": "srgb", "components": [1, 1, 1], "hex": "#ffffff" } }
    },
    "text": {
      "$type": "color",
      "primary": { "$value": { "colorSpace": "srgb", "components": [0.07, 0.07, 0.07], "hex": "#121212" } }
    }
  }
}
```

tokens/themes/dark.tokens.json:
```json
{
  "$extensions": { "mode": "dark" },
  "color": {
    "background": {
      "$type": "color",
      "page": { "$value": { "colorSpace": "srgb", "components": [0.07, 0.07, 0.07], "hex": "#121212" } }
    },
    "text": {
      "$type": "color",
      "primary": { "$value": { "colorSpace": "srgb", "components": [0.95, 0.95, 0.95], "hex": "#f2f2f2" } }
    }
  }
}
```

**Step 3:** Create terrazzo.config.mjs
```javascript
import { defineConfig } from "@terrazzo/cli";
import pluginCSS from "@terrazzo/plugin-css";

export default defineConfig({
  tokens: [
    "./tokens/primitives.tokens.json",
    "./tokens/themes/light.tokens.json",
    "./tokens/themes/dark.tokens.json"
  ],
  outDir: "./dist/",
  plugins: [
    pluginCSS({
      filename: "tokens.css",
      modeSelectors: [
        { mode: "light", selectors: [":root", "[data-theme='light']"] },
        { mode: "dark", selectors: ["[data-theme='dark']", "@media (prefers-color-scheme: dark)"] }
      ]
    })
  ]
});
```

**Step 4:** Build and use
```bash
npx terrazzo build
```

In your HTML:
```html
<html data-theme="light"><!-- or "dark" -->
```

---

### Quick Start: Import Figma Variables Export

**Step 1:** Export from Figma
- Open Variables panel in Figma
- Use a DTCG export plugin or Figma's built-in export
- Save as `figma-export.json`

**Step 2:** Validate the export
```bash
# Check JSON is valid
jq '.' figma-export.json > /dev/null && echo "Valid JSON"

# List all token paths
jq -r 'paths(has("$value")) | join(".")' figma-export.json
```

**Step 3:** Add mode extensions if needed

If Figma exported separate mode files, add `$extensions.mode`:
```bash
# Add mode to light theme file
jq '. + {"$extensions": {"mode": "light"}}' light.json > light.tokens.json
```

**Step 4:** Add hex fallbacks (if missing)

Figma exports sRGB components but may omit hex:
```bash
# Quick check if hex values exist
jq '.. | objects | select(.colorSpace == "srgb") | select(.hex == null)' figma-export.json
```

**Step 5:** Configure Terrazzo

Create `terrazzo.config.mjs` pointing to your imported files and build.

**Common Figma export issues:**
- Flat structure (no primitives/semantic separation) - reorganize manually
- Space in token names - use jq to convert to kebab-case
- Missing `$type` on groups - add type inheritance

---

## Workflows

### Creating a Token File

```
Token File Creation:
- [ ] Step 1: Define file structure (primitives → semantic → components)
- [ ] Step 2: Create primitive tokens with explicit types
- [ ] Step 3: Create semantic tokens referencing primitives
- [ ] Step 4: Validate structure and references
- [ ] Step 5: Test with target tools (Terrazzo, etc.)
```

**Step 1: Define structure**

Organize into layers:
```
tokens/
├── primitives.tokens.json   # Raw values (colors, spacing scales)
├── semantic.tokens.json     # Purpose-driven aliases
└── components.tokens.json   # Component-specific tokens
```

**Step 2: Create primitives**

```json
{
  "color": {
    "primitive": {
      "$type": "color",
      "blue": {
        "500": {"$value": {"colorSpace": "srgb", "components": [0.15, 0.39, 0.92], "hex": "#2563eb"}}
      }
    }
  }
}
```

**Step 3: Create semantic tokens**

```json
{
  "color": {
    "interactive": {
      "$type": "color",
      "default": {"$value": "{color.primitive.blue.500}"}
    }
  }
}
```

**Step 4: Validate**

Check for:
- All tokens have resolvable `$type`
- No circular references
- Valid value formats for each type
- Names don't contain `{`, `}`, `.` or start with `$`

**Step 5: Test with tools**

```bash
terrazzo validate tokens.json
terrazzo build --input tokens.json --output test.css --format css
```

---

### Setting Up a Theme Resolver

```
Resolver Setup:
- [ ] Step 1: Organize token files by concern
- [ ] Step 2: Create resolver.json with version and sets
- [ ] Step 3: Define theme modifier with contexts
- [ ] Step 4: Configure resolution order
- [ ] Step 5: Test with different inputs
```

**Step 1: Organize files**

```
tokens/
├── resolver.json
├── base.tokens.json
└── themes/
    ├── light.tokens.json
    └── dark.tokens.json
```

**Step 2: Create resolver**

```json
{
  "name": "my-design-system",
  "version": "2025.10",
  "sets": {
    "foundation": {
      "sources": [{"$ref": "base.tokens.json"}]
    }
  }
}
```

**Step 3: Define theme modifier**

```json
{
  "modifiers": {
    "theme": {
      "contexts": {
        "light": [{"$ref": "themes/light.tokens.json"}],
        "dark": [{"$ref": "themes/dark.tokens.json"}]
      },
      "default": "light"
    }
  }
}
```

**Step 4: Set resolution order**

```json
{
  "resolutionOrder": [
    {"$ref": "#/sets/foundation"},
    {"$ref": "#/modifiers/theme"}
  ]
}
```

**Step 5: Test**

```bash
terrazzo build --resolver resolver.json --output light.css
terrazzo build --resolver resolver.json --input theme=dark --output dark.css
```

---

### Validating Token Files

```
Validation Checklist:
- [ ] Step 1: Check JSON syntax
- [ ] Step 2: Verify type declarations
- [ ] Step 3: Validate value formats
- [ ] Step 4: Check reference resolution
- [ ] Step 5: Verify naming constraints
```

**Step 1: JSON syntax**

```bash
jq '.' tokens.json > /dev/null && echo "Valid JSON"
```

**Step 2: Type declarations**

Every token needs a resolvable `$type` (explicit or inherited from parent group).

**Step 3: Value formats**

| Type | Valid Format |
|------|--------------|
| color | `{colorSpace, components, [alpha], [hex]}` |
| dimension | `{value: number, unit: "px"|"rem"}` |
| duration | `{value: number, unit: "ms"|"s"}` |
| cubicBezier | `[P1x, P1y, P2x, P2y]` where P1x, P2x ∈ [0,1] |
| fontWeight | 1-1000 or string ("normal", "bold", etc.) |

**Step 4: References**

- All `{path.to.token}` references must resolve
- No circular references (A → B → A)
- No self-references

**Step 5: Naming**

- Names cannot start with `$`
- Names cannot contain `{`, `}`, `.`

---

### Migrating from Other Formats

```
Migration Workflow:
- [ ] Step 1: Export existing tokens to JSON
- [ ] Step 2: Map types to DTCG equivalents
- [ ] Step 3: Convert color values to structured format
- [ ] Step 4: Update reference syntax
- [ ] Step 5: Validate and test
```

**Common conversions:**

| From | To DTCG |
|------|---------|
| `"#ff0000"` | `{colorSpace: "srgb", components: [1,0,0], hex: "#ff0000"}` |
| `"16px"` | `{value: 16, unit: "px"}` |
| `"$colors.primary"` or `{colors.primary}` | `"{colors.primary}"` |

**Terrazzo conversion:**

```bash
terrazzo convert --from style-dictionary --to dtcg input.json output.tokens.json
```

## Best Practices

### Token Layers

1. **Primitives** - Raw values without semantic meaning
2. **Semantic** - Purpose-driven tokens referencing primitives
3. **Component** - Specific component tokens referencing semantic

### Naming Conventions

- Use lowercase with hyphens: `color.brand.primary`
- Structure: `[category].[subcategory].[variant].[state]`
- Semantic over appearance: `color.interactive.default` not `color.blue-500`

### Theming Strategy

Use resolvers for themes (recommended over group extension):
- Cleaner separation of concerns
- Token paths stay consistent across themes
- Easy to compose themes (e.g., dark + high-contrast)
- Standardized input handling for build tools

### Accessibility

**Color contrast:** Document contrast ratios in `$extensions`:

```json
{
  "$extensions": {
    "com.example.a11y": {"contrastRatio": 7.5, "wcagLevel": "AA"}
  }
}
```

**Reduced motion:** Use resolver modifier:

```json
{
  "modifiers": {
    "motion": {
      "contexts": {
        "full": [{"$ref": "motion/full.json"}],
        "reduced": [{"$ref": "motion/reduced.json"}]
      },
      "default": "full"
    }
  }
}
```

### File Conventions

- Token files: `.tokens` or `.tokens.json`
- Resolver files: `.resolver.json`
- Encoding: UTF-8

## Common Tasks

| Task | Approach |
|------|----------|
| Format validation | Check against DTCG spec, use Terrazzo validate |
| Structure optimization | Organize into primitive → semantic → component layers |
| Alias resolution | Trace references, check for circular dependencies |
| Resolver configuration | Define sets, modifiers, resolution order |
| Theme implementation | Use resolver modifiers with context files |
| Multi-context builds | Generate outputs per theme/platform/density |
| Tool integration | Use jq for queries, Terrazzo for transforms |
| Migration | Convert colors to structured format, update references |

## Your Role

When helping with design tokens:

1. **Verify before claiming** - Check reference files before stating what DTCG does/doesn't support. Never assume spec limitations.
2. **Use latest DTCG spec** - Structured color format, proper types
3. **Validate structure** - Check `$value`, `$type`, references
4. **Suggest best practices** - Naming, organization, layering
5. **Help with tools** - jq queries, Terrazzo commands, JSONata transforms
6. **Consider platforms** - Web, iOS, Android via `$extensions`
7. **Think about scale** - Design for maintainability
8. **Prioritize accessibility** - Contrast, motion, focus indicators
9. **Connect design and code** - Bridge tools and implementation

**Important:** When asked about spec capabilities (what syntax is valid, what features exist), always read the relevant reference file first. Do not rely on assumptions or prior knowledge about the spec.

Always provide clear examples and explain reasoning behind recommendations.
