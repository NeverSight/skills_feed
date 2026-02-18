---
name: accessibility-audit
description: Run comprehensive accessibility audit (WCAG 2.1) on Webflow pages - checks buttons, forms, links, focus states, headings, keyboard navigation, and generates detailed reports with fixes. Requires Webflow Designer connection. Excludes image alt text (covered by asset-audit skill).
---

# Accessibility Audit

Comprehensive WCAG 2.1 accessibility audit for Webflow pages with detailed issue detection and actionable fixes.

## Important Note

**ALWAYS use Webflow MCP tools for all operations:**
- Use Webflow MCP's `webflow_guide_tool` to get best practices before starting
- Use Webflow MCP's `data_sites_tool` with action `list_sites` to identify available sites
- Use Webflow MCP's `data_sites_tool` with action `get_site` to retrieve site details
- Use Webflow MCP's `data_pages_tool` with action `list_pages` to get all pages
- Use Webflow MCP's `element_tool` with action `get_all_elements` to get detailed element information (requires Designer)
- Use Webflow MCP's `element_tool` with action `add_or_update_attribute` to fix accessibility issues (requires Designer)
- Use Webflow MCP's `element_snapshot_tool` to get visual previews of elements
- DO NOT use any other tools or methods for Webflow operations
- All tool calls must include the required `context` parameter (15-25 words, third-person perspective)
- **Designer connection required** - This skill needs Designer to access element attributes and styles

## Instructions

### Phase 1: Site & Page Selection
1. **Get site information**: Use Webflow MCP's `data_sites_tool` with action `list_sites` to identify target site
2. **Ask for page selection**:
   - If user provides page ID, use it directly
   - Otherwise, use `data_pages_tool` with action `list_pages` to show available pages
   - Let user select which page(s) to audit
3. **Confirm audit scope**: Ask user what to check:
   - Full audit (all accessibility checks)
   - Critical issues only (WCAG Level A)
   - Specific categories (forms, buttons, navigation, etc.)

### Phase 2: Element Extraction & Analysis
4. **Ensure Designer is connected**: Before proceeding, verify Webflow Designer is open and connected
   - If not connected, instruct user to open Designer and connect
   - This is required to access element attributes and styles
5. **Switch to target page**: Use `de_page_tool` with action `switch_page` to navigate to the page being audited
6. **Extract all elements**: Use `element_tool` with action `get_all_elements` for detailed analysis
   - Set `include_style_properties: true` to check focus styles
   - Set `include_all_breakpoint_styles: false` to minimize data
7. **Parse element data**: Identify interactive and content elements:
   - Buttons (Button, LinkBlock with button role)
   - Links (TextLink, Link, LinkBlock)
   - Form inputs (Input, Select, Textarea)
   - Headings (Heading elements with levels)
   - Interactive divs/spans (check for onClick or interactive roles)
   - Images (Image elements) - **SKIP for this audit**
8. **Extract attributes for each element**:
   - ARIA attributes (aria-label, aria-describedby, role, tabIndex)
   - DOM attributes (id, domId, href, type, placeholder)
   - Text content
   - Style properties (outline, border for focus states)
   - Element metadata (canHaveAttributes, tag name)

### Phase 3: Accessibility Checks

#### Critical Issues (Must Fix - WCAG Level A)
9. **Icon-only buttons without labels** (WCAG 4.1.2)
   - Find: Button elements with no text content
   - Check: Missing `aria-label` or `aria-labelledby`
   - Impact: Screen readers cannot identify button purpose
   - Fix: Add `aria-label` attribute with descriptive text

10. **Form inputs without labels** (WCAG 1.3.1)
    - Find: Input, Select, Textarea elements
    - Check: Missing associated label or `aria-label`
    - Impact: Users don't know what input is for
    - Fix: Add `aria-label` or associate with `<label>` using `id`

11. **Non-semantic click handlers** (WCAG 2.1.1)
    - Find: Div or Span elements (identified by element type)
    - Check: Interactive behavior without proper role/keyboard support
    - Impact: Not keyboard accessible, screen readers miss interactivity
    - Fix: Add `role="button"`, `tabIndex="0"`, suggest using real `<button>`

12. **Links without destination** (WCAG 2.1.1)
    - Find: Link elements with no `href` attribute
    - Check: Links that only use onClick without href
    - Impact: Not keyboard accessible, breaks browser features
    - Fix: Add proper `href` or convert to button

#### Serious Issues (Should Fix - WCAG Level AA)
13. **Focus outline removed without replacement** (WCAG 2.4.7)
    - Find: Elements with `outline: none` style
    - Check: No visible alternative focus indicator
    - Impact: Keyboard users can't see focus
    - Fix: Add visible focus style (border, box-shadow, background change)

14. **Missing keyboard handlers** (WCAG 2.1.1)
    - Find: Elements with onClick handlers
    - Check: Missing onKeyDown for Enter/Space keys
    - Impact: Not usable with keyboard alone
    - Fix: Add keyboard event handlers

15. **Touch target too small** (WCAG 2.5.5)
    - Find: Clickable elements (buttons, links)
    - Check: Width or height < 44px
    - Impact: Hard to tap on mobile devices
    - Fix: Increase padding or min-width/min-height to 44px

#### Moderate Issues (Consider Fixing)
16. **Heading hierarchy problems** (WCAG 1.3.1)
    - Find: Heading elements (h1-h6)
    - Check: Skipped levels (h1 → h3, skipping h2)
    - Impact: Confusing document structure
    - Fix: Use proper sequential heading levels

17. **Positive tabIndex** (WCAG 2.4.3)
    - Find: Elements with tabIndex > 0
    - Check: Disrupts natural tab order
    - Impact: Confusing keyboard navigation
    - Fix: Use tabIndex="0" or "-1" only, let natural DOM order work

18. **Role without required attributes** (WCAG 4.1.2)
    - Find: Elements with ARIA roles
    - Check: Missing required ARIA attributes (e.g., role="button" without tabIndex)
    - Impact: Incomplete accessibility semantics
    - Fix: Add required attributes for role

### Phase 4: Issue Categorization & Scoring
19. **Categorize all findings**:
    - Critical: Must fix (blocks access)
    - Serious: Should fix (significantly impacts usability)
    - Moderate: Consider fixing (improves experience)

20. **Calculate accessibility score** (0-100):
    - Start at 100
    - Critical issue: -10 points each
    - Serious issue: -5 points each
    - Moderate issue: -2 points each
    - Minimum score: 0

21. **Generate severity summary**:
    - Total issues found
    - Breakdown by severity
    - Most common issue types
    - Pages/sections most affected

### Phase 5: Report Generation
22. **Create detailed report** with specific format:
    ```
    ═══════════════════════════════════════════════════
    ACCESSIBILITY AUDIT: [Page Name]
    ═══════════════════════════════════════════════════

    CRITICAL (X issues)
    ───────────────────
    [A11Y] Element: Button "Submit"
      Issue: Button missing accessible name
      Location: Form section, element ID: {component: "abc", element: "xyz"}
      Current: <button><CloseIcon /></button>
      Fix: Add aria-label="Close"
      WCAG: 4.1.2 Name, Role, Value

    [A11Y] Element: Input field
      Issue: Form input without label
      Location: Contact form, element ID: {component: "def", element: "uvw"}
      Current: <input type="email" />
      Fix: Add aria-label="Email address" or associate with <label>
      WCAG: 1.3.1 Info and Relationships

    SERIOUS (X issues)
    ──────────────────
    [A11Y] Element: Link "Read more"
      Issue: Focus outline removed without visible alternative
      Location: Blog section
      Current: outline: none
      Fix: Add visible focus style (e.g., border: 2px solid blue)
      WCAG: 2.4.7 Focus Visible

    MODERATE (X issues)
    ───────────────────
    [A11Y] Element: Heading
      Issue: Heading hierarchy skipped (h1 → h3)
      Location: Article section
      Current: <h3>Subsection</h3> after <h1>Title</h1>
      Fix: Change to <h2> or add intermediate h2
      WCAG: 1.3.1 Info and Relationships

    ═══════════════════════════════════════════════════
    SUMMARY
    ───────────────────────────────────────────────────
    Total Issues: X
    - Critical: X issues
    - Serious: X issues
    - Moderate: X issues

    Accessibility Score: XX/100

    Most Common Issues:
    1. [Issue type] - X occurrences
    2. [Issue type] - X occurrences
    3. [Issue type] - X occurrences
    ═══════════════════════════════════════════════════
    ```

23. **Provide actionable insights**:
    - Prioritized fix list (critical first)
    - Quick wins (easy fixes with big impact)
    - Design pattern recommendations
    - Resources for learning more

### Phase 6: Fix Suggestions & Approval (Optional)
24. **Offer to fix issues automatically**: Designer is already connected, so offer auto-fixes
25. **Show preview of fixes**:
    ```
    Which issues would you like to fix?

    [1] ✓ Add aria-label to Submit button
        Element: Button in contact form
        Fix: Add aria-label="Submit contact form"
        Safe: Yes (adding attribute only)

    [2] ✓ Add aria-label to email input
        Element: Input in contact form
        Fix: Add aria-label="Email address"
        Safe: Yes

    [3] ⚠️ Fix heading hierarchy
        Element: h3 in article section
        Fix: Change heading level from h3 to h2
        Safe: May affect visual styling

    Type numbers to skip (e.g., "3"), "all" for all, "none" to cancel
    ```

26. **Apply approved fixes**: Use `element_tool` with action `add_or_update_attribute`
    - Process in batches
    - Show progress for large fix sets
    - Report success/failure for each

27. **Generate post-fix report**:
    - Issues fixed: X
    - Issues remaining: Y
    - New accessibility score: XX/100 (improved from YY/100)

### Phase 7: Export & Resources (Optional)
28. **Offer export formats**:
    - Markdown (readable documentation)
    - JSON (machine-readable for tracking)
    - CSV (spreadsheet for team review)

29. **Provide resources**:
    - WCAG 2.1 quick reference links
    - Webflow accessibility best practices
    - Recommended testing tools (browser extensions, screen readers)

## Important Considerations

### What This Skill Checks
✅ Button accessibility (labels, roles)
✅ Form input labels and associations
✅ Link semantics and keyboard access
✅ Focus visibility and keyboard navigation
✅ Heading hierarchy and structure
✅ ARIA roles and attributes
✅ Touch target sizes
✅ Interactive element semantics

### What This Skill Does NOT Check
❌ Image alt text (use **asset-audit** skill instead)
❌ Color contrast ratios (requires visual analysis)
❌ Animation/motion preferences
❌ Screen reader testing (needs manual verification)
❌ Content readability (language level, clarity)

### Limitations
- Cannot detect visual-only issues (color contrast, small text)
- Cannot test actual screen reader behavior
- Cannot validate content quality or clarity
- Relies on element attributes and structure only

## Examples

### Example 1: Full Page Audit

**User prompt:**
```
Run an accessibility audit on my homepage
```

**Step 1: Site & Page Selection**
```
🔍 Accessibility Audit: Page Selection

I'll help you audit your homepage for accessibility issues.

First, let me get your site information...

Available sites:
1. Company Website
2. Portfolio Site

Which site? (1/2)
```

**User response:** `1`

**Step 2: Page Selection**
```
Available pages in Company Website:
1. Home (/)
2. About (/about)
3. Contact (/contact)
4. Blog (/blog)

Which page would you like to audit? (1 for Home)
```

**User response:** `1`

**Step 3: Audit Scope**
```
What level of audit would you like?

1. Full audit (all WCAG checks) - Recommended
2. Critical issues only (Level A compliance)
3. Specific categories (buttons, forms, navigation)

Your choice: (1/2/3)
```

**User response:** `1`

**Step 4: Audit Progress**
```
🔄 Running Accessibility Audit...

Progress:
✅ Extracted page content (45 elements)
✅ Analyzing buttons and interactive elements
✅ Checking form inputs and labels
✅ Validating heading hierarchy
✅ Checking keyboard navigation
🔄 Analyzing focus states...

Analysis complete!
```

**Step 5: Report**
```
═══════════════════════════════════════════════════
ACCESSIBILITY AUDIT: Home
═══════════════════════════════════════════════════

CRITICAL (3 issues)
───────────────────
[A11Y] Element: Button (navigation toggle)
  Issue: Icon-only button missing accessible name
  Location: Header navigation
  Element ID: {component: "nav-01", element: "btn-menu"}
  Current: <button><MenuIcon /></button>
  Fix: Add aria-label="Open navigation menu"
  WCAG: 4.1.2 Name, Role, Value

[A11Y] Element: Input (email subscription)
  Issue: Form input without label
  Location: Footer, newsletter signup
  Element ID: {component: "footer-01", element: "email-input"}
  Current: <input type="email" placeholder="Enter email" />
  Fix: Add aria-label="Email address for newsletter"
  WCAG: 1.3.1 Info and Relationships

[A11Y] Element: Div (clickable card)
  Issue: Non-semantic interactive element
  Location: Services section, card 2
  Element ID: {component: "services-01", element: "card-02"}
  Current: <div onClick={...}>Service card</div>
  Fix: Convert to <button> or add role="button" + tabIndex="0"
  WCAG: 2.1.1 Keyboard

SERIOUS (5 issues)
──────────────────
[A11Y] Element: Link "Learn more"
  Issue: Focus outline removed without visible alternative
  Location: Hero section
  Element ID: {component: "hero-01", element: "cta-link"}
  Current: outline: none
  Fix: Add focus style - border: 2px solid #0066cc or box-shadow
  WCAG: 2.4.7 Focus Visible

[A11Y] Element: Button "Subscribe"
  Issue: Touch target too small (30px × 36px)
  Location: Footer newsletter form
  Element ID: {component: "footer-01", element: "submit-btn"}
  Current: Small button
  Fix: Increase padding or set min-height: 44px
  WCAG: 2.5.5 Target Size

[continues with 3 more serious issues...]

MODERATE (4 issues)
───────────────────
[A11Y] Element: Heading "Our Services"
  Issue: Heading hierarchy skipped (h1 → h3)
  Location: Services section
  Element ID: {component: "services-01", element: "heading"}
  Current: <h3>Our Services</h3> follows <h1>Welcome</h1>
  Fix: Change to <h2> to maintain proper hierarchy
  WCAG: 1.3.1 Info and Relationships

[continues with 3 more moderate issues...]

═══════════════════════════════════════════════════
SUMMARY
───────────────────────────────────────────────────
Total Issues: 12
- Critical: 3 issues (must fix)
- Serious: 5 issues (should fix)
- Moderate: 4 issues (consider fixing)

Accessibility Score: 64/100

Most Common Issues:
1. Missing button labels - 2 occurrences
2. Focus styles removed - 3 occurrences
3. Heading hierarchy problems - 2 occurrences

Quick Wins (Easy + High Impact):
✨ Add aria-label to icon buttons (2 min, +20 score points)
✨ Add input labels (5 min, +10 score points)
✨ Add focus styles (10 min, +15 score points)

═══════════════════════════════════════════════════

💡 Next Steps:
1. Fix critical issues first (blocks access for some users)
2. Add visible focus styles for keyboard users
3. Test with keyboard navigation (Tab, Enter, Space keys)
4. Consider testing with screen reader (NVDA/JAWS/VoiceOver)

Would you like me to help fix these issues? (requires Designer connection)
```

### Example 2: Multi-Page Audit

**User prompt:**
```
Audit accessibility across my entire site
```

**Agent response:**
```
🔍 Multi-Page Accessibility Audit

I'll audit all pages on your site for accessibility issues.

Found 8 pages:
1. Home
2. About
3. Services
4. Team
5. Blog
6. Blog Post Template (CMS)
7. Contact
8. Privacy Policy

This will take approximately 2-3 minutes.

Proceed with full site audit? (yes/no)
```

**User:** `yes`

**Progress:**
```
🔄 Auditing Site Accessibility...

Progress: ████████████░░░░░░░░ 60% (5/8 pages)

✅ Home - Score: 64/100 (12 issues)
✅ About - Score: 78/100 (6 issues)
✅ Services - Score: 71/100 (9 issues)
✅ Team - Score: 85/100 (4 issues)
✅ Blog - Score: 82/100 (5 issues)
🔄 Analyzing Blog Post Template...
```

**Final Report:**
```
═══════════════════════════════════════════════════
SITE-WIDE ACCESSIBILITY AUDIT
═══════════════════════════════════════════════════

OVERALL SCORE: 73/100

Pages Audited: 8
Total Issues: 48
- Critical: 11 issues
- Serious: 21 issues
- Moderate: 16 issues

═══════════════════════════════════════════════════
ISSUES BY PAGE
═══════════════════════════════════════════════════

🔴 Lowest Scores (Need Attention):
1. Home - 64/100 (12 issues: 3 critical, 5 serious, 4 moderate)
2. Services - 71/100 (9 issues: 2 critical, 5 serious, 2 moderate)
3. About - 78/100 (6 issues: 1 critical, 3 serious, 2 moderate)

🟢 Highest Scores:
1. Team - 85/100 (4 issues: 0 critical, 2 serious, 2 moderate)
2. Blog - 82/100 (5 issues: 1 critical, 2 serious, 2 moderate)

═══════════════════════════════════════════════════
SITE-WIDE PATTERNS
═══════════════════════════════════════════════════

Most Common Issues Across Site:
1. Missing button labels (icon buttons) - 8 occurrences
   Pages affected: Home, Services, Blog, Contact

2. Focus outline removed - 12 occurrences
   Pages affected: All pages (site-wide CSS issue)

3. Form inputs without labels - 5 occurrences
   Pages affected: Home, Contact

4. Small touch targets (<44px) - 9 occurrences
   Pages affected: Home, About, Services, Contact

═══════════════════════════════════════════════════
RECOMMENDATIONS
═══════════════════════════════════════════════════

🎯 Site-Wide Fixes (Fix Once, Helps Everywhere):
1. Add focus styles to global CSS (affects 12 issues across all pages)
2. Update button component to require aria-label (affects 8 issues)
3. Increase minimum touch target size in design system (affects 9 issues)

📋 Page-Specific Priorities:
1. Home page: Fix navigation menu button and newsletter form
2. Services page: Add labels to service card interactions
3. Contact page: Add proper labels to all form inputs

💡 Design System Improvements:
- Create accessible button component with required aria-label
- Add focus state variants to all interactive components
- Set minimum touch target size standard (44px)

Would you like:
1. Detailed report for specific page
2. Export findings to file (Markdown/JSON/CSV)
3. Help fixing site-wide issues (requires Designer)
```

### Example 3: Critical Issues Only

**User prompt:**
```
Check my contact page for critical accessibility issues only
```

**Agent response:**
```
🔍 Critical Issues Audit: Contact Page

Running quick scan for blocking accessibility issues...

✅ Page analyzed

═══════════════════════════════════════════════════
CRITICAL ISSUES: Contact Page
═══════════════════════════════════════════════════

Found: 4 critical issues

[1] Form Input Missing Label
    Element: Email input field
    Location: Contact form, top
    Issue: No accessible name for screen readers
    Fix: Add aria-label="Your email address"
    WCAG: 1.3.1 (Level A)

[2] Form Input Missing Label
    Element: Message textarea
    Location: Contact form, bottom
    Issue: No accessible name for screen readers
    Fix: Add aria-label="Your message"
    WCAG: 1.3.1 (Level A)

[3] Button Missing Label
    Element: Submit button
    Location: Contact form, bottom
    Issue: Icon-only button with no text
    Fix: Add aria-label="Submit contact form"
    WCAG: 4.1.2 (Level A)

[4] Non-Semantic Interactive Element
    Element: Social media link (Instagram)
    Location: Footer
    Issue: Div with onClick instead of proper link
    Fix: Convert to <a href="..."> with aria-label="Instagram"
    WCAG: 2.1.1 (Level A)

═══════════════════════════════════════════════════

⚠️ Impact: These issues prevent screen reader users from using your contact form.

🔧 Estimated fix time: 5 minutes

Would you like me to:
1. Run full audit (includes serious and moderate issues)
2. Fix these 4 critical issues now (requires Designer)
3. Export this report (Markdown/JSON/CSV)
```

## Safety Rules

### Preview & Confirmation
- Always show detailed issue list before suggesting fixes
- Clearly mark severity levels (critical/serious/moderate)
- Explain impact of each issue in user-friendly terms
- Provide specific WCAG reference for each finding

### Granular Approval for Fixes
- Allow user to select which issues to fix
- Warn about fixes that might affect visual design
- Process fixes in batches with progress indicators
- Report success/failure for each fix attempt

### Error Handling
- If page cannot be accessed, explain clearly
- If Designer not connected, list limitations
- If element cannot be modified, suggest manual fix
- Separate automated fixes from manual review items

### Validation
- Verify element types before suggesting fixes
- Check if element supports attributes before adding
- Test that suggested fixes are valid for element type
- Warn if fix might break existing functionality

## Output Standards

### Icons & Formatting
- 🔍 Discovery/Analysis
- 🔄 Processing
- ✅ Pass/Success
- ❌ Fail/Critical Issue
- ⚠️ Warning/Serious Issue
- 💡 Suggestion/Moderate Issue
- 📊 Report/Summary
- 🎯 Priority/Action Item
- 🔴 Critical Priority
- 🟡 Medium Priority
- 🟢 Low Priority

### Report Structure
1. Clear severity categorization
2. Specific element identification with IDs
3. Current state vs recommended fix
4. WCAG reference for each issue
5. Summary with actionable priorities
6. Score for measurable progress

### Communication
- Use clear, jargon-free language
- Explain WHY something is an issue (impact on users)
- Provide specific, actionable fixes
- Encourage testing with real assistive technology
- Emphasize that automated checks are just the start

## Resources to Include

### WCAG 2.1 Quick Reference
- https://www.w3.org/WAI/WCAG21/quickref/

### Webflow Accessibility Resources
- Webflow University: Accessibility best practices
- Using semantic HTML in Webflow
- Adding ARIA attributes in Webflow

### Testing Tools
- Keyboard: Tab, Shift+Tab, Enter, Space
- Screen readers: NVDA (Windows), JAWS, VoiceOver (Mac/iOS)
- Browser extensions: axe DevTools, WAVE, Lighthouse

### Common Fixes
- Button labels: Always include visible text or aria-label
- Form labels: Use Webflow's label element or aria-label
- Focus styles: Use :focus-visible pseudo-class
- Semantic HTML: Use proper elements (button, a, label)
