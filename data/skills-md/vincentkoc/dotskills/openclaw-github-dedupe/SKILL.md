---
name: openclaw-github-dedupe
description: Investigate a cluster of GitHub issues and PRs, determine canonical candidates, post duplicate/related status, preserve contributor credit, and execute cleanup actions (comments, closes, labels, changelog touchpoints).
license: AGPL-3.0-only
metadata:
  short-description: GitHub triage for issue/PR clusters and dedupe decisions
  source: "https://github.com/vincentkoc/dotskills"
---

# Issue/PR Cluster Deduper

Use this skill when a cluster of GitHub issues and pull requests has been reported for a common failure mode (Slack, iMessage, support threads, or manual list), and you need an evidence-based dedupe recommendation or execution.

## Purpose

Provide a consistent, evidence-driven triage pass for issue and PR clusters so duplicate work is folded, contributor credit is preserved, and cleanup actions stay auditable.

Execution is command-led and conservative: drive decisions from `gh` readbacks plus deterministic file/metadata checks only, and avoid speculative local analysis beyond triage logic.

Primary goal: make every run action-ready with explicit per-item actions, links, and command outcomes.

## Vision

Treat each cluster as a triage system, not a documentation exercise. The expected behavior is deterministic classification, auditable comment text, safe mutation flow, and fast operator comprehension.

## Principles (read before execution)

These are defined in `principles.md`:

- Evidence over narrative
- Root-cause alignment over title similarity
- Credit-preserving attribution
- Safe defaults (`dry-run` and blockers)
- Complete audit trail in comments and labels
- Humans first: communicate like a senior developer advocate, not a script.

Read `constitution.md` for governance requirements and decision quality rules before choosing final outcomes.

## Operator experience and communication defaults

This workflow is designed for high-velocity maintainers and external contributors:

- Keep every reply short, clear, and respectful.
- Lead with what happened, then why.
- Include a plain-English next step and reopen path.
- Avoid abrupt or accusatory language, especially on duplicates.
- Never hide uncertainty; if blocked, say what is missing and what you need next.
- Treat the assistant as a Developer Experience lead: helpful, practical, and direct without sounding mechanical.
- Use examples as style guidance, not templates to paste verbatim.
- Vary sentence ordering and opener lines per message so repeated runs do not sound identical.
- Do not repeat the exact same message body twice in one cluster run unless no safe variation is possible.
- Use short, conversational paragraphs (2-4 paragraphs), and avoid one-liner robotic templates.
- If intent is clear, keep tone warm and explanatory even when issuing a close.

## When to use

- You have a cluster of suspected duplicates to classify as canonical/related/independent.
- You need a concrete action plan with exact statuses instead of generic commentary.
- The user asked to execute safe closure/label/comment steps.
- You need to avoid duplicate PR churn by identifying which change should stay canonical.

## Inputs

- `cluster_refs` (required): list of issue/PR references as IDs or URLs.
- `mode` (optional): `plan` (default) or `execute`.
- `channel` (optional): source context like `slack`, `imessage`, `support`, etc.
- `repo` (optional): explicit `owner/repo` when not using current checkout.
- `canonical_hint` (optional): explicit preference when ambiguity exists.
- `merge_guard` (optional): `high|medium` mergeability strictness; default `high`.
- `max_changed_files_for_canonical` (optional): default `30`.
- `max_delta_lines_for_canonical` (optional): default `2500`.
- `min_greptile_score` (optional): default `65` when available.
- `body_noise_mode` (optional): `strict|medium` for junk body tolerance; default `medium`.
- `reuse_copy_detection` (optional): `off|on` with default `on` for bot/copied-work checks.
- `bot_author_pattern` (optional): list of substrings for suspicious authors.
- `merge_tool_pref` (optional): `auto`, `gh`, `merge-skill`, or `land-skill`; default `auto`.
- `dry_run` (optional): `0|1` to force non-mutating mode.
- `output_mode` (optional): `compact|detailed`; default `detailed`.
- `triage_report` (optional): path to a triage report file (like `/Users/vincentkoc/Desktop/triage_report.md`) to seed initial cluster candidates.
- `search_limit` (optional): max similar items per item from GH search; default `12`.
- `search_queries` (optional): explicit query terms (space-separated).

## Outputs

- Per-item action matrix with explicit status (`KEEP_OPEN_CANONICAL`, `CLOSE_DUPLICATE`, `KEEP_OPEN_RELATED`, `KEEP_OPEN_UNRELATED`, `MANUAL_REVIEW_REQUIRED`) and each row showing title + author.
- Evidence matrix with root-cause mapping, scope deltas, and risk blockers.
- Credit chain and attribution rationale (single-credit default, dual-credit only by exception).
- Required command set (dry-run and execution mode): close, comment, label, merge, and changelog actions.
- Escalation list for `manual-review-required` outcomes, with confidence score and hard-stop reason.

## Sub-agent orchestration

Use sub-agents in this chain for higher consistency and lower mistakes:

- `agents/cluster-intake-agent.md`
- `agents/cluster-similarity-agent.md`
- `agents/cluster-evidence-agent.md`
- `agents/cluster-decision-agent.md`
- `agents/cluster-synthesis-agent.md`

Run in sequence and feed each output to the next.

- Intake → Similarity → Evidence → Decision → Synthesis.

1. Intake: normalize cluster refs (required first), including optional `triage_report` expansion.
2. Similarity: find additional related open issues/PRs from GitHub search and attach ranked candidates.
3. Evidence: pull full context for cluster + similar candidates.
4. Decision: maps risk and hard-stop states.
5. Synthesis: emits final action matrix and command plan.

If any sub-agent blocks, continue only with explicit `manual-review-required` and keep execution safe.

When orchestrator support exists, run them as a chain and pass structured outputs between steps:

- Start with `cluster-intake-agent`
- Feed output to `cluster-similarity-agent`
- Feed output to `cluster-evidence-agent`
- Feed output to `cluster-decision-agent`
- Feed output to `cluster-synthesis-agent`

If sub-agents are unavailable, execute the same steps manually in this file order and keep output format intact.

## Execution discipline for consistent tool UIs

Use `update_plan` at runtime and keep one in-progress step at a time.

- `Discover` → `Assess` → `Plan` → `Execute` (if requested) → `Verify`.
- Convert each stage between `in_progress` and `completed`.
- If hard-stop blockers exist, keep `Execute` as `pending` and return `manual-review-required`.
- This keeps Codex/Cursor/Claude execution format consistent.

## Workflow

1. Cluster intake and normalization
   - Resolve each input to canonical links and types.
   - Skip malformed entries with a reasoned note for `manual-review-required`.

2. Similarity sweep (required)
   - Use the supplied `cluster-intake-agent` summary as the primary seed.
   - Expand search surface by running GitHub queries for additional candidates and include likely neighbors in the same root-cause family.
   - Pull:
     - `gh issue list --search "<query> in:title" --state all --repo <repo> --json number,title,url,state,author,updatedAt,labels`
     - `gh pr list --search "<query> in:title" --state all --repo <repo> --json number,title,url,state,author,updatedAt,isDraft,mergeable`
   - Keep likely matches when title/body overlap is explicit, not keyword-only.

3. Fetch evidence from GitHub
   - For PRs: `gh pr view <ref> --json number,title,body,state,author,labels,createdAt,updatedAt,mergedAt,closedAt,mergeable,mergeStateStatus,isDraft,changedFiles,additions,deletions,statusCheckRollup,commits,url`
   - For issues: `gh issue view <ref> --json number,title,body,state,labels,author,createdAt,updatedAt,url,comments`
   - Pull file footprint for PRs when deciding canonical scope: `gh pr diff <ref> --name-only`
   - Pull check state for PRs: `gh pr checks <ref>`
   - Pull review/AI-tool signal text: `gh issue view <ref> --json comments`

3. Normalize guardrails
   - Mergeability: mergeable flag, merge-state blockers, draft state, check rollup status.
   - Churn: `changedFiles`, `additions`, `deletions`.
   - Body hygiene: concrete root-cause detail vs template/placeholder-only text.
   - AI-review score: Greptile-like comments below threshold downgrade confidence.
   - Copy/bot signal: generated/copied language, bot-like authors, low-evidence mechanical commits.
   - Any hard-stop issue marks item `manual-review-required` and blocks automatic close.

4. Review candidate canonicals
   - For each top candidate PR: `gh pr view <id> --json files` and `gh pr diff <id>`.
   - If healthy, treat as canonical candidate and move toward merge prep.
   - If two candidates are equivalent, prefer stable, lower-risk scope.
   - If a newer PR is superset-safe, prefer the newer with higher-surface fix coverage.

5. Decide outcomes
   - Canonical issue/PR: keep open.
   - Duplicate PR/issue: close with explicit comment and reasoned message.
   - Related not duplicate: keep open and mark relationship.
   - Unrelated: split into a separate cluster/routing note.
   - For any hard-stop failure: keep `manual-review-required` with explicit blockers.

6. Merge and changelog follow-up
   - If execute + winning PR is green:
     - prefer merge/land helper when available
     - fallback: `gh pr merge <id> --auto --merge` (or repo policy `--squash` / `--rebase`)
     - rerun check discovery and report final state
   - If changelog is needed, add only once under Unreleased `### Fixes` and do not duplicate existing entries.
   - If changelog cannot be added before merge, create a follow-up squash commit only if required by repo policy.

7. Emit outcomes
   - In `plan` mode: only draft comments, labels, close commands, and blockers.
   - In `execute` mode: run only safe GH mutations after all guardrails pass.
   - Return final output using the required format below.

8. Review for governance drift
   - Check `AGENTS.md` and `CONTRIBUTING.md` for scope changes or repo policy changes.
   - Validate that output keeps explicit credit references and concise issue/PR references.

## Governance and anti-drift checks

- If the repo has a higher-priority instruction source (project-specific AGENTS/CONTRIBUTING), that source wins over this skill's defaults.
- Keep close reasons and comments compliant with repository conventions.
- Never ignore required validation gates.

## Required final output format

### Cluster summary (compact)
- Canonical PR: `<url-or-id or none>`
- Canonical issue: `<url-or-id or none>`
- Merge gate: `<ready|blocked|merged>`
- Credit chain: `<foundational work ref(s) + final fix ref>` (default 1 credited contributor in 95%+ cases; max 2 only by explicit exception)
- Dry run: `<on|off>`

### Per-item action matrix (required)
Render this as a table:

| item | action | title | author | artifact | rationale | target |
|---|---|---|---|---|---|---|
| `pr:xxxxx` | `KEEP_OPEN_CANONICAL` | `Streaming recipient-id root-cause fix` | `@canonical_author` | `https://github.com/openclaw/openclaw/pull/xxxxx` | `canonical remediation path` | `-` |
| `issue:yyyyy` | `CLOSE_DUPLICATE` | `Slack stream stop race condition` | `@duplicate_author` | `https://github.com/openclaw/openclaw/issues/yyyyy` | `covered by canonical PR` | `#zzzzz` |
| `issue:aaaaa` | `KEEP_OPEN_RELATED` | `Block-mode emission behavior mismatch` | `@related_author` | `https://github.com/openclaw/openclaw/issues/aaaaa` | `adjacent area: block-path semantics` | `-` |

Required matrix fields: item, action, title, author, artifact link, short rationale, and canonical target/duplicate mapping target where applicable.

### Command/result block (required)
Render command outcomes as a table:

| status | command | state |
|---|---|---|
| `planned`/`executed`/`blocked` | `gh issue view ...` | `passed` / `applied` / `blocked by checks` |

Include exact command text and resulting state for each operation.

### Evidence matrix (required)
Render evidence per item as a table:

| item | title | author | root-cause marker | scope delta | merge risk | confidence |
|---|---|---|---|---|---|---|
| `pr:xxxxx` | `Streaming recipient-id root-cause fix` | `@canonical_author` | `recipient IDs + stream pipeline` | `touches stream API + block pipeline` | `low` | `high` |

Blockers must be explicit.

### Credit and closure rationale block (required)
- Explicit credit chain for all merged/closed outcomes with default one credited contributor in 95%+ cases; max two only by explicit exception.
  - Rule: default one credited contributor (target 95%+ of cases), two only when the earlier PR is non-mergeable and the later PR is a direct, clean continuation.
- Canonical/related boundary rationale for each non-canonical item.
- Include the exact customer-facing message body (or template) for each comment-close action, using the communication defaults above.

### Escalations
- List unresolved blockers and uncertainty with `manual-review-required` if any.
- Include confidence per item (`high|med|low`) and hard-stop reason.

## Message templates

### Message behavior contract

Use template intent only; do not replay exact wording across issues/PRs.

- Start with context acknowledgment.
- Explain keep/close decision in plain terms.
- State why this is the chosen path.
- Include a direct reopen path when uncertainty remains.
- End with one clear next action.

Prefer sentence variation over strict block copying. Keep grammar natural and avoid repetitive phrasing.

### Canonical PR credit line
Style rule: use the intent below, then vary wording naturally for each message. Do not output a single fixed text.

`Great progress here.

The final fix is in #<canonical_pr> by @<canonical_author>.
This is the version we're keeping because it is the most stable and complete path.

If you think there's a gap, tell me and I'll reopen review right away.`

Default single-credit template:
`Thanks for the earlier contribution.

The final fix is in #<canonical_pr> by @<canonical_author>.
Your earlier contribution is preserved in the canonical history.

If this looks off, tell me and I can reopen review right away.`

Exceptional dual-credit template:
`I appreciate the earlier pass.

The final fix is in #<canonical_pr> by @<canonical_author> and @<foundational_author>.
The earlier path in #<prior_pr> built strong groundwork, and the later PR completed a merge-safe continuation.

If this needs correction, tell me and I can re-check credit and closure right away.`

### Close duplicate PR
`Thanks for the earlier contribution.

I'm going to close this as a duplicate of #<canonical_pr>.
Great attempt here, but this PR is stale and a newer, stable PR is handling the same root-cause path.
Your work is preserved in the canonical attribution trail.

If this is a mistake, tell me and I can reopen review right away.`

Single-credit close template:
`I appreciate you pushing this.

I'm going to close this as a duplicate of #<canonical_pr>.
This was an earlier step, and the newer canonical fix now includes the covered scope.

If this feels wrong, tell me and I can reopen review right away.`

Exceptional dual-credit close template:
`Thank you for taking this on.

I'm going to close this as a duplicate of #<canonical_pr>.
#<prior_pr> created the initial path, and the later PR carried it into a merge-safe continuation.
Both contributions are retained in the canonical credit trail.

If this is a mistake, tell me and I can reopen review right away.`

### Keep canonical issue open
`Keeping this open as canonical for this cluster.

This appears to be the shared issue shape for the channel cluster we are solving.

If this should be reassigned, tell me what you're seeing and I'll reassess the boundary.`

### Close duplicate issue
`Thanks for the report.

I'm closing this as duplicate of #<canonical>.
The same failure pattern and behavior map to the canonical fix path there.

If this is a mistake, tell me and I can reopen review right away.`

### Related / not duplicate
`Good call raising this.

This appears related, but this is not a duplicate. It diverges at {reason}, so it stays as a separate track.

If this feels like a miss, tell me and I can re-check it quickly.`

### Unrelated
`Thanks for flagging this.

This appears separate from this cluster and will stay in its own thread.

If this looks related, point to the shared failure step and I can rerun dedupe right away.`

### Variation examples
Use a starter bank (never replay the same opener twice in one run):

`Great call on this one.

I’m closing this as a duplicate of #xxxxx. The same failure pattern is now covered in the canonical fix, and this path is fully superseded there.

Your earlier work is still part of the attribution trail. If this is a miss, tell me what changed and I can reopen review right away.`

`Nice work surfacing this with clear context.

I reviewed the overlap and confirmed the final fix is in #xxxxx by @canonical_author. We’re keeping that one because it has the most complete root-cause coverage.

If this looks off in your repro, tell me and I can re-check the boundary quickly.`

`Thanks for pushing this.

This appears related, not a duplicate. It diverges at `{reason}` and belongs in a separate track for now.

If you think that boundary is wrong, point me to the shared failure step and I’ll reassess it right away.`

`I appreciate the early pass here.

I’m treating #xxxxx as canonical because it is the safest and most complete path for this cluster.

If I should rerun this split, share the exact overlap and I can do that immediately.`

## Messaging examples by situation

### Situation 1: clean duplicate, single-credit result
- Canonical: `pr:xxxxx` by `@canonical_author`
- Duplicate: `issue:yyyyy` by `@first_author`, `issue:zzzzz` by `@second_author`
- Required behavior:
  - One credited canonical author only (target 95%+ of cases).
  - Duplicate closure uses single-credit close templates.
  - Related notes include a specific divergence reason.

### Situation 2: earlier PR non-mergeable, direct follow-up continuation, dual-credit
- Canonical: `pr:xxxxx`
- Earlier groundwork: `pr:yyyyy` (not mergeable, direct continuation proven by diff overlap and clean follow-up checks)
- Required behavior:
  - Dual-credit templates are used.
- Rationale statement must include:
  - non-mergeability reason for the first PR,
  - why the second PR is a direct continuation,
  - why test/conflict risk remains clean.

### Situation 3: related but not duplicate
- Example outcome: `KEEP_OPEN_RELATED`.
- Message must use the related template with explicit `{reason}` describing vector divergence.

## Action commands

> Run commands from repo checkout unless explicitly using full `owner/repo` URLs.

### Add labels for closed duplicates
- PR/issue duplicate: `gh issue edit <id> --add-label dedupe:child --add-label close:duplicate`
- Canonical issue: `gh issue edit <canonical_id> --add-label dedupe:parent`

### Close with comment (issues)
- Comment first, then close:
  - `gh issue comment <id> --body "..."`
  - `gh issue close <id> --reason not planned`

### Close PR
- `gh pr close <id> --comment "..."` (preferred with canonical close message).

### Merge helpers
- `gh pr merge <id> --merge --auto`
- `gh pr merge <id> --squash --auto`
- `gh pr merge <id> --rebase --auto`

### Guardrail checks
- `gh pr view <id> --json mergeable,mergeStateStatus,isDraft,statusCheckRollup`
- `gh pr view <id> --json changedFiles,additions,deletions`
- `gh issue view <id> --json comments`

## scripts/alias.sh helper

Run the helper from this skill directory for batch-driven dedupe actions:

`./scripts/alias.sh run-cluster /path/to/cluster.txt`

`./scripts/alias.sh --dry-run run-cluster /path/to/cluster.txt`

Supported cluster format:

`<type>:<id>|<action>|<target>`

Supported actions:
- `inspect`
- `close-pr-duplicate`
- `close-issue-duplicate`
- `noop`

Example:

```text
pr:xxxxx|inspect|
pr:yyyyy|close-pr-duplicate|xxxxx
issue:bbbbb|close-issue-duplicate|aaaaa
issue:ccccc|noop|
```

Use placeholder IDs in examples only:

`pr:xxxxx|inspect|`

Prefer using `scripts/cluster-example.txt` as your starting template for reusable cluster runs.

## Git cleanup option

- Remove stale branch: `git branch -D <branch>`
- Remove remote branch: `git push origin --delete <branch>`

## Safety / anti-patterns

- Do not classify duplicates from metadata alone; inspect body and diff semantics.
- Do not use invalid GH issue-close reasons (for example `--reason duplicate`).
- Preserve source attribution when duplicate actions are taken.
- Never auto-close when hard-stop guardrails fail.
- Do not merge or close items while mergeability/churn/AI-review blockers are unresolved.
