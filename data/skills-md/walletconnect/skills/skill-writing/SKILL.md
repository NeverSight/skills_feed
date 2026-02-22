---
name: skill-writing
description: Designs and writes high-quality Agent Skills (SKILL.md + optional reference files/scripts). Use when asked to create a new Skill, rewrite an existing Skill, improve Skill structure/metadata, or generate templates/evaluations for Skills.
---

# Skill Writing

## Goal
Produce a usable Skill package: **SKILL.md** (always) + optional **reference files** and **scripts** (when helpful). Optimize for: discoverability, correctness, concision, testability.

## Output contract
When triggered, deliver:
1) **SKILL.md** with valid YAML frontmatter (`name`, `description`)
2) If needed: suggested folder layout + filenames + brief contents for each extra file (do NOT bloat SKILL.md)
3) 3+ **evaluation prompts** to test activation + behavior

## Workflow (do in order)
### 1) Extract requirements
Capture (infer if missing):
- **Primary job**: what the Skill reliably accomplishes
- **Triggers**: phrases/users requests that should activate it
- **Inputs**: files/types/tools needed (pdf/docx/xlsx/pptx, repos, APIs, etc.)
- **Constraints**: tone, formatting, compliance, latency, determinism
- **Failure modes**: common mistakes to guardrail

### 2) Design information architecture
Use progressive disclosure:
- Keep **SKILL.md short** (prefer <300 lines)
- Push long content into one-level-deep files:
  - `REFERENCE.md` (APIs/schemas)
  - `WORKFLOWS.md` (multi-step procedures)
  - `EXAMPLES.md` (I/O pairs)
  - `CHECKLISTS.md` (validation rubrics)
- Prefer **scripts** for deterministic transforms/validation; document how to run them.

### 3) Write frontmatter (strict)
- `name`: lowercase letters/numbers/hyphens only; <=64 chars; no reserved words
- `description`: 3rd-person; states *what* + *when to use*; <=1024 chars; non-empty

### 4) Write SKILL.md body (minimum necessary)
Include only what improves success:
- **Goal**
- **When to use / When not to use**
- **Default approach** (1 best path)
- **Decision points** (few, explicit)
- **Templates** (copy/pasteable)
- **Validation loop** (draft → check → fix → finalize)
- **Examples** (at least 2)

### 5) Add evaluations
Create at least 3 tests:
- **Activation test** (should trigger)
- **Non-activation test** (should not trigger)
- **Edge case** (most likely failure mode)

## Templates

### Frontmatter template
```yaml
---
name: <lowercase-hyphen-name>
description: <does X. Use when Y.>
---
````

### SKILL.md skeleton (recommended)

```markdown
# <Skill Title>

## Goal
...

## When to use
- ...
## When not to use
- ...

## Inputs
- ...
## Outputs
- ...

## Default workflow
1) ...
2) ...
3) ...

## Validation checklist
- [ ] ...
- [ ] ...

## Examples
### Example 1
Input: ...
Output: ...
```

### “High-level + references” pattern

In SKILL.md, link (one level deep):

* `REFERENCE.md` for details
* `WORKFLOWS.md` for complex steps
* `EXAMPLES.md` for many examples
  Avoid SKILL.md → advanced.md → details.md chains.

## Writing rules (hard)

* One primary approach; alternatives only as fallback
* No time-sensitive branching (“before/after date”); instead: “Current method” + “Legacy (deprecated)” section
* Consistent terminology (pick one term per concept)
* No Windows paths; use forward slashes
* If scripts exist: specify exact commands + expected outputs
* Always include a validator/checklist step for fragile tasks

## Common anti-patterns

* Vague description (“helps with documents”)
* Too many options (“use A/B/C/D…”)
* Long tutorials Claude already knows
* Deeply nested references
* “Just figure it out” steps without verification

## Evaluation pack (copy/paste)

Write 3+ prompts like:

1. “Create a Skill that … (include triggers + constraints). Return SKILL.md.”
2. “User asks for adjacent task that should NOT trigger; respond normally.”
3. “Edge case: missing inputs or conflicting constraints; infer defaults and still produce SKILL.md.”

## Done criteria

* Frontmatter validates
* SKILL.md under 500 lines
* Clear activation triggers in description + “When to use”
* Includes checklist + examples + evaluations


