---
name: code-review-orchestrator
description: This skill should be used when the user asks to "review code", "do a code review", "review my branch", "review MR !1234", "review PR #567", "review feature/auth branch", "review feature/auth vs dev", "check code quality", "review entire project", "review all code", or wants to orchestrate multiple code review skills/subagents. Coordinates parallel code reviews using multiple review skills and generates comprehensive summary reports.
version: 0.3.1
---

# Code Review Orchestrator

Orchestrate comprehensive code reviews by coordinating multiple review skills and subagents in parallel, then consolidate findings into actionable reports.

## Purpose

This skill manages the complete code review workflow:
- Collect and organize code content for review (diffs, commits, branches, MR/PR info)
- Coordinate multiple subagents using different review skills
- Consolidate individual review reports into comprehensive summaries
- Help users identify and fix issues

## Debug Mode

**Current Status**: 🔍 Debug mode is ENABLED

This skill includes debug outputs (marked with 🔍) to help track execution progress:
- Step indicators: `[Step X/6]`
- Checkpoints: `[Checkpoint N]`
- Progress tracking and status displays
- Detailed information at each stage

**To disable debug mode**: Remove all lines marked with 🔍 from this skill file.

## When to Use

Trigger this skill when users request code review with phrases like:
- "Review my code"
- "Review feature/auth branch"
- "Review MR !1234" / "Review PR #567"
- "Review feature/auth vs dev branch"
- "Do a comprehensive code review"

## Workflow

**DEBUG MODE ENABLED**: This skill includes debug outputs to track execution progress.

### Step 1: Determine Review Scope

**🔍 DEBUG [Step 1/6]**: Starting - Determine Review Scope

Identify what code to review based on user input:

**Review Sources:**
- **Branch**: Single branch (e.g., `feature/auth`) - review all changes in branch
- **Branch Comparison**: Branch A vs Branch B (e.g., `feature/auth` vs `dev`) - **IMPORTANT**: Find merge base and diff from merge base to branch A's HEAD
- **MR/PR**: Merge Request (GitLab) or Pull Request (GitHub) by number or URL
- **Project**: Monorepo with multiple subprojects - ask which to review
- **Full Project**: Multiple independent projects or entire codebase - collect all project paths

**Required Information:**
- Branch names (if comparing branches)
- MR/PR number or URL
- Project paths (for monorepos or full project review)
- Repository URL (if not current directory)

**For Full Project Review:**
When user asks to "review entire project" or "review all code":
1. Ask user to specify which projects/directories to review
2. For each project, check if it's a git repository
3. Collect project metadata (tech stack, LOC, file count)
4. Confirm with user before proceeding

### Step 2: Establish Working Directory

**🔍 DEBUG [Step 2/6]**: Establishing working directory

**IMPORTANT**: Working directory name MUST include date and sequence number to avoid conflicts.

**Directory Naming Convention**: `{review_name}-{YYYYMMDD}-{sequence}`

**Generate unique working directory**:
```bash
# Get current date
DATE=$(date +%Y%m%d)

# Base directory name
BASE_DIR="{review_name}-${DATE}"

# Find existing directories with same base
EXISTING=$(ls -d reviews/${BASE_DIR}-* 2>/dev/null | wc -l)

# Calculate next sequence number
SEQUENCE=$((EXISTING + 1))

# Final directory name
WORKING_DIR="${BASE_DIR}-${SEQUENCE}"
```

**Examples**:
```
First review on 2026-01-30:    mr557-aihub-refactor-20260130-1
Second review on same day:     mr557-aihub-refactor-20260130-2
First review next day:         mr557-aihub-refactor-20260131-1
```

**Full path**: `{project_root}/reviews/{review_name}-{YYYYMMDD}-{sequence}`

**Implementation**:
```bash
# Example implementation
project_root="/home/user/myapp"
review_name="auth-feature"
date=$(date +%Y%m%d)

# Check for existing reviews today
existing_dirs=$(find "$project_root/reviews" -maxdepth 1 -name "${review_name}-${date}-*" | wc -l)
sequence=$((existing_dirs + 1))

working_dir="$project_root/reviews/${review_name}-${date}-${sequence}"
mkdir -p "$working_dir"
```

**Ask user for confirmation with generated directory name** (optional, can be auto-generated)

**Directory Structure:**
```
reviews/{review_name}-{YYYYMMDD}-{sequence}/
├── code-context.json                     # All review metadata
├── diff.patch                             # Git diff output
├── commits.json                           # Commit history
├── branch-info.json                       # Branch details
├── DEBUG-SESSION.md                       # Debug session log (always uppercase)
├── {review_name}-{YYYYMMDD}-{sequence}-comprehensive-summary.md # Final report
└── reports/                               # Individual skill reports
    ├── skill1-report.md
    ├── skill2-report.md
    └── ...
```

**IMPORTANT File Naming Conventions:**
1. **Working directory**: `{review_name}-{YYYYMMDD}-{sequence}` (date + sequence for uniqueness)
2. **Summary file**: `{review_name}-{YYYYMMDD}-{sequence}-comprehensive-summary.md` (include date+sequence)
3. **Debug session file**: `DEBUG-SESSION.md` (always uppercase, fixed name)
4. **Individual reports**: `{skill-name}-report.md` (use skill's short name)
5. **Context files**: lowercase with hyphens (code-context.json, diff.patch, etc.)

### Step 3: Collect and Save Code Content

**🔍 DEBUG [Step 3/6]**: Collecting code context and metadata

Collect comprehensive review information and save to working directory:

**Use `scripts/collect-review-data.sh`** to automate data collection.

**Save as `code-context.json`:**
```json
{
  "review_type": "branch_comparison|branch|mr|pr",
  "source_branch": "feature/auth",
  "target_branch": "dev",
  "merge_base": "abc123",
  "mr_number": "!1234",
  "pr_number": "567",
  "repository": "git@gitlab.com:group/project.git",
  "project_path": "/path/to/project",
  "working_directory": "/path/to/reviews/auth-feature-20260130-1",
  "review_date": "2026-01-30",
  "review_sequence": 1,
  "timestamp": "2026-01-30T14:30:22Z"
}
```

**Save as `diff.patch`:**
- Use `git diff merge_base...source_branch` for branch comparison
- Use `git diff dev...feature/auth` format (three dots) for correct merge base
- Include full context for review

**Save as `commits.json`:**
```json
{
  "commits": [
    {
      "hash": "def456",
      "author": "John Doe",
      "date": "2025-01-28T09:00:00Z",
      "message": "Add login form",
      "files_changed": ["src/auth/login.js"]
    }
  ]
}
```

**Save as `branch-info.json`:**
```json
{
  "source_branch": {
    "name": "feature/auth",
    "head_commit": "def456",
    "is_merged": false
  },
  "target_branch": {
    "name": "dev",
    "head_commit": "abc123"
  }
}
```

**For Full Project Review (non-Git or multi-project):**
```json
{
  "review_type": "full_project",
  "review_name": "full-project-review",
  "working_directory": "/path/to/reviews/full-project-review-20260130-1",
  "review_date": "2026-01-30",
  "review_sequence": 1,
  "projects": [
    {
      "name": "frontend",
      "path": "/path/to/frontend",
      "tech_stack": ["Nuxt.js", "Vue 2"],
      "language": "javascript"
    },
    {
      "name": "backend",
      "path": "/path/to/backend",
      "tech_stack": ["Spring Boot", "MyBatis"],
      "language": "java"
    }
  ]
}
```

**Critical for Branch Comparison:**
When comparing branch A vs branch B:
1. Find merge base: `git merge-base A B`
2. Diff from merge base to A: `git diff merge_base...A`
3. This ensures only unique changes in A are reviewed

**Confirm with User:**
After collecting code context, present to user using AskUserQuestion tool:

**🔍 DEBUG [Checkpoint 1]**: Display collected information and request confirmation

**IMPORTANT**: Use AskUserQuestion tool for user confirmation, not text prompts.

**Example AskUserQuestion call:**
```python
AskUserQuestion(
    questions=[
        {
            "question": "代码审查信息已收集，是否继续？",
            "header": "确认审查",
            "options": [
                {
                    "label": "继续审查",
                    "description": "开始执行代码审查，启动并行子代理"
                },
                {
                    "label": "取消",
                    "description": "取消本次审查，退出技能"
                }
            ],
            "multiSelect": false
        }
    ]
)
```

**Information to present in question description:**
```
Review Type: Full project review
Projects: 2 projects (frontend, backend)

Frontend:
  - Path: /projects/bupt/eduiot-lab
  - LOC: ~13,800
  - Tech Stack: Nuxt.js, Vue 2, Element UI

Backend:
  - Path: /projects/bupt/space-server
  - LOC: ~7,000
  - Tech Stack: Spring Boot, MyBatis, MySQL

Working Directory: /projects/bupt/reviews/full-project-review-20260130-1
```

**🔍 DEBUG**: Wait for user confirmation via AskUserQuestion before proceeding

**DO NOT proceed to Step 4 without user confirmation.**

### Step 4: Discover Available Review Skills

**🔍 DEBUG [Step 4/6]**: Discovering available review skills

**🔍 DEBUG**: Check system-reminder for available skills list

Identify which code review skills are available in the current environment.

**Check available skills:**
Look for skills with these patterns in their description:
- "code review", "review code", "review MR/PR"
- "security", "performance", "quality", "lint"

**Common review skills:**
- `code-review:code-review` - General code review
- `code-review-orchestrator` - Orchestrates parallel reviews (this skill)
- `pr-review-toolkit:review-pr` - Comprehensive PR review with multi-dimensional analysis
- `pr-review-toolkit:silent-failure-hunter` - Silent failure and error handling detection
- `pr-review-toolkit:code-simplifier` - Code simplification and clarity analysis
- `pr-review-toolkit:comment-analyzer` - Comment accuracy and completeness review
- `pr-review-toolkit:pr-test-analyzer` - Test coverage and quality analysis for PRs
- `pr-review-toolkit:type-design-analyzer` - Type design and encapsulation review
- `superpowers:code-reviewer` - Post-development review against plan
- `superpowers:receiving-code-review` - Receiving and implementing code review feedback
- `code-documentation:code-reviewer` - Elite code review expert
- `security-scanning:security-auditor` - Security vulnerability scan
- `security-scanning:threat-modeling-expert` - Threat modeling and security analysis
- `comprehensive-review:code-reviewer` - Deep code analysis and architecture review
- `comprehensive-review:architect-review` - Architecture and design pattern review
- `comprehensive-review:security-auditor` - Comprehensive security audit
- `code-review-ai:code-review` - AI-powered code review
- `codebase-cleanup:code-reviewer` - Codebase cleanup and optimization review
- `feature-dev:code-reviewer` - Feature development code review
- `feature-dev:code-explorer` - Code exploration and understanding

**Skill Discovery Process:**
1. Review the list of available skills in system-reminder
2. Identify skills whose description mentions "review", "security", "quality", etc.
3. Filter to skills relevant to code review
4. Present findings to user

**Present options to user using AskUserQuestion tool:**

**🔍 DEBUG [Checkpoint 2]**: Display discovered skills and request selection

**IMPORTANT**: Use AskUserQuestion tool for skill selection, not text prompts.

**Example AskUserQuestion call:**
```python
# Dynamically build options based on available skills
skill_options = [
    {"label": "code-review:code-review", "description": "通用代码质量审查"},
    {"label": "pr-review-toolkit:review-pr", "description": "全面的PR/MR审查"},
    {"label": "security-scanning:security-auditor", "description": "安全漏洞扫描"},
    # ... add more discovered skills
]

AskUserQuestion(
    questions=[
        {
            "question": f"发现 {len(skill_options)} 个审查技能。请选择要使用的技能：",
            "header": "选择审查技能",
            "options": skill_options + [
                {
                    "label": "使用所有技能",
                    "description": "使用所有发现的技能进行全方位审查"
                },
                {
                    "label": "推荐组合",
                    "description": "使用推荐的技能组合（通用审查 + 安全审查 + PR审查）"
                }
            ],
            "multiSelect": True
        }
    ]
)
```

**Information to include in question:**
```
Found {count} review skills:
1. skill-name - Brief description
2. skill-name - Brief description
...

Projects to review:
- Project details...

Recommended: Use 2-4 different skills for comprehensive coverage
```

**🔍 DEBUG**: Show user's skill selection: `[skill1, skill2, ...]`

**Ask user to select which skills to use using AskUserQuestion.**
**DO NOT proceed to Step 5 without user skill selection.**

### Step 5: Launch Parallel Subagents

**🔍 DEBUG [Step 5/6]**: Launching parallel subagents with review skills

**🔍 DEBUG**: Show selected skills and subagent configuration before launch

**Use Task tool with run_in_background=true** to launch multiple subagents in parallel.

**CRITICAL**: Each subagent MUST use a DIFFERENT review skill via the Skill tool.

**Example parallel launch:**

**🔍 DEBUG [Checkpoint 3]**: Display subagent launch configuration

```
═════════════════════════════════════════════════════════
🚀 Launching Parallel Subagents
═════════════════════════════════════════════════════════

Subagent 1: code-review:code-review
  - Review scope: Frontend (Nuxt.js)
  - Output: reports/code-review-report.md

Subagent 2: security-scanning:security-auditor
  - Review scope: Both projects
  - Output: reports/security-report.md

Subagent 3: pr-review-toolkit:review-pr
  - Review scope: All files
  - Output: reports/pr-review-report.md
═════════════════════════════════════════════════════════
```

**🔍 DEBUG**: Track subagent status
```
Agent 1 (code-review): ⏳ Starting...
Agent 2 (security):    ⏳ Starting...
Agent 3 (pr-review):    ⏳ Starting...
```

**Provide each subagent with:**
- Location of `code-context.json`
- Location of `diff.patch` (for git reviews) OR project paths (for full project review)
- Output report path: `reports/{skill-name}-report.md`
- **INSTRUCTION to use Skill tool to invoke the review skill**

**Subagent Prompt Template:**
```markdown
You are reviewing code as part of a comprehensive code review.

**Your assigned skill**: {skill_name}

**Task**:
1. Use the Skill tool to invoke: {skill_name}
2. Provide the skill with:
   - Review scope: {scope_description}
   - Code location: {code_path}
   - Any additional context from code-context.json
3. Generate a comprehensive report following that skill's workflow
4. Save your report to: {output_path}

**IMPORTANT**:
- You MUST use the Skill tool to invoke {skill_name}
- Do NOT review code manually - let the skill guide you
- The skill will provide the specific review methodology
- Follow the skill's workflow exactly
```

**Example Task tool calls:**
```yaml
Task 1:
  subagent_type: general-purpose
  description: Review using code-review:code-review
  run_in_background: true
  prompt: |
    You are reviewing the frontend code using the code-review:code-review skill.
    Project path: /projects/bupt/eduiot-lab
    Output: /projects/bupt/reviews/full-project-review/reports/code-review-report.md
    Use the Skill tool to invoke code-review:code-review

Task 2:
  subagent_type: general-purpose
  description: Review using security-scanning:security-auditor
  run_in_background: true
  prompt: |
    You are reviewing both frontend and backend for security issues.
    Frontend: /projects/bupt/eduiot-lab
    Backend: /projects/bupt/space-server
    Output: /projects/bupt/reviews/full-project-review/reports/security-report.md
    Use the Skill tool to invoke security-scanning:security-auditor

Task 3:
  subagent_type: general-purpose
  description: Review using pr-review-toolkit:review-pr
  run_in_background: true
  prompt: |
    You are reviewing code quality using pr-review-toolkit:review-pr skill.
    Review all files in both projects.
    Output: /projects/bupt/reviews/full-project-review/reports/pr-review-report.md
    Use the Skill tool to invoke pr-review-toolkit:review-pr
```

**File Writing Strategy:**
- Subagents should use Write tool to save their reports
- If subagents cannot write files, they should output the full report content
- Main agent: Collect all outputs and save using Write tool
- Ensure `reports/` directory exists before launching subagents

**Wait for all subagents to complete** using TaskOutput tool before proceeding to Step 6.

**🔍 DEBUG**: Show subagent completion status
```
Agent 1 (code-review): ✅ Complete
Agent 2 (security):    ✅ Complete
Agent 3 (pr-review):    ✅ Complete

All reports generated successfully!
```

### Step 6: Generate Consolidated Summary

**🔍 DEBUG [Step 6/6]**: Generating consolidated summary from all reports

**🔍 DEBUG [Checkpoint 4]**: Display report collection status

```
═════════════════════════════════════════════════════════
📊 Collecting Reports from Subagents
═════════════════════════════════════════════════════════

Found 3 reports in reports/ directory:
✓ code-review-report.md (32 issues found)
✓ security-report.md (19 issues found)
✓ pr-review-report.md (25 issues found)

Total issues to consolidate: 76 issues
═════════════════════════════════════════════════════════
```

**🔍 DEBUG**: Show categorization progress
```
Categorizing issues by severity...
- Critical: 3 issues
- High: 13 issues
- Medium: 31 issues
- Low: 29 issues
```

**Read all individual reports** from `reports/` directory.

**Analyze findings and categorize by severity:**
- **Critical**: Security vulnerabilities, crashes, data loss risks
- **High**: Major bugs, performance issues, breaking changes
- **Medium**: Code smells, maintainability issues
- **Low**: Style issues, minor optimizations

**Create `{review_name}-{YYYYMMDD}-{sequence}-comprehensive-summary.md`:**

**IMPORTANT File Naming Convention:**
- **Summary file**: `{review_name}-{YYYYMMDD}-{sequence}-comprehensive-summary.md` (include date+sequence)
- **Debug session file**: `DEBUG-SESSION.md` (always uppercase, fixed name)

**Structure:**
```markdown
# Code Review Comprehensive Summary: {review_name}

## 🤖 Review Skills Used

This review used multiple AI skills, each analyzing from different perspectives:

| Skill Name | Focus Area | Key Contributions |
|------------|------------|-------------------|
| code-review:code-review | 代码质量与最佳实践 | 代码规范、潜在bug、可维护性 |
| security-scanning:security-auditor | 安全漏洞审计 | OWASP Top 10、注入攻击、认证授权 |
| pr-review-toolkit:review-pr | 全面PR审查 | 功能完整性、测试覆盖、文档 |

**Total Issues Found**: X issues (after deduplication)

## Overview
- Review Type: Branch comparison (feature/auth vs dev)
- Commits: 5 commits
- Files changed: 12 files
- Review Skills: 3 skills used in parallel
- Date: 2025-01-28

## Findings Summary
- Critical: 2 issues
- High: 5 issues
- Medium: 8 issues
- Low: 3 issues

## 🔴 Critical Issues

### 1. SQL Injection Risk in auth/login.js
- **Location**: `src/auth/login.js:45`
- **Severity**: Critical
- **Found by**: code-review:code-review, security-scanning:security-auditor
- **Issue**: User input directly concatenated into SQL query
- **Recommendation**: Use parameterized queries
- **Code snippet**:
  ```javascript
  // Current (unsafe)
  const query = `SELECT * FROM users WHERE name = '${username}'`

  // Suggested (safe)
  const query = 'SELECT * FROM users WHERE name = ?'
  db.query(query, [username])
  ```

### 2. Authentication Bypass
- **Location**: `src/auth/check.js:12`
- **Severity**: Critical
- **Found by**: security-scanning:security-auditor, pr-review-toolkit:review-pr
- **Issue**: Missing authentication check on admin endpoint
- **Recommendation**: Add authentication middleware

## 🟠 High Priority Issues

### 1. Missing Error Handling in API client
- **Location**: `src/api/client.js:78`
- **Severity**: High
- **Found by**: code-review:code-review
- **Issue**: No try-catch around fetch request
- **Recommendation**: Add error handling with retry logic

## 🟡 Medium Priority Issues

### 1. Inconsistent Naming Convention
- **Location**: Multiple files
- **Severity**: Medium
- **Found by**: code-review:code-review
- **Issue**: Mix of camelCase and snake_case
- **Recommendation**: Standardize on camelCase

## 🟢 Low Priority Issues

### 1. Unused Imports
- **Location**: `src/utils/helpers.js:3`
- **Severity**: Low
- **Found by**: code-review:code-review
- **Issue**: Import 'lodash' unused
- **Recommendation**: Remove unused imports

## 📊 Skill Contributions Summary

### code-review:code-review
**Issues Found**: X
**Focus**: 代码质量与最佳实践
**Key Findings**:
- Finding 1
- Finding 2

### security-scanning:security-auditor
**Issues Found**: Y
**Focus**: 安全漏洞审计
**Key Findings**:
- Finding 1
- Finding 2

### pr-review-toolkit:review-pr
**Issues Found**: Z
**Focus**: 全面PR审查
**Key Findings**:
- Finding 1
- Finding 2

## Detailed Reports

Individual skill reports:
- [code-review:code-review report](reports/code-review-report.md)
- [security-scanning:security-auditor report](reports/security-auditor-report.md)
- [pr-review-toolkit:review-pr report](reports/pr-review-report.md)
```

### Step 7: Interactive Issue Resolution

**After generating summary, present actionable next steps:**

```
Found 18 issues. Which issues would you like to fix?

Options:
1. Fix all Critical issues (2)
2. Fix all High priority issues (5)
3. Fix specific issues (select by number)
4. Review specific issues first
5. Skip fixing for now

Enter your choice:
```

**If user chooses to fix issues:**
- Use appropriate development skills (e.g., `feature-dev:feature-dev`)
- Create implementation plan for fixes
- Apply fixes with user confirmation
- Verify fixes don't introduce new issues

## Additional Resources

### Scripts

- **`scripts/collect-review-data.sh`** - Automates collection of diff, commits, branch info
- **`scripts/find-merge-base.sh`** - Finds merge base for branch comparison
- **`scripts/launch-subagents.sh`** - Launches parallel review subagents

### References

- **`references/subagent-coordination.md`** - Detailed guide on coordinating multiple subagents
- **`references/report-formatting.md`** - Report structure and formatting standards
- **`references/issue-categories.md`** - Issue classification and severity guidelines

### Examples

- **`examples/review-session-output/`** - Complete example of a review session
- **`examples/code-context-example.json`** - Sample code context file
- **`examples/summary-example.md`** - Sample consolidated summary

## Best Practices

### Branch Comparison

**Always use three-dot diff** (`git diff A...B`) for branch comparison:
- `git diff dev...feature/auth` - Changes since branches diverged
- NOT `git diff dev feature/auth` - Changes between branch heads (wrong)

**Example:**
```bash
# Find merge base
MERGE_BASE=$(git merge-base dev feature/auth)

# Diff from merge base to feature branch
git diff $MERGE_BASE...feature/auth > diff.patch
```

### Full Project Review

When reviewing entire projects or multiple independent projects:

**1. Discover Project Structure**
- Use `ls` and `find` to understand directory layout
- Check for package.json, pom.xml, requirements.txt, etc.
- Identify tech stack and language
- Count lines of code

**2. Collect Project Metadata**
```bash
# Example: Frontend project
cd /projects/bupt/eduiot-lab
find . -name "*.vue" -o -name "*.js" | wc -l  # Count files
cat package.json  # Identify framework

# Example: Backend project
cd /projects/bupt/space-server
find . -name "*.java" | wc -l  # Count files
cat pom.xml  # Identify framework
```

**3. Use Appropriate Review Skills**
- For frontend: code-review:code-review, javascript-typescript:javascript-pro
- For backend: code-review:code-review, jvm-languages:java-pro
- For security: security-scanning:security-auditor
- For architecture: code-review-ai:architect-review

**4. Coordinate Subagent Communication**
- Each subagent reviews independently
- No inter-subagent communication needed
- Main agent consolidates all reports
- Use file system for data sharing

### Parallel Subagent Execution

**Launch subagents in parallel** using Task tool with `run_in_background=true`:
```yaml
subagent_type: general-purpose
run_in_background: true
prompt: |
  Review the code in /path/to/diff.patch
  Use the code-review:code-review skill
  Output report to /path/to/reports/code-review-report.md
```

**Wait for completion** using TaskOutput tool before generating summary.

### Report Consolidation

**Read all reports** before generating summary:
- Use Read tool to load each report
- Extract findings with severity levels
- Cross-reference duplicate findings
- Prioritize by severity

**Categorize issues** using severity guidelines in `references/issue-categories.md`.

### User Interaction

**Ask before making changes**:
- Present issues in prioritized list
- Let user choose which to fix
- Confirm each fix before applying
- Provide rollback options

## Troubleshooting

### Project Not Recognized

**Problem**: Commands like `cd space-server` fail with "No such file or directory"

**Root Cause**: Skill assumes git workflow, but user has independent projects

**Solutions:**
1. Identify this is "full project review", not branch comparison
2. Use absolute paths to projects
3. Don't use `cd` - use full paths in commands
4. Ask user to confirm project paths

**Example:**
```bash
# WRONG
cd space-server && git log

# RIGHT
cd /projects/bupt/space-server && git log
# OR
git -C /projects/bupt/space-server log
```

### No Diff Output

**Problem**: Empty `diff.patch` file

**Solutions:**
- Verify branch names are correct
- Check merge base calculation
- Ensure branches have diverged
- Use `git log --oneline A..B` to verify commits exist

### Subagent Failures

**Problem**: Subagent crashes or times out

**Solutions:**
- Check subagent logs for errors
- Verify skill is available
- Reduce scope (fewer files)
- Increase timeout limits

### Subagents Cannot Write Files

**Problem**: Report files not created in `reports/` directory

**Root Cause**: Subagents may not have write permissions or Write tool access

**Solutions:**
1. Main agent creates `reports/` directory before launching subagents
2. Subagent attempts to write file using Write tool
3. If write fails, subagent outputs full report content as text
4. Main agent collects outputs and saves using Write tool

**Pattern:**
```yaml
# Main agent
mkdir -p reports/

# Launch subagent with fallback instruction
Task(prompt: |
  1. Perform review using {skill}
  2. Try to save report to: reports/{skill}-report.md
  3. If Write tool fails, output full report as markdown text
  4. Include "REPORT_START" and "REPORT_END" markers
)

# Main agent collects output
TaskOutput(task_id, block=true)
Read output file, extract report between markers
Save using Write tool
```

### Skills Not Discovered

**Problem**: No review skills found or presented to user

**Solutions:**
- Check system-reminder for available skills list
- Look for skills with "review" in description
- Ask user which skills they want to use
- Fall back to general-purpose agents with custom prompts

### Duplicate Findings

**Problem**: Multiple skills report same issue

**Solutions:**
- Group by file and line number
- Cite all skills that found it
- Consolidate into single finding
- Note which found it first

## Technical Notes

### Git Diff Formats

- **Two dots (`git diff A..B`)**: Diff between A and B tips
- **Three dots (`git diff A...B`)**: Diff from merge base to B (correct for review)
- **Use three dots** for branch comparison reviews

### Subagent Communication

- Each subagent works independently
- No inter-subagent communication needed
- Consolidation happens after all complete
- Use file system for data sharing

### Performance Considerations

- Large diffs (>10,000 lines): Consider splitting
- Many files (>100): Review in batches
- Many subagents (>5): Limit parallelism
- Cache results for repeated reviews
