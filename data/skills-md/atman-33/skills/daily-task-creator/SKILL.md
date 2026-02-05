---
name: daily-task-creator
description: Creates a new daily task file in .tmp with a sequence number (e.g., task-20241225-1.md). Use when the user wants to start a new task, log a daily activity, or create a task file.
---

# Daily Task Creator

## Overview

This skill automates the creation of daily task files in the `.tmp` directory. It ensures files are named with the current date and a unique sequence number (e.g., `task-YYYYMMDD-N.md`).

## Usage

To create a new task file, run the included Python script:

```python
python3 {path}/scripts/create_task.py
```

This script will:
1.  Check the `.tmp` directory.
2.  Find the next available sequence number for today's date.
3.  Create a new markdown file with a header and timestamp.
4.  Print the path of the created file.
