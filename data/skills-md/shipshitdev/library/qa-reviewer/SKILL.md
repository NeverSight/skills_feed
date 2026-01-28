---
name: qa-reviewer
description: Systematically review AI agent work for quality, accuracy, and completeness. Catches bugs, verifies patterns, checks against requirements, and suggests improvements before committing changes.
version: 1.0.0
tags:
  - quality-assurance
  - verification
  - code-review
  - accuracy
  - completeness
---

# QA Reviewer: Systematic Work Verification

## Purpose

Structured framework for reviewing AI agent work before finalizing changes. Catches bugs, verifies accuracy, ensures completeness, validates solutions match requirements.

**Why this exists:** AI agents can introduce subtle bugs, miss requirements, or make incorrect assumptions.

## When to Use

- User says "check your work" or "review this"
- After completing complex multi-step implementations
- Before committing major refactors
- When modifying commands or skills
- After implementing new features
- Proactively after any task >5 steps

## QA Workflow Phases

### 1. Context Gathering

- Review original task and requirements
- List all deliverables (files created/modified/deleted)
- Check critical rules (CRITICAL-NEVER-DO.md)

### 2. Requirement Verification

- Create checklist of all requirements
- Verify solution alignment
- Check for edge cases

### 3. Accuracy Verification

- Verify file paths exist
- Confirm patterns match codebase
- Cross-reference citations

### 4. Bug Detection

- Check syntax (markdown, code, paths)
- Look for logic errors
- Verify project-specific rules

### 5. Completeness Audit

- Reconcile todo list
- Verify all mentioned files changed
- Check for side effects

### 6. Optimization Review

- Evaluate solution quality
- Check pattern consistency
- Consider alternatives

## Quick Verification Commands

```bash
# Verify file exists
ls -la <file-path>

# Check balanced code blocks
grep -c '\`\`\`' file.md

# Find violations
grep -r "console\.log" <files>
grep -r ": any" <files>
```

## Project Rules Check

- [ ] No console.log (use logger)
- [ ] No `any` types
- [ ] No inline interfaces
- [ ] AGENTS/CLAUDE/CODEX files intact
- [ ] .agent/ folders untouched
- [ ] Multi-tenancy preserved

## Final Assessment Categories

- **Approve** - Ready to commit
- **Conditional** - Fix issues first
- **Reject** - Significant problems

---

**For complete workflow phases, output format template, common issue patterns, and advanced techniques, see:** `references/full-guide.md`
