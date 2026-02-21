---
name: theme-audit
description: Validate all themes for completeness and correct usage
---

# Theme Audit

Audit theme definitions and usage across the codebase.

## Theme definitions
!`cat internal/theme/theme.go | head -200`

## Theme usage in UI
!`grep -r "theme\." internal/app/ --include="*.go" | head -50`

## Potential hardcoded colours
!`grep -rE "(lipgloss\.(Color|AdaptiveColor)\(|#[0-9a-fA-F]{6})" internal/app/ --include="*.go" | head -30`

---

Audit themes for:
1. Missing colour fields that UI code expects
2. Unused theme values that can be removed
3. Hardcoded colours in UI code that should use theme fields
4. Contrast issues between foreground and background colours
5. Inconsistencies between different theme variants
