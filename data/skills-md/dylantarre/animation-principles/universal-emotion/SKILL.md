---
name: universal-emotion
description: Use when you need to achieve any emotional outcome through animation—provides a framework for mapping Disney principles to any target emotion.
---

# Universal Emotion Animation Framework

Map Disney's 12 principles to any emotional goal through systematic analysis.

## Emotional Goal

Any emotion can be achieved through intentional application of animation principles. This framework helps translate emotional intent into specific motion parameters.

## Emotion Mapping Framework

### Step 1: Define the Emotion

Identify your target on these spectrums:
- **Energy**: Low ←→ High
- **Valence**: Negative ←→ Positive
- **Arousal**: Calm ←→ Excited
- **Dominance**: Submissive ←→ Powerful

### Step 2: Map Principles to Emotion

| Principle | Low Energy | High Energy |
|-----------|------------|-------------|
| Squash & Stretch | 0-10% | 20-40% |
| Anticipation | 50-100ms | 150-300ms |
| Timing | 400-800ms | 100-250ms |
| Exaggeration | 0-15% | 25-50% |
| Follow Through | Extended settle | Quick bounce |

| Principle | Serious | Playful |
|-----------|---------|---------|
| Arc | Direct/Linear | Curved/Bouncy |
| Secondary Action | Minimal | Abundant |
| Straight Ahead | Avoid | Embrace |
| Appeal | Clean/Geometric | Round/Organic |

### Step 3: Select Easing

| Emotion Type | Easing Style | Example |
|--------------|--------------|---------|
| Calm | Symmetric ease | `ease-in-out` |
| Confident | Strong ease-out | `cubic-bezier(0,0,0.2,1)` |
| Playful | Overshoot | `cubic-bezier(0.34,1.56,0.64,1)` |
| Urgent | Sharp ease-out | `cubic-bezier(0.0,0,0.2,1)` |
| Elegant | Extended ease | `cubic-bezier(0.4,0,0.6,1)` |

## Quick Reference by Emotion

### Positive Emotions
- **Joy**: Fast timing, high squash/stretch, bouncy easing
- **Trust**: Consistent timing, minimal deformation, smooth easing
- **Calm**: Slow timing, subtle movement, symmetric easing
- **Excitement**: Fast timing, high energy, dynamic easing

### Functional Emotions
- **Urgency**: Very fast, direct paths, attention-grabbing
- **Professional**: Moderate timing, minimal decoration, standard easing
- **Friendly**: Moderate timing, soft deformation, gentle easing

### Premium Emotions
- **Elegant**: Slower timing, no deformation, refined easing
- **Powerful**: Deliberate timing, impact emphasis, strong easing

## CSS Variables Template

```css
:root {
  /* Adjust based on target emotion */
  --emotion-duration: 300ms;
  --emotion-easing: cubic-bezier(0.4, 0, 0.2, 1);
  --emotion-squash: 1;
  --emotion-overshoot: 0;
}
```

## Decision Tree

1. Is the emotion high or low energy?
2. Is the feeling positive, negative, or neutral?
3. Should users feel in control or guided?
4. Is this a moment or a state?
5. What's the brand personality?

## Combining Emotions

Real experiences blend emotions. Layer principles:
- Primary emotion: 70% influence
- Secondary emotion: 30% influence
- Adjust timing/easing accordingly

## When to Use

- Novel emotional requirements
- Brand-specific interpretations
- Complex emotional journeys
- A/B testing emotional impact
- Cross-cultural considerations
- Accessibility adaptations
