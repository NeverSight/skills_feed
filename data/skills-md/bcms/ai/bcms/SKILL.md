---
name: bcms-best-practices
description: >
  A skill that teaches the AI how to work with BCMS. It covers connecting to the BCMS API using the
  `@thebcms/client` SDK, managing templates, entries, groups, widgets,
  media assets, functions and webhooks, handling permissions, and following
  security best‑practices.
---

# BCMS Skills

This skill gives the AI coding agent concise, BCMS‑specific guidance and defers longer explanations to the files in `references/`.
The agent should keep this file under roughly 500 lines and load deeper guides only when needed.

Key topics:

- Setup and client initialization (see `references/bcms-api-basics.md`)
- Working with templates (see `references/templates.md`)
- Entries (see `references/entries.md`)
- Groups (see `references/groups.md`)
- Widgets (see `references/widgets.md`)
- Media (see `references/media.md`)
- Properties and field types (see `references/properties.md`)
- Functions and webhooks (see `references/functions-webhooks.md`)
- Permissions (see `references/permissions.md`)
- Framework integrations (see `references/frameworks.md`)

## Integration principles and defaults

- **Default to the latest BCMS stack**: use the latest BCMS features and the newest `@thebcms/*` and `@bcms-types/*` packages unless the user explicitly targets an older version.
- **Model content with BCMS primitives first**: prefer **templates + entries** as your main content model, with **groups** for reusable structures, **widgets** for reusable content blocks, and the **media library** for files.
- **Use CLI starters when possible**: for framework projects (Next, Nuxt, Astro, etc.) prefer the official `@thebcms/cli` starters before hand‑rolling integration; see `references/frameworks.md`.
- **Render via BCMS components**: in UI frameworks, prefer `BCMSContentManager` and `BCMSImage` (or their framework equivalents) to render rich text, widgets and media instead of building your own renderers.
- **Always isolate secrets**: read `orgId`, `instanceId` and API key credentials from environment variables, use separate keys per environment (dev/stage/prod) and prefer scoped keys, especially for media delivery; see `references/bcms-api-basics.md` and `references/permissions.md`.
- **Design for localisation**: when sites are multi‑lingual, use BCMS locales and model `meta`/`content` per locale; see `references/entries.md` and `references/properties.md`.
- **Evolve schemas, don't break them**: when changing content models, add or migrate fields via templates and groups; avoid destructive changes on production data; see `references/templates.md` and `references/groups.md`.

## Patterns to avoid (and what to do instead)

- **Never hard‑code API keys or use admin keys in the browser**.
  Instead, store secrets in environment variables and use minimally scoped keys; see `references/bcms-api-basics.md` and `references/permissions.md`.
- **Never delete templates, groups, widgets or media in production without checking impact**.
  Always inspect usage first (`group.whereIsItUsed`, `widget.whereIsItUsed`, `template.whereIsItUsed`) and plan a migration path; see `references/templates.md`, `references/groups.md`, `references/widgets.md`, and `references/media.md`.
- **Avoid stuffing unstructured JSON into `meta` or `content` when a property, group or widget fits**.
  Prefer explicit properties (string, rich text, enum, pointers, media) and reusable groups/widgets for structure; see `references/properties.md`, `references/groups.md`, and `references/widgets.md`.
- **Avoid re‑implementing rich‑text and widget rendering when `BCMSContentManager` is available**.
  Use the official components (`@thebcms/components-*`) with `BCMSContentManager` and `BCMSImage`, and only drop down to custom parsing when you have a clear requirement; see `references/entries.md` and `references/frameworks.md`.
- **Avoid exposing unnecessary write capabilities to public clients**.
  Do not use keys with create/update/delete rights from the frontend; keep mutations behind server‑side code or functions, and use read‑only or media‑only keys in the browser; see `references/permissions.md`.
- **Do not bypass webhook security**.
  Always verify webhook signatures, check timestamps, and design idempotent handlers; see `references/functions-webhooks.md`.

## When to reach for which BCMS features

- **Marketing, blog, or documentation sites**
  Use templates like `page`, `blog`, `doc` with structured properties, groups for SEO/author blocks, widgets for reusable sections, and the media library for images; render with `BCMSContentManager` and `BCMSImage`.
  See `references/templates.md`, `references/entries.md`, `references/groups.md`, `references/widgets.md`, and `references/media.md`.

- **Multi‑locale content**
  Model `meta` and `content` per locale, use BCMS locales, and ensure frontends handle missing translations gracefully via types from `@bcms-types/ts`.
  See `references/entries.md` and `references/properties.md`.

- **Asset‑heavy or image‑driven experiences**
  Rely on the media library, folder structure, and auto‑generated sizes; use a dedicated media API key for public delivery and `BCMSImage` (or equivalent) to serve optimised variants.
  See `references/media.md` and `references/bcms-api-basics.md`.

- **Framework‑based frontends (Next.js, Nuxt, Astro, Gatsby, Svelte, Vite)**
  Prefer the official BCMS starters; otherwise, follow the framework‑specific guides, using the standard `Client` constructor, generated types, and the appropriate `@thebcms/components-*` package.
  See `references/frameworks.md`.

## Setup and Client Initialization

- Always use **environment variables** for secrets, never hard‑code BCMS credentials.
- Use separate **API keys per environment** (development, staging, production).
- Prefer **scoped keys** with the minimum necessary permissions.

Example client initialization (TypeScript):

```ts
import { Client } from '@thebcms/client';

export const bcms = new Client(
  process.env.BCMS_ORG_ID!,
  process.env.BCMS_INSTANCE_ID!,
  {
    id: process.env.BCMS_API_KEY_ID!,
    secret: process.env.BCMS_API_KEY_SECRET!,
  },
  {
    injectSvg: true, // inline SVG icons into HTML
    useMemCache: true, // enable in‑memory caching
    enableSocket: false, // disable websockets when not needed
  },
);
```

For more, including API key structure and environment setup, see `references/bcms-api-basics.md`.

## Working with Templates

- Treat **templates** as your content types (e.g., `blog`, `page`, `author`).
- Use **singular, descriptive names** and rely on groups for reusable structures.
- Only admins (or keys with advanced rights) should create or modify templates.

Common operations:

- List all templates: `await bcms.template.getAll()`
- Get a template by ID or name
- Update or delete templates when refactoring content models

See `references/templates.md` for naming conventions, creation guidelines and code examples.

## Entries

- **Entries** are instances of templates (e.g., a single blog post).
- Entries usually have:
  - `meta` fields (title, slug, SEO, etc.)
  - `content` fields, often localized by language code

Example: get all entries for a `blog` template:

```ts
const blogPosts = await bcms.entry.getAll('blog');
```

Agents should be able to:

- Create, update and delete entries
- Retrieve entries by ID, slug or status
- Filter entries by template and status (e.g., draft vs. published)

See `references/entries.md` for full CRUD examples and multilingual details.

## Groups, Widgets and Media

- **Groups** are reusable structures that can be nested inside templates, widgets or other groups.
- **Widgets** are reusable content blocks embedded in rich‑text fields.
- **Media** refers to files in the BCMS media library (images, documents, etc.).

Typical operations:

- Groups:
  - `bcms.group.getAll()`
  - `bcms.group.whereIsItUsed(groupId)`
- Widgets:
  - `bcms.widget.getAll()`
  - `bcms.widget.whereIsItUsed(widgetId)`
- Media:
  - `bcms.media.getAll()`, `bcms.media.getById(id)`
  - Create folders and upload files using media API helpers

Widgets cannot currently be deleted via the SDK and must be removed via the BCMS dashboard.
See `references/groups.md`, `references/widgets.md` and `references/media.md` for concrete examples and media best‑practices.

## Properties and Field Types

BCMS supports various property types used in templates, groups and widgets, including:

- String, rich‑text, number, date, boolean
- Enumeration
- Entry pointer, group pointer
- Media fields (single and multiple)

Agents should choose appropriate field types based on content modelling goals and reusability.
See `references/properties.md`, `references/groups.md`, `references/widgets.md` and `references/templates.md` for details.

## Permissions and API Key Scopes

- BCMS enforces granular **permissions** for users and API keys.
- Permissions can be:
  - **Simple**: broad access levels
  - **Advanced**: per‑resource `get/create/update/delete` scopes
- Only admins can create templates, widgets, groups and API keys.

API keys:

- Should be scoped per template, function and media access where possible.
- Use **least privilege**: grant only the rights needed for the specific integration.

See `references/permissions.md` for a deeper explanation and configuration examples.

## Functions and Webhooks

- **Functions** are serverless handlers you deploy inside BCMS and call via REST.
- **Webhooks** notify external systems about events such as entry or media changes.

Agents should:

- Call functions using the correct URL and headers, including an API key with function permissions.
- Configure and secure webhooks by:
  - Verifying the `X-Bcms-Webhook-Signature` header
  - Validating timestamps to avoid replay attacks
  - Making handlers idempotent and rate‑limited

See `references/functions-webhooks.md` for full examples and security notes.

## Best Practices and Troubleshooting

- Prefer TypeScript and generated BCMS types (e.g., `@bcms-types/ts`) where available.
- Use caching (e.g., in‑memory or application‑level) for frequently read data.
- Separate dev, staging and production environments and API keys.
- On errors, check:
  - URL correctness (org, instance, function ID)
  - API key scopes and permissions
  - Network and TLS configuration

For in‑depth guidance, always cross‑reference the official BCMS documentation from the `references/` files.
