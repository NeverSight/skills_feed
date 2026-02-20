---
name: writing-checks
description: Write Continue check files that review pull requests with AI agents. Use when the user asks to create, write, or generate a check, or wants to enforce a convention on PRs.
license: Apache-2.0
metadata:
  author: continuedev
  version: "1.0.0"
---

# Writing Checks

Write check files for Continue — markdown files that define AI agents that review pull requests.

## File format

A check is a markdown file with YAML frontmatter and a body. The frontmatter configures metadata. The body is the prompt the agent follows when reviewing a PR.

```markdown
---
name: Migration Safety
description: Flag destructive database migrations
---

Your prompt here. This becomes the agent's system prompt
when evaluating the pull request.
```

### Frontmatter fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | Yes | string | Display name shown in GitHub status checks and on continue.dev |
| `description` | Yes | string | Short description of what the check verifies |
| `model` | No | string | Model to use. Defaults to Claude Sonnet. Example: `anthropic/claude-sonnet-4-5-20250514` |

### File location

Save checks to `.continue/checks/<name>.md` at the repository root. Only `.md` files in that directory are scanned — subdirectories are not.

## Writing the body

The body is an agent prompt. Write it as direct instructions telling the agent what to look for and what to do about it.

### Scope narrowly

One check per concern. A check that tries to cover security, test coverage, and documentation will produce muddled results. Split into three checks.

### Be specific

List concrete criteria. Vague instructions produce vague results.

**Good:**

```
Look for these issues in the changed code and fix them:

- New REST endpoints missing request body validation
- Database queries using string interpolation instead of parameterized queries
- Error responses that expose stack traces or internal paths
```

**Bad:**

```
Check that the code is secure.
```

### What you don't need to write

The system automatically prepends a meta prompt that:

- Provides the full diff and list of changed files
- Instructs the agent to only review changed lines
- Prevents the agent from touching pre-existing issues in unchanged code
- Restricts edits to changed files only

Don't include instructions like "review the changed files" or "only look at the diff" — that's already handled. Focus on **what to look for and how to fix it**.

### What checks can do

The agent running a check can:

- **Read files** in the repository beyond the diff for context
- **Run bash commands** like `grep`, `find`, or custom scripts
- **Use a browser** to visit URLs, take screenshots, and verify rendered output
- **Access the PR diff** including file names, additions, and deletions
- **Use the GitHub CLI** (`gh`) to read PR metadata, comments, or linked issues

### Checks vs. tests vs. linting

**Linting** handles formatting, style, and static patterns. If a rule can be expressed as a pattern match on syntax, it belongs in a linter.

**Tests** verify correctness and behavior. If the question is "does this function return the right output," write a test.

**Checks** handle judgment calls that require understanding context:

- "Is this database migration safe to run on a 500M-row table?"
- "Does this PR update the API docs to reflect the endpoint changes?"
- "Are there security issues in this auth flow a linter wouldn't catch?"

## Workflow

When the user asks you to write a check:

1. **Understand the codebase** — Read relevant source files, configs, and existing checks in `.continue/checks/` to understand the project's stack, conventions, and what's already covered.
2. **Pick one concern** — If the user asks for something broad (e.g. "security"), identify the most impactful single concern for their stack and write a check for that. Offer to write more as follow-ups.
3. **Write concrete criteria** — List exactly what to look for. Include good/bad code examples using the project's actual frameworks and patterns when possible.
4. **Define pass/fail clearly** — The agent needs to know when to pass and when to fail. Include explicit "no action needed if" conditions where appropriate.
5. **Save the file** — Write to `.continue/checks/<name>.md`.

## Example check

```markdown .continue/checks/migration-safety.md
---
name: Migration Safety
description: Flag destructive database migrations
---

If no migration files were added or changed, no action is needed.

When migrations are present, look for these issues:

- `DROP TABLE` or `DROP COLUMN` without a preceding migration that backs up or migrates the data — add a data migration step or split into separate migrations
- Column type narrowing (e.g., `TEXT` to `VARCHAR(50)`, `BIGINT` to `INT`) without a backfill step — add a backfill or guard against data truncation
- `NOT NULL` constraint added to an existing column without a `DEFAULT` value — add a default or a data backfill migration
- Renaming a column or table that is referenced by application code without updating that code in the same PR — update the references
- A destructive and a constructive change in the same migration file — split into separate migrations for safe rollback
```
