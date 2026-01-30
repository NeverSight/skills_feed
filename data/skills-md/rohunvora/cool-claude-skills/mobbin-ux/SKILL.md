---
name: mobbin-ux
description: >
  Research-driven UI/UX improvement using Mobbin. Use when user explicitly requests
  design pattern research ("use Mobbin", "research design patterns", "find UX patterns for X").
  Requires Mobbin account and browser automation (claude-in-chrome MCP). Searches Mobbin
  for relevant UI patterns, extracts design principles, generates a spec document for
  approval, then implements. NOT for general UI work—only when user wants research-backed design.
---

# Mobbin UX Research

Research UI/UX patterns on Mobbin, generate a design spec, then implement after approval.

## Workflow

### 1. Clarify the UI component

Ask what type of UI to research:
- "inbox", "dashboard", "settings", "onboarding", "checkout", "profile", etc.
- Platform: web or mobile (iOS/Android)

### 2. Search Mobbin

Use browser automation:

```
1. tabs_context_mcp → get/create tab
2. navigate → mobbin.com
3. Log in if needed (user handles auth)
4. navigate → mobbin.com/search/apps/{web|ios|android}?q={query}
5. screenshot → capture search results
6. Click 3-5 top results, screenshot key screens
```

Search tips:
- Component names: "inbox", "notification", "settings"
- Add qualifiers: "inbox email", "dashboard analytics"

### 3. Extract design patterns

From screenshots, identify:

**Layout:** Column structure, sidebar placement, content organization

**Visual hierarchy:** Typography, colors, spacing, theme (light/dark)

**Interactions:** Hover states, action buttons, progress indicators

**Navigation:** Tabs, filtering, view switching

### 4. Generate design spec

Create spec with `/quick-view`:

```markdown
## Design Patterns for [Component]

**Sources:** [App1], [App2], [App3] via Mobbin

### Layout
- [Pattern]: [Why it works]

### Visual Hierarchy
- [Pattern]: [Why it works]

### Interactions
- [Pattern]: [Why it works]

### Recommended Changes
1. [Specific change]
2. [Specific change]
```

### 5. Get approval

Ask user: "Should I implement these patterns? Any to skip or modify?"

### 6. Implement

After approval, rebuild UI following the spec.

## Example searches

| UI Type | Query |
|---------|-------|
| Email inbox | `inbox email` |
| Task list | `todo inbox` |
| Dashboard | `dashboard analytics` |
| Settings | `settings preferences` |

## Reference apps

- **Inbox:** Superhuman, Spark, Twist
- **Tasks:** Linear, Asana, Todoist
- **Dashboards:** Stripe, Notion, Figma
