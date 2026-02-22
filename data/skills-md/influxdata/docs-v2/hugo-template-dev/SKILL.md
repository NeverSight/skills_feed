---
name: hugo-template-dev
description: Hugo template development skill for InfluxData docs-v2. Enforces proper build and runtime testing to catch template errors that build-only validation misses.
author: InfluxData
version: "1.1"
---

# Hugo Template Development Skill

## Purpose

This skill enforces proper Hugo template development practices, including **mandatory runtime testing** to catch errors that static builds miss.

## Critical Testing Requirement

**Hugo's `npx hugo --quiet` only validates template syntax, not runtime execution.**

Template errors like accessing undefined fields, nil values, or incorrect type assertions only appear when Hugo actually renders pages. You MUST test templates by running the server.

## Mandatory Testing Protocol

### For ANY Hugo Template Change

After modifying files in `layouts/`, `layouts/partials/`, or `layouts/shortcodes/`:

**Step 1: Start Hugo server and capture output**

```bash
npx hugo server --port 1315 2>&1 | head -50
```

**Success criteria:**

- No `error calling partial` messages
- No `can't evaluate field` errors
- No `template: ... failed` messages
- Server shows "Web Server is available at <http://localhost:1315/>"

**If errors appear:** Fix the template and repeat Step 1 before proceeding.

**Step 2: Verify the page renders**

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:1315/PATH/TO/PAGE/
```

**Expected:** HTTP 200 status code

**Step 3: Browser testing (if MCP browser tools available)**

If `mcp__claude-in-chrome__*` tools are available, use them for visual inspection:

```
# Navigate and screenshot
mcp__claude-in-chrome__navigate({ url: "http://localhost:1315/PATH/", tabId: ... })
mcp__claude-in-chrome__computer({ action: "screenshot", tabId: ... })

# Check for JavaScript errors
mcp__claude-in-chrome__read_console_messages({ tabId: ..., onlyErrors: true })
```

This catches runtime JavaScript errors that template changes may introduce.

**Step 4: Stop the test server**

```bash
pkill -f "hugo server --port 1315"
```

### Quick Test Command

Use this one-liner to test and get immediate feedback:

```bash
timeout 15 npx hugo server --port 1315 2>&1 | grep -E "(error|Error|ERROR|fail|FAIL)" | head -20; pkill -f "hugo server --port 1315" 2>/dev/null
```

If output is empty, no errors were detected.

## Common Hugo Template Errors

### 1. Accessing Hyphenated Keys

**Wrong:**

```go
{{ .Site.Data.article-data.influxdb }}
```

**Correct:**

```go
{{ index .Site.Data "article-data" "influxdb" }}
```

### 2. Nil Field Access

**Wrong:**

```go
{{ range $articles }}
  {{ .path }}  {{/* Fails if item is nil or wrong type */}}
{{ end }}
```

**Correct:**

```go
{{ range $articles }}
  {{ if . }}
    {{ with index . "path" }}
      {{ . }}
    {{ end }}
  {{ end }}
{{ end }}
```

### 3. Type Assertion on Interface{}

**Wrong:**

```go
{{ range $data }}
  {{ .fields.menuName }}
{{ end }}
```

**Correct:**

```go
{{ range $data }}
  {{ if isset . "fields" }}
    {{ $fields := index . "fields" }}
    {{ if isset $fields "menuName" }}
      {{ index $fields "menuName" }}
    {{ end }}
  {{ end }}
{{ end }}
```

### 4. Empty Map vs Nil Check

**Problem:** Hugo's `{{ if . }}` passes for empty maps `{}`:

```go
{{/* This doesn't catch empty maps */}}
{{ if $data }}
  {{ .field }}  {{/* Still fails if $data is {} */}}
{{ end }}
```

**Solution:** Check for specific keys:

```go
{{ if and $data (isset $data "field") }}
  {{ index $data "field" }}
{{ end }}
```

## Hugo Data Access Patterns

### Safe Nested Access

```go
{{/* Build up access with nil checks at each level */}}
{{ $articleDataRoot := index .Site.Data "article-data" }}
{{ if $articleDataRoot }}
  {{ $influxdbData := index $articleDataRoot "influxdb" }}
  {{ if $influxdbData }}
    {{ $productData := index $influxdbData $dataKey }}
    {{ if $productData }}
      {{ with $productData.articles }}
        {{/* Safe to use . here */}}
      {{ end }}
    {{ end }}
  {{ end }}
{{ end }}
```

### Iterating Over Data Safely

```go
{{ range $idx, $item := $articles }}
  {{/* Declare variables with defaults */}}
  {{ $path := "" }}
  {{ $name := "" }}

  {{/* Safely extract values */}}
  {{ if isset $item "path" }}
    {{ $path = index $item "path" }}
  {{ end }}

  {{ if $path }}
    {{/* Now safe to use $path */}}
  {{ end }}
{{ end }}
```

## File Organization

### Layouts Directory Structure

```
layouts/
├── _default/           # Default templates
├── partials/           # Reusable template fragments
│   └── api/            # API-specific partials
├── shortcodes/         # Content shortcodes
└── TYPE/               # Type-specific templates (api/, etc.)
    └── single.html     # Single page template
```

### Partial Naming

- Use descriptive names: `api/sidebar-nav.html`, not `nav.html`
- Group related partials in subdirectories
- Include comments at the top describing purpose and required context

## Separation of Concerns: Templates vs TypeScript

**Principle:** Hugo templates handle structure and data binding. TypeScript handles behavior and interactivity.

### What Goes Where

| Concern          | Location                    | Example                             |
| ---------------- | --------------------------- | ----------------------------------- |
| HTML structure   | `layouts/**/*.html`         | Navigation markup, tab containers   |
| Data binding     | `layouts/**/*.html`         | `{{ .Title }}`, `{{ range .Data }}` |
| Static styling   | `assets/styles/**/*.scss`   | Layout, colors, typography          |
| User interaction | `assets/js/components/*.ts` | Click handlers, scroll behavior     |
| State management | `assets/js/components/*.ts` | Active tabs, collapsed sections     |
| DOM manipulation | `assets/js/components/*.ts` | Show/hide, class toggling           |

### Anti-Pattern: Inline JavaScript in Templates

**Wrong - JavaScript mixed with template:**

```html
{{/* DON'T DO THIS */}}
<nav class="api-nav">
  {{ range $articles }}
    <button onclick="toggleSection('{{ .id }}')">{{ .name }}</button>
  {{ end }}
</nav>

<script>
function toggleSection(id) {
  document.getElementById(id).classList.toggle('is-open');
}
</script>
```

**Correct - Clean separation:**

Template (`layouts/partials/api/sidebar-nav.html`):

```html
<nav class="api-nav" data-component="api-nav">
  {{ range $articles }}
    <button class="api-nav-group-header" aria-expanded="false">
      {{ .name }}
    </button>
    <ul class="api-nav-group-items">
      {{/* items */}}
    </ul>
  {{ end }}
</nav>
```

TypeScript (`assets/js/components/api-nav.ts`):

```typescript
interface ApiNavOptions {
  component: HTMLElement;
}

export default function initApiNav({ component }: ApiNavOptions): void {
  const headers = component.querySelectorAll('.api-nav-group-header');

  headers.forEach((header) => {
    header.addEventListener('click', () => {
      const isOpen = header.classList.toggle('is-open');
      header.setAttribute('aria-expanded', String(isOpen));
      header.nextElementSibling?.classList.toggle('is-open', isOpen);
    });
  });
}
```

Register in `main.js`:

```javascript
import initApiNav from './components/api-nav.js';

const componentRegistry = {
  'api-nav': initApiNav,
  // ... other components
};
```

### Data Passing Pattern

Pass Hugo data to TypeScript via `data-*` attributes:

Template:

```html
<div
  data-component="api-toc"
  data-headings="{{ .headings | jsonify | safeHTMLAttr }}"
  data-scroll-offset="80"
>
</div>
```

TypeScript:

```typescript
interface TocOptions {
  component: HTMLElement;
}

interface TocData {
  headings: string[];
  scrollOffset: number;
}

function parseData(component: HTMLElement): TocData {
  const headingsRaw = component.dataset.headings;
  const headings = headingsRaw ? JSON.parse(headingsRaw) : [];
  const scrollOffset = parseInt(component.dataset.scrollOffset || '0', 10);

  return { headings, scrollOffset };
}

export default function initApiToc({ component }: TocOptions): void {
  const data = parseData(component);
  // Use data.headings and data.scrollOffset
}
```

### Minimal Inline Scripts (Exception)

The **only** acceptable inline scripts are minimal initialization that MUST run before component registration:

```html
{{/* Acceptable: Critical path, no logic, runs immediately */}}
<script>
  document.documentElement.dataset.theme =
    localStorage.getItem('theme') || 'light';
</script>
```

Everything else belongs in `assets/js/`.

### TypeScript Component Checklist

When creating a new interactive feature:

1. [ ] Create TypeScript file in `assets/js/components/`
2. [ ] Define interface for component options
3. [ ] Export default initializer function
4. [ ] Register in `main.js` componentRegistry
5. [ ] Add `data-component` attribute to HTML element
6. [ ] Pass data via `data-*` attributes (not inline JS)
7. [ ] **NO inline `<script>` tags in templates**

## Debugging Templates

### Enable Verbose Mode

```bash
npx hugo server --port 1315 --verbose 2>&1 | head -100
```

### Print Variables for Debugging

```go
{{/* Temporary debugging - REMOVE before committing */}}
<pre>{{ printf "%#v" $myVariable }}</pre>
```

### Check Data File Loading

```bash
# Verify data files exist and are valid YAML
cat data/article-data/influxdb/influxdb3-core/articles.yml | head -20
```

## Integration with CI/CD

### Pre-commit Hook (Recommended)

Add to `.lefthook.yml` or pre-commit configuration:

```yaml
pre-commit:
  commands:
    hugo-template-test:
      glob: "layouts/**/*.html"
      run: |
        timeout 20 npx hugo server --port 1315 2>&1 | grep -E "error|Error" && exit 1 || exit 0
        pkill -f "hugo server --port 1315" 2>/dev/null
```

### GitHub Actions Workflow

```yaml
- name: Test Hugo templates
  run: |
    npx hugo server --port 1315 &
    sleep 10
    curl -f http://localhost:1315/ || exit 1
    pkill -f hugo
```

## Quick Reference

| Action                    | Command                                                              |
| ------------------------- | -------------------------------------------------------------------- |
| Test templates (runtime)  | `npx hugo server --port 1315 2>&1 \| head -50`                       |
| Build only (insufficient) | `npx hugo --quiet`                                                   |
| Check specific page       | `curl -s -o /dev/null -w "%{http_code}" http://localhost:1315/path/` |
| Stop test server          | `pkill -f "hugo server --port 1315"`                                 |
| Debug data access         | `<pre>{{ printf "%#v" $var }}</pre>`                                 |

## Remember

1. **Never trust `npx hugo --quiet` alone** - it only checks syntax
2. **Always run the server** to test template changes
3. **Check error output first** before declaring success
4. **Use `isset` and `index`** for safe data access
5. **Hyphenated keys require `index` function** - dot notation fails

## Related Skills

- **cypress-e2e-testing** - For E2E testing of UI components and pages
- **docs-cli-workflow** - For creating/editing documentation content
- **ts-component-dev** (agent) - TypeScript component behavior and interactivity
- **ui-testing** (agent) - Cypress E2E testing for UI components
