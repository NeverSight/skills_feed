---
name: code-comment
description: Add comments to code according to language conventions. Use when the user asks for comments, documentation, or code explanation (e.g., add comments, document this, comment this).
---

# Code Comment

**Use this skill only when the user explicitly requests comments**, for example: "add comments", "document this", "explain this code", "comment this", "add documentation". Do not enable when the user is only refactoring, fixing bugs, etc., without also asking for comments.

**Response must follow user input**: Infer comment language, level of detail (brief vs. detailed), and scope (selection vs. whole file) from what the user says and what is selected. **Important: If the user does not specify detail level, default to "line-by-line detailed comments"**: add a comment for **every executable line** (or every logical block) explaining what it does, why, or what to watch for; complex logic should be explained in detail and called out. **Do not stop after only a file header or function header**—every statement with logic (e.g., regex, variable assignment, conditionals, loops, return, API calls) must have a corresponding line or end-of-line comment.

## Quick Start

1. Identify the target file’s programming language and use the usual comment style for that language.

## Trigger Conditions (User Input)

- Enable when the user **explicitly asks** for comments, in any language (e.g., add comments, document, explain).
- Do not enable when the user has **not** asked for comments.

## Response Rules (Infer from User)

| Item to decide | How to infer |
|----------------|--------------|
| **Comment language** | Prefer the same language as the user’s message. If unclear, match existing comments in the file. If neither is available, default to English. |
| **Detail level** | "Simple comments" / "brief" → minimal (file/function summary only). "Detailed" / "line-by-line" → comment every line or logical block. **If not specified → default to line-by-line detailed comments.** |
| **Scope** | User selected a range → comment only that range. User said "whole file" → entire file. Otherwise infer from selection. |

If the user’s intent is unclear, ask once (e.g., "Comments in English or Chinese?" or "Brief or detailed comments?").

## Details

1. **Identify language**: Determine the target file’s programming language.
2. **Match existing style**: Use the same comment delimiters, indentation, and line width as existing comments; if the file already has a comment language, use that.
3. **Comments only**: Do not change any executable code (no renaming, refactoring, or logic changes). Do not add TODO/FIXME unless the user asks.
4. **Keep existing comments**: Preserve them unless they are clearly outdated or wrong. Merge new comments with existing ones; avoid duplication. If an existing comment is inaccurate, update it in place.
5. **Avoid**: Comments that only restate the code (e.g., `// set x to 5`); repeating type information already in the code (focus on meaning and intent); putting secrets, passwords, or other sensitive data in comments. For line-by-line detailed comments, each comment should explain **what is being done, why, or what to watch for**, not meaningless restatement.

## When doing "line-by-line detailed comments", the following must have corresponding comments and must not be omitted:

- **Regular expressions**: Explain the meaning of the pattern or `RegExp` and what each part matches (e.g., `[^&#]*` means "until `&` or `#`").
- **Variable assignments**: If the meaning is not obvious (e.g., constructed regex strings, intermediate variables), explain purpose or meaning of the value.
- **Conditionals / branches / loops**: Explain what the condition represents and why the branch is structured that way.
- **return / exceptions**: Explain the meaning of the return value and when that value is returned.
- **API or library calls**: Briefly explain what is being done and why that API is used.

**Self-check**: After finishing, scan the target code; if any executable line has no comment, add one.

## Rules (Must Follow When Executing)

1. **Default behavior**: If the user does not explicitly ask for "simple" or "brief" comments, **default to line-by-line (or per-logical-block) detailed comments**; do not stop after only file/function headers.
2. **Forbidden**: Writing only a file header and function JSDoc while leaving statements in the function body (e.g., `const regexS = ...`, `regex.exec(...)`, `return ...`) without comments—that does **not** count as line-by-line detailed comments.
3. If you see potential issues in the user’s code, mention them in comments only; do not change the user’s code.
