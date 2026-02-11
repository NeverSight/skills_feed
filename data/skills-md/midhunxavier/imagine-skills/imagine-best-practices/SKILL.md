---
name: imagine-best-practices
description: Publication-quality scientific figures with the Imagine framework (React → SVG/PNG). Use when designing, reviewing, or exporting charts/diagrams/multi-panel figures for papers, posters, or preprints, especially when you need mm+dpi sizing, vector-first SVG, typography/color guidance, and final submission checks.
---

## When to use

Use this skill whenever you are working on Imagine figures for scientific articles, especially when you need:

- publication-oriented sizing (`mm` + `dpi`)
- SVG-first figure components
- chart/diagram/multi-panel/math patterns
- deterministic scaffolding for new projects and figures
- reliable PNG/SVG export and renderer debugging

## Scaffolding

When creating projects and figures, load [./rules/scaffold-cli.md](./rules/scaffold-cli.md) and [./rules/scaffold-templates.md](./rules/scaffold-templates.md) first.

## How to use

Read individual rule files for focused implementation guidance:

- [rules/project-structure.md](./rules/project-structure.md) - Project folder and module conventions for Imagine
- [rules/manifest-and-variants.md](./rules/manifest-and-variants.md) - Figure manifest schema, variants, props, controls, sizing
- [rules/components-svg-only.md](./rules/components-svg-only.md) - SVG-first component patterns for clean vector export
- [rules/publication-quality.md](./rules/publication-quality.md) - Paper-ready design checklist (size, typography, color, multi-panel)
- [rules/rendering-and-export.md](./rules/rendering-and-export.md) - Render pipeline and export workflows
- [rules/troubleshooting.md](./rules/troubleshooting.md) - Common rendering and export failures

- [rules/scaffold-cli.md](./rules/scaffold-cli.md) - `new_project.mjs` and `new_figure.mjs` usage
- [rules/scaffold-templates.md](./rules/scaffold-templates.md) - Included templates and default kind mappings

- [rules/chart-patterns.md](./rules/chart-patterns.md) - D3 scale/axis/grid/legend chart patterns
- [rules/publication-chart-style.md](./rules/publication-chart-style.md) - Chart typography, stroke, marker, and density standards

- [rules/diagram-primitives.md](./rules/diagram-primitives.md) - Box/Arrow/Label/Callout usage
- [rules/layout-and-spacing.md](./rules/layout-and-spacing.md) - Diagram alignment and spacing heuristics

- [rules/multi-panel-guidelines.md](./rules/multi-panel-guidelines.md) - Panel labels, shared legends, spacing

- [rules/mathjax-and-rendering.md](./rules/mathjax-and-rendering.md) - MathJax behavior in render/export
- [rules/latex-authoring-tips.md](./rules/latex-authoring-tips.md) - LaTeX writing patterns for figure text

- [rules/render-cli.md](./rules/render-cli.md) - Renderer CLI cookbook
- [rules/debugging.md](./rules/debugging.md) - Renderer debugging playbook
