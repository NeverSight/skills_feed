---
name: start-issue
description: Start working on a Marshroom cart issue — creates branch, injects context, updates status to running
---

Start working on a Marshroom cart issue in the current repository.

## Critical Requirements

- **state.json update is MANDATORY**. After creating the branch, you MUST update the issue status to `running` in `~/.config/marshroom/state.json`. If this fails, stop and report the error — do NOT silently continue.
- Use `marsh start` if available; otherwise fall back to direct `jq` atomic write (see step 10).

## Steps

1. Read `~/.config/marshroom/state.json` and parse the JSON
2. Extract the `cart` array. If the cart is empty, tell the user to add issues in the Marshroom app
3. Run `git remote get-url origin` to get the current repo's remote URL
4. Extract `owner/repo` from the remote URL (handle both HTTPS and SSH formats)
5. Filter cart entries where `repoCloneURL` (HTTPS) or `repoSSHURL` (SSH) matches the current remote. Compare by extracting `owner/repo` from each
6. If no matching cart entries, tell the user this repo has no cart issues
7. If `$ARGUMENTS` contains an issue number, find that entry; otherwise if multiple matches, list them and ask the user to pick one
8. Run `git checkout main && git pull origin main` to ensure main is up to date
9. Create and checkout the branch: `git checkout -b {branchName}` The branch name should be `Feature/#N` or `HotFix/#N`. `N` is issue number.
10. **Update issue status (MANDATORY)**:
    - First try: `marsh start #{issueNumber}`
    - If `marsh` is not found in PATH, fall back to direct atomic update:
      ```bash
      TMP="$(mktemp ~/.config/marshroom/state.json.XXXXXX)"
      jq --argjson n ISSUE_NUMBER '.cart |= map(if .issueNumber == $n then .status = "running" else . end)' \
        ~/.config/marshroom/state.json > "$TMP" && mv -f "$TMP" ~/.config/marshroom/state.json
      ```
    - Verify the update succeeded by reading state.json and confirming status is `running`
11. Inject issue context:
    - Read the `issueBody` field from the matched cart entry
    - If non-null, display it under a "## Issue Details" header
    - This gives the agent full context about what needs to be done
12. Confirm the branch was created and display:
    - Issue: #{issueNumber} {issueTitle}
    - Branch: {branchName}
    - Repository: {repoFullName}
    - Status: running
13. Ask the user permission to start planning to resolve issue. If the user allows it, starts planning using /plan mode.
