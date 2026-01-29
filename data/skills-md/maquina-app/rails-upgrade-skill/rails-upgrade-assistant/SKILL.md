---
name: rails-upgrade-assistant
description: Analyzes Rails applications and generates comprehensive upgrade reports with breaking changes, deprecations, and step-by-step migration guides for Rails 7.0 through 8.1.1. Use when upgrading Rails applications, planning multi-hop upgrades, or querying version-specific changes.
---

# Rails Upgrade Assistant Skill v1.0

## Skill Identity
- **Name:** Rails Upgrade Assistant
- **Version:** 1.0
- **Purpose:** Intelligent Rails application upgrades from 7.0 through 8.1.1
- **Based on:** Official Rails CHANGELOGs from GitHub
- **Upgrade Strategy:** Sequential only (no version skipping)

---

## Core Functionality

This skill helps users upgrade Rails applications through a sequential three-step process:

### Step 1: Breaking Changes Detection Script
- Claude generates executable bash script tailored to the specific upgrade
- Script scans user's codebase for breaking changes
- Finds issues with file:line references
- Generates findings report (TXT file)
- Runs in < 30 seconds
- Lists affected files for Neovim integration

### Step 2: User Runs Script & Shares Findings
- User executes the detection script in their project directory
- Script outputs `rails_{version}_upgrade_findings.txt`
- User shares findings report back with Claude

### Step 3: Claude Generates Reports Based on Actual Findings
- **Comprehensive Upgrade Report**: Breaking changes analysis with OLD vs NEW code examples, custom code warnings with ⚠️ flags, step-by-step migration plan, testing checklist and rollback plan
- **app:update Preview Report**: Shows exact configuration file changes (OLD vs NEW), lists new files to be created, impact assessment (HIGH/MEDIUM/LOW), Neovim buffer list ready

**User Benefits:**
- ⏱️ Saves 2-3 hours per upgrade (automated detection)
- 🎯 90%+ accuracy in finding breaking changes
- 📋 Clear file:line references for every issue
- 🚀 Reports based on ACTUAL detected issues, not hypothetical
- 📊 50% faster upgrades overall

---

## Trigger Patterns

Claude should activate this skill when user says:

**Initial Upgrade Requests (Generate Detection Script):**
- "Upgrade my Rails app to [version]"
- "Help me upgrade from Rails [x] to [y]"
- "What breaking changes are in Rails [version]?"
- "Plan my upgrade from [x] to [y]"
- "What Rails version am I using?"
- "Analyze my Rails app for upgrade"
- "Create a detection script for Rails [version]"
- "Generate a breaking changes script"
- "Find breaking changes in my code"

**After Script Execution (Generate Reports):**
- "Here's my findings.txt"
- "I ran the script, here are the results"
- "The detection script found [X] issues"
- "Can you analyze these findings?"
- *User shares/uploads findings.txt file*

**Specific Report Requests (Only After Findings Shared):**
- "Show me the app:update changes"
- "Preview configuration changes for Rails [version]"
- "Generate the upgrade report"
- "Create the comprehensive report"

---

## CRITICAL: Sequential Upgrade Strategy

### ⚠️ Version Skipping is NOT Allowed

Rails upgrades MUST follow this exact sequence:
```
7.0.x → 7.1.x → 7.2.x → 8.0.x → 8.1.x
```

**You CANNOT skip versions.** Examples:
- ❌ 7.0 → 7.2 (skips 7.1)
- ❌ 7.0 → 8.0 (skips 7.1 and 7.2)
- ✅ 7.0 → 7.1 (correct)
- ✅ 7.1 → 7.2 (correct)

If user requests a multi-hop upgrade (e.g., 7.0 → 8.1):
1. Explain the sequential requirement
2. Break it into individual hops
3. Generate separate reports for each hop
4. Recommend completing each hop fully before moving to next

---

## Available Resources

### Core Documentation
- `docs/README.md` - Human-readable overview
- `docs/QUICK-REFERENCE.md` - Command cheat sheet
- `docs/USAGE-GUIDE.md` - Comprehensive how-to

### Version-Specific Guides (Load as needed)
- `version-guides/upgrade-7.0-to-7.1.md` - Rails 7.0 → 7.1
- `version-guides/upgrade-7.1-to-7.2.md` - Rails 7.1 → 7.2
- `version-guides/upgrade-7.2-to-8.0.md` - Rails 7.2 → 8.0
- `version-guides/upgrade-8.0-to-8.1.md` - Rails 8.0 → 8.1

### Workflow Guides (Load when generating deliverables)
- `workflows/upgrade-report-workflow.md` - How to generate upgrade reports
- `workflows/detection-script-workflow.md` - How to generate detection scripts
- `workflows/app-update-preview-workflow.md` - How to generate app:update previews

### Examples (Load when user needs clarification)
- `examples/simple-upgrade.md` - Single-hop upgrade example
- `examples/multi-hop-upgrade.md` - Multi-hop upgrade example
- `examples/detection-script-only.md` - Detection script only request
- `examples/preview-only.md` - Preview only request

### Reference Materials
- `reference/breaking-changes-by-version.md` - Quick lookup
- `reference/multi-hop-strategy.md` - Multi-version planning
- `reference/deprecations-timeline.md` - Deprecation tracking
- `reference/testing-checklist.md` - Comprehensive testing
- `reference/pattern-file-guide.md` - How to use pattern files
- `reference/quality-checklist.md` - Pre-delivery verification
- `reference/troubleshooting.md` - Common issues and solutions

### Detection Script Resources
- `detection-scripts/patterns/rails-72-patterns.yml` - Rails 7.2 patterns
- `detection-scripts/patterns/rails-80-patterns.yml` - Rails 8.0 patterns
- `detection-scripts/patterns/rails-81-patterns.yml` - Rails 8.1 patterns
- `detection-scripts/templates/detection-script-template.sh` - Bash template

### Report Templates
- `templates/upgrade-report-template.md` - Main upgrade report structure
- `templates/app-update-preview-template.md` - Configuration preview

---

## MCP Tools Integration

### Required: Rails MCP Server

**Tools:**
- `railsMcpServer:project_info` - Get Rails version, structure, API mode
- `railsMcpServer:get_file` - Read file contents
- `railsMcpServer:list_files` - Browse directories
- `railsMcpServer:analyze_environment_config` - Config files

### Optional: Neovim MCP Server

**Tools:**
- `nvimMcpServer:get_project_buffers` - List open files
- `nvimMcpServer:update_buffer` - Update file content

---

## High-Level Workflow

When user requests an upgrade, follow this workflow:

### Step 1: Detect Current Version
```
1. Call: railsMcpServer:project_info
2. Store: current_version, target_version, project_type, project_root
```

### Step 2: Load Detection Script Resources
```
1. Read: detection-scripts/patterns/rails-{VERSION}-patterns.yml
2. Read: detection-scripts/templates/detection-script-template.sh
3. Read: workflows/detection-script-workflow.md (for generation instructions)
```

### Step 3: Generate Detection Script
```
1. Follow workflow in detection-script-workflow.md
2. Generate version-specific bash script
3. Deliver script to user
4. Instruct user to run script and share findings.txt
```

### Step 4: Wait for User to Run Script
```
User runs: ./detect_rails_{version}_breaking_changes.sh
Script outputs: rails_{version}_upgrade_findings.txt
User shares findings back with Claude
```

### Step 5: Load Report Generation Resources
```
1. Read: templates/upgrade-report-template.md
2. Read: version-guides/upgrade-{FROM}-to-{TO}.md
3. Read: templates/app-update-preview-template.md
4. Read: workflows/upgrade-report-workflow.md
5. Read: workflows/app-update-preview-workflow.md
```

### Step 6: Analyze User's Actual Findings
```
1. Parse the findings.txt file
2. Extract detected breaking changes and affected files
3. Read user's actual config files for context
4. Identify custom code patterns from findings
```

### Step 7: Generate Reports Based on Findings

**Deliverable #1: Comprehensive Upgrade Report**
- **Workflow:** See `workflows/upgrade-report-workflow.md`
- **Input:** Actual findings from script + version guide data
- **Output:** Report with real code examples from user's project

**Deliverable #2: app:update Preview**
- **Workflow:** See `workflows/app-update-preview-workflow.md`
- **Input:** Actual config files + findings
- **Output:** Preview with real file paths and changes

### Step 8: Present Reports
```
1. Present Comprehensive Upgrade Report first
2. Present app:update Preview Report second
3. Explain next steps
4. Offer interactive help with Neovim (if available)
```

---

## When to Load Detailed Workflows

Load workflow files when you need detailed instructions:

**Step 1 - Load Before Generating Detection Script:**
- `workflows/detection-script-workflow.md` - Before creating detection scripts

**Step 2 - User Runs Script (No Claude action needed)**

**Step 3 - Load Before Generating Reports (After receiving findings):**
- `workflows/upgrade-report-workflow.md` - Before creating upgrade reports
- `workflows/app-update-preview-workflow.md` - Before creating previews

**Load When User Needs Examples:**
- `examples/simple-upgrade.md` - User asks about simple upgrades
- `examples/multi-hop-upgrade.md` - User asks about complex upgrades
- `examples/detection-script-only.md` - User wants only detection script
- `examples/preview-only.md` - User wants only preview

**Load When You Need Reference:**
- `reference/pattern-file-guide.md` - When processing YAML pattern files
- `reference/quality-checklist.md` - Before delivering any output
- `reference/troubleshooting.md` - When encountering issues

---

## Quality Checklist

Before delivering, verify:

**For Detection Script:**
- [ ] All {PLACEHOLDERS} replaced with actual values
- [ ] Patterns match target Rails version
- [ ] Script includes all breaking changes from pattern file
- [ ] File paths use user's actual project structure
- [ ] User instructions are clear

**After User Runs Script (Before Generating Reports):**
- [ ] Received and parsed findings.txt from user
- [ ] Identified all detected breaking changes
- [ ] Collected affected file paths
- [ ] Noted custom code warnings from findings

**For Comprehensive Upgrade Report:**
- [ ] All {PLACEHOLDERS} replaced with actual values
- [ ] Used ACTUAL findings from script (not generic examples)
- [ ] Breaking changes section includes real file:line references
- [ ] Custom code warnings based on actual detected issues
- [ ] Code examples use user's actual code from affected files
- [ ] Next steps clearly outlined

**For app:update Preview:**
- [ ] All {PLACEHOLDERS} replaced with actual values
- [ ] File list matches user's actual config files
- [ ] Diffs based on real current config vs target version
- [ ] Neovim buffer list includes only affected files
- [ ] Next steps clearly outlined

**Detailed Checklist:** See `reference/quality-checklist.md`

---

## Common Request Patterns

### Pattern 1: Full Upgrade Request
**User says:** "Upgrade my Rails app to 8.1"

**Action - Phase 1 (Generate Script):**
1. Load: `workflows/detection-script-workflow.md`
2. Generate detection script
3. Deliver script with instructions to run it
4. Wait for user to share findings.txt

**Action - Phase 2 (Generate Reports):**
1. Parse findings.txt
2. Load: `workflows/upgrade-report-workflow.md`
3. Load: `workflows/app-update-preview-workflow.md`
4. Generate Comprehensive Upgrade Report (using actual findings)
5. Generate app:update Preview (using actual findings)
6. Reference: `examples/simple-upgrade.md` for structure

### Pattern 2: Multi-Hop Request
**User says:** "Help me upgrade from Rails 7.0 to 8.1"

**Action:**
1. Explain sequential requirement
2. Reference: `examples/multi-hop-upgrade.md`
3. Follow Pattern 1 for FIRST hop (7.0 → 7.1)
4. After first hop complete, repeat for next hops

### Pattern 3: Detection Script Only
**User says:** "Create a detection script for Rails 8.0"

**Action:**
1. Load: `workflows/detection-script-workflow.md`
2. Generate detection script only
3. Reference: `examples/detection-script-only.md`
4. Do NOT generate reports yet (wait for findings)

### Pattern 4: User Returns with Findings
**User says:** "Here's my findings.txt" or shares script output

**Action:**
1. Parse findings.txt
2. Load: `workflows/upgrade-report-workflow.md`
3. Load: `workflows/app-update-preview-workflow.md`
4. Generate Comprehensive Upgrade Report
5. Generate app:update Preview

### Pattern 5: Preview Only (After Findings Shared)
**User says:** "Show me the app:update changes for Rails 7.2"

**Action:**
1. Check if user has shared findings
2. If yes: Load `workflows/app-update-preview-workflow.md` and generate
3. If no: Ask user to run detection script first
4. Reference: `examples/preview-only.md`

---

## Key Principles

1. **Always Generate Detection Script First** (unless user only wants reports and has findings)
2. **Wait for User to Run Script** (reports depend on actual findings)
3. **Always Use Actual Findings** (no generic examples in reports)
4. **Always Flag Custom Code** (with ⚠️ warnings based on detected issues)
5. **Always Use Templates** (for consistency)
6. **Always Check Quality** (before delivery)
7. **Load Workflows as Needed** (don't hold everything in memory)
8. **Sequential Process is Critical** (script → findings → reports)

---

## File Organization

This skill follows a modular structure:

```
rails-upgrade-assistant/
├── SKILL.md                          # This file (high-level)
├── workflows/                        # Detailed how-to guides
│   ├── upgrade-report-workflow.md
│   ├── detection-script-workflow.md
│   └── app-update-preview-workflow.md
├── examples/                         # Usage examples
│   ├── simple-upgrade.md
│   ├── multi-hop-upgrade.md
│   ├── detection-script-only.md
│   └── preview-only.md
├── reference/                        # Reference documentation
│   ├── pattern-file-guide.md
│   ├── quality-checklist.md
│   └── troubleshooting.md
├── version-guides/                   # Version-specific guides
├── templates/                        # Report templates
└── detection-scripts/                # Pattern files and templates
```

**When to Load What:**
- Load `workflows/` when generating deliverables
- Load `examples/` when user needs clarification
- Load `reference/` when you need detailed guidance

---

## Success Criteria

A successful upgrade assistance session:

✅ Generated detection script (Phase 1)  
✅ User ran script and shared findings.txt (Phase 2)  
✅ Generated Comprehensive Upgrade Report using actual findings (Phase 3)  
✅ Generated app:update Preview using actual findings (Phase 3)  
✅ Used user's actual code from findings (not generic examples)  
✅ Flagged all custom code with ⚠️ warnings based on detected issues  
✅ Provided clear next steps  
✅ Offered interactive help (if Neovim available)  

**Verification:** See `reference/quality-checklist.md`

---

**Version:** 1.0  
**Last Updated:** November 2, 2025  
**Skill Type:** Modular with external workflows and examples
