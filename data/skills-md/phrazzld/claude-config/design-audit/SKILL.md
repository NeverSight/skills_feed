---
name: design-audit
description: |
  DESIGN-AUDIT
---

---
description: Audit current design system for consistency and debt
---

# DESIGN-AUDIT

Analyze the current design system for violations, gaps, and inconsistencies.

## What This Does

1. **Inventory tokens** — Colors, typography, spacing, shadows
2. **Check consistency** — Are tokens used consistently?
3. **Find violations** — Hardcoded values, magic numbers
4. **Assess accessibility** — WCAG compliance
5. **Report debt** — Design debt that's accumulated

## Process

### 1. Load Design Skills

```
Skill("design-tokens")        # Token patterns
Skill("ui-skills")            # Implementation constraints
Skill("web-interface-guidelines")  # Vercel standards
```

### 2. Extract Current Tokens

Scan for design token definitions:
- Tailwind config (`tailwind.config.ts`, `globals.css`)
- CSS variables
- Theme files
- Component defaults

### 3. Audit Token Usage

For each token category:

**Colors**:
- Are colors from the palette? Or hardcoded hex?
- Is there semantic naming (primary, error, success)?
- Dark mode support?

**Typography**:
- Font scales defined?
- Consistent heading hierarchy?
- Line heights appropriate?

**Spacing**:
- Spacing scale in use?
- Magic numbers in margins/padding?

**Components**:
- Consistent component patterns?
- Reusable primitives?
- Duplicated styles?

### 4. Accessibility Check

```
/rams — Score current state
```

Check:
- Color contrast (WCAG AA minimum)
- Focus states
- Touch targets
- Screen reader support

### 5. Report Findings

```markdown
## Design Audit: [Project Name]

### Token Inventory
- Colors: [count] defined, [violations] hardcoded
- Typography: [count] scales, [violations] magic sizes
- Spacing: [count] values, [violations] arbitrary

### Consistency Score: [X]/100

### Critical Issues
- [ ] [Issue] - [location] - [fix]

### Debt Items
- [ ] [Tech debt] - [impact] - [effort]

### RAMS Score: [X]/100

### Recommendations
1. [Priority fix]
2. [Improvement]
```

## Output

Audit report ready. Next: `/design-catalog` to explore new directions, or `/design-theme` to fix issues.
