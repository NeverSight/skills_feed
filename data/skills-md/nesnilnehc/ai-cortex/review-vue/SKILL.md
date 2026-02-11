---
name: review-vue
description: Review Vue 3 code for Composition API, reactivity, components, state (Pinia), routing, and performance. Framework-only atomic skill; output is a findings list.
tags: [eng-standards]
related_skills: [review-diff, review-codebase, review-code]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
---

# Skill: Review Vue

## Purpose

Review **Vue 3** code for **framework conventions** only. Do not define scope (diff vs codebase) or perform security/architecture analysis; those are handled by scope and cognitive skills. Emit a **findings list** in the standard format for aggregation. Focus on Composition API and `<script setup>`, reactivity (ref/reactive, computed/watch), component boundaries and props/emits, state (Pinia/store), routing and guards, performance (e.g. v-memo), and accessibility where relevant.

---

## Use Cases

- **Orchestrated review**: Used as the framework step when [review-code](../review-code/SKILL.md) runs scope → language → framework → library → cognitive for Vue projects.
- **Vue-only review**: When the user wants only Vue/frontend framework conventions checked.
- **Pre-PR Vue checklist**: Ensure Composition API usage, reactivity, and component contracts are correct.

**When to use**: When the code under review is Vue 3 and the task includes framework quality. Scope is determined by the caller or user.

---

## Behavior

### Scope of this skill

- **Analyze**: Vue 3 framework conventions in the **given code scope** (files or diff provided by the caller). Do not decide scope; accept the code range as input.
- **Do not**: Perform scope selection, security review, or architecture review; do not review non-Vue files for Vue rules unless in scope (e.g. mixed repo).

### Review checklist (Vue framework only)

1. **Composition API and script setup**: Prefer `<script setup>` and Composition API; correct use of defineProps, defineEmits, defineExpose; lifecycle hooks (onMounted, onUnmounted, etc.).
2. **Reactivity**: Correct use of ref vs reactive; computed vs watch; avoid mutating props; deep reactivity and unwrapping in templates.
3. **Component boundaries**: Clear props/emits contracts; avoid prop drilling where a store or provide/inject is appropriate; single responsibility per component.
4. **State (Pinia/store)**: Appropriate use of Pinia (or Vuex) stores; avoid duplicating server state in multiple places; actions vs direct mutation.
5. **Routing and guards**: Vue Router usage; navigation guards and lazy loading; route params and query handling.
6. **Performance**: v-memo where list rendering is expensive; avoid unnecessary re-renders; key usage in lists.
7. **Accessibility**: Semantic HTML and ARIA where relevant; form labels and focus management.

### Tone and references

- **Professional and technical**: Reference specific locations (file:line or component name). Emit findings with Location, Category, Severity, Title, Description, Suggestion.

---

## Input & Output

### Input

- **Code scope**: Files or directories (or diff) containing Vue 3 code (.vue, .ts with Vue APIs). Provided by the user or scope skill.

### Output

- Emit zero or more **findings** in the format defined in **Appendix: Output contract**.
- Category for this skill is **framework-vue**.

---

## Restrictions

- **Do not** perform scope selection, security, or architecture review. Stay within Vue 3 framework conventions.
- **Do not** give conclusions without specific locations or actionable suggestions.
- **Do not** review non-Vue code for Vue-specific rules unless explicitly in scope.

---

## Self-Check

- [ ] Was only the Vue framework dimension reviewed (no scope/security/architecture)?
- [ ] Are Composition API, reactivity, components, state, routing, and performance covered where relevant?
- [ ] Is each finding emitted with Location, Category=framework-vue, Severity, Title, Description, and optional Suggestion?
- [ ] Are issues referenced with file:line or component?

---

## Examples

### Example 1: Mutating props

- **Input**: Component that assigns to a prop in script or template.
- **Expected**: Emit a finding (major/minor) for prop mutation; suggest local state or emit to parent. Category = framework-vue.

### Example 2: Missing key in v-for

- **Input**: v-for without :key or with non-stable key (e.g. index).
- **Expected**: Emit finding for list identity and performance; suggest stable unique key. Category = framework-vue.

### Edge case: Vue 2 Options API

- **Input**: Legacy Vue 2 Options API in a mixed codebase.
- **Expected**: Review for Vue 2 patterns (data, methods, lifecycle) if the skill is extended to Vue 2; otherwise note "Vue 3 Composition API preferred" where migration is feasible. For this skill, focus on Vue 3; note Vue 2 only if explicitly in scope.

---

## Appendix: Output contract

Each finding MUST follow the standard findings format:

| Element | Requirement |
| :--- | :--- |
| **Location** | `path/to/file.vue` or `.ts` (optional line or range). |
| **Category** | `framework-vue`. |
| **Severity** | `critical` \| `major` \| `minor` \| `suggestion`. |
| **Title** | Short one-line summary. |
| **Description** | 1–3 sentences. |
| **Suggestion** | Concrete fix or improvement (optional). |

Example:

```markdown
- **Location**: `src/components/UserList.vue:18`
- **Category**: framework-vue
- **Severity**: major
- **Title**: v-for missing stable key
- **Description**: Using index as key can cause incorrect reuse and state bugs when list order changes.
- **Suggestion**: Use a unique stable id (e.g. user.id) as :key.
```
