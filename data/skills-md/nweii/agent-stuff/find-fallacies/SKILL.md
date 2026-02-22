---
name: find-fallacies
description: "Analyze text for logical fallacies. Use when reviewing arguments, debates, articles, or reasoning that may contain flawed logic."
metadata:
  author: nweii
  version: "1.0.0"
---

# Find Fallacies

Analyze the provided text and identify any logical fallacies present. For each fallacy found, explain:

1. The fallacy name and type
2. Where it appears in the text
3. Why it's fallacious (brief explanation)

## Fallacy Reference

### Formal Fallacies

Errors in logical form.

- **Appeal to probability** — Taking something for granted because it would probably be the case
- **Argument from fallacy** — Assuming fallacious argument means false conclusion
- **Base rate fallacy** — Ignoring prior probabilities in conditional reasoning
- **Conjunction fallacy** — Multiple conditions seem more probable than single condition
- **Non sequitur** — Conclusion doesn't follow premise
- **Affirming the consequent** — if A then B; B, therefore A
- **Denying the antecedent** — if A then B; not A, therefore not B
- **Modal fallacy** — Confusing necessity with sufficiency

### Informal Fallacies

#### Improper Premise

- **Begging the question** — Using conclusion to support itself
- **Circular reasoning** — Beginning with what you're trying to prove
- **Loaded question** — Question presupposes something unproven

#### Faulty Generalizations

- **Cherry picking** — Using only confirming data
- **Survivorship bias** — Focusing on successes, ignoring failures
- **Hasty generalization** — Broad conclusion from small sample
- **No true Scotsman** — Redefining to exclude counterexamples
- **False analogy** — Poorly suited comparison

#### Questionable Cause

- **Correlation implies causation** — Assuming correlation means cause
- **Post hoc ergo propter hoc** — After this, therefore because of this
- **Single cause fallacy** — Assuming one cause when multiple exist
- **Regression fallacy** — Failing to account for natural fluctuations

#### Relevance Fallacies

- **Appeal to the stone** — Dismissing as absurd without proof
- **Argument from ignorance** — Not proven false = true (or vice versa)
- **Argument from incredulity** — Can't imagine it, so must be false
- **Red herring** — Introducing irrelevant topic

#### Ad Hominem Variants

- **Ad hominem** — Attacking arguer instead of argument
- **Circumstantial ad hominem** — Dismissing due to perceived benefit
- **Poisoning the well** — Discrediting source preemptively
- **Appeal to motive** — Dismissing based on assumed motives
- **Tu quoque** — "You do it too"
- **Tone policing** — Focusing on emotion over substance

#### Appeals

- **Appeal to authority** — True because authority says so
- **Appeal to emotion** — Manipulating feelings over reasoning
- **Appeal to nature** — Natural = good
- **Appeal to tradition** — True because long held
- **Appeal to popularity** — True because many believe it
- **Appeal to consequences** — True because of desired outcomes

#### Other Common Fallacies

- **Straw man** — Refuting a different argument than presented
- **False dilemma** — Only two options when more exist
- **False equivalence** — Treating unequal things as equal
- **Slippery slope** — Small step leads inevitably to disaster
- **Moving the goalposts** — Demanding more evidence when some provided
- **Nirvana fallacy** — Rejecting imperfect solutions
- **Motte-and-bailey** — Defending modest claim when challenged on bold one
- **Special pleading** — Claiming exemption without justification
- **Whataboutism** — Deflecting by pointing to other wrongs
- **Kafkatrapping** — Denial as evidence of guilt

## Output Format

Present findings as:

**FALLACIES**

- **Fallacy Name**: Fallacy Type — Brief explanation of where and why it appears.

If no fallacies are found, say so and note any areas where the reasoning is sound or where claims are well-supported.
