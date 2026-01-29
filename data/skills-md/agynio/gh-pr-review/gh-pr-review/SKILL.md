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
- Access PR review context for automated workflows
- Filter reviews by state, reviewer, or resolution status

This tool is particularly useful for:
- Automated PR review workflows
- LLM-based code review agents
- Terminal-based PR review processes
- Getting structured review data without multiple API calls

## Installation

First, ensure the extension is installed:

```sh
gh extension install agynio/gh-pr-review
```

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
gh pr-review review --start -R owner/repo <pr-number>
```

Add inline comments to pending review:

```sh
gh pr-review review --add-comment \
  --review-id <PRR_...> \
  --path <file-path> \
  --line <line-number> \
  --body "Your comment" \
  -R owner/repo <pr-number>
```

Submit the review:

```sh
gh pr-review review --submit \
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

1. Start: `gh pr-review review --start -R owner/repo <pr>`
2. Add comments: `gh pr-review review --add-comment -R owner/repo <pr> --review-id <PRR_...> --path <file> --line <num> --body "..."`
3. Submit: `gh pr-review review --submit -R owner/repo <pr> --review-id <PRR_...> --event REQUEST_CHANGES --body "Summary"`

## Important Notes

- All IDs use GraphQL format (PRR_... for reviews, PRRT_... for threads)
- Commands use pure GraphQL (no REST API fallbacks)
- Empty arrays `[]` are returned when no data matches filters
- The `--include-comment-node-id` flag adds PRRC_... IDs when needed
- Thread replies are sorted by created_at ascending

## Documentation Links

- Usage guide: docs/USAGE.md
- JSON schemas: docs/SCHEMAS.md
- Agent workflows: docs/AGENTS.md
- Blog post: https://agyn.io/blog/gh-pr-review-cli-agent-workflows
