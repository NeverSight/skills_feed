---
name: seo-baseline
description: |
  Quick SEO checklist for any URL. Essential basics in 15 minutes.
  Lighter than full /seo-audit - just the must-haves.

  Auto-invoke when: shipping new product, reviewing landing page,
  or user mentions SEO basics.
argument-hint: "[url]"
---

# /seo-baseline

Essential SEO in 15 minutes. No fluff.

## What This Does

Checks the absolute basics that every page needs:
1. Title tag (exists, good length, keyword)
2. Meta description (exists, compelling, right length)
3. OG image (exists, right size)
4. Sitemap (exists, accessible)
5. robots.txt (allows indexing)

That's it. Not a full audit. Just the table stakes.

## Process

### 1. Fetch Page & Check Meta Tags

Use browser automation or curl to fetch the page:

```bash
curl -s "$URL" | head -200
```

Or with browser tools:
```
mcp__claude-in-chrome__navigate to URL
mcp__claude-in-chrome__javascript_tool to extract meta tags
```

**Check Title Tag:**
```javascript
document.querySelector('title')?.textContent
```
- [ ] Exists
- [ ] 50-60 characters
- [ ] Contains primary keyword
- [ ] Unique (not generic like "Home")

**Check Meta Description:**
```javascript
document.querySelector('meta[name="description"]')?.content
```
- [ ] Exists
- [ ] 150-160 characters
- [ ] Compelling (would you click?)
- [ ] Contains primary keyword

**Check OG Tags:**
```javascript
({
  title: document.querySelector('meta[property="og:title"]')?.content,
  description: document.querySelector('meta[property="og:description"]')?.content,
  image: document.querySelector('meta[property="og:image"]')?.content,
})
```
- [ ] og:title exists
- [ ] og:description exists
- [ ] og:image exists (1200x630px recommended)

### 2. Check Sitemap

```bash
curl -s "${DOMAIN}/sitemap.xml" | head -20
```

- [ ] Sitemap exists at /sitemap.xml
- [ ] Returns valid XML
- [ ] Contains page URLs

If missing, note: "Add sitemap generation to build process"

### 3. Check robots.txt

```bash
curl -s "${DOMAIN}/robots.txt"
```

- [ ] robots.txt exists
- [ ] Does NOT block important pages
- [ ] Points to sitemap

Good robots.txt:
```
User-agent: *
Allow: /

Sitemap: https://example.com/sitemap.xml
```

Bad robots.txt:
```
User-agent: *
Disallow: /
```

### 4. Check Google Search Console

Prompt user:
```
Is this site added to Google Search Console?

If not:
1. Go to https://search.google.com/search-console
2. Add property: [domain]
3. Verify ownership (DNS or HTML file)
4. Submit sitemap

This enables Google to find and index your pages.
```

## Output Format

```
SEO BASELINE CHECK: volume.app
═══════════════════════════════════════════════════

TITLE TAG                                    ✅ PASS
  "Volume - Track Your Lifts"
  52 characters (good)
  Contains keyword "track lifts"

META DESCRIPTION                             ✅ PASS
  "Simple strength training tracker..."
  156 characters (good)
  Compelling and keyword-rich

OG IMAGE                                     ⚠️ FIX
  Missing og:image tag
  → Add: <meta property="og:image" content="https://volume.app/og.png"/>
  → Create 1200x630px image

SITEMAP                                      ✅ PASS
  Found at /sitemap.xml
  Contains 12 URLs

ROBOTS.TXT                                   ✅ PASS
  Allows all crawlers
  References sitemap

GOOGLE SEARCH CONSOLE                        ❓ CHECK
  Verify site is added and sitemap submitted

═══════════════════════════════════════════════════
SCORE: 4/5 checks passed

ACTION ITEMS:
1. Create OG image (1200x630px) with product screenshot
2. Add og:image meta tag to layout
3. Verify Google Search Console setup

Time to fix: ~10 minutes
```

## Quick Fixes

### Missing OG Image

Generate with Gemini image generation or screenshot:
```bash
# Option 1: Use existing screenshot
cp screenshot.png public/og.png

# Option 2: Generate with skill
~/.claude/skills/gemini-imagegen/scripts/generate_image.py \
  "Product screenshot showing [app name] dashboard, clean modern design" \
  public/og.png --size 1200x630
```

Add to `<head>`:
```html
<meta property="og:image" content="https://example.com/og.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
```

### Missing/Bad Title

Good title formula:
```
[Primary Keyword] - [Brand] | [Benefit]
```

Examples:
- "Strength Training Tracker - Volume | See Your Gains"
- "Word Puzzle Game - Crondle | Daily Brain Training"

### Missing Meta Description

Good description formula:
```
[What it does] + [Key benefit] + [Call to action or differentiator]
```

Example:
"Track your lifts and see your strength progress over time. Simple, focused, no-nonsense. Start your free workout log today."

### Missing Sitemap

For Next.js, add to `next.config.js`:
```javascript
// next-sitemap.config.js
module.exports = {
  siteUrl: 'https://example.com',
  generateRobotsTxt: true,
}
```

Then: `pnpm add next-sitemap && pnpm next-sitemap`

## vs /seo-audit

| | /seo-baseline | /seo-audit |
|---|---|---|
| Time | 15 min | 1+ hour |
| Scope | 5 essentials | Full technical SEO |
| When | New product launch | Established site optimization |
| Depth | Surface check | Deep crawl analysis |

Use `/seo-baseline` for new MVPs.
Use `/seo-audit` when you're ready to optimize.

## Related Skills

- `/seo-audit` - Full SEO audit
- `/programmatic-seo` - Pages at scale
- `/announce` - Uses good SEO for launch posts
