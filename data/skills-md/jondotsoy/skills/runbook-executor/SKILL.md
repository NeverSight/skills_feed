---
name: runbook-executor
description: Executes runbooks and generates timestamped evidence documentation of the execution results
license: MIT
metadata:
  author: Jonathan Delgado <hi@jon.soy> (https://jon.soy)
  version: "1.0"
---

# Overview

This skill helps execute runbooks and document the execution with timestamped evidence. When a user runs through a runbook's steps, this skill generates a structured evidence file that captures what actually happened during execution, including results, deviations, issues, and validations.

Evidence files are stored alongside the runbook in timestamped directories, allowing multiple executions to be tracked over time without overwriting previous evidence.

# Configuration

Evidence location pattern: `<runbook-path>/evidence/<YYYY-MM-DD-HH-MM>/result.md`

Example: `./runbooks/user-login-flow/evidence/2026-01-31-14-30/result.md`

# Evidence Structure

Each evidence file documents:

1. **Execution Summary**: Status, duration, environment, executor
2. **Technical Requirements Verification**: Confirmation of prerequisites
3. **Step-by-Step Execution**: Actual commands run, results obtained, timestamps
4. **Validation Results**: Database checks, API responses, UI verifications
5. **Issues Encountered**: Problems found and their resolutions
6. **Deviations**: Any differences from the documented runbook
7. **Recommendations**: Suggestions for improving the runbook
8. **Conclusion**: Overall assessment and follow-up actions

# Instructions

When asked to execute a runbook and document evidence:

1. Run the evidence creation script: `./runbook-executor/scripts/create-evidence.sh <runbook-path>`
2. Follow the runbook steps in `<runbook-path>/STEPS.md`
3. Document each step's execution in the generated evidence file
4. Capture actual commands, outputs, and results
5. Note any deviations or issues encountered
6. Complete all validation sections
7. Add screenshots or logs to the evidence directory if needed
8. Write the conclusion with overall assessment

When asked to review past executions:

1. Run the list script: `./runbook-executor/scripts/list-evidence.sh <runbook-path>`
2. Review the list of executions ordered by date (newest first)
3. Open the relevant `result.md` file from the desired timestamp

# Examples

Execute a runbook and create evidence:
```bash
./runbook-executor/scripts/create-evidence.sh runbooks/user-login-flow
```

Execute an API testing runbook:
```bash
./runbook-executor/scripts/create-evidence.sh runbooks/api-payment-flow
```

List all evidence executions for a runbook (newest first):
```bash
./runbook-executor/scripts/list-evidence.sh runbooks/user-login-flow
```

# Resources

- Template: `assets/evidence-template.md`
- Creation script: `scripts/create-evidence.sh`
- List script: `scripts/list-evidence.sh`
