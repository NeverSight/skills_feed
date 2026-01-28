---
name: decision-log
description: "MANDATORY pre-commit workflow for vibe coding. ALWAYS trigger when user says 'commit', 'git commit', or any commit-related command. Forces diff review and decision log generation BEFORE allowing commit to proceed."
---

# Decision Log - Pre-Commit Workflow

## CRITICAL: ALWAYS Execute This Workflow Before Any Commit

This skill is **mandatory** when user mentions commit. Do NOT skip to git commit directly.

## Workflow (Execute in Order)

### Step 1: STOP - Do Not Commit Yet

When user says "commit" or "git commit":

- **DO NOT** execute `git commit` immediately
- User wants a commit, but you must generate decision log FIRST

### Step 2: Review What's Being Committed

Run these commands in sequence:

```bash
# See what files are staged
git diff --cached --name-only

# See the actual changes
git diff --cached
```

Show the user:

- Which files changed
- Key changes (summarize if diff is >50 lines)

### Step 3: Generate Decision Log

Based on the diff, create a 3-line decision log:

```
[YYYY-MM-DD HH:MM] <one-line summary>
- Why: <core reason for this change>
- Risk: <known issues/shortcuts or "none">
```

**Rules:**

- Summary: Extract from user's recent messages or infer from code changes
- Why: The business/technical reason (not "user asked")
- Risk: Be honest about shortcuts, missing tests, or edge cases

**Example:**

```
[2026-01-28 14:30] Sync pairing settings types across test env
- Why: Test suite needed updated Setting type to match production
- Risk: May break other tests expecting old type structure
```

### Step 4: Show Proposed Commit

Present to user:

```
I'll commit these changes:

Files:
- src/types/setting.ts
- src/test/setup.ts
(+ 3 more files)

With message:
---
fix: sync pairing settings types and test env

[Decision Log]
[2026-01-28 14:30] Sync pairing settings types across test env
- Why: Test suite needed updated Setting type to match production
- Risk: May break other tests expecting old type structure
---

Proceed with commit? [y/n]
```

### Step 5: APPEND Decision Log to File (DO NOT OVERWRITE)

**CRITICAL: This step must APPEND, not overwrite existing content**

Execute these commands in this exact order:

```bash
# 1. Create directory if needed
mkdir -p .decisions

# 2. Get today's date
TODAY=$(date +%Y-%m-%d)

# 3. APPEND to file (NEVER overwrite)
# Use >> for append, NOT > which overwrites
cat >> .decisions/$TODAY.md << 'EOF'
[18:00] Make build workflow package-only
- Why: Build pipeline should only produce artifacts without tagging or releasing
- Risk: none

EOF
```

**VERIFICATION REQUIRED:**

After appending, verify the file still contains old entries:

```bash
# Show the file to confirm old entries are preserved
cat .decisions/$TODAY.md
```

**Expected output:**

```
[15:05] Add pairing orchestration tracing...
[15:51] Improve pairing usecase...
[16:28] Remove direct deps...
[18:00] Make build workflow package-only  ← New entry appended
```

**If old entries are missing → ABORT and show error**

### Step 6: Stage the Decision Log File

```bash
# Stage the entire .decisions/ directory
git add .decisions/
```

**Why this matters:**

- The decision log file must be included in the same commit
- Without staging, it won't be part of the commit

### Step 7: Execute Commit

**Only after user confirms AND verification passes**, run:

```bash
git commit -m "fix: make build workflow package-only

[Decision Log]
[2026-01-28 18:00] Make build workflow package-only
- Why: Build pipeline should only produce artifacts without tagging or releasing
- Risk: none"
```

**Result:**

- Commit includes both code changes AND the `.decisions/YYYY-MM-DD.md` file
- Old decision log entries are preserved in the file
- No second commit needed

## Anti-Patterns (NEVER DO THESE)

❌ **Using `>` instead of `>>`:** This OVERWRITES the file

```bash
cat > .decisions/2026-01-28.md  # ❌ WRONG - deletes old content
```

✅ **Correct: Use `>>`** This APPENDS to the file

```bash
cat >> .decisions/2026-01-28.md  # ✅ CORRECT - preserves old content
```

❌ **Not verifying after append:** Always check that old entries still exist

❌ **Recreating the file:** Don't do `rm .decisions/$TODAY.md && echo ...`

## Complete Example Workflow

```
User: "commit"

Claude:
[Step 1] Reviewing staged changes...

[Step 2]
Files to commit:
- src/workflows/build.yml (modified)

Key changes:
- Removed release steps from build workflow

[Step 3 & 4]
I'll commit with this message:
---
fix: make build workflow package-only

[Decision Log]
[2026-01-28 18:00] Make build workflow package-only
- Why: Build pipeline should only produce artifacts without tagging
- Risk: none
---

Proceed? (y/n)

User: "y"

Claude:
[Step 5] Appending decision log...
$ mkdir -p .decisions
$ cat >> .decisions/2026-01-28.md << 'EOF'
[18:00] Make build workflow package-only
- Why: Build pipeline should only produce artifacts without tagging
- Risk: none

EOF

[Verification] Checking file contents...
$ cat .decisions/2026-01-28.md

File contents:
[15:05] Add pairing orchestration tracing...
[15:51] Improve pairing usecase...
[16:28] Remove direct deps...
[18:00] Make build workflow package-only  ✓ Appended correctly

[Step 6] Staging decision log...
$ git add .decisions/

[Step 7] Committing...
$ git commit -m "fix: make build workflow package-only

[Decision Log]
[2026-01-28 18:00] Make build workflow package-only
- Why: Build pipeline should only produce artifacts without tagging
- Risk: none"

✓ Committed: abc1234
✓ Decision log appended (preserving 3 previous entries)
```

## Troubleshooting

### Problem: Old entries disappeared

**Symptoms:**

```bash
$ cat .decisions/2026-01-28.md
[18:00] Make build workflow package-only  # ← Only new entry, old ones gone
```

**Cause:** Used `>` instead of `>>`, or recreated the file

**Fix:**

1. Check git history: `git show HEAD^:.decisions/2026-01-28.md`
2. Restore old entries from previous commit
3. Append new entry correctly with `>>`

### Problem: File not included in commit

**Symptoms:**

```bash
$ git show --name-only HEAD | grep .decisions
# (nothing)
```

**Cause:** Forgot to run `git add .decisions/` before commit

**Fix:**

1. Amend the commit: `git add .decisions/ && git commit --amend --no-edit`

## Integration Notes

**For repositories with existing .decisions/ files:**

- The skill will automatically append to existing files
- Old entries are preserved
- Multiple commits per day all go into the same dated file

**File structure over time:**

```
.decisions/
├── 2026-01-27.md  (5 entries)
├── 2026-01-28.md  (8 entries ← growing throughout the day)
└── 2026-01-29.md  (2 entries so far)
```

## Resources

This skill includes a helper script that correctly handles append operations.
