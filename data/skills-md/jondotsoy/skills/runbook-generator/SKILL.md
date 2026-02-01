---
name: runbook-generator
description: Creates structured runbooks to document reproducible scenarios for APIs, UX flows, and technical procedures
license: MIT
metadata:
  author: Jonathan Delgado <hi@jon.soy> (https://jon.soy)
  version: "1.0"
---

# Overview

This skill helps create standardized runbooks that document reproducible scenarios in a clear, step-by-step format. Runbooks are ideal for documenting API workflows, user interface flows, deployment procedures, and any technical process that needs to be executed consistently.

A runbook is a living document that describes an ideal, reproducible scenario - not a log of past executions. It should be executable multiple times with the same expected results.

# Configuration

Default runbook location: `./runbooks/<task-name>/STEPS.md`

You can customize the runbook path when creating a new runbook.

# Runbook Structure

Each runbook must include:

1. **Overview**: Brief description of what this runbook accomplishes
2. **Technical Requirements**: Environment setup needed before execution
   - Git branch/commit to checkout
   - Database state requirements
   - Required credentials or configurations
   - Environment context (local, dev, staging, prod)
   - Any pre-execution setup (delete records, modify configs, etc.)
3. **Steps to Reproduce**: Clear, actionable steps
   - Exact commands to run
   - UI elements to click
   - API calls to make (with curl examples)
   - Expected responses at each step
4. **Validations**: How to verify successful completion
   - Database queries to run
   - UI states to check
   - API responses to validate
   - Success criteria

# Instructions

When asked to create a runbook:

1. Run the creation script: `./runbook-generator/scripts/create-runbook.sh <runbook-path>`
2. Edit the generated template with specific details
3. Ensure all sections are complete and actionable
4. Verify the runbook is reproducible

When asked to update a runbook:

1. Locate the existing STEPS.md file
2. Update the relevant sections
3. Maintain the standard structure

# Examples

Create a runbook for user login flow:
```bash
./runbook-generator/scripts/create-runbook.sh runbooks/user-login-flow
```

Create a runbook for API endpoint testing:
```bash
./runbook-generator/scripts/create-runbook.sh runbooks/api-payment-flow
```

# Resources

- Template: `assets/runbook-template.md`
- Creation script: `scripts/create-runbook.sh`
