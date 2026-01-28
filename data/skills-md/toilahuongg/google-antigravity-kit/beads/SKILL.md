---
name: beads
description: Guide for using Beads (bd) - A memory upgrade and task management tool for AI agents.
---

# Beads (bd) Skill

Beads is a distributed task management system designed specifically for AI agents. It effectively gives you a "long-term memory" and a structured way to plan, track, and execute complex workflows without losing context. It uses Git as its database, meaning tasks are versioned, branched, and merged alongside code.

## 📦 Installation

If `bd` is not found, you can install it using one of the following methods for the user (ask for permission if unsure):

### npm (Recommended)
```bash
npm install -g @beads/bd
```

### Homebrew
```bash
brew install steveyegge/beads/bd
```

### Go
```bash
go install github.com/steveyegge/beads/cmd/bd@latest
```

## 🚀 Initialization

Before using Beads in a repository, you must initialize it.

1.  **Initialize**:
    ```bash
    bd init
    ```
    *Use `bd init --stealth` if you want to use Beads locally without committing the `.beads` directory to the remote repo (good for personal tracking).*

2.  **Install Hooks** (CRITICAL for Agents):
    ```bash
    bd hooks install
    ```
    *This ensures that your changes are automatically synced and consistency is maintained between the JSONL database and Git.*

## 🤖 Agent Workflow (CRITICAL RULES)

As an AI agent, you must follow these rules strictly to interact with `bd` correctly.

### 1. NO Interactive Editors
**NEVER** use `bd edit`. It opens a text editor (vim/nano) which you cannot interact with.
**ALWAYS** use `bd update` with specific flags.

### 2. ALWAYS Sync
At the end of a session or after making a batch of changes, **ALWAYS** run:
```bash
bd sync
```
*This forces an immediate flush of the 30-second debounce buffer, commits changes, pulls from remote, imports updates, and pushes to remote. Without this, your changes might be lost or become stale.*

### 3. Creating Tasks
Create a new task with a title and priority (`-p`).
- Priority 0: High
- Priority 1: Medium
- Priority 2: Low

```bash
bd create "Refactor login component" -p 1
# Output: Created task bd-a1b2
```

### 4. Updating Tasks
Use flags to update specific fields.

```bash
# Update description
bd update bd-a1b2 --description "Refactoring the login component to use hooks."

# Update title
bd update bd-a1b2 --title "Refactor Login to Functional Component"

# Update status
bd update bd-a1b2 --status in_progress

# Update design notes
bd update bd-a1b2 --design "Using React.useState and React.useEffect"

# Update acceptance criteria
bd update bd-a1b2 --acceptance "1. User can login\n2. User can logout"
```

### 5. Managing Dependencies
Structure your work hierarchically.

```bash
# Add a child task to a parent
bd dep add bd-child-id bd-parent-id
```

### 6. Closing Tasks
Close a task when it's done.

```bash
bd close bd-a1b2 --reason "Completed"
```

### 7. Listing Tasks
View current tasks to understand your state.

```bash
bd ready   # Show actionable tasks (unblocked, open)
bd show bd-a1b2 # Show details of a specific task
```

## 📝 Example Session

```bash
# 1. Start a new feature
bd create "Implement Dark Mode" -p 0
# > Created bd-d4rks

# 2. Break it down
bd create "Add theme context" -p 1
# > Created bd-ctx1
bd dep add bd-ctx1 bd-d4rks

bd create "Add toggle button" -p 1
# > Created bd-t0g1
bd dep add bd-t0g1 bd-d4rks

# 3. Start working
bd update bd-ctx1 --status in_progress

# ... (Do the coding work) ...

# 4. Mark as done
bd close bd-ctx1 --reason "Implemented"

# 5. SYNC YOUR WORK
bd sync
```

## 💡 Why use Beads?
- **Context Preservation**: Offload your planning to `bd` so you don't have to hold everything in your immediate context window.
- **Resilience**: If your session crashes or restarts, run `bd ready` to see exactly where you left off.
- **Collaboration**: If the user is also using `bd`, you can see their tasks and status updates instantly.
