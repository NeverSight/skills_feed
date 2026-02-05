---
name: commit
description: Generate a conventional commit message from staged changes and commit safely.
---

# Commit

Use this skill to draft a clean conventional commit message based on staged changes.

## Rules

- Only use staged changes.
- Do not include test results or file lists in the message.
- Keep the subject line <= 50 characters, lowercase, imperative.
- Never add your signature to the commit message.

## Workflow

1. **Check status**
   - `git status --porcelain`
   - If nothing is staged, ask the user to stage changes first.

2. **Review staged diff**
   - `git diff --staged --name-only`
   - `git diff --staged`

3. **Select commit type**
   - `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`

4. **Optional scope**
   - Use a short lowercase scope if it adds clarity.

5. **Compose message**
   - Format:
     `type(scope): description`
   - Optional body: 1-3 lines explaining what and why.

6. **Confirm and commit**
   - Show the proposed message and ask for confirmation before running `git commit`.
