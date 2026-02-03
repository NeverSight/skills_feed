---
name: beads
description: 'This skill should be used when the user asks to "track issues", "create beads issue", "show blockers", "what''s ready to work on", "beads routing", "prefix routing", "cross-rig beads", "BEADS_DIR", "two-level beads", "town vs rig beads", "slingable beads", or needs guidance on git-based issue tracking with the bd CLI.'
---

# Beads - Persistent Task Memory for AI Agents

Graph-based issue tracker that survives conversation compaction.

## Overview

**bd (beads)** replaces markdown task lists with a dependency-aware graph stored in git.

**Key Distinction**:
- **bd**: Multi-session work, dependencies, survives compaction, git-backed
- **TodoWrite**: Single-session tasks, linear execution, conversation-scoped

**Decision Rule**: If resuming in 2 weeks would be hard without bd, use bd.

## Prerequisites

- **bd CLI**: Version 0.34.0+ installed and in PATH
- **Git Repository**: Current directory must be a git repo
- **Initialization**: `bd init` run once (humans do this, not agents)
