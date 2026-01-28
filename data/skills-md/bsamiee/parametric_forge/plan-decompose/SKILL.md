---
name: plan-decompose
type: simple
depth: extended
description: >-
  Extracts work units from plan artifacts and creates sequenced GitHub issues.
  Use when (1) decomposing plan.md into actionable issues, (2) creating issues
  with validation checklists, (3) linking issue dependencies, or (4) executing
  after /plan command completion.
---

# [H1][PLAN-DECOMPOSE]
>**Dictum:** *Work units become issues; issues enable parallel agent execution.*

<br>

Decompose plan into GitHub issues via work unit extraction.

**Workflow:**
1. §PARSE — Extract work units from plan
2. §VALIDATE — Verify labels exist, check structure
3. §CREATE — Create issues in dependency order
4. §LINK — Add blocker references to dependent issues

**Dependencies:**
- `github-tools` — Issue creation via gh CLI
- `plan.md` — Input with Work Units section

**Input:**
- `Plan`: Path to plan artifact with Work Units section

---
## [1][PARSE]
>**Dictum:** *Accurate issues require complete context extraction.*

<br>

Extract from plan:

| [INDEX] | [SECTION]  | [EXTRACT]                                                    |
| :-----: | ---------- | ------------------------------------------------------------ |
|   [1]   | Context    | Plan title, summary                                          |
|   [2]   | Approach   | Selected approach for reference                              |
|   [3]   | Phases     | Task details for embedding                                   |
|   [4]   | Work Units | WU-N blocks with scope, tasks, priority, depends, validation |

**Work Unit Structure:**
```
### [N.M][WU_M]: [Name]
| [INDEX] | [KEY]    | [VALUE]   |
| :-----: | -------- | --------- |
|   [1]   | Scope    | ...       |
|   [2]   | Tasks    | N.X, N.Y  |
|   [3]   | Priority | ...       |
|   [4]   | Depends  | WU-M or — |

[VERIFY]:
- [ ] check 1
- [ ] check 2
```

[IMPORTANT]:
- [ALWAYS] Parse ALL work units before creating any issues.
- [ALWAYS] Extract task details for embedding in issue body.
- [NEVER] Proceed if Work Units section missing.

---
## [2][VALIDATE]
>**Dictum:** *Failed operations waste agent cycles.*

<br>

### [2.1][VALIDATE_LABELS]

Fetch available labels via github-tools:
```bash
uv run .claude/skills/github-tools/scripts/gh.py label-list
```

Verify labels exist:
- `task` — agentic category
- `triage` — initial status
- Priority labels: `critical`, `high`, `medium`, `low`

[IMPORTANT] If priority label missing, fall back to `task,triage` only.

### [2.2][VALIDATE_STRUCTURE]

| [INDEX] | [CHECK]    | [REQUIREMENT]                |
| :-----: | ---------- | ---------------------------- |
|   [1]   | Work Units | At least 1 WU-N block        |
|   [2]   | Scope      | Non-empty per work unit      |
|   [3]   | Tasks      | Reference valid task numbers |
|   [4]   | Validation | At least typecheck + lint    |

[CRITICAL] Abort if structure invalid—report missing elements.

---
## [3][CREATE]
>**Dictum:** *Dependency tracking requires creation order.*

<br>

Create issues in dependency order (WU-1 before WU-2 if WU-2 depends on WU-1).

**Per Work Unit:**

### [3.1][BUILD_TITLE]

```
[TASK]: [Work unit descriptive name]
```

### [3.2][BUILD_LABELS]

```
task,triage,[priority]
```

### [3.3][BUILD_BODY]

```markdown
## [1][WORK_UNIT]: [Name]

**Plan:** [Plan title]

---
## [2][SCOPE]

[File/module area from work unit]

---
## [3][TASKS]

### [3.1][TASK_N_X]

| [INDEX] | [KEY]  | [VALUE]           |
| :-----: | ------ | ----------------- |
|   [1]   | Target | `path/to/file.ts` |
|   [2]   | Action | [Specific change] |

[Repeat for each task in work unit]

---
## [4][DEPENDENCIES]

[None OR Blocked by: #[prior issue numbers]]

---
## [5][VALIDATION]

[VERIFY]:
[Copied from work unit validation section]

---
## [6][PR_WORKFLOW]

**Branch:** `feat/[issue-number]-[slug]`

[EXECUTE]:
1. [ ] Create branch: `git checkout -b feat/[issue-number]-[slug]`
2. [ ] Implement all tasks in §TASKS
3. [ ] Run validation checks in §VALIDATION
4. [ ] Commit changes with message referencing issue
5. [ ] Push branch: `git push -u origin feat/[issue-number]-[slug]`
6. [ ] Create PR: `gh pr create --title "[TASK]: [name]"` (uses `.github/PULL_REQUEST_TEMPLATE.md`)
7. [ ] Add `Closes #[issue-number]` to PR summary section

---
## [7][COMPLETION]

[VERIFY]:
- [ ] All tasks implemented
- [ ] `nx run-many -t typecheck` — zero errors
- [ ] `nx run-many -t check` — zero Biome violations
- [ ] `pnpm sonar` — no new code smells/issues
- [ ] PR created and linked to issue
```

### [3.4][CREATE_ISSUE]

```bash
uv run .claude/skills/github-tools/scripts/gh.py issue-create \
  --title "[TASK]: [name]" \
  --body "[body]"
```

Then add labels:
```bash
uv run .claude/skills/github-tools/scripts/gh.py issue-edit \
  --number [N] \
  --labels "task,triage,[priority]"
```

**Track mapping:** `{WU-N: issue_number}`

[CRITICAL]:
- [ALWAYS] Create in dependency order.
- [ALWAYS] Track WU → issue number mapping.
- [ALWAYS] Wait for creation success before next issue.

---
## [4][LINK]
>**Dictum:** *Workflow sequencing requires explicit blockers.*

<br>

After all issues created, update dependent issues with blocker references.

**For each issue with dependencies:**

1. Look up prior issue numbers from mapping
2. Edit issue body to include: `Blocked by: #[N], #[M]`

```bash
uv run .claude/skills/github-tools/scripts/gh.py issue-edit \
  --number [dependent_issue] \
  --body "[updated body with blocker refs]"
```

[IMPORTANT] Blocker format: `Blocked by: #42, #43`

---
## [5][OUTPUT]
>**Dictum:** *Verification confirms successful decomposition.*

<br>

Return creation summary:
```markdown
## [1][DECOMPOSITION_COMPLETE]

| [INDEX] | [WORK_UNIT] | [ISSUE] | [TITLE] | [PRIORITY] | [DEPENDS] |
| :-----: | ----------- | ------- | ------- | ---------- | --------- |
|   [1]   | WU-1        | #42     | [name]  | high       | —         |
|   [2]   | WU-2        | #43     | [name]  | medium     | #42       |
|   [3]   | WU-3        | #44     | [name]  | medium     | #42, #43  |

**Total:** N issues created<br>
**Plan:** [plan title]
```

---
## [6][VALIDATION]
>**Dictum:** *Incomplete execution corrupts downstream workflow.*

<br>

[VERIFY]:
- [ ] Parse: All work units extracted
- [ ] Validate: Labels verified, structure valid
- [ ] Create: Issues created in order
- [ ] Link: Dependencies added to issue bodies
- [ ] Output: Summary table returned

---
## [7][CONSTRAINTS]

[CRITICAL]:
- [ALWAYS] Parse before create—never stream.
- [ALWAYS] Create in dependency order.
- [ALWAYS] Track WU → issue mapping.
- [ALWAYS] Include validation checklist in every issue.
- [ALWAYS] Include PR_WORKFLOW section in every issue.
- [ALWAYS] Use `[TASK]:` prefix for titles.
- [NEVER] Create issues without Work Units section.
- [NEVER] Skip dependency linking.
- [NEVER] Hardcode labels—verify they exist first.
