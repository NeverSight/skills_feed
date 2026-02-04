---
name: bootstrap-components
description: This skill should be used when the user asks about Bootstrap components, "how to create a modal", "navbar not collapsing", "carousel autoplay", "responsive card grid", "toast notifications", "dropdown menu", "accordion FAQ", "offcanvas sidebar", "tab navigation", "tooltip not showing", "popover not working", Bootstrap accordion, alerts, badges, breadcrumb, buttons, button groups, cards, carousel, close button, collapse, dropdowns, list group, modal, navbar, navs and tabs, offcanvas, pagination, placeholders, popovers, progress, scrollspy, spinners, toasts, tooltips, or needs help implementing any Bootstrap UI component.
---

# Bootstrap 5.3 Components

Bootstrap provides ready-to-use UI components for building interfaces. This skill covers all major components with usage patterns, JavaScript initialization requirements, and accessibility best practices.

**JavaScript Initialization Overview:** Some components work purely with data attributes, while others require JavaScript initialization. Components marked with **Requires JS** below won't function without explicit initialization.

| Component | Requires JS Init | Data Attributes Only |
|-----------|------------------|----------------------|
| Tooltip | Yes | No |
| Popover | Yes | No |
| Toast | Yes (to show) | No |
| Scrollspy | Optional | Yes |
| Modal | Optional | Yes |
| Carousel | Optional | Yes |
| Collapse | Optional | Yes |
| Dropdown | Optional | Yes |

## Interactive Components

These components require or benefit from JavaScript. See `references/interactive-components.md` for detailed code examples, JavaScript APIs, and accessibility guidance.

### Accordion

Collapsible content panels that show one section at a time. Use `.accordion` wrapper with `.accordion-item` children containing `.accordion-header` and `.accordion-collapse`. Remove `data-bs-parent` to allow multiple panels open simultaneously. Use `.accordion-flush` for borderless variant.

### Carousel

Image slideshow with optional controls and indicators. Use `.carousel.slide` wrapper with `.carousel-inner` containing `.carousel-item` slides. Add `.carousel-control-prev`/`.carousel-control-next` for navigation. Use `data-bs-ride="carousel"` for autoplay. Respects `prefers-reduced-motion` automatically.

### Collapse

Toggle content visibility with smooth animations. Use `data-bs-toggle="collapse"` on trigger with `data-bs-target` pointing to `.collapse` element. Use `.collapse-horizontal` for width-based collapse. Target multiple elements with class selector (`.multi-collapse`).

### Dropdowns

Toggleable contextual menus for links and actions. Use `.dropdown` wrapper with `.dropdown-toggle` button and `.dropdown-menu` list. Direction variants: `.dropup`, `.dropend`, `.dropstart`. Add `.dropdown-menu-dark` for dark theme. Keyboard navigation is built-in.

### Modal

Dialog boxes that overlay the page and trap focus. Use `data-bs-toggle="modal"` with `data-bs-target` pointing to `.modal` element. Sizes: `.modal-sm`, `.modal-lg`, `.modal-xl`. Modifiers: `.modal-dialog-centered`, `.modal-dialog-scrollable`. Use `data-bs-backdrop="static"` to prevent dismiss on outside click.

### Offcanvas

Hidden sidebars that slide from viewport edge. Positions: `.offcanvas-start` (left), `.offcanvas-end` (right), `.offcanvas-top`, `.offcanvas-bottom`. Use `data-bs-scroll="true"` to allow body scrolling. Use `data-bs-backdrop="static"` for persistent sidebars.

### Popovers

**Requires JS init and Popper.js.** Rich overlay content triggered by click or hover. Use `data-bs-toggle="popover"` with `data-bs-title` and `data-bs-content`. Initialize with `new bootstrap.Popover(el)` or batch initialize all: `document.querySelectorAll('[data-bs-toggle="popover"]').forEach(el => new bootstrap.Popover(el))`. Placements: top, right, bottom, left. Use `bootstrap.bundle.js` (includes Popper) or include Popper separately before `bootstrap.js`.

### Scrollspy

Auto-update navigation based on scroll position. Use `data-bs-spy="scroll"` on scrollable container with `data-bs-target` pointing to nav. Use `data-bs-root-margin` to control activation threshold. Container needs `tabindex="0"` so keyboard-only users can focus and scroll the container without a mouse.

### Toasts

**Requires JS to show.** Lightweight dismissible notifications. Use `.toast-container` for positioning and stacking. Initialize with `new bootstrap.Toast(el)` then call `.show()`. Options: `autohide: true`, `delay: 5000`. Placements via container positioning classes.

### Tooltips

**Requires JS init and Popper.js.** Hover hints for brief descriptions. Use `data-bs-toggle="tooltip"` with `data-bs-title` (preferred) or `title` attribute. Initialize with `new bootstrap.Tooltip(el)` or batch initialize all: `document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => new bootstrap.Tooltip(el))`. Placements: top, right, bottom, left. Tooltips on disabled buttons require a wrapper `<span>` or `<div>` with `tabindex="0"` for keyboard accessibility. Use `bootstrap.bundle.js` (includes Popper) or include Popper separately before `bootstrap.js`.

## Static Components

These components work primarily with CSS and HTML. See `references/static-components.md` for detailed code examples and accessibility guidance.

### Alerts

Contextual feedback messages. Use `.alert.alert-{color}` with `role="alert"`. Colors: primary, secondary, success, danger, warning, info, light, dark. Use `.alert-link` for styled links. Add `.alert-dismissible` with close button for dismissible alerts.

### Badges

Labels, counters, and status indicators. Use `.badge.bg-{color}` on `<span>`. Use `.rounded-pill` for pill shape. Position with `.position-absolute` utilities for notification badges. Include `.visually-hidden` text for screen reader context.

### Breadcrumb

Navigation hierarchy indicator. Wrap `<ol class="breadcrumb">` in `<nav aria-label="breadcrumb">`. Use `.breadcrumb-item` on `<li>` elements. Mark current page with `.active` and `aria-current="page"`. Customize divider via `--bs-breadcrumb-divider` CSS variable.

### Buttons

Interactive button elements. Base: `.btn.btn-{color}`. Outline: `.btn-outline-{color}`. Sizes: `.btn-lg`, `.btn-sm`. Full width: wrap in `.d-grid`. States: `disabled` attribute, `.active` class. Use `<button>` for actions, `<a>` for navigation.

### Button Group

Related buttons grouped together. Use `.btn-group` with `role="group"` and `aria-label`. Vertical: `.btn-group-vertical`. Toolbar: `.btn-toolbar` wrapper with `role="toolbar"`. Sizes: `.btn-group-lg`, `.btn-group-sm`.

### Cards

Flexible content containers. Structure: `.card` > `.card-body` > `.card-title`, `.card-text`. Optional: `.card-header`, `.card-footer`, `.card-img-top`/`.card-img-bottom`. Grid layout: use `.row.row-cols-{n}` with `.col` > `.card.h-100` for equal heights.

### Close Button

Generic dismiss button. Use `.btn-close` with `aria-label="Close"`. White variant: `.btn-close-white`. Dismiss targets via `data-bs-dismiss="alert|modal|offcanvas|toast"`.

### List Group

Series of content items as lists. Use `.list-group` > `.list-group-item`. Actionable: add `.list-group-item-action`. Borderless: `.list-group-flush`. Horizontal: `.list-group-horizontal`. Colors: `.list-group-item-{color}`.

### Navbar

Responsive navigation header. Use `.navbar.navbar-expand-{breakpoint}`. Contains `.navbar-brand`, `.navbar-toggler`, `.navbar-collapse`. Placement: `.fixed-top`, `.fixed-bottom`, `.sticky-top`. Theme: `data-bs-theme="dark"` (`.navbar-light` deprecated in v5.3).

### Navs and Tabs

Base navigation with visual styles. Styles: `.nav-tabs`, `.nav-pills`, `.nav-underline`. Layout: `.nav-fill` (equal width), `.nav-justified` (full width), `.flex-column` (vertical). For tabbed content, use `role="tablist"` with `role="tab"` buttons and `role="tabpanel"` panes.

### Pagination

Navigation for paginated content. Use `<nav aria-label="...">` > `.pagination` > `.page-item` > `.page-link`. Sizes: `.pagination-lg`, `.pagination-sm`. Alignment: `.justify-content-center`, `.justify-content-end`. Mark current: `.active` with `aria-current="page"`.

### Placeholders

Loading state indicators. Use `.placeholder` spans with column widths (`.col-6`). Animations: wrap in `.placeholder-glow` or `.placeholder-wave`. Sizes: `.placeholder-lg`, `.placeholder-sm`, `.placeholder-xs`. Add `aria-hidden="true"` to placeholder containers.

### Progress

Progress indicators for tasks. Use `.progress` wrapper with `.progress-bar` inside. Set width via `style="width: X%"`. Variants: `.progress-bar-striped`, `.progress-bar-animated`. Colors: `.bg-{color}`. Include ARIA attributes: `role="progressbar"`, `aria-valuenow`, `aria-valuemin`, `aria-valuemax`.

### Spinners

Loading indicators. Types: `.spinner-border` (spinning), `.spinner-grow` (pulsing). Sizes: `.spinner-border-sm`, `.spinner-grow-sm`. Colors: `.text-{color}`. Include `role="status"` and `.visually-hidden` loading text.

## Common Gotchas & Tips

### Components Requiring JavaScript Initialization

Tooltips and popovers will not work without explicit JavaScript initialization. Unlike modals, dropdowns, and carousels (which work via data attributes), these components must be initialized:

```javascript
// Initialize all tooltips
document.querySelectorAll('[data-bs-toggle="tooltip"]')
  .forEach(el => new bootstrap.Tooltip(el));

// Initialize all popovers
document.querySelectorAll('[data-bs-toggle="popover"]')
  .forEach(el => new bootstrap.Popover(el));
```

Toasts also require JavaScript to show—they are hidden by default and must be shown programmatically with `toast.show()`.

### Tooltip/Popover Positioning Issues

If tooltips or popovers appear in the wrong position, get clipped, or behave strangely in complex layouts (input groups, button groups, tables, modals), use `container: 'body'`:

```javascript
// Append to body to avoid rendering issues
new bootstrap.Tooltip(el, { container: 'body' });
new bootstrap.Popover(el, { container: 'body' });
```

For popovers inside modals, set `container` to the modal body so focus remains trapped:

```javascript
new bootstrap.Popover(el, { container: '.modal-body' });
```

### Modal Best Practices

**Semantic headings**: Bootstrap recommends using `<h1>` for modal titles semantically (the modal represents its own document context). Use font size utilities like `.fs-5` to control visual appearance while maintaining proper heading hierarchy.

**Autofocus workaround**: The HTML `autofocus` attribute has no effect in Bootstrap modals due to HTML5 semantics. To focus an input when a modal opens:

```javascript
myModal.addEventListener('shown.bs.modal', () => {
  document.getElementById('myInput').focus();
});
```

**Nested modals**: Bootstrap only supports one modal at a time. Nested modals are not supported and considered poor user experience. If multiple dialogs are needed, close the current modal before opening another.

**Dynamic content height**: After dynamically changing modal body content that affects height, call `modal.handleUpdate()` to readjust the modal's position.

### Cross-Component Patterns

**Modals with forms**: Place form validation feedback inside the modal body. On successful submission, call `modal.hide()` and optionally show a toast notification.

**Toast stacking**: Use `.toast-container` with positioning utilities (`.position-fixed.bottom-0.end-0.p-3`) for consistent toast placement. Multiple toasts stack automatically.

**Navbar with offcanvas**: For mobile navigation, combine `.navbar` with offcanvas for a sliding menu. Use `data-bs-toggle="offcanvas"` on the navbar toggler instead of collapse for a different UX pattern.

**Cards in grids**: Use `.row.row-cols-{n}` with `.col` > `.card.h-100` to create equal-height card grids that respond to breakpoints.

## Additional Resources

### Reference Files

- `references/components-reference.md` - Quick reference tables for all component classes
- `references/css-custom-properties.md` - CSS custom properties for runtime component theming
- `references/interactive-components.md` - Detailed documentation for JS-dependent components
- `references/static-components.md` - Detailed documentation for CSS/HTML components

### Example Files

- `examples/accordion-patterns.html` - Accordion and FAQ patterns
- `examples/alert-patterns.html` - Alert variants, dismissible alerts, live region patterns
- `examples/badge-button-patterns.html` - Badges, buttons, button groups, and close buttons
- `examples/breadcrumb-patterns.html` - Breadcrumb navigation with custom dividers and icons
- `examples/card-grid-patterns.html` - Responsive card grid layouts
- `examples/carousel-patterns.html` - Carousel implementation patterns
- `examples/collapse-patterns.html` - Collapse, horizontal collapse, and multi-target patterns
- `examples/dropdown-patterns.html` - Dropdown menus, split buttons, and form dropdowns
- `examples/list-group-patterns.html` - List groups, actionable items, and tab integration
- `examples/modal-patterns.html` - Modal dialog patterns
- `examples/navbar-patterns.html` - Navigation bar layouts
- `examples/offcanvas-patterns.html` - Offcanvas sidebar patterns
- `examples/pagination-patterns.html` - Pagination variants, alignment, and responsive patterns
- `examples/placeholder-patterns.html` - Loading skeleton patterns for cards, lists, and tables
- `examples/popovers-tooltips-patterns.html` - Tooltip and popover patterns (requires JS init)
- `examples/progress-spinner-patterns.html` - Progress bars and spinner loading indicators
- `examples/scrollspy-patterns.html` - Scrollspy with navbar, list group, and documentation patterns
- `examples/tabs-patterns.html` - Tab navigation patterns
- `examples/toasts-patterns.html` - Toast notification patterns (requires JS init)
