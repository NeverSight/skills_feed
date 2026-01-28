---
name: grant-proposal-assistant
description: Use when writing or reviewing NIH, NSF, or foundation grant proposals. Invoke when user mentions specific aims, R01, R21, K-series, significance, innovation, approach section, grant writing, proposal review, research strategy, or needs help with fundable hypothesis, reviewer-friendly structure, or compliance with grant guidelines.
---

# Grant Proposal Assistant

## Table of Contents
- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Core Questions](#core-questions)
- [Workflow](#workflow)
- [Section Frameworks](#section-frameworks)
- [Reviewer Mindset](#reviewer-mindset)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

This skill guides the creation and review of competitive grant proposals (NIH R01/R21/K, NSF, foundations) by ensuring clear hypotheses, compelling significance, genuine innovation, and feasible approaches. It applies reviewer-perspective thinking to structure proposals that address common critique points before submission.

## When to Use

Use this skill when:

- **Writing new proposals**: NIH R01, R21, R03, K-series; NSF grants; Foundation applications
- **Specific Aims development**: Crafting the critical 1-page aims document
- **Section drafting**: Significance, Innovation, Approach sections
- **Proposal review**: Pre-submission critique, mock study section preparation
- **Resubmission**: Addressing reviewer critiques, strengthening weak areas
- **Budget justification**: Aligning resources with proposed work

Trigger phrases: "grant proposal", "specific aims", "R01", "R21", "NIH grant", "NSF proposal", "significance section", "innovation", "approach", "study section", "reviewer", "fundable"

**Do NOT use for:**
- Manuscripts (use `scientific-manuscript-review`)
- Fellowship personal statements (use `career-document-architect`)
- Letters of recommendation (use `academic-letter-architect`)

## Core Questions

Every grant proposal must convincingly answer these four questions:

**1. What is the central hypothesis?**
- Testable, specific, falsifiable
- Not just "we will study X" but "we hypothesize that X causes Y through mechanism Z"

**2. Why is the problem important NOW?**
- What gap exists in current knowledge?
- Why is this gap significant for the field/patients/society?
- Why is this the right time (new tools, preliminary data, shifting paradigm)?

**3. What makes the approach innovative?**
- What is genuinely new (concept, method, application)?
- How does this advance beyond incremental improvement?
- Innovation in approach AND/OR innovation in what will be learned

**4. Is the plan feasible and logical?**
- Can this team do this work in this timeframe with these resources?
- Do aims build logically without fatal dependencies?
- Are pitfalls anticipated with alternatives ready?

## Workflow

Copy this checklist and track your progress:

```
Grant Proposal Progress:
- [ ] Step 1: Identify grant mechanism and constraints
- [ ] Step 2: Core questions audit
- [ ] Step 3: Specific Aims review (1-page)
- [ ] Step 4: Significance section review
- [ ] Step 5: Innovation section review
- [ ] Step 6: Approach section review (per aim)
- [ ] Step 7: Reviewer alignment check
- [ ] Step 8: Compliance verification
```

**Step 1: Identify Grant Mechanism and Constraints**

Determine mechanism (R01, R21, K, NSF, Foundation). Note page limits, required sections, and review criteria. R01 = 12 pages; R21 = 6 pages; K = 12 pages + career development. See [resources/methodology.md](resources/methodology.md#grant-mechanisms) for mechanism-specific guidance.

**Step 2: Core Questions Audit**

Read entire proposal looking ONLY for answers to the four core questions. Mark where each is addressed (or missing). Flag unclear hypotheses, weak significance, or missing innovation. See [resources/methodology.md](resources/methodology.md#core-question-audit) for audit checklist.

**Step 3: Specific Aims Review**

Evaluate the 1-page Aims against the gold standard: Opening hook → Gap → Hypothesis → Aims (testable, independent, coherent) → Impact. This is the most important page. See [resources/template.md](resources/template.md#specific-aims-template) for structure.

**Step 4: Significance Section Review**

Check: What is the problem? Why does it matter? What will change if successful? Look for explicit gap statements and impact predictions. See [resources/methodology.md](resources/methodology.md#significance-checklist) for evaluation criteria.

**Step 5: Innovation Section Review**

Check: What is genuinely new? Be specific (not "innovative approach" but "first application of X to Y"). Innovation can be conceptual, methodological, or in expected outcomes. See [resources/methodology.md](resources/methodology.md#innovation-checklist) for evaluation criteria.

**Step 6: Approach Section Review**

For EACH aim: Rationale (why this aim?) → Strategy (how?) → Expected outcomes → Pitfalls → Alternatives. Check for adequate controls, statistical power, timeline realism. See [resources/template.md](resources/template.md#approach-per-aim) for per-aim structure.

**Step 7: Reviewer Alignment Check**

Read as a non-expert reviewer would. Can they understand significance without deep domain knowledge? Are impact statements prominent? Is the writing accessible? See [resources/methodology.md](resources/methodology.md#reviewer-perspective) for reviewer simulation.

**Step 8: Compliance Verification**

Check page limits, required sections, biosketch format, reference formatting. Verify all required components present. Validate using [resources/evaluators/rubric_grant_proposal.json](resources/evaluators/rubric_grant_proposal.json). **Minimum standard**: Average score ≥ 3.5.

## Section Frameworks

### Specific Aims Page (1 page)

**The most important page of your grant.**

**Structure:**
```
OPENING PARAGRAPH (4-6 sentences)
- Hook: Why this problem matters (significance)
- Gap: What's missing in current understanding
- Long-term goal: Your program of research
- Central hypothesis: Testable, specific
- Rationale: Why this hypothesis is reasonable (preliminary data)

AIM 1: [Verb phrase describing objective]
- Brief description (2-3 sentences)
- Expected outcome and interpretation
- Must be testable and achievable

AIM 2: [Verb phrase describing objective]
- Brief description (2-3 sentences)
- Expected outcome and interpretation
- Independent of Aim 1 (can proceed if Aim 1 fails)

AIM 3 (optional): [Verb phrase describing objective]
- Brief description (2-3 sentences)
- May integrate findings from Aims 1-2

CLOSING PARAGRAPH (2-3 sentences)
- Expected outcomes of the project
- Impact: How this advances the field
- Future directions this enables
```

### Significance Section

**Goal:** Convince reviewers the problem matters

**Key elements:**
1. **The Problem**: What clinical/scientific problem exists?
2. **Current State**: What's known, what's been tried?
3. **The Gap**: What critical question remains unanswered?
4. **Impact of Gap**: What's the cost of not knowing?
5. **If Successful**: What changes? Be specific.

**Red flags:**
- ❌ Generic statements ("cancer is bad")
- ❌ No clear gap statement
- ❌ Impact statements too vague ("will advance the field")
- ✅ Specific gap, specific impact, quantifiable where possible

### Innovation Section

**Goal:** Show this is not incremental

**Types of innovation:**
1. **Conceptual**: New framework, paradigm, or understanding
2. **Methodological**: New technique, approach, or model
3. **Application**: Known method applied to new problem
4. **Expected Outcomes**: Will generate novel insights

**Format:**
- Use bullet points for scannability
- Start each with "This project is innovative because..."
- Be specific, not vague

### Approach Section (Per Aim)

**Structure for each aim:**

```
AIM X: [Title]

RATIONALE (1 paragraph)
Why is this aim necessary? How does it address the hypothesis?

PRELIMINARY DATA (if applicable)
What have you already shown that supports feasibility?

STRATEGY (2-4 paragraphs)
- Experimental design
- Methods and procedures
- Controls (positive and negative)
- Statistical analysis plan

EXPECTED OUTCOMES
What results do you expect? How will you interpret them?

POTENTIAL PITFALLS AND ALTERNATIVES
What could go wrong? What's your backup plan?

TIMELINE/MILESTONES
When will this be completed? Dependencies on other aims?
```

## Reviewer Mindset

### How Study Sections Work

- Reviewers assigned based on expertise (but may not be YOUR exact field)
- Primary reviewers read carefully; secondary skim
- 3 reviewers score; others may not read deeply
- Scored on: Significance, Investigators, Innovation, Approach, Environment
- Overall Impact = "How important is this research?"

### What Reviewers Look For

**Good proposals make reviewers' jobs easy:**
- Clear hypothesis on page 1
- Explicit significance statements
- Obvious innovation points (bulleted)
- Logical aim flow
- Pitfalls acknowledged with alternatives

**Proposals get criticized for:**
- Vague hypotheses ("We will explore...")
- Missing controls
- Overly ambitious scope
- Aim dependencies (if Aim 1 fails, whole project fails)
- No preliminary data for risky approaches
- Unclear statistical plans

## Guardrails

**Critical requirements:**

1. **Testable hypothesis**: Must be falsifiable, not just a goal
2. **Explicit gaps**: State what's unknown, not just what you'll do
3. **Real innovation**: Specific, not "innovative approach"
4. **Independent aims**: Project survives if one aim fails
5. **Feasibility evidence**: Preliminary data for risky elements
6. **Power calculations**: Know your sample sizes and why
7. **Pitfall acknowledgment**: Show you've anticipated problems

**Common pitfalls:**
- ❌ **Fishing expedition**: "We will determine..." without hypothesis
- ❌ **Aim dependency**: Aim 2 impossible without Aim 1 success
- ❌ **Scope creep**: Too ambitious for budget/time
- ❌ **Missing controls**: Experiments without proper comparisons
- ❌ **Vague statistics**: "Data will be analyzed appropriately"
- ❌ **No alternatives**: Assuming everything will work

## Quick Reference

**Key resources:**
- **[resources/methodology.md](resources/methodology.md)**: Grant mechanisms, audit checklists, reviewer perspective
- **[resources/template.md](resources/template.md)**: Specific aims template, approach per-aim structure
- **[resources/evaluators/rubric_grant_proposal.json](resources/evaluators/rubric_grant_proposal.json)**: Quality scoring

**Page limits:**
| Mechanism | Research Strategy | Specific Aims |
|-----------|------------------|---------------|
| R01 | 12 pages | 1 page |
| R21 | 6 pages | 1 page |
| R03 | 6 pages | 1 page |
| K-series | 12 pages (+career) | 1 page |

**NIH scoring:**
- 1-3: Exceptional to Excellent (funded)
- 4-5: Very Good to Good (may fund)
- 6-7: Satisfactory to Fair (unlikely)
- 8-9: Marginal to Poor (not funded)

**Typical writing time:**
- Specific Aims (polished): 3-5 days
- Full R01 first draft: 4-6 weeks
- R21 first draft: 2-3 weeks
- Revision cycle: 1-2 weeks per round

**Inputs required:**
- Research idea with preliminary data
- Grant mechanism and deadline
- Institutional resources available

**Outputs produced:**
- Structured grant sections
- Commentary on strengths/weaknesses
- Reviewer-perspective critique
