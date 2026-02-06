---
name: ui-design-review
description: Comprehensive visual design and aesthetics evaluation. Analyzes typography, color, spacing, hierarchy, consistency, branding, and modern design trends for polished, professional interfaces.
---

# UI Design Review

This skill enables AI agents to perform a comprehensive **visual design and aesthetics evaluation** of digital interfaces, analyzing elements like typography, color palettes, spacing, visual hierarchy, and overall design quality.

While other UX skills focus on functionality and usability, this skill evaluates the **visual polish, aesthetic appeal, and design craftsmanship** that makes interfaces feel professional, trustworthy, and delightful.

Use this skill to elevate visual design quality, ensure brand consistency, and create interfaces that not only work well but also look exceptional.

Combine with "Nielsen Heuristics" for usability, "WCAG Accessibility" for inclusive design, or "Don Norman Principles" for intuitive interaction.

## When to Use This Skill

Invoke this skill when:
- Evaluating visual design quality and polish
- Assessing brand consistency and personality
- Reviewing typography, color, and spacing decisions
- Identifying visual hierarchy issues
- Comparing design to modern standards and trends
- Preparing for design QA or handoff
- Evaluating design system consistency
- Assessing first impression and aesthetic appeal
- Identifying visual debt or outdated design elements

## Inputs Required

When executing this review, gather:

- **interface_description**: Description of interface (product type, target audience, brand personality) [REQUIRED]
- **screenshots_or_urls**: Visual references of the interface (multiple screens preferred) [REQUIRED]
- **brand_guidelines**: Brand colors, fonts, style guide (if available) [OPTIONAL]
- **target_audience**: Demographics, preferences, expectations [OPTIONAL]
- **competitors**: Competitor products for context [OPTIONAL]
- **design_goals**: Modern/classic, minimal/rich, playful/serious, etc. [OPTIONAL]

## Design Evaluation Framework

Evaluate across **10 key design dimensions**:

### 1. Visual Hierarchy
**Definition**: The arrangement of elements to show their importance and guide user attention.

**Evaluate:**
- Clear primary, secondary, tertiary levels
- Size, color, position used effectively
- Important actions stand out
- Content scannable and organized
- F-pattern or Z-pattern consideration

**Common Issues:**
- Everything looks equally important
- CTA buttons don't stand out
- Headers same size as body text
- Poor use of visual weight

---

### 2. Typography
**Definition**: Font choices, sizes, line heights, and text styling.

**Evaluate:**
- Font selection (appropriate, readable, on-brand)
- Font pairing (max 2-3 typefaces)
- Type scale (consistent sizing system)
- Line height (1.4-1.6 for body text)
- Line length (50-75 characters optimal)
- Font weights used effectively
- Readability on all devices

**Common Issues:**
- Too many fonts
- Poor font pairing
- Tiny text (<14px body)
- Insufficient line height
- Long lines (>100 characters)
- Script fonts for body text

---

### 3. Color Palette
**Definition**: Color choices, combinations, and usage.

**Evaluate:**
- Primary, secondary, accent colors defined
- Color harmony (complementary, analogous, triadic)
- Sufficient contrast (WCAG compliant)
- Intentional color usage (not arbitrary)
- Neutrals for balance
- Color psychology alignment with brand
- Accessible to color-blind users

**Common Issues:**
- Too many colors (no system)
- Low contrast combinations
- Clashing colors
- Colors don't reflect brand
- Overuse of pure black (#000)
- No neutral palette

---

### 4. Spacing & White Space
**Definition**: Margins, padding, gaps, and negative space.

**Evaluate:**
- Consistent spacing scale (8px grid common)
- Generous white space
- Proper padding in components
- Balanced margins
- Breathing room around elements
- Doesn't feel cramped or chaotic

**Common Issues:**
- Inconsistent spacing (3px here, 17px there)
- Too cramped (insufficient padding)
- Elements touching edges
- No breathing room
- Random gaps

---

### 5. Visual Consistency
**Definition**: Uniformity of design elements throughout.

**Evaluate:**
- Button styles consistent
- Card designs uniform
- Icon style cohesive
- Border radius consistent
- Shadow/elevation system
- Form styling standardized
- Pattern library adherence

**Common Issues:**
- Multiple button styles for same action
- Inconsistent border radius
- Mixed icon styles (outline + filled)
- No design system
- One-off components

---

### 6. Imagery & Graphics
**Definition**: Photos, illustrations, icons, and visual assets.

**Evaluate:**
- High quality, not pixelated
- Consistent style (photography, illustration)
- Appropriate to content
- Proper aspect ratios
- Icons clear and recognizable
- Graphics support content, not distract
- Optimized for performance

**Common Issues:**
- Low-resolution images
- Mixed illustration styles
- Stock photos look generic
- Icons inconsistent style
- Graphics don't match brand
- Overly decorative, no purpose

---

### 7. Layout & Grid
**Definition**: Structural organization and alignment.

**Evaluate:**
- Clear grid system (12-column common)
- Proper alignment
- Balanced composition
- Responsive breakpoints
- Logical content organization
- Visual flow guides eye
- Consistent page templates

**Common Issues:**
- Misaligned elements
- No grid system evident
- Unbalanced layouts
- Poor responsive behavior
- Elements floating randomly

---

### 8. Component Design
**Definition**: Quality of UI components (buttons, forms, cards, etc.).

**Evaluate:**
- Buttons look clickable (affordance)
- Forms easy to complete
- Cards well-defined
- Proper states (hover, active, disabled, focus)
- Interactive elements obvious
- Feedback on interaction
- Component variants consistent

**Common Issues:**
- Flat buttons (no depth/hover)
- Missing states
- Form inputs unclear
- Cards poorly defined
- No visual feedback

---

### 9. Branding & Personality
**Definition**: Expression of brand identity through design.

**Evaluate:**
- Brand colors prominent
- Typography reflects brand voice
- Personality evident (playful, serious, etc.)
- Unique, not generic
- Consistent tone
- Memorable design elements
- Differentiated from competitors

**Common Issues:**
- Generic, cookie-cutter design
- Doesn't reflect brand
- No personality
- Looks like Bootstrap template
- Inconsistent brand application

---

### 10. Modern Design Standards
**Definition**: Alignment with current best practices and trends.

**Evaluate:**
- Contemporary, not outdated
- Appropriate use of shadows/depth
- Clean, not cluttered
- Follows platform conventions
- Doesn't use deprecated patterns
- Fresh, not dated
- Balances trends with timelessness

**Common Issues:**
- Dated design (Web 2.0 gradients, bevels)
- Skeuomorphism when flat is standard
- Outdated patterns (carousels, splash screens)
- Ignores mobile-first
- Looks 5+ years old

---

## Review Procedure

Follow these steps systematically:

### Step 1: First Impression Analysis (5 minutes)

Evaluate initial visual impact:

**Questions to answer:**
- What's the immediate feeling? (Professional, playful, trustworthy, cheap, etc.)
- Does it look modern and polished?
- Is the brand immediately recognizable?
- What stands out first? (Good or bad?)
- Does it inspire confidence?
- First impression score: 1-10

**Document:**
- Initial reaction
- Strongest visual elements
- Most glaring issues
- Competitive comparison (if applicable)

---

### Step 2: Dimension-by-Dimension Evaluation (45-60 minutes)

For each of the 10 dimensions:

**Analysis template:**

```markdown
## Dimension: [Name]

### Overall Rating: ⭐⭐⭐⚪⚪ (3/5)

### Strengths
- ✅ [Positive finding 1]
- ✅ [Positive finding 2]

### Issues Found

#### Issue 1: [Title]
- **Severity**: Critical / High / Medium / Low
- **Location**: [Where it appears]
- **Problem**: [Specific description]
- **Impact**: [Why it matters]
- **Current**: [Screenshot or description]
- **Recommendation**: [Specific fix]
- **Effort**: Low (1-4h) / Medium (1-2d) / High (1w+)

#### Issue 2: [Title]
[Continue...]

### Best Practices Comparison
- Industry Standard: [What's expected]
- Current Implementation: [What exists]
- Gap: [Difference]

### Recommendations Summary
1. [Priority 1 fix]
2. [Priority 2 fix]
3. [Priority 3 fix]
```

---

### Step 3: Component Inventory (15 minutes)

Audit key UI components:

**Component Checklist:**
- [ ] Buttons (primary, secondary, tertiary, destructive)
- [ ] Forms (inputs, labels, validation, errors)
- [ ] Navigation (header, footer, sidebar, mobile menu)
- [ ] Cards (content cards, product cards)
- [ ] Typography (headings, body, links, captions)
- [ ] Icons (style, size, consistency)
- [ ] Images (quality, aspect ratios, treatment)
- [ ] Modals/dialogs
- [ ] Tables (if applicable)
- [ ] Empty states
- [ ] Loading states
- [ ] Error states

**For each component:**
- Consistency check ✅ / ❌
- Quality rating: 1-5
- Issues identified

---

### Step 4: Design System Assessment (10 minutes)

Evaluate if a design system exists and its quality:

**Design System Elements:**
- **Color Palette**: Defined, documented, consistently applied?
- **Typography Scale**: Systematic or arbitrary?
- **Spacing System**: Grid-based (4px, 8px) or random?
- **Component Library**: Reusable components or one-offs?
- **Icon Set**: Unified style?
- **Shadow/Elevation**: Consistent depth levels?
- **Border Radius**: Standardized?
- **Breakpoints**: Defined responsive rules?

**Rating:**
- No system evident: 0/10
- Inconsistent patterns: 3/10
- Some system, gaps: 5/10
- Mostly systematic: 7/10
- Complete design system: 10/10

---

### Step 5: Competitive Comparison (10 minutes)

If competitors provided, compare visually:

**Comparison Matrix:**

| Aspect | This Product | Competitor 1 | Competitor 2 | Industry Standard |
|--------|--------------|--------------|--------------|-------------------|
| Visual Polish | [Rating] | [Rating] | [Rating] | [Benchmark] |
| Modernity | [Rating] | [Rating] | [Rating] | [Benchmark] |
| Brand Strength | [Rating] | [Rating] | [Rating] | [Benchmark] |
| Hierarchy | [Rating] | [Rating] | [Rating] | [Benchmark] |

**Insights:**
- Where does it excel?
- Where does it lag?
- What can be learned from competitors?

---

### Step 6: Synthesize and Report (15 minutes)

Compile findings into comprehensive report.

---

## Report Structure

```markdown
# UI Design Review Report

**Interface**: [Name]
**Date**: [Date]
**Reviewer**: [AI Agent]
**Pages Reviewed**: [Number and types]

---

## Executive Summary

### Visual Design Score: [X]/100

| Dimension | Score | Status |
|-----------|-------|--------|
| Visual Hierarchy | [X]/10 | ✅ / ⚠️ / ❌ |
| Typography | [X]/10 | ✅ / ⚠️ / ❌ |
| Color Palette | [X]/10 | ✅ / ⚠️ / ❌ |
| Spacing & White Space | [X]/10 | ✅ / ⚠️ / ❌ |
| Visual Consistency | [X]/10 | ✅ / ⚠️ / ❌ |
| Imagery & Graphics | [X]/10 | ✅ / ⚠️ / ❌ |
| Layout & Grid | [X]/10 | ✅ / ⚠️ / ❌ |
| Component Design | [X]/10 | ✅ / ⚠️ / ❌ |
| Branding & Personality | [X]/10 | ✅ / ⚠️ / ❌ |
| Modern Standards | [X]/10 | ✅ / ⚠️ / ❌ |

### Overall Assessment
[2-3 sentences summarizing visual design quality]

### Top 3 Strengths
1. [Strength 1]
2. [Strength 2]
3. [Strength 3]

### Top 3 Issues
1. [Critical issue 1]
2. [Critical issue 2]
3. [Critical issue 3]

### First Impression
**Immediate Feeling**: [Professional/Dated/Playful/Generic/etc.]
**Trust Level**: [High/Medium/Low]
**Competitive Standing**: [Leading/On-par/Behind]

---

## Detailed Analysis

### 1. Visual Hierarchy ⭐⭐⭐⭐⚪ (4/5)

#### Strengths
- ✅ Primary CTAs clearly stand out with high contrast
- ✅ Heading sizes create clear content levels
- ✅ Good use of color to guide attention

#### Issues

**Issue 1.1: Secondary CTAs compete with primary**
- **Severity**: Medium
- **Location**: Homepage hero section
- **Problem**: "Learn More" button uses same visual weight as "Get Started" primary CTA
- **Current**: Both buttons same size, similar colors (blue vs. teal)
- **Impact**: Dilutes focus, users unsure which action is preferred
- **Recommendation**: Make secondary button text-only or outline style. Reduce size to 80% of primary.
- **Effort**: Low (1 hour)

**Issue 1.2: No clear focal point on product page**
- **Severity**: High
- **Problem**: Product image, price, description, and CTA all compete equally
- **Impact**: No visual flow, overwhelming, unclear what to do
- **Recommendation**: Increase product image size to 60% of space, make "Add to Cart" button 2x larger with strong color
- **Effort**: Medium (4 hours)

#### Recommendations Summary
1. Establish clear CTA hierarchy (primary > secondary > tertiary)
2. Use size, color, and position to create focal points
3. Apply 60-30-10 rule (60% dominant, 30% secondary, 10% accent)

---

### 2. Typography ⭐⭐⚪⚪⚪ (2/5)

#### Strengths
- ✅ Clean, readable sans-serif font choice (Inter)

#### Issues

**Issue 2.1: Body text too small**
- **Severity**: Critical
- **Location**: All body copy throughout site
- **Current**: 12px font size
- **Problem**: Strains eyes, fails accessibility, looks unprofessional
- **Standard**: 16px minimum for body text
- **Recommendation**: Increase to 16px (1rem) base font size
- **Effort**: Low (2 hours - global CSS change)

**Issue 2.2: Too many font sizes**
- **Severity**: Medium
- **Location**: Throughout interface
- **Current**: Using 14px, 15px, 16px, 17px, 18px (no system)
- **Problem**: Creates visual noise, no clear hierarchy
- **Recommendation**: Implement type scale:
  ```
  h1: 48px
  h2: 36px
  h3: 24px
  h4: 20px
  body: 16px
  small: 14px
  ```
- **Effort**: Medium (1 day - requires systematic update)

**Issue 2.3: Insufficient line height**
- **Severity**: High
- **Current**: Line height 1.2 on body text
- **Problem**: Text feels cramped, hard to read
- **Standard**: 1.5-1.6 for body text
- **Recommendation**: Set line-height: 1.5 (24px on 16px text)
- **Effort**: Low (1 hour)

---

### 3. Color Palette ⭐⭐⭐⭐⚪ (4/5)

#### Strengths
- ✅ Well-defined primary blue (#2563EB)
- ✅ Good use of neutrals (grays)
- ✅ Brand colors consistently applied

#### Issues

**Issue 3.1: Accent color overused**
- **Severity**: Low
- **Problem**: Orange accent appears everywhere, loses impact
- **Recommendation**: Reserve orange for important CTAs and alerts only
- **Effort**: Low (2-3 hours)

**Issue 3.2: Insufficient color shades**
- **Current**: Only using one shade of blue
- **Problem**: Can't create visual depth, hover states unclear
- **Recommendation**: Create 9-shade palette (50-900) for primary color:
  ```
  blue-50: #EFF6FF
  blue-100: #DBEAFE
  ...
  blue-500: #2563EB (primary)
  ...
  blue-900: #1E3A8A
  ```
- **Effort**: Medium (4 hours - requires design tokens)

---

[Continue for all 10 dimensions...]

---

## Component Audit

### Buttons

**Primary Button**
- Status: ⚠️ Needs improvement
- Issues:
  - Insufficient padding (8px vs. 12-16px standard)
  - Border radius inconsistent (4px vs. 6px elsewhere)
  - No hover state animation
- Recommendation:
  ```css
  /* Current */
  padding: 8px 16px;
  border-radius: 4px;

  /* Recommended */
  padding: 12px 24px;
  border-radius: 6px;
  transition: all 0.2s ease;

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  }
  ```

**Secondary Button**
- Status: ❌ Problematic
- Issues: Looks identical to primary, no differentiation
- Recommendation: Use outline style or lower visual weight

---

### Forms

**Input Fields**
- Status: ⚠️ Needs improvement
- Issues:
  - Small height (32px vs. 40-44px standard)
  - Border too subtle
  - No focus state
  - Labels not bold enough
- Recommendation: [Specific CSS improvements]

---

### Cards

**Product Cards**
- Status: ✅ Good
- Strengths: Clean, well-spaced, good hover effect
- Minor: Could use subtle shadow instead of border

---

[Continue for all key components...]

---

## Design System Status

**Overall Score**: 4/10 (Inconsistent patterns)

### What Exists
- ✅ Basic color palette defined
- ✅ Some typography styles
- ✅ Button variations

### What's Missing
- ❌ Documented spacing system
- ❌ Complete type scale
- ❌ Shadow/elevation system
- ❌ Consistent border radius values
- ❌ Icon guidelines
- ❌ Responsive breakpoint rules

### Recommendation
Invest in formal design system:
1. Define design tokens (colors, spacing, typography)
2. Create component library (Figma or code)
3. Document usage guidelines
4. Enforce consistency in new designs

**Effort**: High (2-4 weeks)
**Impact**: Massive - eliminates future inconsistency

---

## Competitive Comparison

| Aspect | This Product | Competitor A | Competitor B | Winner |
|--------|--------------|--------------|--------------|--------|
| **Visual Polish** | 6/10 | 8/10 | 7/10 | Competitor A |
| **Modernity** | 5/10 | 9/10 | 6/10 | Competitor A |
| **Typography** | 4/10 | 8/10 | 7/10 | Competitor A |
| **Color Usage** | 7/10 | 7/10 | 8/10 | Competitor B |
| **Consistency** | 5/10 | 9/10 | 7/10 | Competitor A |
| **Brand Strength** | 6/10 | 7/10 | 8/10 | Competitor B |

**Key Insights:**
- Competitor A sets the visual standard in the category
- Our product lags in typography and consistency
- Opportunity to differentiate through stronger branding
- Need to modernize visual language to compete

---

## Prioritized Recommendations

### Phase 1: Critical Fixes (1 week, High ROI)

**Visual Impact: ★★★★★ | Effort: Low | Cost: ~20 hours**

1. **Increase body text to 16px**
   - Impact: Immediate professionalism boost
   - Effort: 2 hours
   - Tools: Global CSS update

2. **Fix CTA hierarchy**
   - Impact: Clearer user guidance
   - Effort: 4 hours
   - Details: Primary stands out, secondary subdued

3. **Improve button padding and states**
   - Impact: More premium feel
   - Effort: 4 hours
   - Details: Add hover, focus, active states

4. **Increase spacing throughout**
   - Impact: Cleaner, less cramped
   - Effort: 8 hours
   - Details: Apply consistent 8px spacing scale

5. **Add subtle shadows to cards**
   - Impact: Better depth and hierarchy
   - Effort: 2 hours
   - Details: Use elevation system (2px, 4px, 8px)

**Expected Outcome:** Professional, polished appearance

---

### Phase 2: Design System Foundation (2-3 weeks)

**Visual Impact: ★★★★☆ | Effort: Medium | Cost: ~80 hours**

1. **Create design tokens**
   - Colors (9 shades per color)
   - Spacing scale (4, 8, 12, 16, 24, 32, 48, 64px)
   - Type scale (with line heights)
   - Shadow system
   - Border radius values

2. **Build component library**
   - Buttons (all variants)
   - Forms (inputs, selects, checkboxes)
   - Cards (all types)
   - Navigation components
   - Modals and overlays

3. **Document guidelines**
   - When to use each component
   - Do's and don'ts
   - Code snippets
   - Figma library

**Expected Outcome:** Consistency across all future designs

---

### Phase 3: Visual Enhancement (1-2 months)

**Visual Impact: ★★★★☆ | Effort: High | Cost: ~160 hours**

1. **Refresh brand application**
2. **Custom illustrations/graphics**
3. **Micro-interactions and animations**
4. **Dark mode (if applicable)**
5. **Advanced responsive optimization**

**Expected Outcome:** Premium, differentiated visual design

---

## Design Trends Assessment (2026)

### Current Trends in Product Design

**In (Modern):**
- ✅ Generous white space
- ✅ Large typography
- ✅ Subtle shadows (not flat)
- ✅ Rounded corners (6-8px)
- ✅ Soft color palettes
- ✅ Micro-interactions
- ✅ Dark mode support
- ✅ Glassmorphism (subtle)
- ✅ 3D elements (tasteful)

**Out (Dated):**
- ❌ Extreme flat design
- ❌ Harsh shadows
- ❌ Gradients everywhere
- ❌ Small text (<14px)
- ❌ Overly complex layouts
- ❌ Skeuomorphism
- ❌ Carousels/sliders

**This Product's Alignment:**
- Moderate - Some modern elements, some dated patterns
- Needs update to feel current

---

## Accessibility-Visual Overlap

While WCAG audit covers technical accessibility, visual design impacts it:

**Color Contrast:**
- Current contrast ratios meet/fail WCAG?
- Issues: [List contrast failures]

**Typography Readability:**
- Font sizes appropriate for all users?
- Line heights sufficient?

**Touch Targets:**
- Buttons large enough (44×44px minimum)?
- Spacing between interactive elements?

**Visual Indicators:**
- Relying on color alone for meaning?
- Icons + text labels?

[Cross-reference with WCAG audit]

---

## Before/After Mockup Recommendations

For maximum impact, prioritize these visual transformations:

### Homepage Hero

**Before Issues:**
- Cluttered, no clear focal point
- Small, timid CTA
- Weak visual hierarchy

**After Improvements:**
- Clear headline with generous spacing
- Bold, confident CTA (2x size)
- Strong visual hierarchy
- Better use of imagery

**Expected Impact:** +30% CTA click rate

---

### Product Page

**Before Issues:**
- Everything same size
- No breathing room
- "Add to Cart" lost in noise

**After Improvements:**
- Product image dominates
- Clear price display
- Prominent "Add to Cart"
- Organized product details

**Expected Impact:** +20% add-to-cart rate

---

[Continue for key pages...]

---

## Design Quality Checklist

Use this checklist for ongoing quality assurance:

### Typography ✓
- [ ] Body text 16px minimum
- [ ] Consistent type scale (max 6-8 sizes)
- [ ] Line height 1.5-1.6 for body
- [ ] Max 2-3 typefaces
- [ ] Font weights used intentionally
- [ ] Line length 50-75 characters

### Color ✓
- [ ] Defined color palette (primary, secondary, accent, neutrals)
- [ ] All combinations pass WCAG AA contrast
- [ ] Color shades available (not just one blue)
- [ ] Intentional color usage (not decorative)
- [ ] Consistent application across site

### Spacing ✓
- [ ] Consistent spacing scale (8px grid or similar)
- [ ] Generous white space
- [ ] Elements have breathing room
- [ ] Padding/margin follows system
- [ ] No random spacing values

### Components ✓
- [ ] All interactive states defined (hover, focus, active, disabled)
- [ ] Buttons look clickable
- [ ] Form inputs clear and labeled
- [ ] Cards well-defined
- [ ] Icons consistent style
- [ ] Components reusable

### Consistency ✓
- [ ] Same actions look the same
- [ ] Border radius consistent
- [ ] Shadow system applied uniformly
- [ ] Icon style cohesive
- [ ] Design patterns repeated

### Layout ✓
- [ ] Clear grid system
- [ ] Elements aligned
- [ ] Balanced composition
- [ ] Responsive breakpoints defined
- [ ] Visual flow guides eye

---

## Tools Recommended

**For Design Review:**
- Figma/Sketch - Design files
- Chrome DevTools - Inspect CSS
- Contrast Checker - WebAIM, Stark
- WhatFont - Identify typography
- Page Ruler - Measure spacing
- ColorZilla - Extract colors

**For Improvement:**
- Figma - Design system, mockups
- Tailwind CSS - Utility-first CSS framework
- shadcn/ui - Component library
- Radix UI - Accessible primitives
- Coolors - Color palette generator
- Type Scale - Typography scale tool

---

## Next Steps

1. **Review findings** with design/dev team
2. **Prioritize Phase 1 fixes** (quick wins)
3. **Create design system foundation** (Phase 2)
4. **Establish design QA process** (use checklist)
5. **Re-audit in 3 months** to measure progress

---

## Methodology Notes

- **Evaluation Method**: Expert visual design review
- **Standards**: Modern web design best practices (2026)
- **Focus**: Visual aesthetics, polish, consistency
- **Limitations**:
  - Subjective elements (some design preferences vary)
  - Not user testing (perception-based)
  - Should be validated with target audience
- **Complement with**: User research, A/B testing, analytics

---

## References

- Steve Krug - "Don't Make Me Think" (Visual design for usability)
- Robin Williams - "The Non-Designer's Design Book"
- Refactoring UI - Adam Wathan & Steve Schoger
- Material Design Guidelines (Google)
- Human Interface Guidelines (Apple)
- Laws of UX - Jon Yablonski

---

**Version**: 1.0
**Date**: [Date]
```

---

## Scoring System

### Overall Design Score Calculation

Each dimension scored 0-10:
- **9-10**: Exceptional, industry-leading
- **7-8**: Strong, professional
- **5-6**: Adequate, room for improvement
- **3-4**: Below par, needs attention
- **0-2**: Poor, requires major redesign

**Overall Score** = Average of all 10 dimensions

**Grade:**
- 90-100: A+ (Exceptional)
- 80-89: A (Excellent)
- 70-79: B (Good)
- 60-69: C (Acceptable)
- 50-59: D (Needs Work)
- 0-49: F (Poor)

---

## Common Design Smells

Quick indicators of visual design issues:

🚩 **Typography Red Flags:**
- Body text <14px
- More than 3 font families
- Line height <1.3
- Comic Sans, Papyrus (unless satirical)

🚩 **Color Red Flags:**
- Pure black (#000) on pure white (#FFF)
- Rainbow explosion (no color system)
- Low contrast combinations
- Clashing color combinations

🚩 **Spacing Red Flags:**
- Random pixel values (13px, 23px, 17px)
- Elements touching screen edges
- No consistent spacing
- Too cramped or too sparse

🚩 **Consistency Red Flags:**
- Multiple button styles for same action
- Border radius varies wildly
- Mixed icon styles
- No evident design system

🚩 **Modernity Red Flags:**
- Beveled edges
- Web 2.0 gloss/gradients
- Outdated stock photos
- Flash-era animations
- Non-responsive design

---

## Design Quality Levels

### Level 1: Bootstrap Template (Score: 40-50)
- Generic, off-the-shelf appearance
- Minimal customization
- No personality or brand
- Functional but forgettable

### Level 2: Customized Framework (Score: 60-70)
- Some brand application
- Customized colors/fonts
- Inconsistencies evident
- Decent but not distinctive

### Level 3: Professional Design (Score: 70-80)
- Strong brand identity
- Consistent design system
- Polished and intentional
- Competitive quality

### Level 4: Design Excellence (Score: 80-90)
- Exceptional craft and attention to detail
- Strong personality and uniqueness
- Memorable and delightful
- Industry-leading

### Level 5: Award-Worthy (Score: 90-100)
- Innovative and trendsetting
- Perfect execution
- Emotional resonance
- Benchmark for others

**Goal**: Aim for Level 3+ (70+) to be competitive.

---

## Version

1.0 - Initial release

---

**Remember**: Great visual design isn't about trends or decoration—it's about creating clear, beautiful, functional interfaces that serve users while expressing brand personality. Design is not just how it looks, but how it works.
