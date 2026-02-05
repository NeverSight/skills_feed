---
name: taskwarrior-manager
description: |
  Manages tasks using Taskwarrior with strict adherence to project and tag requirements.
  Enforces mandatory project assignment, tagging, and task lifecycle rules (start before work, 
  done after completion). Ensures agent-created tasks are attributed with +agent tag.
---

# Taskwarrior Manager

This skill provides instructions for managing tasks via the Taskwarrior command-line tool. 
It enforces strict rules to ensure data consistency, trackability, and proper task lifecycle management.

## When to use this skill
Use this skill when you need to:
- Look at what tasks need to be done 
- Note tasks that need to be done in the future
- Manage your tasks

## Usage
### How to view tasks
The main command is: `task`

### How to query
You can query tasks in the project `foo` using:
`task project:foo`

You can query by the tags `foo` and `bar` using:
`task +foo +bar`

You can combine them (look for tasks in the project `foo` with tag `bar`): `task project:foo +bar`

### How to mark a task as in progress
Use its ID (first column in the output of `task`)
For example, to mark task 3 as in progress: `task start 3`

### How to mark a task as done
Use its ID (first column in the output of `task`)
For example, to mark task 3 as in progress: `task done 3`

### How to add a new task
You can add a task titled 'hello world' with the tag `bar`, in project `foo` with:
`task add project:foo +bar hello world`

A task can depend on other tasks. Here's how to create a task that depends on tasks 3 and 4
`task add project:foo +bar depends:3,4 hello world`

### How to modify a task
To modify a task you first use the same syntax for querying tasks (you can just
use the task ID you have it instead) then the `mod` command, then the updated
properties.

To modify task 4 and add the `bar` tag, do: `task 4 mod +bar`
To change the project of task 4 to `foo`, do `task 4 mod project:foo`
To change the dependencies of task 4 to 2 and 3, do `task 4 mod depends:2,3`

NOTE: You cannot append a dependency; if you want to add a new dependency,
re-specify all the dependencies.

``

## Rules
1. Every task must always belong to a project
2. Every task must have at least one tag 
3. When you (the agent) create a task you must always add the `+agent` tag
4. Before starting work on a task you must always mark it as in progress
4. After finishing a task you must always mark it as done
