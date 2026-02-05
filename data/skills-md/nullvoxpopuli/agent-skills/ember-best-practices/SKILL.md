---
name: ember-best-practices
description: Ember.js performance optimization and accessibility guidelines. This skill should be used when writing, reviewing, or refactoring Ember.js code to ensure optimal performance patterns and accessibility. Triggers on tasks involving Ember components, routes, data fetching, bundle optimization, or accessibility improvements.
license: MIT
metadata:
  author: Ember.js Community
  version: "1.0.0"
---

# Ember.js Best Practices

Comprehensive performance optimization and accessibility guide for Ember.js applications. Contains 58 rules across 9 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Writing new Ember components or routes
- Implementing data fetching with WarpDrive
- Reviewing code for performance issues
- Refactoring existing Ember.js code
- Optimizing bundle size or load times
- Implementing accessibility features

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Route Loading and Data Fetching | CRITICAL | `route-` |
| 2 | Build and Bundle Optimization | CRITICAL | `bundle-` |
| 3 | Component and Reactivity | HIGH | `component-` |
| 4 | Accessibility Best Practices | HIGH | `a11y-` |
| 5 | Service and State Management | MEDIUM-HIGH | `service-` |
| 6 | Template Optimization | MEDIUM | `template-` |
| 7 | Performance Optimization | MEDIUM | `performance-` |
| 8 | Testing Best Practices | MEDIUM | `testing-` |
| 9 | Tooling and Configuration | MEDIUM | `tooling-` |
| 10 | Advanced Patterns | MEDIUM-HIGH | `advanced-` |

## Quick Reference

### 1. Route Loading and Data Fetching (CRITICAL)

- `route-parallel-model` - Use RSVP.hash() for parallel data loading
- `route-loading-substates` - Implement loading substates for better UX
- `route-lazy-routes` - Use route-based code splitting with Embroider
- `route-templates` - Use route templates with co-located syntax
- `route-model-caching` - Implement smart route model caching

### 2. Build and Bundle Optimization (CRITICAL)

- `bundle-direct-imports` - Import directly, avoid entire namespaces
- `bundle-embroider-static` - Enable Embroider static mode for tree-shaking
- `bundle-lazy-dependencies` - Lazy load heavy dependencies

### 3. Component and Reactivity Optimization (HIGH)

- `component-use-glimmer` - Use Glimmer components over classic components
- `component-cached-getters` - Use @cached for expensive computations
- `component-minimal-tracking` - Only track properties that affect rendering
- `component-tracked-toolbox` - Use tracked-built-ins for complex state
- `component-composition-patterns` - Use yield blocks and contextual components
- `component-reactive-chains` - Build reactive chains with dependent getters
- `component-class-fields` - Use class fields for component composition
- `component-controlled-forms` - Implement controlled form patterns
- `component-on-modifier` - Use {{on}} modifier for event handling
- `component-args-validation` - Validate component arguments
- `component-memory-leaks` - Prevent memory leaks in components
- `component-strict-mode` - Use strict mode and template-only components
- `component-avoid-classes-in-examples` - Avoid unnecessary classes in component examples
- `component-avoid-constructors` - Avoid constructors in Glimmer components
- `component-avoid-lifecycle-hooks` - Avoid legacy lifecycle hooks
- `component-file-conventions` - Follow proper file naming conventions
- `exports-named-only` - Use named exports only

### 4. Accessibility Best Practices (HIGH)

- `a11y-automated-testing` - Use ember-a11y-testing for automated checks
- `a11y-semantic-html` - Use semantic HTML and proper ARIA attributes
- `a11y-keyboard-navigation` - Ensure full keyboard navigation support
- `a11y-form-labels` - Associate labels with inputs, announce errors
- `a11y-route-announcements` - Announce route transitions to screen readers

### 5. Service and State Management (MEDIUM-HIGH)

- `service-cache-responses` - Cache API responses in services
- `service-shared-state` - Use services for shared state
- `service-ember-data-optimization` - Optimize WarpDrive queries
- `service-owner-linkage` - Manage service owner and linkage patterns
- `service-data-requesting` - Implement robust data requesting patterns

### 6. Template Optimization (MEDIUM)

- `template-let-helper` - Use {{#let}} to avoid recomputation
- `template-each-key` - Use {{#each}} with @key for efficient list updates
- `template-avoid-computation` - Move expensive work to cached getters
- `template-helper-imports` - Import helpers directly in templates
- `template-conditional-rendering` - Optimize conditional rendering
- `template-fn-helper` - Use {{fn}} helper for partial application
- `template-only-component-functions` - Use template-only components
- `helper-composition` - Compose helpers for reusable logic
- `helper-builtin-functions` - Use built-in helpers effectively
- `helper-plain-functions` - Write helpers as plain functions

### 7. Performance Optimization (MEDIUM)

- `performance-on-modifier-vs-handlers` - Use {{on}} modifier instead of event handler properties

### 8. Testing Best Practices (MEDIUM)

- `testing-modern-patterns` - Use modern testing patterns
- `testing-qunit-dom-assertions` - Use qunit-dom for better test assertions
- `testing-test-waiters` - Use @ember/test-waiters for async testing
- `testing-render-patterns` - Use correct render patterns for components
- `testing-msw-setup` - Mock API requests with MSW
- `testing-library-dom-abstraction` - Use Testing Library patterns

### 9. Tooling and Configuration (MEDIUM)

- `vscode-setup-recommended` - VS Code extensions and MCP server setup

### 10. Advanced Patterns (MEDIUM-HIGH)

- `advanced-modifiers` - Use modifiers for DOM side effects
- `advanced-helpers` - Extract reusable logic into helpers
- `advanced-tracked-built-ins` - Use reactive collections from @ember/reactive/collections
- `advanced-concurrency` - Use ember-concurrency for task management
- `advanced-data-loading-with-ember-concurrency` - Data loading patterns with ember-concurrency

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/route-parallel-model.md
rules/bundle-embroider-static.md
rules/a11y-automated-testing.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references

## Accessibility with OSS Tools

Ember has excellent accessibility support through community addons:

- **ember-a11y-testing** - Automated accessibility testing in your test suite
- **ember-a11y** - Route announcements and focus management
- **ember-focus-trap** - Focus trapping for modals and dialogs
- **ember-page-title** - Accessible page title management
- **Platform-native validation** - Use browser's Constraint Validation API for accessible form validation

These tools, combined with native web platform features, provide comprehensive a11y support with minimal configuration.

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
