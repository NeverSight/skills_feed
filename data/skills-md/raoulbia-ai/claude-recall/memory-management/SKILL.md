---
name: memory-management
description: Persistent memory for Claude across conversations. Use when starting any task, before writing or editing code, before making decisions, when user mentions preferences or conventions, when user corrects your work, or when completing a task that overcame challenges. Ensures Claude never repeats mistakes and always applies learned patterns.
version: "1.0.0"
license: "MIT"
---

# Memory Management

Persistent memory system that ensures Claude never repeats mistakes and always applies learned patterns across conversations.

## When to Use This Skill

Invoke memory search in these situations:

- **Starting any task** - Check for existing patterns, preferences, past failures
- **Before writing/editing code** - Apply learned conventions and avoid past mistakes
- **Before making architectural decisions** - Check for established patterns
- **When user mentions preferences** - Store for future sessions
- **When user corrects your work** - Store correction with highest priority
- **After overcoming a challenge** - Store the learning cycle (fail → fix → success)

## Key Directives

1. **ALWAYS search before acting** - Call `mcp__claude-recall__search` before Write, Edit, or significant Bash operations
2. **Apply what you find** - Use retrieved preferences, patterns, and corrections
3. **Capture corrections immediately** - User fixes are highest priority
4. **Store learning cycles** - When you fail then succeed, that's valuable knowledge
5. **Never store secrets** - No API keys, passwords, tokens, or PII

## Quick Reference

### Search (Before Every Task)

```
mcp__claude-recall__search({ "query": "[task] [domain] preferences patterns" })
```

Examples:
- Before tests: `"testing tdd framework location"`
- Before git: `"git commit branch workflow"`
- Before deploy: `"deploy docker build ci/cd"`
- Before coding: `"[language] style conventions preferences"`

### Store (When Something Important Happens)

```
mcp__claude-recall__store_memory({
  "content": "Description of what to remember",
  "metadata": { "type": "preference|correction|devops|success|failure" }
})
```

## What Gets Stored

### Automatic Capture (You Don't Need to Store)

The system auto-captures when users say:
- "I prefer X" / "Always use X" / "Never do X" → Preferences
- "We use X for Y" / "Tests go in X" → Project conventions
- "This is a [type] project" → Project context

### Manual Storage Required

Store these explicitly:

**Corrections** (highest priority):
```
User: "No, put tests in __tests__/ not tests/"
→ Store: "CORRECTION: Test files go in __tests__/ directory, not tests/"
```

**Complex workflows**:
```
→ Store: "Deploy process: 1) npm test 2) docker build 3) push to ECR 4) kubectl apply"
```

**Learning cycles** (fail → fix → success):
```
→ Store: "REST API failed due to CORS. Solution: Use GraphQL endpoint instead."
```

## Memory Priority Order

1. **Corrections** - User explicitly fixed a mistake (HIGHEST)
2. **DevOps** - Git, testing, deploy, architecture patterns
3. **Preferences** - Code style, tool choices, conventions
4. **Success/Failure** - Learning cycles and past mistakes

## What NOT to Store

Never store:
- API keys, tokens, passwords, secrets
- Personal emails, phone numbers, addresses
- Database connection strings with credentials
- Any sensitive configuration values

Safe to store:
- "We use JWT for auth" (pattern, not credentials)
- "API base URL is https://api.example.com" (non-sensitive)
- "PostgreSQL for production, SQLite for tests" (tool choice)

## Example Workflows

### Starting a New Task

```
1. User: "Add user authentication"

2. Search first:
   mcp__claude-recall__search({ "query": "authentication auth jwt session preferences" })

3. Found: "We use JWT for auth, store tokens in httpOnly cookies"

4. Implement using JWT + httpOnly cookies (not sessions)

5. User approves → Done (no need to store, just applied existing knowledge)
```

### User Corrects Your Work

```
1. You: Created auth with localStorage tokens

2. User: "No, we always use httpOnly cookies for security"

3. Fix the code

4. Store the correction:
   mcp__claude-recall__store_memory({
     "content": "CORRECTION: Always use httpOnly cookies for auth tokens, never localStorage",
     "metadata": { "type": "correction" }
   })
```

### Overcoming a Challenge

```
1. Tried: Redis sessions for auth
   Failed: "Session sync issues in k8s cluster"

2. User suggested: "Try stateless JWT"

3. Implemented JWT → Works!

4. Store the learning:
   mcp__claude-recall__store_memory({
     "content": "Auth in k8s: Redis sessions failed (sync issues). JWT stateless tokens work correctly.",
     "metadata": { "type": "success", "learning_cycle": true }
   })
```

## Troubleshooting

**Search returns nothing relevant:**
- Broaden keywords: include domain + task + "preferences patterns"
- This may be a new project with no history yet

**Automatic capture missed something:**
- Store it manually with appropriate type
- Future searches will find it

**Check what's been captured:**
```
mcp__claude-recall__get_recent_captures({ "limit": 10 })
```

---

**The Learning Loop**: Search → Apply → Execute → Capture outcomes → Better next time
