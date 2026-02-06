---
name: cognitive-walkthrough
description: Deep-dive usability evaluation of specific user tasks. Simulates novice user cognition step-by-step to identify learnability issues, unclear actions, and points of confusion.
---

# Cognitive Walkthrough

This skill enables AI agents to perform a **task-specific usability evaluation** using the Cognitive Walkthrough method, a technique that simulates how users (especially novices) think through completing specific tasks in an interface.

Unlike broad heuristic evaluations, Cognitive Walkthrough provides deep analysis of particular user journeys, identifying where users get stuck, confused, or make errors.

Use this skill when you need granular, task-focused insights into learnability and ease of first use.

Combine with "Nielsen Heuristics" for general usability, "Don Norman Principles" for intuitive design, or "WCAG Accessibility" for inclusive access.

## When to Use This Skill

Invoke this skill when:
- Analyzing specific user tasks (e.g., "complete checkout", "upload a file")
- Evaluating learnability for first-time users
- Identifying points of confusion in a flow
- Debugging why users fail to complete tasks
- Assessing onboarding or critical user journeys
- Comparing alternative designs for the same task
- Preparing for usability testing (hypothesis generation)

## Inputs Required

When executing this walkthrough, gather:

- **task_description**: Specific task to evaluate (e.g., "Create a new account and add first item to wishlist") [REQUIRED]
- **user_persona**: Target user type (novice/intermediate/expert, demographics, goals, prior experience) [REQUIRED]
- **interface_description**: Description of the interface (web/mobile app, key features) [REQUIRED]
- **screenshots_or_prototype**: Visual references of the interface [OPTIONAL but highly recommended]
- **starting_point**: Where the task begins (e.g., "homepage", "logged-in dashboard") [OPTIONAL, defaults to common entry point]
- **success_criteria**: How to know task is complete [OPTIONAL, inferred from task if not specified]

## The Cognitive Walkthrough Method

Cognitive Walkthrough evaluates **four key questions** at each step:

### For Each Action in the Task:

**Q1: Will users try to achieve the right effect?**
- Do users understand what they need to do next?
- Is the goal of this step clear?
- Does it match their mental model of the task?

**Q2: Will users notice that the correct action is available?**
- Is the control/action visible?
- Can users find what they need to interact with?
- Is it discoverable without hunting?

**Q3: Will users associate the correct action with the effect they're trying to achieve?**
- Does the control's appearance/label suggest it will do what they want?
- Is there a clear connection between action and goal?
- Are affordances and signifiers clear?

**Q4: If the correct action is performed, will users see that progress is being made?**
- Is there immediate feedback?
- Does the system confirm the action succeeded?
- Can users tell they're closer to their goal?

## Walkthrough Procedure

Follow these steps systematically:

### Step 1: Define the Context (5 minutes)

1. **Identify the task:**
   - What is the user trying to accomplish?
   - What is the success criteria?
   - Example: "Add a product to cart and proceed to checkout"

2. **Define the user:**
   - Experience level: First-time user / Occasional user / Expert
   - Domain knowledge: Novice / Familiar / Expert
   - Technical proficiency: Low / Medium / High
   - Context: Desktop / Mobile / Tablet, Time pressure, Environment
   - Motivation: Why are they doing this task?

3. **Establish starting state:**
   - Where does the task begin? (homepage, search results, profile page)
   - What do users already know?
   - What are they thinking/feeling at the start?

### Step 2: Decompose the Task (10 minutes)

Break the task into **atomic actions** (smallest meaningful steps):

**Example Task:** "Create account and add item to wishlist"

1. Navigate to homepage
2. Find "Sign Up" or "Create Account" button
3. Click "Sign Up" button
4. Locate email field
5. Enter email address
6. Locate password field
7. Enter password
8. Click "Create Account" button
9. Wait for confirmation/redirect
10. Navigate to product page
11. Find "Add to Wishlist" button
12. Click "Add to Wishlist"
13. Confirm item was added

**Key principle:** Each action should be a single, observable user behavior.

### Step 3: Walk Through Each Action (30-60 minutes)

For **each action**, answer the 4 cognitive questions:

#### Action Template:

```markdown
## Action [N]: [Description]

**User's Goal at this step:** [What they're trying to accomplish]
**Current State:** [What they see/where they are]

### Q1: Will users try to achieve the right effect?
- **Analysis**: [Will users know what to do next?]
- **Issues**: [Problems if any]
- **Rating**: ✅ Clear / ⚠️ Unclear / ❌ Confusing

### Q2: Will users notice the correct action is available?
- **Analysis**: [Is the control visible/findable?]
- **Issues**: [Problems if any]
- **Rating**: ✅ Visible / ⚠️ Somewhat hidden / ❌ Hidden

### Q3: Will users associate action with intended effect?
- **Analysis**: [Does the control suggest what it does?]
- **Issues**: [Problems if any]
- **Rating**: ✅ Clear / ⚠️ Ambiguous / ❌ Misleading

### Q4: Will users see progress is being made?
- **Analysis**: [Is there feedback after the action?]
- **Issues**: [Problems if any]
- **Rating**: ✅ Clear feedback / ⚠️ Delayed/weak / ❌ No feedback

### Critical Issues Found:
- [Issue 1]
- [Issue 2]

### Recommendations:
- [Specific improvement 1]
- [Specific improvement 2]

---
```

### Step 4: Synthesize Findings (15 minutes)

After walking through all actions:

1. **Identify failure points:**
   - Where did multiple questions get ❌ or ⚠️ ratings?
   - Which steps are most likely to cause user confusion?
   - Where might users give up?

2. **Categorize issues:**
   - **Critical blockers**: Users likely can't complete task
   - **Major friction**: Users struggle significantly but may succeed
   - **Minor issues**: Small delays or confusion
   - **Cognitive load**: Mental effort required

3. **Calculate success likelihood:**
   - Estimate % of target users who would complete task on first try
   - Identify most common failure modes

4. **Prioritize improvements:**
   - Quick wins (easy fixes, high impact)
   - Major redesigns (complex fixes, high impact)
   - Nice-to-haves (easy fixes, low impact)

### Step 5: Generate Report (10 minutes)

Create comprehensive walkthrough report (see format below).

---

## Report Structure

```markdown
# Cognitive Walkthrough Report

**Task**: [Task description]
**User Persona**: [User type and characteristics]
**Interface**: [System/app being evaluated]
**Date**: [Date]
**Evaluator**: [AI Agent]

---

## Executive Summary

### Task Success Prediction
**Estimated Success Rate (First Attempt)**: [X]% of target users

### Critical Findings
1. [Most critical issue]
2. [Second critical issue]
3. [Third critical issue]

### Overall Assessment
[2-3 sentence summary of learnability]

---

## User Context

### Target User Profile
- **Experience Level**: [Novice/Intermediate/Expert]
- **Domain Knowledge**: [Description]
- **Technical Proficiency**: [Low/Medium/High]
- **Device/Context**: [Desktop/Mobile, environment]
- **Motivation**: [Why they're doing this]
- **Prior Experience**: [What they already know]

### Task Definition
**Goal**: [What user wants to accomplish]
**Success Criteria**: [How to know they succeeded]
**Starting Point**: [Where task begins]

---

## Step-by-Step Walkthrough

### Action 1: [Navigate to homepage]

**User's Goal**: Find where to start creating an account
**Current State**: User just arrived at homepage

#### Q1: Will users try to achieve the right effect?
- **Analysis**: Users typically look for "Sign Up", "Register", or "Create Account" in header/nav
- **Issues**: None expected - standard mental model
- **Rating**: ✅ Clear

#### Q2: Will users notice the correct action is available?
- **Analysis**: "Sign Up" button is in top-right corner of header (standard location)
- **Issues**: Small text (12px), low contrast (#999 on #FFF = 2.8:1)
- **Rating**: ⚠️ Somewhat hidden

#### Q3: Will users associate action with intended effect?
- **Analysis**: "Sign Up" is standard terminology, clearly indicates account creation
- **Issues**: None
- **Rating**: ✅ Clear

#### Q4: Will users see progress is being made?
- **Analysis**: N/A - no action taken yet (just viewing)
- **Issues**: N/A
- **Rating**: N/A

#### Critical Issues:
- **Low contrast on "Sign Up" button** - WCAG fail, hard to see
- Button is small (24px height) - mobile users may struggle

#### Recommendations:
1. Increase contrast to 4.5:1 minimum (WCAG AA)
2. Increase button size to 44px (touch target guideline)
3. Consider more prominent placement or visual weight

---

[Continue for all actions...]

---

## Failure Points Analysis

### Critical Blockers (Users likely to fail)

**1. Action 7: Create password with complexity requirements**
- **Problem**: Password requirements not shown until after submission fails
- **Impact**: Users guess rules, get frustrated by repeated errors
- **Affected Users**: 70-80% of novices
- **Severity**: Critical
- **Fix Priority**: P0 (Must fix)
- **Recommendation**: Show requirements inline before user types

**2. Action 12: Find "Add to Wishlist" button**
- **Problem**: Icon-only button (heart icon) with no label, not obvious
- **Impact**: Users don't see it or don't understand what it does
- **Affected Users**: 50-60% of first-time users
- **Severity**: High
- **Fix Priority**: P1 (Should fix)
- **Recommendation**: Add text label "Add to Wishlist" next to icon

### Major Friction Points

[Continue...]

### Minor Issues

[Continue...]

---

## Success Probability by User Type

| User Type | Estimated Success Rate | Time to Complete | Confidence |
|-----------|------------------------|------------------|------------|
| **Novice** | 45% | 8-12 minutes | Low frustration tolerance |
| **Intermediate** | 75% | 4-6 minutes | Moderate confidence |
| **Expert** | 95% | 2-3 minutes | High efficiency |

**Target**: Novices should have ≥80% success rate with ≤5 minutes time.

**Gap**: Current design falls short for novices by 35 percentage points.

---

## Cognitive Load Assessment

### Memory Burden
- **Items to remember**: [List what users must recall]
- **Rating**: Low / Medium / High
- **Issue**: [If high, explain why]

### Decision Points
- **Choices users make**: [Number and complexity]
- **Rating**: Low / Medium / High
- **Issue**: [Unnecessary decisions increase cognitive load]

### Error Recovery
- **How easy to fix mistakes**: [Analysis]
- **Rating**: Easy / Moderate / Difficult
- **Issue**: [Problems with undo/back/reset]

---

## Prioritized Recommendations

### Phase 1: Critical Fixes (1-2 weeks)

**1. Show password requirements inline (Action 7)**
- **Why**: Eliminates #1 failure point
- **Impact**: +25% success rate for novices
- **Effort**: Low (4 hours)

**2. Add text label to wishlist button (Action 12)**
- **Why**: Makes feature discoverable
- **Impact**: +15% task completion
- **Effort**: Low (2 hours)

**3. Increase "Sign Up" button contrast (Action 1)**
- **Why**: Accessibility + discoverability
- **Impact**: +10% users find starting point
- **Effort**: Low (1 hour)

**Total Phase 1 Impact**: +50% novice success rate (45% → 67.5%)

---

### Phase 2: Major Improvements (1-2 months)

[Continue with medium priority items...]

---

### Phase 3: Polish (3+ months)

[Continue with nice-to-have improvements...]

---

## Alternative Design Suggestions

Based on walkthrough findings, consider these alternative approaches:

### Alternative 1: Progressive Disclosure for Signup
**Current**: All fields shown at once
**Proposed**: Step-by-step (email → password → confirm)
**Pros**: Reduces cognitive load, clearer feedback per step
**Cons**: More clicks, may feel slower
**Recommendation**: A/B test with target users

### Alternative 2: Social Sign-Up
**Current**: Email/password only
**Proposed**: Add "Sign up with Google/Apple"
**Pros**: Faster, no password to remember
**Cons**: Privacy concerns, dependency on third-party
**Recommendation**: Offer as option alongside email signup

[Continue with other alternatives...]

---

## Comparison to Best Practices

| Practice | Current Implementation | Recommendation |
|----------|------------------------|----------------|
| Password requirements visibility | Hidden until error | Show inline before typing |
| Button sizing (mobile) | 24px | 44px minimum |
| Color contrast | 2.8:1 (WCAG fail) | 4.5:1 (WCAG AA) |
| Error messages | Generic | Specific and actionable |
| Confirmation feedback | Weak | Clear success messages |

---

## Next Steps

1. **Prioritize fixes**: Start with Phase 1 critical items
2. **Prototype improvements**: Create clickable mockups with changes
3. **User testing**: Validate findings with 5-8 target users
4. **Iterate**: Run another cognitive walkthrough after changes
5. **Monitor metrics**: Track task completion rates, time-on-task, error rates

---

## Methodology Notes

- **Method**: Cognitive Walkthrough (Wharton et al., 1994)
- **Evaluator**: AI agent simulating UX expert
- **Perspective**: Novice user (first-time, no training)
- **Limitations**:
  - Based on interface analysis, not actual user behavior
  - Success rates are estimates, not measured data
  - Should be validated with real user testing

---

## References

- Wharton, C., Rieman, J., Lewis, C., & Polson, P. (1994). "The Cognitive Walkthrough Method"
- Nielsen, J. (1994). "Heuristic Evaluation"
- Spencer, R. (2000). "The Streamlined Cognitive Walkthrough Method"

---

**Version**: 1.0
**Date**: [Date]
```

---

## Key Principles of Cognitive Walkthrough

### 1. Focus on Learnability
- Emphasis on first-time use, not expert performance
- "Can users figure it out?" vs. "Is it efficient?"

### 2. Question-Driven Analysis
- The 4 questions provide structured evaluation
- Every action is scrutinized from user perspective

### 3. Task-Specific
- Evaluates actual user goals, not general interface
- Deep dive vs. broad sweep

### 4. Theory-Grounded
- Based on cognitive psychology (information processing theory)
- Simulates human problem-solving process

### 5. Predictive Method
- Identifies issues before user testing
- Generates testable hypotheses

---

## Common Walkthrough Findings

### Typical Issues Discovered:

**Discoverability Problems:**
- Hidden buttons or controls
- Unlabeled icons
- Non-standard locations
- Poor visual hierarchy

**Unclear Affordances:**
- Links that don't look clickable
- Buttons that look disabled
- Confusing icon meanings
- Misleading labels

**Feedback Failures:**
- No confirmation after actions
- Unclear error messages
- No progress indicators
- Silent failures

**Mental Model Mismatches:**
- Unexpected behavior
- Counter-intuitive flows
- Inconsistent patterns
- Violates conventions

**Cognitive Load:**
- Too many choices
- Requiring memory of previous screens
- Complex multi-step processes
- Unclear next steps

---

## Success Metrics

Measure walkthrough effectiveness:

**Before Walkthrough:**
- Baseline task completion rate
- Average time on task
- Error rate
- User satisfaction scores

**After Implementing Fixes:**
- Improved completion rate (target: +20-40%)
- Reduced time on task (target: -30-50%)
- Lower error rate (target: -40-60%)
- Higher satisfaction (target: +1-2 points on 5-point scale)

---

## Combining with Other Methods

**Use cognitive walkthrough when:**
- You have specific tasks to evaluate
- You need deep, granular insights
- You're early in design (pre-user testing)
- You want to predict first-use issues

**Complement with:**
- **Nielsen Heuristics**: General usability issues
- **Don Norman Principles**: Intuitive design assessment
- **WCAG Audit**: Accessibility compliance
- **User Testing**: Validate predictions with real users
- **Analytics**: Quantitative validation (funnels, drop-off)

---

## Tips for Effective Walkthroughs

1. **Be specific about users**: "Novice" is better than "user"; "65+ non-tech-savvy" is even better
2. **Stay in character**: Think like the user, not the designer
3. **Document assumptions**: What does the user know? What don't they know?
4. **Be honest about issues**: Don't rationalize or excuse bad design
5. **Provide actionable recommendations**: "Unclear" → "Add tooltip explaining X"
6. **Quantify when possible**: "50% of users" vs. "some users"
7. **Consider context**: Time pressure, mobile vs. desktop, distractions
8. **Test assumptions**: Validate findings with actual users

---

## Version

1.0 - Initial release

---

**Remember**: Cognitive Walkthrough is a predictive method. While it's highly effective at identifying learnability issues, always validate findings with real users through usability testing.
