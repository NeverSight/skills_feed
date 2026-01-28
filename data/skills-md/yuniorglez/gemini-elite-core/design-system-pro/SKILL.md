---
name: design-system-pro
description: Senior Design System Architect & Token Engineer for 2026. Specialized in layered design tokens, Tailwind 4 CSS-first themes, and headless UI orchestration using Radix. Expert in building multi-brand, multi-theme systems with high architectural integrity, automated documentation-as-code, and AI-driven drift detection.
---

# 🎨 Skill: design-system-pro (v1.0.0)

## Executive Summary
Senior Design System Architect & Token Engineer for 2026. Specialized in layered design tokens, Tailwind 4 CSS-first themes, and headless UI orchestration using Radix. Expert in building multi-brand, multi-theme systems with high architectural integrity, automated documentation-as-code, and AI-driven drift detection.

---

## 📋 The Conductor's Protocol

1.  **Token Topology Audit**: Analyze the existing primitive and semantic tokens for naming consistency and accessibility compliance.
2.  **Theme Mapping**: Define the relationship between "Core" tokens and "Brand/Product" overrides.
3.  **Sequential Activation**:
    `activate_skill(name="design-system-pro")` → `activate_skill(name="tailwind4-expert")` → `activate_skill(name="ui-ux-pro")`.
4.  **Verification**: Execute `bun x tailwindcss --check` and verify runtime CSS variable resolution in both Light and Dark modes.

---

## 🛠️ Mandatory Protocols (2026 Standards)

### 1. Layered Token Architecture
As of 2026, a flat token list is a legacy pattern.
- **Rule**: Follow the **Primitive → Semantic → Component** hierarchy.
- **Protocol**: Never use primitive tokens (e.g., `blue-500`) directly in components. Use semantic tokens (e.g., `action-primary-bg`).

### 2. Tailwind 4 CSS-First Configuration
- **Rule**: The `tailwind.config.js` is deprecated. Use `@theme` blocks in CSS.
- **Protocol**: Centralize tokens as native CSS variables in a `packages/design-tokens` package for runtime interoperability.

### 3. Headless UI & Radix Integration
- **Rule**: Avoid "Themed Components" that bundle styles. Use headless logic (Radix) and apply semantic utility classes.
- **Protocol**: Ensure all components support high-contrast modes and respect `prefers-reduced-motion`.

### 4. Documentation-as-Code (DaC)
- **Rule**: Documentation must be a side-effect of the code, not a manual task.
- **Protocol**: Use JSON-LD or typed JSON files as the source of truth for tokens, transformed via Style Dictionary for CSS, Android, and iOS.

---

## 🚀 Show, Don't Just Tell (Implementation Patterns)

### Tailwind 4 CSS-First Theme
`packages/design-tokens/src/base.css`:
```css
@import "tailwindcss";

@theme {
  /* Primitive Scale */
  --color-blue-500: #3b82f6;
  
  /* Semantic Layer */
  --color-brand-primary: var(--color-blue-500);
  --color-action-hover: color-mix(in srgb, var(--color-brand-primary), black 10%);
  
  /* Component Layer */
  --button-radius: var(--radius-lg);
}
```

### Semantic Component Usage (React 19 + Radix)
```tsx
import * as Tooltip from "@radix-ui/react-tooltip";

export function CustomTooltip({ children, content }: { children: React.ReactNode, content: string }) {
  return (
    <Tooltip.Root>
      <Tooltip.Trigger asChild>{children}</Tooltip.Trigger>
      <Tooltip.Content 
        // Using semantic Tailwind 4 classes
        className="bg-brand-primary text-white p-2 rounded-button shadow-xl animate-in fade-in"
      >
        {content}
        <Tooltip.Arrow className="fill-brand-primary" />
      </Tooltip.Content>
    </Tooltip.Root>
  );
}
```

---

## 🛡️ The Do Not List (Anti-Patterns)

1.  **DO NOT** hardcode hex codes or pixel values in components. Always use tokens.
2.  **DO NOT** create "Component Overrides" via deep CSS nesting. Use CSS variables.
3.  **DO NOT** ignore the accessibility of your color tokens. Check contrast ratios at the "Semantic" layer.
4.  **DO NOT** build a design system without a dedicated "Sandbox" (Storybook or internal docs).
5.  **DO NOT** mix naming conventions. If you use `camelCase` for variables, don't use `kebab-case` for tokens.

---

## 📂 Progressive Disclosure (Deep Dives)

- **[Layered Token Strategy](./references/token-layers.md)**: Primitives, Semantics, and Components.
- **[Tailwind 4 Monorepo Config](./references/tw4-monorepo.md)**: CSS-First themes at scale.
- **[Headless UI Patterns](./references/headless-patterns.md)**: Using Radix and Aria-Kit.
- **[Automated Token Pipelines](./references/token-pipelines.md)**: From Figma to Production with Style Dictionary.

---

## 🛠️ Specialized Tools & Scripts

- `scripts/validate-contrast.py`: Audits the semantic token list for WCAG 2.2 compliance.
- `scripts/generate-theme-json.ts`: Exports the CSS `@theme` block into a JSON format for mobile apps.

---

## 🎓 Learning Resources
- [Tailwind CSS v4.0 Alpha Docs](https://tailwindcss.com/blog/tailwindcss-v4-alpha)
- [Radix UI primitives](https://www.radix-ui.com/)
- [Design Tokens Community Group](https://www.w3.org/community/design-tokens/)

---
*Updated: January 23, 2026 - 21:55*
