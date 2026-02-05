---
name: design
description: |
  Create distinctive, non-generic UI designs with aesthetic direction and ASCII wireframes.
  Use when asked to "design the UI", "create a layout", "wireframe this", or when building
  UI that should be memorable rather than generic. Avoids AI slop patterns.
license: MIT
metadata:
  author: howells
website:
  order: 8
  desc: Visual design direction
  summary: Establish the visual identity for your UI—colors, typography, spacing, tone. Comes with opinionated references to avoid generic AI aesthetics.
  what: |
    Design walks you through visual decisions: What's the tone? What makes this memorable? It can research real-world examples from Siteinspire (websites) and Mobbin (UI patterns) to inform your direction. From there it produces a design direction document—color palette, typography scale, spacing system, and ASCII wireframes for key screens. It draws from built-in references on font pairing, component patterns, and animation. As you build, it can screenshot via Chrome to verify implementation matches intent.
  why: |
    AI-generated UI tends toward the same safe choices—the same gradients, the same card layouts, the same hero sections. Design fights this by forcing you to make distinctive choices upfront and documenting them. The references help you avoid common pitfalls and give the AI better taste.
  decisions:
    - Opinionated references built in. Font choices, spacing scales, animation patterns—not starting from scratch.
    - ASCII wireframes over mockups. Version-controllable, forces focus on structure.
    - Visual verification via screenshots. Catches when implementation drifts from intent.
---

# Design Workflow

Create distinctive, non-generic UI. Avoids AI slop (purple gradients, cookie-cutter layouts).

**Announce at start:** "I'm using the design skill to create distinctive, non-generic UI."

<important>
**This skill is user-interactive. Do NOT spawn agents to do design work.**

- This skill walks through design decisions WITH the user — it's collaborative, not delegated
- There is no `arc:design:designer` agent — design creation happens through this skill
- `arc:review:designer` exists but is for REVIEWING implementations AFTER they're built, not for creating designs
- If asked to "design X", follow this skill's phases; don't try to spawn an agent
</important>

---

## Phase 0: Load References (MANDATORY)

**You MUST read these files before proceeding. Do not skip this step.**

<mandatory_references>
**Read ALL of these using the Read tool:**

1. `${CLAUDE_PLUGIN_ROOT}/references/frontend-design.md` — Fonts, anti-patterns, design review checklist. **Critical.**
2. `${CLAUDE_PLUGIN_ROOT}/references/design-philosophy.md` — Timeless principles from Refactoring UI
3. `${CLAUDE_PLUGIN_ROOT}/references/ascii-ui-patterns.md` — Wireframe syntax and patterns

**Then load interface rules:**
4. `${CLAUDE_PLUGIN_ROOT}/rules/interface/index.md` — Interface rules index

**And relevant domain rules based on what you're designing:**
- `${CLAUDE_PLUGIN_ROOT}/rules/interface/design.md` — Visual principles
- `${CLAUDE_PLUGIN_ROOT}/rules/interface/colors.md` — Color palettes
- `${CLAUDE_PLUGIN_ROOT}/rules/interface/spacing.md` — Spacing system
- `${CLAUDE_PLUGIN_ROOT}/rules/interface/typography.md` — Typography rules
- `${CLAUDE_PLUGIN_ROOT}/rules/interface/layout.md` — Layout patterns, z-index
- `${CLAUDE_PLUGIN_ROOT}/rules/interface/animation.md` — If motion is involved
- `${CLAUDE_PLUGIN_ROOT}/rules/interface/forms.md` — If designing forms
- `${CLAUDE_PLUGIN_ROOT}/rules/interface/interactions.md` — Touch, keyboard, hover patterns
- `${CLAUDE_PLUGIN_ROOT}/rules/interface/marketing.md` — If designing marketing pages
</mandatory_references>

<progress_context>
**Use Read tool:** `docs/progress.md` (first 50 lines)

Check for related prior design work and aesthetic decisions.
</progress_context>

---

## Phase 1: Visual Reconnaissance

**Before designing anything, see what exists.**

### If Redesigning Existing UI:

**Use Chrome MCP to capture current state:**

```
1. mcp__claude-in-chrome__tabs_context_mcp (get available tabs)
2. mcp__claude-in-chrome__tabs_create_mcp (create new tab if needed)
3. mcp__claude-in-chrome__navigate to the local dev URL
4. mcp__claude-in-chrome__computer action=screenshot
```

**Analyze the screenshot against the Design Review Checklist from frontend-design.md:**
- Does it have any Red Flags (AI slop indicators)?
- What's the current aesthetic direction (if any)?
- What's working? What's not?

**Report findings to user:** "Here's what I see in the current UI: [observations]. The main issues are: [problems]."

### If Designing From Scratch:

- Confirm dev server is running (or will be)
- Ask if there's any existing brand/style guide to reference
- Check if there are reference designs or inspiration URLs to screenshot

---

## Phase 2: Gather Direction

Ask these questions **one at a time**:

### Question 1: Tone
"What tone fits this UI?"
- Minimal, bold, playful, editorial, luxury, brutalist, retro, organic, industrial, art deco, soft/pastel

### Question 2: Memorable Element
"What should be memorable about this?"
- The animation? Typography? Layout? A specific interaction? Color? Photography style?

### Question 3: Existing Constraints
"Any existing brand/style to match, or fresh start?"

### Question 4: Inspiration
"Any reference designs or inspiration?"
- If provided, **screenshot them immediately using Chrome MCP** for visual reference

### Question 5: UI Chrome
"Should this have standard website chrome (header, footer, navigation), or feel more like an app?"

Consider:
- **Standard website chrome** — Fixed header with logo/nav, footer with links. Good for content sites, marketing pages, multi-page experiences where users need to navigate.
- **App-like experience** — Minimal or no persistent chrome. Content takes full focus. Good for tools, dashboards, immersive experiences, single-purpose flows.
- **Hybrid** — Minimal header (maybe just a logo), no footer. Common for SaaS apps.

**The default shouldn't always be "header + footer".** If the experience is focused (a tool, a game, a single flow), standard chrome can feel clunky and distract from the core experience. Let the purpose guide the frame.

---

## Phase 3: Research Inspiration (Optional)

**Use WebFetch to explore curated design examples based on the chosen direction.**

This phase is optional but recommended when:
- Starting from scratch with no existing references
- The user wants to see examples matching their chosen tone
- You need concrete visual patterns to inform decisions

### Siteinspire (Website/Homepage Design)

Siteinspire curates high-quality website designs. Use WebFetch to explore based on the chosen tone:

```
WebFetch URL patterns by tone:
- Minimal:    https://www.siteinspire.com/websites?style=minimal
- Bold:       https://www.siteinspire.com/websites?style=bold
- Playful:    https://www.siteinspire.com/websites?style=playful
- Editorial:  https://www.siteinspire.com/websites?style=editorial
- Luxury:     https://www.siteinspire.com/websites?style=luxury
- Brutalist:  https://www.siteinspire.com/websites?style=brutalist
- Retro:      https://www.siteinspire.com/websites?style=retro
- Organic:    https://www.siteinspire.com/websites?style=organic

By page type:
- Homepage:   https://www.siteinspire.com/websites?page=homepage
- Portfolio:  https://www.siteinspire.com/websites?page=portfolio
- E-commerce: https://www.siteinspire.com/websites?page=e-commerce
- Blog:       https://www.siteinspire.com/websites?page=blog
```

**WebFetch prompt:** "List the website names, their URLs, and a brief description of their visual style. Focus on typography choices, color palettes, and layout patterns."

### Mobbin (UI/Mobile Design Patterns)

Mobbin collects UI patterns from real apps. Use for component and interaction inspiration:

```
WebFetch URL patterns:
- iOS apps:     https://mobbin.com/browse/ios/apps
- Android:      https://mobbin.com/browse/android/apps
- Web apps:     https://mobbin.com/browse/web/apps

By screen type:
- Onboarding:   https://mobbin.com/browse/ios/screens?screen=onboarding
- Dashboard:    https://mobbin.com/browse/ios/screens?screen=dashboard
- Settings:     https://mobbin.com/browse/ios/screens?screen=settings
- Profile:      https://mobbin.com/browse/ios/screens?screen=profile
- Search:       https://mobbin.com/browse/ios/screens?screen=search
```

**WebFetch prompt:** "List the apps shown and describe their UI patterns—navigation style, card layouts, typography hierarchy, and interaction patterns."

### Research Workflow

1. **Based on user's chosen tone**, fetch 1-2 relevant Siteinspire pages
2. **Based on what you're designing** (homepage, dashboard, form), fetch relevant Mobbin screens
3. **Summarize findings** to user: "I found these patterns that match your direction: [observations]"
4. **Ask:** "Any of these resonate? Should I explore a specific site further with Chrome MCP?"

### Deep Dive with Chrome MCP

If a specific example catches interest, use Chrome MCP for detailed inspection:

```
1. mcp__claude-in-chrome__navigate to the specific site URL
2. mcp__claude-in-chrome__computer action=screenshot
3. Analyze: typography, colors, spacing, layout patterns
4. Report specific values observed (font names, hex colors, spacing)
```

**Note:** WebFetch provides quick overview; Chrome MCP provides detailed visual inspection. Use both strategically.

---

## Phase 4: Make Concrete Visual Decisions

**Capture SPECIFIC visual decisions, not conceptual themes.**

Apply knowledge from the loaded references to make these decisions:

### Typography Selection
Using the font recommendations from `frontend-design.md`:
- **Display font:** [specific font name]
- **Body font:** [specific font name]
- **Mono font (if needed):** [specific font name]

**Never use:** Roboto, Arial, system-ui defaults, Instrument Serif (AI slop)

### Color Palette
- **Background:** [specific hex, e.g., #0a0a0a]
- **Surface/card:** [specific hex]
- **Text primary:** [specific hex]
- **Text secondary:** [specific hex]
- **Accent:** [specific hex]
- **Accent hover:** [specific hex]

**Never use:** Purple-to-blue gradients (AI cliché)

### Spacing System
Define the scale being used:
- **Base unit:** 4px or 8px
- **Common values:** 4, 8, 12, 16, 24, 32, 48, 64
- **Component padding:** [e.g., 16px default, 24px for cards]
- **Section spacing:** [e.g., 64px between major sections]

### Motion Philosophy
- **Where animation is used:** [specific locations]
- **Animation style:** [e.g., ease-out for enters, springs for interactive]
- **Duration range:** [e.g., 150-300ms]

---

## Phase 5: ASCII Wireframe

**Create ASCII wireframes before any code.** Use patterns from `ascii-ui-patterns.md`.

```
┌─────────────────────────────────────┐
│  Logo        [Search...]    [Menu]  │
├─────────────────────────────────────┤
│                                     │
│  [Main Content Area]                │
│                                     │
└─────────────────────────────────────┘
```

**Include:**
1. Primary layout structure
2. Key interactive elements
3. Mobile version if responsive
4. States: empty, loading, error (where relevant)

**Ask:** "Does this layout feel right before I continue?"

---

## Phase 6: Produce Design Document

**Create the design direction document at `docs/plans/design-[component-name].md`:**

```markdown
# Design Direction: [Component/Page Name]

## Aesthetic Direction
- **Tone:** [chosen - e.g., "minimal", "bold", "editorial"]
- **Memorable element:** [specific - e.g., "oversized typography", "micro-interactions on hover"]

## Typography
- **Display:** [font name] — [where used]
- **Body:** [font name] — [where used]
- **Mono:** [font name] — [where used, if applicable]

## Color Palette
| Role | Value | Usage |
|------|-------|-------|
| Background | #0a0a0a | Page background |
| Surface | #1a1a1a | Cards, panels |
| Text primary | #fafafa | Headings, body |
| Text secondary | #a1a1a1 | Labels, hints |
| Accent | #f59e0b | CTAs, links |
| Accent hover | #fbbf24 | Hover states |

## Spacing
- Base unit: 8px
- Component padding: 16px (small), 24px (medium), 32px (large)
- Section gaps: 48px (tight), 64px (normal), 96px (generous)

## Motion
- Page transitions: fade, 200ms ease-out
- Interactive elements: spring (stiffness: 400, damping: 25)
- Hover states: 150ms ease-out

## Layout

### Desktop
[ASCII wireframe]

### Mobile
[ASCII wireframe]

## Implementation Notes
- [Any specific technical considerations]
- [Component library preferences]
- [Animation library: CSS-only vs motion/react]

## Anti-Patterns to Avoid
- [Specific things NOT to do for this design]
```

---

## Phase 7: Verify Against Checklist

**Run the Design Review Checklist from frontend-design.md:**

### Red Flags (must be zero)
- [ ] Uses default system fonts
- [ ] Purple-to-blue gradient present
- [ ] White background + gray cards throughout
- [ ] Could be mistaken for generic AI output

### Green Flags (should have most)
- [ ] Clear aesthetic direction documented
- [ ] Typography is deliberate
- [ ] At least one memorable element
- [ ] Layout has unexpected decisions

**If any Red Flags are present, revise before proceeding.**

---

## Phase 8: Hand Off

**Use AskUserQuestion tool:**
```
Question: "Design documented. What's next?"
Header: "Next step"
Options:
  1. "Create detailed plan" (Recommended) — Run /arc:detail for task breakdown
  2. "Save and stop" — Return to this later
```

**IMPORTANT: Do NOT automatically invoke other skills.**

- **If option 1:** Tell user: "Design saved. Run `/arc:detail` to create implementation tasks."
- **If option 2:** Tell user: "Design saved to `docs/plans/design-[name].md`. Return anytime."

---

## During Implementation (Reference for /arc:implement)

When implementing this design (via /arc:implement), use Chrome MCP continuously:

### After Every Significant Change
```
mcp__claude-in-chrome__computer action=screenshot
```

### Check Responsive Behavior
```
mcp__claude-in-chrome__resize_window width=375 height=812  # Mobile
mcp__claude-in-chrome__computer action=screenshot
mcp__claude-in-chrome__resize_window width=1440 height=900 # Desktop
mcp__claude-in-chrome__computer action=screenshot
```

### Verify Against Design Doc
- Does the typography match what was specified?
- Are the colors exactly as documented?
- Does spacing feel consistent with the system?
- Is the memorable element actually memorable?

**Never commit UI code without visually verifying it looks correct.**

---

## Anti-Patterns (Quick Reference)

From `frontend-design.md`:

**🚫 Never use sparkles/stars to denote AI features.** Overused, meaningless, dated.

**🚫 Never propose conceptual themes with metaphors.** No "Direction: Darkroom / Metaphor: Photo emerging from developer bath". Instead: "Dark background (#0a0a0a) with warm red accents (#dc2626)."

**🚫 Never use these:**
- Roboto/Arial/system-ui defaults
- Purple-to-blue gradients
- White backgrounds with gray cards
- Rounded corners on everything
- Mixed icon styles

---

<arc_log>
**After completing this skill, append to the activity log.**
See: `${CLAUDE_PLUGIN_ROOT}/references/arc-log.md`

Entry: `/arc:design — [Component/page] design ([aesthetic direction])`
</arc_log>

<success_criteria>
Design is complete when:
- [ ] All mandatory references were loaded and applied
- [ ] Current UI was screenshotted (if redesigning)
- [ ] Aesthetic direction established with SPECIFIC values
- [ ] Typography selected from recommended fonts
- [ ] Color palette defined with hex values
- [ ] Spacing system documented
- [ ] ASCII wireframes created and approved
- [ ] Design document saved to docs/plans/
- [ ] Red flag checklist passed (zero red flags)
- [ ] Progress journal updated
</success_criteria>

## Interop

- Produces design doc consumed by **/arc:implement**
- Can invoke **web-design-guidelines** skill for compliance review (if available)
- Uses **Chrome MCP** (`mcp__claude-in-chrome__*`) for visual capture throughout
- Uses **WebFetch** to research design inspiration from Siteinspire and Mobbin
- References feed into implementation to maintain design fidelity
