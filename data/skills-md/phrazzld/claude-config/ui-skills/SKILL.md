---
name: ui-skills
user-invocable: false
description: Opinionated constraints for building better interfaces with agents.
---

# UI Skills

When invoked, apply these opinionated constraints for building better interfaces.

## MANDATORY: Kimi Delegation for UI Implementation

**All UI implementation work MUST be delegated to Kimi K2.5 via MCP.**

Kimi excels at frontend development. Claude reviews, Kimi builds:

```javascript
// Delegate UI implementation to Kimi
mcp__kimi__spawn_agent({
  prompt: `Implement [component/feature].
Apply ui-skills constraints:
- Tailwind CSS defaults, cn() utility
- Accessible primitives (Base UI/Radix/React Aria)
- No h-screen (use h-dvh), respect safe-area-inset
- Animator only transform/opacity, max 200ms feedback
- text-balance for headings, tabular-nums for data
Existing patterns: [reference files]
Output: ${targetPath}`,
  thinking: true
})
```

**Workflow:**
1. Define constraints → Claude (this skill)
2. Implement UI → Kimi (Agent Swarm)
3. Review quality → Claude (expert panel review)

**Anti-pattern:** Implementing UI yourself instead of delegating to Kimi.

## How to use

- `/ui-skills`
  Apply these constraints to any UI work in this conversation.

- `/ui-skills <file>`
  Review the file against all constraints below and output:
  - violations (quote the exact line/snippet)
  - why it matters (1 short sentence)
  - a concrete fix (code-level suggestion)

## Stack

- MUST use Tailwind CSS defaults unless custom values already exist or are explicitly requested
- MUST use `motion/react` (formerly `framer-motion`) when JavaScript animation is required
- SHOULD use `tw-animate-css` for entrance and micro-animations in Tailwind CSS
- MUST use `cn` utility (`clsx` + `tailwind-merge`) for class logic

## Components

- MUST use accessible component primitives for anything with keyboard or focus behavior (`Base UI`, `React Aria`, `Radix`)
- MUST use the project’s existing component primitives first
- NEVER mix primitive systems within the same interaction surface
- SHOULD prefer [`Base UI`](https://base-ui.com/react/components) for new primitives if compatible with the stack
- MUST add an `aria-label` to icon-only buttons
- NEVER rebuild keyboard or focus behavior by hand unless explicitly requested

## Interaction

- MUST use an `AlertDialog` for destructive or irreversible actions
- SHOULD use structural skeletons for loading states
- NEVER use `h-screen`, use `h-dvh`
- MUST respect `safe-area-inset` for fixed elements
- MUST show errors next to where the action happens
- NEVER block paste in `input` or `textarea` elements

## Animation

- NEVER add animation unless it is explicitly requested
- MUST animate only compositor props (`transform`, `opacity`)
- NEVER animate layout properties (`width`, `height`, `top`, `left`, `margin`, `padding`)
- SHOULD avoid animating paint properties (`background`, `color`) except for small, local UI (text, icons)
- SHOULD use `ease-out` on entrance
- NEVER exceed `200ms` for interaction feedback
- MUST pause looping animations when off-screen
- SHOULD respect `prefers-reduced-motion`
- NEVER introduce custom easing curves unless explicitly requested
- SHOULD avoid animating large images or full-screen surfaces

## Typography

- MUST use `text-balance` for headings and `text-pretty` for body/paragraphs
- MUST use `tabular-nums` for data
- SHOULD use `truncate` or `line-clamp` for dense UI
- NEVER modify `letter-spacing` (`tracking-*`) unless explicitly requested

## Layout

- MUST use a fixed `z-index` scale (no arbitrary `z-*`)
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

## Performance

- NEVER animate large `blur()` or `backdrop-filter` surfaces
- NEVER apply `will-change` outside an active animation
- NEVER use `useEffect` for anything that can be expressed as render logic

## Design

- NEVER use gradients unless explicitly requested
- NEVER use purple or multicolor gradients
- NEVER use glow effects as primary affordances
- SHOULD use Tailwind CSS default shadow scale unless explicitly requested
- MUST give empty states one clear next action
- SHOULD limit accent color usage to one per view
- SHOULD use existing theme or Tailwind CSS color tokens before introducing new ones

## Expert Panel Review (MANDATORY)

**Before returning ANY design output to the user, it MUST pass expert panel review.**

See full details: `references/expert-panel-review.md`

### Quick Reference

1. Simulate 10 world-class advertorial experts:
   - **Ogilvy** (advertising), **Rams** (industrial design), **Scher** (typography)
   - **Wiebe** (conversion copy), **Laja** (CRO), **Walter** (UX)
   - **Cialdini** (persuasion), **Ive** (product design), **Wroblewski** (mobile)
   - **Millman** (brand strategy)

2. Each expert scores 0-100 with specific improvement feedback

3. **Threshold: 90+ average required**

4. If below 90: implement feedback, iterate, re-review

5. Only return design to user when 90+ achieved

### Example Output

```markdown
Expert Panel Review: Hero Section

| Expert | Score | Critical Improvement |
|--------|-------|---------------------|
| Ogilvy | 88 | Lead with benefit, not feature |
| Rams | 94 | Clean, focused |
| Scher | 86 | H2 needs more weight contrast |
| Wiebe | 81 | "Get Started" → "Start Free Trial" |
| Laja | 77 | No social proof above fold |
| Walter | 90 | Good emotional resonance |
| Cialdini | 83 | Add urgency element |
| Ive | 92 | Refined execution |
| Wroblewski | 88 | Touch targets good |
| Millman | 85 | Voice slightly inconsistent |

**Average: 86.4** ❌ Below threshold

Implementing: Laja (social proof), Wiebe (CTA), Cialdini (urgency)...
```

### Anti-Patterns

- ❌ Skipping review for "quick fixes"
- ❌ Accepting 85+ as "close enough"
- ❌ Generic feedback ("make it better")
- ❌ Returning design without 90+ score
