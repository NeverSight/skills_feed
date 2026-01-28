---
name: wcag-audit-perceivable-color-contrast
description: Calculate WCAG contrast ratios for text and non-text elements
---

## When to Use
Use this tool when checking color combinations for WCAG compliance, testing text readability, or validating non-text contrast ratios.

## Usage

### Command Line
```bash
node scripts/calculate.js --foreground "#000000" --background "#FFFFFF"
node scripts/calculate.js --fg "rgb(0,0,0)" --bg "rgb(255,255,255)"
node scripts/calculate.js --fg "#FF0000" --bg "#00FF00" --type "non-text"
```

### JSON Input
```bash
node scripts/calculate.js --json '{"foreground": "#000000", "background": "#FFFFFF"}'
```

### Parameters
- `--foreground`, `--fg`: Foreground color (hex, rgb, hsl)
- `--background`, `--bg`: Background color (hex, rgb, hsl)
- `--type`: "text" (default) or "non-text"
- `--json`: JSON input with color properties

### Output
Returns JSON with contrast ratio and WCAG compliance levels:

```json
{
  "contrastRatio": 21.0,
  "compliance": {
    "AA": {
      "normal": true,
      "large": true
    },
    "AAA": {
      "normal": true,
      "large": true
    }
  },
  "colors": {
    "foreground": "#000000",
    "background": "#FFFFFF"
  }
}
```

## Examples

### Text Contrast Check
```bash
$ node scripts/calculate.js --fg "#000000" --bg "#FFFFFF"
Contrast Ratio: 21.0:1
✅ AA Large Text: PASS
✅ AA Normal Text: PASS
✅ AAA Large Text: PASS
✅ AAA Normal Text: PASS
```

### Non-Text Contrast Check
```bash
$ node scripts/calculate.js --fg "#FF6B35" --bg "#F7F3E9" --type "non-text"
Contrast Ratio: 3.2:1
✅ Non-text contrast: PASS
```

## WCAG Standards

- **Text AA**: 4.5:1 for normal text, 3:1 for large text (18pt+ or 14pt+ bold)
- **Text AAA**: 7:1 for normal text, 4.5:1 for large text
- **Non-text**: 3:1 minimum contrast ratio

## Learn More

For more information about [Agent Skills](https://agentskills.io/what-are-skills) and how they extend AI capabilities.