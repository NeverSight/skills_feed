---
name: gts-design-system-integration
description: Integrate and implement apps and screens using gts-central-library tokens, styles, and components. Use when adding the design system to Vite, Next.js, Lovable, or React apps; migrating from shadcn or parallel token systems; setting up Tailwind v4 with GTS css; implementing configurator-style layouts; or troubleshooting token/theme/style mismatches.
---

# GTS Design System Integration

## Quick Workflow
1. Identify the app type and current styling stack.
2. Align dependencies and Tailwind v4 tooling.
3. Set up one Tailwind css entrypoint and correct import order.
4. Import GTS css once at the app root.
5. Remove conflicting token/theme/global style sources.
6. Apply GTS layout and typography patterns.
7. For complex pages (for example configurator screens), compose reusable layout sections and variant-driven states.
8. Validate build, lint, and visual output.

## Load These References
- Always read `references/guidelines.md`.
- Always read `references/shadcn-compatibility.md`.
- Always read `references/tailwind-style-usage.md`.
- Always read `references/tailwind-utility-inventory.md`.
- Read `references/app-integration-playbook.md` for app-specific steps.

## Guardrails
- Treat `gts-central-library` as the styling source of truth.
- Keep app behavior and routing unchanged during migration.
- Keep local css minimal and app-specific.
- Avoid duplicate semantic variable systems.
- Keep Tailwind configuration modern (v4 syntax/tooling) and avoid legacy layering patterns.
- Prefer GTS components and token-backed values over one-off styles.
- For configurator implementations, model screen states as explicit variants (`summary`, `style`, `personalize`, etc.) instead of duplicating near-identical page code.
- Reuse existing primitives (`Header`, `USPBar`, `ActionBar`, `Button`, `SearchBar`, token utilities) before introducing new components.
- Keep configurator sections data-driven (accordion rows, swatches, option grids) so behavior and structure stay consistent across variants.
- Add Storybook coverage for each major layout state; do not create separate stories for transient interactive states (hover/focus/pressed).

## Validation
Use the app's standard checks:
```bash
npm run build
npm run lint
```
Then verify representative screens for token resolution, spacing, typography, and color parity.

For `gts-central-library` itself, use:
```bash
bun run build
bun run lint
```
