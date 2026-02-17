---
name: call-cursor-agent
description: Call cursor-agent to perform a task.
---

# Call cursor-agent to perform a task

This skill requests a task to cursor-agent.

## Checking for the Existence of cursor-agent

```bash
# Check if cursor-agent is installed. Exit code 0 means success, 1 means failure.
# If not installed, skip the subsequent steps of the skill.
which cursor-agent
if [ $? -ne 0 ]; then
  echo "cursor-agent is not installed"
fi
```

## Requesting a Task to cursor-agent

```bash
# If the model is not specified, the default model is composer-1.
model=composer-1
cursor-agent --model=$model <<EOT
{task_description}
EOT
```
