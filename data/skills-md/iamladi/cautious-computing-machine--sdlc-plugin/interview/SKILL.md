---
name: interview
description: Interview me about anything in depth
argument-hint: [topic or file]
model: opus
---

# Deep Interview Skill

Conduct an in-depth interview about any topic, file, or idea the user provides.

## Detecting Input Type

First, determine what the user wants to discuss:

1. **If `$1` looks like a file path** (contains `/`, `.md`, `.ts`, etc.):
   - Read the file using the Read tool
   - Interview about its contents
   - At the end, update the file in-place with refined insights

2. **If `$1` is a topic or description**:
   - Interview about that concept/idea
   - At the end, summarize the key insights

## Interview Process

### Round-by-Round Approach

Interview iteratively - one round of questions at a time:

1. **Analyze** what you know so far
2. **Identify** the most important ambiguities, assumptions, or unexplored areas
3. **Ask 1-4 questions** using `AskUserQuestion` tool
4. **Process** the answers
5. **Repeat** until the user says "done" or you've covered everything meaningful

### Question Quality Rules

**DO ask about:**
- Implementation tradeoffs ("Should this be sync or async?")
- Edge cases ("What happens when the input is empty?")
- Scope boundaries ("Is X in scope for the first version?")
- User preferences ("Do you prefer explicit errors or silent fallbacks?")
- Architecture choices ("Should this be a separate service or integrated?")
- Constraints ("Are there performance requirements?")
- Alternatives ("Have you considered approach Y instead?")

**DON'T ask:**
- Obvious things ("Do you want tests?")
- Things you can infer ("What language?" when codebase is TypeScript)
- Yes/no validation questions ("Is this correct?")
- Surface-level stuff ("What's the feature name?")
- Questions answerable by quick code discovery (read configs/existing patterns first)
- Open-ended questions when multiple-choice would eliminate branches faster

### Question Format

Always use `AskUserQuestion` with multiple choice options. Optimize for fast responses:

**Standard format:**
```
AskUserQuestion:
  questions:
    - question: "How should the system handle API failures?"
      header: "Errors"
      options:
        - label: "Retry with backoff (Recommended)"
          description: "Automatically retry failed requests with exponential backoff"
        - label: "Fail fast"
          description: "Return error immediately, let caller decide"
        - label: "Not sure - you decide"
          description: "Let me pick based on codebase patterns"
      multiSelect: false
```

**For power users:** When asking multiple questions, add this footer:
> Reply format: `1a 2b` or `defaults` to accept all recommended options

**Always include:**
- One clearly marked "(Recommended)" option when you have a strong opinion
- A "Not sure - you decide" escape hatch for low-stakes decisions

### Interview Categories

Adapt questions based on context, but consider exploring:

1. **Technical Implementation**
   - Architecture patterns
   - Technology choices
   - Integration points
   - Data flow

2. **User Experience**
   - Interaction patterns
   - Error states
   - Edge cases
   - Feedback mechanisms

3. **Constraints & Requirements**
   - Performance needs
   - Security considerations
   - Scalability requirements
   - Compliance/regulatory

4. **Scope & Priorities**
   - Must-have vs nice-to-have
   - First version vs future iterations
   - Dependencies and blockers

5. **Risks & Concerns**
   - What could go wrong?
   - What are you uncertain about?
   - What alternatives exist?

## Completion

When the interview is complete (user says "done" or all areas explored):

**For file input:**
1. Summarize key decisions made during the interview
2. Update the original file with refined information
3. Add an "Interview Insights" or similar section if appropriate
4. Preserve the original structure

**For topic input:**
1. Provide a comprehensive summary of insights gathered
2. List key decisions and preferences discovered
3. Highlight any unresolved questions or areas for future exploration

## Topic

$ARGUMENTS
