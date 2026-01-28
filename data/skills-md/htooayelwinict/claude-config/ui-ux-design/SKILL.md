---
name: ui-ux-design
description: Design and implement UI/UX changes using existing components and Tailwind tokens; ensure accessibility. EXCLUSIVE to ui-ux-designer agent.
allowed-tools: Read, Edit, Grep, Glob, Write, mcp_context7, mcp_playwright, mcp_zai-mcp-server
---
# UI/UX Design

**Exclusive to:** `ui-ux-designer` agent

## 📚 Context7 (Memory) — Up-to-Date Docs

Lookup latest component patterns and accessibility guidelines:
```
mcp_context7_resolve-library-id(libraryName="shadcn-ui", query="dialog modal")
mcp_context7_query-docs(libraryId="/shadcn-ui/ui", query="accessible form patterns")
```

## 🖼️ Visual Verification (Web Apps)

After UI implementation, capture and analyze:

### Screenshot & Analyze
```
mcp_playwright_browser_navigate(url="http://localhost:8000/[page]")
mcp_playwright_browser_take_screenshot(filename="ui-check.png")

mcp_zai-mcp-server_analyze_image(
  image_path="ui-check.png",
  prompt="Check this UI for: design consistency, spacing, alignment, accessibility"
)
```

### Responsive Verification
```
mcp_playwright_browser_resize(width=375, height=812)   # Mobile
mcp_playwright_browser_resize(width=768, height=1024)  # Tablet  
mcp_playwright_browser_resize(width=1920, height=1080) # Desktop
```

## Instructions

1. Audit existing UI for patterns to follow
2. Use existing shadcn/ui components (see component map below)
3. Follow Tailwind design tokens, avoid custom CSS
4. Ensure accessibility (keyboard, labels, contrast)
5. Test responsive behavior (mobile + desktop)

## shadcn/ui Component Map

| Need | Component |
|------|-----------|
| Button | `<Button>` |
| Input | `<Input>` |
| Select | `<Select>` |
| Modal | `<Dialog>` |
| Dropdown | `<DropdownMenu>` |
| Toast | `<Toast>` |
| Card | `<Card>` |
| Alert | `<Alert>` |

## Design Tokens

### Colors
```tsx
text-foreground           // Primary text
text-muted-foreground     // Secondary text
bg-background             // Page background
bg-muted                  // Subtle background
border-border             // Default borders
```

### Spacing
```tsx
p-1 (4px)  p-2 (8px)  p-4 (16px)  p-6 (24px)  p-8 (32px)
```

## Responsive Breakpoints
| Prefix | Width | Device |
|--------|-------|--------|
| `sm:` | 640px | Phone |
| `md:` | 768px | Tablet |
| `lg:` | 1024px | Laptop |
| `xl:` | 1280px | Desktop |

## Accessibility Checklist (WCAG 2.1)

### Forms
- [ ] Inputs have `<Label>` with `htmlFor`
- [ ] Errors linked with `aria-describedby`
- [ ] Invalid state with `aria-invalid`

### Interactive
- [ ] Keyboard accessible
- [ ] Focus states visible
- [ ] Logical focus order

### Content
- [ ] Images have `alt` text
- [ ] 4.5:1 color contrast

## Form Pattern
```tsx
<Label htmlFor="name">Name</Label>
<Input
    id="name"
    aria-invalid={!!errors.name}
    aria-describedby={errors.name ? 'name-error' : undefined}
/>
{errors.name && (
    <p id="name-error" className="text-sm text-destructive">
        {errors.name}
    </p>
)}
```

## Rules
- ✅ Use existing components and tokens
- ✅ Follow `docs/code-standards.md`
- ✅ Implement loading/error states
- ❌ Don't create new colors/fonts
- ❌ Don't use inline styles
- ❌ Don't skip mobile responsiveness

## Examples
- "Improve a form's validation UX"
- "Adjust layout for readability"
