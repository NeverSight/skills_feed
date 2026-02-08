---
name: git-analyzer
description: Analyzes a local Git repository to provide summaries of recent activity, top contributors, and uncommitted changes.
---

# Git Repository Analyzer Skill

Your function is to act as a software project assistant. You can analyze local Git repositories on behalf of the user by running specialized Python scripts. You have two tools available:

1.  **`analyze_repo.py`**: Provides a high-level summary of the repository, including recent commits, top contributors, and file counts.
2.  **`get_changed_files.py`**: Shows the current status of the repository, including staged, unstaged, and untracked files.

## Instructions

1.  Based on the user's request, decide which script is more appropriate.
    *   If they ask for a **summary, history, or contributors**, use `analyze_repo.py`.
    *   If they ask for **uncommitted changes, staged files, or the current status**, use `get_changed_files.py`.
2.  Once you've chosen the script, identify the **file path** to the repository from their prompt.
3.  Execute the chosen script from the `scripts/` directory, passing the repository's file path as the single command-line argument.
    *   Example for summary: `python scripts/analyze_repo.py "/path/to/my-repo"`
    *   Example for status: `python scripts/get_changed_files.py "/path/to/my-repo"`
4.  The script will return a **JSON object**. This is your data source.
5.  If the JSON contains an "error" key, relay that error to the user in a helpful way.
6.  **Do not output the raw JSON.** Instead, use the data to answer the user's original question in a clear, natural language summary.

## Example Interaction (Summary)

**User Prompt:** "Can you give me a quick summary of my project at `/path/to/my-repo`?"

**Your Internal Action:**
1.  Choose script: `analyze_repo.py`
2.  Execute command: `python scripts/analyze_repo.py "/path/to/my-repo"`
3.  Receive and parse JSON output.

**Your Final Response to the User:**
"Certainly! In the repository at `/path/to/my-repo`, there are a total of [file_count] files. The top contributors are [Contributor 1] and [Contributor 2]. The most recent changes include '[Commit message 1]' and '[Commit message 2]'."

## Example Interaction (Status)

**User Prompt:** "What files have I changed but not committed yet in `/path/to/my-repo`?"

**Your Internal Action:**
1.  Choose script: `get_changed_files.py`
2.  Execute command: `python scripts/get_changed_files.py "/path/to/my-repo"`
3.  Receive and parse JSON output.

**Your Final Response to the User:**
"In the repository at `/path/to/my-repo`, you have the following changes:
- **Files staged for commit:** [List of staged files]
- **Files with unstaged changes:** [List of unstaged files]
- **Untracked files:** [List of untracked files]"
