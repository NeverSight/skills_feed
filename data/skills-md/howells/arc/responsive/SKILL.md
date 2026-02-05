---
name: responsive
description: |
  Audit and fix responsive/mobile issues across every page of a project, using Chrome MCP
  screenshots at two breakpoints (375px mobile, 1440px desktop). Design-aware: reads existing
  design docs to preserve aesthetic intent, not just "make it fit."
  Use when asked to "make it responsive", "fix mobile", "responsive audit", or after building
  a desktop-first UI that needs mobile adaptation.
license: MIT
metadata:
  author: howells
website:
  order: 13
  desc: Mobile responsive audit & fix
  summary: Systematically audit and fix every page for mobile responsiveness, with visual verification via browser screenshots.
  what: |
    Responsive discovers all routes in your project, then works through each page with a tight loop: screenshot at mobile width, identify issues, fix them in code, re-screenshot to verify, then check desktop hasn't broken. It reads your design doc first so fixes preserve your aesthetic direction—typography hierarchy, memorable elements, spacing system—not just make things fit on a small screen. Uses container queries for reusable components and viewport queries for page layout.
  why: |
    Desktop-first is a valid workflow, but the "make it responsive later" pass is tedious and error-prone. You resize the browser, spot something broken, fix it, accidentally break desktop, fix that, move to the next page, miss three others. This skill automates the systematic part so you can focus on the design decisions.
  decisions:
    - Two breakpoints only. 375px mobile and 1440px desktop catches 95% of issues. Tablet deferred to v2.
    - Design-aware. Reads your design doc first to preserve aesthetic intent, not just fix layout.
    - Chrome MCP required. No fallback path—single code path, already the Arc standard.
    - Container queries for components. Reusable components adapt to their container, not the viewport.
---

<tool_restrictions>
# Tool Restrictions

**Do NOT use the `EnterPlanMode` tool.** This skill manages its own workflow and writes results directly. Claude's built-in plan mode would bypass this process.

**Do NOT use the `ExitPlanMode` tool.** This skill is never in plan mode.

**ALWAYS use the `AskUserQuestion` tool for questions.** Never ask questions as plain text in your response. Every question to the user — whether confirming routes, choosing options, or validating fixes — MUST use the `AskUserQuestion` tool. This enforces one question at a time and prevents walls of text. If you need to provide context before asking, keep it to 2-3 sentences max, then use the tool.
</tool_restrictions>

# Responsive Audit & Fix

Systematically audit and fix every page for mobile responsiveness, with visual verification via Chrome MCP screenshots.

**Announce at start:** "I'm using the responsive skill to audit and fix mobile responsiveness across your project."

---

## Phase 1: Setup & Discovery

### Step 1: Check Chrome MCP

Attempt to use `mcp__claude-in-chrome__tabs_context_mcp` to verify Chrome MCP is available.

**If Chrome MCP is unavailable:**
Tell the user: "This skill requires the Claude in Chrome extension for screenshot-based verification. Please install it and try again."
**Stop.**

### Step 2: Confirm Dev Server

```
AskUserQuestion:
  question: "What's your dev server URL?"
  header: "Dev server"
  options:
    - label: "localhost:3000"
      description: "Default Next.js dev server"
    - label: "localhost:5173"
      description: "Default Vite dev server"
    - label: "localhost:4321"
      description: "Default Astro dev server"
```

Then verify the server is running:
```
mcp__claude-in-chrome__tabs_context_mcp (get or create tab)
mcp__claude-in-chrome__navigate to the dev server URL
mcp__claude-in-chrome__computer action=screenshot
```

If the page doesn't load, tell the user to start their dev server and try again.

### Step 3: Load Design Context

**Read design doc (if exists):**
```
Glob: docs/plans/design-*.md
```

If found, read the design doc and note:
- **Aesthetic direction** (tone, memorable element)
- **Typography hierarchy** (display, body, mono fonts)
- **Spacing system** (base unit, scale)
- **Color palette** (so you don't introduce new colors)

This context guides every fix decision. If there's no design doc, that's fine — apply general responsive best practices from the interface rules.

**Read interface rules:**
1. `${CLAUDE_PLUGIN_ROOT}/rules/interface/layout.md`
2. `${CLAUDE_PLUGIN_ROOT}/rules/interface/interactions.md`
3. `${CLAUDE_PLUGIN_ROOT}/rules/interface/spacing.md`

### Step 4: Discover Routes

**Detect framework:**

| Check | Grep Pattern | Framework |
|-------|-------------|-----------|
| `"next"` in `package.json` | Next.js | `app/**/page.{tsx,jsx}` |
| `"@remix-run"` in `package.json` | Remix | `app/routes/**/*.{tsx,jsx}` |
| `"astro"` in `package.json` | Astro | `src/pages/**/*.{astro,mdx}` |
| `"@sveltejs/kit"` in `package.json` | SvelteKit | `src/routes/**/+page.svelte` |

**Scan for page files** using the appropriate glob pattern. Exclude API routes (`app/api/**`).

**Build route list** from file paths:
- `app/page.tsx` → `/`
- `app/about/page.tsx` → `/about`
- `app/blog/[slug]/page.tsx` → `/blog/[slug]` (dynamic)
- `app/dashboard/page.tsx` → `/dashboard` (may need auth)

**Flag dynamic routes** — these need sample values from the user.

**Flag potentially auth-protected routes** — routes under common auth-gated paths like `/dashboard`, `/settings`, `/account`, `/admin`.

### Step 5: Confirm Routes with User

Present the discovered routes:

```
AskUserQuestion:
  question: "I found these routes. Any to skip?"
  header: "Routes"
  multiSelect: true
  options:
    - label: "/ (homepage)"
      description: "Public page"
    - label: "/about"
      description: "Public page"
    - label: "/blog/[slug]"
      description: "Dynamic — I'll need a sample slug"
    - label: "/dashboard"
      description: "May need auth — log in via Chrome first"
```

**If dynamic routes exist**, ask for sample slugs:
```
AskUserQuestion:
  question: "What slug should I use for /blog/[slug]?"
  header: "Sample URL"
  options:
    - label: "first-post"
      description: "Use /blog/first-post"
    - label: "hello-world"
      description: "Use /blog/hello-world"
```

**If auth-protected routes exist:**
Tell the user: "Some routes may need authentication. Please log in via the Chrome browser, then let me know when you're ready."

```
AskUserQuestion:
  question: "Are the auth-protected routes ready to audit?"
  header: "Auth"
  options:
    - label: "Yes, I'm logged in"
      description: "Continue with all routes including auth-protected ones"
    - label: "Skip auth routes"
      description: "Only audit public pages for now"
```

---

## Phase 2: Page-by-page Audit & Fix

Work through each confirmed route. The loop is tight: **screenshot → analyze → fix → verify → check desktop → next page.**

### For Each Page:

#### Step 1: Mobile Screenshot (375x812)

```
mcp__claude-in-chrome__navigate to [dev-server-url]/[route]
mcp__claude-in-chrome__resize_window width=375 height=812
mcp__claude-in-chrome__computer action=wait duration=2
mcp__claude-in-chrome__computer action=screenshot
```

Wait briefly for any animations or lazy-loaded content to settle before screenshotting.

#### Step 2: Analyze the Screenshot

Look at the screenshot and evaluate against these categories:

**Layout:**
- Horizontal overflow (content wider than viewport, horizontal scrollbar)
- Elements overlapping or clipping
- Grids/flexbox not stacking properly
- Fixed-width elements that don't fit

**Spacing:**
- Content touching container edges (needs padding)
- Inconsistent gaps between elements
- Sections too cramped or too sparse for mobile

**Typography:**
- Body text smaller than 16px (hard to read on mobile)
- Headings that are too large and cause overflow
- Typography hierarchy lost (everything looks the same size)

**Usability:**
- Touch targets smaller than 44x44px (buttons, links, icons)
- Input fields without `text-base` (causes iOS auto-zoom)
- Missing viewport meta tag
- Hover-dependent functionality with no touch alternative

**Design intent (if design doc was loaded):**
- Does the page still feel like the same design at mobile width?
- Is the memorable element preserved (even if scaled)?
- Are the documented spacing values being used (not arbitrary new values)?
- Is the typography hierarchy intact (scaled down proportionally, not collapsed)?

#### Step 3: Fix Issues

Apply fixes in code. Follow these principles:

**Container queries for component-level fixes:**
Use `@container` when fixing a reusable component (card, sidebar, content block, form layout). This makes the component adapt to its container rather than the viewport, so it works in any layout context.

**Viewport queries for page-level layout:**
Use viewport media queries (`@media`) when fixing page structure — grid column counts, section stacking order, navigation collapse, page-level padding.

**Use existing spacing values:**
Reference `rules/interface/spacing.md`. Use the Tailwind spacing scale (4, 8, 12, 16, 24, 32, 48, 64). Never invent new spacing values like 13px or 27px.

**Use `h-dvh` not `h-screen`:**
Reference `rules/interface/layout.md`. Dynamic viewport height respects mobile browser chrome.

**Gate hover styles:**
Reference `rules/interface/interactions.md`. Use `@media(hover:hover)` so hover effects don't fire on touch devices.

**Shared components:**
If you recognize the same component causing issues across multiple pages, fix the component source file rather than adding page-specific overrides. This is the natural, correct approach — not a special detection system.

#### Step 4: Verify Mobile Fix

After applying fixes:

```
mcp__claude-in-chrome__computer action=screenshot
```

Compare visually to the pre-fix screenshot. Are the issues resolved? If not, iterate.

#### Step 5: Desktop Regression Check (1440x900)

```
mcp__claude-in-chrome__resize_window width=1440 height=900
mcp__claude-in-chrome__computer action=screenshot
```

**Verify desktop is intact.** The fix should not have broken the desktop layout. Check:
- Grid layouts still multi-column
- Spacing still generous (not collapsed)
- Typography still at desktop scale
- No visual artifacts from responsive changes

**If desktop broke:** Fix the regression, then re-verify at both 375px and 1440px before moving on.

#### Step 6: Scroll Check

For pages longer than the viewport:

```
mcp__claude-in-chrome__resize_window width=375 height=812
mcp__claude-in-chrome__computer action=scroll scroll_direction=down scroll_amount=5
mcp__claude-in-chrome__computer action=screenshot
```

Repeat scrolling and screenshotting until you've covered the full page. Look for below-the-fold issues:
- Footer overflow
- Long content sections with broken layout
- Images or embeds that don't fit
- Sticky/fixed elements obscuring content

#### Step 7: Next Page

Move to the next route in the list and repeat from Step 1.

**Progress update:** After each page, briefly note what was fixed: "Homepage: fixed hero grid and nav. Moving to /about."

---

## Phase 3: Summary & Commit

### Step 1: Present Change Summary

After all pages are audited and fixed, present a summary grouped by page and shared component:

```
## Responsive Fixes Applied

### / (homepage)
- Fixed hero grid: 3-column → single-column on mobile (container query on HeroCard)
- Fixed nav: added mobile sheet menu via viewport query
- Fixed section padding: p-4 on mobile, p-16 on desktop

### /about
- Fixed image overflow: added max-w-full to team photos
- Fixed touch targets on CTA buttons: expanded hit area to 44px

### /blog/first-post
- Fixed prose width: constrained to viewport on mobile
- Fixed code blocks: added overflow-x-auto

### Shared: components/Card.tsx
- Added @container query for horizontal → vertical layout below 400px

### Shared: components/Navigation.tsx
- Added mobile sheet menu pattern with viewport query
```

### Step 2: Commit

Batch commit all responsive fixes:

```bash
git add .
git commit -m "fix: responsive fixes across [N] pages

- [Brief list of key changes]
- Container queries for [components]
- Viewport queries for [page layouts]"
```

### Step 3: Optional Audit Document

```
AskUserQuestion:
  question: "Want me to save a responsive audit doc with all issues found and fixes applied?"
  header: "Audit doc"
  options:
    - label: "Yes, save audit doc"
      description: "Write to docs/plans/responsive-audit.md for future reference"
    - label: "No, the commit is enough"
      description: "Skip the audit doc"
```

If yes, write `docs/plans/responsive-audit.md` with the full change summary, and commit it.

### Step 4: Final Desktop Verification

Do one final pass: resize to 1440x900 and quickly navigate through all audited pages to confirm everything looks correct at desktop width. This catches any cumulative issues from the page-by-page fixes.

```
mcp__claude-in-chrome__resize_window width=1440 height=900
```

Navigate to each page and take a quick screenshot. If anything looks off, fix and re-commit.

---

<success_criteria>
Responsive audit is complete when:
- [ ] Chrome MCP connected and dev server verified
- [ ] Design doc read (if exists) for aesthetic context
- [ ] Interface rules loaded (layout, interactions, spacing)
- [ ] Routes discovered and confirmed with user
- [ ] Each page screenshotted at 375px (mobile)
- [ ] Issues identified and fixed per page
- [ ] Each fix verified with re-screenshot at mobile
- [ ] Desktop (1440px) checked after mobile fixes — no regressions
- [ ] Final desktop pass across all pages
- [ ] Changes committed
- [ ] Activity log updated
</success_criteria>

## Interop

- Invoked after `/arc:implement` — the natural post-build polish step
- Reads design docs from `/arc:design` for aesthetic context
- References `rules/interface/layout.md`, `interactions.md`, `spacing.md` for implementation patterns
- Uses **Chrome MCP** (`mcp__claude-in-chrome__*`) for all browser interaction
- Follows `/arc:commit` discipline for commits
- Can invoke `web-design-guidelines` skill for compliance review (if available)

<arc_log>
**After completing this skill, append to the activity log.**
See: `${CLAUDE_PLUGIN_ROOT}/references/arc-log.md`

Entry: `/arc:responsive — [N] pages audited, [N] issues fixed`
</arc_log>
