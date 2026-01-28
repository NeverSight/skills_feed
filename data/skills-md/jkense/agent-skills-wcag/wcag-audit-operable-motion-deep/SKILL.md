---
name: wcag-audit-operable-motion-deep
description: Animation and movement accessibility rules for dynamic interface elements
---

## When to Use
Apply when implementing animations, transitions, scrolling effects, or moving visual content.

## Rules
- Provide option to pause, stop, or hide moving content
- Limit animation duration to 5 seconds or less for auto-playing content
- Avoid animations that flash more than 3 times per second
- Respect user motion preferences when available
- Ensure content remains usable during and after animations
- Provide static alternatives for animated content
- Avoid large-scale movement that could trigger vestibular disorders
- Test animations with different motion sensitivity settings

## Avoid
- Auto-playing animations that cannot be paused or stopped
- Rapid flashing or strobe effects above safe thresholds
- Animations that continue when content loses focus
- Motion that obscures important interface elements