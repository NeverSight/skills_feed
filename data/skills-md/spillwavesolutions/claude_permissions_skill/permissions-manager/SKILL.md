---
name: permissions-manager
description: |
  Configures Claude Code permissions via natural language for CLI tools (git, gcloud, aws, kubectl, maven, gradle, npm, docker), project types (Rust, Java, TypeScript, Python), and file patterns. Use when asked to "configure permissions", "enable git", "allow docker", "setup project permissions", "apply permission profile", or "make files editable". Auto-detects project types and researches unknown tools.
version: 1.0.0
category: automation
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - mcp__perplexity-ask__perplexity_ask
  - mcp__brave-search__brave_web_search
  - WebSearch
  - Skill
tier1_token_budget: 100
tier2_token_budget: 2500
---

# Permissions Manager

## Table of Contents

- [Quick Reference](#quick-reference)
- [Intent Classification Decision Tree](#intent-classification-decision-tree)
- [Core Detection Logic](#core-detection-logic)
- [Resource Loading Policy](#resource-loading-policy---critical)
- [Safety Rules](#safety-rules---always-apply)
- [Token Budget Management](#token-budget-management)
- [Error Handling](#error-handling)
- [Skill Integration Points](#skill-integration-points)
- [Success Criteria Checklist](#success-criteria-checklist)
- [Quick Start Examples](#quick-start-examples)

---

## Quick Reference

**Purpose**: Auto-configure Claude Code permissions via natural language
**Token Budget**: T1(100) + T2(2,500) + T3(1,500-3,000 per workflow)
**Architecture**: Progressive Disclosure (3-tier) - Load only what's needed

---

## Intent Classification Decision Tree

### Step 1: Detect Request Type

Parse user message for patterns:

**CLI Tool Request** - Indicators:
- Keywords: "enable", "allow", "configure" + tool name
- Tool names: git, gcloud, aws, kubectl, docker, npm, pip, maven, gradle, cargo, helm, terraform, pulumi, ansible
- Modes: "read", "write", "read-only", "commits", "pushes"
- **Route to**: `guides/workflows/cli-tool-workflow.md`

**File Pattern Request** - Indicators:
- Keywords: "make editable", "edit", "write" + file type/pattern
- Patterns: "**.md", "TypeScript files", "src/", "docs folder"
- **Route to**: `guides/workflows/file-pattern-workflow.md`

**Project Type Request** - Indicators:
- Keywords: "this is a [language] project", "setup", "project"
- Languages: Rust, Java, TypeScript, Python, Go, Ruby, PHP, C#, C++, Swift
- **Route to**: `guides/workflows/project-setup-workflow.md`

**Profile Request** - Indicators:
- Keywords: "apply profile", "use profile" + profile name
- Profiles: read-only, development, ci-cd, production, documentation, code-review, testing
- **Route to**: `guides/workflows/profile-application-workflow.md`

**Validation/Troubleshooting** - Indicators:
- Keywords: "validate", "check", "troubleshoot", "not working"
- **Route to**: `guides/workflows/validation-workflow.md`

**Backup/Restore** - Indicators:
- Keywords: "backup", "restore", "rollback", "undo"
- **Route to**: `guides/workflows/backup-restore-workflow.md`

### Step 2: Load Appropriate Workflow

**CRITICAL**: Load ONLY the workflow guide needed. Do NOT load multiple guides.

| Request Type | Workflow File | Token Cost |
|-------------|---------------|------------|
| CLI Tool | `guides/workflows/cli-tool-workflow.md` | +1,500 |
| File Pattern | `guides/workflows/file-pattern-workflow.md` | +1,200 |
| Project Type | `guides/workflows/project-setup-workflow.md` | +1,800 |
| Profile | `guides/workflows/profile-application-workflow.md` | +1,000 |
| Validation | `guides/workflows/validation-workflow.md` | +1,200 |
| Backup/Restore | `guides/workflows/backup-restore-workflow.md` | +750 |
| Unknown Tool | `guides/workflows/research-workflow.md` | +2,000 |

---

## Core Detection Logic

### CLI Tool Recognition

**Known Tools** (check against `references/cli_commands.json`):
- Version Control: git
- Cloud: gcloud, aws, az
- Containers: docker, kubectl, helm
- Build: npm, pip, maven, gradle, cargo, go, yarn, bundle, composer
- Infrastructure: terraform, pulumi, ansible

**Mode Detection**:
- Contains "read", "list", "show", "describe" -> READ mode (safer default)
- Contains "write", "push", "commit", "deploy", "publish" -> WRITE mode
- No mode -> Default to READ

**Tool Lookup**:
1. Check if tool in `references/cli_commands.json` (use grep)
2. If found -> Extract commands for detected mode
3. If NOT found -> Route to research workflow

### Project Type Detection

**Auto-Detection** (via file scanning):
```
Cargo.toml                      -> Rust
pom.xml                         -> Java Maven
build.gradle*                   -> Java Gradle
package.json + tsconfig.json    -> TypeScript
package.json (alone)            -> JavaScript
pyproject.toml | setup.py       -> Python
go.mod                          -> Go
Gemfile                         -> Ruby
composer.json                   -> PHP
*.csproj | *.sln                -> C#
CMakeLists.txt                  -> C++
Package.swift                   -> Swift
```

**Detection Method**: Run `scripts/detect_project.py` or scan for indicator files

### Profile Recognition

**Available Profiles** (from `assets/permission_profiles.json`):
- `read-only` - Code review, security audit
- `development` - Active development (most common)
- `ci-cd` - Continuous integration
- `production` - Monitoring only
- `documentation` - Docs writing
- `code-review` - PR review
- `testing` - TDD workflow

---

## Resource Loading Policy - CRITICAL

**NEVER load resources proactively or "just in case"**

### Loading Workflow Guides

**DO**: Load specific workflow when decision tree routes to it
```bash
Read guides/workflows/{workflow-name}.md
```

**DON'T**: Load all guides upfront or multiple guides

### Loading Reference Data - Surgical Only

**CLI Commands** (one tool only):
```bash
grep -A 25 '"git"' references/cli_commands.json
# Token cost: ~150 tokens (vs 2,650 for full file)
```

**Project Templates** (one language only):
```bash
jq '.rust' references/project_templates.json
# Token cost: ~200 tokens (vs 1,955 for full file)
```

**Security Patterns** (one level only):
```bash
jq '.recommended_deny_set.standard' references/security_patterns.json
# Token cost: ~100 tokens (vs 805 for full file)
```

**Permission Profiles** (one profile only):
```bash
jq '.development' assets/permission_profiles.json
# Token cost: ~200 tokens (vs 1,240 for full file)
```

### Executing Scripts

**ONLY execute when workflow instructs**:

- **detect_project.py** - When project type ambiguous or need recommendations
- **apply_permissions.py** - When all rules gathered, handles backup/validation/writing
- **validate_config.py** - When user requests validation or troubleshooting

---

## Safety Rules - Always Apply

Every permission operation MUST:

1. **Load security patterns**: `jq '.recommended_deny_set.standard' references/security_patterns.json`
2. **Apply minimum deny rules**: See `references/security_patterns.json#recommended_deny_set.standard` for full list (14 rules)
3. **Create backup** before any settings write (automatic via `scripts/apply_permissions.py`)
4. **Validate syntax** before applying (automatic via `scripts/apply_permissions.py`)

---

## Token Budget Management

**Budget Tiers**:
- Simple request (CLI tool): <5,000 tokens
- Medium request (project setup): <7,000 tokens
- Complex request (unknown tool): <10,000 tokens
- Warning threshold: >10,000 tokens

**Cost Optimization**:
- Use grep/jq for references (90% token savings)
- Load only needed workflow guide
- Execute scripts instead of explaining them
- Avoid loading examples unless requested

See `references/token_tracking_template.md` for tracking template.

---

## Error Handling

**If workflow guide not found**:
- Proceed with best-effort inline logic
- Inform user of missing guide
- Suggest filing an issue

**If reference file not found**:
- Attempt operation without reference
- For unknown tools -> use web search
- Warn user about limited functionality

**If script execution fails**:
- Show error message to user
- Suggest manual permission editing
- Provide settings file location

**If validation fails**:
- Report specific errors
- Suggest fixes
- Offer to restore from backup

---

## Skill Integration Points

**Other Skills** (invoke when appropriate):
- **gemini skill**: If user mentions "gemini CLI" and skill available

**MCP Tools** (priority order for research):
1. `mcp__perplexity-ask__perplexity_ask` (preferred)
2. `mcp__brave-search__brave_web_search` (fallback)
3. `WebSearch` (final fallback)

---

## Success Criteria Checklist

Permission operation complete when:
- Backup created (timestamped)
- Permissions validated (syntax + conflicts)
- Safety rules applied (deny patterns)
- Settings written successfully
- User informed of changes
- Restart reminder provided

---

## Quick Start Examples

| Request | Route |
|---------|-------|
| Enable git (read-only) | `cli-tool-workflow.md` |
| Make markdown editable | `file-pattern-workflow.md` |
| Setup TypeScript project | `project-setup-workflow.md` |
| Apply development profile | `profile-application-workflow.md` |

See `guides/workflows/` for complete workflow documentation.

---

## Workflow Pattern

Every request follows this pattern:

1. **Classify intent** using decision tree
2. **Route to workflow** based on detection
3. **Load workflow guide** from guides/workflows/
4. **Follow workflow** step-by-step
5. **Load references** surgically as needed
6. **Execute scripts** when required
7. **Track token budget** throughout
8. **Complete operation** per success criteria
9. **Inform user** of changes

**Remember**: Load only needed workflow, use grep/jq for references, execute scripts for heavy lifting, apply safety rules always.

---

**End of Tier 2 (SKILL.md)**
