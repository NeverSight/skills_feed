---
name: tzurot-council-mcp
description: 'MCP consultation procedures. Invoke with /tzurot-council-mcp when stuck, planning major refactors, or needing a second opinion.'
lastUpdated: '2026-02-04'
---

# Council MCP Procedures

**Invoke with /tzurot-council-mcp** when you need external AI consultation.

## When to Consult Council

### Always Use For

- **Major Refactorings (>500 lines)**
- **Before Completing Major PRs**
- **When Thinking "This seems unnecessary"** - STOP! Consult before removing code.
- **Structured Debugging**

### Don't Use For

- Questions answered by existing docs/skills
- Obvious code issues (typos, syntax errors)
- Small style preferences

## Debugging Procedure

```typescript
mcp__council__debug({
  error_message: 'Memory leak in BullMQ workers',
  code_context: 'Workers OOM after 2 hours',
  previous_attempts: ['Checked event listeners', 'Reviewed Redis connections'],
});
```

## Code Review Procedure

```typescript
mcp__council__code_review({
  code: changes,
  focus: 'behavior preservation, edge cases',
  language: 'typescript',
});
```

## Refactoring Plan Procedure

```typescript
mcp__council__refactor({
  code: myCode,
  goal: 'reduce_complexity', // extract_method, simplify_logic, improve_naming, etc.
  language: 'typescript',
});
```

## Brainstorming Procedure

```typescript
mcp__council__brainstorm({
  topic: 'Risks in refactoring PersonalityService',
  constraints: 'Must maintain exact functionality',
});
```

## Model Selection

| Task Type      | Recommended Models                 |
| -------------- | ---------------------------------- |
| Coding/Review  | Claude Sonnet 4, Claude 3.5 Sonnet |
| Reasoning/Math | DeepSeek R1, Gemini 3 Pro          |
| Vision/Images  | Gemini 2.5 Flash, Gemini 2.5 Pro   |
| Long Documents | Gemini (1M tokens)                 |

```typescript
// Get recommendation
mcp__council__recommend_model({ task: 'code_review' });

// Specify per-call
mcp__council__code_review({
  code: myCode,
  model: 'anthropic/claude-3.5-sonnet',
});
```

## Multi-Turn Conversations

```typescript
// Start session
const { session_id } = await mcp__council__start_conversation({
  model: 'deepseek/deepseek-r1',
  system_prompt: 'You are a TypeScript architecture expert',
  initial_message: 'Review this service design...',
});

// Continue
await mcp__council__continue_conversation({
  session_id,
  message: 'What about the error handling?',
});

// End and summarize
await mcp__council__end_conversation({
  session_id,
  summarize: true,
});
```

## When Council and Claude Disagree

**Resolution hierarchy:**

1. Project guidelines (CLAUDE.md, rules)
2. Existing codebase patterns
3. Technical correctness
4. User preference

## Available Tools

| Tool                            | Purpose               |
| ------------------------------- | --------------------- |
| `mcp__council__ask`             | General questions     |
| `mcp__council__brainstorm`      | Brainstorm ideas      |
| `mcp__council__code_review`     | Code review           |
| `mcp__council__debug`           | Structured debugging  |
| `mcp__council__refactor`        | Refactoring plans     |
| `mcp__council__test_cases`      | Test case suggestions |
| `mcp__council__explain`         | Explain code/concepts |
| `mcp__council__recommend_model` | Model recommendations |
