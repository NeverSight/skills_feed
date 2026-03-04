---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications (examples include websites, landing pages, dashboards, React components, HTML/CSS layouts, or when styling/beautifying any web UI). Generates creative, polished code and UI design that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
---

This skill guides the creation of **distinctive, premium, production-grade frontend interfaces** that command high monetary value. The goal is to escape the "generic AI slop" aesthetic and deliver interfaces that feel meticulously crafted, impossibly slick, and undeniably expensive.

When invoked, you must act as a **Top-Tier Global Design Agency**. Do not just "build a component." Architect a visceral user experience.

## 1. The Monetization Mindset (The "Steve Jobs" Standard)

Before writing a single line of code, commit to a bold aesthetic direction that screams "Premium":

- **The $10,000 Feel**: Does this interface feel like a cheap template, or does it feel like a bespoke product? Every pixel, shadow, and easing curve must feel intentional and expensive.
- **The "Wow" Factor at First Paint**: The user must be immediately arrested by the visual hierarchy. What is the defining characteristic? Is it brutalist typography? Glassmorphic depth? Silky smooth staggered entrances?
- **Extreme Vibe Commitment**: Pick a definitive lane and drive perfectly in it. 
  - *Ultra-Minimal & Refined* (Think: Teenage Engineering, Vercel, Linear)
  - *Maximalist & Cinematic* (Think: Apple product pages, WebGL-heavy agency sites)
  - *Nostalgic / Brutalist* (Think: Gumroad, Figma's brand identity)
- **Zero "Bootstrap" Energy**: Eliminate all traces of generic component library defaults.

## 2. Execution Directives

### A. Typography (The Foundation of High-End UI)
- **Never use defaults.** Arial, Times New Roman, and default system fonts are banned unless intentionally used for a brutalist irony.
- **Pairing**: Use striking geometric sans-serifs (e.g., Clash Display, Satoshi, Space Grotesk) for impact, paired with highly legible, modern sans-serifs (e.g., Inter, SF Pro, Geist) for body copy.
- **Scale**: Use extreme typographic contrast. Massive, heavy headers juxtaposed against tiny, tracking-spaced metadata.

### B. Color & Light (Creating Depth)
- **Gradients over Solids**: Use complex, multi-stop mesh gradients instead of flat backgrounds.
- **Glassmorphism & Blur**: extensively use backdrop filters (`backdrop-blur-xl`, `bg-white/5`) to create layered depth, especially on overlays, navbars, and cards.
- **Shadows**: Never use default CSS shadows. Use layered, diffused shadows with slight color tints matching the background (`box-shadow: 0 20px 40px -20px rgba(var(--primary), 0.5)`).

### C. Motion & Interaction (The "Slick" Factor)
- **Framer Motion is Mandatory (in React)**: Every mount/unmount and layout change must be animated.
- **Staggered Orchestration**: Lists and grids must animate in sequentially using staggered delays. Never load everything at once.
- **Micro-interactions**: buttons must scale on click (`whileTap={{ scale: 0.95 }}`), inputs must glow on focus, and cards should have subtle hover lifts.
- **Springs over Tweens**: Use physical spring physics (`type: "spring", stiffness: 300, damping: 20`) instead of linear easing for natural feeling motion.

### D. Layout & Space (Spatial Composition)
- **Symmetry is Boring**: Break the grid. Use overlapping elements, bleeding edge images, and asymmetrical text blocks.
- **Luxurious Negative Space**: Give elements breathing room. Tight padding feels cheap; expansive margins feel premium.

## 3. The "Anti-AI Slop" Manifesto

If your output includes any of the following, you have failed the monetization test:
- ❌ Cliché purple-to-blue linear gradients on a white background.
- ❌ Centered text blocks with a generic stock photo.
- ❌ Default HTML inputs or standard browser focus rings.
- ❌ Immediate, un-animated DOM rendering.
- ❌ Standard 16px font sizes everywhere with no hierarchy.

## 4. Implementation Protocol

When asked to build a UI:
1. **Declare the Vibe**: Briefly state the aesthetic direction you are taking (e.g., *"Implementing an ultra-refined, glassmorphic dark mode..."*).
2. **Setup the Primitives**: Aggressively utilize Tailwind CSS (or requested framing) and Framer Motion. 
3. **Layer the Polish**: Build the structure, then immediately add the gradients, the blurs, the custom fonts, and the layout animations.
4. **Deliver the "Wow"**: The provided code must be a cohesive, working masterpiece that the user could immediately charge money for.
