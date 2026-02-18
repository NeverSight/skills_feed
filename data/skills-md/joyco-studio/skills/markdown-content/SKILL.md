---
name: markdown-content
description: >
  Guide for building markdown content pages (blogs, legal, changelogs) in Next.js using
  fumadocs-mdx, rehype-pretty-code, and shiki. Covers MDX collections, self-contained prose
  typography, syntax-highlighted code blocks, and the component mappings that keep rendered
  markdown and custom React code components visually consistent. No documentation UI framework
  required.
license: MIT
metadata:
  author: joyco-studio
  version: "0.0.1"
---

# Markdown Content Pages — Next.js

This skill defines how to build content-driven pages (blog posts, changelogs, legal pages, knowledge bases) in a Next.js App Router project using MDX.

The goal is **visual and behavioral consistency** between:

- Markdown codeblocks written in `.mdx` files (processed at build time)
- Custom React code components rendered on the page (highlighted at runtime)

---

## Stack Overview

| Layer | Library | Purpose |
|---|---|---|
| Content framework | `fumadocs-mdx` | MDX collection definitions, frontmatter schemas, build-time processing |
| Content runtime | `fumadocs-core` | Source loader, page tree, slug resolution |
| Syntax highlighting | `shiki` + `rehype-pretty-code` | Dual-theme code highlighting at build time (MDX) and runtime (components) |
| Schema validation | `zod` | Typed frontmatter with defaults and optional fields |
| Styling | Tailwind CSS v4 | Utility-first styles, custom prose CSS, code block styles |
| Framework | Next.js (App Router) | File-based routing with catch-all `[[...slug]]` for content pages |

```bash
npm install fumadocs-mdx fumadocs-core shiki rehype-pretty-code zod
```

---

## Project Structure

```
├── app/
│   ├── layout.tsx                       # Root layout
│   ├── styles/
│   │   ├── globals.css                  # Tailwind + stylesheet imports (order matters)
│   │   ├── prose.css                    # Self-contained typography for .prose class
│   │   ├── shiki.css                    # Code block styling (themes, line numbers, highlights)
│   │   └── theming.css                  # Color variables (light/dark) — imported first
│   └── (content)/                       # Route group for content pages
│       ├── layout.tsx                   # Content layout wrapper
│       └── [[...slug]]/
│           └── page.tsx                 # Catch-all page rendering MDX content
├── content/
│   ├── meta.json                        # Top-level page ordering
│   ├── index.mdx                        # Landing page
│   └── <category>/                      # e.g. blog/, legal/, changelog/
│       ├── meta.json                    # Category page ordering
│       └── <page>.mdx                   # Individual content pages
├── components/                          # Code block components (see Code Block Components)
├── lib/
│   ├── source.ts                        # fumadocs-core source loader
│   ├── shiki.ts                         # Shared shiki config, transformers, highlightCode()
│   └── cn.ts                            # clsx + tailwind-merge utility
├── mdx-components.tsx                   # MDX element → React component mappings
└── source.config.ts                     # fumadocs-mdx collection + rehype pipeline
```

---

## Content Collection

### `source.config.ts`

Defines two things:

1. **The content collection** — `defineDocs()` pointing at the `content/` directory with a Zod-extended frontmatter schema.
2. **The MDX pipeline** — `defineConfig()` with rehype-pretty-code replacing the default fumadocs highlighter.

Key patterns:

- Call `plugins.shift()` inside `rehypePlugins` to remove the built-in fumadocs syntax highlighter, then `plugins.push()` rehype-pretty-code.
- Configure **dual shiki themes** (one light, one dark) so both color sets are embedded in the markup. CSS toggles which is visible.
- Pass custom **shiki transformers** that inject metadata into the AST (raw source text) for components to read at render time.
- Use `onVisitTitle` to add `not-prose` to code block title elements so prose typography doesn't affect them.

### `next.config.ts`

Wrap the Next.js config with `createMDX()` from `fumadocs-mdx/next`.

### `lib/source.ts`

Create a `loader()` from `fumadocs-core/source` with a `baseUrl` and the collection's `.toFumadocsSource()`. Export the source and a `Page` type via `InferPageType`.

---

## Content Files

### MDX Frontmatter

Every `.mdx` file starts with YAML frontmatter validated by the Zod schema in `source.config.ts`. Imports go after the closing `---`. React components can be used inline alongside standard markdown. Code blocks use fenced syntax with language tags, and a `title="filename.tsx"` meta string adds a title bar.

### `meta.json`

Controls page ordering within a directory — an array of slug strings:

```json
{
  "pages": ["index", "terms-of-service", "privacy-policy"]
}
```

---

## Catch-All Content Page

The `[[...slug]]/page.tsx` route resolves slugs via `source.getPage(params.slug)`, returns `notFound()` if missing, and renders:

```tsx
<article className="prose">
  <h1>{page.data.title}</h1>
  <p className="text-muted-foreground">{page.data.description}</p>
  <MDX components={getMDXComponents()} />
</article>
```

Export `generateStaticParams` using `source.generateParams()` for static generation.

---

## Shiki Configuration

### `lib/shiki.ts`

Centralizes all syntax highlighting config. Used by **both** the MDX pipeline (build-time) and custom code components (runtime).

This module should export:

1. **A language map** — `Record<string, BuiltinLanguage>` mapping file extensions (`ts`, `tsx`, `sh`, etc.) to shiki language identifiers. Plus a `getLanguageFromExtension()` helper.

2. **Shiki transformers** — run during MDX compilation, attaching custom properties to AST nodes that components read at render time. Attach the raw source string (for copy button) so the component mapping can use it.

3. **`highlightCode(code, language)`** — an async function using `codeToHtml()` with the **same dual themes** as the MDX pipeline. This is the consistency mechanism — both build-time and runtime highlighting use identical shiki config and produce the same data attributes (`data-line-numbers`, `data-line`), ensuring matching visual output everywhere.

---

## MDX Component Mappings

### `mdx-components.tsx`

Maps HTML elements from the MDX compiler to React components. This is the bridge between raw markdown and the component system.

Key mappings:

- **`code`** — Renders a styled inline `<code>` element.

- **`pre`** — Reads transformer metadata from props. Renders a `<pre>` with a `CopyButton` overlay using the raw source text.

- **`img`** — Optionally wrap with Next.js `Image` for optimization.

The flow: author writes fenced code block → rehype-pretty-code + shiki produce `<pre><code>` with syntax tokens → shiki transformers attach metadata → MDX calls these mappings → components read metadata and render accordingly.

---

## Code Block Components

Build these client components for the code display system:

### `CodeBlock`

Single code display. Accepts `highlightedCode` (HTML string), `language`, optional `title`, `rawCode` (for copy), `maxHeight`, `wrap`. Renders a `<figure data-rehype-pretty-code-figure>` with optional `<figcaption>` title bar, the highlighted HTML via `dangerouslySetInnerHTML`, and a `CopyButton`.

### `CodeBlockTabs`

Multi-file tabbed code. Accepts an array of `{ filename, highlightedCode, rawCode }` tabs. Uses controlled tab state. Renders tabs in a `<figcaption>` with a `CopyButton` for the active tab.

### `CopyButton`

Clipboard button with visual feedback. Uses a `useCopyToClipboard` hook that calls `navigator.clipboard.writeText()` and shows a checkmark for ~2 seconds. Positioned absolutely (top-right) with opacity transition on group hover.

---

## Styling Architecture

### `globals.css` — Import Order

```css
@import 'tailwindcss';
@import './theming.css';
@import './prose.css';
@import './shiki.css';
```

`theming.css` must come first — it defines the color variables that prose and shiki consume.

### `theming.css` — Color Variables

Define light and dark mode variables consumed by `shiki.css` and component classes:

- `--color-code` — code block background
- `--color-code-foreground` — code block text
- `--color-code-highlight` — highlighted line background

### `prose.css` — Self-Contained Typography

A hand-rolled `.prose` class that doesn't depend on `@tailwindcss/typography` or any UI framework. Use `:where()` selectors to keep specificity at zero. Use `.not-prose` as an escape hatch for embedded components.

Cover at minimum: body color and line-height, headings (h1–h6), paragraphs, links, strong, lists (ul/ol/li), blockquotes, horizontal rules, tables, and code figures (`figure[data-rehype-pretty-code-figure]`).

Design decisions:
- Body text at reduced opacity (e.g. 70% of `--foreground` via `color-mix`) for softer reading
- Headings at full `--foreground` with tighter line-height
- Code figures with vertical margin and first/last child resets

### `shiki.css` — Code Block Styles

Style all code blocks uniformly — MDX-rendered and component-rendered both use the same data attributes.

Key rules:

- **Dual-theme switching** — In `.dark`, swap `color` to `var(--shiki-dark)` on `[data-rehype-pretty-code-figure] span`. Light theme is the default; shiki embeds both color sets as CSS variables.
- **Container** — `[data-rehype-pretty-code-figure]` gets background from `--color-code`, rounded corners, overflow hidden.
- **Line numbers** — CSS counters on `[data-line-numbers] [data-line]::before`. Sticky left position so they stay visible on horizontal scroll.
- **Line highlighting** — `[data-highlighted-line]` gets a subtle background and left border.
- **Title bar** — `[data-rehype-pretty-code-title]` styled with mono font, muted color, bottom border.
- **Text wrapping** — `[data-wrap='true'] code` enables `white-space: pre-wrap`.

---

## Consistency Model

The system ensures a fenced markdown code block and a `<CodeBlock>` React component produce **identical** visual output. This is achieved through:

1. **Same shiki themes** — Both MDX pipeline and `highlightCode()` use the same dual-theme pair.
2. **Same CSS targets** — Both produce `[data-rehype-pretty-code-figure]` elements styled by `shiki.css`.
3. **Same data attributes** — `data-line`, `data-line-numbers`, `data-highlighted-line`, `data-wrap` are used by both paths.
4. **Same color variables** — `--color-code` family from `theming.css` applies uniformly.
5. **Shared copy button** — Every code display uses the same `CopyButton` component.

---

## Implementation Checklist

1. Install dependencies: `fumadocs-mdx`, `fumadocs-core`, `shiki`, `rehype-pretty-code`, `zod`
2. Create `source.config.ts` with frontmatter schema and rehype-pretty-code pipeline
3. Wrap `next.config.ts` with `createMDX()`
4. Create `lib/source.ts` with the source loader
5. Create `lib/shiki.ts` with language map, transformers, and `highlightCode()`
6. Create `mdx-components.tsx` mapping `pre` and `code` to custom components
7. Create code block components (`CodeBlock`, `CodeBlockTabs`, `CopyButton`)
8. Set up `prose.css` (self-contained typography) and `shiki.css` (code block styling)
9. Define theme variables in `theming.css` including `--color-code` family
10. Create content directory with `meta.json` files
11. Create catch-all `[[...slug]]/page.tsx` route
12. Import stylesheets in `globals.css` in correct order (theming → prose → shiki)
