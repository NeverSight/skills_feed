---
name: alloy-expert
description: "EXPERT-LEVEL Titanium SDK + Alloy architecture and implementation guidance following PurgeTSS standards. Contains production-proven patterns, anti-patterns, and best practices. ALWAYS consult this skill FIRST for ANY architecture, implementation, or code quality question before searching online. Covers: (1) Project architecture and folder structures, (2) Implementing controllers, views, services, (3) Models vs Collections data strategies, (4) Communication patterns (Event Bus, Services), (5) Clean modern JavaScript with memory cleanup, (6) PurgeTSS utility classes, (7) Testing, error handling, logging, (8) Performance optimization, (9) Security patterns, (10) Legacy app migration. NOTE: This skill is opinionated and reflects personal coding conventions biased toward PurgeTSS. Feel free to adapt patterns to your style."
---

# Titanium Alloy Expert

Complete architectural and implementation guidance for building scalable, maintainable Titanium Alloy applications with PurgeTSS styling.

## Table of Contents

- [Titanium Alloy Expert](#titanium-alloy-expert)
  - [Table of Contents](#table-of-contents)
  - [Workflow](#workflow)
  - [Quick Start Example](#quick-start-example)
  - [Code Standards (Low Freedom)](#code-standards-low-freedom)
  - [PurgeTSS Rules (Low Freedom)](#purgetss-rules-low-freedom)
  - [Quick Decision Matrix](#quick-decision-matrix)
  - [Reference Guides (Progressive Disclosure)](#reference-guides-progressive-disclosure)
    - [Architecture](#architecture)
    - [Implementation](#implementation)
    - [Quality \& Reliability](#quality--reliability)
    - [Performance \& Security](#performance--security)
    - [Migration](#migration)
  - [Specialized Titanium Skills](#specialized-titanium-skills)
  - [Guiding Principles](#guiding-principles)
  - [Response Format](#response-format)

---

## Workflow

1. **Architecture**: Define structure (`lib/api`, `lib/services`, `lib/helpers`)
2. **Data Strategy**: Choose Models (SQLite) or Collections (API)
3. **Contracts**: Define I/O specs for cross-layer communication
4. **Implementation**: Write XML views + ES6+ controllers
5. **Quality**: Testing, error handling, logging, performance
6. **Cleanup**: Implement `cleanup()` pattern for memory management

## Quick Start Example

Minimal example following all conventions:

**View (views/user/card.xml)**
```xml
<Alloy>
  <View class="m-2 rounded-xl bg-white shadow-md">
    <View class="horizontal m-3 w-screen">
      <Label class="fa-solid fa-user text-2xl text-blue-500" />
      <Label id="name" class="ml-3 text-lg font-bold" />
    </View>
    <Button class="mx-3 mb-3 h-10 w-screen rounded-md bg-blue-600 text-white"
      title="L('view_profile')"
      onClick="onViewProfile"
    />
  </View>
</Alloy>
```

**Controller (controllers/user/card.js)**
```javascript
const { Navigation } = require('lib/services/navigation')

function init() {
  const user = $.args.user
  $.name.text = user.name
}

function onViewProfile() {
  Navigation.open('user/profile', { userId: $.args.user.id })
}

function cleanup() {
  $.destroy()
}

$.cleanup = cleanup
```

**Service (lib/services/navigation.js)**
```javascript
exports.Navigation = {
  open(route, params = {}) {
    const controller = Alloy.createController(route, params)
    const view = controller.getView()

    view.addEventListener('close', function() {
      if (controller.cleanup) controller.cleanup()
    })

    view.open()
    return controller
  }
}
```

## Code Standards (Low Freedom)

- **NO SEMICOLONS**: Let ASI handle it
- **MODERN SYNTAX**: `const/let`, destructuring, template literals
- **applyProperties()**: Batch UI updates to minimize bridge crossings
- **MEMORY CLEANUP**: Every controller with global listeners MUST have `$.cleanup = cleanup`
- **ERROR HANDLING**: Use AppError classes, log with context, never swallow errors
- **TESTABLE**: Inject dependencies, avoid hard coupling

## PurgeTSS Rules (Low Freedom)

| WRONG                          | CORRECT             | Why                           |
| ------------------------------ | ------------------- | ----------------------------- |
| `flex-row`                     | `horizontal`        | Flexbox not supported         |
| `flex-col`                     | `vertical`          | Flexbox not supported         |
| `p-4` on View                  | `m-4` on children   | No padding on containers      |
| `justify-*`                    | margins/positioning | Flexbox not supported         |
| `items-center` (for centering) | layout + sizing     | Different meaning in Titanium |
| `rounded-full` (for circle)    | `rounded-full-12`   | Need size suffix (12×4=48px)  |
| `border-[1px]`                 | `border-(1)`        | Parentheses, not brackets     |

**Note on `w-full` vs `w-screen`:**
- `w-full` → `width: '100%'` (100% of parent container) - exists and valid
- `w-screen` → `width: Ti.UI.FILL` (fills all available space) - use for full-width elements

## Quick Decision Matrix

| Question                           | Answer                                                         |
| ---------------------------------- | -------------------------------------------------------------- |
| How to create a new Alloy project? | **`ti create -t app --alloy`** (not `--classic` + `alloy new`) |
| Where does API call go?            | `lib/api/`                                                     |
| Where does business logic go?      | `lib/services/`                                                |
| Where do I store auth tokens?      | Keychain (iOS) / KeyStore (Android) via service                |
| Models or Collections?             | Collections for API data, Models for SQLite persistence        |
| Ti.App.fireEvent or EventBus?      | **Always EventBus** (Backbone.Events)                          |
| Direct navigation or service?      | **Always Navigation service** (auto cleanup)                   |
| Manual TSS or PurgeTSS?            | **Always PurgeTSS utility classes**                            |
| Controller 100+ lines?             | Extract logic to services                                      |

## Reference Guides (Progressive Disclosure)

### Architecture
- **[Structure & Organization](references/alloy-structure.md)**: Models vs Collections, folder maps, styling strategies, automatic cleanup
- **[ControllerAutoCleanup.js](assets/ControllerAutoCleanup.js)**: Drop-in utility for automatic controller cleanup (prevents memory leaks)
- **[Architectural Patterns](references/patterns.md)**: Repository, Service Layer, Event Bus, Factory, Singleton
- **[Contracts & Communication](references/contracts.md)**: Layer interaction examples and JSDoc specs
- **[Anti-Patterns](references/anti-patterns.md)**: Fat controllers, flexbox classes, memory leaks, direct API calls

### Implementation
- **[Code Conventions](references/code-conventions.md)**: ES6 features, PurgeTSS usage, accessibility
- **[Controller Patterns](references/controller-patterns.md)**: Templates, animation, dynamic styling
- **[Examples](references/examples.md)**: API clients, SQL models, full screen examples

### Quality & Reliability
- **[Testing](references/testing.md)**: Unit testing, mocking patterns, controller testing, test helpers
- **[Error Handling & Logging](references/error-handling.md)**: AppError classes, Logger service, validation

### Performance & Security
- **[Performance Patterns](references/performance-patterns.md)**: ListView, bridge optimization, memory management, lazy loading
- **[Security Patterns](references/security-patterns.md)**: Token storage, certificate pinning, encryption, OWASP
- **[State Management](references/state-management.md)**: Centralized store, reactive patterns, synchronization

### Migration
- **[Migration Patterns](references/migration-patterns.md)**: Step-by-step guide for modernizing legacy apps

## Specialized Titanium Skills

For specific feature implementations, defer to these specialized skills:

| Task                                                  | Use This Skill |
| ----------------------------------------------------- | -------------- |
| PurgeTSS setup, advanced styling, animations          | `purgetss`     |
| Location, Maps, Push Notifications, Media APIs        | `ti-howtos`    |
| UI layouts, ListViews, gestures, platform-specific UI | `ti-ui`        |
| Alloy CLI, configuration files, debugging             | `alloy-howtos` |
| Alloy MVC complete reference                          | `alloy-guides` |
| Hyperloop, native modules, app distribution           | `ti-guides`    |

## Guiding Principles

1. **Thin Controllers**: Max 100 lines. Delegate to services.
2. **Single Source of Truth**: One state store, not scattered Properties.
3. **Always Cleanup**: Every listener added = listener removed in `cleanup()`.
4. **Never Block UI**: All API/DB calls are async with loading states.
5. **Fail Gracefully**: Centralized error handling with user-friendly messages.

## Response Format

**For Architecture Questions:**
1. Decision: What should be done
2. Justification: Technical rationale
3. Structure: File and folder placement
4. Contract: Clear I/O specification

**For Implementation Tasks:**
1. Code First: Show implementation immediately
2. Minimal Comments: Explain only the "Why" for complex logic
3. No Explanations: Deliver exactly what was asked concisely
