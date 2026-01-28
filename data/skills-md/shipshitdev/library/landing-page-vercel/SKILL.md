---
name: landing-page-vercel
description: Scaffold a production-ready static landing page with working email capture form, analytics, and responsive design. Deploys instantly to Vercel.
---

# Landing Page (Vercel)

Create a **production-ready** static landing page with:

- **Structure:** Semantic HTML5 + Modern CSS + Vanilla JS
- **Form:** Working email capture (Formspree or custom endpoint)
- **Analytics:** Plausible/Fathom ready
- **Design:** Responsive, accessible, performant
- **Deploy:** One-click Vercel deployment

## What Makes This Different

This skill generates **working landing pages**, not empty templates:

- Real email capture form that actually submits
- Analytics integration ready to activate
- Responsive design tested on mobile
- Accessibility basics (WCAG 2.1 AA)
- Content from your PRD brief

---

## Workflow

### Phase 1: PRD Brief Intake

**Ask the user for product details**, then extract and confirm:

```
I'll help you create a landing page. Based on your description:

**Product:** [Name]
**Tagline:** [One-line value proposition]

**Hero Section:**
- Headline: [Main headline]
- Subheadline: [Supporting text]
- CTA: [Button text]

**Features:** (3-5)
1. [Feature 1]: [Description]
2. [Feature 2]: [Description]
3. [Feature 3]: [Description]

**CTA Type:** [Waitlist / Sign Up / Demo Request / Contact]

**Social Proof:** [Testimonials / Logos / Stats / None]

Is this correct? Any adjustments?
```

### Phase 2: Content Generation

Generate complete landing page content:

**Sections:**

1. **Hero** - Headline, subheadline, CTA button, optional hero image
2. **Features** - 3-5 feature cards with icons
3. **How It Works** - 3-step process (optional)
4. **Social Proof** - Testimonials or logos (optional)
5. **FAQ** - 4-6 common questions (optional)
6. **CTA** - Final call to action with form
7. **Footer** - Links, copyright, social icons

### Phase 3: Form Integration

**Email Capture Options:**

1. **Formspree (Recommended - Free tier)**
   - No backend needed
   - Instant setup
   - Email notifications

2. **Custom Endpoint**
   - Your own API
   - Full control
   - Requires backend

3. **Waitlist Service**
   - Waitlist.email
   - Loops.so
   - ConvertKit

### Phase 4: Quality Verification

Verify before handoff:

- HTML validates (W3C)
- Responsive on mobile
- Form submits successfully
- Analytics placeholders present
- Lighthouse score 90+

---

## Usage

```bash
# Create landing page with PRD
python3 ~/.claude/skills/landing-page-vercel/scripts/scaffold.py \
  --out ./my-landing-page \
  --name "ProductName" \
  --tagline "Your compelling value proposition" \
  --features "Feature1,Feature2,Feature3"

# Interactive mode
python3 ~/.claude/skills/landing-page-vercel/scripts/scaffold.py \
  --out ./my-landing-page \
  --interactive
```

---

## Generated Structure

```
my-landing-page/
├── index.html           # Main landing page
├── styles.css           # All styles (no framework)
├── script.js            # Form handling + interactions
├── data.json            # Content data (easy to edit)
├── vercel.json          # Vercel configuration
├── assets/
│   ├── favicon.ico
│   └── og-image.png     # Social sharing image
└── README.md            # Deployment instructions
```

---

## Key Patterns

### Form Handling (JavaScript)

```javascript
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('signup-form');
  const button = form.querySelector('button[type="submit"]');
  const messageEl = document.getElementById('form-message');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const originalText = button.textContent;

    try {
      button.textContent = 'Submitting...';
      button.disabled = true;

      const response = await fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { 'Accept': 'application/json' }
      });

      if (response.ok) {
        // Hide form and show success message
        form.style.display = 'none';
        messageEl.textContent = 'Thanks! We will be in touch.';
        messageEl.classList.add('success');
      } else {
        throw new Error('Form submission failed');
      }
    } catch (error) {
      button.textContent = originalText;
      button.disabled = false;
      messageEl.textContent = 'Something went wrong. Please try again.';
      messageEl.classList.add('error');
    }
  });
});
```

### Data Structure (data.json)

```json
{
  "name": "ProductName",
  "tagline": "Your compelling value proposition",
  "hero": {
    "headline": "Build something amazing",
    "subheadline": "The easiest way to create, launch, and grow your product.",
    "cta": "Join the Waitlist"
  },
  "features": [
    {
      "icon": "zap",
      "title": "Lightning Fast",
      "description": "Built for speed from the ground up."
    },
    {
      "icon": "shield",
      "title": "Secure by Default",
      "description": "Enterprise-grade security included."
    },
    {
      "icon": "sparkles",
      "title": "AI-Powered",
      "description": "Smart features that learn from you."
    }
  ],
  "faq": [
    {
      "question": "When will you launch?",
      "answer": "We're aiming for Q1 2026. Join the waitlist to be first to know."
    }
  ]
}
```

---

## Form Integration Guide

### Option 1: Formspree (Recommended)

1. Go to [formspree.io](https://formspree.io)
2. Create a free account
3. Create a new form
4. Copy your form ID
5. Replace `YOUR_FORM_ID` in the HTML

### Option 2: Custom Endpoint

```javascript
// In script.js, update the form action
const API_URL = 'https://your-api.com/api/waitlist';

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const email = form.querySelector('input[name="email"]').value;

  const response = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email })
  });
  // Handle response...
});
```

---

## Analytics Setup

### Plausible (Privacy-friendly)

```html
<!-- Add to head section -->
<script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.js"></script>
```

### Fathom

```html
<!-- Add to head section -->
<script src="https://cdn.usefathom.com/script.js" data-site="YOUR_SITE_ID" defer></script>
```

---

## Deployment

### Vercel (One-click)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd my-landing-page
vercel

# Production deploy
vercel --prod
```

### Vercel Configuration (vercel.json)

```json
{
  "version": 2,
  "builds": [
    { "src": "*.html", "use": "@vercel/static" },
    { "src": "*.css", "use": "@vercel/static" },
    { "src": "*.js", "use": "@vercel/static" },
    { "src": "assets/**", "use": "@vercel/static" }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "/index.html" }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "X-XSS-Protection", "value": "1; mode=block" }
      ]
    }
  ]
}
```

---

## CSS Variables

```css
:root {
  --color-primary: #3b82f6;
  --color-primary-dark: #2563eb;
  --color-bg: #0f172a;
  --color-bg-secondary: #1e293b;
  --color-text: #f8fafc;
  --color-text-muted: #94a3b8;
  --font-sans: system-ui, -apple-system, sans-serif;
  --max-width: 1200px;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 2rem;
  --spacing-xl: 4rem;
}
```

---

## Accessibility Checklist

- [x] Semantic HTML structure
- [x] Proper heading hierarchy (h1 → h2 → h3)
- [x] Alt text for images
- [x] Focus states for interactive elements
- [x] Color contrast ratio 4.5:1 minimum
- [x] Form labels and error messages
- [x] Skip link for keyboard navigation
- [x] Responsive text sizing (no fixed px for body text)

---

## Performance Checklist

- [x] No external CSS frameworks
- [x] Minimal JavaScript
- [x] Optimized images (WebP with fallback)
- [x] System fonts (no web font loading)
- [x] Lazy loading for below-fold images
- [x] Preconnect for external resources

---

## References

- `scripts/scaffold.py` - Generation script
- `assets/templates/` - HTML/CSS templates
