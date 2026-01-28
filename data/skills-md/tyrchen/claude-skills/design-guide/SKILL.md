---
name: design-guide
description: Extract comprehensive design language from websites including colors, typography, animations, interactive states, shadows, gradients, component patterns, and UX behaviors. Generates pixel-perfect design guides with responsive screenshots and complete design system documentation. Use when analyzing website design, creating design systems, or rebuilding sites.
---

# Comprehensive Design Guide Generator

Extract the complete design language from any website with automated analysis of colors, typography, animations, interactions, and UX patterns. Goes far beyond basic CSS extraction to capture the full design system.

## When to Use This Skill

Use this skill when you want to:
- **Analyze a website's complete design system** - Not just colors and fonts, but the entire design language
- **Extract interactive design patterns** - Hover states, transitions, animations, micro-interactions
- **Document component libraries** - Buttons, cards, forms, navigation patterns
- **Create pixel-perfect recreations** - Comprehensive data for exact replicas
- **Build design systems** - Complete token systems with all design decisions documented
- **Understand UX patterns** - Interaction patterns, accessibility features, responsive behavior
- **Reverse-engineer designs** - Full extraction of design decisions from live websites

## What This Skill Extracts

### 🎨 Visual Design

**Colors & Gradients**
- Text colors (all variations)
- Background colors
- Border colors
- Shadow colors (extracted from box-shadow)
- Linear and radial gradients
- Complete color palette with CSS custom properties

**Typography System**
- Font families and fallback stacks
- Complete type scale (all font sizes used)
- Font weights (100-900)
- Line heights
- Letter spacing
- Text transforms
- Heading hierarchy (H1-H6) with exact styles
- Body text specifications

**Visual Effects**
- Box shadows (all variations)
- Text shadows
- CSS filters (blur, brightness, contrast, etc.)
- Transform properties
- Opacity values
- Border radius values

### ⚡ Interactive Design

**Interactive States**
- Hover effects (color, transform, shadow changes)
- Focus states
- Active states
- Transition properties
- Before/after comparisons for hover states
- Screenshots of interactive elements in hover state

**Animations**
- CSS transitions (timing, easing, duration)
- Keyframe animations
- Animated element detection
- Animation names and rules

### 📐 Layout & Spacing

**Spacing System**
- Margin values (sorted scale)
- Padding values (sorted scale)
- Gap values (Flexbox/Grid)
- Complete spacing token system

**Layout Patterns**
- Container max-widths
- Centered container patterns
- Flexbox configurations
- Grid layouts
- Sticky/fixed positioning

### 🧩 Component Patterns

**UI Components Identified**
- Buttons (with exact styling)
- Cards (background, shadow, radius, padding)
- Navigation bars
- Forms and inputs
- Modals
- Badges
- Alerts

**Component Documentation**
- Exact CSS for each component variant
- Component text content
- Visual hierarchy

### 🎭 UX & Behavior

**Interaction Patterns**
- Scroll behavior
- Cursor styles used
- Interactive element count
- Sticky/fixed element patterns

**Accessibility Features**
- ARIA labels count
- ARIA descriptions count
- Role attributes count
- Image alt text usage

### 📱 Responsive Design

**Multi-Device Analysis**
- Mobile screenshots (375x812)
- Tablet screenshots (768x1024)
- Desktop screenshots (1920x1080)
- Layout metrics at each breakpoint
- Viewport-specific behaviors

## Instructions for Claude

### Step 1: Verify Setup

Navigate to the skill directory:
```bash
cd /Users/tchen/projects/mycode/claude-skills/design-guide
```

Ensure dependencies are installed (first time only):
```bash
uv sync
playwright install chromium
```

### Step 2: Gather Requirements

Ask the user for:
- **URL** (required): The website to analyze
- **Output directory** (optional): Where to save results (default: `./output`)
- **Viewport size** (optional): Custom viewport dimensions (default: 1600x1200)

### Step 3: Run the Enhanced Extractor

Execute the comprehensive extraction:

```bash
uv run main.py --url <URL> [OPTIONS]
```

**Available Options:**
- `--url, -u`: Website URL to analyze (required)
- `--output, -o`: Output directory (default: `./output`)
- `--viewport-width`: Viewport width in pixels (default: 1600)
- `--viewport-height`: Viewport height in pixels (default: 1200)

**What happens during extraction:**

The tool will:
1. 📄 Load the page and wait for network idle
2. 📸 Take viewport and full-page screenshots
3. 🔍 Extract HTML structure
4. 💅 Extract all CSS (linked and inline)
5. 🎯 Compute styles for every element
6. ⚡ Capture interactive states (hover 10 elements)
7. 🎨 Analyze complete color palette
8. 📝 Extract typography system
9. 📐 Analyze layout and spacing
10. ✨ Detect animations and transitions
11. 🌟 Extract shadows and visual effects
12. 🧩 Identify component patterns
13. 🎭 Analyze UX patterns
14. 📱 Test responsive behavior (3 breakpoints)
15. 💾 Save all data and generate design guide

### Step 4: Review Generated Assets

After extraction, the output directory contains:

**Documentation**
- `design-guide.md` - Comprehensive design guide (main deliverable)
- `design_data.json` - Complete structured data

**Visual Assets**
- `viewport_screenshot.png` - Desktop viewport capture
- `fullpage_screenshot.png` - Complete page capture
- `interactive_hover.png` - Hover state demonstrations
- `responsive_mobile.png` - Mobile view (375x812)
- `responsive_tablet.png` - Tablet view (768x1024)
- `responsive_desktop.png` - Large desktop view (1920x1080)

**Source Code**
- `extracted.html` - Original HTML
- `extracted.css` - All CSS (can be 2-3MB for complex sites)
- `computed_styles.json` - Computed styles for every element (can be large)

### Step 5: Explore the Design Guide

The generated `design-guide.md` contains:

1. **Visual Assets** - All screenshots with descriptions
2. **Color System** - Complete palette with CSS variables
3. **Typography System** - Font stacks, type scale, heading hierarchy
4. **Spacing & Layout** - Complete spacing tokens and container patterns
5. **Visual Effects** - Shadows, filters, transforms, opacity
6. **Animations & Transitions** - All transitions and keyframe animations
7. **Interactive States** - Hover effects with before/after comparisons
8. **Component Patterns** - Button, card, form, nav styling
9. **UX Patterns** - Accessibility, cursor styles, sticky elements
10. **Responsive Design** - Breakpoint analysis
11. **Implementation Guide** - Step-by-step recreation instructions

### Step 6: Analyze Design Patterns

Use the extracted data to understand:

**Design System Maturity**
- Consistent spacing scale? (Check margin/padding variations)
- Defined type scale? (Check font size progression)
- Component library? (Check identified components)
- Accessibility? (Check ARIA features)

**Design Decisions**
- Color choices and usage patterns
- Typography hierarchy clarity
- Animation smoothness (check transition timings)
- Shadow depth system
- Border radius consistency

### Step 7: Pixel-Perfect Recreation (Advanced)

For recreating the design:

1. **Use Design Tokens**: Copy CSS variables from design guide
2. **Match Typography**: Use exact font stacks and sizes
3. **Implement Spacing**: Follow extracted spacing scale
4. **Apply Effects**: Use exact shadow and border-radius values
5. **Add Interactions**: Implement hover/focus states as documented
6. **Test Responsive**: Match layouts at all breakpoints
7. **Verify Visually**: Compare with extracted screenshots

### Step 8: Interactive Exploration with Playwright MCP (Optional)

If you need deeper interaction analysis:

```python
# Use Playwright MCP to:
1. Navigate to specific pages/states
2. Test form interactions
3. Trigger modals/dropdowns
4. Capture specific UI states
5. Test animations manually
6. Explore navigation flows
```

## Usage Examples

### Basic Usage - Any Website
```bash
uv run main.py --url https://stripe.com
```

### E-commerce Site Analysis
```bash
uv run main.py --url https://shopify.com --output ./shopify-design
```

### Custom Viewport
```bash
uv run main.py --url https://github.com --viewport-width 1920 --viewport-height 1080
```

### Design System Extraction
```bash
# Extract from design system documentation
uv run main.py --url https://primer.style --output ./primer-system
```

## Example Output

After analyzing **GitHub.com**, you get:

**Colors:**
- 100+ unique colors cataloged
- Dark theme palette (rgb(13, 17, 23) backgrounds)
- Brand colors (rgb(31, 111, 235))
- 5+ gradient variations
- Shadow color system

**Typography:**
- Mona Sans font family
- 10-level type scale (12px to 72px)
- 5 font weights (400, 450, 500, 600, 700)
- Heading hierarchy

**Components:**
- 5+ button variations
- Card patterns with exact shadows
- Navigation bar styles
- Form input specifications

**Interactive:**
- Hover state transitions
- Animation keyframes
- Transform effects

**Responsive:**
- Mobile, tablet, desktop screenshots
- Layout adaptations documented

## Advanced Features

### Component Pattern Recognition

The skill automatically identifies:
- **Buttons**: Searches for button, [role="button"], .btn, input[type="button"]
- **Cards**: Searches for [class*="card"], article, [class*="post"]
- **Nav**: Searches for nav, [role="navigation"], header nav
- **Forms**: Extracts input, select, textarea styling

### Interactive State Capture

- Hovers over first 10 interactive elements
- Captures computed styles before and after hover
- Takes screenshot in hover state
- Documents changes in design guide

### Responsive Testing

Automatically tests at:
- **Mobile**: 375x812 (iPhone X/11/12/13/14 size)
- **Tablet**: 768x1024 (iPad portrait)
- **Desktop**: 1920x1080 (Full HD)

### Animation Detection

- Scans all elements for CSS animations
- Extracts keyframe rules from stylesheets
- Identifies animated elements
- Documents transition properties

## Tips for Best Results

### Choosing the Right URL

✅ **Good URLs:**
- Homepage (comprehensive overview)
- Marketing pages (best design work)
- Component libraries (design system docs)
- Login/signup pages (form patterns)

❌ **Challenging URLs:**
- Authenticated content (may redirect)
- Dynamic SPAs (may need extra wait time)
- Sites with aggressive anti-bot measures

### Viewport Selection

- **1600x1200** - Default, good for most sites
- **1920x1080** - Large desktop analysis
- **1280x720** - Smaller desktop
- **Custom** - Match specific design requirements

### Multiple Page Analysis

For complete design systems, run on multiple pages:

```bash
# Homepage
uv run main.py --url https://example.com -o ./design/home

# Product page
uv run main.py --url https://example.com/product -o ./design/product

# About page
uv run main.py --url https://example.com/about -o ./design/about

# Then compare to find:
# - Consistent design tokens
# - Page-specific variations
# - Component reuse patterns
```

### Performance Notes

**Extraction Time:**
- Simple sites: 30-60 seconds
- Complex sites (GitHub, Stripe): 60-120 seconds
- Includes responsive testing at 3 breakpoints

**Output Size:**
- Design guide: 5-20KB (markdown)
- Screenshots: 500KB - 3MB total
- CSS file: 10KB - 5MB (complex sites)
- Computed styles: 100KB - 10MB
- Design data JSON: 50KB - 500KB

## Troubleshooting

### Browser Not Installed
```bash
playwright install chromium
```

### Page Load Timeout
- Increase timeout in code if needed
- Some SPAs may need extra wait time
- Check network connectivity

### Missing Interactive States
- Some sites block mouse events
- Screenshot may capture only first few hovers
- Manual Playwright MCP can capture more

### Empty Design Guide Sections
- Page may not use certain features (animations, shadows, etc.)
- This is normal for minimalist designs
- Check `design_data.json` for raw data

### CORS Errors for CSS
- External stylesheets may be blocked
- Tool extracts what it can access
- Check extracted.css for completeness
- Use browser DevTools to manually inspect

## Cost Considerations

**Resource Usage:**
- Local Playwright (free)
- No external APIs (free)
- CPU: Moderate (page rendering)
- Memory: 500MB-2GB (complex sites)
- Disk: 5-50MB per extraction

**No API Keys Required!**

## Design Guide Quality

The generated design guide is:
- ✅ **Comprehensive** - Covers all design aspects
- ✅ **Actionable** - Ready to use for implementation
- ✅ **Organized** - Clear sections and categories
- ✅ **Visual** - References screenshots throughout
- ✅ **Technical** - Exact CSS values and code
- ✅ **Accessible** - Documents accessibility features

## Integration with Claude Code Workflow

### Typical Usage Flow

1. **User Request**: "Analyze the design of stripe.com"

2. **Claude Uses Skill**:
   ```bash
   cd /Users/tchen/projects/mycode/claude-skills/design-guide
   uv run main.py --url https://stripe.com --output ./stripe-design
   ```

3. **Claude Reviews Output**: Reads design-guide.md

4. **Claude Presents Findings**:
   - Color system overview
   - Typography hierarchy
   - Key components identified
   - Interactive patterns found
   - Accessibility score

5. **User Follow-up**: "Recreate the hero section"

6. **Claude Implements**: Uses extracted design tokens to build pixel-perfect HTML/CSS

## Example User Interactions

**User**: "What design system does Shopify use?"

**Claude**:
```bash
# Runs extraction
uv run main.py --url https://shopify.com -o ./shopify-design

# Analyzes output
# Reports findings:
```
"Shopify uses:
- **Polaris design system**
- Typography: Inter font family
- Colors: Green primary (rgb(0, 128, 96))
- Spacing: 4px base unit
- Components: Identified 12 button variants, card system, navigation
- Shadows: 3-level depth system
- Responsive: Mobile-first approach"

---

**User**: "Extract the button styles from GitHub"

**Claude**:
```bash
uv run main.py --url https://github.com -o ./github-design
```

"Found 5 button variants on GitHub:

1. **Primary Button**:
   - Background: rgb(31, 111, 235)
   - Color: white
   - Padding: 5px 16px
   - Border-radius: 6px
   - Hover: Transforms darker

[Shows exact CSS from design guide]"

---

## Advanced: Claude-Driven Analysis

When using this skill, Claude should:

1. **Run extraction** automatically
2. **Read design-guide.md** to understand design
3. **Analyze patterns** for insights
4. **Present findings** in structured format
5. **Offer to recreate** components if requested
6. **Use Playwright MCP** for deeper interaction testing if needed

## Deliverables

After running this skill, deliver to user:

✅ **design-guide.md** - Main comprehensive guide
✅ **All screenshots** - Visual reference
✅ **design_data.json** - Structured data for programmatic use
✅ **Source files** - HTML, CSS, computed styles

Optional:
✅ **Recreated components** - If requested
✅ **Comparison analysis** - If analyzing multiple sites
✅ **Token library** - CSS/SCSS variables file

---

**Skill Version:** 2.0 (Enhanced - Full Design Language Extraction)
**Last Updated:** 2025-11-16
**Extraction Depth:** Comprehensive (11+ analysis types)
