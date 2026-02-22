---
name: pr-message
description: Write a concise, high-signal GitHub pull request message that explains intent, impact, and risk
disable-model-invocation: true
---

# Write PR Message

## Overview
Write a concise, high-signal GitHub pull request message that explains intent, impact, and risk
without duplicating information already visible in GitHub.

## PR Structure

### Summary
- 1–3 sentences.
- Explain what this PR does and why it exists.
- Focus on behavior and outcome, not implementation details.
- Do not list files, commits, tickets, or branches.

### What Changed
- 1–3 short bullet points.
- Describe **behavioral or functional changes** only.
- No file names or low-level implementation details.
- Skip this section if it adds no value.

### Testing
- 1–2 bullets describing how this was verified.
- Be concrete (tests added, manual flows checked, API exercised).
- Avoid generic statements like "tests passed".

### Screenshots (UI only, optional)
- Include screenshots only if this PR changes UI or UX.
- Prefer inline images over external links.
- Omit this section entirely for non-UI changes.

### Risk / Rollout
- Answer briefly:
  - Is this feature-flagged?
  - Is a migration required?
  - How can this be reverted?
- "No / Not needed" is a valid and useful answer.

### Notes for Reviewers (Optional)
- Call out:
  - Tricky logic
  - Non-obvious decisions
  - Areas that deserve extra attention
- Keep this short and targeted.

## Rules
- Keep the entire PR message scannable.
- Avoid repeating information GitHub already shows.
- Prefer clarity over completeness.
- Omit sections that don't apply rather than filling them with placeholders.
- Always write PR message in markdown code.

## Steps
1. Review the changes and commits on the branch.
2. Write the Summary first.
3. Add only the sections that meaningfully help a reviewer.
4. Output a clean PR message ready to paste into GitHub.
