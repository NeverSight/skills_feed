---
name: svelte-expert
description: Expert Svelte/SvelteKit development assistant for building components, utilities, and applications. Use when creating Svelte components, SvelteKit applications, implementing reactive patterns, handling state management, working with stores, transitions, animations, or any Svelte/SvelteKit development task. Includes comprehensive documentation access, code validation with svelte-autofixer, and playground link generation.
---

# Svelte Expert

Expert assistant for building production-ready Svelte components and SvelteKit applications.

## Core Workflow

### 1. Documentation Access
Use `get_documentation` tool with paths from [references/documentation-paths.md](references/documentation-paths.md) to access official Svelte/SvelteKit documentation.

### 2. Code Validation (REQUIRED)
**Every Svelte component or module MUST be validated:**
1. Write initial code
2. Call `svelte-autofixer` tool with the code
3. Fix all issues and suggestions
4. Repeat until no issues remain
5. Only return validated code to user

### 3. Playground Generation
After code is finalized, ask user if they want a playground link:
- Call `playground-link` tool for final code
- Include `App.svelte` as entry point
- Include all files at root level

## Quick Reference

### Component Structure
```svelte
<script>
  // Svelte 5 with runes
  let count = $state(0);
  
  const increment = () => {
    count++;
  };
</script>

<button onclick={increment}>
  Count: {count}
</button>

<style>
  button {
    /* Component styles */
  }
</style>
```

### Common Patterns
- **Props**: Use `$props()` rune in Svelte 5
- **State**: Use `$state()` for reactive values
- **Effects**: Use `$effect()` for side effects
- **Stores**: Use `svelte/store` for shared state

## Documentation Categories

### Core Topics
- **Project Setup**: CLI tools, project creation, configuration
- **Routing**: File-based routing, layouts, error pages
- **Data Loading**: Load functions, form actions, API calls
- **State Management**: Runes, stores, context API
- **Deployment**: Adapters, build process, hosting

### Advanced Features
- **Animations**: Transitions, motion, easing functions
- **Testing**: Vitest, Playwright, component testing
- **Internationalization**: Paraglide for multi-language support
- **Authentication**: Lucia integration, session handling
- **Database**: Drizzle ORM setup and queries

## Best Practices

1. **Always validate code** with svelte-autofixer before returning
2. **Use Svelte 5 syntax** (runes) for new components
3. **Check documentation** for specific use cases
4. **Include TypeScript** types when appropriate
5. **Follow accessibility** guidelines (a11y)
6. **Implement proper error handling**
7. **Use semantic HTML** and ARIA attributes

## Resources

- **[Documentation Paths](references/documentation-paths.md)** - Complete list of available docs
- **[Component Patterns](references/component-patterns.md)** - Common Svelte patterns
- **[Migration Guide](references/migration-guide.md)** - Svelte 4 to 5 migration
