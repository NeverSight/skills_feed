---
name: forms-inputs
description: Use when animating form fields, inputs, textareas, selects, or interactive form elements to improve usability and feedback
---

# Form & Input Animation Principles

Apply Disney's 12 principles to forms for clear feedback and delightful interactions.

## Principles Applied to Form Elements

### 1. Squash & Stretch
Input fields can subtly expand on focus (1-2px height). Submit button compresses on click. Checkboxes bounce on toggle.

### 2. Anticipation
Label floats up before user types. Focus ring appears before content entry. Prepares user for input action.

### 3. Staging
Focused input should be visually prominent: border color, shadow, label position. Other fields can slightly dim. Guide attention.

### 4. Straight Ahead & Pose to Pose
Define input states: default, focus, filled, valid, invalid, disabled. Clear poses for each state with smooth transitions.

### 5. Follow Through & Overlapping Action
Floating label settles after reaching final position. Validation icon can bounce slightly. Character counter updates with subtle motion.

### 6. Ease In & Ease Out
Focus transitions: `ease-out`. Validation feedback: `ease-in-out`. Label float: `cubic-bezier(0.4, 0, 0.2, 1)`.

### 7. Arcs
Floating labels should arc slightly during upward movement, not straight line. Adds organic feel to mechanical action.

### 8. Secondary Action
While border highlights (primary), label floats (secondary), helper text appears (tertiary). Coordinate without overwhelming.

### 9. Timing
- Focus border: 100-150ms
- Label float: 150-200ms
- Validation feedback: 200ms
- Error shake: 300ms (3-4 cycles)
- Success check: 250ms
- Checkbox toggle: 150ms

### 10. Exaggeration
Error states can shake (4-6px, 2-3 times). Success states can pulse green briefly. Invalid inputs deserve clear, noticeable feedback.

### 11. Solid Drawing
Maintain border-radius consistency. Label typography should stay crisp during transform. Icons should scale proportionally.

### 12. Appeal
Responsive forms feel modern. Micro-animations guide users. Satisfying feedback reduces form abandonment. Worth the investment.

## CSS Implementation

```css
.input-field {
  transition: border-color 150ms ease-out,
              box-shadow 150ms ease-out;
}

.floating-label {
  transition: transform 200ms cubic-bezier(0.4, 0, 0.2, 1),
              font-size 200ms ease-out,
              color 150ms ease-out;
}

.input-field:focus + .floating-label {
  transform: translateY(-24px) scale(0.85);
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}
```

## Key Properties
- `transform`: translateY (label), translateX (shake)
- `border-color`: state indication
- `box-shadow`: focus rings
- `color`: label/text states
- `opacity`: helper text, icons
