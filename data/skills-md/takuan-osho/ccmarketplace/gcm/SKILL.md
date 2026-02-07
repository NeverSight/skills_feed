---
name: gcm
description: Generate Git Commit Message. This skill should be used when generating a commit message for staged changes. It analyzes git staged changes and generates an appropriate English commit message following Conventional Commits format.
---

# Generate Git Commit Message

## Overview

This skill analyzes the current git staged changes and generates an appropriate English commit message. It follows Conventional Commits format and provides clear, informative commit messages that accurately reflect the nature of the changes.

## Workflow

### 1. Analyze Current State

First, check the current git status and staged changes.

```bash
# Check current state
git status

# Analyze staged changes
git diff --cached

# Check recent commit history to understand the style
git log --oneline -5
```

### 2. Generate Commit Message

Based on the staged changes analysis, generate an appropriate English commit message with:

#### Subject Line
- **Maximum 50 characters**
- Summary of the changes
- Use **Conventional Commits format**:
  - `feat:` - New feature addition
  - `fix:` - Bug fix
  - `refactor:` - Code refactoring (no functional change)
  - `test:` - Test addition or modification
  - `docs:` - Documentation changes
  - `chore:` - Build process or auxiliary tool changes
  - `style:` - Code style changes (formatting, missing semicolons, etc.)
  - `perf:` - Performance improvements
  - `ci:` - CI configuration changes

#### Body (optional but recommended)
- Detailed explanation of the changes
- Reason for the changes
- Impact scope
- Blank line between subject and body

### 3. Output Format

Generate commit messages in the following format:

```
<type>: <concise summary of changes>

<detailed description of what changed and why>

<impact scope or additional context if applicable>
```

## Example

For a change that fixes a parameter format issue:

```
fix: Change servercode parameter format to use snake_case

Change trace_info.model_dump(by_alias=True) to by_alias=False to send
parameters in snake_case format (request_id, trace_header, root_trace_id)
instead of camelCase format (requestId, traceHeader, rootTraceId).

This resolves staging environment 504 errors where customer servercode
expects snake_case parameter names according to the API specification.
```

## Use Cases

- Bug fix commit messages
- Feature addition commit messages
- Refactoring description
- Configuration change recording
- Maintaining consistent commit history

## Guidelines

1. **Be specific** - Describe what actually changed, not vague descriptions
2. **Focus on the "why"** - Explain the reason for the change, not just the "what"
3. **Keep it concise** - Subject line should be scannable in git log
4. **Match project style** - Reference recent commits to maintain consistency
5. **Technical accuracy** - Ensure the message accurately reflects the code changes
