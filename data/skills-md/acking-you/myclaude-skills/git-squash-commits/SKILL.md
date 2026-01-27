---
name: git-squash-commits
description: Squash multiple git commits into a single commit with an auto-generated comprehensive commit message based on the changes made.
---

# Git Squash Commits Skill

## Overview

This skill helps you squash a range of git commits into a single commit with an automatically generated commit message that summarizes all the changes. It analyzes the commit history and file changes to create a comprehensive, well-structured commit message.

## When to Use

- Cleaning up messy commit history before merging
- Consolidating multiple work-in-progress commits
- Preparing commits for code review or pull request
- Simplifying feature branch history
- Removing unnecessary intermediate commits

## Prerequisites

**IMPORTANT**: Before invoking this skill, you MUST manually reset your branch to the parent of the earliest commit you want to squash. The skill will verify this and prompt you if needed.

Example:
```bash
# If you want to squash commits from abc123 to xyz789
# First find the parent of abc123
git log --oneline abc123~5..abc123

# Then reset to the parent (e.g., parent_commit)
git reset --hard parent_commit
```

## Usage

When invoking this skill, provide:
1. **Start commit ID**: The earliest commit in the range (will NOT be included in current branch after squash)
2. **End commit ID**: The latest commit in the range (will NOT be included in current branch after squash)

The skill will:
1. Verify the current HEAD is at the parent of the start commit
2. Analyze all commits between start and end (inclusive)
3. Examine the file changes and commit messages
4. Generate a comprehensive commit message with:
   - High-level summary
   - Major changes grouped by category
   - Detailed improvements and fixes
   - Statistics (files changed, lines added/removed)
5. Prompt user to run build/compilation to verify changes
   - Wait for user confirmation
   - If build fails, help resolve errors
   - If build succeeds, proceed to next step
6. Create the squash commit
7. Verify the old commits are no longer in the branch history
8. Save a summary record to `ai_docs/git-squash-commits/` directory containing:
   - Squash operation metadata (timestamp, branch, commit hashes)
   - The generated commit message
   - Statistics and list of original commits

## Commit Message Structure

The generated commit message follows this structure:

```
<Type>: <Brief summary of the main changes>

Major changes:
- <Category 1>: <Description>
- <Category 2>: <Description>
- ...

<Specific area> improvements:
- <Detailed change 1>
- <Detailed change 2>
- ...

Other changes:
- <Miscellaneous improvements>
- ...

This squash consolidates N commits focusing on <focus areas>.

Statistics: X files changed, Y insertions(+), Z deletions(-)
```

## Example Invocation

**User request:**
```
Help me squash commits from f2da9a6 to d2755e90
```

**Skill execution flow:**
1. Check current HEAD position
2. If not at correct position, prompt user:
   ```
   Please first reset to the parent of f2da9a6:
   git reset --hard <parent_commit_id>

   Then invoke this skill again.
   ```
3. If at correct position, proceed with:
   - List all commits to be squashed
   - Show statistics of changes
   - Analyze commit messages and file changes
   - Generate comprehensive commit message
   - Prompt user to run build/compile and wait for confirmation
   - If build fails, help resolve errors
   - If build succeeds, continue to next step
   - Execute `git merge --squash d2755e90`
   - Commit with generated message
   - Verify old commits are removed from branch

## Implementation Guidelines

### Step 1: Verify Prerequisites
```bash
# Get current HEAD
git rev-parse HEAD

# Get parent of start commit
git rev-parse <start_commit>^

# Compare - they should match
```

### Step 2: Analyze Commits
```bash
# List commits to squash (from start to end, inclusive)
git log --oneline <start_commit>..<end_commit>

# Include the end commit itself
git log --oneline <end_commit> -1

# Get commit messages for analysis
git log --format="%s" <start_commit>~1..<end_commit>
```

### Step 3: Analyze Changes
```bash
# Get file statistics
git diff --stat <start_commit>~1..<end_commit>

# Get detailed changes for major files
git diff <start_commit>~1..<end_commit> -- <important_files>
```

### Step 4: Generate Commit Message

Analyze the commits and changes to create a message that:
- Identifies the main purpose (Refactor, Feature, Fix, etc.)
- Groups changes by functional area
- Highlights important improvements
- Includes quantitative metrics

### Step 5: Build Verification

After generating the commit message but before executing the squash, prompt the user to verify the changes build correctly:

```
Please run your project's build/compilation command to verify the changes:
- For Node.js: npm run build or yarn build
- For Python: python -m pytest or your test suite
- For Go: go build ./...
- For Rust: cargo build
- For Java/Maven: mvn compile
- For other projects: use your project-specific build command

Please run the build and let me know:
1. If the build succeeds, I will proceed with creating the squash commit
2. If the build fails, share the error output and I will help resolve it
```

Wait for user response:
- If build succeeds: proceed to Step 6
- If build fails: analyze the error, help fix issues, ask user to rebuild, repeat until success

### Step 6: Execute Squash
```bash
# Squash merge all commits
git merge --squash <end_commit>

# Commit with generated message
git commit -m "$(cat <<'EOF'
<generated_message_here>
EOF
)"
```

### Step 7: Verify Result
```bash
# Check new commit is created
git log --oneline -3

# Verify old commits are NOT in current branch
git log --oneline HEAD~20..HEAD | grep -E "(<start_commit_short>|<end_commit_short>)"
# Should return empty
```

### Step 8: Save Summary to ai_docs
```bash
# Create ai_docs directory structure if not exists
mkdir -p ai_docs/git-squash-commits

# Generate summary filename with timestamp and commit hash
SUMMARY_FILE="ai_docs/git-squash-commits/$(date +%Y%m%d_%H%M%S)_$(git rev-parse --short HEAD).md"

# Write summary containing:
# - Squash operation metadata (date, commit range, new commit hash)
# - Generated commit message
# - Statistics (files changed, insertions, deletions)
# - List of original commits that were squashed
cat > "$SUMMARY_FILE" <<EOF
# Git Squash Summary

**Date**: $(date +"%Y-%m-%d %H:%M:%S")
**Branch**: $(git branch --show-current)
**New Commit**: $(git rev-parse HEAD)

## Commit Range Squashed
- Start: <start_commit>
- End: <end_commit>

## Generated Commit Message
\`\`\`
<paste the generated commit message here>
\`\`\`

## Statistics
<paste git diff --stat output>

## Original Commits
<paste git log --oneline output of squashed commits>
EOF

echo "Summary saved to: $SUMMARY_FILE"
```

## Notes

- The skill assumes a linear commit history between start and end commits
- Merge commits in the range will be included in the squash
- The generated commit message aims to be comprehensive yet concise
- All original commits will be removed from the current branch history
- The squash commit will have the current branch HEAD parent as its parent
- Statistics include all accumulated changes from start to end
- **Summary records**: Each squash operation creates a markdown file in `ai_docs/git-squash-commits/` directory
  - Filename format: `YYYYMMDD_HHMMSS_<short_hash>.md` (timestamp + new commit hash)
  - Content includes: operation metadata, generated commit message, statistics, and list of squashed commits
  - Records are useful for auditing and understanding the history of squash operations
  - The `ai_docs/` directory should be added to `.gitignore` if you prefer not to commit these records

## Error Handling

If the user hasn't reset to the correct parent commit:
1. Calculate the correct parent: `git rev-parse <start_commit>^`
2. Show current HEAD: `git rev-parse HEAD`
3. Instruct user to run: `git reset --hard <correct_parent>`
4. Exit and ask user to re-invoke after reset

## Best Practices

- Always verify the commit range before squashing
- Keep the generated message focused on "what" and "why"
- Group related changes together
- Highlight breaking changes or important modifications
- Include statistics for transparency
- **Always run build/compilation before creating the squash commit** to catch errors early
- Resolve all build errors before proceeding with the squash
- Test the changes after squashing to ensure nothing broke
