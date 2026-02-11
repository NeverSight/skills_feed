---
name: issue-fixer
description: This skill provides a systematic approach for investigating and fixing bugs and issues in the codebase. Use this skill when users report bugs, unexpected behavior, test failures, or request fixes for specific issues. The skill guides through issue registration, root cause analysis, impact assessment, minimal code changes, quality validation, and E2E testing.
metadata:
  author: cyberelf
  version: "1.0"
---

# Issue Fixer

## Overview

This skill provides a comprehensive, systematic workflow for investigating and fixing issues with minimal impact. It ensures proper issue tracking, thorough root cause analysis, impact assessment, quality validation, and automated testing for all fixes.

## When to Use This Skill

Invoke this skill when:
- User reports a bug or unexpected behavior
- Tests are failing and need investigation
- Features are broken or not working as expected
- User explicitly requests a fix for a specific issue
- Error messages or exceptions need resolution

## Core Workflow

The issue-fixing process follows seven sequential phases:

1. **Issue Registration** - Track the issue in `.issues/opening.md`
2. **Investigation** - Find all related code and identify root cause
3. **Impact Assessment** - Determine if it requires a simple fix or feature plan
4. **Implementation** - Apply minimal, surgical changes
5. **Validation** - Run quality checks and tests
6. **E2E Testing** - Create/update end-to-end tests for full-stack fixes
7. **Finalization** - Update issue status and generate summary

## Quick Start Decision Tree

```
User reports issue
    │
    ├─→ Is issue already tracked in .issues/opening.md?
    │   ├─→ Yes: Note issue number, proceed to Investigation
    │   └─→ No: Register new issue, proceed to Investigation
    │
    └─→ After investigation, what is the impact?
        ├─→ HIGH (6+ files, 200+ LOC, architecture changes, breaking changes)
        │   └─→ Create feature plan, suggest handoff to speckit.plan, STOP
        │
        └─→ LOW/MEDIUM (1-5 files, <200 LOC, no breaking changes)
            └─→ Proceed with implementation → validation → testing → finalization
```

## Detailed Workflow

For the complete step-by-step guide covering all seven phases, refer to:

**`references/workflow.md`** - Comprehensive workflow with detailed instructions for each phase including:
- Issue registration format and procedures
- Code discovery and root cause analysis techniques
- Impact assessment criteria and decision points
- Implementation principles and patterns
- Quality validation commands for backend and frontend
- E2E testing guidelines and patterns
- Issue finalization procedures

Load this reference when beginning an issue fix to understand the complete process.

## Critical Principles

Always follow these principles when fixing issues:

1. **Minimal Changes** - Modify only what's necessary to fix the issue
2. **No Unrelated Changes** - Don't fix other issues or refactor unrelated code
3. **Preserve Working Code** - Don't delete functioning code
4. **Follow Existing Patterns** - Match the project's architecture and style
5. **Type Safety** - Maintain or improve type annotations
6. **Proper Error Handling** - Add error handling if missing
7. **Test Incrementally** - Run checks after each file modification
8. **Document Decisions** - Add comments explaining non-obvious fixes

## Project Standards

Always review and follow project-specific standards before making changes:

- **Backend**: `.github/instructions/backend.instructions.md`
- **Frontend**: `.github/instructions/frontend.instructions.md`
- **Python**: `.github/instructions/python_standard.instructions.md`
- **TypeScript**: `.github/instructions/ts_standard.instructions.md`

## Quality Checks

### Backend (Python)
```bash
# Type checking (must pass with 0 errors)
python -m pyright app/

# Formatting
ruff format app/

# Linting
ruff check app/ --fix

# Tests
pytest tests/ -v
```

### Frontend (TypeScript)
```bash
# Build (includes type check and lint)
cd frontend && npm run build

# Tests (if available)
npm test
```

## Resources

### references/workflow.md
Complete step-by-step guide for all seven phases of issue fixing, including:
- Detailed instructions for each phase
- Code discovery and analysis techniques
- Impact assessment criteria
- Implementation patterns
- E2E testing guidelines
- Example code snippets and templates
