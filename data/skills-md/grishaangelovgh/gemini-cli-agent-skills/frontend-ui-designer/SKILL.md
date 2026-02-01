---
name: frontend-ui-designer
description: Expert guidance for creating modern, intuitive, and visually stunning user interfaces. Use this skill when designing or implementing frontend UIs, components, layout structures, or styling.
---

# Frontend UI Designer Instructions

## 1. Visual Hierarchy & Composition
- **Priority:** Ensure the most important actions (CTAs) are most prominent. Use size, weight, and color to guide the eye.
- **F-Pattern & Z-Pattern:** Design layouts that follow natural scanning patterns for text-heavy and visual-heavy pages respectively.
- **White Space:** Use generous white space to reduce cognitive load and group related elements.
- **Grouping:** Use proximity and subtle borders/shadows to group related information (Law of Proximity).

## 2. Color Theory & Application
- **The 60-30-10 Rule:** 60% dominant neutral color (backgrounds/surfaces), 30% secondary color (borders/text), 10% accent color (CTAs/links).
- **Contrast:** Maintain WCAG AA/AAA compliance. Use high-contrast ratios for readability.
- **Semantic Colors:** Use consistent colors for status (Success: #10B981, Error: #EF4444, Warning: #F59E0B, Info: #3B82F6).
- **Dark Mode Support:** Ensure all colors have a dark mode equivalent. Use lighter grays (e.g., Slate-800/900) instead of pure black for backgrounds to reduce eye strain.
- **Modern Palette Recommendation:**
  - **Primary:** Indigo (#6366F1) or Slate (#0F172A)
  - **Surface:** White (#FFFFFF) or extremely light gray (#F8FAFC)
  - **Text:** Slate-900 (#0F172A) for headings, Slate-600 (#475569) for body text.

## 3. Typography
- **Font Pairing:** Use modern sans-serif fonts like 'Inter', 'Geist', 'Roboto', or 'SF Pro Display'. Limit to two font families.
- **Scale:** Use a modular scale (e.g., Major Third).
  - H1: 2.25rem (36px), Bold
  - H2: 1.875rem (30px), Semi-bold
  - H3: 1.5rem (24px), Semi-bold
  - Body: 1rem (16px), Regular
  - Small: 0.875rem (14px), Medium
- **Line Height:** 1.5 - 1.6 for body text to ensure readability; tighter (1.2-1.3) for headings.

## 4. Layout & Spacing
- **8pt Grid System:** Use 4, 8, 16, 24, 32, 48, 64px for all spacing. This creates a rhythmic, professional feel.
- **Containerization:** Use standard widths (max-w-7xl, max-w-5xl) to keep content centered and readable on wide screens.
- **Bento Box Grids:** Consider organized, grid-like layouts for dashboard or data-heavy views to structure information clearly.
- **Responsive Design:** Always consider Mobile-First. Use flexible flex/grid layouts.

## 5. Modern UI Trends & Techniques (2025/2026)
- **Soft Shadows & Depth:** Use `box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);` instead of harsh borders.
- **Glassmorphism:** For overlays/navbars, use `background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(10px);`.
- **Subtle Gradients:** Use very subtle linear gradients (e.g., Slate-50 to White) or mesh gradients to add depth without distraction.
- **Border Radius:** Use `rounded-lg` (8px) or `rounded-xl` (12px) for a soft, modern aesthetic.
- **Micro-interactions:** Add purposeful motion (hover states, button clicks, loading skeletons) to provide feedback and delight. Keep animations fast (150-300ms).

## 6. Component Patterns & Polishing
- **Form Design:**
  - **Single Column:** Preferred for readability and mobile-friendliness.
  - **Labels:** Always visible above inputs (avoid placeholders as labels).
  - **Validation:** Real-time inline validation with clear error messages.
  - **Autofill:** Support appropriate autocomplete attributes.
- **Empty States:**
  - **Never Blank:** Provide a helpful illustration, explanation, and a primary action button (e.g., "No projects yet. [Create Project]").
  - **Educational:** Use this space to teach users about the feature.
- **Skeleton Loading:**
  - **Perceived Performance:** Use shimmering skeleton screens instead of generic spinners for initial content loads.
  - **Structure:** Mimic the final layout (image, title, text lines) to reduce layout shift (CLS).
- **Navigation:**
  - **Thumb Zone:** Place primary navigation/actions at the bottom on mobile.
  - **Gestures:** Support common gestures like "swipe to go back" or "swipe to dismiss".

## 7. Accessibility & Inclusivity (A11y)
- **Keyboard Navigation:** Ensure all interactive elements are focusable and have visible focus states (e.g., `ring-2 ring-offset-2`).
- **Touch Targets:** Minimum touch target size of 44x44px (or 48x48px) for mobile users.
- **Screen Readers:** Use semantic HTML (`<button>`, `<nav>`, `<main>`) and ARIA labels where visual context isn't enough.
- **Neurodiversity:** Offer clear, distraction-free modes where possible. Avoid autoplaying media.

## 8. Best Practices & UX
- **Affordance:** Buttons should look clickable. Links should be clearly identifiable.
- **Feedback:** Provide immediate visual feedback for all user actions (loading states, success toasts, error messages).
- **Consistency:** Use a design system or component library to ensure buttons, inputs, and cards look identical across the app.
- **Ethical Design:** Avoid dark patterns. Be transparent about data usage and provide easy opt-outs.

# Available Resources
- [Refactoring UI](https://www.refactoringui.com/) - Practical design tips.
- [Google Material 3](https://m3.material.io/) - Design system reference.
- [Lucide Icons](https://lucide.dev/) - Clean, consistent icon set.
- [Adobe Color](https://color.adobe.com/) - Palette generation.
- [Coolors.co](https://coolors.co/) - Fast color schemes.
- [WCAG Guidelines](https://www.w3.org/WAI/standards-guidelines/wcag/) - Accessibility standards.
