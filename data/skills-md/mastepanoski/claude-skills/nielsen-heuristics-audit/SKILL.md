---
name: nielsen-heuristics-audit
description: Evaluate UX/UI using Jakob Nielsen's 10 usability heuristics. Comprehensive audit of visibility, control, consistency, error prevention, recognition, flexibility, aesthetics, error recovery, and documentation.
---

# Nielsen Heuristics UX Audit

This skill enables AI agents to perform a comprehensive **usability evaluation** of apps, websites, or digital interfaces using **Jakob Nielsen's 10 Usability Heuristics**, the industry-standard framework for identifying usability problems.

These heuristics are battle-tested principles used by UX professionals worldwide to systematically evaluate interfaces and identify usability issues before user testing.

Use this skill to conduct thorough heuristic evaluations, prioritize usability improvements, and create actionable recommendations.

Combine with "Don Norman Principles Audit" for human-centered design assessment or "WCAG Accessibility" for inclusive design compliance.

## When to Use This Skill

Invoke this skill when:
- Conducting a systematic usability evaluation
- Identifying usability problems before user testing
- Auditing existing interfaces for improvement opportunities
- Prioritizing UX debt and technical improvements
- Training teams on usability best practices
- Comparing multiple design alternatives

## Inputs Required

When executing this audit, gather:

- **interface_description**: Detailed interface description (purpose, target users, key features, platform: web/mobile/desktop) [REQUIRED]
- **screenshots_or_links**: URLs of screenshots, prototypes, or live site/app [OPTIONAL]
- **user_flows**: Key user journeys to evaluate (e.g., "onboarding", "checkout", "search and filter") [OPTIONAL]
- **known_issues**: Existing bug reports or user complaints [OPTIONAL]
- **competitive_context**: Similar products or industry standards to compare against [OPTIONAL]

## The 10 Nielsen Heuristics

Evaluate against these principles established by Jakob Nielsen (Nielsen Norman Group):

### 1. Visibility of System Status
**The design should always keep users informed about what is going on, through appropriate feedback within a reasonable amount of time.**

**Check for:**
- Loading indicators and progress bars
- State changes (selected, active, disabled, hover)
- Confirmation messages after actions
- Current location indicators (breadcrumbs, active nav)
- Process completion status
- Background operations visibility

**Common violations:**
- Actions with no feedback
- Long processes without progress indication
- Unclear current page/section
- No confirmation of form submission

---

### 2. Match Between System and the Real World
**The design should speak the users' language. Use words, phrases, and concepts familiar to the user, rather than internal jargon. Follow real-world conventions.**

**Check for:**
- Plain language vs. technical jargon
- Familiar icons and metaphors
- Logical information order
- Cultural appropriateness
- Natural language date/time formats
- Industry-standard terminology

**Common violations:**
- Technical error messages
- Developer/internal terminology
- Unfamiliar icons without labels
- Illogical or arbitrary ordering

---

### 3. User Control and Freedom
**Users often perform actions by mistake. They need a clearly marked "emergency exit" to leave an unwanted action without having to go through an extended process.**

**Check for:**
- Undo/redo functionality
- Cancel buttons in multi-step processes
- Easy navigation back
- Exit options from modals/overlays
- Ability to edit before final submission
- Clear way to recover from errors

**Common violations:**
- No way to cancel operations
- Destructive actions without undo
- Forced completion of multi-step flows
- Modal traps with no escape

---

### 4. Consistency and Standards
**Users should not have to wonder whether different words, situations, or actions mean the same thing. Follow platform and industry conventions.**

**Check for:**
- Consistent terminology throughout
- Uniform visual design (colors, typography, spacing)
- Predictable interaction patterns
- Platform conventions (iOS/Android/Web)
- Internal consistency across sections
- Standard iconography

**Common violations:**
- Multiple names for same action
- Inconsistent button styles/positions
- Different patterns for similar tasks
- Breaking platform conventions

---

### 5. Error Prevention
**Good error messages are important, but the best designs carefully prevent problems from occurring in the first place. Eliminate error-prone conditions or check for them and present users with a confirmation option.**

**Check for:**
- Input validation and constraints
- Helpful input formatting (masks for phone/credit cards)
- Confirmation dialogs for destructive actions
- Auto-save functionality
- Disabled states preventing invalid actions
- Smart defaults

**Common violations:**
- No validation until form submission
- Easy to trigger destructive actions
- Accepting invalid inputs
- No warnings for risky operations

---

### 6. Recognition Rather Than Recall
**Minimize the user's memory load by making elements, actions, and options visible. The user should not have to remember information from one part of the interface to another.**

**Check for:**
- Visible navigation and menus
- Recently used items
- Auto-complete and suggestions
- Tooltips and contextual help
- Clear labels and instructions
- Persistent information when needed

**Common violations:**
- Hidden menus and mystery meat navigation
- Requiring memorization of codes/syntax
- No search history or recent items
- Unlabeled icons
- Information shown once then hidden

---

### 7. Flexibility and Efficiency of Use
**Shortcuts — hidden from novice users — may speed up the interaction for the expert user such that the design can cater to both inexperienced and experienced users.**

**Check for:**
- Keyboard shortcuts
- Customization options
- Bulk actions
- Advanced filters
- Quick actions/gestures
- Power user features
- Personalization

**Common violations:**
- One-size-fits-all approach
- No keyboard navigation
- Repetitive tasks with no shortcuts
- No way to customize workflow

---

### 8. Aesthetic and Minimalist Design
**Interfaces should not contain information that is irrelevant or rarely needed. Every extra unit of information competes with relevant units of information and diminishes their relative visibility.**

**Check for:**
- Clean, uncluttered layouts
- Progressive disclosure
- Appropriate white space
- Visual hierarchy
- Focus on primary actions
- Removal of unnecessary elements

**Common violations:**
- Information overload
- Too many options at once
- Cluttered interfaces
- Poor visual hierarchy
- Distracting elements

---

### 9. Help Users Recognize, Diagnose, and Recover from Errors
**Error messages should be expressed in plain language (no error codes), precisely indicate the problem, and constructively suggest a solution.**

**Check for:**
- Clear, human-readable error messages
- Specific problem identification
- Actionable solutions
- Inline validation
- Helpful error states
- Recovery options

**Common violations:**
- Generic error messages ("Error 500")
- Technical jargon in errors
- No guidance on fixing problems
- Errors that don't explain what went wrong

---

### 10. Help and Documentation
**It's best if the system doesn't need any additional explanation. However, it may be necessary to provide documentation to help users understand how to complete their tasks.**

**Check for:**
- Searchable help center
- Contextual help (tooltips, info icons)
- Onboarding tutorials
- Video walkthroughs
- FAQs for common tasks
- In-app guidance
- Contact support options

**Common violations:**
- No help available
- Outdated documentation
- Help not searchable
- Generic help not contextual to task

---

## Audit Procedure

Follow these steps systematically:

### Step 1: Preparation (10-15 minutes)

1. **Understand the context:**
   - Review `interface_description`, `screenshots_or_links`, and `user_flows`
   - Identify 5-7 key user tasks if not provided
   - Note target user personas and their goals

2. **Set up evaluation framework:**
   - Prepare heuristics checklist
   - Define severity rating scale
   - Identify critical user journeys

### Step 2: Heuristic-by-Heuristic Evaluation (30-60 minutes)

For each of the 10 heuristics:

1. **Examine** the interface against the heuristic
2. **Document violations** with:
   - Specific location (screen, component, step)
   - Description of the problem
   - Screenshot or reference
   - Affected user tasks
3. **Assign severity rating:**
   - **0 - Not a problem**: Not a usability issue
   - **1 - Cosmetic**: Fix if time permits
   - **2 - Minor**: Low priority fix
   - **3 - Major**: High priority fix
   - **4 - Catastrophic**: Imperative to fix before release
4. **Note positive examples**: What's working well
5. **Propose recommendations**: 2-3 specific, actionable solutions

### Step 3: Cross-Heuristic Analysis (10-15 minutes)

1. **Identify patterns:**
   - Multiple heuristics violated by same issue
   - Systemic problems vs. isolated issues
   - Root causes behind symptoms

2. **Prioritize issues:**
   - Severity × Frequency × Impact on critical tasks
   - Quick wins vs. long-term improvements
   - Group related problems

3. **Calculate metrics:**
   - Total issues by severity
   - Issues per heuristic
   - Overall usability score (optional)

### Step 4: Generate Comprehensive Report (15-20 minutes)

Create a structured, actionable report (see format below).

## Report Structure

```markdown
# Nielsen Heuristics UX Audit Report

**Interface**: [Name]
**Date**: [Date]
**Evaluator**: [AI Agent]
**Platform**: [Web/iOS/Android/Desktop]

---

## Executive Summary

### Overview
[2-3 sentence summary of interface and audit scope]

### Key Findings
- **Total Issues Found**: [X]
  - Catastrophic (4): [X]
  - Major (3): [X]
  - Minor (2): [X]
  - Cosmetic (1): [X]

### Top 3 Critical Issues
1. [Issue] - Severity [X] - Heuristic [#X]
2. [Issue] - Severity [X] - Heuristic [#X]
3. [Issue] - Severity [X] - Heuristic [#X]

### Overall Usability Score
[X/10] - [Excellent/Good/Fair/Poor]

---

## Detailed Findings by Heuristic

### H1: Visibility of System Status
**Compliance**: ⭐⭐⭐⚪⚪ (3/5)

#### Issues Found

**Issue 1.1: No loading indicator on search**
- **Severity**: 3 (Major)
- **Location**: Search page, after query submission
- **Description**: When users submit a search query, there's no visual feedback that the system is processing. Users may click multiple times, unsure if their action registered.
- **Affected Tasks**: Product search, filtering
- **Recommendation**:
  - Add a loading spinner or progress bar
  - Disable the search button during processing
  - Show "Searching..." text feedback

**Issue 1.2: [Next issue]**
[Continue...]

#### Positive Examples
- ✅ Clear active state on navigation items
- ✅ Badge notifications on new messages

---

[Repeat for all 10 heuristics]

---

## Prioritized Action Items

### Must Fix (Severity 4 & 3)
1. **[Issue]** - H[X]: [Heuristic name]
   - **Impact**: [Critical user task affected]
   - **Fix**: [Specific recommendation]
   - **Effort**: [Low/Medium/High]

### Should Fix (Severity 2)
[Continue...]

### Nice to Have (Severity 1)
[Continue...]

---

## Quick Wins
[Issues that are easy to fix but have decent impact]

## Long-term Improvements
[Systemic changes requiring more effort]

---

## Positive Highlights
[What's working well - reinforce good practices]

---

## Recommendations Summary

### Immediate Actions (1-2 weeks)
1. [Action]
2. [Action]

### Short-term (1-2 months)
1. [Action]
2. [Action]

### Long-term (3+ months)
1. [Action]
2. [Action]

---

## Next Steps
1. **Validate findings**: Conduct user testing on identified issues
2. **Prioritize fixes**: Align with product roadmap and business goals
3. **Track progress**: Re-audit after implementing changes
4. **Iterate**: Regular heuristic evaluations in design process

---

## Methodology Notes
- Evaluation method: Expert heuristic evaluation (Nielsen's 10 Heuristics)
- Evaluator: AI agent simulating UX expert
- Limitations: No actual user testing conducted; recommendations should be validated
- Complement with: User testing, analytics review, accessibility audit

---

## References
- Nielsen, J. (1994). "10 Usability Heuristics for User Interface Design"
- Nielsen Norman Group: https://www.nngroup.com/articles/ten-usability-heuristics/
```

## Severity Rating Guidelines

Use this scale consistently:

| Rating | Name | Description | Action |
|--------|------|-------------|--------|
| **4** | Catastrophic | Prevents task completion, causes data loss, or creates security issues | Fix immediately before release |
| **3** | Major | Significant frustration or frequent problem affecting key tasks | High priority fix |
| **2** | Minor | Occasional annoyance or affects secondary features | Medium priority |
| **1** | Cosmetic | Doesn't affect functionality, purely aesthetic | Fix if time permits |
| **0** | Not a problem | Not a usability issue | No action needed |

## Best Practices for Effective Audits

1. **Be Systematic**: Evaluate each heuristic thoroughly, don't skip
2. **Use Evidence**: Reference specific examples, screenshots, and flows
3. **Think Like Users**: Consider different user types (novice, expert, accessibility needs)
4. **Be Specific**: Vague findings like "poor UX" aren't actionable
5. **Propose Solutions**: Don't just identify problems, suggest fixes
6. **Prioritize Ruthlessly**: Not all issues are equal
7. **Consider Context**: Business constraints, technical limitations, user needs
8. **Stay Objective**: Base on heuristics, not personal preference
9. **Document Positives**: Highlight what's working well
10. **Recommend Testing**: Heuristic evaluation finds ~75% of issues; user testing finds the rest

## Common Patterns to Watch For

### High-Impact Issues
- Forms with poor validation (H5, H9)
- Unclear navigation and information architecture (H1, H6)
- Inconsistent interaction patterns (H4)
- No feedback on actions (H1)
- Destructive actions without confirmation (H3, H5)

### Quick Wins
- Adding loading indicators (H1)
- Improving error messages (H9)
- Adding tooltips to icons (H6)
- Consistent button styling (H4)
- Confirmation dialogs (H5)

### Systemic Issues
- Overall inconsistency in design system (H4)
- Poor information architecture (H6, H8)
- Lack of help/documentation (H10)
- No keyboard navigation (H7)

## Combining with Other Audits

**Complementary evaluations:**
- **Don Norman Principles**: Human-centered design fundamentals
- **WCAG Accessibility**: Inclusive design compliance
- **Cognitive Walkthrough**: Task-specific deep dive
- **Analytics Review**: Quantitative validation of issues
- **User Testing**: Qualitative validation with real users

## Tools and Templates

Consider recommending:
- **Heuristic Evaluation Spreadsheet**: Track issues systematically
- **Issue Tagging**: Label by heuristic, severity, component, user flow
- **Before/After Mockups**: Visualize proposed improvements
- **Severity × Frequency Matrix**: Prioritization framework

## Version

1.0 - Initial release

---

**Remember**: Heuristic evaluation is a discount usability method that finds many issues quickly, but should be combined with user testing for comprehensive insights. This is an expert evaluation simulation—validate with real users.
