---
name: wcag-audit-operable-motion-test
description: Test animations for motion sensitivity compliance and reduced motion preferences
---

## When to Use
Use this tool when implementing animations, transitions, or moving content to ensure compliance with motion sensitivity guidelines and respect for user reduced motion preferences.

## Usage

### Command Line
```bash
node scripts/test.js --duration 3.5 --type parallax
node scripts/test.js --duration 2.0 --flashes 5 --reduced-motion true
node scripts/test.js --json '{"duration": 4.2, "type": "scroll", "flashes": 0}'
```

### JSON Input
```bash
node scripts/test.js --json '{
  "duration": 3.5,
  "type": "carousel",
  "flashes": 0,
  "userPrefersReducedMotion": true
}'
```

### Parameters
- `--duration`: Animation duration in seconds
- `--type`: Animation type (scroll, parallax, carousel, transition, etc.)
- `--flashes`: Number of flashes per second (default: 0)
- `--reduced-motion`: Whether to simulate reduced motion preference (true/false)
- `--json`: JSON input with animation properties

### Output
Returns JSON with compliance assessment and recommendations:

```json
{
  "animation": {
    "duration": 3.5,
    "type": "parallax",
    "flashes": 0
  },
  "compliance": {
    "reducedMotion": true,
    "flashing": true,
    "duration": false
  },
  "issues": ["Animation duration exceeds 5 seconds"],
  "recommendations": [
    "Provide option to pause or disable parallax scrolling",
    "Consider using reduced motion alternative"
  ]
}
```

## Examples

### Test short animation
```bash
$ node scripts/test.js --duration 2.0 --type transition
✅ Reduced motion: RESPECTED
✅ Flashing: PASS (no flashes detected)
✅ Duration: PASS (2.0s within limit)
Animation meets accessibility requirements
```

### Test long animation
```bash
$ node scripts/test.js --duration 8.5 --type carousel
⚠️  Reduced motion: NEEDS ATTENTION
✅ Flashing: PASS (no flashes detected)
❌ Duration: FAIL (8.5s exceeds 5s limit)
Recommendations:
- Provide pause/stop controls for auto-advancing carousel
- Consider shorter transition duration or user control
- Offer static alternative when reduced motion is preferred
```

### Test flashing content
```bash
$ node scripts/test.js --duration 1.0 --flashes 4
✅ Reduced motion: RESPECTED
❌ Flashing: FAIL (4 flashes/s exceeds 3 flashes/s limit)
❌ Duration: PASS (1.0s within limit)
Recommendations:
- Reduce flashing frequency to maximum 3 flashes per second
- Consider non-flashing alternatives
- Test with users sensitive to flashing content
```

## WCAG Standards

- **Reduced Motion**: Respect `prefers-reduced-motion` user preference
- **Flashing Limit**: Maximum 3 flashes per second
- **Auto-play Duration**: Moving content should be pausable within 5 seconds
- **User Control**: Provide options to pause, stop, or hide moving content
- **Alternatives**: Offer static alternatives for animated content

## Animation Types

### Safe Types
- **Fade transitions**: Gradual opacity changes
- **Slide transitions**: Smooth position changes
- **Scale transforms**: Size changes without movement

### Risk Types
- **Parallax scrolling**: Multiple layers moving at different speeds
- **Auto-advancing carousels**: Content that changes automatically
- **Flashing elements**: Rapid visibility changes
- **Spinning animations**: Rotational movement

## Best Practices

1. **Check user preferences**: Always respect `prefers-reduced-motion`
2. **Provide controls**: Allow users to pause/stop animations
3. **Limit duration**: Keep auto-playing content under 5 seconds
4. **Avoid flashing**: Never exceed 3 flashes per second
5. **Test alternatives**: Ensure functionality without animation

## Learn More

For more information about [Agent Skills](https://agentskills.io/what-are-skills) and how they extend AI capabilities.