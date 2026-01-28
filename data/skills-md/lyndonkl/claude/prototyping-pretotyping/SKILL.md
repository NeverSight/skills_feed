---
name: prototyping-pretotyping
description: Use when testing ideas cheaply before building (pretotyping with fake doors, concierge MVPs, paper prototypes) to validate desirability/feasibility, choosing appropriate prototype fidelity (paper/clickable/coded), running experiments to test assumptions (demand, pricing, workflow), or when user mentions prototype, MVP, fake door test, concierge, Wizard of Oz, landing page test, smoke test, or asks "how can we validate this idea before building?".
---
# Prototyping & Pretotyping

## Table of Contents
1. [Purpose](#purpose)
2. [When to Use](#when-to-use)
3. [What Is It?](#what-is-it)
4. [Workflow](#workflow)
5. [Common Patterns](#common-patterns)
6. [Fidelity Ladder](#fidelity-ladder)
7. [Guardrails](#guardrails)
8. [Quick Reference](#quick-reference)

## Purpose

Test assumptions and validate ideas before investing in full development. Use cheapest/fastest method to answer key questions: Do people want this? Will they pay? Can we build it? Does it solve the problem? Pretotype (test idea with minimal implementation) before prototype (build partial version) before product (build full version).

## When to Use

**Use this skill when:**

- **High uncertainty**: Unvalidated assumptions about customer demand, willingness to pay, or technical feasibility
- **Before building**: Need evidence before committing resources to full development
- **Feature prioritization**: Multiple ideas, limited resources, want data to decide
- **Pivot evaluation**: Considering major direction change, need quick validation
- **Stakeholder buy-in**: Need evidence to convince execs/investors idea is worth pursuing
- **Pricing uncertainty**: Don't know what customers will pay
- **Workflow validation**: Unsure if proposed solution fits user mental model
- **Technical unknowns**: New technology, integration, or architecture approach needs validation

**Common triggers:**
- "Should we build this feature?"
- "Will customers pay for this?"
- "Can we validate demand before building?"
- "What's the cheapest way to test this idea?"
- "How do we know if users want this?"

## What Is It?

**Pretotyping** (Alberto Savoia): Test if people want it BEFORE building it
- Fake it: Landing page, "Buy Now" button that shows "Coming Soon", mockup videos
- Concierge: Manually deliver service before automating (e.g., manually curate results before building algorithm)
- Wizard of Oz: Appear automated but human-powered behind scenes

**Prototyping**: Build partial/simplified version to test assumptions
- **Paper prototype**: Sketches, wireframes (test workflow/structure)
- **Clickable prototype**: Figma/InVision (test interactions/flow)
- **Coded prototype**: Working software with limited features (test feasibility/performance)

**Example - Testing meal kit delivery service:**
- **Pretotype** (Week 1): Landing page "Sign up for farm-to-table meal kits, launching soon" → Measure sign-ups
- **Concierge MVP** (Week 2-4): Manually source ingredients, pack boxes, deliver to 10 sign-ups → Validate willingness to pay, learn workflow
- **Prototype** (Month 2-3): Build supplier database, basic logistics system for 50 customers → Test scalability
- **Product** (Month 4+): Full platform with automated sourcing, routing, subscription management

## Workflow

Copy this checklist and track your progress:

```
Prototyping Progress:
- [ ] Step 1: Identify riskiest assumption to test
- [ ] Step 2: Choose pretotype/prototype approach
- [ ] Step 3: Design and build minimum test
- [ ] Step 4: Run experiment and collect data
- [ ] Step 5: Analyze results and decide (pivot/persevere/iterate)
```

**Step 1: Identify riskiest assumption**

List all assumptions (demand, pricing, feasibility, workflow), rank by risk (probability of being wrong × impact if wrong). Test highest-risk assumption first. See [Common Patterns](#common-patterns) for typical assumptions by domain.

**Step 2: Choose approach**

Match test method to assumption and available time/budget. See [Fidelity Ladder](#fidelity-ladder) for choosing appropriate fidelity. Use [resources/template.md](resources/template.md) for experiment design.

**Step 3: Design and build minimum test**

Create simplest artifact that tests assumption (landing page, paper prototype, manual service delivery). See [resources/methodology.md](resources/methodology.md) for specific techniques (fake door, concierge, Wizard of Oz, paper prototyping).

**Step 4: Run experiment**

Deploy test, recruit participants, collect quantitative data (sign-ups, clicks, payments) and qualitative feedback (interviews, observations). Aim for minimum viable data (n=5-10 for qualitative, n=100+ for quantitative confidence).

**Step 5: Analyze and decide**

Compare results to success criteria (e.g., "10% conversion validates demand"). Decide: Pivot (assumption wrong, change direction), Persevere (assumption validated, build it), or Iterate (mixed results, refine and re-test).

## Common Patterns

**By assumption type:**

**Demand Assumption** ("People want this"):
- Test: Fake door (landing page with "Buy Now" → "Coming Soon"), pre-orders, waitlist sign-ups
- Success criteria: X% conversion, Y sign-ups in Z days
- Example: "10% of visitors sign up for waitlist in 2 weeks" → validates demand

**Pricing Assumption** ("People will pay $X"):
- Test: Price on landing page, offer with multiple price tiers, A/B test prices
- Success criteria: Z% conversion at target price
- Example: "5% convert at $49/mo" → validates pricing

**Workflow Assumption** ("This solves user problem in intuitive way"):
- Test: Paper prototype, task completion with clickable prototype
- Success criteria: X% complete task without help, <Y errors
- Example: "8/10 users complete checkout in <2 minutes with 0 errors" → validates workflow

**Feasibility Assumption** ("We can build/scale this"):
- Test: Technical spike, proof-of-concept with real data, manual concierge first
- Success criteria: Performance meets targets, costs within budget
- Example: "API responds in <500ms at 100 req/sec" → validates architecture

**Value Proposition Assumption** ("Customers prefer our approach over alternatives"):
- Test: A/B test messaging, fake door with different value props, competitor comparison
- Success criteria: X% choose our approach over alternative
- Example: "60% choose AI-powered vs manual curation" → validates differentiation

## Fidelity Ladder

**Choose appropriate fidelity for your question:**

**Level 0 - Pretotype (Hours to Days, $0-100):**
- **What**: Fake it before building anything real
- **When**: Test demand, pricing, value prop assumptions
- **Methods**: Landing page with sign-up, fake door test, manual concierge, video mockup
- **Example**: Dropbox video showing product before building it (3-4 min video, 70K→75K sign-ups overnight)
- **Pros**: Fastest, cheapest, tests real behavior (not opinions)
- **Cons**: Can't test workflow/usability in detail, ethical concerns if too deceptive

**Level 1 - Paper Prototype (Hours to Days, $0-50):**
- **What**: Hand-drawn sketches, printed screens, index cards
- **When**: Test workflow, information architecture, screen structure
- **Methods**: Users "click" on paper, you swap screens, observe confusion points
- **Example**: Banking app - 10 paper screens, users simulate depositing check, identify 3 workflow issues
- **Pros**: Very fast to iterate (redraw in minutes), forces focus on structure not polish
- **Cons**: Can't test real interactions (gestures, animations), feels "fake" to users

**Level 2 - Clickable Prototype (Days to Week, $100-500):**
- **What**: Interactive mockups in Figma, InVision, Adobe XD (no real code)
- **When**: Test user flow, UI patterns, interaction design
- **Methods**: Users complete tasks, measure success rate/time/errors, collect feedback
- **Example**: E-commerce checkout - 8 screens, 20 users, 15% abandon at shipping → fix before coding
- **Pros**: Looks real, easy to change, tests realistic interactions
- **Cons**: Can't test performance, scalability, backend complexity

**Level 3 - Coded Prototype (Weeks to Month, $1K-10K):**
- **What**: Working software with limited features, subset of data, shortcuts
- **When**: Test technical feasibility, performance, integration complexity
- **Methods**: Real users with real tasks, measure latency/errors, validate architecture
- **Example**: Search engine - 10K documents (not 10M), 50 users, <1s response time → validates approach
- **Pros**: Tests real technical constraints, reveals integration issues
- **Cons**: More expensive/time-consuming, harder to throw away if wrong

**Level 4 - Minimum Viable Product (Months, $10K-100K+):**
- **What**: Simplest version that delivers core value to real customers
- **When**: Assumptions mostly validated, ready for market feedback
- **Methods**: Launch to small segment, measure retention/revenue, iterate based on data
- **Example**: Instagram v1 - photo filters only (no video, stories, reels), launched to small group
- **Pros**: Real market validation, revenue, learning
- **Cons**: Expensive, longer timeline, public commitment

## Guardrails

**Ensure quality:**

1. **Test riskiest assumption first**: Don't test what you're confident about
   - ✓ "Will customers pay $X?" (high uncertainty) before "Can we make button blue?" (trivial)
   - ❌ Testing minor details before validating core value

2. **Match fidelity to question**: Don't overbuild for question at hand
   - ✓ Paper prototype for testing workflow (hours), coded prototype for testing latency (weeks)
   - ❌ Building coded prototype to test if users like color scheme (overkill)

3. **Set success criteria before testing**: Avoid confirmation bias
   - ✓ "10% conversion validates demand" (decided before test)
   - ❌ "7% conversion? That's pretty good!" (moving goalposts after test)

4. **Test with real target users**: Friends/family are not representative
   - ✓ Recruit from target segment (e.g., enterprise IT buyers for B2B SaaS)
   - ❌ Test with whoever is available (founder's friends who are polite)

5. **Observe behavior, not opinions**: What people do > what they say
   - ✓ "50% clicked 'Buy Now' but 0% completed payment" (real behavior → pricing/friction issue)
   - ❌ "Users said they'd pay $99/mo" (opinion, not reliable predictor)

6. **Be transparent about faking it**: Ethical pretotyping
   - ✓ "Sign up for early access" or "Launching soon" (honest)
   - ❌ Charging credit cards for fake product, promising features you won't build (fraud)

7. **Throw away prototypes**: Don't turn prototype code into production
   - ✓ Rebuild with proper architecture after validation
   - ❌ Ship prototype code (technical debt, security issues, scalability problems)

8. **Iterate quickly**: Multiple cheap tests > one expensive test
   - ✓ 5 paper prototypes in 1 week (test 5 approaches)
   - ❌ 1 coded prototype in 1 month (locked into one approach)

## Quick Reference

**Resources:**
- **Quick start**: [resources/template.md](resources/template.md) - Pretotype/prototype experiment template
- **Advanced techniques**: [resources/methodology.md](resources/methodology.md) - Fake door, concierge, Wizard of Oz, paper prototyping, A/B testing
- **Quality check**: [resources/evaluators/rubric_prototyping_pretotyping.json](resources/evaluators/rubric_prototyping_pretotyping.json) - Evaluation criteria

**Success criteria:**
- ✓ Identified 3-5 riskiest assumptions ranked by risk (prob wrong × impact if wrong)
- ✓ Tested highest-risk assumption with minimum fidelity needed
- ✓ Set quantitative success criteria before testing (e.g., "10% conversion")
- ✓ Recruited real target users (n=5-10 qualitative, n=100+ quantitative)
- ✓ Collected behavior data (clicks, conversions, task completion), not just opinions
- ✓ Results clear enough to make pivot/persevere/iterate decision
- ✓ Documented learning and shared with team

**Common mistakes:**
- ❌ Testing trivial assumptions before risky ones
- ❌ Overbuilding (coded prototype when landing page would suffice)
- ❌ No success criteria (moving goalposts after test)
- ❌ Testing with wrong users (friends/family, not target segment)
- ❌ Relying on opinions ("users said they liked it") not behavior
- ❌ Analysis paralysis (perfect prototype before testing)
- ❌ Shipping prototype code (technical debt disaster)
- ❌ Testing one thing when could test many (cheap tests run serially/parallel)

**When to use alternatives:**
- **A/B testing**: When have existing product/traffic, want to compare variations
- **Surveys**: When need quantitative opinions at scale (but remember: opinions ≠ behavior)
- **Customer interviews**: When understanding problem/context, not testing solution
- **Beta testing**: When product mostly built, need feedback on polish/bugs
- **Smoke test**: Same as pretotype (measure interest before building)
