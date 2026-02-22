---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
---

This skill guides creation of distinctive, production-grade frontend interfaces. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

---

## A note on LLM design limitations — read this first

**Be transparent with the user about this.** Before generating any design, the user needs to understand what you can and can't do, so they know where their input is critical.

### What you struggle with and why

You generate design by predicting the most probable next token. This means every design choice you make gravitates toward the statistical center of your training data — the average of "good design." You will produce competent, well-structured, polished work that looks like every other competent, well-structured, polished work. This isn't laziness — it's how the mechanism works. The average is what you're optimized to find.

Specifically:

- **You can't see what you're producing.** You write HTML/CSS as text tokens. You have no visual feedback loop. You cannot perceive whether something looks beautiful, unsettling, boring, or distinctive. You're painting blindfolded.
- **You optimize for coherence.** Your training rewards consistency, polish, and completeness. Deliberately unfinished, misaligned, or rule-breaking design goes against your weights. When you write CSS with a "broken" element, everything in your training pulls you to fix it.
- **You can't feel tension.** Great experimental design creates productive discomfort — violating expectations in a way that's generative, not random. You can't feel that discomfort, so you can't calibrate it. You either produce comfortable (convergent) design or break things randomly.
- **You don't have taste.** Taste is judgment that isn't reducible to rules. "This feels corporate." "That color is trying too hard." "This needs to breathe." These are perceptual, embodied calls that you can only approximate with heuristics — and heuristics are generalizations, and generalizations converge to the mean.
- **You can generate divergence but you can't evaluate it.** You can produce ten structurally different layouts. You genuinely cannot tell which one has the quality of being surprising and right at the same time.

### What this means for the user

**Your direction and reference material are not optional — they are the design.** You are the hand, not the eye. The user's taste, references, and gut reactions are what push the output somewhere it would never go alone. Without that input, you will produce the statistical center of whatever category the brief falls into.

The user should:
- **Provide reference images or sites** they're drawn to, especially from outside the same industry. A restaurant menu layout applied to a fintech page is more distinctive than any "experimental fintech" prompt.
- **Name what they hate**, not just what they want. "I hate card grids" is more useful than "make it interesting" because it eliminates a convergence attractor.
- **Expect to do multiple rounds.** The first output will be the most average. Each round of "kill this, keep that, push this further" moves the design away from the center.
- **Kill boldly.** If a variant feels safe or familiar, it is. The user's discomfort with a variant is often a signal that it's actually distinctive — unfamiliarity feels wrong before it feels right.

### The process that works

Do not treat this as a single-pass pipeline (brief → design → done). That guarantees convergence. Instead:

1. **Diverge**: Generate 3-5 structurally different variants. Not color/font swaps — fundamentally different spatial logic, rhythm, and composition. Each variant should explicitly name what design convention it's "fighting."
2. **Kill**: User makes binary decisions. Alive or dead. No blending — blending is averaging.
3. **Mutate**: Within the surviving direction, introduce deliberate "breaks" — named violations of design convention. The user picks which breaks work.
4. **Repeat**: Each cycle moves further from the center. The user's selections are the creative act. You're the generator.

Deploy variants to a comparison page so the user can see them side by side in a browser, not described in text. Visual comparison is the only honest evaluation.

---

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?
- **References**: Ask the user for reference images, sites, or non-digital references (architecture, print, film, physical objects) that capture something they're drawn to. These are more valuable than any verbal brief.

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

Remember: your execution quality is high — you can write precise, sophisticated CSS and build complex interactions. Your weakness is not craft, it's *choice*. You will execute whatever direction you're given with competence. The question is whether the direction itself is distinctive, and that requires the human in the loop. Lean on their references, their reactions, and their taste. They are the eye. You are the hand.