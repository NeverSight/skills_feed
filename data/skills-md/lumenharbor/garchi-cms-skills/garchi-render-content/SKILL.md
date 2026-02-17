---
name: garchi-render-content
description: Render and integrate content from Garchi CMS into an app/website (Next/Nuxt/Laravel/etc). This skill focuses on code architecture, fetching, and rendering. Content creation/management should be done via MCP tools or the CMS.
---

# Skill: garchi-render-content

## Scope
- ✅ Build or improve the code needed to **fetch and render** Garchi CMS content (pages, sections, data items).
- ✅ Integrate Garchi CMS into an existing codebase without breaking conventions.
- ❌ Do not manage CMS content (create pages/sections/assets/templates) unless the user explicitly asks. Prefer MCP tools for CMS actions.

## Always (non-negotiable rules)
1. **Preserve Visual Editor attributes**
   - For every section component, forward unknown/extra props/attributes to the **root element** (outermost wrapper).
   - Framework-agnostic rule: “Unknown attributes must not be dropped; attach them to the root/host element.”
   - Patterns:
     - React/Preact/Solid: spread `...other` on root
     - Vue: `v-bind="$attrs"` on root
     - Svelte: spread `...$$restProps` on root
     - Angular: preserve/pass through host attributes; do not strip unknown attrs
     - Web Components: keep attrs on host or forward to outer wrapper
     - Laravel Blade: ensure attributes are passed to the root element of the section component {{ $attributes->merge()}}

2. **Do not modify reference snippets/docs**
   - Treat [code-snippets](./resources/code-snippet.md) and provided examples as reference. Do not rewrite them unless asked.

3. **Keep codebase conventions**
   - Follow existing linting, formatting, naming, and folder conventions.
   - Avoid large refactors unless requested.

## Initial checks (do first)
1. Read [Garchi CMS documentation](./resources/garchi-cms-doc.md) (mandatory).
2. Review [OpenAPI spec](https://garchi.co.uk/docs/v2.openapi) (mandatory).
3. Read [Node SDK documentation](./resources/garchi-sdk-node.md) if using Node (optional but recommended).
4. Read [PHP SDK documentation](./resources/garchi-sdk-php.md) if using PHP (optional but recommended).
5. Identify the target stack and project type:
   - Is this a starter-kit project or an existing codebase?
6. Confirm configuration:
   - API key + Space UID available in `.env` / config
   - If preview mode is needed: preview token config exists

## Recommended implementation workflow
### A) Choose access method
- Prefer starter kits for fresh projects. Ask user for the choice of available stack, next, nuxt, and laravel.
- Prefer SDKs where available (Node SDK / PHP SDK).
- If using raw API, create a small service layer (DRY/SOLID, typed, reusable). Raw API call should be made from server environment and is doesn't support client side calls. Use the OpenAPI spec for reference.

### B) Build the rendering pipeline
1. Fetch page/data item from server-side (SSR/server runtime).
2. Render sections via a single section renderer (mapper).
3. Each section maps to a reusable component.
4. Support nested sections (`subsections`) if present.

### C) Quality + safety
- Sanitize HTML before rendering (XSS).
- Handle errors gracefully (notFound, fallback UI).
- Use stable keys (prefer section id/uid over array index when available).
- Add basic logging for missing components or invalid payload shapes.

## Definition of Done (what “complete” means)
- Pages/data items render correctly in the chosen stack.
- Visual Editor attributes are preserved on all section components.
- Preview/draft mode works (if required).
- Errors are handled without infinite retries/loops.
- HTML content is sanitized where applicable.

## Loop prevention (stop conditions)
- Do not retry the same failing operation more than 2 times.
- After an update/fetch, verify state once; if still incorrect, stop and report what’s missing.
