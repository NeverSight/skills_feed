---
name: expressive-design
description: Material 3 Expressive (M3E). Comprehensive guidance on expressive design system for Flutter with platform support for Android and Linux desktop. Covers color tokens, typography scales, motion specifications, shape tokens, spacing ramps, and component enhancements for creating emotionally engaging UIs. Includes migration guidance from standard M3 and platform-specific integration notes.
---

# Material 3 Expressive Design System

Material 3 Expressive (M3E) is Google's most researched design system update, based on 46 studies with 18,000+ participants. It creates emotionally engaging user experiences through strategic use of color, shape, size, motion, and containment.

## Quick Reference

| Category | Reference | Description |
|----------|-----------|-------------|
| Foundations | [FOUNDATIONS.md](references/FOUNDATIONS.md) | Research, principles, communication, core elements |
| Color | [COLOR.md](references/COLOR.md) | Tokens, palettes, contrast specs |
| Typography | [TYPOGRAPHY.md](references/TYPOGRAPHY.md) | Scales, values, treatments |
| Motion | [MOTION.md](references/MOTION.md) | Durations, easing, transitions |
| Shapes | [SHAPES.md](references/SHAPES.md) | Radii, tokens, containment |
| Spacing | [SPACING.md](references/SPACING.md) | Spacing ramps, touch targets |
| Components | [COMPONENTS.md](references/COMPONENTS.md) | Component specifications |
| Migration | [MIGRATION.md](references/MIGRATION.md) | M3 to M3E migration guide |
| Accessibility | [ACCESSIBILITY.md](references/ACCESSIBILITY.md) | Compliance, testing |
| Platforms | [PLATFORMS.md](references/PLATFORMS.md) | Android and Linux desktop |

## Core Expressive Elements

1. **Color** - Expanded tonal palettes, container tiers, emotional selection
2. **Shape** - Expressive radii, containment, visual boundaries
3. **Size** - Larger touch targets, visual hierarchy
4. **Motion** - Energetic transitions, emotional timing
5. **Containment** - Surface elevation, tonal separation

## When to Use M3 Expressive

- Media and entertainment applications
- Communication apps (email, messaging)
- Social platforms
- Creative tools
- Consumer-facing products

## When to Avoid M3 Expressive

- Banking and financial applications
- Safety-critical interfaces
- Healthcare and medical software
- Productivity tools requiring efficiency
- Forms-heavy applications

## Platform Support

- **Android** - Dynamic color, Android 16 integration, native behaviors
- **Linux Desktop** - Keyboard navigation, focus management, desktop interactions

## Key Research Findings

- 87% preference among 18-24 age group
- 4x faster element recognition
- 32% increase in subculture perception
- 34% boost in modernity
- Erases age-related usability gaps

## Flutter Integration

Use the [m3e_design](https://pub.dev/packages/m3e_design) package for M3 Expressive implementation:

```yaml
dependencies:
  m3e_design: ^0.2.1
  dynamic_color: ^1.8.1
```

## Next Steps

1. Review [FOUNDATIONS.md](references/FOUNDATIONS.md) for core principles
2. Apply color system from [COLOR.md](references/COLOR.md)
3. Implement typography from [TYPOGRAPHY.md](references/TYPOGRAPHY.md)
4. Add motion from [MOTION.md](references/MOTION.md)
5. Apply shapes from [SHAPES.md](references/SHAPES.md)
6. Configure spacing from [SPACING.md](references/SPACING.md)
7. Implement components from [COMPONENTS.md](references/COMPONENTS.md)
8. Migrate existing M3 from [MIGRATION.md](references/MIGRATION.md)
9. Ensure accessibility with [ACCESSIBILITY.md](references/ACCESSIBILITY.md)
10. Configure platform-specifics from [PLATFORMS.md](references/PLATFORMS.md)
