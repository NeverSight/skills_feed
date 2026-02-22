---
name: create-pr
description: Create a Pull Request for a Marshroom cart issue matching the current branch with proper closing keywords
---

Create a Pull Request for a Marshroom cart issue matching the current branch.

## Critical Requirements

- **state.json update is MANDATORY**. After creating the PR, you MUST update the issue status to `pending` with `prNumber` and `prURL` in `~/.config/marshroom/state.json`. If this fails, stop and report the error — do NOT silently continue.
- Use `marsh pr` if available; otherwise fall back to direct `jq` atomic write (see step 9).

## Steps

1. Read `~/.config/marshroom/state.json` and parse the JSON
2. Run `git branch --show-current` to get the current branch name
3. Find the cart entry matching the current branch and repo. Use relaxed matching:
   - First try exact `branchName` match
   - Then try `/#N` suffix match (e.g., current branch `HotFix/#20` matches cart entry with `branchName: "Feature/#20"` because both end with `/#20`)
   - If no match, tell the user they're not on a cart issue branch
3-1. Commit the current changes. Give proper commit message to commits. Ask user permission if the changes are too large or suspicious (e.g. 100+ changes, dummy files, DB updates, logs, and so on)
4. Push the current branch: `git push -u origin HEAD`
5. Build the PR body:
   - Start with a brief description of the changes made
   - If the matched cart entry has an `issueBody` field (non-null), include it under a "## Original Issue" section for reviewer context
   - The body MUST include `close #<issueNumber>` (this is mandatory for auto-closing the issue)
6. Create the PR using `gh pr create`:
   - Title: the issue title from the matched cart entry
   - Body: the constructed body from step 5
7. After PR creation, verify the body contains the closing keyword:
   - Run `gh pr view --json body -q '.body'`
   - If `close #<issueNumber>` is NOT found in the body, fix it: `gh pr edit --body "$(gh pr view --json body -q '.body')\n\nclose #<issueNumber>"`
8. Capture the PR URL and number:
   - Run `gh pr view --json number,url -q '.number,.url'`
9. **Update issue status (MANDATORY)**:
   - First try: `marsh pr`
   - If `marsh` is not found in PATH, fall back to direct atomic update using the PR number and URL from step 8:
     ```bash
     TMP="$(mktemp ~/.config/marshroom/state.json.XXXXXX)"
     jq --argjson n ISSUE_NUMBER --argjson prNum PR_NUMBER --arg prUrl "PR_URL" \
       '.cart |= map(if .issueNumber == $n then .status = "pending" | .prNumber = $prNum | .prURL = $prUrl else . end)' \
       ~/.config/marshroom/state.json > "$TMP" && mv -f "$TMP" ~/.config/marshroom/state.json
     ```
   - Verify the update succeeded by reading state.json and confirming status is `pending`
10. Display the result:
    - PR URL
    - PR Number
    - Issue: #{issueNumber} {issueTitle}
    - Status: pending
