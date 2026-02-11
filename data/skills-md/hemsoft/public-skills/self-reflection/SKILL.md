---
name: self-reflection
description: V1.0 - Helps AI agents troubleshoot difficult tasks and record lessons learned into persistent memory to prevent future mistakes and enable continuous improvement.
license: MIT
---

# Self-Reflection

Use this skill when a task was particularly difficult, required multiple retries, or resulted in unexpected behavior/errors. The goal is to analyze what went wrong and store actionable insights to avoid future mistakes.

## Core Principles

When reflecting on mistakes, consider these guidelines:

- **Never Fabricate** - Don't invent numbers, counts, paths, or URLs without verifying
- **Verify Before Asserting** - Read files, check paths, run commands to get real data
- **Admit Uncertainty** - Say "I don't know" rather than guessing with false confidence
- **Be Consistent** - Follow established output formats, count before stating counts
- **Self-Correct Promptly** - Acknowledge errors immediately, don't defend mistakes

## Workflow

### 1. Verify Output

Before concluding a task, always verify the final output against the user's original request and any relevant project specifications. Ensure all expected files, data points, and behaviors are present.

### 2. Analyze the Hiccup

If the verification fails or if the task was particularly difficult, review the conversation history and tool outputs to identify exactly where the execution deviated from the plan or encountered friction.

Ask yourself:

- What was the expected outcome?
- What actually happened?
- At what step did things go wrong?
- Was the error in understanding, execution, or verification?

### 3. Draft a Reflection

Summarize the issue, the root cause, and the specific strategy or "golden rule" that would have prevented it.

**Reflection Template:**

```markdown
### {Date} - {Task/Tool Name}

- **Issue**: {Brief description of the hiccup}
- **Root Cause**: {Why it happened}
- **Lesson**: {Actionable instruction for future self}
```

### 4. Human-in-the-Loop

Present the drafted reflection to the user:

- Explain what you intend to save to memory
- Ask for their agreement
- Ask if they have any additional input or corrections

### 5. Record to Memory

Once approved, save the insight to a persistent location:

- Create or update a file like `memories/lessons-learned.md`
- Or use a task-specific file under `memories/troubleshooting/`
- If no memory system is available, present the reflection for the user to save

## Example Entry

```markdown
### 2026-01-30 - File Path Verification

- **Issue**: Assumed a config file existed at the expected path without checking
- **Root Cause**: Made an assumption based on typical project structure instead of verifying
- **Lesson**: Always use `test -f` or equivalent to verify file existence before attempting to read or modify
```

## When to Trigger Self-Reflection

- Task required more than 2 retry attempts
- User had to correct an error in your output
- Tool call failed unexpectedly
- Output didn't match user expectations
- You had to apologize for a mistake

## Categories of Common Issues

| Category | Example | Prevention |
|----------|---------|------------|
| **Assumption** | Assumed file exists | Verify before acting |
| **Misread** | Misunderstood user intent | Clarify ambiguous requests |
| **Tool Misuse** | Wrong parameters | Check tool documentation |
| **Fabrication** | Made up a count or path | Always verify with tools |
| **Incomplete** | Missed a step | Review checklist before completing |

## Benefits

- **Pattern Recognition** - Identify recurring mistakes
- **Continuous Improvement** - Build a knowledge base of lessons
- **Accountability** - Document what went wrong and why
- **Prevention** - Avoid repeating the same mistakes

---

*"The only real mistake is the one from which we learn nothing."* — Henry Ford
