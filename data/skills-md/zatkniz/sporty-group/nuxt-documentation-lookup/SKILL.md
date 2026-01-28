---
name: nuxt-documentation-lookup
description: Look up official Nuxt documentation for specific APIs, advanced features, or implementation details not covered in repository instructions. Use when precise Nuxt framework information is needed.
---

# Nuxt Documentation Lookup

Retrieve official Nuxt documentation for specific implementation details, APIs, or advanced features.

## When to Use

**DO USE** when:
- User asks about specific Nuxt APIs or advanced features
- Need implementation details for middleware, plugins, hooks, or runtime APIs
- Questions about Nuxt 4 migration or version-specific features
- Debugging Nuxt-specific errors
- Advanced configuration not in repository instructions

**DO NOT USE** when:
- Basic structure/conventions (covered in repository instructions)
- Auto-import usage (covered in path-specific instructions)  
- General Vue or TypeScript questions

## Process

1. **Search**: `mcp_nuxt_list-documentation-pages` (version: "4.x")
2. **Retrieve**: `mcp_nuxt_get-documentation-page` with exact path
3. **Combine**: Merge documentation with repository instructions

## Key Paths

- `/docs/4.x/api/*` - API references
- `/docs/4.x/guide/going-further/*` - Advanced topics
- `/docs/4.x/guide/concepts/*` - Core concepts

## Example

**User: "How do I use runtime hooks?"**
1. Search for "hooks" in documentation
2. Get `/docs/4.x/api/advanced/hooks`
3. Provide hook examples with local project context
