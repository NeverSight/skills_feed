---
name: spec-to-issue
description: |
  Create GitHub Issue from spec documents — Auto-generate structured Feature Issues from specifications.

  Analyzes spec documents (requirement.md, design.md, tasks.md) in .specs/{feature}/ and
  generates a structured Feature Issue via gh issue create.
  Best used with specs created by spec-generator.

  English triggers:
  - "Create issue from spec", "Register spec as issue"
  - "Convert spec to GitHub issue", "Publish spec to issue"
  - After spec-generator: "Turn this into an issue"

  日本語トリガー:
  - 「仕様書をIssueにして」「Issueに登録して」「specからIssue作成」
  - 「仕様書からIssue生成」「specをIssueに変換」
  - spec-generator完了後に「これをIssueにして」「Issueにして」
license: MIT
---

# spec-to-issue — Spec to GitHub Issue

Auto-generate GitHub Issues from spec directories (`.specs/{feature}/`).

## Language Rules

1. **Auto-detect input language** → output in the same language
2. Japanese input → Japanese issue, use `references/issue-template.ja.md` as template reference
3. English input → English issue, use `references/issue-template.md` as template reference
4. Explicit override takes priority

**Reference file selection**: Based on the detected output language, use the corresponding template:
- English → `references/issue-template.md`
- Japanese → `references/issue-template.ja.md`

## Execution Flow

### 1. Locate Spec Directory

**With argument**: `spec-to-issue auth-feature` → use `.specs/auth-feature/`

**Without argument**: Scan `.specs/` and present a list → ask user to select

```
Spec directories found in .specs/:
1. auth-feature (requirement.md, design.md, tasks.md)
2. member-management (requirement.md, tasks.md)
Which spec do you want to create an issue from?
```

### 2. File Validation

Required: `requirement.md` must exist. Otherwise, exit with error.
Recommended: `tasks.md` (if missing, generate a basic checklist)
Optional: `design.md` (used as supplementary info if present)

### 3. Spec Analysis

Extract from each file:

**requirement.md:**
- Title: First `# ` line, strip suffixes like "Requirements", "要件定義書"
- Overview: `## Overview` or `## 概要` section
- Key features: Sections starting with `### 1.`, `### 2.`, etc.
- Tech stack: `## Technology Stack` or `## 技術要件` section

**tasks.md:**
- Phases: Lines starting with `## Phase` or `## フェーズ`
- Tasks: `### ` headings within each phase, simplified for checklist
- Done criteria: `## Definition of Done` or `## 完了の定義` section
- Notes: `## Notes` or `## 注意事項` section

**design.md (optional):**
- Architecture overview (as supplementary info)

### 4. Resolve Project Settings

Determine defaults in this priority order:

```
Command arguments > .specs/.config.yml > CLAUDE.md > Built-in defaults
```

**From CLAUDE.md:**
- Branch name: PR target branch from Git Workflow section → `--branch` default
- GitHub Organization: Inferred from repository URL

**.specs/.config.yml (optional):**
```yaml
default-branch: develop
default-labels: [feature, spec-generated]
project-number: 7
assignee: username
```

### 5. Compose Issue Body

See template details in the appropriate reference file (based on Language Rules):
- English: [references/issue-template.md](references/issue-template.md)
- Japanese: [references/issue-template.ja.md](references/issue-template.ja.md)

### 6. Create Issue

**Without --preview (default)**: Show a brief summary and execute `gh issue create`

```
Creating Issue:
  Title: [Feature] Member Management
  Labels: feature, spec-generated
  Phases: 3
  Tasks: 12
→ Running gh issue create...
Issue #42 created: https://github.com/org/repo/issues/42
```

**With --preview**: Display the full issue body, confirm, then execute

### 7. Additional Actions (optional)

- `--label`: Apply specified labels
- `--project`: Add to GitHub Project board via `gh project item-add`
- `--assignee`: Set assignee

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--preview` | Display issue body for confirmation | OFF |
| `--label <labels>` | Comma-separated labels | `.config.yml` value or none |
| `--project <number>` | Add to GitHub Project | `.config.yml` value or none |
| `--branch <name>` | Base branch for spec links | CLAUDE.md or `main` |
| `--assignee <user>` | Set assignee | `.config.yml` value or none |

## Integration with spec-generator

After spec-generator's `full` phase completes, suggest:

```
All three spec documents have been generated.
→ Create a GitHub Issue from them? (Y/n)
```

If yes, run spec-to-issue on the same directory.

## Error Handling

| Situation | Response |
|-----------|----------|
| `.specs/` does not exist | Error: Spec directory not found |
| `requirement.md` missing | Error: requirement.md is required |
| `tasks.md` missing | Warning: Use basic checklist as fallback |
| `gh` CLI not authenticated | Error: Guide user to `gh auth login` |
| Section not found | Use default value, show warning |

## Usage Examples

```
# With argument
/spec-to-issue auth-feature

# Auto-detect and select
/spec-to-issue

# With preview
/spec-to-issue auth-feature --preview

# With labels and Project
/spec-to-issue auth-feature --label "feature,priority:high" --project 7

# After spec-generator
"Create full spec for todo-app" → done → "Turn this into an issue"

# Japanese
「仕様書を全部作って」→ 完了 →「これをIssueにして」
```
