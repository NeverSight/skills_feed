---
name: call-codex
description: Call codex to perform a task.
---

# Call codex to perform a task

Call codex to perform a task.

## Checking for the Existence of codex

```bash
# Check if codex is installed. Exit code 0 means success, 1 means failure.
# If not installed, skip the subsequent steps of the skill.
which codex
if [ $? -ne 0 ]; then
  echo "codex is not installed"
fi
```

## Requesting a Task to codex

This task may take a long time. If the timeout value of the Bash tool can be set, please specify the maximum timeout value.

```bash
codex exec --sandbox danger-full-access <<EOT
{task_description}
EOT
```
