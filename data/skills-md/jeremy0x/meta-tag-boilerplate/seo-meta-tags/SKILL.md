---
name: seo-meta-tags
description: "Comprehensive SEO and social metadata implementation for HTML, Next.js App Router, and Vite (React & Vue) projects. Use when: (1) Creating, editing, or reviewing meta tags, Open Graph, Twitter Cards, canonical/hreflang links, JSON-LD structured data, theme-color, or favicon/manifest config; (2) Working with html/index.html, nextjs/metadata.ts, nextjs/dynamic-metadata-example.tsx, vite/index.html, vite/SEO.tsx, or vite/SEO.vue; (3) Adding SEO to a new page or route; (4) Migrating from react-helmet, vue-meta, or next-seo; (5) Generating dynamic metadata for content-driven pages; (6) Auditing metadata for completeness or best-practice compliance."
---

# SEO Meta Tags

Boilerplate and component library for production-ready metadata across three framework targets.

## Decision Tree

Determine the correct framework path first:

1. **Static HTML site or any-backend project** — Read [references/html.md](references/html.md)
2. **Next.js 13+ App Router** — Read [references/nextjs.md](references/nextjs.md)
3. **Vite + React** — Read [references/vite.md](references/vite.md), React section
4. **Vite + Vue 3** — Read [references/vite.md](references/vite.md), Vue section
5. **Multiple frameworks at once** — Read all relevant reference files

Then determine action type:

- **Creating metadata from scratch?** — Read matching reference → copy boilerplate → replace placeholders.
- **Updating existing metadata?** — Load file → keep structure → change requested values → verify parity across tag families.
- **Auditing / reviewing metadata?** — Run through Quality Gate below → report issues.
- **Migrating between frameworks?** — Read source reference → read target reference → map fields.

## Framework Selection

| Framework   | When to use                     | Reference                                    |
| ----------- | ------------------------------- | -------------------------------------------- |
| **HTML**    | Static sites, any backend, SSGs | [references/html.md](references/html.md)     |
| **Next.js** | Next.js 13+ App Router projects | [references/nextjs.md](references/nextjs.md) |
| **Vite**    | Vite + React or Vite + Vue apps | [references/vite.md](references/vite.md)     |

Read only the reference file that matches the user's target framework.

## Metadata Families

Every framework target must keep parity across these families. When modifying one family, verify the others remain consistent.

### 1. Essential / Primary

| Tag                 | Constraint                                                                                              |
| ------------------- | ------------------------------------------------------------------------------------------------------- |
| `<title>` / `title` | Under 60 characters                                                                                     |
| `description`       | 150-160 characters                                                                                      |
| `keywords`          | 5-10 terms max, comma-separated                                                                         |
| `author`            | Full name                                                                                               |
| `robots`            | `index, follow` by default; include `max-image-preview:large`, `max-snippet:-1`, `max-video-preview:-1` |
| `canonical`         | Absolute URL, must match deployment URL                                                                 |
| `viewport`          | `width=device-width, initial-scale=1.0`                                                                 |

### 2. Open Graph (`og:*`)

| Property                             | Notes                                                                          |
| ------------------------------------ | ------------------------------------------------------------------------------ |
| `og:type`                            | `website` for home/landing; `article` for blog posts; `product` for e-commerce |
| `og:url`                             | Absolute URL                                                                   |
| `og:title`                           | Can differ from `<title>` for social context                                   |
| `og:description`                     | Can differ from meta description                                               |
| `og:image`                           | Absolute URL, 1200x630px, JPG or PNG, under 1 MB                               |
| `og:image:width` / `og:image:height` | `1200` / `630`                                                                 |
| `og:image:alt`                       | Required when image is present                                                 |
| `og:site_name`                       | Brand name                                                                     |
| `og:locale`                          | e.g. `en_US`                                                                   |

For `article` type also include: `article:published_time`, `article:modified_time`, `article:author`, `article:tag`.

### 3. Twitter Cards (`twitter:*`)

| Property              | Notes                                        |
| --------------------- | -------------------------------------------- |
| `twitter:card`        | `summary_large_image` (default) or `summary` |
| `twitter:site`        | Organization handle with `@` prefix          |
| `twitter:creator`     | Author handle with `@` prefix                |
| `twitter:title`       | Under 70 characters                          |
| `twitter:description` | Under 200 characters                         |
| `twitter:image`       | Same spec as OG image                        |
| `twitter:image:alt`   | Required when image is present               |

### 4. Theme Color

Provide three values:

- Default: `<meta name="theme-color" content="...">` or single value
- Light: `media="(prefers-color-scheme: light)"`
- Dark: `media="(prefers-color-scheme: dark)"`

Next.js uses the `themeColor` array in the Metadata object.

### 5. Icons and Manifest

| Asset                  | Size                | Format |
| ---------------------- | ------------------- | ------ |
| `favicon.ico`          | 32x32 or multi-size | ICO    |
| `icon-16x16.png`       | 16x16               | PNG    |
| `icon-32x32.png`       | 32x32               | PNG    |
| `apple-touch-icon.png` | 180x180             | PNG    |
| `site.webmanifest`     | n/a                 | JSON   |

Generate with [favicon.io](https://favicon.io/) or [RealFaviconGenerator](https://realfavicongenerator.net/).

### 6. Structured Data (JSON-LD)

Emit a `<script type="application/ld+json">` block (HTML/Vite) or use a separate Script component in Next.js. Required keys:

```json
{
	"@context": "https://schema.org",
	"@type": "WebSite",
	"name": "",
	"description": "",
	"url": "",
	"image": { "@type": "ImageObject", "url": "", "width": 1200, "height": 630 },
	"author": { "@type": "Person", "name": "" },
	"publisher": {
		"@type": "Organization",
		"name": "",
		"logo": { "@type": "ImageObject", "url": "" }
	}
}
```

Common `@type` values: `WebSite`, `Article`, `Organization`, `Product`, `FAQPage`, `BreadcrumbList`.

### 7. Internationalization (hreflang)

```html
<link rel="alternate" hreflang="en" href="https://example.com/en/" />
<link rel="alternate" hreflang="es" href="https://example.com/es/" />
<link rel="alternate" hreflang="x-default" href="https://example.com/" />
```

Next.js equivalent: `alternates.languages` in the Metadata object.

### 8. Performance Hints

Include when external resources are used:

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="dns-prefetch" href="https://www.google-analytics.com" />
```

## Placeholder Tokens

All boilerplate files use `{{PLACEHOLDER_NAME}}` tokens. Common tokens:

| Token                                                                                               | Purpose                                    |
| --------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| `{{PAGE_TITLE}}`                                                                                    | Page `<title>`                             |
| `{{PAGE_DESCRIPTION}}`                                                                              | Meta description                           |
| `{{PAGE_URL}}`                                                                                      | Page URL (absolute)                        |
| `{{CANONICAL_URL}}`                                                                                 | Canonical URL                              |
| `{{KEYWORDS}}`                                                                                      | Comma-separated keywords                   |
| `{{AUTHOR_NAME}}`                                                                                   | Content author                             |
| `{{SITE_NAME}}`                                                                                     | Brand / site name                          |
| `{{THEME_COLOR}}` / `{{THEME_COLOR_LIGHT}}` / `{{THEME_COLOR_DARK}}`                                | Hex color codes                            |
| `{{OG_TITLE}}` / `{{OG_DESCRIPTION}}` / `{{OG_IMAGE_URL}}` / `{{OG_IMAGE_ALT}}`                     | Open Graph                                 |
| `{{TWITTER_TITLE}}` / `{{TWITTER_DESCRIPTION}}` / `{{TWITTER_IMAGE_URL}}` / `{{TWITTER_IMAGE_ALT}}` | Twitter                                    |
| `{{TWITTER_HANDLE}}` / `{{TWITTER_CREATOR_HANDLE}}`                                                 | Twitter handles                            |
| `{{SCHEMA_TYPE}}` / `{{SCHEMA_IMAGE_URL}}`                                                          | JSON-LD                                    |
| `{{PUBLISHER_NAME}}` / `{{PUBLISHER_LOGO_URL}}`                                                     | Publisher org                              |
| `{{FAVICON_32x32_URL}}` / `{{FAVICON_16x16_URL}}` / `{{APPLE_TOUCH_ICON_URL}}`                      | Icons                                      |
| `{{AUTHOR_URL}}`                                                                                    | Author website URL (Next.js)               |
| `{{CREATOR_NAME}}`                                                                                  | Content creator name (Next.js)             |
| `{{CATEGORY}}`                                                                                      | Site category (Next.js)                    |
| `{{GOOGLE_VERIFICATION_CODE}}` / `{{YANDEX_VERIFICATION_CODE}}` / `{{FACEBOOK_VERIFICATION_CODE}}`  | Search engine verification codes (Next.js) |
| `{{EN_URL}}` / `{{ES_URL}}`                                                                         | Language-specific alternate URLs (Next.js) |
| `{{ALTERNATE_EN_URL}}` / `{{ALTERNATE_DEFAULT_URL}}`                                                | hreflang alternate URLs (HTML/Vite)        |

When implementing for a user, replace every `{{...}}` token. Never leave placeholders in production output.

## Quality Gate

Run these checks before considering any metadata task complete:

1. **No placeholders** — grep for `{{` in all modified files; count must be zero.
2. **Absolute URLs** — canonical, OG url, OG image, Twitter image, JSON-LD url/image must start with `https://`.
3. **Image alt text** — every `og:image` / `twitter:image` must have a corresponding alt field.
4. **No duplicate tags** — no two conflicting `<title>`, `description`, or `canonical` tags in the same scope.
5. **Title length** — verify under 60 characters.
6. **Description length** — verify 150-160 characters.
7. **JSON-LD validity** — valid JSON with required `@context` and `@type` keys.
8. **OG/Twitter parity** — if OG title is set, Twitter title should also be set (and vice versa).
9. **Canonical consistency** — canonical URL matches the actual page URL or intended redirect target.
10. **Theme color** — includes both light and dark media variants.
11. **hreflang** — includes `x-default` when language alternates exist.
12. **Robots** — allows indexing unless user explicitly requests noindex.

## Image Specifications

| Use case     | Dimensions | Ratio  | Format     | Max size |
| ------------ | ---------- | ------ | ---------- | -------- |
| OG / Twitter | 1200x630   | 1.91:1 | JPG or PNG | 1 MB     |
| Favicon 32   | 32x32      | 1:1    | PNG        | n/a      |
| Favicon 16   | 16x16      | 1:1    | PNG        | n/a      |
| Apple Touch  | 180x180    | 1:1    | PNG        | n/a      |

## Testing Tools

Recommend to users after deployment:

- [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)
- [Twitter Card Validator](https://cards-dev.twitter.com/validator)
- [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/)
- [Open Graph Check](https://www.opengraph.xyz/)
- [Schema Markup Validator](https://validator.schema.org/)
- [Google Rich Results Test](https://search.google.com/test/rich-results)

## Common Mistakes

| Mistake                                                | Impact                                       | Fix                                                                    |
| ------------------------------------------------------ | -------------------------------------------- | ---------------------------------------------------------------------- |
| Relative URLs in `og:image` or `twitter:image`         | Social platforms can't fetch the image       | Always use absolute URLs starting with `https://`                      |
| Missing `<HelmetProvider>` in Vite React               | All `<SEO>` tags silently fail to render     | Wrap app root in `<HelmetProvider>` in `main.tsx`                      |
| Missing `createHead()` in Vite Vue                     | `useHead()` throws at runtime                | Call `app.use(createHead())` in `main.ts`                              |
| Committing verification codes to public repos          | Exposes site ownership tokens                | Use environment variables for `verification` values                    |
| Duplicate `<title>` or `description` tags              | Crawlers pick an unpredictable one           | Use only one source of truth per scope (layout vs. page)               |
| `og:image` set without `og:image:alt`                  | Accessibility failure, some validators warn  | Always pair image with alt text                                        |
| Using `generateMetadata` for static pages              | Unnecessary async overhead on every request  | Use static `export const metadata` when values are known at build time |
| Leaving `{{...}}` placeholder tokens                   | Broken display on social platforms, poor SEO | Grep for `{{` before shipping                                          |
| JSON-LD with trailing commas or comments               | Invalid JSON, structured data ignored        | Validate JSON before finishing                                         |
| `twitter:card` set to `summary` when image is 1200x630 | Image gets cropped to tiny square            | Use `summary_large_image` for landscape images                         |

## Migration Paths

| From                  | To                      | Notes                                                              |
| --------------------- | ----------------------- | ------------------------------------------------------------------ |
| `react-helmet`        | Vite React (`SEO.tsx`)  | Replace with `react-helmet-async`; wrap root in `<HelmetProvider>` |
| `vue-meta`            | Vite Vue (`SEO.vue`)    | Replace `metaInfo` with `@unhead/vue` `useHead()` composable       |
| `next-seo`            | Next.js (`metadata.ts`) | Remove `<NextSeo>`; use exported `metadata` or `generateMetadata`  |
| Pages Router `<Head>` | App Router              | Replace `import Head` with `export const metadata`                 |
