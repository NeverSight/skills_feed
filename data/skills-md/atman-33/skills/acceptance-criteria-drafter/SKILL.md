---
name: acceptance-criteria-drafter
description: Creates a draft of Acceptance Criteria for GitHub Issues by interviewing the user about feature requirements and outputting a markdown file in .tmp folder. Triggers on phrases like 'create AC draft', 'draft acceptance criteria', 'write acceptance criteria', or when user wants to define acceptance conditions for a feature.
metadata:
  short-description: Draft Acceptance Criteria for GitHub Issues
---

# Acceptance Criteria Drafter

This skill helps you create well-structured Acceptance Criteria drafts for GitHub Issues by interviewing users about their feature requirements.

## What This Skill Does

1. Interviews the user to understand the feature/requirement
2. Generates Acceptance Criteria following best practices
3. Outputs a markdown draft file to `.tmp/` folder for review and refinement

## Interview Questions

Ask the user these essential questions:

1. **Feature Overview**: What feature or change are you planning?
2. **User Perspective**: Who is the user and what do they want to achieve?
3. **Success Conditions**: How do you know when this is complete?
4. **Edge Cases**: Are there any error conditions or special cases to handle?

Keep the interview conversational and adaptive—you don't need to ask all questions if the user has already provided the information.

## Acceptance Criteria Guidelines

### Core Principles (3-Rule Minimum)

1. **User-oriented**: Write from the user's perspective, not implementation details
2. **Verifiable**: Each criterion must be clearly testable (satisfied / not satisfied)
3. **Concise**: Keep it to 3-5 bullet points in checkbox format

### What to Include

✅ User behavior and outcomes
✅ Error conditions and messages
✅ State changes visible to users
✅ Data persistence requirements

### What to Avoid

❌ Implementation details (API endpoints, database tables)
❌ Technical architecture decisions
❌ Browser/device-specific test cases
❌ More than 5 criteria (split into multiple issues if needed)

## Output Format

Create a file in `.tmp/ac-draft-YYYYMMDD-N.md` with this structure:

```markdown
# Acceptance Criteria Draft

**Generated on**: YYYY-MM-DD
**Feature**: [Brief feature description]

---

## Acceptance Criteria

- [ ] [User-facing behavior 1]
- [ ] [User-facing behavior 2]
- [ ] [Error handling or edge case]
- [ ] [State persistence or data requirement]

---

## Notes

[Any additional context, assumptions, or clarifications]

---

## Next Steps

1. Review and refine this draft
2. Copy to GitHub Issue template
3. Discuss with team during sprint planning
```

## Examples

### Example 1: User Article Posting

```markdown
## Acceptance Criteria

- [ ] ログイン済みユーザーは記事を投稿できる
- [ ] タイトルが未入力の場合、投稿できずエラーメッセージが表示される
- [ ] 投稿後、記事一覧に表示される
```

### Example 2: Notification Settings

```markdown
## Acceptance Criteria

- [ ] 通知をOFFにすると通知が送信されない
- [ ] 設定変更後もページ再読み込みで状態が保持される
```

### Example 3: Data Export Feature

```markdown
## Acceptance Criteria

- [ ] ユーザーは自分のデータをCSV形式でエクスポートできる
- [ ] データが存在しない場合、「データがありません」と表示される
- [ ] エクスポート中は進捗インジケーターが表示される
- [ ] ダウンロード完了後、通知が表示される
```

## File Naming Convention

Use sequential numbering for the same day:
- `.tmp/ac-draft-20260126-1.md`
- `.tmp/ac-draft-20260126-2.md`
- `.tmp/ac-draft-20260126-3.md`

## Workflow Tips

1. **Start Light**: If the user is unsure, create a minimal 1-2 criterion draft and iterate
2. **Iterate in Conversation**: Refine criteria through dialogue before finalizing
3. **Language**: Write in Japanese unless explicitly requested otherwise (following project guidelines)
4. **Team Adaptation**: Adjust verbosity based on team maturity—less experienced teams benefit from slightly more detailed criteria

## When NOT to Use This Skill

- User wants to create the full GitHub Issue (use different workflow)
- User wants to write technical specifications (not user-facing acceptance criteria)
- User wants to create test cases (more detailed than AC)
