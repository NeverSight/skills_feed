---
name: typescript
description: TypeScript standards and best practices with modern tooling. Use when working with TypeScript or TypeScript React files.
---

# TypeScript Guidelines

Standards and best practices for TypeScript development with modern tooling. Follow these guidelines when writing or modifying TypeScript code.

## Design Principles

Apply DRY, KISS, and SOLID consistently. Prefer functional approaches where relevant; use classes for stateful behavior. Use composition over inheritance. Each module should have a single responsibility. Use dependency injection for class dependencies.

## Code Style

- **Naming**: Descriptive yet concise names for variables, functions, and classes
- **Documentation**: JSDoc comments for public APIs, complex logic, and non-obvious design decisions
- **Type annotations**: Be explicit with typing to reduce inference time; avoid `any` unless necessary
- **Imports**: Avoid barrel exports to prevent circular dependencies; prefer direct imports

## Type Safety

- **Strict TypeScript**: Use strict mode with proper type definitions. Use type-safe patterns like Zod schemas for validation and type-safe DOM helpers where applicable.
- **Avoid `any`**: Use `unknown` instead of `any` when the type is truly unknown. Narrow types appropriately.
- **Type inference**: Be explicit with typing to reduce inference time and improve clarity

## Type Patterns

- **Union types**: Use union types for values that can be one of several types
- **Discriminated unions**: Use discriminated unions for type-safe state machines
- **Generic constraints**: Use generic constraints to ensure type safety
- **Utility types**: Leverage TypeScript utility types (Pick, Omit, Partial, etc.)

## Architecture

### Module Organization

- Each module focuses on one concern with clear boundaries
- Extract reusable functions to avoid duplication
- Design for reusability across contexts
- Co-locate types with their usage or in dedicated type files
- Keep types at appropriate module boundaries

### Dependency Management

- Use dependency injection for testability
- Prefer composition over inheritance
- Keep dependencies minimal and focused

## Testing

### Structure

- Tests mirror `src/` directory structure
- Test files: `*.test.ts` or `*.spec.ts`
- Use descriptive test names
- Always check for appropriate unit tests when changing code

### Quality

- Use AAA (Arrange, Act, Assert) pattern
- Tests should be useful, readable, concise, maintainable
- Test edge cases and error conditions
- Maintain test coverage for critical paths

### Tools

- **Vitest**: Use Vitest for unit and integration tests (preferred over Jest)
- Use `@vitest/coverage-v8` for coverage
- Use `jsdom` for DOM testing when needed
- Mock external dependencies appropriately
- **Playwright**: Use Playwright for end-to-end (E2E) tests

## Code Formatting and Linting

### Prettier

- Use Prettier for consistent code formatting
- Config: `printWidth: 120`, `singleQuote: true`, `jsxSingleQuote: true`
- Run `pnpm format` to format code
- Run `pnpm format:check` to check formatting

### ESLint

- Use ESLint with TypeScript plugin
- Use `@typescript-eslint/parser` and `@typescript-eslint/eslint-plugin`
- Run `pnpm lint` to check linting
- Run `pnpm lint:fix` to auto-fix issues

## Framework Recommendations

### For Non-Heavy Client Interaction

- **Astro**: Excellent choice for content-focused sites, blogs, documentation
  - Minimal JavaScript by default
  - Static generation with server islands when needed
  - Great performance and SEO
  - TypeScript-first with excellent DX

### For Heavy Client Interaction

- React, Svelte, or SolidJS with TypeScript
- Choose based on team preference and project requirements

## Build Tools

- **Vite**: Preferred build tool for development and production (unless directed otherwise)
- **Modern Rust-based tooling**: Prefer Rolldown or other lower-level language tooling
  - Avoid Webpack and other older JavaScript-based bundlers unless specifically required

## Package Management

- **pnpm**: Preferred package manager (faster, more efficient than npm/yarn)
- Use `packageManager` field in package.json
- Use pnpm workspaces for monorepos

## Implementation

When implementing TypeScript code:
- Ensure code passes type checking before committing
- Group related changes with tests in atomic commits
- Check for existing workflow patterns (spec-first, TDD, etc.) and follow them

## References

For monorepo-specific patterns using pnpm, see `references/pnpm-monorepo.md`.
