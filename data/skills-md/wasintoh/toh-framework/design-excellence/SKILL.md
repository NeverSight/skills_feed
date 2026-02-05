---
name: design-excellence
description: >
  Design system and anti-patterns for professional UI. Ensures apps don't look 
  "AI generated". Defines color palettes, typography, spacing, animations, and 
  common anti-patterns to avoid. Used by Design Reviewer sub-agent to polish UI.
  Triggers: design review, polish UI, improve aesthetics, looks like AI made it,
  design system, style guide, make it beautiful.
---

# Design Excellence

Make AI-built apps look human-crafted. No generic templates. No obvious patterns.

<core_principle>
## The Craft Standard

If someone can tell it was AI-generated, we failed.

Good design is invisible. Users should feel the app is professional,
not notice it follows a template.
</core_principle>

<color_system>
## Color Philosophy

### The Problem with AI Color Choices
AI tends to pick:
- Purple gradients on white (Lovable default look)
- Overly saturated accent colors
- Too many colors in one interface
- Gradients where solid colors work better

### Our Approach: Restraint

**Base Palette (Default)**
```css
/* Use Tailwind's slate scale for neutrals */
--background: slate-50       /* Page background */
--surface: white             /* Cards, modals */
--border: slate-200          /* Dividers, borders */
--text-primary: slate-900    /* Headlines */
--text-secondary: slate-600  /* Body text */
--text-muted: slate-400      /* Placeholders, hints */
```

**Accent Colors (Pick ONE per app)**
```css
/* Default: Blue (professional, trustworthy) */
--accent: blue-600
--accent-hover: blue-700
--accent-light: blue-50

/* Alternative by app type: */
/* Finance/Banking → Green (money) */
/* Health/Wellness → Teal (calm) */
/* Food/Restaurant → Orange (appetite) */
/* Creative/Design → Purple (creativity) */
/* Urgent/Alert → Red (attention) */
```

**Rules**
1. ONE accent color per app, no exceptions
2. Use accent sparingly - buttons, links, highlights only
3. Never gradient on primary buttons
4. Background is white or near-white, not colored
5. Dark mode: invert properly, don't just make it gray
</color_system>

<typography_system>
## Typography Rules

### The Font Stack
```css
/* Don't specify Inter everywhere - use system fonts */
font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 
  "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;

/* This looks native on every platform */
```

### Type Scale (Tailwind classes)
```
Page Title:     text-2xl font-semibold   (24px)
Section Title:  text-lg font-medium      (18px)
Card Title:     text-base font-medium    (16px)
Body:           text-sm                  (14px)
Small/Caption:  text-xs text-slate-500   (12px)
```

### Anti-Patterns
❌ Don't use `font-bold` on everything
❌ Don't mix too many font sizes in one card
❌ Don't use ALL CAPS for long text
❌ Don't center-align body paragraphs
❌ Don't use pure black (#000) - use slate-900

### Good Patterns
✅ Headlines: semibold or medium, never regular
✅ Body: regular weight, good line-height (1.5-1.6)
✅ Keep hierarchy: max 3 sizes per component
✅ Left-align most text (except headings in centered layouts)
</typography_system>

<spacing_system>
## Spacing & Layout

### Spacing Scale
Use Tailwind's default scale consistently:
```
4   (1rem/16px)  - Small gaps, inline elements
6   (1.5rem/24px) - Medium gaps, between components
8   (2rem/32px)  - Large gaps, between sections
12  (3rem/48px)  - XL gaps, page sections
```

### Page Layout
```tsx
// Standard page container
<div className="p-4 md:p-6 lg:p-8">
  {/* Page title */}
  <h1 className="text-2xl font-semibold mb-6">Dashboard</h1>
  
  {/* Content sections with consistent spacing */}
  <section className="mb-8">
    {/* Section content */}
  </section>
</div>
```

### Card Internal Spacing
```tsx
<Card>
  <CardHeader className="pb-4">  {/* Reduce default padding */}
    <CardTitle>Title</CardTitle>
  </CardHeader>
  <CardContent className="space-y-4">
    {/* Content with vertical gaps */}
  </CardContent>
</Card>
```

### Anti-Patterns
❌ Inconsistent padding (p-3 here, p-5 there)
❌ Too little whitespace (cramped feel)
❌ Too much whitespace (disconnected feel)
❌ Different gap sizes for same-level elements
</spacing_system>

<animation_system>
## Motion & Animation

### Philosophy
Animation should:
- Feel natural, not flashy
- Provide feedback, not distraction
- Be fast (150-300ms), not slow
- Be subtle, not dramatic

### Standard Transitions
```tsx
// Hover states - use transition-colors or transition-all
<div className="transition-colors hover:bg-slate-50">

// Card hover - subtle lift
<Card className="transition-shadow hover:shadow-md">

// Button hover - built into shadcn, don't override
<Button>Already animated</Button>
```

### Framer Motion Patterns
```tsx
// Page transitions
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.3 }}
>

// List stagger
<motion.div
  variants={{
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: { staggerChildren: 0.1 }
    }
  }}
  initial="hidden"
  animate="show"
>
  {items.map(item => (
    <motion.div
      key={item.id}
      variants={{
        hidden: { opacity: 0, y: 20 },
        show: { opacity: 1, y: 0 }
      }}
    >
      {item.content}
    </motion.div>
  ))}
</motion.div>

// Micro-interaction - button tap
<motion.button whileTap={{ scale: 0.98 }}>
  Click me
</motion.button>
```

### Animation Timing
- Hover effects: 150ms
- Small transitions: 200ms
- Page transitions: 300ms
- Complex animations: 400-500ms max

### Anti-Patterns
❌ Bounce effects (feels cheap)
❌ Slow animations (>500ms feels sluggish)
❌ Animation on every element (overwhelming)
❌ Spinning loaders everywhere (use skeleton instead)
❌ Dramatic entrance animations
</animation_system>

<component_patterns>
## Component Design Patterns

### Cards
```tsx
// Clean card - no excessive decoration
<Card className="bg-white border shadow-sm">
  <CardContent className="p-4">
    {/* Content */}
  </CardContent>
</Card>

// DO NOT: rounded-3xl, heavy shadows, gradient borders
```

### Buttons
```tsx
// Primary action
<Button>Save</Button>

// Secondary action
<Button variant="outline">Cancel</Button>

// Destructive action
<Button variant="destructive">Delete</Button>

// Icon button
<Button variant="ghost" size="icon">
  <Settings className="h-4 w-4" />
</Button>

// DO NOT: gradient buttons, 3D effects, icons in primary buttons (usually)
```

### Forms
```tsx
// Clean form layout
<div className="space-y-4">
  <div className="space-y-2">
    <Label>Name</Label>
    <Input placeholder="Enter name" />
  </div>
  
  <div className="space-y-2">
    <Label>Email</Label>
    <Input type="email" placeholder="email@example.com" />
  </div>
</div>

// DO NOT: inline labels, floating labels (unless requested), icons inside inputs
```

### Tables
```tsx
// Clean table
<Table>
  <TableHeader>
    <TableRow className="bg-slate-50">
      <TableHead>Name</TableHead>
      <TableHead>Status</TableHead>
      <TableHead className="text-right">Actions</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    <TableRow className="hover:bg-slate-50">
      <TableCell>John Smith</TableCell>
      <TableCell><Badge>Active</Badge></TableCell>
      <TableCell className="text-right">
        <Button variant="ghost" size="sm">Edit</Button>
      </TableCell>
    </TableRow>
  </TableBody>
</Table>

// DO NOT: zebra stripes (outdated), heavy borders, centered content
```
</component_patterns>

<anti_patterns_detail>
## AI-Generated Red Flags

### The "Lovable Look" (Avoid)
- Purple/violet as primary color
- Gradient backgrounds on white cards
- Rounded-3xl on everything
- Emoji in headers
- "Welcome back, User! 👋"
- Generic stock-photo-style illustrations

### The "Bootstrap Look" (Avoid)
- Heavy drop shadows
- Rounded pill buttons
- Blue links on everything
- Card decks with equal heights
- Jumbotron-style headers

### The "Material Look" (Avoid, unless requested)
- Floating action buttons
- Raised cards everywhere
- Ripple effects on everything
- Hamburger menu on desktop

### What Makes It Look "Human-Made"

1. **Restraint** - Not every feature is highlighted
2. **Hierarchy** - Clear primary, secondary, tertiary
3. **Whitespace** - Room to breathe
4. **Consistency** - Same patterns repeated
5. **Subtle details** - Tiny touches that don't scream
6. **Real content** - No placeholder text visible
</anti_patterns_detail>

<review_checklist>
## Design Review Checklist

### Color Check
- [ ] Only ONE accent color used
- [ ] No gradients on white backgrounds
- [ ] No pure black text
- [ ] Sufficient contrast for accessibility

### Typography Check
- [ ] Max 3 font sizes per component
- [ ] Proper hierarchy (semibold titles, regular body)
- [ ] No ALL CAPS paragraphs
- [ ] Line height is readable (1.5+)

### Spacing Check
- [ ] Consistent padding throughout
- [ ] Enough whitespace between sections
- [ ] Content doesn't feel cramped
- [ ] Mobile spacing is proportional

### Animation Check
- [ ] Transitions are subtle (150-300ms)
- [ ] No bounce/spring effects
- [ ] Loading uses skeleton, not spinner
- [ ] Hover states provide feedback

### Component Check
- [ ] Cards don't have excessive decoration
- [ ] Buttons follow hierarchy (primary/secondary)
- [ ] Forms are cleanly laid out
- [ ] Tables are readable and interactive

### Final Check
- [ ] Would a user know this is AI-made? (Should be NO)
- [ ] Does it look like a real product? (Should be YES)
- [ ] Is it consistent with modern SaaS apps? (Should be YES)
</review_checklist>
