---
name: deslop
description: Remove AI-generated code slop from a branch. Use to delete unnecessary comments/docs, defensive checks, broad try/catch blocks, type-cast hacks, lint suppressions, dead code, duplication, and style drift. Diff against base (main/master) and align changes with existing project idioms without altering intended behavior.
---

# Remove AI Code Slop

Check the diff against the base branch and remove all AI-generated slop introduced in this branch.

## Remove

- Redundant comments/docs: Delete narration that restates obvious behavior (e.g., "Increment the date"). Remove stale bug/workaround notes that no longer apply. 
- Verbose comments: Make long comment blocks more concise while keeping the intent.
- Over-defensive handling: Remove unnecessary null/validation guards and broad try/catch blocks when inputs are trusted or exceptions should propagate. Prefer direct flow over catch-and-rethrow, empty catches.
- Silent fallbacks: Replace defensive fallbacks that silently mask invalid input with explicit errors. Surface potential bugs instead of hiding them.
- Type-system bypasses: Replace or remove casts/pragmas used only to silence errors (e.g., `any`, `as unknown as T`, `// @ts-ignore`, `# type: ignore`). Restore correct typing or remove the unnecessary construction.
- Dead/unused code: Delete unused imports, variables, helpers, alternate implementations, and commented-out code. Keep the diff free of placeholders and vestiges.
- Style drift: Conform to local patterns (naming, formatting, error handling, structure). 
- Duplication: Remove repeated logic and refactor to avoid duplicated semantics.

## Process

1. Diff against base:
   `git diff $(gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name')...HEAD`
2. Scan for slop: Identify added narration, guards, catches, casts, suppressions, dead code, duplication, and out-of-style constructs.
3. Edit for intent: 
  - Remove slop while preserving legitimate behavior. 
  - Fix root causes behind suppressions when feasible; otherwise remove the suppression if it was unnecessary.
  - Keep high-value comments that capture critical behavior or design intent that is not immediately obvious.
4. Verify and summarize: Run tests/linters and write a 1–3 sentence summary of the cleanup (e.g., removed redundant commentary and null checks; removed unnecessary try/catch; aligned code with project conventions).

