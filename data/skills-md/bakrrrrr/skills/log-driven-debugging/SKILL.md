---
name: "log-driven-debugging"
description: "Guides systematic verification-based debugging for JavaScript/TypeScript (Node.js, Bun, browser). Use when: (1) User reports unexpected behavior, errors, or bugs, (2) Need to trace data flow or state changes without assuming root causes, (3) Issue requires identifying exactly where code deviates from expected behavior."
---

# Log-Driven Debugging

## Core Principle

**Never assume the cause. Verify with logs.**

## Debugging Workflow

1. **Gather Information**
   - Ask: "What is the exact symptom?"
   - Ask: "When does it occur?"
   - Ask: "What is the expected behavior?"

2. **Form Hypotheses**
   - List 2-3 probable causes ranked by likelihood
   - Consider: API issues, state mutations, async timing, type errors

3. **Add Targeted Logs**
   - Add `console.log` at probable cause points
   - Use log patterns from [patterns.md](references/patterns.md)
   - Always include context: variable names, values, and execution path

4. **Request Console Output**
   - Ask user: "Run your code and paste the complete console output"
   - For browser: "Open DevTools (F12) → Console tab → paste output"

5. **Analyze & Iterate**
   - Compare actual vs expected values
   - If log missing → code path is different than expected
   - If undefined/null → trace upstream
   - Repeat until root cause found

## Log Placement Strategy

- **Entry logs**: Log function/method entry with input parameters
- **Exit logs**: Log function/method exit with return values
- **Before/after critical operations**: Log state before and after mutations
- **Conditional branches**: Log which branch executed and why
- **Async operations**: Log before and after promises/await points
- **Boundary points**: Log data entering/leaving modules or components

## Log Format Cheatsheet

| Context        | Format                                                       |
| -------------- | ------------------------------------------------------------ |
| Variable       | `console.log('userId:', userId)`                             |
| Object         | `console.log('user:', JSON.stringify(user, null, 2))`        |
| Execution path | `console.log('[Service] Method starting...')`                |
| Error          | `console.error('[API] Failed:', error.message, error.stack)` |
| Timing         | `console.time('op'); ... console.timeEnd('op')`              |

## Example Interaction

**User**: "My API call returns undefined but should return user data"

**Agent adds logs**:

```javascript
async function getUser(id) {
  console.log("[getUser] Called with id:", id);
  const response = await fetch(`/api/users/${id}`);
  console.log("[getUser] Response status:", response.status);
  const data = await response.json();
  console.log("[getUser] Parsed data:", JSON.stringify(data, null, 2));
  return data.user.profile;
}
```

**Console output reveals**:

```
[getUser] Called with id: 123
[getUser] Response status: 200
[getUser] Parsed data: { "user": { "name": "John" } }
```

**Analysis**: `data.user.profile` is undefined because the API returns `{ user: { name } }` without a `profile` property → fix: return `data.user` or update API.

## When Not to Use

- **Build/compilation errors**: Clear error messages; no logs needed
- **Type-only issues**: Use TypeScript compiler diagnostics instead
- **Performance profiling**: Use browser DevTools Performance tab
- **Production debugging**: Consider structured logging (Winston, Pino)

## Common Patterns

See [patterns.md](references/patterns.md) for debugging scenarios:

- API/Network issues
- State mutation issues
- Async/timing issues
- Type/TypeScript issues
