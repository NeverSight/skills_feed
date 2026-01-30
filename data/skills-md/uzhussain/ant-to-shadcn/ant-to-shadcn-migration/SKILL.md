---
name: ant-to-shadcn-migration
description: Migrate Ant Design UIs to shadcn/ui + Tailwind (React/CRA/Vite → Next.js App Router) with layout/page skeleton generation, component mapping, and aggressive legacy CSS cleanup guidance.
license: MIT
metadata:
  author: community
  version: "0.1.0"
---

# Ant Design to shadcn/ui Migration Guide

Comprehensive guide for migrating legacy Ant Design frontends to shadcn/ui + Tailwind (Radix under the hood), covering component equivalence, theming/tokens, layout/navigation, forms/tables, overlays/alerts, accessibility, and bundle-size cleanup. Targets React (CRA/Vite) apps moving to Next.js App Router, with patterns for running Ant and shadcn side-by-side during transition. Includes automated skeleton generation guidance for fresh layouts/pages with role-aware routing.

## When to Apply

- Migrating a CRA/Vite React app that uses Ant Design to Next.js App Router with shadcn/ui.
- Replacing Ant Design components with shadcn/ui (and Radix) while moving styling to Tailwind and design tokens.
- Cleaning up legacy global CSS/LESS, z-index stacks, and inline styles that conflict with Tailwind/shadcn.
- Generating fresh layout/page skeletons per route (optionally role-aware) to reduce legacy cruft.

## Version Policy

Use the latest stable versions of:
- `next` ≥ 16.x (App Router)
- `react` ≥ 19.x
- `tailwindcss` ≥ 3.4.x
- `shadcn/ui` latest
- `@radix-ui` packages as pulled by shadcn/ui
- `class-variance-authority`, `tailwind-merge`, `lucide-react`, `sonner`
- `react-hook-form` ≥ 7.x and `zod` ≥ 3.x for forms (recommended)

## Rule Categories by Priority

| Priority | Category                            | Impact   | Prefix          | Rules |
| -------- | ----------------------------------- | -------- | --------------- | ----- |
| 1        | Setup & Dependencies                | CRITICAL | `setup-`        | 5     |
| 2        | Design Tokens & Theming             | CRITICAL | `theme-`        | 2     |
| 3        | Layout & Navigation (Responsive)    | HIGH     | `layout-`       | 3     |
| 4        | Forms & Validation                  | HIGH     | `forms-`        | 3     |
| 5        | Data Display (Tables/Lists)         | HIGH     | `data-`         | 2     |
| 6        | Feedback & Overlays                 | HIGH     | `overlay-`      | 2     |
| 7        | Content, Icons, Typography          | MEDIUM   | `content-`      | 1     |
| 8        | Styling & CSS Cleanup               | MEDIUM   | `css-`          | 2     |
| 9        | Accessibility, Responsiveness & Interop | MEDIUM | `a11y-`         | 4     |
| 10       | Testing & Verification              | LOW      | `test-`         | 2     |
| 11       | Common Gotchas                      | HIGH     | `gotchas-`      | 3     |

## Component Equivalence (Matrix)

| Ant Design 6.x        | shadcn/ui + Tailwind (or pattern)                           | Notes |
| --------------------- | ----------------------------------------------------------- | ----- |
| Button                | `Button`, `ButtonGroup`                                     | |
| FloatButton           | `Button` with fixed/absolute + shadow                       | |
| Icon                  | `lucide-react`                                              | Drop Ant icons |
| Typography            | Tailwind text utilities; `Typography` classes               | |
| Divider               | `Separator`                                                 | |
| Flex/Grid/Masonry     | Tailwind flex/grid; CSS masonry if needed                   | |
| Layout, Space, Splitter| Tailwind stack/gap; custom splitter with `Resizable`        | |
| Anchor                | `NavigationMenu`/`ScrollArea` or manual anchor links        | |
| Breadcrumb            | `Breadcrumb`                                                | |
| Dropdown              | `DropdownMenu`                                              | |
| Menu                  | `NavigationMenu` or `Sheet` nav                             | |
| Pagination            | `Pagination`                                                | |
| Steps                 | Custom flex steps                                           | |
| Tabs                  | `Tabs`                                                      | |
| AutoComplete/Mentions | `Combobox`/`Command`                                        | |
| Cascader/TreeSelect   | `Combobox` with grouped/indented options                    | |
| Checkbox/Radio        | `Checkbox`, `RadioGroup`                                    | |
| ColorPicker           | Custom popover + color input                                | |
| DatePicker/TimePicker | `Calendar` + `Popover`, time input                          | |
| Form/Form.Item        | `Form` (RHF) + shadcn fields                                | |
| Input/InputNumber     | `Input` (number type), `InputGroup`                         | |
| Rate                  | Custom star row using `Button`/`Toggle`                     | |
| Select                | `Select` or `Combobox`                                      | |
| Slider/Switch         | `Slider`, `Switch`                                          | |
| Transfer              | Dual list with checkboxes and buttons                       | |
| Upload                | File input + dropzone + progress                            | |
| Avatar                | `Avatar`                                                    | |
| Badge/Tag             | `Badge`                                                     | |
| Calendar              | `Calendar`                                                  | |
| Card                  | `Card`                                                      | |
| Carousel              | `Carousel`                                                  | |
| Collapse              | `Accordion`                                                 | |
| Descriptions          | Definition list with grid/flex                              | |
| Empty                 | `Empty` or custom empty block                               | |
| Image                 | `img` with Tailwind classes                                 | |
| List                  | Cards/grid/flex list                                        | |
| Popover/Tooltip       | `Popover`, `Tooltip`                                        | |
| QRCode                | Use QR library + `Card`                                     | |
| Segmented             | `ToggleGroup`                                               | |
| Statistic             | `Card` + text/metric styling                                | |
| Table                 | tanstack + `Table`                                          | |
| Timeline              | Custom vertical list with bullets                           | |
| Tour                  | Custom popover walkthrough (command + popover)              | |
| Tree                  | Indented list + checkboxes; virtualize if large             | |
| Alert                 | `Alert`                                                     | |
| Drawer                | `Sheet`                                                     | |
| Message/Notification  | `toast`/`sonner`                                            | |
| Modal/Popconfirm      | `Dialog` / `AlertDialog`                                    | |
| Progress              | `Progress`                                                  | |
| Result                | `Alert` success/error block                                 | |
| Skeleton/Spin         | `Skeleton` or spinner utility                               | |
| Watermark             | CSS background or canvas overlay                            | |
| Affix                 | `sticky` positioning                                        | |
| App/ConfigProvider/Util| Not needed; use shadcn/Tailwind tokens and providers       | |
| Pro* (ProTable, etc.) | Compose with tanstack table + filters/forms + cards         | |

### Notes on gaps
- Rate: star toggles via `Button`/`Toggle`.
- Transfer: dual list with checkboxes and CTA buttons.
- QRCode: use a QR library; render inside `Card`.
- Tour: custom step popovers anchored to elements.
- Watermark: CSS `background-image` or canvas; keep scoped.
- Affix: `position: sticky` on containers.
- Tree: indented list; add virtualization for large sets.
- Pro* suites: rebuild via tanstack table + forms + cards; no direct shadcn equivalent.
- ConfigProvider/App/Util: not needed; use Tailwind/shadcn tokens and providers already configured.
- Masonry: CSS columns or grid with `grid-auto-rows` + spans.
- Statistic: simple text/number in `Card` with muted labels.
- Shadcn-only (helpful replacements): `Command`/`Combobox` for search/select; `Sonner` for toasts; `Menubar`/`Sidebar` for complex nav; `Spinner` for lightweight loading; `Chart` (community/blocks) where Ant charts were used; `Input OTP` for code entry; `Field`/`Textarea` for richer forms.

## Migration Order

0) Verify/upgrade Ant to latest 6.x before mapping (align with [Ant components](https://ant.design/components/overview/)).
1) Setup: Tailwind/shadcn install, deps, project structure, shadcn MCP server ready.
2) CSS Cleanup: Identify global/LESS/inlined styles; decide what to keep; add base resets and z-index tokens.
3) Theming: Map Ant tokens → CSS vars/Tailwind theme; dark mode guardrails; spacing/radius/typography scales.
4) Layout/Nav (Responsive): Rebuild layouts/nav/breadcrumbs with desktop/tablet/mobile variants; role-aware scaffolding; drawer-on-mobile.
5) Forms: Convert `Form.Item` patterns to shadcn + react-hook-form + zod; validation and submission states; success/failure/inline errors.
6) Data Display: Tables/lists/empty states; pagination/sorting/filtering patterns; loading/skeleton/error states.
7) Overlays/Feedback: Dialogs/sheets/popovers/tooltips/toasts/alerts/spinners with z-index scale.
8) Content/Icons: Replace Ant icons/typography with lucide and Tailwind text styles; see `content-icons-typography`.
9) Accessibility/Interop: Focus traps, keyboard nav, ARIA, responsive checks; safe coexistence during phased rollout; see `a11y-responsive-checks`, `a11y-motion-contrast`, `responsive-touch`, `rtl-l10n`.
10) Testing/Verification: Visual checks, a11y scans, bundle/size linting, API/error-path checks; prefer modern UX fallbacks over 1:1 Ant copies when overlays/patterns conflict (`gotchas-ux-fallbacks`).
11) Performance/Bundle: verify Ant CSS/icons absent; use lucide; virtualize large tables/lists to avoid jank (`perf-bundle-guard`).
12) Observability: keep analytics/error logging when refactoring flows; don’t drop events when swapping notifications with toasts (`analytics-observability`).
13) Scroll/State: guard useEffect/init to avoid state resets; use stable handlers and shadcn ScrollArea for section navigation (`gotchas-scroll-state`).

## Scans and Mapping

Run scans to route findings to rules:
- `antd` imports and package version → `setup-antd-upgrade`, `setup-`, `css-legacy`, `theme-bridge`, component mappings.
- `ConfigProvider`, `theme.useToken` → `theme-bridge`, `theme-dark-mode`, `css-layering`.
- Global CSS/LESS (`*.less`, `global.css`, `index.css`) → `css-legacy-inventory`, `css-layering`, `css-asset-hygiene`.
- Inline `style=` with Ant tokens → `theme-bridge`, `css-inline-cleanup`.
- `Layout.Sider`, `Menu`, `Breadcrumb` → `layout-shell`, `layout-nav`.
- `Form`, `Form.Item`, `message`, `notification`, `Modal.confirm` → `forms-*`, `overlay-*`, `gotchas-ux-fallbacks`.
- `Table`, `List`, `Descriptions`, `Tag`, `Badge`, `Empty` → `data-*`, `components-*` (pagination/result/empty), `data-table-tanstack`.
- Route configs/menus/guards → `layout-route-scaffold`, `layout-auth-discovery`, `gotchas-coexistence`.
- Auth/roles (Clerk/Supabase/cookies/hooks), router guards, landing vs app shell → `layout-auth-discovery`.
- `@ant-design/icons`, global Ant CSS, LESS files → `content-icons-typography`, `css-legacy-inventory`, `perf-bundle-guard`.
- Dark-mode selectors or toggles → `theme-dark-mode-guardrails`.
- Public assets references → `css-asset-hygiene`, `assets-images`.
- Fonts → `fonts-setup`.
- Scroll/section nav code → `gotchas-scroll-state`.
- Reduced motion/contrast/focus → `a11y-motion-contrast`, `a11y-responsive-checks`, `responsive-touch`.
- RTL/l10n → `rtl-l10n`.
- Analytics/logging → `analytics-observability`.

### Quick scan commands (adjust paths as needed)
```bash
# Ant version
npm ls antd

# Ant imports and icons
rg \"antd\" src app
rg \"@ant-design/icons\" src app

# ConfigProvider and tokens
rg \"ConfigProvider\" src app
rg \"theme\\.useToken\" src app

# Ant imperative APIs
rg \"Modal\\.confirm\" src app
rg \"notification\\.\" src app
rg \"message\\.\" src app

# Table/columns
rg \"columns\\s*=\\s*\\[\" src app

# LESS and global CSS
rg --files -g\"*.less\" src app
rg \"global\\.css\" src app

# Dark mode selectors
rg \"\\.dark\" src app

# Assets and fonts
rg --files -g\"*.{png,jpg,jpeg,svg}\" public/ src app
rg \"font-family\" src app

# Responsive/touch/scroll
rg \"overflow\" src app
rg \"scrollIntoView\" src app

# Routes/guards/menus
rg \"<Router\" -g\"*.tsx\" src app
rg \"RequireAuth|useAuth|Clerk|Supabase\" src app
rg \"menu\" src app/components

# Analytics/logging
rg \"track|analytics|logEvent\" src app
```

## Post-Migration Verification (UI-first)

- Shell/nav: responsive desktop/tablet/mobile; active states; breadcrumbs; role-guarded routes.
- Forms: validation + error/success toasts; disabled states; loading indicators; keyboard focus order; screen reader labels.
- Tables/lists: empty/loading/error/skeleton states; pagination/sort/filter; row focus/hover.
- Overlays/toasts: focus trap, ESC/close, return focus; z-index layering; no console errors on open/close.
- Theming: light/dark parity; token application (colors/spacing/radius); contrast and focus outlines.
- CSS sanity: no leaking global styles; no unexpected z-index overlaps; Ant CSS isolated or removed; legacy UI parked separately.
- Performance: bundle size reduced (no Ant CSS), tree-shaking verified.

## Rule Index (by prefix)

- Setup: `setup-antd-upgrade`, `setup-shadcn-install`, `setup-shadcn-mcp`, `setup-legacy-parking`, `build-env`
- Theme: `theme-bridge-tokens`, `theme-dark-mode-guardrails`
- Layout: `layout-route-scaffold`, `layout-responsive-shell`, `layout-auth-discovery`
- Forms: `forms-rhf-shadcn`, `forms-api-states`, `forms-select-date-upload`
- Data: `data-tables-state`, `data-table-tanstack`, `components-pagination`, `components-result-empty`
- Overlays: `overlay-alerts-toasts`, `overlay-toast-console`
- Components (augment data/overlay): `components-tabs-steps`, `components-tree-cascader`, `components-upload`, `components-pagination`, `components-result-empty`
- Content: `content-icons-typography`
- Styling: `css-legacy-inventory`, `css-asset-hygiene`, `assets-images`, `fonts-setup`
- Accessibility/Responsive: `a11y-responsive-checks`, `a11y-motion-contrast`, `responsive-touch`, `rtl-l10n`
- Performance: `perf-bundle-guard`
- Testing: `test-visual-a11y`, `test-e2e-visual`
- Gotchas: `gotchas-coexistence`, `gotchas-ux-fallbacks`, `gotchas-scroll-state`
- Other: `analytics-observability`

## How to Use

1) Run scans to inventory Ant usage, CSS/LESS, routes/roles, and inline styles.
2) Apply rules by category (see `rules/`), starting with setup, CSS cleanup, theming, then layout/forms/data/overlays.
3) Generate new App Router layouts/pages per route with shadcn skeletons; migrate features incrementally; keep Ant components only where not yet migrated (side-by-side strategy).
4) Verify with the post-migration checklist; add visual/a11y snapshots where possible.

### Structure readiness check (reuse vs fresh scaffold)
- Reuse existing structure if: routes/nav/breadcrumb data are centralized; CSS/LESS is scoped/minimal; assets/fonts are organized; guards/roles are discoverable and centralized.
- Fresh scaffold if: routing/layouts are unclear, Ant CSS bleeds globally, assets/styles are scattered, or guards/roles are ad-hoc.
- Always run scans first (antd imports, ConfigProvider, LESS, icons, overflow/scroll, assets/fonts, routes/guards, analytics) to inform the choice.

### Component sourcing (shadcn-first)
- Install components via shadcn CLI/MCP (registry) only; do not hand-roll replacements if a shadcn component/block exists.
- Prefer shadcn MCP for updated patterns/blocks; avoid custom ad-hoc builds unless the component does not exist in the registry.
- Keep installs tracked in `components.json` and use `npx shadcn@latest` for additions.
