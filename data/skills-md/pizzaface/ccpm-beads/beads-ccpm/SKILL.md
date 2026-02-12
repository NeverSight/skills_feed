---
name: beads-ccpm
description: Full project management system powered by Beads task tracker. Includes PRD creation, epic decomposition, task management, parallel agent execution, bidirectional sync, git worktrees, and comprehensive workflow commands. Use when the user needs to manage software projects with PRDs, epics, issues, and sprint workflows.
---

# Beads CCPM - Project Management Skill

A comprehensive, agent-agnostic project management system for AI-assisted software development, powered by the Beads local-first task tracker.

## Capabilities

- **PRD Management**: Create, edit, list, and track Product Requirements Documents
- **Epic Workflow**: Decompose PRDs into epics, break epics into tasks, sync to Beads
- **Issue Tracking**: Start, sync, close, and analyze issues with parallel work streams
- **Parallel Execution**: Launch multiple agents to work on independent tasks simultaneously
- **Git Integration**: Worktree and branch-based workflows for isolated development
- **Bidirectional Sync**: Keep local markdown files and Beads task tracker in sync
- **Context Management**: Create, prime, and update project context for agent sessions

## Quick Start

1. `/pm:init` - Initialize the PM system and install Beads
2. `/pm:prd-new <feature>` - Create a new PRD through brainstorming
3. `/pm:prd-parse <feature>` - Convert PRD to a technical epic
4. `/pm:epic-decompose <epic>` - Break epic into numbered tasks
5. `/pm:epic-sync <epic>` - Push epic and tasks to Beads
6. `/pm:epic-start <epic>` - Launch parallel agent execution

## Project Data

This skill stores project data in `.project/` at the project root:
- `.project/prds/` - Product Requirements Documents
- `.project/epics/` - Epics and their task files
- `.project/context/` - Project context documentation
- `.project/adrs/` - Architecture Decision Records

## Dependencies

- [Beads CLI](https://github.com/steveyegge/beads) - Local-first task tracker (auto-installed by `/pm:init`)
- Git - Version control
