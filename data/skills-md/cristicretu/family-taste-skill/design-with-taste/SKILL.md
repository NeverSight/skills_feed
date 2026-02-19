---
name: design-with-taste
description: Apply the "Family Values" design philosophy to every UI you build. Use this skill whenever creating frontends, components, apps, landing pages, dashboards, or any user-facing interface. Enforces three core principles — Simplicity (gradual revelation), Fluidity (seamless transitions), and Delight (selective emphasis) — so that every output feels crafted, intentional, and alive. Prevents generic, static, lifeless UI. Works alongside other skills like frontend-design, web-animation-design, etc.
---

# Design with Taste

This skill encodes the design philosophy behind [Family](https://family.co) — a product widely praised for feeling *alive*, *welcoming*, and *intentional*. Originally documented by Benji Taylor at [benji.org/family-values](https://benji.org/family-values).

**Read this before writing any UI code. Every time.**

The user wants something built. Your job is to make it feel like a human who gives a shit designed it.

---

## The Three Pillars

Ordered by priority. You cannot have Delight without Fluidity, and you cannot have Fluidity without Simplicity.

---

### 1. Simplicity — Gradual Revelation

> "Each action by the user makes the interface unfold and evolve, much like walking through a series of interconnected rooms."

**The problem**: Most UIs dump everything at once — every feature, every option, every edge case, all visible, all the time. This transfers cognitive burden from the designer to the user.

**The principle**: Show only what matters *right now*. The interface should feel like walking through rooms — you glimpse what's next before you arrive.

**Rules**:

- **One primary action per view.** Two equally weighted CTAs = failure. Make everything else secondary.
- **Progressive disclosure over feature dumps.** Layered trays, step-by-step flows, expandable sections. Never show a 12-field form when 3 steps of 4 fields works.
- **Context-preserving overlays over full-page navigations.** Sheets/trays/modals that overlay the current context keep users oriented. Full-screen transitions displace them.
- **Vary heights of stacked layers.** Each subsequent sheet/tray must be a visibly different height so the progression is unmistakably clear. Never stack two identical-height layers.
- **Every sheet/tray/modal needs a title and dismiss action.** Users must always know what they're looking at and how to get back.
- **Trays adapt to context.** A tray appearing within a dark-themed flow should adopt a darker color scheme. The visual environment follows the user.
- **Trays can launch full-screen flows.** A compact tray is a valid entry point for a multi-step full-screen experience — don't force a binary choice between "tray" and "page."
- **Use trays for transient actions; full screens for persistent destinations.** Confirmations, warnings, and contextual info = tray. Settings, core content = full screen.

```jsx
// GOOD: Progressive tray — compact, focused, context-aware
<Sheet>
  <SheetTrigger>Confirm Send</SheetTrigger>
  <SheetContent className="h-[45vh]"> {/* height varies from parent */}
    <SheetHeader>
      <SheetTitle>Review Transaction</SheetTitle>
      <DismissButton />
    </SheetHeader>
    {/* Core info only — no extras */}
    <Button>Send $42.00</Button>
  </SheetContent>
</Sheet>
```

**Self-check**: Can the user tell within 1 second what to do next? If not, simplify.

---

### 2. Fluidity — Seamless Transitions

> "We fly instead of teleport."

**The problem**: Static transitions make products feel dead. A dead product feels uncared for. Instant cuts destroy spatial orientation — where did that come from? Where did it go?

**The principle**: Treat your app as a space with **unbreakable physical rules**. Know *why* a transition makes sense architecturally before adding it. Every element moves *from* somewhere *to* somewhere.

**Rules**:

- **No instant show/hide.** Every element that appears or disappears must animate. Pick a transition that makes spatial sense — fade, slide, scale, morph.
- **Shared element transitions.** If an element exists in both State A and State B (a card that expands, a button that becomes a sheet), it must visually *travel* between them. Never unmount and remount — morph.
- **Directional consistency.** Navigate right (next step, next tab) → content enters from right. Go back → content enters from left. Tabs to the left of current slide left. This builds spatial memory.
- **Text morphing over instant replacement.** When button labels change (e.g., "Continue" → "Confirm"), animate the transition. Identify shared letter sequences ("Con") — keep them fixed while the rest morphs. Use [torph](https://torph.lochie.me/) (`npm i torph`) — dependency-free, works with React/Vue/Svelte. Crossfade is the minimum fallback; shared-letter morphing is the ideal.
- **Partial text changes: only animate what changes.** If a sentence gains or loses a word, keep the unchanged portion static. Animating unchanged text creates jarring redundancy.
- **Persistent elements stay put.** If a header, card, or component persists across a transition, it must NOT animate out and back in. Only the changing parts move.
- **Loading states travel to their destination.** A spinner doesn't just sit where triggered — it moves to where the user will look for results (e.g., after submitting a transaction, the spinner migrates to the activity tab icon).
- **Micro-directional cues.** Chevrons, arrows, and carets should animate to reflect the action taken. A `→` becomes a `←` on back-navigation. An accordion chevron rotates on expand.
- **Unified interpolation.** All visual elements driven by the same data should share the same lerp/easing. This makes the interface feel like *one thing breathing* rather than a bunch of parts updating independently. When the value changes, the line, the label, the axis, and the badge should all move as one.

```jsx
// Text morphing — use torph
import { TextMorph } from 'torph/react';
<TextMorph>{label}</TextMorph>  // handles shared-letter animation automatically

// Directional tab transitions
const direction = newIndex > currentIndex ? 1 : -1;
<motion.div
  key={currentTab}
  initial={{ x: direction * 20, opacity: 0 }}
  animate={{ x: 0, opacity: 1 }}
  exit={{ x: -direction * 20, opacity: 0 }}
  transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
/>

// Shared element: card → detail view
<motion.div
  layoutId={`card-${id}`}
  className={isExpanded ? "fixed inset-0 rounded-none" : "rounded-xl"}
  transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
/>
```

**The golden easing curve**: `cubic-bezier(0.16, 1, 0.3, 1)` — fast start, gentle settle. Default for all entrances and morphs. Use `ease-in` (`cubic-bezier(0.4, 0, 1, 1)`) for exits only. Never use linear.

**Self-check**: Record your screen and play back at 0.5x speed. Can you follow every element's journey? Anything that teleports needs a transition.

---

### 3. Delight — Selective Emphasis

> "Mastering delight is mastering selective emphasis."

**The problem**: Either zero personality (corporate slop) or everything bounces and sparkles (annoying). Both miss the point.

**The principle**: The **Delight-Impact Curve** — the less frequently a feature is used, the *more* delightful it should be. Daily actions need efficiency with subtle touches. Rare moments deserve theatrical ones.

```
Delight ↑
        |         *  (rare features: theatrical)
        |       *
        |     *
        |   * *  (medium: memorable)
        | * *
        |* *  *  (frequent: subtle)
        +------------------→ Feature frequency
```

**Rules**:

- **Polish everything equally.** The settings page, the empty state, the error screen — all receive the same care as the hero section. One unpolished corner makes the whole feel unpolished. *"Like a fancy restaurant with a dirty bathroom."*
- **Easter eggs reward exploration.** Hide moments in unexpected places. They create stories users share. Key: place them in features used just enough that discovery feels like reward, not annoyance.
- **Celebrate completions.** Significant actions (backup, onboarding, first transaction) deserve confetti, a custom animation, a satisfying sound — not a green checkmark.
- **Make destructive actions satisfying.** Deleting items? They tumble into a trash can with a sound effect. Destructive ≠ unpleasant.
- **Animate numbers and live charts.** Values that change (prices, counts, balances) should count/flip/morph. Commas should shift position smoothly as numbers grow — never just swap. For real-time line charts, use [liveline](https://benji.org/liveline) (`npm i liveline`) — one canvas, no dependencies beyond React 18, 60fps interpolation. For 60fps value overlays, update the DOM directly rather than through React state to avoid re-render overhead.
- **Empty states are first impressions.** An animated arrow pointing toward the create button, a floating illustration, a warm message. Never "No items yet" with nothing else.
- **Sound design amplifies physicality.** Completion sounds, subtle interaction feedback. Sound reinforces reward and makes actions feel real.
- **Drag-and-drop should feel satisfying.** Stacking animations, smooth reorder, visual feedback on lift. Reordering items should feel better than the result deserves.

**Delight pattern library** — concrete moments proven to work:

| Feature | Frequency | Delight Level | Pattern |
|---|---|---|---|
| Number input | Daily | Subtle | Commas shift position as digits are typed |
| Tab/chart navigation | Daily | Subtle | Arrow icon flips direction with value change |
| Empty state | First visit | Medium | Animated arrow + floating illustration |
| Item reorder | Occasional | Medium | Stacking animation + smooth drop |
| Delete/trash | Occasional | Medium | Item tumbles into skeuomorphic trash + sound |
| First feature use | Once | High | Animated guide arrow in empty state |
| Critical completion (backup, onboarding) | Once | Theatrical | Confetti explosion + celebratory sound |
| Easter egg (QR, hidden gesture) | Rare | Theatrical | Ripple on tap → sequin effect on swipe |

```jsx
// Animated number with smooth comma shifting
function AnimatedNumber({ value }) {
  const spring = useSpring(value, { stiffness: 80, damping: 20 });
  return <motion.span>{useTransform(spring, v => Math.round(v).toLocaleString())}</motion.span>;
}

// Real-time chart — liveline handles interpolation, momentum arrows, scrub, theming
import { Liveline } from 'liveline';
<div style={{ height: 200 }}>
  <Liveline
    data={history}           // [{ time, value }]
    value={latestValue}      // current number
    momentum                 // directional arrows (green/red/grey)
    showValue                // 60fps DOM overlay, no re-renders
    color="#3b82f6"          // derives full palette from one color
  />
</div>

// Satisfying empty state
function EmptyState() {
  return (
    <div className="flex flex-col items-center gap-4 py-16">
      <motion.div animate={{ y: [0, -8, 0] }} transition={{ repeat: Infinity, duration: 2, ease: "easeInOut" }}>
        <IllustrationIcon />
      </motion.div>
      <p className="text-muted">Nothing here yet</p>
      <motion.div animate={{ x: [0, 5, 0] }} transition={{ repeat: Infinity, duration: 1.5 }}>
        <ArrowRight className="inline mr-1" /> Create your first item
      </motion.div>
    </div>
  );
}

// Confetti on significant completion
function CompletionScreen() {
  useEffect(() => { playSound('success'); }, []);
  return (
    <motion.div initial={{ scale: 0.8, opacity: 0 }} animate={{ scale: 1, opacity: 1 }}
      transition={{ type: "spring", damping: 15, stiffness: 200 }}>
      <ConfettiExplosion />
      <h2>You're all set!</h2>
    </motion.div>
  );
}
```

**Self-check**: Show your UI to someone for 30 seconds. Do they smile? If not, add delight. Do they look annoyed? You over-delighted a high-frequency interaction.

---

## The Taste Checklist

Run before considering any UI "done":

### Simplicity
- [ ] Each screen has ONE clear primary action
- [ ] Complex flows broken into digestible steps
- [ ] Information revealed progressively, not all at once
- [ ] Context preserved during transitions (overlays > navigations)
- [ ] Stacked layers are visibly different heights
- [ ] Every overlay has a title and dismiss action
- [ ] User always knows where they are and how to go back

### Fluidity
- [ ] Zero instant show/hide — everything animates
- [ ] Shared elements morph between states (not unmount/remount)
- [ ] Directional transitions match spatial logic
- [ ] Persistent elements don't redundantly animate
- [ ] Text changes use torph or crossfade minimum
- [ ] Only the changing part of partial text updates animates
- [ ] Loading states move to where results will appear
- [ ] Micro-directional cues on chevrons and arrows
- [ ] Elements driven by same data share the same lerp/easing (unified interpolation)
- [ ] Default easing is `cubic-bezier(0.16, 1, 0.3, 1)`

### Delight
- [ ] Frequent features have subtle micro-interactions
- [ ] Infrequent features have memorable moments
- [ ] Empty states are designed, not afterthoughts
- [ ] Completions are celebrated (not just a checkmark)
- [ ] Numbers animate when they change
- [ ] At least one easter egg or hidden moment
- [ ] All corners equally polished — no dirty bathrooms
- [ ] At least one moment makes someone say "oh, that's nice"

### General Taste
- [ ] No generic AI aesthetics (Inter font, purple gradients, cookie-cutter layouts)
- [ ] Typography is intentional — display + body pairing
- [ ] Color palette has a dominant color with sharp accents
- [ ] Spacing is generous and consistent
- [ ] Interface feels like a physical space, not a slideshow
- [ ] Every pixel looks placed by someone who cares

---

## Anti-Patterns — Things That Kill Taste

1. **Static tab switches.** No directional slide = digital whiplash.
2. **Modals that pop from nowhere.** Grow from trigger or slide from edge. Never just `opacity: 0 → 1` centered.
3. **Skeleton screens that don't match the real layout.** If the skeleton has 3 bars and the content has 5 lines, you've broken the illusion.
4. **Redundant animations.** A persistent header that fades out and back in during a page transition. Persistent = stays.
5. **Linear easing.** Nothing in the physical world moves linearly.
6. **"No items" empty text.** First impression. Treat it like one.
7. **Uniform sizing in stacked layers.** Two sheets the same height = no sense of depth or progression.
8. **Toasts for important outcomes.** Toasts = background info. Success/error/completion = inline, contextual, animated.
9. **Forms that are just stacked inputs.** Step-by-step with transitions between them.
10. **Buttons that don't respond to interaction.** Hover, active, and focus states. Always.
11. **Animating unchanged text.** If only one word changes in a sentence, only that word moves.
12. **Spinner left at origin after action.** Move it to where the user will look for the result.

---

## Easing & Timing Reference

| Use Case | Easing | Duration |
|---|---|---|
| Element entering | `cubic-bezier(0.16, 1, 0.3, 1)` | 300–400ms |
| Element exiting | `cubic-bezier(0.4, 0, 1, 1)` | 200–250ms |
| Shared element morph | `cubic-bezier(0.16, 1, 0.3, 1)` | 350–500ms |
| Micro-interaction (hover, press) | `cubic-bezier(0.2, 0, 0, 1)` | 100–150ms |
| Spring (bouncy) | `damping: 20, stiffness: 300` | auto |
| Spring (smooth) | `damping: 30, stiffness: 200` | auto |
| Number counting | ease-out cubic | 400–800ms |
| Page transition | `cubic-bezier(0.16, 1, 0.3, 1)` | 300ms |
| Stagger between items | — | 30–60ms per item |

---

## Recommended Tools

These libraries are built by the same people behind Family and embody the same philosophy:

| Library | Purpose | Install |
|---|---|---|
| [torph](https://torph.lochie.me/) | Dependency-free text morphing. Handles shared-letter transitions automatically. React, Vue, Svelte. | `npm i torph` |
| [liveline](https://benji.org/liveline) | Real-time animated line charts. One canvas, 60fps lerp, momentum arrows, no dependencies beyond React 18. | `npm i liveline` |

When building anything with text that changes or live numeric/chart data, reach for these before rolling your own.

---

## How to Use This Skill

1. **Read this before every UI task.** Not after. Before.
2. **Apply pillars in order.** Simplicity → Fluidity → Delight. You can't polish a bad layout with animations.
3. **Run the checklist** before delivering.
4. **Pair with `frontend-design` skill** for visual aesthetics (typography, color, layout). This skill handles *feel* and *interaction quality*.
5. **When in doubt, animate.** Easier to tone down than to add life to a dead interface.
6. **Record and review at 0.5x.** Slow motion reveals every teleport, every jarring cut, every missed opportunity.

The goal is not to make something that "works." The goal is to make something that someone uses and thinks: *"Whoever made this actually gives a shit."*

That's taste.
