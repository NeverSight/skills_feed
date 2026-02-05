---
name: code
description: Open the current working directory or a specified folder in Visual Studio Code.
allowed-tools: Bash(code *)
---

## Usage

- `/code` - Opens the current working directory
- `/code /path/to/folder` - Opens the specified folder

## Implementation

Run `code` with arguments if provided, otherwise open current directory:

```bash
code ${ARGUMENTS:-.}
```
