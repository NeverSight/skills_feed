---
name: pinia-documentation-lookup
description: Look up Pinia documentation for store patterns, API reference, and advanced features. Use when users need specific Pinia implementation details or state management patterns.
---

# Pinia Documentation Lookup

Access official Pinia documentation for state management patterns, API references, and advanced features.

## When to Use

**DO USE** when:
- Questions about specific Pinia APIs (`defineStore`, `storeToRefs`, `$patch`, etc.)
- State persistence strategies
- SSR/Nuxt-specific Pinia usage
- Advanced features (plugins, subscriptions, hot module replacement)
- Testing Pinia stores
- Store composition patterns
- Migration from Vuex to Pinia
- Composition API setup store patterns

**DO NOT USE** when:
- Basic store creation covered in project instructions
- Simple state management questions
- General Nuxt questions (use nuxt-documentation-lookup instead)
- Questions about Option Stores (project uses Composition API only)

## Process

1. **Search Pinia Docs**: Use `mcp_nuxt_search_nuxt_docs` with query
   - Searches official Pinia documentation
   - Returns relevant sections with content

2. **Specific Topics**:
   - **Core Concepts**: "defineStore", "state", "getters", "actions"
   - **Setup Stores**: "composition API", "setup stores", "ref", "computed"
   - **Advanced**: "plugins", "subscriptions", "$patch", "hot reload"
   - **SSR**: "server side rendering", "nuxt", "hydration"
   - **TypeScript**: "typing stores", "type inference", "TypeScript"
   - **Testing**: "testing stores", "unit tests", "mocking"

3. **Provide Context**: Include relevant examples from project instructions

## Common Queries

### Composition API Patterns
```
Query: "pinia composition api setup stores"
→ Get Composition API store patterns
```

### API Reference
```
Query: "storeToRefs pinia destructuring"
→ Learn how to properly destructure store properties
```

### SSR & Nuxt
```
Query: "pinia nuxt server side rendering"
→ Understand SSR considerations with Pinia
```

### Advanced Features
```
Query: "pinia plugins custom"
→ Learn about creating custom Pinia plugins
```

### State Persistence
```
Query: "pinia persist state localStorage"
→ Find persistence strategies and plugins
```

### Testing
```
Query: "testing pinia stores unit tests"
→ Get testing strategies and examples
```

### Store Composition
```
Query: "pinia composing stores"
→ Learn how to use multiple stores together
```

## Example Workflow

**User: "How do I persist Pinia store to localStorage?"**

1. Search: "pinia persist state localStorage"
2. Find documentation on persistence plugins
3. Recommend `@pinia-plugin-persistedstate/nuxt`
4. Provide installation and code example adapted to project structure

**User: "What's the difference between setup stores and option stores?"**

1. Inform: This project uses **Composition API (setup stores) ONLY**
2. Reference project instructions
3. Show setup store example from project conventions
4. Explain why: consistency with Vue 3 Composition API

**User: "How to use stores in server-side code?"**

1. Search: "pinia nuxt server composables"
2. Get SSR-specific documentation
3. Explain server context considerations
4. Provide Nuxt-specific example

**User: "How do I test Pinia stores?"**

1. Search: "pinia testing unit tests"
2. Get testing documentation
3. Provide vitest/jest setup example
4. Show test examples from project instructions

## Integration with Project

**PROJECT STANDARD**: This project uses **EXCLUSIVELY** Composition API (setup stores).

Always reference project conventions from `stores.instructions.md`:
- ✅ **Use setup stores ONLY** (Composition API style with arrow function)
- ❌ **Never use option stores** (object with state/getters/actions)
- Use **auto-imports** (no explicit imports needed)
- Return **readonly()** for state properties
- Follow naming convention: `use[Domain]Store`
- Use `storeToRefs()` for destructuring reactive properties
- Use `ref()` for state, `computed()` for getters

## Tools Available

### Search Nuxt Docs (includes Pinia)
```
mcp_nuxt_search_nuxt_docs
- query: Search term for Pinia documentation
```

### For Module Info
```
mcp_nuxt_get-module
- slug: "@pinia/nuxt" for module details
```

## Response Format

1. **Direct answer** from documentation
2. **Code example** adapted to project structure
3. **Reference** project instructions if applicable
4. **Additional context** for Nuxt 4 compatibility

## Common Topics & Keywords

### Basic Concepts
- "defineStore" - Creating stores
- "state" - Reactive state
- "getters" - Computed properties
- "actions" - Methods that can be async

### Advanced Features
- "storeToRefs" - Destructuring stores
- "$patch" - Batch state updates
- "$reset" - Reset store to initial state
- "$subscribe" - Watch for state changes
- "plugins" - Extend Pinia functionality

### Composition API
- "setup stores" - Composition API style stores
- "ref" - Reactive state in setup stores
- "computed" - Getters in setup stores
- "watch" - Watching store changes

### SSR & Nuxt
- "nuxt" - Nuxt-specific usage
- "server side rendering" - SSR considerations
- "hydration" - Client-side state hydration
- "useState" - Nuxt composable for SSR state

### TypeScript
- "TypeScript" - Type definitions
- "typing stores" - Store type inference
- "typed actions" - Action type safety

### Testing
- "testing" - Testing strategies
- "unit tests" - Unit testing stores
- "mocking" - Mocking dependencies
- "setActivePinia" - Testing setup

## Important Notes

- Pinia is Vue's official state management solution (replaces Vuex)
- Setup stores align with Vue 3 Composition API
- Auto-imports via `@pinia/nuxt` module
- SSR-compatible by default in Nuxt
- Lighter and more intuitive than Vuex
- Full TypeScript support with type inference
- No mutations - actions can be synchronous or asynchronous
- DevTools support for debugging

## Additional Resources

- [Pinia Official Docs](https://pinia.vuejs.org/)
- [Pinia Core Concepts](https://pinia.vuejs.org/core-concepts/)
- [Pinia Nuxt Integration](https://pinia.vuejs.org/ssr/nuxt.html)
- [Pinia Cookbook](https://pinia.vuejs.org/cookbook/)
- [Pinia API Reference](https://pinia.vuejs.org/api/)
