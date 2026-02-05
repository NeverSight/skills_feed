---
name: prd-to-json
description: Convert .prd PRD markdown into .prd/prd.json with validation.
---

# PRD to JSON

Use this skill to convert `.prd/prd-*.md` into `.prd/prd.json` for Ralph.

## Inputs

- If multiple PRD files exist, ask which one to convert.
- If no PRD file exists, instruct the user to run `/prd-discovery` first.

## Workflow

1. **Find the PRD**
   - Look for `.prd/prd-*.md`.
   - If one file exists, use it. Otherwise ask the user to choose.

2. **Parse the PRD**
   - Extract title, overview, and user stories.
   - For each story, capture id, title, description, and acceptance criteria.

3. **Validate content**
   - Each story must be completable in one iteration.
   - Stories must be ordered by dependency.
   - Acceptance criteria must be verifiable.
   - Every story must include "Typecheck/lint/test passes".
   - UI stories must include "Verify in browser".

4. **Generate JSON**
   - Use the template structure.
   - Set `passes: false` on all stories.
   - Use double quotes and valid JSON.

5. **Save output**
   - Write to `.prd/prd.json`.
   - Create `.prd` if missing.

6. **Report**
   - Summarize the number of stories and the generated branch name.
   - Suggest running Ralph next.
