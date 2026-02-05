---
name: 05-review
description: "Perform a structured review focused on correctness, security best practices, bugs, and edge cases. Review either a GitHub PR (preferred, via gh) or a local diff vs base when no PR exists. Update tracking: mark PRD as Reviewed when LGTM; if the PR is merged, mark Merged, rename PRD to done-*, and update tasks/todo.md status to ✅. Triggers: review, self review, code review, security review, edge cases, pre-merge, gh pr diff, gh pr checks."
---

# 05 review

Review a change set against the prd with an explicit verdict and a clear list of issues and risks.

---

## Guardrails

- Default to review/report only. Do not change code unless explicitly asked.
- Only mark **Merged** when the PR is actually merged (verified via `gh` or explicitly confirmed).
- Do not invent test results or reproduction steps; run them or ask for evidence.

---

## Workflow

1. **Gather inputs**
   - prd path (e.g. `tasks/f-##-<slug>.md`)
   - review mode:
     - **PR mode** (preferred): PR URL/number
     - **Local mode**: base branch (default: `main`)

2. **Collect context**
   - PR mode:
     - `gh pr view --json url,title,body,baseRefName,headRefName,files,additions,deletions`
     - `gh pr diff`
     - `gh pr checks`
   - Local mode:
     - `git diff "<base>...HEAD"`
     - `git log "<base>..HEAD" --oneline`

3. **Review against the prd**
   - Confirm the change matches the prd goals and acceptance criteria.
   - Confirm non-goals are not being implemented.
   - Confirm edge cases and error states are handled.

4. **Review checklist**
   - Correctness:
     - boundary values, null/empty inputs, error paths
     - idempotency / retries (if applicable)
     - concurrency / ordering assumptions (if applicable)
     - timezones / pagination / encoding (if applicable)
   - Security best practices (as applicable to the change):
     - authn/authz checks
     - input validation + output encoding (XSS/injection risk)
     - CSRF/SSRF/path traversal/file upload handling (if relevant)
     - secrets handling (no tokens/keys), safe logging (no PII leakage)
     - dependency changes (new packages, supply-chain risk)
   - Tests:
     - happy path + key negative cases
     - regression coverage for touched areas
   - Maintainability:
     - clear naming, small functions, understandable control flow
     - comments/docs only where they add durable clarity

5. **Write the review report**
   - Use this structure:

     ```text
     Verdict: LGTM | Request changes

     Blockers (must fix):
     - …

     Suggestions (nice to have):
     - …

     Questions:
     - …

     Security notes:
     - …

     Regression risks / watch-outs:
     - …

     Manual QA checklist:
     - …
     ```

6. **Update tracking**
   - If verdict is **LGTM**:
     - In the prd `## Execution Status`, check **Reviewed**.
   - If in PR mode, detect whether the PR is merged:
     - `gh pr view --json mergedAt -q .mergedAt`
   - If merged:
     1. In the prd `## Execution Status`, check **Merged**.
     2. Rename the prd file with a `done-` prefix (e.g., `tasks/f-01-foo.md` → `tasks/done-f-01-foo.md`).
     3. Update `tasks/todo.md`:
        - update the feature’s `prd:` path to the renamed file
        - update the feature’s status indicator from `🔨` to `✅`

7. **Next**
   - Run `06-memory` to capture durable notes: what shipped, risks, and follow-ups.

---

## Output

- Review report (using the template above).
- What tracking was updated (prd checkboxes, renamed prd path, `tasks/todo.md` status), if any.
