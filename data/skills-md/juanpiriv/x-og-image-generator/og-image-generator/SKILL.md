---
name: og-image-generator
description: Generate and optimize Open Graph meta images for social media sharing. Use this skill when building web applications that need dynamic OG image generation with support for Vercel's @vercel/og library, pre-generated image storage, and social media optimization (Twitter Cards, Facebook, LinkedIn). Handles dynamic routes, performance optimization, and includes best practices for crawler compatibility and testing.
---

# Open Graph Image Generator

Generate high-performance Open Graph images for social media sharing with support for dynamic generation and pre-generated storage patterns.

## When to use

Use this skill when:
- Building a web application that needs OG images for social sharing
- Creating meta images for articles, blog posts, or user-generated content
- Optimizing social media previews for Twitter Cards, Facebook, or LinkedIn
- Need both dynamic generation (few pages) and pre-generation (many pages) patterns
- Implementing performance-critical image generation with crawler timeout awareness

## Quick Start: Dynamic Generation (3 minutes)

### 1. Install dependency
```bash
npm install @vercel/og
```

### 2. Create API route (Next.js)
```typescript
import { ImageResponse } from '@vercel/og';

export async function GET(request: Request) {
  return new ImageResponse(
    (
      <div style={{
        width: '100%',
        height: '100%',
        display: 'flex',
        backgroundColor: '#0a0f1c',
        padding: '100px',
        fontFamily: 'system-ui, -apple-system, sans-serif',
      }}>
        <h1 style={{ color: '#fff', fontSize: '64px', fontWeight: 'bold' }}>
          Your Title
        </h1>
      </div>
    ),
    { width: 2400, height: 1200 } // 2x scale for retina
  );
}
```

### 3. Add meta tags
```html
<meta property="og:image" content="https://yoursite.com/api/og" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="600" />
<meta name="twitter:card" content="summary_large_image" />
```

### 4. Test
Visit: https://cards-dev.twitter.com/validator and paste your URL.

---

## Production Pattern: Pre-Generated Images

For user-generated content or high-traffic pages, pre-generate images when content is created to ensure instant crawler responses.

### Pre-generation at content creation
```typescript
import { ImageResponse } from '@vercel/og';

async function generateAndStoreOgImage(contentData) {
  const image = new ImageResponse(
    (
      <div style={{
        width: '100%',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        backgroundColor: '#0a0f1c',
        padding: '100px',
        justifyContent: 'space-between',
      }}>
        <h1 style={{ color: '#fff', fontSize: '64px', fontWeight: 'bold' }}>
          {contentData.title}
        </h1>
        <p style={{ color: '#b0b0b0', fontSize: '28px' }}>
          {contentData.description}
        </p>
      </div>
    ),
    { width: 2400, height: 1200 }
  );

  const buffer = await image.arrayBuffer();
  
  // Store in database
  await db.ogImages.insert({
    contentId: contentData.id,
    imageData: buffer,
    mimeType: 'image/png',
  });

  return buffer;
}
```

### Serve pre-generated image
```typescript
export async function getOgImage(contentId: string) {
  const { imageData } = await db.ogImages.findOne({ contentId });
  
  return new Response(imageData, {
    headers: {
      'Content-Type': 'image/png',
      'Cache-Control': 'public, max-age=86400', // 24 hours
    },
  });
}
```

### Express pattern
```typescript
app.get('/og/:slug.png', async (req, res) => {
  try {
    const { slug } = req.params;
    const content = await db.getContent(slug);

    const image = new ImageResponse(
      (/* JSX here */),
      { width: 2400, height: 1200 }
    );

    const buffer = await image.arrayBuffer();
    res.setHeader('Content-Type', 'image/png');
    res.setHeader('Cache-Control', 'public, max-age=86400');
    res.send(Buffer.from(buffer));
  } catch (error) {
    res.status(500).send('Generation failed');
  }
});
```

---

## Decision: Dynamic vs Pre-Generated

**Use Dynamic Generation if:**
- Few unique pages (<50)
- Content rarely changes
- Generation time < 2 seconds
- Traffic is low to medium

**Use Pre-Generation if:**
- Many unique pages (100+)
- User-generated content
- High traffic expected
- Need instant crawler response (avoid timeouts)

**Recommended:** Pre-generate for production; dynamic for development/testing.

---

## HTML Meta Tags

Include these in your page `<head>`:

```html
<!-- Open Graph -->
<meta property="og:image" content="https://example.com/og/page.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="600" />
<meta property="og:image:type" content="image/png" />
<meta property="og:title" content="Your Title​" /> <!-- Zero-width space required -->
<meta property="og:description" content="Brief description" />

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:image" content="https://example.com/og/page.png" />
<meta name="twitter:title" content="Your Title​" />
```

**Important:** Include a zero-width space (​) in `og:title` to prevent crawlers from using default title when og:image is present.

---

## Design Best Practices

### Dimensions
- **Size:** 1200×600px (2:1 aspect ratio)
- **Rendering:** 2400×1200px (2x scale for retina quality)
- **Safe margins:** 50-56px on all sides
- **Format:** PNG (lossless, predictable)

### Visual Design
- **High contrast:** Text readable at small thumbnail sizes
- **Minimal text:** 3-5 words maximum for headline
- **Brand colors:** Consistent palette with your site
- **No complex gradients:** Use solid colors or simple patterns

### Performance
- **Generation time:** Target <3 seconds (crawlers timeout at ~5s)
- **File size:** Keep <200KB per image
- **Cache:** Set to 24 hours minimum (`Cache-Control: public, max-age=86400`)

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Twitter shows blank preview | Check: zero-width space in og:title, image is 1200×600, URL is public |
| Crawler timeout (X/Twitter) | Switch to pre-generated images; dynamic generation is too slow |
| Image doesn't load on social media | Verify CDN/storage URL is public; check CORS if cross-origin |
| Generation takes >5 seconds | Reduce complexity; pre-generate instead; use smaller images |
| File size >500KB | Reduce color palette; simplify shapes; avoid complex gradients |
| Meta tags not appearing | Ensure tags are in `<head>` (not `<body>`); use valid HTML |

---

## Validation Checklist

- [ ] Image dimensions: 1200×600px (or 2400×1200px for 2x)
- [ ] Aspect ratio: 2:1
- [ ] Safe margins: 50-56px padding
- [ ] High contrast colors (WCAG AA minimum)
- [ ] File format: PNG
- [ ] File size: <200KB
- [ ] Zero-width space in `og:title`
- [ ] `Cache-Control` header: `public, max-age=86400`
- [ ] Test with Twitter Card Validator: https://cards-dev.twitter.com/validator
- [ ] Response time <3 seconds (dynamic) or instant (pre-generated)
- [ ] Fallback error handling if generation fails

---

## Implementation Patterns

### Next.js with Dynamic Route
```typescript
// app/api/og/[slug]/route.ts
import { ImageResponse } from '@vercel/og';

export async function GET(
  request: Request,
  { params }: { params: { slug: string } }
) {
  const content = await getContentBySlug(params.slug);
  
  return new ImageResponse(
    (
      <div style={{
        width: '100%',
        height: '100%',
        display: 'flex',
        backgroundColor: '#0a0f1c',
        padding: '100px',
      }}>
        <h1 style={{ color: '#fff', fontSize: '64px' }}>
          {content.title}
        </h1>
      </div>
    ),
    { width: 2400, height: 1200 }
  );
}
```

### Error Handling Pattern
```typescript
try {
  const image = new ImageResponse(/* ... */);
  return new Response(await image.arrayBuffer(), {
    headers: { 'Content-Type': 'image/png' },
  });
} catch (error) {
  console.error('OG generation failed:', error);
  // Return fallback or placeholder
  return new Response('Image generation failed', { status: 500 });
}
```

### Hybrid Cache Pattern
```typescript
export async function getOgImage(contentId: string) {
  // 1. Check cache
  const cached = await cache.get(`og:${contentId}`);
  if (cached) return cached;

  // 2. Check if generating
  if (isGenerating.has(contentId)) {
    await waitFor(contentId);
    return (await cache.get(`og:${contentId}`));
  }

  // 3. Generate with timeout
  isGenerating.add(contentId);
  try {
    const buffer = await Promise.race([
      generateOgImage(contentId),
      timeout(4000), // Crawler safety
    ]);
    await cache.set(`og:${contentId}`, buffer);
    return buffer;
  } finally {
    isGenerating.delete(contentId);
  }
}
```

---

## Common Variants

### Minimal Design
```typescript
const image = new ImageResponse(
  (
    <div style={{
      width: '100%',
      height: '100%',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      backgroundColor: '#0a0f1c',
      padding: '100px',
    }}>
      <h1 style={{ color: '#fff', fontSize: '72px', textAlign: 'center' }}>
        {title}
      </h1>
    </div>
  ),
  { width: 2400, height: 1200 }
);
```

### Card Style (Articles)
```typescript
const image = new ImageResponse(
  (
    <div style={{
      width: '100%',
      height: '100%',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'space-between',
      backgroundColor: '#0a0f1c',
      padding: '100px',
    }}>
      <div style={{ color: '#00d9ff', fontSize: '24px', fontWeight: '600' }}>
        {category}
      </div>
      <h1 style={{ color: '#fff', fontSize: '64px', fontWeight: 'bold' }}>
        {title}
      </h1>
      <div style={{ color: '#808080', fontSize: '20px' }}>
        {publishDate}
      </div>
    </div>
  ),
  { width: 2400, height: 1200 }
);
```

### With Image
```typescript
const image = new ImageResponse(
  (
    <div style={{ display: 'flex' }}>
      <img
        src={imageUrl}
        style={{
          width: '600px',
          height: '1200px',
          objectFit: 'cover',
        }}
        alt="Preview"
      />
      <div style={{ flex: 1, padding: '100px' }}>
        <h1 style={{ color: '#fff', fontSize: '64px' }}>{title}</h1>
      </div>
    </div>
  ),
  { width: 2400, height: 1200 }
);
```

---

## Resources & Links

- **Vercel OG Documentation:** https://vercel.com/docs/og-image-generation
- **Twitter Card Validator:** https://cards-dev.twitter.com/validator
- **Open Graph Protocol:** https://ogp.me
- **Twitter Cards Docs:** https://developer.twitter.com/en/docs/twitter-for-websites/cards

---

## Summary

1. **For quick setup:** Use dynamic generation pattern above
2. **For production:** Pre-generate images at content creation
3. **For testing:** Use Twitter Card Validator
4. **For performance:** Monitor generation time; cache aggressively
5. **For crawlers:** Always be aware of 5-second timeout; pre-generation is safer

---

## Version

**v1.0** | MIT License | Production Ready
