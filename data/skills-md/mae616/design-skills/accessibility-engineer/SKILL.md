---
name: accessibility-engineer
description: Apply semantic HTML/JSX and WAI-ARIA correctly and minimally. Apply when implementing any UI, especially forms, interactive components, or when accessibility is mentioned.
user-invocable: false
metadata:
  tags: accessibility, a11y, aria, semantic-html, screen-reader, keyboard
---

# Accessibility Engineer Skill

## When to Apply

Apply this skill when the request involves:
- Accessibility, a11y, WAI-ARIA, screen reader support, semantic HTML, keyboard navigation, focus management
- アクセシビリティ対応、WAI-ARIA、スクリーンリーダー対応、セマンティックHTML、キーボード操作、フォーカス管理
- Any UI implementation (should be applied alongside other skills)

## Core Principles (Most Important)

- **Native elements first.** Solve with proper HTML elements (`button`, `a`, `label`, `input`, etc.) before reaching for ARIA.
- **ARIA is minimal.** Don't add `role`/`aria-*` to make things "seem" accessible. Only add when there's a real requirement.
- **Operable = Communicable.** Not just visually—assistive tech must receive state, name, and purpose. This is the Definition of Done.
- **Keyboard is the baseline.** Mouse-only UI is incomplete. Design focus movement and operations first.

## Implementation Rules

### 1) Semantic Structure

- Maintain heading order (`h1` → `h2` → ...). Don't skip levels for styling.
- Create landmarks for main regions (`header`, `nav`, `main`, `footer`, `aside` if needed).
- Use `ul/ol/li` for lists, `dl/dt/dd` for definitions—not `div` substitutes.

### 2) Accessible Names

- Buttons, links, inputs need "names" (labels read by screen readers).
  - Priority: **Visible text**
  - Fallback: `aria-label` (when visible text isn't possible)
  - Composition: `aria-labelledby` (referencing existing elements)
- Icon-only buttons/links MUST have names (e.g., "Search", "Close").

### 3) Forms (Required)

- Associate `label` with `input` (`for`/`id`). Never use placeholder as the only label.
- Communicate required/optional, errors, hints machine-readably (e.g., `aria-describedby` for helper text).
- Errors must explain: what's wrong, why, and how to fix.

### 4) States and Announcements (Dynamic UI)

- Use native `disabled` attribute first (`button disabled`, etc.).
- For toggles, use `aria-pressed` / `aria-expanded` only when native elements aren't sufficient.
- Use `aria-live` for async completion/failure announcements—but don't overuse.

### 5) Keyboard Operation and Focus

- Design DOM order so tab sequence is logical. Don't force reorder with `tabindex`.
- `tabindex="0"`: minimal use to make something focusable.
- `tabindex="-1"`: only for programmatic focus movement.
- Always preserve visible focus (`focus-visible`). Never hide it.
- Dialogs/modals: define focus destination on open and return destination on close. Implement focus trap if needed.

### 6) Images and Media

- Use `alt` based on purpose (decorative images get empty `alt=""`).
- For video/audio: confirm controls (play/stop) and alternatives (captions/transcript). Ask if unclear.

## Anti-Patterns (Never Do This)

- `div` with `onClick` acting as button (breaks keyboard/role).
- Using `role="button"` as a workaround (use native `button`).
- Adding `aria-label` everywhere (causes duplicate announcements when visible label exists).
- Removing focus ring (invisible focus = inoperable).

## Clarification Questions (Don't Assume)

- Must this UI be completable with keyboard only? (If yes, enumerate operation steps and agree.)
- For modal/drawer: what gets focus on open? What gets focus on close?
- When are errors announced? Immediately? After submit?
- Does video/audio need captions or text alternatives?

## Output Format (For Implementation)

1. Semantic structure (landmarks, headings, lists)
2. Keyboard operation (Tab order, Enter, Space, Escape)
3. ARIA usage (only where needed, with justification)
4. States (disabled/loading/error) and announcements (aria-live if needed)
5. Accessibility checklist self-assessment (OK / needs work)
