---
name: zenforge-init
description: Use when onboarding a new or existing repository, setting up task tracking, configuring .agents/task-tracker.md, or scaffolding SSOT documentation governance.
---

# zenforge-init — Repository Scaffolding & Ecosystem Bootstrapper

Initialize repository task tracking, Git privacy safeguards, SSOT documentation governance, and agent constitution hooks.

## Operating Invariants

- **Authority Grounding**: Inspect existing repository conventions before proposing structure. Preserve established documentation and obtain explicit consent before adjusting existing layouts.
- **Pre-Mutation Gate**: Stage all planned file additions, modifications, and `.gitignore` entries in Changeset format. Forbid creating or modifying files on disk without affirmative human approval.
- **Privacy First**: Automatically ignore `.agents/scratch/` and `.agents/tasks/` in `.gitignore` by default to isolate scratchpads and local task drafts; users unignore manually if shared tracking is desired.
- **Define Once in SSOT**: Establish `.agents/task-tracker.md` as canonical authority for task tracking, and `docs/README.md` as authority for documentation placement. Keep `AGENTS.md` lean with direct pointer links.

## Domain Engine & Standards

### 1. Tracker Type Selection
- Check `git remote -v`:
  - Remote points to GitHub (`github.com`) -> Propose **GitHub Issues (`gh`)** or **Local Markdown**.
  - Remote points to GitLab (`gitlab.com` or custom host) -> Propose **GitLab Issues (`glab`)** or **Local Markdown**.
  - No remote or offline environment -> Propose **Local Markdown (`.agents/tasks/`)**.

### 2. Git Privacy & Ignore Invariants
- **Default Privacy Baseline**: Stage local-first privacy rules in `.gitignore` by default:
  ```gitignore
  .agents/scratch/
  .agents/tasks/
  ```
- **Team Tracking Opt-In**: Keep temporary scratchpads and task drafts strictly local by default. Users manually remove `.agents/tasks/` from `.gitignore` if shared team repository tracking is desired.

### 3. Canonical Templates

#### A. Task Tracker (`.agents/task-tracker.md`)
```markdown
# Agent Task Tracker

- **Type**: local-markdown # (or: github | gitlab)
- **Task Directory**: .agents/tasks/
- **Status Vocabulary**: ready | blocked | done
- **Remote**: <none or owner/repo>
```

#### B. Baseline Placement Matrix (`docs/README.md`)
Use as baseline for greenfield repositories; adapt rows dynamically to map observed documentation for existing projects:
```markdown
# Documentation Index & Placement Matrix

| Topic / Scope | Authoritative SSOT | Responsibility |
| :--- | :--- | :--- |
| **Tasks & Execution** | `.agents/tasks/` | Decomposed task units and progress tracking |
| **Domain & Specifications** | `docs/specs/` | Business rules, use cases, domain vocabulary |
| **Architecture & Decisions** | `docs/adr/` | Architectural Decision Records (MADR format) |
```

#### C. Constitution Hook (`AGENTS.md`)
```markdown
## Agent Workflow
- **Task Tracker**: Configured in `.agents/task-tracker.md`. Active tasks in `.agents/tasks/`.
- **Documentation**: Governed by `docs/README.md`.
```

## Execution Protocol

### Step 1: Read-Only Discovery
Inspect repository state:
- Run `git remote -v` to detect remotes.
- Check existence of `.agents/task-tracker.md`, `.agents/tasks/`, and `.gitignore`.
- Check existence of `AGENTS.md`.
- Scan for existing documentation files and directories across the repository.

### Step 2: Changeset Staging & Lean Delivery
1. Stage proposed modifications for missing or unconfigured scaffolding assets in Changeset format:
   ```text
   # Changeset: Repository Initialization

   📁 .agents/
   ├── 📄 task-tracker.md
   │   └── [CREATE] Configure task tracking mode and status vocabulary.
   ├── 📁 tasks/
   │   └── [CREATE] Create task directory for local markdown workflow.
   └── 📁 scratch/
       └── [CREATE] Create scratchpad directory for temporary test harnesses and probes.

   📁 docs/
   └── 📄 README.md
       └── [CREATE] Establish documentation Placement Matrix.

   📁 /
   ├── 📄 .gitignore
   │   └── [UPDATE] Add .agents/scratch/ and .agents/tasks/ privacy rules.
   └── 📄 AGENTS.md
       └── [UPDATE] Add agent workflow and documentation pointers.
   ```
2. **Lean Delivery**: Present strictly the Changeset summary, recommended configuration choices, and technical rationale. Forbid dumping voluminous raw file contents into chat by default.

### Step 3: Authorization Gate
1. Present the staged Changeset and offer execution options:
   - Approve applying proposed configuration directly.
   - Request to adjust settings (Tracker type, Placement Matrix paths).
   - Request to inspect markdown previews.
2. Forbid modifying workspace files on disk within this turn.
3. Halt turn immediately and wait for affirmative human authorization (e.g., 'proceed', 'approved').

### Step 4: Atomic Application & Handoff
1. Upon receiving approval, write staged files to disk.
2. Report completed setup and suggest next commands: `/clarify` (to deliberate new features) or `/to-tasks` (to decompose existing plans).
