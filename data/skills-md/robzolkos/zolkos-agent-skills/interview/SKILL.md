---
name: interview
description: Interview me about the plan
argument-hint: [file or text]
model: opus
disable-model-invocation: true
---

The user has provided input: $1

First, determine if this input is a file path or raw text:
- If it looks like a file path (contains `/` or ends with `.md`, `.txt`, etc.), use the Read tool to read the file contents as the plan
- If it's raw text (a description, idea, or plan written directly), treat it as the plan content directly

If raw text was provided (not a file):
1. Generate a filename using the format: `PLAN-YYYY-MM-DD-<short-summary>.md` where `<short-summary>` is 2-4 lowercase words from the plan separated by hyphens (use bash `date` command to get the date)
2. Create this file in the current working directory with the initial plan text

Then interview me in detail using the AskUserQuestion tool about literally anything: technical implementation, UI & UX, concerns, tradeoffs, etc. but make sure the questions are not obvious.

Be very in-depth and continue interviewing me continually until it's complete, then write the final spec to the file (either the original file if a file was provided, or the newly created timestamped file if text was provided).
