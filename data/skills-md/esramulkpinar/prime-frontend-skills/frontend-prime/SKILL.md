---
name: frontend-prime
description: >
  Build distinctive, production-grade frontend interfaces. Use when creating any web UI —
  sites, apps, dashboards, components. Focuses on design quality and avoiding generic AI
  aesthetics. Composable with other skills (docx, pdf, xlsx).
---

# Ultimate Frontend Skill

Every output must feel intentionally crafted — never generic, never "AI slop."

---

## 1. Design Before Code

Before writing ANY code, decide:

1. **Aesthetic direction** (pick ONE, match it to the product's audience):
   Brutally minimal · Maximalist editorial · Retro-futuristic · Organic/natural · Luxury/refined · Playful · Brutalist · Art deco · Dark/moody · Lo-fi/zine · Handcrafted · Swiss/international · Neo-glassmorphic · Industrial · Soft/pastel

2. **One unforgettable element**: a scroll animation, a bold typographic moment, a micro-interaction — something memorable.

3. **Then commit fully.** Half-hearted design = generic output.

---

## 2. The AI Slop Blacklist

These instantly mark output as AI-generated. **Never:**

- Purple/blue gradient on white cards
- Every element with identical `rounded-xl`
- Perfectly centered, symmetrical layouts with no visual tension
- `text-gray-600` on everything
- Cards in a perfect 3-column grid with identical heights
- Rainbow or evenly-distributed color schemes
- Generic hero with stock illustration placeholder

**Instead, always:**

- Load distinctive Google Fonts (Instrument Serif, DM Sans, Clash Display, Bricolage Grotesque, Syne, Fraunces, Cabinet Grotesk, Satoshi, Young Serif, Outfit)
- One dominant color doing 80% of the work + one sharp accent
- Asymmetric layouts, grid-breaking elements, dramatic scale jumps
- Atmosphere via gradient meshes, noise textures, glassmorphism, or depth layers
- Generous negative space as a design element
- Negative `letter-spacing` on large headings, `text-wrap: balance` on headlines
- Body text `max-width: 65ch`, `line-height: 1.5–1.7`

---

## 3. Color & Theming — Do It Right

Define colors as CSS custom properties with semantic names. Never hardcode hex in components.

```css
[data-theme="light"] {
  --bg-primary: #fafafa; --bg-secondary: #ffffff;
  --text-primary: #18181b; --text-secondary: #52525b;
  --accent: #2563eb; --border: #e4e4e7;
}
[data-theme="dark"] {
  --bg-primary: #09090b; --bg-secondary: #18181b;
  --text-primary: #fafafa; --text-secondary: #a1a1aa;
  --accent: #3b82f6; --border: #27272a;
}
```

Dark mode rules: higher elevation = lighter surface, desaturate accents ~15%, use borders not shadows for hierarchy, offer Light/Dark/System toggle, persist in localStorage and apply before paint.

---

## 4. SEO — Claude Forgets This

Every page needs:

```html
<title>Page Title — Brand</title>
<meta name="description" content="150-160 chars">
<link rel="canonical" href="https://example.com/page">
<meta property="og:title/description/image/url" ...>
<meta name="twitter:card" content="summary_large_image">
```

Also: JSON-LD structured data, `sitemap.ts` + `robots.ts`, one `h1` per page, no skipped heading levels, descriptive `alt` text, clean lowercase hyphenated URLs, `hreflang` for i18n.

In Next.js: use `metadata` export with `metadataBase`, `openGraph`, `twitter`, `alternates.canonical`.

---

## 5. Quick Reminders

- **Motion**: Stagger entrances, hover states on all interactives, `0.2s ease` micro-interactions, always respect `prefers-reduced-motion`
- **Mobile**: Mobile-first, `clamp()` for fluid type/spacing, `dvh` not `vh`, 44×44px touch targets
- **A11y**: Semantic HTML, `<button>` for actions / `<a>` for links, `aria-label` on icon buttons, 4.5:1 contrast, full keyboard nav
- **Perf**: `font-display: swap`, lazy load images with dimensions, `content-visibility: auto`, LCP<2.5s
- **Forms**: Visible labels always, validate on blur, helpful error messages, correct `input type` + `autocomplete`
- **Errors**: Error boundaries per section, custom 404/500, toast for feedback (auto-dismiss success, persist errors)
- **Security**: CSP headers, never unsanitized `dangerouslySetInnerHTML`, validate URLs in `href`, httpOnly cookies for auth, server-side validation
