---
name: paper-to-intuition
description: Transforms an academic paper into deep, multi-layered understanding. Use when asked to explain a paper, break down a research paper, understand an arXiv paper, or build intuition for a technical concept from a paper. Generates explanations at multiple levels plus visual intuition diagrams.
---

# Paper to Intuition

Transform dense academic papers into genuine understanding through layered explanation and visual intuition.

## Process

1. **Get the paper** - Ask for the arXiv link, PDF, or paper title
2. **Extract the core** - Identify the single key insight (one sentence)
3. **Build the ladder** - Create explanations at 4 levels
4. **Visualize intuition** - Generate interactive diagrams
5. **Stress test understanding** - "What breaks if we remove X?"

## The Explanation Ladder

Generate explanations at each level, with each building on the last:

### Level 1: ELI5 (1 paragraph)
- No jargon, no equations
- Use familiar analogies from everyday life
- A curious 10-year-old should roughly get it

### Level 2: Undergraduate (2-3 paragraphs)
- Assume calculus, basic linear algebra, intro ML
- Introduce key terms with definitions
- Connect to textbook concepts they'd know

### Level 3: Graduate (3-4 paragraphs)
- Assume ML fundamentals, optimization, probability
- Discuss relationship to prior work
- Explain why naive approaches don't work
- Cover the key equations with plain-English annotations

### Level 4: Researcher (2-3 paragraphs)
- Assume field expertise
- Subtle technical contributions
- Limitations and open questions
- How this changes what's possible

## Key Equations Breakdown

For each important equation:

```
[Equation in LaTeX]

In words: [Plain English translation]

Each term:
- [symbol]: [what it represents] [why it's there]

Intuition: [Why this mathematical form? What would change if we used a different form?]
```

## Visual Intuition Artifact

Generate a self-contained HTML file with:

- **Architecture diagram** - Boxes and arrows showing information flow
- **Interactive sliders** - Manipulate key parameters, see effects
- **Before/after comparisons** - What the method improves over baselines
- **Failure case visualization** - When and why it breaks down

Use SVG for diagrams, vanilla JavaScript for interactivity. Dark theme, clean typography.

```html
<!DOCTYPE html>
<html>
<head>
  <title>[Paper Name] - Visual Intuition</title>
  <style>
    :root { --bg: #1a1a2e; --text: #eee; --accent: #4f8cff; }
    /* Clean, research-aesthetic styling */
  </style>
</head>
<body>
  <h1>[Paper Title]</h1>
  <p class="tldr">[One-sentence insight]</p>

  <section id="architecture">
    <svg><!-- Information flow diagram --></svg>
  </section>

  <section id="interactive">
    <!-- Parameter sliders with live updates -->
  </section>

  <section id="comparisons">
    <!-- Before/after, ablations -->
  </section>
</body>
</html>
```

## The "What Breaks?" Analysis

For each major component, explain:

1. **What it does** - The role this component plays
2. **What breaks without it** - Concrete failure mode
3. **Why this solution** - Alternatives considered, why this won
4. **The tradeoff** - What we pay for this choice (compute, complexity, assumptions)

## Output Structure

Deliver as a structured document:

```markdown
# [Paper Title]

**TL;DR:** [One sentence]

**Why it matters:** [One paragraph on significance]

## The Explanation Ladder

### ELI5
[...]

### Undergraduate Level
[...]

### Graduate Level
[...]

### Researcher Level
[...]

## Key Equations

### Equation 1: [Name]
[Breakdown as specified above]

## What Breaks If We Remove...

### [Component 1]
[Analysis]

### [Component 2]
[Analysis]

## Visual Intuition

[Link to or embed HTML artifact]

## Further Reading

- [Prerequisite paper 1]
- [Follow-up work 1]
```

## Quality Standards

- Every analogy must be accurate, not just catchy
- Equations must be explained, not just translated
- Visuals must reveal structure, not just decorate
- The researcher-level section should contain insight, not just summary
- Admit when something is genuinely confusing or poorly explained in the original paper
