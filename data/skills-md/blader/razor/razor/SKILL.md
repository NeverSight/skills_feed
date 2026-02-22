---
name: razor
description: "Minimize local diff size against merge base for uncommitted branch work using only behavior-preserving, scope-preserving architectural reductions."
---

# Razor

Reduce local diff size with merge-base-anchored architectural planning and behavior-preserving execution only.

## Core Iteration Directive
On every iteration, follow this exact directive:

"Deeply analyze this implementation across the entire PR (not file-by-file in isolation), and create a detailed plan called TRIM_CODEX.MD with the most impactful architectural ideas to dramatically reduce the total size of this PR, without reducing scope or behavior. Comments do not count."

## Non-negotiables
- Always anchor to merge base: `MB=$(git merge-base <base-ref> HEAD)` (`origin/latest` by default).
- Use unified working-tree diff only: `git diff "$MB"`.
- Include untracked code-file lines in insertion totals.
- Only propose/apply behavior-preserving, scope-preserving reductions.
- Never generate functionality-loss or scope-reduction options.
- Do not remove/trim comments or doc-comments. Comment lines do not count toward reduction targets.
- Keep optimization priority:
  1. Primary: reduce non-comment insertions.
  2. Secondary: reduce non-comment total churn.
- Optimize at PR architecture level first:
  1. Identify duplication and redundant abstractions spanning multiple files/components.
  2. Prefer ideas that remove whole cross-file patterns or flows, not local line edits.
  3. Treat file-local cleanups as fallback only after high-impact PR-wide ideas are exhausted.
- Read every line of every file in the diff on every iteration.
- Update `TRIM_CODEX.MD` every iteration before execution, then refresh after re-measurement.
- Run formatting on touched files and run targeted validation each pass.
- Never use destructive git commands.

## Workflow
1. Establish base and merge base.
2. Measure unified diff (`status`, `numstat`, `name-status`, untracked files, untracked code lines).
3. Compute baseline metrics:
   - insertions
   - deletions
   - total churn
   - comment-line additions (reported separately, not targeted)
4. Full-diff read (mandatory):
   - For each file in `git diff --name-status "$MB"`, read full current file contents.
   - For modified files, also review `git diff "$MB" -- <file>` hunks.
5. Deep architectural analysis:
   - Identify structural duplication and avoidable abstraction layers across the full PR surface.
   - Map cross-file data/control flow to find consolidation cuts that remove entire repeated paths.
   - Rank ideas by expected PR-wide churn reduction; prioritize multi-file high-leverage cuts.
6. Write/update `TRIM_CODEX.MD` with:
   - Goal and invariants.
   - Merge-base baseline and divergence.
   - Runtime/test hotspot ranking.
   - Architectural diagnosis of churn drivers.
   - Ranked behavior-preserving architectural ideas with explicit PR-wide scope (estimated insertion/churn savings, risk, validation notes).
   - Clear separation of `PR-wide architectural cuts` vs `local cleanup` (local cleanup only when no higher-impact architectural cuts remain).
   - Ordered execution sequence and validation gates.
   - Iteration history.
7. Apply viable behavior-preserving ideas.
8. Format touched files.
9. Run targeted validation.
10. Re-measure and refresh `TRIM_CODEX.MD` with before/after metrics and applied/skipped status.
11. Rerun fresh planning on the updated tree.

## Output contract
Always return:
1. Base ref and merge-base SHA.
2. Before stats and after stats (insertions, deletions, churn).
3. Primary and secondary percent reductions.
4. Comment-line additions count (reported separately).
5. Ranked behavior-preserving ideas and applied changes.
6. Confirmation `TRIM_CODEX.MD` was refreshed this iteration.
7. Confirmation every diff file was fully read this iteration.
8. Explicit statement whether any additional behavior-preserving, scope-preserving reductions remain after fresh rerun.
