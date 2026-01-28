---
name: agent-skill-templates
description: Comprehensive templates, patterns, and best practices for creating Claude Code subagents and skills. Use when building new agents/skills or need reference examples for proper structure and formatting.
---

# Agent & Skill Templates

## Purpose

This skill provides comprehensive templates, patterns, and examples for creating well-structured Claude Code subagents and skills. Use this as a reference when building new agents or skills, or when improving existing ones.

## Context

Quality agents and skills follow consistent patterns and best practices. This skill codifies those patterns into reusable templates that ensure:
- Proper YAML frontmatter structure
- Clear, comprehensive documentation
- Appropriate tool selection
- Effective system prompts
- Well-organized supporting files

## Quick Reference

### When to Use What

**Use a Subagent when:**
- Task requires independent AI reasoning
- Need context isolation from main conversation
- Specialized tool set required
- Recurring complex tasks
- Want proactive automation

**Use a Skill when:**
- Documenting processes/conventions
- Teaching domain-specific knowledge
- Providing templates and references
- Sharing team standards
- Defining workflows

## Subagent Templates

### Template 1: Read-Only Analyzer Agent

**Use for:** Code reviewers, security scanners, analyzers

```yaml
---
name: [agent-name]
description: [Clear, keyword-rich description explaining when to use this agent. Include action verbs users might say like 'review', 'analyze', 'check'. Specify if proactive.]
tools: Read, Grep, Glob, Bash
proactive: [true/false]
---

# [Agent Title]

You are a [role/specialty] specializing in [domain/expertise].

## Your Responsibilities

1. **[Primary Responsibility]**
   - [Specific task 1]
   - [Specific task 2]
   - [Specific task 3]

2. **[Secondary Responsibility]**
   - [Specific task 1]
   - [Specific task 2]

3. **[Tertiary Responsibility]**
   - [Specific task 1]
   - [Specific task 2]

## Analysis Process

1. **[Step 1 Name]**
   - Use [tool] to [action]
   - Identify [what to look for]
   - Document [what to capture]

2. **[Step 2 Name]**
   - Analyze [what]
   - Consider [factors]
   - Evaluate [criteria]

3. **[Step 3 Name]**
   - Generate [output]
   - Structure findings by [organization]
   - Prioritize by [criteria]

## Output Format

You MUST return results in this exact format:

```markdown
# [Analysis Type] Summary

## Overview
[Brief summary of what was analyzed]

## Critical Issues
### 1. [Issue Title]
**Location:** [file:line or section]
**Problem:** [Description]
**Impact:** [Why this matters]
**Recommendation:** [Specific fix]

## Major Issues
[Same format]

## Minor Issues
[Same format]

## Suggestions
[Same format]

## Positive Observations
- ✅ [Good practice identified]
- ✅ [Good practice identified]

## Summary
[Overall assessment and next steps]
```

## Guidelines

1. **[Guideline 1 Title]**
   - [Specific guidance]
   - [Example or clarification]

2. **[Guideline 2 Title]**
   - [Specific guidance]
   - [Example or clarification]

3. **[Guideline 3 Title]**
   - [Specific guidance]
   - [Example or clarification]

## What to Look For

### [Category 1]
- [Specific item to check]
- [Specific item to check]
- [Specific item to check]

### [Category 2]
- [Specific item to check]
- [Specific item to check]

## Constraints

- Do NOT [action you should not take]
- Do NOT [another prohibited action]
- ONLY use [allowed tools/methods]
- Focus on [what to focus on]
- Limit [what to limit]

## Examples

### Example 1: [Scenario]
**Input:** [What user provides]
**Expected Analysis:** [What you should analyze]
**Output:** [What format to return]

### Example 2: [Another Scenario]
[Same pattern]
```

### Template 2: Generator/Writer Agent

**Use for:** Test generators, documentation writers, code generators

```yaml
---
name: [agent-name]
description: [Clear description. Include keywords like 'generate', 'create', 'write'. Explain what it generates and following what standards.]
tools: Read, Write, Edit, Bash
proactive: [false typically - generation usually needs user approval]
---

# [Agent Title]

You are a [role] specializing in generating [what you generate].

## Your Responsibilities

1. **[Generation Responsibility]**
   - Analyze [source material]
   - Generate [output type]
   - Follow [standards/conventions]
   - Ensure [quality criteria]

2. **[Quality Assurance]**
   - Verify [what to verify]
   - Validate [what to validate]
   - Check [what to check]

3. **[Documentation]**
   - Document [what to document]
   - Include [what to include]

## Generation Process

1. **[Step 1: Analysis]**
   - Read [source files]
   - Understand [what to understand]
   - Identify [what to identify]

2. **[Step 2: Planning]**
   - Determine [what to determine]
   - Organize [how to organize]
   - Structure [how to structure]

3. **[Step 3: Generation]**
   - Create [what to create]
   - Follow [conventions/skill]
   - Apply [patterns/templates]

4. **[Step 4: Validation]**
   - Verify [what to verify]
   - Test [what to test]
   - Confirm [what to confirm]

## Standards to Follow

Consult these skills for conventions:
- `[relevant-skill-name]`: For [what standards]
- `[another-skill-name]`: For [what standards]

## Output Format

Generated files should follow this structure:

```[language]
// [Header/documentation]
[Standard file structure]
```

## Guidelines

1. **[Guideline about quality]**
   - [Specific requirement]
   - [Example]

2. **[Guideline about conventions]**
   - [Specific requirement]
   - [Example]

3. **[Guideline about completeness]**
   - [Specific requirement]
   - [Example]

## Templates

Use these templates when generating:

### [Template 1 Name]
```[language]
[Template content]
```

### [Template 2 Name]
```[language]
[Template content]
```

## Constraints

- Do NOT generate [what not to generate]
- ALWAYS include [what must be included]
- MUST follow [what must be followed]
- Verify [what to verify] before writing

## Examples

### Example: [Use Case]
**Input:** [What user provides]
**Analysis:** [What you determine]
**Generated Output:**
```[language]
[Example of generated content]
```

## Validation Checklist

After generation, verify:
- [ ] [Verification item 1]
- [ ] [Verification item 2]
- [ ] [Verification item 3]
- [ ] [Verification item 4]
```

### Template 3: Specialist Agent (Domain Expert)

**Use for:** Security specialists, performance optimizers, architecture advisors

```yaml
---
name: [agent-name]
description: [Clear description of domain expertise. Include technical terms and concepts. Explain when to consult this specialist.]
tools: Read, Grep, Glob, [Write/Edit if making changes]
proactive: [usually false - consultation is user-initiated]
---

# [Agent Title]

You are a [domain] specialist with deep expertise in [specific areas].

## Your Expertise

1. **[Expertise Area 1]**
   - [Specific knowledge/capability]
   - [Specific knowledge/capability]
   - [Specific knowledge/capability]

2. **[Expertise Area 2]**
   - [Specific knowledge/capability]
   - [Specific knowledge/capability]

3. **[Expertise Area 3]**
   - [Specific knowledge/capability]
   - [Specific knowledge/capability]

## When to Consult You

Users should invoke you for:
- [Scenario 1]
- [Scenario 2]
- [Scenario 3]
- [Scenario 4]

## Consultation Process

1. **[Understand the Problem]**
   - Clarify [what needs clarification]
   - Gather [what information needed]
   - Analyze [what to analyze]

2. **[Apply Expertise]**
   - Evaluate [using what criteria]
   - Consider [what factors]
   - Assess [what aspects]

3. **[Provide Recommendations]**
   - Suggest [type of recommendations]
   - Explain [what to explain]
   - Justify [reasoning]
   - Offer alternatives

## Recommendation Format

```markdown
# [Domain] Consultation

## Problem Analysis
[What you understand the problem to be]

## Key Considerations
1. [Consideration 1]
2. [Consideration 2]
3. [Consideration 3]

## Recommendations

### Option 1: [Approach Name] (Recommended)
**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

**Implementation:**
[How to implement]

### Option 2: [Alternative Approach]
**Pros:**
- [Pro 1]

**Cons:**
- [Con 1]

**When to use:** [Specific scenarios]

### Option 3: [Another Alternative]
[Same format]

## Recommended Decision
[Your recommendation with justification]

## Next Steps
1. [Action step 1]
2. [Action step 2]
3. [Action step 3]
```

## Domain Knowledge

### [Concept/Pattern 1]
[Explanation of key concept in your domain]

Best practices:
- [Best practice 1]
- [Best practice 2]

Common pitfalls:
- [Pitfall 1]
- [Pitfall 2]

### [Concept/Pattern 2]
[Similar format]

## Guidelines

1. **[Always do this]**
   - [Specific guidance]

2. **[Never do this]**
   - [Specific guidance]

3. **[Consider this]**
   - [Specific guidance]

## Constraints

- Recommendations must [requirement]
- Analysis should [requirement]
- Do NOT [prohibition]

## Reference Materials

Key principles from [framework/standard]:
- [Principle 1]
- [Principle 2]
- [Principle 3]
```

### Template 4: Process Guide Agent

**Use for:** Deployment guides, workflow managers, procedure executors

```yaml
---
name: [agent-name]
description: [Clear description of process being guided. Include process steps and when to use. Often references a skill for the documented procedure.]
tools: Read, Bash, [Write if creating artifacts]
proactive: [false - processes need user initiation]
---

# [Agent Title]

You are a [process] guide who helps users through [specific procedure].

## Your Responsibilities

1. **[Lead Through Process]**
   - Guide user step-by-step
   - Verify prerequisites
   - Check completion of each step
   - Handle errors and issues

2. **[Ensure Safety]**
   - Validate before proceeding
   - Prevent common mistakes
   - Provide rollback if needed

3. **[Documentation]**
   - Record what was done
   - Document any issues
   - Note deviations from standard

## Process Overview

The [process name] consists of these phases:
1. [Phase 1]: [Brief description]
2. [Phase 2]: [Brief description]
3. [Phase 3]: [Brief description]
4. [Phase 4]: [Brief description]

## Process Execution

### Phase 1: [Phase Name]

**Checklist:**
- [ ] [Prerequisite 1]
- [ ] [Prerequisite 2]
- [ ] [Prerequisite 3]

**Steps:**
1. [Step 1]
   ```bash
   [Command if applicable]
   ```
   **Expected result:** [What should happen]

2. [Step 2]
   [Instructions]
   **Verification:** [How to verify]

**Proceed only after all steps complete successfully.**

### Phase 2: [Phase Name]
[Similar format]

### Phase 3: [Phase Name]
[Similar format]

### Phase 4: [Phase Name]
[Similar format]

## Error Handling

### If [Error Scenario 1] occurs:
1. [Recovery step 1]
2. [Recovery step 2]
3. [When to retry vs rollback]

### If [Error Scenario 2] occurs:
[Similar format]

## Rollback Procedure

If process must be aborted:
1. [Rollback step 1]
2. [Rollback step 2]
3. [Rollback step 3]

## Verification

After process completion, verify:
- [ ] [Verification 1]
- [ ] [Verification 2]
- [ ] [Verification 3]

Commands to verify:
```bash
[Verification commands]
```

## Communication Style

- Ask user to confirm before each phase
- Explain what will happen before doing it
- Report results after each step
- Pause and ask if errors occur
- Summarize at end

## Guidelines

1. **Never skip verification steps**
2. **Always wait for user confirmation before proceeding**
3. **Document any deviations from standard procedure**
4. **Provide clear rollback instructions if issues occur**

## Constraints

- Do NOT proceed if prerequisites not met
- Do NOT skip safety checks
- MUST get user confirmation for destructive operations
- MUST provide rollback option

## Example Session

```
Agent: "Starting [process]. First, I'll verify prerequisites..."

[Checks prerequisites]

Agent: "All prerequisites met. Ready to proceed with Phase 1: [name].
This will [what it does]. Proceed? (yes/no)"

User: "yes"

Agent: "Executing Phase 1..."
[Performs steps]
[Reports results]

Agent: "Phase 1 complete. Results: [summary]. Proceed to Phase 2? (yes/no)"

[Continues through phases]
```
```

## Skill Templates

### Template 1: Conventions/Standards Skill

**Use for:** Coding standards, testing conventions, style guides

```yaml
---
name: [skill-name]
description: [What conventions/standards this documents. Include framework names, technologies, and when to apply these standards.]
allowed-tools: Read, Write, Edit, Bash
---

# [Skill Title]

## Purpose

This skill defines [what standards] for [what area of the project]. Use when [situations where this applies].

## Philosophy

Our approach to [topic] is based on:
1. [Principle 1]: [Explanation]
2. [Principle 2]: [Explanation]
3. [Principle 3]: [Explanation]

## Project Structure

```
[directory-structure]/
├── [subdirectory]/
│   ├── [pattern]/
│   └── [pattern]/
└── [subdirectory]/
```

**Organization:**
- [Directory]: [What goes here]
- [Directory]: [What goes here]
- [Directory]: [What goes here]

## Naming Conventions

### [Type 1] Names
- **Format:** [pattern]
- **Example:** [example]
- **Rules:**
  - [Rule 1]
  - [Rule 2]

### [Type 2] Names
[Similar format]

## Code Standards

### [Category 1]

❌ **Bad:**
```[language]
[Bad example with explanation]
```
**Why bad:** [Explanation]

✅ **Good:**
```[language]
[Good example with explanation]
```
**Why good:** [Explanation]

### [Category 2]
[Similar format]

## Patterns to Use

### Pattern 1: [Pattern Name]
**When to use:** [Scenario]

**Implementation:**
```[language]
[Pattern implementation]
```

**Example:**
```[language]
[Complete example]
```

### Pattern 2: [Pattern Name]
[Similar format]

## Patterns to Avoid

### Anti-Pattern 1: [Name]
**Problem:** [What's wrong]

❌ **Don't do this:**
```[language]
[Anti-pattern example]
```

✅ **Do this instead:**
```[language]
[Correct pattern]
```

**Reason:** [Why the correct way is better]

## Best Practices

1. **[Practice 1]**
   - [Specific guideline]
   - [Why it matters]
   - Example:
     ```[language]
     [Example]
     ```

2. **[Practice 2]**
   [Similar format]

3. **[Practice 3]**
   [Similar format]

## Common Pitfalls

### Pitfall 1: [Name]
**What happens:** [Description of problem]

**How to avoid:**
- [Solution 1]
- [Solution 2]

**Example:**
```[language]
// Pitfall
[Bad code]

// Solution
[Good code]
```

### Pitfall 2: [Name]
[Similar format]

## Checklist

Use this to verify compliance:
- [ ] [Check 1]
- [ ] [Check 2]
- [ ] [Check 3]
- [ ] [Check 4]

## Tools and Configuration

### [Tool 1]
**Configuration:**
```[config-format]
[Configuration file content]
```

**Usage:**
```bash
[Command to run tool]
```

### [Tool 2]
[Similar format]

## Related Skills

- **[related-skill-1]**: [When to use instead/together]
- **[related-skill-2]**: [Relationship]

## References

- [External documentation link]
- [Internal wiki/docs]
- [Standards documentation]
```

### Template 2: Process Documentation Skill

**Use for:** Deployment processes, CI/CD workflows, incident response

```yaml
---
name: [skill-name]
description: [What process this documents. Include keywords for when this process applies and what triggers it.]
allowed-tools: Read, Write, Bash
---

# [Skill Title]

## Purpose

This skill documents the [process name] procedure for [context]. Use when [triggering scenarios].

## Prerequisites

Before starting:
- [ ] [Requirement 1]
- [ ] [Requirement 2]
- [ ] [Requirement 3]

**How to verify:**
```bash
[Commands to check prerequisites]
```

## Process Overview

```
[Phase 1] → [Phase 2] → [Phase 3] → [Phase 4]
   ↓            ↓            ↓            ↓
 [Tasks]     [Tasks]      [Tasks]      [Tasks]
```

**Timeline:** [Expected duration]
**Participants:** [Who's involved]

## Phase 1: [Phase Name]

### Objective
[What this phase accomplishes]

### Steps

#### Step 1: [Step Name]
**Action:**
[What to do]

**Commands:**
```bash
[Commands to execute]
```

**Expected Output:**
```
[What you should see]
```

**Verification:**
```bash
[How to verify success]
```

#### Step 2: [Step Name]
[Similar format]

### Completion Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Phase 2: [Phase Name]
[Similar format to Phase 1]

## Phase 3: [Phase Name]
[Similar format]

## Phase 4: [Phase Name]
[Similar format]

## Error Handling

### Error: [Error Type 1]
**Symptoms:**
- [Symptom 1]
- [Symptom 2]

**Diagnosis:**
```bash
[Commands to diagnose]
```

**Resolution:**
1. [Resolution step 1]
2. [Resolution step 2]

**Prevention:**
[How to prevent this error]

### Error: [Error Type 2]
[Similar format]

## Rollback Procedure

If the process must be aborted:

### Step 1: [Rollback Step]
```bash
[Rollback commands]
```

### Step 2: [Rollback Step]
[Continue]

### Verification After Rollback
```bash
[Verify system state]
```

## Best Practices

1. **[Practice 1]**
   - [Why this matters]
   - [How to apply]

2. **[Practice 2]**
   [Similar format]

## Common Mistakes

### Mistake 1: [Description]
**Problem:** [What goes wrong]
**Solution:** [How to avoid]

### Mistake 2: [Description]
[Similar format]

## Checklists

### Pre-Process Checklist
- [ ] [Item 1]
- [ ] [Item 2]
- [ ] [Item 3]

### During Process Checklist
- [ ] [Item 1]
- [ ] [Item 2]

### Post-Process Checklist
- [ ] [Item 1]
- [ ] [Item 2]

## Supporting Scripts

### Script: [script-name.sh]
**Location:** `scripts/[script-name].sh`

**Purpose:** [What it does]

**Usage:**
```bash
./scripts/[script-name].sh [arguments]
```

**Parameters:**
- `[param1]`: [Description]
- `[param2]`: [Description]

## Templates

### Template: [Template Name]
**Location:** `templates/[template-file]`

**Usage:**
1. Copy template
2. Replace placeholders:
   - `[PLACEHOLDER1]`: [What to put]
   - `[PLACEHOLDER2]`: [What to put]
3. Save to [location]

## Related Skills

- **[related-skill]**: [How they relate]

## References

- [Documentation links]
- [Runbook links]
- [Team wiki]
```

### Template 3: Technical Domain Knowledge Skill

**Use for:** API design patterns, security practices, architecture patterns

```yaml
---
name: [skill-name]
description: [What domain knowledge this provides. Include technical terms, concepts, and when this knowledge applies.]
---

# [Skill Title]

## Purpose

This skill provides guidance on [domain topic] for [context]. Use when [scenarios].

## Core Concepts

### Concept 1: [Name]
**Definition:** [Clear definition]

**When to use:** [Scenarios]

**How it works:**
[Explanation with diagrams if helpful]

**Example:**
```[language/format]
[Concrete example]
```

### Concept 2: [Name]
[Similar format]

### Concept 3: [Name]
[Similar format]

## Design Patterns

### Pattern 1: [Pattern Name]

**Intent:** [What problem this solves]

**When to use:**
- [Scenario 1]
- [Scenario 2]
- [Scenario 3]

**Structure:**
```
[ASCII diagram or description of pattern structure]
```

**Implementation:**
```[language]
[Code example showing pattern]
```

**Pros:**
- [Advantage 1]
- [Advantage 2]

**Cons:**
- [Limitation 1]
- [Limitation 2]

**Example:**
```[language]
[Complete working example]
```

### Pattern 2: [Pattern Name]
[Similar format]

## Decision Framework

When deciding [what to decide]:

```
Question 1: [Decision question]?
├─ Yes → [Recommendation A]
│   └─ Use: [Pattern/approach]
└─ No → Question 2: [Next decision]?
    ├─ Yes → [Recommendation B]
    └─ No → [Recommendation C]
```

## Best Practices

### Practice 1: [Name]
**Principle:** [Core principle]

**Why it matters:** [Explanation]

**How to apply:**
1. [Step 1]
2. [Step 2]

❌ **Wrong:**
```[language]
[Bad example]
```

✅ **Right:**
```[language]
[Good example]
```

### Practice 2: [Name]
[Similar format]

## Common Mistakes

### Mistake 1: [Anti-Pattern Name]
**Problem:** [What people do wrong]

**Why it's wrong:** [Consequences]

**Impact:**
- [Negative impact 1]
- [Negative impact 2]

**How to fix:**
```[language]
// Before (wrong)
[Wrong code]

// After (correct)
[Correct code]
```

### Mistake 2: [Anti-Pattern Name]
[Similar format]

## Examples

### Example 1: [Real-World Scenario]
**Context:** [Situation]

**Requirements:**
- [Requirement 1]
- [Requirement 2]

**Solution:**
```[language]
[Complete implementation]
```

**Explanation:**
[Why this solution works]

### Example 2: [Another Scenario]
[Similar format]

## Advanced Topics

### Topic 1: [Advanced Concept]
[Explanation for experienced users]

### Topic 2: [Advanced Concept]
[Similar format]

## Trade-Offs

### Trade-Off 1: [A vs B]
**Option A: [Approach A]**
- Pros: [Pros]
- Cons: [Cons]
- When to choose: [Scenarios]

**Option B: [Approach B]**
- Pros: [Pros]
- Cons: [Cons]
- When to choose: [Scenarios]

## Related Skills

- **[related-skill-1]**: [Relationship]
- **[related-skill-2]**: [Relationship]

## Further Reading

- [External resource 1]
- [External resource 2]
- [Internal documentation]
```

## Supporting File Templates

### Template: Unit Test Template

**Location:** `templates/unit-test.template`

```javascript
// tests/unit/[module-name].test.js
import { describe, it, expect, beforeEach, afterEach } from 'vitest'
import { [ClassOrFunction] } from '@/[path]'

describe('[ClassOrFunction]', () => {
  let [instance]

  beforeEach(() => {
    // Setup before each test
    [instance] = new [ClassOrFunction]()
  })

  afterEach(() => {
    // Cleanup after each test
  })

  describe('[methodName]', () => {
    it('should [expected behavior] when [condition]', () => {
      // Arrange
      const [input] = { /* test data */ }

      // Act
      const result = [instance].[methodName]([input])

      // Assert
      expect(result).toEqual(/* expected output */)
    })

    it('should throw [ErrorType] when [invalid condition]', () => {
      // Arrange
      const [invalidInput] = { /* invalid data */ }

      // Act & Assert
      expect(() => [instance].[methodName]([invalidInput]))
        .toThrow([ErrorType])
    })

    it('should [edge case behavior]', () => {
      // Test edge cases
    })
  })
})
```

### Template: Integration Test Template

**Location:** `templates/integration-test.template`

```javascript
// tests/integration/[module-name].integration.test.js
import { describe, it, expect, beforeAll, afterAll } from 'vitest'
import { setupTestDatabase, teardownTestDatabase } from '@/tests/helpers/db'
import request from 'supertest'
import app from '@/app'

describe('[Feature] Integration Tests', () => {
  beforeAll(async () => {
    await setupTestDatabase()
  })

  afterAll(async () => {
    await teardownTestDatabase()
  })

  describe('[HTTP_METHOD] /[endpoint]', () => {
    it('should return [status] with [expected data] when [condition]', async () => {
      // Arrange
      const [requestData] = {
        // Request payload
      }

      // Act
      const response = await request(app)
        .[method]('/[endpoint]')
        .send([requestData])

      // Assert
      expect(response.status).toBe([expectedStatus])
      expect(response.body).toMatchObject({
        // Expected response shape
      })
    })

    it('should return [error status] when [error condition]', async () => {
      // Test error scenarios
    })
  })
})
```

### Template: Agent Creation Script

**Location:** `templates/create-agent.sh`

```bash
#!/bin/bash

# Agent Creation Helper Script
# Usage: ./create-agent.sh <agent-name> <agent-type>
# Types: analyzer, generator, specialist, process-guide

AGENT_NAME=$1
AGENT_TYPE=${2:-"analyzer"}

if [ -z "$AGENT_NAME" ]; then
  echo "Usage: $0 <agent-name> [agent-type]"
  echo "Types: analyzer, generator, specialist, process-guide"
  exit 1
fi

AGENT_FILE=".claude/agents/${AGENT_NAME}.md"

mkdir -p .claude/agents

case $AGENT_TYPE in
  "analyzer")
    TOOLS="Read, Grep, Glob, Bash"
    ROLE="analyzer"
    ;;
  "generator")
    TOOLS="Read, Write, Edit, Bash"
    ROLE="generator"
    ;;
  "specialist")
    TOOLS="Read, Grep, Glob"
    ROLE="specialist"
    ;;
  "process-guide")
    TOOLS="Read, Bash"
    ROLE="process guide"
    ;;
  *)
    echo "Unknown type: $AGENT_TYPE"
    exit 1
    ;;
esac

cat > "$AGENT_FILE" <<EOF
---
name: $AGENT_NAME
description: [FILL IN: Clear description of when to use this agent]
tools: $TOOLS
proactive: false
---

# ${AGENT_NAME^} Agent

You are a $ROLE specializing in [FILL IN: domain].

## Your Responsibilities

1. **[FILL IN: Primary Responsibility]**
   - [Task 1]
   - [Task 2]

## Guidelines

1. [FILL IN: Guideline]

## Output Format

[FILL IN: Define output structure]

## Constraints

- Do NOT [FILL IN: constraints]
EOF

echo "Created agent: $AGENT_FILE"
echo "Please edit and fill in the [FILL IN: ...] placeholders"
```

### Template: Skill Creation Script

**Location:** `templates/create-skill.sh`

```bash
#!/bin/bash

# Skill Creation Helper Script
# Usage: ./create-skill.sh <skill-name> <skill-type>
# Types: conventions, process, domain-knowledge

SKILL_NAME=$1
SKILL_TYPE=${2:-"conventions"}

if [ -z "$SKILL_NAME" ]; then
  echo "Usage: $0 <skill-name> [skill-type]"
  echo "Types: conventions, process, domain-knowledge"
  exit 1
fi

SKILL_DIR=".claude/skills/${SKILL_NAME}"
SKILL_FILE="${SKILL_DIR}/SKILL.md"

mkdir -p "$SKILL_DIR"
mkdir -p "${SKILL_DIR}/templates"
mkdir -p "${SKILL_DIR}/examples"

cat > "$SKILL_FILE" <<EOF
---
name: $SKILL_NAME
description: [FILL IN: Clear description with keywords]
---

# ${SKILL_NAME^} Skill

## Purpose

[FILL IN: What this skill teaches and when to use it]

## Instructions

1. **[FILL IN: Step 1]**
   - [Detail]

## Examples

### Example 1: [FILL IN: Scenario]

❌ **Bad:**
\`\`\`
[Bad example]
\`\`\`

✅ **Good:**
\`\`\`
[Good example]
\`\`\`

## Best Practices

1. **[FILL IN: Practice]**
   - [Why it matters]

## Common Pitfalls

### Pitfall 1: [FILL IN: Name]
**How to avoid:** [Solution]

## Related Skills

- **[related-skill]**: [Relationship]
EOF

echo "Created skill: $SKILL_FILE"
echo "Created directories:"
echo "  - ${SKILL_DIR}/templates/"
echo "  - ${SKILL_DIR}/examples/"
echo ""
echo "Please edit and fill in the [FILL IN: ...] placeholders"
```

## Best Practices Summary

### For Subagents

1. **Single Responsibility**: One clear, focused purpose
2. **Tool Minimalism**: Only grant necessary tools
3. **Clear Descriptions**: Keyword-rich, specific, 20+ words
4. **Explicit Output**: Define exact format in system prompt
5. **Appropriate Proactivity**: Most agents should be `proactive: false`
6. **Comprehensive Prompts**: Role, responsibilities, guidelines, constraints, examples

### For Skills

1. **Clear Instructions**: Step-by-step, actionable guidance
2. **Comprehensive Examples**: Both good and bad with explanations
3. **Focused Scope**: One domain/topic per skill, under 500 lines
4. **Supporting Files**: Templates, examples, scripts well-organized
5. **Best Practices**: Document "why" not just "what"
6. **Common Pitfalls**: Show mistakes and how to avoid them

## Quality Checklist

### Before Creating an Agent
- [ ] Is a subagent the right tool? (vs skill or just asking Claude)
- [ ] Is the scope focused enough? (single responsibility)
- [ ] Have I minimized the tool set?
- [ ] Is the description clear and keyword-rich?
- [ ] Is the output format explicitly defined?
- [ ] Have I included examples in the system prompt?
- [ ] Are constraints clearly stated?

### Before Creating a Skill
- [ ] Is a skill the right tool? (vs subagent)
- [ ] Is the scope focused enough? (one domain/topic)
- [ ] Are instructions step-by-step and actionable?
- [ ] Do I have comprehensive examples (good & bad)?
- [ ] Are supporting files needed and created?
- [ ] Are best practices documented?
- [ ] Are common pitfalls covered?
- [ ] Is it under 500 lines? (if not, should it be split?)

## Quick Reference Commands

```bash
# List all agents
ls -1 .claude/agents/

# List all skills
ls -1 .claude/skills/

# Create new agent (using template script)
./templates/create-agent.sh my-agent analyzer

# Create new skill (using template script)
./templates/create-skill.sh my-skill conventions

# View agent
cat .claude/agents/agent-name.md

# View skill
cat .claude/skills/skill-name/SKILL.md
```

## Related Agents

- **agent-builder**: Uses these templates to create new agents
- **skill-builder**: Uses these templates to create new skills
- **agent-skill-analyzer**: Uses these templates as quality benchmarks

---

**Remember:** These templates are starting points. Customize them for your specific use case while maintaining the core structure and best practices.

**Version:** 1.0
**Last Updated:** 2025-12-19
