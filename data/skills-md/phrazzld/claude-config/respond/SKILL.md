---
name: respond
description: |
  Systematically analyze all PR review feedback and comments, categorize them by priority and scope, and create actionable responses for immediate and future work.
---

Systematically analyze all PR review feedback and comments, categorize them by priority and scope, and create actionable responses for immediate and future work.

## 1. Review Analysis
- **Goal:** Comprehensively evaluate all PR comments and feedback.
- **Actions:**
    - **Collect all feedback types** - GitHub PRs have three distinct comment sources:
        - **Review comments**: Inline code comments attached to specific file lines (where bots like Codex leave suggestions)
        - **Issue comments**: General PR conversation comments
        - **Review summaries**: Top-level review state and summary feedback
        - Use pagination when fetching to ensure no comments are missed on large PRs
    - **Parse bot-generated feedback** - Automated review bots (e.g., Codex, Danger, lint bots) often include:
        - Priority/severity indicators (P0, P1, P2 badges or similar)
        - Structured suggestions with specific line numbers and file paths
        - Links to documentation or standards
        - Extract and respect these priority signals when categorizing
    - **Handle large PRs strategically** - For PRs with >1000 lines changed or >10 comments:
        - First assess scope: count comments by type and priority
        - Group related feedback by file/component
        - Process high-priority/blocking items first to avoid context overflow
        - Consider loading only changed portions of large files rather than full diffs
    - Think critically about each comment's legitimacy, scope, and impact.
    - Assess technical merit, alignment with project goals, and implementation complexity.
    - Consider reviewer expertise and context behind each suggestion.

## 2. Categorize Feedback
- **Goal:** Classify comments into actionable categories based on urgency and scope.
- **Categories:**
    - **Critical/Merge-blocking:** Issues that must be addressed before merge
    - **In-scope improvements:** Enhancements that fit this branch's purpose
    - **Follow-up work:** Valid suggestions for future iterations
    - **Low priority/Not applicable:** Comments that don't warrant immediate action

## 3. Create Action Plans

### Categorization Summary
First, present categorized summary:
- **Critical/Merge-blocking**: {count} items
- **In-scope improvements**: {count} items
- **Follow-up work**: {count} items
- **Low priority/Not applicable**: {count} items

### Parallel Fix Implementation (Critical + In-scope)

For actionable feedback, use parallel pr-comment-resolver agents:

**If 1-3 comments**: Launch Task agents in parallel
```
Task pr-comment-resolver("Comment: Add error handling to payment processing method at PaymentService.ts:45")
Task pr-comment-resolver("Comment: Extract validation logic from UserController to helper at app/controllers/users_controller.rb:120")
Task pr-comment-resolver("Comment: Fix variable naming - rename `data` to `userData` in UserService.ts:78")
```

**If 4+ comments**: Process in batches of 3-5 to avoid overwhelming context
```
# Batch 1: Most critical issues
Task pr-comment-resolver("Comment 1 details")
Task pr-comment-resolver("Comment 2 details")
Task pr-comment-resolver("Comment 3 details")

# Wait for completion, review changes, commit

# Batch 2: Remaining issues
Task pr-comment-resolver("Comment 4 details")
Task pr-comment-resolver("Comment 5 details")
```

**Agent input format**: Pass comment text with file location context
- Include: File path, line number, reviewer's specific request
- Each agent makes changes and reports resolution independently
- Review agent reports before committing

**Manual fallback**: If comment is ambiguous or requires design decision:
- Add to TODO.md as regular task
- Document question/blocker in task details

### For Follow-up Work
- Create GitHub issues for valid suggestions using `gh issue create`
- Include rationale for deferring and link back to original PR comments
- Label appropriately (e.g., `enhancement`, `tech-debt`, `low-priority`)

### For Low Priority/Rejected Feedback
- Document reasoning for not addressing immediately
- Consider: erroneous suggestions, out-of-scope changes, low ROI improvements
- Provide clear justification to inform future discussions

## 4. Document Decisions
- **Goal:** Create transparent record of feedback handling decisions.
- **Actions:**
    - Summarize analysis approach and decision criteria
    - For each comment category, explain rationale and next steps
    - Ensure all feedback is acknowledged and appropriately addressed

## 5. MANDATORY CODIFICATION

After addressing PR comments, codification is REQUIRED, not optional.

### Philosophy

Every piece of PR feedback represents something the system failed to prevent. The goal is not just to fix this PR, but to make this class of issue impossible in future PRs.

### Process

For each piece of feedback received, brainstorm how to prevent it systemically:

- Could a **hook** catch this before the code was written?
- Should an **agent** reviewer flag this pattern?
- Is there a **skill** that should encode this workflow?
- Does **CLAUDE.md** need this convention documented?

Don't be prescriptive about targets. Think creatively about prevention.

### Output Format

After resolving PR feedback, include:

```
CODIFICATION:
- [feedback] → [target]: [what was added/updated]
- [feedback] → [target]: [what was added/updated]

NOT CODIFIED (with justification):
- [feedback]: Already in [exact path] OR External constraint: [explanation]
```

### Invalid Justifications

- ❌ "First occurrence" - Cross-session memory doesn't exist
- ❌ "Pattern not detected" - One occurrence IS enough
- ❌ "Seems minor" - Minor issues compound
- ❌ "Not sure how to codify" - Brainstorm, don't skip

See CLAUDE.md "Continuous Learning Philosophy" for valid exceptions.

### Invoke Codification

After documenting decisions, invoke:
```
/codify-learning
```
