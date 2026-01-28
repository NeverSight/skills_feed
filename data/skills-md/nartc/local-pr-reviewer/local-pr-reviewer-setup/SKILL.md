---
name: local-pr-reviewer-setup
description: Setup and usage guide for local-pr-reviewer - a local PR review tool for AI coding agents. Enables users to review code changes via a web UI and send comments back to their AI coding session.
---

# Local PR Reviewer

A local PR review tool that lets you review code changes in a web UI and send feedback to your AI coding session.

## First-time Setup

If the user hasn't set up local-pr-reviewer yet, guide them to run:

```bash
npx local-pr-reviewer setup
```

This will:

- Install the review server to `~/.config/local-pr-reviewer/`
- Configure MCP tools for your coding agent
- Optionally setup AI features for comment processing

## Starting a Review Session

To start reviewing code, use the `start_review_server` MCP tool. This will:

1. Start the web server if not already running
2. Return a URL to the review interface for the current repository

Alternatively, the user can run:

```bash
npx local-pr-reviewer start
```

## Workflow

1. **Start Review Server**: Use `start_review_server` tool to get the review URL
2. **Open Review UI**: Navigate to the URL in a browser
3. **Write Comments**: Review the diff, add comments to specific lines or files
4. **Send Comments**: Click "Send" to queue comments for the coding agent
5. **Receive Comments**: Use `check_pr_comments` tool to fetch pending comments
6. **Address Comments**: Make the requested changes
7. **Mark Resolved**: Use `mark_comment_resolved` tool after addressing each comment

## Proactive Comment Monitoring

When `start_review_server` is called or user mentions reviewing, enable continuous monitoring mode.

### Monitoring Behavior

After starting PR review:

1. Check `.local-pr-reviewer-pending` file in repo root after completing ANY task
2. If `pendingCount > 0`, call `check_pr_comments` MCP tool
3. Present new comments to user before proceeding to next task

### Integration Points

Check for comments at these natural breakpoints:

- **After completing a code edit**
- **After running builds/tests**
- **Before responding "done" or "complete" to user**
- **When idle/waiting for user input**

### Signal File Format

The `.local-pr-reviewer-pending` file contains:

```json
{
	"sessionId": "...",
	"repoPath": "/path/to/repo",
	"pendingCount": 3,
	"updatedAt": "2024-01-15T10:30:00.000Z"
}
```

**Quick check pattern**:

1. Read `.local-pr-reviewer-pending` file
2. If `pendingCount > 0`, call `check_pr_comments` to fetch details
3. Address comments before moving on

### Example Flow

```
User: "Review my changes"
Agent: *calls start_review_server, gives URL to user*

User: "Fix the login bug"
Agent: *fixes bug*
Agent: *reads .local-pr-reviewer-pending, sees pendingCount: 2*
Agent: *calls check_pr_comments*
Agent: "Done with the fix. I also see you added 2 review comments - let me address those..."
```

## Available MCP Tools

### `start_review_server`

Starts the review web server and returns the URL for the current repository.

**When to use**: When user wants to review code or start a review session.

### `get_server_status`

Check if the review server is running and get its URL.

**When to use**: To check server status without starting it.

### `check_pr_comments`

Fetch pending review comments for the current repository. Comments are marked as delivered after fetching.

**When to use**:

- After user has written comments in the web UI
- When user asks to check for comments
- Proactively while user is reviewing (poll periodically)

### `mark_comment_resolved`

Mark a comment as resolved after addressing it. Use the comment ID from `check_pr_comments`.

**When to use**: After you've addressed a review comment. This updates the signal file with the new pending count.

### `list_pending_comments`

List pending comments across all repositories.

**When to use**: To see all pending review work.

### `list_repo_pending_comments`

List pending comments for the current repository only.

**When to use**: To see pending comments for the current project.

### `get_comment_details`

Get full details of a specific comment including file path, line numbers, and content.

**When to use**: When you need more context about a specific comment.

## Stopping the Server

To stop the running server:

```bash
npx local-pr-reviewer stop
```

## Updating

To update to the latest version:

```bash
npx local-pr-reviewer@latest setup
```

## Troubleshooting

### Server not starting

- Run `npx local-pr-reviewer setup` to ensure proper installation
- Check if another process is using the port

### Comments not appearing

- Ensure you're in the correct repository
- Check that the repository is registered in the review UI
- Use `check_pr_comments` to manually fetch comments

### MCP tools not available

- Run `npx local-pr-reviewer setup-mcp` to reconfigure MCP
- Restart your coding agent after configuration changes
