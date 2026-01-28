---
name: hook-creator
description: 'Creates and registers hooks for the Claude Code framework. Handles pre/post tool execution, validation, memory, and session hooks. Use when new validation, safety, or automation hooks are needed.'
version: 2.1.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash, Glob, Grep]
best_practices:
  - Always register hooks in appropriate config
  - Test hooks before deployment
  - Include error handling in all hooks
  - Document hook triggers and behavior
  - Use graceful degradation (warn, not block by default)
error_handling: graceful
streaming: supported
output_location: .claude/hooks/
---

# Hook Creator Skill

Creates, validates, and registers hooks for the multi-agent orchestration framework.

## ROUTER UPDATE REQUIRED (CRITICAL - DO NOT SKIP)

**After creating ANY hook, you MUST update documentation:**

```
1. Add to .claude/hooks/README.md under appropriate category
2. Register in config.yaml or settings.json if required
3. Update learnings.md with hook summary
```

**Verification:**

```bash
grep "<hook-name>" .claude/hooks/README.md || echo "ERROR: hooks/README.md NOT UPDATED!"
```

**WHY**: Hooks not documented are invisible and unmaintainable.

---

## Overview

This skill creates hooks for the Claude Code framework:

- **Pre-tool execution** - Safety validation before commands run
- **Post-tool execution** - Logging, memory updates, telemetry
- **Session lifecycle** - Initialize context, cleanup on exit
- **Memory management** - Auto-extract learnings, format memory files
- **Routing enforcement** - Ensure Router-First protocol compliance

## Hook Types

| Type    | Location                 | Purpose                                 | When Triggered         |
| ------- | ------------------------ | --------------------------------------- | ---------------------- |
| Safety  | `.claude/hooks/safety/`  | Validate commands, block dangerous ops  | Before Bash/Write/Edit |
| Memory  | `.claude/hooks/memory/`  | Auto-update learnings, extract insights | After task completion  |
| Routing | `.claude/hooks/routing/` | Enforce router-first protocol           | On UserPromptSubmit    |
| Session | `.claude/hooks/session/` | Initialize/cleanup sessions             | Session start/end      |

## Claude Code Hook Types

| Hook Event         | When Triggered            | Use Case                                |
| ------------------ | ------------------------- | --------------------------------------- |
| `PreToolUse`       | Before tool executes      | Validation, blocking, permission checks |
| `PostToolUse`      | After tool completes      | Logging, cleanup, notifications         |
| `UserPromptSubmit` | Before model sees message | Routing, intent analysis, filtering     |

## Workflow Steps

### Reference Hook

**Use `.claude/hooks/routing/router-enforcer.cjs` as the canonical reference hook.**

Before finalizing any hook, compare against router-enforcer structure:

- [ ] Has proper CommonJS exports (module.exports)
- [ ] Exports required functions for hook type (validate, main, etc.)
- [ ] Has comprehensive test file (.test.cjs)
- [ ] Has proper error handling (try/catch, graceful fallbacks)
- [ ] Returns correct response format for hook type

### Step 1: Gather Hook Requirements

Before creating a hook, gather:

1. **Purpose**: What should this hook do?
2. **Trigger**: When should it run? (pre-tool, post-tool, session event)
3. **Target tools**: Which tools does it apply to? (Bash, Write, Edit, Read)
4. **Behavior**: Block operation or warn only?
5. **Exit codes**: What indicates success/failure?

```javascript
// Example requirements gathering
{
  purpose: "Validate git push commands to prevent force push",
  trigger: "pre-tool (Bash)",
  target_tools: ["Bash"],
  behavior: "block if force push detected",
  exit_codes: { 0: "allow", 1: "block" }
}
```

### Step 2: Determine Hook Type and Location

| If hook does...      | Type    | Location                 |
| -------------------- | ------- | ------------------------ |
| Validates commands   | Safety  | `.claude/hooks/safety/`  |
| Modifies routing     | Routing | `.claude/hooks/routing/` |
| Updates memory       | Memory  | `.claude/hooks/memory/`  |
| Session init/cleanup | Session | `.claude/hooks/session/` |

**Naming Convention:** `<action>-<target>.cjs`

Examples:

- `validate-git-force-push.cjs`
- `enforce-tdd-workflow.cjs`
- `extract-workflow-learnings.cjs`
- `memory-reminder.cjs`

### Step 3: Generate Hook Code (CJS Format)

All hooks use CommonJS format and follow this template:

```javascript
'use strict';

/**
 * {Hook Name}
 *
 * Type: {pre|post}-{tool} | session-{start|end} | user-prompt
 * Purpose: {One line description}
 * Trigger: {When this hook runs}
 *
 * Exit codes:
 * - 0: Allow operation (with optional warning)
 * - 1: Block operation (when in blocking mode)
 *
 * Environment:
 *   {HOOK_NAME}_MODE=block|warn|off (default: warn)
 */

const fs = require('fs');
const path = require('path');

// Find project root by looking for .claude directory
function findProjectRoot() {
  let dir = __dirname;
  while (dir !== path.parse(dir).root) {
    if (fs.existsSync(path.join(dir, '.claude'))) {
      return dir;
    }
    dir = path.dirname(dir);
  }
  return process.cwd();
}

const PROJECT_ROOT = findProjectRoot();
const ENFORCEMENT_MODE = process.env.HOOK_NAME_MODE || 'warn';

/**
 * Parse hook input from Claude Code
 * Claude Code passes JSON via process.argv[2] for hooks
 * @returns {Object|null} Parsed hook input or null
 */
function parseHookInput() {
  try {
    if (process.argv[2]) {
      return JSON.parse(process.argv[2]);
    }
  } catch (e) {
    // Fallback for testing or invalid input
  }
  return null;
}

/**
 * Validate hook - called by Claude Code or programmatically
 * @param {Object} context - Hook context with tool info
 * @param {string} context.tool - Tool name (Bash, Write, Edit, Read)
 * @param {Object} context.parameters - Tool parameters
 * @returns {{ valid: boolean, error: string, warning?: string }}
 */
function validate(context) {
  const { tool, parameters } = context;

  // YOUR VALIDATION LOGIC HERE

  // Return validation result
  return { valid: true, error: '' };
}

/**
 * Main execution for CLI hook usage
 */
function main() {
  // Skip if enforcement is off
  if (ENFORCEMENT_MODE === 'off') {
    process.exit(0);
  }

  const hookInput = parseHookInput();
  if (!hookInput) {
    process.exit(0);
  }

  // Get tool name and input
  const toolName = hookInput.tool_name || hookInput.tool;
  const toolInput = hookInput.tool_input || hookInput.input || {};

  // Run validation
  const result = validate({ tool: toolName, parameters: toolInput });

  if (!result.valid) {
    if (ENFORCEMENT_MODE === 'block') {
      console.error(`BLOCKED: ${result.error}`);
      process.exit(1);
    } else {
      console.warn(`WARNING: ${result.error}`);
      process.exit(0);
    }
  }

  if (result.warning) {
    console.warn(`WARNING: ${result.warning}`);
  }

  process.exit(0);
}

// Run main if executed directly
if (require.main === module) {
  main();
}

// Export for programmatic use and testing
module.exports = {
  validate,
  findProjectRoot,
  PROJECT_ROOT,
};
```

### Step 4: Create Test File

Every hook MUST have a corresponding test file:

```javascript
'use strict';

const { validate } = require('./hook-name.cjs');

describe('Hook Name', () => {
  test('allows valid operations', () => {
    const result = validate({
      tool: 'Bash',
      parameters: { command: 'git status' },
    });
    expect(result.valid).toBe(true);
    expect(result.error).toBe('');
  });

  test('blocks dangerous operations', () => {
    const result = validate({
      tool: 'Bash',
      parameters: { command: 'git push --force' },
    });
    expect(result.valid).toBe(false);
    expect(result.error).toContain('force push');
  });

  test('handles missing parameters gracefully', () => {
    const result = validate({
      tool: 'Bash',
      parameters: {},
    });
    expect(result.valid).toBe(true);
  });
});
```

### Step 5: Register Hook (If Needed)

Some hooks require registration in config files:

**For pre/post-tool hooks (settings.json):**

```json
{
  "hooks": {
    "pre-tool": [".claude/hooks/safety/hook-name.cjs"],
    "post-tool": [".claude/hooks/memory/hook-name.cjs"]
  }
}
```

**For event hooks (config.yaml):**

```yaml
hooks:
  UserPromptSubmit:
    - path: .claude/hooks/routing/hook-name.cjs
      type: command
  SessionStart:
    - path: .claude/hooks/session/hook-name.cjs
      type: command
```

### Step 6: Update Documentation (MANDATORY - BLOCKING)

After creating a hook, update `.claude/hooks/README.md`:

```markdown
#### {Hook Name} (`hook-name.cjs`)

{Description of what the hook does}

**When it runs:** {Trigger condition}
**What it checks/does:** {Detailed behavior}
```

Verify with:

```bash
grep "hook-name" .claude/hooks/README.md || echo "ERROR: Not documented!"
```

### Step 7: System Impact Analysis (MANDATORY)

**This analysis is MANDATORY. Hook creation is INCOMPLETE without it.**

After creating a hook:

1. **Settings Registration (BLOCKING)**
   - Add to .claude/settings.json PreToolUse/PostToolUse/etc.
   - Verify with: `grep "hook-name" .claude/settings.json`

2. **Test Coverage (BLOCKING)**
   - Create .test.cjs file with minimum 10 test cases
   - Run tests: `node .claude/hooks/<category>/<name>.test.cjs`

3. **Documentation**
   - Update .claude/docs/ if hook adds new capability
   - Add usage examples

4. **Related Hooks**
   - Check if hook affects other hooks in same trigger category
   - Document interaction patterns

**Full Checklist:**

```
[HOOK-CREATOR] System Impact Analysis for: <hook-name>

1. HOOK FILE CREATED
   [ ] Created at .claude/hooks/<type>/<hook-name>.cjs
   [ ] Follows CJS format with validate() export
   [ ] Has main() function for CLI execution
   [ ] Handles graceful degradation (warn by default)

2. TEST FILE CREATED (minimum 10 test cases)
   [ ] Created at .claude/hooks/<type>/<hook-name>.test.cjs
   [ ] Tests valid operations (3+ cases)
   [ ] Tests blocked operations (3+ cases)
   [ ] Tests edge cases (3+ cases)
   [ ] Tests error handling (1+ cases)

3. DOCUMENTATION UPDATED
   [ ] Added to .claude/hooks/README.md
   [ ] Documented trigger conditions
   [ ] Documented exit codes

4. REGISTRATION (BLOCKING)
   [ ] Added to settings.json (pre/post-tool hooks)
   [ ] Added to config.yaml (event hooks)
   [ ] Verified: grep "<hook-name>" .claude/settings.json

5. MEMORY UPDATED
   [ ] Added to learnings.md with hook summary
```

**BLOCKING**: If ANY item above is missing, hook creation is INCOMPLETE.

---

## CLI Reference

```bash
# Create hook using CLI tool
node .claude/tools/hook-creator/create-hook.mjs \
  --name "hook-name" \
  --type "PreToolUse|PostToolUse|UserPromptSubmit" \
  --purpose "Description of what the hook does" \
  --category "safety|routing|memory|audit|security|validation|custom" \
  --matcher "Edit|Write|Bash"  # Optional: tool matcher regex

# List all hooks
node .claude/tools/hook-creator/create-hook.mjs --list

# Validate hook structure
node .claude/tools/hook-creator/create-hook.mjs --validate "<path>"

# Assign to agents
node .claude/tools/hook-creator/create-hook.mjs --assign "name" --agents "agent1,agent2"

# Unregister hook
node .claude/tools/hook-creator/create-hook.mjs --unregister "<path>"

# Test with sample input
node .claude/hooks/<category>/<hook-name>.cjs '{"tool_name":"Edit","tool_input":{"file_path":"test.js"}}'
```

---

## Hook Patterns Reference

### Pattern 1: Safety Validator (Pre-Tool)

For validating commands before execution:

```javascript
'use strict';

/**
 * Validate Git Force Push
 * Prevents accidental force pushes to protected branches
 */

const PROTECTED_BRANCHES = ['main', 'master', 'production'];

function validate(context) {
  const { tool, parameters } = context;

  if (tool !== 'Bash') {
    return { valid: true, error: '' };
  }

  const command = parameters?.command || '';

  // Check for force push
  if (command.includes('git push') && (command.includes('--force') || command.includes('-f'))) {
    // Check if pushing to protected branch
    for (const branch of PROTECTED_BRANCHES) {
      if (command.includes(branch)) {
        return {
          valid: false,
          error: `Force push to ${branch} blocked. Use --force-with-lease instead.`,
        };
      }
    }

    return {
      valid: true,
      error: '',
      warning: 'Force push detected. Ensure you know what you are doing.',
    };
  }

  return { valid: true, error: '' };
}

module.exports = { validate };
```

### Pattern 2: Memory Extractor (Post-Tool)

For extracting learnings after task completion:

```javascript
'use strict';

/**
 * Extract Workflow Learnings
 * Automatically captures patterns from completed workflows
 */

const fs = require('fs');
const path = require('path');

function findProjectRoot() {
  let dir = __dirname;
  while (dir !== path.parse(dir).root) {
    if (fs.existsSync(path.join(dir, '.claude'))) return dir;
    dir = path.dirname(dir);
  }
  return process.cwd();
}

const LEARNINGS_PATH = path.join(findProjectRoot(), '.claude/context/memory/learnings.md');

function extractLearnings(context) {
  const { tool, parameters, result } = context;

  // Only process completed tasks
  if (!result || result.status !== 'completed') {
    return { extracted: false };
  }

  // Extract patterns from result
  const learnings = [];

  if (result.patterns) {
    learnings.push(...result.patterns);
  }

  if (result.decisions) {
    learnings.push(...result.decisions);
  }

  if (learnings.length === 0) {
    return { extracted: false };
  }

  // Append to learnings file
  const entry = `\n## [${new Date().toISOString().split('T')[0]}] ${context.taskName || 'Task'}\n\n`;
  const content = learnings.map(l => `- ${l}`).join('\n');

  fs.appendFileSync(LEARNINGS_PATH, entry + content + '\n');

  return { extracted: true, count: learnings.length };
}

module.exports = { extractLearnings };
```

### Pattern 3: Routing Enforcer (User Prompt)

For enforcing routing protocols:

```javascript
'use strict';

/**
 * Router First Enforcer
 * Ensures all requests go through the Router agent
 */

function validate(context) {
  const { prompt, currentAgent } = context;

  // Skip if already routed
  if (currentAgent === 'router') {
    return { valid: true, error: '' };
  }

  // Skip slash commands (handled by skill system)
  if (prompt && prompt.trim().startsWith('/')) {
    return { valid: true, error: '' };
  }

  // Suggest routing
  return {
    valid: true,
    error: '',
    warning: 'Consider using Router to spawn appropriate agent via Task tool.',
  };
}

module.exports = { validate };
```

### Pattern 4: Session Initializer

For session lifecycle management:

```javascript
'use strict';

/**
 * Session Memory Initializer
 * Reminds agents to read memory files at session start
 */

const fs = require('fs');
const path = require('path');

function findProjectRoot() {
  let dir = __dirname;
  while (dir !== path.parse(dir).root) {
    if (fs.existsSync(path.join(dir, '.claude'))) return dir;
    dir = path.dirname(dir);
  }
  return process.cwd();
}

const MEMORY_FILES = [
  '.claude/context/memory/learnings.md',
  '.claude/context/memory/issues.md',
  '.claude/context/memory/decisions.md',
];

function initialize() {
  const root = findProjectRoot();

  console.log('\n' + '='.repeat(50));
  console.log(' SESSION MEMORY REMINDER');
  console.log('='.repeat(50));
  console.log('\n  Before starting work, read these memory files:');

  for (const file of MEMORY_FILES) {
    const fullPath = path.join(root, file);
    if (fs.existsSync(fullPath)) {
      const stats = fs.statSync(fullPath);
      const modified = stats.mtime.toISOString().split('T')[0];
      console.log(`  - ${file} (updated: ${modified})`);
    }
  }

  console.log('\n' + '='.repeat(50) + '\n');

  return { initialized: true };
}

// Run on direct execution
if (require.main === module) {
  initialize();
}

module.exports = { initialize };
```

---

## Examples

### Security Validation Hook

```bash
node .claude/tools/hook-creator/create-hook.mjs \
  --name "secret-detector" \
  --type "PreToolUse" \
  --purpose "Blocks commits containing secrets or credentials" \
  --category "security" \
  --matcher "Bash"
```

### Audit Logging Hook

```bash
node .claude/tools/hook-creator/create-hook.mjs \
  --name "operation-logger" \
  --type "PostToolUse" \
  --purpose "Logs all file modifications to audit trail" \
  --category "audit"
```

### Intent Analysis Hook

```bash
node .claude/tools/hook-creator/create-hook.mjs \
  --name "intent-classifier" \
  --type "UserPromptSubmit" \
  --purpose "Classifies user intent for intelligent routing" \
  --category "routing"
```

---

## Workflow Integration

This skill is part of the unified artifact lifecycle. For complete multi-agent orchestration:

**Router Decision:** `.claude/workflows/core/router-decision.md`

- How the Router discovers and invokes this skill's artifacts

**Artifact Lifecycle:** `.claude/workflows/core/skill-lifecycle.md`

- Discovery, creation, update, deprecation phases
- Version management and registry updates
- CLAUDE.md integration requirements

**External Integration:** `.claude/workflows/core/external-integration.md`

- Safe integration of external artifacts
- Security review and validation phases

---

## Cross-Reference: Creator Ecosystem

This skill is part of the **Creator Ecosystem**. After creating a hook, consider if companion artifacts are needed:

| Need                           | Creator to Invoke  | Command                             |
| ------------------------------ | ------------------ | ----------------------------------- |
| Dedicated skill for hook logic | `skill-creator`    | `Skill({ skill: 'skill-creator' })` |
| Agent that uses this hook      | `agent-creator`    | `Skill({ skill: 'agent-creator' })` |
| Workflow for hook testing      | `workflow-creator` | Create in `.claude/workflows/`      |
| Schema for hook config         | `schema-creator`   | Create in `.claude/schemas/`        |
| Template for hook scaffold     | `template-creator` | Create in `.claude/templates/`      |

### Integration Workflow

After creating a hook that needs additional capabilities:

```javascript
// 1. Hook created but needs dedicated skill
Skill({ skill: 'skill-creator' });
// Create skill that encapsulates hook logic

// 2. Hook needs to be assigned to agent
// Update agent's workflow to include hook awareness

// 3. Hook needs workflow for testing
// Create workflow in .claude/workflows/<hook-name>-test-workflow.md
```

### Post-Creation Checklist for Ecosystem Integration

After hook is fully created and validated:

```
[ ] Does hook need a skill wrapper? -> Use skill-creator
[ ] Does hook need dedicated agent? -> Use agent-creator
[ ] Does hook need testing workflow? -> Create workflow
[ ] Should hook be enabled by default? -> Update config.yaml
[ ] Does hook interact with other hooks? -> Document in README.md
```

---

## Iron Laws of Hook Creation

These rules are INVIOLABLE. Breaking them causes silent failures.

```
1. NO HOOK WITHOUT validate() EXPORT
   - Every hook MUST export validate() function
   - Hooks without validate() cannot be called programmatically

2. NO HOOK WITHOUT main() FOR CLI
   - Every hook MUST have main() for CLI execution
   - Run only when require.main === module

3. NO HOOK WITHOUT GRACEFUL DEGRADATION
   - Default to 'warn' mode, not 'block'
   - Use environment variables for enforcement mode
   - Never crash on malformed input

4. NO HOOK WITHOUT ERROR HANDLING
   - Wrap JSON.parse in try/catch
   - Handle missing parameters gracefully
   - Return valid: true when unsure (fail open, not closed)

5. NO HOOK WITHOUT TEST FILE
   - Every hook needs <hook-name>.test.cjs
   - Test valid, invalid, and edge cases

6. NO HOOK WITHOUT DOCUMENTATION
   - Add to .claude/hooks/README.md
   - Document trigger, behavior, exit codes

7. CROSS-PLATFORM PATHS
   - Use path.join() not string concatenation
   - Handle both / and \ path separators
   - Use path.normalize() for comparison

8. NO CREATION WITHOUT SYSTEM IMPACT ANALYSIS
   - Check if hook requires settings.json registration
   - Check if hook requires config.yaml registration
   - Check if related hooks need updating
   - Document all system changes made
```

---

## Integration Points

- **Ecosystem Assessor**: Hook creator integrates with ecosystem assessment for reverse lookups
- **Agent Creator**: Agents can reference hooks in their frontmatter
- **Skill Creator**: Skills can define hooks in their hooks/ directory
- **Settings.json**: Hooks are auto-registered with proper triggers and matchers
- **Config.yaml**: Event hooks registered for UserPromptSubmit, SessionStart, etc.

---

## File Placement & Standards

### Output Location Rules

This skill outputs to: `.claude/hooks/<category>/`

Categories:

- `safety/` - Safety validators (command validation, security checks)
- `routing/` - Router enforcement hooks
- `memory/` - Memory management hooks
- `session/` - Session lifecycle hooks
- `validation/` - Input/output validation hooks

### Mandatory References

- **File Placement**: See `.claude/docs/FILE_PLACEMENT_RULES.md`
- **Developer Workflow**: See `.claude/docs/DEVELOPER_WORKFLOW.md`
- **Artifact Naming**: See `.claude/docs/ARTIFACT_NAMING.md`

### Enforcement

File placement is enforced by `file-placement-guard.cjs` hook.
Invalid placements will be blocked in production mode.

---

## Memory Protocol (MANDATORY)

**Before creating a hook:**

```bash
cat .claude/context/memory/learnings.md
```

Check for:

- Previously created hooks
- Known hook patterns
- User preferences for hook behavior

**After completing:**

- New hook created -> Append to `.claude/context/memory/learnings.md`
- Issue with hook -> Append to `.claude/context/memory/issues.md`
- Hook design decision -> Append to `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
