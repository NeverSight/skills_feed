---
name: typo3-records-list-types
description: Configure and extend the Records List Types extension for TYPO3 v14. Grid, Compact, Teaser, and custom view modes for the backend Records module with thumbnails, drag-and-drop, dark mode, workspace indicators, and zero-PHP extensibility via TSconfig + Fluid templates. Use when working with backend record listing, creating custom view types, or configuring per-table display fields.
version: 1.1.0
typo3_compatibility: "14.0 - 14.x"
triggers:
  - records list types
  - grid view backend
  - compact view
  - teaser view
  - custom view type
  - backend record cards
  - drag and drop records
  - records module view
  - view mode tsconfig
---

# TYPO3 Records List Types

> **Compatibility:** TYPO3 v14.0+ / PHP 8.3+
> Extension key: `records_list_types` / Composer: `webconsulting/records-list-types`
> GitHub: https://github.com/dirnbauer/typo3-records-list-types

> **TYPO3 API First:** Always use TYPO3's built-in APIs, core features, and established conventions before creating custom implementations. Do not reinvent what TYPO3 already provides. Always verify that the APIs and methods you use exist and are not deprecated in your target TYPO3 version (v13 or v14) by checking the official TYPO3 documentation.

## 1. Overview

Transforms the TYPO3 backend **Records** module with multiple view modes:

| View | Description | Best for |
|------|-------------|----------|
| **List** | Standard TYPO3 table (unchanged) | Data-heavy tables, system records |
| **Grid** | Card layout with thumbnails, drag-and-drop | News, products, team members, media |
| **Compact** | Dense single-line rows, fixed columns | Address books, logs, settings, bulk data |
| **Teaser** | Minimal cards with title, date, excerpt | Blog posts, events, press releases |
| **Custom** | Your own views via TSconfig + Fluid | Timeline, kanban, catalog, gallery |

All views include: pagination, sorting, search, record actions, workspace indicators, dark mode, WCAG 2.1 accessibility.

### Features

- **Grid View** -- Card-based layout with thumbnails, drag-and-drop reordering, and field display
- **Compact View** -- Dense single-line rows with fixed columns and horizontal scrolling
- **Teaser View** -- News-style cards with title, date, and description excerpt
- **Custom Views** -- Register your own view types via PSR-14 events or TSconfig
- **Drag & Drop** -- Mouse and keyboard reordering with full WCAG 2.1 accessibility
- **Language Flags** -- Language flag icons displayed per record in grid cards
- **Workspace Support** -- Color-coded indicators for new, modified, moved, and deleted records
- **Dark Mode** -- Full compatibility with TYPO3's dark mode (light/dark themes)
- **Per-Table Config** -- Configure title, description, image, and display fields via TSconfig
- **User Preferences** -- View mode is persisted per backend user via AJAX
- **Sorting Controls** -- Manual drag ordering and field-based sorting with direction toggle
- **Pagination** -- Matches TYPO3 Core: multi-table mode shows limited records with "Expand table" button, single-table mode shows full pagination (record range, page input, first/prev/next/last)
- **Image Preview Hint** -- Subtle notice below thumbnails reminding editors that the image may not appear on the frontend for certain record types
- **Zero-PHP Extensibility** -- Add new view types with just TSconfig + Fluid template + CSS, no PHP classes needed
- **Search** -- Client-side search filtering across all view modes
- **Accessibility** -- WCAG 2.1 compliant keyboard navigation, ARIA labels, and screen reader support

## 2. Installation

```bash
composer require webconsulting/records-list-types
./vendor/bin/typo3 extension:activate records_list_types
```

After activation, view mode toggle buttons appear in the Records module header.

## 3. View Mode Configuration

### Set Default and Allowed Views

```tsconfig
mod.web_list.viewMode {
    default = grid                          # Default for new users
    allowed = list,grid,compact,teaser      # Available in toggle
}
```

### Grid Column Count

```tsconfig
mod.web_list.gridView.cols = 4    # 2-6 columns (default: 4)
```

### View Mode Resolution Order

1. **URL parameter** (`?displayMode=grid`) -- highest priority
2. **User preference** (stored via AJAX, persisted per session)
3. **TSconfig default** (`mod.web_list.viewMode.default`)
4. **Fallback**: `list`

## 4. Per-Table Field Configuration

Configure which fields appear on cards for each table:

```tsconfig
mod.web_list.gridView.table.<tableName> {
    titleField = title              # Card title (default: TCA ctrl.label)
    descriptionField = teaser       # Card body text
    imageField = fal_media          # FAL field for thumbnail
    preview = 1                     # Enable thumbnails (1/0)
}
```

### Common Tables

```tsconfig
# News
mod.web_list.gridView.table.tx_news_domain_model_news {
    titleField = title
    descriptionField = teaser
    imageField = fal_media
    preview = 1
}

# Pages
mod.web_list.gridView.table.pages {
    titleField = title
    descriptionField = abstract
    imageField = media
    preview = 1
}

# Content Elements
mod.web_list.gridView.table.tt_content {
    titleField = header
    descriptionField = bodytext
    imageField = image
    preview = 1
}

# Frontend Users
mod.web_list.gridView.table.fe_users {
    titleField = name
    descriptionField = email
    imageField = image
    preview = 1
}
```

## 5. View Modes Detail

### Grid View

- **Card structure**: Header (icon, title, drag handle, actions), optional thumbnail image (16:9), field values body, footer (UID, PID, language flag)
- **Thumbnails**: Automatically resolved from FAL image fields (configurable per table)
- **Field display**: Type-aware formatting -- booleans as badges, dates in monospace, relations with count indicators, links as clickable, text truncated with ellipsis
- **Two-column field layout**: Small fields display side-by-side; text/richtext fields span full width
- **Drag-and-drop**: Both mouse and keyboard (Space to grab, arrows to move, Space to drop, Escape to cancel)
- **Record actions**: Inline visibility toggle, edit, delete, plus dropdown for info, history, copy, cut
- **State indicators**: Hidden records get amber headers; workspace records show blue/purple/cyan/red headers
- **Language flags**: Each card shows the record's language flag icon in the bottom-right corner
- **Responsive grid**: Auto-fills columns from 320px minimum, scales from 1 column on mobile to multiple on wide screens

### Compact View

- **Fixed columns**: Icon, UID, and title pinned on the left; status toggle, edit, delete pinned on the right
- **Scrollable middle**: Additional fields scroll horizontally between fixed columns
- **Scroll shadows**: Visual indicators when content extends beyond the visible area
- **Sortable headers**: Click column headers to sort ascending/descending via TYPO3's native dropdown API
- **Zebra striping**: Alternating row colors for readability
- **Hidden record styling**: Muted background and dimmed title for hidden records

### Teaser View

- **Clean design**: Title, date with calendar icon, description excerpt (2-line clamp)
- **Status badges**: UID pill and hidden/visible indicator
- **Compact actions**: Visibility toggle, edit, delete buttons
- **Hidden state**: Accent bar on hidden records
- **CSS `light-dark()`**: Native theme switching support

## 6. Pagination

Matches TYPO3 Core List View behavior:

- **Multi-table mode**: Limited records per table with "Expand table" button
- **Single-table mode**: Full pagination (record range, page input, first/prev/next/last)

```tsconfig
# Global default items per page
mod.web_list.viewMode.itemsPerPage = 100

# Per-type override
mod.web_list.viewMode.types.grid.itemsPerPage = 100
mod.web_list.viewMode.types.compact.itemsPerPage = 300
mod.web_list.viewMode.types.teaser.itemsPerPage = 100

# Disable pagination
mod.web_list.viewMode.types.grid.itemsPerPage = 0
```

## 7. Sorting

Tables with TCA `sortby` support two modes:

- **Manual**: Drag-and-drop reordering (default)
- **Field**: Sort by column with ascending/descending toggle

A segmented toggle switches between modes. Drag-and-drop supports both mouse and keyboard (Space to grab, arrows to move, Space to drop, Escape to cancel).

## 8. Custom View Types (Quick Start)

Add a view in **3 steps** -- zero PHP required.

### Step 1: Register via TSconfig

```tsconfig
mod.web_list.viewMode {
    allowed = list,grid,compact,teaser,timeline

    types.timeline {
        label = Timeline
        icon = actions-calendar
        template = TimelineView
        templateRootPath = EXT:my_sitepackage/Resources/Private/Backend/Templates/
        css = EXT:my_sitepackage/Resources/Public/Css/timeline.css
        displayColumns = label,datetime,teaser
        columnsFromTCA = 0
    }
}
```

### Step 2: Create Fluid Template

Copy `GenericView.html` from the extension as a starting point. Key variables: `tableData`, `tableData.records`, `record.title`, `record.displayValues`.

### Step 3: Add CSS (optional)

Use TYPO3 CSS variables for automatic dark mode:

```css
.timeline-item {
    background: var(--typo3-component-bg, #fff);
    border: 1px solid var(--typo3-component-border-color, #d4d4d8);
}
```

> **Full documentation**: See [SKILL-CUSTOM-VIEWS.md](SKILL-CUSTOM-VIEWS.md) for complete reference including template variables, real-world examples, asset loading, PSR-14 registration, and page-scoped views.

### Reuse Built-in Templates

No new template needed -- reuse existing ones with custom columns:

```tsconfig
# Address book using CompactView with fixed columns
mod.web_list.viewMode.types.addressbook {
    label = Address Book
    icon = actions-user
    template = CompactView
    displayColumns = name,email,phone,company,city
    columnsFromTCA = 0
    itemsPerPage = 500
}
```

### Page-Scoped Views

Restrict views to specific pages:

```tsconfig
[page["uid"] == 42]
    mod.web_list.viewMode {
        allowed = list,timeline
        default = timeline
    }
[end]
```

## 9. Column Display

Two modes control which fields appear:

| Mode | Setting | Behavior |
|------|---------|----------|
| **Editor-controlled** | `columnsFromTCA = 1` | Respects editor's "Show columns" selection |
| **Fixed layout** | `columnsFromTCA = 0` | Uses `displayColumns` list exactly |

### `columnsFromTCA = 1` Resolution Order

1. **Editor's "Show columns" selection** (stored per-user per-table)
2. **TSconfig `showFields`** (`mod.web_list.table.<table>.showFields`)
3. **TCA `searchFields`** (the table's most relevant fields)
4. **Label field only** (final fallback)

### Special Column Names

| Name | Resolves to |
|------|-------------|
| `label` | TCA `ctrl.label` field (record title) |
| `datetime` | First date field (`datetime`, `date`, `starttime`, `crdate`) |
| `teaser` | First description field (`teaser`, `abstract`, `description`, `bodytext`) |

## 10. TSconfig Reference

### View Type Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `label` | string | *required* | Display name (supports `LLL:`) |
| `icon` | string | *required* | TYPO3 icon identifier |
| `description` | string | | Tooltip |
| `template` | string | `<Id>View` | Fluid template name |
| `partial` | string | `Card` | Default partial |
| `templateRootPath` | string | | Custom template path |
| `partialRootPath` | string | | Custom partial path |
| `layoutRootPath` | string | | Custom layout path |
| `css` | string | | CSS file (`EXT:` syntax) |
| `js` | string | | JS module (`@vendor/module.js`) |
| `columnsFromTCA` | bool | `1` | Use editor column selection |
| `displayColumns` | string | | Comma-separated field list |
| `itemsPerPage` | int | `100` | Records per page (`0` = no pagination) |

## 11. Workspace Support

Records display color-coded indicators in workspaces:

| State | Color | Visual |
|-------|-------|--------|
| New | Blue | Blue header + left border |
| Modified | Purple | Purple header + left border |
| Moved | Cyan | Cyan header + left border |
| Deleted | Red | Red header + strikethrough title |

Workspace overlays applied via `BackendUtility::workspaceOL()`.

> **Note:** Workspace support is experimental. Visual indicators work, but drag-and-drop within workspaces has limited testing.

## 12. PSR-14 Events

| Event | Purpose |
|-------|---------|
| `RegisterViewModesEvent` | Register, remove, or modify view types |
| `GridViewButtonBarListener` | Injects toggle buttons into DocHeader |
| `GridViewQueryListener` | Modifies database queries |
| `GridViewRecordActionsListener` | Collects record action buttons |

### Register a View Type via Event

```php
use TYPO3\CMS\Core\Attribute\AsEventListener;
use Webconsulting\RecordsListTypes\Event\RegisterViewModesEvent;

#[AsEventListener]
final class RegisterKanbanViewListener
{
    public function __invoke(RegisterViewModesEvent $event): void
    {
        $event->addViewMode('kanban', [
            'label' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang.xlf:viewMode.kanban',
            'icon' => 'actions-view-table-columns',
            'description' => 'Kanban board view',
        ]);
    }
}
```

### Event API

```php
$event->addViewMode(string $id, array $config): void
$event->removeViewMode(string $id): void
$event->hasViewMode(string $id): bool
$event->modifyViewMode(string $id, array $config): void
$event->getViewModes(): array
```

## 13. Extending

### Override Templates via TypoScript

```typoscript
module.tx_recordsgridview {
    view {
        templateRootPaths.100 = EXT:your_extension/Resources/Private/Templates/RecordsListTypes/
        partialRootPaths.100 = EXT:your_extension/Resources/Private/Partials/RecordsListTypes/
        layoutRootPaths.100 = EXT:your_extension/Resources/Private/Layouts/RecordsListTypes/
    }
}
```

### Custom Record Actions

Listen to `ModifyRecordListRecordActionsEvent` (TYPO3 Core event):

```php
#[AsEventListener]
final class CustomRecordActionListener
{
    public function __invoke(ModifyRecordListRecordActionsEvent $event): void
    {
        if ($event->getTable() === 'tx_yourext_domain_model_item') {
            $event->setAction(
                action: '<a href="..." title="My Action"><span class="icon">...</span></a>',
                actionName: 'myCustomAction',
                group: 'primary',
                after: 'edit'
            );
        }
    }
}
```

### Custom Thumbnail Logic

```php
class CustomThumbnailService extends ThumbnailService
{
    public function getThumbnailForRecord(string $table, array $record, string $imageField): ?FileInterface
    {
        if ($table === 'tx_yourext_domain_model_item') {
            return $this->getFromExternalSource($record);
        }
        return parent::getThumbnailForRecord($table, $record, $imageField);
    }
}
```

Register override in `Services.yaml`:

```yaml
services:
  Webconsulting\RecordsListTypes\Service\ThumbnailService:
    class: YourVendor\YourExtension\Service\CustomThumbnailService
```

### JavaScript Hooks

```javascript
document.addEventListener('recordsGridview:viewModeChanged', (event) => {
    console.log('View mode changed to:', event.detail.mode);
});
```

## 14. Architecture

### Services

| Service | Purpose |
|---------|---------|
| `RecordGridDataProvider` | Fetches records with thumbnails, icons, workspace state |
| `GridConfigurationService` | Parses TSconfig for per-table settings |
| `ThumbnailService` | Resolves FAL references, generates thumbnail URLs |
| `ViewModeResolver` | Determines active view from request/preference/TSconfig |
| `ViewTypeRegistry` | Registry for built-in + custom view types |
| `MiddlewareDiagnosticService` | Detects middleware interference with view rendering |

### ViewHelpers

| ViewHelper | Purpose |
|------------|---------|
| `RecordActionsViewHelper` | Renders cached record actions (`<gridview:recordActions>`) |

### CSS Architecture

```
base.css            ← Always loaded (heading, pagination, sorting)
├── grid-view.css   ← Grid-only: cards, drag-drop, field types
├── compact-view.css← Compact-only: table, sticky columns
├── teaser-view.css ← Teaser-only: teaser cards, badges
└── view-mode-toggle.css ← DocHeader toggle buttons
```

Custom view types automatically receive `base.css`.

### JavaScript Modules

| Module | Purpose |
|--------|---------|
| `GridViewActions.js` | Drag-drop, record actions, sorting, search, pagination, ARIA |
| `view-switcher.js` | View mode switching with AJAX persistence |

### AJAX Routes

| Route | Purpose |
|-------|---------|
| `records_list_types_set_view_mode` | Persist user's view mode preference |
| `records_list_types_get_view_mode` | Retrieve current view mode preference |

## 15. Common Recipes

### Grid as Default for Media Folders

```tsconfig
[page["doktype"] == 254]
    mod.web_list.viewMode.default = grid
    mod.web_list.viewMode.allowed = list,grid
    mod.web_list.gridView.cols = 6
[end]
```

### Disable Extension for Specific Pages

```tsconfig
[page["uid"] == 123 || page["pid"] == 123]
    mod.web_list.viewMode.allowed = list
[end]
```

### Force View for User Group

```tsconfig
# User TSconfig
options.layout.records.forceView = grid
```

### Photo Gallery (48 items, Grid template)

```tsconfig
mod.web_list.viewMode.types.gallery {
    label = Photo Gallery
    icon = actions-image
    template = GridView
    columnsFromTCA = 0
    displayColumns = label
    itemsPerPage = 48
}

mod.web_list.gridView.table.sys_file_metadata {
    titleField = title
    imageField = file
    preview = 1
}
```

### Companion Extension

Install [typo3-records-list-examples](https://github.com/dirnbauer/typo3-records-list-examples) for 6 ready-to-use view types: Timeline, Catalog, Address Book, Event List, Gallery, Dashboard.

## 16. File Structure

```
records_list_types/
├── Classes/
│   ├── Constants.php
│   ├── Controller/
│   │   ├── Ajax/ViewModeController.php        # AJAX preference persistence
│   │   └── RecordListController.php           # Main controller (XClass)
│   ├── Event/
│   │   └── RegisterViewModesEvent.php         # PSR-14: custom view registration
│   ├── EventListener/
│   │   ├── GridViewButtonBarListener.php      # Injects toggle buttons
│   │   ├── GridViewQueryListener.php          # Query modification bridge
│   │   └── GridViewRecordActionsListener.php  # Record action collection
│   ├── Pagination/
│   │   └── DatabasePaginator.php              # Paginator for pre-fetched records
│   ├── Service/
│   │   ├── GridConfigurationService.php       # TSconfig parsing
│   │   ├── MiddlewareDiagnosticService.php    # Middleware diagnostics
│   │   ├── RecordGridDataProvider.php         # Record fetching & enrichment
│   │   ├── ThumbnailService.php               # FAL image processing
│   │   ├── ViewModeResolver.php               # View mode determination
│   │   └── ViewTypeRegistry.php               # View type management
│   └── ViewHelpers/
│       └── RecordActionsViewHelper.php        # Record actions rendering
├── Configuration/
│   ├── Backend/AjaxRoutes.php
│   ├── Icons.php
│   ├── JavaScriptModules.php
│   ├── page.tsconfig
│   └── Services.yaml
├── Documentation/
├── Resources/
│   ├── Private/
│   │   ├── Language/ (en, de)
│   │   ├── Layouts/
│   │   ├── Partials/ (Card, CompactRow, Pagination, RecordActions, SortingDropdown, TeaserCard, ViewSwitcher)
│   │   └── Templates/ (CompactView, GenericView, GridView, TeaserView)
│   └── Public/
│       ├── Css/ (base, grid-view, compact-view, teaser-view, view-mode-toggle)
│       ├── Icons/
│       └── JavaScript/ (GridViewActions, view-switcher)
├── Tests/ (Unit, Functional, Architecture)
├── composer.json
├── ext_emconf.php
└── ext_localconf.php
```

## 17. Accessibility

- **Keyboard drag-and-drop**: Space/Enter to grab, arrows to move, Space/Enter to drop, Escape to cancel
- **ARIA live regions**: Announce drag state and position ("Position 3 of 12")
- **Semantic markup**: `role="listbox"` on grids, `role="option"` on cards
- **Focus management**: Visible focus indicators, proper tab order

## 18. Dark Mode

All views support TYPO3 dark mode via CSS custom properties:
- `[data-color-scheme="dark"]` attribute support
- `prefers-color-scheme: dark` system preference
- Design tokens for all colors, shadows, and borders

## 19. Security

- **SQL Injection Prevention**: All queries use TYPO3's QueryBuilder with parameterized named parameters
- **CSRF Protection**: AJAX endpoints use TYPO3's built-in token handling
- **Access Control**: Full integration with TYPO3's backend user permissions and workspace restrictions
- **Input Validation**: View mode, table names, UIDs, and sort parameters validated and sanitized
- **XSS Prevention**: Fluid templates with proper escaping; no raw HTML output of user data

## 20. Known Limitations

- **Workspace support is experimental.** Visual indicators work, but drag-and-drop within workspaces has limited testing.
- **Drag-and-drop accessibility**: Keyboard-based drag-and-drop is implemented with ARIA, but screen reader testing (NVDA, JAWS, VoiceOver) has been limited. Standard List View is a more tested fallback.
