---
name: squash-stretch-mastery
description: Use when implementing deformation effects, bounce animations, impact responses, or any motion requiring organic elasticity and weight expression.
---

# Squash & Stretch Mastery

## The Foundation Principle

Squash and stretch is considered the most important of Disney's 12 principles because it solves animation's fundamental problem: making rigid objects feel alive. Developed in the 1930s at Disney, it emerged from observing how real flesh and rubber deform under force while maintaining constant volume.

## Core Theory

**Volume Preservation**: When an object squashes, it must widen. When it stretches, it must narrow. This constraint creates believability—violate it and objects appear to grow or shrink rather than deform.

**Force Visualization**: Squash and stretch makes invisible forces visible. A ball squashing on impact shows us the floor's resistance. A character stretching mid-leap reveals velocity and momentum.

## The Elasticity Spectrum

Not all objects deform equally:
- **High elasticity**: Rubber balls, cartoon characters, jelly (extreme deformation)
- **Medium elasticity**: Human faces, cloth, muscle (subtle deformation)
- **Low elasticity**: Wood, metal, bone (minimal but present micro-deformation)

Even "rigid" objects benefit from 1-2% deformation—it prevents the dead, mechanical feel.

## Interaction with Other Principles

**Timing amplifies squash/stretch**: Fast impacts demand more squash; slow floats need gentle stretch. The deformation amount must match velocity.

**Anticipation uses stretch**: A character winding up for a jump often stretches slightly before the motion begins.

**Follow-through extends it**: After landing, the squash ripples through secondary elements (hair, clothing, flesh).

## Domain Applications

### UI/Motion Design
- Button press: subtle squash (95-98% height) on tap
- List items: stretch slightly when pulled beyond bounds (rubber-band scroll)
- Notifications: squash on arrival, bounce to rest

### Character Animation
- Facial expressions: cheeks squash on smile, stretch on surprise
- Walk cycles: torso compresses on contact, extends on passing
- Emotional beats: extreme stretch for shock, squash for dejection

### Logo Animation
- Bouncing logos: exaggerated squash creates playful personality
- Subtle breathing: micro-squash/stretch keeps static logos alive

### Game Feel
- Jump arcs: stretch on ascent, squash on landing
- Hit reactions: brief squash sells impact before knockback
- Collectibles: rhythmic pulse using gentle squash/stretch

## Common Mistakes

1. **Breaking volume**: Objects appear to grow/shrink instead of deform
2. **Uniform deformation**: Real objects deform more where force is applied
3. **Over-application**: Subtle contexts need 1-5%, not cartoon 50%
4. **Static extremes**: Deformation should ease in/out, never snap

## Implementation Heuristic

Start with 10% deformation for energetic motions, 2-3% for subtle polish. Adjust based on material and tone. When in doubt, less is more—squash/stretch should be felt, not consciously noticed.
