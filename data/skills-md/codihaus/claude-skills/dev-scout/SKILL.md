---
name: dev-scout
description: Discover and document how the codebase works - patterns, rules, and team conventions
version: 3.0.0
---

# /dev-scout - Codebase Pattern Discovery

> **Skill Awareness**: See `skills/_registry.md` for all available skills.
> - **Before**: Use `/debrief` if requirements unclear
> - **After**: Use `/dev-specs` for implementation plans
> - **Utils**: `/utils/diagram` for architecture visualization

Discover and document **how the codebase works** - patterns, rules, and team conventions for EXISTING code.

## When to Use

- Understand **how the project works** before implementation
- Document **team patterns and conventions** for new engineers
- Discover **architectural patterns** that must be followed
- Capture **existing features** and how they're implemented

## What Scout Does vs Doesn't

**Scout documents EXISTING code:**
- ✅ How the project currently works (patterns, conventions)
- ✅ Complete list of existing features
- ✅ How each feature is implemented (for understanding/extending)

**Scout does NOT plan NEW features:**
- ❌ NOT for creating implementation specs
- ❌ NOT for planning new features
- ❌ Use `/dev-specs` for new feature planning

**Not for:** Listing files, counting components, inventorying routes (use Glob/Grep fresh instead)

## Usage

```
/dev-scout                      # Project-level, medium mode
/dev-scout deep                 # Project-level, deep mode
/dev-scout auth                 # Feature-level
/dev-scout deep billing         # Feature-level, deep mode
```

## Core Rule: Capture Patterns, Not Inventory

**Capture (Stable):**
- Patterns & abstractions (e.g., `apiRequest()` wrapper)
- Architecture decisions (e.g., Server Actions)
- Code conventions (e.g., naming, structure)
- Tech choices (e.g., Zod, Prisma)
- Team process (e.g., git workflow)

**Don't Capture (Volatile):**
- File trees → use Glob fresh
- Component/route lists → discover when needed
- File counts → meaningless
- Exhaustive inventories → stale immediately

## Output

### Project-Level
**Location:** `plans/brd/tech-context.md` (~150-200 lines)
**History:** `plans/brd/history/tech-context-{date}.md`

**Answers:**
- How do we make API calls?
- How do we access data?
- How do we structure code?
- How does our team work?

### Feature-Level
**Location:** `plans/features/{feature}/codebase-context.md`

**Prerequisite:** MUST have `tech-context.md` first (patterns already documented)

**Answers:**
- How does THIS feature work? (not patterns - those are in tech-context.md)
- Where are the key files for this feature?
- How to extend this feature?
- What to watch out for?

**Does NOT repeat:**
- Project-wide patterns (already in tech-context.md)
- Tech stack info (already documented)
- Code conventions (already documented)

## Expected Outcome

### Project-Level: `tech-context.md` (~150-200 lines)

Answers: **How does this project work?**

**For new developers, provide:**
- **Patterns** - How we make API calls, access data, structure code (with file/location references)
- **Conventions** - Team standards for naming, formatting, git workflow
- **Stack** - Tech choices and why
- **All existing features** - Complete list (important: don't miss any!)

**Format:** Overview + location reference, NOT do/don't lists

**Example:**
```markdown
### API Communication
**Pattern:** All API calls go through `lib/api/client.ts` wrapper
**Location:** See `lib/api/client.ts` for implementation
**Usage:** Import `apiClient` and call methods
```

NOT:
```markdown
✅ DO: Use apiClient
❌ DON'T: Use fetch directly
```

### Feature-Level: `codebase-context.md`

Answers: **How does THIS already-implemented feature work?**

**Purpose:** Document existing implementation for understanding/extending, NOT create specs

**Prerequisite:** MUST have `tech-context.md` first

**Captures:**
- How this feature uses the patterns (reference tech-context.md)
- Where key files are (locations, entry points)
- How it currently works (flow, architecture)
- How to extend it (what to modify where)

**Does NOT:**
- Create implementation specs (this is for EXISTING code)
- Repeat patterns (reference tech-context.md instead)
- Include do/don't lists (show pattern usage with locations)

## Success Criteria

- New engineer can follow patterns from output
- Patterns shown with examples, not theory
- Rules captured, not procedures
- No file inventories or counts
- Feature scout reuses patterns from tech-context.md
- ~150-200 lines for tech-context.md

## Discovery Approach

### Project-Level

**Medium Mode (default):**
- Read project docs (CLAUDE.md, README, configs)
- Detect tech stack from package.json, configs
- Sample 2-3 files per category to discover patterns
- Extract conventions from configs
- **Discover ALL existing features** (don't miss any - scan routes, pages, API endpoints)

**Deep Mode:**
- All of Medium +
- Deeper pattern analysis (API, data access)
- Code convention detection
- Git & team process

**Output:** `tech-context.md` with patterns + complete feature list

### Feature-Level

**Purpose:** Document existing implementation for understanding/extending

**NOT FOR:** Creating specs or planning new features

**Lightweight approach:**

1. **Check prerequisite:** tech-context.md exists? If not, run project-level first
2. **Read patterns:** Load tech-context.md (now you know API pattern, data access, conventions)
3. **Focus on feature:** Find files (Glob/Grep), read 2-3 key files, identify entry points
4. **Document existing code:** How it works NOW, where files are, how to extend

**Output:** `codebase-context.md` describing current implementation

## Pattern Discovery Rules

1. **Sample, don't exhaust** - Read 2-3 representative files, not all
2. **Find abstractions** - Wrappers, base classes, shared utilities
3. **Capture with example** - Show the pattern in action
4. **Ask "what's the rule?"** - Not "what files exist?"

## Strategy by Codebase Size

| Size | Strategy |
|------|----------|
| Small (<100 files) | Sequential discovery |
| Medium (100-500) | Parallel by concern (API, data, UI, conventions) |
| Large (500+) | Use `/utils/gemini` first, then focused Claude analysis |

## Version Management

**When tech-context.md exists:**
- Move current to `history/tech-context-{date}.md`
- Note what changed (pattern changes, not file changes)

**When feature scout requested:**
- Check tech-context.md exists first
- If not, run project-level scout first

## Output Template

See `references/output-template.md` for structure.

## Tools

| Tool | Purpose |
|------|---------|
| `Read` | Docs, configs, sample files |
| `Glob` | Find patterns (wrappers, configs) |
| `Grep` | Search code patterns |
| `Bash` | Git history for conventions |
| `Task` | Parallel pattern discovery |
| `Context7` | Library patterns |

## Large Codebase Strategy

For 500+ files, use `/utils/gemini`:
1. Gemini scans full codebase (1M context)
2. Claude reads Gemini output
3. Claude deep dives on key patterns identified
4. Creates pattern-focused scout

## Anti-Patterns

**General:**
❌ Listing every file in a directory
❌ Counting components/routes
❌ Including full file trees
❌ Documenting file locations (use Glob instead)
❌ Reading every file (sample instead)

**Feature Scout Specific:**
❌ Rediscovering project patterns (already in tech-context.md)
❌ Repeating API/data/validation patterns (reference, don't rewrite)
❌ Re-documenting tech stack (already known)
❌ Running full project analysis (lightweight, feature-focused only)

## Reference

See `references/output-template.md` for output structure (principle + empty template).
