---
name: html-to-image
description: Generate crisp, high-quality images with perfect typography and precise geometric layouts using HTML/CSS. Use when creating social cards, diagrams, certificates, UI mockups, code screenshots, or any image requiring sharp text rendering, exact alignment, or vector-like precision. AI excels at designing symmetric, pixel-perfect layouts as HTML rather than generating raster images directly. Supports Tailwind CSS, Google Fonts, icon libraries, and any web-based design resource.
---

# HTML to Image API

Convert HTML/CSS to PNG, WebP, or PDF via `html2png.dev`.

## Endpoint

```
POST https://html2png.dev/api/convert
```

## Request

Send HTML as raw body or JSON:

```bash
curl -X POST "https://html2png.dev/api/convert?width=1200&height=630" \
  -H "Content-Type: text/html" \
  -d '<div style="padding: 40px;">Content</div>'
```

```bash
curl -X POST "https://html2png.dev/api/convert" \
  -H "Content-Type: application/json" \
  -d '{"html": "<div>...</div>", "width": 1200}'
```

## Parameters

| Parameter           | Type   | Default  | Description             |
| ------------------- | ------ | -------- | ----------------------- |
| `html`              | string | required | HTML content            |
| `width`             | int    | 1200     | Width in px             |
| `height`            | int    | 630      | Height in px            |
| `format`            | string | png      | png, webp, pdf          |
| `deviceScaleFactor` | float  | 2        | Retina scale (1-4)      |
| `delay`             | int    | 0        | Wait ms before capture  |
| `selector`          | string | body     | CSS selector to capture |
| `omitBackground`    | bool   | false    | Transparent bg          |
| `colorScheme`       | string | -        | light or dark           |
| `zoom`              | float  | 1        | Viewport zoom           |

## Response

```json
{
  "success": true,
  "url": "https://html2png.dev/api/blob/abc.png",
  "format": "png",
  "cached": false
}
```

## CDN Resources

Use these CDNs for high-quality designs:

**Tailwind CSS (preferred):**

```html
<script src="https://cdn.tailwindcss.com"></script>
```

**Google Fonts:**

```html
<link
  href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap"
  rel="stylesheet"
/>
```

**Icons (use instead of inline SVGs):**

- Lucide: `https://unpkg.com/lucide@latest`
- Font Awesome: `https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css`

**Images:**

- Unsplash: `https://images.unsplash.com/photo-xxx`
- Any direct image URL

## Example with Tailwind + Fonts + Icons

```html
<!DOCTYPE html>
<html>
  <head>
    <script src="https://cdn.tailwindcss.com"></script>
    <link
      href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap"
      rel="stylesheet"
    />
    <script src="https://unpkg.com/lucide@latest"></script>
  </head>
  <body
    class="bg-gradient-to-br from-purple-600 to-blue-600 flex items-center justify-center"
    style="width: 1200px; height: 630px; font-family: 'Inter', sans-serif;"
  >
    <div
      class="bg-white/10 backdrop-blur-lg rounded-2xl p-12 text-white text-center"
    >
      <i data-lucide="sparkles" class="w-16 h-16 mx-auto mb-4"></i>
      <h1 class="text-6xl font-extrabold mb-4">Hello World</h1>
      <p class="text-2xl opacity-90">Beautiful generated image</p>
    </div>
    <script>
      lucide.createIcons();
    </script>
  </body>
</html>
```

Request with delay for resources to load:

```bash
curl -X POST "https://html2png.dev/api/convert?width=1200&height=630&delay=1000&deviceScaleFactor=2" \
  -H "Content-Type: text/html" \
  -d '<!DOCTYPE html>...</html>'
```

## Key Tips

- Always use `deviceScaleFactor=2` or higher for quality
- Use `delay=1000-2000` when loading fonts/icons/images
- Any CSS works: grid, flex, transforms, filters, animations
- JavaScript executes (use delay for rendering)

## Website Screenshot

```
POST https://html2png.dev/api/screenshot
```

```bash
curl -X POST "https://html2png.dev/api/screenshot" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "width": 1280, "fullPage": true}'
```

Extra params: `fullPage` (bool), `userAgent` (string)

## Rate Limits

50 requests/hour per IP. Cached results are free.
