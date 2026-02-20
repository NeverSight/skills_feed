---
name: branch-quiz
description: "Use when the user wants to verify their understanding of a branch's code changes by being quizzed on runtime behavior, assumptions, failure points, and edge cases instead of just reading diffs"
---

## Overview

Quiz the user on a git branch's changes to verify genuine comprehension. Rather than passively reading diffs, the user answers targeted questions covering: runtime behavior, embedded assumptions, failure points, edge cases, API design decisions, data model changes, data flows, security implications, performance impacts, and dependencies & integration effects. Score their understanding and surface any gaps.

## Process

### 1. Gather the Diff

Run `git diff main...HEAD` to collect all changes on the current branch. If the branch has no diff against main, inform the user and stop.

### 2. Analyze the Changes

Read through every changed file. Build a mental model of:
- What behavior changed and why
- What assumptions are baked into the new code
- Where things could break under unexpected input or load
- How the changes affect API contracts, data models, and data flows
- Security surface area introduced or altered
- Performance characteristics that shifted
- How the changes ripple into other parts of the system

### 3. Generate the Quiz

Produce 5-10 questions that test genuine understanding, not surface recall. Each question should:
- Target a specific dimension (behavior, assumptions, failure, edge cases, API design, data model, data flow, security, performance, or dependencies)
- Require reasoning about the code, not just restating what changed
- Be answerable from the diff alone — no trick questions

Label each question with its dimension in brackets, e.g. `[Failure Points]`.

Present questions one at a time using AskUserQuestion. Provide 3-4 multiple choice options per question when possible. For questions that require free-form reasoning, use open-ended format.

### 4. Evaluate Answers

After each answer, respond with:
- **Correct** or **Incorrect**
- A brief explanation referencing the relevant code
- The file and line range where the answer lives

Track the running score as the quiz progresses.

### 5. Report Results

After all questions, present a summary:
- Overall score (e.g. 7/10)
- Comprehension breakdown by dimension (which areas were strong, which had gaps)
- For any missed questions, a focused explanation of what the user should review
- Suggest specific files or sections to re-read for any weak areas

## Common Mistakes

- **Don't ask trivia questions.** "What line number was changed?" tests nothing. Every question should require the user to reason about consequences.
- **Don't reveal answers in the question.** Avoid leading phrasing that gives away the correct option.
- **Don't skip the diff analysis.** Read every changed file before generating questions. Shallow analysis produces shallow questions.
- **Don't overwhelm with questions.** Stay in the 5-10 range. Quality over quantity.
- **Don't grade harshly on wording.** If the user demonstrates understanding with different terminology, mark it correct.
