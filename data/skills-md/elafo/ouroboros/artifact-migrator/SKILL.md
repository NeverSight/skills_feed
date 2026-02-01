---
name: artifact-migrator
description: Help migrate and update existing Claude Code artifacts (Skills, Commands, Subagents, Hooks) when specifications change or best practices evolve. Detect outdated patterns, suggest improvements, and guide migration process. Use when artifacts stop working, need updates, or when Claude Code specifications change.
allowed-tools: Read, Edit, Grep, Glob, Bash
---

# Artifact Migrator

You are an expert guide for migrating and updating Claude Code artifacts. As Claude Code evolves, artifacts may need updates to work with new specifications or follow updated best practices.

## Core Responsibilities

When helping migrate artifacts:
1. Detect outdated patterns and specifications
2. Identify breaking changes in artifacts
3. Suggest specific improvements
4. Guide migration step-by-step
5. Validate migrated artifacts
6. Preserve functionality during migration
7. Document changes made

---

## Understanding Artifact Migration

### Why Migrate?

Artifacts may need migration when:
- **Specification changes** - Claude Code updates YAML format
- **Best practices evolve** - New patterns emerge
- **Activation issues** - Skills stop activating reliably
- **Tool changes** - Available tools change
- **Performance improvements** - More efficient patterns available
- **Security updates** - Security best practices change

### Migration vs. Validation

**Artifact Migrator (this skill):**
- Updates outdated artifacts to new standards
- Detects specification changes
- Suggests improvements over time
- Handles breaking changes

**Artifact Validator:**
- Checks current artifact quality
- Validates against current spec
- Grades artifacts
- No modification

---

## Migration Workflow

### Step 1: Discovery and Assessment (5-10 min)

**Identify what needs migration:**

```
To assess migration needs, I need to:

1. **What artifacts need review?**
   - Specific artifact? (e.g., "my-skill")
   - All artifacts in project?
   - Artifacts that stopped working?

2. **What's the problem?**
   - Not activating?
   - Errors during execution?
   - Following old patterns?
   - General health check?

3. **When were artifacts created?**
   - Recent (< 1 month)
   - Older (> 1 month)
   - Unknown

4. **Any specific issues noticed?**
   - Describe symptoms
```

**Automatic detection:**

```bash
# Find all artifacts
find .claude -name "SKILL.md" -o -name "*.md" -path "*/.claude/commands/*" -o -name "*.md" -path "*/.claude/agents/*" -o -name "*.json" -path "*/.claude/hooks/*"

# Check for common outdated patterns
grep -r "old-pattern" .claude/
```

---

### Step 2: Artifact Analysis (10-15 min)

**For each artifact, check:**

#### Skills (SKILL.md files)

**Location:** `.claude/skills/*/SKILL.md`

**Common issues:**

1. **Outdated YAML format:**
```yaml
# ❌ Old: Array syntax for tools
---
name: my-skill
allowed-tools:
  - Read
  - Write
---

# ✅ New: Comma-separated
---
name: my-skill
allowed-tools: Read, Write
---
```

2. **Vague descriptions:**
```yaml
# ❌ Old: Too vague
description: Helps with PDFs

# ✅ New: Specific with trigger keywords
description: Extract text, images, and tables from PDFs. Fill PDF forms, merge documents, convert between formats (PDF↔Word). Use when working with PDF files or document processing tasks.
```

3. **Missing fields:**
```yaml
# ❌ Old: No description
---
name: my-skill
---

# ✅ New: Complete frontmatter
---
name: my-skill
description: [Detailed description with trigger keywords]
allowed-tools: Read, Grep, Glob
---
```

4. **Poor activation triggers:**
- Description lacks specific keywords
- Too generic or too narrow
- Missing "Use when..." clause

---

#### Commands (*.md files in commands/)

**Location:** `.claude/commands/*.md`

**Common issues:**

1. **Incomplete frontmatter:**
```yaml
# ❌ Old: Missing description
---
name: deploy
---

# ✅ New: Complete
---
name: deploy
description: Deploy application to specified environment with validation
arguments:
  - name: environment
    description: Target environment (staging, production)
    required: true
---
```

2. **Unclear content:**
```markdown
# ❌ Old: Vague instructions
Deploy the app.

# ✅ New: Explicit steps
## Process

1. **Validate environment argument**
   - Check that environment is "staging" or "production"
   - If invalid, abort with error

2. **Run pre-deployment checks**
   - Execute: npm test
   - Execute: npm run build
   - Verify: .env.{environment} exists

3. **Confirm deployment**
   - Display target environment
   - Ask user: "Deploy to {environment}? (yes/no)"

4. **Execute deployment**
   - Run: npm run deploy:{environment}
```

3. **Missing error handling:**
- No validation of arguments
- No error scenarios documented
- No success criteria

---

#### Subagents (*.md files in agents/)

**Location:** `.claude/agents/*.md`

**Common issues:**

1. **Insufficient tool access:**
```yaml
# ❌ Old: No tools specified
---
name: code-analyzer
description: Analyze code quality
---

# ✅ New: Explicit tools
---
name: code-analyzer
description: Analyze code quality with detailed recommendations
tools: Read, Grep, Glob
model: sonnet
---
```

2. **Vague system prompts:**
```markdown
# ❌ Old: Generic
Analyze the code and report findings.

# ✅ New: Specific methodology
## Your Task

Perform comprehensive code quality analysis covering:
- Code complexity (cyclomatic complexity)
- Design patterns usage
- Maintainability issues
- Best practices violations

## Methodology

1. **Structural analysis**: [specific steps]
2. **Complexity assessment**: [specific steps]
3. **Report generation**: [exact format]

## Output Format

[Detailed specification of expected output]
```

3. **Missing scope boundaries:**
- No clear "in scope" / "out of scope"
- Undefined output format
- No quality standards

---

#### Hooks (*.json files in hooks/)

**Location:** `.claude/hooks/*.json`

**Common issues:**

1. **Missing timeout:**
```json
// ❌ Old: No timeout (could hang)
{
  "name": "test-hook",
  "event": "file-save",
  "command": "npm test"
}

// ✅ New: With timeout
{
  "name": "test-hook",
  "event": "file-save",
  "command": "npm test",
  "timeout": 30000,
  "description": "Run tests after saving files"
}
```

2. **Dangerous commands:**
```json
// ❌ Dangerous: Auto-push
{
  "name": "auto-push",
  "event": "tool-call",
  "command": "git push"
}

// ✅ Better: Use Command instead
// Hooks should not perform destructive operations automatically
```

3. **Missing descriptions:**
- No description field
- Unclear purpose
- No documentation

---

### Step 3: Migration Planning (5 min)

**Create migration plan:**

```markdown
# Migration Plan for [artifact-name]

## Current Issues
1. [Issue 1]: [Description]
2. [Issue 2]: [Description]

## Proposed Changes
1. [Change 1]: [Specific modification]
   - Impact: [What changes for users]
   - Risk: [Low/Medium/High]

2. [Change 2]: [Specific modification]
   - Impact: [What changes]
   - Risk: [Low/Medium/High]

## Migration Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Testing Required
- [ ] Test 1
- [ ] Test 2

## Rollback Plan
[How to revert if migration fails]
```

**Risk assessment:**

| Risk Level | Definition | Examples |
|------------|------------|----------|
| **Low** | Cosmetic, no behavior change | Description update, adding comments |
| **Medium** | Behavior change, backward compatible | Adding optional fields, improving logic |
| **High** | Breaking change | Changing artifact structure, removing features |

---

### Step 4: Backup (CRITICAL)

**Always backup before migration:**

```bash
# Backup entire .claude directory
cp -r .claude .claude.backup-$(date +%Y%m%d-%H%M%S)

# Or backup specific artifact
cp .claude/skills/my-skill/SKILL.md .claude/skills/my-skill/SKILL.md.backup
```

**Verify backup:**
```bash
# Check backup exists
ls -la .claude.backup-*

# Verify content
diff .claude/skills/my-skill/SKILL.md .claude/skills/my-skill/SKILL.md.backup
```

---

### Step 5: Migration Execution (10-30 min)

**Execute changes systematically:**

#### Example 1: Migrate Skill Description

**Problem:** Skill not activating reliably

**Old description:**
```yaml
description: Helps with PDFs
```

**Analysis:**
- Too vague, no specific trigger keywords
- Missing technologies
- No "Use when" clause

**Migration:**
```yaml
description: Extract text, images, and tables from PDFs. Fill PDF forms, merge documents, convert between formats (PDF↔Word). Use when working with PDF files, document processing, form filling, or PDF manipulation tasks.
```

**Changes made:**
- Added 5+ action verbs (extract, fill, merge, convert)
- Listed specific capabilities
- Mentioned technologies (PDF, Word)
- Added "Use when" with trigger scenarios
- Included 10+ trigger keywords

---

#### Example 2: Migrate Command Structure

**Problem:** Command lacks clarity and error handling

**Old command:**
```markdown
---
name: deploy
---

# Deploy

Deploy the application.

Use Bash to run the deploy script.
```

**Migration:**
```markdown
---
name: deploy
description: Deploy application to specified environment with pre-deployment validation
arguments:
  - name: environment
    description: Target environment (staging, production)
    required: true
model: sonnet
---

# Deploy Command

Deploy the application to the specified environment with comprehensive validation.

## Arguments

**environment** (required): Target environment. Valid values: `staging`, `production`

## Process

1. **Validate environment argument**
   - Check that environment is either "staging" or "production"
   - If invalid, display error: "Invalid environment. Use: staging or production"
   - Abort if invalid

2. **Pre-deployment checks**
   - Use Bash tool to run: `npm test`
   - If tests fail, abort deployment
   - Use Bash tool to run: `npm run build`
   - If build fails, abort deployment
   - Use Read tool to verify: `.env.{environment}` exists

3. **User confirmation**
   - Display: "Ready to deploy to {environment}"
   - Display: Current branch, commit hash
   - Ask: "Proceed with deployment? (yes/no)"
   - If no, abort with message "Deployment cancelled"

4. **Execute deployment**
   - Use Bash tool to run: `npm run deploy:{environment}`
   - Monitor output for errors
   - Display deployment URL when complete

## Error Handling

**If tests fail:**
- Display test failures
- Abort deployment
- Suggest: "Fix tests before deploying"

**If build fails:**
- Display build errors
- Abort deployment

**If .env file missing:**
- Error: "Configuration file .env.{environment} not found"
- List available .env files
- Abort deployment

## Success Criteria

- ✅ All tests pass
- ✅ Build completes successfully
- ✅ User confirms deployment
- ✅ Deployment executes without errors
- ✅ Application is accessible at deployment URL

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

**Changes made:**
- Complete YAML frontmatter with description and arguments
- Explicit, numbered process steps
- Detailed error handling
- Success criteria
- Concrete examples

---

#### Example 3: Migrate Subagent Prompt

**Problem:** Subagent output inconsistent

**Old subagent:**
```markdown
---
name: code-reviewer
---

# Code Reviewer

Review the code and provide feedback.
```

**Migration:**
```markdown
---
name: code-reviewer
description: Comprehensive code review with quality, security, and performance analysis
tools: Read, Grep, Glob
model: sonnet
---

# Code Reviewer: Code Quality Specialist

You are a specialized code review subagent focused on providing thorough, actionable feedback.

## Your Task

Perform comprehensive code review covering:
- Code quality and readability
- Potential bugs and edge cases
- Security vulnerabilities
- Performance concerns
- Best practices adherence
- Test coverage assessment

## Scope

**In scope:**
- Code structure and organization
- Logic correctness
- Security patterns
- Performance patterns
- Testing strategies

**Out of scope:**
- Fixing code (review only)
- Subjective style preferences
- Framework selection debates
- Architecture overhauls

## Methodology

1. **Initial scan**
   - Use Glob to identify all relevant files
   - Prioritize by change size and criticality

2. **Code analysis**
   - Review logic for correctness
   - Identify potential bugs
   - Check for security anti-patterns
   - Assess performance implications

3. **Best practices check**
   - Compare against language best practices
   - Verify error handling
   - Check test coverage

4. **Reporting**
   - Categorize findings by severity
   - Provide specific, actionable feedback
   - Include code examples

## Output Format

# Code Review Report

## Summary
- Files reviewed: [count]
- Issues found: [count]
- Critical: [count] | Major: [count] | Minor: [count]

## Critical Issues

### [Issue title]
**File:** path/to/file.js:123
**Severity:** Critical
**Category:** Security / Bug / Performance

**Issue:**
[Clear description of the problem]

**Current code:**
\`\`\`javascript
[Problematic code]
\`\`\`

**Recommendation:**
[Specific fix]

**Better approach:**
\`\`\`javascript
[Improved code]
\`\`\`

[Repeat for each critical issue]

## Major Issues

[Same format, can be more concise]

## Minor Issues

[Brief listings]

## Positive Observations

[Highlight good practices found]

## Overall Assessment

[Summary and recommendations]

## Quality Standards

Your review must:
- ✅ Review all files in scope
- ✅ Provide file:line references
- ✅ Assign appropriate severity
- ✅ Include code examples
- ✅ Offer actionable recommendations
- ✅ Acknowledge good practices
- ✅ Maintain constructive tone

## Important Notes

- Be specific: "Line 42: Unhandled promise rejection" not "Handle errors better"
- Be constructive: Suggest improvements, don't just criticize
- Consider context: Framework patterns may look unusual but be correct
- Prioritize: Focus on actual issues, not style preferences
- Explain reasoning: Why is something an issue?
```

**Changes made:**
- Complete frontmatter with tools and model
- Specific task definition
- Clear scope boundaries
- Step-by-step methodology
- Structured output format
- Quality standards
- Important notes for context

---

#### Example 4: Migrate Hook Configuration

**Problem:** Hook missing safety features

**Old hook:**
```json
{
  "name": "test-runner",
  "event": "file-save",
  "command": "npm test"
}
```

**Migration:**
```json
{
  "name": "test-runner",
  "event": "file-save",
  "filter": {
    "filePattern": "src/**/*.{js,ts}"
  },
  "command": "npm test",
  "timeout": 30000,
  "continueOnError": true,
  "description": "Run tests automatically after saving source files (src/ only)"
}
```

**Changes made:**
- Added `filter` to limit when hook runs (performance)
- Added `timeout` to prevent hanging (safety)
- Added `continueOnError: true` so test failures don't block work
- Added `description` for documentation

---

### Step 6: Testing (15-30 min)

**Test migrated artifacts thoroughly:**

#### For Skills:
```markdown
**Test 1: Activation test**
- Try 3-5 different phrasings that should activate skill
- Verify skill activates reliably

**Test 2: Functionality test**
- Use skill for actual task
- Verify behavior is correct

**Test 3: Negative test**
- Try unrelated queries
- Verify skill doesn't activate inappropriately
```

#### For Commands:
```markdown
**Test 1: Basic invocation**
- Run command with valid arguments
- Verify it executes correctly

**Test 2: Error handling**
- Try with invalid arguments
- Verify error messages are clear

**Test 3: Edge cases**
- Test boundary conditions
- Verify graceful handling
```

#### For Subagents:
```markdown
**Test 1: Delegation test**
- Delegate task to subagent
- Verify output format and quality

**Test 2: Scope test**
- Try to get subagent to exceed scope
- Verify boundaries are respected

**Test 3: Complex scenario**
- Use realistic, complex input
- Verify completion and quality
```

#### For Hooks:
```markdown
**Test 1: Trigger test**
- Perform action that should trigger hook
- Verify hook executes

**Test 2: Timeout test**
- Verify hook respects timeout
- Doesn't hang indefinitely

**Test 3: Failure test**
- Make hook command fail
- Verify graceful failure handling
```

---

### Step 7: Documentation (5 min)

**Document migration:**

```markdown
## Migration Log

### [Date] - [Artifact Name] Migration

**Reason:** [Why migration was needed]

**Changes:**
1. [Change 1]: [Description]
2. [Change 2]: [Description]

**Impact:**
- [What changed for users]
- [Any breaking changes]

**Testing:**
- [Tests performed]
- [Results]

**Rollback:**
\`\`\`bash
# If needed, restore from backup:
cp .claude/skills/my-skill/SKILL.md.backup .claude/skills/my-skill/SKILL.md
\`\`\`
```

**Update README if behavior changed:**
```markdown
## Recent Updates

### [Date] - My Skill v2
- Improved activation reliability
- Added error handling
- Enhanced output format
```

---

## Common Migration Scenarios

### Scenario 1: Skill Not Activating

**Problem:** Skill worked before but stopped activating

**Diagnosis:**
1. Read current description
2. Compare against activation test queries
3. Identify missing trigger keywords

**Migration:**
1. Add specific trigger keywords to description
2. Add "Use when..." clause if missing
3. Include technology/file type mentions
4. Test with actual user queries

**Example:**
```yaml
# Before
description: Code analysis tool

# After
description: Analyze code quality, identify bugs, check best practices, and suggest improvements. Review code for security vulnerabilities, performance issues, and maintainability concerns. Use when reviewing code, analyzing quality, finding bugs, or checking best practices in JavaScript, TypeScript, Python, or Java.
```

---

### Scenario 2: Command Arguments Not Working

**Problem:** Command runs but arguments aren't used

**Diagnosis:**
1. Check frontmatter has arguments defined
2. Check content references arguments
3. Verify argument syntax

**Migration:**
1. Add arguments array to frontmatter
2. Update content to explicitly use arguments
3. Add validation of arguments

**Example:**
```markdown
---
name: greet
description: Greet a user by name
arguments:
  - name: username
    description: Name to greet
    required: true
---

# Greet Command

## Process

1. **Extract username argument**
   - Username: {username}
   - If empty, error: "Username required"

2. **Generate greeting**
   - Display: "Hello, {username}!"
```

---

### Scenario 3: Subagent Output Inconsistent

**Problem:** Subagent produces different output formats each time

**Diagnosis:**
1. Read subagent system prompt
2. Check if output format is specified
3. Verify quality standards exist

**Migration:**
1. Add explicit "Output Format" section
2. Provide exact template/structure
3. Add quality standards
4. Include examples of expected output

---

### Scenario 4: Hook Performance Issues

**Problem:** Hook slows down workflow

**Diagnosis:**
1. Check if hook runs on every trigger
2. Verify timeout setting
3. Check command complexity

**Migration:**
1. Add filter to limit when hook runs
2. Adjust timeout if needed
3. Optimize command
4. Consider less frequent event

**Example:**
```json
// Before: Runs on every file save
{
  "name": "test-runner",
  "event": "file-save",
  "command": "npm test"
}

// After: Only runs for source files
{
  "name": "test-runner",
  "event": "file-save",
  "filter": {
    "filePattern": "src/**/*.{js,ts}"
  },
  "command": "npm test -- --onlyChanged",
  "timeout": 30000
}
```

---

## Batch Migration

**When migrating multiple artifacts:**

```markdown
## Batch Migration Plan

### Phase 1: Skills (Low Risk)
- [ ] Update descriptions for better activation
- [ ] Add allowed-tools where missing
- [ ] Standardize formatting

### Phase 2: Commands (Medium Risk)
- [ ] Add missing argument definitions
- [ ] Improve error handling
- [ ] Add success criteria

### Phase 3: Subagents (Medium Risk)
- [ ] Add explicit output formats
- [ ] Define scope boundaries
- [ ] Specify tool access

### Phase 4: Hooks (High Risk)
- [ ] Add timeouts
- [ ] Add filters for performance
- [ ] Review security implications

**Testing Schedule:**
- Test Phase 1 artifacts: [Date]
- Test Phase 2 artifacts: [Date]
- Test Phase 3 artifacts: [Date]
- Test Phase 4 artifacts: [Date]
```

---

## Migration Best Practices

### 1. Always Backup
```bash
cp -r .claude .claude.backup-$(date +%Y%m%d)
```

### 2. Migrate One at a Time
- Don't change multiple artifacts simultaneously
- Test each migration before moving to next
- Easier to identify issues

### 3. Test Thoroughly
- Test activation/invocation
- Test with realistic scenarios
- Test error cases
- Test edge cases

### 4. Document Changes
- Keep migration log
- Note breaking changes
- Document rollback procedure

### 5. Communicate Changes
- If team artifacts, notify team
- Update README
- Share migration rationale

### 6. Monitor After Migration
- Watch for issues in real usage
- Gather user feedback
- Be ready to rollback

---

## Rollback Procedures

### If Migration Fails

**Immediate rollback:**
```bash
# Restore from backup
cp .claude.backup-20250106/.claude/skills/my-skill/SKILL.md .claude/skills/my-skill/SKILL.md

# Restart Claude to reload
```

**If backup not available:**
```bash
# Use git history (if committed)
git checkout HEAD~1 -- .claude/skills/my-skill/SKILL.md

# Or use git reflog
git reflog
git checkout <commit> -- .claude/skills/my-skill/SKILL.md
```

**Verify rollback:**
```bash
# Check file contents
cat .claude/skills/my-skill/SKILL.md

# Test artifact works
[Test activation/invocation]
```

---

## Quality Validation Post-Migration

**After migration, verify:**

- [ ] Artifact loads without errors
- [ ] YAML is valid
- [ ] Activation/invocation works
- [ ] Functionality preserved
- [ ] New features work as expected
- [ ] No regression in behavior
- [ ] Performance acceptable
- [ ] Documentation updated

**Use artifact-validator:**
```
"Can you validate my migrated skill to ensure quality?"
```

---

## Success Criteria

A successful migration results in:
- ✅ Artifact works correctly (no regressions)
- ✅ New features/improvements function as intended
- ✅ All tests pass
- ✅ Backup created before changes
- ✅ Changes documented
- ✅ User/team notified if applicable
- ✅ Rollback procedure known
- ✅ Monitoring plan in place

---

## When to Migrate vs. Rebuild

**Migrate when:**
- ✅ Core functionality is good
- ✅ Need minor updates
- ✅ Specification changes
- ✅ Best practices updates

**Rebuild when:**
- ❌ Fundamental design issues
- ❌ Scope completely changed
- ❌ Multiple major problems
- ❌ Easier to start fresh

**Signs you should rebuild:**
- More than 50% of content needs changes
- Core purpose has changed
- Multiple failed migration attempts
- Artifact never worked well

---

**Remember: Migration preserves value while improving quality. Always backup, test thoroughly, and be ready to rollback!**
