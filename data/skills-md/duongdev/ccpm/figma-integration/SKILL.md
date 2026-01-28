---
name: figma-integration
description: Guides design-to-code workflow using Figma integration. Helps extract designs, analyze components, and generate implementation specs. Auto-activates when users mention Figma URLs, design implementation, component conversion, or design-to-code workflows. Works with /ccpm:plan, design-approve, design-refine, and /ccpm:figma-refresh commands.
---

# Figma Integration Skill

Transform Figma designs into implementation-ready specifications with CCPM's design-to-code workflow.

## When This Skill Activates

This skill auto-activates when:

- User mentions **"Figma"** or **"design"** in implementation context
- User asks about **"component"**, **"design system"**, or **"design tokens"**
- Running **`/ccpm:plan`** (starts design process)
- Running **`/ccpm:plan`** (refine designs)
- Running **`/ccpm:plan`** (generate specs)
- Running **`/ccpm:figma-refresh`** (refresh cached designs)
- User mentions **"design-to-code"**, **"design file"**, or **"Figma component"**

## The Figma Workflow

### Phase 1: Design Phase

**Command**: `/ccpm:plan ISSUE-ID`

Start the design process by attaching Figma links to your Linear issue:

```
1. Create/update Linear issue with task description
2. Attach Figma design link in issue description
3. Run /ccpm:plan TASK-123
4. CCPM extracts design metadata and creates options
```

**What happens**:
- Detects Figma links from issue and related documents
- Analyzes design file metadata (frames, components, assets)
- Extracts design tokens (colors, typography, spacing)
- Creates visual options or wireframes
- Caches design data for instant access

**Example**:
```
/ccpm:plan PSN-123

✅ Detected Figma link: https://figma.com/file/ABC123/UserDashboard
📦 Design Analysis:
   - 12 frames found
   - 15 components detected
   - Color palette: 8 colors
   - Typography: 4 font families
   - Spacing pattern: 4px, 8px, 16px grid

Ready for design review. Run: /ccpm:plan PSN-123
```

### Phase 2: Refinement Phase

**Command**: `/ccpm:plan ISSUE-ID [OPTION] [FEEDBACK]`

Iterate on designs based on feedback:

```
1. Review design options from Phase 1
2. Provide feedback or request changes
3. Run /ccpm:plan TASK-123 "feedback"
4. CCPM creates refined design options
```

**What happens**:
- Analyzes your feedback
- Generates refined design variations
- Adjusts colors, layout, or components
- Updates design cache with new versions
- Shows side-by-side comparisons

**Example**:
```
/ccpm:plan PSN-123 1 "Make the buttons larger, use primary color"

🎨 Refining Design Option 1...

Changes applied:
- Button height: 36px → 44px
- Button color: #6366F1 → primary color
- Button spacing: 12px → 16px

Preview: [design-option-1-v2]

Ready for approval? Run: /ccpm:plan PSN-123 1
```

### Phase 3: Approval & Spec Generation

**Command**: `/ccpm:plan ISSUE-ID OPTION-NUMBER`

Approve final design and generate implementation specifications:

```
1. Review refined design options
2. Choose best option
3. Run /ccpm:plan TASK-123 1
4. CCPM generates comprehensive specs
```

**What happens**:
- Locks design as final reference
- Extracts component specifications
- Generates implementation specs with:
  - Component breakdown
  - Props and state recommendations
  - Styling specifications
  - Accessibility guidelines
  - Responsive design rules
- Creates Linear Document with specs
- Updates issue description with spec link

**Example**:
```
/ccpm:plan PSN-123 1

✅ Design Approved!

Generated Implementation Specs:
📄 Component Specifications
📄 Styling Guidelines
📄 Responsive Rules
📄 Accessibility Checklist

Specs saved to: https://linear.app/doc/ABC123
Ready for implementation!
```

### Phase 4: Cache Management

**Command**: `/ccpm:figma-refresh ISSUE-ID`

Refresh cached design data when designs change:

```
1. Update Figma designs
2. Run /ccpm:figma-refresh TASK-123
3. CCPM re-extracts design data
4. Cache is updated with latest designs
```

**When to refresh**:
- Design significantly changed
- New components added to Figma
- Colors or typography updated
- Design tokens modified
- Last refresh was >1 hour ago (cache TTL)

## Design Analysis Deep Dive

### What CCPM Extracts From Figma

**Component Structure**:
```
Dashboard
├── Header
│   ├── Logo
│   ├── Navigation
│   └── UserMenu
├── Sidebar
│   ├── NavItems
│   └── UserProfile
└── MainContent
    ├── Cards
    └── Charts
```

**Design Tokens**:
- Color palette with hex/RGB values
- Typography: font families, sizes, weights
- Spacing: margin, padding, gap values
- Shadows and effects
- Border radius patterns

**Component Metadata**:
- Frame dimensions (width, height)
- Layout type (flex, grid, auto)
- Constraints and responsive behavior
- Text content and styles
- Image assets and sizing

### Component Detection

CCPM automatically identifies:

1. **UI Components**: Buttons, inputs, cards, modals, etc.
2. **Layout Components**: Headers, sidebars, grids, etc.
3. **Screens/Pages**: Full page layouts with multiple components
4. **Variants**: Different states (hover, active, disabled)
5. **Assets**: Icons, images, and design patterns

**Example detection**:
```
Frame: "Button / Primary / Large"
├── Detection: UI Component (Button)
├── Style: Primary (blue)
├── Size: Large (44px height)
├── State: Default
└── Variations: [Hover, Active, Disabled]
```

## Implementation Specification Generation

### What Gets Generated

When you approve a design, CCPM creates specs including:

**1. Component Definition**
```
Component: PrimaryButton
Props:
  - label: string (required)
  - size: "sm" | "md" | "lg" (default: "md")
  - disabled: boolean (default: false)
  - onClick: () => void
  - icon?: React.ReactNode

State:
  - loading: boolean
  - hover: boolean
  - focus: boolean
```

**2. Visual Specifications**
```
Sizing:
  - Small: 32px height
  - Medium: 40px height
  - Large: 44px height

Spacing:
  - Horizontal padding: 16px
  - Vertical padding: 8px

Typography:
  - Font: Inter
  - Weight: 600 (semibold)
  - Size: 14px

Colors:
  - Background: #6366F1
  - Text: #FFFFFF
  - Hover: #4F46E5
```

**3. Responsive Rules**
```
Breakpoints:
  - Mobile (< 768px): Single column
  - Tablet (768px - 1024px): Two columns
  - Desktop (> 1024px): Three columns

Mobile adjustments:
  - Button height: 40px → 36px
  - Padding: 16px → 12px
  - Font size: 14px → 12px
```

**4. Accessibility Checklist**
```
WCAG 2.1 AA Compliance:
- [ ] Color contrast ratio ≥ 4.5:1 for text
- [ ] Button hit target ≥ 44x44px
- [ ] Focus indicators visible
- [ ] ARIA labels for icons
- [ ] Keyboard navigation support
```

## Practical Examples

### Example 1: Simple Button Component

**Start the workflow**:
```
1. Create Linear issue: PSN-100 "Design primary button"
2. Add Figma link to issue description:
   https://figma.com/file/ABC123/Components?node-id=15:2
3. Run: /ccpm:plan PSN-100
```

**Design phase output**:
```
✅ Design Analysis Complete

Component: Button / Primary
├── Size: 44px height
├── Color: #6366F1
├── Typography: Inter, 600, 14px
└── States: Default, Hover, Active, Disabled

Generated specs location: [Linear Document]
Ready for implementation.
```

**Developer implements**:
```tsx
export function PrimaryButton({ label, onClick }) {
  return (
    <button
      onClick={onClick}
      className="h-11 px-4 bg-indigo-600 text-white font-semibold
                 rounded hover:bg-indigo-700 focus:outline-none
                 focus:ring-2 focus:ring-indigo-500"
    >
      {label}
    </button>
  );
}
```

### Example 2: Dashboard Page

**Complex multi-component design**:
```
1. Create issue: PSN-200 "Design dashboard page"
2. Add Figma file: https://figma.com/file/XYZ789/Dashboard
3. Run: /ccpm:plan PSN-200
```

**Analysis reveals**:
```
✅ Design Analysis Complete

Components detected: 12
├── Header (1)
├── Sidebar (1)
├── Cards (5)
├── Charts (3)
└── Tables (2)

Color palette:
├── Primary: #6366F1
├── Secondary: #EC4899
├── Neutral: #F3F4F6 - #1F2937
└── Success: #10B981

Typography:
├── Display: Space Mono
├── Body: Inter
└── Code: Monaco

Generated breakdown: [Linear Document]

Recommended approach:
1. Build layout shell (Header + Sidebar)
2. Implement card components
3. Add data visualization
4. Connect to API
```

**Design refinement**:
```
/ccpm:plan PSN-200 1 "Increase sidebar width to 280px,
make cards taller"

✅ Refined Design Option 1

Adjustments:
- Sidebar width: 240px → 280px
- Card height: 220px → 280px
- Card padding: 16px → 20px
- Grid gap: 16px → 20px

Side-by-side comparison: [View]
Ready for approval!
```

**Final approval**:
```
/ccpm:plan PSN-200 1

✅ Dashboard Design Approved!

Implementation specs generated:
📄 Layout Specification (Header, Sidebar, Grid)
📄 Card Component Specs (5 variations)
📄 Chart Integration Guide
📄 Responsive Breakpoints
📄 Accessibility Requirements

Linear Document: [docs/specs/dashboard-implementation]

Next: Run /ccpm:work PSN-200
```

### Example 3: Design Iteration Workflow

**Scenario**: Design changed mid-implementation

```
Situation:
- Approved design shows 3-column layout
- Designer changes it to 2-column layout
- Specs are now outdated

Solution:
1. Update Figma file with new layout
2. Run: /ccpm:figma-refresh PSN-300
3. Specs automatically update
```

**Cache refresh process**:
```
/ccpm:figma-refresh PSN-300

🔄 Refreshing Figma cache...

Changes detected:
- ✅ Layout changed: 3-column → 2-column
- ✅ Card sizes updated
- ✅ Color palette modified (1 color added)
- ✅ Typography updated

Updated specs: [Linear Document]
Notified: Design changes affect layout components

Action items:
- Review responsive breakpoints
- Update card widths
- Check new color usage
```

## Best Practices

### Do's ✅

1. **Organize your Figma file**
   - Use clear, descriptive frame names
   - Group related components
   - Label variants (e.g., "Button / Primary / Large")
   - Document component purpose in descriptions

2. **Keep designs up-to-date**
   - Update Figma as designs change
   - Use design tokens consistently
   - Document color meanings (primary, success, error)
   - Update component descriptions with specs

3. **Use descriptive Figma links**
   - Link to specific components, not entire file
   - Use node IDs for precise targeting
   - Example: `/file/ABC123?node-id=15:2`

4. **Attach Figma links to Linear issues**
   - Always include design link in issue description
   - Add to existing issues during planning
   - Update links if design file changes

5. **Review extracted specs**
   - Verify component detection is correct
   - Check color values match your palette
   - Ensure spacing recommendations work
   - Validate responsive breakpoints

### Don'ts ❌

1. **Don't implement without approved specs**
   - Always run design-approve first
   - Prevents scope creep
   - Ensures design alignment

2. **Don't ignore cache invalidation**
   - Refresh designs when file changes significantly
   - Don't work with stale cache
   - Keeps specs synchronized

3. **Don't use vague frame names**
   - "Frame 15" is not helpful
   - Use: "UserCard / Default / Light"
   - Helps CCPM detect components correctly

4. **Don't skip accessibility specs**
   - Review WCAG checklist before implementation
   - Test color contrast
   - Verify button sizes and spacing

5. **Don't bypass refinement phase**
   - Always iterate with design-refine
   - Get feedback before approval
   - Prevents rework during implementation

## Caching & Performance

### How Caching Works

CCPM caches Figma data to provide instant access:

**Cache storage**:
- Stored in Linear issue comments
- Timestamped for validation
- TTL: 1 hour (configurable)
- Survives across sessions

**Cache includes**:
- Component metadata
- Design tokens (colors, typography, spacing)
- Frame hierarchy
- Text content
- Asset references

**Example cache entry**:
```
## 🎨 Figma Design Cache (PSN-123)

Design File: Dashboard.fig
Cached: 2025-11-21 14:30:00 UTC
Expires: 2025-11-21 15:30:00 UTC
Server: figma-repeat

Components: 12
Colors: 8
Typography: 4 styles
Spacing grid: [4, 8, 16, 32]px

Status: ✅ Valid cache
Action: Use `figma-refresh` to update
```

### When Cache Expires

Cache automatically invalidates if:
- 1 hour has passed
- Design file was significantly modified
- User explicitly runs `figma-refresh`
- New Figma link was added

**What happens when cache expires**:
1. CCPM re-fetches design data from Figma
2. Analyzes updated design
3. Updates cache with new data
4. Notifies of any changes

### Rate Limiting

CCPM respects Figma API rate limits:

**Official Figma API** (6 calls/month):
- Used for critical operations
- Careful rate limit management
- Falls back to cache on limit

**Community servers** (60 calls/hour):
- Higher rate limits
- Recommended for active development
- Better for iterative design workflows

**Check rate limit status**:
```
/ccpm:figma-refresh PSN-123 --status

📊 Figma Rate Limit Status

Official API: 4/6 used (66%)
Community (figma-repeat): 42/60 used (70%)

Recommendation: Use community server to preserve official API calls
```

## Integration with CCPM Commands

### Works With Planning Commands

**`/ccpm:plan`**
- Starts design extraction
- Creates design options
- Caches metadata

**`/ccpm:plan`**
- Iterates on designs
- Applies feedback
- Updates cache

**`/ccpm:plan`**
- Finalizes design
- Generates full specs
- Creates Linear Document

### Works With Implementation Commands

**`/ccpm:work`**
- Loads approved specs
- Uses component breakdown
- References styling guidelines

**`/ccpm:sync`**
- References design specs
- Verifies implementation matches design
- Flags design deviations

### Works With Utility Commands

**`/ccpm:figma-refresh`**
- Force refresh design cache
- Check rate limit status
- View cache information

**`/ccpm:work`**
- Loads design specs for task context
- Includes component breakdown
- Shows styling guidelines

## Troubleshooting

### Design Not Detected

**Problem**: Figma link not found in issue

**Solutions**:
1. Verify link is in issue description
   ```
   Add to issue: https://figma.com/file/ABC123/Project
   ```

2. Check link format
   ```
   ✅ Correct: https://figma.com/file/ABC123/Project
   ❌ Wrong: figma.com/file (missing protocol)
   ```

3. Try explicit link parameter
   ```
   /ccpm:plan PSN-123 --figma-url "https://..."
   ```

### Colors Not Extracted

**Problem**: Design colors not in generated specs

**Solutions**:
1. Ensure colors are defined in Figma file
   - Use color styles, not custom colors
   - Name colors consistently (e.g., "Primary Blue")

2. Refresh cache
   ```
   /ccpm:figma-refresh PSN-123
   ```

3. Check server configuration
   ```
   /ccpm:figma-refresh PSN-123 --status
   ```

### Rate Limit Exceeded

**Problem**: Too many Figma API calls

**Solutions**:
1. Switch to community server (higher limits)
   - Community servers: 60/hour
   - Official API: 6/month

2. Wait for rate limit reset
   - Community servers reset hourly
   - Official API resets monthly

3. Use cached data
   - Cache remains valid even with rate limit
   - Use `figma-refresh` only when needed

### Spec Generation Failed

**Problem**: Linear Document creation failed

**Solutions**:
1. Check Linear permissions
   - Verify write access to Linear workspace

2. Try again with larger issue ID
   ```
   /ccpm:plan PSN-123 1 --retry
   ```

3. Check cache validity
   ```
   /ccpm:figma-refresh PSN-123
   ```

## Summary

This skill enables:

- ✅ **Design extraction** from Figma files
- ✅ **Component detection** and analysis
- ✅ **Specification generation** for implementation
- ✅ **Design iteration** with refinement
- ✅ **Cache management** for performance
- ✅ **Best practices** guidance throughout workflow

**Typical workflow time**:
- Simple component: 2-5 minutes
- Complex page: 10-15 minutes
- Design iteration: 5-10 minutes per cycle

**Key commands**:
```
/ccpm:plan PSN-123          # Start design
/ccpm:plan PSN-123      # Iterate
/ccpm:plan PSN-123 1   # Generate specs
/ccpm:figma-refresh PSN-123         # Refresh cache
```

---

**Integration**: Works with `/ccpm:plan` and `/ccpm:figma-refresh` commands
**MCP Servers**: Figma MCP (figma-repeat, figma-trainer-guru, etc.)
**Linear Integration**: Stores designs and specs in Linear Documents
**Shared Module**: Uses `_shared-figma-detection.md` for link detection
