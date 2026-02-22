---
name: spec-inspect
description: |
  Specification quality checker for spec-generator documents.

  Validates requirement.md, design.md, tasks.md for consistency, completeness, and quality.
  Detects requirement ID mismatches, missing sections, contradictions, and ambiguous expressions.

  English triggers: "inspect specs", "check specification quality", "validate requirements"
  日本語トリガー: 「仕様書を検査」「品質チェック」「仕様を検証」「spec-inspect実行」
license: MIT
---

# spec-inspect — Specification Quality Checker

Automatically validates spec-generator output (requirement.md, design.md, tasks.md) and reports quality issues.

## Language Rules

1. **Auto-detect input language** → output in the same language
2. Japanese input → Japanese report output
3. English input → English report output
4. Explicit override takes priority (e.g., "in English", "日本語で")

## When to Run

- After spec-generator completes (auto-suggested)
- Before registering Issues with spec-to-issue
- After updating specification documents

## Execution Flow

### Step 1: Locate Project Path

Identify the `.specs/{project-name}/` path from user input or current context.

**Validation**:
- `.specs/{project-name}/requirement.md` exists
- `.specs/{project-name}/design.md` exists
- `.specs/{project-name}/tasks.md` exists

If any file is missing, display an error message and exit.

### Step 2: Read Specifications

Read all three specification files:

```
requirement_content = Read(".specs/{project-name}/requirement.md")
design_content = Read(".specs/{project-name}/design.md")
tasks_content = Read(".specs/{project-name}/tasks.md")
```

### Step 3: Run Quality Checks

Execute the following checks sequentially. Add detected issues to an issues list.

#### Check 1: Requirement ID Consistency [CRITICAL]

**Purpose**: Verify that requirement IDs defined in requirement.md are correctly referenced in design.md and tasks.md.

**Procedure**:
1. Extract requirement IDs from requirement.md (regex: `\[(REQ|NFR|CON|ASM|T)-\d{3,}\]`)
2. Extract referenced requirement IDs from design.md
3. Extract referenced requirement IDs from tasks.md

**Detection patterns**:

- **[CRITICAL]** ID referenced in design.md or tasks.md but not defined in requirement.md
  ```
  ID: CRITICAL-{seq}
  Title: "Requirement ID {req_id} does not exist"
  File: design.md or tasks.md
  Line: {line_number}
  Description: "{req_id} is referenced in {file} but not defined in requirement.md"
  Suggestion: "Add {req_id} to requirement.md or fix the reference"
  ```

- **[INFO]** ID defined in requirement.md but never referenced
  ```
  ID: INFO-{seq}
  Title: "Requirement ID {req_id} is unreferenced"
  File: requirement.md
  Line: {line_number}
  Description: "{req_id} is not linked to any design or task"
  Suggestion: "Is this requirement still needed? Consider removing if unnecessary"
  ```

- **[WARNING]** Insufficient requirement coverage (calculate design.md reference rate for all IDs including [NFR-XXX]; warn if below 100%)
  ```
  ID: WARNING-{seq}
  Title: "Requirement coverage: {covered}/{total} ({percentage}%)"
  Description: "The following requirements are not mentioned in design.md: {uncovered_list}"
  Suggestion: "Add coverage for each requirement in design.md"
  ```

#### Check 2: Required Section Validation [WARNING]

**Purpose**: Confirm each spec has the expected structure.

**Required sections**:
- **requirement.md**: Overview, Functional Requirements, Non-Functional Requirements, Constraints, Assumptions
- **design.md**: Architecture Overview, Technology Stack, Data Model, API Design (if applicable), Security Design
- **tasks.md**: Task List, Priority

**Procedure**:
1. Extract Markdown headings (`#` or `##`) from each file
2. Check for required sections (partial match, case-insensitive)

**Detection pattern**:
- **[WARNING]** Required section missing
  ```
  ID: WARNING-{seq}
  Title: "Required section '{section_name}' is missing"
  File: {filename}
  Line: 1
  Description: "{filename} should contain a '{section_name}' section"
  Suggestion: "Add a '{section_name}' section"
  ```

#### Check 3: Contradiction Detection [WARNING]

**Purpose**: Detect contradictory statements across specification documents.

**Detection examples**:
- Technology stack mismatch (e.g., requirement says PostgreSQL, design says MySQL)
- Numeric mismatch (e.g., requirement says "100 users", design says "1000 users")
- API endpoint mismatch
- Components designed in design.md but missing from tasks.md implementation plan

**Procedure**:
1. Extract technical proper nouns from requirement.md (database names, library names, etc.)
2. Check if the same concept is referred to by a different name in design.md
3. Detect numeric data inconsistencies

**Detection pattern**:
- **[WARNING]** Contradictory statements
  ```
  ID: WARNING-{seq}
  Title: "Contradiction: {concept}"
  File: requirement.md, design.md
  Line: {line_number}
  Description: "requirement.md states {value1}, but design.md states {value2}"
  Suggestion: "Unify to one value"
  ```

#### Check 4: Ambiguous Expression Detection [INFO]

**Purpose**: Detect vague expressions that lack the specificity needed for implementation.

**Detection keywords** (English):
- "appropriately", "as much as possible", "reasonable", "adequate"
- "fast", "large amount", "many" (without numeric criteria)
- "to be determined", "under consideration", "planned" (not finalized)

**Detection keywords** (Japanese):
- 「適切に」「できる限り」「なるべく」「ある程度」
- 「高速に」「大量の」「多くの」（数値基準なし）
- 「検討する」「考慮する」「予定」（確定していない）

**Procedure**:
1. Search all three specs for ambiguous keywords
2. List all occurrences

**Detection pattern**:
- **[INFO]** Ambiguous expression
  ```
  ID: INFO-{seq}
  Title: "Ambiguous expression: '{keyword}'"
  File: {filename}
  Line: {line_number}
  Description: "The expression '{context}' may be interpreted differently by implementors"
  Suggestion: "Specify concrete numbers or criteria"
  ```

#### Check 5: Terminology Consistency [WARNING]

**Purpose**: Ensure consistent terminology usage across all specifications.

**Detection patterns**:
- Same concept expressed with different terms (e.g., "user" vs "member", "delete" vs "remove")
- Inconsistent abbreviations (e.g., "DB" and "database" mixed)
- Terms deviating from glossary definitions (if a glossary section exists)

**Procedure**:
1. Extract key nouns/concepts from all three specs
2. Detect synonym/near-synonym pairs
3. Cross-reference with glossary section if present

**Output**: `WARNING-{seq}` "Terminology inconsistency: '{term1}' vs '{term2}'" + recommendation to unify

#### Check 6: Design-to-Task Coverage [WARNING]

**Purpose**: Verify that design.md components have corresponding implementation tasks in tasks.md.

**Detection patterns**:
- Designed component/module with no corresponding task
- DB schema design with no migration task
- API design with no implementation task

**Procedure**:
1. Extract major component/module names from design.md
2. Check if each component has a corresponding task in tasks.md
3. List uncovered design elements

**Output**: `WARNING-{seq}` "Design element '{component}' has no corresponding task"

#### Check 7: Dependency Validation [WARNING]

**Purpose**: Verify that task dependencies are logically correct.

**Detection patterns**:
- Circular dependencies (Task A depends on B, B depends on A)
- Undefined prerequisite tasks (dependency on non-existent task)
- Obviously reversed dependency order (e.g., test task before implementation task)

**Procedure**:
1. Extract inter-task dependencies from tasks.md
2. Build dependency graph and detect cycles
3. Flag logically inconsistent ordering

**Output**: `WARNING-{seq}` "Circular dependency: {taskA} ⇄ {taskB}" or "Illogical dependency order"

#### Check 8: Infeasible Requirement Warning [WARNING]

**Purpose**: Detect technically difficult or contradictory requirements.

**Detection patterns**:
- Conflicting non-functional requirements (e.g., "response under 1ms" + "encrypt all data")
- Features difficult to achieve with the chosen technology stack
- Unrealistic resource requirements (e.g., unlimited storage, zero downtime)

**Output**: `WARNING-{seq}` "Potentially infeasible: {requirement}" + alternative suggestion

#### Check 9: Missing Requirement Detection [WARNING]

**Purpose**: Detect clearly necessary but undocumented requirements.

**Detection patterns**:
- Authentication present → no security requirements
- Database used → no backup/recovery requirements
- External API integration → no error handling/retry requirements
- File upload → no size/format restrictions
- User data storage → no privacy/data protection requirements

**Procedure**:
1. Extract feature characteristics from requirement.md / design.md
2. Match against detection patterns and check for corresponding requirements

**Output**: `WARNING-{seq}` "Possible missing requirement: {requirement_type} for {feature} is undefined"

#### Check 10: Naming Convention Consistency [INFO]

**Purpose**: Verify consistent naming conventions across specifications.

**Detection patterns**:
- Mixed kebab-case / camelCase / snake_case
- Naming variations in the same context (e.g., `user_id` vs `userId` vs `userID`)
- Convention violations in constants, table names, component names

**Procedure**:
1. Extract code-related names (variable names, table names, API names, etc.) from design.md / tasks.md
2. Gather naming pattern statistics and flag minority patterns

**Output**: `INFO-{seq}` "Naming convention inconsistency: {pattern1} ({count1} occurrences) vs {pattern2} ({count2} occurrences)"

#### Check 11: Directory Structure Consistency [INFO]

**Purpose**: Verify consistent directory structure and placement rules.

**Detection patterns**:
- Inconsistent placement of similar components (e.g., `src/features/A/` vs `src/components/B/`)
- Mixed test file placement (`tests/` vs `__tests__/`)
- Scattered configuration files

**Output**: `INFO-{seq}` "Directory structure inconsistency: {pattern description}"

#### Check 12: Reinvention Detection [INFO]

**Purpose**: Detect custom implementations of functionality already available in declared libraries.

**Detection patterns**:
- Reimplementation of features provided by libraries in the technology stack
  - e.g., Custom date handling when date-fns is included
  - e.g., Custom validation when Zod is included
- Reimplementation of standard library features

**Procedure**:
1. Extract library list from the "Technology Stack" section of design.md
2. Compare against implementation tasks in tasks.md to detect overlapping functionality

**Output**: `INFO-{seq}` "Possible reinvention: {task} could be handled by {library_name}"

#### Check 13: Project Rule Compliance [WARNING]

**Purpose**: Check that specifications comply with project-specific rules defined in CLAUDE.md / AGENTS.md.

**Procedure**:
1. Read `CLAUDE.md`, `AGENTS.md`, and `.claude/` from the project root
2. Extract coding conventions, prohibited patterns, and required patterns
3. Cross-reference with design.md / tasks.md

**Detection examples**:
- "TypeScript strict mode required" → not mentioned in design.md
- "JWT authentication required" → design.md uses a different approach
- "console.log prohibited" → tasks.md describes console.log usage

**Output**: `WARNING-{seq}` "Project rule violation: {rule} conflicts with {violation_location}"

#### Check 14: API / UI Naming Convention Consistency [WARNING]

**Purpose**: Validate API and UI naming conventions (for web app / API specifications).

**Detection patterns**:
- Inconsistent singular/plural in REST resource names (`/user/:id` vs `/comments`)
- Non-RESTful verb paths (`/getUsers` → `/users` (GET) is recommended)
- Path casing inconsistency (`/user-profile` vs `/userProfile`)
- Path parameter format inconsistency (`:id` vs `{id}`)
- Screen component suffix inconsistency (`Screen` vs `Page`)

**Procedure**:
1. Extract endpoint list from the "API Design" section of design.md
2. Extract screen names / routing from tasks.md
3. Identify majority pattern as "recommended" and flag minority pattern

**Output**: `WARNING-{seq}` "API naming inconsistency: {details}" + unification suggestion

#### Check 15: Documentation Update Analysis [INFO]

**Purpose**: Analyze whether existing documentation needs updating based on spec content.

**Target documents**:
- README.md, CLAUDE.md, AGENTS.md
- Files in documentation directories specified by CLAUDE.md (e.g., `docs/`)

**Procedure**:
1. Check for README.md, CLAUDE.md, AGENTS.md at project root
2. Parse CLAUDE.md for documentation directory references and scan them
3. Cross-reference with spec content:
   - New feature → not listed in README.md feature list
   - New API endpoint → not in API docs
   - Technology stack change → setup guide not updated
   - New coding convention → CLAUDE.md / AGENTS.md not updated
4. Propose needed updates as DOC-XXX tasks

**Output**:
- `INFO-{seq}` "Documentation update needed: {filename} — {reason}"
- Suggest additions to tasks.md:
  ```
  ### Documentation Update Tasks (auto-detected)
  - [ ] DOC-001: Update {section} in {filename} ({reason})
  ```

### Step 4: Generate Summary

Aggregate detected issues by severity:
- Critical: {count}
- Warning: {count}
- Info: {count}

### Step 5: Generate Report

Write a Markdown report to `.specs/{project-name}/inspection-report.md`.

**Template**: `# spec-inspect Report — {project_name}` → Inspection summary (date, targets, counts) → Severity sections (CRITICAL / WARNING / INFO). Each issue: `### [{issue.id}] {issue.title}` + file:line, details, suggestion. Display "None" for sections with 0 issues.

Save with Write tool to `.specs/{project-name}/inspection-report.md`.

### Step 6: Console Output

Display a user-friendly summary:

```
spec-inspect complete

Results:
  CRITICAL: {count}
  WARNING:  {count}
  INFO:     {count}

{if critical_count > 0}
Critical issues found. Fix before implementation.

{if critical_count == 0}
No critical issues found.

Report: .specs/{project-name}/inspection-report.md
```

### Step 7: Next Action Suggestion (Workflow Integration)

Use AskUserQuestion to suggest the next action based on results (header: "Next action" / "次のアクション", multiSelect: false):

| Result | Question | Options |
|--------|----------|---------|
| Critical issues | "{count} critical issue(s) found. Action needed." / "Critical問題が{count}件。修正が必要です" | "Fix and re-run" / "修正して再実行", "Skip to Issue registration" / "スキップしてIssue登録", "Cancel" / "キャンセル" |
| Warning/Info only | "{count} warning(s) found. Proceed to Issue registration?" / "Warningが{count}件。Issue登録しますか？" | "Register Issue" / "Issue登録する", "Fix and re-run" / "修正して再実行", "Cancel" / "キャンセル" |
| No issues | "Quality check passed. Register Issues?" / "品質チェック完了。Issue登録しますか？" | "Register Issue" / "Issue登録する", "Cancel" / "キャンセル" |

**Handling user selection**:
- "Register Issue" / "Skip to Issue registration" → invoke spec-to-issue skill
- "Fix and re-run" → exit (user fixes and re-runs manually)
- "Cancel" → exit

### Step 8: Save Handoff Data for spec-to-issue

Save inspection results as a temporary file for the next skill:

```json
{
  "project_path": ".specs/{project-name}",
  "project_name": "{project-name}",
  "critical_count": 0,
  "warning_count": 0,
  "info_count": 0,
  "report_path": ".specs/{project-name}/inspection-report.md",
  "timestamp": "{ISO 8601}"
}
```

Save with Write tool:
```
Write(".specs/{project-name}/.inspection_result.json", json_content)
```

## Error Handling

- **File not found**: "Error: Required file not found" + missing filename, path verification guidance
- **Read error**: "Error: Failed to read file" + filename, error details
- **ID extraction error**: Continue processing and display "Warning: Partial error during requirement ID extraction"

## Implementation Notes

- **Efficiency**: Minimize Read operations for large files. Use search tools for efficient scanning. Show progress after each check.
- **Accuracy**: Use partial matching for section names. Consider context for contradiction detection. Flexibly match both Japanese and English content.
- **UX**: Errors should include concrete, actionable fix suggestions. Use emoji indicators for visual clarity.

## Constraints

- Supports specifications in both Japanese and English (natural language analysis has inherent accuracy limits)
- Only Markdown-format specifications are supported
- Depends on spec-generator output format

## Success Criteria

- Requirement ID reference error detection rate: 100%
- Missing required section detection rate: 100%
- Contradiction detection accuracy: Best effort (depends on LLM reasoning capability)
- Processing time: Under 30 seconds for combined spec files under 3000 lines
