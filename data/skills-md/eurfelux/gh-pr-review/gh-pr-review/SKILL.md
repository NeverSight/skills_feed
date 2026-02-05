---
name: gh-pr-review
description: View and manage inline GitHub PR review comments with full thread context from the terminal
---

# gh-pr-review

A GitHub CLI extension that provides complete inline PR review comment access from the terminal with LLM-friendly JSON output.

## When to Use

Use this skill when you need to:

- View inline review comments and threads on a pull request
- Reply to review comments programmatically
- Resolve or unresolve review threads
- Create and submit PR reviews with inline comments
- Edit comments in pending reviews
- Delete comments from pending reviews
- Preview pending review comments with code context before submitting
- Access PR review context for automated workflows
- Filter reviews by state, reviewer, or resolution status

This tool is particularly useful for:
- Automated PR review workflows
- LLM-based code review agents
- Terminal-based PR review processes
- Getting structured review data without multiple API calls

## Installation

Install the latest release directly from GitHub:

```sh
gh extension install EurFelux/gh-pr-review
```

Or download the pre-built binary for your platform from the [releases page](https://github.com/EurFelux/gh-pr-review/releases) and install manually.

## Core Commands

### 1. View All Reviews and Threads

Get complete review context with inline comments and thread replies:

```sh
gh pr-review review view -R owner/repo --pr <number>
```

**Useful filters:**
- `--unresolved` - Only show unresolved threads
- `--reviewer <login>` - Filter by specific reviewer
- `--states <APPROVED|CHANGES_REQUESTED|COMMENTED|DISMISSED>` - Filter by review state
- `--tail <n>` - Keep only last n replies per thread
- `--not_outdated` - Exclude outdated threads

**Output:** Structured JSON with reviews, comments, thread_ids, and resolution status.

### 2. Reply to Review Threads

Reply to an existing inline comment thread:

```sh
gh pr-review comments reply <pr-number> -R owner/repo \
  --thread-id <PRRT_...> \
  --body "Your reply message"
```

### 3. List Review Threads

Get a filtered list of review threads:

```sh
gh pr-review threads list -R owner/repo <pr-number> --unresolved --mine
```

### 4. Resolve/Unresolve Threads

Mark threads as resolved:

```sh
gh pr-review threads resolve -R owner/repo <pr-number> --thread-id <PRRT_...>
```

### 5. Create and Submit Reviews

Start a pending review:

```sh
gh pr-review review start -R owner/repo <pr-number>
```

Add inline comment (recommended - explicit single line):

```sh
gh pr-review review add-comment \
  --review-id <PRR_...> \
  --path <file-path> \
  --start-line <line-number> \
  --line <line-number> \
  --body "Your comment" \
  -R owner/repo <pr-number>
```

Add multi-line comment (range):

```sh
gh pr-review review add-comment \
  --review-id <PRR_...> \
  --path <file-path> \
  --start-line <start-line> \
  --line <end-line> \
  --start-side <LEFT|RIGHT> \
  --side <LEFT|RIGHT> \
  --body "Your comment" \
  -R owner/repo <pr-number>
```

> **Note**: While `--line` alone works for single-line comments, using both `--start-line` and `--line` with the same value is recommended for clarity.

**Tip: Using heredoc for multi-line comments with code blocks**

When your comment contains code blocks or special characters, use a heredoc to avoid shell escaping issues:

```bash
gh pr-review review add-comment \
  --review-id <PRR_...> \
  --path <file-path> \
  --line <line-number> \
  --body "$(cat <<'EOF'
**Issue: Unstable React key**

Using `index` as React key is problematic:

```tsx
// Before
todos.map((todo, index) => <Todo key={index} />)

// After
todos.map((todo) => <Todo key={todo.id} />)
```

This causes unnecessary re-renders when list reorders.
EOF
)" \
  -R owner/repo <pr-number>
```

The `<<'EOF'` syntax prevents variable expansion, preserving `$` and backticks literally.

**Comment positioning parameters:**

- `--line` (required) - The absolute line number in the file where the comment ends. For `RIGHT` side, this is the line number in the **modified** file. For `LEFT` side, this is the line number in the **original** file. The line must fall within a diff hunk range.
- `--side` (optional) - Which version of the code to comment on: `LEFT` (original) or `RIGHT` (modified). Default: `RIGHT`
- `--start-line` (optional) - The starting line number for multi-line comments. When specified, `--line` becomes the end line
  - **Best practice**: Even for single-line comments, consider using `--start-line` with the same value as `--line`. This makes your intent explicit and avoids confusion about whether you're targeting a single line or a range.
- `--start-side` (optional) - Which side the start line is on. Use when `--start-line` is specified

**Line Number Rules:**

`--line` takes the **absolute line number in the file** — the same number you see in your editor or in the diff gutter on GitHub. The line must fall within a diff hunk range (GitHub rejects lines outside the diff).

### How to verify a line is within a diff hunk

**Step 1: Get the patch for the file**
```sh
gh api repos/OWNER/REPO/pulls/PR/files --jq '.[] | select(.filename == "path/to/file.ts") | .patch'
```

**Step 2: Read the diff hunk header**
```
@@ -oldStart,oldCount +newStart,newCount @@
```
- For `RIGHT` side: valid range is `newStart` to `newStart + newCount - 1`
- For `LEFT` side: valid range is `oldStart` to `oldStart + oldCount - 1`
- For **new files** (`-0,0 +1,N`): valid range is `1` to `N`

### Examples

**Example 1: New file**
```diff
@@ -0,0 +1,10 @@
+line 1
+line 2
+line 3
```
To comment on "line 3": Use `--line 3` (absolute line number in the new file)

**Example 2: Modified file (RIGHT side)**
```diff
@@ -100,5 +100,15 @@
 existing code line 100    <- RIGHT line 100
 existing code line 101    <- RIGHT line 101
+new code A                <- RIGHT line 102
+new code B                <- RIGHT line 103 (comment here: --line 103)
+new code C                <- RIGHT line 104
 existing code line 105    <- RIGHT line 105
```
To comment on "new code B": Use `--line 103 --side RIGHT`

**Example 3: Modified file (LEFT side)**
```diff
@@ -50,7 +50,7 @@
 import { isJSON, parseJSON } from '@renderer/utils'
-import { defaultTimeout } from '@shared/config/constant'    <- LEFT line 53
+import { DEFAULT_TIMEOUT } from '@shared/config/constant'
```
To comment on the deleted import: Use `--line 53 --side LEFT`

### Quick Reference Table

| Diff Header | Side | To comment on... | Use |
|-------------|------|------------------|-----|
| `@@ -0,0 +1,173 @@` | RIGHT | Line 80 of new file | `--line 80` |
| `@@ -224,6 +224,112 @@` | RIGHT | Line 280 in the modified file | `--line 280` |
| `@@ -50,7 +50,7 @@` | LEFT | Deleted line at old file line 53 | `--line 53 --side LEFT` |

### Common Mistakes

❌ **Wrong**: Using a line number that falls outside any diff hunk range
❌ **Wrong**: Confusing LEFT/RIGHT side — LEFT uses old file line numbers, RIGHT uses new file line numbers

✅ **Correct**: Use the absolute line number as shown in the diff gutter
✅ **Correct**: Verify the line falls within a hunk range using the `@@` header

> **Note on LEFT side ranges**: When using `--start-line` / `--line` with `--side LEFT`, the GitHub diff view will include any interleaved RIGHT side additions that fall between your start and end lines. This is a GitHub rendering behavior, not a tool issue.

**Debug tip**: If you get a "line number is invalid" error, verify the line falls within a hunk range. Use `gh api repos/OWNER/REPO/pulls/PR/files` to inspect the patch.

Edit a comment in pending review (requires comment node ID PRRC_...):

```sh
gh pr-review review edit-comment \
  --comment-id <PRRC_...> \
  --body "Updated comment text" \
  -R owner/repo <pr-number>
```

Delete a comment from pending review (requires comment node ID PRRC_...):

```sh
gh pr-review review delete-comment \
  --comment-id <PRRC_...> \
  -R owner/repo <pr-number>
```

Preview pending review comments before submitting:

```sh
# Preview all pending comments
gh pr-review review preview -R owner/repo <pr-number>

# Preview a single thread's comment by thread ID
gh pr-review review preview --thread-id <PRRT_...> -R owner/repo <pr-number>
```

**Output:** Shows pending comments with code context (diff lines each comment is attached to), including accurate LEFT/RIGHT side identification. The `code_context` field contains the actual diff lines.

> **Critical:** Always verify `code_context` content matches your intended target code. A successful API response doesn't guarantee correct positioning — only the `code_context` lines confirm where your comment will actually appear.

Submit the review:

```sh
gh pr-review review submit \
  --review-id <PRR_...> \
  --event <APPROVE|REQUEST_CHANGES|COMMENT> \
  --body "Overall review summary" \
  -R owner/repo <pr-number>
```

## Output Format

All commands return structured JSON optimized for programmatic use:

- Consistent field names
- Stable ordering
- Omitted fields instead of null values
- Essential data only (no URLs or metadata noise)
- Pre-joined thread replies

Example output structure:

```json
{
  "reviews": [
    {
      "id": "PRR_...",
      "state": "CHANGES_REQUESTED",
      "author_login": "reviewer",
      "comments": [
        {
          "thread_id": "PRRT_...",
          "path": "src/file.go",
          "author_login": "reviewer",
          "body": "Consider refactoring this",
          "created_at": "2024-01-15T10:30:00Z",
          "is_resolved": false,
          "is_outdated": false,
          "thread_comments": [
            {
              "author_login": "author",
              "body": "Good point, will fix",
              "created_at": "2024-01-15T11:00:00Z"
            }
          ]
        }
      ]
    }
  ]
}
```

## Best Practices

1. **Always use `-R owner/repo`** to specify the repository explicitly
2. **Use `--unresolved` and `--not_outdated`** to focus on actionable comments
3. **Save thread_id values** from `review view` output for replying
4. **Filter by reviewer** when dealing with specific review feedback
5. **Use `--tail 1`** to reduce output size by keeping only latest replies
6. **Parse JSON output** instead of trying to scrape text
7. **Verify line numbers fall within a diff hunk range** before adding inline comments
   - Use `gh api repos/OWNER/REPO/pulls/PR/files` to get patches
   - Check the `@@ -oldStart,oldCount +newStart,newCount @@` header for valid ranges
   - Use absolute file line numbers (RIGHT = new file, LEFT = old file)
8. **Preview each comment immediately after adding** — After each `add-comment`, run `review preview --thread-id <PRRT_...>` and verify the `code_context` matches your intended target code. If there's a mismatch, delete and re-add the comment on the correct line before proceeding to the next comment.

## Per-Comment Verification Checklist (MANDATORY)

After each `review add-comment`, you MUST immediately verify the comment by running `review preview --thread-id <PRRT_...>`.

### Verification Steps (per comment)
1. **Code Context Check (Critical):**
   - [ ] The `code_context` contains the **actual code** you intended to comment on (NOT comments, NOT empty lines, NOT JSDoc)
   - [ ] If commenting on a function call, `code_context` shows the call, not the comment above it
   - [ ] If commenting on an assignment, `code_context` shows `x = y`, not `}` or `/**`

2. **Intent Alignment Check:**
   - [ ] The comment body matches the code shown in `code_context`
   - [ ] If the comment says "this line does X", `code_context` actually shows that line

3. **On mismatch:** Delete the misplaced comment (`review delete-comment --comment-id <PRRC_...>`) and re-add it on the correct line. Do NOT proceed to the next comment until the current one passes verification.

**Example - Wrong vs Correct:**
```json
// ❌ WRONG - Comment attached to JSDoc
{
  "code_context": ["366:    * @param level - The log level to set"]
}

// ✅ CORRECT - Comment attached to implementation
{
  "code_context": ["369: +    this.consoleLevel = level", "370:     this.logger.level = level"]
}
```

**WARNING:** DO NOT submit if any comment has `code_context` pointing to JSDoc, empty lines, or incorrect code.

## Common Workflows

### Get Unresolved Comments for Current PR

```sh
gh pr-review review view --unresolved --not_outdated -R owner/repo --pr $(gh pr view --json number -q .number)
```

### Reply to All Unresolved Comments

1. Get unresolved threads: `gh pr-review threads list --unresolved -R owner/repo <pr>`
2. For each thread_id, reply: `gh pr-review comments reply <pr> -R owner/repo --thread-id <id> --body "..."`
3. Optionally resolve: `gh pr-review threads resolve <pr> -R owner/repo --thread-id <id>`

### Create Review with Inline Comments

Line numbers are **absolute file line numbers** (the same numbers shown in the diff gutter). They must fall within a diff hunk range.

1. Start: `gh pr-review review start -R owner/repo <pr>`
2. **Verify line is within a diff hunk**:
   ```sh
   gh api repos/OWNER/REPO/pulls/PR/files --jq '.[] | select(.filename == "target/file.ts") | {filename, patch}'
   ```
   Check the `@@ +newStart,newCount @@` header — valid range for RIGHT side is `newStart` to `newStart + newCount - 1`.
3. Add a comment: `gh pr-review review add-comment -R owner/repo <pr> --review-id <PRR_...> --path <file> --line <num> --body "..."`
4. **Immediately preview the comment just added:** `gh pr-review review preview --thread-id <PRRT_...> -R owner/repo <pr>` — verify `code_context` matches the intended target code. If mismatched, delete and re-add on the correct line.
5. Repeat steps 3–4 for each comment.
6. Edit comments (if needed): `gh pr-review review edit-comment -R owner/repo <pr> --comment-id <PRRC_...> --body "Updated text"`
7. Delete comments (if needed): `gh pr-review review delete-comment -R owner/repo <pr> --comment-id <PRRC_...>`
8. Submit: `gh pr-review review submit -R owner/repo <pr> --review-id <PRR_...> --event REQUEST_CHANGES --body "Summary"`

## Important Notes

- All IDs use GraphQL format (PRR_... for reviews, PRRT_... for threads)
- Commands use pure GraphQL (no REST API fallbacks)
- Empty arrays `[]` are returned when no data matches filters
- The `--include-comment-node-id` flag adds PRRC_... IDs when needed
- Thread replies are sorted by created_at ascending
- Use `--start-line` and `--start-side` for multi-line comments; `--line` becomes the end line

## Documentation Links

- Usage guide: docs/USAGE.md
- JSON schemas: docs/SCHEMAS.md
- Agent workflows: docs/AGENTS.md
- Blog post: https://agyn.io/blog/gh-pr-review-cli-agent-workflows
