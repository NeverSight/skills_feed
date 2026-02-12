---
name: slidev-transitions
description: Add smooth slide transitions in Slidev. Use this skill for fade, slide, and custom transitions between slides.
---

# Slide Transitions in Slidev

This skill covers adding smooth transitions between slides in Slidev, including built-in transitions, custom animations, and directional transitions.

## When to Use This Skill

- Adding polish to presentations
- Creating smooth navigation experiences
- Emphasizing slide changes
- Matching presentation themes
- Creating unique visual effects

## Setting Transitions

### Global Transition (Frontmatter)

```yaml
---
transition: slide-left
---
```

Applied to all slides in the presentation.

### Per-Slide Transition

```markdown
---
transition: fade
---

# This slide fades in

---
transition: slide-up
---

# This slide slides up
```

### Inline with Separator

```markdown
# Slide 1

---
transition: zoom
---

# Slide 2 (zooms in)
```

## Built-in Transitions

### Fade Transitions

| Name | Effect |
|------|--------|
| `fade` | Simple fade in/out |
| `fade-out` | Fade out, then appear |

```markdown
---
transition: fade
---
```

### Slide Transitions

| Name | Effect |
|------|--------|
| `slide-left` | New slide enters from right |
| `slide-right` | New slide enters from left |
| `slide-up` | New slide enters from bottom |
| `slide-down` | New slide enters from top |

```markdown
---
transition: slide-left
---
```

### View Transition

Uses the modern View Transitions API:

```markdown
---
transition: view-transition
---
```

**Note**: Requires browser support for View Transitions API.

## Directional Transitions

### Forward/Backward Different

Use `|` to separate forward and backward transitions:

```markdown
---
transition: slide-left | slide-right
---
```

- Going forward: slides left
- Going backward: slides right

### Common Patterns

```markdown
# Natural slide direction
---
transition: slide-left | slide-right
---

# Vertical navigation
---
transition: slide-up | slide-down
---

# Fade forward, slide back
---
transition: fade | slide-right
---
```

## Custom Transitions

### CSS-based Custom Transition

Create `styles/index.css`:

```css
/* Define custom transition */
.my-transition-enter-active,
.my-transition-leave-active {
  transition: all 0.5s ease;
}

.my-transition-enter-from {
  opacity: 0;
  transform: translateX(100px) rotate(10deg);
}

.my-transition-leave-to {
  opacity: 0;
  transform: translateX(-100px) rotate(-10deg);
}
```

Use in frontmatter:

```yaml
---
transition: my-transition
---
```

### Transition Classes

Slidev uses Vue transition classes:

| Class | When Applied |
|-------|--------------|
| `[name]-enter-from` | Starting state for enter |
| `[name]-enter-active` | During enter transition |
| `[name]-enter-to` | Ending state for enter |
| `[name]-leave-from` | Starting state for leave |
| `[name]-leave-active` | During leave transition |
| `[name]-leave-to` | Ending state for leave |

## Transition Examples

### Scale Transition

```css
.scale-enter-active,
.scale-leave-active {
  transition: all 0.4s ease;
}

.scale-enter-from {
  opacity: 0;
  transform: scale(0.8);
}

.scale-leave-to {
  opacity: 0;
  transform: scale(1.2);
}
```

### Flip Transition

```css
.flip-enter-active,
.flip-leave-active {
  transition: all 0.6s ease;
  transform-style: preserve-3d;
}

.flip-enter-from {
  opacity: 0;
  transform: rotateY(-90deg);
}

.flip-leave-to {
  opacity: 0;
  transform: rotateY(90deg);
}
```

### Blur Transition

```css
.blur-enter-active,
.blur-leave-active {
  transition: all 0.5s ease;
}

.blur-enter-from {
  opacity: 0;
  filter: blur(20px);
}

.blur-leave-to {
  opacity: 0;
  filter: blur(20px);
}
```

### Bounce Transition

```css
.bounce-enter-active {
  animation: bounce-in 0.5s;
}

.bounce-leave-active {
  animation: bounce-out 0.5s;
}

@keyframes bounce-in {
  0% {
    opacity: 0;
    transform: scale(0.3);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes bounce-out {
  0% {
    opacity: 1;
    transform: scale(1);
  }
  100% {
    opacity: 0;
    transform: scale(0.3);
  }
}
```

### Swipe Transition

```css
.swipe-enter-active,
.swipe-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.swipe-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.swipe-leave-to {
  opacity: 0;
  transform: translateX(-100%);
}
```

## View Transitions API

### Basic Usage

```yaml
---
transition: view-transition
---
```

### Named View Transitions

```markdown
<div style="view-transition-name: hero">
  Content that transitions smoothly
</div>
```

Elements with the same `view-transition-name` on consecutive slides will animate between their positions.

### Practical Example

```markdown
---
transition: view-transition
---

<div style="view-transition-name: card" class="w-32 h-32 bg-blue-500">
  Small card
</div>

---
transition: view-transition
---

<div style="view-transition-name: card" class="w-64 h-64 bg-blue-500">
  Card grows!
</div>
```

## Transition Timing

### Duration

```css
.slow-fade-enter-active,
.slow-fade-leave-active {
  transition: all 1s ease; /* 1 second */
}
```

### Easing Functions

```css
/* Common easing functions */
.ease-in { transition-timing-function: ease-in; }
.ease-out { transition-timing-function: ease-out; }
.ease-in-out { transition-timing-function: ease-in-out; }
.linear { transition-timing-function: linear; }

/* Cubic bezier for custom easing */
.custom { transition-timing-function: cubic-bezier(0.68, -0.55, 0.265, 1.55); }
```

### Delay

```css
.delayed-enter-active {
  transition: all 0.5s ease 0.2s; /* 0.2s delay */
}
```

## Transition Per Slide Type

### Different Transitions for Different Content

```markdown
---
layout: cover
transition: fade
---

# Title Slide

---
layout: default
transition: slide-left
---

# Content Slide

---
layout: section
transition: zoom
---

# Section Break

---
layout: end
transition: fade
---

# Thank You
```

## Disabling Transitions

### No Transition

```yaml
---
transition: none
---
```

### Disable Globally

```yaml
---
transition: false
---
```

## Best Practices

### 1. Consistency

Use the same transition family throughout:

```markdown
# Good: Consistent slide family
---
transition: slide-left | slide-right
---
```

### 2. Match Content Type

| Content | Suggested Transition |
|---------|---------------------|
| Cover/Title | `fade` |
| Regular content | `slide-left` |
| Section break | `fade` or `zoom` |
| Demo/Code | `fade` |
| Conclusion | `fade` |

### 3. Keep It Subtle

❌ **Too flashy**
```css
.crazy-enter-active {
  animation: spin 2s, bounce 1s, flash 0.5s;
}
```

✓ **Professional**
```css
.subtle-enter-active {
  transition: opacity 0.3s ease;
}
```

### 4. Consider Audience

- Technical presentations: Minimal transitions
- Creative presentations: More freedom
- Long presentations: Less distracting

### 5. Test Performance

Complex transitions may lag on:
- Large presentations
- Older devices
- When exporting to PDF

## Transition Presets

### Professional Set

```css
/* styles/transitions.css */

/* Gentle fade */
.pro-fade-enter-active,
.pro-fade-leave-active {
  transition: opacity 0.3s ease;
}
.pro-fade-enter-from,
.pro-fade-leave-to {
  opacity: 0;
}

/* Smooth slide */
.pro-slide-enter-active,
.pro-slide-leave-active {
  transition: all 0.35s ease-out;
}
.pro-slide-enter-from {
  opacity: 0;
  transform: translateX(30px);
}
.pro-slide-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}
```

### Playful Set

```css
/* Energetic bounce */
.playful-enter-active {
  animation: pop-in 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

@keyframes pop-in {
  0% { transform: scale(0); opacity: 0; }
  80% { transform: scale(1.1); }
  100% { transform: scale(1); opacity: 1; }
}
```

## Output Format

When configuring transitions:

```yaml
---
# GLOBAL TRANSITION (first slide)
transition: [transition-name] | [backward-transition]
---

# Slide content...

---
# PER-SLIDE OVERRIDE (if needed)
transition: [different-transition]
---

# Different slide content...
```

**TRANSITION PLAN:**
1. Cover slide: [transition]
2. Content slides: [transition]
3. Section breaks: [transition]
4. Conclusion: [transition]

**CUSTOM CSS (if needed):**
```css
.[name]-enter-active { ... }
.[name]-leave-to { ... }
```
