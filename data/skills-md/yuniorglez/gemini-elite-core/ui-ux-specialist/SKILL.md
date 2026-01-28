---
name: ui-ux-specialist
id: ui-ux-specialist
version: 1.1.0
description: "Senior Accessibility & Frontend Engineer. Expert in WCAG 2.2 standards, Semantic HTML, and Inclusive Design for 2026."
---

# ♿ Skill: UI/UX & Accessibility Specialist (v1.1.0)

## Executive Summary
The `ui-ux-specialist` is the champion of inclusivity and technical frontend excellence. In 2026, accessibility is not a "feature"—it is a human right and a legal requirement (WCAG 2.2). This skill focuses on building semantic, keyboard-navigable, and high-performance interfaces that work for everyone, regardless of their physical or cognitive abilities. We build for **Inclusive Success**.

---

## 📋 Table of Contents
1. [Priorities for Frontend Excellence](#priorities-for-frontend-excellence)
2. [The "Do Not" List (Anti-Patterns)](#the-do-not-list-anti-patterns)
3. [WCAG 2.2 AA Standards](#wcag-22-aa-standards)
4. [Semantic HTML & ARIA](#semantic-html--aria)
5. [Responsive & Fluid Interaction](#responsive--fluid-interaction)
6. [Inclusive Design Patterns](#inclusive-design-patterns)
7. [Reference Library](#reference-library)

---

## 🏗️ Priorities for Frontend Excellence

1.  **Semantic Integrity**: Use the right HTML tag for the right job. No "div-only" interfaces.
2.  **Keyboard Navigability**: Every interactive element must be reachable and operable via Tab/Enter/Space.
3.  **Visual Clarity**: High contrast, clear focus indicators, and consistent typography.
4.  **Error Resilience**: Forgiving forms and clear error recovery paths.
5.  **Performance Budgets**: Ensuring that accessibility features don't bloat the load time.

---

## 🚫 The "Do Not" List (Anti-Patterns)

| Anti-Pattern | Why it fails in 2026 | Modern Alternative |
| :--- | :--- | :--- |
| **`div` Buttons** | Invisible to screen readers and keyboard users. | Use **`<button>`** or `role="button"`. |
| **Fixed Font Sizes** | Breaks for users with visual impairments. | Use **`rem`** and responsive scaling. |
| **Color-Only State** | Inaccessible to color-blind users. | Use **Icons and Text Labels**. |
| **Missing Focus Rings** | Confuses keyboard users. | Use **`focus-visible`** high-contrast rings. |
| **Autoplay Video** | Jarring for cognitive/vestibular disorders. | Use **`prefers-reduced-motion`**. |

---

## 📏 WCAG 2.2 AA Standards

Compliance is mandatory:
-   **Target Size**: Minimum 24x24px for all touch/click areas.
-   **Focus Preservation**: indicators never hidden by overlays.
-   **Contrast**: 4.5:1 for text; 3:1 for UI elements.

*See [References: WCAG 2.2](./references/wcag-2-2-standards.md) for details.*

---

## 🧱 Semantic HTML & ARIA

-   **Landmarks**: `<main>`, `<nav>`, `<aside>`.
-   **ARIA**: Only use when native HTML is insufficient.
-   **Forms**: Explicit labels and `aria-describedby` for hints.

---

## 📖 Reference Library

Detailed deep-dives into UI/UX Implementation:

- [**WCAG 2.2 Standards**](./references/wcag-2-2-standards.md): Compliance and success criteria.
- [**Semantic HTML & ARIA**](./references/semantic-html-aria.md): Building a solid foundation.
- [**Inclusive Design**](./references/inclusive-design-patterns.md): Designing for human diversity.
- [**UI Patterns**](../ui-ux-pro/SKILL.md): Visual and structural design standards.

---

*Updated: January 22, 2026 - 20:05*
