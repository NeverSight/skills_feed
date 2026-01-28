---
name: one-pager-prd
description: Use when proposing new features/products, documenting product requirements, creating concise specs for stakeholder alignment, pitching initiatives, scoping projects before detailed design, capturing user stories and success metrics, or when user mentions one-pager, PRD, product spec, feature proposal, product requirements, or brief.
---

# One-Pager PRD

## Table of Contents
- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [What Is It](#what-is-it)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

Create concise, decision-ready product specifications that align stakeholders on problem, solution, users, success metrics, and constraints—enabling fast approval and reducing back-and-forth.

## When to Use

**Early-Stage Product Definition:**
- Proposing new feature or product
- Need stakeholder alignment before building
- Scoping initiative for resource allocation
- Pitching idea to leadership for approval

**Documentation Needs:**
- Capturing requirements for engineering handoff
- Documenting decisions for future reference
- Creating spec for cross-functional team (PM, design, eng)
- Recording what's in/out of scope

**Communication:**
- Getting buy-in from multiple stakeholders
- Explaining complex feature simply
- Aligning sales/marketing on upcoming releases
- Onboarding new team members to initiative

**When NOT to Use:**
- Detailed technical design docs (use ADRs instead)
- Comprehensive product strategy (too high-level for one-pager)
- User research synthesis (different format)
- Post-launch retrospectives (use postmortem skill)

## What Is It

A one-pager PRD is a 1-2 page product specification covering:

**Core Elements:**
1. **Problem:** What user pain are we solving? Why now?
2. **Solution:** What are we building? (High-level approach)
3. **Users:** Who benefits? Personas, segments, use cases
4. **Goals & Metrics:** How do we measure success?
5. **Scope:** What's in/out? Key user flows
6. **Constraints:** Technical, business, timeline limits
7. **Open Questions:** Unknowns to resolve

**Format:**
- **One-Pager:** 1 page, bullet points, for quick approval
- **PRD (Product Requirements Document):** 1-2 pages, more detail, for execution

**Example One-Pager:**

**Feature:** Bulk Edit for Data Tables

**Problem:** Users managing 1000+ rows waste hours editing one-by-one. Competitors have bulk edit. Churn risk for power users.

**Solution:** Select multiple rows → Edit panel → Apply changes to all. Support: text, dropdowns, dates, numbers.

**Users:** Data analysts (15% of users, 60% of usage), operations teams.

**Goals:** Reduce time-to-edit by 80%. Increase retention of power users by 10%. Launch Q2.

**In Scope:** Select all, filter+select, edit common fields (5 field types).
**Out of Scope:** Undo/redo (v2), bulk delete (security concern).

**Metrics:** Time per edit (baseline: 5 min/row), adoption rate (target: 40% of power users in month 1).

**Constraints:** Must work with 10K rows without performance degradation.

**Open Questions:** Validation—fail entire batch or skip invalid rows?

## Workflow

Copy this checklist and track your progress:

```
One-Pager PRD Progress:
- [ ] Step 1: Gather context
- [ ] Step 2: Choose format
- [ ] Step 3: Draft one-pager
- [ ] Step 4: Validate quality
- [ ] Step 5: Review and iterate
```

**Step 1: Gather context**

Identify the problem (user pain, data supporting it), proposed solution (high-level approach), target users (personas, segments), success criteria (goals, metrics), and constraints (technical, business, timeline). See [Common Patterns](#common-patterns) for typical problem types.

**Step 2: Choose format**

For simple features needing quick approval → Use [resources/template.md](resources/template.md) one-pager format (1 page, bullets). For complex features/products requiring detailed requirements → Use [resources/template.md](resources/template.md) full PRD format (1-2 pages). For writing guidance and structure → Study [resources/methodology.md](resources/methodology.md) for problem framing, metric definition, scope techniques.

**Step 3: Draft one-pager**

Create `one-pager-prd.md` with: problem statement (user pain + why now), solution overview (what we're building), user personas and use cases, goals with quantified metrics, in-scope flows and out-of-scope items, constraints and assumptions, open questions to resolve. Keep concise—1 page for one-pager, 1-2 for PRD.

**Step 4: Validate quality**

Self-assess using [resources/evaluators/rubric_one_pager_prd.json](resources/evaluators/rubric_one_pager_prd.json). Check: problem is specific and user-focused, solution is clear without being overly detailed, metrics are measurable and have targets, scope is realistic and boundaries clear, constraints acknowledged, open questions identified. Minimum standard: Average score ≥ 3.5.

**Step 5: Review and iterate**

Share with stakeholders (PM, design, engineering, business). Gather feedback on problem framing, solution approach, scope boundaries, and success metrics. Iterate based on input. Get explicit sign-off before moving to detailed design/development.

## Common Patterns

### By Problem Type

**User Pain (Most Common):**
- **Pattern:** Users can't do X, causing friction Y
- **Example:** "Users can't search by multiple filters, forcing 10+ clicks to find items"
- **Validation:** User interviews, support tickets, analytics showing workarounds

**Competitive Gap:**
- **Pattern:** Competitor has feature, we don't, causing churn
- **Example:** "Competitors offer bulk actions. 20% of churned users cited this"
- **Validation:** Churn analysis, competitive analysis, win/loss interviews

**Strategic Opportunity:**
- **Pattern:** Market shift creates opening for new capability
- **Example:** "Remote work surge → need async collaboration features"
- **Validation:** Market research, early customer interest, trend analysis

**Technical Debt/Scalability:**
- **Pattern:** Current system doesn't scale, blocking growth
- **Example:** "Database queries timeout above 100K users. Growth blocked."
- **Validation:** Performance metrics, system capacity analysis

### By Solution Complexity

**Simple Feature (Weeks):**
- Clear requirements, minor scope
- Example: Add export to CSV button
- **One-Pager:** Problem, solution (1 sentence), metrics, constraints

**Medium Feature (Months):**
- Multiple user flows, some complexity
- Example: Commenting system with notifications
- **PRD:** Detailed flows, edge cases, phasing (MVP vs v2)

**Large Initiative (Quarters):**
- Cross-functional, strategic
- Example: Mobile app launch
- **Multi-Page PRD:** Break into phases, each with own one-pager

### By User Segment

**B2B SaaS:**
- Emphasize: ROI, admin controls, security, integrations
- Metrics: Adoption rate, time-to-value, NPS

**B2C Consumer:**
- Emphasize: Delight, ease of use, viral potential
- Metrics: Daily active users, retention curves, referrals

**Enterprise:**
- Emphasize: Compliance, customization, support
- Metrics: Deal size impact, deployment success, enterprise NPS

**Internal Tools:**
- Emphasize: Efficiency gains, adoption by teams
- Metrics: Time saved, task completion rate, employee satisfaction

## Guardrails

**Problem:**
- **Specific, not vague:** ❌ "Users want better search" → ✓ "Users abandon search after 3 failed queries (30% of sessions)"
- **User-focused:** Focus on user pain, not internal goals ("We want to increase engagement" is goal, not problem)
- **Validated:** Cite data (analytics, interviews, support tickets) not assumptions

**Solution:**
- **High-level, not over-specified:** Describe what, not how. Leave design/engineering latitude.
- **Falsifiable:** Clear enough that stakeholders can disagree or suggest alternatives
- **Scope-appropriate:** Don't design UI in one-pager. "Filter panel" not "Dropdown menu with checkbox multi-select"

**Metrics:**
- **Measurable:** Must be quantifiable. ❌ "Improve UX" → ✓ "Reduce time-to-complete from 5 min to 2 min"
- **Leading + Lagging:** Include both (leading: adoption rate, lagging: revenue impact)
- **Baselines + Targets:** Current state + goal. "Increase NPS from 40 to 55"

**Scope:**
- **Crisp boundaries:** Explicitly state what's in/out
- **MVP vs Future:** Separate must-haves from nice-to-haves
- **User flows:** Describe key happy path, edge cases

**Constraints:**
- **Realistic:** Acknowledge tech debt, dependencies, timeline limits
- **Trade-offs:** Explicit about what we're sacrificing (speed vs quality, features vs simplicity)

**Red Flags:**
- Solution looking for problem (built it because cool tech, not user need)
- Vague metrics (no baselines, no targets, no timeframes)
- Scope creep (everything is "must-have")
- No constraints mentioned (unrealistic optimism)
- No open questions (haven't thought deeply)

## Quick Reference

**Resources:**
- `resources/template.md` - One-pager and PRD templates with section guidance
- `resources/methodology.md` - Problem framing techniques, metric trees, scope prioritization, writing clarity
- `resources/evaluators/rubric_one_pager_prd.json` - Quality criteria

**Output:** `one-pager-prd.md` with problem, solution, users, goals/metrics, scope, constraints, open questions

**Success Criteria:**
- Problem is specific with validation (data/research)
- Solution is clear high-level approach (what, not how)
- Metrics are measurable with baselines + targets
- Scope has crisp in/out boundaries
- Constraints acknowledged
- Open questions identified
- Stakeholder sign-off obtained
- Score ≥ 3.5 on rubric

**Quick Decisions:**
- **Simple feature, quick approval?** → One-pager (1 page, bullets)
- **Complex feature, detailed handoff?** → Full PRD (1-2 pages)
- **Multiple phases?** → Separate one-pager per phase
- **Strategic initiative?** → Start with one-pager, expand to multi-page if needed

**Common Mistakes:**
1. Problem too vague ("improve experience")
2. Solution too detailed (specifying UI components)
3. No metrics or unmeasurable metrics
4. Scope creep (no "out of scope" section)
5. Ignoring constraints (unrealistic timelines)
6. No validation (assumptions not data)
7. Writing for yourself, not stakeholders

**Key Insight:**
Brevity forces clarity. If you can't explain it in 1-2 pages, you haven't thought it through. One-pager is thinking tool as much as communication tool.

**Format Tips:**
- Use bullets, not paragraphs (scannable)
- Lead with problem (earn the right to propose solution)
- Quantify everything possible (numbers > adjectives)
- Make scope boundaries explicit (prevent misunderstandings)
- Surface open questions (show you've thought deeply)

**Stakeholder Adaptation:**
- **For Execs:** Emphasize business impact, metrics, resource needs
- **For Engineering:** Technical constraints, dependencies, phasing
- **For Design:** User flows, personas, success criteria
- **For Sales/Marketing:** Competitive positioning, customer value, launch timing
