---
name: rule-creator
description: Creates rule files for the Claude Code framework. Rules are markdown files in .claude/rules/ that are auto-loaded by Claude Code.
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit]
args: '--name <rule-name> --content <rule-content> [--category <category>]'
best_practices:
  - Rules are concise guidelines (not detailed workflows)
  - Use markdown formatting for clarity
  - Group related rules into sections
  - Keep rules under 50 lines unless detailed guidance needed
error_handling: graceful
streaming: supported
output_location: .claude/rules/
verified: false
lastVerifiedAt: 2026-02-19T05:29:09.098Z
---

# Rule Creator

Create rule files in `.claude/rules/`. Rules are auto-discovered by Claude Code and loaded into agent context.

## Step 0: Check for Existing Rule

Before creating, check if rule already exists:

```bash
test -f .claude/rules/<rule-name>.md && echo "EXISTS" || echo "NEW"
```

If EXISTS → invoke `Skill({ skill: "artifact-updater", args: "--type rule --path .claude/rules/<rule-name>.md --changes '...'" })`

If NEW → continue with Step 0.5.

## Step 0.5: Companion Check

Before proceeding with creation, run the ecosystem companion check:

1. Use `companion-check.cjs` from `.claude/lib/creators/companion-check.cjs`
2. Call `checkCompanions("rule", "{rule-name}")` to identify companion artifacts
3. Review the companion checklist — note which required/recommended companions are missing
4. Plan to create or verify missing companions after this artifact is complete
5. Include companion findings in post-creation integration notes

This step is **informational** (does not block creation) but ensures the full artifact ecosystem is considered.

## When to Use

- Creating project-specific coding guidelines
- Documenting framework conventions
- Establishing team standards
- Defining workflow protocols

## Rule File Format

Rules are simple markdown files:

```markdown
# Rule Name

## Section 1

- Guideline 1
- Guideline 2

## Section 2

- Guideline 3
- Guideline 4
```

**Example: testing.md**

```markdown
# Testing

## Test-Driven Development

- Use TDD for new features and bug fixes (Red-Green-Refactor cycle)
- Write failing test first, then minimal code to pass, then refactor
- Never write production code without a failing test first

## Test Organization

- Add unit tests for utilities and business logic
- Add integration tests for API boundaries
- Keep tests deterministic and isolated (no shared state)
- Place test files in `tests/` directory mirroring source structure
```

## Creation Workflow

### Step 1: Validate Inputs

```javascript
// Validate rule name (lowercase, hyphens only)
const ruleName = args.name.toLowerCase().replace(/[^a-z0-9-]/g, '-');

// Validate content is not empty
if (!args.content || args.content.trim().length === 0) {
  throw new Error('Rule content cannot be empty');
}
```

### Step 2: Create Rule File

```javascript
const rulePath = `.claude/rules/${ruleName}.md`;

// Format content as markdown
const content = args.content.startsWith('#')
  ? args.content
  : `# ${ruleName.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}\n\n${args.content}`;

await writeFile(rulePath, content);
```

### Step 3: Verify Auto-Discovery

Rules in `.claude/rules/` are automatically loaded by Claude Code. No manual registration needed.

```javascript
// Verify file was created
const fileExists = await exists(rulePath);
if (!fileExists) {
  throw new Error('Rule file creation failed');
}
```

### Step 4: Run Post-Creation Integration

```javascript
const {
  runIntegrationChecklist,
  queueCrossCreatorReview,
} = require('.claude/lib/creator-commons.cjs');

await runIntegrationChecklist('rule', rulePath);
await queueCrossCreatorReview('rule', rulePath, {
  artifactName: ruleName,
  createdBy: 'rule-creator',
});
```

## Post-Creation Integration

After rule creation, run integration checklist:

```javascript
const {
  runIntegrationChecklist,
  queueCrossCreatorReview,
} = require('.claude/lib/creator-commons.cjs');

// 1. Run integration checklist
const result = await runIntegrationChecklist('rule', '.claude/rules/<rule-name>.md');

// 2. Queue cross-creator review
await queueCrossCreatorReview('rule', '.claude/rules/<rule-name>.md', {
  artifactName: '<rule-name>',
  createdBy: 'rule-creator',
});

// 3. Review impact report
// Check result.mustHave for failures - address before marking complete
```

**Integration verification:**

- [ ] Rule file created in `.claude/rules/`
- [ ] Rule is auto-discovered by Claude Code
- [ ] Rule content is clear and actionable
- [ ] No conflicts with existing rules

## Usage Examples

### Create Code Standards Rule

```javascript
Skill({
  skill: 'rule-creator',
  args: `--name code-standards --content "# Code Standards

## Organization
- Prefer small, cohesive files over large ones
- Keep interfaces narrow; separate concerns by feature

## Style
- Favor immutability; avoid in-place mutation
- Validate inputs and handle errors explicitly"`,
});
```

### Create Git Workflow Rule

```javascript
Skill({
  skill: 'rule-creator',
  args: `--name git-workflow --content "# Git Workflow

## Commit Guidelines
- Keep changes scoped and reviewable
- Use conventional commits: feat:, fix:, refactor:, docs:, chore:

## Branch Workflow
- Create feature branches from main
- Never force-push to main/master"`,
});
```

## Related Skills

- `artifact-updater` - Update existing rules
- `skill-creator` - Create detailed workflows (for complex guidance)

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New rule pattern → `.claude/context/memory/learnings.md`
- Rule creation issue → `.claude/context/memory/issues.md`
- Guideline decision → `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.

## Ecosystem Alignment Contract (MANDATORY)

This creator skill is part of a coordinated creator ecosystem. Any artifact created here must align with and validate against related creators:

- `agent-creator` for ownership and execution paths
- `skill-creator` for capability packaging and assignment
- `tool-creator` for executable automation surfaces
- `hook-creator` for enforcement and guardrails
- `rule-creator` and `semgrep-rule-creator` for policy and static checks
- `template-creator` for standardized scaffolds
- `workflow-creator` for orchestration and phase gating
- `command-creator` for user/operator command UX

### Cross-Creator Handshake (Required)

Before completion, verify all relevant handshakes:

1. Artifact route exists in `.claude/CLAUDE.md` and related routing docs.
2. Discovery/registry entries are updated (catalog/index/registry as applicable).
3. Companion artifacts are created or explicitly waived with reason.
4. `validate-integration.cjs` passes for the created artifact.
5. Skill index is regenerated when skill metadata changes.

### Research Gate (Exa First, arXiv Fallback)

For new patterns, templates, or workflows, research is mandatory:

1. Use Exa first for implementation and ecosystem patterns.
2. If Exa is insufficient, use `WebFetch` plus arXiv references.
3. Record decisions, constraints, and non-goals in artifact references/docs.
4. Keep updates minimal and avoid overengineering.

### Regression-Safe Delivery

- Follow strict RED -> GREEN -> REFACTOR for behavior changes.
- Run targeted tests for changed modules.
- Run lint/format on changed files.
- Keep commits scoped by concern (logic/docs/generated artifacts).
