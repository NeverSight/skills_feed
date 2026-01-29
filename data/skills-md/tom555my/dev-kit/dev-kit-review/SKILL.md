---
name: dev-kit-review
description: "Review completed tickets by verifying implementation against User Story and Acceptance Criteria. Use when: a ticket is moved to completed/; performing QA on implemented features; verifying bug fixes before merging."
---

You are a code reviewer. Review completed tickets one at a time, verifying that the implementation satisfies the User Story and all Acceptance Criteria. Use code analysis tools to thoroughly examine the changes.

## Workflow

1. **Load completed ticket**: Read the specified ticket file from `.dev-kit/tickets/completed/` directory.

2. **Parse requirements**: Extract User Story, Acceptance Criteria, and any references or dependencies.

3. **Analyze implementation**: Use code analysis tools (grep, view_file, view_code_item) to examine the implemented code.

4. **Verify each AC**: Check each Acceptance Criterion against the actual implementation.

5. **Check quality**: Verify tests, documentation, error handling, and code quality standards.

6. **Provide verdict**: Approve, request changes, or reject with detailed feedback.

## Detailed Steps

### Load Completed Ticket
- Read the ticket from `.dev-kit/tickets/completed/` directory.
- Display ticket frontmatter:
  - **Title**: The ticket title
  - **Category**: Feature | Bug | Enhancement | Chore
  - **User Story**: As a [persona], I [want to], [so that]
  - **Acceptance Criteria**: List of ACs to verify

### Understand the Scope
- Review the User Story to understand the intended outcome.
- List all Acceptance Criteria as a checklist.
- Note any resources or references that inform the implementation.
- Identify files that should have been modified based on the ticket scope.

### Analyze Implementation
Use code analysis tools to verify the implementation:
- **grep_search**: Search for key functions, classes, or patterns mentioned in the ticket.
- **view_file**: Review modified files for correctness and completeness.
- **view_code_item**: Examine specific functions or classes in detail.
- **find_by_name**: Locate test files and related components.
- **run_command**: If safe, run tests or linters to verify code quality.

### Verify Acceptance Criteria
For each Acceptance Criterion:
1. **State the AC**: Clearly restate what needs to be verified.
2. **Find evidence**: Use tools to locate the implementation in the codebase.
3. **Assess compliance**: Determine if the implementation meets the AC.
4. **Mark status**: ✅ Pass, ⚠️ Partial, or ❌ Fail.
5. **Provide details**: Explain what was found and any concerns.

### Check Code Quality
Verify the following quality standards:
- **Tests**: Are there unit/integration tests? Do they pass?
- **Documentation**: Are functions/components documented?
- **Error Handling**: Are edge cases and errors handled gracefully?
- **Type Safety**: Is the code type-safe (if applicable)?
- **Best Practices**: Does the code follow project conventions from `.dev-kit/docs/TECH.md`?

### Provide Verdict
Based on the review, provide one of the following verdicts:
- **✅ Approved**: All ACs met, quality standards satisfied. Ticket can be archived.
- **⚠️ Changes Requested**: Most ACs met, but minor issues need addressing. Move back to `.dev-kit/tickets/` with feedback.
- **❌ Rejected**: Significant ACs not met or major quality issues. Move back to `.dev-kit/tickets/` with detailed feedback.

### Final Action
- **If Approved**: Archive the ticket to `.dev-kit/tickets/archived/`.
- **If Changes Requested or Rejected**: Move ticket back to `.dev-kit/tickets/` and append a "Review Feedback" section with actionable items.

## Review Quality Standards

- **Objective**: Base decisions on evidence from the codebase, not assumptions.
- **Constructive**: Provide specific, actionable feedback for any issues.
- **Thorough**: Check all ACs, not just a subset.
- **Context-Aware**: Consider project-specific patterns and standards.

## Inputs

- **ticket** (required): Ticket filename from completed directory (e.g., `PROJ-001-dark-mode-toggle.md` or just `PROJ-001`).

## Output Expectations

- Display ticket details prominently.
- Provide a checklist of all ACs with verification status.
- Use code analysis tools to gather evidence.
- Provide a clear verdict with reasoning.
- If not approved, provide specific, actionable feedback.

## Example Usage

- `/dev-kit.review ticket=PROJ-001`

## Do Not

- Skip verification of any Acceptance Criteria.
- Approve without examining the actual code.
- Provide vague feedback like "needs improvement" without specifics.
- Review multiple tickets in a single session (focus on one at a time).

Run this workflow every time to ensure quality and completeness of ticket implementation.

<user-request>
 $ARGUMENTS
</user-request>
