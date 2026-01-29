---
name: frontend-design-system
description: >
  Design and refactor React/Tailwind frontends using the project design system.
  Use this Skill when working on UI components, pages, layouts, or UX improvements
  and you want distinctive, accessible, non-generic designs that avoid AI slop.
allowed-tools: Read, Grep, Glob
---

# Frontend Design System Skill

## Purpose

This Skill packages opinionated guidance for building and refactoring frontend UI so that output:
- Uses the existing design system instead of ad-hoc styles.
- Avoids generic “AI slop” UI and looks intentional and product-ready.
- Meets accessibility, responsiveness, and basic performance expectations.

Use this Skill whenever the user:
- Asks for React/Tailwind components, HTML/CSS layouts, or UI redesigns.
- Mentions design, UX, responsiveness, accessibility, or “make this look better”.
- Wants to refactor messy or inconsistent frontend code.

## Tech stack assumptions

Unless the user clearly states otherwise, assume:
- Framework: React function components (with hooks, TypeScript when present).
- Styling: Tailwind CSS with design tokens (CSS variables, theme config).
- Layout: Mobile-first, using flexbox and grid.
- Routing: Next.js or React Router style (do not invent routes unless requested).

If the project uses a different stack (e.g. Svelte, Vue, plain HTML/CSS), keep the same design principles and adapt syntax.

## Design system rules

When generating or editing UI, always:

1. **Use design tokens and theme**
   - Use semantic classes and variables for color (primary, secondary, accent, danger, surface, background, border, text).
   - Use the project spacing scale (e.g. `gap-2/3/4/6`, `p-4/6`, etc.) instead of arbitrary values.
   - Use only the established radii and shadows (e.g. `rounded-sm`, `rounded-md`, `shadow-sm`, `shadow-md`).

2. **Typography hierarchy**
   - Keep a clear hierarchy: page title, section title, body, caption.
   - Limit to 1–2 font stacks; never introduce new fonts unless the user asks.
   - Ensure line height and spacing are readable on mobile and desktop.

3. **Consistent component patterns**
   - Buttons: primary, secondary, subtle, destructive variants with consistent paddings and icon spacing.
   - Cards: shared padding, radius, shadow, header/body/footer patterns.
   - Forms: aligned labels, consistent input heights, clear error/help text styling.

If the repo has existing tokens/components, inspect them first (using Read/Grep/Glob) and align with those patterns.

## Anti–AI slop guardrails

Treat “AI slop” as any UI that is obviously default, generic, or visually incoherent.

**Never:**
- Use arbitrary rainbow gradients, neon glows, or random color mixes by default.
- Spam shadows, borders, and animations without purpose.
- Produce layouts that are just centered blobs of identical cards with no hierarchy.
- Fill UI with meaningless placeholder content or fake stats unless explicitly requested.

**Always:**
- Provide a clear visual hierarchy: one primary action, visible section grouping, obvious reading order.
- Use asymmetry and whitespace to create structure, not clutter.
- Limit motion: subtle hover and focus states, and respect `prefers-reduced-motion`.

Before finalizing any UI, mentally run a quick anti-slop checklist:
- Does this look like a bland, default template?
- Are color, typography, spacing, and radii consistent?
- Is there a clear primary action and purpose in each section?

If the answer is “yes, it looks generic” or “no, the hierarchy is unclear”, refactor the design.

## Accessibility requirements

For all generated UI:

- Use semantic HTML elements (`<header>`, `<main>`, `<section>`, `<nav>`, `<button>`, `<form>`, `<label>`, `<ul>`, `<li>`, etc.).
- Keep headings in logical order (`h1` then `h2`, `h3`, …).
- All interactive elements:
  - Are keyboard-focusable.
  - Have visible focus states that meet contrast requirements.
  - Have accessible names (visible text or `aria-label`).
- Ensure text and UI elements meet WCAG 2.1 AA contrast.
- For forms:
  - Every input has a `<label>` or `aria-label`.
  - Error states are communicated visually and via text near the field.

If the user asks for something that breaks basic accessibility (e.g. invisible focus), comply only if they are explicit and briefly warn about the trade-off.

## Responsive layout patterns

Default to mobile-first CSS and then enhance for larger breakpoints.

Prefer these patterns when the user does not specify a layout:

1. **Dashboard**
   - Left nav, main content, optional right sidebar.
   - Sticky header in main area with title and primary actions.

2. **Landing / marketing**
   - Hero (headline, supporting text, primary CTA, optional secondary CTA).
   - Supporting sections: features, use cases, social proof, footer.

3. **List + filters**
   - Filters/search controls in a header or left panel.
   - List or grid of items with clear empty/loading states.

4. **Detail + sidebar**
   - Main detail content (record, document, form).
   - Sidebar for metadata, secondary actions, or related content.

Choose the pattern that best fits the user’s described use case and note the choice briefly when answering.

## Code quality expectations

- Keep components focused; extract subcomponents when markup becomes repetitive or complex.
- Avoid deeply nested `div` structures; use meaningful wrappers and utility classes.
- Match existing project conventions:
  - File/folder structure.
  - Naming for components, props, hooks.
  - Import paths and alias usage.
- Remove unused imports, dead code, and commented-out sections from final output.
- Where helpful, add concise comments or JSDoc for complex props or layout logic.

## Workflow when this Skill is active

When a request matches this Skill (frontend, UI, UX, layout, React, Tailwind):

1. **Understand the context**
   - Restate the goal: what page/feature, who uses it, what the user is trying to do.
   - If key constraints are missing (data shape, breakpoints, brand rules), ask for them or make clearly marked assumptions.

2. **Scan existing code and design system**
   - Use Read/Grep/Glob to find:
     - Layout shells, shared components, and existing tokens.
     - Current patterns for buttons, forms, and typography.
   - Align new work with what already exists.

3. **Propose structure first**
   - Outline sections, components, and state responsibilities in prose or comments.
   - Select a layout pattern and explain it briefly.

4. **Implement the UI**
   - Write React/Tailwind or HTML/CSS following all rules above.
   - Include loading/empty/error states where appropriate.
   - Ensure responsiveness and accessibility from the start, not as an afterthought.

5. **Review and refine**
   - Re-run the anti-slop checklist.
   - Tighten inconsistent spacing, colors, and typography.
   - Remove unnecessary elements and complexity.

6. **Explain extension points**
   - Mention how to:
     - Add more variants.
     - Integrate with existing state/data fetching.
     - Reuse subcomponents in other screens.

## Examples

These examples are illustrative of process and expectations. When generating new UI, follow the same level of structure and attention to detail, not the exact content.

### Example: Improve an existing form screen

- Analyze the current form component and identify:
  - Inconsistent paddings and gaps.
  - Missing labels or help text.
  - Poor mobile layout (overflow, cramped fields).
- Propose:
  - A two-column layout on desktop, single-column on mobile.
  - Clear grouping of related fields with section headings.
  - Consistent button placement for primary/secondary actions.
- Implement:
  - Error and success message styling.
  - Accessible labels and focus handling.

### Example: New dashboard widget

- Given a requirement for a small dashboard card:
  - Select the shared card pattern.
  - Show title, key metric, optional trend badge, and subtle description.
- Implement:
  - A reusable `<MetricCard>` component using existing design tokens.
  - Responsive behavior: single column on mobile, grid on larger screens.

## Version history

- v1.0.0 (2025-11-23): Initial version for React/Tailwind, anti–AI slop design guardrails, and accessibility defaults.
