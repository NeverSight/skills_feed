---
name: shadcn-vue
description: shadcn-vue for Vue/Nuxt with Reka UI components and Tailwind. Use for accessible UI, Auto Form, data tables, charts, dark mode, MCP server setup, or encountering component imports, Reka UI errors.
---

# shadcn-vue

---

## Quick Start (3 Minutes)

### For Vue Projects (Vite)

#### 1. Initialize shadcn-vue

```bash
npx shadcn-vue@latest init
```

**During initialization**:

- Style: `New York` or `Default` (cannot change later!)
- Base color: `Slate` (recommended)
- CSS variables: `Yes` (required for dark mode)

#### 2. Configure TypeScript Path Aliases

```json
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

#### 3. Configure Vite

```typescript
// vite.config.ts
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import tailwindcss from "@tailwindcss/vite"; // Tailwind v4
import path from "path";

export default defineConfig({
  plugins: [vue(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
```

#### 4. Add Your First Component

```bash
npx shadcn-vue@latest add button
```

---

## Quick Reference

| Need                    | Command or file                                    |
| ----------------------- | -------------------------------------------------- |
| Initialize project      | `npx shadcn-vue@latest init`                       |
| Add component           | `npx shadcn-vue@latest add button`                 |
| Add multiple components | `npx shadcn-vue@latest add button card dialog`     |
| Build registry JSON     | `npx shadcn-vue@latest build`                      |
| Generate component docs | `npx tsx scripts/generate-shadcn-components.ts`    |
| Enable CSS variables    | `components.json` → `tailwind.cssVariables: true`  |
| Add registry namespace  | `components.json` → `registries` map               |
| Opencode MCP init       | `npx shadcn-vue@latest mcp init --client opencode` |
| Codex MCP config        | `~/.codex/config.toml` with `mcp_servers.shadcn`   |

---

## Bundled Resources

**Templates** (`templates/`):

- `quick-setup.ts` - Complete setup guide for Vue/Nuxt with examples (190 lines)

**References** (`references/`):

- `cli.md` - CLI commands and options
- `mcp.md` - MCP setup, client configs, prompts
- `theming.md` - Theming and `cssVariables`
- `error-catalog.md` - All 7 documented issues with solutions (267 lines)
- `component-examples.md` - All 50+ component examples with code
- `dark-mode-setup.md` - Complete dark mode implementation guide
- `data-tables.md` - Data tables with TanStack Table

**Component Documentation** (`components/`):

- `references/components.md` - Index of all shadcn-vue components
- `components/<component>.md` - Individual component documentation with installation, usage, and examples

**Official Documentation**:

- shadcn-vue Docs: https://shadcn-vue.com
- Reka UI Docs: https://reka-ui.com
- GitHub: https://github.com/radix-vue/shadcn-vue

---

## When to Load References

Load these references based on the task:

1. **Load `references/error-catalog.md` when:**
   - User encounters "component not found" or import errors
   - Setup commands fail or configuration issues arise
   - Tailwind CSS variables or TypeScript paths broken
   - **Trigger phrases:** "not working", "error", "fails to", "broken"

2. **Load `references/components.md` when:**
   - User asks what components are available (names, categories, status)
   - User needs to add/use a component and wants the correct install/import paths
   - You need to confirm a component exists before recommending a custom build

3. **Load `references/component-examples.md` when:**
   - User asks "how do I implement [component]?"
   - Need copy-paste examples for specific components
   - Building forms, tables, navigation, or data display
   - **Trigger phrases:** "example", "how to use", "implement", "code sample"

4. **Load `references/cli.md` when:**
   - User asks how to run the CLI (`init`, `add`, `update`) or what prompts mean
   - Need the exact command/flags for installing one or more components
   - Troubleshooting CLI-related issues (registry, paths, overwrites)

5. **Load `references/dark-mode-setup.md` when:**
   - Implementing dark mode / theme switching
   - User mentions Vue 3 + Vite, Nuxt, or Astro setup
   - Need composable patterns for theme management
   - **Trigger phrases:** "dark mode", "theme", "light/dark", "color scheme"

6. **Load `references/theming.md` when:**
   - User wants to customize theme tokens via CSS variables (`cssVariables`, `:root`, `.dark`)
   - Need to wire Tailwind to CSS-variable-based colors and radii
   - Setting up/adjusting design tokens (colors, radius, typography) for shadcn-vue

7. **Load `references/mcp.md` when:**
   - Setting up MCP server for opencode, Codex, Cursor, VS Code
   - Configuring registries in `components.json`
   - Troubleshooting missing components or registry namespaces
   - **Trigger phrases:** "MCP", "opencode", "codex", "cursor", "registry"

8. **Load `references/data-tables.md` when:**
   - Building sortable/filterable/paginated tables
   - User mentions TanStack Table or `DataTable`
   - **Trigger phrases:** "data table", "table", "tanstack", "sorting", "pagination"

---

## Critical Rules

### Always Do

✅ **Run `init` before adding components**

- Creates required configuration and utilities
- Sets up path aliases

✅ **Use CSS variables for theming** (`cssVariables: true`)

- Enables dark mode support
- Flexible theme customization

✅ **Configure TypeScript path aliases**

- Required for component imports
- Must match `components.json` aliases

✅ **Keep components.json in version control**

- Team members need same configuration
- Documents project setup

### Never Do

❌ **Don't change `style` after initialization**

- Requires complete reinstall
- Reinitialize in new directory instead

❌ **Don't mix Radix Vue and Reka UI v2**

- Incompatible component APIs
- Use one or the other

❌ **Don't skip TypeScript configuration**

- Component imports will fail
- IDE autocomplete won't work

❌ **Don't use without Tailwind CSS**

- Components are styled with Tailwind
- Won't render correctly

---

## Common Mistakes

- Running `add` before `init` and missing `components.json`.
- Forgetting to enable the MCP server in the client UI/config.
- Mis-typed registry namespaces (`@namespace/component`).
- Using CSS variable classes without `tailwind.cssVariables: true`.

---

## CLI Commands Reference

### init Command

```bash
# Initialize in current directory
npx shadcn-vue@latest init

# Initialize in specific directory (monorepo)
npx shadcn-vue@latest init -c ./apps/web
```

### add Command

```bash
# Add single component
npx shadcn-vue@latest add button

# Add multiple components
npx shadcn-vue@latest add button card dialog

# Add all components
npx shadcn-vue@latest add --all
```

### diff Command

```bash
# Check for component updates
npx shadcn-vue@latest diff button
```

### mcp Command

```bash
# Initialize MCP for specific client
npx shadcn-vue@latest mcp init --client opencode
npx shadcn-vue@latest mcp init --client codex
npx shadcn-vue@latest mcp init --client cursor
npx shadcn-vue@latest mcp init --client vscode
```

---

## Configuration

shadcn-vue uses `components.json` to configure:

- Component paths (`@/components/ui`)
- Utils location (`@/lib/utils`)
- Tailwind config paths
- TypeScript paths

**Full example:** See `templates/components.json` or generate via `npx shadcn-vue@latest init`

---

## Utils Library

The `@/lib/utils.ts` file provides the `cn()` helper for merging Tailwind classes:

- Combines multiple className strings
- Uses `clsx` + `tailwind-merge` for conflict resolution

**Auto-generated** by `shadcn-vue init` - no manual setup needed.
