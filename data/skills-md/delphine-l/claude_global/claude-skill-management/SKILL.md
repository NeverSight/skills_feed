---
name: claude-skill-management
description: Expert guide for managing Claude Code global skills and commands. Use when creating new skills, symlinking to projects, updating existing skills, or organizing the centralized skill repository.
---

# Claude Code Skill Management Expert

Expert knowledge for managing Claude Code skills and commands using the centralized repository pattern with `$CLAUDE_METADATA`.

## When to Use This Skill

- Creating new global skills or commands
- Setting up skills for a new project
- Synchronizing projects with updated global skills
- Organizing the centralized skill repository
- Troubleshooting skill discovery or activation issues
- Understanding the skill lifecycle

## Environment Setup

### Required Environment Variable

**`$CLAUDE_METADATA`** must be set to your centralized skills directory.

**Check if set:**
```bash
echo $CLAUDE_METADATA
# Should output your claude_data directory path
```

**If not set, add to `~/.zshrc` (or `~/.bashrc`):**
```bash
export CLAUDE_METADATA="$HOME/path/to/claude_data"  # Adjust to your actual path
```

**Apply immediately:**
```bash
source ~/.zshrc  # or source ~/.bashrc
```

### Verify Directory Structure

```bash
ls -la $CLAUDE_METADATA/
# Should show:
# ├── skills/       # Global skills
# ├── commands/     # Global commands
# ├── README.md
# └── QUICK_REFERENCE.md
```

### Complete Setup from Scratch

If setting up a centralized skill repository for the first time:

1. **Create directory structure**:
   ```bash
   mkdir -p $CLAUDE_METADATA/{skills,commands}
   cd $CLAUDE_METADATA
   ```

2. **Set environment variable** (add to `~/.zshrc` or `~/.bashrc`):
   ```bash
   echo 'export CLAUDE_METADATA="$HOME/path/to/claude_data"  # Adjust to your actual path' >> ~/.zshrc
   source ~/.zshrc
   ```

3. **Verify setup**:
   ```bash
   echo $CLAUDE_METADATA
   # Should output your claude_data directory path
   ```

4. **Create initial documentation**:
   ```bash
   # Create README and QUICK_REFERENCE
   # (use templates from claude-skill-management skill)
   ```

5. **Initialize git** (recommended):
   ```bash
   cd $CLAUDE_METADATA
   git init
   git add .
   git commit -m "Initial centralized skill repository"
   ```

6. **Create your first skill**:
   ```bash
   mkdir -p $CLAUDE_METADATA/skills/my-first-skill
   # Create SKILL.md with frontmatter
   ```

7. **Link to first project**:
   ```bash
   cd ~/Workdir/my-project
   mkdir -p .claude/skills
   ln -s $CLAUDE_METADATA/skills/my-first-skill .claude/skills/
   ```

**Environment variable best practices:**
- Use `$HOME` not hardcoded paths for portability
- Source shell config after adding: `source ~/.zshrc`
- Verify in new terminals: `echo $CLAUDE_METADATA`
- Document for team members in README.md

---

## Creating New Skills

### Step 1: Create Skill Directory

```bash
mkdir -p $CLAUDE_METADATA/skills/your-skill-name
```

**Naming conventions:**
- Use `kebab-case` (lowercase with hyphens)
- Be descriptive but concise
- Examples: `galaxy-tool-wrapping`, `python-testing`, `docker-workflows`

### Step 2: Create SKILL.md with Frontmatter

```bash
cat > $CLAUDE_METADATA/skills/your-skill-name/SKILL.md << 'EOF'
---
name: your-skill-name
description: Brief description that helps Claude decide when to activate this skill (1-2 sentences)
---

# Your Skill Name

Detailed instructions for Claude when this skill is activated.

## When to Use This Skill

- Specific use case 1
- Specific use case 2
- Specific use case 3

## Core Concepts

### Concept 1

Explanation and examples...

### Concept 2

Explanation and examples...

## Best Practices

- Practice 1
- Practice 2

## Common Issues and Solutions

### Issue 1

**Problem:** Description
**Solution:** How to fix it

## Examples

### Example 1: Task Name

Description and code examples...
EOF
```

**Frontmatter fields:**
- `name` (required): Must match directory name
- `description` (required): Clear, concise description for activation
- `version` (optional): Semantic versioning (e.g., `1.0.0`)
- `dependencies` (optional): Required tools/packages

### Step 3: Add Supporting Files (Optional)

```bash
# Add detailed reference documentation
cat > $CLAUDE_METADATA/skills/your-skill-name/reference.md << 'EOF'
# Reference Documentation

Detailed technical information, API references, etc.
EOF

# Add examples directory
mkdir -p $CLAUDE_METADATA/skills/your-skill-name/examples

# Add templates directory
mkdir -p $CLAUDE_METADATA/skills/your-skill-name/templates
```

### Step 4: Test the Skill

```bash
# Create a test project
mkdir -p /tmp/test-skill-project/.claude/skills

# Symlink the new skill
ln -s $CLAUDE_METADATA/skills/your-skill-name /tmp/test-skill-project/.claude/skills/your-skill-name

# Start Claude Code in test project
cd /tmp/test-skill-project
# Tell Claude: "Use the your-skill-name skill to [test task]"
```

---

## Creating New Commands

### Step 1: Choose or Create Category Directory

```bash
# Use existing category
ls $CLAUDE_METADATA/commands/
# Or create new category
mkdir -p $CLAUDE_METADATA/commands/your-category
```

**Common categories:**
- `vgp-pipeline/` - VGP workflow commands
- `git-workflows/` - Git-related commands
- `testing/` - Testing-related commands
- `deployment/` - Deployment commands

### Step 2: Create Command File

```bash
cat > $CLAUDE_METADATA/commands/your-category/command-name.md << 'EOF'
---
name: command-name
description: Brief description shown in /help
---

Your command prompt here. This will be expanded when the user types /command-name.

You can include:
- Multi-line instructions
- Variable references: {{variable_name}}
- Markdown formatting
- Code blocks

Example:
Check the status of all workflows for species {{species_name}}.
Show me which workflows are complete, running, or failed.
EOF
```

**Naming conventions:**
- Use `kebab-case`
- Start with verb: `check-status`, `debug-failed`, `update-skills`
- Be specific: `deploy-production` not just `deploy`

### Step 3: Test the Command

```bash
# Symlink to test project
ln -s $CLAUDE_METADATA/commands/your-category/command-name.md /tmp/test-project/.claude/commands/

# Start Claude Code and test
# Type: /command-name
```

---

## Symlinking Skills and Commands to Projects

### Recommended Global Skills (Always Symlink These)

**Every new project should include these globally useful skills:**

#### 1. token-efficiency (Essential)
**Why:** Automatically optimizes Claude's token usage, saving 80-90% on typical operations
```bash
ln -s $CLAUDE_METADATA/skills/token-efficiency .claude/skills/token-efficiency
```

**Benefits:**
- Uses `--quiet` mode for commands automatically
- Reads log files efficiently (tail/grep instead of full read)
- Strategic file selection for learning mode
- Extends your Claude Pro usage 5-10x

#### 2. claude-collaboration (Highly Recommended)
**Why:** Teaches best practices for managing skills and team collaboration
```bash
ln -s $CLAUDE_METADATA/skills/claude-collaboration .claude/skills/claude-collaboration
```

**Benefits:**
- Explains when and how to update skills
- Documents skill lifecycle and version control
- Helps onboard team members
- Ensures consistency across projects

#### 3. galaxy-automation (For Galaxy projects)
**Why:** Universal BioBlend and Planemo knowledge for any Galaxy automation project
```bash
ln -s $CLAUDE_METADATA/skills/galaxy-automation .claude/skills/galaxy-automation
```

**Benefits:**
- Foundation for Galaxy workflow automation
- Required dependency for vgp-pipeline
- Useful for galaxy-tool-wrapping (Planemo testing)
- Reduces duplication across Galaxy-related skills

#### 4. Recommended Global Commands (Highly Recommended)
**Useful for managing skills across all projects:**
```bash
mkdir -p .claude/commands
# Symlink ALL global commands (always include)
ln -s $CLAUDE_METADATA/commands/global/*.md .claude/commands/



```

**Available commands:**
- `/update-skills` - Review session and suggest skill updates
- `/list-skills` - Show all available skills in $CLAUDE_METADATA
- `/setup-project` - Set up a new project with intelligent defaults
- `/sync-skills` - Check for new skills/commands added to $CLAUDE_METADATA
- `/cleanup-project` - End-of-project cleanup (working docs, verbose READMEs)

#### Quick Setup for Both Skills and Commands
```bash
# Navigate to your new project
cd ~/Workdir/your-new-project/

# Create .claude directories
mkdir -p .claude/skills .claude/commands

# Symlink essential global skills
ln -s $CLAUDE_METADATA/skills/token-efficiency .claude/skills/token-efficiency
ln -s $CLAUDE_METADATA/skills/claude-collaboration .claude/skills/claude-collaboration
ln -s $CLAUDE_METADATA/skills/python-environment-management .claude/skills/python-environment-management

# Symlink ALL global commands (always include)
ln -s $CLAUDE_METADATA/commands/global/*.md .claude/commands/

# Add project-specific skills as needed
# For Galaxy projects:
# ln -s $CLAUDE_METADATA/skills/galaxy-automation .claude/skills/galaxy-automation



# Verify
ls -la .claude/skills/
ls -la .claude/commands/
```

**Or ask Claude:**
```
Set up this new project with Claude Code. Symlink the essential global skills
(token-efficiency, claude-collaboration, and python-environment-management) and global commands
from $CLAUDE_METADATA/skills/ and ALL global commands from $CLAUDE_METADATA/commands/global/, then show me
other available skills I might want to add.
```

**Or simply use:**
```
/setup-project
```
(if the setup-project command is already symlinked)

---

### Method 1: Quick Setup (Recommended for New Projects)

**Tell Claude:**
```
Set up Claude Code for this project. Show me available skills in $CLAUDE_METADATA and let me choose which ones to symlink.
```

Claude will:
1. **Automatically symlink token-efficiency, claude-collaboration, python-environment-management** (if not already present)
2. List all available skills and commands
3. Ask which additional ones you want
4. Create the symlinks
5. Verify everything works

### Method 2: Manual Symlink (Specific Skills)

```bash
# Navigate to your project
cd ~/Workdir/your-project/

# Create directories if needed
mkdir -p .claude/skills .claude/commands

# Symlink specific skill
ln -s $CLAUDE_METADATA/skills/skill-name .claude/skills/skill-name

# Symlink all commands from a category
ln -s $CLAUDE_METADATA/commands/category/*.md .claude/commands/

# Symlink specific command
ln -s $CLAUDE_METADATA/commands/category/command-name.md .claude/commands/command-name.md
```

### Method 3: Symlink All Skills

```bash
# Link every skill (use cautiously)
for skill in $CLAUDE_METADATA/skills/*; do
    ln -s "$skill" .claude/skills/$(basename "$skill")
done

# Link all commands from all categories
for category in $CLAUDE_METADATA/commands/*; do
    ln -s "$category"/*.md .claude/commands/
done
```

**Note:** Progressive disclosure means having many skills doesn't hurt performance, but keep projects focused on relevant skills for clarity.

### Verify Symlinks

```bash
# Check what's linked
ls -la .claude/skills/
ls -la .claude/commands/

# Verify targets exist
ls -L .claude/skills/    # Follows symlinks
```

---

## Updating Existing Skills

### When to Update Skills

**Update when you discover:**
- ✅ Repeated patterns or solutions
- ✅ New best practices
- ✅ Common errors and their fixes
- ✅ Token optimizations
- ✅ Workflow improvements

**Don't update for:**
- ❌ One-time issues
- ❌ Experimental approaches (wait until proven)
- ❌ User-specific preferences
- ❌ Obvious information

### Method 1: Direct Editing

```bash
# Edit the skill file
nano $CLAUDE_METADATA/skills/skill-name/SKILL.md

# Or use Claude
# Tell Claude: "Update the skill-name skill to add [new information]"
```

### Method 2: Use /update-skills Command

```bash
# If you have the update-skills command linked
/update-skills

# Claude will:
# 1. Review your session
# 2. Suggest skill updates
# 3. Ask for approval
# 4. Apply changes
```

### Method 3: End-of-Session Updates

**Tell Claude:**
```
Review today's session and suggest updates to relevant skills in $CLAUDE_METADATA.
```

### Propagation of Updates

**Automatic propagation:**
```bash
# Update skill in central location
vim $CLAUDE_METADATA/skills/vgp-pipeline/SKILL.md

# ALL projects with symlinks immediately see the update! 🎉
# No need to update each project individually
```

---

## Synchronizing Projects with Global Skills

### Scenario: Added New Skills to $CLAUDE_METADATA

**Tell Claude (in existing project):**
```
Check what skills and commands are available in $CLAUDE_METADATA and compare with what's currently symlinked in this project. Show me what's new or missing, and let me choose which ones to add.
```

Claude will:
1. List current symlinks
2. List available skills in `$CLAUDE_METADATA`
3. Show what's new
4. Create symlinks for selected items

### Manual Sync

```bash
# List available skills
ls $CLAUDE_METADATA/skills/

# List what you have
ls .claude/skills/

# Add missing ones
ln -s $CLAUDE_METADATA/skills/new-skill .claude/skills/new-skill
```

---

## Organizing the Centralized Repository

### Directory Organization Best Practices

**By domain/technology:**
```
$CLAUDE_METADATA/skills/
├── vgp-pipeline/              # VGP workflows
├── galaxy-tool-wrapping/      # Galaxy development
├── python-testing/            # Python test patterns
├── docker-workflows/          # Docker/containers
└── bioinformatics-common/     # General bioinformatics
```

**By function:**
```
$CLAUDE_METADATA/commands/
├── vgp-pipeline/              # VGP-specific commands
│   ├── check-status.md
│   └── debug-failed.md
├── git-workflows/             # Git commands
│   └── review-commits.md
└── deployment/                # Deployment commands
    └── deploy-production.md
```

### Naming Consistency

**Skills:**
- Format: `domain-subdomain` or `technology-purpose`
- Examples:
  - `galaxy-tool-wrapping` (technology-purpose)
  - `vgp-pipeline` (project-type)
  - `python-testing` (language-purpose)

**Commands:**
- Format: `verb-noun` or `verb-target`
- Examples:
  - `check-status` (verb-noun)
  - `debug-failed` (verb-state)
  - `update-skills` (verb-noun)

### Documentation Requirements

**Every skill directory should have:**
- ✅ `SKILL.md` (required) - Main skill file
- ✅ Clear frontmatter with name and description
- ✅ "When to Use This Skill" section
- ⚠️ `reference.md` (optional) - Detailed documentation
- ⚠️ `examples/` (optional) - Example code/configs

**Every command should have:**
- ✅ Frontmatter with name and description
- ✅ Clear prompt/instructions
- ✅ Examples if the command takes parameters

---

## Version Control with Git

### Initialize Git Repository

```bash
cd $CLAUDE_METADATA
git init
git add .
git commit -m "Initial commit: centralized skills and commands"
```

### Track Changes

```bash
# After updating skills
cd $CLAUDE_METADATA
git status          # See what changed
git diff            # Review changes

# Commit updates
git add skills/skill-name/SKILL.md
git commit -m "Add troubleshooting section for XYZ issue"

# Optional: Push to remote for team sharing
git push origin main
```

### Team Collaboration

**Setup shared repository:**
```bash
# Create GitHub/GitLab repo
git remote add origin git@github.com:your-team/claude-metadata.git
git push -u origin main
```

**Team members clone:**
```bash
git clone git@github.com:your-team/claude-metadata.git ~/path/to/claude_data
export CLAUDE_METADATA="$HOME/path/to/claude_data"  # Adjust to your actual path
```

**Pull updates:**
```bash
cd $CLAUDE_METADATA
git pull  # All projects with symlinks auto-update!
```

### Good Commit Messages

**Good:**
```bash
git commit -m "Add token optimization for VGP log files (96% savings)"
git commit -m "Document WF8 failure pattern when Hi-C R2 missing"
git commit -m "Create galaxy-tool-wrapping skill for tool development"
```

**Bad:**
```bash
git commit -m "update"
git commit -m "changes"
git commit -m "fix stuff"
```

---

## Troubleshooting

### Skill Not Activating

**Check 1: Verify symlink exists**
```bash
ls -la .claude/skills/
# Should show: skill-name -> $CLAUDE_METADATA/skills/skill-name
```

**Check 2: Verify target exists**
```bash
ls -L .claude/skills/skill-name
# Should show: SKILL.md
```

**Check 3: Check frontmatter**
```bash
head -10 .claude/skills/skill-name/SKILL.md
# Should have:
# ---
# name: skill-name
# description: ...
# ---
```

**Check 4: Description clarity**
- Is the description clear about when to use the skill?
- Does it match your request?
- Try explicitly mentioning: "Use the skill-name skill to..."

### Command Not Found

**Check 1: Verify symlink**
```bash
ls -la .claude/commands/command-name.md
```

**Check 2: Restart Claude Code**
Commands are loaded at session start, so restart if you just added it.

**Check 3: Check frontmatter**
```bash
head -5 .claude/commands/command-name.md
# Should have:
# ---
# name: command-name
# description: ...
# ---
```

### $CLAUDE_METADATA Not Set

**Symptom:** Symlink commands fail with "No such file or directory"

**Fix:**
```bash
# Check current value
echo $CLAUDE_METADATA

# If empty, add to shell config
echo 'export CLAUDE_METADATA="$HOME/path/to/claude_data"  # Adjust to your actual path' >> ~/.zshrc
source ~/.zshrc

# Verify
echo $CLAUDE_METADATA
```

### Symlink Points to Wrong Location

**Symptom:** `ls -la .claude/skills/skill-name` shows wrong path

**Fix:**
```bash
# Remove broken symlink
rm .claude/skills/skill-name

# Recreate with correct path
ln -s $CLAUDE_METADATA/skills/skill-name .claude/skills/skill-name

# Verify
ls -L .claude/skills/skill-name
```

### Changes Not Appearing in Projects

**Symptom:** Updated skill in `$CLAUDE_METADATA` but projects don't see changes

**Possible causes:**
1. **Not using symlinks** - Projects have copies instead
   ```bash
   # Check if it's a symlink
   ls -la .claude/skills/skill-name
   # Should show -> pointing to $CLAUDE_METADATA
   ```

2. **Claude Code hasn't restarted** - Skills loaded at session start
   - Fix: Restart Claude Code session

3. **Editing wrong file** - Multiple copies exist
   ```bash
   # Find all copies
   find ~/Workdir -name "SKILL.md" -path "*/skill-name/*"
   # Should only show one in $CLAUDE_METADATA
   ```

---

## Best Practices

### 1. Keep Skills Focused

**Good:** One skill per domain
- `galaxy-tool-wrapping/SKILL.md` - Only Galaxy tools
- `vgp-pipeline/SKILL.md` - Only VGP workflows

**Bad:** Kitchen sink skill
- `everything/SKILL.md` - Galaxy + VGP + Docker + Python + ...

### 2. Use Clear, Specific Descriptions

**Good descriptions:**
```yaml
description: Expert in Galaxy tool wrapper development, XML schemas, and Planemo testing
description: VGP genome assembly pipeline orchestration, debugging, and workflow management
```

**Bad descriptions:**
```yaml
description: Helps with stuff
description: Development skill
```

### 3. Regular Maintenance

**Weekly:**
- Review session learnings
- Update skills with new patterns
- Commit changes with clear messages

**Monthly:**
- Audit all skills for conflicts
- Remove outdated information
- Reorganize if needed

### 4. Document Rationale

Include "why" not just "what":

```markdown
## Use --quiet Mode for Status Checks

**Why:** Status checks with verbose output produce 15K tokens, but only 2K
with --quiet mode. Over a typical workflow (10 checks), this saves 130K tokens
(87% reduction).

**When to override:** User explicitly requests detailed output, or debugging
requires full logs.
```

### 5. Version Control Everything

```bash
# Always use git
cd $CLAUDE_METADATA
git add .
git commit -m "Descriptive message"

# Never work without version control
# You'll want to undo changes eventually!
```

### 6. Share with Team

```bash
# Use git for team collaboration
git push origin main

# Team members stay updated
cd $CLAUDE_METADATA && git pull
```

### 7. Symlink, Don't Copy

**Good:**
```bash
ln -s $CLAUDE_METADATA/skills/my-skill .claude/skills/my-skill
```

**Bad:**
```bash
cp -r $CLAUDE_METADATA/skills/my-skill .claude/skills/my-skill
```

**Why:** Symlinks mean updates propagate automatically. Copies create maintenance nightmares.

### 8. Template-Based Script Generation

When creating reusable installers or scripts that need customization across repositories:

**Use placeholders in templates:**
```bash
# Template with placeholders
TEMPLATE='
MAIN_FILE="__MAIN_FILE__"
BACKUP_DIR="__BACKUP_BASE_DIR__"
DAYS="__DAYS_TO_KEEP__"
'

# Substitute with actual values
echo "$TEMPLATE" | \
  sed "s|__MAIN_FILE__|$ACTUAL_FILE|g" | \
  sed "s|__BACKUP_BASE_DIR__|$ACTUAL_DIR|g" | \
  sed "s|__DAYS_TO_KEEP__|$ACTUAL_DAYS|g" \
  > final_script.sh
```

**Benefits:**
- Reusable across projects
- Single source of truth for logic
- Easy to maintain and update
- Parameter validation in one place
- Reduces duplication

**Example use case:**
Creating a global installer for backup systems that can be customized for any data file and directory structure. The template contains all the logic, and sed substitution customizes it for each project.

**Alternative: Template files:**
```bash
# Store template in file
cat > template.sh << 'EOF'
MAIN_FILE="__MAIN_FILE__"
BACKUP_DIR="__BACKUP_BASE_DIR__"
EOF

# Generate from template
sed "s|__MAIN_FILE__|data.csv|g" template.sh > backup.sh
```

---

## Quick Reference

### Create New Skill
```bash
mkdir -p $CLAUDE_METADATA/skills/skill-name
cat > $CLAUDE_METADATA/skills/skill-name/SKILL.md << 'EOF'
---
name: skill-name
description: Brief description
---
# Content here
EOF
```

### Link to Project
```bash
ln -s $CLAUDE_METADATA/skills/skill-name .claude/skills/skill-name
```

### Update Skill
```bash
# Edit directly
vim $CLAUDE_METADATA/skills/skill-name/SKILL.md

# Or tell Claude
"Update the skill-name skill to add [information]"
```

### Sync Project
```bash
# Tell Claude
"Check what skills are available in $CLAUDE_METADATA and show me what's new"
```

### List Available Skills
```bash
ls $CLAUDE_METADATA/skills/
```

### List Available Commands
```bash
ls $CLAUDE_METADATA/commands/*/
```

### Verify Setup
```bash
echo $CLAUDE_METADATA
ls -la .claude/skills/
ls -la .claude/commands/
```

### Setup New Project with Essential Skills and Commands
```bash
# Quick setup for new project
cd ~/Workdir/new-project
mkdir -p .claude/skills .claude/commands

# Always symlink these essential skills
ln -s $CLAUDE_METADATA/skills/token-efficiency .claude/skills/token-efficiency
ln -s $CLAUDE_METADATA/skills/claude-collaboration .claude/skills/claude-collaboration

# Always symlink these useful commands
ln -s $CLAUDE_METADATA/commands/global/*.md .claude/commands/

# Verify
ls -la .claude/skills/
ls -la .claude/commands/
```

---

## Common Workflows

### Workflow 1: Creating and Using a New Skill

1. **Create skill**:
   ```bash
   mkdir -p $CLAUDE_METADATA/skills/docker-workflows
   # Create SKILL.md with frontmatter
   ```

2. **Test in isolated project**:
   ```bash
   mkdir -p /tmp/test/.claude/skills
   ln -s $CLAUDE_METADATA/skills/docker-workflows /tmp/test/.claude/skills/
   # Start Claude Code, test the skill
   ```

3. **Link to real projects**:
   ```bash
   cd ~/Workdir/real-project
   ln -s $CLAUDE_METADATA/skills/docker-workflows .claude/skills/
   ```

4. **Share with team**:
   ```bash
   cd $CLAUDE_METADATA
   git add skills/docker-workflows/
   git commit -m "Add docker-workflows skill"
   git push
   ```

### Workflow 2: Updating Skill After Learning

1. **Work with Claude, discover pattern**
2. **Tell Claude**: "Add this pattern to the vgp-pipeline skill"
3. **Claude updates**: `$CLAUDE_METADATA/skills/vgp-pipeline/SKILL.md`
4. **Review changes**: `git diff`
5. **Commit**: `git commit -m "Add WF8 troubleshooting pattern"`
6. **Push**: `git push` (if using team repo)
7. **All projects auto-updated** via symlinks! 🎉

### Workflow 3: Setting Up New Project

1. **Create .claude directory**:
   ```bash
   cd ~/Workdir/new-project
   mkdir -p .claude/skills .claude/commands
   ```

2. **Symlink essential global skills**:
   ```bash
   # Always include these
   ln -s $CLAUDE_METADATA/skills/token-efficiency .claude/skills/token-efficiency
   ln -s $CLAUDE_METADATA/skills/claude-collaboration .claude/skills/claude-collaboration
   ln -s $CLAUDE_METADATA/skills/python-environment-management .claude/skills/python-environment-management
   ```

3. **Symlink ALL global commands**:
   ```bash
   # Always include for all projects
   ln -s $CLAUDE_METADATA/commands/global/*.md .claude/commands/
   ```

4. **Add project-specific skills** (if needed):
   ```bash
   # For Galaxy projects:
   ln -s $CLAUDE_METADATA/skills/galaxy-automation .claude/skills/galaxy-automation
   ```

5. **Tell Claude** (or use `/setup-project` if already linked):
   ```
   I've set up the essential skills and commands. Show me other available skills in
   $CLAUDE_METADATA that might be relevant for [describe your project type].
   ```

   Or simply:
   ```
   /list-skills
   ```

5. **Claude shows list**, you choose project-specific skills

6. **Claude creates additional symlinks**

7. **Commit symlinks to project**:
   ```bash
   git add .claude/
   git commit -m "Add Claude Code configuration

   Essential global skills and commands:
   - token-efficiency (token optimization)
   - claude-collaboration (team best practices)
   - galaxy-automation (BioBlend & Planemo)
   - Global commands: /update-skills, /list-skills, /setup-project

   [Additional project-specific skills if added]"
   ```

8. **Team members get symlinks** via git pull

9. **Team members point to their $CLAUDE_METADATA**
   - They need to set `$CLAUDE_METADATA` in their shell config
   - Symlinks work automatically once environment variable is set

**Pro tip**: Use `/update-skills` at the end of productive sessions to capture new learnings!

---

## Repository Maintenance

### Periodic Cleanup to Remove Redundancies

As your skill repository grows, redundancies can accumulate from:
- Legacy files after reorganizations
- Duplicate documentation in different locations
- Outdated quick-start guides
- Superseded command files

**Cleanup workflow:**

1. **Identify redundancies**:
   ```bash
   # List all markdown files
   find $CLAUDE_METADATA -name "*.md" -type f | sort

   # Compare similar files
   diff file1.md file2.md

   # Search for overlapping content
   grep -r "specific topic" $CLAUDE_METADATA
   ```

2. **Categorize files**:
   - Skills (must be unique, in `skills/*/SKILL.md`)
   - Supporting docs (should be in skill subdirectories)
   - Commands (one version only, in `commands/category/`)
   - Root docs (only README.md, QUICK_REFERENCE.md)

3. **Always backup before cleanup**:
   ```bash
   cd $CLAUDE_METADATA
   mkdir -p .backup-$(date +%Y%m%d-%H%M%S)
   cp -r files-to-modify .backup-$(date +%Y%m%d-%H%M%S)/
   ```

4. **Consolidation patterns**:
   - **Standalone docs** → Move to `skills/skill-name/reference.md`
   - **Legacy commands** → Remove if superseded by new versions
   - **Duplicate guides** → Consolidate into single skill
   - **Quick reference prompts** → Replace with standardized QUICK_REFERENCE.md

5. **Update skill to reference supporting docs**:
   ```markdown
   ## Supporting Documentation

   This skill includes detailed reference documentation:
   - **reference.md** - Comprehensive guide
   - **troubleshooting.md** - Common issues and solutions
   ```

6. **Verify structure**:
   ```bash
   tree -L 3 $CLAUDE_METADATA
   # Should show clean, logical organization
   ```

**Benefits of regular cleanup:**
- Reduces confusion about which file to use
- Improves discoverability via progressive disclosure
- Easier maintenance (single source of truth)
- Faster skill loading (no duplicate content)

---

## Summary

**Key Principles:**
1. **Central repository** - All skills in `$CLAUDE_METADATA`
2. **Symlinks, not copies** - Updates propagate automatically
3. **Version control** - Track changes with git
4. **Essential global skills first** - Always symlink token-efficiency, claude-collaboration, and python-environment-management
5. **Selective activation** - Link only relevant skills per project
6. **Team collaboration** - Share via git, everyone benefits

**Every new project should start with:**
```bash
# Essential global skills (always)
ln -s $CLAUDE_METADATA/skills/token-efficiency .claude/skills/token-efficiency
ln -s $CLAUDE_METADATA/skills/claude-collaboration .claude/skills/claude-collaboration
ln -s $CLAUDE_METADATA/skills/python-environment-management .claude/skills/python-environment-management

# ALL global commands (always include for management)
ln -s $CLAUDE_METADATA/commands/global/*.md .claude/commands/

# Project-specific skills (add as needed)
# For Galaxy projects:
# ln -s $CLAUDE_METADATA/skills/galaxy-automation .claude/skills/galaxy-automation
```

**Available global commands:**
- `/update-skills` - Capture learnings from current session
- `/list-skills` - Show all available skills
- `/setup-project` - Set up a new project intelligently
- `/sync-skills` - Check for new skills/commands to symlink
- `/cleanup-project` - End-of-project cleanup (removes working docs, condenses READMEs)

**Remember:** The centralized pattern makes skills:
- ✅ Maintainable (update once, apply everywhere)
- ✅ Shareable (team uses same knowledge)
- ✅ Versionable (track evolution with git)
- ✅ Scalable (works for 1 or 100 projects)
- ✅ Efficient (progressive disclosure = no token waste)

**With token-efficiency skill active:**
- 80-90% token savings on typical operations
- 5-10x more interactions from your Claude Pro subscription
- Strategic file reading for learning and debugging
