---
name: og-image
description: Generate Open Graph (OG) images and social media preview cards for websites, blog posts, and products. Use when creating social share images, Twitter/X cards, LinkedIn post images, or any visual preview that appears when sharing links on social platforms. Produces properly sized images (1200x630, 1200x675, etc.) with crisp typography and professional layouts.
---

# OG Image Generator

Generate Open Graph and social media preview images via `html2png.dev`.

## Standard Sizes

| Platform          | Size      | Aspect Ratio  |
| ----------------- | --------- | ------------- |
| Facebook/LinkedIn | 1200×630  | 1.91:1        |
| Twitter/X         | 1200×675  | 1.78:1 (16:9) |
| Twitter Large     | 1200×600  | 2:1           |
| Square            | 1200×1200 | 1:1           |

## Endpoint

```
POST https://html2png.dev/api/convert
```

## Example

```bash
curl -X POST "https://html2png.dev/api/convert?width=1200&height=630&deviceScaleFactor=2" \
  -H "Content-Type: text/html" \
  -d '<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
</head>
<body class="flex items-center justify-center" style="width: 1200px; height: 630px; font-family: Inter, sans-serif; background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);">
  <div class="text-center text-white px-16">
    <h1 class="text-7xl font-extrabold mb-6 leading-tight">How to Build APIs</h1>
    <p class="text-3xl opacity-90 mb-8">A complete guide to RESTful design</p>
    <div class="flex items-center justify-center gap-4">
      <div class="w-16 h-16 rounded-full bg-white/20"></div>
      <span class="text-xl">By John Doe · 10 min read</span>
    </div>
  </div>
</body>
</html>'
```

## Key Elements

**Typography:**

- Large, bold headline (60-80px)
- Readable subheadline (24-32px)
- High contrast against background

**Layout:**

- Centered or left-aligned content
- Generous padding (60-100px)
- Clear visual hierarchy

**Backgrounds:**

- Gradient overlays
- Subtle patterns
- Brand colors

**Images:**

- Author avatars (circular, 80-120px)
- Logos (top corner or centered)
- Decorative elements (subtle)

## CDN Resources

**Fonts:**

```html
<link
  href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap"
  rel="stylesheet"
/>
```

**Icons:**

```html
<script src="https://unpkg.com/lucide@latest"></script>
```

## Tips

- Always use `deviceScaleFactor=2` for crisp text
- Use `delay=1000` for font loading
- Keep text minimal (3-5 words headline max)
- Test at small sizes (images get compressed in feeds)
- Use high contrast for readability

## Rate Limits

50 requests/hour per IP.
