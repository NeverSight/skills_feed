---
name: openspec-proposal-creation
description: Creates structured change proposals with specification deltas for new features, breaking changes, or architecture updates. Use when planning features, creating proposals, speccing changes, introducing new capabilities, or starting development workflows. Triggers include "openspec proposal", "create proposal", "plan change", "spec feature", "new capability", "add feature planning", "design spec".
---

# Specification Proposal Creation

Creates comprehensive change proposals following spec-driven development methodology.

## Quick Start

Creating a spec proposal involves three main outputs:
1. **proposal.md** - Why, what, and impact summary
2. **tasks.md** - Numbered implementation checklist
3. **spec-delta.md** - Formal requirement changes (ADDED/MODIFIED/REMOVED)

**Basic workflow**: Generate change ID → scaffold directories → draft proposal → create spec deltas → validate structure

## Workflow

Copy this checklist and track progress:

```
Proposal Progress:
- [ ] Step 1: Review existing specifications
- [ ] Step 2: Generate unique change ID
- [ ] Step 3: Scaffold directory structure
- [ ] Step 4: Draft proposal.md (Why/What/Impact)
- [ ] Step 5: Create tasks.md implementation checklist
- [ ] Step 6: Write spec deltas with EARS format
- [ ] Step 7: Validate proposal structure
- [ ] Step 8: Present for user approval
```

### Step 1: Review existing specifications

Before creating a proposal, understand the current state:

```bash
# List all existing specs
find spec/specs -name "spec.md" -type f

# List active changes to avoid conflicts
find spec/changes -maxdepth 1 -type d -not -path "*/archive"

# Search for related requirements
grep -r "### Requirement:" spec/specs/
```

### Step 2: Generate unique change ID

Choose a descriptive, URL-safe identifier:

**Format**: `add-<feature>`, `fix-<issue>`, `update-<component>`, `remove-<feature>`

**Examples**:
- `add-user-authentication`
- `fix-payment-validation`
- `update-api-rate-limits`
- `remove-legacy-endpoints`

**Validation**: Check for conflicts:
```bash
ls spec/changes/ | grep -i "<proposed-id>"
```

### Step 3: Scaffold directory structure

Create the change folder with standard structure:

```bash
# Replace {change-id} with actual ID
mkdir -p spec/changes/{change-id}/specs/{capability-name}
```

**Example**:
```bash
mkdir -p spec/changes/add-user-auth/specs/authentication
```

### Step 4: Draft proposal.md

Use the template at [templates/proposal.md](templates/proposal.md) as starting point.

**Required sections**:
- **Why**: Problem or opportunity driving this change
- **What Changes**: Bullet list of modifications
- **Impact**: Affected specs, code, APIs, users

**Tone**: Clear, concise, decision-focused. Avoid unnecessary background.

### Step 5: Create tasks.md implementation checklist

Break implementation into concrete, testable tasks. Use the template at [templates/tasks.md](templates/tasks.md).

**Format**:
```markdown
# Implementation Tasks

1. [First concrete task]
2. [Second concrete task]
3. [Test task]
4. [Documentation task]
```

**Best practices**:
- Each task is independently completable
- Include testing and validation tasks
- Order by dependencies (database before API, etc.)
- 5-15 tasks is typical; split if more needed

### Step 6: Write spec deltas with EARS format

This is the most critical step. Spec deltas use **EARS format** (Easy Approach to Requirements Syntax).

**For complete EARS guidelines**, see [reference/EARS_FORMAT.md](reference/EARS_FORMAT.md)

**Delta operations**:
- `## ADDED Requirements` - New capabilities
- `## MODIFIED Requirements` - Changed behavior (include full updated text)
- `## REMOVED Requirements` - Deprecated features

**Basic requirement structure**:
```markdown
## ADDED Requirements

### Requirement: User Login
WHEN a user submits valid credentials,
the system SHALL authenticate the user and create a session.

#### Scenario: Successful Login
GIVEN a user with email "user@example.com" and password "correct123"
WHEN the user submits the login form
THEN the system creates an authenticated session
AND redirects to the dashboard
```

**For validation patterns**, see [reference/VALIDATION_PATTERNS.md](reference/VALIDATION_PATTERNS.md)

### Step 7: Validate proposal structure

Run these checks before presenting to user:

```markdown
Structure Checklist:
- [ ] Directory exists: `spec/changes/{change-id}/`
- [ ] proposal.md has Why/What/Impact sections
- [ ] tasks.md has numbered task list (5-15 items)
- [ ] Spec deltas have operation headers (ADDED/MODIFIED/REMOVED)
- [ ] Requirements follow `### Requirement: <name>` format
- [ ] Scenarios use `#### Scenario:` format (4 hashtags)
```

**Automated checks**:
```bash
# Count delta operations (should be > 0)
grep -c "## ADDED\|MODIFIED\|REMOVED" spec/changes/{change-id}/specs/**/*.md

# Verify scenario format (should show line numbers)
grep -n "#### Scenario:" spec/changes/{change-id}/specs/**/*.md

# Check requirement headers
grep -n "### Requirement:" spec/changes/{change-id}/specs/**/*.md
```

### Step 8: Present for user approval

Summarize the proposal clearly:

```markdown
## Proposal Summary

**Change ID**: {change-id}
**Scope**: {brief description}

**Files created**:
- spec/changes/{change-id}/proposal.md
- spec/changes/{change-id}/tasks.md
- spec/changes/{change-id}/specs/{capability}/spec-delta.md

**Next steps**:
Review the proposal. If approved, say "openspec implement" or "apply the change" to begin implementation.
```

## Advanced Topics

**EARS format details**: See [reference/EARS_FORMAT.md](reference/EARS_FORMAT.md)
**Validation patterns**: See [reference/VALIDATION_PATTERNS.md](reference/VALIDATION_PATTERNS.md)
**Complete examples**: See [reference/EXAMPLES.md](reference/EXAMPLES.md)

## Common Patterns

### Pattern 1: New feature proposal

When adding net-new capability:
- Use `ADDED Requirements` delta
- Include positive scenarios AND error handling
- Consider edge cases in scenarios

### Pattern 2: Breaking change proposal

When changing existing behavior:
- Use `MODIFIED Requirements` delta
- Include complete updated requirement text
- Document what changes and why in proposal.md
- Consider migration tasks in tasks.md

### Pattern 3: Deprecation proposal

When removing features:
- Use `REMOVED Requirements` delta
- Document removal rationale in proposal.md
- Include cleanup tasks in tasks.md
- Consider user migration in impact section

## Anti-Patterns to Avoid

**Don't**:
- Skip validation checks (always run grep patterns)
- Create proposals without reviewing existing specs first
- Use vague task descriptions ("Fix the thing")
- Write requirements without scenarios
- Forget error handling scenarios
- Mix multiple unrelated changes in one proposal

**Do**:
- Check for conflicts before creating change ID
- Write concrete, testable tasks
- Include positive AND negative scenarios
- Keep one concern per proposal
- Validate structure before presenting

## File Templates

All templates are in the `templates/` directory:
- [proposal.md](templates/proposal.md) - Proposal structure
- [tasks.md](templates/tasks.md) - Task checklist format
- [spec-delta.md](templates/spec-delta.md) - Spec delta template

## Reference Materials

- [EARS_FORMAT.md](reference/EARS_FORMAT.md) - Complete EARS syntax guide
- [VALIDATION_PATTERNS.md](reference/VALIDATION_PATTERNS.md) - Grep/bash validation
- [EXAMPLES.md](reference/EXAMPLES.md) - Real-world proposal examples

---

**Token budget**: This SKILL.md is approximately 450 lines, under the 500-line recommended limit. Reference files load only when needed for progressive disclosure.
