---
name: openspec-archiving
description: Archives completed changes and merges specification deltas into living documentation. Use when changes are deployed, ready to archive, or specs need updating after implementation. Triggers include "openspec archive", "archive change", "merge specs", "complete proposal", "update documentation", "finalize spec", "mark as done".
---

# Specification Archiving

Archives completed change proposals and merges their spec deltas into the living specification documentation.

## Quick Start

Archiving involves two main operations:
1. **Move change folder** to archive with timestamp
2. **Merge spec deltas** into living specs (ADDED/MODIFIED/REMOVED operations)

**Critical rule**: Verify all tasks are complete before archiving. Archiving signifies deployment and completion.

## Workflow

Copy this checklist and track progress:

```
Archive Progress:
- [ ] Step 1: Verify implementation is complete
- [ ] Step 2: Review spec deltas to merge
- [ ] Step 3: Create timestamped archive directory
- [ ] Step 4: Merge ADDED requirements into living specs
- [ ] Step 5: Merge MODIFIED requirements into living specs
- [ ] Step 6: Merge REMOVED requirements into living specs
- [ ] Step 7: Move change folder to archive
- [ ] Step 8: Validate living spec structure
```

### Step 1: Verify implementation is complete

Before archiving, confirm all work is done:

```bash
# Check for IMPLEMENTED marker
test -f spec/changes/{change-id}/IMPLEMENTED && echo "✓ Implemented" || echo "✗ Not implemented"

# Review tasks
cat spec/changes/{change-id}/tasks.md

# Check git status for uncommitted work
git status
```

**Ask the user**:
```markdown
Are all tasks complete and tested?
Has this change been deployed to production?
Should I proceed with archiving?
```

### Step 2: Review spec deltas to merge

Understand what will be merged:

```bash
# List all spec delta files
find spec/changes/{change-id}/specs -name "*.md" -type f

# Read each delta
for file in spec/changes/{change-id}/specs/**/*.md; do
    echo "=== $file ==="
    cat "$file"
done
```

**Identify**:
- Which capabilities are affected
- How many requirements are ADDED/MODIFIED/REMOVED
- Where in living specs these changes belong

### Step 3: Create timestamped archive directory

```bash
# Create archive with today's date
TIMESTAMP=$(date +%Y-%m-%d)
mkdir -p spec/archive/${TIMESTAMP}-{change-id}
```

**Example**:
```bash
# For change "add-user-auth" archived on Oct 26, 2025
mkdir -p spec/archive/2025-10-26-add-user-auth
```

### Step 4: Merge ADDED requirements into living specs

For each `## ADDED Requirements` section:

**Process**:
1. Locate the target living spec file
2. Append the new requirements to the end of the file
3. Maintain proper markdown formatting

**Example**:

**Source** (`spec/changes/add-user-auth/specs/authentication/spec-delta.md`):
```markdown
## ADDED Requirements

### Requirement: User Login
WHEN a user submits valid credentials,
the system SHALL authenticate the user and create a session.

#### Scenario: Successful Login
GIVEN valid credentials
WHEN user submits login form
THEN system creates session
```

**Target** (`spec/specs/authentication/spec.md`):
```bash
# Append to living spec
cat >> spec/specs/authentication/spec.md << 'EOF'

### Requirement: User Login
WHEN a user submits valid credentials,
the system SHALL authenticate the user and create a session.

#### Scenario: Successful Login
GIVEN valid credentials
WHEN user submits login form
THEN system creates session
EOF
```

### Step 5: Merge MODIFIED requirements into living specs

For each `## MODIFIED Requirements` section:

**Process**:
1. Locate the existing requirement in the living spec
2. Replace the ENTIRE requirement block (including all scenarios)
3. Use the complete updated text from the delta

**Example using sed**:

```bash
# Find and replace requirement block
# This is conceptual - actual implementation depends on structure

# First, identify the line range of the old requirement
START_LINE=$(grep -n "### Requirement: User Login" spec/specs/authentication/spec.md | cut -d: -f1)

# Find the end (next requirement or end of file)
END_LINE=$(tail -n +$((START_LINE + 1)) spec/specs/authentication/spec.md | \
           grep -n "^### Requirement:" | head -1 | cut -d: -f1)

# Delete old requirement
sed -i "${START_LINE},${END_LINE}d" spec/specs/authentication/spec.md

# Insert new requirement at same position
# (Extract from delta and insert)
```

**Manual approach** (recommended for safety):
```markdown
1. Open living spec in editor
2. Find the requirement by name
3. Delete entire block (requirement + all scenarios)
4. Paste updated requirement from delta
5. Save
```

### Step 6: Merge REMOVED requirements into living specs

For each `## REMOVED Requirements` section:

**Process**:
1. Locate the requirement in the living spec
2. Delete the entire requirement block
3. Add a comment documenting the removal

**Example**:

```bash
# Option 1: Delete with comment
# Manually edit spec/specs/authentication/spec.md

# Add deprecation comment
echo "<!-- Requirement 'Legacy Password Reset' removed $(date +%Y-%m-%d) -->" >> spec/specs/authentication/spec.md

# Delete the requirement block manually or with sed
```

**Pattern**:
```markdown
<!-- Removed 2025-10-26: User must use email-based password reset -->
~~### Requirement: SMS Password Reset~~
```

### Step 7: Move change folder to archive

After all deltas are merged:

```bash
# Move entire change folder to archive
mv spec/changes/{change-id} spec/archive/${TIMESTAMP}-{change-id}
```

**Verify move succeeded**:
```bash
# Check archive exists
ls -la spec/archive/${TIMESTAMP}-{change-id}

# Check changes directory is clean
ls spec/changes/ | grep "{change-id}"  # Should return nothing
```

### Step 8: Validate living spec structure

After merging, validate the living specs are well-formed:

```bash
# Check requirement format
grep -n "### Requirement:" spec/specs/**/*.md

# Check scenario format
grep -n "#### Scenario:" spec/specs/**/*.md

# Count requirements per spec
for spec in spec/specs/**/spec.md; do
    count=$(grep -c "### Requirement:" "$spec")
    echo "$spec: $count requirements"
done
```

**Manual review**:
- Open each modified spec file
- Verify markdown formatting is correct
- Check requirements flow logically
- Ensure no duplicate requirements exist

## Merge Logic Reference

### ADDED Operation

```
Action: Append to living spec
Location: End of file (before any footer/appendix)
Format: Copy requirement + all scenarios exactly as written
```

### MODIFIED Operation

```
Action: Replace existing requirement
Location: Find by requirement name, replace entire block
Format: Use complete updated text from delta (don't merge, replace)
Note: Old version is preserved in archive
```

### REMOVED Operation

```
Action: Delete requirement, add deprecation comment
Location: Find by requirement name
Format: Delete entire block, optionally add <!-- Removed YYYY-MM-DD: reason -->
```

### RENAMED Operation (uncommon)

```
Action: Update requirement name, keep content
Location: Find by old name, update to new name
Format: Just change the header: ### Requirement: NewName
Note: Typically use MODIFIED instead
```

## Best Practices

### Pattern 1: Verify Before Moving

**Always** verify delta merges before moving to archive:

```bash
# After merging, check diff
git diff spec/specs/

# Review changes
git diff spec/specs/authentication/spec.md

# If correct, commit
git add spec/specs/
git commit -m "Merge spec deltas from add-user-auth"

# Then archive
mv spec/changes/add-user-auth spec/archive/2025-10-26-add-user-auth
```

### Pattern 2: Atomic Archiving

Archive entire changes, not individual files:

**Good**:
```bash
# Move complete change folder
mv spec/changes/add-user-auth spec/archive/2025-10-26-add-user-auth
```

**Bad**:
```bash
# Don't cherry-pick files
mv spec/changes/add-user-auth/proposal.md spec/archive/
# (leaves orphaned files)
```

### Pattern 3: Archive Preservation

The archive is a historical record. Never modify archived files:

```markdown
❌ Don't: Edit files in spec/archive/
✓ Do: Treat archive as read-only history
```

### Pattern 4: Git Commit Strategy

Recommended commit workflow:

```bash
# Commit 1: Merge deltas
git add spec/specs/
git commit -m "Merge spec deltas from add-user-auth

- Added User Login requirement
- Modified Password Policy requirement
- Removed Legacy Auth requirement"

# Commit 2: Archive change
git add spec/archive/ spec/changes/
git commit -m "Archive add-user-auth change"
```

## Advanced Topics

**For complex deltas**: See [reference/MERGE_LOGIC.md](reference/MERGE_LOGIC.md)

**Conflict resolution**: If multiple changes modified the same requirement, manual merge is required.

**Rollback strategy**: To rollback an archive, reverse the process (move from archive back to changes, remove merged content from living specs).

## Common Patterns

### Pattern 1: Simple Addition

```markdown
Change adds 1 new requirement → Append to spec → Archive
```

### Pattern 2: Behavioral Change

```markdown
Change modifies 1 requirement → Replace in spec → Archive
```

### Pattern 3: Deprecation

```markdown
Change removes 1 requirement → Delete from spec with comment → Archive
```

### Pattern 4: Feature with Multiple Requirements

```markdown
Change adds 5 requirements across 2 specs
→ Append each to respective spec
→ Verify all are merged
→ Archive
```

## Anti-Patterns to Avoid

**Don't**:
- Archive incomplete implementations
- Merge deltas before deployment
- Modify archived files
- Skip validation after merging
- Forget to git commit merged specs

**Do**:
- Verify all tasks complete before archiving
- Merge deltas carefully and completely
- Treat archive as immutable history
- Validate merged specs structure
- Commit merged specs before archiving move

## Troubleshooting

### Issue: Merge conflict (requirement exists in living spec)

**Solution**:
```markdown
1. If names match but content differs → Use MODIFIED pattern
2. If truly different requirements → Rename one
3. If duplicate by mistake → Use whichever is correct
```

### Issue: Can't find requirement to modify/remove

**Solution**:
```markdown
1. Search by partial name: grep -i "login" spec/specs/**/*.md
2. Check if already removed
3. Check if in different capability file
```

### Issue: Living spec has formatting errors after merge

**Solution**:
```markdown
1. Fix formatting manually
2. Re-run validation: grep -n "###" spec/specs/**/*.md
3. Ensure consistent heading levels
```

## Reference Materials

- [MERGE_LOGIC.md](reference/MERGE_LOGIC.md) - Detailed merge operation rules

---

**Token budget**: This SKILL.md is approximately 480 lines, under the 500-line recommended limit.
