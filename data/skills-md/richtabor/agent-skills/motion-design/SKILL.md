---
name: motion-design
description: Provides motion design guidance for UI components. Triggers on animation requests ("animate this", "add transition", "motion for"), refinement requests ("clean up this animation", "clean up the motion", "this feels too fast/slow", "make this feel more alive/natural"), and questions about easing, timing, or micro-interactions.
---

# Motion Design

## Overview

Design intentional, purposeful motion for product UI. This skill evaluates animation needs and recommends specific easing curves, durations, and implementation approaches based on interaction frequency and purpose.

Every animation needs a job. If it has no job, don't animate.

## Process

### Phase 1: Load References (Required)

Before any recommendations, read both reference files:

1. **Decision Tree** (`references/decision-tree.md`) - Which easing category to use based on the interaction type, plus scale/origin/hover guidance
2. **Easing Tokens** (`references/easing-tokens.md`) - Specific curves, duration values, and performance guidelines

### Phase 2: Evaluate the Animation

For each component or interaction, determine:

**2.1 Purpose**

What job does this animation do?

- **Responsiveness** - Button press, menu open, immediate feedback
- **Spatial continuity** - Things come from somewhere and go somewhere
- **Understanding** - Illustrating a concept, onboarding, marketing
- **Delight** - Rare interactions only (use sparingly)

If no clear purpose exists, recommend no animation.

**2.2 Frequency**

How often will users trigger this?

- **High-frequency / keyboard-driven** - Prefer no animation or near-instant
- **Medium-frequency / common interactions** - Keep it fast (120-240ms)
- **Low-frequency / illustrative** - More freedom for slower, richer motion

**2.3 Pattern Type**

What kind of motion is this?

- **Enter/exit** - Popover, modal, toast, dropdown appearing or leaving (exits are typically faster than enters—users want things gone quickly)
- **On-screen morph** - Layout shift, expanding content, repositioning
- **Time-based** - Progress indicator, marquee, hold-to-delete
- **Hover/subtle** - Color change, opacity fade, background shift
- **Keyboard navigation** - Arrow keys, tab focus, rapid selection

### Phase 3: Recommend

Based on the evaluation, provide specific recommendations using tokens from the reference files.

## Output Format

For each animation request, provide:

```
## Animation Recommendation

**Component**: [What's being animated]

### Evaluation
- **Purpose**: [responsiveness / spatial / understanding / delight / none]
- **Frequency**: [high / medium / low]
- **Pattern**: [enter-exit / morph / time-based / hover / keyboard]

### Recommendation
- **Easing**: [token name] — `[cubic-bezier value]`
- **Duration**: [token name] — `[ms value]`
- **Properties**: [transform, opacity, etc.]
- **Transform Origin**: [if applicable]
- **Spring vs Bezier**: [recommendation and why]
- **Bounce**: [yes/no and why]

### Implementation
[Code snippet or CSS/JS example]

### Notes
[Any specific guidance for this case]
```

## Example Interaction

**User**: "How should I animate this dropdown menu?"

**Response**:

```
## Animation Recommendation

**Component**: Dropdown menu

### Evaluation
- **Purpose**: Responsiveness — immediate feedback when user clicks trigger
- **Frequency**: Medium — common interaction but not rapid-fire
- **Pattern**: Enter/exit — appearing and disappearing from screen

### Recommendation
- **Easing**: --ease-out-quart — `cubic-bezier(.165, .84, .44, 1)`
- **Duration**: --dur-2 — `180ms`
- **Properties**: transform (scale, translateY), opacity
- **Transform Origin**: Top center (or top-left/top-right based on trigger position)
- **Spring vs Bezier**: Bezier is fine here; spring useful if menu can be interrupted mid-animation
- **Bounce**: No — tap-to-open shouldn't bounce

### Implementation
```css
.dropdown {
  transform-origin: top center;
  transition:
    transform 180ms cubic-bezier(.165, .84, .44, 1),
    opacity 180ms cubic-bezier(.165, .84, .44, 1);
}

.dropdown[data-state="closed"] {
  opacity: 0;
  transform: scale(0.96) translateY(-8px);
}

.dropdown[data-state="open"] {
  opacity: 1;
  transform: scale(1) translateY(0);
}
```

### Notes
- Use scale(0.96), not scale(0)
- Set transform-origin to match trigger position
- Keep under 240ms for snappy feel
```

## Tips for Best Results

1. **Be specific about the component** - "dropdown" vs "modal" vs "tooltip" matters
2. **Mention the trigger** - Click, hover, keyboard, scroll
3. **Share context** - "This is a productivity app" vs "marketing landing page"
4. **Ask about multiple states** - Open, close, hover, disabled
5. **Specify framework** - CSS, Framer Motion, GSAP, React Spring

## Resources

This skill includes:

### references/decision-tree.md
Flowchart for choosing the right easing category based on interaction type. Includes scale values, transform-origin guidance, hover/touch considerations, and accessibility.

### references/easing-tokens.md
Complete set of easing curves (ease-out, ease-in-out families), duration tokens, and performance guidelines.
