---
name: check
description: Runs .continue/agents checks locally against the current diff, simulating the GitHub PR checks experience. Use when the user says /check to review their changes before pushing.
---

# Local Agent Checks

Run every `.continue/agents/*.md` check against the current changes, just like the GitHub PR checks do in CI.

## Workflow

### 1. Gather context (write to disk, NOT into your context)

- Run `git diff main...HEAD` and write it to `/tmp/check-diff.patch`. If the diff is empty, also try `git diff --cached` and `git diff`.
  - **Cap the diff**: If the diff exceeds 3000 lines, truncate it to 3000 lines when writing. Add a final line: `\n... (diff truncated at 3000 lines)`.
  - Use a single bash command like: `git diff main...HEAD | head -3000 > /tmp/check-diff.patch`
- Run `git log main..HEAD --oneline` and write it to `/tmp/check-log.txt`.
- If there are no changes at all, tell the user and stop.
- **Do NOT read these files back into your own context.** The sub-agents will read them directly.

### 2. Discover agent checks

- Glob `.continue/agents/*.md` to find all agent check files.
- **Do NOT read the agent files.** Just extract the filename and use it to derive the check name (e.g., `code-conventions.md` → "Code Conventions").
- Present the user with the list of checks that will run, then proceed immediately without waiting.

### 3. Run checks in parallel (background agents)

For each agent check file, spawn a sub-agent with these settings:
- `subagent_type: "general-purpose"`
- `model: "haiku"` (fast and cheap for review tasks)
- `run_in_background: true`

Use this prompt structure:

```
You are a code reviewer running an automated check on a pull request.

## Setup
1. Read your check instructions from: {absolute path to .continue/agents/xxx.md}
2. Read the diff from: /tmp/check-diff.patch
3. Read the commit log from: /tmp/check-log.txt

## Your Task
Review the diff according to your check instructions. For each finding:
1. State the severity (Error / Warning / Info)
2. Reference the specific file and line from the diff
3. Explain what's wrong and how to fix it

If everything looks good and you have no findings, say "PASS" and briefly explain why the changes are clean for your check.

If you have findings, say "FAIL" and list them.

Keep your response concise. Do not repeat the diff back. Focus only on actionable findings.
Your final message must start with either "PASS" or "FAIL" on its own line.
```

Launch ALL sub-agents in a single message (all Task tool calls together).

### 4. Collect results efficiently

After launching all agents, wait for them to complete by reading their output files. **Do NOT read full outputs into your context.** Instead:

- For each background agent, use Bash to read just the last 30 lines of its output file: `tail -30 {output_file}`
- Parse whether it says PASS or FAIL and extract the key findings.

### 5. Summarize results

Present a summary table with emoji status indicators:

```
| Check | Result |
|-------|--------|
| ✅ Code Conventions | Passed |
| ❌ Security | 2 errors, 1 warning |
| ✅ Test Quality | Passed |
| ⚠️ Mobile Layout | 1 warning |
| ... | ... |
```

Use these emojis:
- ✅ = all clear, no findings
- ❌ = has Error-severity findings
- ⚠️ = has Warning-severity findings but no errors

### 6. Triage findings interactively

Do NOT dump all failure details in a big block. Instead, use AskUserQuestion to present each failed check's findings and let the user decide what to do.

For each check that has findings, present ONE AskUserQuestion with:
- The check name as the header
- A concise description of the finding(s) in the question text
- Options like:
  - "Fix it" — you will fix the issue
  - "Skip" — ignore this finding
  - (Add other options if contextually appropriate, e.g. "Add to backlog")

You can batch multiple failed checks into a single AskUserQuestion call (one question per failed check, up to 4 per call). If there are more than 4 failed checks, use multiple AskUserQuestion calls.

Then execute whatever the user chose — fix the issues they said to fix, skip the ones they said to skip.