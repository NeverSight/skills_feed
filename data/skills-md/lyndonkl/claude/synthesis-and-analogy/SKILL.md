---
name: synthesis-and-analogy
description: Use when synthesizing information from multiple sources (literature review, stakeholder feedback, research findings, data from different systems), creating or evaluating analogies for explanation or problem-solving (cross-domain transfer, "X is like Y", structural mapping), combining conflicting viewpoints into unified framework, identifying patterns across disparate sources, finding creative solutions by transferring principles from one domain to another, testing whether analogies hold (surface vs deep similarities), or when user mentions "synthesize", "combine sources", "analogy", "like", "similar to", "transfer from", "integrate findings", "what's it analogous to".
---
# Synthesis & Analogy

## Table of Contents
- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [What Is It](#what-is-it)
- [Workflow](#workflow)
- [Synthesis Techniques](#synthesis-techniques)
- [Analogy Techniques](#analogy-techniques)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

Synthesize information from multiple sources into coherent insights and use analogical reasoning to transfer knowledge across domains, explain complex concepts, and find creative solutions.

## When to Use

**Information Synthesis:**
- Literature review (combine 10+ research papers into narrative)
- Multi-source integration (customer feedback + analytics + competitive data)
- Conflicting viewpoint reconciliation (synthesize disagreeing experts)
- Pattern identification across sources (themes from interviews, support tickets, reviews)

**Analogical Reasoning:**
- Explain complex concepts (use familiar domain to explain unfamiliar)
- Cross-domain problem-solving (transfer solution from different field)
- Creative ideation (find novel solutions through structural mapping)
- Teaching/communication (make abstract concepts concrete)

**Combined Synthesis + Analogy:**
- Synthesize multiple analogies to build richer understanding
- Use analogies to reconcile conflicting sources ("both are right from different perspectives")
- Transfer synthesized insights from one domain to another

## What Is It

**Synthesis**: Combining information from multiple sources into unified, coherent whole that reveals patterns, resolves conflicts, and generates new insights beyond individual sources.

**Analogy**: Structural mapping between domains where relationships in source domain (familiar) illuminate relationships in target domain (unfamiliar). Good analogies preserve deep structure, not just surface features.

**Example - Synthesis**: Synthesizing 15 customer interviews + 5 surveys + support ticket analysis → "Customers struggle with onboarding (87% mention), specifically Step 3 configuration (65% abandon here), because terminology is domain-specific (42% request glossary). Three user types emerge: novices (need hand-holding), intermediates (need examples), experts (need speed)."

**Example - Analogy**: "Microservices architecture is like a city of specialized shops vs monolithic architecture like a department store. City: each shop (service) independent, can renovate without closing whole city, but must coordinate deliveries (APIs). Department store: everything under one roof (codebase), easier coordination, but renovating one section disrupts whole store. Trade-off: flexibility vs simplicity."

## Workflow

Copy this checklist and track your progress:

```
Synthesis & Analogy Progress:
- [ ] Step 1: Clarify goal and gather sources/domains
- [ ] Step 2: Choose approach (synthesis, analogy, or both)
- [ ] Step 3: Apply synthesis or analogy techniques
- [ ] Step 4: Test quality and validity
- [ ] Step 5: Refine and deliver insights
```

**Step 1: Clarify goal**

For synthesis: What sources? What question are we answering? What conflicts need resolving? For analogy: What's source domain (familiar)? What's target domain (explaining)? What's goal (explain, solve, ideate)? See [Common Patterns](#common-patterns) for typical goals.

**Step 2: Choose approach**

Synthesis only → Use [Synthesis Techniques](#synthesis-techniques). Analogy only → Use [Analogy Techniques](#analogy-techniques). Both → Start with synthesis to find patterns, then use analogy to explain or transfer. For straightforward cases → Use [resources/template.md](resources/template.md). For complex multi-domain synthesis → Study [resources/methodology.md](resources/methodology.md).

**Step 3: Apply techniques**

For synthesis: Identify themes across sources, note agreements/disagreements, resolve conflicts via higher-level framework, extract patterns. For analogy: Map structure from source to target (what corresponds to what?), identify shared relationships (not surface features), test mapping validity. See [Synthesis Techniques](#synthesis-techniques) and [Analogy Techniques](#analogy-techniques).

**Step 4: Test quality**

Self-assess using [resources/evaluators/rubric_synthesis_and_analogy.json](resources/evaluators/rubric_synthesis_and_analogy.json). Synthesis checks: captures all sources? resolves conflicts? identifies patterns? adds insight? Analogy checks: structure preserved? deep not surface? limitations acknowledged? helps understanding? Minimum standard: Score ≥3.5 average.

**Step 5: Refine and deliver**

Create `synthesis-and-analogy.md` with: synthesis summary (themes, agreements, conflicts, patterns, new insights) OR analogy explanation (source domain, target domain, mapping table, what transfers, limitations), supporting evidence from sources, actionable implications.

## Synthesis Techniques

**Thematic Synthesis** (identify recurring themes):
1. **Extract**: Read each source, note key points and themes
2. **Code**: Label similar ideas with same theme tag (e.g., "onboarding friction", "pricing confusion")
3. **Count**: Track frequency (how many sources mention each theme?)
4. **Rank**: Prioritize by frequency × importance
5. **Synthesize**: Describe each major theme with supporting evidence from sources

**Conflict Resolution Synthesis** (reconcile disagreements):
- **Meta-level framework**: Both right from different perspectives (e.g., "Source A prioritizes speed, Source B prioritizes quality - depends on context")
- **Scope distinction**: Disagree on scope ("Source A: feature X broken for enterprise. Source B: works for SMB. Synthesis: works for SMB, broken for enterprise")
- **Temporal**: Disagreement over time ("Source A: strategy X failed in 2010. Source B: works in 2024. Context changed: market maturity")
- **Null hypothesis**: Genuinely conflicting evidence → state uncertainty, propose tests

**Pattern Identification** (find cross-cutting insights):
- Look for repeated structures (same problem in different guises)
- Find causal patterns (when X, then Y across multiple sources)
- Identify outliers (sources that contradict pattern - why?)
- Extract meta-insights (what does the pattern tell us?)

**Example**: Synthesizing 10 postmortems → Pattern: 80% of incidents involve config change + lack of rollback plan. Outliers: 2 incidents hardware failure. Meta-insight: Need config change review process + automatic rollback capability.

## Analogy Techniques

**Structural Mapping Theory**:
1. **Identify source domain** (familiar, well-understood)
2. **Identify target domain** (unfamiliar, explaining)
3. **Map entities**: What in source corresponds to what in target?
4. **Map relationships**: Preserve relationships (if A→B in source, then A'→B' in target)
5. **Test mapping**: Do relationships transfer? Are there unmapped elements?
6. **Acknowledge limits**: Where does analogy break down?

**Surface vs Deep Analogies**:
- **Surface (weak)**: Share superficial features (both round, both red) - not illuminating
- **Deep (strong)**: Share structural relationships (both have hub-spoke topology, both use feedback loops) - insightful

**Example - Surface**: "Brain is like computer (both process information)" - too vague, doesn't help
**Example - Deep**: "Brain neurons are like computer transistors: neurons fire/don't fire (binary), connect in networks, learning = strengthening connections (weights). BUT neurons are analog/probabilistic, computer precise/deterministic" - preserves structure, acknowledges limits

**Analogy Quality Tests**:
- **Systematicity**: Do multiple relationships map (not just one)?
- **Structural preservation**: Do causal relations transfer?
- **Productivity**: Does analogy generate new predictions/insights?
- **Scope limits**: Where does analogy break? (Always acknowledge)

## Common Patterns

**Pattern 1: Literature Review Synthesis**
- Goal: Combine research papers into narrative
- Technique: Thematic synthesis (extract themes, note agreements/conflicts, identify gaps)
- Output: "Research shows X (5 studies support), but Y remains controversial (3 for, 2 against due to methodology differences). Gap: no studies on Z population."

**Pattern 2: Multi-Stakeholder Synthesis**
- Goal: Integrate feedback from design, engineering, product, customers
- Technique: Conflict resolution synthesis (meta-level framework, scope distinctions)
- Output: "Design wants A (aesthetics), Engineering wants B (performance), Product wants C (speed). All valid - prioritize C (speed) for v1, A (aesthetics) for v2, B (performance) as ongoing optimization."

**Pattern 3: Explanatory Analogy**
- Goal: Explain technical concept to non-technical audience
- Technique: Structural mapping from familiar domain
- Output: "Git branches are like alternate timelines in sci-fi: main branch is prime timeline, feature branches are 'what if' explorations. Merge = timeline convergence. Conflicts = paradoxes to resolve."

**Pattern 4: Cross-Domain Problem-Solving**
- Goal: Solve problem by transferring solution from different field
- Technique: Identify structural similarity, map solution elements
- Output: "Warehouse routing problem is structurally similar to ant colony optimization: ants find shortest paths via pheromone trails. Transfer: use reinforcement learning with 'digital pheromones' (successful route weights) to optimize warehouse paths."

**Pattern 5: Creative Ideation via Analogy**
- Goal: Generate novel ideas by exploring analogies
- Technique: Forced connections, random domain pairing, systematic variation
- Output: "How is code review like restaurant food critique? Critic (reviewer) evaluates dish (code) on presentation (readability), taste (correctness), technique (architecture). Transfer: multi-criteria rubric for code review focusing on readability, correctness, architecture."

## Guardrails

**Synthesis Quality:**
- Covers all relevant sources (no cherry-picking)
- Resolves conflicts explicitly (doesn't ignore disagreements)
- Identifies patterns beyond what individual sources state (adds value)
- Distinguishes facts from interpretations
- Cites sources for claims
- Acknowledges gaps and uncertainties

**Analogy Quality:**
- Maps structure not surface features (deep analogy)
- Explicitly states what corresponds to what (mapping table)
- Tests validity (do relationships transfer?)
- Acknowledges where analogy breaks down (limitations)
- Doesn't overextend (knows when to stop pushing analogy)
- Appropriate for audience (familiar source domain)

**Avoid:**
- **False synthesis**: Forcing agreement where genuine conflict exists
- **Surface analogies**: "Both are round" doesn't help understanding
- **Analogy as proof**: Analogies illustrate, don't prove
- **Overgeneralization**: One source ≠ pattern
- **Cherry-picking**: Ignoring inconvenient sources
- **Mixing levels**: Confusing data with interpretation

## Quick Reference

**Inputs Required:**

For synthesis:
- Multiple sources (papers, interviews, datasets, feedback, research)
- Question to answer or goal to achieve
- Conflicts or patterns to identify

For analogy:
- Source domain (familiar, well-understood)
- Target domain (unfamiliar, explaining or solving)
- Goal (explain, solve problem, generate ideas)

**Techniques to Use:**

Synthesis:
- Thematic synthesis → Identify recurring themes
- Conflict resolution → Reconcile disagreements via meta-framework
- Pattern identification → Find cross-cutting insights

Analogy:
- Structural mapping → Map entities and relationships
- Surface vs deep test → Ensure structural not superficial similarity
- Validity test → Check if relationships transfer

**Outputs Produced:**

- `synthesis-and-analogy.md` with:
  - Synthesis: themes, agreements, conflicts resolved, patterns, new insights, supporting evidence
  - Analogy: source domain, target domain, mapping table (what↔what), transferred insights, limitations
  - Actionable implications

**Resources:**
- Quick synthesis or analogy → [resources/template.md](resources/template.md)
- Complex multi-source or multi-domain → [resources/methodology.md](resources/methodology.md)
- Quality validation → [resources/evaluators/rubric_synthesis_and_analogy.json](resources/evaluators/rubric_synthesis_and_analogy.json)

**Minimum Quality Standard:**
- Synthesis: covers all sources, resolves conflicts, identifies patterns, adds insight
- Analogy: structural mapping clear, deep not surface, limitations acknowledged
- Both: evidence-based, cited sources, actionable
- Average rubric score ≥ 3.5/5 before delivering
