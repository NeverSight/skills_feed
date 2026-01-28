---
name: compound
description: "Knowledge retrieval, storage, and design system management for iterative agent loops. Use 'compound retrieve' at start, 'compound store' at end, 'compound design' for UI consistency. Prevents duplicates, manages size, keeps docs organized."
---

# Compound 🧠

Efficient project knowledge and design system management. Retrieve context fast, store learnings without bloat, maintain consistent UI across pages.

## Commands

| Command | When | Purpose |
|---------|------|---------|
| `compound retrieve` | Start of iteration | Find relevant knowledge for current task |
| `compound store` | End of iteration | Persist learnings not captured in code |
| `compound design retrieve` | Before building UI | Load design system tokens and patterns |
| `compound design store` | After UI decisions | Persist design tokens, patterns, components |
| `compound design sync` | Cross-page work | Ensure consistency with existing UI |

---

## Compound Retrieve

**Goal:** Get relevant context in <30 seconds with minimal token waste.

### Step 1: Index Scan
```bash
# List all knowledge files (cached mentally for the session)
find docs -name "*.md" -type f 2>/dev/null | head -50
```

### Step 2: Keyword Extraction
From the current ticket/task, extract 3-5 keywords:
- Entity names (User, Auth, API)
- Technical terms (JWT, WebSocket, migration)
- Domain concepts (billing, notifications)

### Step 3: Targeted Grep
```bash
# Search for keywords in docs (parallel, fast)
grep -ril "keyword1\|keyword2\|keyword3" docs/ | head -10
```

### Step 4: Smart Read
- **Small files (<100 lines):** Read fully
- **Large files:** Read only matching sections (grep -B2 -A5)
- **Index files (README, index.md):** Skim for pointers

### Step 5: Relevance Filter
Only load knowledge that's **directly applicable**:
- ✅ "JWT refresh tokens expire after 7 days" (for auth task)
- ❌ "We chose React over Vue" (not relevant to auth)

**Output:** Mental model of relevant project context, ready to apply.

---

## Compound Store

**Goal:** Persist valuable learnings without creating duplicates or bloat.

### Step 1: Identify Storable Knowledge

Only store what **code comments can't capture**:
- ✅ Why we chose X over Y (decision rationale)
- ✅ Non-obvious gotchas discovered during implementation
- ✅ Cross-component relationships not visible in one file
- ✅ External API quirks, rate limits, undocumented behavior
- ❌ What the code does (that's what code is for)
- ❌ How to run commands (put in README or AGENTS.md)

### Step 2: Duplicate Check (CRITICAL)

**Before writing ANYTHING, search for existing coverage:**

```bash
# Check if topic already exists
grep -ril "topic keyword" docs/

# Check similar filenames
find docs -name "*keyword*" -type f
```

**If found:**
- Read the existing file
- UPDATE it rather than create new
- Merge new info into existing sections
- Add/update the `updated:` frontmatter date

### Step 3: Choose Location

| Content Type | Location | Example |
|--------------|----------|---------|
| Architecture decisions | `docs/arch/` | `docs/arch/auth-flow.md` |
| Why X over Y | `docs/decisions/` | `docs/decisions/adr-001-db-choice.md` |
| Gotchas, edge cases | `docs/gotchas/` | `docs/gotchas/jwt-refresh-edge-cases.md` |
| Reusable patterns | `docs/patterns/` | `docs/patterns/error-handling.md` |
| External API notes | `docs/integrations/` | `docs/integrations/stripe-webhooks.md` |
| **Design system** | `docs/design/` | `docs/design/tokens.md` |

### Step 4: File Format

```markdown
---
tags: [searchable, terms, here]
updated: 2024-01-23
related: [../arch/auth.md, ../patterns/error-handling.md]
---

# Clear Descriptive Title

## Context
[Why this knowledge exists - 1-2 sentences]

## Key Points
- Bullet points for scannability
- One concept per bullet
- Include specifics (numbers, names, versions)

## Examples (if applicable)
[Code or scenarios that illustrate the point]

## See Also
- [Related doc](../path/to/related.md)
```

### Step 5: Size Management

**Per-file limits:**
- Target: 50-150 lines per file
- Max: 200 lines (split if larger)
- One focused topic per file

**Folder hygiene:**
```bash
# Check folder sizes periodically
find docs -name "*.md" | wc -l  # Should stay <50 files

# Find potential duplicates (similar names)
ls docs/**/*.md | sort | uniq -d
```

**If docs/ grows too large (>50 files):**
1. Consolidate related small files
2. Archive obsolete knowledge to `docs/_archive/`
3. Merge overlapping content

---

## Compound Design

**Goal:** Maintain consistent UI across all pages through tracked design tokens, patterns, and component decisions.

### Design System Location

All design system knowledge lives in `docs/design/`:

| File | Purpose | Example Content |
|------|---------|-----------------|
| `docs/design/tokens.md` | Design tokens | Colors, spacing, typography, shadows, breakpoints |
| `docs/design/components.md` | Component patterns | Button variants, card styles, form inputs |
| `docs/design/layout.md` | Layout conventions | Grid systems, page structures, responsive behavior |
| `docs/design/motion.md` | Animation & transitions | Durations, easing curves, animation patterns |
| `docs/design/decisions.md` | Design rationale | Why X font, why Y color palette |

### Compound Design Retrieve

**Before building ANY UI component:**

```bash
# Check for design system folder
ls docs/design/ 2>/dev/null

# Load tokens first (always required)
cat docs/design/tokens.md 2>/dev/null

# Load component patterns if building components
cat docs/design/components.md 2>/dev/null

# Load layout patterns if building pages
cat docs/design/layout.md 2>/dev/null
```

**If no design system exists:** Run mise-en-place Phase 2, or create one during first UI work. Don't proceed with UI without establishing tokens.

### Compound Design Store

**After making UI decisions, persist them to `docs/design/`.**

#### Step 1: Check for existing design system

```bash
ls docs/design/ 2>/dev/null
```

If exists, UPDATE the relevant file. If not, create the structure.

#### Step 2: Store tokens in `docs/design/tokens.md`

```markdown
---
updated: 2024-01-23
---

# Design Tokens

## Colors
| Token | Value | Usage |
|-------|-------|-------|
| `--color-primary` | oklch(55% 0.18 250) | CTAs, links, active states |
| `--color-surface` | oklch(98% 0.01 250) | Card backgrounds |
| `--color-text` | oklch(20% 0.02 250) | Body text |
| `--color-muted` | oklch(50% 0.01 250) | Secondary text |
| `--color-border` | oklch(90% 0.01 250) | Borders, dividers |
| `--color-error` | oklch(55% 0.2 25) | Error states |
| `--color-success` | oklch(55% 0.15 145) | Success states |

## Typography
| Token | Value | Usage |
|-------|-------|-------|
| `--font-display` | 'Instrument Serif', serif | Headings |
| `--font-body` | 'Inter', sans-serif | Body text |
| `--font-mono` | 'JetBrains Mono', monospace | Code |
| `--text-xs` | 0.75rem | Small labels |
| `--text-sm` | 0.875rem | Secondary text |
| `--text-base` | 1rem | Body text |
| `--text-lg` | 1.125rem | Emphasis |
| `--text-xl` | 1.25rem | Subheadings |
| `--text-2xl` | 1.5rem | Headings |

## Spacing
| Token | Value | Usage |
|-------|-------|-------|
| `--space-1` | 0.25rem | Tight groupings |
| `--space-2` | 0.5rem | Related items |
| `--space-4` | 1rem | Default gap |
| `--space-6` | 1.5rem | Medium separation |
| `--space-8` | 2rem | Section separation |
| `--space-12` | 3rem | Large separation |
| `--space-16` | 4rem | Major divisions |

## Border Radius
| Token | Value | Usage |
|-------|-------|-------|
| `--radius-sm` | 4px | Buttons, inputs |
| `--radius-md` | 8px | Cards |
| `--radius-lg` | 12px | Modals |
| `--radius-full` | 9999px | Avatars, pills |

## Shadows
| Token | Value | Usage |
|-------|-------|-------|
| `--shadow-sm` | 0 1px 2px oklch(0% 0 0 / 0.05) | Subtle elevation |
| `--shadow-md` | 0 4px 6px oklch(0% 0 0 / 0.1) | Cards |
| `--shadow-lg` | 0 10px 15px oklch(0% 0 0 / 0.1) | Modals, dropdowns |

## Breakpoints
| Token | Value | Usage |
|-------|-------|-------|
| `--bp-sm` | 640px | Mobile landscape |
| `--bp-md` | 768px | Tablet |
| `--bp-lg` | 1024px | Desktop |
| `--bp-xl` | 1280px | Wide desktop |
```

#### Step 3: Store component patterns in `docs/design/components.md`

```markdown
---
updated: 2024-01-23
---

# Component Patterns

## Buttons
- **Primary**: solid bg `--color-primary`, white text
- **Secondary**: border only, `--color-primary` border/text
- **Ghost**: no border, subtle hover bg
- **Destructive**: `--color-error` bg, white text
- All: `--radius-sm`, `--space-2` `--space-4` padding

## Cards
- `--color-surface` bg, `--radius-md`
- Padding: `--space-4` to `--space-6`
- Border: 1px `--color-border`
- NO nested cards, NO excessive shadows

## Forms
- Labels above inputs, `--space-1` gap
- Inputs: 1px border, `--radius-sm`, `--space-2` padding
- Focus: 2px ring `--color-primary`
- Error: border `--color-error`, message below

## Navigation
- Header height: 64px
- Sidebar width: 280px (collapsible to 64px)
- Active state: `--color-primary` accent
```

#### Step 4: Store layout patterns in `docs/design/layout.md`

```markdown
---
updated: 2024-01-23
---

# Layout Patterns

## Container
- Max-width: 1280px
- Padding: `--space-4` (mobile), `--space-8` (desktop)

## Page Layouts
- **Sidebar**: 280px fixed left, fluid content
- **Stacked**: header, main content, footer
- **Centered**: max-width content, centered

## Grid
- 12-column base grid
- Gap: `--space-4` default
- Responsive: 1 col mobile, 2-3 col tablet, 4+ col desktop
```

### Compound Design Sync

**When working on a new page in existing project:**

1. **Load the design system first**
   ```bash
   cat docs/design/tokens.md docs/design/components.md docs/design/layout.md 2>/dev/null
   ```

2. **Verify consistency before writing UI**
   - Use exact token names from `tokens.md` (e.g., `var(--color-primary)`)
   - Follow component patterns from `components.md`
   - Match layout conventions from `layout.md`

3. **Update design system if extending**
   - Adding a new color? Update `docs/design/tokens.md`
   - New component variant? Update `docs/design/components.md`
   - New layout pattern? Update `docs/design/layout.md`
   - Never create one-off values—extend the system or reuse existing

### Design System Anti-Patterns

❌ **Hardcoding values instead of tokens**
```css
/* Wrong */
color: #3b82f6;
padding: 16px;

/* Right - use established tokens */
color: var(--color-primary);
padding: var(--space-md);
```

❌ **Creating inconsistent component variants**
```jsx
/* Wrong - different button styles per page */
<button className="rounded-lg px-4">  {/* Page A */}
<button className="rounded-md px-6">  {/* Page B */}

/* Right - one consistent pattern */
<Button variant="primary">
```

❌ **Ignoring existing design system**
```bash
# Wrong - building UI without checking
# Just start coding...

# Right - always check first
cat docs/design/tokens.md
# Then build using those tokens
```

❌ **Storing design tokens in code comments**
```css
/* Wrong - tokens scattered in code */
/* Primary color: #3b82f6, spacing: 16px */

/* Right - centralized in docs/design/tokens.md */
```

❌ **Creating tokens outside the system**
```css
/* Wrong - one-off values */
padding: 18px;
color: #4a7c59;

/* Right - use or extend the system */
padding: var(--space-4);  /* existing token */
/* Or add to docs/design/tokens.md first */
```

---

## Anti-Patterns

❌ **Creating near-duplicate files**
```
docs/gotchas/auth-issues.md
docs/gotchas/authentication-problems.md  # DUPLICATE!
```

❌ **Storing obvious information**
```markdown
# How to Start the Server
Run the dev server command  # This belongs in README/AGENTS.md!
```

❌ **Huge monolithic files**
```
docs/knowledge.md  # 500 lines of everything
```

❌ **Vague file names**
```
docs/notes.md
docs/stuff.md
docs/misc.md
```

❌ **Forgetting to update existing files**
```bash
# Wrong: Create new file
touch docs/gotchas/jwt-issue-2.md

# Right: Update existing
edit docs/gotchas/jwt-refresh-edge-cases.md
```

---

## Quick Reference

### Retrieve Checklist
- [ ] List docs structure
- [ ] Extract task keywords
- [ ] Grep for relevant files
- [ ] Read only what's needed
- [ ] Apply context to task

### Store Checklist
- [ ] Is this code-external knowledge?
- [ ] Search for existing coverage
- [ ] Update existing OR create focused new file
- [ ] Add frontmatter (tags, updated, related)
- [ ] Keep file <150 lines
- [ ] Verify no duplicates created

### Design Retrieve Checklist
- [ ] Check for `docs/design/` folder
- [ ] Load `tokens.md` first (always required)
- [ ] Load `components.md` if building components
- [ ] Load `layout.md` if building pages
- [ ] If no design system, run mise-en-place or create one

### Design Store Checklist
- [ ] Check if `docs/design/` exists
- [ ] Create folder structure if missing
- [ ] Store tokens in `tokens.md`
- [ ] Store component patterns in `components.md`
- [ ] Store layout patterns in `layout.md`
- [ ] Update `updated:` date in frontmatter

### Design Sync Checklist
- [ ] Load all design files before new page
- [ ] Use exact token names (`var(--color-primary)`)
- [ ] Follow component patterns exactly
- [ ] If extending: update the appropriate file in `docs/design/`
- [ ] Never use hardcoded values—extend the system


