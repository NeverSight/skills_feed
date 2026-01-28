---
name: skill-webdesign
description: Expert web designer for responsive, mobile-first websites. Specializes in landing pages using Astro, Tailwind CSS, and Cloudflare Pages. Enforces design consistency through style guides, semantic HTML, and accessibility. Prioritizes data-driven content patterns to minimize hardcoding. Trigger when working on website projects, landing pages, web components, or design system implementation.
---

# Web Designer Skill

Expert guidance for creating responsive, maintainable websites with sharp attention to design details.

## Core Principles

### Design Consistency
- Load project styleguide first—check `references/styleguide.md` or project's design tokens
- Use semantic color names (`--color-navy`) not raw values (`#1E3A5F`)
- Maintain typography hierarchy: one display size per page, consistent heading progression
- Spacing: use design tokens (`section-gap`, `card-padding`) not arbitrary values

### Mobile-First Responsive
- Start with mobile layout, progressively enhance for larger screens
- Breakpoints: `sm:640px`, `md:768px`, `lg:1024px`, `xl:1280px`
- Touch targets: minimum 44x44px for interactive elements
- Test: content readable without horizontal scroll at 320px width

### Accessibility Non-Negotiables
- Color contrast: 4.5:1 for body text, 3:1 for large text
- Focus states: visible on all interactive elements
- Semantic HTML: proper heading hierarchy, landmarks, form labels
- Images: meaningful alt text or `aria-hidden` for decorative

## Tech Stack: Astro + Tailwind + Cloudflare

### Project Structure
```
src/
├── components/
│   └── ui/           # Reusable UI components
├── layouts/          # Page layouts (BaseLayout.astro)
├── pages/            # Routes - each .astro = a page
├── content/          # Markdown/MDX for content collections
├── styles/           # Global CSS, Tailwind config
└── assets/           # Images, fonts (processed by Astro)
public/               # Static assets (copied as-is)
```

### Component Patterns

**Astro Components** - Use for static or lightly interactive UI:
```astro
---
interface Props {
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
}
const { variant = 'primary', size = 'md' } = Astro.props;
---
<button class:list={['btn', `btn-${variant}`, `btn-${size}`]}>
  <slot />
</button>
```

**Content Collections** - For blog posts, reports, case studies:
```typescript
// src/content/config.ts
import { defineCollection, z } from 'astro:content';

const posts = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.date(),
    featured: z.boolean().default(false),
    tags: z.array(z.string()).optional(),
  }),
});

export const collections = { posts };
```

### Automation Patterns

**No Hardcoding - Use Data-Driven Approaches:**

```astro
---
// ❌ Hardcoded featured posts
const featured = [{ title: "Post 1" }, { title: "Post 2" }];

// ✅ Query from content collection
import { getCollection } from 'astro:content';
const featured = await getCollection('posts', ({ data }) => data.featured);
---
```

**Dynamic Dates:**
```astro
---
// ❌ Hardcoded year
const year = "2024";

// ✅ Dynamic
const year = new Date().getFullYear();
---
<footer>© {year} Company Name</footer>
```

**Environment-Based Config:**
```typescript
// astro.config.mjs
export default defineConfig({
  site: import.meta.env.PROD 
    ? 'https://example.com' 
    : 'http://localhost:4321',
});
```

## Landing Page Structure

### Essential Sections
1. **Hero** - Clear value proposition, single primary CTA
2. **Social Proof** - Logos, testimonials, metrics
3. **Features/Benefits** - 3-4 key points with icons
4. **How It Works** - Simple 3-step process
5. **CTA Section** - Reinforce action before footer
6. **Footer** - Navigation, legal links, copyright

### SEO Checklist
- Unique `<title>` (50-60 chars) and `<meta name="description">` (150-160 chars)
- Open Graph tags for social sharing
- Canonical URL set
- Structured data (JSON-LD) for organization/product
- Sitemap.xml generated
- robots.txt configured

### Performance Targets
- Lighthouse Performance: >90
- First Contentful Paint: <1.5s
- Cumulative Layout Shift: <0.1
- Use `loading="lazy"` on below-fold images
- Prefer `<picture>` with WebP + fallback

## Workflow

1. **Before starting**: Load `references/styleguide.md` if project has design system
2. **Component creation**: Check existing UI components before creating new
3. **Styling**: Use existing design tokens; propose additions to styleguide if needed
4. **Content**: Use content collections for repeated content types
5. **Testing**: Verify mobile layout, accessibility, performance

## References

- `references/styleguide.md` - Fund Investigator design system (colors, typography, components)
- `references/astro-patterns.md` - Common Astro patterns and gotchas