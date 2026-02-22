---
name: skill-creator
description: Guide for creating effective agent skills following the Agent Skills open standard. This skill should be used when users want to create a new skill (or update an existing skill) that extends agent capabilities with specialized knowledge, workflows, or tool integrations.
argument-hint: "[domain or topic]"
---

# Skill Authoring

Create agent skills (SKILL.md files) following the [Agent Skills open standard](https://agentskills.io). Skills produce consistent, deterministic agent behavior across any compatible platform. Skills are filesystem-based instruction sets that transform an agent into a domain specialist.

When invoked with arguments, create a skill for: $ARGUMENTS

## Workflow

1. **Define scope**: Identify the domain, target tasks, and activation triggers
2. **Gather requirements**: Collect domain knowledge, constraints, expected inputs/outputs, and success criteria. Ask clarifying questions for missing context
3. **Determine freedom levels**: Classify each instruction as high/medium/low freedom based on task sensitivity
4. **Write frontmatter**: Name, description with activation triggers
5. **Write instructions**: Imperative commands, structured for LLM parsing
6. **Add examples**: Concrete input/output pairs for ambiguous or complex behaviors
7. **Add supporting files**: Move detailed reference material to separate files when SKILL.md approaches 300 lines
8. **Verify**: Run through the checklist below

## SKILL.md Structure

Every skill requires a `SKILL.md` file in a named directory:

```
skill-name/
├── SKILL.md              # Required. Main instructions (under 500 lines)
├── references/           # Optional. Deep-dive material
│   └── *.md              # One level deep only
├── scripts/              # Optional. Executable utilities
│   └── *.py|*.sh
└── assets/               # Optional. Templates, schemas, static resources
```

## Frontmatter

YAML frontmatter between `---` markers. The open standard requires `name` and `description`.

```yaml
---
name: kebab-case-name
description: What this skill does. Use when (1) trigger one, (2) trigger two, (3) trigger three, (4) trigger four, or (5) trigger five.
---
```

### Name (required)

**Must match the parent directory name.** Lowercase letters, numbers, hyphens only. Maximum 64 characters. Must not start or end with a hyphen. Must not contain consecutive hyphens (`--`).

### Description (required)

Maximum 1024 characters. Write in third person. Include both what the skill does AND when to activate.

**Template**: `[Value proposition sentence]. Use when (1) [trigger], (2) [trigger], ... (N) [trigger].`

Enumerate 4-6 specific activation triggers. Base triggers on user intent and tasks, not file types.

### Optional Universal Fields

| Field | Constraints |
|-------|-------------|
| `license` | License name or reference to a bundled license file. Include when sharing or publishing. |
| `compatibility` | Max 500 chars. Declare environment requirements (required tools, network access, intended platform). |
| `metadata` | Arbitrary key-value map. Use reasonably unique key names to avoid conflicts. |
| `allowed-tools` | Space-delimited list of pre-approved tools. Experimental; support varies across platforms. |

For platform-specific extensions (Claude Code's `argument-hint`, `context`, `agent`, `disable-model-invocation`, `user-invocable`, `model`, `hooks`), see [references/frontmatter.md](references/frontmatter.md).

## Writing Instructions

### Core Principles

The context window is a shared resource. Only add context the model lacks. Assume high baseline capability.

**Imperative language only.** "Validate input at boundaries" not "You should consider validating input."

**Zero ambiguity.** Every instruction must have exactly one interpretation. Eliminate hedge words: "consider", "try to", "when possible", "generally".

**Specificity scales with risk.** Use high freedom (text instructions) when multiple approaches are valid. Use low freedom (exact commands, scripts) when consistency is critical.

### Formatting for LLM Parsing

| Format | Use For |
|--------|---------|
| **Headings** | Scope and context boundaries |
| **Tables** | Structured comparisons, reference data, decision matrices |
| **Lists** | Discrete, parallel, independent items |
| **Prose** | Relationships between ideas, conditional logic, rationale |
| **Code blocks** | Exact commands, templates, output formats (always language-labeled) |
| **Bold** | Hard constraints where violation causes failure (max 10% of content) |
| **Blockquotes** | Key insights, breaking changes, critical warnings |

### Emphasis Modifiers

Use MUST, MUST NOT, REQUIRED only for hard constraints where violation causes failure. If every instruction uses MUST, none stand out. Reserve bold for the same purpose.

### Terminology Consistency

Choose one term per concept. Use it throughout the entire skill. Do not alternate between synonyms.

### Progressive Disclosure

Keep SKILL.md body under 500 lines. Start with core instructions. Link to separate files for deep-dive material.

**Pattern**: High-level guide in SKILL.md with `[reference.md](reference.md)` links for specialized content.

Keep all references one level deep from SKILL.md. Do not chain: `SKILL.md -> advanced.md -> details.md`.

Reference files longer than 100 lines include a table of contents at the top.

## Instruction Patterns

### Workflow Pattern

Use for procedural, multi-step tasks. Numbered steps with clear sequencing.

```markdown
## Workflow
1. Detect framework from `package.json`
2. Select base image from Image Guide table
3. Generate Dockerfile using selected pattern
4. Create `.dockerignore` if missing
5. Validate with checklist
```

### Decision Table Pattern

Use for selection logic with discrete options.

```markdown
| Condition | Action |
|-----------|--------|
| API endpoint | Validate input schema, return JSON |
| Background job | Log start/end, handle timeout |
| CLI command | Parse args with yargs, exit codes 0/1 |
```

### Template Pattern

Use when output must follow an exact structure.

````markdown
Output format:

```markdown
## [Title]
### Summary
[2-3 sentence overview]
### Findings
| Finding | Severity | Recommendation |
|---------|----------|----------------|
```
````

### Conditional Workflow Pattern

Use when the workflow branches based on input.

```markdown
1. Determine modification type:
   **Creating new?** -> Follow Creation workflow
   **Editing existing?** -> Follow Editing workflow
```

### Examples Pattern

Use input/output pairs to demonstrate expected behavior. Wrap in `<example>` tags for complex cases.

````markdown
<example>
Input: User requests API endpoint for user registration
Output:
```typescript
// POST /api/users
export async function handler(req: Request) {
  const body = await req.json()
  // validate, create user, return 201
}
```
</example>
````

For additional patterns (feedback loops, checklist tracking, dynamic context), see [references/patterns.md](references/patterns.md).

## Content Guidelines

### What to Include

- Domain-specific knowledge the model lacks
- Exact commands with all flags and arguments
- Concrete examples demonstrating desired output format
- Decision tables for selection logic
- Verification steps for critical operations
- Constraints and prohibited actions

### What to Exclude

- Information the model already knows (framework basics, language syntax)
- Decorative language ("please", "remember", "it's important")
- Welcome messages, motivational text, background history
- Time-sensitive information ("Before August 2025, use...")
- Hypothetical scenarios ("If we ever migrate to...")
- Vague best practices ("Functions should be small")

### Reducing Hallucination Risk

When a skill processes external documents or data:
- Instruct to extract direct quotes before analyzing
- Require citations for claims
- Include explicit fallback: "If information is unavailable, state 'Insufficient data' instead of inferring"
- Restrict to provided context when accuracy is critical

For comprehensive anti-patterns reference, see [references/anti-patterns.md](references/anti-patterns.md).

## Platform Extensions

The open standard defines the universal format above. Individual platforms add extensions for deeper integration. Use universal fields by default; add platform extensions only when the extra capability is needed.

### Claude Code Extensions

Skills double as slash commands in Claude Code. Support argument passing with `$ARGUMENTS`.

```yaml
---
name: review-pr
description: Review a pull request for code quality and standards
argument-hint: "[PR number or URL]"
---
Review pull request $ARGUMENTS.
1. Fetch PR diff
2. Check against coding standards
3. Report findings
```

Positional arguments: `$0`, `$1`, `$2` or `$ARGUMENTS[0]`, `$ARGUMENTS[1]`.

Dynamic context injection runs shell commands and inserts output before the model sees the content. Prefix a backtick-wrapped command with the bang character (the exclamation mark).

For complete syntax reference and a working example, see [references/frontmatter.md](references/frontmatter.md#string-substitutions).

Other platforms may define their own extensions. Consult the target platform's documentation for available fields.

For the complete Claude Code extension reference, see [references/frontmatter.md](references/frontmatter.md).

## Verification Checklist

Run through before finalizing any skill.

### Frontmatter (Universal)
- [ ] `name` is kebab-case, under 64 characters, matches parent directory name
- [ ] `name` does not start/end with hyphen, no consecutive hyphens
- [ ] `description` is non-empty, under 1024 characters, third person
- [ ] Description includes what the skill does AND 4-6 activation triggers
- [ ] `license` field present if skill will be shared or published
- [ ] `compatibility` field present if skill requires specific environment

### Frontmatter (Platform-Specific)
- [ ] `argument-hint` present if skill accepts slash command arguments (Claude Code)
- [ ] Platform-specific fields only used when universal fields are insufficient

### Instructions
- [ ] All instructions use imperative mood
- [ ] No hedge words (consider, try to, when possible, generally)
- [ ] No decorative language (please, remember, make sure)
- [ ] Zero ambiguity: each instruction has exactly one interpretation
- [ ] Emphasis modifiers (MUST, bold) reserved for hard constraints only
- [ ] Consistent terminology: one term per concept throughout
- [ ] Code blocks are language-labeled

### Structure
- [ ] SKILL.md body under 500 lines
- [ ] Sections follow: Title -> Overview -> Workflow/Principles -> Detail -> Examples -> Checklist
- [ ] Tables used for structured data, lists for discrete items, prose for relationships
- [ ] Supporting files one level deep from SKILL.md
- [ ] Reference files over 100 lines have a table of contents

### Content
- [ ] Only adds context the model lacks
- [ ] No framework documentation the model already knows
- [ ] No time-sensitive information
- [ ] Examples are concrete input/output pairs, not abstract descriptions
- [ ] Output format explicitly defined when consistency matters
- [ ] Verification/validation steps included for critical operations

### Execution
- [ ] Produces consistent behavior across multiple runs
- [ ] Includes clear invocation conditions (when to use AND when NOT to use)
- [ ] Specifies expected inputs, outputs, and validation criteria
- [ ] Freedom levels match task sensitivity (high freedom for creative tasks, low for critical operations)
