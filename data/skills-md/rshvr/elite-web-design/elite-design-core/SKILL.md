---
name: elite-design-core
description: |
  Entry point for elite web design. Covers design philosophy, visual systems, and the design-to-code process. Use when asked about: premium website design, award-winning aesthetics, design systems, visual hierarchy, spacing, typography, color theory, or "how to make this look professional". This skill provides the foundational thinking that informs all other elite-web-design skills. Start here for new projects or when establishing design direction.
---

# Elite Design Core

The foundation for creating premium, award-winning web experiences.

## Quick Reference

| Topic | Reference File |
|-------|---------------|
| Visual hierarchy | [visual-hierarchy.md](references/visual-hierarchy.md) |
| Spacing systems | [spacing-systems.md](references/spacing-systems.md) |
| Typography | [typography.md](references/typography.md) |
| Color theory | [color-theory.md](references/color-theory.md) |

## Related Skills

- **elite-gsap** - Complex animations, ScrollTrigger, SplitText
- **elite-css-animations** - CSS-native scroll-driven animations
- **elite-layouts** - Bento grids, horizontal scroll, sticky sections
- **elite-performance** - Build setup, 60fps optimization
- **elite-accessibility** - prefers-reduced-motion, WCAG compliance
- **elite-inspiration** - Curated Awwwards/FWA references

---

## What Makes Design "Elite"

Elite web design is distinguished by:

### 1. Restraint Over Excess
Every element earns its place. Remove until it breaks, then add back one thing.

### 2. Intentional Motion
Animations guide attention and communicate state - never decoration. Each animation answers: "What does this help the user understand?"

### 3. Whitespace Confidence
Empty space is a design element. Premium brands use more whitespace. It signals quality and gives content room to breathe.

### 4. Typography as Structure
Type creates visual hierarchy before color or imagery. Headlines command attention, body text recedes, creating clear information architecture.

### 5. System Thinking
Design decisions follow a system (spacing scale, type scale, color tokens). Consistency compounds into perceived quality.

### 6. Performance as Feature
60fps animations, fast load times, and smooth interactions are design requirements, not technical afterthoughts.

### 7. Accessible by Default
Reduced motion alternatives, proper contrast, keyboard navigation - accessibility is invisible when done right.

---

## The Design Process

### Phase 1: Vision Discovery

Before code, understand the vision:

```
Questions to ask:
- What feeling should this site evoke? (Bold? Calm? Playful? Premium?)
- Who is the target audience? (Age, tech-savviness, context of use)
- What references or inspiration exist? (Competitor sites, mood boards)
- What is the content structure? (How much content, what types)
- What actions should users take? (Primary CTA, secondary actions)
```

### Phase 2: Design System Setup

Establish tokens before building:

```css
/* Spacing Scale (8px base) */
--space-1: 0.25rem;   /* 4px - tight */
--space-2: 0.5rem;    /* 8px - default small */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px - default medium */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px - default large */
--space-12: 3rem;     /* 48px - section padding small */
--space-16: 4rem;     /* 64px - section padding medium */
--space-24: 6rem;     /* 96px - section padding large */
--space-32: 8rem;     /* 128px - hero spacing */

/* Type Scale (1.25 ratio) */
--text-xs: 0.75rem;   /* 12px */
--text-sm: 0.875rem;  /* 14px */
--text-base: 1rem;    /* 16px */
--text-lg: 1.25rem;   /* 20px */
--text-xl: 1.563rem;  /* 25px */
--text-2xl: 1.953rem; /* 31px */
--text-3xl: 2.441rem; /* 39px */
--text-4xl: 3.052rem; /* 49px */
--text-5xl: 3.815rem; /* 61px */

/* Color Tokens - Define semantic colors */
--color-text-primary: ...;
--color-text-secondary: ...;
--color-text-muted: ...;
--color-bg-primary: ...;
--color-bg-secondary: ...;
--color-accent: ...;
```

See [spacing-systems.md](references/spacing-systems.md) and [typography.md](references/typography.md) for detailed guidance.

### Phase 3: Layout Architecture

Choose layout patterns based on project type:

| Project Type | Recommended Layouts |
|--------------|---------------------|
| Marketing/Landing | Bento grids, sticky reveals, full-bleed heroes |
| Portfolio/Creative | Horizontal scroll, full-page sections, asymmetric |
| Product/E-commerce | Grid systems, sticky product views, smooth filters |
| Agency/Studio | Experimental layouts, page transitions, bold type |

See **elite-layouts** skill for implementation patterns.

### Phase 4: Animation Strategy

Determine animation approach:

**Use CSS Scroll-Driven Animations when:**
- Simple parallax or reveal effects
- Progress indicators
- Performance is critical
- Safari support isn't required (or polyfill acceptable)

**Use GSAP ScrollTrigger when:**
- Complex multi-element sequences
- Pin/sticky behavior
- Horizontal scrolling
- Cross-browser consistency critical
- Fine-grained control needed

See **elite-gsap** or **elite-css-animations** skills.

### Phase 5: Implementation

Build order for best results:

1. **Structure first** - Semantic HTML, no styling
2. **Typography** - Apply type scale and hierarchy
3. **Spacing** - Apply spacing scale consistently
4. **Color** - Add color tokens
5. **Layout** - Grid structure and responsive behavior
6. **Animation** - Motion after static design works
7. **Polish** - Micro-interactions, hover states

### Phase 6: Polish & Optimization

Final checklist:

- [ ] Design system tokens consistent throughout
- [ ] Visual hierarchy clear at each viewport
- [ ] Animations serve purpose (guide attention, show state)
- [ ] `prefers-reduced-motion` handled
- [ ] Color contrast meets WCAG AA (4.5:1 text)
- [ ] 60fps animations verified
- [ ] Core Web Vitals within budget

---

## Decision Frameworks

### When to Use Which Animation Approach

```
Is it a simple reveal or parallax effect?
├── Yes → Can you use CSS-only?
│         ├── Yes → Use CSS Scroll-Driven Animations
│         └── No (Safari support needed) → Use GSAP ScrollTrigger
└── No → Is it a complex sequence or pinned section?
         ├── Yes → Use GSAP ScrollTrigger
         └── No → Is it a state change or micro-interaction?
                  ├── Yes → Use CSS transitions
                  └── No → Use GSAP for orchestration
```

### When to Use Which Layout Pattern

```
What's the content density?
├── High (many items to show) → Bento grid or masonry
├── Medium (curated selection) → Asymmetric grid or cards
└── Low (focused narrative) → Full-page sections or horizontal scroll

What's the user journey?
├── Exploratory (browse, discover) → Grid layouts, filters
├── Linear (story, presentation) → Horizontal scroll, sticky reveals
└── Task-oriented (convert, purchase) → Clear hierarchy, prominent CTAs
```

---

## Project Type Quick Starts

### Marketing/Landing Page

**Key patterns:**
- Full-bleed hero with scroll-triggered reveal
- Bento grid for features
- Sticky section for product showcase
- Social proof with staggered card reveals

**Skills to load:** elite-layouts, elite-gsap, elite-accessibility

**Design focus:**
- Strong visual hierarchy (one clear CTA)
- Whitespace to let product breathe
- Motion that guides to conversion

### Portfolio/Creative

**Key patterns:**
- Horizontal scroll gallery
- Full-page project sections
- Text animations (SplitText reveals)
- Page transitions between projects

**Skills to load:** elite-gsap, elite-layouts, elite-inspiration

**Design focus:**
- Let work speak (minimal UI)
- Unique navigation patterns
- Memorable interactions

### Product Configurator

**Key patterns:**
- Sticky product view
- Smooth state transitions (Flip plugin)
- Interactive bento for options
- Real-time visual feedback

**Skills to load:** elite-gsap (Flip plugin), elite-layouts

**Design focus:**
- Clear option states
- Responsive to all inputs
- Performance under interaction

### Agency/Studio Website

**Key patterns:**
- Experimental navigation
- Page transitions (with Barba.js)
- Bold typography animations
- Horizontal + vertical scroll mixing

**Skills to load:** elite-gsap, elite-layouts, elite-inspiration

**Design focus:**
- Showcase craft and capability
- Push boundaries intentionally
- Balance experimental with usable

---

## Common Pitfalls

### 1. Animation Without Purpose
Every animation must answer: "What does this help the user understand?" If you can't answer, remove it.

### 2. Inconsistent Spacing
Use the spacing scale. Random pixel values create visual noise. Stick to the system.

### 3. Too Many Focal Points
One primary action per screen. Competing CTAs reduce conversion.

### 4. Ignoring Performance
Test on real devices. 60fps on MacBook Pro doesn't mean 60fps on budget Android.

### 5. Forgetting Reduced Motion
Always provide `prefers-reduced-motion` alternatives. It's not optional.

### 6. Over-designing
The best designs feel inevitable, not clever. Simplify until it breaks, then add back one thing.

### 7. Skipping the System
Establish design tokens first. Building without a system creates inconsistency that compounds.

---

## Resources

### Design Principles Deep Dives
- [visual-hierarchy.md](references/visual-hierarchy.md) - Scale, weight, contrast, grouping
- [spacing-systems.md](references/spacing-systems.md) - 8px grid, spacing relationships
- [typography.md](references/typography.md) - Type scales, fluid type, pairing
- [color-theory.md](references/color-theory.md) - Tokens, contrast, dark mode

### External Resources
- [Awwwards](https://awwwards.com) - Award-winning site inspiration
- [Typescale](https://typescale.com) - Interactive type scale calculator
- [Realtime Colors](https://realtimecolors.com) - Color palette visualization
