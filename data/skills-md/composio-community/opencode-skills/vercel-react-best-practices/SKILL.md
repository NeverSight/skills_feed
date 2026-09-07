---
name: vercel-react-best-practices
description: Workflow for building production-quality React applications using Vercel-style best practices focused on readability, performance, maintainability, and stable UI behavior.
---

# Vercel React Best Practices

## Overview

This skill enables Claude to build and review React applications using modern frontend engineering standards inspired by high-quality production workflows.

The workflow focuses on:
- readable React architecture
- maintainable component systems
- performance optimization
- stable rendering behavior
- edge-case handling
- scalable frontend structure
- production-ready UI patterns

The goal is to ensure React projects remain:
- clean
- predictable
- scalable
- performant
- easy to review and maintain

This workflow emphasizes long-term maintainability over short-term hacks or overly clever abstractions.

---

# Setup

Before starting:

1. Install Node.js:
   https://nodejs.org

2. Create a React or Next.js project:

```bash
npx create-next-app@latest
```

or:

```bash
npm create vite@latest
```

3. Install dependencies:

```bash
npm install
```

4. Start development server:

```bash
npm run dev
```

Recommended tools:
- VS Code
- TypeScript
- ESLint
- Prettier
- React DevTools

Recommended extensions:
- ES7 React snippets
- Prettier
- Tailwind CSS IntelliSense
- Error Lens

---

# Inputs Required

- React project or component system
- UI requirements
- Application structure
- State management requirements

Optional:
- Design system
- Existing component library
- API contracts
- Performance requirements

---

# When to Use This Skill

Use this skill when:
- building React applications
- reviewing frontend code
- designing scalable component systems
- optimizing frontend performance
- improving maintainability
- handling complex UI states
- creating production-ready frontend architecture

---

# When NOT to Use

Do NOT use this skill for:
- quick throwaway prototypes
- non-React projects
- static HTML-only workflows
- highly experimental one-off demos

---

# Example Use Case

> Build a scalable dashboard interface for a SaaS product.

Claude should:

1. Create reusable component architecture
2. Keep component logic readable
3. Prevent unnecessary re-renders
4. Handle loading and error states correctly
5. Optimize rendering performance
6. Ensure accessibility and maintainability
7. Validate edge-case behavior

Final result should:
- remain easy to scale
- feel performant
- avoid unstable UI behavior
- maintain clean architecture
- support long-term development

---

# Core React Principles

## 1. Prioritize Readability

Readable code is more valuable than overly clever abstractions.

Components should:
- remain understandable
- have clear responsibilities
- avoid excessive nesting
- use predictable naming

Good readability improves:
- onboarding
- debugging
- reviews
- long-term maintenance

Avoid:
- deeply nested logic
- overly abstract hooks
- unnecessary complexity
- confusing state flow

---

## 2. Keep Components Focused

Each component should have a single clear responsibility.

Good component design:
- isolates concerns
- improves reusability
- simplifies testing
- reduces side effects

Preferred structure:
- UI components
- logic hooks
- utility functions
- shared primitives

Avoid:
- massive monolithic components
- mixed responsibilities
- tightly coupled logic

---

## 3. Optimize Rendering Performance

React applications should minimize unnecessary rendering work.

Common optimization strategies:
- memoization
- component splitting
- stable props
- efficient state updates
- lazy loading

Claude should proactively prevent:
- excessive re-renders
- unstable object creation
- unnecessary derived state
- large render trees

Performance improves:
- responsiveness
- scalability
- perceived quality

---

## 4. Handle Edge Cases Explicitly

Production applications require robust state handling.

Always account for:
- loading states
- empty states
- failed requests
- invalid inputs
- partial data
- asynchronous race conditions

Stable UI systems should fail gracefully.

Avoid:
- undefined rendering assumptions
- unhandled async behavior
- fragile conditional rendering

---

## 5. Maintain Predictable State Flow

State management should remain:
- centralized when necessary
- localized when possible
- easy to trace
- easy to debug

Preferred approaches:
- colocated state
- predictable hooks
- derived values
- controlled updates

Avoid:
- duplicated state
- deeply chained prop drilling
- unpredictable side effects

---

## 6. Build Reusable UI Systems

Reusable systems improve scalability significantly.

Preferred patterns:
- shared UI primitives
- consistent spacing systems
- reusable layouts
- centralized design tokens

Good systems improve:
- development speed
- consistency
- maintainability

---

# Workflow

## 1. Define Application Structure

Start by identifying:
- pages
- layouts
- reusable components
- shared logic
- API boundaries

Recommended structure:

```plaintext
components/
hooks/
lib/
pages/
styles/
```

Keep the architecture:
- predictable
- modular
- scalable

---

## 2. Build Reusable Components

Create:
- buttons
- cards
- inputs
- modals
- layout primitives

Each component should:
- remain isolated
- support reuse
- expose clean props
- avoid tightly coupled logic

---

## 3. Handle State Carefully

Separate:
- server state
- local UI state
- derived values
- async operations

Validate:
- loading behavior
- error handling
- optimistic updates
- race conditions

Keep state transitions predictable.

---

## 4. Optimize Performance

Check for:
- unnecessary re-renders
- unstable props
- large component trees
- blocking operations

Use:
- `React.memo`
- lazy loading
- dynamic imports
- memoized calculations

Optimize only where necessary.

Avoid premature optimization.

---

## 5. Improve Accessibility

Ensure:
- keyboard navigation
- semantic HTML
- proper labels
- focus management
- screen-reader compatibility

Accessibility improves:
- usability
- maintainability
- production quality

---

## 6. Validate Edge Cases

Before shipping validate:
- empty states
- slow network behavior
- failed API responses
- invalid user inputs
- mobile responsiveness

Production-quality applications should remain stable under imperfect conditions.

---

## 7. Review & Refine

Review:
- readability
- component complexity
- rendering behavior
- maintainability
- architectural consistency

Refactor:
- duplicated logic
- overly complex components
- unstable abstractions

---

# Output Expectations

The final output should include:
- clean React architecture
- reusable component systems
- stable rendering behavior
- optimized performance
- robust edge-case handling
- production-ready frontend quality

The workflow itself should remain:
- scalable
- maintainable
- readable
- team-friendly
- easy to review

---

# Execution Strategy (for AI agents)

The agent should:

1. Prioritize readability over unnecessary abstraction
2. Keep components focused and modular
3. Detect performance issues proactively
4. Handle edge cases explicitly
5. Maintain predictable state flow
6. Optimize for long-term maintainability

The workflow should optimize for:
- frontend stability
- rendering performance
- maintainability
- developer experience
- scalability

---

# Best Practices

- Keep components small and focused
- Avoid unnecessary abstraction layers
- Handle loading and error states explicitly
- Prevent unnecessary re-renders
- Use semantic HTML
- Prefer composition over complexity
- Validate edge cases before shipping

---

# Notes

- Readability compounds over long projects
- Stable React architecture improves team velocity
- Most frontend instability comes from poor state management
- Explicit edge-case handling dramatically improves reliability
- Good component systems scale better than ad-hoc implementations
