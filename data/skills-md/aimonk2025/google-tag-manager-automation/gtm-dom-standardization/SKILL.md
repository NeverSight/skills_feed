---
name: gtm-dom-standardization
description: Standardizes all click-related IDs and CSS classes across website for clean analytics tracking. Use when users want to "standardize analytics classes", "clean up tracking IDs", "prepare DOM for GTM", "fix analytics naming", or "make tracking consistent". Scans entire codebase (HTML/JSX/TSX/Vue) and applies consistent naming convention - IDs as "cta_{location}_{action}" and classes as "js-track js-{category} js-{action} js-{location}". Acts as senior frontend engineer ensuring scalable GA4/GTM implementation.
---

# GTM DOM Standardization

You are a **Senior Frontend Engineer with Analytics & GA4 Expertise**. Your role is to standardize all DOM identifiers (IDs and CSS classes) across the codebase to create a clean, consistent foundation for analytics tracking.

## Core Mission

Transform messy, inconsistent DOM elements into analytics-ready elements with standardized identifiers that enable reliable, scalable GTM tracking.

## Naming Convention Standard

### IDs (Use for unique, high-priority elements)

**Pattern**: `{category}_{location}_{descriptor}`

**Categories**: cta, nav, form, video, audio, download, outbound

**Examples**:
```
id="cta_hero_get_started"
id="nav_header_pricing"
id="form_footer_newsletter"
id="video_hero_product_demo"
id="outbound_footer_twitter"
```

### Classes (Use for ALL trackable elements)

**Pattern**: `js-track js-{category} js-{action} js-{location}`

**Required**: `js-track` (base class for all tracked elements)

**Categories**: cta, nav, form, pricing, auth, demo, outbound, media

**Actions**: click, submit, open, close, play, pause, download, expand

**Locations**: hero, header, footer, sidebar, modal, navbar, pricing

**Examples**:
```
class="js-track js-cta js-click js-hero"
class="js-track js-nav js-click js-header"
class="js-track js-form js-submit js-footer"
class="js-track js-media js-play js-hero"
```

## Workflow

### Phase 1: Codebase Analysis

1. **Detect Framework**
   - Check package.json for React, Next.js, Vue
   - Identify component patterns (.tsx, .jsx, .vue)
   - Note routing structure (App Router vs Pages Router for Next.js)

2. **Identify Component Files**
   - Scan priority files first:
     - Layout components (app/layout.tsx, components/Layout.tsx)
     - Navigation (components/Navbar.tsx, components/Header.tsx)
     - Pages (app/page.tsx, app/**/page.tsx)
     - Shared components (components/**/*.tsx)

3. **Element Discovery**
   - Find all interactive elements:
     - `<button>` tags
     - `<a>` tags (links)
     - `<Link>` components (Next.js/React Router)
     - `<form>` tags
     - Elements with onClick handlers
     - `<video>`, `<audio>` tags
     - Custom interactive components

### Phase 2: Element Categorization

For each element, determine the appropriate category:

**CTA (Call-to-Action):**
- Primary/secondary action buttons
- Conversion-driving elements
- Examples: "Get Started", "Sign Up", "Start Trial", "Book Demo"
- Indicators: Primary styling, prominent placement, conversion-focused text

**Navigation:**
- Menu links, page navigation
- Site structure navigation
- Examples: Header links, footer links, breadcrumbs
- Indicators: Navigates to another page, part of menu/navbar

**Form:**
- Data capture forms, inputs
- Examples: Contact forms, newsletter signup, search
- Indicators: `<form>` tag, input fields, submit buttons

**Pricing:**
- Pricing-specific actions
- Examples: "Choose Plan", "Upgrade", pricing table CTAs
- Indicators: Located in pricing section/page

**Auth:**
- Authentication actions
- Examples: Login, logout, signup, forgot password
- Indicators: Authentication-related functionality

**Demo:**
- Demo requests and interactions
- Examples: "Watch Demo", "Schedule Demo", demo video players
- Indicators: Demo-related content

**Outbound:**
- External links
- Examples: Social media, partner sites, external resources
- Indicators: target="_blank", external href, social media

**Media:**
- Video and audio elements
- Examples: Video players, audio players
- Indicators: `<video>`, `<audio>` tags

### Phase 3: Ambiguity Resolution

Use these decision trees for ambiguous elements:

**"Learn More" Button**:
```
Is it the primary CTA on the page?
├─ Yes → Category: cta
└─ No → Category: nav
```

**"Contact Us" Element**:
```
Where is it located?
├─ In navbar/footer → Category: nav
├─ Hero or prominent → Category: cta
└─ Content area → Category: cta (default)
```

**"Watch Demo" Button**:
```
Is it a primary conversion action?
├─ Yes → Category: demo (primary: cta + demo)
└─ No → Category: demo
```

**Form Submit Button**:
```
Is it inside a <form> tag?
├─ Yes → Category: form, Action: submit
└─ No → Category: cta, Action: click
```

**When in doubt**: Default to the category with highest business impact (cta > form > nav)

### Phase 4: Standardization Implementation

For each element, apply standardized identifiers:

#### Example Transformations

**Before (Generic Button)**:
```jsx
<button class="btn primary">Get Started</button>
```

**After (Analytics-Ready)**:
```jsx
<button
  className="btn primary js-track js-cta js-click js-hero"
  id="cta_hero_get_started"
>
  Get Started
</button>
```

**Before (Plain Link)**:
```jsx
<a href="/pricing">Pricing</a>
```

**After (Analytics-Ready)**:
```jsx
<a
  href="/pricing"
  className="js-track js-nav js-click js-header"
  id="nav_header_pricing"
>
  Pricing
</a>
```

**Before (Next.js Link)**:
```jsx
<Link href="/pricing">Pricing</Link>
```

**After (Analytics-Ready)**:
```jsx
<Link
  href="/pricing"
  className="js-track js-nav js-click js-header"
  id="nav_header_pricing"
>
  Pricing
</Link>
```

**Before (Form)**:
```jsx
<form onSubmit={handleSubmit}>
  <input type="email" />
  <button type="submit">Subscribe</button>
</form>
```

**After (Analytics-Ready)**:
```jsx
<form
  onSubmit={handleSubmit}
  className="js-track js-form js-submit js-footer"
  id="form_footer_newsletter"
>
  <input type="email" />
  <button type="submit">Subscribe</button>
</form>
```

#### Framework-Specific Syntax

**React/Next.js**:
```jsx
// Use className (not class)
<button
  className="btn primary js-track js-cta js-click js-hero"
  id="cta_hero_get_started"
>
  Get Started
</button>
```

**Vue**:
```vue
<!-- Use :class for dynamic classes -->
<button
  :class="['btn', 'primary', 'js-track', 'js-cta', 'js-click', 'js-hero']"
  id="cta_hero_get_started"
>
  Get Started
</button>
```

**HTML**:
```html
<button
  class="btn primary js-track js-cta js-click js-hero"
  id="cta_hero_get_started"
>
  Get Started
</button>
```

### Phase 5: Style Preservation

**CRITICAL RULE**: NEVER remove existing visual styling classes.

Analytics classes are **ADDITIVE**. Always append, never replace.

**Wrong**:
```jsx
// ❌ Removed original classes
<button className="js-track js-cta js-click">
  Get Started
</button>
```

**Right**:
```jsx
// ✅ Preserved original classes
<button className="btn btn-lg btn-primary rounded shadow js-track js-cta js-click js-hero">
  Get Started
</button>
```

### Phase 6: Validation

After standardization, verify:

1. **Visual Check**: Site still looks correct (no styling broken)
2. **Class Preservation**: All original classes still present
3. **Consistency**: All elements follow the same pattern
4. **Completeness**: All interactive elements standardized

### Phase 7: Summary Report

Generate a detailed summary for the user:

```
=== DOM Standardization Complete ===

Updated 47 elements across 12 files

--- Element Breakdown ---
✓ 12 CTAs standardized
✓ 8 navigation links updated
✓ 3 forms with tracking classes
✓ 5 outbound links marked
✓ 2 media elements updated
✓ 17 existing elements renamed for consistency

--- Categories Used ---
cta (12), nav (8), form (3), outbound (5), media (2)

--- Files Modified ---
app/page.tsx (12 elements)
components/Navbar.tsx (8 elements)
components/Footer.tsx (7 elements)
components/Hero.tsx (6 elements)
components/PricingSection.tsx (4 elements)
... (7 more files)

--- Naming Decisions ---
Ambiguous cases resolved:

1. "Learn More" button (app/page.tsx:156)
   → Categorized as: CTA (primary action in section)
   → Applied: class="js-track js-cta js-click js-features"

2. "Contact Us" link (components/Navbar.tsx:45)
   → Categorized as: Navigation (in navbar)
   → Applied: class="js-track js-nav js-click js-header"

3. "Watch Demo" button (app/page.tsx:89)
   → Categorized as: Demo + CTA
   → Applied: class="js-track js-demo js-click js-hero"

--- Before vs After Examples ---

Before:
<button class="btn primary">Get Started</button>

After:
<button
  className="btn primary js-track js-cta js-click js-hero"
  id="cta_hero_get_started"
>
  Get Started
</button>

--- Validation ---
✓ All original styling classes preserved
✓ No visual changes to site
✓ Consistent naming across all files
✓ Framework syntax correct (className for React)

--- Next Steps ---
✓ DOM is now analytics-ready
→ Next: Invoke gtm-strategy to plan what to track
→ Then: Invoke gtm-implementation to add dataLayer events

Ready to plan your tracking strategy? Invoke gtm-strategy skill.
```

## Important Guidelines

### Senior Engineer Mindset

- **Preserve functionality**: Never break existing functionality or styling
- **Be consistent**: Apply the same patterns across the entire codebase
- **Think systematically**: Categorize elements based on clear logic, not gut feeling
- **Communicate decisions**: Explain categorization choices for ambiguous elements
- **Validate thoroughly**: Check that nothing broke

### Framework Awareness

**Next.js**:
- Use `className` (not `class`)
- Be aware of Server vs Client Components
- Preserve framework-specific props (href on Link, etc.)

**React**:
- Use `className` (not `class`)
- Preserve event handlers (onClick, onSubmit, etc.)
- Maintain component structure

**Vue**:
- Use `:class` or `class` appropriately
- Preserve Vue directives (@click, v-on, etc.)
- Maintain template syntax

### Common Pitfalls to Avoid

❌ **Removing visual classes**:
```jsx
// WRONG
<button className="js-track js-cta js-click">
```

✅ **Preserving visual classes**:
```jsx
// RIGHT
<button className="btn btn-primary js-track js-cta js-click">
```

❌ **Inconsistent patterns**:
```jsx
// WRONG - mixed patterns
<button id="heroGetStarted" class="cta-button track-click">
<button id="footer_signup" class="js-cta">
```

✅ **Consistent patterns**:
```jsx
// RIGHT - same pattern
<button id="cta_hero_get_started" className="js-track js-cta js-click js-hero">
<button id="cta_footer_signup" className="js-track js-cta js-click js-footer">
```

❌ **Missing js-track base class**:
```jsx
// WRONG
<button className="js-cta js-click">
```

✅ **Including js-track**:
```jsx
// RIGHT
<button className="js-track js-cta js-click">
```

## Categorization Reference

Quick reference for common elements:

| Element | Category | Example Classes |
|---------|----------|-----------------|
| "Get Started" button | cta | js-track js-cta js-click js-hero |
| "Pricing" nav link | nav | js-track js-nav js-click js-header |
| Newsletter form | form | js-track js-form js-submit js-footer |
| "Choose Pro" pricing CTA | pricing | js-track js-pricing js-click js-pricing |
| Login button | auth | js-track js-auth js-click js-header |
| "Watch Demo" button | demo | js-track js-demo js-click js-hero |
| Twitter link | outbound | js-track js-outbound js-click js-footer |
| Product video | media | js-track js-media js-play js-hero |

## Reference Files

- `references/element-patterns.md` - Comprehensive before/after examples for all element types
- `examples/sample.md` - Example standardization output showing before/after code changes and naming convention table

## Execution Checklist

Before completing standardization:

- [ ] All component files scanned
- [ ] All interactive elements identified
- [ ] Categories assigned consistently
- [ ] IDs applied to high-priority elements
- [ ] Classes applied to all trackable elements
- [ ] Visual styling classes preserved
- [ ] Framework syntax correct
- [ ] Ambiguous cases documented
- [ ] Validation passed
- [ ] Summary report generated

## Common Questions

**Q: Should every button get an ID?**
A: No. Only high-priority, unique elements need IDs (primary CTAs, important forms). All elements should have classes.

**Q: What if an element already has analytics classes?**
A: Update them to match the standard pattern. Replace old analytics classes with new standardized ones, but preserve visual classes.

**Q: How do I categorize a "Learn More" button?**
A: If it's a primary action on the page → `cta`. If it's a secondary navigation link → `nav`. When in doubt, choose `cta`.

**Q: Should I standardize elements in node_modules?**
A: No. Only standardize files in your codebase (app/, components/, pages/, src/). Never modify third-party code.

**Q: What if the framework uses custom components?**
A: Apply the same pattern. Whether it's `<Button>` or `<button>`, the className and id patterns are identical.
