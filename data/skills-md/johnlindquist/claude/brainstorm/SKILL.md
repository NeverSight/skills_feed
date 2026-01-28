---
name: brainstorm
description: Generate ideas and explore possibilities with AI. Use for creative problem solving, generating alternatives, and expanding on concepts.
---

# Brainstorming Assistant

Generate and explore ideas systematically.

## Prerequisites

```bash
pip install google-generativeai
export GEMINI_API_KEY=your_api_key
```

## Brainstorming Operations

### Generate Ideas

```bash
gemini -m pro -o text -e "" "Generate 10 creative ideas for: [topic]

Requirements:
- Mix of conventional and unconventional
- Varying levels of complexity
- Consider different user perspectives
- Include at least 2 'wild card' ideas

For each idea:
- Brief description
- Key benefit
- Main challenge"
```

### Quick Brainstorm

```bash
gemini -m pro -o text -e "" "Quick brainstorm (5 ideas in 1 sentence each):

Topic: [your topic]

Just list ideas, no explanation needed."
```

### Expand an Idea

```bash
gemini -m pro -o text -e "" "Expand on this idea:

IDEA: [brief idea]
CONTEXT: [relevant background]

Explore:
1. How it would work in practice
2. Required components/resources
3. Potential variations
4. Who would benefit most
5. First steps to validate"
```

## Structured Techniques

### SCAMPER Method

```bash
gemini -m pro -o text -e "" "Apply SCAMPER to: [product/feature/process]

- Substitute: What can be replaced?
- Combine: What can be merged?
- Adapt: What can be modified?
- Modify/Magnify: What can be enlarged or emphasized?
- Put to other uses: What else could this be used for?
- Eliminate: What can be removed?
- Reverse/Rearrange: What can be reorganized?"
```

### Six Thinking Hats

```bash
gemini -m pro -o text -e "" "Analyze this decision using Six Thinking Hats:

DECISION: [what you're considering]

- White Hat (Facts): What do we know?
- Red Hat (Feelings): Gut reactions?
- Black Hat (Caution): What could go wrong?
- Yellow Hat (Optimism): What are the benefits?
- Green Hat (Creativity): What alternatives exist?
- Blue Hat (Process): What's the best approach?"
```

### Reverse Brainstorming

```bash
gemini -m pro -o text -e "" "Reverse brainstorm: How could we make [goal] FAIL?

Goal: [your goal]

1. List ways to guarantee failure
2. Then flip each into a success strategy
3. Identify hidden risks from the failure scenarios"
```

### Constraint Removal

```bash
gemini -m pro -o text -e "" "Brainstorm without constraints:

PROBLEM: [your problem]
CURRENT CONSTRAINTS: [list constraints]

1. What would you do with unlimited budget?
2. What if time wasn't a factor?
3. What if you had any technology?
4. What if there were no legacy systems?

Then: Which ideas can be scaled down to reality?"
```

## Domain-Specific Brainstorms

### Feature Ideas

```bash
gemini -m pro -o text -e "" "Generate feature ideas for:

PRODUCT: [description]
USERS: [who uses it]
CURRENT PAIN POINTS: [list issues]

Suggest features that:
- Solve real problems
- Differentiate from competitors
- Are technically feasible
- Can be built incrementally"
```

### Architecture Options

```bash
gemini -m pro -o text -e "" "Brainstorm architecture approaches for:

REQUIREMENTS:
- [requirement 1]
- [requirement 2]

CONSTRAINTS:
- [constraint 1]
- [constraint 2]

Generate 5 different architectural approaches with trade-offs."
```

### Naming Ideas

```bash
gemini -m pro -o text -e "" "Generate name ideas for:

WHAT: [what is being named]
QUALITIES: [characteristics to convey]
AVOID: [things to avoid]

Provide 15 options across categories:
- Descriptive names
- Abstract/creative names
- Compound words
- Acronyms
- References/allusions"
```

### Problem Decomposition

```bash
gemini -m pro -o text -e "" "Break down this complex problem:

PROBLEM: [description]

1. Identify sub-problems
2. Find the core challenge
3. Map dependencies between parts
4. Suggest which to tackle first
5. Identify quick wins vs. hard parts"
```

## Evaluation and Selection

### Idea Evaluation

```bash
gemini -m pro -o text -e "" "Evaluate these ideas against criteria:

IDEAS:
1. [idea 1]
2. [idea 2]
3. [idea 3]

CRITERIA:
- Feasibility (1-5)
- Impact (1-5)
- Effort (1-5, lower is better)
- Risk (1-5, lower is better)

Create a comparison matrix and recommend top choice."
```

### Combine Ideas

```bash
gemini -m pro -o text -e "" "Combine the best elements of these ideas:

IDEA A: [description]
IDEA B: [description]
IDEA C: [description]

Create hybrid approaches that take the strengths of each."
```

## Best Practices

1. **Quantity first** - Generate many ideas before judging
2. **Defer judgment** - Don't critique during generation
3. **Build on ideas** - Use 'yes, and...' thinking
4. **Embrace wild ideas** - They often lead to practical ones
5. **Visualize** - Sketch or diagram ideas
6. **Set constraints** - Paradoxically, limits boost creativity
7. **Take breaks** - Let ideas incubate
8. **Mix inputs** - Combine different perspectives
