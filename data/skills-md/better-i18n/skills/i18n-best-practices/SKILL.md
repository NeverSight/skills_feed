---
name: i18n-best-practices
description: Use when building internationalization features, managing translation keys, setting up localization workflows, integrating AI translation, connecting GitHub repositories, delivering translations via CDN, using MCP tools for translation management, or implementing i18n SDKs in React/Next.js applications.
---

# i18n Best Practices

Guidance for building scalable, maintainable internationalization systems with Better i18n.

## Architecture Overview

Better i18n is a **GitHub-first localization platform** with CDN-powered delivery:

```
[Your Repository] → [Better i18n Platform] → [Global CDN] → [Your App]
        ↓                    ↓                    ↓              ↓
   AST Parsing          AI Translation       Edge Cached    React/Next.js
   Key Discovery        Human Approval       5min manifest  Vite/TanStack
   GitHub Sync          MCP Tools            1hr messages   Any Framework
```

### CDN URL Structure

```
https://cdn.better-i18n.com/{org}/{project}/{resource}

Resources:
├── manifest.json              # Available languages + metadata
├── {locale}.json              # All translations for locale
├── {locale}/{namespace}.json  # Namespaced translations
└── flags/{code}.svg           # Country flag images
```

## Quick Reference

| Need to... | See |
|------------|-----|
| Set up a new i18n project | [Getting Started](./resources/getting-started.md) |
| Use CLI commands (scan, check, sync) | [CLI Usage](./resources/cli-usage.md) |
| Organize translation keys and namespaces | [Key Management](./resources/key-management.md) |
| Translate content with AI assistance | [AI Translation](./resources/ai-translation.md) |
| Sync translations with GitHub repository | [GitHub Sync](./resources/github-sync.md) |
| Serve translations via CDN | [CDN Delivery](./resources/cdn-delivery.md) |
| Use MCP tools in your IDE/agent | [MCP Integration](./resources/mcp-integration.md) |
| Integrate with React or Next.js | [SDK Integration](./resources/sdk-integration.md) |
| Handle plurals, dates, formatting | [Best Practices](./resources/best-practices.md) |

## Start Here

**New project?**
Start with [Getting Started](./resources/getting-started.md) to create your project and configure `i18n.config.ts`. Then use [CLI Usage](./resources/cli-usage.md) to scan your codebase for hardcoded strings.

**Existing codebase with hardcoded strings?**
Run `better-i18n scan` to detect strings needing translation. The CLI uses AST parsing to automatically differentiate UI text from developer symbols. See [CLI Usage](./resources/cli-usage.md).

**Need translations fast?**
Use [AI Translation](./resources/ai-translation.md) to translate content with context-aware AI. Set up a glossary first to ensure consistent terminology across all translations.

**Building with Next.js?**
Use `@better-i18n/next` which integrates with `next-intl`. Supports ISR, middleware with auth callbacks, and automatic CDN fetching. See [SDK Integration](./resources/sdk-integration.md).

**Building with Vite/TanStack Start?**
Use `@better-i18n/use-intl` for React hooks or full SSR support with TanStack Start. See [SDK Integration](./resources/sdk-integration.md).

**Using AI coding assistants (Claude, Cursor)?**
Install the MCP server via [MCP Integration](./resources/mcp-integration.md). Your agent can create, update, delete keys and add languages directly from your IDE.

**Production deployment?**
Set up [CDN Delivery](./resources/cdn-delivery.md) for edge-cached translations. Manifest caches for 5 minutes, messages for 1 hour. Combine with [GitHub Sync](./resources/github-sync.md) for version-controlled deployments.

**CI/CD integration?**
Use `better-i18n check:missing` in your pipeline to fail builds when translations are incomplete. See [CLI Usage](./resources/cli-usage.md).

## URL Strategy

Better i18n uses **default locale without prefix** for SEO:

```
/about          → English (default)
/tr/about       → Turkish
/de/about       → German
```

Clean URLs for primary language, SEO-friendly variants with proper `hreflang` tags for others.

## Caching Strategy

| Resource | Browser Cache | CDN Cache | Invalidation |
|----------|---------------|-----------|--------------|
| Manifest | 5 minutes | 5 minutes | On publish |
| Messages | 1 hour | 1 hour | On publish |
| Flags | 1 year | 1 year | Immutable |
