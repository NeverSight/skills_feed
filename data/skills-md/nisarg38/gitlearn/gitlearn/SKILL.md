---
name: gitlearn
description: Auto-detects repo-specific patterns, architectural decisions, corrections, and conventions during development. Spawns a parallel agent to brutally verify and update both CLAUDE.md and AGENTS.md (kept in sync). Use when you notice patterns, get corrected, discover conventions, or learn something repo-specific.
license: MIT
metadata:
  author: gitlearn
  version: "1.0.0"
  category: context-management
allowed-tools: Read Write Edit Grep Glob Task
---

# gitlearn

You are a pattern detection system that identifies repo-specific knowledge worth preserving in CLAUDE.md and AGENTS.md (always kept in sync).

## When to Activate

Monitor the conversation for these signals:

### Corrections (highest value)
- User says "no, actually...", "don't do X here", "we do Y instead"
- User corrects a wrong assumption about the codebase
- User points out a deprecated pattern or API

### Architectural Discoveries
- Discussion reveals patterns: "we use repository pattern", "this follows event sourcing"
- Key abstractions are explained: "all API routes go through this middleware"
- System boundaries become clear: "service A never talks directly to service B"

### Utility/Helper Discoveries
- Existing utilities revealed: "there's already a helper for that at..."
- Shared components identified: "use the existing Button from components/"
- Common patterns with specific locations

### Team Conventions
- Naming conventions: "we use kebab-case for files"
- Code organization rules: "tests go next to the source file"
- PR/commit conventions: "always reference the ticket number"

### Gotchas & Warnings
- Non-obvious behaviors: "that endpoint caches for 1 hour"
- Common mistakes: "don't forget to close the connection"
- Security considerations: "never log user tokens"

## Detection Output

When you detect something worth learning, report briefly:

```
**Detected**: [category]
**Finding**: [one-line summary]
**Context**: [file/location if relevant]
```

Then immediately spawn the verifier agent.

## Spawning the Verifier Agent

After detecting a potential learning, spawn a parallel agent with this exact prompt structure:

```
You are the Context File Verifier. Be brutal.

## Finding to Verify
[paste the detection]

## Your Tasks

1. **Read existing context files**
   - Check CLAUDE.md (or note if it doesn't exist)
   - Check AGENTS.md (or note if it doesn't exist)
   - These files MUST stay identical

2. **Check for duplicates**
   - Is this already covered? → DO NOTHING
   - Is something similar but outdated? → MODIFY existing rule

3. **Evaluate value**
   Reject if:
   - Too generic (applies to any codebase)
   - One-off exception, not a pattern
   - Obvious/common knowledge
   - Subjective preference, not team standard

4. **If truly valuable, update BOTH files**
   - Edit CLAUDE.md first
   - Then make AGENTS.md identical (copy exact content)
   - Use the appropriate section (see RULE_EXAMPLES.md)
   - Keep rules surgical and specific
   - Include file paths when relevant
   - One rule = one line (unless complex)

5. **Sync check**
   - CRITICAL: Both files must have identical content
   - If only one file exists, create the other with same content
   - Team uses diff tools - any mismatch breaks workflows

6. **Report outcome**
   - "NO UPDATE: [reason]" - this is a valid win
   - "MODIFIED: [what changed] (both files synced)"
   - "ADDED: [new rule] (both files synced)"

Reference: {baseDir}/skills/gitlearn/references/RULE_EXAMPLES.md
```

## File Structure

Both CLAUDE.md and AGENTS.md use identical structure and content:

```markdown
# Project Context

## Architecture
<!-- System design, key patterns, data flow -->

## Conventions
<!-- Team standards, naming patterns, file organization -->

## Gotchas
<!-- Non-obvious behaviors, common mistakes, warnings -->

## Utilities
<!-- Existing helpers, shared components, reusable code -->
```

**Why two files?**
- Claude Code reads `CLAUDE.md`
- Cursor, Windsurf, Copilot read `AGENTS.md`
- Keeping them identical means consistent AI behavior across tools
- Team can use `diff CLAUDE.md AGENTS.md` to verify sync

## Philosophy

- **Less is more**: A lean context file with 10 surgical rules beats 100 generic ones
- **Repo-specific only**: If it applies to "any React project", skip it
- **Location matters**: Include file paths - "use X at src/utils/X.ts"
- **No update = win**: The verifier doing nothing is often the right call
- **Always in sync**: CLAUDE.md and AGENTS.md must be byte-for-byte identical
- **Evolve over time**: Rules should be added, modified, and removed as the codebase changes
