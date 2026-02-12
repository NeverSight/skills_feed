---
name: gemini
description: Invokes Google Gemini CLI for an independent second opinion with a 1M+ token context window. Use when (1) reviewing plans, diffs, or architecture decisions before acting, (2) analyzing large volumes of files or content that exceed normal context limits, (3) wanting a competing perspective from a different model family, (4) scanning or summarizing entire directories or large codebases.
context: fork
user-invocable: true
model: opus
allowed-tools:
  - Glob
  - Grep
  - Read
  - Bash(gemini:*)
  - Bash(cp:*)
  - Bash(rm:*)
---

# Gemini Second Opinion

Use Gemini to get an independent review from a model with a 1M+ token context window.

## Invocation

Use `-p` for non-interactive (headless) mode. Always use `-o text` for plain text output.

**Prefer telling Gemini to read files directly** over piping via stdin. Gemini can read files within the project workspace on its own, and stdin truncates at 8MB.

```bash
# PREFERRED: Tell Gemini to read files itself (non-interactive)
gemini -p "Read the files in /path/within/project/ and review them for bugs" -o text
```

```bash
# OK for small content: pipe via stdin
git diff main..HEAD | gemini -p "Review this diff for issues" -o text
```

## Workspace Sandbox

Gemini is sandboxed to the project directory. It **cannot** read files outside the workspace, even via symlinks.

If files live outside the project (e.g., `~/.claude/`), **copy them into the project first**, then clean up after:

```bash
cp -r ~/.claude/some-data /path/to/project/.tmp-data
gemini -o text "Read the files in /path/to/project/.tmp-data/ and analyze them"
rm -rf /path/to/project/.tmp-data
```

## Workflow

1. **Gather context**: Identify the files, plans, or diffs Gemini needs
2. **Ensure accessibility**: If files are outside the workspace, copy them in
3. **Compose a focused prompt**: Be specific about what to review and what feedback you want
4. **Invoke Gemini**: Tell it to read files directly, or pipe small content via stdin. Always use `-p` and `-o text`
5. **Clean up**: Remove any temporary copies
6. **Report findings**: Present Gemini's feedback to the user with your own assessment of which points are valid

## Prompt Guidelines

- State the review goal explicitly (e.g., "find logical errors", "evaluate scalability", "check for missing edge cases")
- Include constraints or requirements Gemini should check against
- Ask for structured output (numbered issues, severity levels) for actionable feedback
- For large volumes of files, tell Gemini to read the directory rather than listing each file
