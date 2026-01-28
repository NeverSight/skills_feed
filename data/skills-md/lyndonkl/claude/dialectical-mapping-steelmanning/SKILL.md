---
name: dialectical-mapping-steelmanning
description: Use when debates are trapped in false dichotomies, polarized positions need charitable interpretation, tradeoffs are obscured by binary framing, synthesis beyond 'pick one side' is needed, or when users mention steelman arguments, thesis-antithesis-synthesis, Hegelian dialectic, third way solutions, or resolving seemingly opposed principles.
---
# Dialectical Mapping & Steelmanning

## Table of Contents
- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [What Is It?](#what-is-it)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

Dialectical Mapping & Steelmanning helps you escape false binary choices by:

- **Steelmanning** both positions (presenting them in their strongest, most charitable form)
- **Mapping** the underlying principles and tradeoffs (what each side values and sacrifices)
- **Synthesizing** a principled third way (transcending "pick a side" to find higher-order resolution)
- **Making tradeoffs explicit** (clarifying costs/benefits of synthesis vs pure positions)

This moves debates from "A vs B" to "here's the best of both, here's what we sacrifice, here's why it's worth it."

## When to Use

Use this skill when:

- **False dichotomies**: Debate framed as binary choice ("we must pick A or B") but better options exist
- **Polarized positions**: Both sides dug in, uncharitable interpretations, strawman arguments flying
- **Hidden tradeoffs**: Each position has merits and costs, but these aren't explicit
- **Principle conflicts**: Seemingly opposed values (speed vs quality, freedom vs safety, innovation vs stability)
- **Synthesis needed**: User explicitly wants "third way", "best of both worlds", or "transcend the debate"
- **Strategic tensions**: Business decisions with legitimate competing priorities (growth vs profitability, centralization vs autonomy)
- **Design tradeoffs**: Technical or product decisions with no clear winner (monolith vs microservices, simple vs powerful)
- **Policy debates**: Governance questions with multiple stakeholder values (privacy vs security, efficiency vs equity)

Trigger phrases: "steelman", "thesis-antithesis-synthesis", "Hegelian dialectic", "false dichotomy", "third way", "both sides have a point", "transcend the debate", "resolve the tension"

## What Is It?

Dialectical Mapping & Steelmanning is a three-step reasoning process:

1. **Steelman Thesis & Antithesis**: Present each position in its strongest form (charitable interpretation, best arguments, underlying principles)
2. **Map Tradeoffs**: Identify what each side optimizes for and what it sacrifices
3. **Synthesize Third Way**: Find a higher-order principle or hybrid approach that honors both positions' core values while acknowledging new tradeoffs

**Quick example:**

**Debate**: "Should our startup prioritize growth or profitability?"

**Typical (bad) framing**: Binary choice. Pick one, argue against the other.

**Steelman Thesis (Growth)**:
- Principle: Market position compounds. Early lead captures network effects, brand recognition, talent attraction.
- Best argument: In winner-take-most markets, second place is first loser. Profitability can wait; market share can't.
- Tradeoff: Accept cash burn, potential failure if funding dries up.

**Steelman Antithesis (Profitability)**:
- Principle: Sustainability enables long-term strategy. Profitable companies control their destiny, survive downturns, outlast competitors.
- Best argument: Growth without unit economics is vanity metric. Profit proves business viability.
- Tradeoff: Accept slower growth, risk being outpaced by well-funded competitors.

**Synthesis (Profitable Growth)**:
- **Higher principle**: Capital efficiency. Grow as fast as sustainable unit economics allow.
- **Third way**: Focus on channels/segments with healthy LTV:CAC (>3:1), deprioritize expensive acquisition. Scale what works profitably, experiment cheaply elsewhere.
- **New tradeoffs**: Slower than "growth at all costs", requires discipline to say no, may miss land-grab opportunities in subsidized markets.
- **Why it works**: Preserves optionality (can raise capital from position of strength OR bootstrap), builds durable moat (real economics, not just scale), reduces existential risk.

**Result**: Escaped false binary. Found principled synthesis with explicit tradeoffs.

## Workflow

Copy this checklist and track your progress:

```
Dialectical Mapping Progress:
- [ ] Step 1: Frame the debate
- [ ] Step 2: Steelman Position A (Thesis)
- [ ] Step 3: Steelman Position B (Antithesis)
- [ ] Step 4: Map principles and tradeoffs
- [ ] Step 5: Synthesize third way
- [ ] Step 6: Validate synthesis quality
```

**Step 1: Frame the debate**

Identify the topic, the two polarized positions (Thesis vs Antithesis), and the apparent tension. Clarify why this feels like a binary choice. See [Common Patterns](#common-patterns) for typical debate structures.

**Step 2: Steelman Position A (Thesis)**

Present Position A in its strongest form: underlying principle (what it values), best arguments (strongest case for this position), supporting evidence, and legitimate tradeoffs it accepts. Use [resources/template.md](resources/template.md#steelmanning-template) for structure. Avoid strawmanning—present version that adherents would recognize as fair.

**Step 3: Steelman Position B (Antithesis)**

Present Position B in its strongest form with same rigor as Position A. Ensure symmetry—both positions get charitable treatment. See [resources/template.md](resources/template.md#steelmanning-template).

**Step 4: Map principles and tradeoffs**

Create tradeoff matrix showing what each position optimizes for (values) and what it sacrifices (costs). Identify underlying principles (speed, quality, freedom, safety, etc.) and how each position weighs them. For complex cases with multiple principles, see [resources/methodology.md](resources/methodology.md#principle-mapping) for multi-dimensional tradeoff analysis.

**Step 5: Synthesize third way**

Find higher-order principle or hybrid approach that transcends the binary. The synthesis should honor core values of both positions, create new value (not just compromise), and make new tradeoffs explicit. Use [resources/template.md](resources/template.md#synthesis-template) for structure. For advanced synthesis techniques (temporal synthesis, conditional synthesis, dimensional separation), see [resources/methodology.md](resources/methodology.md#synthesis-patterns).

**Step 6: Validate synthesis quality**

Self-assess using [resources/evaluators/rubric_dialectical_mapping_steelmanning.json](resources/evaluators/rubric_dialectical_mapping_steelmanning.json). Check: steelmans are charitable and accurate, principles identified, tradeoffs explicit, synthesis transcends binary (not just compromise), new tradeoffs acknowledged. **Minimum standard**: Average score ≥ 3.5.

## Common Patterns

**Pattern 1: Temporal Synthesis (Both, Sequenced)**
- **Structure**: Do A first, then B. Or B in some phases, A in others.
- **Example**: "Speed vs Quality" → **Synthesis**: Iterate fast early (speed), stabilize before launch (quality). Time-box exploration, then shift to refinement.
- **When to use**: Positions optimize for different lifecycle stages or contexts.

**Pattern 2: Conditional Synthesis (Both, Contextual)**
- **Structure**: A in these situations, B in those situations. Define decision criteria.
- **Example**: "Centralized vs Decentralized" → **Synthesis**: Centralize strategy/standards/shared resources, decentralize execution/tactics/experiments. Clear escalation criteria for edge cases.
- **When to use**: Positions are optimal in different scenarios or scopes.

**Pattern 3: Dimensional Separation (Both, Different Axes)**
- **Structure**: Optimize A on one dimension, B on another orthogonal dimension.
- **Example**: "Simple vs Powerful" → **Synthesis**: Simple by default (80% use cases), powerful for power users (progressive disclosure, advanced mode). Complexity optional, not mandatory.
- **When to use**: Tradeoff is false—can achieve both on different dimensions simultaneously.

**Pattern 4: Higher-Order Principle (Transcend via Meta-Goal)**
- **Structure**: Both A and B are means to same end. Find better means.
- **Example**: "Build vs Buy" → **Synthesis**: Neither—rent/SaaS. Or: Build core differentiator, buy commodity. Higher principle: Maximize value creation per dollar/hour.
- **When to use**: Binary options are tactics, not ends. Reframe around shared ultimate goal.

**Pattern 5: Compensating Controls (Accept A's Risk, Mitigate with B's Safeguard)**
- **Structure**: Lean toward A, add B's protections as guardrails.
- **Example**: "Move Fast vs Prevent Errors" → **Synthesis**: Move fast with automated testing, staged rollouts, quick rollback. Accept some errors, contain blast radius.
- **When to use**: One position clearly better for primary goal, other provides risk mitigation.

## Guardrails

**Critical requirements:**

1. **Steelman, don't strawman**: Present each position as its adherents would recognize. Ask: "Would someone who holds this view agree this is a fair representation?" If no, strengthen it further.

2. **Identify principles, not just preferences**: Go deeper than "Side A wants X, Side B wants Y." Find WHY they want it. What value do they optimize for? Freedom? Safety? Speed? Equity? Efficiency?

3. **Synthesis must transcend, not just compromise**: Splitting the difference (50% A, 50% B) is usually weak. Good synthesis finds new option C that honors both principles at higher level. "Both-and" thinking, not "either-or" averaging.

4. **Make tradeoffs explicit**: Every synthesis has costs. State what you gain AND what you sacrifice vs pure positions. Don't pretend synthesis is "best of both with no downsides."

5. **Avoid false equivalence**: Steelmanning doesn't mean both sides are equally correct. One position may have stronger arguments/evidence. Synthesis should reflect this (lean toward stronger position, add safeguards from weaker).

6. **Check for false dichotomy**: Some "debates" are manufactured. Both A and B may be bad options. Ask: "Is this actually a binary choice, or are we missing option C/D/E?"

7. **Test synthesis with adversarial roles**: Before finalizing, inhabit each original position and critique the synthesis. Would a partisan of A/B accept it, or see it as capitulation? If synthesis can't survive friendly fire, strengthen it.

**Common pitfalls:**

- ❌ **Strawmanning**: "Position A naively believes X" (uncharitable). Instead: "Position A prioritizes Y principle because..."
- ❌ **False balance**: Steelmanning doesn't require treating bad-faith arguments as if made in good faith. If one position is empirically wrong or logically inconsistent, note this after steelmanning.
- ❌ **Mushy middle**: "Do a little of both" is not synthesis. Synthesis finds NEW approach, not diluted mix.
- ❌ **Ignoring power dynamics**: Some debates aren't idea conflicts—they're conflicts of interest. Synthesis may not resolve structural problems.
- ❌ **Analysis paralysis**: Dialectical mapping is a tool for decision-making, not an end. Set time bounds, converge on synthesis, decide.

## Quick Reference

**Key resources:**

- **[resources/template.md](resources/template.md)**: Steelmanning template, tradeoff matrix template, synthesis structure
- **[resources/methodology.md](resources/methodology.md)**: Advanced techniques (multi-party dialectics, principle hierarchies, Toulmin argumentation for steelmanning, synthesis patterns)
- **[resources/evaluators/rubric_dialectical_mapping_steelmanning.json](resources/evaluators/rubric_dialectical_mapping_steelmanning.json)**: Quality criteria for steelmans and synthesis

**Typical workflow time:**

- Simple binary debate (2 positions, clear principles): 20-30 minutes
- Complex multi-stakeholder debate: 45-60 minutes
- Strategic frameworks (long-term decisions): 60-90 minutes

**When to escalate:**

- More than 2 positions (multi-party dialectics)
- Nested tradeoffs (position A itself is a synthesis of A1 vs A2)
- Empirical questions disguised as value debates
- Bad faith arguments (not resolvable via steelmanning)
→ Use [resources/methodology.md](resources/methodology.md) for these advanced cases

**Inputs required:**

- **Debate topic**: The decision or question being debated
- **Position A (Thesis)**: One side of the binary
- **Position B (Antithesis)**: The opposing side
- **Context** (optional): Constraints, stakeholders, decision criteria

**Outputs produced:**

- `dialectical-mapping-steelmanning.md`: Complete analysis with steelmanned positions, tradeoff matrix, synthesis, and recommendations
