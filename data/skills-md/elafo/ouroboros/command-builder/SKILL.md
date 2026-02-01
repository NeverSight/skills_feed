---
name: command-builder
description: Guide creation of Claude Code Commands with step-by-step workflows, argument handling, frontmatter configuration, and testing. Ensures Commands follow best practices and correct YAML structure. Use when creating Commands, building slash commands, making user-triggered workflows, or when users want explicit command execution.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Command Builder

You are an expert guide for creating Claude Code Commands. Commands are user-triggered workflows that execute when explicitly invoked with a slash command (e.g., `/deploy`, `/test`, `/review-pr`).

## Core Responsibilities

When helping create Commands:
1. Guide through complete creation workflow
2. Design intuitive command names and arguments
3. Generate valid YAML frontmatter
4. Create clear, actionable command content
5. Design testing protocol
6. Validate before deployment

---

## Command vs. Other Artifacts

**Use Commands when:**
- ✅ User needs explicit control over execution
- ✅ Parameters vary each time (arguments)
- ✅ Multi-step workflow needs to be standardized
- ✅ Team needs shared, repeatable processes
- ✅ Operation is potentially destructive (requires confirmation)

**DON'T use Commands when:**
- ❌ Automatic activation needed → Use Skill
- ❌ Complex delegation needed → Use Subagent
- ❌ Automatic execution needed → Use Hook (with caution)
- ❌ One-time operation → Use main conversation

---

## Command Creation Workflow

### Step 1: Planning (5-10 min)

**Gather requirements:**

```
To create an effective Command, I need to understand:

1. **What workflow will this Command standardize?**
   Example: "Deploy to staging environment"

2. **What are the steps involved?**
   List the sequence of operations

3. **What parameters/arguments are needed?**
   Example: environment name, version number, branch name

4. **Who will use this Command?**
   Individual developer? Whole team? CI/CD?

5. **How often will it be used?**
   Daily? Weekly? Per release?

6. **What could go wrong?**
   Think about error scenarios
```

**Output of Step 1:** Clear understanding of Command purpose, steps, and parameters

---

### Step 2: Command Naming (5 min)

**Naming guidelines:**

**Structure:** `/verb-noun` or `/verb-noun-context`

**Good examples:**
- `/deploy-staging` - Clear action and target
- `/run-tests` - Clear action
- `/review-pr` - Clear action and target
- `/create-migration` - Clear action and artifact
- `/check-dependencies` - Clear action

**Bad examples:**
- ❌ `/do-stuff` - Vague
- ❌ `/x` - Cryptic
- ❌ `/deploy-staging-environment-with-validation` - Too long
- ❌ `/DeployStaging` - Wrong case (use kebab-case)

**Naming rules:**
- Lowercase only
- Hyphens for word separation (kebab-case)
- Start with verb (action-oriented)
- Be specific but concise
- Max 32 characters
- Memorable and intuitive

**Consider namespacing for plugin Commands:**
```
/plugin-name:command-name

Examples:
/deploy:staging
/test:unit
/db:migrate
```

---

### Step 3: Argument Design (10 min)

**Types of arguments:**

**1. Required positional arguments:**
```bash
/deploy [environment]
# Usage: /deploy staging
```

**2. Optional positional arguments:**
```bash
/deploy [environment] [version]
# Usage: /deploy staging v1.2.3
# Usage: /deploy staging
```

**3. Named arguments (future feature):**
```bash
/deploy --env=staging --version=v1.2.3
```

**Argument best practices:**

```markdown
✅ DO:
- Keep arguments to 0-3 (more is confusing)
- Use clear, descriptive names
- Provide defaults where sensible
- Document all arguments clearly
- Validate arguments in command content

❌ DON'T:
- Require more than 3 arguments
- Use abbreviations (--env vs --e)
- Have ambiguous argument order
- Forget to validate input
```

**Common patterns:**

```bash
# No arguments (simple workflow)
/run-tests

# Single argument (target)
/deploy [environment]

# Two arguments (target + parameter)
/create-migration [name]
/review-pr [pr-number]

# Optional argument (default behavior)
/build [target]
# Where target defaults to "all"
```

---

### Step 4: Directory Setup (2 min)

**Command file location:**

**For project Commands:**
```bash
mkdir -p .claude/commands
```

**For user Commands:**
```bash
mkdir -p ~/.claude/commands
```

**File naming:**
```bash
# Command: /deploy-staging
# File: deploy-staging.md

# Command: /run-tests
# File: run-tests.md

# With namespace: /plugin:command
# File: plugin/command.md
```

**Validation:**
```bash
# Verify directory exists
test -d .claude/commands && echo "✅ Commands directory exists"

# Check file naming
# File name (without .md) should match command name
```

---

### Step 5: YAML Frontmatter (5 min)

**Basic Command structure:**

```markdown
---
name: command-name
description: Brief description of what this command does
---

# Command Content

[Actual instructions that Claude will follow]
```

**With arguments:**

```markdown
---
name: deploy
description: Deploy application to specified environment
arguments:
  - name: environment
    description: Target environment (staging, production)
    required: true
  - name: version
    description: Version to deploy (defaults to current)
    required: false
---

# Deploy Command

When this command is invoked, deploy the application following these steps:

1. Validate the environment argument...
```

**Complete example:**

```yaml
---
name: review-pr
description: Comprehensive code review of a GitHub pull request with security and performance analysis
arguments:
  - name: pr-number
    description: Pull request number to review
    required: true
model: sonnet
allowed-tools: Read, Bash, Grep, Glob, WebFetch
---
```

**Frontmatter fields:**

| Field | Required | Description | Notes |
|-------|----------|-------------|-------|
| `name` | ✅ | Command name | Must match filename (without .md) |
| `description` | ✅ | What command does | Shown in /help, 50-200 chars |
| `arguments` | ❌ | Argument definitions | Array of argument specs |
| `model` | ❌ | AI model to use | `sonnet`, `opus`, or `haiku` |
| `allowed-tools` | ❌ | Tool restrictions | Comma-separated list |

**Validation checklist:**
- [ ] Opening `---` on line 1
- [ ] Closing `---` after fields
- [ ] `name` matches filename exactly
- [ ] `description` is clear and concise
- [ ] Arguments (if any) are properly formatted
- [ ] No tabs (use spaces)
- [ ] No smart quotes (use straight quotes)

---

### Step 6: Content Development (15-45 min)

**Command content structure:**

```markdown
---
[YAML frontmatter]
---

# [Command Name]: [One-line purpose]

[1-2 paragraph overview explaining what this command does]

## Arguments

[If command has arguments, document them clearly]

**[argument-name]** (required/optional): Description and valid values

## Process

[Clear, numbered steps for Claude to follow]

1. **[Step name]**: [Detailed instructions]
   - Sub-step or clarification
   - What to check or validate

2. **[Step name]**: [Detailed instructions]

3. **[Step name]**: [Detailed instructions]

## Validation

[Checks to perform before completing]

- [ ] Validation check 1
- [ ] Validation check 2

## Error Handling

[Common errors and how to handle them]

**Error scenario 1:** What to do
**Error scenario 2:** What to do

## Success Criteria

[How to know the command completed successfully]

- ✅ Criteria 1
- ✅ Criteria 2

## Examples

[Show 2-3 example invocations]

### Example 1: [Scenario]
\`\`\`
/command-name arg1 arg2
\`\`\`

Expected result: [What happens]

### Example 2: [Different scenario]
\`\`\`
/command-name arg1
\`\`\`

Expected result: [What happens]
```

**Content guidelines:**

**1. Be explicit and actionable:**
```markdown
✅ Good:
1. Use the Bash tool to run `npm test`
2. If tests fail, read the error output and identify failing tests
3. Use the Edit tool to fix the identified issues

❌ Bad:
1. Run tests
2. Fix errors if any
```

**2. Include validation:**
```markdown
Before proceeding, verify:
- [ ] All required files exist
- [ ] Environment variables are set
- [ ] User has confirmed the action
```

**3. Handle errors explicitly:**
```markdown
## Error Handling

**If tests fail:**
1. Display the failing test output
2. Ask user if they want to:
   - Fix tests automatically
   - Review test failures first
   - Abort the command

**If environment is not found:**
1. List available environments
2. Ask user to specify valid environment
```

**4. Use tool calls correctly:**
```markdown
Use the Bash tool to execute:
\`\`\`bash
npm run build
\`\`\`

Use the Read tool to examine the configuration:
- File: .env.staging

Use the Edit tool to update the version number.
```

**5. Include examples:**
Show realistic usage scenarios with expected outcomes.

---

### Step 7: Testing Protocol (10-15 min)

**Test 1: Basic Invocation**
```bash
/command-name

# Expected: Command activates and runs through steps
```

**Test 2: With Arguments**
```bash
/command-name arg1

# Expected: Argument is correctly parsed and used
```

**Test 3: Invalid Arguments**
```bash
/command-name invalid-arg

# Expected: Clear error message, guidance on valid values
```

**Test 4: Edge Cases**
```bash
# Missing required argument
/command-name

# Extra arguments
/command-name arg1 arg2 arg3

# Expected: Appropriate handling and user feedback
```

**Test 5: Error Scenarios**
```bash
# Simulate failure conditions
# Expected: Graceful error handling, helpful messages
```

**Testing checklist:**
- [ ] Command activates with correct name
- [ ] Arguments are parsed correctly
- [ ] Required arguments are enforced
- [ ] Optional arguments work with defaults
- [ ] Invalid input produces clear errors
- [ ] Command completes successfully in happy path
- [ ] Error scenarios are handled gracefully
- [ ] Output is clear and actionable

---

### Step 8: Documentation (5 min)

**Add to project README:**

```markdown
## Commands

### /command-name [arguments]
**Purpose:** [Brief description]
**Arguments:**
- `arg1` (required): Description
- `arg2` (optional): Description

**Example:**
\`\`\`bash
/command-name value1 value2
\`\`\`

**When to use:** [Scenarios where this command is helpful]
```

**Commit to git (project Commands):**
```bash
git add .claude/commands/command-name.md
git commit -m "Add /command-name command for [purpose]"
git push
```

---

## Common Command Patterns

### Pattern 1: Deployment Command

```markdown
---
name: deploy
description: Deploy application to specified environment with validation and rollback support
arguments:
  - name: environment
    description: Target environment (staging, production)
    required: true
model: sonnet
---

# Deploy Command

Deploy the application to the specified environment with pre-deployment validation.

## Arguments

**environment** (required): Target environment. Valid values: `staging`, `production`

## Process

1. **Validate environment argument**
   - Check that environment is either "staging" or "production"
   - If invalid, show valid options and abort

2. **Pre-deployment checks**
   - Run tests: `npm test`
   - Build project: `npm run build`
   - Validate configuration exists: `.env.{environment}`

3. **Confirm deployment**
   - Show what will be deployed (branch, commit, environment)
   - Ask user to confirm: "Deploy to {environment}? (yes/no)"

4. **Execute deployment**
   - Run deployment command based on environment
   - Staging: `npm run deploy:staging`
   - Production: `npm run deploy:production`

5. **Verify deployment**
   - Check deployment status
   - Run smoke tests if available
   - Display deployment URL

## Error Handling

**If tests fail:** Abort deployment, show test failures

**If build fails:** Abort deployment, show build errors

**If user declines confirmation:** Abort with message "Deployment cancelled"

## Success Criteria

- ✅ All tests pass
- ✅ Build completes successfully
- ✅ Deployment command executes without errors
- ✅ Deployment URL is accessible

## Examples

### Example 1: Deploy to staging
\`\`\`
/deploy staging
\`\`\`

### Example 2: Deploy to production
\`\`\`
/deploy production
\`\`\`
```

---

### Pattern 2: Testing Command

```markdown
---
name: run-tests
description: Run project tests with optional filtering and reporting
arguments:
  - name: filter
    description: Optional test filter pattern
    required: false
---

# Run Tests Command

Execute project tests with optional filtering and detailed reporting.

## Arguments

**filter** (optional): Pattern to filter tests. Examples: "unit", "integration", "auth/*"

## Process

1. **Determine test command**
   - If filter provided: `npm test -- {filter}`
   - If no filter: `npm test`

2. **Execute tests**
   - Run the test command using Bash tool
   - Capture output for analysis

3. **Analyze results**
   - Count passing/failing tests
   - Identify any failing test suites
   - Check for coverage information

4. **Report results**
   - Display summary (X passed, Y failed)
   - Show failing tests with details
   - Offer to help fix failures

## Error Handling

**If no tests found:** Inform user and check test configuration

**If tests fail:** Show failures and ask if user wants help fixing them

## Success Criteria

- ✅ All tests pass
- ✅ Clear summary displayed
- ✅ Coverage meets threshold (if configured)

## Examples

### Example 1: Run all tests
\`\`\`
/run-tests
\`\`\`

### Example 2: Run specific tests
\`\`\`
/run-tests auth
\`\`\`
```

---

### Pattern 3: Code Review Command

```markdown
---
name: review-pr
description: Comprehensive code review of a GitHub pull request
arguments:
  - name: pr-number
    description: Pull request number to review
    required: true
model: sonnet
allowed-tools: Read, Bash, Grep, Glob
---

# Review Pull Request Command

Perform a thorough code review of a GitHub pull request.

## Arguments

**pr-number** (required): The GitHub pull request number to review

## Process

1. **Fetch PR information**
   - Use `gh pr view {pr-number}` to get PR details
   - Get list of changed files
   - Get diff for review

2. **Analyze changes**
   - Review each changed file
   - Check for:
     - Code quality issues
     - Security vulnerabilities
     - Performance concerns
     - Test coverage
     - Documentation updates

3. **Generate review**
   - Summarize changes
   - List findings by severity (critical, major, minor)
   - Provide specific suggestions for improvement

4. **Format output**
   - Create structured review comments
   - Offer to post review to GitHub (with confirmation)

## Error Handling

**If PR not found:** Verify PR number and repository

**If gh CLI not available:** Instruct user to install GitHub CLI

## Success Criteria

- ✅ All files reviewed
- ✅ Findings clearly categorized
- ✅ Actionable feedback provided

## Examples

### Example 1: Review PR #123
\`\`\`
/review-pr 123
\`\`\`
```

---

### Pattern 4: Generator Command

```markdown
---
name: create-component
description: Generate a new React component with tests and styles
arguments:
  - name: component-name
    description: Name of component to create (PascalCase)
    required: true
---

# Create Component Command

Generate a new React component with associated test and style files.

## Arguments

**component-name** (required): Component name in PascalCase (e.g., "UserProfile")

## Process

1. **Validate component name**
   - Check PascalCase format
   - Ensure name doesn't already exist
   - Create safe file name (kebab-case)

2. **Create component file**
   - Generate React component boilerplate
   - Path: `src/components/{kebab-name}/{PascalName}.tsx`

3. **Create test file**
   - Generate test boilerplate
   - Path: `src/components/{kebab-name}/{PascalName}.test.tsx`

4. **Create style file**
   - Generate styles boilerplate
   - Path: `src/components/{kebab-name}/{PascalName}.module.css`

5. **Create index file**
   - Generate barrel export
   - Path: `src/components/{kebab-name}/index.ts`

6. **Update imports**
   - Add to main components index if it exists

## Error Handling

**If component exists:** Ask user if they want to overwrite

**If invalid name format:** Show correct format and ask for valid name

## Success Criteria

- ✅ All files created successfully
- ✅ Component renders without errors
- ✅ Tests pass
- ✅ Files follow project conventions

## Examples

### Example 1: Create UserProfile component
\`\`\`
/create-component UserProfile
\`\`\`

This creates:
- src/components/user-profile/UserProfile.tsx
- src/components/user-profile/UserProfile.test.tsx
- src/components/user-profile/UserProfile.module.css
- src/components/user-profile/index.ts
```

---

## Troubleshooting

### Issue 1: Command Not Found

**Symptoms:** `/command-name` doesn't activate

**Diagnosis:**
```bash
# Check file exists
ls -la .claude/commands/command-name.md

# Validate YAML
python3 -c "
import yaml
content = open('.claude/commands/command-name.md').read()
frontmatter = content.split('---')[1]
yaml.safe_load(frontmatter)
"
```

**Common causes:**
1. File name doesn't match command name
2. YAML syntax error
3. File in wrong location
4. Session not restarted

---

### Issue 2: Arguments Not Working

**Symptoms:** Command runs but arguments aren't used

**Solution:**
Ensure command content explicitly handles arguments:

```markdown
## Process

1. **Extract arguments**
   - Environment: {environment} (from command invocation)
   - Validate: must be "staging" or "production"
```

Reference arguments in your content as `{argument-name}`.

---

### Issue 3: YAML Validation Errors

**Common errors:**

```yaml
# ❌ Missing closing ---
---
name: deploy
description: Deploy app

# ❌ Array syntax for allowed-tools
allowed-tools:
  - Read
  - Write

# ❌ Tab character
---
name: deploy
	description: Deploy app
```

**Fixes:**
- Always close with `---`
- Use comma-separated: `allowed-tools: Read, Write`
- Use spaces, never tabs
- Validate with Python or online YAML validator

---

### Issue 4: Command Runs But Fails

**Symptoms:** Command activates but doesn't complete successfully

**Debugging steps:**
1. Check command content for clarity
2. Verify tool calls are correct
3. Add explicit error handling
4. Test each step manually
5. Add validation checks

---

## Advanced Patterns

### Conditional Logic

```markdown
## Process

1. **Check if CI environment**
   - Use Bash: `echo $CI`
   - If CI=true: Skip interactive prompts
   - If CI=false: Ask for user confirmation

2. **Environment-specific behavior**
   - If production: Require extra validation
   - If staging: Allow faster deployment
```

### User Confirmation

```markdown
3. **Confirm destructive action**
   - Display what will be deleted/modified
   - Ask: "Are you sure you want to proceed? (yes/no)"
   - If no: Abort command with friendly message
   - If yes: Continue with operation
```

### Multi-stage Operations

```markdown
## Process

1. **Stage 1: Preparation**
   - Validate prerequisites
   - Set up environment

2. **Stage 2: Execution**
   - Perform main operation
   - Monitor progress

3. **Stage 3: Verification**
   - Validate results
   - Run post-operation checks

4. **Stage 4: Cleanup**
   - Remove temporary files
   - Reset state if needed
```

---

## Quality Guidelines

A well-crafted Command has:
- ✅ Clear, intuitive name
- ✅ Valid YAML frontmatter
- ✅ Explicit, actionable steps
- ✅ Clear argument documentation
- ✅ Error handling for common issues
- ✅ User confirmation for destructive operations
- ✅ Validation checks
- ✅ Success criteria
- ✅ 2-3 realistic examples
- ✅ No placeholders or TODOs

**Target quality:** Grade A (≥0.90 on validation framework)

---

## Success Criteria

A successful Command creation results in:
- ✅ Command activates with correct invocation
- ✅ Arguments are handled properly
- ✅ Steps are clear and actionable
- ✅ Errors are handled gracefully
- ✅ User understands when to use command
- ✅ Command completes successfully in testing
- ✅ Documented for team (if project command)

---

**Remember: Commands are about standardizing workflows and giving users explicit control. Make them clear, safe, and easy to use!**
