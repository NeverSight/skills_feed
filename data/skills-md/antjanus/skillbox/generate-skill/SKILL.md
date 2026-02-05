---
name: generate-skill
description: Use when asked to "create a skill", "generate a SKILL.md", "make me a skill", "build a custom skill", or when user wants to extend Claude Code capabilities with a new skill
license: MIT
metadata:
  author: Antonin Januska
  version: "1.1.0"
  argument-hint: [skill-topic]
tags: [skill-creation, meta, automation, documentation]
---

# Generate Skill - Interactive Skill Builder

## Overview

This skill guides users through creating high-quality Claude Code skills using proven patterns from top community skills (obra/superpowers, Anthropic, Vercel). It asks targeted questions to understand requirements, then generates a complete SKILL.md file with appropriate structure, documentation, and best practices.

**Core principle:** Generate skills that activate reliably, enforce processes effectively, and consume context efficiently.

## When to Use

**Always use when user asks to:**
- "Create a skill for [topic]"
- "Generate a SKILL.md for [workflow]"
- "Build me a skill that does [task]"
- "Help me make a custom skill"
- "Turn these instructions into a skill"

**Useful for:**
- Capturing team workflows as reusable skills
- Documenting methodology enforcement (TDD, debugging, code review)
- Creating automation skills (deployment, testing, setup)
- Building domain-specific guidance (architecture, security, performance)

**Avoid when:**
- User just wants general help (not skill creation)
- Requirement is too vague to create useful skill
- Task is better solved with existing skills

## The Skill Generation Process

### Phase 1: Discovery - Understanding Requirements

**You MUST gather this information through AskUserQuestion:**

1. **Skill purpose and triggers**
   - What should this skill help with?
   - When should Claude activate it?
   - What user phrases should trigger it?

2. **Skill type identification**
   - Methodology enforcement? (TDD, debugging process, code review)
   - Technical implementation? (project setup, build automation, deployment)
   - Rule-based auditing? (code quality, performance, accessibility)
   - Automation/integration? (browser testing, API calls, CI/CD)
   - Reference/knowledge? (library patterns, architecture, best practices)

3. **Content requirements**
   - Existing documentation to incorporate?
   - Specific rules or checklists?
   - Code examples needed?
   - Scripts or automation required?

4. **Enforcement level**
   - Strict methodology with "Iron Laws"?
   - Flexible guidance with recommendations?
   - Checklist-based verification?

**Ask these questions interactively:**
```markdown
Use AskUserQuestion tool with these questions:

Question 1: "What task or workflow should this skill help with?"
- Header: "Purpose"
- Options:
  1. Enforce a development methodology (TDD, debugging, code review)
  2. Automate technical tasks (setup, deployment, testing)
  3. Audit code against rules (performance, accessibility, security)
  4. Provide reference knowledge (patterns, architecture, APIs)
  5. Integrate external tools (browsers, services, CI/CD)

Question 2: "What should trigger this skill?"
- Header: "Triggers"
- Options:
  1. Specific user phrases (list them)
  2. File types or patterns (e.g., *.tsx files)
  3. Project characteristics (e.g., Next.js projects)
  4. Development phases (e.g., before implementing features)

Question 3: "How strict should enforcement be?"
- Header: "Enforcement"
- Options:
  1. Strict - Iron Laws with mandatory phases
  2. Guided - Clear recommendations with Red Flags
  3. Flexible - Best practices and suggestions
  4. Reference only - Information when needed
```

**Verification before proceeding:**
- [ ] Skill purpose clearly defined
- [ ] Activation triggers identified
- [ ] Skill type determined
- [ ] Enforcement level chosen
- [ ] User provided any existing documentation or rules

### Phase 2: Pattern Selection

**Based on skill type, select appropriate pattern:**

#### Pattern A: Methodology Enforcement
**Use when:** TDD, debugging, code review, quality gates

**Structure:**
```markdown
# Skill Title

## Overview
[Core principle statement]

## The Iron Law (if strict enforcement)
```
NON-NEGOTIABLE RULE
```

## When to Use
[Specific triggers]

## The Process (Phase-Based)

### Phase 1: [Step Name]
**Before proceeding, you MUST:**
- [ ] Requirement 1
- [ ] Requirement 2

### Phase 2: [Step Name]
[...]

## Red Flags - STOP
- Warning sign 1
- Warning sign 2

**If you see these: STOP and return to Phase 1**

## Verification Checklist
- [ ] Requirement 1
- [ ] Requirement 2

## Common Rationalizations
| Excuse | Reality |
|--------|---------|
| "Just this once..." | Always leads to problems |

## Examples
<Good>
[Code example]
</Good>

<Bad>
[Code example]
</Bad>
```

#### Pattern B: Technical Implementation
**Use when:** Project setup, build automation, deployment

**Structure:**
```markdown
# Skill Title

## Overview
[What it does and tech stack]

## Quick Start

### Step 1: Setup
```bash
command-here
```

### Step 2: Configure
[Instructions]

### Step 3: Execute
```bash
command-here
```

## Configuration Options
[Customization details]

## Common Patterns
[Code examples]

## Troubleshooting
**Problem:** [Issue]
**Solution:** [Fix]

## Integration
**Pairs with:**
- Other skills
```

#### Pattern C: Rule-Based Auditing
**Use when:** Code quality, performance, accessibility checks

**Structure:**
```markdown
# Skill Title

## How It Works
1. Read specified files
2. Check against rules
3. Output findings in priority order

## Rule Categories

| Priority | Category | Impact |
|----------|----------|--------|
| CRITICAL | Category A | Must fix |
| HIGH | Category B | Should fix |

## Quick Reference

### Category A (CRITICAL)
- `rule-id-1` - Description
- `rule-id-2` - Description

## Usage
[How to invoke]

## Output Format
```
CRITICAL: Issue description (file.js:123)
- Impact: [explanation]
- Fix: [solution]
```
```

#### Pattern D: Automation/Integration
**Use when:** Browser testing, API integration, external tools

**Structure:**
```markdown
# Skill Title

## How It Works
[High-level workflow]

## Critical Workflow
1. Auto-detect environment
2. Generate configuration
3. Execute with parameters
4. Present results

## Auto-Detection
```bash
# Detection script
```

## Configuration
[Parameterization details]

## Helper Functions
[Utility library if needed]

## Common Tasks
[Pre-built examples]

## Troubleshooting
[Common issues]
```

#### Pattern E: Reference/Knowledge
**Use when:** Library usage, architecture patterns, domain knowledge

**Structure:**
```markdown
# Skill Title

## Overview
[When to use this knowledge]

## Core Concepts
[Key ideas explained]

## Patterns Library

### Pattern A: [Use Case]
```javascript
// Code example with annotations
```

### Pattern B: [Use Case]
```javascript
// Code example
```

## Best Practices
[Guidelines]

## Common Mistakes
[Anti-patterns to avoid]

## When NOT to Use
[Situations to avoid]
```

**You MUST select pattern before generating:**
- [ ] Pattern matches skill type
- [ ] Pattern supports enforcement level
- [ ] Pattern includes necessary sections

### Phase 3: Content Generation

**Generate SKILL.md with these required components:**

#### 1. Frontmatter (CRITICAL)
```yaml
---
name: skill-name-kebab-case
description: |
  Use when [trigger phrase 1], when asked to "[user phrase]",
  or when [situation]. Include multiple trigger variations for
  better activation. Be specific about WHEN to activate.
license: MIT
metadata:
  author: [author-name]
  version: "1.0.0"
  argument-hint: <optional-args>
tags: [relevant, tags, here]
hooks:                           # Optional: automation triggers
  post_tool_use:
    - Action after Write/Edit operations
  stop:
    - Action before session ends
---
```

**Required fields:**
- `name` - kebab-case skill identifier (used in `/skill-name`)
- `description` - Trigger-rich activation text (see best practices below)

**Optional fields:**
- `license` - License type (default: MIT)
- `metadata.author` - Creator name
- `metadata.version` - Semantic version (e.g., "1.0.0")
- `metadata.argument-hint` - Hint shown for skill arguments (e.g., `<branch-name>`)
- `tags` - Array of categorization tags
- `hooks` - Automation triggers (post_tool_use, stop, etc.)

**Description field best practices:**
- ✅ Include 3-5 specific trigger phrases
- ✅ Use "when" clauses for situations
- ✅ Include user language ("when asked to 'do X'")
- ✅ Be concrete, not vague
- ❌ Avoid: "A skill for..." (too vague)
- ❌ Avoid: Single generic description

**Hooks field (advanced):**
Use hooks to automate actions at specific points:
- `post_tool_use` - Runs after Write, Edit, or other tools
- `stop` - Runs before session ends (verification, cleanup)
- Example use: Auto-updating progress files, verification checklists

#### 2. Overview Section
```markdown
# Skill Title

## Overview

[1-2 sentence description of what this skill does and why it matters]

**Core principle:** [One-line principle statement]
```

#### 3. When to Use Section
```markdown
## When to Use

**Always use when:**
- Specific situation A
- Specific situation B

**Useful for:**
- Use case C
- Use case D

**Avoid when:**
- Situation E (use skill-X instead)
- Situation F (not applicable)
```

#### 4. Main Content (Pattern-Specific)
[Insert selected pattern structure here]

#### 5. Quick Reference (if applicable)
```markdown
## Quick Reference

| Situation | Action |
|-----------|--------|
| Case A | Do X |
| Case B | Do Y |

Or:

```bash
# Common commands
command-1  # Description
command-2  # Description
```
```

#### 6. Red Flags (for methodology skills)
```markdown
## Red Flags - STOP

If you catch yourself thinking:
- "Quick fix for now..."
- "Skip this step just once..."
- "I don't fully understand but..."

**ALL of these mean: STOP. Return to Phase 1.**
```

#### 7. Examples Section
```markdown
## Examples

### Example 1: [Common Scenario]

<Good>
```language
// Good example code
```
[Explanation why this is good]
</Good>

<Bad>
```language
// Bad example code
```
[Explanation why this is bad]
</Bad>
```

#### 8. Troubleshooting Section
```markdown
## Troubleshooting

### Problem: [Common Issue]

**Cause:** [Why it happens]

**Solution:**
```bash
commands-to-fix
```

[Explanation]
```

#### 9. Integration Section (if applicable)
```markdown
## Integration

**This skill:**
- What it does in workflow

**Pairs with:**
- skill-name-1 - How they work together
- skill-name-2 - How they work together

**Called by:**
- Parent skill (Phase N) - When it's invoked
```

#### 10. References Section
```markdown
## References

**Based on:**
- [Source 1](url)
- [Source 2](url)

**Official Documentation:**
- [Doc 1](url)

**Community Resources:**
- [Resource 1](url)
```

**Verification checklist:**
- [ ] All 10 components included
- [ ] Trigger-rich description field
- [ ] Clear examples with Good/Bad comparisons
- [ ] Phase-based workflow (if methodology)
- [ ] Troubleshooting section complete
- [ ] Integration points documented

### Phase 4: Enhancement and Refinement

**Add these enhancements based on skill complexity:**

#### For Simple Skills (< 300 lines)
- ✅ Single SKILL.md file
- ✅ Inline examples
- ✅ Basic troubleshooting
- ✅ Quick reference table

#### For Medium Skills (300-500 lines)
- ✅ SKILL.md with detailed sections
- ✅ Multiple examples (3-5)
- ✅ Comprehensive troubleshooting
- ✅ Integration documentation
- ✅ Consider reference/ directory for extended docs

#### For Complex Skills (> 500 lines)
- ✅ SKILL.md (core guide, < 500 lines)
- ✅ reference/ directory with:
  - STANDARDS.md (detailed rules)
  - EXAMPLES.md (extensive code samples)
  - TROUBLESHOOTING.md (advanced issues)
- ✅ scripts/ directory if automation needed
- ✅ Progressive disclosure pattern
- ✅ Helper libraries (lib/ directory)

**Progressive disclosure example:**
```markdown
## Deep Reference

For detailed information, load these files when needed:

- **[📋 Complete Standards](./reference/STANDARDS.md)** - Full rule set
- **[⚡ Code Examples](./reference/EXAMPLES.md)** - 50+ examples
- **[🔧 Advanced Troubleshooting](./reference/TROUBLESHOOTING.md)**

*Only load these when specifically needed to save context.*
```

**Verification:**
- [ ] Appropriate complexity level chosen
- [ ] Files organized logically
- [ ] Progressive disclosure if > 500 lines
- [ ] No unnecessary complexity

### Phase 5: Scripts and Automation (Optional)

**If skill requires scripts, create these:**

#### Setup Script Pattern
```bash
#!/bin/bash
set -e  # Fail fast

echo "Setting up [skill-name]..." >&2

# Install dependencies
npm install dependency1 dependency2

# Configure environment
cp .env.example .env

# Verify installation
echo '{"status": "success", "message": "Setup complete"}' # JSON output
```

#### Execution Script Pattern
```bash
#!/bin/bash
set -e

# Parse arguments
TARGET="${1:-default-value}"

echo "Running [task] on $TARGET..." >&2

# Auto-detect environment
DETECTED=$(detect_environment)

# Execute main task
result=$(perform_task "$TARGET")

# Output structured result
echo "{\"status\": \"success\", \"result\": \"$result\"}"
```

#### Helper Library Pattern (Node.js)
```javascript
// lib/helpers.js
module.exports = {
  async autoDetect() {
    // Auto-detection logic
    return detected_value;
  },

  async safeOperation(params) {
    // Safe operations with retry
    for (let i = 0; i < 3; i++) {
      try {
        return await operation(params);
      } catch (e) {
        if (i === 2) throw e;
      }
    }
  },

  formatOutput(data) {
    // Standardized formatting
    return JSON.stringify(data, null, 2);
  }
};
```

**Script best practices:**
- ✅ Use `set -e` for error handling
- ✅ Status messages to stderr (>&2)
- ✅ Data output to stdout (JSON preferred)
- ✅ Cleanup traps for temp files
- ✅ Parameterization at top
- ✅ Auto-detection where possible

**Verification:**
- [ ] Scripts executable (chmod +x)
- [ ] Error handling implemented
- [ ] Output properly formatted
- [ ] Dependencies documented
- [ ] Scripts tested manually

### Phase 6: Finalization and Output

**Before presenting skill to user:**

1. **Run quality checklist:**
   - [ ] Description field has 3+ trigger phrases
   - [ ] Overview explains core principle clearly
   - [ ] Examples include Good/Bad comparisons
   - [ ] Troubleshooting section addresses common issues
   - [ ] Appropriate pattern for skill type
   - [ ] Under 500 lines or uses progressive disclosure
   - [ ] Integration points documented
   - [ ] References included

2. **Validate against anti-patterns:**
   - ❌ Vague description ("provides testing")
   - ❌ No examples
   - ❌ Missing troubleshooting
   - ❌ No clear triggers
   - ❌ Monolithic structure (>1000 lines without reference/)
   - ❌ No verification checklists (for methodology skills)

3. **Generate folder structure suggestion:**
```markdown
## Skill Structure

```
skill-name/
├── SKILL.md              # Core skill (generated)
├── reference/            # Optional: extended docs
│   ├── STANDARDS.md
│   └── EXAMPLES.md
├── scripts/              # Optional: automation
│   ├── setup.sh
│   └── execute.sh
└── lib/                  # Optional: helpers
    └── helpers.js
```

## Installation

**Local (for testing):**
```bash
mkdir -p ~/.claude/skills/skill-name
# Save SKILL.md to this directory
```

**Project-specific:**
```bash
mkdir -p .claude/skills/skill-name
# Save SKILL.md to this directory
```

## Usage

Activate by asking Claude:
- "[trigger phrase 1]"
- "[trigger phrase 2]"

Or explicitly: `/skill-name`
```

4. **Present complete SKILL.md:**
   - Write full SKILL.md content
   - Include folder structure
   - Include installation instructions
   - Include usage examples

**Final verification:**
- [ ] Complete SKILL.md generated
- [ ] Quality checklist passed
- [ ] Installation instructions provided
- [ ] Usage examples included
- [ ] No anti-patterns present

## Skill Generation Templates

### Template Variables

When generating, customize these placeholders:

```markdown
# Frontmatter variables
{{SKILL_NAME}}         # kebab-case name (required)
{{DESCRIPTION}}        # Trigger-rich description (required)
{{LICENSE}}            # License type (default: MIT)
{{AUTHOR}}             # Author name
{{VERSION}}            # Semantic version (default: "1.0.0")
{{ARGUMENT_HINT}}      # Argument hint (e.g., <branch-name>)
{{TAGS}}               # Array of tags
{{HOOKS}}              # Optional automation hooks

# Content variables
{{SKILL_TITLE}}        # Human-readable title
{{CORE_PRINCIPLE}}     # One-line principle
{{TRIGGER_PHRASES}}    # List of activation phrases
{{PATTERN_CONTENT}}    # Pattern-specific structure
{{EXAMPLES}}           # Code examples
{{TROUBLESHOOTING}}    # Common issues
{{REFERENCES}}         # Source links
```

### Quick Generation Flow

```
1. Ask user questions →
2. Determine skill type →
3. Select pattern →
4. Generate content →
5. Add examples →
6. Add troubleshooting →
7. Quality check →
8. Present to user
```

## Red Flags During Generation

If you catch yourself:

- **Generating without asking questions** - Need user input first!
- **Using vague description field** - Add specific triggers
- **Skipping examples section** - Always include Good/Bad examples
- **No troubleshooting** - Users will encounter issues
- **Wrong pattern for skill type** - Review pattern selection
- **Over 500 lines without progressive disclosure** - Split into reference/
- **No verification checklist for methodology skills** - Required for enforcement

**ALL of these mean: STOP. Return to appropriate phase.**

## Examples of Generated Skills

### Example 1: Methodology Skill Request

**User:** "Create a skill for enforcing commit message conventions"

**Generated Skill Structure:**
- Pattern A (Methodology Enforcement)
- Iron Law: "No commit without following format"
- Phases: Validate → Format → Verify
- Red Flags: "Quick commit for now..."
- Verification Checklist
- Examples: Good/Bad commit messages

### Example 2: Automation Skill Request

**User:** "Make a skill that runs database migrations safely"

**Generated Skill Structure:**
- Pattern D (Automation/Integration)
- Auto-detect: Database type, migration tool
- Workflow: Backup → Dry run → Execute → Verify
- Scripts: setup.sh, migrate.sh, rollback.sh
- Helper functions: safe_backup(), verify_schema()
- Troubleshooting: Connection issues, rollback procedures

### Example 3: Auditing Skill Request

**User:** "Build a skill to check Python code for security issues"

**Generated Skill Structure:**
- Pattern C (Rule-Based Auditing)
- Rule categories: CRITICAL, HIGH, MEDIUM, LOW
- Rules: SQL injection, XSS, hardcoded secrets, unsafe eval
- Output format: `file.py:123 CRITICAL: SQL injection risk`
- Quick reference: Table of rules by priority
- Examples: Vulnerable code → Secure code

## Advanced: Multi-File Skills

For complex skills, generate multiple files:

**SKILL.md (core, < 500 lines):**
```yaml
---
name: complex-skill
description: [triggers]
---

# Complex Skill

## Quick Start
[Essential info]

## Core Workflow
[Main process]

## Deep Reference
- [📋 Standards](./reference/STANDARDS.md) - 100+ rules
- [⚡ Examples](./reference/EXAMPLES.md) - 50+ examples
```

**reference/STANDARDS.md:**
```markdown
# Detailed Standards Reference

## Category A Rules

### Rule: RULE-001
- **Severity:** Critical
- **Description:** [detailed explanation]
- **Fix:** [solution]
- **Example:** See EXAMPLES.md #001

[... extensive rule documentation ...]
```

**reference/EXAMPLES.md:**
```markdown
# Code Examples

## Example #001: [Rule Name]

### Before (Problematic)
```python
# Bad code
```

### After (Fixed)
```python
# Good code
```

[... 50+ examples ...]
```

**Generate this structure when:**
- Skill has 20+ rules
- Extensive examples needed (10+)
- Complex troubleshooting
- Multiple integration points

## Quality Standards Checklist

Before delivering generated skill:

### Documentation Quality
- [ ] Description has 3-5 trigger phrases
- [ ] Overview explains core principle (1-2 sentences)
- [ ] "When to Use" lists specific situations
- [ ] Examples show Good/Bad comparisons
- [ ] Quick reference included (table or commands)

### Structure Quality
- [ ] SKILL.md under 500 lines (or progressive disclosure)
- [ ] Sections in logical order
- [ ] Proper Markdown formatting
- [ ] Code blocks have language specified

### Content Quality
- [ ] Step-by-step instructions clear
- [ ] Phases have completion criteria (methodology skills)
- [ ] Red flags documented (methodology skills)
- [ ] Verification checklist provided (methodology skills)
- [ ] Troubleshooting addresses real issues
- [ ] Integration points documented

### Script Quality (if applicable)
- [ ] Scripts use `set -e`
- [ ] Status to stderr, data to stdout
- [ ] Cleanup traps for temp files
- [ ] Dependencies documented

### User Experience
- [ ] Auto-detection where possible
- [ ] Clear prompts for ambiguity
- [ ] Helpful error messages
- [ ] Examples show real usage

## Troubleshooting Skill Generation

### Problem: User request is too vague

**Example:** "Make me a skill for React"

**Solution:**
Use AskUserQuestion to clarify:
- What aspect of React? (performance, patterns, testing)
- What should it enforce or guide?
- When should it activate?
- What's the primary goal?

### Problem: Skill type unclear

**Example:** "Create a skill for deployment"

**Solution:**
Determine if it's:
- Automation (Pattern D) - if scripted deployment
- Methodology (Pattern A) - if deployment process enforcement
- Reference (Pattern E) - if deployment best practices knowledge

Ask: "Should this automate deployment or guide the process?"

### Problem: Generated skill too long

**Cause:** Too much content in SKILL.md

**Solution:**
1. Keep SKILL.md under 500 lines
2. Move extensive content to reference/
3. Use progressive disclosure pattern
4. Link to reference files with clear descriptions

### Problem: Description doesn't trigger activation

**Cause:** Description too generic

**Solution:**
❌ Bad: "A skill for testing"
✅ Good: "Use when writing tests, implementing TDD, creating test suites, or when asked to 'test my code' or 'add test coverage'"

Include specific phrases users actually say.

### Problem: No clear examples

**Cause:** Skill too abstract

**Solution:**
Always include:
- At least 2 Good/Bad code comparisons
- Real-world scenarios
- Before/after examples
- Common use cases

## Integration Patterns

### Skill Chains

Some skills naturally call others:

```markdown
## Integration

**This skill (git-workflow):**
- Creates feature branch
- Guides development process

**Then activates:**
- test-driven-development - For implementation
- code-review - Before committing
- git-commit - For proper commit messages

**Pairs with:**
- git-worktree - For parallel features
```

### Skill Composition

Multiple skills working together:

```markdown
## Integration

**Works with:**
- react-best-practices - Performance checks
- web-design-guidelines - Accessibility audit
- security-audit - Vulnerability scanning

**Combined usage:**
All three skills active = comprehensive component review
```

## When NOT to Generate Skills

| User Request | Why Not | Alternative |
|--------------|---------|-------------|
| "Help me with React" | Too vague | Ask clarifying questions first |
| "Create a skill to fix bugs" | Too general | Use systematic-debugging skill |
| "Make a skill for everything" | Not focused | Create multiple focused skills |
| "Turn this 5000 line doc into skill" | Too large | Split into multiple skills with progressive disclosure |

## Meta: This Skill's Structure

This skill itself follows Pattern B (Technical Implementation):

- **Phase 1:** Discovery (questions to user)
- **Phase 2:** Pattern Selection (match type to structure)
- **Phase 3:** Content Generation (create SKILL.md)
- **Phase 4:** Enhancement (add complexity if needed)
- **Phase 5:** Scripts (if applicable)
- **Phase 6:** Finalization (quality check and output)

Each phase has verification checkboxes and clear completion criteria.

## References

- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [obra/superpowers](https://github.com/obra/superpowers)
- [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills)

**Official Resources:**
- [Agent Skills Specification](https://agentskills.io/specification)
- [Claude Code Documentation](https://code.claude.com/docs/)

## Integration

**This skill enables:**
- Custom skill creation for any workflow
- Capturing team processes as skills
- Extending Claude Code capabilities
- Documenting methodologies

**Pairs with:**
- Existing skills as examples
- Git workflows for versioning skills
- Team documentation processes

**Use this skill to create:**
- Methodology enforcement skills
- Technical automation skills
- Audit and validation skills
- Domain knowledge skills
- Tool integration skills
