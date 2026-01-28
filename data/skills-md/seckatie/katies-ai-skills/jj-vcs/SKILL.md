---
name: jj-vcs
description: Jujutsu (jj) is a powerful Git-compatible version control system with innovative features like automatic rebasing, working-copy-as-a-commit, operation log with undo, and first-class conflict tracking. This skill is triggered when the user says things like "use jj", "run jj commands", "jujutsu version control", "migrate from git to jj", "jj rebase", "jj squash", "jj log", or "help with jj workflow".
---

# Jujutsu (jj) Version Control System

Jujutsu is a next-generation version control system that uses Git repositories as storage while providing a fundamentally different and more powerful user experience. This skill includes the complete official documentation from the jj repository.

**Quick Start:** Read `tutorial.md` for hands-on introduction. See `git-comparison.md` for Git users migrating to jj.

## What is Jujutsu?

Jujutsu (command: `jj`) is a VCS designed to be easy to use for both beginners and experienced users. Key innovations include:

- **Working-copy-as-a-commit**: Changes are automatically recorded as commits and amended on each change
- **Operation log & undo**: Every operation is recorded and can be undone (like version control for your version control!)
- **Automatic rebase**: When you modify a commit, descendants are automatically rebased
- **First-class conflicts**: Conflicts are tracked as objects and can be committed, resolved later, and propagated
- **No staging area**: Simplified workflow without Git's index/staging complexity
- **Git compatible**: Works with existing Git repositories and forges like GitHub

## Documentation Structure

### Getting Started

- **README.md** - Project overview, key features, and introduction
- **index.md** - Documentation homepage with useful links
- **install-and-setup.md** - Installation instructions for all platforms and initial configuration
- **tutorial.md** - Comprehensive hands-on tutorial (assumes Git knowledge)
- **FAQ.md** - Frequently asked questions and common issues
- **glossary.md** - Definitions of jj-specific terminology

### Core Concepts

- **working-copy.md** - How the working copy works as a commit
- **operation-log.md** - Understanding the operation log and undo functionality
- **conflicts.md** - How jj handles merge conflicts as first-class objects
- **revsets.md** - Powerful language for selecting revisions (like Mercurial revsets)
- **templates.md** - Customizing output formatting with the template language
- **bookmarks.md** - Working with bookmarks (similar to Git branches)
- **filesets.md** - Language for selecting files

### Configuration

- **config.md** - Complete configuration reference and options
- **config.toml** - Example configuration file
- **cli-reference.md** - Command-line interface reference

### Git Integration

- **git-compatibility.md** - How jj works with Git repositories and Git features
- **git-comparison.md** - Comparison of jj vs Git workflows and commands
- **git-command-table.md** - Quick reference table mapping Git commands to jj equivalents
- **github.md** - Working with GitHub repositories and pull requests
- **gerrit.md** - Working with Gerrit code review system

### Guides

- **guides/divergence.md** - Understanding and resolving divergent changes
- **guides/multiple-remotes.md** - Working with multiple remote repositories

### Technical Documentation

- **technical/architecture.md** - High-level architecture and design decisions
- **technical/concurrency.md** - How jj handles concurrent operations safely
- **technical/conflicts.md** - Technical details of conflict handling

### Development and Contributing

- **contributing.md** - How to contribute to jj development
- **code-of-conduct.md** - Community code of conduct
- **core_tenets.md** - Core principles guiding jj's design
- **roadmap.md** - Development roadmap and planned features
- **community_tools.md** - Community-maintained tools and integrations
- **releasing.md** - Release process documentation
- **design_docs.md** - Index of design documents
- **design_doc_blueprint.md** - Template for writing design docs

### Comparisons and Context

- **sapling-comparison.md** - Comparison with Meta's Sapling VCS
- **related-work.md** - Other related version control systems
- **testimonials.md** - User testimonials and experiences

### Platform-Specific

- **windows.md** - Windows-specific considerations and setup

### Project Information

- **CHANGELOG.md** - Version history and release notes
- **GOVERNANCE.md** - Project governance structure
- **SECURITY.md** - Security policy and reporting

## Common Usage Patterns

When the user asks to:
- **Get started with jj** → Check `tutorial.md` and `install-and-setup.md`
- **Migrate from Git** → Check `git-comparison.md` and `git-command-table.md`
- **Understand a concept** → Check `glossary.md` and relevant concept docs (working-copy, conflicts, etc.)
- **Configure jj** → Check `config.md`
- **Work with GitHub** → Check `github.md`
- **Select revisions** → Check `revsets.md`
- **Customize output** → Check `templates.md`
- **Handle conflicts** → Check `conflicts.md`
- **Troubleshoot issues** → Check `FAQ.md`
- **Undo a mistake** → Check `operation-log.md`
- **Understand architecture** → Check `technical/architecture.md`

## Quick Command Reference

### Basic Operations
```bash
# Clone a Git repository
jj git clone <url>

# Check status
jj st  # or jj status

# Create a new change
jj new

# Edit a change description
jj describe

# Show change log
jj log

# Undo last operation
jj undo

# Show operation log
jj op log
```

### Working with Changes
```bash
# Abandon a change
jj abandon

# Move changes between commits
jj squash  # move changes into parent
jj move    # move changes to another commit

# Rebase changes
jj rebase -r <revision> -d <destination>

# Resolve conflicts
jj resolve  # interactive conflict resolution
```

### Git Integration
```bash
# Fetch from Git remote
jj git fetch

# Push to Git remote
jj git push

# Import Git branches as bookmarks
jj bookmark track <name>@<remote>
```

### Selecting Revisions (Revsets)
```bash
# Common revset expressions
@              # working copy commit
@-             # parent of working copy
main@origin    # bookmark from remote
::@            # ancestors of working copy
@::            # descendants of working copy
~empty()       # non-empty changes
```

## Key Concepts to Understand

### Working Copy as Commit
- The working copy is always a commit (shown as `@`)
- Changes are automatically committed as you work
- No explicit `commit` command needed (use `jj describe` to add a message)
- Use `jj new` to start a new change

### Revsets
- Powerful language for selecting commits (similar to Mercurial)
- Used in many commands: `jj log -r`, `jj show`, `jj rebase`, etc.
- Supports boolean operations, functions, and composition
- See `revsets.md` for complete reference

### Operation Log
- Every jj operation is recorded (commit, rebase, push, etc.)
- Use `jj op log` to see operation history
- Use `jj undo` to undo the last operation
- Use `jj op restore` to restore to any previous state

### Bookmarks vs Branches
- jj uses "bookmarks" which are similar to Git branches but simpler
- Changes can exist without bookmarks (anonymous branches)
- Bookmarks are just pointers, not required for workflow
- Git branches are imported as bookmarks

### Conflicts
- Conflicts are stored in commits, not just in working copy
- You can commit conflicted changes and resolve later
- Conflict resolution is propagated through rebases
- Use `jj resolve` for interactive resolution

## File Organization

- **README.md** - Main project README with overview
- **docs/** - All documentation files
  - **tutorial.md** - Getting started tutorial
  - **config.md** - Configuration reference
  - **revsets.md** - Revset language reference
  - **templates.md** - Template language reference
  - **git-*.md** - Git integration documentation
  - **guides/** - How-to guides for specific workflows
  - **technical/** - Technical architecture documentation
  - **design/** - Design documents for features

## Tips

- Start with the tutorial to understand the jj mental model
- Use `jj help <command>` for detailed command help
- The operation log is your safety net - don't be afraid to experiment
- Revsets are powerful - learn them to work efficiently
- Conflicts are normal and can be handled gracefully
- jj works best when you embrace its philosophy (working-copy-as-commit, auto-rebase)
- Check the FAQ when you encounter unexpected behavior
- Use templates to customize `jj log` output to your preferences

## Important Notes

- Jujutsu is experimental but actively developed and used daily by its developers
- Git compatibility is stable - safe to use with existing Git workflows
- Some features are experimental (check README warnings)
- Breaking changes may occur but are documented in CHANGELOG
- Community is active on Discord, GitHub Discussions, and IRC (#jujutsu on Libera Chat)

## Resources

- Homepage: https://jj-vcs.github.io/jj
- GitHub: https://github.com/jj-vcs/jj
- Discord: https://discord.gg/dkmfj3aGQN
- Documentation: https://jj-vcs.github.io/jj/latest/
- Tutorial by Steve Klabnik: https://steveklabnik.github.io/jujutsu-tutorial/
- Chris Krycho's YouTube series: https://www.youtube.com/playlist?list=PLelyiwKWHHAq01Pvmpf6x7J0y-yQpmtxp
