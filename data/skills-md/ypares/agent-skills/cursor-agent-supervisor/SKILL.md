---
name: cursor-agent-supervisor
description: Offloading tasks with a well-defined scope to sub-agents, for instance to use a sub-agent to implement a set of specs. Use this skill whenever a task should not need a broad knowledge of the whole project
---

# Agent Supervisor

You can start subagents (e.g. to work on a specific JJ revision) with:

```bash
# Create a conversation with a sub-agent:
cursor-agent --print --model <model-name> create-chat  # Prints a conversation uuid

# Give a task to the sub-agent: (command will finish when sub-agent is done)
cursor-agent --print --resume <conversation-uuid> "...description of the subagent's task..."
```

## Model Selection

`cursor-agent --print --model unknown-model` will print an error that will list available models.
Unless you know which model is best for the task, just use `sonnet-4.5` by default.

## Invocation

**Important:** Sub-agent tasks can take several minutes. Always use a longer timeout:

```bash
# In your Shell tool call, set timeout to 10 minutes
timeout: 600000
```

The `--print` flag makes the sub-agent run on its own, and reply only once it is done.

## Setting Things up for the Sub-agent

Prepare things up so the agent can focus on its task (eg. if using JJ, don't ask them to run jj commands unless really necessary.
Notably run `jj edit` yourself first to get into the revision where the work should be done).
Ideally, the sub-agent should only have to read your instructions, hack on code, run build/tests, hack on code, etc.
until your instructions are implemented, and then reply with a final answer.
YOU are in charge of bookkeeping, not them. YOU have the big picture, they don't.

## Giving Good Instructions

Give the subagent the instructions they will need to complete the task, but do not overwhelm them.

**Do:**
- Provide a clear, specific goal
- List key files to read/modify
- Specify what "done" looks like
- Include relevant patterns to follow or reference implementations
- Tell them which skills to load if needed

**Don't:**
- Dump or link to entire skills when they only need a subset
- Include irrelevant context
- Leave success criteria ambiguous

### Task Description Template

```
Work on [specific task] in [repo/directory].

**Setup:**
- Skills to load or files to read IN FULL
- Summarized instructions from skills or files, tailored to the task

**Goal:**
[Clear description of what to implement/fix]

**Key files:**
- path/to/main/file.ts - [why it matters]
- path/to/reference.ts - [pattern to follow]

**Requirements:**
- [Specific requirement 1]
- [Specific requirement 2]

**Done when:**
- [Testable criterion 1]
- [Testable criterion 2]
- [e.g., "pnpm -F @pkg lint passes"]
```

## After Sub-agent Completes

Always verify the sub-agent's work:

1. **Check what changed:** check the commit/revision diff, and adequation with the task
2. **Review the actual code** if the changes are non-trivial
3. **Run verification commands** (tests, type-check, lint)
4. **Update task status** based on results (if using jj-todo-workflow)

## When Things Go Wrong

If the sub-agent:

- **Fails or errors out:** Read the output, fix any blocking issues, retry with more context
- **Produces incomplete work:** Continue the work yourself or spawn another sub-agent with clarified instructions
- **Goes off track:** Review what happened, potentially revert changes, retry with tighter constraints
- **Gets stuck on tooling:** May need to provide explicit commands or paths
