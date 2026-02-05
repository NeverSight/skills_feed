---
name: skill-authoring
description: Guide for creating Claude Code skills to document @rytass packages (建立套件文件 skill 指南). Use when creating new package documentation skills, writing SKILL.md files, or designing skill structure.
---

# Package Documentation Skill Authoring Guide

This skill documents the methodology for creating Claude Code skills that document `@rytass/*` packages.

## Overview

When creating skills for package documentation, follow this structured approach:

1. **Explore** - Understand the package structure
2. **Plan** - Design the skill architecture
3. **Implement** - Write the skill files
4. **Refine** - Add bilingual triggers and optimize

---

## Phase 1: Exploration

### 1.1 Identify Package Scope

Determine which packages to document:

```
packages/{category}-*          # e.g., invoice-*, payments-*, storages-*
```

Questions to answer:
- Is there a base package defining interfaces? (e.g., `@rytass/invoice`)
- How many adapter implementations exist?
- What is the relationship between packages?

### 1.2 Analyze Package Exports

For each package, identify:

| Category | What to Document |
|----------|------------------|
| **Classes** | Gateway, Entity, Allowance classes |
| **Interfaces** | Core interfaces and their properties |
| **Enums** | All enum values with descriptions |
| **Types** | Type aliases and union types |
| **Functions** | Utility functions with signatures |
| **Constants** | Exported constants and helpers |

### 1.3 Understand Usage Patterns

Identify common operations:
- Initialization / configuration
- CRUD operations (create, read, update, delete)
- Validation methods
- Error handling patterns

---

## Phase 2: Planning

### 2.1 Determine Skill Structure

**Single Skill** - For simple packages with limited scope
```
.claude/skills/{package-name}/
└── SKILL.md
```

**Multi-File Skill** - For complex packages (recommended for adapters)
```
.claude/skills/{package-name}/
├── SKILL.md              # Overview, quick start, comparison
├── {PROVIDER-1}.md       # Detailed reference
├── {PROVIDER-2}.md       # Detailed reference
└── ...
```

**Dual Skill** - When separating user vs developer concerns
```
.claude/skills/{package}-adapters/     # User-facing
.claude/skills/{package}-development/  # Developer-facing
```

### 2.2 Content Architecture

**SKILL.md (Main File)** - Keep under 500 lines

| Section | Purpose |
|---------|---------|
| Overview | What the packages do, unified interface |
| Installation | npm install commands |
| Quick Start | Minimal working examples |
| Feature Comparison | Table comparing providers |
| Detailed Docs Links | Links to reference files |

**Reference Files** - One per provider/component

| Section | Purpose |
|---------|---------|
| Constructor | Parameters and initialization |
| Methods | All public methods with signatures |
| Classes | Entity and value object classes |
| Types | Provider-specific type definitions |
| Complete Example | Full working code sample |

### 2.3 Progressive Disclosure Pattern

```
SKILL.md (loaded first)
    │
    ├── Quick overview (always visible)
    ├── Common operations
    └── Links to details
            │
            └── PROVIDER.md (loaded on demand)
                    │
                    └── Full API reference
```

Benefits:
- Reduces initial context load
- Users get relevant detail only when needed
- Keeps main file scannable

---

## Phase 3: Implementation

### 3.1 YAML Frontmatter

```yaml
---
name: package-name
description: Brief description with trigger words in English (中文觸發詞). Maximum 1024 characters.
---
```

**Name Rules:**
- Lowercase letters, numbers, hyphens only
- Maximum 64 characters
- Should match directory name

**Description Best Practices:**
- Include both English and Chinese trigger words
- Format: `English term (中文)` for key concepts
- Cover primary use cases
- Include provider names if applicable

### 3.2 Description Template

```
{What it does} ({中文說明}). Use when {use case 1}, {use case 2 (中文)}.
Covers {topic 1} ({中文}), {topic 2} ({中文}).
```

**Example:**
```
Taiwan e-invoice integration (台灣電子發票整合). Use when working with
ECPay (綠界), EZPay (藍新). Covers issuing invoices (開立發票),
voiding (作廢), allowances (折讓).
```

### 3.3 Markdown Structure

**Overview Section:**
```markdown
# Package Name

Brief description of the package family.

## Overview

| Package | Provider | Description |
|---------|----------|-------------|
| `@rytass/pkg-adapter-a` | Provider A (中文名) | Brief desc |
| `@rytass/pkg-adapter-b` | Provider B (中文名) | Brief desc |
```

**Installation Section:**
```markdown
## Installation

\`\`\`bash
npm install @rytass/package-name
\`\`\`
```

**Quick Start Section:**
```markdown
## Quick Start

### Provider A

\`\`\`typescript
import { ProviderAGateway } from '@rytass/pkg-adapter-a';

const gateway = new ProviderAGateway({
  // configuration
});

// Basic operation
const result = await gateway.operation({
  // parameters
});
\`\`\`
```

**Method Documentation:**
```markdown
#### `methodName(options: OptionsType): Promise<ReturnType>`

Brief description.

**Parameters:**

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `param1` | `string` | Yes | Description |
| `param2` | `number` | No | Description (default: value) |

**Returns:** `Promise<ReturnType>`

**Example:**

\`\`\`typescript
const result = await gateway.methodName({
  param1: 'value',
});
\`\`\`
```

---

## Phase 4: Refinement

### 4.1 Bilingual Trigger Words

Add Chinese keywords for Taiwan users:

| English | 中文 |
|---------|------|
| invoice | 發票、電子發票 |
| issue | 開立 |
| void | 作廢 |
| allowance | 折讓 |
| payment | 付款、支付 |
| storage | 儲存、存儲 |

### 4.2 Feature Comparison Tables

Always include a comparison table for multi-provider skills:

```markdown
| Feature | Provider A | Provider B | Provider C |
|---------|:----------:|:----------:|:----------:|
| Feature 1 | Yes | Yes | No |
| Feature 2 | Yes | No | Yes |
```

Use `:-----:` for centered alignment with checkmarks.

### 4.3 Complete Examples

Every reference file should end with a complete, runnable example:

```markdown
## Complete Example

\`\`\`typescript
import { Gateway, Type1, Type2 } from '@rytass/package';

async function main() {
  // 1. Initialize
  const gateway = new Gateway({ /* config */ });

  // 2. Create
  const entity = await gateway.create({ /* options */ });

  // 3. Query
  const found = await gateway.query({ /* options */ });

  // 4. Update/Modify
  const updated = await gateway.modify(entity, { /* options */ });

  // 5. Delete/Void
  await gateway.delete(entity);
}

main().catch(console.error);
\`\`\`
```

---

## Checklist

Before finalizing a skill:

- [ ] YAML frontmatter starts on line 1 (no blank lines before)
- [ ] `name` is lowercase with hyphens only
- [ ] `description` includes Chinese trigger words
- [ ] `description` is under 1024 characters
- [ ] SKILL.md is under 500 lines
- [ ] All public methods documented
- [ ] All types and enums documented
- [ ] Installation instructions included
- [ ] Quick start examples work
- [ ] Feature comparison table included (if multi-provider)
- [ ] Complete example at end of each reference file
- [ ] Links to reference files use relative paths

---

## Example: Invoice Skills Structure

Reference implementation from `invoice-adapters` and `invoice-development`:

```
.claude/skills/
├── invoice-adapters/           # User-facing skill
│   ├── SKILL.md               # Overview, quick start, comparison
│   ├── ECPAY.md               # ECPay full reference
│   ├── EZPAY.md               # EZPay full reference
│   ├── BANK-PRO.md            # BankPro full reference
│   └── AMEGO.md               # Amego full reference
│
└── invoice-development/        # Developer-facing skill
    ├── SKILL.md               # Base package overview
    ├── BASE-INTERFACES.md     # Interface specifications
    └── CREATE-ADAPTER.md      # How to create new adapter
```

**Key decisions made:**
1. Split into user vs developer skills
2. One reference file per provider
3. Progressive disclosure for detailed API
4. Chinese keywords in description for Taiwan users
