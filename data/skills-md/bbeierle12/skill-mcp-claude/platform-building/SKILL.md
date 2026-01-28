---
name: platform-building
description: Platform-specific building systems for mobile, VR, and accessibility. Use when implementing touch controls for building games, VR spatial input, colorblind-friendly feedback, or cross-platform building mechanics. Covers input adaptation and inclusive design patterns.
---

# Platform Building

Touch controls, VR input, and accessibility patterns for building systems.

## Quick Start

```javascript
import { TouchBuildController } from './scripts/touch-build-controller.js';
import { VRBuildingAdapter } from './scripts/vr-building-adapter.js';
import { AccessibilityConfig } from './scripts/accessibility-config.js';

// Mobile touch building
const touch = new TouchBuildController(canvas, {
  doubleTapToPlace: true,
  pinchToRotate: true,
  swipeToChangePiece: true
});

touch.onPlace = (position, rotation) => buildingSystem.place(position, rotation);
touch.onRotate = (angle) => ghost.rotate(angle);

// VR building with hand tracking
const vr = new VRBuildingAdapter(xrSession, {
  dominantHand: 'right',
  snapToGrid: true,
  comfortMode: true // Reduces motion sickness
});

vr.onGrab = (piece) => selection.select(piece);
vr.onRelease = (position) => buildingSystem.place(position);

// Accessibility configuration
const a11y = new AccessibilityConfig({
  colorblindMode: 'deuteranopia', // red-green
  highContrast: true,
  screenReaderHints: true
});

// Apply to ghost preview
ghost.setColors(a11y.getValidityColors());
```

## Reference

See `references/platform-considerations.md` for:
- Mobile gesture patterns (Fortnite Mobile, Minecraft PE)
- VR building research and comfort guidelines
- Colorblind palette recommendations
- Screen reader integration patterns
- Cross-platform input abstraction

## Scripts

| File | Lines | Purpose |
|------|-------|---------|
| `touch-build-controller.js` | ~450 | Mobile gestures: tap, drag, pinch, swipe |
| `vr-building-adapter.js` | ~400 | VR hand/controller input, comfort settings |
| `accessibility-config.js` | ~350 | Colorblind modes, contrast, screen reader |

## Platform Detection

```javascript
// Detect platform capabilities
const platform = {
  isMobile: /Android|iPhone|iPad|iPod/i.test(navigator.userAgent),
  isTouch: 'ontouchstart' in window,
  isVR: navigator.xr !== undefined,
  prefersReducedMotion: window.matchMedia('(prefers-reduced-motion: reduce)').matches,
  prefersHighContrast: window.matchMedia('(prefers-contrast: more)').matches
};

// Initialize appropriate controllers
if (platform.isVR && xrSession) {
  setupVRControls();
} else if (platform.isTouch) {
  setupTouchControls();
} else {
  setupMouseKeyboard();
}
```

## Mobile Considerations

Fortnite Mobile demonstrates effective touch building with customizable HUD, auto-material selection, and gesture-based piece rotation. Key patterns include dedicated build mode toggle, large touch targets (minimum 44px), and visual feedback for all actions.

## VR Considerations

VR building requires attention to comfort. Snap rotation reduces motion sickness, and arm-length building distances prevent fatigue. Hand tracking enables intuitive grab-and-place, while controller building benefits from laser-pointer selection for distant pieces.

## Accessibility Patterns

Valheim uses blue/yellow instead of green/red for stability indicators, supporting deuteranopia (the most common colorblind condition). High contrast modes should use 7:1 ratio for critical indicators, and all visual feedback should have audio/haptic alternatives.
