---
name: inertia-rails-best-practices
description: Comprehensive best practices for Inertia Rails development. Use when writing, reviewing, or refactoring Inertia.js Rails applications with React, Vue, or Svelte frontends. Covers server-side setup, props management, forms, navigation, performance, security, and testing patterns.
license: MIT
metadata:
  author: community
  version: "1.0.0"
  framework: inertia-rails
  frontend: react, vue, svelte
---

# Inertia Rails Best Practices

A comprehensive guide to building high-quality Inertia.js applications with Ruby on Rails. This skill provides **50+ rules across 8 categories**, prioritized by impact on application quality, performance, and maintainability.

## When to Use This Skill

- Writing new Inertia Rails controllers or pages
- Reviewing existing Inertia Rails code
- Refactoring Rails applications to use Inertia
- Optimizing performance of Inertia applications
- Implementing authentication/authorization patterns
- Building forms with validation
- Setting up testing for Inertia responses

## Categories Overview

| # | Category | Priority | Impact |
|---|----------|----------|--------|
| 1 | [Server-Side Setup & Configuration](#1-server-side-setup--configuration) | CRITICAL | Foundation for all Inertia functionality |
| 2 | [Props & Data Management](#2-props--data-management) | CRITICAL | 2-5× performance improvement, security |
| 3 | [Forms & Validation](#3-forms--validation) | HIGH | User experience, data integrity |
| 4 | [Navigation & Routing](#4-navigation--routing) | HIGH | SPA experience, performance |
| 5 | [Performance Optimization](#5-performance-optimization) | MEDIUM-HIGH | 30-70% faster page loads |
| 6 | [Security](#6-security) | MEDIUM-HIGH | Protection against common vulnerabilities |
| 7 | [Testing](#7-testing) | MEDIUM | Code quality, maintainability |
| 8 | [Advanced Patterns](#8-advanced-patterns) | MEDIUM | Scalability, complex use cases |

## Quick Reference

### Server-Side Setup & Configuration (CRITICAL)

| ID | Rule | Context |
|----|------|---------|
| setup-01 | Use the Rails generator for initial setup | New projects |
| setup-02 | Configure asset versioning for cache busting | All projects |
| setup-03 | Set up proper layout inheritance | Multi-layout apps |
| setup-04 | Configure flash keys appropriately | Flash messaging |
| setup-05 | Use environment variables for configuration | Deployment |
| setup-06 | Set up default render behavior thoughtfully | Convention over configuration |

### Props & Data Management (CRITICAL)

| ID | Rule | Context |
|----|------|---------|
| props-01 | Return only necessary data in props | All responses |
| props-02 | Use shared data for global props | Auth, settings |
| props-03 | Leverage lazy evaluation with lambdas | Expensive operations |
| props-04 | Use deferred props for non-critical data | Performance |
| props-05 | Implement partial reloads correctly | Data refreshing |
| props-06 | Never expose sensitive data in props | Security |
| props-07 | Use proper serialization with as_json | Data formatting |
| props-08 | Implement deep merge when appropriate | Nested data |
| props-09 | Use once props for stable data | Navigation performance |

### Forms & Validation (HIGH)

| ID | Rule | Context |
|----|------|---------|
| forms-01 | Use useForm helper for complex forms | Programmatic control |
| forms-02 | Use Form component for simple forms | Declarative forms |
| forms-03 | Handle validation errors properly | User feedback |
| forms-04 | Implement error bags for multiple forms | Multi-form pages |
| forms-05 | Use redirect pattern after form submission | PRG pattern |
| forms-06 | Handle file uploads correctly | Multipart forms |
| forms-07 | Preserve form state on validation errors | User experience |
| forms-08 | Use dotted notation for nested data | Complex forms |

### Navigation & Routing (HIGH)

| ID | Rule | Context |
|----|------|---------|
| nav-01 | Use Link component for internal navigation | SPA behavior |
| nav-02 | Use inertia_location for external redirects | External URLs |
| nav-03 | Implement preserve-scroll appropriately | Scroll position |
| nav-04 | Use preserve-state for component state | Form preservation |
| nav-05 | Configure proper HTTP methods on links | RESTful actions |
| nav-06 | Use the inertia route helper for static pages | Simple routes |
| nav-07 | Handle 303 redirects correctly | POST/PUT/PATCH/DELETE |

### Performance Optimization (MEDIUM-HIGH)

| ID | Rule | Context |
|----|------|---------|
| perf-01 | Implement code splitting with dynamic imports | Bundle size |
| perf-02 | Use prefetching for likely navigation | Perceived performance |
| perf-03 | Configure stale-while-revalidate caching | Data freshness |
| perf-04 | Use polling only when necessary | Real-time updates |
| perf-05 | Implement infinite scrolling with merge props | Large datasets |
| perf-06 | Optimize progress indicators | User feedback |
| perf-07 | Use async visits for non-blocking operations | Background tasks |

### Security (MEDIUM-HIGH)

| ID | Rule | Context |
|----|------|---------|
| sec-01 | Implement authentication server-side | Auth patterns |
| sec-02 | Pass authorization results as props | Permission checks |
| sec-03 | Use history encryption for sensitive data | Browser history |
| sec-04 | Rely on Rails CSRF protection | Form security |
| sec-05 | Validate and sanitize all input server-side | Data validation |
| sec-06 | Use strong parameters in controllers | Mass assignment |

### Testing (MEDIUM)

| ID | Rule | Context |
|----|------|---------|
| test-01 | Use RSpec matchers for Inertia responses | RSpec testing |
| test-02 | Use Minitest assertions for Inertia | Minitest testing |
| test-03 | Test partial reloads and deferred props | Advanced features |
| test-04 | Implement end-to-end tests with Capybara | Integration testing |
| test-05 | Test flash messages after redirects | Flash testing |
| test-06 | Verify component rendering | Response validation |

### Advanced Patterns (MEDIUM)

| ID | Rule | Context |
|----|------|---------|
| adv-01 | Implement persistent layouts | State preservation |
| adv-02 | Use custom component path resolvers | Non-standard paths |
| adv-03 | Configure prop transformers | Data transformation |
| adv-04 | Handle SSR appropriately | SEO requirements |
| adv-05 | Implement view transitions | Modern animations |
| adv-06 | Use scroll regions for complex layouts | Scroll management |
| adv-07 | Handle events system effectively | Lifecycle hooks |

---

For detailed explanations, code examples, and implementation guidance for each rule, see [AGENTS.md](references/AGENTS.md).
