---
name: writing-laws
description: Write formal laws and covenants for codebases using proper legal-style structure. Use when establishing inviolable standards, architectural constraints, or domain-specific rules that must be followed without exception.
---

# Writing Laws Skill

Use this skill when creating formal laws, covenants, or standards for a codebase. Laws are not suggestions or guidelines - they are inviolable requirements that govern behavior within a specific domain.

## Core Principle: Laws Define, They Do Not Persuade

Laws state what IS and what SHALL BE. They do not:
- Explain why (that belongs in preambles)
- Describe consequences (that belongs in severity classifications)
- Use conditional or hedging language
- Appeal to preference or opinion

## Law Structure

### Section Numbering

Laws use hierarchical section notation with the section symbol (§):

```
§ I      - Roman numerals for major laws
§ I.1    - Decimal for subsections
§ I.1.a  - Lowercase letters for sub-subsections
```

### Section Naming

Each section receives a bracketed name that serves as its short identifier:

```
§ VII [The Atom Suffix Convention]
§ VIII [The Confinement of Atoms]
§ XII [The Service Yield]
```

### Internal References

Reference other sections by their number and name:

```
As required by § III [The Export of the Live Layer], ...
This law supersedes § IV.2 when ...
See § IX [The Action Patterns] for related requirements.
```

## Legal Language

### Mandatory Modal Verbs

| Verb | Meaning | Usage |
|------|---------|-------|
| SHALL | Absolute requirement | `[Subject] SHALL [action].` |
| SHALL NOT | Absolute prohibition | `[Subject] SHALL NOT [action].` |
| MUST | Equivalent to SHALL | `[Subject] MUST [provide/include/satisfy].` |
| MUST NOT | Equivalent to SHALL NOT | `[Subject] MUST NOT [action].` |
| IS REQUIRED TO | Alternative to SHALL | `[Subject] IS REQUIRED TO [action].` |
| IS PROHIBITED FROM | Alternative to SHALL NOT | `[Subject] IS PROHIBITED FROM [action].` |
| IS HEREBY DECREED | Declarative establishment | `IT IS HEREBY DECREED that ...` |

### Definitional Language

| Phrase | Purpose |
|--------|---------|
| `[Term] means ...` | Define a term |
| `[Thing] is [classification]` | Classify something |
| `Any [X] that [condition]` | Define scope by condition |
| `For purposes of this section` | Limit scope of definition |
| `includes but is not limited to` | Non-exhaustive list |

### Classification Language

```
Any [thing] that [exhibits property] is [classified as] [category].
Any [action] that [meets criteria] constitutes [violation type].
```

## Law Templates

### Simple Prohibition Law

```markdown
## § X [Name]

**IT IS HEREBY DECREED** that [subject] SHALL NOT [prohibited action].

[Subject] that [exhibits prohibited behavior] constitutes a violation of this law.
```

### Simple Requirement Law

```markdown
## § X [Name]

**IT IS HEREBY DECREED** that [subject] SHALL [required action].

The [required element] MUST [satisfy condition]. [Additional requirements].
```

### Multi-Part Law

```markdown
## § X [Name]

**IT IS HEREBY DECREED** that [general principle].

### § X.1 [First Aspect]

[Subject] SHALL [requirement 1].

### § X.2 [Second Aspect]

[Subject] SHALL NOT [prohibition].

### § X.3 [Exception]

This law does not apply when [exception condition].
```

### Definition Law

```markdown
## § X [Definitions]

For purposes of these covenants:

**"[Term A]"** means [definition].

**"[Term B]"** includes:
- [item 1]
- [item 2]
- [item 3]

**"[Term C]"** does not include [exclusion].
```

## Document Structure

### Preamble

The preamble establishes WHY the laws exist. It uses WHEREAS clauses:

```markdown
## PREAMBLE

WHEREAS [foundational truth 1];

WHEREAS [foundational truth 2];

WHEREAS [problem being solved];

NOW THEREFORE, the following LAWS are hereby declared and SHALL govern [domain] in perpetuity.
```

### Laws Section

Laws follow the preamble. Each law stands alone as a complete requirement:

```markdown
## LAW I: [The Principle Name]

**IT IS HEREBY DECREED** that [core requirement].

[Elaboration of requirements, conditions, and constraints.]

```[language]
// Code example showing compliance
```

```[language]
// FORBIDDEN: Code example showing violation
```

### Severity Classification

After all laws, classify violation severity:

```markdown
## SEVERITY CLASSIFICATION

| Severity | Laws | Consequence |
|----------|------|-------------|
| CRITICAL | [Laws X, Y] | [Impact description] |
| MAJOR | [Laws A, B, C] | [Impact description] |
| MINOR | [Laws D, E] | [Impact description] |
```

### Compliance Checklist

Provide a verification checklist:

```markdown
## COMPLIANCE CHECKLIST

Before [artifact] is considered complete:

- [ ] **LAW I**: [Verification statement]
- [ ] **LAW II**: [Verification statement]
- [ ] **LAW III**: [Verification statement]
```

## Good Law Writing

### Characteristics

1. **Precise** - No ambiguity about what is required
2. **Complete** - All cases covered
3. **Testable** - Compliance can be objectively verified
4. **Self-contained** - Each law understandable without external context
5. **Imperative** - Commands, not suggestions

### Examples

**GOOD:**
```markdown
## § VII [The Atom Suffix Convention]

**IT IS HEREBY DECREED** that all atom properties SHALL bear the `$` suffix.

This convention provides immediate visual identification of reactive state.

```typescript
export interface SessionVM {
  readonly inputValue$: Atom.Atom<string>;    // $
  readonly history$: Atom.Atom<Prompt>;       // $
  readonly setInputValue: (value: string) => void;  // No $ - not an atom
}
```

**THE `$` SUFFIX** is the mark of reactivity. Its absence on an atom constitutes deception.
```

**BAD:**
```markdown
## Naming Things

You should probably use the $ suffix for atoms because it makes them easier to identify.
If you don't use it, other developers might get confused and that would be bad.
Consider using it when you remember to.
```

## What to Avoid

### Hedging Language

| Avoid | Use Instead |
|-------|-------------|
| should | SHALL |
| might | - (remove uncertainty) |
| probably | - (state definitively) |
| consider | IS REQUIRED TO |
| try to | SHALL |
| it's better to | SHALL |
| you might want to | IS REQUIRED TO |

### Consequence Descriptions in Laws

Laws define requirements. Consequences belong in severity classifications, not in the law itself.

**AVOID in law body:**
```markdown
If you violate this, bad things will happen and the codebase will become unmaintainable.
```

**ACCEPTABLE in severity section:**
```markdown
| CRITICAL | VIII, XII | Immediate remediation required. Untestable code. |
```

### Opinion and Preference

Laws do not express preference. They establish fact.

**AVOID:**
```markdown
I think it's better to use namespace imports because they're cleaner.
```

**USE:**
```markdown
[Subject] SHALL be imported as a namespace. Named imports are PROHIBITED.
```

### Conditional Requirements

If something is conditional, make the condition explicit and the requirement absolute:

**AVOID:**
```markdown
You might need to add spans if you want observability.
```

**USE:**
```markdown
All asynchronous actions SHALL be wrapped with `Effect.withSpan()`. No exceptions.
```

## Adding Laws to Existing Standards

When extending an existing covenant document:

### 1. Identify the Next Law Number

Review existing laws and use the next sequential Roman numeral.

### 2. Follow Established Patterns

Match the structure, language, and formatting of existing laws in the document.

### 3. Add to Severity Classification

Determine the appropriate severity for the new law and add it to the classification table.

### 4. Update Compliance Checklist

Add corresponding verification item(s) to the checklist.

### 5. Cross-Reference Related Laws

If the new law relates to existing laws, add cross-references in both directions.

## Example: Complete Mini-Covenant

```markdown
# THE IMPORT COVENANTS

## PREAMBLE

WHEREAS consistent import patterns reduce cognitive load;

WHEREAS namespace imports preserve type and value unity;

WHEREAS scattered named imports cause name collisions;

NOW THEREFORE, the following LAWS are hereby declared and SHALL govern all import statements.

---

## LAW I: The Namespace Requirement

**IT IS HEREBY DECREED** that all Effect module imports SHALL use the namespace pattern.

```typescript
// CORRECT
import * as Effect from "effect/Effect"
import * as Option from "effect/Option"

// FORBIDDEN
import { Effect, pipe } from "effect"
import { Option, none, some } from "effect/Option"
```

---

## LAW II: The Local Module Pattern

**IT IS HEREBY DECREED** that local domain modules SHALL be imported as namespaces.

```typescript
// CORRECT
import * as Task from "@/schemas/Task"
const task = Task.makePending({ ... })

// FORBIDDEN
import { makePending, isPending } from "@/schemas/Task"
```

---

## SEVERITY CLASSIFICATION

| Severity | Laws | Impact |
|----------|------|--------|
| MINOR | I, II | Inconsistency. Compounds over time. |

---

## COMPLIANCE CHECKLIST

- [ ] **LAW I**: All Effect imports use namespace pattern
- [ ] **LAW II**: All local domain imports use namespace pattern
```

## When to Use This Skill

- Establishing architectural constraints that must never be violated
- Codifying patterns that have proven essential to maintainability
- Creating domain-specific standards for new areas of the codebase
- Formalizing existing informal rules into enforceable covenants
- Extending existing covenant documents with new laws

## Key Principles Summary

1. Laws use SHALL/SHALL NOT - never suggestions
2. Definitions are precise - no ambiguity
3. Structure follows § section notation
4. Preambles explain why; laws state what
5. Consequences belong in severity tables, not law bodies
6. Every law is testable and verifiable
7. Code examples show both compliance and violation
8. Cross-reference related laws explicitly
9. Compliance checklists enable verification
10. Laws define - they do not persuade
