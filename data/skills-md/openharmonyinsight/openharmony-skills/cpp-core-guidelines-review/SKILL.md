---
name: cpp-core-guidelines-review
description: Parallel C++ Core Guidelines code review using multiple specialized sub-agents. Use when reviewing C++ code, modules, or files against C++ Core Guidelines to identify violations. Each sub-agent reviews against a specific guideline section (Functions, Classes, Resource Management, etc.) and outputs findings to separate markdown files in the review/ directory, followed by a consolidated summary.
---

# C++ Core Guidelines Review

## Overview

Review C++ code against the C++ Core Guidelines by launching parallel sub-agents, each analyzing code against a specific guideline section. This skill ensures comprehensive coverage while maintaining high confidence in violation identification.

## Workflow

### Step 1: Understand Scope Clarification

Before launching any sub-agents, clarify the review scope with the user:

1. **Target files/directories**: Which C++ source files or directories to review?
2. **File patterns**: What file extensions should be included? (e.g., `.cpp`, `.h`, `.hpp`)
3. **Exclusions**: Any files or directories to exclude?

**Important**: Do not proceed until the scope is clearly defined and unambiguous.

### Step 2: Launch Parallel Sub-Agents

**CRITICAL REQUIREMENTS**:
- You MUST launch one sub-agent for **EVERY** file in `references/Content/`. Do not skip any files. Each guideline section requires its own dedicated sub-agent.
- Use the **guideline-section-reviewer** agent in `agents/guideline-section-reviewer.md` from this plugin for each sub-agent.

**Parallel launch strategy**: To maximize performance, launch all sub-agents in parallel by sending multiple Task tool calls in a single response message. The Task tool documentation explicitly states: "When the user specifies that they want you to run agents 'in parallel', you MUST send a single message with multiple Task tool use content blocks."

Launch one sub-agent per guideline section. Each sub-agent:
- Reviews **only** against rules in its assigned guideline file
- Outputs findings to `<current-working-directory>/review/<SectionName>.md`
- Reports violations with: file path, line numbers, code snippet, and specific rule(s) violated

**Agent invocation process**:
1. **Read the agent template**: Read the agent definition from `agents/guideline-section-reviewer.md`
2. **Substitute parameters**: Replace the template variables in the agent file with actual values:
   - `{{SECTION_NAME}}`: The display name of the section (e.g., "Functions")
   - `{{SECTION_FILE}}`: The filename of the section in `references/Content/` (e.g., "Functions.md")
   - `{{TARGET_FILES_PATTERN}}`: The files/directories to review (e.g., "src/**/*.cpp" or specific file paths)
   - `{{OUTPUT_DIR}}`: The output directory (typically `<current-working-directory>/review`)
   - `{{DATE}}`: Current date in YYYY-MM-DD format
   - `{{FILES_COUNT}}`: Number of files being reviewed
   - `{{VIOLATION_COUNT}}`: Placeholder, will be filled by agent
3. **Launch the agent**: Use the Task tool with `subagent_type=general` and the substituted prompt as the agent's instruction

**Example invocation**:
```
For section "Functions":
- Read agent template from agents/guideline-section-reviewer.md
- Substitute: SECTION_NAME="Functions", SECTION_FILE="Functions.md", etc.
- Launch guideline-section-reviewer agent with substituted prompt
```

The agent will:
1. Read the guideline section from the plugin's `references/Content/` directory
2. Review the target files against that section's rules
3. Output findings to `<OUTPUT_DIR>/<SECTION_NAME>.md`
4. Report violations with file paths, line numbers, code snippets, and specific rule violations

### Step 3: Wait for All Sub-Agents

After launching all sub-agents, collect their task IDs and wait for completion:

**Waiting process**:
1. **Track task IDs**: Store the task ID returned by each Task tool invocation
2. **Wait for completion**: For each task ID, use `TaskOutput` with:
   - `task_id`: The task ID from the sub-agent launch
   - `block=true`: Wait until the sub-agent completes
   - `timeout=600000` (10 minutes): Maximum wait time per agent
3. **Verify success**: Check that each sub-agent:
   - Completed without errors
   - Created its output file in `<current-working-directory>/review/<SectionName>.md`
   - Did not modify any source files

**Error handling**:
- If a sub-agent fails: Report the error to the user and continue with other agents
- If timeout occurs: Note which agents timed out and report to user
- If output file missing: Indicate which section's review is incomplete

**Verification checklist**:
- [ ] All sub-agents have been launched
- [ ] All sub-agents have completed (or reported failures)
- [ ] Output files exist for each completed section
- [ ] No source files were modified

### Step 4: Generate Summary

After all sub-agents complete, create `<current-working-directory>/review/Summary.md` with a comprehensive analysis of all findings.

**Process**:
1. Read all section review files from `<current-working-directory>/review/*.md` (excluding Summary.md itself)
2. Aggregate violation counts, affected files, and rule violations
3. Generate summary using the template below

**Summary.md template**:

```markdown
# C++ Core Guidelines Review Summary

## Overview

**Date**: YYYY-MM-DD
**Review Scope**: <Files/directories reviewed>
**Total Sections Reviewed**: <Number of sections completed>
**Total Violations Found**: <Total count across all sections>

## Summary by Section

| Section | Violations | Most Violated Rule |
|---------|------------|-------------------|
| Functions | N | F.15, ... |
| Classes and Class Hierarchies | N | C.7, ... |
| Resource Management | N | R.1, ... |
| [Continue for all sections] | | |

## Summary by File

| File | Total Violations | Top Violation Categories |
|------|------------------|--------------------------|
| path/to/file1.cpp | N | Resource Management, Error Handling |
| path/to/file2.h | M | Const Correctness, Interfaces |
| [Continue for affected files] | | |

## Top Violations by Frequency

| Rank | Rule ID | Rule Summary | Count |
|------|---------|--------------|-------|
| 1 | F.15 | Prefer simple and default constructs | N |
| 2 | R.3 | Raw pointers should not be used | M |
| [Continue] | | | |

## Critical Findings

### High-Priority Issues
<List violations with high impact or security implications>

### Most Common Patterns
<Identify recurring violation patterns across the codebase>

## Detailed Section Breakdown

### Functions (N violations)
<Brief summary of key violations in this section>
See: [Functions.md](Functions.md)

### Classes and Class Hierarchies (N violations)
<Brief summary of key violations in this section>
See: [Classes and Class Hierarchies.md](Classes%20and%20Class%20Hierarchies.md)

### [Continue for all sections with violations]

## Recommendations

1. **Immediate Actions**: <Critical violations that should be addressed soon>
2. **Process Improvements**: <Suggestions to avoid common violations>
3. **Training Topics**: <Areas where team education may help>

## Review Metadata

- **Sections Completed**: <List of sections that completed>
- **Sections Skipped/Failed**: <List of sections that had issues>
- **Total Files Reviewed**: <Count>
- **Lines of Code Reviewed**: <If available>
```

**Key requirements for summary**:
- Include exact violation counts aggregated from all section reports
- Sort tables by violation count (descending) where applicable
- Link to individual section reports for detailed findings
- Highlight patterns and systemic issues
- Provide actionable recommendations based on findings

## Critical Constraints (Highest Priority)

1. **No modifications**: This skill and all sub-agents MUST NOT modify reviewed files. Write operations ONLY to `<current-working-directory>/review/` directory.
2. **Main session non-involvement**: Main conversation MUST NOT perform code review. Only coordinate sub-agents.
3. **Section-specific enforcement**: Each sub-agent reviews ONLY against its assigned section. Cross-section violations are not reported.
4. **Rule correspondence**: Every reported violation MUST map to a specific guideline rule. Unmappable findings are invalid.
5. **High confidence threshold**: Only report violations with high confidence. Uncertain cases must be omitted.
6. **Violations only**: Report ONLY guideline violations. Do NOT report code that follows guidelines correctly. Positive/conforming code must NOT appear in findings.

## C++ Core Guidelines Structure

The C++ Core Guidelines reference files are bundled in this skill's `references/` directory:
- `Introduction.md` - Overview and glossary
- `Content/` - Individual guideline sections

Each section contains multiple rules with:
- Rule identifier (e.g., "C.7", "F.15")
- Rule statement
- Rationale (Reason)
- Examples (positive/negative)
- Exceptions (if applicable)
- Enforcement suggestions

## User Interaction Patterns

**Example 1**: Review specific files
```
User: "Review src/transaction.cpp and src/account.h against C++ Core Guidelines"
```
→ Clarify scope, then launch sub-agents for those files.

**Example 2**: Review directory
```
User: "Review all C++ files in the services/ directory"
```
→ Clarify file patterns and exclusions, then launch sub-agents.

**Example 3**: Review against specific sections
```
User: "Review using only Resource Management and Error Handling guidelines"
```
→ Launch only those two sub-agents.
