---
name: debrief
description: This skill should be used when the user asks to "create a Debrief trace", "generate a code walkthrough", "make a narrated code explanation", "create a replay trace", "write trace narration", or mentions Debrief traces, JSONL trace files, or code walkthrough generation. Provides comprehensive guidance for writing natural, engaging narration that sounds like a senior engineer explaining code.
version: 2.4.0
argument-hint: [what to debrief - optional]
---

# Debrief Trace Authoring

## What to Debrief

**Topic/scope:** $ARGUMENTS

**CRITICAL:** Do NOT ask the user what they want to debrief or say "the skill is loaded." Act immediately:

- **If a topic/scope is provided above:** Create a trace for that specific topic. Read the relevant files, understand the code, and generate the trace JSONL file immediately.
- **If no topic/scope is provided (empty or blank above):** Debrief **everything you have done in this conversation so far.** Look at all files you created, modified, or discussed. Walk through each change, explaining what was done and why. Generate the trace JSONL file immediately.

In both cases, start working right away. Read the code, plan the walkthrough structure, and write the trace file. Never ask "what would you like me to debrief?" — the answer is either the argument above or the full conversation history.

**Trace file location:** Each trace goes in its own subfolder under `.debrief/replay/`. The folder and file share the same name:

```
.debrief/replay/<trace-name>/<trace-name>.jsonl
```

For example: `.debrief/replay/auth-refactor/auth-refactor.jsonl`

Choose a short, descriptive kebab-case name for the trace (e.g., `auth-refactor`, `add-caching`, `fix-race-condition`).

---

This skill teaches how to create Debrief replay traces with natural, engaging narration. The goal is to sound like a senior engineer explaining code to a colleague, not like documentation or a robot.

## Highlight Stability

The extension automatically snapshots referenced files when a trace is loaded, so highlights stay accurate even if the code changes later. No special action is needed from the agent — just create the trace normally.

## Key Principles

1. **Atomic steps**: One highlight per step, one focused thought per narration
2. **Grouped by topic**: Related steps are wrapped in `sectionStart`/`sectionEnd` for smooth playback
3. **Natural narration**: Sound like a senior engineer, not a robot

## Trace Format

Debrief traces are JSONL files (one JSON object per line). Each line is a trace event:

```jsonl
{"id":"e1","type":"sectionStart","title":"Authentication","narration":""}
{"id":"e2","type":"highlightRange","filePath":"src/auth.ts","range":{"startLine":10,"startCol":0,"endLine":15,"endCol":0},"title":"Token extraction","narration":"Let's start with how we grab the token from the request."}
{"id":"e3","type":"highlightRange","filePath":"src/auth.ts","range":{"startLine":18,"startCol":0,"endLine":22,"endCol":0},"title":"Token verification","narration":"Once we have it, we verify it against our secret here."}
{"id":"e4","type":"sectionEnd","title":"","narration":""}
```

## Event Types

| Type | Purpose | When to Use |
|------|---------|-------------|
| `highlightRange` | Navigate to file + highlight lines | **Primary event** - use for most explanations |
| `say` | Narration only, no navigation | Transitions, summaries, context without code |
| `sectionStart` | Begin a group of related steps | Group 2-5 steps that flow together |
| `sectionEnd` | End a section | Pair with `sectionStart` |
| `openFile` | Open file without highlighting | Rarely needed - prefer `highlightRange` |
| `showDiff` | Show before/after diff | Code changes, refactoring explanations |

## Fine-Grained Steps: Break It Down

**The #1 mistake is highlighting too much code at once.** Large chunks overwhelm users. Instead, break code into small, digestible pieces that are easy to follow.

### The Golden Rule

**Highlight 2-6 lines per step.** If you're highlighting more than 8 lines, you're probably trying to explain too much at once.

### How to Break Down a Function

When explaining a function, DON'T highlight the whole thing. Instead:

1. **Step 1**: Highlight just the function signature (1-2 lines)
2. **Step 2**: Highlight the first logical chunk (2-4 lines)
3. **Step 3**: Highlight the next chunk (2-4 lines)
4. **Continue**: One concept per step until the function is covered

### Example: Breaking Down a Function

Given this function:
```typescript
async function fetchUserData(userId: string): Promise<User> {
  const cached = await cache.get(userId);
  if (cached) {
    return cached;
  }

  const user = await db.users.findById(userId);
  if (!user) {
    throw new NotFoundError(`User ${userId} not found`);
  }

  await cache.set(userId, user, { ttl: 300 });
  return user;
}
```

**BAD: One giant step (13 lines)**
```json
{"range":{"startLine":1,"endLine":13},"narration":"This function fetches user data, first checking the cache, then the database, and caches the result."}
```

**GOOD: Fine-grained steps**
```jsonl
{"id":"e1","range":{"startLine":1,"endLine":1},"title":"Function signature","narration":"This async function takes a user ID and returns their data."}
{"id":"e2","range":{"startLine":2,"endLine":4},"title":"Cache check","narration":"First, we check if the user is already in cache. If so, we return early."}
{"id":"e3","range":{"startLine":6,"endLine":9},"title":"Database lookup","narration":"If not cached, we fetch from the database and throw if not found."}
{"id":"e4","range":{"startLine":11,"endLine":12},"title":"Cache and return","narration":"Finally, we cache the result for 5 minutes before returning."}
```

### Step Size Guidelines

| Lines | Verdict | When to Use |
|-------|---------|-------------|
| 1-2 | Perfect | Function signatures, single statements, key lines |
| 3-6 | Ideal | Most steps - one logical chunk |
| 7-10 | Caution | Only if lines are tightly coupled |
| 11+ | Too much | Split into multiple steps |

### Signs You Need to Split

- Your narration contains "and then" or "also"
- You're explaining multiple concepts
- The highlighted code has blank lines separating logic
- You're scrolling to see the whole highlight

### More Examples of Fine-Grained Splitting

**Explaining a class:**
```jsonl
{"id":"e1","range":{"startLine":1,"endLine":3},"title":"Class declaration","narration":"This service class handles all authentication logic."}
{"id":"e2","range":{"startLine":4,"endLine":6},"title":"Dependencies","narration":"We inject the user repository and token service."}
{"id":"e3","range":{"startLine":8,"endLine":8},"title":"Login method","narration":"The main login method takes credentials."}
{"id":"e4","range":{"startLine":9,"endLine":11},"title":"Find user","narration":"First, we look up the user by email."}
{"id":"e5","range":{"startLine":12,"endLine":14},"title":"Verify password","narration":"Then we verify the password hash matches."}
```

**Explaining a config object:**
```jsonl
{"id":"e1","range":{"startLine":1,"endLine":2},"title":"Config setup","narration":"Here's our database configuration."}
{"id":"e2","range":{"startLine":3,"endLine":4},"title":"Connection settings","narration":"Host and port come from environment variables."}
{"id":"e3","range":{"startLine":5,"endLine":6},"title":"Pool settings","narration":"We use a connection pool with min 2, max 10 connections."}
{"id":"e4","range":{"startLine":7,"endLine":8},"title":"Timeout settings","narration":"Queries timeout after 30 seconds to prevent hanging."}
```

### One Concept Per Step

- **One highlight** per step
- **One idea** per narration
- **1-2 sentences** max per step
- If you say "and then", split into two steps
- Steps within a section play with ~100ms pause (feels like continuous speech)

## Section Structure

Sections group related steps. Use them sparingly and semantically.

### Section Rules

- **Max 2-3 levels deep** - Never nest sections more than 3 levels
- **Semantic nesting only** - Only nest when there's a clear parent-child relationship:
  - Good: "Authentication" -> "Login Handler" -> (steps)
  - Bad: Every sequential section nested inside the previous
- **Close sections before opening siblings** - If you're moving to a new area, close the current section first
- **Prefer flat** - When in doubt, use flat sections at the same level
- Group **2-5 steps** per section (sweet spot for flow)
- `sectionStart` and `sectionEnd` have **empty narration** (no TTS)
- Use descriptive titles for the timeline

### Example - Good Section Nesting

```jsonl
{"type": "sectionStart", "title": "API Layer"}
{"type": "highlightRange", "title": "Router setup", ...}
{"type": "sectionStart", "title": "Auth Middleware"}
{"type": "highlightRange", "title": "Token validation", ...}
{"type": "sectionEnd"}
{"type": "sectionEnd"}
{"type": "sectionStart", "title": "Database Layer"}
...
```

### Example - Bad (infinite nesting)

```jsonl
{"type": "sectionStart", "title": "API Layer"}
{"type": "sectionStart", "title": "Database Layer"}  // Wrong! Should close API first
{"type": "sectionStart", "title": "Service Layer"}   // Wrong! Even deeper nesting
```

### Example: Grouped Steps

```jsonl
{"id":"s1","type":"sectionStart","title":"Request Validation","narration":""}
{"id":"e1","type":"highlightRange","filePath":"src/api/validate.ts","range":{"startLine":10,"startCol":0,"endLine":18,"endCol":0},"title":"Schema check","narration":"First, we validate the request body against our schema."}
{"id":"e2","type":"highlightRange","filePath":"src/api/validate.ts","range":{"startLine":20,"startCol":0,"endLine":28,"endCol":0},"title":"Auth check","narration":"If that passes, we verify the user has permission."}
{"id":"e3","type":"highlightRange","filePath":"src/api/validate.ts","range":{"startLine":30,"startCol":0,"endLine":38,"endCol":0},"title":"Rate limiting","narration":"Finally, we check they haven't exceeded their rate limit."}
{"id":"s1-end","type":"sectionEnd","title":"","narration":""}
{"id":"e4","type":"say","title":"Transition","narration":"With validation done, let's see what happens next."}
```

## Writing Natural Narration

### DO: Sound Like a Senior Engineer

Write as if you're sitting next to a colleague, pointing at their screen:

```json
{"narration": "This is where we grab the token from the Authorization header."}
{"narration": "If verification fails, we bail out early with a 401."}
{"narration": "The clever bit here is how we handle the retry logic."}
```

### DON'T: Sound Like Documentation

Avoid robotic, structured language:

```json
// BAD - sounds like a robot
{"narration": "This section contains the authentication middleware implementation."}
{"narration": "Line 12 extracts the token. Line 15 performs verification."}
```

### Narration Guidelines

1. **Use conversational phrases**: "Let's look at...", "Notice how...", "The key insight here is...", "What's happening is...", "The clever bit is..."

2. **Explain WHY, not just WHAT**: Don't just describe code - explain the reasoning, trade-offs, or gotchas.

3. **Connect ideas**: Use transitions like "Now that we have X, we can...", "This feeds into...", "Building on that..."

4. **Keep it brief**: Each step should be 1-2 sentences. Long explanations should be split into multiple steps.

5. **Avoid announcements**: Don't say "Now entering the Authentication section" - just explain the code.

## Event Schema

### highlightRange (most common)

```json
{
  "id": "e1",
  "type": "highlightRange",
  "filePath": "src/api/auth.ts",
  "range": {
    "startLine": 10,
    "startCol": 0,
    "endLine": 18,
    "endCol": 0
  },
  "title": "Short title for timeline",
  "narration": "Brief, focused explanation of this specific code."
}
```

### say (narration only)

```json
{
  "id": "e2",
  "type": "say",
  "title": "Transition",
  "narration": "Now let's see how this is used in the routes."
}
```

### sectionStart / sectionEnd

```json
{"id": "s1", "type": "sectionStart", "title": "Section Name", "narration": ""}
{"id": "s1-end", "type": "sectionEnd", "title": "", "narration": ""}
```

## User Comments (Code Feedback)

Users can add comments to any step while reviewing the trace. These comments are saved to the JSONL file as a `comment` field and represent **feedback about the code shown in that step**.

### When Asked to Review a Trace

**Always check for user comments.** Comments tell you what the user wants changed in the code:

```json
{"id":"e5","type":"highlightRange","filePath":"src/auth.ts","range":{"startLine":10,"endLine":18},"title":"Token validation","narration":"...","comment":"This should also check token expiration"}
```

This means: go to `src/auth.ts` lines 10-18 and add token expiration checking.

### How to Handle Comments

1. **Scan the trace for `comment` fields** before making changes
2. **Each comment is a code change request** for the highlighted file/lines
3. **Address the feedback** by modifying the actual source code
4. **After fixing**, you may update or regenerate the trace to reflect changes

### Example Comments and Actions

| Comment on Step | Action in Code |
|-----------------|----------------|
| "Add error handling here" | Add try/catch to the highlighted code |
| "This should be async" | Refactor the function to be async |
| "Missing null check" | Add validation for null/undefined |
| "Use the new API instead" | Update to use the newer API |

## Risk Annotations

Risks are explicitly specified by the agent in the trace to highlight steps that need reviewer attention.

### When to Add Risks

Only add risks for steps that truly warrant attention:
- **security**: Touches auth, encryption, user data, permissions
- **breaking-change**: Changes public API, removes features
- **migration**: Database schema changes
- **performance**: Could impact performance significantly

### Risk Syntax

```json
{
  "id": "e1",
  "type": "highlightRange",
  "filePath": "src/auth/validate.ts",
  "range": {"startLine": 10, "startCol": 0, "endLine": 18, "endCol": 0},
  "title": "Validate user token",
  "narration": "This is where we validate the JWT token from the request.",
  "risks": [
    {"category": "security", "label": "User authentication logic"}
  ]
}
```

### Multiple Risks

A step can have multiple risks if warranted:

```json
{
  "risks": [
    {"category": "security", "label": "Password hashing"},
    {"category": "breaking-change", "label": "New auth flow"}
  ]
}
```

### Don't Over-Tag

- Not every API endpoint is a "public API change"
- Not every file in `/api/` needs a risk tag
- Only tag genuine risks that need reviewer attention
- If you're unsure whether something is a risk, it probably isn't

## Complete Example

Here's a well-structured trace for explaining a caching implementation:

```jsonl
{"id":"s1","type":"sectionStart","title":"Cache Interface","narration":""}
{"id":"e1","type":"highlightRange","filePath":"src/cache.ts","range":{"startLine":1,"startCol":0,"endLine":8,"endCol":0},"title":"Interface definition","narration":"The caching system is built around this simple interface."}
{"id":"e2","type":"highlightRange","filePath":"src/cache.ts","range":{"startLine":5,"startCol":0,"endLine":6,"endCol":0},"title":"Core methods","narration":"Get and set are your basic operations."}
{"id":"e3","type":"highlightRange","filePath":"src/cache.ts","range":{"startLine":7,"startCol":0,"endLine":8,"endCol":0},"title":"TTL parameter","narration":"The TTL parameter is what makes it interesting - every entry can have its own expiration."}
{"id":"s1-end","type":"sectionEnd","title":"","narration":""}
{"id":"s2","type":"sectionStart","title":"Memory Implementation","narration":""}
{"id":"e4","type":"highlightRange","filePath":"src/cache.ts","range":{"startLine":17,"startCol":0,"endLine":24,"endCol":0},"title":"Storage maps","narration":"Here's the in-memory implementation. This Map stores the values, and this second one tracks expiration times."}
{"id":"e5","type":"highlightRange","filePath":"src/cache.ts","range":{"startLine":28,"startCol":0,"endLine":35,"endCol":0},"title":"Get with TTL check","narration":"When you call get, we check the timestamp first and return undefined if it's stale."}
{"id":"e6","type":"highlightRange","filePath":"src/cache.ts","range":{"startLine":50,"startCol":0,"endLine":56,"endCol":0},"title":"Cleanup interval","narration":"The clever bit is this cleanup interval that removes expired entries every 60 seconds."}
{"id":"s2-end","type":"sectionEnd","title":"","narration":""}
{"id":"e7","type":"say","title":"Summary","narration":"That's the core caching layer - intentionally simple, just TTL-based expiration."}
```

## Structuring a Walkthrough

### Recommended Structure

1. **Opening** (`say`): Brief context about what we'll cover
2. **Sections** (`sectionStart`/`sectionEnd`): Group related concepts
   - 2-5 `highlightRange` steps per section
   - Each step: one highlight, one focused explanation
3. **Transitions** (`say`): Connect sections naturally
4. **Closing** (`say`): Summarize key takeaways

### Things to Avoid

- **Overloaded steps**: If you're highlighting 20+ lines or writing a paragraph, split it up
- **Separate "open file" steps**: Merge into `highlightRange` - the file opens automatically
- **Section announcements**: Don't say "Now entering the Authentication section"
- **Over-explaining**: Trust your audience to understand code basics
- **Orphan steps**: Steps outside sections have longer pauses - group related ones

## Checklist Before Generating

- [ ] Each step highlights 2-6 lines (max 8-10 for tightly coupled code)
- [ ] Functions are broken down: signature first, then body in chunks
- [ ] Narration is 1-2 sentences per step
- [ ] No "and then" in narration (split if needed)
- [ ] Related steps are grouped in sections
- [ ] Section nesting is max 2-3 levels deep with semantic parent-child relationships
- [ ] Section events have empty narration
- [ ] Natural, conversational language (not robotic)
- [ ] Explanations focus on WHY, not just WHAT
- [ ] Transitions connect sections naturally
- [ ] IDs are unique and sequential (e1, e2, e3... or s1, s1-end for sections)
- [ ] Risk annotations only on genuinely risky steps (security, breaking-change, migration, performance)
- [ ] No metadata header needed — the extension handles highlight stability via snapshots
