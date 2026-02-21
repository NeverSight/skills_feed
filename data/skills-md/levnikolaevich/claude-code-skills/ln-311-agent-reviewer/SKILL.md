---
name: ln-311-agent-reviewer
description: "Worker that runs parallel external agent reviews (Codex + Gemini) on Story/Tasks. Background tasks, process-as-arrive, critical verification with debate. Returns filtered suggestions for Story validation."
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Agent Reviewer (Story)

Runs parallel external agent reviews on validated Story and Tasks, critically verifies suggestions, returns editorial improvements.

## Purpose & Scope
- Worker in ln-310 validation pipeline (invoked in Phase 5)
- Run codex-review + gemini-review as background tasks in parallel
- Process results as they arrive (first-finished agent processed immediately)
- Critically verify each suggestion; debate with agent if Claude disagrees
- Return filtered, deduplicated, verified suggestions for Story/Tasks improvement
- Health check + prompt execution in single invocation

## When to Use
- **Invoked by ln-310-story-validator** Phase 5 (Agent Review)
- After Phase 4 auto-fixes applied, Penalty Points = 0
- Story and Tasks are in their final form before approval

## Inputs (from parent skill)
- `storyId`: Linear Story identifier (e.g., "PROJ-123")

## Workflow

**MANDATORY READ:** Load `shared/references/agent_delegation_pattern.md` for Reference Passing Pattern, Review Persistence Pattern, Agent Timeout Policy, and Debate Protocol (Challenge Round 1 + Follow-Up Round).

1) **Health check:** `python shared/agents/agent_runner.py --health-check`
   - Filter output by `skill_groups` containing "311"
   - If 0 agents available -> return `{verdict: "SKIPPED", reason: "no agents available"}`
   - Display: `"Agent Health: codex-review OK, gemini-review OK"` (or similar)

2) **Get references:** Call Linear MCP `get_issue(storyId)` -> extract URL + identifier. Call `list_issues(filter: {parent: {id: storyId}})` -> extract child Task URLs/identifiers.
   - If project stores tasks locally (e.g., `docs/tasks/`) -> use local file paths instead of Linear URLs.

3) **Ensure .agent-review/:**
   - If `.agent-review/` exists -> reuse as-is, do NOT recreate `.gitignore`
   - If `.agent-review/` does NOT exist -> create it + `.agent-review/.gitignore` (content: `*` + `!.gitignore`)
   - Create `.agent-review/{agent}/` subdirs only if they don't exist
   - Do NOT add `.agent-review/` to project root `.gitignore`

4) **Build prompt:** Read template `shared/agents/prompt_templates/story_review.md`.
   - Replace `{story_ref}` with `- Linear: {url}` or `- File: {path}`
   - Replace `{task_refs}` with bullet list: `- {identifier}: {url_or_path}` per task
   - Save to `.agent-review/{agent}/{identifier}_storyreview_prompt.md` (one copy per agent — identical content)

5) **Run agents (background, process-as-arrive):**

   a) Launch BOTH agents as background Bash tasks (run_in_background=true):
      - `python shared/agents/agent_runner.py --agent codex-review --prompt-file .agent-review/codex/{identifier}_storyreview_prompt.md --output-file .agent-review/codex/{identifier}_storyreview_result.md --cwd {cwd}`
      - `python shared/agents/agent_runner.py --agent gemini-review --prompt-file .agent-review/gemini/{identifier}_storyreview_prompt.md --output-file .agent-review/gemini/{identifier}_storyreview_result.md --cwd {cwd}`

   b) When first agent completes (background task notification):
      - Read its result file from `.agent-review/{agent}/{identifier}_storyreview_result.md`
      - Parse JSON between `<!-- AGENT_REVIEW_RESULT -->` / `<!-- END_AGENT_REVIEW_RESULT -->` markers
      - Parse `session_id` from runner JSON output; write `.agent-review/{agent}/{identifier}_session.json`: `{"agent": "...", "session_id": "...", "review_type": "storyreview", "created_at": "..."}`
      - Proceed to Step 6 (Critical Verification) for this agent's suggestions

   c) When second agent completes:
      - Read its result file, parse suggestions
      - Run Step 6 for second batch
      - Merge verified suggestions from both agents

   d) If an agent fails: log failure, continue with available results

6) **Critical Verification + Debate** (per Debate Protocol in `shared/references/agent_delegation_pattern.md`):

   For EACH suggestion from agent results:

   a) **Claude Evaluation:** Independently assess — is the issue real? Actionable? Conflicts with project patterns?

   b) **AGREE** → accept as-is. **DISAGREE/UNCERTAIN** → initiate challenge.

   c) **Challenge + Follow-Up (with session resume):** Follow Debate Protocol (Challenge Round 1 → Follow-Up Round if not resolved). Resume agent's review session for full context continuity:
      - Read `session_id` from `.agent-review/{agent}/{identifier}_session.json`
      - Run with `--resume-session {session_id}` — agent continues in same session, preserving file analysis and reasoning
      - If `session_resumed: false` in result → log warning, result still valid (stateless fallback)
      - `{review_type}` = "Story/Tasks"
      - Challenge files: `.agent-review/{agent}/{identifier}_storyreview_challenge_{N}_prompt.md` / `_result.md`
      - Follow-up files: `.agent-review/{agent}/{identifier}_storyreview_followup_{N}_prompt.md` / `_result.md`

   d) **Persist:** all challenge and follow-up prompts/results in `.agent-review/{agent}/`

7) **Aggregate + Return:** Collect ACCEPTED suggestions only (after verification + debate).
   Deduplicate by `(area, issue)` — keep higher confidence.
   **Filter:** `confidence >= 90` AND `impact_percent > 2`.
   **Return** JSON with suggestions + agent_stats + debate_log to parent skill. **NO cleanup/deletion.**

## Output Format

```yaml
verdict: STORY_ACCEPTABLE | SUGGESTIONS | SKIPPED
suggestions:
  - area: "security | performance | architecture | feasibility | best_practices | risk_analysis"
    issue: "What is wrong or could be improved"
    suggestion: "Specific change to Story or Tasks"
    confidence: 95
    impact_percent: 15
    source: "codex-review"
    resolution: "accepted | accepted_after_debate | accepted_after_followup | rejected"
agent_stats:
  - name: "codex-review"
    duration_s: 8.2
    suggestion_count: 2
    accepted_count: 1
    challenged_count: 1
    followup_count: 1
    status: "success | failed | timeout"
debate_log:
  - suggestion_summary: "Missing rate limiting on POST /api/users"
    agent: "codex-review"
    rounds:
      - round: 1
        claude_position: "Rate limiting exists in nginx config"
        agent_decision: "DEFEND"
        resolution: "follow_up"
      - round: 2
        claude_position: "Nginx config covers /api/* routes, agent cited only app-level"
        agent_decision: "MODIFY"
        resolution: "accepted_after_followup"
    final_resolution: "accepted_after_followup"
```

## Fallback Rules

| Condition | Action |
|-----------|--------|
| Both agents succeed | Aggregate verified suggestions from both |
| One agent fails | Use successful agent's verified suggestions, log failure |
| Both agents fail | Return `{verdict: "SKIPPED", reason: "agents failed"}` |
| Parent skill (ln-310) | Falls back to Self-Review (native Claude) |

## Verdict Escalation
- **No escalation.** Suggestions are editorial only — they modify Story/Tasks text.
- Parent skill (ln-310) Gate verdict remains unchanged by agent suggestions.

## Critical Rules
- Read-only review — agents must NOT modify project files (enforced by prompt CRITICAL CONSTRAINTS)
- Same prompt to all agents (identical input for fair comparison)
- JSON output schema required from agents (via `--json` / `--output-format json`)
- Log all attempts for user visibility (agent name, duration, suggestion count)
- **Persist** prompts, results, and challenge artifacts in `.agent-review/{agent}/` — do NOT delete
- Ensure `.agent-review/.gitignore` exists before creating files (only create if `.agent-review/` is new)
- **MANDATORY INVOCATION:** Parent skills MUST invoke this skill. Returns SKIPPED gracefully if agents unavailable. Parent must NOT pre-check and skip.
- **NO TIMEOUT KILL — WAIT FOR RESPONSE:** Do NOT kill agent background tasks. WAIT until agent completes and delivers its response — do NOT proceed without it, do NOT use TaskStop. Agents are instructed to respond within 10 minutes via prompt constraint, but the hard behavior is: wait for completion or crash. Only a hard crash (non-zero exit code, connection error) is treated as failure. TaskStop is FORBIDDEN for agent tasks.
- **CRITICAL VERIFICATION:** Do NOT trust agent suggestions blindly. Claude MUST independently verify each suggestion and debate if disagreeing. Accept only after verification.

## Definition of Done
- All available agents launched as background tasks (or gracefully failed with logged reason)
- Prompts persisted in `.agent-review/{agent}/` for each agent
- Raw results persisted in `.agent-review/{agent}/` (no cleanup)
- Each suggestion critically verified by Claude; challenges executed for disagreements
- Follow-up rounds executed for suggestions rejected after Round 1 (DEFEND+weak / MODIFY+disagree)
- Challenge and follow-up prompts/results persisted alongside review artifacts
- Accepted suggestions filtered by confidence >= 90 AND impact_percent > 2
- Deduplicated verified suggestions returned to parent skill with verdict, agent_stats, and debate_log
- `.agent-review/.gitignore` exists (created only if `.agent-review/` was new)
- Session files persisted in `.agent-review/{agent}/{identifier}_session.json` for debate resume

## Reference Files
- **Agent delegation pattern:** `shared/references/agent_delegation_pattern.md`
- **Prompt template (review):** `shared/agents/prompt_templates/story_review.md`
- **Prompt template (challenge):** `shared/agents/prompt_templates/challenge_review.md`
- **Agent registry:** `shared/agents/agent_registry.json`
- **Agent runner:** `shared/agents/agent_runner.py`
- **Challenge schema:** `shared/agents/schemas/challenge_review_schema.json`

---
**Version:** 2.0.0
**Last Updated:** 2026-02-11
