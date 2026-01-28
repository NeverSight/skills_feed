---
name: faion-frontend-developer
description: "Frontend: Tailwind, CSS-in-JS, design tokens, UI libraries, PWA, accessibility."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite, Skill
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# Frontend Developer Skill

Frontend development specializing in styling, UI libraries, design systems, and modern frontend patterns.

## Purpose

Handles frontend styling, design systems, UI component libraries, accessibility, PWA, and responsive design.

## When to Use

- Tailwind CSS styling and architecture
- Design tokens and design systems
- CSS-in-JS patterns
- UI component libraries (shadcn/ui, etc.)
- Progressive Web Apps (PWA)
- Responsive and mobile design
- Accessibility (a11y)
- SEO for SPAs
- Storybook component development

## Methodologies

| Category | Methodology | File |
|----------|-------------|------|
| **Tailwind CSS** |
| Tailwind basics | Setup, utilities, responsive design | tailwind.md |
| Tailwind architecture | Component organization, theme config | tailwind-architecture.md |
| Tailwind patterns | Best practices, patterns, plugins | tailwind-patterns.md |
| **CSS-in-JS** |
| CSS-in-JS basics | Styled components, emotion basics | css-in-js-basics.md |
| CSS-in-JS advanced | Theme, SSR, performance | css-in-js-advanced.md |
| **Design Systems** |
| Design tokens basics | Token structure, naming conventions | design-tokens-basics.md |
| Design tokens implementation | Token generation, tooling | design-tokens-implementation.md |
| **UI Libraries** |
| shadcn/ui | Component setup and usage | shadcn-ui.md |
| shadcn/ui architecture | Project structure, customization | shadcn-ui-architecture.md |
| UI lib basics | Component library patterns | ui-lib-basics.md |
| UI lib patterns | Advanced component patterns | ui-lib-patterns.md |
| Storybook setup | Storybook configuration, stories | storybook-setup.md |
| **Responsive & Mobile** |
| Mobile responsive | Responsive design, breakpoints | mobile-responsive.md |
| **PWA** |
| PWA core | Service workers, caching, offline | pwa-core.md |
| PWA advanced | Push notifications, sync, install | pwa-advanced.md |
| **SEO & Accessibility** |
| SEO for SPAs | SSR, meta tags, structured data | seo-for-spas.md |
| Accessibility | ARIA, keyboard nav, screen readers | accessibility.md |
| **Frontend Design** |
| Frontend design | UI/UX implementation patterns | frontend-design.md |

## Tools

- **Styling:** Tailwind CSS, CSS-in-JS (styled-components, emotion)
- **Design tokens:** Style Dictionary, Figma Tokens
- **UI libraries:** shadcn/ui, Radix UI, Headless UI
- **Storybook:** Component development and documentation
- **Accessibility:** axe-core, WAVE, Lighthouse

## Related Sub-Skills

| Sub-skill | Relationship |
|-----------|--------------|
| faion-javascript-developer | React components, Next.js |
| faion-ux-ui-designer | Design specs and mockups |
| faion-devtools-developer | Build tools, bundlers |

## Integration

Invoked by parent skill `faion-software-developer` for frontend styling and UI work.

---

*faion-frontend-developer v1.0 | 18 methodologies*
