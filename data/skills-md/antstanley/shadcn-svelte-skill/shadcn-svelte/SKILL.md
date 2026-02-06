---
name: shadcn-svelte
description: Expert guidance for shadcn-svelte, a Svelte 5 port of shadcn/ui. Use this skill when working with shadcn-svelte components, installing UI components via CLI, implementing forms with Superforms/Formsnap, adding dark mode with mode-watcher, creating data tables with TanStack Table, theming with Tailwind CSS v4 and OKLCH colors, or building custom component registries. Triggers on mentions of shadcn-svelte, Bits UI components, or SvelteKit UI component libraries.
---

# shadcn-svelte

A Svelte 5 / SvelteKit port of shadcn/ui - beautifully designed, accessible components built with Bits UI and Tailwind CSS.

## Quick Start

### Installation

```bash
# SvelteKit
pnpm dlx shadcn-svelte@latest init

# Add components
pnpm dlx shadcn-svelte@latest add button card dialog
```

### Basic Usage

Components use namespace imports:

```svelte
<script lang="ts">
  import * as Card from "$lib/components/ui/card/index.js";
  import { Button } from "$lib/components/ui/button/index.js";
</script>

<Card.Root>
  <Card.Header>
    <Card.Title>Title</Card.Title>
    <Card.Description>Description</Card.Description>
  </Card.Header>
  <Card.Content>Content here</Card.Content>
  <Card.Footer>
    <Button>Action</Button>
  </Card.Footer>
</Card.Root>
```

## Key Patterns

### Component Import Pattern

```svelte
<!-- Compound components (most components) -->
import * as Dialog from "$lib/components/ui/dialog/index.js";

<!-- Single components -->
import { Button } from "$lib/components/ui/button/index.js";
import { Input } from "$lib/components/ui/input/index.js";
```

### Form Implementation

Use Superforms + Formsnap for forms:

```svelte
<script lang="ts">
  import * as Form from "$lib/components/ui/form/index.js";
  import { superForm } from "sveltekit-superforms";

  let { data } = $props();
  const form = superForm(data.form);
</script>

<form method="POST" use:form.enhance>
  <Form.Field {form} name="email">
    <Form.Control>
      {#snippet children({ props })}
        <Input {...props} type="email" />
      {/snippet}
    </Form.Control>
    <Form.FieldErrors />
  </Form.Field>
</form>
```

### Dark Mode

```svelte
<!-- +layout.svelte -->
<script lang="ts">
  import { ModeWatcher } from "mode-watcher";
</script>

<ModeWatcher />
{@render children()}
```

Toggle with `toggleMode()`, `setMode("dark")`, or `resetMode()` from mode-watcher.

## Reference Documentation

Detailed documentation is organized in `references/`:

- **Overview**: `about.md`, `cli.md`, `components-json.md`, `theming.md`
- **Installation**: `installation/sveltekit.md`, `installation/astro.md`, `installation/vite.md`
- **Components**: `components/[name].md` - 59 component guides
- **Dark Mode**: `dark-mode/svelte.md`, `dark-mode/astro.md`
- **Migration**: `migration/svelte-5.md`, `migration/tailwind-v4.md`
- **Registry**: `registry/getting-started.md` - custom registry creation

### Finding Component Documentation

For any component, read `references/components/[component-name].md`:
- Button → `references/components/button.md`
- Dialog → `references/components/dialog.md`
- Data Table → `references/components/data-table.md`

## Common Tasks

| Task | Reference |
|------|-----------|
| Add a component | `pnpm dlx shadcn-svelte@latest add [name]` |
| Form validation | `references/components/form.md` |
| Data tables | `references/components/data-table.md` |
| Theming/colors | `references/theming.md` |
| Dark mode | `references/dark-mode/svelte.md` |
| Custom registry | `references/registry/getting-started.md` |
