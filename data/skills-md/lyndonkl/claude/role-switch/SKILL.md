---
name: role-switch
description: Use when stakeholders have conflicting priorities and need alignment, suspect decision blind spots from single perspective, need to pressure-test proposals before presenting, want empathy for different viewpoints (eng vs PM vs legal vs user), building consensus across functions, evaluating tradeoffs with multi-dimensional impact, or when user mentions "what would X think", "stakeholder alignment", "see from their perspective", "blind spots", or "conflicting interests".
---

# Role Switch

## Table of Contents
1. [Purpose](#purpose)
2. [When to Use](#when-to-use)
3. [What Is It](#what-is-it)
4. [Workflow](#workflow)
5. [Role Selection Patterns](#role-selection-patterns)
6. [Synthesis Principles](#synthesis-principles)
7. [Common Patterns](#common-patterns)
8. [Guardrails](#guardrails)
9. [Quick Reference](#quick-reference)

## Purpose

Role Switch helps uncover blind spots, align stakeholders, and make better decisions by systematically analyzing from multiple perspectives. It transforms single-viewpoint analysis into multi-stakeholder synthesis with explicit tradeoffs and alignment paths.

## When to Use

**Invoke this skill when you need to:**
- Align stakeholders with conflicting priorities (eng vs PM vs sales vs legal)
- Uncover blind spots in decisions by viewing from multiple angles
- Pressure-test proposals before presenting to diverse audiences
- Build empathy for perspectives different from your own
- Navigate cross-functional tradeoffs (cost vs quality, speed vs thoroughness)
- Evaluate decisions with multi-dimensional impact (technical, business, user, regulatory)
- Find consensus paths when positions seem incompatible
- Validate assumptions by seeing what different roles would challenge

**User phrases that trigger this skill:**
- "What would [stakeholder] think about this?"
- "How do we get alignment across teams?"
- "I'm worried we're missing something"
- "See this from their perspective"
- "Conflicting priorities between X and Y"
- "Stakeholder buy-in strategy"

## What Is It

A structured analysis that:
1. **Identifies relevant roles** (stakeholders with different goals, constraints, incentives)
2. **Adopts each perspective** (inhabits mindset, priorities, success criteria of that role)
3. **Articulates viewpoint** (what this role cares about, fears, values, measures)
4. **Surfaces tensions** (where perspectives conflict, tradeoffs emerge)
5. **Synthesizes alignment** (finds common ground, proposes resolutions, sequences decisions)

**Quick example (API versioning decision):**
- **Engineer**: "Deprecate v1 now—maintaining two versions doubles complexity and slows new features"
- **Product Manager**: "Keep v1 for 12 months—customers need migration time or we risk churn"
- **Customer Success**: "Offer v1→v2 migration service—customers value hand-holding over self-service docs"
- **Finance**: "Charge for extended v1 support—converts maintenance burden into revenue stream"
- **Synthesis**: Deprecate v1 in 12 months with 6-month free support + paid extended support option, PM owns migration docs + webinars, CS offers premium service

## Workflow

Copy this checklist and track your progress:

```
Role Switch Progress:
- [ ] Step 1: Frame the decision or situation
- [ ] Step 2: Select relevant roles
- [ ] Step 3: Inhabit each role's perspective
- [ ] Step 4: Surface tensions and tradeoffs
- [ ] Step 5: Synthesize alignment and path forward
```

**Step 1: Frame the decision or situation**

Clarify what's being decided, key constraints (time, budget, scope), and why alignment matters. See [Common Patterns](#common-patterns) for decision framing by type.

**Step 2: Select relevant roles**

Choose 3-6 roles with different goals, incentives, or constraints. See [Role Selection Patterns](#role-selection-patterns) for stakeholder mapping. For complex multi-stakeholder decisions → Study [resources/methodology.md](resources/methodology.md) for RACI + power-interest analysis.

**Step 3: Inhabit each role's perspective**

For each role, articulate: what they optimize for, what they fear, how they measure success, what constraints they face. Use [resources/template.md](resources/template.md) for structured analysis. For realistic roleplay → See [resources/methodology.md](resources/methodology.md) for cognitive empathy techniques.

**Step 4: Surface tensions and tradeoffs**

Identify where perspectives conflict, map incompatible goals, articulate explicit tradeoffs. See [Synthesis Principles](#synthesis-principles) for tension analysis.

**Step 5: Synthesize alignment and path forward**

Find common ground, propose resolutions that address core concerns, sequence decisions to build momentum. Self-check using [resources/evaluators/rubric_role_switch.json](resources/evaluators/rubric_role_switch.json). Minimum standard: Average score ≥ 3.5.

## Role Selection Patterns

**Classic product triad (most common):**
- **Engineering**: Feasibility, technical debt, system complexity, maintainability
- **Product**: User value, roadmap prioritization, market timing, feature completeness
- **Design**: User experience, accessibility, consistency, delight

**Business decision quads:**
- **Finance**: Cost, ROI, cash flow, unit economics, margin
- **Sales**: Customer acquisition, deal closure, competitive positioning, quota attainment
- **Marketing**: Brand perception, customer lifetime value, positioning, conversion funnel
- **Operations**: Scalability, process efficiency, risk management, resource utilization

**Regulatory/compliance contexts:**
- **Legal**: Risk mitigation, liability, contract terms, IP protection
- **Compliance**: Regulatory adherence, audit trail, policy enforcement, certification
- **Privacy/Security**: Data protection, threat model, access control, incident response
- **Ethics**: Fairness, transparency, stakeholder impact, values alignment

**External stakeholders:**
- **End Users**: Usability, reliability, cost, privacy, delight
- **Customers** (B2B): Integration ease, support quality, vendor stability, total cost of ownership
- **Partners**: Revenue share, mutual value, integration burden, strategic alignment
- **Regulators**: Public interest, safety, competition, transparency

## Synthesis Principles

**Finding common ground:**
1. **Shared goals**: What do all roles ultimately want? (e.g., company success, customer satisfaction)
2. **Compatible sub-goals**: Where do objectives align even if paths differ?
3. **Mutual fears**: What do all roles want to avoid? (e.g., reputational damage, security breach)

**Resolving conflicts:**
- **Sequential decisions**: "Do X first (satisfies role A), then Y (satisfies role B)" (e.g., pilot then scale)
- **Hybrid approaches**: Combine elements from multiple perspectives (e.g., freemium = marketing + finance)
- **Constraints as creativity**: Use one role's limits to sharpen another's solution (e.g., budget constraint forces prioritization)
- **Risk mitigation**: Address fears with safeguards (e.g., eng fears tech debt → schedule refactoring sprint)

**When perspectives are truly incompatible:**
- **Escalate decision**: Flag for leadership with clear tradeoff framing
- **Run experiment**: Pilot to gather data, convert opinions to evidence
- **Decouple decisions**: Split into multiple decisions with different owners
- **Accept tradeoff explicitly**: Document the choice and reasoning for future reference

## Common Patterns

**Pattern 1: Build vs Buy Decisions**
- **Roles**: Engineering (control, customization), Finance (TCO), Product (time-to-market), Legal (vendor risk), Operations (support burden)
- **Typical tensions**: Eng wants control, Finance sees build cost underestimation, PM sees opportunity cost of delay
- **Synthesis paths**: Pilot buy option with build fallback, build core/buy periphery, time-box build with buy backstop

**Pattern 2: Feature Prioritization**
- **Roles**: PM (roadmap vision), Engineering (technical feasibility), Design (UX quality), Sales (customer requests), Users (actual need)
- **Typical tensions**: Sales wants everything promised, Eng sees scope creep, Users want simplicity, PM balances all
- **Synthesis paths**: MoSCoW prioritization (must/should/could/won't), release in phases, v1 vs v2 scoping

**Pattern 3: Pricing Strategy**
- **Roles**: Finance (margin), Marketing (positioning), Sales (close rate), Customers (value perception), Product (feature gating)
- **Typical tensions**: Finance wants premium, Sales wants competitive, Marketing wants simple, Product wants value-based tiers
- **Synthesis paths**: Tiered pricing (serves multiple segments), usage-based (aligns value), anchoring (premium + standard)

**Pattern 4: Organizational Change (e.g., return-to-office)**
- **Roles**: Leadership (collaboration), Employees (flexibility), HR (retention), Finance (real estate cost), Managers (productivity)
- **Typical tensions**: Leadership sees serendipity loss, Employees see autonomy loss, Finance sees sunk cost, HR sees turnover
- **Synthesis paths**: Hybrid model (balance), role-based policy (nuance), trial periods (data-driven), opt-in incentives (voluntary)

**Pattern 5: Technical Migration**
- **Roles**: Engineering (technical improvement), PM (feature freeze), Users (potential downtime), DevOps (operational risk), Finance (ROI)
- **Typical tensions**: Eng sees long-term benefit, PM sees short-term cost, Users fear disruption, Finance wants ROI proof
- **Synthesis paths**: Incremental migration (reduce risk), feature parity first (minimize disruption), ROI projection (justify investment)

## Guardrails

**Avoid strawman perspectives:**
- Don't caricature roles (e.g., "Finance only cares about cost cutting")
- Inhabit perspective charitably—what's the *strongest* version of this viewpoint?
- Seek conflicting evidence to your own bias

**Distinguish position from interest:**
- **Position**: What they say they want (surface demand)
- **Interest**: Why they want it (underlying need)
- Example: "I want this feature" (position) because "customers are churning" (interest = retention)
- Synthesis works at interest level, not position level

**Acknowledge information asymmetry:**
- Some roles have context others lack (e.g., Legal sees confidential liability exposure)
- Flag assumptions: "If Legal has info we don't, that could change this analysis"
- Invite real stakeholders to validate your perspective-taking

**Don't replace actual stakeholder input:**
- Role-switch is for *preparing* conversations, not *replacing* them
- Use to pressure-test before presenting, not as substitute for gathering input
- Best used when stakeholder access is limited or to refine proposals before socializing

**Power dynamics matter:**
- Not all perspectives carry equal weight in decision-making (hierarchy, expertise, accountability)
- Synthesis should acknowledge who has decision authority
- Don't assume consensus is always possible or desirable

## Quick Reference

**Resources:**
- **Quick analysis**: [resources/template.md](resources/template.md)
- **Complex stakeholder mapping**: [resources/methodology.md](resources/methodology.md)
- **Quality rubric**: [resources/evaluators/rubric_role_switch.json](resources/evaluators/rubric_role_switch.json)

**5-Step Process**: Frame Decision → Select Roles → Inhabit Perspectives → Surface Tensions → Synthesize Alignment

**Role selection**: Choose 3-6 roles with different goals, incentives, constraints

**Synthesis principles**: Find shared goals, resolve conflicts (sequential, hybrid, constraints as creativity), escalate when incompatible

**Avoid**: Strawman perspectives, position vs interest confusion, replacing actual stakeholder input
