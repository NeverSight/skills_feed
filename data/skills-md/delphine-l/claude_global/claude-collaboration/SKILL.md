---
name: claude-collaboration
description: Best practices for using Claude Code in team environments. Covers skill management, knowledge capture, version control, and collaborative workflows.
version: 1.0.0
---

# Claude Code Collaboration Best Practices

This skill provides guidance on effectively using Claude Code in team environments, managing shared knowledge through skills, and maximizing value from AI-assisted development.

## Core Principles

1. **Skills are living documentation** - They evolve as you learn
2. **Capture knowledge explicitly** - Claude doesn't auto-update skills
3. **All skills live in $CLAUDE_METADATA** - No local skills or commands in projects
4. **Share knowledge across the team** - Centralized repo ensures consistency
5. **Version control your skills** - Track changes and improvements
6. **Be intentional about updates** - Not everything learned needs to be captured

### Critical: No Local Skills or Commands

**ALL skills and commands MUST be in the $CLAUDE_METADATA repository, never in individual project directories.**

**❌ Never do this:**
```bash
# Creating local skill in project
echo "---" > .claude/skills/my-local-skill/SKILL.md
```

**✅ Always do this:**
```bash
# Create skill in central repo
mkdir -p $CLAUDE_METADATA/skills/project-name
echo "---" > $CLAUDE_METADATA/skills/project-name/SKILL.md

# Then symlink to project
ln -s $CLAUDE_METADATA/skills/project-name .claude/skills/project-name
```

**Why centralization is mandatory:**
- **Version control**: All skills tracked in one git repo
- **Team sharing**: Everyone uses the same knowledge
- **Consistency**: No divergence between projects
- **Maintenance**: Update once, applies everywhere
- **Discovery**: Team can see all available skills

**Even project-specific skills go in the central repo** under `$CLAUDE_METADATA/skills/project-name/`.

---

## Understanding How Skills Work

### What Happens During a Session

**At session start:**
- Claude reads all `.claude/skills/` files in your directory
- Skills provide context and guidelines for the session
- Knowledge from skills is "loaded" into Claude's working context

**During the session:**
- Claude learns from your conversation (temporary, in-context learning)
- Solutions discovered apply only to this conversation
- Skills remain unchanged unless you explicitly update them

**At session end:**
- All temporary learning is lost
- Skills remain exactly as they were at the start
- Next session starts fresh, reading skills again

### What This Means

**✅ Skills persist across sessions** - They're files on disk
**❌ Session learnings don't persist** - They exist only in conversation context
**⚠️ You must explicitly update skills** - Claude won't do it automatically

---

## When to Update Skills

### Always Update Skills For:

1. **Repeated problems with known solutions**
   - "We keep hitting this error, here's how to fix it"
   - Add to troubleshooting section

2. **New best practices discovered**
   - "Using --quiet saves 85% tokens, use it by default"
   - Add to optimization guidelines

3. **Common workflows that need standardization**
   - "Our team always does X before Y"
   - Add to standard procedures

4. **Configuration patterns that work**
   - "This cron job setup works best for our HPC"
   - Add as recommended configuration

5. **Important architectural decisions**
   - "We decided to use symlinks for global skills because..."
   - Document rationale for future reference

### Don't Update Skills For:

1. **One-time issues** - Specific to a particular run or environment
2. **Experimental approaches** - Wait until proven effective
3. **User-specific preferences** - Unless they should be team defaults
4. **Obvious information** - Already well-documented elsewhere
5. **Temporary workarounds** - Not worth making permanent

### Example: When to Update

**Scenario 1: New error pattern discovered**
```
Session: "WF8 fails when Hi-C files are missing R2 reads"
Action: ✅ ADD to troubleshooting - this will happen again
Rationale: Common issue with known solution
```

**Scenario 2: One-off configuration issue**
```
Session: "My personal laptop has Python 3.7, need 3.8"
Action: ❌ DON'T ADD to skill - personal environment issue
Rationale: Not relevant to others, not a recurring pattern
```

**Scenario 3: Token optimization discovered**
```
Session: "Using --quiet mode saves 15K → 2K tokens!"
Action: ✅ ADD to token efficiency skill
Rationale: Valuable for entire team, significant impact
```

---

## How to Update Skills

### Method 1: Explicit Request (Recommended)

```
User: "We just solved the issue with workflow timeouts in HPC environments.
       Add this to the VGP skill under troubleshooting."

Claude: [Reads current skill, adds new troubleshooting entry, saves file]
```

**Benefits:**
- You control what gets captured
- You review the update
- Clear and intentional

### Method 2: Ask Claude to Suggest Updates

```
User: "Based on our work today, what should we add to the VGP skill?"

Claude: [Reviews conversation, suggests additions]

User: "Yes, add those three things."

Claude: [Updates skill file]
```

**Benefits:**
- Claude identifies patterns you might miss
- Quick end-of-session review
- Collaborative approach

### Method 3: End-of-Session Summary

```
User: "Summarize today's learnings and update the relevant skills."

Claude: [Creates summary, updates multiple skills if needed]
```

**Benefits:**
- Batch updates
- Comprehensive capture
- Good for long sessions

### Method 4: Periodic Review

```
User: "We've been working on VGP for a month.
       Review our conversation history and suggest skill improvements."

Claude: [Analyzes patterns, suggests updates]
```

**Benefits:**
- Catches accumulated knowledge
- Identifies trends
- Good for major skill overhauls

---

## Skill Organization Patterns

### Pattern 1: Project-Specific Skills (In Central Repo)

**Use for:**
- Project-specific knowledge (VGP workflows, Galaxy APIs)
- Custom tooling and scripts
- Domain-specific patterns

**Location:** `$CLAUDE_METADATA/skills/project-name/` (NOT in project directory)

**Example:**
```
$CLAUDE_METADATA/
└── skills/
    ├── my-project/              # Project-specific skill
    │   └── SKILL.md
    └── another-project/         # Another project-specific skill
        └── SKILL.md

my-project/
└── .claude/
    └── skills/
        └── my-project -> $CLAUDE_METADATA/skills/my-project  # Symlink only!
```

**Important:** Even project-specific skills live in the central repo and are symlinked to projects.

### Pattern 2: General Skills (Cross-Project)

**Use for:**
- General development practices
- Tool-agnostic optimizations (token efficiency)
- Team-wide standards

**Location:** `$CLAUDE_METADATA/skills/`

**Example:**
```
$CLAUDE_METADATA/skills/
├── token-efficiency/
│   └── SKILL.md
├── claude-collaboration/
│   └── SKILL.md
└── python-testing-patterns/
    └── SKILL.md
```

### Pattern 3: Symlinking Skills to Projects

**This is THE standard pattern - all projects use symlinks, no exceptions.**

**Setup:**
```bash
# In each project
cd /path/to/project
mkdir -p .claude/skills .claude/commands

# Symlink skills from central repo
ln -s $CLAUDE_METADATA/skills/token-efficiency .claude/skills/token-efficiency
ln -s $CLAUDE_METADATA/skills/my-project .claude/skills/my-project

# Symlink commands from central repo
ln -s $CLAUDE_METADATA/commands/global/*.md .claude/commands/
```

**Benefits:**
- Update once, applies everywhere
- Consistent across all projects
- Easy to maintain
- Version controlled in one place
- Team can discover all skills

**Critical rule:** Projects contain ONLY symlinks, never actual skill/command files.

### Pattern 4: Skills with Supporting Documentation

**Structure:**
```
skills/skill-name/
├── SKILL.md              # Core concepts and quick reference
├── reference.md          # Detailed technical documentation
├── troubleshooting.md    # Common issues and solutions
├── examples/             # Code examples
└── templates/            # Template files
```

**When to use:**
- SKILL.md is getting too long (>1000 lines)
- Detailed reference material available
- Multiple categories of information (guides, troubleshooting, examples)

**Progressive disclosure benefit:**
- Claude sees SKILL.md description always (minimal tokens)
- Supporting files only loaded when skill activated
- Deep details available without cluttering main skill

**Example - galaxy-tool-wrapping:**
```markdown
## Supporting Documentation

This skill includes detailed reference documentation:

- **reference.md** - Comprehensive Galaxy tool wrapping guide
- **troubleshooting.md** - Practical troubleshooting guide
- **dependency-debugging.md** - Dependency conflict resolution

These files provide deep technical details that complement the core concepts above.
```

**Best practice:**
- Keep SKILL.md under 500 lines if possible
- Move detailed guides to supporting files
- Reference supporting files at end of SKILL.md
- Use descriptive filenames (troubleshooting.md, not tips.md)

---

## Centralized Skill Repository Pattern

**Problem**: Managing skills across multiple projects leads to duplication and maintenance overhead.

**Solution**: Use a centralized repository with selective symlinks and environment variables.

### Setup

1. **Create central repository**:
   ```bash
   mkdir -p $CLAUDE_METADATA/{skills,commands}
   ```

2. **Set environment variable** in `~/.zshrc`:
   ```bash
   export CLAUDE_METADATA="$CLAUDE_METADATA"
   ```

3. **Organize by domain**:
   ```
   $CLAUDE_METADATA/
   ├── skills/
   │   ├── domain-1/SKILL.md
   │   └── domain-2/SKILL.md
   └── commands/
       └── category/
           └── command.md
   ```

### Per-Project Activation

**Key principle**: Only symlink skills needed for each project

```bash
# In project directory
ln -s $CLAUDE_METADATA/skills/domain-1 .claude/skills/domain-1
ln -s $CLAUDE_METADATA/commands/category/*.md .claude/commands/
```

### Benefits

- **No performance penalty**: Progressive disclosure loads skills only when activated
- **Selective activation**: Each project sees only relevant skills
- **Easy maintenance**: Update once, all projects benefit
- **Portable**: Change location via environment variable
- **Team-friendly**: Commit symlinks, team members use their own central repo

### Standardized Setup Prompts

Provide users with copy-paste prompts for new projects in `$CLAUDE_METADATA/QUICK_REFERENCE.md`:

**Basic setup**:
```
Set up Claude Code for this project. Show me available skills in $CLAUDE_METADATA and let me choose which ones to symlink.
```

**Sync existing project**:
```
Check what skills and commands are available in $CLAUDE_METADATA and compare with what's currently symlinked in this project. Show me what's new or missing, and let me choose which ones to add.
```

**VGP-specific**:
```
Set up Claude Code for a VGP pipeline project. Symlink the vgp-pipeline skill and all VGP commands from $CLAUDE_METADATA.
```

### Example Directory Structure

```
$CLAUDE_METADATA/
├── README.md                    # Setup documentation
├── QUICK_REFERENCE.md           # Copy-paste prompts for users
├── NEW_MACHINE_SETUP.md         # First-time machine setup
├── skills/                      # ALL skills (general + project-specific)
│   ├── token-efficiency/        # General skill
│   │   └── SKILL.md
│   ├── claude-collaboration/    # General skill
│   │   └── SKILL.md
│   ├── vgp-pipeline/           # Project-specific skill
│   │   └── SKILL.md
│   └── galaxy-tool-wrapping/   # Domain skill
│       └── SKILL.md
└── commands/                    # ALL commands
    ├── global/                  # Commands for all projects
    │   ├── update-skills.md
    │   └── sync-skills.md
    └── vgp-pipeline/           # Project-specific commands
        ├── check-status.md
        └── debug-failed.md
```

**Key point:** ALL skills and commands live in this central repo. Projects contain only symlinks.

### Migration Pattern

**From duplicated or local skills** (old/wrong way):
```
project-1/.claude/skills/my-skill/SKILL.md          # ❌ Duplicate!
project-2/.claude/skills/my-skill/SKILL.md          # ❌ Duplicate!
project-3/.claude/skills/project-specific/SKILL.md  # ❌ Local only!
```

**To centralized skills** (correct way):
```
$CLAUDE_METADATA/skills/my-skill/SKILL.md          # ✅ Single source of truth
$CLAUDE_METADATA/skills/project-specific/SKILL.md  # ✅ Even project-specific!

project-1/.claude/skills/my-skill -> $CLAUDE_METADATA/skills/my-skill
project-2/.claude/skills/my-skill -> $CLAUDE_METADATA/skills/my-skill
project-3/.claude/skills/project-specific -> $CLAUDE_METADATA/skills/project-specific
```

**Critical rule:** ALL skills in $CLAUDE_METADATA, even if only used by one project.

### Team Workflow

1. **Central repo is git-tracked**:
   ```bash
   cd $CLAUDE_METADATA
   git init
   git remote add origin git@github.com:team/claude-metadata.git
   ```

2. **Team members clone**:
   ```bash
   git clone git@github.com:team/claude-metadata.git $CLAUDE_METADATA
   export CLAUDE_METADATA="$CLAUDE_METADATA"
   ```

3. **Projects use symlinks**:
   ```bash
   # Commit symlinks to project repos
   git add .claude/
   git commit -m "Add Claude Code skill symlinks"
   ```

4. **Updates propagate automatically**:
   ```bash
   # Update central skills
   cd $CLAUDE_METADATA
   git pull

   # All projects with symlinks now use updated skills! 🎉
   ```

---

## Version Control for Skills

### Why Version Control Skills?

1. **Track evolution** - See how knowledge grows over time
2. **Review changes** - Understand what was added and why
3. **Rollback mistakes** - Undo bad updates
4. **Share with team** - Everyone uses same skills
5. **Audit trail** - Know who added what when

### Setup Git for Global Skills

```bash
cd $CLAUDE_METADATA
git init
git add .claude/
git commit -m "Initial skills: token-efficiency, claude-collaboration"

# Optional: Push to GitHub for team sharing
git remote add origin git@github.com:your-team/claude-skills.git
git push -u origin main
```

### Workflow for Skill Updates

```bash
# Before making changes
cd $CLAUDE_METADATA
git status  # See current state

# After Claude updates a skill
git diff  # Review changes

# If changes look good
git add .claude/skills/
git commit -m "Add WF8 Hi-C troubleshooting pattern"
git push

# If changes are wrong
git checkout -- .claude/skills/token-efficiency/SKILL.md  # Undo
```

### Team Collaboration

```bash
# Team member pulls latest skills
cd $CLAUDE_METADATA
git pull

# All symlinked projects auto-update! 🎉

# Team member adds their own learning
# (Claude updates skill based on their session)
git add .
git commit -m "Add HPC-specific cron patterns"
git push

# Other team members pull and benefit
git pull
```

---

## Sharing Skills with Team

### Method 1: Git Repository (Recommended)

**Setup:**
```bash
# Create shared skills repo
mkdir claude-team-skills
cd claude-team-skills
mkdir -p .claude/skills

# Add initial skills
cp -r $CLAUDE_METADATA/skills/* .claude/skills/

# Initialize git
git init
git add .
git commit -m "Initial team skills"
git remote add origin git@github.com:your-org/claude-team-skills.git
git push -u origin main
```

**Team members use:**
```bash
# Clone shared skills
git clone git@github.com:your-org/claude-team-skills.git ~/claude-team-skills

# Link to their projects
cd /path/to/project
ln -s ~/claude-team-skills/.claude/skills/token-efficiency .claude/skills/token-efficiency

# Stay updated
cd ~/claude-team-skills
git pull  # Periodically pull updates
```

### Method 2: Shared Network Drive

**Setup:**
```bash
# Create skills on shared drive
mkdir /mnt/shared/claude-skills/.claude/skills

# Team members symlink
ln -s /mnt/shared/claude-skills/.claude/skills/token-efficiency .claude/skills/token-efficiency
```

**Pros:** Simple, immediate updates
**Cons:** No version control, risk of conflicts

### Method 3: Copy-Based (Simple but Manual)

**Setup:**
```bash
# Share skills file via email/Slack
# Team members copy to their projects
cp received-skill.md .claude/skills/my-skill/SKILL.md
```

**Pros:** Simple, no infrastructure needed
**Cons:** No automatic updates, easy to diverge

---

## Best Practices for Skill Maintenance

### 1. Regular Review Sessions

**Weekly quick review:**
```
"Review this week's work and suggest skill updates"
```

**Monthly deep review:**
```
"Analyze patterns from this month's sessions and propose major skill improvements"
```

### 2. Clear Update Messages

**Good commit messages:**
```
git commit -m "Add token optimization for VGP log files (96% savings)"
git commit -m "Document WF8 failure pattern when Hi-C R2 missing"
git commit -m "Add HPC cron job environment setup"
```

**Bad commit messages:**
```
git commit -m "update skill"
git commit -m "fixes"
git commit -m "stuff"
```

### 3. Keep Skills Focused

**Good:** One skill per topic
- `token-efficiency.md` - Only token optimization
- `vgp-troubleshooting.md` - Only VGP issues
- `deployment.md` - Only deployment procedures

**Bad:** Kitchen sink skills
- `everything.md` - Token optimization + VGP + deployment + testing + ...
- Hard to maintain, hard to use

### 4. Document Rationale

**Include "why" not just "what":**

```markdown
## Use --quiet Mode by Default

**Why:** VGP status checks produce 15K tokens of output with verbose mode,
but only 2K with --quiet mode. Over a typical workflow (10 status checks),
this saves 130K tokens (87% reduction).

**When to override:** User explicitly requests detailed output, or debugging
requires seeing all intermediate steps.
```

### 5. Prioritize High-Impact Knowledge

**Capture first:**
- Patterns that save significant time/tokens
- Solutions to common, repeated problems
- Critical configuration requirements
- Team-wide standards

**Capture later:**
- Nice-to-know information
- Rarely-used edge cases
- Obvious procedures

---

## Measuring Skill Effectiveness

### Signs Your Skills Are Working

1. **Fewer repeated questions** - Claude knows the answer from skills
2. **Consistent behavior** - Claude follows team patterns automatically
3. **Faster onboarding** - New team members get instant context
4. **Token efficiency** - Optimizations applied automatically
5. **Better debugging** - Known issues resolved quickly

### Signs Skills Need Improvement

1. **Claude ignores guidelines** - Skills aren't clear or prominent enough
2. **Repeated manual corrections** - Patterns not captured in skills
3. **Team divergence** - Different team members do things differently
4. **Outdated information** - Skills reference old tools/patterns
5. **Too verbose** - Skills are too long, key info buried

### Metrics to Track

**Before/after comparison:**
```
Before token-efficiency skill:
- Average status check: 15K tokens
- Weekly VGP monitoring: 60K tokens

After token-efficiency skill:
- Average status check: 2K tokens (87% reduction)
- Weekly VGP monitoring: 8K tokens (87% reduction)
```

**Knowledge retention:**
```
Before skill updates:
- Same question asked 5 times over 2 months

After skill update:
- Question answered correctly from skill every time
```

---

## Common Pitfalls and Solutions

### Pitfall 1: Forgetting to Update Skills

**Problem:** Valuable knowledge stays in conversation, gets lost

**Solution:** End-of-session ritual
```
Last message every session:
"What did we learn today that should go in our skills?"
```

### Pitfall 2: Skills Become Too Long

**Problem:** Skills are 10,000+ lines, Claude can't find key info

**Solution:** Split into focused sub-skills
```
Before: vgp-everything.md (10K lines)
After:
  - vgp-setup.md (2K lines)
  - vgp-troubleshooting.md (3K lines)
  - vgp-optimization.md (2K lines)
```

### Pitfall 3: Skills Conflict

**Problem:** Multiple skills give contradictory advice

**Solution:** Regular conflict audits
```
"Review all my skills and identify any conflicting guidelines"
```

### Pitfall 4: No Version Control

**Problem:** Can't undo bad changes, can't see history

**Solution:** Set up git from day one
```bash
cd $CLAUDE_METADATA
git init
git add .claude/
git commit -m "Initial skills"
```

### Pitfall 5: Skills Not Shared

**Problem:** Each team member has different skills, inconsistent behavior

**Solution:** Use shared git repo or symlinks
```bash
# Team repo for skills
git clone git@github.com:team/claude-skills.git ~/claude-team-skills

# Each project links to shared skills
ln -s ~/claude-team-skills/.claude/skills/* .claude/skills/
```

---

## Advanced Patterns

### Pattern 1: Tiered Skills (Beginner → Expert)

**Beginner skill:**
```markdown
# VGP Basics
- What VGP workflows are
- How to run simple commands
- Basic troubleshooting
```

**Expert skill:**
```markdown
# VGP Advanced
- Architecture internals
- Custom workflow modifications
- Performance tuning
```

**Usage:** Load appropriate tier based on user expertise

### Pattern 2: Conditional Skills (Environment-Specific)

**Development skill:**
```markdown
# Development Mode
- Use test datasets
- Enable verbose logging
- Skip certain validations
```

**Production skill:**
```markdown
# Production Mode
- Use --quiet mode
- Enable all validations
- Follow strict procedures
```

**Usage:** Swap skills based on environment

### Pattern 3: Role-Based Skills

**For users:**
```markdown
# User Guide
- How to run workflows
- Common commands
- Troubleshooting
```

**For developers:**
```markdown
# Developer Guide
- Code architecture
- How to add new workflows
- Testing patterns
```

**Usage:** Different skills for different team roles

---

## Documentation for Session Interruptions

### Creating Resume Documentation

When working on long-running tasks that may span multiple sessions, create comprehensive documentation to enable seamless resume:

**Three-tier documentation approach**:

1. **RESUME_HERE.md** - Quick start guide
   - 3-5 step quick start
   - Essential commands only
   - Clear current status
   - Visual indicators (✅🔄⏸️ emojis)

2. **PROJECT_STATUS.md** - Complete context
   - What has been done
   - What's in progress
   - What's next
   - All files created
   - Key findings
   - Sample of missing data points

3. **scripts/README.md** - Technical details
   - Script documentation
   - How to run each tool
   - Troubleshooting
   - Expected outputs

### Template: RESUME_HERE.md

```markdown
# 🔄 Resume [Project Name]

## Current Status
✅ Completed: [brief status with metrics]
🔄 In Progress: [what's running, % complete]
⏸️ Interrupted at: [specific point with details]

## Resume in 3 Steps

### 1️⃣ Setup
\```bash
cd /path/to/project
conda activate env_name
\```

### 2️⃣ Continue work
\```bash
./script.py  # Brief explanation of what this does
\```

### 3️⃣ Check results
\```bash
# Quick validation command with expected output
\```

## Full Documentation
📄 **PROJECT_STATUS.md** - Complete context
📄 **scripts/README.md** - Technical details
```

### Best Practices

1. **Create early**: Don't wait until interruption is imminent
   - Create documentation as you work
   - Update it throughout the session

2. **Test commands**: Verify resume commands actually work
   - Don't assume paths or commands will work
   - Include absolute paths when needed

3. **Status tracking**: Include counts, percentages, specific progress points
   - "6% complete (31/518 species)" not just "in progress"
   - Show what's done vs. what remains

4. **Next actions**: Be explicit about what happens next
   - "Run script X, then merge with Y, then verify with Z"
   - Include expected runtime

5. **Background processes**: Document how to check/resume running processes
   - Process IDs if applicable
   - How to check status
   - How to restart if needed

### Example: Long-Running Data Fetch Project

```markdown
# 🔄 Resume GenomeScope Data Retrieval

## Current Status
✅ **123 species** have GenomeScope data (17.2% of 716 total)
🔄 **Comprehensive search was running** - searches all assembly folders
⏸️ **Interrupted at ~6% progress** (31/518 remaining species)

## Resume in 3 Steps

### 1️⃣ Navigate and activate environment
\```bash
cd /Users/user/project
conda activate curation_paper
\```

### 2️⃣ Resume comprehensive search
\```bash
# This will pick up where we left off (skips existing data automatically)
python scripts/03c_comprehensive_genomescope_search.py
# Expected runtime: ~2 hours
\```

### 3️⃣ Merge new data (after search completes)
\```bash
python scripts/04_merge_and_enrich.py
\```

## Files Already Created
- genomescope_data/ - 123 raw summary files
- genomescope_enrichment_data.csv - Parsed data
- VGPPhase1-freeze-1.0-ENRICHED.csv - Main dataset

## Full Documentation
📄 **GENOMESCOPE_DATA_RETRIEVAL_STATUS.md** - Complete status
📄 **scripts/README_GENOMESCOPE_SCRIPTS.md** - Script docs
```

### When to Create Resume Documentation

**Always create when:**
- Task will take hours to complete
- Running scripts that can be interrupted
- Multiple scripts need to be run in sequence
- Complex setup with multiple steps
- Work may span multiple days/sessions

**Pattern ensures:**
- Anyone (including you later) can resume work
- No mental overhead to remember state
- Clear next steps visible immediately
- All context preserved

---

## Quick Reference

### Daily Workflow

```
1. Start session → Claude reads skills
2. Work on task → Learn new patterns
3. End session → "What should we add to skills?"
4. Claude suggests → You approve/modify
5. Git commit → Share with team
```

### Weekly Maintenance

```
1. Review week's commits
2. Identify patterns across sessions
3. Consolidate related updates
4. Remove outdated info
5. Share changelog with team
```

### Monthly Review

```
1. Audit all skills for conflicts
2. Measure token savings
3. Collect team feedback
4. Major refactoring if needed
5. Update skill documentation
```

---

## Summary

**Key Principles:**
1. **Skills are permanent, sessions are temporary**
2. **Update skills explicitly** - Claude won't auto-update
3. **ALL skills in $CLAUDE_METADATA** - No local skills or commands ever
4. **Version control your skills** with git in central repo
5. **Share skills across team** - Centralization ensures consistency
6. **Regular reviews** keep skills valuable

**Critical Architectural Rule:**
🚫 **NEVER create skills or commands directly in project directories**
✅ **ALWAYS create in $CLAUDE_METADATA and symlink to projects**

Even project-specific skills must live in the central repository. This ensures:
- **Single source of truth** - No duplicates, no divergence
- **Version control** - All skills tracked in one git repo
- **Team sharing** - Everyone can discover and use all skills
- **Easy maintenance** - Update once, applies everywhere

**Remember:** Claude is a powerful assistant, but skills are how you make that power consistent, shareable, and permanent. The centralized architecture ensures your team's knowledge remains organized, discoverable, and maintainable. Invest in your skills, and they'll pay dividends for your entire team.
