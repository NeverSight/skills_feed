---
name: wcag-audit-operable-target-size
description: Validate touch target sizes meet 44x44px minimum requirement
---

## When to Use
Use this tool when designing buttons, links, form controls, or any interactive elements to ensure they meet minimum touch target size requirements for accessibility.

## Usage

### Command Line
```bash
node scripts/check.js --width 48 --height 48
node scripts/check.js --width 32 --height 40 --spacing 8
node scripts/check.js --element "button" --dimensions "44x44"
```

### JSON Input
```bash
node scripts/check.js --json '{"width": 48, "height": 48, "spacing": 8}'
```

### Parameters
- `--width`: Element width in pixels
- `--height`: Element height in pixels
- `--spacing`: Minimum spacing between adjacent targets (optional)
- `--element`: Element type description (optional)
- `--dimensions`: Dimensions as "WxH" format (alternative to width/height)
- `--json`: JSON input with dimensions and spacing properties

### Output
Returns JSON with compliance status and recommendations:

```json
{
  "dimensions": {
    "width": 48,
    "height": 48
  },
  "minimumRequired": {
    "width": 44,
    "height": 44
  },
  "compliance": {
    "size": true,
    "spacing": true
  },
  "recommendations": []
}
```

## Examples

### Check a button size
```bash
$ node scripts/check.js --width 48 --height 48 --element "primary button"
✅ Size: PASS (48x48px meets 44x44px minimum)
✅ Spacing: PASS (8px spacing provided)
No issues found - this target meets accessibility requirements
```

### Check a small link
```bash
$ node scripts/check.js --width 24 --height 16 --element "footer link"
❌ Size: FAIL (24x16px is below 44x44px minimum)
❌ Spacing: FAIL (insufficient spacing between targets)
Recommendations:
- Increase width to at least 44px (currently 24px)
- Increase height to at least 44px (currently 16px)
- Ensure at least 8px spacing between adjacent interactive elements
```

## WCAG Standards

- **Minimum Size**: 44px by 44px (approximately 9mm) for touch targets
- **Spacing**: Adequate spacing between adjacent targets to prevent accidental activation
- **Exceptions**: Smaller targets allowed if identical function available with larger target within same page
- **Enhanced**: 44px by 44px strongly recommended, smaller targets only in exceptional cases

## Best Practices

1. **Use 44x44px minimum**: Design all touch targets at least this size
2. **Consider thumb size**: Account for finger/thumb size in mobile designs
3. **Provide spacing**: Ensure at least 8px between interactive elements
4. **Test on device**: Verify usability on actual touch devices
5. **Consider context**: Smaller targets may be acceptable in non-critical areas

## Learn More

For more information about [Agent Skills](https://agentskills.io/what-are-skills) and how they extend AI capabilities.