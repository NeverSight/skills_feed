---
name: coaching-reporter
description: Generates detailed reports and analysis from coaching sessions. Use when analyzing coaching session files, tracking coachee progress, extracting insights from coaching notes, or creating structured reports for coaching development plans.
---

## Overview

This skill transforms coaching session information into useful reports and analysis to improve the performance and development of coachees.

**Before using this skill, read [AGENTS.md](AGENTS.md) for complete implementation guidance and detailed instructions.**

## Vocabulary

- **Coachee**: The person receiving coaching. This is the professional being accompanied, guided, and supported in their professional and personal development through coaching sessions. The coachee is the active protagonist of their own growth and development process.

## Instructions

### Generating Coaching Session Reports

1. **Identify the session file**: If the user doesn't specify a file, ask which coaching session file they want to analyze from `coaching/sessions/`
   - Session files follow the format: `<coachee>-<date>.md` (date in YYYY-MM-DD format)
   - Files contain session details, summaries, notes, and transcripts

2. **Generate the report**: Create a detailed report following the template and guidelines specified in [AGENTS.md](AGENTS.md)

3. **Save the report**: Store the generated report in `coaching/reports/` with the naming format: `<coachee>-<date>-report.md`
