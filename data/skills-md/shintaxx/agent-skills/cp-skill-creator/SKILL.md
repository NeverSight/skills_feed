---
name: cp-skill-creator
description: Creates and evaluates Agent Skills following the official specification. Use when the user wants to create a new skill, scaffold a skill directory, evaluate or validate an existing skill, or needs guidance on skill structure and format.
metadata:
  author: skill-repo
  version: "1.0"
---

# Skill Creator

This skill helps you create new Agent Skills that follow the official specification.

## When to Use

- User wants to create a new skill
- User needs to scaffold a skill directory structure
- User asks about skill format or structure
- User wants to evaluate or validate an existing skill (e.g., "〜のスキルを評価して")

## Steps to Create a New Skill

### 1. Gather Requirements

Ask the user for:
- **Skill name**: Must be lowercase, use hyphens, 1-64 characters (e.g., `pdf-processing`, `code-review`)
- **Description**: What the skill does and when to use it (1-1024 characters)
- **Optional**: License, compatibility requirements, metadata

### 2. Confirm Installation Location

**IMPORTANT:** Before creating any files, confirm the installation location with the user.

**Default Installation Path:** `.github/skills`

The installation path varies by tool/environment. Determine a reasonable default based on:
- Current working directory structure
- Existing skills directories (e.g., `./skills/`, `./.claude/skills/`)
- Project conventions

Then ask the user for confirmation:
```
スキル「{skill-name}」を以下の場所に作成します：
  {full-path}/{skill-name}/

この場所でよろしいですか？別の場所を指定することもできます。
```

Only proceed after user confirms the location.

### 3. Create Directory Structure

Create the skill directory at the confirmed location:

```
skill-name/
├── SKILL.md          # Required - main skill file
├── references/       # Optional - additional documentation
├── scripts/          # Optional - executable code
└── assets/           # Optional - static resources
```

### 4. Create SKILL.md

The SKILL.md file must contain:

1. **YAML Frontmatter** (required):
   ```yaml
   ---
   name: skill-name
   description: A clear description of what this skill does and when to use it.
   ---
   ```

2. **Markdown Body** (recommended sections):
   - Step-by-step instructions
   - Examples of inputs and outputs
   - Common edge cases

### 5. Validation Checklist

Before finishing, verify:
- [ ] `name` field matches the directory name
- [ ] `name` is lowercase with hyphens only, no consecutive hyphens
- [ ] `description` clearly explains what the skill does AND when to use it
- [ ] Main SKILL.md is under 500 lines
- [ ] File references use relative paths from skill root

## Name Constraints

The `name` field must:
- Be 1-64 characters
- Use only lowercase letters, numbers, and hyphens (`a-z`, `0-9`, `-`)
- Not start or end with `-`
- Not contain consecutive hyphens (`--`)
- Match the parent directory name exactly

**Valid**: `pdf-processing`, `code-review`, `data-analysis`
**Invalid**: `PDF-Processing`, `-pdf`, `pdf--processing`, `pdf-`

## Example SKILL.md

```markdown
---
name: example-skill
description: Does X and Y. Use when the user mentions A, B, or C.
license: MIT
metadata:
  author: your-name
  version: "1.0"
---

# Example Skill

Instructions for the agent go here.

## Usage

1. First step
2. Second step

## Examples

Input: ...
Output: ...
```

## Optional Directories

### references/
Additional documentation loaded on demand. Keep files focused and small.

### scripts/
Executable code (Python, Bash, JavaScript). Should be self-contained with clear error messages.

### assets/
Static resources: templates, images, data files, schemas.

## Evaluating an Existing Skill

When the user asks to evaluate a skill (e.g., "〜のスキルを評価して"), follow these steps:

### 1. Read the Specification

First, read [skills-spec.md](references/skills-spec.md) to understand the complete format requirements.

### 2. Read the Target Skill

Read the target skill's SKILL.md file and any related files.

### 3. Check Against Specification

Evaluate the skill against these criteria:

**Required Checks:**
- [ ] SKILL.md exists in the skill directory
- [ ] YAML frontmatter is present and valid
- [ ] `name` field exists and follows naming rules:
  - 1-64 characters
  - Lowercase letters, numbers, hyphens only
  - No leading/trailing hyphens
  - No consecutive hyphens (`--`)
  - Matches parent directory name
- [ ] `description` field exists (1-1024 characters)
- [ ] Description explains both WHAT the skill does AND WHEN to use it

**Recommended Checks:**
- [ ] SKILL.md is under 500 lines
- [ ] Body contains step-by-step instructions
- [ ] Examples are provided
- [ ] File references use relative paths
- [ ] Reference files are focused and not too large

**Optional Field Checks (if present):**
- [ ] `license` field is concise
- [ ] `compatibility` field is under 500 characters
- [ ] `metadata` has string keys and string values
- [ ] `allowed-tools` is space-delimited

### 4. Report Findings

Present the evaluation results to the user:
1. List all issues found (errors and warnings)
2. Provide specific suggestions for each issue
3. Show example corrections where applicable

### 5. Wait for User Permission

**IMPORTANT:** Do NOT make any modifications automatically. Always:
1. Present the evaluation report
2. Ask the user if they want to apply the suggested fixes
3. Only proceed with modifications after explicit user approval

Example response format:
```
## 評価結果

### エラー (必須修正)
1. `name` フィールドが...

### 警告 (推奨修正)
1. `description` が...

### 修正案
[具体的な修正内容]

これらの修正を適用しますか？
```

## Reference

For the complete specification, see [skills-spec.md](references/skills-spec.md).
