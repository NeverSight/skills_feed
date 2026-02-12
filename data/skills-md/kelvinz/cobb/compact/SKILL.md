---
name: compact
description: "Compact `tasks/todo.md` and `tasks/memory.md` by summarising older completed history while preserving active context. Triggers: compact tracking files, prune todo history, trim memory log."
---

# compact

Keep `tasks/todo.md` and `tasks/memory.md` short and scannable by consolidating older entries into readable summaries.

---

## Guardrails

- Do not change product scope or implementation code.
- Do not move or rename PRDs here; completed PRDs are archived during `commit` finalise.
- Only compact `tasks/todo.md` feature entries when the corresponding PRD is already archived in `tasks/archive/`.
- Never compact checked entries whose PRD is still under `tasks/` (planned/in-progress, not completed).
- Do not create separate memory archive files.
- Keep feature IDs stable; never renumber.
- Ask for explicit confirmation before applying consolidation edits.
- Always propose retention/consolidation counts first; let the user choose the final numbers.

---

## Workflow

1. Preflight:
   - Ensure `tasks/` exists.
   - Inspect `tasks/todo.md` and `tasks/memory.md`.
   - Count items to compact:
     - `todo`: unchecked features, checked+archived features (eligible), checked+active features (ineligible)
     - `memory`: dated/log-style entries in `Key decisions`, `Completed`, `Notes / gotchas`
2. Propose consolidation options and ask for a decision:
   - Suggest how many entries to keep in full detail vs consolidate into summary.
   - Provide recommended defaults, then allow user override (more or fewer).
3. Compact `tasks/todo.md` in place:
   - Preserve all unchecked features unchanged.
   - Preserve all checked features whose PRD is not archived yet.
   - Keep the user-selected number of most recent checked+archived features in full detail.
   - Consolidate only older checked+archived features into a short `Completed (summarised)` section.
   - If there are no checked+archived features, skip todo compaction and state why.
4. Compact `tasks/memory.md` in place:
   - Preserve `Project` and `Current state` sections.
   - Keep the user-selected number of most recent detailed entries.
   - Before consolidating, extract any still-relevant risks, open questions, or gotchas from older entries into `Notes / gotchas` or `Current state: Blockers` so they are not lost.
   - Replace older entries with a concise historical summary block (themes, major outcomes, recurring risks).
5. Report results:
   - Show retained vs consolidated counts for both files.
   - Call out any sections intentionally left untouched.

---

## Suggested Defaults

Use these as initial recommendations, then ask the user to confirm or adjust:

- `tasks/todo.md`:
  - Keep all unchecked features.
  - Keep the latest 8 checked+archived features in detail.
  - Consolidate older checked+archived features into summary.
- `tasks/memory.md`:
  - Keep the latest 15 dated entries in detail across historical sections.
  - Consolidate older entries into summary.

---

## Prompt Format for Threshold Choice

Use a short choice prompt before edits:

```text
Proposed compact plan:
1) TODO detailed checked+archived items to keep: 8 (consolidate: 24)
2) Memory detailed entries to keep: 15 (consolidate: 41)

Reply with:
- "use defaults", or
- custom numbers (for example: "todo 12, memory 20"), or
- "less" / "more" and the target file.
```

---

## Summary Patterns

### `tasks/todo.md` completed-summary example

```markdown
### Completed (summarised)
- f-01 to f-14: Foundation and onboarding capabilities completed.
- f-15 to f-19: Reliability and bugfix pass completed.
```

### `tasks/memory.md` historical-summary example

```markdown
## Historical summary
- Earlier phase focused on onboarding, auth hardening, and export reliability.
- Main recurring risk was cross-feature dependency ordering; mitigated by stricter finalise discipline.
- Key tradeoff pattern: shipped simpler defaults first, then expanded configurability.
```

---

## Output

- Update only `tasks/todo.md` and/or `tasks/memory.md` as needed.
- Return:
  - proposed numbers and user-selected numbers
  - retained vs consolidated counts
  - concise summary of what changed
- End with a short status block:
  - **Files changed**: list of created/updated files
  - **Key decisions**: any assumptions or choices made (if any)
  - **Next step**: recommended next skill or action
