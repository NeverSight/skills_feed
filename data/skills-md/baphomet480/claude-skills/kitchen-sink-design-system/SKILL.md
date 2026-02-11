---
name: kitchen-sink-design-system
description: Kitchen Sink design system workflow for any frontend stack — Next.js, Hugo, Astro, SvelteKit, Nuxt, or plain HTML. Use when asked for a Kitchen Sink page, Design System, UI Audit, Style Guide, or Component Inventory, or when a project needs a component inventory plus component creation and a sink page implementation.
---

# Kitchen Sink Design System

Build every component for real, wire it into a single sink page, and let the page prove the design system works.

## Core Philosophy

- **Source of truth** — The sink page is the canonical reference for design direction. If it's not in the sink, it doesn't exist.
- **No placeholders** — Every component rendered on the sink page must be a real, importable module. Never use draft placeholders or TODO stubs.
- **Layered semantics** — Every component follows a base + variant architecture. Shared structure in the base, visual differences in the variant layer.
- **Progressive disclosure** — Start with core primitives, layer in app-level components, finish with data display. Each tier builds on the last.
- **Design-forward** — Define design direction in the sink first; production pages consume what the sink establishes.
- **Agent-readable** — The design system should be equally consumable by human developers and AI coding agents. Semantic tokens, typed props, and explicit contracts over implicit conventions.
- **Framework-native** — Respect each framework's idioms. Don't impose React conventions on a Hugo project or vice versa.

## Phase 0: Detect Stack

Before anything else, identify the project's framework and lock in the implementation strategy. If you cannot see the file tree, stop and request it.

### Detection Signals

| Signal file / directory | Framework |
|---|---|
| `next.config.*`, `app/` or `pages/` | Next.js (React) |
| `hugo.toml`, `hugo.yaml`, `layouts/partials/` | Hugo |
| `astro.config.*`, `src/components/` | Astro |
| `nuxt.config.*` | Nuxt (Vue) |
| `svelte.config.*` | SvelteKit |
| None of the above | Static HTML/CSS |

### Strategy Table

Once detected, lock in these mappings for the rest of the workflow:

| Concept | React / Next.js | Hugo | Astro | Static HTML |
|---|---|---|---|---|
| **Component** | `.tsx` in `components/` | `.html` partial in `themes/<theme>/layouts/partials/components/` | `.astro` in `src/components/` | Reusable HTML snippet |
| **Component call** | `<Button variant="primary" />` | `{{ partial "components/button" (dict ...) }}` | `<Button variant="primary" />` | Copy/paste or `include` |
| **Props / params** | React props (TypeScript) | `dict` context | Astro props (TypeScript) | CSS classes / data-attrs |
| **Interactivity** | `useState`, event handlers | Alpine.js `x-data` or `<details>` | `client:load` + framework islands | Vanilla JS or Alpine.js |
| **Sink route** | `app/sink/page.tsx` | `content/sink/_index.md` + `themes/<theme>/layouts/sink/list.html` | `src/pages/sink.astro` | `sink.html` |
| **Prod guard** | `process.env` check → return `null` | Config overlay or `hugo.Environment` check | `import.meta.env` check | Don't deploy the file |
| **Shortcodes** | N/A (components serve both roles) | `themes/<theme>/layouts/shortcodes/` wrapping partials | Components usable in MDX | N/A |
| **Content authors** | Components in MDX | Shortcodes in markdown | Components in MDX / `.astro` | N/A |
| **Utility helper** | `cn()` via `clsx` + `tailwind-merge` | `classnames` partial or inline concat | `cn()` or `class:list` | Inline concat |

### Additional Detection Checks

After identifying the framework, also detect:

1. **CSS approach** — Tailwind (which version?), vanilla CSS, CSS modules, Sass, etc.
2. **Icon library** — Lucide, Heroicons, inline SVG, icon fonts, Hugo module, etc.
3. **Interactivity layer** — Alpine.js, HTMX, vanilla JS, React, Vue, Svelte, none.
4. **CMS** — TinaCMS (`tina/`), Decap/Netlify CMS (`static/admin/`), Sanity, Contentful, plain markdown, none.
5. **Existing component patterns** — Where do components live? What naming conventions are in use? Is there an existing helper like `cn()`?

Adapt all subsequent phases to what you detected. Do not impose one framework's conventions on another.

### Tailwind Detection

Detect which Tailwind version is in use, then read the appropriate source:

- **Tailwind v3** — Read `tailwind.config.js` / `tailwind.config.ts` for `theme.extend` (custom colors, spacing, fonts, breakpoints).
- **Tailwind v4** — No config file required. Read `globals.css`, `app.css`, or the project's main CSS entry for `@theme` blocks and CSS custom properties (`--color-*`, `--spacing-*`, `--font-*`). Also check for `@import "tailwindcss"` as a v4 indicator.
- **Detection heuristic:** If `tailwind.config.*` exists → v3. If the CSS entry contains `@theme` or `@import "tailwindcss"` → v4.
- **No Tailwind** — Read the project's main CSS for custom properties, Sass variables, or hardcoded values.

## Phase 0b: Design System Discovery

Before building anything, determine whether the project already has a documented design system or needs one created from scratch. This phase branches into two modes.

### Discovery Manifest

Scan the project root (and common subdirectories like `docs/`, `.github/`, `.cursor/`, `.agent/`) for any of these files:

**Brand & style guides:**
- `GEMINI.md`, `CLAUDE.md`, `AGENTS.md`, `COPILOT.md`
- `.cursorrules`, `.cursor/rules`
- `.github/copilot-instructions.md`
- `brand-guide.md`, `STYLE.md`, `BRAND.md`
- `design-tokens.json`, `tokens.css`, `tokens.json`
- `CONTENT_GUIDELINES.md`, `VOICE.md`, `BRAND_VOICE.md`

**Agent configuration files:**
- `.clinerules`, `.windsurfrules`
- `.agent/skills/*/SKILL.md`
- `README.md` (check for design system or brand sections)

**Hugo-specific:**
- `data/design-tokens.json`, `data/tokens.json`
- `assets/css/` for custom properties

If **any** of these contain design direction (colors, typography, voice, component patterns), enter **Adopt mode**. Otherwise, enter **Establish mode**.

### Adopt Mode — Existing Brand Guide

When the project already has documented design direction:

1. **Ingest** — Read all discovered guide files. Extract:
   - Color palette (named tokens with hex/HSL values)
   - Typography scale (font families, sizes, weights)
   - Spacing system (if documented)
   - Voice & tone adjectives
   - Component patterns already specified
2. **Map** — For every extracted token, identify:
   - The corresponding Tailwind config value, CSS custom property, or Hugo `data/` entry
   - Whether it's a **primitive** token (raw color: `--blue-500`) or **semantic** token (purpose: `--color-interactive`)
3. **Audit** — Scan existing components for drift:
   - Hardcoded hex values instead of tokens
   - Arbitrary Tailwind values (`w-[37px]`) instead of design scale
   - Inconsistent naming conventions
   - Missing dark mode support
4. **Surface gaps** — Report what the guide documents vs. what actually exists in code

### Establish Mode — No Guide Exists

When the project has no documented design system:

1. **Extract** — Scan existing CSS/Tailwind for de-facto tokens:
   - Run through `globals.css`, `tailwind.config.*`, component files (or Hugo's `assets/css/`, Astro's `src/styles/`)
   - Catalog every color, font, and spacing value actually in use
   - Identify the implicit palette and type scale
2. **Propose** — Generate a `design-tokens.md` with:
   - Discovered palette organized as primitive → semantic layers
   - Recommended additions to fill gaps (e.g., missing destructive color, no muted variant)
   - Type scale (H1–H6, body, caption) with sizes and weights
   - Spacing ramp mapped to Tailwind's scale (or CSS custom properties for non-Tailwind projects)
3. **Voice** — Define initial voice & tone:
   - Propose 3–5 voice adjectives based on the project's domain
   - Draft tone map for common UI states
   - Apply the project's franchise placeholder convention (per user rules)
4. **Approve** — Present the proposal to the user. Do NOT proceed to Phase 1 until tokens and voice are approved.

**Automated option:** Run `bash scripts/scan_components.sh [component_dir]` from the skill directory to get a Phase 0 discovery report + EXISTING / MISSING inventory against the tiered checklist.

**Reference:** [design-system-discovery.md](references/design-system-discovery.md)

## Phase 1: Inventory & Plan

Compare existing components against the tiered checklist. Mark each:
- **EXISTING** — import from codebase as-is
- **MISSING** — create the component, then wire it into the sink
- **SHORTCODE/MDX CANDIDATE** — if a component is meant for content authors (not just the sink), also create the content-author-facing wrapper (shortcode for Hugo, MDX export for React/Astro, etc.)

### Tier 1: Core Primitives (mandatory)

- Typography: H1–H6, paragraph, list (ol/ul), inline code, blockquote
- Buttons: primary, secondary, outline, ghost, destructive; sizes sm/md/lg; disabled state
- Badges / Tags: color variants, dismissible
- Avatars: image, initials fallback, sizes, status indicator
- Icons: render a sampler grid from the project's icon library
- Cards: basic, with header/footer, interactive (hover lift)
- Modals / Dialogs: trigger + overlay + close behavior
- Alerts / Toasts: info, success, warning, error variants
- Form controls: text input, textarea, select, checkbox, radio, toggle/switch, with label + error states

### Tier 2: Navigation & Layout (include when app-level complexity exists)

- Tabs: horizontal, with active/disabled states
- Breadcrumbs: with separator and current-page indicator
- Sidebar / Nav: collapsible, with active link
- Dropdown menu: trigger + item list + keyboard nav
- Accordion / Collapsible: expand/collapse with animation
- Tooltip / Popover: hover and click triggers
- Navigation patterns: header, sidebar, mobile menu
- Footer variants

### Tier 3: Content-Author Components (CMS-dependent)

Include when the site has a CMS or content authors who write markdown/MDX:

- Callout / admonition (info, warning, tip, caution)
- Figure / image with caption
- Button / CTA (link styled as button)
- Embed (YouTube, etc.)
- Card grid (n-up layout of cards from content)

For Hugo, each of these should have both a partial (for templates) and a shortcode (for content authors). For React/Astro, the component serves both roles via MDX.

### Tier 4: Data Display (include when data-heavy views exist)

- Table: sortable headers, striped rows, responsive scroll
- Stats / KPI cards: value, label, trend indicator
- Charts: placeholder pattern using the project's chart library (Recharts, Chart.js, etc.)
- Progress bar / Skeleton loaders: determinate and indeterminate states

## Phase 2: Layered Component Architecture

Every component — whether EXISTING or newly created — must follow the **base + variant** pattern. This makes components predictable for both humans and AI agents. The exact mechanism depends on the framework detected in Phase 0.

### React / Next.js — CVA Pattern

Use `class-variance-authority` (CVA) or an equivalent pattern to separate structural base classes from variant-specific classes:

```tsx
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils"; // clsx + tailwind-merge wrapper

// ── Base + Variants ──────────────────────────────────────────────
const buttonVariants = cva(
  // Base: shared structure (always applied)
  "inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        primary:     "bg-primary text-primary-foreground hover:bg-primary/90",
        secondary:   "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        outline:     "border border-input bg-transparent hover:bg-accent",
        ghost:       "hover:bg-accent hover:text-accent-foreground",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
      },
      size: {
        sm: "h-8 px-3 text-sm",
        md: "h-10 px-4 text-sm",
        lg: "h-12 px-6 text-base",
      },
    },
    compoundVariants: [
      { variant: "destructive", size: "lg", class: "font-semibold" },
    ],
    defaultVariants: {
      variant: "primary",
      size: "md",
    },
  }
);

// ── Component ────────────────────────────────────────────────────
interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

export function Button({ className, variant, size, ...props }: ButtonProps) {
  return (
    <button className={cn(buttonVariants({ variant, size }), className)} {...props} />
  );
}
```

### Hugo — Dict Context Pattern

Hugo components use Go template partials with a `dict` context contract. Document params in a comment block, use `| default` for optional params, build BEM classes from variant/size, and `delimit` to join. Call via `{{ partial "components/button" (dict "label" "Submit" "variant" "primary") }}`.

### Astro — Props Interface Pattern

Astro components define a TypeScript `Props` interface in frontmatter with defaults via destructuring. Build classes from variant/size, use `class:list` for merging. Pattern mirrors React CVA but uses Astro's native `Props` + `<slot />`.

### Static HTML — BEM + Data-Attribute Pattern

Use BEM class conventions (`.btn`, `.btn--primary`, `.btn--sm`) and document the contract in an HTML comment at the top of the file listing available classes and data attributes.

### Rules (All Frameworks)

1. **Base layer** — Shared structural classes: layout, border-radius, font-size, focus ring, transitions, disabled state. These NEVER change between variants.
2. **Variant layer** — Only what differs: colors, borders, shadows, backgrounds. Defined as named variants.
3. **Type / param export** — Always export the variant types (React: `VariantProps<>`, Hugo: param comment block, Astro: `Props` interface) so consumers (including AI agents) can discover available variants.
4. **Escape hatch** — Accept an additional class prop and merge it last so consumers can override when necessary.
5. **No raw conditionals** — Never use `isDestructive ? "bg-red-500" : "bg-blue-500"` inline. All visual branching goes through the variant API.

### Semantic Design Tokens

Components should reference **semantic** token names, not primitive color names:

| ❌ Primitive | ✅ Semantic |
|---|---|
| `bg-blue-500` | `bg-primary` |
| `text-gray-500` | `text-muted-foreground` |
| `border-red-500` | `border-destructive` |
| `bg-gray-100` | `bg-muted` |

The semantic layer means dark mode, theme changes, and brand pivots only require updating the token definitions — component code stays unchanged.

### Utility Fallback

If the project lacks a class-merging utility: **React** — add `cn()` via `clsx` + `tailwind-merge`. **Hugo** — create a `classnames.html` partial that filters and `delimit`s a slice. **Astro** — use built-in `class:list`. **Static** — inline concat or a tiny JS helper.

## Phase 3: Voice & Tone

Every design system needs content guidance. The sink page includes a **Voice & Tone** section covering:

- **Voice definition** — 3–5 adjectives defining the brand's consistent personality. Extract from existing guides or propose based on domain.
- **Tone map** — How tone adapts to user emotional states (pleased, neutral, confused, frustrated, first-time).
- **Content patterns** — Standard copy for empty states, error messages, success confirmations, loading states, destructive actions.
- **Franchise placeholders** — A pop-culture franchise for all placeholder content (form labels, sample data, empty states). Document in the sink header.

**Reference:** [voice-and-tone.md](references/voice-and-tone.md) — full templates, examples, and writing checklist.

## Phase 3b: Image & Illustration

Photography sourced from the web cannot be used directly (copyright, brand inconsistency). Define an **illustration style** and a **reinterpretation pipeline** to transform reference photos into brand-safe assets.

- **Define style** — Set rendering, palette, detail level, stroke, texture, and mood keywords during discovery. Document in the brand guide.
- **Reinterpretation pipeline** — Describe subject → strip photographer style → compose prompt with brand tokens → generate → validate against sink samples → optimize & store prompt.
- **Sink page section** — Include an Illustration Gallery with 3–5 canonical illustrations, a style definition card, and the generation prompt template.
- **Rules** — Never use unmodified photos. Always store the generation prompt alongside the asset. Every illustration gets descriptive alt text.

**Reference:** [image-reinterpretation.md](references/image-reinterpretation.md) — full pipeline, prompt templates, validation checklist, and sink page integration code.

## Phase 4: Motion & Interaction

Animation is the body language of the product. Define motion patterns in the sink for consistent, purposeful animation.

- **Principles** — Purposeful (no decorative animation), informative, consistent, respectful of `prefers-reduced-motion`.
- **Duration scale** — Define named tokens: `--duration-instant` (100ms), `--duration-fast` (200ms), `--duration-normal` (300ms), `--duration-slow` (500ms).
- **Easing curves** — `--ease-out` for entrances, `--ease-in` for exits, `--ease-in-out` for state changes.
- **Common patterns** — Hover lift, fade in, slide in, expand/collapse, skeleton shimmer, modal entrance/exit.
- **Reduced motion** — Always include `prefers-reduced-motion` media query or use Tailwind `motion-safe:`/`motion-reduce:` modifiers.
- **Sink section** — Include an interactive **Motion Sampler** demonstrating all patterns with their duration/easing tokens displayed.

**Reference:** [motion-guidelines.md](references/motion-guidelines.md) — full CSS/Tailwind code, keyframe definitions, Framer Motion patterns, and reduced-motion implementation.

## Phase 5: Build Components

For every **MISSING** item from Phase 1, create the component using the framework's native patterns.

### File Location & Naming

| Framework | Location | Convention |
|---|---|---|
| React / Next.js | `components/` or `components/ui/` | `Button.tsx`, `card.tsx` — match existing project convention |
| Hugo | `themes/<theme>/layouts/partials/components/` | `button.html`, `card.html` |
| Astro | `src/components/` | `Button.astro`, `Card.astro` |
| Static HTML | `components/` or `includes/` | `button.html`, `card.html` |

### Component Creation Standard (All Frameworks)

1. **Create the component** in the project's established component location with a stable export/interface.
2. **Document the interface** at the top of the file:
   - React: TypeScript interface or JSDoc props comment.
   - Hugo: Go template comment block listing expected `dict` keys, their types, and defaults.
   - Astro: TypeScript `Props` interface in frontmatter.
   - Static: Comment block describing expected classes/data attributes.
3. **Use design tokens** from the project's Tailwind config, CSS custom properties, or Hugo `data/` entries; avoid arbitrary/magic values.
4. **Keep components self-contained** — rely only on dependencies already in the project.
5. **Make interactive components actually interactive** using whatever the project's interactivity layer is:
   - React: `useState`, event handlers
   - Hugo: Alpine.js `x-data` or `<details>/<summary>` for zero-JS
   - Astro: `client:load` + framework islands
   - Static: vanilla JS, Alpine.js, or `<details>/<summary>`
6. **Apply the variant pattern** from Phase 2 (CVA for React, dict params for Hugo, Props for Astro).
7. **Apply voice & tone** patterns from Phase 3. Error messages answer what/why/fix. Empty states guide the user.
8. **Apply motion** patterns from Phase 4. Use the defined duration and easing tokens.
9. Wire the component into the sink page immediately. No placeholders.

### Content-Author Wrappers

When a component is marked as a **SHORTCODE/MDX CANDIDATE** in Phase 1:

- **Hugo** — Create a shortcode in `themes/<theme>/layouts/shortcodes/` that wraps the partial. Pass through all relevant parameters.
- **React / Astro** — The component itself is usable in MDX. Ensure it's exported from the project's MDX component registry.
- **Static** — Document usage instructions for copy/paste inclusion.

## Phase 6: Assemble Sink Page

Create the sink route file based on the framework detected in Phase 0.

### Sink Route Creation

**React / Next.js** — `app/sink/page.tsx`
- Add `"use client"` directive.
- Return `null` when `process.env.NEXT_PUBLIC_VERCEL_ENV === "production"`.
- Use `examples/minimal-sink.tsx` as a starter template.

**Hugo** — `content/sink/_index.md` + `layouts/sink/list.html`
- Frontmatter: `type: sink`, exclude from sitemap (`sitemap: exclude`), hide from nav.
- Layout: check `hugo.Environment` or `site.Params.showSink`; redirect in production.
- Preferred production guard: config overlay at `config/production/hugo.toml` with `showSink = false`.
- Use `examples/minimal-sink.html` as a starter template.

**Astro** — `src/pages/sink.astro`
- Check `import.meta.env.PROD` and return redirect or empty page.

**SvelteKit** — `src/routes/sink/+page.svelte`
- Use `$app/environment` to check for production.

**Nuxt** — `pages/sink.vue`
- Use `useRuntimeConfig()` to check environment.

**Static HTML** — `sink.html`
- Simply don't include in production deployment.

### Architecture Rules

- Never import other page/route files — only import components or define helpers locally.
- The sink page is a dev tool — exclude it from production, sitemap, RSS, search indexes, and navigation.

### Sink Page Layout

The sink page follows the same section structure regardless of framework. Adapt the syntax to match.

**Sections (in order):**

1. **Header** — Title, description, last-updated timestamp, franchise declaration
2. **Design Tokens** — Color palette (primitive → semantic), typography scale, spacing ramp
3. **Voice & Tone** — Voice definition, tone map, content pattern examples
4. **Illustration Gallery** — Canonical illustrations, reinterpretation examples, prompt template
5. **Site Header** — Rendered inline to test responsive breakpoints and nav states
6. **Site Footer** — Rendered inline to test link columns and brand consistency
7. **Typography** — H1–H6, body, caption, lists, blockquote, inline code
8. **Buttons** — All variants × sizes × states (variant grid)
9. **Badges** — Color variants, dismissible
10. **Cards** — Basic, with header/footer, interactive
11. **Form Controls** — All input types with label + error states
12. **Modals & Dialogs** — Working open/close demo
13. **Alerts** — All severity variants
14. **Motion Sampler** — Interactive demos of hover lift, fade, slide, expand/collapse
15. **Content-Author Specimens** — How shortcodes/MDX components render (if applicable)
16. **Tier 2 components** — Tabs, breadcrumbs, accordion, tooltip, dropdown (if applicable)
17. **Tier 4 components** — Table, stats cards, progress, skeleton (if applicable)
18. **Chaos Laboratory** — Token visualization, state matrix, dark/light side-by-side

### Chaos Laboratory

1. **Token visualization** — Programmatically render design tokens (colors, spacing).
   - React: Import resolved config via `resolveConfig`.
   - Hugo: Export tokens to `data/design-tokens.json` at build time, read with `site.Data`.
   - Astro: Import config in frontmatter.
   - Static: Maintain a JSON file manually or generate with a script.
2. **State matrix** — Render variants side by side (default, hover, focus, disabled, active).
3. **Theme test** — Light and dark columns, forced via wrapper class.
4. **Responsive stubs** — `iframe` containers with fixed widths (320px, 768px) to verify mobile layouts.

## Phase 7: Verify

Run these checks before considering the sink complete. Commands vary by framework.

### Automated Checks

| Framework | Build | Lint |
|---|---|---|
| Next.js | `pnpm build` | `pnpm lint` |
| Hugo | `hugo --minify` | `hugo --templateMetrics` (check for template errors) |
| Astro | `pnpm build` | `pnpm lint` |
| SvelteKit | `pnpm build` | `pnpm lint` |
| Nuxt | `pnpm build` | `pnpm lint` |
| Static | N/A | HTML validator |

Optional accessibility audit: `pnpm dlx @axe-core/cli http://localhost:<port>/sink`

### Manual Checklist

- [ ] **A. Completeness** — Every Tier 1 item is present. Tier 2/3/4 items included where relevant.
- [ ] **B. Real components** — Every rendered element is imported from the project's component location (no inline-only markup pretending to be a component).
- [ ] **C. Layered architecture** — Every component uses the framework-appropriate variant pattern (CVA for React, dict params for Hugo, Props for Astro, BEM for static).
- [ ] **D. Semantic tokens** — No hardcoded hex values or primitive color names in component code.
- [ ] **E. Interactivity** — Modals open, toggles toggle, tabs switch, dropdowns expand. Every stateful component works.
- [ ] **F. Voice & tone** — Content patterns documented. Error messages answer what/why/fix. Empty states guide the user.
- [ ] **G. Motion** — Animations use defined duration/easing tokens. `prefers-reduced-motion` respected.
- [ ] **H. Theming** — Dark/light columns render correctly. No hard-coded colors bypassing tokens.
- [ ] **I. Production guard** — Sink page is excluded from production via the framework's native mechanism.
- [ ] **J. No import cycles** — Sink page does not import any page/route file.
- [ ] **K. Content-author wrappers** — Shortcodes/MDX exports pass through all relevant parameters (if applicable).

## CMS Notes

The sink page is **never** CMS-managed — it's a developer tool.

However, when a CMS is present, content-author-facing components (Tier 3) should respect the CMS content model:

- **TinaCMS** — Component params should align with the fields defined in `tina/config.ts` collections. Note: TinaCMS visual editing requires React — in Hugo projects, Tina functions only as a markdown/frontmatter editor GUI.
- **Decap CMS** — Component params should map to widget types in `static/admin/config.yml`.
- **MDX-based CMS** (Contentful, Sanity, etc.) — Exported components should match the expected props shape from the CMS schema.

## AI Agent Readiness

Ensure the design system is consumable by AI agents: use semantic tokens over primitives, store tokens in CSS custom properties and/or JSON, export typed props as the API contract, use purpose-based naming (`text-muted-foreground` not `gray-light`), reference tokens in the project's rules file (`CLAUDE.md`, `.cursorrules`, etc.), and treat the sink page as the single source of truth.

## Companion Skills

When available, leverage: **design-lookup** for CSS components, SVG icons, and design inspiration during Establish mode. **Frontend/brand identity skills** for project-specific visual identity constraints during discovery. **deep-research** for evaluating design system approaches from scratch. This skill acts as the **integrator** — consuming companion skill outputs and codifying them into the component library and sink page.

## Anti-patterns

- **Draft placeholders** — `{/* TODO: add button */}` is never acceptable. Build the real component.
- **Arbitrary Tailwind values** — `w-[35px]` or `text-[#ff0000]` instead of using config tokens.
- **Raw conditional classes** — `isDestructive ? "bg-red-500" : "bg-blue-500"` instead of using variants.
- **Importing page files** — `import X from "../other-page/page"` creates coupling and build issues.
- **Skipping tiers** — Don't jump to Tier 4 charts before Tier 1 buttons exist.
- **Static mockups** — A modal that doesn't open, a toggle that doesn't toggle, a tab bar that doesn't switch.
- **One-off inline components** — If it's rendered in the sink, it belongs in the component directory as an importable module.
- **Appearance-based token names** — `blue-primary` instead of `color-interactive`. Semantic names survive brand pivots.
- **Missing voice guidance** — A sink without content patterns is only half a design system.
- **Decorative animation** — Motion without purpose. Every animation should inform or guide.
- **Framework mismatch** — Imposing React idioms (JSX, hooks) on a Hugo or static HTML project.

## Reference

For detailed per-component specs (expected props, variants, states, accessibility), the sink page section template, and concrete code examples:

- **Components:** [component-catalog.md](references/component-catalog.md)
- **Discovery:** [design-system-discovery.md](references/design-system-discovery.md)
- **Voice & Tone:** [voice-and-tone.md](references/voice-and-tone.md)
- **Image & Illustration:** [image-reinterpretation.md](references/image-reinterpretation.md)
- **Motion:** [motion-guidelines.md](references/motion-guidelines.md)
