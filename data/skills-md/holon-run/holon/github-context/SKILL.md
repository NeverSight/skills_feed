---
name: github-context
description: "Shared GitHub context collection skill used by other skills. Collects issue/PR metadata, comments, files, diffs, review threads, commits, and check runs into a standard layout under ${GITHUB_CONTEXT_DIR}/github/."
---

# GitHub Context Skill

Foundational skill for collecting GitHub issue and pull request context into a standardized, structured format.

## Why Use This Skill?

Instead of running multiple `gh` commands manually, this skill provides:

- **Structured Output**: Consistent JSON format with all metadata in predictable locations
- **Comprehensive Collection**: Automatically gathers issues/PRs, comments, diffs, review threads, commits, and CI logs in one pass
- **Configurable Scope**: Fine-grained control over what to collect (diffs, checks, threads, etc.) via environment variables
- **Manifest Generation**: Produces `manifest.json` with collection metadata for downstream processing
- **Reusability**: Can be invoked standalone or as a dependency by other skills

## Environment and Paths

- **`GITHUB_CONTEXT_DIR`**: Output directory for collected context  
  - Default: `/holon/output/github-context` if the path exists; otherwise a temp dir `/tmp/holon-ghctx-*`
- **`MANIFEST_PROVIDER`** / **`COLLECT_PROVIDER`**: Provider name written to `manifest.json` (default: `github-context`)
- **`TRIGGER_COMMENT_ID`**: Comment ID to flag with `is_trigger` in comments/review threads
- **`INCLUDE_DIFF`** (default: `true`): Fetch PR diff
- **`INCLUDE_CHECKS`** (default: `true`): Fetch check runs and workflow logs
- **`INCLUDE_THREADS`** (default: `true`): Fetch review comment threads
- **`INCLUDE_FILES`** (default: `true`): Fetch changed files list
- **`INCLUDE_COMMITS`** (default: `true`): Fetch commits for the PR
- **`MAX_FILES`** (default: `200`): Limit for files collected when `INCLUDE_FILES=true`

## Usage

Use the skill runner (Holon or host) to invoke `scripts/collect.sh` with the reference; examples assume the script is on PATH or referenced relative to the skill directory:

```bash
collect.sh "holon-run/holon#123"
collect.sh 123 holon-run/holon
INCLUDE_CHECKS=false MAX_FILES=50 collect.sh https://github.com/holon-run/holon/pull/123
```

## Output Contract

Artifacts are written to `${GITHUB_CONTEXT_DIR}/github/`:

- `issue.json` (issues) or `pr.json` (PRs)
- `comments.json`
- `review_threads.json` (when `INCLUDE_THREADS=true` and PR)
- `files.json` (when `INCLUDE_FILES=true` and PR)
- `pr.diff` (when `INCLUDE_DIFF=true` and PR)
- `commits.json` (when `INCLUDE_COMMITS=true` and PR)
- `check_runs.json` and `test-failure-logs.txt` (when `INCLUDE_CHECKS=true` and PR)
- `manifest.json` (written at `${GITHUB_CONTEXT_DIR}/manifest.json`)

## Integration Notes

- Wrapper skills set their own defaults and `MANIFEST_PROVIDER` before delegating to this collector.
- The helper library lives at `scripts/lib/helpers.sh` and provides parsing, dependency checks, fetching helpers, and manifest writing. Source it instead of copying.

## Input Payload

When invoking this skill, you can provide a payload file with metadata:

- **`/holon/input/payload.json`** (optional): Contains task metadata with GitHub reference
  ```json
  {
    "ref": "holon-run/holon#502",
    "repo": "holon-run/holon",
    "type": "issue|pr",
    "trigger_comment_id": 123456
  }
  ```

The agent should extract the `ref` field from `payload.json` and pass it to the collection script. If `payload.json` doesn't exist or `ref` is not provided, check for:
1. Command-line arguments or environment variables with the reference
2. Fallback to requesting the reference from the user

## Reference Formats

The collection script accepts GitHub references in multiple formats:

- `holon-run/holon#502` - owner/repo#number format
- `502` - numeric (requires repo_hint as second argument)
- `https://github.com/holon-run/holon/issues/502` - full URL

## Context Files

When collection completes, the following files are available under `${GITHUB_CONTEXT_DIR}/github/`:

### Issue Context Files
- `issue.json`: Issue metadata
- `comments.json`: Issue comments

### PR Context Files
- `pr.json`: Pull request metadata including reviews and stats
- `files.json`: Changed files list (capped by `MAX_FILES`)
- `review_threads.json`: Review threads with line-specific comments (includes `comment_id`)
- `comments.json`: PR discussion comments
- `pr.diff`: The code changes being reviewed
- `commits.json`: PR commits (when `INCLUDE_COMMITS=true`)
- `check_runs.json`: CI/check run metadata (when `INCLUDE_CHECKS=true`)
- `test-failure-logs.txt`: Complete workflow logs for failed tests (when `INCLUDE_CHECKS=true`)

