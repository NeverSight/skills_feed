---
name: c3-query
description: |
  Navigates C3 architecture docs and explores corresponding code to answer architecture questions.
  Use when the user asks "where is X", "how does X work", "explain X", "show me the architecture",
  "find component", "what handles X", "what constraints apply to X", or references C3 IDs (c3-0, c3-1, adr-*).
  Requires .c3/ to exist. For changes, route to c3-alter instead.
---

# C3 Query - Architecture Navigation

Navigate C3 docs AND explore corresponding code. Full context = docs + code.

**Relationship to c3-navigator agent:** This skill defines the query workflow. The `c3-skill:c3-navigator` agent implements this workflow with sub-agent dispatch for token efficiency. Use the agent when spawning via Task tool; use this skill directly for inline execution.

## REQUIRED: Load References

Before proceeding, use Glob to find and Read these files:
1. `**/references/skill-harness.md` - Red flags and complexity rules
2. `**/references/layer-navigation.md` - How to traverse C3 docs

## Query Flow

```
Query → Clarify Intent → Navigate Layers → Extract References → Explore Code
              │
              └── Use AskUserQuestion if ambiguous
```

## Progress Checklist

```
Query Progress:
- [ ] Step 0: Intent clarified (or skipped if specific)
- [ ] Step 1: Context navigated (found relevant container)
- [ ] Step 2: References extracted (code paths, symbols)
- [ ] Step 3: Code explored (verified against docs)
- [ ] Response delivered with layer, refs, insights
```

---

## Step 0: Clarify Intent

**Ask when:**
- Query vague ("how does X work?" - which aspect?)
- Multiple interpretations ("authentication" - login? tokens? sessions?)
- Scope unclear ("frontend" - whole container or specific component?)

**Skip when:**
- Query includes C3 ID (c3-102)
- Query specific ("where is login form submitted?")
- User says "show me everything about X"

---

## Step 1-2: Navigate and Extract

Follow layer navigation: **Context → Container → Component**

| Doc Section | Extract For Code |
|-------------|------------------|
| Component name | Class/module names |
| `## References` | Direct file paths, symbols |
| Technology | Framework patterns |
| Entry points | Main files, handlers |

### Reference Lookup

If query relates to patterns/conventions:
1. Check `.c3/refs/` for `ref-*` matching topic
2. Return ref content + citing components

---

## Step 3: Explore Code

Use extracted references:
- **Glob**: `src/auth/**/*.ts`
- **Grep**: Class names, functions
- **Read**: Specific files from `## References`

---

## Query Types

| Type | User Says | Response |
|------|-----------|----------|
| Docs | "where is X", "explain X" | Docs + suggest code exploration |
| Code | "show me code for X" | Full flow through code |
| Deep | "explore X thoroughly" | Docs + Code + Related |
| Constraints | "what rules/constraints apply to X" | Full constraint chain |

---

## Constraint Chain Query

When user asks about rules, constraints, or boundaries for a layer:

### Flow

```
Identify Layer → Read Upward Chain → Collect Cited Refs → Synthesize Chain
```

### Steps

1. **Identify target layer** from query (c3-NNN, c3-N, or c3-0)

2. **Read upward through hierarchy:**
   - If component: read component → container → context
   - If container: read container → context
   - If context: read context only

3. **At each level, extract:**
   - Explicit constraints ("components MUST...", "MUST NOT...")
   - Implicit boundaries (what the layer is responsible for)
   - Layer-specific rules

4. **Collect cited refs:**
   - From component's `Related Refs` section
   - From container's pattern references
   - From context's system-wide patterns

5. **Read each cited ref** and extract key rules

### Response Format

```
**Constraint Chain for c3-NNN (Component Name)**

**Context Constraints (c3-0):**
- [System-wide rule 1]
- [System-wide rule 2]

**Container Constraints (c3-N):**
- [Container boundary 1]
- [Coordination rule]

**Cited Pattern Constraints:**
- **ref-X:** [Key rules from this pattern]
- **ref-Y:** [Key rules from this pattern]

**Layer Boundaries:**
This component MAY:
- [Permitted responsibilities]

This component MUST NOT:
- [Prohibited actions - from higher layers]

**Visualization:**
[Mermaid diagram showing constraint inheritance]
```

### Example

```
User: "What constraints apply to c3-201?"

1. Read c3-201-auth-middleware.md → cites ref-error-handling, ref-auth
2. Read c3-2-api/README.md → "Middleware must be stateless"
3. Read .c3/README.md → "All auth uses RS256"
4. Read ref-error-handling.md → "Use correlation IDs"
5. Read ref-auth.md → "Tokens expire in 24h"

Response:
**Constraint Chain for c3-201 (Auth Middleware)**

**Context Constraints (c3-0):**
- All authentication must use RS256 signing

**Container Constraints (c3-2-api):**
- Middleware must be stateless
- Request context via headers, not shared state

**Cited Pattern Constraints:**
- **ref-error-handling:** Use correlation IDs in all error responses
- **ref-auth:** Token expiry 24h, refresh via /auth/refresh

**Layer Boundaries:**
This component MAY:
- Validate JWT tokens
- Reject unauthorized requests
- Set request context for downstream handlers

This component MUST NOT:
- Store session state (container: stateless middleware)
- Define new auth schemes (context: RS256 only)
- Handle business logic errors (use ref-error-handling pattern)
```

## Edge Cases

| Situation | Action |
|-----------|--------|
| Topic not in C3 docs | Search code directly, suggest documenting if significant |
| Spans multiple containers | List all affected containers, explain relationships |
| Docs seem stale | Note discrepancy, suggest `/c3 audit` or `/alter` to fix |

---

## Examples

**Example 1: Component lookup**
```
User: "Where is authentication handled?"

Step 1: Read .c3/README.md → Find c3-2-api container handles auth
Step 2: Read .c3/c3-2-api/README.md → Find c3-201-auth-middleware
Step 3: Read .c3/c3-2-api/c3-201-auth-middleware.md → Get code refs

Response:
**Layer:** c3-201 (Auth Middleware)

Authentication is handled by the AuthMiddleware component in the API container.

**Code References:**
- `src/api/middleware/auth.ts` - JWT validation
- `src/api/middleware/session.ts` - Session management

**Key Insights:**
Uses RS256 for JWT signing. Sessions stored in Redis.

**Related:** See c3-202-user-service for user lookup
```

**Example 2: Pattern lookup**
```
User: "How does error handling work?"

Step 1: Read .c3/README.md → Multiple containers
Step 2: Check .c3/refs/ → Find ref-error-handling.md

Response:
**Pattern:** ref-error-handling

Error handling follows a centralized pattern documented in refs.

**Pattern Summary:**
- All errors extend BaseError class
- HTTP errors map to status codes via errorToStatus()
- Logged with correlation ID

**Used By:** c3-201, c3-203, c3-205
```

---

## Response Format

```
**Layer:** <c3-id> (<name>)

<Architecture from docs>

**Code References:**
- `path/file.ts` - <role>

**Key Insights:**
<Observations from code>

**Related:** <navigation hints>
```
