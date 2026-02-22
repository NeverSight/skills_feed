---
name: make-commits
description: Analyzes git changes and generates semantic commits iteratively with [Why]/[What]/[Impact] structure. Groups related files, allows manual editing, and executes git add + commit. Use when you have uncommitted changes and need structured messages following conventional commits (feat, fix, docs, refactor, etc.).
license: MIT
metadata:
  author: aroldolanderos
  version: "1.0.0"
---

# Make Commits

Generate semantic commits by analyzing changes file by file.
Iterative flow with manual confirmation.

## Workflow

### 1. Get changes

```bash
git status --porcelain
```

Identify modified (M) and untracked (??) files.

### 2. Group related files

Group together if:

- Same module/directory
  (models.py + schemas.py + resources.py)
- Cohesive logical change:
  - (Python) auth.py + auth_decorators.py
  - (PHP) Controller + views + routes
  - (Nuxt) components + store + server
- Same feature or bug fix

Do NOT group if:

- Different domains
- One file is a refactor, another is a new feature
- Changes are independent

### 3. Analyze changes per group

For each file group:

```bash
git diff <file>
```

Read the full diff. Identify:

- **Motivation**: What problem does it solve?
- **Implementation**: What changed technically?
- **Impact**: How does it affect the app/users?

### 4. Generate semantic message

Structure:

```
<type>: <concise subject>

[Why]: <motivation in 1 sentence>

[What]: <implementation in 1 sentence>

[Impact]: <impact in 1 sentence>
```

**Types**: feat, fix, docs, style, refactor, perf, test, chore

See `references/commit-conventions.md` for detailed guide.

### 5. Confirm with user

Use `AskUserQuestion`:

**Question**: "What to do with this commit?"

**Options**:

1. Confirm and execute
2. Edit message
3. Skip for now

### 6. Execute confirmed commit

```bash
git add <file1> <file2> ...
git commit -m "<message>"
```

### 7. Continue with next group

Repeat steps 3-6 for each group.

At the end: summary of commits made and skipped groups.

## Example

**Input**: User invokes `/make-commits`

**Step 1**: Run git status

```
M  src/modules/diagram/models.py
M  src/modules/diagram/schemas.py
M  src/modules/diagram/resources.py
```

**Step 2**: Group (same module)

```
Group 1: [models.py, schemas.py, resources.py]
```

**Step 3**: Read diffs for all 3 files

**Step 4**: Generate message

```
feat: Add diagram validation with centralized schemas

[Why]: Diagrams needed consistent validation to prevent
invalid data in the database.

[What]: Implemented Marshmallow schemas to validate
required/optional fields and centralized logic in
DiagramStore.

[Impact]: All diagram operations validate data; errors
return 400 with clear messages instead of crashes.
```

**Step 5**: Ask user

```
What to do with this commit?
1. Confirm and execute
2. Edit message
3. Skip for now
```

**Step 6**: If confirmed, execute

```bash
git add src/modules/diagram/models.py \
        src/modules/diagram/schemas.py \
        src/modules/diagram/resources.py
git commit -m "feat: Add diagram validation..."
```

## Important Notes

- Only commits (user pushes manually)
- Uses native tools: Bash, Read, AskUserQuestion
- Focus on intelligent analysis, not orchestration
- Respects files already ignored by .gitignore

**IMPORTANT - Professional commits:**

- Do NOT add "Co-Authored-By: Claude" or Anthropic mentions
- Do NOT mention AI/assistant anywhere in the commit
- Commits must be 100% professional with no tool references
- The message should reflect only the actual technical change
