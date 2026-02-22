---
name: forge-status
description: >
  Displays the FORGE sprint status: stories, metrics, progress.
  Usage: /forge-status
---

# /forge-status — FORGE Sprint Status

Displays the current sprint status by reading `.forge/sprint-status.yaml`.

## French Language Rule

All content generated in French MUST use proper accents (é, è, ê, à, ù, ç, ô, î, etc.), follow French grammar rules (agreements, conjugations), and use correct spelling.

## Workflow

1. Read `.forge/sprint-status.yaml`
2. Display a summary table:
   - Stories by status (completed, in_progress, pending, blocked)
   - Metrics (points, velocity, test coverage)
   - Current blockers
   - Recent history
3. Identify the next story to work on (first unblocked `pending` story)
4. Suggest the next action (`/forge-build STORY-XXX`)
5. **Backlog section**: List all story files in `docs/stories/` and compare with stories in the sprint. Display stories NOT in the current sprint as "Backlog" with their ID and title (read from the story file's front matter or first heading). This gives visibility on upcoming work outside the sprint.
