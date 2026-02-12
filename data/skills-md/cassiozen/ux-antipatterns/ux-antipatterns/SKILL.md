---
name: ux-antipatterns
description: Use when reviewing, building, or refactoring frontend UI — components, pages, forms, or interactive flows. Triggers on code review, pull requests, and new feature implementation involving user-facing interfaces.
---

# UX Anti-Pattern Detection

Scan frontend code for patterns that cause user frustration. 

## Core Axioms

Before checking individual rules, internalize these. They are the "why" behind every item below.

| # | Axiom | One-liner |
|---|-------|-----------|
| 1 | **Acknowledge every action** | Every user action must produce visible feedback within 100ms, even if the result takes seconds. |
| 2 | **Never destroy user input** | Not on error, not on navigation, not on timeout, not on refresh. |
| 3 | **State survives the unexpected** | Refresh, double-clicks or double submits, network loss — code must handle edge cases. |
| 4 | **Most recent intent wins** | Stale responses must never overwrite a newer user action. |
| 5 | **Explain every constraint** | If it's disabled, say why. If it failed, say how to fix it. If it succeeded, say what happened. |
| 6 | **Don't fight the platform** | Browser conventions, OS gestures, native controls, and accessibility APIs encode billions of hours of UX research. |

## When NOT to Use

- Backend-only code with no UI layer
- CLI tools or non-visual interfaces
- Design system tokens/docs without implementation code
- Pure API or data-layer reviews
- Performance profiling (unless it manifests as a UX symptom like layout shift)

## Workflow

1. Read [references/antipatterns.md](references/antipatterns.md) to load the full detection heuristics.
2. Scan the code under review against each applicable anti-pattern category.
3. Report findings grouped by anti-pattern, citing specific file:line locations.
4. For each finding, state: the anti-pattern name, the user harm, and a concrete fix.
5. If no anti-patterns are found, state that the code is clean rather than manufacturing findings.

## Anti-Pattern Categories

| # | Category | User Harm |
|---|----------|-----------|
| 1 | Layout Stability | Click target moves; wrong thing clicked. |
| 2 | Feedback & Responsiveness | Action feels ignored; user retries, waits, or loses trust that the system is working. |
| 3 | Error Handling & Recovery | User is stuck with no way forward; input destroyed; problem unsolvable without guessing. |
| 4 | Forms & Input Interference | Platform fights the user's typing; data mangled, basic editing broken. |
| 5 | Focus | User is typing and the UI yanks them elsewhere. |
| 6 | Notifications, Interruptions & Dialogs | User's flow broken; attention taxed by noise; forced to parse ambiguous choices under pressure. |
| 7 | Navigation, Routing & State Persistence | User can't go back; context evaporates on refresh or redirect. |
| 8 | Scroll & Viewport | Content unreachable or unstable; user fights the interface to see what they came for. |
| 9 | Timing, Debounce & Race Conditions | Actions fire twice, responses arrive stale, sessions expire mid-task; system behaves unpredictably under normal use. |
| 10 | Accessibility as UX | Entire interaction modes broken — keyboard users can't navigate, touch users locked out. |
| 11 | Visual Layering & Rendering | UI elements overlap, clip, or hide each other; controls become unreachable. |
| 12 | Mobile & Viewport-Specific | Keyboard covers input, layout jumps on scroll, tap targets unresponsive; basic mobile interaction degraded. |
| 13 | Cumulative Decay & Long-Term UX | App degrades over time; preferences lost, performance rots, stale experiments create inconsistencies. |

## Quick Reference: Symptom → Category

| User complaint / code smell | Category |
|---|---|
| "Button does nothing when I click it" | 2. Feedback & Responsiveness |
| "I clicked the wrong thing — it moved" | 1. Layout Stability |
| "I lost my form data" | 4. Forms & Input Interference |
| "It says 'Something went wrong' with no explanation" | 3. Error Handling & Recovery |
| "The page jumped while I was typing" | 5. Focus |
| "I got the same notification 5 times" | 6. Notifications & Dialogs |
| "I logged in and it forgot where I was going" | 7. Navigation & State Persistence |
| "I scrolled back and lost my place" | 8. Scroll & Viewport |
| "My order was placed twice" | 9. Timing & Race Conditions |
| "I was filling out a form and it logged me out" | 9. Timing & Race Conditions |
| "I clicked delete and it just... deleted it" | 6. Notifications & Dialogs |
| "It's been loading for 2 minutes with no progress bar" | 2. Feedback & Responsiveness |
| "I can't use this with my keyboard" | 10. Accessibility as UX |
| "The dropdown is hidden behind the modal" | 11. Visual Layering |
| "The keyboard covers the input on my phone" | 12. Mobile & Viewport-Specific |
| "The app gets slower over time" | 13. Cumulative Decay |

## Common Mistakes

- **Flagging style preferences as anti-patterns.** A non-standard button shape is a design choice, not a UX violation. Only flag patterns that cause measurable user harm per the axioms.
- **Ignoring context.** A disabled button inside a wizard step IS explained by the wizard's own flow. Check for nearby explanatory elements before reporting.
- **Suggesting fixes that break accessibility.** A fix that adds a visual indicator but removes keyboard access trades one violation for another. Verify fixes against Axiom 6.
- **Over-reporting on handled edge cases.** If the code already has an AbortController, don't flag it for race conditions. Read the implementation before reporting.
- **Reporting framework internals as violations.** React's `key` prop remounts, Next.js loading states, or SvelteKit form actions may handle anti-patterns at the framework level. Understand the framework before flagging.
