---
name: scientific-manuscript-review
description: Use when reviewing or editing research manuscripts, journal articles, reviews, or perspectives. Invoke when user mentions manuscript, paper draft, article, research writing, journal submission, reviewer feedback, or needs to improve scientific writing clarity, structure, or argumentation in their manuscript.
---

# Scientific Manuscript Review

## Table of Contents
- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Core Principles](#core-principles)
- [Workflow](#workflow)
- [Section-by-Section Review](#section-by-section-review)
- [Language Guidelines](#language-guidelines)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

This skill provides systematic review and editing of scientific manuscripts (research articles, reviews, perspectives) to improve clarity, structure, scientific rigor, and reader comprehension. It applies a multi-pass approach covering structure, scientific logic, language, and formatting to transform drafts into publication-ready documents.

## When to Use

Use this skill when:

- **Drafting manuscripts**: Research articles, short communications, review papers, perspectives
- **Pre-submission review**: Final polish before journal submission
- **Revision cycles**: Addressing reviewer comments, improving based on feedback
- **Collaborative editing**: Reviewing co-author drafts, mentoring student writing
- **Self-editing**: Systematic review of your own writing for blind spots
- **Journal transfer**: Adapting manuscript for different journal format

Trigger phrases: "manuscript review", "paper draft", "journal article", "research writing", "improve my paper", "reviewer feedback", "submission ready", "scientific writing"

**Do NOT use for:**
- Grant proposals (use `grant-proposal-assistant`)
- Recommendation letters (use `academic-letter-architect`)
- General emails (use `scientific-email-polishing`)

## Core Principles

Seven foundational beliefs guiding manuscript review:

1. **Clarity over cleverness**: Scientific clarity is more important than stylistic elegance
2. **Narrative shapes comprehension**: Structure and story arc determine reader understanding
3. **Audience dictates tone**: Expert vs. general audience requires different depth and framing
4. **Format signals credibility**: Professional formatting reflects scientific rigor
5. **Claims require evidence**: Strong assertions need strong data and appropriate hedging
6. **Each section has a job**: Introduction sells the problem, Results show the data, Discussion interprets
7. **Constraints shape structure**: Word limits and journal guidelines determine emphasis

## Workflow

Copy this checklist and track your progress:

```
Manuscript Review Progress:
- [ ] Step 1: Identify manuscript type and extract core message
- [ ] Step 2: Structural pass - map and evaluate overall organization
- [ ] Step 3: Introduction review - gap statement, focus, hypothesis
- [ ] Step 4: Results review - question, approach, finding, interpretation
- [ ] Step 5: Discussion review - synthesis, context, limitations
- [ ] Step 6: Scientific clarity check - claims, controls, hedging
- [ ] Step 7: Language polish - terminology, voice, jargon
- [ ] Step 8: Formatting check - journal compliance
```

**Step 1: Identify Manuscript Type and Core Message**

Determine document type (research article, review, perspective, short communication). Extract the ONE finding or message readers must remember. Ask: "If readers remember only one thing, what should it be?" See [resources/methodology.md](resources/methodology.md#core-message-extraction) for extraction techniques.

**Step 2: Structural Pass**

Map overall organization against standard IMRaD (Introduction, Methods, Results, Discussion) or review structure. Check logical sequencing - does each section flow into the next? Identify unclear transitions or missing context. See [resources/methodology.md](resources/methodology.md#structural-assessment) for structure evaluation.

**Step 3: Introduction Review**

Evaluate using the Introduction Arc: Broad context → Narrow focus → Knowledge gap → Hypothesis/Objective. Check that gap statement is explicit and compelling. Verify ending with clear hypothesis or objective. See [resources/template.md](resources/template.md#introduction-arc) for template.

**Step 4: Results Review**

For each figure/table/experiment: Question addressed? → Approach used? → Key finding (with statistics)? → Interpretation (what it means)? Flag data-dump writing that lacks interpretation. Ensure findings build toward core message. See [resources/template.md](resources/template.md#results-paragraph) for results structure.

**Step 5: Discussion Review**

Verify structure: Revisit hypothesis → Interpret findings in field context → Place in broader literature → Acknowledge limitations → Suggest future directions. Check for overclaiming (speculation presented as fact). Ensure clear separation of data interpretation vs. speculation. See [resources/methodology.md](resources/methodology.md#discussion-structure) for discussion framework.

**Step 6: Scientific Clarity Check**

Run the clarity checklist: Claims supported by data? Quantitative details present (statistics, n values)? Controls adequately described? Interpretations appropriately hedged? Mechanistic explanations where needed? See [resources/template.md](resources/template.md#clarity-checklist) for full checklist.

**Step 7: Language Polish**

Ensure terminology consistency throughout. Remove or define jargon on first use. Prefer active voice when it aids clarity. Standardize abbreviations. Check for hedging language ("suggests" vs "proves"). See [resources/methodology.md](resources/methodology.md#language-guidelines) for specific guidance.

**Step 8: Formatting Check**

Verify compliance with target journal guidelines (word limits, reference format, figure requirements). Check section headings match journal requirements. Ensure abstract follows structured/unstructured requirement. Validate using [resources/evaluators/rubric_scientific_manuscript.json](resources/evaluators/rubric_scientific_manuscript.json). **Minimum standard**: Average score ≥ 3.5.

## Section-by-Section Review

### Introduction Structure

**Goal:** Convince readers the problem matters and your approach is sound

**The Funnel Structure:**
```
[Broad context - establish field importance, 1-2 sentences]
        ↓
[Narrow to specific area - what's been done]
        ↓
[Knowledge gap - what's missing, why it matters]
        ↓
[Your hypothesis/objective - what you will address]
```

**Common problems:**
- Gap statement buried or implicit (make it explicit: "However, X remains unknown")
- Too broad opening (readers don't need history of the universe)
- No clear hypothesis at end (readers don't know what to expect)
- Overlong literature review (move details to Discussion)

### Results Structure

**Goal:** Present data clearly with interpretation, not just numbers

**Per-paragraph/figure structure:**
```
[Question this experiment addresses]
[Approach/method used]
[Key finding - with quantification]
[Brief interpretation - what this means]
```

**Common problems:**
- Data dump (listing results without interpretation)
- Missing statistics (p-values, n values, confidence intervals)
- Vague descriptions ("we found differences" vs "we found 3-fold increase")
- Figures not referenced in logical order
- Key findings buried in text (highlight important results)

### Discussion Structure

**Goal:** Interpret findings and place in broader context

**Standard flow:**
```
[Restate main finding and hypothesis status]
        ↓
[Interpret key results in field context]
        ↓
[Compare to prior literature - agreements/disagreements]
        ↓
[Mechanistic implications (if applicable)]
        ↓
[Limitations - honest acknowledgment]
        ↓
[Future directions - what comes next]
        ↓
[Concluding statement - big picture significance]
```

**Common problems:**
- Overclaiming (data doesn't support conclusions)
- Repeating Results section (discuss, don't recapitulate)
- Missing limitations (reviewers will note them anyway)
- Speculation unmarked (clearly label "we speculate that...")
- No connection to field (discuss in isolation)

## Language Guidelines

**Active vs. Passive Voice:**
- Use active for clarity: "We measured" not "Measurements were made"
- Use passive when agent is obvious or unimportant: "Samples were incubated at 37°C"
- Avoid dangling modifiers: Not "Having analyzed the data, the conclusion was..." but "Having analyzed the data, we concluded..."

**Hedging Language:**
- Strong data: "demonstrates", "shows", "establishes"
- Moderate confidence: "suggests", "indicates", "supports"
- Speculation: "may", "might", "could potentially"
- Match hedge strength to evidence strength

**Jargon Management:**
- Define on first use: "polymerase chain reaction (PCR)"
- Avoid unnecessary jargon when plain language works
- Field-standard terms don't need definition (DNA, protein, cell)
- Reader-appropriate: more definition for broad audience journals

**Terminology Consistency:**
- Pick one term and stick with it (don't alternate between "subjects", "participants", "patients")
- Create terminology table for complex manuscripts
- Check abbreviations defined before use

## Guardrails

**Critical requirements:**

1. **Preserve author voice**: Edit for clarity, don't rewrite. Never invent claims or change meaning. Mark suggestions clearly when proposing new content.

2. **Claims match data**: Every conclusion must be supported by presented results. Flag overclaiming immediately. Speculation must be labeled.

3. **Quantitative rigor**: Statistics required for comparisons. N values for all experiments. Significance thresholds stated. Variability measures included.

4. **Logical flow**: Each section should flow naturally to the next. Transitions explicit. Conclusions follow from premises.

5. **Appropriate hedging**: Strong claims need strong evidence. Use hedging language proportional to certainty.

6. **Consistent terminology**: Same concept = same term throughout. Abbreviations defined before use.

**Common pitfalls:**
- ❌ **Overclaiming**: "This proves X" when data only suggests
- ❌ **Missing context**: Results without interpretation
- ❌ **Buried lede**: Important finding hidden in paragraph
- ❌ **Inconsistent terms**: Alternating between synonyms
- ❌ **Dense paragraphs**: Walls of text without breaks
- ❌ **Vague descriptions**: "Some increase" instead of "3-fold increase"

## Quick Reference

**Key resources:**
- **[resources/methodology.md](resources/methodology.md)**: Detailed review methods, structural assessment, language guidelines
- **[resources/template.md](resources/template.md)**: Introduction arc, results paragraph, clarity checklist
- **[resources/evaluators/rubric_scientific_manuscript.json](resources/evaluators/rubric_scientific_manuscript.json)**: Quality scoring criteria

**Introduction checklist:**
- [ ] Broad context establishes importance
- [ ] Narrows to specific problem
- [ ] Gap statement explicit ("However, X remains unknown")
- [ ] Ends with clear hypothesis or objective

**Results checklist:**
- [ ] Each experiment has question, approach, finding, interpretation
- [ ] Statistics present (p-values, n, confidence intervals)
- [ ] Quantitative descriptions (numbers, not "some/many")
- [ ] Figures referenced in logical order
- [ ] Key findings highlighted

**Discussion checklist:**
- [ ] Opens by revisiting hypothesis
- [ ] Interprets (doesn't just repeat) results
- [ ] Places in literature context
- [ ] Acknowledges limitations
- [ ] Suggests future directions
- [ ] Speculation clearly labeled

**Typical review time:**
- Quick review (structure + major issues): 20-30 minutes
- Standard review (full checklist): 45-60 minutes
- Deep revision (rewriting sections): 2-3 hours

**Inputs required:**
- Manuscript draft (any stage)
- Target journal (if known)
- Specific concerns from author (if any)

**Outputs produced:**
- Edited manuscript with tracked changes
- Commentary on major structural/logic changes
- Summary of key improvements made
