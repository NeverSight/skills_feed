---
name: terminal-execution
description: Best practices for reliable terminal command execution and output capture. Use this skill when running shell commands, especially in environments like WSL where output might be truncated or lost, to ensure results are properly captured and inspected.
metadata:
  short-description: Reliable command execution & output capture
---

# Terminal Execution Guidelines

This skill defines the standard workflows for executing terminal commands to ensure reliability and visibility of outputs, particularly in complex environments like WSL.

## 1. Primary Execution Method

Always prioritize structured execution tools over raw terminal input when possible.

1.  **Use `execute_command`**: Call the `execute_command` tool from the `terminal-runner` MCP server. This provides the most reliable way to get exit codes and standard output programmatically.
2.  **Fallback**: If `terminal-runner` is unavailable, use the standard `run_in_terminal` tool.

## 2. Handling Missing Output (WSL/Complex Environments)

In some environments (like WSL), terminal output may not be returned to the agent context correctly, or it may be truncated. If you suspect output is missing:

### File-Based Capture Workflow

1.  **Prepare Directory**: Ensure `.tmp/copilot/` exists.
2.  **Redirect Output**: Run the command redirecting both stdout and stderr to a file.
3.  **Read Result**: Use file reading tools to inspect the output.

### Common Patterns

**Capture stdout and stderr:**
```bash
some-command > .tmp/copilot/output.txt 2>&1
```

**Capture and view live (if interactive):**
```bash
some-command 2>&1 | tee .tmp/copilot/output.txt
```

**Capture exit code separately:**
```bash
some-command > .tmp/copilot/output.txt 2>&1; echo $? > .tmp/copilot/exit-code.txt
```

## 3. Best Practices

- **File Naming**: Use descriptive names for capture files (e.g., `.tmp/copilot/build-log.txt`, `.tmp/copilot/test-results.txt`).
- **Cleanup**: Periodically clean up the `.tmp/copilot/` directory to avoid confusion with stale data.
