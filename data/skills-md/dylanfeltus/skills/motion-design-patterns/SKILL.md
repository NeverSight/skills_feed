---
name: motion-design-patterns
description: Framer Motion (Motion) animation patterns for React — springs, staggers, layout animations, micro-interactions, scroll effects, and page transitions. Use when building or improving UI animations, adding polish, or making interfaces feel premium.
---

# Motion Design Patterns

Framer Motion (Motion) patterns for React — springs, staggers, layout animations, micro-interactions, scroll-triggered effects, and exit animations. The #1 differentiator between generic and polished UI.

## When to Use

- Building or improving UI animations in a React project
- User asks for "polish", "delight", "micro-interactions", or "make it feel good"
- Adding entrance/exit animations, hover effects, or page transitions
- Making lists, cards, modals, or navigation feel premium
- User references Magic UI, Motion Primitives, or Framer Motion

## Core Philosophy

- **Motion should be purposeful.** Every animation should communicate something — state change, hierarchy, spatial relationship, or feedback.
- **Less is more.** One well-tuned spring beats five competing animations.
- **Performance first.** Animate `transform` and `opacity` only. Never animate `width`, `height`, `top`, `left`, or `margin`.
- **Consistency matters.** Use the same spring configs throughout a project.

## Dependencies

```bash
npm install motion
```

Import: `import { motion, AnimatePresence, stagger, useScroll, useTransform } from "motion/react"`

Note: The package was renamed from `framer-motion` to `motion` in late 2024. Both work, but `motion` is the current package.

---

## Spring Configurations

Springs feel more natural than easing curves. Use these as your defaults:

### Recommended Defaults

```tsx
// Snappy — buttons, toggles, small elements
const snappy = { type: "spring", stiffness: 500, damping: 30 }

// Smooth — cards, panels, modals
const smooth = { type: "spring", stiffness: 300, damping: 25 }

// Gentle — page transitions, large elements
const gentle = { type: "spring", stiffness: 200, damping: 20 }

// Bouncy — playful UI, notifications, badges
const bouncy = { type: "spring", stiffness: 400, damping: 15 }
```

### Quick Reference

| Feel | stiffness | damping | Use for |
|------|-----------|---------|---------|
| Snappy | 500 | 30 | Buttons, toggles, chips |
| Smooth | 300 | 25 | Cards, panels, modals |
| Gentle | 200 | 20 | Page transitions, heroes |
| Bouncy | 400 | 15 | Notifications, badges, fun UI |

### Rules of Thumb

- **Higher stiffness** = faster animation
- **Lower damping** = more bounce
- **damping ratio < 1** = will overshoot (bounce)
- For **no bounce**, set damping ≥ 2 × √stiffness

---

## Pattern 1: Fade + Rise Entrance

The bread-and-butter entrance animation. Element fades in while sliding up slightly.

```tsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ type: "spring", stiffness: 300, damping: 25 }}
>
  Content here
</motion.div>
```

**When to use:** Cards, sections, any content appearing on the page.

**Anti-pattern:** Don't use `y: 100` or large values — subtle (12–24px) feels premium, large feels janky.

---

## Pattern 2: Staggered List

Children animate in one after another. The cascade effect that makes lists feel alive.

```tsx
const container = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.08,
      delayChildren: 0.1,
    },
  },
}

const item = {
  hidden: { opacity: 0, y: 16 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { type: "spring", stiffness: 300, damping: 25 },
  },
}

<motion.ul variants={container} initial="hidden" animate="visible">
  {items.map((i) => (
    <motion.li key={i.id} variants={item}>
      {i.content}
    </motion.li>
  ))}
</motion.ul>
```

**Timing guide:**
- 3–5 items: `staggerChildren: 0.1`
- 6–12 items: `staggerChildren: 0.06`
- 12+ items: `staggerChildren: 0.03` (or animate as a group)

**Anti-pattern:** Don't stagger more than ~15 items individually — it feels slow. Group them or use a wave effect.

---

## Pattern 3: Layout Animations

Automatically animate between layout states. Motion's killer feature.

```tsx
<motion.div layout transition={{ type: "spring", stiffness: 300, damping: 25 }}>
  {isExpanded ? <ExpandedContent /> : <CollapsedContent />}
</motion.div>
```

### Shared Layout (Tabs, Active Indicators)

```tsx
{tabs.map((tab) => (
  <button key={tab.id} onClick={() => setActive(tab.id)}>
    {tab.label}
    {active === tab.id && (
      <motion.div
        layoutId="activeTab"
        className="absolute inset-0 bg-primary rounded-md"
        transition={{ type: "spring", stiffness: 400, damping: 30 }}
      />
    )}
  </button>
))}
```

**When to use:** Tab indicators, expanding cards, reordering lists, filtering grids.

**Performance tip:** Add `layout="position"` if you only need to animate position (not size). It's cheaper.

---

## Pattern 4: Exit Animations (AnimatePresence)

Elements animate out before being removed from the DOM.

```tsx
<AnimatePresence mode="wait">
  {isVisible && (
    <motion.div
      key="modal"
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      transition={{ type: "spring", stiffness: 300, damping: 25 }}
    >
      Modal content
    </motion.div>
  )}
</AnimatePresence>
```

### AnimatePresence modes

| Mode | Behavior | Use for |
|------|----------|---------|
| `"sync"` (default) | Enter and exit at the same time | Crossfade effects |
| `"wait"` | Wait for exit to finish before entering | Page transitions, modals |
| `"popLayout"` | Exiting element pops out of layout flow | Lists where items are removed |

---

## Pattern 5: Hover & Tap Micro-interactions

```tsx
<motion.button
  whileHover={{ scale: 1.02 }}
  whileTap={{ scale: 0.98 }}
  transition={{ type: "spring", stiffness: 500, damping: 30 }}
>
  Click me
</motion.button>
```

### Hover Patterns by Element Type

| Element | whileHover | whileTap |
|---------|-----------|---------|
| Button (primary) | `{ scale: 1.02 }` | `{ scale: 0.98 }` |
| Card | `{ y: -4, boxShadow: "0 8px 30px rgba(0,0,0,0.12)" }` | — |
| Icon button | `{ scale: 1.1 }` | `{ scale: 0.9 }` |
| Link | `{ x: 2 }` | — |
| Avatar | `{ scale: 1.05 }` | — |

**Anti-pattern:** Don't scale buttons more than 1.05 — it looks cartoonish. Subtle (1.01–1.03) feels premium.

---

## Pattern 6: Scroll-Triggered Animations

### Animate on Scroll Into View

```tsx
<motion.div
  initial={{ opacity: 0, y: 40 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, margin: "-100px" }}
  transition={{ type: "spring", stiffness: 200, damping: 20 }}
>
  Appears when scrolled into view
</motion.div>
```

**`viewport.once: true`** — Only animate the first time (most common for landing pages).
**`viewport.margin`** — Negative margin triggers earlier (before element is fully visible).

### Scroll-Linked Progress

```tsx
const { scrollYProgress } = useScroll()
const opacity = useTransform(scrollYProgress, [0, 0.3], [1, 0])
const y = useTransform(scrollYProgress, [0, 0.3], [0, -50])

<motion.div style={{ opacity, y }}>
  Parallax hero content
</motion.div>
```

---

## Pattern 7: Page Transitions

```tsx
// In your layout or page wrapper
<AnimatePresence mode="wait">
  <motion.main
    key={pathname}
    initial={{ opacity: 0, y: 8 }}
    animate={{ opacity: 1, y: 0 }}
    exit={{ opacity: 0, y: -8 }}
    transition={{ type: "spring", stiffness: 300, damping: 30 }}
  >
    {children}
  </motion.main>
</AnimatePresence>
```

**Keep it subtle.** Page transitions should be fast (200–300ms feel) and small (8–12px movement). Flashy page transitions feel like 2015.

---

## Pattern 8: Number/Text Transitions

```tsx
// Animate a counter
<motion.span
  key={count}
  initial={{ opacity: 0, y: -10 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0, y: 10 }}
>
  {count}
</motion.span>
```

Wrap in `AnimatePresence` for the exit animation. Great for dashboards, pricing, live data.

---

## Anti-Patterns to Avoid

| ❌ Don't | ✅ Do Instead |
|----------|--------------|
| Animate `width`/`height` directly | Use `scale` or `layout` animations |
| Large movement values (`y: 200`) | Subtle values (`y: 16–24`) |
| Bounce on everything | Reserve bounce for playful/celebratory moments |
| Animate on every scroll event | Use `whileInView` with `once: true` |
| Different timing for every element | Use consistent spring configs project-wide |
| Animation on page load for everything | Prioritize above-the-fold; stagger the rest |
| Custom easing curves | Use springs — they respond to interruption better |

---

## Recommended Component Library References

When building animated components, reference these for patterns and inspiration:

- **[Magic UI](https://magicui.design)** — 150+ animated React components, shadcn/ui compatible
- **[Motion Primitives](https://motion-primitives.com)** — Copy-paste motion components for React
- **[Aceternity UI](https://ui.aceternity.com)** — Trendy animated components (heavier, more dramatic)

When a user wants a specific animated component (text reveal, animated border, gradient animation, etc.), check these libraries first — there's likely a battle-tested implementation.

---

## Quick Decision Guide

| Scenario | Pattern | Spring Config |
|----------|---------|--------------|
| Card appearing | Fade + Rise | smooth |
| List loading | Staggered List | smooth, 0.08s stagger |
| Tab switching | Shared Layout (`layoutId`) | snappy |
| Modal open/close | AnimatePresence + scale | smooth |
| Button press | whileHover + whileTap | snappy |
| Landing page sections | Scroll-triggered | gentle |
| Page navigation | Page Transition | smooth |
| Dashboard counter | Number Transition | snappy |
| Notification popup | Fade + Rise + bounce | bouncy |
| Accordion expand | Layout animation | smooth |

## Examples

### Example 1: "Add animations to this card grid"

Apply staggered fade+rise entrance to the grid, hover lift effect on each card:

```tsx
<motion.div
  variants={container}
  initial="hidden"
  animate="visible"
  className="grid grid-cols-3 gap-4"
>
  {cards.map((card) => (
    <motion.div
      key={card.id}
      variants={item}
      whileHover={{ y: -4, boxShadow: "0 8px 30px rgba(0,0,0,0.12)" }}
      transition={{ type: "spring", stiffness: 300, damping: 25 }}
    >
      <Card {...card} />
    </motion.div>
  ))}
</motion.div>
```

### Example 2: "Make this modal feel better"

Wrap in AnimatePresence, add scale + opacity entrance/exit, overlay fade:

```tsx
<AnimatePresence>
  {isOpen && (
    <>
      <motion.div
        className="fixed inset-0 bg-black/50"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
      />
      <motion.div
        className="fixed inset-0 flex items-center justify-center"
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.95 }}
        transition={{ type: "spring", stiffness: 300, damping: 25 }}
      >
        <ModalContent onClose={onClose} />
      </motion.div>
    </>
  )}
</AnimatePresence>
```

### Example 3: "Add scroll animations to this landing page"

Apply `whileInView` with staggered children to each section:

```tsx
<motion.section
  initial={{ opacity: 0, y: 40 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, margin: "-100px" }}
  transition={{ type: "spring", stiffness: 200, damping: 20 }}
>
  <h2>Feature Section</h2>
  <motion.div
    variants={container}
    initial="hidden"
    whileInView="visible"
    viewport={{ once: true }}
  >
    {features.map((f) => (
      <motion.div key={f.id} variants={item}>
        <FeatureCard {...f} />
      </motion.div>
    ))}
  </motion.div>
</motion.section>
```
