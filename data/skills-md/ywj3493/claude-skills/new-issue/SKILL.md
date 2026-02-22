---
name: new-issue
description: Creates a new numbered issue document in docs/issue/ following the project's standard issue format, and simultaneously creates the corresponding Korean translation in docs/dev/issue/. Use this whenever starting new work — features, bug fixes, tasks, or investigations. The user may say "create an issue", "new issue", "이슈 만들어줘", or simply describe work they want to start.
---

# new-issue

Creates a properly numbered, bilingual issue document for tracking a unit of work.

## When to Use

- User says "create an issue", "new issue", "start an issue", "이슈 만들기"
- Beginning a new feature, bug fix, investigation, or task
- User describes work that should be formally tracked

## Step-by-Step Instructions

### Step 1: Determine the Next Issue Number

Check what issue numbers already exist:

```bash
ls docs/issue/ 2>/dev/null | grep -E '^issue[0-9]+\.md$' | sort
```

Take the highest number found and add 1. If no issues exist yet, start at `001`.
Format as zero-padded 3 digits: `001`, `002`, ..., `099`, `100`, `101`, ...

### Step 2: Gather Issue Details

If the user has already described the work in their message, draft the issue
content from that description and **ask for confirmation** before writing.

Otherwise, ask the user for:

1. **Title** — one-line summary of the work
2. **Background** — why is this needed? what problem does it solve?
3. **Acceptance Criteria** — what does "done" look like?
4. **Initial Tasks** — what are the first known steps?

### Step 3: Create the English Issue Document

Create `docs/issue/issue<NNN>.md`:

```markdown
# Issue <NNN>: <Title>

**Status**: Open
**Created**: <YYYY-MM-DD>

## Background

<Why this work is needed and what problem it solves>

## Acceptance Criteria

- [ ] <Criterion 1>
- [ ] <Criterion 2>

## Tasks

- [ ] 1. <Task 1>
- [ ] 2. <Task 2>

## Notes

<!-- Record decisions, discoveries, and blockers here as work progresses -->
```

See `references/issue-template.md` for the raw template.

### Step 4: Create the Korean Mirror

Create `docs/dev/issue/issue<NNN>.ko.md` with the same structure in Korean.
Code blocks, file paths, commands, and technical identifiers remain in English.

```markdown
# 이슈 <NNN>: <한국어 제목>

**상태**: 열림
**생성일**: <YYYY-MM-DD>

## 배경

<이 작업이 필요한 이유와 해결하려는 문제>

## 완료 기준

- [ ] <기준 1>
- [ ] <기준 2>

## 작업 목록

- [ ] 1. <작업 1>
- [ ] 2. <작업 2>

## 참고 사항

<!-- 작업 진행 중 결정 사항, 발견 사항, 차단 사항을 여기에 기록하세요 -->
```

### Step 5: Confirm and Report

Tell the user:

> Created:
> - `docs/issue/issue<NNN>.md`
> - `docs/dev/issue/issue<NNN>.ko.md`
>
> Reference this issue in commit messages with `Refs: issue<NNN>`.

## Updating Issues During Work

As work progresses, keep the issue document current:

- Check off completed tasks: `- [x] 1. Task 1`
- Update **Status** from `Open` → `In Progress` → `Done`
- Record key decisions in the **Notes** section
- Update the Korean mirror when significant changes are made
