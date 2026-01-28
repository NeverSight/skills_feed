---
name: wcag-audit-perceivable-text-size
description: Convert between px, pt, em, rem units with accessibility context
---

## When to Use
Use this tool when converting font sizes between units, checking accessibility compliance, or ensuring consistent typography scaling across different contexts.

## Usage

### Command Line
```bash
node scripts/convert.js --from 16px --to rem
node scripts/convert.js --value 1.25rem --base-font 16px --to px
node scripts/convert.js --from 14pt --to px --accessibility-check
```

### JSON Input
```bash
node scripts/convert.js --json '{"from": "16px", "to": "rem", "baseFontSize": "16px"}'
```

### Parameters
- `--from`: Source font size with unit (e.g., "16px", "12pt", "1.5em")
- `--to`: Target unit (px, pt, em, rem)
- `--value`: Alternative to --from for specifying the value
- `--base-font`: Base font size for em/rem calculations (default: 16px)
- `--accessibility-check`: Include WCAG compliance assessment
- `--json`: JSON input with conversion parameters

### Output
Returns JSON with conversion results and accessibility assessment:

```json
{
  "input": "16px",
  "output": "1rem",
  "baseFontSize": "16px",
  "accessibility": {
    "meetsMinimum": true,
    "recommendations": []
  }
}
```

## Examples

### Basic conversion
```bash
$ node scripts/convert.js --from 16px --to rem
16px = 1rem (base font: 16px)
✅ Accessibility: PASS (16px meets 14px minimum)
```

### Point to pixel conversion
```bash
$ node scripts/convert.js --from 12pt --to px
12pt = 16px (1pt ≈ 1.333px)
✅ Accessibility: PASS (16px meets 14px minimum)
```

### EM calculation with custom base
```bash
$ node scripts/convert.js --value 1.5em --base-font 18px --to px
1.5em = 27px (base font: 18px)
✅ Accessibility: PASS (27px exceeds 14px minimum)
```

### Accessibility check
```bash
$ node scripts/convert.js --from 12px --to pt --accessibility-check
12px = 9pt
❌ Accessibility: FAIL (12px below 14px minimum for body text)
Recommendation: Increase to at least 14px (≈10.5pt) for readable text
```

## Unit Conversions

### Absolute Units
- **px (pixels)**: Screen pixels, most common for web
- **pt (points)**: Print units, 1pt = 1/72 inch

### Relative Units
- **em**: Relative to parent element's font size
- **rem**: Relative to root element's font size (usually 16px)

### Conversion Formulas
- 1pt ≈ 1.333px (at 96 DPI)
- 1em = 1 × parent font size
- 1rem = 1 × root font size (default: 16px)

## WCAG Standards

- **Minimum Size**: 14px for body text, 18px for headings
- **Zoom Support**: Text must resize up to 200% without loss of functionality
- **Relative Units**: Prefer rem/em for better accessibility and responsiveness
- **Print Compatibility**: Consider pt units for print stylesheets

## Best Practices

1. **Use relative units**: rem/em scale better with user preferences
2. **Set root font size**: Use 16px as base for consistent calculations
3. **Test zoom**: Ensure text remains readable when zoomed to 200%
4. **Consider context**: Different minimum sizes for different content types
5. **Avoid fixed sizes**: Allow user font size preferences to take effect

## Learn More

For more information about [Agent Skills](https://agentskills.io/what-are-skills) and how they extend AI capabilities.