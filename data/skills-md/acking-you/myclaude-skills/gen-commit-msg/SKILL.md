---
name: gen-commit-msg
description: Generate concise commit messages based on conversation context and minimal git inspection.
---

# Generate Commit Message Skill

## Overview

This skill generates concise, meaningful commit messages by:
1. **First priority**: Use conversation context (files edited, changes discussed)
2. **Fallback**: Run `git diff` when context is unavailable
3. Keep messages brief and focused

## When to Use

- After implementing changes discussed in the conversation
- When you want a commit message that reflects the actual work done
- To quickly commit without manual message writing

## Usage

Simply invoke this skill after making changes. The skill will:
1. Check conversation context for what was changed
2. If no context: run `git diff --cached` to analyze changes
3. Generate a concise commit message
4. Prompt for user confirmation before committing

## Commit Message Format

```
<type>: <brief summary (<=50 chars)>

[Optional body: concise explanation of what/why, <=3 lines]

[Optional footer: Breaking changes, issue refs]
```

### Type Prefixes

- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code restructure without behavior change
- `perf`: Performance improvement
- `docs`: Documentation only
- `style`: Formatting, whitespace
- `test`: Add/update tests
- `chore`: Build, tools, dependencies
- `build`: Build system changes
- `ci`: CI/CD changes

## Implementation Guidelines

### Step 1: Check Conversation Context

**Has context if:**
- Files were edited via Write/Edit tools in this conversation
- User described what was changed
- Features/fixes were discussed

**No context if:**
- User just says "commit my changes" without prior discussion
- Changes were made outside this conversation
- Files were modified manually by user

### Step 2: Get Change Information

**If context available:**
- Use known file edits and changes
- Skip git diff entirely

**If no context:**
```bash
# Get list of changed files with status
git diff --cached --name-status

# Get file-level stats
git diff --cached --stat

# Get actual changes (for understanding what was done)
git diff --cached

# Alternative: if nothing staged, check working directory
git status --short
git diff --stat
git diff
```

### Step 3: Generate Concise Message

Principles:
- **Brevity**: Summary <=50 chars, body <=3 lines
- **What, not how**: Describe the outcome, not implementation
- **Imperative mood**: add, fix, update (not added, fixed)

**Good Examples:**
```
feat: add scroll limit config commands

Add get-scroll-settings and set-scroll-limit commands
to es_tool.sh for managing ES scroll configuration.
```

```
fix: ensure bulk requests end with newline

ES bulk API requires NDJSON format with trailing newline.
```

```
refactor: translate es_tool comments to English
```

**Bad Examples:**
```
feat: implement comprehensive elasticsearch scroll configuration management system

This commit adds a full suite of commands for managing scroll-related
settings in Elasticsearch including viewing current configuration,
modifying document count limits, enabling/disabling rejection behavior...
[TOO VERBOSE]
```

### Step 4: Present and Confirm

```bash
# Show what will be committed
git status --short

# Present message
echo "Proposed commit message:"
echo "----------------------------------------"
echo "<generated_message>"
echo "----------------------------------------"
echo ""
read -p "Commit these changes? (y/n): " response
```

### Step 5: Execute Commit

**CRITICAL**: The commit message MUST be clean and professional. DO NOT include:
- `🤖 Generated with [Claude Code]` markers
- `Co-Authored-By: Claude` attributions
- Any other tool-generated metadata or signatures

These add no value and clutter the commit history.

```bash
# Commit with generated message (NO extra metadata)
git commit -m "$(cat <<'EOF'
<generated_message>
EOF
)"

# Show result
git log -1 --oneline
```

## Decision Flow

```
START
  |
  v
Do we have conversation context about changes?
  |
  +-- YES --> Use context to generate message
  |            (Skip git diff)
  |
  +-- NO --> Run git diff to analyze changes
              |
              v
            Are changes staged?
              |
              +-- YES --> git diff --cached
              |
              +-- NO --> git diff (working directory)
  |
  v
Generate concise commit message
  |
  v
Present to user for confirmation
  |
  v
User confirms?
  |
  +-- YES --> git commit
  |
  +-- NO --> Exit (no commit)
  |
  v
END
```

## Examples

### Example 1: With Context (No Git Diff)

**Conversation:**
```
User: Add health check commands to es_tool.sh
Assistant: [edits es_tool.sh, adds check-health, check-shards, etc.]
User: Create a commit
```

**Skill execution:**
1. Context available: Edited es_tool.sh, added health check commands
2. Skip git diff
3. Generate:
   ```
   feat: add cluster health check commands

   Implements check-health, check-shards, explain-allocation,
   and fix-red-shards for ES cluster diagnostics.
   ```

### Example 2: No Context (Use Git Diff)

**Conversation:**
```
User: Generate commit message
```

**Skill execution:**
1. No context available
2. Run git diff --cached:
   ```diff
   diff --git a/script/es_tool.sh b/script/es_tool.sh
   @@ -841,7 +841,7 @@ execute_http_request() {
   -            content_type="text/plain"
   +            content_type="application/x-ndjson"
   +            # Ensure body ends with newline
   +            if [[ "$body" != *$'\n' ]]; then
   +                body="${body}"$'\n'
   +            fi
   ```
3. Analyze: Changed content-type for bulk requests, added newline
4. Generate:
   ```
   fix: correct bulk request content-type

   Use application/x-ndjson and ensure trailing newline
   for ES bulk API NDJSON format compliance.
   ```

### Example 3: User Provides Context

**Conversation:**
```
User: Commit the fix for the bulk API newline issue
```

**Skill execution:**
1. Context from user: "fix for bulk API newline issue"
2. Quick check: `git diff --cached --name-only` (just filenames)
   ```
   script/es_tool.sh
   ```
3. Generate (minimal diff needed):
   ```
   fix: ensure bulk requests end with newline

   Add trailing newline to bulk request body for
   ES NDJSON format requirements.
   ```

## Best Practices

### DO:
- Use conversation context when available
- Run git diff when context is missing
- Keep summary under 50 characters
- Use imperative mood (add, fix, update)
- Focus on WHAT and WHY
- Confirm with user before committing

### DON'T:
- Skip git diff when you have no context
- Write verbose explanations
- Describe HOW code was implemented
- Auto-commit without confirmation
- Use past tense (added, fixed, updated)

## Git Tags

When user requests creating a tag (for CI/CD pipeline trigger, release, etc.):

1. **Check existing tag format first**:
   ```bash
   git tag --sort=-creatordate | head -5
   ```

2. **Keep format consistent** - DO NOT add 'v' prefix unless project already uses it:
   - If existing: `0.4.0`, `0.3.0` → use `0.4.1` (no 'v')
   - If existing: `v0.4.0`, `v0.3.0` → use `v0.4.1` (with 'v')

3. **Never assume tag format** - always verify from existing tags

## Notes

- Optimizes for speed by using context when available
- Falls back to git diff when needed for accuracy
- Generates concise but informative messages
- Always confirms before committing
- Works in both interactive and standalone scenarios
