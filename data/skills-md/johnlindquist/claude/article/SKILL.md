---
name: article
description: Generate technical articles and documentation using AI. Use for writing blog posts, documentation, and technical content.
---

# Article Generator

Create technical articles and documentation with AI assistance.

## Prerequisites

```bash
# Claude CLI for article generation
npm install -g @anthropic-ai/claude-cli
export ANTHROPIC_API_KEY=your_api_key

# Or Gemini as alternative
pip install google-generativeai
export GEMINI_API_KEY=your_api_key
```

## Article Operations

### Generate Article

```bash
claude --print --model opus "Write a technical article about: [topic]

Requirements:
- Target audience: [developers/beginners/etc]
- Length: ~[1500] words
- Include code examples
- Practical focus

Structure:
1. Hook/intro that establishes the problem
2. Context/background
3. Main content with examples
4. Best practices
5. Conclusion with next steps"
```

### Quick Draft

```bash
gemini -m pro -o text -e "" "Write a first draft article about: [topic]

Keep it concise (~800 words) with:
- Clear thesis
- 3-4 main points
- One code example
- Actionable takeaway"
```

### Expand Outline

```bash
gemini -m pro -o text -e "" "Expand this outline into a full article:

OUTLINE:
1. [Point 1]
2. [Point 2]
3. [Point 3]

For each section, provide:
- 2-3 paragraphs
- Relevant examples
- Transitions between sections"
```

## Article Types

### Tutorial

```bash
claude --print --model opus "Write a step-by-step tutorial for: [task]

Format:
- Prerequisites section
- Numbered steps with code
- Expected output at each step
- Common errors and fixes
- Complete working example at end"
```

### Comparison Article

```bash
gemini -m pro -o text -e "" "Write a comparison article:

COMPARING: [Option A] vs [Option B]
CONTEXT: [Use case]

Include:
- Overview of each
- Feature comparison table
- Code examples for each
- When to use which
- Clear recommendation"
```

### Explainer

```bash
gemini -m pro -o text -e "" "Write an explainer article about: [concept]

Audience: [technical level]

Cover:
- What it is (simple definition)
- Why it matters
- How it works (with diagrams if helpful)
- Real-world examples
- Common misconceptions"
```

### How We Built It

```bash
gemini -m pro -o text -e "" "Write a 'how we built it' article based on:

PROJECT: [description]
TECH STACK: [technologies]
CHALLENGES: [key challenges faced]
SOLUTIONS: [how you solved them]

Format as engineering blog post with:
- Problem statement
- Architecture decisions
- Implementation details
- Lessons learned
- Results/metrics"
```

## Content Enhancement

### Verify Technical Accuracy

```bash
ARTICLE=$(cat draft.md)
gemini -m pro -o text -e "" "Review this technical article for accuracy:

$ARTICLE

Check:
1. Code examples work correctly
2. Technical claims are accurate
3. Best practices are current
4. No outdated information
5. Security considerations

Flag any issues with corrections."
```

### Improve Readability

```bash
ARTICLE=$(cat draft.md)
gemini -m pro -o text -e "" "Improve the readability of this article:

$ARTICLE

Focus on:
- Clearer sentences
- Better transitions
- Active voice
- Removing jargon
- Adding helpful examples"
```

### Add Code Examples

```bash
ARTICLE=$(cat draft.md)
gemini -m pro -o text -e "" "Add practical code examples to this article:

$ARTICLE

For each concept:
- Add working code snippet
- Include comments
- Show expected output
- Provide variations where helpful"
```

### Generate Revision

```bash
ARTICLE=$(cat draft.md)
FEEDBACK="[feedback from reviewers]"

gemini -m pro -o text -e "" "Revise this article based on feedback:

CURRENT:
$ARTICLE

FEEDBACK:
$FEEDBACK

Incorporate the feedback while maintaining the article's voice and structure."
```

## Structure Templates

### Blog Post Template

```markdown
# [Catchy Title]

[1-2 sentence hook that identifies the problem]

## The Problem

[Describe the pain point readers face]

## The Solution

[Introduce your approach]

### [Key Point 1]

[Explanation with code example]

### [Key Point 2]

[Explanation with code example]

## Putting It Together

[Complete example combining the concepts]

## Conclusion

[Summary and call to action]
```

### Tutorial Template

```markdown
# How to [Do Something]

## Prerequisites

- [Requirement 1]
- [Requirement 2]

## What We're Building

[Brief description and screenshot/diagram]

## Step 1: [First Step]

[Instructions]

```code
[Example]
```

## Step 2: [Second Step]

...

## Complete Code

```code
[Full working example]
```

## Next Steps

[Where to go from here]
```

## Best Practices

1. **Start with the reader** - What problem do they have?
2. **Show, don't tell** - Use code examples
3. **One idea per section** - Keep it focused
4. **Use concrete examples** - Abstract concepts need grounding
5. **Include working code** - Test everything
6. **End with action** - Tell readers what to do next
7. **Get feedback** - Have someone else read it
8. **Revise ruthlessly** - First drafts are just the start
