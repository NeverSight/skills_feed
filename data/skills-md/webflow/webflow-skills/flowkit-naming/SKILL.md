---
name: flowkit-naming
description: Apply Flowkit CSS naming system in Webflow. Use when creating classes, auditing existing naming, or building new components following Flowkit conventions. Flowkit is Webflow's official CSS framework with utility-first approach.
---

# Flowkit Naming System

Apply FlowKit CSS naming conventions in Webflow projects using Webflow Designer tools.

## Important Note

**ALWAYS use Webflow MCP tools for all operations:**
- Use Webflow MCP's `webflow_guide_tool` to get best practices before starting
- Use Webflow MCP's `data_sites_tool` with action `list_sites` to identify the target site
- Use Webflow MCP's `de_page_tool` to get current page and switch pages
- Use Webflow MCP's `element_tool` to select elements and inspect current classes
- Use Webflow MCP's `style_tool` to create and update FlowKit-compliant styles
- Use Webflow MCP's `de_learn_more_about_styles` to understand supported style properties
- DO NOT use any other tools or methods for Webflow operations
- All tool calls must include the required `context` parameter (15-25 words, third-person perspective)
- **Designer connection required**: User must be connected to Webflow Designer for this skill to work

## Instructions

### Phase 1: Discovery & Setup
1. **Identify the task**: Determine if user is:
   - Creating new component classes
   - Auditing existing class names
   - Building complete page sections
   - Refactoring non-FlowKit classes to FlowKit
2. **Connect to Designer**: Confirm user has Webflow Designer open and connected
3. **Get current page**: Use Webflow MCP's `de_page_tool` to identify current working page
4. **Ask for scope**: Clarify which elements or sections to work with

### Phase 2: Analysis (if auditing existing)
5. **Get all elements**: Use Webflow MCP's `element_tool` to retrieve current page elements
6. **Extract classes**: Identify all class names currently applied
7. **Categorize issues**:
   - Missing `fk-` prefix
   - Incorrect case (uppercase/mixed case)
   - Wrong separators (underscores instead of hyphens)
   - Non-semantic naming
   - Inconsistent component structure
8. **Generate audit report**: Show current vs suggested FlowKit-compliant names

### Phase 3: Suggestion Generation
9. **Apply FlowKit patterns**: Generate class names following FlowKit v2 conventions
10. **Structure by type**:
    - Component wrappers: `fk-[component]`
    - Child elements: `fk-[component]-[element]`
    - State modifiers: combo classes with `is-[state]`
    - Layout utilities: `fk-flex`, `fk-grid`, `fk-stack`
    - Spacing utilities: `fk-space-[size]`, `fk-py-[size]`, `fk-px-[size]`
    - Typography utilities: `fk-text-[style]`
11. **Validate suggestions**: Ensure all suggestions follow FlowKit conventions
12. **Show preview**: Display hierarchical structure with suggested classes

### Phase 4: Application (if user confirms)
13. **Create styles**: Use Webflow MCP's `style_tool` to create new FlowKit-compliant class styles
14. **Update elements**: Use Webflow MCP's `element_tool` to apply classes to elements
15. **Process in batches**: If many elements, process in groups of 10-15
16. **Show progress**: Display which elements are being updated

### Phase 5: Verification & Reporting
17. **Verify application**: Check that classes were applied correctly
18. **Generate report**: Show what was created/updated
19. **Provide documentation**: Explain the FlowKit structure used
20. **Suggest next steps**: Recommend additional FlowKit patterns to implement

## FlowKit Naming Reference

### Core Naming Patterns

| Pattern | Purpose | Example |
|---------|---------|---------|
| `fk-[component]` | Component wrapper (base class) | `fk-card`, `fk-nav`, `fk-hero` |
| `fk-[component]-[element]` | Child element within component | `fk-card-title`, `fk-nav-link` |
| `fk-[component].[modifier]` | Combo class modifier (state/variant) | `fk-card.is-featured` |
| `fk-text-[style]` | Typography utility | `fk-text-xl`, `fk-text-bold` |
| `fk-flex` / `fk-grid` | Layout utilities | `fk-flex-center`, `fk-grid-3` |
| `fk-space-[size]` | Spacing utilities | `fk-space-md`, `fk-py-lg` |
| `is-[state]` | State modifiers (combo) | `is-active`, `is-hidden`, `is-disabled` |

### Layout Utilities

```
fk-section              Section wrapper with padding
fk-container            Max-width container (centered)
fk-flex                 Flexbox container
fk-flex-center          Centered flex (both axes)
fk-flex-between         Space-between flex
fk-flex-around          Space-around flex
fk-flex-col             Flex column direction
fk-grid                 Grid container (base)
fk-grid-2               2-column grid
fk-grid-3               3-column grid
fk-grid-4               4-column grid
fk-grid-6               6-column grid
fk-stack                Vertical stack (gap between items)
fk-row                  Horizontal row
fk-wrap                 Flex wrap enabled
```

### Typography Utilities

```
fk-text-xs              Extra small text (12px)
fk-text-sm              Small text (14px)
fk-text-md              Medium text (16px - default)
fk-text-lg              Large text (18px)
fk-text-xl              Extra large text (24px)
fk-text-2xl             2x large text (32px)
fk-text-3xl             3x large text (48px)
fk-text-bold            Bold weight (700)
fk-text-semibold        Semibold weight (600)
fk-text-medium          Medium weight (500)
fk-text-light           Light weight (300)
fk-text-center          Center aligned
fk-text-left            Left aligned
fk-text-right           Right aligned
fk-text-uppercase       Uppercase transform
fk-text-lowercase       Lowercase transform
fk-text-capitalize      Capitalize transform
```

### Spacing Utilities

```
fk-space-xs             4px spacing
fk-space-sm             8px spacing
fk-space-md             16px spacing (default)
fk-space-lg             24px spacing
fk-space-xl             32px spacing
fk-space-2xl            48px spacing
fk-space-3xl            64px spacing

Directional Spacing:
fk-py-[size]            Padding vertical (top + bottom)
fk-px-[size]            Padding horizontal (left + right)
fk-pt-[size]            Padding top
fk-pb-[size]            Padding bottom
fk-pl-[size]            Padding left
fk-pr-[size]            Padding right

fk-my-[size]            Margin vertical (top + bottom)
fk-mx-[size]            Margin horizontal (left + right)
fk-mt-[size]            Margin top
fk-mb-[size]            Margin bottom
fk-ml-[size]            Margin left
fk-mr-[size]            Margin right
```

### Color Utilities

```
fk-bg-primary           Primary background color
fk-bg-secondary         Secondary background color
fk-bg-accent            Accent background color
fk-bg-light             Light background
fk-bg-dark              Dark background
fk-text-primary         Primary text color
fk-text-secondary       Secondary text color
fk-text-muted           Muted text color
```

### Border & Visual Utilities

```
fk-rounded              Border radius (default)
fk-rounded-sm           Small border radius
fk-rounded-lg           Large border radius
fk-rounded-full         Fully rounded (pill/circle)
fk-border               Border (1px solid)
fk-border-top           Border top only
fk-border-bottom        Border bottom only
fk-shadow               Box shadow (default)
fk-shadow-sm            Small shadow
fk-shadow-lg            Large shadow
```

### State Modifiers (Combo Classes)

```
is-active               Active state (navigation, tabs)
is-hidden               Hidden visibility
is-visible              Visible visibility
is-disabled             Disabled state
is-loading              Loading state
is-error                Error state
is-success              Success state
is-primary              Primary variant
is-secondary            Secondary variant
is-featured             Featured/highlighted variant
is-horizontal           Horizontal layout variant
is-vertical             Vertical layout variant
```

## Examples

### Example 1: Creating Hero Section

**User prompt:**
```
Build a hero section with FlowKit naming
```

**Step 1: Analysis**
```
🎨 FlowKit Hero Section Structure

I'll create a hero section following FlowKit v2 conventions.

Structure:
fk-section (wrapper with padding)
└── fk-container (max-width container)
    └── fk-hero (component wrapper)
        ├── fk-hero-content + fk-flex + fk-flex-col + fk-flex-center
        │   ├── fk-hero-eyebrow + fk-text-sm + fk-text-uppercase + fk-mb-sm
        │   ├── fk-hero-title + fk-text-3xl + fk-text-bold + fk-mb-md
        │   ├── fk-hero-subtitle + fk-text-lg + fk-text-muted + fk-mb-lg
        │   └── fk-hero-actions + fk-flex + fk-space-md
        │       ├── fk-button.is-primary
        │       └── fk-button.is-secondary
        └── fk-hero-image + fk-rounded-lg

Total classes to create: 12 base classes + 2 combo classes
Ready to create these in Webflow Designer? (yes/no)
```

**Step 2: After user confirms**
```
🔄 Creating FlowKit Hero Classes...

Progress: ████████████████████ 100% (14/14 classes)

✅ Classes Created:

**Layout Classes:**
- ✅ fk-section - Section wrapper with padding
- ✅ fk-container - Max-width container
- ✅ fk-hero - Hero component wrapper

**Element Classes:**
- ✅ fk-hero-content - Hero content container
- ✅ fk-hero-eyebrow - Small label above title
- ✅ fk-hero-title - Main hero heading
- ✅ fk-hero-subtitle - Supporting text
- ✅ fk-hero-actions - Button container
- ✅ fk-hero-image - Hero image wrapper

**Utility Classes:**
- ✅ fk-flex, fk-flex-col, fk-flex-center
- ✅ fk-text-sm, fk-text-lg, fk-text-3xl
- ✅ fk-text-uppercase, fk-text-bold, fk-text-muted
- ✅ fk-mb-sm, fk-mb-md, fk-mb-lg
- ✅ fk-space-md, fk-rounded-lg

**Component Classes:**
- ✅ fk-button (with combo classes: is-primary, is-secondary)

---

📋 Usage Guide:

1. Create a Section element → Apply `fk-section`
2. Add Container inside → Apply `fk-container`
3. Add Div inside → Apply `fk-hero`
4. Build content structure following the hierarchy above
5. Use combo classes for button variants: `fk-button.is-primary`

🎉 Your FlowKit hero section structure is ready!
```

### Example 2: Auditing Existing Classes

**User prompt:**
```
Check these classes: feature-card, FK-Button, fk_hero_title, cardTitle
```

**Response:**
```
📋 FlowKit Audit Report

Checking 4 classes against FlowKit v2 conventions...

---

## Issues Found: 4

### 1. `feature-card` ⚠️
**Issue:** Missing FlowKit prefix
**Reason:** All FlowKit classes must start with `fk-`
**Suggested:** `fk-feature-card` or `fk-card.is-feature`
**Fix:** Rename class to include `fk-` prefix

### 2. `FK-Button` ❌
**Issue:** Incorrect case (uppercase)
**Reason:** FlowKit uses lowercase only
**Suggested:** `fk-button`
**Fix:** Convert to lowercase: `fk-button`

### 3. `fk_hero_title` ❌
**Issue:** Wrong separator (underscore)
**Reason:** FlowKit uses hyphens, not underscores
**Suggested:** `fk-hero-title`
**Fix:** Replace underscores with hyphens

### 4. `cardTitle` ❌
**Issue:** Multiple violations
  - Missing `fk-` prefix
  - CamelCase instead of kebab-case
**Reason:** FlowKit requires `fk-` prefix and hyphen separation
**Suggested:** `fk-card-title`
**Fix:** Add prefix and convert to kebab-case

---

## FlowKit Naming Rules:

✅ **Correct patterns:**
- `fk-card` (component)
- `fk-card-title` (element)
- `fk-button.is-primary` (with modifier)
- `fk-text-xl` (utility)

❌ **Incorrect patterns:**
- `card` (no prefix)
- `FK-Card` (wrong case)
- `fk_card` (wrong separator)
- `cardTitle` (camelCase)

Would you like me to rename these classes in Webflow Designer? (yes/no)
```

### Example 3: Building Card Component

**User prompt:**
```
Create a product card component with FlowKit classes
```

**Response:**
```
🎨 FlowKit Product Card Component

Structure:
fk-card (base component)
├── fk-card-image-wrapper
│   └── fk-card-image + fk-rounded-lg
├── fk-card-badge + fk-text-xs + fk-text-uppercase + fk-bg-accent
├── fk-card-content + fk-space-md
│   ├── fk-card-category + fk-text-sm + fk-text-muted
│   ├── fk-card-title + fk-text-lg + fk-text-bold
│   ├── fk-card-description + fk-text-md
│   └── fk-card-price + fk-text-xl + fk-text-bold + fk-text-primary
└── fk-card-footer + fk-flex + fk-flex-between + fk-pt-md + fk-border-top
    ├── fk-card-rating + fk-flex + fk-space-xs
    └── fk-button.is-primary + fk-text-sm

---

## Variants (Combo Classes):

### Featured Card
`fk-card.is-featured`
- Highlighted border/shadow
- Accent background
- Use for promoted products

### Horizontal Layout
`fk-card.is-horizontal`
- Side-by-side image/content
- Better for list views
- Image on left, content on right

### Compact Size
`fk-card.is-compact`
- Reduced padding
- Smaller text sizes
- Use in tight layouts

---

## Responsive Modifiers:

Desktop (default):
- `fk-grid-3` (3 cards per row)

Tablet:
- Add combo: `fk-grid-3.tablet-2`

Mobile:
- Add combo: `fk-grid-3.tablet-2.mobile-1`

---

Ready to create these classes? (yes/no)
```

### Example 4: Refactoring to FlowKit

**User prompt:**
```
Refactor my navigation to use FlowKit naming
```

**Step 1: Current Analysis**
```
🔍 Analyzing Current Navigation Classes...

Found 8 elements with non-FlowKit classes:
├── navbar → fk-nav
├── navbar-container → fk-nav-container
├── logo-wrapper → fk-nav-logo
├── menu → fk-nav-menu
├── menu-item → fk-nav-link
├── menu-item active → fk-nav-link.is-active
├── button-group → fk-nav-actions
└── btn-primary → fk-button.is-primary

---

## Migration Plan:

**Phase 1: Create FlowKit Classes** (8 classes)
- Create all `fk-nav-*` classes
- Create utility classes: `fk-flex`, `fk-flex-between`, `fk-flex-center`
- Create `fk-button` with `is-primary` modifier

**Phase 2: Update Elements** (8 elements)
- Replace old classes with new FlowKit classes
- Apply combo classes where needed
- Preserve existing styles

**Phase 3: Cleanup** (optional)
- Old classes can be removed after verification
- Keep for now to maintain backwards compatibility

---

Proceed with migration? (yes/no)
```

**Step 2: After Migration**
```
✅ Navigation Refactored to FlowKit

**Classes Created:** 8
**Elements Updated:** 8
**Time elapsed:** ~3 seconds

---

## Updated Structure:

fk-nav
├── fk-nav-container + fk-flex + fk-flex-between
│   ├── fk-nav-logo
│   ├── fk-nav-menu + fk-flex + fk-flex-center + fk-space-md
│   │   ├── fk-nav-link (x5)
│   │   └── fk-nav-link.is-active (current page)
│   └── fk-nav-actions + fk-flex + fk-space-sm
│       ├── fk-button.is-secondary
│       └── fk-button.is-primary

---

## Before → After:

| Old Class | New FlowKit Class |
|-----------|-------------------|
| navbar | fk-nav ✅ |
| navbar-container | fk-nav-container ✅ |
| logo-wrapper | fk-nav-logo ✅ |
| menu | fk-nav-menu ✅ |
| menu-item | fk-nav-link ✅ |
| menu-item active | fk-nav-link.is-active ✅ |
| button-group | fk-nav-actions ✅ |
| btn-primary | fk-button.is-primary ✅ |

---

🎉 Navigation is now FlowKit compliant!

**Next steps:**
- Test navigation on all breakpoints
- Verify active states work correctly
- Consider adding `fk-nav.is-transparent` for transparent header variant
- Consider adding `fk-nav.is-sticky` for sticky navigation
```

## Guidelines

### Phase 1: Critical Requirements

**FlowKit Prefix Rule:**
- ALL component and element classes MUST start with `fk-`
- Exception: State modifiers use `is-` prefix (as combo classes)
- Exception: Utility classes for third-party integrations may omit prefix

**Case Sensitivity:**
- All class names are lowercase only
- No uppercase letters anywhere
- No camelCase or PascalCase

**Separator Rule:**
- Use hyphens (`-`) to separate words
- Never use underscores (`_`)
- Never use spaces or special characters

**Naming Structure:**
```
Component:        fk-[component]
Element:          fk-[component]-[element]
Sub-element:      fk-[component]-[element]-[detail]
Utility:          fk-[property]-[value]
State modifier:   is-[state] (combo class only)
Responsive:       .[breakpoint]-[value] (combo class)
```

### Phase 2: Component Naming Rules

**Component Names:**
- Keep concise and semantic
- Use common web component terms: `card`, `nav`, `hero`, `footer`
- Avoid overly specific names: prefer `fk-card` over `fk-product-feature-card`
- Use modifiers for variants: `fk-card.is-featured` not `fk-card-featured`

**Element Hierarchy:**
- Parent component: `fk-card`
- Direct children: `fk-card-[element]` (e.g., `fk-card-title`)
- Deep nesting: Avoid more than 3 levels
- Bad: `fk-card-content-section-text-wrapper`
- Good: `fk-card-content`, `fk-card-text`

**Common Component Patterns:**

**Cards:**
```
fk-card
├── fk-card-image
├── fk-card-content
│   ├── fk-card-title
│   └── fk-card-text
└── fk-card-footer
```

**Navigation:**
```
fk-nav
├── fk-nav-logo
├── fk-nav-menu
│   └── fk-nav-link
└── fk-nav-actions
```

**Hero:**
```
fk-hero
├── fk-hero-content
│   ├── fk-hero-title
│   ├── fk-hero-subtitle
│   └── fk-hero-actions
└── fk-hero-media
```

**Forms:**
```
fk-form
├── fk-form-group
│   ├── fk-form-label
│   └── fk-form-input
└── fk-form-actions
```

### Phase 3: Utility Classes

**Utility Naming:**
- Format: `fk-[property]-[value]`
- Examples: `fk-text-lg`, `fk-space-md`, `fk-grid-3`

**Spacing Utilities:**
- Use t-shirt sizing: `xs`, `sm`, `md`, `lg`, `xl`, `2xl`, `3xl`
- Directional: `py` (vertical), `px` (horizontal), `pt` (top), `pr` (right), `pb` (bottom), `pl` (left)
- Same for margins: `my`, `mx`, `mt`, `mr`, `mb`, `ml`

**Typography Utilities:**
- Size: `fk-text-[xs|sm|md|lg|xl|2xl|3xl]`
- Weight: `fk-text-[light|medium|semibold|bold]`
- Alignment: `fk-text-[left|center|right]`
- Transform: `fk-text-[uppercase|lowercase|capitalize]`

**Layout Utilities:**
- Flexbox: `fk-flex`, `fk-flex-col`, `fk-flex-center`, `fk-flex-between`
- Grid: `fk-grid`, `fk-grid-2`, `fk-grid-3`, `fk-grid-4`, `fk-grid-6`
- Container: `fk-container`, `fk-section`

### Phase 4: State Modifiers (Combo Classes)

**State Modifier Rules:**
- Always use as combo classes with `is-` prefix
- Applied in addition to base class
- Example: `<div class="fk-button is-primary">...</div>`

**Common States:**
```
is-active           Currently active/selected
is-disabled         Disabled interaction
is-hidden           Hidden visibility
is-visible          Visible (override hidden)
is-loading          Loading state
is-error            Error state
is-success          Success state
is-primary          Primary variant
is-secondary        Secondary variant
is-tertiary         Tertiary variant
is-featured         Featured/highlighted
is-horizontal       Horizontal layout
is-vertical         Vertical layout
is-expanded         Expanded state (accordions, dropdowns)
is-collapsed        Collapsed state
```

**Applying Combo Classes in Webflow:**
1. Select element
2. Add base class: `fk-button`
3. Add combo class: `is-primary`
4. Element has both classes: `fk-button is-primary`
5. Style the combo: `.fk-button.is-primary { ... }`

### Phase 5: Responsive Design

**Responsive Modifiers:**
- FlowKit uses combo classes for responsive behavior
- Format: `.[breakpoint]-[value]`
- Example: `fk-grid-4.tablet-2.mobile-1`

**Breakpoints:**
```
Desktop (default):   No modifier needed
Tablet:              .tablet-[value]
Mobile:              .mobile-[value]
```

**Responsive Grid Example:**
```
Base: fk-grid-4 (4 columns on desktop)
+ Combo: .tablet-2 (2 columns on tablet)
+ Combo: .mobile-1 (1 column on mobile)

Result: <div class="fk-grid-4 tablet-2 mobile-1">
```

**Responsive Text Example:**
```
Base: fk-text-3xl (48px on desktop)
+ Combo: .tablet-2xl (32px on tablet)
+ Combo: .mobile-xl (24px on mobile)

Result: <div class="fk-text-3xl tablet-2xl mobile-xl">
```

### Phase 6: Best Practices

**Always:**
- ✅ Use `fk-` prefix for all components and elements
- ✅ Use hyphens to separate words
- ✅ Use lowercase only
- ✅ Keep component names semantic and concise
- ✅ Use combo classes for modifiers and states
- ✅ Combine utilities freely (`fk-flex fk-flex-center fk-space-md`)
- ✅ Follow component-element hierarchy
- ✅ Use responsive combo classes for breakpoints

**Never:**
- ❌ Omit `fk-` prefix from components
- ❌ Use underscores or spaces
- ❌ Use uppercase or camelCase
- ❌ Create overly specific class names
- ❌ Nest elements more than 3 levels deep
- ❌ Mix FlowKit with other naming systems
- ❌ Create standalone modifier classes (use combo classes)

**Component vs Utility:**

Use **components** when:
- Building reusable UI patterns (cards, buttons, navigation)
- Need semantic meaning
- Multiple instances across site
- Example: `fk-card`, `fk-nav`, `fk-hero`

Use **utilities** when:
- Applying single-purpose styling (spacing, typography, layout)
- Quick adjustments without new classes
- Consistent spacing/sizing across site
- Example: `fk-text-lg`, `fk-space-md`, `fk-flex-center`

**Utility Stacking:**
Utilities can be freely combined:
```html
<div class="fk-flex fk-flex-center fk-space-md fk-py-lg">
  Content
</div>
```

**Component + Utility Combo:**
```html
<div class="fk-card fk-shadow-lg fk-rounded-lg">
  <div class="fk-card-content fk-space-lg">
    <h3 class="fk-card-title fk-text-xl fk-text-bold">Title</h3>
  </div>
</div>
```

### Phase 7: Common Mistakes & Fixes

**Mistake 1: Missing Prefix**
```
❌ card, button, nav
✅ fk-card, fk-button, fk-nav
```

**Mistake 2: Wrong Case**
```
❌ FK-Card, fk-Button, Fk-nav
✅ fk-card, fk-button, fk-nav
```

**Mistake 3: Wrong Separator**
```
❌ fk_card_title, fk.card.title
✅ fk-card-title
```

**Mistake 4: camelCase/PascalCase**
```
❌ fkCardTitle, FkCardTitle
✅ fk-card-title
```

**Mistake 5: Modifier as Standalone Class**
```
❌ <div class="fk-button-primary">
✅ <div class="fk-button is-primary">
```

**Mistake 6: Too Much Nesting**
```
❌ fk-hero-content-wrapper-section-title-text
✅ fk-hero-content, fk-hero-title
```

**Mistake 7: Overly Specific Names**
```
❌ fk-product-feature-card-with-image-and-price
✅ fk-card (use combo: is-product)
```

**Mistake 8: Wrong Responsive Pattern**
```
❌ fk-grid-3-tablet-2 (single class)
✅ fk-grid-3 tablet-2 (two classes)
```

### Phase 8: FlowKit Version Notes

**FlowKit v2 (Current):**
- New naming conventions (documented here)
- Enhanced grid system with responsive combos
- Expanded utility collection
- Improved component library
- Better variable system

**Key v2 Changes:**
- Standardized `fk-` prefix across all components
- Introduced `is-` prefix for state modifiers (combo classes)
- Added responsive combo classes (`.tablet-`, `.mobile-`)
- Expanded spacing scale (xs to 3xl)
- More semantic utility names

**Migration from v1:**
If user has v1 FlowKit classes:
1. Add `fk-` prefix where missing
2. Convert modifiers to `is-` combo classes
3. Update responsive classes to combo format
4. Check spacing utilities for new scale

### Phase 9: Performance Optimization

**Class Creation:**
- Create base component classes first
- Then create element classes
- Finally create utility classes
- Use `style_tool` in batches of 10-15 classes

**Element Updates:**
- Process elements in groups of 10-15
- Show progress for large batches
- If >50 elements, ask user to confirm batch size

**Designer Connection:**
- Always verify Designer connection before starting
- If connection lost, pause and ask user to reconnect
- Save progress between batches

### Phase 10: Error Handling

**Common Errors:**

**1. Designer Not Connected:**
```
❌ Error: Cannot create classes - Designer not connected

Solution:
1. Open Webflow Designer
2. Open the target site
3. Connect to Designer in Claude Code
4. Retry operation
```

**2. Class Already Exists:**
```
⚠️ Warning: Class 'fk-button' already exists

Options:
1. Skip creation (use existing)
2. Update existing class
3. Create with different name
```

**3. Invalid Class Name:**
```
❌ Error: Class name 'fk-My Button' is invalid

Issues:
- Contains spaces
- Contains uppercase

Suggested: 'fk-my-button'
```

**4. Style Property Not Supported:**
```
⚠️ Warning: Property 'custom-property' not supported

This may be:
- Custom CSS property
- Webflow doesn't support via Designer API
- Typo in property name

Recommendation: Apply manually in Designer
```

## Edge Cases

**Case 1: Third-Party Integration Classes**
If integrating with third-party libraries (e.g., animations, sliders):
- Keep third-party classes separate
- Add FlowKit wrapper: `<div class="fk-slider"><div class="swiper">...</div></div>`
- Don't force FlowKit naming on third-party classes

**Case 2: Legacy Code Migration**
When migrating large existing site:
- Create FlowKit classes first
- Apply to new sections
- Gradually refactor old sections
- Keep both systems temporarily for backwards compatibility

**Case 3: Custom Naming Requirements**
If client has existing naming system:
- Discuss FlowKit benefits
- Show side-by-side comparison
- Offer hybrid approach: FlowKit for new components, keep old for existing
- Or fully refactor (more time, better long-term)

**Case 4: Component Library Conflicts**
If site uses another framework (Bootstrap, Tailwind):
- FlowKit can coexist but not recommended
- Choose one primary system
- Use FlowKit for custom components
- Use other framework for pre-built components

**Case 5: Utility Class Explosion**
If too many utility classes on single element:
- Consider creating component class instead
- Example: Instead of `fk-flex fk-flex-center fk-space-md fk-py-lg fk-px-xl fk-rounded-lg fk-shadow`
- Create: `fk-panel` with those properties built-in

## Production Checklist

Before considering FlowKit implementation complete:

**Setup:**
- [ ] Webflow Designer connected
- [ ] Target site identified
- [ ] Current page confirmed
- [ ] Scope defined with user

**Component Structure:**
- [ ] All components use `fk-` prefix
- [ ] Component hierarchy is logical (max 3 levels)
- [ ] Element names are semantic
- [ ] Modifiers use combo classes with `is-` prefix

**Utilities:**
- [ ] Spacing utilities use t-shirt sizing (xs-3xl)
- [ ] Typography utilities cover all text styles
- [ ] Layout utilities handle flex/grid needs
- [ ] Color utilities align with brand

**Responsive:**
- [ ] Responsive combo classes defined for key components
- [ ] Breakpoint modifiers tested (tablet, mobile)
- [ ] Grid systems adapt properly

**States:**
- [ ] State modifiers defined (is-active, is-disabled, etc.)
- [ ] Hover/focus states work correctly
- [ ] Active states styled properly

**Documentation:**
- [ ] Component structure documented
- [ ] Utility classes listed
- [ ] Responsive behavior explained
- [ ] State modifiers documented

**Validation:**
- [ ] All classes follow naming conventions
- [ ] No uppercase letters
- [ ] No underscores
- [ ] All have proper prefixes

**Performance:**
- [ ] Classes created in batches
- [ ] Progress shown for large operations
- [ ] No duplicate classes created

**User Experience:**
- [ ] Clear feedback provided
- [ ] Progress indicators shown
- [ ] Success confirmation given
- [ ] Next steps recommended
