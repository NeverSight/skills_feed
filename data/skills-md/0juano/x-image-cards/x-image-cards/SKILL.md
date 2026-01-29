---
name: x-image-cards
description: Create X/Twitter cards that look like images, not marketing banners. Use when asked to "create OG images", "set up X cards", "make social cards", or "twitter card without text".
metadata:
  author: 0juano
  version: "1.0.0"
---

# X Image Cards

Create X cards that look like images, not marketing banners. Let the visual be the content — X already shows your title and description in the card UI.

## X-Specific Requirements

| Spec | Value | Why |
|------|-------|-----|
| Dimensions | 2400×1200 physical (1200×600 logical) | 2x for retina, 2:1 aspect ratio |
| Safe margins | 50-56px padding (at 1x) | X clips edges on mobile |
| URL format | `/og/page.png` not `/og/page?format=png` | X prefers explicit extensions |
| Colors | `#FFFFFF` primary, avoid subtle grays | Thumbnails are tiny |

## Zero-Width Space Trick

X overlays `og:title` as white text on the image. Hide it with a zero-width space:

```html
<meta property="og:title" content="&#8203;" />
```

In JSX: `content={"\u200B"}`

Your page `<title>` stays descriptive for SEO — only `og:title` uses the trick.

## Meta Tags

```html
<meta property="og:image" content="https://example.com/og/page.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="600" />
<meta property="og:title" content="&#8203;" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:image" content="https://example.com/og/page.png" />
```

## Dynamic Generation

Use `@vercel/og` with 2x scale and safe margins:

```typescript
import { ImageResponse } from '@vercel/og';

const OG_SCALE = 2;

export async function GET(request: Request) {
  return new ImageResponse(
    (
      <div style={{
        width: '100%',
        height: '100%',
        display: 'flex',
        backgroundColor: '#0a0f1c',
        padding: 100, // 50px * 2 for safe margins
      }}>
        {/* Your visual content here */}
      </div>
    ),
    { width: 1200 * OG_SCALE, height: 600 * OG_SCALE }
  );
}
```

### Express

```typescript
app.get('/og/:slug.png', async (req, res) => {
  const image = new ImageResponse(/* ... */);
  const buffer = await image.arrayBuffer();

  res.setHeader('Content-Type', 'image/png');
  res.setHeader('Cache-Control', 'public, max-age=86400');
  res.send(Buffer.from(buffer));
});
```

## Dynamic Routes (Optional)

For per-page OG images, two approaches:

### On-Demand Generation
Generate when crawler requests the image:
```
/og/[slug].png  →  generates image on request
```

**Risk:** X crawlers timeout after ~5 seconds. Cold starts can exceed this, causing blank previews.

### Pre-Generated (Recommended)
Generate and store image when content is created:
```typescript
// On content creation
const imageBuffer = await generateOgImage(data);
await db.insert({ ogImageData: imageBuffer }); // Store as BYTEA

// On request - instant response
app.get('/og/:id.png', (req, res) => {
  const { ogImageData } = await db.get(req.params.id);
  res.setHeader('Content-Type', 'image/png');
  res.send(ogImageData);
});
```

Pre-generation ensures instant response for crawlers.

## Checklist

- [ ] 2400×1200 (2x retina)
- [ ] 2:1 aspect ratio
- [ ] 50-56px safe margins
- [ ] High contrast colors
- [ ] `.png` extension in URL
- [ ] Zero-width space in `og:title`
- [ ] Test: https://cards-dev.twitter.com/validator

---

*Built for [BondTerminal](https://bondterminal.com). See it in action: [example X post](https://x.com/0juano/status/2016559903578407358).*
