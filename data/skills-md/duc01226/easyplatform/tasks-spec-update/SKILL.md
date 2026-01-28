---
name: tasks-spec-update
version: 1.0.0
description: Use when updating specifications, comparing branches, or ensuring documentation reflects current implementation.
infer: false
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task
---

# Specification Update Workflow

## When to Use This Skill

- Syncing specs with implementation
- Branch comparison analysis
- Post-implementation documentation update
- Feature spec verification

## Pre-Flight Checklist

- [ ] Identify specification files to update
- [ ] Determine implementation changes
- [ ] Compare current state vs documented state
- [ ] Plan update strategy

## Phase 1: Change Discovery

### Git-Based Discovery

```bash
# Compare branches
git diff main..feature-branch --name-only

# Get detailed diff
git diff main..feature-branch

# List commits with messages
git log main..feature-branch --oneline
```

### Pattern-Based Discovery

```bash
# Find all spec files
find . -name "*.spec.md" -o -name "*-specification.md"

# Cross-reference specs with code
grep -r "SaveEmployee" --include="*.md"  # In specs
grep -r "SaveEmployee" --include="*.cs"  # In code
```

## Phase 2: Gap Analysis

### Create Analysis Document

```markdown
# Specification Gap Analysis

## Implementation Status

| Component                | Specified | Implemented | Gap                    |
| ------------------------ | --------- | ----------- | ---------------------- |
| Entity: Employee         | Yes       | Yes         | None                   |
| Command: SaveEmployee    | Yes       | Yes         | Missing validation doc |
| Event: OnEmployeeCreated | No        | Yes         | Not in spec            |

## New Implementations (Not in Spec)
1. `BulkUpdateEmployeeCommand` - Added in PR #123

## Spec Items Not Implemented
1. `EmployeeArchiveCommand` - Deferred to Phase 2
```

## Phase 3: Specification Update

### Update Checklist

- [ ] Update entity property list
- [ ] Add new commands/queries
- [ ] Update validation rules
- [ ] Document side effects
- [ ] Add error codes
- [ ] Document new filters
- [ ] Update response schema
- [ ] List event handlers
- [ ] Describe cross-service effects
- [ ] Add new API endpoints
- [ ] Document auth requirements

## Phase 4: Verification

### Cross-Reference Check

```bash
# Verify all commands are documented
grep -r "class.*Command" --include="*.cs" -l
# Cross-check against specs
grep -r "Command" docs/specifications/*.md
```

## Verification Checklist

- [ ] All implementation changes identified
- [ ] Gap analysis completed
- [ ] Specifications updated
- [ ] Cross-references verified
- [ ] Version numbers updated
- [ ] Change log updated

## Related

- `tasks-documentation`
- `documentation`

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**
- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
