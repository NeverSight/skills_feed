---
name: letsgo
disable-model-invocation: true
description: |
  Production readiness checklist covering domains, SEO, security, and deployment.
  Use when asked to "ship it", "deploy to production", "go live", "launch",
  or when preparing a project for production deployment.
license: MIT
metadata:
  author: howells
website:
  order: 11
  desc: Pre-launch checklist
  summary: The pre-launch checklist. Walks through domains, SEO, security headers, error pages, analytics, legal docs, and deployment—tailored to what your project actually uses.
  what: |
    Letsgo scans your project to understand what you're using (auth? payments? database?), then generates a tailored checklist. It covers: domain setup, DNS configuration, SSL. SEO basics—meta tags, OG images, sitemap, robots.txt. Security headers and environment variables. Error pages (404, 500). Analytics and monitoring. Legal pages (triggers /arc:legal if missing). Performance basics. For Vercel projects, it can deploy directly.
  why: |
    The difference between "it works on my machine" and "it works in production" is a hundred small things—DNS, headers, error pages, meta tags. Letsgo is the checklist so you don't ship with a missing favicon and broken OG images.
  decisions:
    - Scans your stack first. Knows if you have Stripe, auth, a database—tailors the checklist.
    - Interactive walkthrough. One section at a time, tracks what's done.
    - Triggers /arc:legal automatically if privacy policy or terms are missing.
---

<progress_context>
**Use Read tool:** `docs/progress.md` (first 50 lines)

Check what's been done recently — ensures nothing is missed before shipping.
</progress_context>

# Letsgo Workflow

Prepare a codebase for production. Generates a **tailored checklist** based on project detection and user input—not a generic one-size-fits-all list.

## Process

### Step 1: Project Detection

Scan the codebase to understand what's present. Look for:

```
Detection signals:
├── Framework: package.json (next, remix, astro, etc.)
├── Auth: auth libraries, OAuth config, session handling
├── Payments: stripe, paddle, lemon-squeezy
├── Email: resend, sendgrid, postmark, nodemailer
├── Database: prisma, drizzle, supabase, planetscale
├── Analytics: GA, mixpanel, posthog, plausible
├── i18n: next-intl, i18next, locale files
├── CMS: sanity, contentful, payload
├── File uploads: uploadthing, cloudinary, S3 config
└── Existing meta: robots.txt, sitemap, og images
```

Report findings:
```markdown
## Project Detection

**Framework:** Next.js 14 (App Router)
**Detected features:**
- ✓ Authentication (NextAuth with Google, GitHub providers)
- ✓ Payments (Stripe)
- ✓ Database (Prisma + PostgreSQL)
- ✓ Email (Resend)
- ✗ i18n (not detected)
- ✗ Analytics (not configured)

**Existing production config:**
- ✓ robots.txt present
- ✗ sitemap.xml missing
- ✗ Site verification meta tags missing
```

### Step 2: Scope Questions

Ask the user to fill gaps detection can't cover:

```markdown
**Questions to scope your checklist:**

1. **Target platforms for site verification?**
   - [ ] Google Search Console
   - [ ] Bing Webmaster Tools
   - [ ] Pinterest
   - [ ] Twitter/X
   - [ ] Facebook/Meta
   - [ ] Yandex
   - [ ] Other: ___

2. **Social sharing requirements?**
   - [ ] Need OG images for all pages
   - [ ] Twitter Cards (summary vs large image)
   - [ ] LinkedIn sharing
   - [ ] Pinterest Rich Pins

3. **Email sending from custom domain?**
   - [ ] Yes (need SPF/DKIM/DMARC DNS records)
   - [ ] No (using provider's domain)

4. **Compliance requirements?**
   - [ ] GDPR (EU users)
   - [ ] CCPA (California)
   - [ ] Cookie consent banner
   - [ ] Accessibility (WCAG 2.1)

5. **Launch type?**
   - [ ] Soft launch (limited audience)
   - [ ] Public launch (SEO, marketing)
   - [ ] Migration (redirects needed)
```

### Step 3: Generate Tailored Checklist

Based on detection + user input, generate ONLY relevant sections:

---

## Checklist Categories

### A. Domain & Hosting (Always)
- [ ] Domain purchased and configured
- [ ] DNS records set up (A/CNAME to Vercel)
- [ ] SSL certificate active (automatic on Vercel)
- [ ] Vercel project linked
- [ ] Environment variables set in Vercel dashboard
- [ ] Production branch configured (main/master)
- [ ] Preview deployments working

### B. Site Verification (If user selected platforms)
```html
<!-- Google Search Console -->
<meta name="google-site-verification" content="..." />

<!-- Bing Webmaster -->
<meta name="msvalidate.01" content="..." />

<!-- Pinterest -->
<meta name="p:domain_verify" content="..." />

<!-- Twitter/X (for analytics, not cards) -->
<meta name="twitter:site:id" content="..." />

<!-- Facebook/Meta domain verification -->
<meta name="facebook-domain-verification" content="..." />

<!-- Yandex -->
<meta name="yandex-verification" content="..." />
```

Checklist:
- [ ] Google Search Console verified (HTML tag or DNS)
- [ ] Sitemap submitted to Google Search Console
- [ ] Bing Webmaster Tools verified
- [ ] Pinterest site claimed
- [ ] Facebook domain verified (for ads/insights)
- [ ] Twitter/X analytics connected

### C. SEO & Meta (Always for public sites)

> Reference: `${CLAUDE_PLUGIN_ROOT}/rules/seo.md` for full SEO rules.

- [ ] `<html lang="...">` attribute set
- [ ] `<meta name="viewport">` present
- [ ] Page titles set (unique, <60 chars per page)
- [ ] Meta descriptions written (unique, <160 chars per page)
- [ ] Single `<h1>` per page, logical heading hierarchy
- [ ] Canonical URLs set (avoid duplicate content)
- [ ] Images have meaningful `alt` text
- [ ] No `noindex` on production marketing pages (check for Vercel preview leftover)
- [ ] Clean URL structure (no UUIDs, no query params for content)
- [ ] robots.txt configured and not blocking marketing pages
- [ ] sitemap.xml generated and submitted
- [ ] Structured data / JSON-LD (if applicable)
- [ ] Rich Results Test passing

*For a comprehensive SEO audit, run `/arc:seo`.*

### D. Social Sharing / Open Graph
- [ ] og:title, og:description, og:image set
- [ ] og:image is 1200x630px (optimal for all platforms)
- [ ] Twitter Card meta tags (twitter:card, twitter:title, etc.)
- [ ] Twitter Card type chosen (summary vs summary_large_image)
- [ ] **Validated with real tools:**
  - [ ] [Twitter Card Validator](https://cards-dev.twitter.com/validator)
  - [ ] [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)
  - [ ] [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/)
  - [ ] [Pinterest Rich Pins Validator](https://developers.pinterest.com/tools/url-debugger/)

**Next.js OG Image Generation (Recommended for Next.js projects):**

Offer to set up dynamic OG images using Next.js built-in `ImageResponse`:

```typescript
// app/og/route.tsx - Dynamic OG image generation
import { ImageResponse } from 'next/og'

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const title = searchParams.get('title') ?? 'Default Title'

  return new ImageResponse(
    (
      <div style={{ /* your design */ }}>
        <h1>{title}</h1>
      </div>
    ),
    { width: 1200, height: 630 }
  )
}
```

Then reference in metadata:
```typescript
// app/layout.tsx or page.tsx
export const metadata: Metadata = {
  openGraph: {
    images: ['/og?title=Your+Page+Title'],
  },
}
```

**⚠️ OG Image Design Quality:**

OG images are often the first impression of your product. Avoid:
- PowerPoint-style slides with generic gradients
- Stock photo backgrounds with overlaid text
- Default template looks (Canva templates, etc.)
- Tiny unreadable text
- Generic "hero image + title" layouts

**Use `/arc:design` to create distinctive OG image designs** that match your brand and stand out in social feeds. The OG image should feel like part of your product, not an afterthought.

Good OG images have:
- Clear visual hierarchy (title readable at thumbnail size)
- Brand colors and typography
- Memorable visual element or illustration
- Consistent style across all pages

### E. Favicons & App Icons
- [ ] favicon.ico (16x16, 32x32)
- [ ] apple-touch-icon.png (180x180)
- [ ] android-chrome icons (192x192, 512x512)
- [ ] site.webmanifest (if PWA)
- [ ] Theme color meta tag

**Next.js Metadata API (Recommended for Next.js projects):**

Next.js can auto-generate favicons from a single source. Offer to set up:

```
app/
├── icon.tsx          # Dynamic favicon (uses ImageResponse)
├── icon.png          # Or static favicon (auto-detected)
├── apple-icon.png    # Apple touch icon (auto-detected)
└── opengraph-image.tsx  # Dynamic OG image per route
```

Example dynamic favicon:
```typescript
// app/icon.tsx
import { ImageResponse } from 'next/og'

export const size = { width: 32, height: 32 }
export const contentType = 'image/png'

export default function Icon() {
  return new ImageResponse(
    (
      <div style={{
        fontSize: 24,
        background: '#000',
        color: '#fff',
        width: '100%',
        height: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        borderRadius: 4,
      }}>
        A
      </div>
    ),
    { ...size }
  )
}
```

**⚠️ Favicon Design Quality:**

Favicons appear in browser tabs, bookmarks, and home screens. Avoid:
- Just shrinking your full logo (unreadable at 16px)
- Generic letter in a colored square
- Too much detail that becomes muddy

**Use `/arc:design` for favicon concepts** if you don't have a dedicated icon mark. Good favicons:
- Work at 16x16, 32x32, and 180x180 (apple-touch-icon)
- Use a simplified version of your brand mark
- Are recognizable in a sea of browser tabs
- Have sufficient contrast on both light and dark browser chrome

### F. Performance (Always)
- [ ] Images optimized (next/image, srcset, WebP/AVIF)
- [ ] Fonts optimized (display: swap, preload critical)
- [ ] Font rendering classes on body (see below)
- [ ] Bundle size reasonable (check with `next build` output)
- [ ] No console errors in production build
- [ ] Core Web Vitals passing (LCP, FID, CLS)
- [ ] Lighthouse score acceptable (aim for 90+)

**Font Rendering & Body Classes:**

Ensure the `<body>` has proper font rendering classes for crisp text:

```tsx
// Tailwind CSS
<body className="antialiased">

// Or with more control:
<body className="antialiased text-base leading-relaxed text-foreground bg-background">
```

If not using Tailwind, add equivalent CSS:
```css
body {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
}
```

Additional body-level considerations:
- [ ] `antialiased` class applied (smoother fonts on macOS/iOS)
- [ ] Base text color set (not relying on browser default black)
- [ ] Base background color set (prevents flash of white)
- [ ] `overflow-x-hidden` on html/body if using full-bleed sections
- [ ] `scroll-behavior: smooth` if desired (or Tailwind `scroll-smooth`)
- [ ] `min-h-screen` on body/main for proper footer positioning

**If React/Next.js and `vercel-react-best-practices` skill available:**
```
Invoke skill: vercel-react-best-practices
"Review performance patterns. Check: component rendering, data fetching, bundle optimization"
```

### G. Security (Always)
- [ ] No secrets in client-side code (check bundle)
- [ ] HTTPS enforced (automatic on Vercel)
- [ ] Environment variables not prefixed with NEXT_PUBLIC_ unless intended
- [ ] Auth tokens stored securely (httpOnly cookies)
- [ ] CORS configured for production origins only
- [ ] `pnpm audit` shows no critical vulnerabilities

**If handling sensitive data:**
- [ ] CSP headers configured
- [ ] Rate limiting on auth/API endpoints
- [ ] Input validation / sanitization

### H. Email Deliverability (If sending email)
- [ ] SPF record added to DNS
- [ ] DKIM record added to DNS
- [ ] DMARC record added to DNS
- [ ] Test email delivery (check spam folder)
- [ ] Unsubscribe mechanism (if marketing emails)
- [ ] From address uses verified domain

### I. Payments (If Stripe/payments detected)
- [ ] Stripe switched to **live mode** (not test)
- [ ] Live API keys in production env vars
- [ ] Webhook endpoint URL updated to production domain
- [ ] Webhook signing secret updated for production
- [ ] Test purchase completed in production
- [ ] Receipts/emails working

### J. Database (If database detected)
- [ ] Production database provisioned
- [ ] Migrations run against production
- [ ] Connection string in production env vars
- [ ] Connection pooling configured (PgBouncer, Prisma Accelerate)
- [ ] Backup strategy in place

### K. Auth (If auth detected)
- [ ] OAuth callback URLs updated to production domain
- [ ] OAuth apps approved for production (some providers require review)
- [ ] Session cookie domain configured for production
- [ ] Magic link / email verification URLs use production domain
- [ ] Auth provider dashboard shows production app

### L. Legal & Compliance (Based on user input)

**Required Documents:**
- [ ] **Privacy Policy** — Required if collecting ANY data (analytics, cookies, forms, auth)
  - What data is collected
  - How it's used and stored
  - Third parties it's shared with
  - User rights (access, deletion, portability)
  - Contact information for data requests
- [ ] **Terms of Service** — Recommended for any app/SaaS
  - Acceptable use policy
  - Liability limitations
  - Dispute resolution
  - Account termination conditions
- [ ] **Cookie Policy** — Required if using cookies (often part of Privacy Policy)
  - Types of cookies used (essential, analytics, marketing)
  - Purpose of each cookie
  - How to opt out

**Cookie Consent:**
- [ ] Cookie consent banner implemented
- [ ] Consent recorded before non-essential cookies set
- [ ] "Reject All" option available (GDPR requirement)
- [ ] Preferences can be changed after initial choice
- [ ] Analytics/tracking only fires AFTER consent

**GDPR Compliance (if EU users):**
- [ ] Legal basis for data processing documented
- [ ] Data export mechanism (user can download their data)
- [ ] Data deletion mechanism (user can request deletion)
- [ ] Data processing agreements with third parties
- [ ] Privacy policy includes EU-specific rights

**Accessibility:**
- [ ] Accessibility statement page (if WCAG compliance needed)
- [ ] Contact method for accessibility issues

**If legal documents are missing, offer to generate them:**
```
Invoke skill: /arc:legal
"Generate Privacy Policy, Terms of Service, and Cookie Policy for this project"
```

This will detect data collection, gather business info, and create template pages.

### M. Analytics & Tracking (If user wants)
- [ ] Analytics provider configured (GA4, Plausible, PostHog, etc.)
- [ ] Privacy-respecting settings (IP anonymization, etc.)
- [ ] Conversion tracking set up (if applicable)
- [ ] Events/goals configured

### N. Error Handling & Monitoring
- [ ] Custom 404 page
- [ ] Custom 500/error page
- [ ] Error tracking set up (Sentry, etc.)
- [ ] Error boundaries in React components
- [ ] Alerts configured for critical errors

### O. Quality (Always)
- [ ] All tests passing
- [ ] No TypeScript errors (`pnpm tsc --noEmit`)
- [ ] No lint errors (`pnpm biome check .` or eslint)
- [ ] `/arc:audit --deslop` run (no LLM artifacts)
- [ ] Placeholder content replaced
- [ ] Lorem ipsum removed

### P. Branding Consistency (Always)

**Audit all brand touchpoints for consistency:**

**Logo usage:**
- [ ] Correct logo version used everywhere (not outdated versions)
- [ ] Logo appears in correct sizes (not stretched/distorted)
- [ ] Logo has proper spacing/clearance
- [ ] Dark mode logo variant used where needed
- [ ] Favicon matches current logo

**Brand name casing:**
- [ ] Product name cased consistently everywhere
- [ ] Check: page titles, meta tags, footer, emails, error messages
- [ ] Third-party brand names correctly cased (see common mistakes below)

**Common brand casing mistakes to check:**
```
WRONG          → CORRECT
Github         → GitHub
Javascript     → JavaScript
Typescript     → TypeScript
NextJS/Nextjs  → Next.js
NodeJS/Nodejs  → Node.js
VSCode         → VS Code
MacOS          → macOS
iOS (correct)  → iOS (not IOS)
PostgreSQL     → PostgreSQL (not Postgres in formal contexts)
MongoDB        → MongoDB (not Mongo in formal contexts)
LinkedIn       → LinkedIn (not Linkedin)
YouTube        → YouTube (not Youtube)
PayPal         → PayPal (not Paypal)
```

**Grep for inconsistencies:**
```bash
# Find potential casing issues (case-insensitive search, then review)
grep -ri "github\|javascript\|typescript\|nextjs\|nodejs" --include="*.tsx" --include="*.ts" --include="*.md" | grep -v node_modules
```

**Brand colors:**
- [ ] Primary brand colors used consistently
- [ ] Colors defined in one place (CSS variables, Tailwind config)
- [ ] No hardcoded hex values that should use brand tokens

**Typography:**
- [ ] Brand fonts loaded and applied
- [ ] Font weights consistent with brand guidelines
- [ ] No system font fallbacks visible where brand fonts expected

**Voice & messaging:**
- [ ] Tagline consistent across touchpoints
- [ ] Product descriptions match (homepage, meta, social)
- [ ] CTA button text consistent ("Get Started" vs "Start Now" vs "Sign Up")

**Ask user:** "What is the exact casing for your product name? (e.g., 'MyApp', 'myApp', 'MYAPP')"

Then grep the codebase for variations and fix any inconsistencies.

### Q. Redirects (If migration)
- [ ] Old URLs mapped to new URLs
- [ ] 301 redirects configured in vercel.json or middleware
- [ ] www vs non-www canonical decided
- [ ] HTTP → HTTPS redirects (automatic on Vercel)

### R. Pre-Launch Testing
- [ ] Responsive audit completed (`/arc:responsive` if not done already)
- [ ] Test on real mobile device (not just DevTools)
- [ ] Test in incognito/private browsing
- [ ] Test critical user flows end-to-end
- [ ] Test with slow network (DevTools throttling)
- [ ] Check print styles (if applicable)

### S. UI Polish (Always)
- [ ] No layout shift on dynamic content (hardcoded dimensions, `tabular-nums`, no font-weight changes on hover)
- [ ] Animations have `prefers-reduced-motion` support
- [ ] Touch targets are 44px minimum
- [ ] Hover effects gated behind `@media (hover: hover)`
- [ ] Keyboard navigation works (tab order, focus trap in modals, arrow keys in lists)
- [ ] Icon-only buttons have `aria-label`
- [ ] Forms submit with Enter; textareas with ⌘/Ctrl+Enter
- [ ] Inputs are `text-base` (16px+) to prevent iOS zoom
- [ ] No `transition: all` — specify exact properties
- [ ] z-index uses fixed scale or `isolation: isolate`
- [ ] No flash on refresh for interactive state (tabs, theme, toggles)
- [ ] Destructive actions require confirmation (`AlertDialog`, not `confirm()`)

> Reference: `${CLAUDE_PLUGIN_ROOT}/rules/interface/` for detailed rules on each item.

---

### Step 4: Address Gaps

For each unchecked item relevant to this project:
1. Explain what's needed and why
2. Offer to implement or provide step-by-step instructions
3. Provide code snippets where helpful

### Step 5: Final Verification

```bash
# Build production
pnpm build

# Run tests
pnpm test

# Check for issues
pnpm tsc --noEmit
pnpm biome check .

# Check bundle for secrets (manual review)
# Look for API keys, tokens, passwords in build output
```

### Step 6: Ship

If all relevant checks pass:
```bash
# Deploy via Vercel CLI
vercel --prod

# Or via git (if Vercel GitHub integration set up)
git push origin main
```

**If `vercel:deploy` skill is available:**
```
Invoke skill: vercel:deploy
```
This handles the deployment workflow with proper verification.

<tasklist_update>
If follow-up work is identified, use **TaskCreate**:
- **subject:** Brief imperative title
- **description:** What needs to be done and why
- **activeForm:** Present continuous form
</tasklist_update>

<arc_log>
**After completing this skill, append to the activity log.**
See: `${CLAUDE_PLUGIN_ROOT}/references/arc-log.md`

Entry: `/arc:letsgo — [Deployed to URL / Checklist complete]`
</arc_log>

<success_criteria>
Letsgo is complete when:
- [ ] Project detected and checklist tailored
- [ ] All relevant checklist items addressed or deferred with reason
- [ ] Critical items resolved (no blockers remaining)
- [ ] Production build succeeds
- [ ] Deployed to production (or ready to deploy)
- [ ] Incomplete items added to tasklist (if any)
- [ ] Progress journal updated
</success_criteria>

## Interop

- Runs **/arc:test** as part of quality check
- Runs **/arc:audit --deslop** as part of quality check (LLM artifact detection)
- References **/arc:vision** to verify alignment
- Invokes **/arc:legal** to generate missing legal documents
- Can invoke **vercel-react-best-practices** skill for performance review (if available)
- Can invoke **vercel:deploy** skill for deployment (if available)
