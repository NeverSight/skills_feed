---
name: session-handoff
description: End-of-session workflow that audits workspace for junk files, validates work against development principles, updates session documentation, and completes handoff. Use when wrapping up a session or when user says "end session", "handoff", "wrap up", "quick handoff", or "full handoff".
allowed-tools: Read, Glob, Grep, Edit, Bash, TodoWrite, Write
---

# Session Handoff Skill

## Workflow Selection

**FIRST: Determine which workflow to follow**

1. User says **"quick handoff"** → Follow **Quick Handoff Workflow** below
2. User says **"full handoff"**, **"wrap up"**, or **"deep clean"** → Follow **Full Handoff Workflow** below
3. Ambiguous request → Ask user: "Would you like a quick handoff or a full handoff with deep cleanup?"

---

## Quick Handoff Workflow

Execute these steps in order:

### Step 1: Quick Workspace Audit

Scan for obvious issues in root directories only:

```bash
# Junk files
find . -maxdepth 3 -type f \( -name "*.tmp" -o -name "*.bak" -o -name "*~" -o -name "*.swp" -o -name ".DS_Store" \) -not -path "./.git/*" -not -path "*/node_modules/*" -not -path "*/archive/*"

# Version conflicts (CRITICAL - always check)
find docs .claude -maxdepth 2 -type f -name "*.md" | grep -iE "(v2|v3|new|old|copy|backup|optimized|updated|revised)" | grep -v archive
```

Report findings to user. Skip to Step 2 if clean.

### Step 2: Resolve Version Conflicts (if any found)

If version conflicts found in Step 1:

1. **Read both files** (first 100 lines minimum)
2. **Determine canonical version**: Which is more recent/complete/referenced?
3. **Choose action**:
   - **Merge** if both have unique valuable content → Combine into single file
   - **Keep newest** if minimal differences → Delete old, rename new to remove version suffix
4. **Update references**: Grep for filename, update any references
5. **Archive old ONLY if valuable historical context**, otherwise delete

```bash
# Archive (if valuable)
git mv docs/guide-old.md archive/docs/

# Delete (if no reference value)
git rm docs/guide-old.md
```

### Step 3: Update Related Documentation

**CRITICAL: Update docs related to session work**

Identify what changed:
```bash
# Files modified this session
git diff --name-only HEAD~5 HEAD | grep -v ".claude/sessions"
```

Update corresponding documentation:
- **MCP tools changed** → Update `docs/MCP_TOOLS_REFERENCE.md`
- **API endpoints changed** → Update `docs/REST_API_GUIDE.md`
- **Workflow changes** → Update `docs/N8N_*.md`
- **Phase completed** → Update `docs/ROADMAP.md`
- **Architecture changed** → Update `.claude/PROJECT_OVERVIEW.md`
- **New known issues** → Update `docs/KNOWN_ISSUES.md`

### Step 4: Update sessions/CURRENT.md

Update with session summary (100-200 lines max):

```markdown
# Current Session Context

> **Last Updated**: YYYY-MM-DD
> **Last Session**: YYYY-MM-DD-N

## Quick Status
[Status table with current phase, components, blockers]

## Last Session (YYYY-MM-DD-N)
**Focus**: Brief description
**Completed**: 2-3 key items
**Commits**: X commits (SHAs)

## Next Session Priorities
1. Priority 1
2. Priority 2
3. Priority 3

## Key Files Changed Recently
- `path/to/file` - What changed
```

### Step 5: Archive Previous Session

Create JSON archive for previous session:

```bash
mkdir -p .claude/sessions/archive/YYYY-MM
```

Create `.claude/sessions/archive/YYYY-MM/YYYY-MM-DD-N.json`:
```json
{
  "session_id": "YYYY-MM-DD-N",
  "date": "YYYY-MM-DD",
  "focus": "Brief description",
  "completed": ["Item 1", "Item 2"],
  "commits": [{"sha": "abc123", "message": "..."}],
  "files_modified": ["path/to/file"],
  "next_priorities": ["Priority 1"]
}
```

### Step 6: Commit and Push

```bash
# Stage changes
git add .claude/sessions/ archive/ docs/

# Commit
git commit -m "$(cat <<'EOF'
docs: Session handoff YYYY-MM-DD - [brief description]

- Archived session YYYY-MM-DD-N
- [Summary of cleanup/updates]

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"

# Push
git push origin main
```

### Step 7: Quick Summary Report

```
✅ Quick Handoff Complete!

📦 Cleanup:
- Junk files: X deleted
- Version conflicts: Y resolved
- Documentation: Z files updated

📋 Git: [SHA] → origin/main

🎯 Next: [Priority 1]
```

**Quick handoff complete!** Stop here.

---

## Full Handoff Workflow

Execute ALL steps in order:

### Step 1: Critical Thinking Sanity Check

**Before applying rigid rules, use common sense:**

1. **Scan entire project structure**:
```bash
# Overview of all directories
tree -L 2 -d . 2>/dev/null || find . -type d -maxdepth 2 | grep -v node_modules | grep -v .git | sort

# List root-level files
ls -lah | grep -v "^d"

# Check key folders
ls -lh docs/ .claude/
```

2. **Apply critical thinking** - flag anything that seems:
   - Out of place or illogical
   - Inconsistently named (kebab-case vs snake_case vs PascalCase)
   - Duplicate/redundant (multiple files serving same purpose)
   - Orphaned or disconnected from current work
   - Violates common project organization patterns

3. **Report abnormalities to user**:
   - "These things stood out as potentially odd..."
   - Get user input before proceeding
   - Examples: "Why is there a random .txt file in root?", "These two folders seem to do the same thing"

**Don't proceed until user responds to abnormalities (if any)**

### Step 2: Deep Workspace Audit

Comprehensive scan for cleanup candidates:

```bash
# All junk files
find . -type f \( -name "*.tmp" -o -name "*.bak" -o -name "*~" -o -name "*.swp" -o -name ".DS_Store" \) -not -path "./.git/*" -not -path "*/node_modules/*" -not -path "*/archive/*"

# All potential duplicates
find . -type f \( -name "*-copy.*" -o -name "*-old.*" -o -name "*-backup.*" -o -name "*-v[0-9]*" \) -not -path "./.git/*" -not -path "*/node_modules/*" -not -path "*/archive/*"

# Version conflicts
find docs .claude -type f -name "*.md" | grep -iE "(v2|v3|new|old|copy|backup|optimized|updated|revised)" | grep -v archive

# Empty directories
find . -type d -empty -not -path "./.git/*"
```

Report ALL findings to user before cleanup.

### Step 3: User Confirmation for Cleanup

Present findings:
```
📋 Deep Workspace Audit Results

🗑️ Junk Files (N found):
- ./path/to/file.tmp
- ./another/file.bak

📦 Potential Duplicates (N found):
- ./docs/guide-old.md
- ./docs/guide-v2.md

⚠️ Version Conflicts (N found):
- Multiple versions of X

What would you like me to do?
1. Delete junk files + resolve conflicts (recommended)
2. Archive everything to ./archive/
3. Review each item individually
4. Skip cleanup
```

**Wait for user response. Do NOT proceed without confirmation.**

### Step 4: Execute User-Approved Cleanup

Based on user's choice from Step 3, apply cleanup rules:

**Archive vs Delete decision criteria:**

**Archive** (valuable for future reference):
- Complex analysis with valuable insights
- Architectural decisions and rationale
- Migration documentation (how we got here)
- Major audits with findings/learnings

**Delete** (no reference value):
- Routine audits and status checks
- One-time import documentation (e.g., `*_IMPORT.md`)
- Temporary analysis documents
- Superseded plans without unique insights

**When in doubt**: Delete (it's in Git history)

**Automatic cleanup triggers:**
1. **Audits >3 sessions old**: Archive major audits with insights, delete routine audits
2. **Completed Plans**: Archive if valuable decisions/rationale, otherwise delete
3. **One-time Import Guides**: Delete (no reference value after import complete)
4. **Version Conflicts**: Merge or keep newest, archive/delete old
5. **Superseded Approaches**: Archive if shows evolution, delete if purely historical
6. **Completed Phase Documents**: Archive if valuable insights/metrics, otherwise delete

Execute cleanup:
```bash
# Archive (if valuable for reference)
git mv .claude/MAJOR_AUDIT.md archive/.claude/audits/
git mv docs/MIGRATION_PLAN.md archive/docs/migrations/

# Delete (if no reference value)
git rm docs/ROUTINE_IMPORT.md
git rm .claude/TEMP_ANALYSIS.md
```

### Step 5: Resolve Version Conflicts

For EACH version conflict found:

1. **Read both files** (first 100 lines minimum)
2. **Determine canonical version**: More recent? Complete? Referenced?
3. **Choose action**:
   - **Merge** if both have unique valuable content
   - **Keep newest** if minimal differences
4. **Update references**: Grep for filename, update any references
5. **Archive old ONLY if valuable**, otherwise delete

### Step 6: Validate Against Development Principles

Read `.claude/DEVELOPMENT_PRINCIPLES.md` and validate session work:

- ✅ **LLM-First Architecture**: Tools leverage LLM intelligence, not replace it
- ✅ **Data First**: Preserved data integrity
- ✅ **Progressive Enhancement**: Features work without AI
- ✅ **Complexity Budget**: Kept it simple
- ✅ **Two-Speed Development**: Treated foundation carefully
- ✅ **Context-First Automation**: Workflows query before acting
- ✅ **Cost-Conscious AI Usage**: Optimized prompts and batch operations

Report validation results. Flag any violations or concerns.

### Step 7: Update Related Documentation

Same as Quick Handoff Step 3 - update all docs related to session work.

### Step 8: Update sessions/CURRENT.md

Same as Quick Handoff Step 4 - update with session summary.

### Step 9: Archive Previous Session

Same as Quick Handoff Step 5 - create JSON archive.

### Step 10: Update PROJECT_OVERVIEW.md (if needed)

**Only update if:**
- Major phase completed
- Architecture changed significantly
- Key decision made that affects overall project

Otherwise skip.

### Step 11: Commit and Push

```bash
# Stage all handoff changes
git add .claude/sessions/ archive/ docs/ .claude/PROJECT_OVERVIEW.md

# Commit with detailed message
git commit -m "$(cat <<'EOF'
docs: Session handoff YYYY-MM-DD - [brief description]

- Archived session YYYY-MM-DD-N ([focus])
- Cleaned up X files (deleted), Y files (archived)
- Resolved Z version conflicts
- Updated N documentation files
- Validated against development principles

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"

# Push
git push origin main
```

### Step 12: Full Summary Report

```
✅ Full Handoff Complete!

🧠 Critical Thinking Review:
- Abnormalities noted: N items
- User-directed cleanup: M items

📊 Workspace Audit:
- Deleted: X files (no reference value)
- Archived: Y documents (valuable for reference)
  - Audits: N (insights/learnings)
  - Plans: M (decisions/rationale)
  - Migrations: P (how we got here)
- Version conflicts: Z resolved

✅ Principles Validation:
- LLM-First: [✅ / ⚠️ Notes]
- Data First: [✅ / ⚠️ Notes]
- Progressive Enhancement: [✅ / ⚠️ Notes]
- Complexity Budget: [✅ / ⚠️ Notes]
- Two-Speed Development: [✅ / ⚠️ Notes]
- Context-First Automation: [✅ / ⚠️ Notes]
- Cost-Conscious AI: [✅ / ⚠️ Notes]

📝 Documentation Updated:
- List of updated docs

📦 Session Archived:
- YYYY-MM-DD-N → .claude/sessions/archive/

📋 Git: [SHA] → origin/main

🎯 Next Session Priorities:
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]
```

**Full handoff complete!**

---

## Reference: Information Architecture

### Active Directories - What Belongs Where

**.claude/** - Claude-specific configuration ONLY
```
.claude/
├── CLAUDE.md                    # Quick start guide
├── PROJECT_OVERVIEW.md          # Current architecture
├── DEVELOPMENT_PRINCIPLES.md    # Timeless principles
├── sessions/                    # Session tracking
│   ├── CURRENT.md              # Current state
│   └── archive/YYYY-MM/        # Session JSON archives
├── skills/                      # Skill definitions
└── settings.local.json         # Local settings
```

**docs/** - ALL active project documentation
```
docs/
├── ROADMAP.md                   # Living roadmap
├── MCP_TOOLS_REFERENCE.md       # Current tool reference
├── REST_API_GUIDE.md            # API documentation
├── KNOWN_ISSUES.md              # Active issues
├── N8N_*.md                     # N8N guides (living)
├── APPLE_SHORTCUTS_GUIDE.md     # Integration guides
└── CLAUDE_WEB_MOBILE_SETUP.md   # Setup guides
```

**archive/** - Completed/superseded artifacts (mirrors active structure)
```
archive/
├── README.md                    # Archive policy
├── .claude/                     # Claude artifacts
│   ├── audits/                 # Completed audits
│   └── plans/                  # Completed plans
├── docs/                       # Documentation artifacts
│   ├── analysis/               # Completed analysis
│   ├── audits/                 # System audits (>3 sessions)
│   ├── guides/                 # Superseded guides
│   ├── imports/                # One-time imports
│   ├── migrations/             # Migration docs
│   └── plans/                  # Completed plans
└── [deprecated-folders]/       # Old approaches
```

---

## Reference: Cleanup Philosophy

### Archive vs Delete

**Git is Our Backup** - Archive only if valuable for future reference

**Archive when:**
- Complex analysis with valuable insights
- Architectural decisions and rationale
- Migration documentation (how we got here)
- Major audits with findings/learnings

**Delete when:**
- Routine audits and status checks
- One-time import documentation
- Temporary analysis documents
- Superseded plans without unique insights

**When in doubt**: Delete (it's in Git history if needed)

### Safety Rules

- **Never delete files modified <24h without user confirmation**
- **Never touch**: node_modules, .git, build directories, supabase/functions
- **Always commit before cleanup** - So mistakes are reversible
- **Get user confirmation** before deleting anything in full mode

### Never Clean Up

- Current tool references (MCP_TOOLS_REFERENCE.md)
- Active roadmap (ROADMAP.md)
- Living guides (N8N_SETUP.md, N8N_WORKFLOW_DEVELOPMENT_GUIDE.md)
- KNOWN_ISSUES.md (always active)
- DEVELOPMENT_PRINCIPLES.md (timeless)

---

## Quick Reference

**Session ID Format**: `YYYY-MM-DD-N` (e.g., `2025-12-16-1`)

**Archive Command Pattern**:
```bash
git mv [source] archive/[mirror-path]/
```

**Files to Update Every Handoff**:
1. `.claude/sessions/CURRENT.md` (always)
2. Docs related to session work (context-dependent)
3. `.claude/PROJECT_OVERVIEW.md` (only if major changes)

**Commit Message Pattern**:
```
docs: Session handoff YYYY-MM-DD - [brief description]

- [Summary of changes]

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```
