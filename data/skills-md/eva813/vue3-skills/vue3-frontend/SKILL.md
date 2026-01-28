---
name: vue3-frontend
description: "Comprehensive Vue 3 frontend development skill. Use when developing Vue 3 applications, components, or composables. Covers: (1) Creating new Vue 3 projects and components, (2) Vue 2 to Vue 3 migration, (3) Code review and optimization, (4) Composition API implementation, (5) Best practices and common patterns, (6) TypeScript integration, (7) State management with Pinia, (8) Performance optimization. Includes component templates, composable examples, migration guides, and best practices documentation."
---

# Vue 3 Frontend Development Skill

全面的 Vue 3 前端開發技能,提供元件範本、最佳實踐指南、遷移協助和常見模式。

## Core Capabilities

### 1. Component Development
建立新的 Vue 3 元件,使用 `<script setup>` 語法和 Composition API。

**Available templates:**
- `assets/component-templates/BasicComponent.vue` - 基本元件範本
- `assets/component-templates/FormComponent.vue` - 完整的表單元件(含驗證)
- `assets/component-templates/DataTable.vue` - 資料表格元件(含排序、分頁、搜尋)
- `assets/component-templates/Modal.vue` - 模態框元件(含完整功能)

**Usage:**
```bash
# 複製範本到專案
cp assets/component-templates/BasicComponent.vue src/components/YourComponent.vue
```

### 2. Composables Development
建立可重用的邏輯抽象。

**Available templates:**
- `assets/composable-templates/useFetch.js` - API 請求封裝
- `assets/composable-templates/useLocalStorage.js` - localStorage 同步狀態

**Usage:**
```bash
# 複製到專案
cp assets/composable-templates/useFetch.js src/composables/
```

### 3. Vue 2 to Vue 3 Migration
協助將 Vue 2 專案遷移到 Vue 3。

**Migration workflow:**
1. Read `references/migration-guide.md` for breaking changes
2. Identify deprecated APIs in existing code
3. Apply migration patterns from the guide
4. Test thoroughly

**Key migration areas:**
- Global API (Vue.use → app.use)
- Reactivity system (Vue.set → direct assignment)
- v-model syntax (value/input → modelValue/update:modelValue)
- Lifecycle hooks (destroyed → unmounted)
- Filters removal (use computed/methods)
- Event Bus replacement (use mitt/Pinia)

### 4. Code Review and Optimization
檢查和優化 Vue 3 程式碼品質。

**Review checklist:**
- Use `<script setup>` for better performance
- Proper ref/reactive usage
- Computed vs methods
- v-show vs v-if
- Key usage in v-for
- Component splitting
- Props validation
- Error handling

## Reference Documentation

### Essential References
Always read these when working on specific tasks:

**Migration tasks:**
- `references/migration-guide.md` - Complete Vue 2 to Vue 3 migration guide with all breaking changes

**Composition API usage:**
- `references/composition-api.md` - Comprehensive Composition API reference (ref, reactive, computed, watch, lifecycle, etc.)

**Best practices:**
- `references/best-practices.md` - Vue 3 best practices covering component design, reactivity, performance, code organization, error handling, TypeScript

**Common patterns:**
- `references/common-patterns.md` - Form handling, data fetching, list rendering, modals, state management, routing, i18n

### When to Read Each Reference

**Before writing any component:**
1. Check `best-practices.md` for component design patterns
2. Review relevant patterns in `common-patterns.md`

**Before migration:**
1. Read entire `migration-guide.md`
2. Reference `composition-api.md` for new API syntax

**When implementing features:**
- Forms → `common-patterns.md` Form Handling section
- Data fetching → `common-patterns.md` Data Fetching section
- State management → `common-patterns.md` State Management section
- i18n → `common-patterns.md` i18n section

## Common Development Workflows

### Workflow 1: Create a New Component

```bash
# 1. Choose appropriate template
view assets/component-templates/

# 2. Read best practices
view references/best-practices.md

# 3. Copy and customize template
cp assets/component-templates/BasicComponent.vue src/components/MyComponent.vue

# 4. Follow naming conventions (PascalCase)
# 5. Define props with validation
# 6. Use <script setup> syntax
# 7. Keep component focused and small
```

### Workflow 2: Migrate Vue 2 Code to Vue 3

```bash
# 1. Read migration guide first
view references/migration-guide.md

# 2. Identify patterns to migrate
# - Options API → Composition API
# - this.$set → direct assignment
# - filters → computed/methods
# - Event Bus → mitt/Pinia

# 3. Apply changes systematically
# 4. Test each change
# 5. Update dependencies
```

### Workflow 3: Implement Data Fetching

```bash
# 1. Review data fetching patterns
view references/common-patterns.md
# Look for "Data Fetching Patterns" section

# 2. Choose approach:
# - Custom composable (useFetch template)
# - VueUse (@vueuse/core)
# - TanStack Query

# 3. Implement with error handling and loading states
```

### Workflow 4: Optimize Performance

```bash
# 1. Review performance section
view references/best-practices.md
# Look for "Performance Optimization" section

# 2. Check for issues:
# - Using methods instead of computed
# - Unnecessary v-if usage
# - Missing keys in v-for
# - Large components without splitting
# - No lazy loading

# 3. Apply optimizations:
# - Use computed for derived data
# - v-show for frequent toggles
# - defineAsyncComponent for heavy components
# - Virtual scrolling for large lists
```

### Workflow 5: Form Development

```bash
# 1. Use form template or VeeValidate pattern
view assets/component-templates/FormComponent.vue
view references/common-patterns.md
# Look for "Form Handling Patterns" section

# 2. Implement validation
# 3. Handle errors and loading states
# 4. Add success/error feedback
```

## Quick Reference Commands

### Component Templates
```bash
# List all templates
ls -la assets/component-templates/

# Copy specific template
cp assets/component-templates/[TemplateName].vue src/components/
```

### Composable Templates
```bash
# List all composables
ls -la assets/composable-templates/

# Copy specific composable
cp assets/composable-templates/[composableName].js src/composables/
```

### Read Documentation
```bash
# Migration guide
view references/migration-guide.md

# Composition API reference
view references/composition-api.md

# Best practices
view references/best-practices.md

# Common patterns
view references/common-patterns.md
```

## Best Practices Summary

### Component Design
- Always use `<script setup>` for better performance and DX
- Define props with full validation
- Use composables for reusable logic
- Keep components small and focused (< 200 lines)
- Extract complex logic into composables

### Reactivity
- Use `ref()` for primitives
- Use `reactive()` for objects
- Use `computed()` for derived data
- Use `watch()` when you need old values
- Use `watchEffect()` for automatic dependency tracking

### Performance
- Use `computed()` not methods for template calculations
- Use `v-show` for frequent toggles
- Use `v-if` for initial render conditions
- Always use unique `key` in `v-for`
- Lazy load heavy components with `defineAsyncComponent()`
- Use virtual scrolling for large lists

### Code Organization
```
src/
├── assets/          # Static resources
├── components/      # Reusable components
│   ├── common/      # Base components
│   ├── layout/      # Layout components
│   └── features/    # Feature components
├── composables/     # Reusable logic
├── stores/          # Pinia stores
├── router/          # Router config
├── views/           # Page components
├── utils/           # Utility functions
└── services/        # API services
```

## TypeScript Support

When using TypeScript:
- Define prop types with interfaces
- Use generics in composables
- Type emits properly
- Use `defineComponent` when needed

See `best-practices.md` TypeScript Integration section for details.

## Common Gotchas

1. **Destructuring reactive objects loses reactivity**
   - Use `toRefs()` or access properties directly

2. **Direct array/object mutation in Vue 2 style**
   - Vue 3 doesn't need `$set`, direct mutation works

3. **Forgetting .value with refs**
   - Remember: refs need `.value` in `<script>`, not in `<template>`

4. **Using reactive() for primitives**
   - Use `ref()` for primitives, `reactive()` for objects

5. **Not cleaning up side effects**
   - Always clean up in `onBeforeUnmount()` or use `watchEffect()` cleanup

## Additional Resources

- Official Vue 3 docs: https://vuejs.org/
- Vue 3 Migration guide: https://v3-migration.vuejs.org/
- Composition API FAQ: https://vuejs.org/guide/extras/composition-api-faq.html
- VueUse: https://vueuse.org/ (utility composables)
- Pinia: https://pinia.vuejs.org/ (state management)

## Tips for Using This Skill

1. **Always start with references**: Read relevant documentation before coding
2. **Use templates as starting points**: Don't write from scratch if a template exists
3. **Follow the workflows**: They embody best practices
4. **Check best practices regularly**: Internalize the patterns
5. **When stuck**: Check common-patterns.md for similar examples