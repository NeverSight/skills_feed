---
name: documentation-standards
user-invocable: false
description: "Apply documentation standards: comment why not what, minimal comments (prefer clear code), maintain README with quick start, update docs with breaking changes. Use when writing comments, creating docs, reviewing documentation, or discussing what to document."
allowed-tools:
  - Read
  - Grep
  - Glob
---

# Documentation Standards

Universal principles for effective documentation. Language-agnostic—focus on what and when to document, not syntax.

## Core Principle

**Good code documents itself. Comments explain what code cannot.**

Prefer clear names and simple structure over comments. Write comments for reasoning, not restating.

---

## Comments vs Code

### When to Comment

**ALWAYS comment:**
- **Why** (reasoning, trade-offs, decisions)
  - "Use exponential backoff to avoid overwhelming API during outages"
  - "Chose algorithm X over Y because of O(n) vs O(n²) performance"

- **Non-obvious decisions**
  - "Cache invalidation: 5 minutes chosen to balance freshness vs load"
  - "Intentionally skipping validation here—already validated upstream"

- **Workarounds**
  - "Temporary fix for bug in library X version 1.2.3"
  - "Work around browser quirk in Safari < 15"

- **Gotchas and constraints**
  - "Must call init() before use or will throw"
  - "Not thread-safe—caller must synchronize"
  - "Order matters: must authenticate before making requests"

**SOMETIMES comment:**
- **Complex algorithms** (high-level what, not line-by-line)
  - "Binary search to find insertion point in sorted array"
  - "Dijkstra's algorithm for shortest path"

- **Business rules**
  - "Tax calculation per regulation ABC-123 effective Jan 2024"
  - "Discount tiers: 10% for >100 items, 20% for >500"

**RARELY comment:**
- **What** (code should be self-documenting)
  - If you need to explain what, improve naming/structure first

**NEVER comment:**
- Obvious code
  - Bad: `i++  // Increment i`
- Commented-out code (delete it—it's in git)
- Lies (outdated comments worse than no comments)

### "Why Not What" Principle

✅ **Good comments** (explain reasoning):
```
// Use exponential backoff to prevent thundering herd
retryDelay = baseDelay * Math.pow(2, attempt)

// Cache for performance—database query is expensive
const cachedResult = cache.get(key)
```

❌ **Bad comments** (restate code):
```
// Set retry delay to base delay times 2 to the power of attempt
retryDelay = baseDelay * Math.pow(2, attempt)

// Get cached result from cache
const cachedResult = cache.get(key)
```

### Exceptions to "Why Not What"

**Complex algorithms benefit from high-level "what":**
```
// Find longest common subsequence using dynamic programming
// Returns length and the subsequence itself
function longestCommonSubsequence(s1, s2)
```

**Public API contracts (inputs, outputs, errors):**
```
// Authenticates user with email and password
// Returns: User object on success
// Throws: AuthError if credentials invalid
// Throws: NetworkError if connection fails
function authenticate(email, password)
```

### Comment Density: Minimal

**Prefer over comments:**
1. Better names
2. Simpler code structure
3. Extracted functions (self-documenting)
4. Smaller modules

**Rule:** If you need a comment to explain what code does, refactor first.

**Comments should add information code cannot express.**

---

## README and Technical Docs

### README.md Structure

**Every project needs a README.**

**Minimal required sections:**

1. **What** (one sentence)
   - Clear, concise description
   - "Task management CLI tool for developers"

2. **Why** (problem it solves)
   - "Existing task managers don't integrate with git/editors"

3. **Quick Start** (fastest path to running)
   - Installation
   - Basic usage example
   - This comes FIRST after description

4. **Setup** (getting started)
   - Prerequisites
   - Installation steps
   - Configuration

**Optional sections** (add as needed):
- Examples (common use cases)
- Features (capabilities)
- Documentation (link to detailed docs)
- Contributing (how to help)
- License
- Troubleshooting (common issues)

### README Anti-Patterns

❌ **Novel-length README**
- Save detailed docs for separate files
- README should get you started, not cover everything

❌ **Out-of-date examples**
- Worse than no examples
- Update with breaking changes or delete

❌ **No quick start**
- Forcing users to read entire doc before trying it
- Put fastest path to success up front

❌ **Installation that doesn't work**
- Test your own installation instructions
- What works on your machine ≠ what works elsewhere

### Other Documentation Types

**ADRs (Architecture Decision Records):**
- **What:** Record of architectural decisions
- **When:** Making significant architectural choices
- **Format:** Context, Decision, Consequences
- **Example:** "Why we chose database X over Y"

**ARCHITECTURE.md:**
- **What:** High-level system design
- **When:** System complex enough to need overview
- **Content:** Components, relationships, data flow
- **Keep:** Updated with major changes

**CONTRIBUTING.md:**
- **What:** How to contribute to project
- **When:** Accepting external contributors (open source, team projects)
- **Content:** Setup, workflow, standards, review process

**CHANGELOG.md:**
- **What:** What changed between versions
- **When:** Project has releases/versions
- **Format:** Chronological, grouped by version
- **Include:** Added, Changed, Fixed, Removed

**API Documentation:**
- **What:** Public API reference
- **When:** Building libraries for others
- **Best:** Generated from code comments (stays in sync)
- **Avoid:** Manually maintained separate docs (get stale)

### When to Create Each Document

- **README:** ALWAYS (every project)
- **ADRs:** Significant architectural decisions
- **ARCHITECTURE.md:** Complex system needing diagram
- **CONTRIBUTING.md:** Accepting external contributions
- **CHANGELOG:** Versioned releases
- **API docs:** Libraries meant for other developers

---

## Documentation Maintenance

### When to Update Docs

**ALWAYS update:**
- Breaking changes (users depend on documented behavior)
- New features (users need to discover them)
- Deprecated features (warn before removal)

**USUALLY update:**
- Bug fixes that change behavior
- New configuration options
- Performance improvements (if significant)

**RARELY update:**
- Internal refactors (implementation changes)
- Bug fixes that don't change behavior
- Code cleanup

### Stale Docs Are Worse Than No Docs

**Users trust documentation.**

Wrong documentation is worse than no documentation—it wastes time and builds mistrust.

**If you can't maintain docs:**
- Delete them (better than lying)
- Or clearly mark as outdated
- Or link to code as source of truth

### Documentation Debt

**When to defer documentation:**
- Experimental features (still exploring)
- Internal tools (team already knows)
- Prototypes (may be discarded)

**When documentation debt becomes unacceptable:**
- Feature shipping to users
- Onboarding new team members
- Open sourcing project

## Automated Documentation Quality

**Link Checking** (lychee - Rust binary):
```bash
lychee **/*.md --offline --cache
```
- Single binary, no Node.js
- ~40x faster than markdown-link-check
- Works offline completely
- Install: `brew install lychee`

**Style Linting** (Vale - Go binary):
```bash
vale docs/
```
- Enforces style guides (Google, Microsoft, write-good)
- Single binary, 100% offline
- YAML configuration (`.vale.ini`)
- Install: `brew install vale`

**Freshness Detection** (git-based):
```bash
# Find docs not updated in 90 days
find docs -name '*.md' | while read f; do
  age=$(( ($(date +%s) - $(git log -1 --format=%ct -- "$f")) / 86400 ))
  [ $age -gt 90 ] && echo "$f: $age days stale"
done
```

**CI Integration**: All run in GitHub Actions without external services

---

## Diagrams

### When to Use Diagrams

✅ **Use diagrams when they clarify:**
- System architecture (components, relationships)
- Data flow (how data moves through system)
- State machines (states and transitions)
- Complex interactions (sequence diagrams)

❌ **Don't use diagrams:**
- As decoration (diagrams should clarify, not prettify)
- For simple systems (often code is clearer)
- Without maintaining them (stale diagrams mislead)

### Diagram Principles

**Keep simple:**
- Complex diagrams become stale
- Focus on high-level relationships
- Details belong in code

**Text-based preferred:**
- Version control friendly
- Easy to update
- Tools: Any text-based diagram format your team prefers

**Maintain or delete:**
- Update diagrams with system changes
- Or delete outdated diagrams (don't let them lie)

---

## Quick Reference

### Documentation Checklist

**Before writing comment:**
- [ ] Can I make code clearer instead?
- [ ] Am I explaining "why" or just "what"?
- [ ] Would future me find this helpful?
- [ ] Is this non-obvious or a gotcha?

**Before shipping feature:**
- [ ] README updated (if user-facing)?
- [ ] Breaking changes documented?
- [ ] Examples still work?
- [ ] Quick start still accurate?

**Starting new project:**
- [ ] README with What, Why, Quick Start, Setup
- [ ] License (if sharing)
- [ ] .gitignore (keep docs, ignore build artifacts)

**When making architectural decision:**
- [ ] Should this be an ADR?
- [ ] Will team need context in 6 months?
- [ ] Is this a significant departure from current approach?

---

## Philosophy

**"Code tells you how. Comments tell you why."**

The best documentation is code that doesn't need documentation. But when code can't express intent, comments bridge the gap.

**Documentation is for humans:**
- Future you (6 months from now)
- Team members (new and experienced)
- Users (trying to use your code)

**Documentation is not:**
- A substitute for clear code
- A place to explain bad design
- Something to write and forget

**Remember:** Undocumented code is hard to use. Documented wrong code is harder.

---

## Exit Codes and Error Codes

**Documentation drift is silent.** When documenting exit codes, error codes, or error-to-behavior mappings:

1. **Trace actual code paths.** Don't document intent—document what the code actually does.
2. **Check all callers.** An error code might be defined but never used, or used differently than named.
3. **Grep for the constant.** `grep -rn "ExitCodeFoo" internal/` reveals actual usage.

**Verification rule:** After writing error/exit code docs, verify each code against its actual trigger in the codebase.
