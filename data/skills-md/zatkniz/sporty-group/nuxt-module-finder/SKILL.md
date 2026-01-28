---
name: nuxt-module-finder
description: Find and compare Nuxt modules for specific features. Use when users need to add functionality via modules (auth, UI, database, etc). Do not use for basic Nuxt concepts.
---

# Nuxt Module Finder

Discover and evaluate Nuxt modules to add specific functionality to the project.

## When to Use

**DO USE** when:
- User wants to add new functionality (authentication, UI library, CMS, etc)
- Comparing module options
- Checking module compatibility with Nuxt 4
- Getting installation/setup instructions for a specific module

**DO NOT USE** when:
- Asking about built-in Nuxt features
- General project setup questions
- Already have module installed (check package.json first)

## Process

1. **Search Modules**: `mcp_nuxt_list-modules`
   - Parameters: `search`, `category`, `sort`, `order`
   - Categories: "ui", "auth", "database", "media", "seo", "cms", "analytics"

2. **Get Details**: `mcp_nuxt_get-module` with exact slug
   - Returns: README, compatibility, stats, installation

3. **Recommend**: Consider Nuxt 4 compatibility, downloads, and maintenance

## Common Modules

- `@nuxt/ui` - Official UI components
- `@nuxtjs/i18n` - Internationalization
- `nuxt-icon` - Icon library
- `@nuxt/image` - Image optimization
- `@pinia/nuxt` - State management
- `nuxt-auth-utils` - Authentication

## Example

**User: "I need authentication"**
1. List: `category: "auth"`
2. Compare top results
3. Get details for best match
4. Provide installation steps and basic setup
