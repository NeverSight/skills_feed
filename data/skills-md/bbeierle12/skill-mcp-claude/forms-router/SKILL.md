---
name: forms-router
description: Router for web form development. Use when creating forms, handling validation, user input, or data entry across React, Vue, or vanilla JavaScript. Routes to 7 specialized skills for accessibility, validation, security, UX patterns, and framework-specific implementations. Start here for form projects.
---

# Forms Router

Routes to 7 specialized skills based on task requirements.

## Routing Protocol

1. **Classify** — Identify framework + form type
2. **Match** — Apply signal matching rules below
3. **Combine** — Production forms need 3-4 skills minimum
4. **Load** — Read matched SKILL.md files before coding

## Quick Route

### Tier 1: Core (Always Include)
| Need | Skill | Signals |
|------|-------|---------|
| WCAG compliance, ARIA | `form-accessibility` | accessible, ARIA, screen reader, keyboard, focus, a11y |
| Zod schemas, timing | `form-validation` | validate, Zod, schema, error, required, pattern |
| Autocomplete, CSRF, XSS | `form-security` | autocomplete, password manager, CSRF, XSS, sanitize |

### Tier 2: Framework
| Need | Skill | Signals |
|------|-------|---------|
| React Hook Form / TanStack | `form-react` | React, useForm, RHF, TanStack, formState |
| VeeValidate / Vuelidate | `form-vue` | Vue, VeeValidate, Vuelidate, v-model |
| No framework | `form-vanilla` | vanilla, plain JS, native, constraint validation |

### Tier 3: Enhanced UX
| Need | Skill | Signals |
|------|-------|---------|
| Wizards, chunking, conditionals | `form-ux-patterns` | multi-step, wizard, progressive, conditional, stepper |

## Signal Priority

When multiple signals present:
1. **Framework explicit** — React/Vue/vanilla determines Tier 2 choice
2. **Auth context** — Login/registration triggers `form-security` priority
3. **Complexity** — Wizard/multi-step triggers `form-ux-patterns`
4. **Default** — Always include all Tier 1 skills

## Common Combinations

### Standard Production Form (4 skills)
```
form-accessibility → WCAG, ARIA binding
form-validation → Zod schemas, timing
form-react → RHF integration
form-security → autocomplete attributes
```

### Secure Auth Form (4 skills)
```
form-security → autocomplete, CSRF (priority)
form-accessibility → focus, error announcements
form-validation → auth schema
form-react → controlled submission
```

### Multi-Step Wizard (4 skills)
```
form-ux-patterns → chunking, navigation
form-validation → per-step validation
form-accessibility → focus on step change
form-react → FormProvider context
```

### Framework-Free Form (3 skills)
```
form-vanilla → Constraint Validation API
form-accessibility → manual ARIA
form-security → autocomplete
```

## Decision Table

| Framework | Form Type | Skills |
|-----------|-----------|--------|
| React | Standard | accessibility + validation + security + react |
| React | Auth | security + accessibility + validation + react |
| React | Wizard | ux-patterns + validation + accessibility + react |
| Vue | Standard | accessibility + validation + security + vue |
| Vue | Complex | accessibility + validation + ux-patterns + vue |
| None | Any | vanilla + accessibility + security |

## Core Principles (All Skills)

**Schema-first**: Define Zod schema → infer TypeScript types  
**Timing**: Reward early (✓ on valid), punish late (✗ on blur only)  
**Autocomplete**: Never optional for auth forms  
**Chunking**: Max 5-7 fields per logical group

## Fallback

- **No framework stated** → Ask: "React, Vue, or vanilla JS?"
- **Ambiguous complexity** → Start with Tier 1 + framework skill
- **Missing context** → Default to `form-react` (most common)

## Reference

See `references/integration-guide.md` for complete wiring patterns and code examples.
