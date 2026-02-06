---
name: wcag-accessibility-audit
description: Comprehensive web accessibility audit using WCAG 2.1/2.2 guidelines. Evaluate compliance across 4 POUR principles (Perceivable, Operable, Understandable, Robust) with A, AA, AAA conformance levels.
---

# WCAG Accessibility Audit

This skill enables AI agents to perform a comprehensive **web accessibility evaluation** using the **Web Content Accessibility Guidelines (WCAG) 2.1 and 2.2** standards, ensuring digital products are usable by people with disabilities.

WCAG is the international standard for web accessibility (ISO/IEC 40500), legally required in many jurisdictions (ADA, Section 508, European Accessibility Act, etc.).

Use this skill to identify accessibility barriers, ensure legal compliance, reach broader audiences, and build inclusive digital experiences.

Combine with "Nielsen Heuristics Audit" for comprehensive usability evaluation or "Don Norman Principles" for human-centered design assessment.

## When to Use This Skill

Invoke this skill when:
- Ensuring legal compliance with accessibility laws (ADA, Section 508, EAA)
- Auditing websites or apps for accessibility barriers
- Planning inclusive design improvements
- Preparing for accessibility certifications
- Evaluating vendor products for procurement
- Training teams on accessibility standards
- Conducting pre-launch accessibility reviews

## Inputs Required

When executing this audit, gather:

- **interface_description**: Detailed description (type: website/web app/mobile app, purpose, target users, key features) [REQUIRED]
- **urls_or_screenshots**: Live URLs (preferred) or screenshots of key pages/screens [OPTIONAL but highly recommended]
- **target_conformance_level**: A, AA (most common), or AAA [OPTIONAL, defaults to AA]
- **specific_concerns**: Known accessibility issues or user complaints [OPTIONAL]
- **assistive_technologies_used**: Screen readers, keyboard-only, voice control, etc. [OPTIONAL]
- **wcag_version**: 2.1 or 2.2 (defaults to 2.2, latest) [OPTIONAL]

## The 4 POUR Principles

WCAG is organized around 4 core principles:

### 1. **Perceivable**
Information and user interface components must be presentable to users in ways they can perceive.

**Guidelines:**
- 1.1 Text Alternatives
- 1.2 Time-based Media
- 1.3 Adaptable
- 1.4 Distinguishable

### 2. **Operable**
User interface components and navigation must be operable.

**Guidelines:**
- 2.1 Keyboard Accessible
- 2.2 Enough Time
- 2.3 Seizures and Physical Reactions
- 2.4 Navigable
- 2.5 Input Modalities

### 3. **Understandable**
Information and the operation of user interface must be understandable.

**Guidelines:**
- 3.1 Readable
- 3.2 Predictable
- 3.3 Input Assistance

### 4. **Robust**
Content must be robust enough that it can be interpreted by a wide variety of user agents, including assistive technologies.

**Guidelines:**
- 4.1 Compatible

## Conformance Levels

WCAG defines three levels of conformance:

- **Level A**: Minimum level (essential accessibility features)
- **Level AA**: Target level for most organizations (addresses major barriers) ⭐ **MOST COMMON**
- **Level AAA**: Highest level (enhanced accessibility, not always achievable for all content)

**Legal Requirements**: Most laws require Level AA compliance.

## Critical Success Criteria (Level A & AA)

Focus on these high-impact criteria:

### Perceivable (Critical Criteria)

**1.1.1 Non-text Content (A)**
- All images, icons, and graphics have meaningful alt text
- Decorative images have empty alt="" or role="presentation"
- Complex images (charts, diagrams) have extended descriptions

**1.3.1 Info and Relationships (A)**
- Semantic HTML (headings, lists, tables, forms)
- Proper heading hierarchy (h1 → h2 → h3)
- Form labels associated with inputs
- Tables have proper headers

**1.3.2 Meaningful Sequence (A)**
- Content order makes sense when CSS is disabled
- Reading order matches visual order
- Tab order is logical

**1.4.1 Use of Color (A)**
- Information not conveyed by color alone
- Color-blind friendly palette
- Alternative indicators (icons, patterns, text)

**1.4.3 Contrast (Minimum) (AA)**
- Text: 4.5:1 contrast ratio (normal text)
- Large text: 3:1 contrast ratio (18pt+ or 14pt+ bold)
- UI components: 3:1 contrast ratio
- Use tools: WebAIM Contrast Checker

**1.4.4 Resize Text (AA)**
- Text can be resized to 200% without loss of content or functionality
- No horizontal scrolling at 200% zoom (1280px width)

**1.4.10 Reflow (AA) - WCAG 2.1**
- Content reflows to 320px width without horizontal scrolling
- No loss of information or functionality
- Responsive design

**1.4.11 Non-text Contrast (AA) - WCAG 2.1**
- UI components and graphical objects: 3:1 contrast
- Focus indicators, buttons, form controls
- Chart elements, infographics

**1.4.12 Text Spacing (AA) - WCAG 2.1**
- No loss of content when users adjust:
  - Line height: 1.5× font size
  - Paragraph spacing: 2× font size
  - Letter spacing: 0.12× font size
  - Word spacing: 0.16× font size

---

### Operable (Critical Criteria)

**2.1.1 Keyboard (A)**
- All functionality available via keyboard
- No keyboard traps (can navigate away)
- Proper focus management
- Test: Navigate entire site with Tab, Enter, Space, Arrow keys

**2.1.2 No Keyboard Trap (A)**
- Users can move focus away from any component
- Modal dialogs can be closed with Esc
- Focus returns properly after actions

**2.1.4 Character Key Shortcuts (A) - WCAG 2.1**
- Single character shortcuts can be turned off, remapped, or only active on focus
- Prevents accidental activation

**2.4.1 Bypass Blocks (A)**
- "Skip to main content" link
- Bypass repetitive navigation
- Landmark regions (header, nav, main, footer)

**2.4.2 Page Titled (A)**
- Every page has unique, descriptive title
- Title describes page purpose/topic
- Format: "Page Name - Site Name"

**2.4.3 Focus Order (A)**
- Focus order is logical and intuitive
- Matches visual/reading order
- No unexpected focus jumps

**2.4.4 Link Purpose (In Context) (A)**
- Link text describes destination
- Avoid "click here", "read more" without context
- Descriptive: "Download Q4 2025 Report (PDF)"

**2.4.5 Multiple Ways (AA)**
- At least 2 ways to find pages (navigation, search, sitemap)
- Breadcrumbs, related links, table of contents

**2.4.6 Headings and Labels (AA)**
- Descriptive headings and labels
- Clear form labels
- Logical heading hierarchy

**2.4.7 Focus Visible (AA)**
- Visible keyboard focus indicator
- Clear outline or highlight
- Minimum 2px, high contrast
- Never remove outline without replacement

**2.5.1 Pointer Gestures (A) - WCAG 2.1**
- Multi-point or path-based gestures have single-pointer alternative
- Pinch zoom → buttons, swipe → arrow buttons

**2.5.2 Pointer Cancellation (A) - WCAG 2.1**
- Click/tap actions trigger on up-event (not down)
- Users can cancel by moving pointer away
- Prevents accidental activation

**2.5.3 Label in Name (A) - WCAG 2.1**
- Visible label text matches accessible name
- Voice control users can activate by visible label

**2.5.4 Motion Actuation (A) - WCAG 2.1**
- Functionality triggered by device motion has UI alternative
- Shake to undo → has undo button

---

### Understandable (Critical Criteria)

**3.1.1 Language of Page (A)**
- HTML lang attribute set correctly
- `<html lang="en">`, `<html lang="es">`, etc.
- Helps screen readers pronounce correctly

**3.1.2 Language of Parts (AA)**
- Foreign language phrases marked with lang attribute
- `<span lang="fr">Bonjour</span>`

**3.2.1 On Focus (A)**
- Focus doesn't automatically trigger actions
- No automatic form submission on focus
- No unexpected navigation

**3.2.2 On Input (A)**
- Changing input doesn't cause unexpected actions
- Select dropdown doesn't auto-submit
- Warn before context changes

**3.2.3 Consistent Navigation (AA)**
- Navigation in same order on every page
- Consistent header/footer/menu placement
- Predictable patterns

**3.2.4 Consistent Identification (AA)**
- Same icons/buttons have same function throughout
- Search icon always means search
- Consistent labeling

**3.3.1 Error Identification (A)**
- Errors are clearly identified
- Specific error messages
- Error location is indicated

**3.3.2 Labels or Instructions (A)**
- Form fields have clear labels
- Required fields indicated
- Format instructions provided (e.g., "MM/DD/YYYY")

**3.3.3 Error Suggestion (AA)**
- Suggestions provided to fix errors
- "Email format should be: user@example.com"
- Helpful, specific guidance

**3.3.4 Error Prevention (Legal, Financial, Data) (AA)**
- Reversible: Users can undo submissions
- Checked: Data is validated before submission
- Confirmed: Users can review and confirm before final submission

---

### Robust (Critical Criteria)

**4.1.1 Parsing (A)**
- Valid HTML (no duplicate IDs, proper nesting)
- Check with W3C Validator
- Critical for assistive technology compatibility

**4.1.2 Name, Role, Value (A)**
- All UI components have accessible name
- Role is programmatically determined
- State changes are announced
- Use ARIA when needed, HTML first

**4.1.3 Status Messages (AA) - WCAG 2.1**
- Status messages announced without receiving focus
- Use ARIA live regions (role="status", aria-live)
- Success messages, progress indicators, errors

---

## Audit Procedure

Follow these steps systematically:

### Step 1: Preparation (15 minutes)

1. **Understand the interface:**
   - Review `interface_description` and `urls_or_screenshots`
   - Identify key user flows (homepage, forms, navigation, media content)
   - Note `target_conformance_level` (default: AA)

2. **Set up tools:**
   - Browser extensions: axe DevTools, WAVE, Lighthouse
   - Screen reader: NVDA (Windows), VoiceOver (Mac), JAWS
   - Keyboard only (unplug mouse)
   - Color contrast analyzer

3. **Define scope:**
   - Select representative pages (10-15 pages or key templates)
   - Include: homepage, main navigation, forms, dynamic content, media

### Step 2: Automated Testing (20 minutes)

Run automated tools to catch obvious issues:

**Recommended Tools:**
- **axe DevTools** (browser extension) - Most accurate automated tool
- **WAVE** (WebAIM) - Visual accessibility evaluation
- **Lighthouse** (Chrome DevTools) - Accessibility score + issues
- **HTML Validator** - W3C Markup Validation Service
- **Color Contrast Analyzer** - WebAIM or Stark

**Document:**
- Tool-detected violations
- Success criteria failed
- Affected components/pages
- Auto-generated severity (Critical/Serious/Moderate/Minor)

**Note**: Automated tools catch ~30-40% of issues. Manual testing is essential.

### Step 3: Manual Testing (60-90 minutes)

Manually test what automation misses:

#### Keyboard Navigation Test (15 minutes)
- [ ] Navigate entire site with Tab key only
- [ ] Test all interactive elements (links, buttons, forms, dropdowns)
- [ ] Check focus visibility (can you see where you are?)
- [ ] Verify logical focus order
- [ ] Test modal dialogs (open/close with keyboard, trap focus)
- [ ] No keyboard traps (can always navigate away)
- [ ] Test keyboard shortcuts (if any)

#### Screen Reader Test (20 minutes)
**NVDA (Windows) / VoiceOver (Mac) / JAWS**
- [ ] Navigate by headings (H key)
- [ ] Navigate by landmarks (D key)
- [ ] Navigate by links (K key)
- [ ] Navigate by form controls
- [ ] Verify alt text is meaningful
- [ ] Check form labels are announced
- [ ] Test dynamic content (ARIA live regions)
- [ ] Verify button/link purpose is clear

#### Visual/Content Test (15 minutes)
- [ ] Zoom to 200% (no horizontal scroll on desktop)
- [ ] Test at 320px width (mobile reflow)
- [ ] Check color contrast (text, buttons, icons)
- [ ] Verify information not conveyed by color alone
- [ ] Test with text spacing adjustments
- [ ] Check video captions/transcripts
- [ ] Check audio descriptions (if applicable)

#### Form Test (15 minutes)
- [ ] All inputs have visible, persistent labels
- [ ] Required fields indicated (not by color alone)
- [ ] Error messages are specific and helpful
- [ ] Errors identified and associated with fields
- [ ] Suggestions provided to fix errors
- [ ] Confirmation before submission (legal/financial)
- [ ] Can review and edit before final submit

#### Semantic HTML Test (10 minutes)
- [ ] Proper heading hierarchy (h1 → h2 → h3)
- [ ] Lists use `<ul>`, `<ol>`, `<li>`
- [ ] Buttons use `<button>` not `<div>`
- [ ] Links use `<a href>`
- [ ] Landmark regions (header, nav, main, footer)
- [ ] Tables have `<th>` headers and captions
- [ ] Form controls use proper elements

#### ARIA Test (10 minutes)
- [ ] ARIA used appropriately (HTML first)
- [ ] No ARIA is better than bad ARIA
- [ ] aria-label/aria-labelledby for custom controls
- [ ] aria-live for dynamic content
- [ ] aria-expanded, aria-pressed, aria-checked for state
- [ ] role="button" for custom buttons
- [ ] Verify ARIA doesn't conflict with HTML semantics

### Step 4: Reporting (30 minutes)

Generate comprehensive, prioritized report.

---

## Report Structure

```markdown
# WCAG Accessibility Audit Report

**Website/App**: [Name]
**URL**: [URL]
**Date**: [Date]
**WCAG Version**: 2.2 (or 2.1)
**Target Conformance Level**: AA
**Auditor**: [AI Agent]
**Scope**: [Pages/screens tested]

---

## Executive Summary

### Conformance Status
**Level A**: ❌ Not Conformant (X issues)
**Level AA**: ❌ Not Conformant (X issues)
**Level AAA**: ⚪ Not Evaluated

### Critical Findings
- **Total Issues**: [X]
  - Critical: [X] (blocks access, legal risk)
  - Serious: [X] (major barriers)
  - Moderate: [X] (some barriers)
  - Minor: [X] (small improvements)

### Top 3 Blockers
1. [Issue] - WCAG [X.X.X] (Level X)
2. [Issue] - WCAG [X.X.X] (Level X)
3. [Issue] - WCAG [X.X.X] (Level X)

### Estimated Remediation Effort
- **Quick Fixes** (1-2 weeks): [X issues]
- **Medium Effort** (1-2 months): [X issues]
- **Major Work** (3+ months): [X issues]

---

## Detailed Findings by Principle

### 1. Perceivable

#### ❌ FAIL: 1.1.1 Non-text Content (Level A)
**Severity**: Critical
**Impact**: Screen reader users cannot understand image content

**Issues Found:**
1. **Missing alt text on product images**
   - **Location**: Product listing pages (20+ images)
   - **Example**: `<img src="product.jpg">` (no alt attribute)
   - **User Impact**: Screen reader announces "image" with no context
   - **Recommendation**:
     - Add descriptive alt text: `<img src="product.jpg" alt="Blue running shoes, size 10">`
     - Use empty alt for decorative images: `alt=""`
   - **Effort**: Medium (need to audit all images)

2. **Icon buttons without labels**
   - **Location**: Navigation menu (hamburger, search, cart icons)
   - **Example**: `<button><svg>...</svg></button>`
   - **User Impact**: Screen reader announces "button" without purpose
   - **Recommendation**: Add aria-label: `<button aria-label="Open menu"><svg>...</svg></button>`
   - **Effort**: Low (10-15 instances)

#### ❌ FAIL: 1.4.3 Contrast (Minimum) (Level AA)
**Severity**: Critical
**Impact**: Low vision users cannot read text

**Issues Found:**
1. **Low contrast on primary buttons**
   - **Location**: Call-to-action buttons throughout site
   - **Current**: #999999 on #FFFFFF (2.85:1) ❌
   - **Required**: 4.5:1 for normal text, 3:1 for large text
   - **Recommendation**: Change to #595959 on #FFFFFF (7.0:1) ✅
   - **Effort**: Low (CSS update)

[Continue for all failed criteria...]

#### ✅ PASS: 1.4.4 Resize Text (Level AA)
**Status**: Conformant
**Notes**: Content reflows properly at 200% zoom, no horizontal scrolling

---

### 2. Operable

#### ❌ FAIL: 2.1.1 Keyboard (Level A)
**Severity**: Critical
**Impact**: Keyboard-only users cannot access functionality

**Issues Found:**
1. **Dropdown menu not keyboard accessible**
   - **Location**: Main navigation "Products" dropdown
   - **Problem**: Requires hover to reveal submenu
   - **User Impact**: Keyboard users cannot access submenu items
   - **Test**: Press Tab to "Products" link, press Enter → nothing happens
   - **Recommendation**:
     - Make dropdown trigger on focus or Enter key
     - Add aria-expanded attribute
     - Trap focus within dropdown when open
     - Close on Esc key
   - **Effort**: Medium (requires JavaScript refactor)

[Continue...]

---

### 3. Understandable

[Continue...]

---

### 4. Robust

[Continue...]

---

## Prioritized Remediation Plan

### Phase 1: Critical Blockers (Must Fix) - 1-2 weeks
**Legal Risk**: High | **User Impact**: Severe

1. **Add alt text to all images** - WCAG 1.1.1 (A)
   - Effort: 40 hours
   - Impact: Screen reader access to visual content

2. **Fix color contrast on buttons/text** - WCAG 1.4.3 (AA)
   - Effort: 8 hours
   - Impact: Readable by low vision users

3. **Make dropdown menus keyboard accessible** - WCAG 2.1.1 (A)
   - Effort: 16 hours
   - Impact: Keyboard users can navigate

4. **Add focus indicators** - WCAG 2.4.7 (AA)
   - Effort: 4 hours
   - Impact: Keyboard users can see focus

5. **Fix form labels** - WCAG 3.3.2 (A)
   - Effort: 12 hours
   - Impact: Screen reader users can complete forms

**Total Phase 1 Effort**: ~80 hours (2 weeks)

---

### Phase 2: Serious Issues (Should Fix) - 1-2 months
**Legal Risk**: Medium | **User Impact**: Significant

[Continue...]

---

### Phase 3: Moderate/Minor Issues (Nice to Have) - 3+ months
**Legal Risk**: Low | **User Impact**: Usability improvements

[Continue...]

---

## Testing Tools Used

### Automated Tools
- ✅ axe DevTools 4.x - 45 issues detected
- ✅ WAVE - 38 issues detected
- ✅ Lighthouse - Accessibility score: 64/100
- ✅ W3C Validator - 12 HTML errors

### Manual Testing
- ✅ Keyboard navigation (Chrome)
- ✅ Screen reader (NVDA 2025.1)
- ✅ Zoom to 200% (Chrome, Firefox)
- ✅ Mobile reflow at 320px
- ✅ Color contrast analyzer

### Assistive Technologies
- NVDA 2025.1 (Windows screen reader)
- Keyboard only (Tab, Enter, Space, Esc, Arrow keys)

---

## Accessibility Statement Recommendations

After remediation, publish an accessibility statement:

```
[Company] is committed to ensuring digital accessibility for people with disabilities.
We continually improve the user experience for everyone and apply relevant
accessibility standards.

Conformance Status: WCAG 2.2 Level AA Partial Conformance
(in progress, targeting full conformance by [date])

Feedback: If you encounter accessibility barriers, please contact [email/form].

Date: Last updated [date]
```

---

## Next Steps

1. **Immediate Actions** (This week)
   - [ ] Review this audit with product/dev teams
   - [ ] Prioritize Phase 1 critical issues
   - [ ] Assign ownership for each issue
   - [ ] Set target completion dates

2. **Short-term** (1-3 months)
   - [ ] Fix Phase 1 critical blockers
   - [ ] Conduct user testing with people with disabilities
   - [ ] Train team on accessibility best practices
   - [ ] Integrate accessibility into design/dev process

3. **Long-term** (3-6 months)
   - [ ] Complete Phase 2 and 3 remediations
   - [ ] Conduct follow-up WCAG audit
   - [ ] Publish accessibility statement
   - [ ] Consider third-party certification (e.g., WebAIM)
   - [ ] Implement automated accessibility testing in CI/CD

4. **Ongoing**
   - [ ] Regular accessibility audits (quarterly)
   - [ ] Include accessibility in definition of done
   - [ ] Monitor user feedback for accessibility issues
   - [ ] Stay updated on WCAG 2.2 and future 3.0

---

## Resources

### WCAG Standards
- [WCAG 2.2 Guidelines](https://www.w3.org/WAI/WCAG22/quickref/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Understanding WCAG 2.2](https://www.w3.org/WAI/WCAG22/Understanding/)

### Testing Tools
- [axe DevTools](https://www.deque.com/axe/devtools/)
- [WAVE](https://wave.webaim.org/)
- [Lighthouse](https://developers.google.com/web/tools/lighthouse)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)

### Screen Readers
- [NVDA](https://www.nvaccess.org/) (Free, Windows)
- [JAWS](https://www.freedomscientific.com/products/software/jaws/) (Paid, Windows)
- [VoiceOver](https://www.apple.com/accessibility/voiceover/) (Built-in, Mac/iOS)

### Training
- [WebAIM](https://webaim.org/)
- [Deque University](https://dequeuniversity.com/)
- [A11y Project](https://www.a11yproject.com/)

---

## Legal Disclaimer

This audit provides guidance on WCAG compliance but is not a legal assessment.
For legal compliance verification, consult with accessibility lawyers and
consider third-party certification.

---

## Methodology Notes

- **Standard**: WCAG 2.2 (or 2.1), Level AA conformance target
- **Method**: Combined automated and manual testing
- **Evaluator**: AI agent simulating accessibility expert
- **Limitations**:
  - Automated tools catch ~30-40% of issues
  - Manual testing required for comprehensive evaluation
  - Should be validated with users with disabilities
- **Scope**: [X pages] representing key templates and user flows

---

**Version**: 1.0
**Date**: [Date]
```

---

## Success Criteria Priority Matrix

Use this to prioritize issues:

| Priority | Criteria | Rationale |
|----------|----------|-----------|
| **P0** | Level A failures | Legal requirement, blocks access |
| **P1** | Level AA failures (high impact) | Legal requirement, major barriers |
| **P2** | Level AA failures (medium impact) | Legal requirement, moderate barriers |
| **P3** | Level AA failures (low impact) | Legal requirement, minor barriers |
| **P4** | Level AAA improvements | Enhanced accessibility (optional) |

---

## Common Quick Wins

These are high-impact, low-effort fixes:

1. **Add alt text** - 1.1.1 (A) - 1-2 days
2. **Fix color contrast** - 1.4.3 (AA) - 4-8 hours
3. **Add focus indicators** - 2.4.7 (AA) - 2-4 hours
4. **Add page titles** - 2.4.2 (A) - 1-2 hours
5. **Add lang attribute** - 3.1.1 (A) - 30 minutes
6. **Add form labels** - 3.3.2 (A) - 4-8 hours
7. **Fix HTML validation errors** - 4.1.1 (A) - 2-4 hours

---

## Best Practices

1. **Test with real users**: People with disabilities provide insights automation misses
2. **Start early**: Build accessibility in, don't bolt on later
3. **Educate team**: Accessibility is everyone's responsibility
4. **Use semantic HTML**: Proper HTML is 80% of accessibility
5. **Test with keyboard**: If it works with keyboard, it usually works with assistive tech
6. **Don't rely on color alone**: Use icons, patterns, text
7. **Provide alternatives**: Captions, transcripts, text descriptions
8. **Keep it simple**: Complex interfaces are harder to make accessible
9. **Stay updated**: WCAG evolves (2.0 → 2.1 → 2.2 → 3.0 coming)
10. **Legal compliance ≠ great UX**: Aim higher than minimum standards

---

## WCAG 2.2 New Success Criteria (2023)

WCAG 2.2 added 9 new criteria:

- **2.4.11 Focus Not Obscured (Minimum)** (AA) - Focus indicator not completely hidden
- **2.4.12 Focus Not Obscured (Enhanced)** (AAA) - Focus indicator not obscured at all
- **2.4.13 Focus Appearance** (AAA) - Focus indicator meets size/contrast requirements
- **2.5.7 Dragging Movements** (AA) - Single pointer alternative for drag operations
- **2.5.8 Target Size (Minimum)** (AA) - Touch targets at least 24×24 CSS pixels
- **3.2.6 Consistent Help** (A) - Help mechanism in same location across pages
- **3.3.7 Redundant Entry** (A) - Don't ask for same info twice in same session
- **3.3.8 Accessible Authentication (Minimum)** (AA) - No cognitive function test for auth
- **3.3.9 Accessible Authentication (Enhanced)** (AAA) - No cognitive function test (stricter)

Include these in 2.2 audits.

---

## Version

1.0 - Initial release (WCAG 2.2 compliant)

---

**Remember**: Accessibility is not just about compliance—it's about ensuring everyone can use your product. Real users with disabilities should validate these findings through usability testing.
