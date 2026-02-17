---
name: tailwind
description: Tailwind CSS patterns for layouts, color schemes, responsive design, and className handling. Use when writing or reviewing component styles.
---

# Tailwind CSS

Act as a frontend engineer reviewing Tailwind CSS usage for consistency, maintainability, and best practices.

Review: $ARGUMENTS

## Layout

- Use `gap-*` on parent containers instead of margins on children. Gaps are consistent and don't leak spacing.
- Use stack utilities (`v-stack`, `h-stack`, `center`, `spacer`, `z-stack`) when the project defines them — prefer these over raw `flex flex-col` / `flex flex-row`.
- Switch layout direction at breakpoints for responsive stacks: `v-stack lg:h-stack gap-4`.

## className Handling

- Always use `cn()` (clsx + tailwind-merge) to merge class names in components. External `className` props go last so consumers can override.
- Type className props properly: `ClassName` for single-element components, `ClassNameRecord<"root" | "label" | "input">` for multi-element components.

## Color Schemes

- Use semantic color tokens (`text-foreground`, `bg-primary`, `border-border`) instead of hardcoded Tailwind colors (`text-gray-900`, `bg-blue-600`).
- Support dark mode via the project's color scheme setup (class-based `dark` variant with OS `prefers-color-scheme`).

## Responsive Design

- Design mobile-first: base styles for mobile, then `md:` / `lg:` / `xl:` for larger screens.
- Scale text responsively with breakpoint prefixes: `text-2xl md:text-3xl lg:text-4xl`.
- Use container queries (`@container`) for component-level responsive behavior independent of viewport width.

## Anti-Patterns

| Avoid | Prefer |
|---|---|
| `flex flex-col` | `v-stack` (if available) |
| `flex flex-row` | `h-stack` (if available) |
| `flex items-center justify-center` | `center` (if available) |
| Child margins (`mb-4` on each item) | Parent `gap-4` |
| `bg-[#hex]` / hardcoded colors | Semantic design tokens |
| `className="..."` without `cn()` | `cn("...", className)` |
| Inline `style` for responsive | Tailwind breakpoint prefixes |
