---
name: wcag-audit-operable-keyboard-focus
description: Validate logical keyboard navigation order for interface elements
---

## When to Use
Use this tool when designing keyboard navigation flows, testing tab order, or ensuring logical focus progression through interactive elements.

## Usage

### Command Line
```bash
node scripts/validate.js --elements "header, nav, main, button, button, footer"
node scripts/validate.js --tab-order "1,2,3,4,5" --expected "1,2,3,4,5"
node scripts/validate.js --json '{"elements": ["header", "nav", "main", "button#submit"], "tabOrder": [1,2,3,4]}'
```

### JSON Input
```bash
node scripts/validate.js --json '{
  "elements": ["header", "nav", "button#menu", "main", "button#submit", "footer"],
  "tabOrder": [1, 2, 3, 4, 5, 6],
  "expectedOrder": [1, 2, 4, 5, 3, 6]
}'
```

### Parameters
- `--elements`: Comma-separated list of element identifiers
- `--tab-order`: Comma-separated list of tab order indices
- `--expected`: Expected logical order (optional)
- `--json`: JSON input with elements and tab order properties

### Output
Returns JSON with validation results and issues:

```json
{
  "elements": ["header", "nav", "main", "button", "footer"],
  "tabOrder": [1, 2, 3, 4, 5],
  "validation": {
    "logical": true,
    "complete": true,
    "issues": []
  },
  "recommendations": [
    "Consider moving primary action button before secondary navigation"
  ]
}
```

## Examples

### Validate simple tab order
```bash
$ node scripts/validate.js --elements "header, nav, main, button, footer" --tab-order "1,2,3,4,5"
✅ Logical order: PASS
✅ Complete coverage: PASS
✅ No focus traps: PASS
Focus order follows logical reading sequence
```

### Detect focus order issues
```bash
$ node scripts/validate.js --elements "header, nav, button, main, footer" --tab-order "1,2,4,3,5"
❌ Logical order: FAIL
⚠️  Tab order issue: "main" (position 3) appears before "button" (position 4)
Recommendations:
- Move main content before secondary buttons
- Consider semantic HTML structure for better default tab order
```

## WCAG Standards

- **Logical Order**: Focus order should follow logical reading sequence
- **No Traps**: Users should not get trapped in focus loops
- **Complete Coverage**: All interactive elements should be keyboard accessible
- **Skip Links**: Provide mechanisms to skip repeated navigation sections
- **Modal Focus**: Modal dialogs should manage focus appropriately

## Best Practices

1. **Follow reading order**: Tab order should match visual reading sequence
2. **Use semantic HTML**: Proper heading hierarchy and landmarks improve default tab order
3. **Provide skip links**: Allow users to skip navigation sections
4. **Test with keyboard**: Verify all interactions work without mouse
5. **Avoid focus traps**: Ensure users can always move forward and backward

## Focus Order Patterns

### Good Order:
1. Header/Skip links
2. Main navigation
3. Main content
4. Footer links
5. Footer

### Problematic Order:
1. Header
2. Footer links
3. Main navigation
4. Main content

## Learn More

For more information about [Agent Skills](https://agentskills.io/what-are-skills) and how they extend AI capabilities.