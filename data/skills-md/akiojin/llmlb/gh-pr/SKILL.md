---
name: gh-pr
description: "Create or update GitHub Pull Requests with the gh CLI, including deciding whether to create a new PR or only push based on existing PR merge status. Use when the user asks to open/create/edit a PR, generate a PR body/template, or says 'PRを出して/PR作成/gh pr'. Defaults: base=develop, head=current branch (same-branch only; never create/switch branches)."
---

# GH PR

## Overview

Create or update GitHub Pull Requests with the gh CLI using a detailed body template and strict same-branch rules.

## Decision rules (must follow)

1. **Do not create or switch branches.** Always use the current branch as the PR head.
2. **Check for an existing PR for the current head branch.**
   - `gh pr list --head <head> --state all --json number,state,mergedAt,updatedAt,url,title,mergeCommit`
3. **If no PR exists** → create a new PR.
4. **If any PR exists and is NOT merged** (`mergedAt` is null) → push only and finish (do **not** create a new PR).
   - This applies to OPEN or CLOSED (unmerged) PRs.
   - Only update title/body/labels if the user explicitly requests changes.
5. **If all PRs for the head are merged** → check for post-merge commits (see below).
6. **If multiple PRs exist for the head** → use the most recently updated PR for reporting, but the create vs push decision is based on `mergedAt`.

## Post-merge commit check (critical)

When all PRs for the head branch are merged, you **must** check whether there are new commits after the merge:

1. **Get the merge commit SHA** of the most recent merged PR.
2. **Count commits after the merge**: `git rev-list --count <merge_commit>..HEAD`
3. **Decision**:
   - If new commits exist → create a new PR (these changes are not in the base branch)
   - If no new commits → report "No changes since last merge" and finish (do **not** create an empty PR)

### Why this matters

- **Scenario A**: PR merged → user makes local changes → pushes → changes are NOT in the merged PR
  - Without this check, the changes would be lost or require manual intervention
- **Scenario B**: PR merged → user says "create PR" without new changes → would create empty/duplicate PR
  - This check prevents unnecessary PR creation

## Workflow (recommended)

1. **Confirm repo + branches**
   - Repo root: `git rev-parse --show-toplevel`
   - Current branch (head): `git rev-parse --abbrev-ref HEAD`
   - Base branch defaults to `develop` unless user specifies.

2. **Fetch latest remote state**
   - `git fetch origin` to ensure accurate comparison

3. **Check existing PR for head branch**
   - Use decision rules above to pick action.
   - Treat `mergedAt` as the source of truth for "merged".

4. **If all PRs are merged, perform post-merge commit check**
   - Get merge commit: `gh pr list --head <head> --state merged --json mergeCommit -q '.[0].mergeCommit.oid'`
   - Count new commits: `git rev-list --count <merge_commit>..HEAD`
   - If 0 → finish with message "No new changes since merge"
   - If >0 → proceed to create new PR

5. **Ensure the head branch is pushed**
   - If no upstream: `git push -u origin <head>`
   - Otherwise: `git push`

6. **Collect PR inputs (for new PR or explicit update)**
   - Title, Summary, Context, Changes, Testing, Risk/Impact, Deployment, Screenshots, Related Links, Notes
   - Optional: labels, reviewers, assignees, draft

7. **Build PR body from template**
   - Read `references/pr-body-template.md` and fill placeholders.
   - If info is missing, keep TODO markers and explicitly mention them in the response.

8. **Create or update the PR**
   - Create: `gh pr create -B <base> -H <head> --title "<title>" --body-file <file>`
   - Update (only if user asked): `gh pr edit <number> --title "<title>" --body-file <file>`

9. **Return PR URL**
   - `gh pr view <number> --json url -q .url`

## Command snippets (bash)

```bash
head=$(git rev-parse --abbrev-ref HEAD)
base=develop

# Fetch latest remote state
git fetch origin

# Check existing PRs for the head branch
pr_json=$(gh pr list --head "$head" --state all --json number,state,mergedAt,mergeCommit)
pr_count=$(echo "$pr_json" | jq 'length')
unmerged_count=$(echo "$pr_json" | jq 'map(select(.mergedAt == null)) | length')

if [ "$pr_count" -eq 0 ]; then
  action=create
elif [ "$unmerged_count" -gt 0 ]; then
  action=push_only
else
  # All PRs are merged - check for post-merge commits
  merge_commit=$(echo "$pr_json" | jq -r 'sort_by(.mergedAt) | last | .mergeCommit.oid')
  
  if [ -n "$merge_commit" ] && [ "$merge_commit" != "null" ]; then
    new_commits=$(git rev-list --count "$merge_commit"..HEAD 2>/dev/null || echo "0")
    
    if [ "$new_commits" -gt 0 ]; then
      echo "Found $new_commits commit(s) after merge - creating new PR"
      action=create
    else
      echo "No new commits since merge - nothing to do"
      action=none
    fi
  else
    # Fallback: check against base branch
    new_commits=$(git rev-list --count "origin/$base"..HEAD 2>/dev/null || echo "0")
    
    if [ "$new_commits" -gt 0 ]; then
      action=create
    else
      action=none
    fi
  fi
fi

# Execute action
case "$action" in
  create)
    # Create PR body from template (edit as needed)
    cat > /tmp/pr-body.md <<'BODY'
## Summary
- TODO (one-sentence outcome)
- TODO (user-visible change, if any)

## Context
- TODO (why this PR is needed)
- TODO (background, ticket, or incident link)

## Changes
- TODO (key changes, bullets)
- TODO (notable refactors or cleanup)

## Testing
- TODO (commands run)
- TODO (manual steps, if any)

## Risk / Impact
- TODO (areas impacted)
- TODO (rollback plan / mitigation)

## Deployment
- TODO (steps, flags, or "none")

## Screenshots
- TODO (UI changes only)

## Related Issues / Links
- TODO (issues, specs, docs)

## Checklist
- [ ] Tests added/updated
- [ ] Lint/format checked
- [ ] Docs updated
- [ ] Migration/backfill plan included (if needed)
- [ ] Monitoring/alerts updated (if needed)

## Notes
- TODO (optional)
BODY

    git push -u origin "$head"
    gh pr create -B "$base" -H "$head" --title "..." --body-file /tmp/pr-body.md
    ;;
  push_only)
    echo "Existing unmerged PR found - pushing changes only"
    git push
    gh pr list --head "$head" --state open --json url -q '.[0].url'
    ;;
  none)
    echo "No action needed - no new changes since last merge"
    ;;
esac
```

## References

- `references/pr-body-template.md`: PR body template
