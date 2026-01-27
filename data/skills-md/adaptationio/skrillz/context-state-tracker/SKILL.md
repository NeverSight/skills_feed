---
name: context-state-tracker
description: State persistence across autonomous coding sessions. Use when saving progress, loading context, managing feature lists, tracking git history, or restoring session state.
version: 1.0.0
category: autonomous-coding
layer: foundation
---

# Context State Tracker

Persists and restores state across autonomous coding sessions using structured artifacts.

## Quick Start

### Save Progress
```python
from scripts.state_tracker import StateTracker

tracker = StateTracker(project_dir)
tracker.save_progress(
    accomplishments=["Implemented login form", "Added validation"],
    blockers=["Need API endpoint for auth"],
    next_steps=["Create auth service", "Add tests"]
)
```

### Load Progress
```python
state = tracker.load_progress()
print(f"Last session: {state.accomplishments}")
print(f"Blockers: {state.blockers}")
```

### Manage Feature List
```python
from scripts.feature_list import FeatureList

features = FeatureList(project_dir)
features.create([
    {"id": "auth-001", "description": "User login", "passes": False},
    {"id": "auth-002", "description": "User logout", "passes": False},
])

# Mark feature as passing
features.update_status("auth-001", passes=True)
```

## State Artifacts

```
project/
├── feature_list.json      # Immutable feature tracking (passes: true/false)
├── claude-progress.txt    # Human-readable session log
└── .git/                  # Git history for detailed rollback
```

### feature_list.json
```json
[
  {
    "id": "feat-001",
    "category": "functional",
    "description": "User can log in with email",
    "steps": ["Navigate to login", "Enter credentials", "Click submit"],
    "passes": false
  }
]
```

### claude-progress.txt
```markdown
# Session Progress

## Session 5 - 2025-01-15 14:30

### Accomplishments
- Implemented user authentication
- Added password validation
- Created login tests

### Blockers
- Need to set up email verification

### Next Steps
- Implement email service
- Add password reset flow
```

## Key Rules

1. **Features are immutable**: Can only transition from `false` → `true`
2. **Never delete features**: Removing features is CATASTROPHIC
3. **Update progress after each session**: Enables quick context restoration
4. **Use git for detailed history**: Commits provide granular rollback

## Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    STATE TRACKING FLOW                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  SESSION START                                               │
│  ├─ Read feature_list.json                                  │
│  ├─ Read claude-progress.txt                                │
│  └─ Get git log (recent commits)                            │
│                                                              │
│  SESSION WORK                                                │
│  ├─ Select next incomplete feature                          │
│  ├─ Implement feature                                       │
│  └─ Verify feature passes                                   │
│                                                              │
│  SESSION END                                                 │
│  ├─ Update feature_list.json (passes: true)                 │
│  ├─ Append to claude-progress.txt                           │
│  └─ Commit with descriptive message                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Integration Points

- **autonomous-session-manager**: Uses state for session detection
- **coding-agent**: Uses feature list for work selection
- **progress-tracker**: Uses state for metrics

## References

- `references/STATE-ARTIFACTS.md` - Artifact specifications
- `references/PROGRESS-FORMAT.md` - Progress file format

## Scripts

- `scripts/state_tracker.py` - Core StateTracker class
- `scripts/progress_file.py` - Progress file management
- `scripts/feature_list.py` - Feature list management
- `scripts/git_state.py` - Git history integration
