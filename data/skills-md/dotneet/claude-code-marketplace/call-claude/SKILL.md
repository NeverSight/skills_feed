---
name: call-claude
description: Call claude to perform a task.
---

# Call claude to perform a task

Call claude to perform a task.

## Checking for the Existence of claude

```bash
# Check if claude is installed. Exit code 0 means success, 1 means failure.
# If not installed, skip the subsequent steps of the skill.
which claude
if [ $? -ne 0 ]; then
  echo "claude is not installed"
fi
```

## Requesting a Task to claude

This task may take a long time. If the timeout value of the Bash tool can be set, please specify the maximum timeout value.

```bash
claude -p --dangerously-skip-permissions <<EOT
{task_description}
EOT
```
