---
name: tanstack-table
description: |
  TanStack Table best practices for building headless, type-safe data tables in React with sorting, filtering, pagination, row selection, and column management.
  Use when building data grids, implementing client-side or server-side table features, defining column structures,
  managing table state, or optimizing table rendering performance.
metadata:
  tags: tanstack-table, react-table, data-grid, sorting, filtering, pagination, row-selection, headless-ui, typescript
---

# TanStack Table

**Version**: @tanstack/react-table@latest
**Requires**: React 16.8+, TypeScript recommended

## Quick Setup

```bash
npm install @tanstack/react-table
```

```tsx
import {
  useReactTable,
  getCoreRowModel,
  flexRender,
  createColumnHelper,
} from '@tanstack/react-table'

type User = {
  name: string
  age: number
  status: string
}

const columnHelper = createColumnHelper<User>()

const columns = [
  columnHelper.accessor('name', { header: 'Name' }),
  columnHelper.accessor('age', { header: 'Age' }),
  columnHelper.accessor('status', { header: 'Status' }),
  columnHelper.display({
    id: 'actions',
    cell: (props) => <button onClick={() => edit(props.row.original)}>Edit</button>,
  }),
]

function App() {
  const [data] = useState<User[]>([]) // must be stable reference

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  })

  return (
    <table>
      <thead>
        {table.getHeaderGroups().map((headerGroup) => (
          <tr key={headerGroup.id}>
            {headerGroup.headers.map((header) => (
              <th key={header.id}>
                {flexRender(header.column.columnDef.header, header.getContext())}
              </th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody>
        {table.getRowModel().rows.map((row) => (
          <tr key={row.id}>
            {row.getVisibleCells().map((cell) => (
              <td key={cell.id}>
                {flexRender(cell.column.columnDef.cell, cell.getContext())}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  )
}
```

### Row Models (Import Only What You Need)

TanStack Table is modular. Only import the row models you actually use:

```tsx
import {
  getCoreRowModel,      // required
  getSortedRowModel,    // client-side sorting
  getFilteredRowModel,  // client-side filtering
  getPaginationRowModel,// client-side pagination
  getExpandedRowModel,  // expanding/sub-rows
  getGroupedRowModel,   // grouping + aggregation
  getFacetedRowModel,   // faceted values
  getFacetedUniqueValues,
  getFacetedMinMaxValues,
} from '@tanstack/react-table'
```

Pipeline order: Core -> Filtered -> Grouped -> Sorted -> Expanded -> Paginated -> Rendered

## Rule Categories

| Priority | Category | Rule File | Impact |
|----------|----------|-----------|--------|
| CRITICAL | Table Setup | `rules/table-setup.md` | Correct table creation, stable data references |
| CRITICAL | Column Definitions | `rules/col-column-defs.md` | Data model, rendering, type safety |
| CRITICAL | Row Models | `rules/rm-row-models.md` | Modular imports, pipeline order |
| HIGH | Sorting | `rules/sort-sorting.md` | Client/server sorting, custom sort functions |
| HIGH | Column Filtering | `rules/filt-column-filtering.md` | Per-column filters, custom filter functions |
| HIGH | Global Filtering | `rules/filt-global-filtering.md` | Table-wide search, global filter function |
| HIGH | Pagination | `rules/pag-pagination.md` | Client/server pagination, page state |
| MEDIUM | Row Selection | `rules/sel-row-selection.md` | Checkbox/radio selection, selection state |
| MEDIUM | Column Visibility | `rules/vis-column-visibility.md` | Show/hide columns dynamically |
| MEDIUM | Column Sizing | `rules/size-column-sizing.md` | Widths, resizing, performance |
| LOW | Expanding | `rules/exp-expanding.md` | Sub-rows, detail panels, hierarchical data |

## Critical Rules

### Always Do

- **Stable `data` reference** — use `useState`, `useMemo`, or define outside component to prevent infinite re-renders
- **Use `createColumnHelper<TData>()`** — for maximum type safety in column definitions
- **Import only needed row models** — don't import `getSortedRowModel` if you don't sort client-side
- **Use `flexRender`** — for rendering header/cell/footer templates from column defs
- **Use `getVisibleCells()`** — not `getAllCells()`, to respect column visibility
- **Use `getRowModel()`** — the final row model that applies all features (filtering, sorting, pagination)
- **Control state with `state` + `on*Change`** — for sorting, filtering, pagination, selection, etc.

### Never Do

- **Define `data` inline** — `useReactTable({ data: fetchData() })` causes infinite re-renders
- **Define `columns` inside render** — columns array must be stable (define outside component or `useMemo`)
- **Use `getAllCells()` for rendering** — ignores column visibility; use `getVisibleCells()`
- **Mix `initialState` and `state` for the same feature** — `state` overrides `initialState`
- **Use client-side row models with `manual*` options** — if `manualSorting: true`, don't import `getSortedRowModel`
- **Forget `getRowId`** — without it, row IDs default to index, breaking selection state across re-fetches

## Key Patterns

```tsx
// Controlled sorting state
const [sorting, setSorting] = useState<SortingState>([])
const table = useReactTable({
  data, columns,
  getCoreRowModel: getCoreRowModel(),
  getSortedRowModel: getSortedRowModel(),
  state: { sorting },
  onSortingChange: setSorting,
})
// Header click handler
<th onClick={header.column.getToggleSortingHandler()}>
  {flexRender(header.column.columnDef.header, header.getContext())}
  {{ asc: ' 🔼', desc: ' 🔽' }[header.column.getIsSorted() as string] ?? ''}
</th>

// Server-side pagination
const [pagination, setPagination] = useState({ pageIndex: 0, pageSize: 10 })
const table = useReactTable({
  data, columns,
  getCoreRowModel: getCoreRowModel(),
  manualPagination: true,
  rowCount: serverData.totalRows,
  state: { pagination },
  onPaginationChange: setPagination,
})

// Row selection with checkbox column
columnHelper.display({
  id: 'select',
  header: ({ table }) => (
    <input type="checkbox" checked={table.getIsAllRowsSelected()}
      onChange={table.getToggleAllRowsSelectedHandler()} />
  ),
  cell: ({ row }) => (
    <input type="checkbox" checked={row.getIsSelected()}
      disabled={!row.getCanSelect()}
      onChange={row.getToggleSelectedHandler()} />
  ),
})

// Column filtering
const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([])
const table = useReactTable({
  data, columns,
  getCoreRowModel: getCoreRowModel(),
  getFilteredRowModel: getFilteredRowModel(),
  state: { columnFilters },
  onColumnFiltersChange: setColumnFilters,
})
// Filter input
<input value={column.getFilterValue() ?? ''} onChange={e => column.setFilterValue(e.target.value)} />

// Stable row IDs for selection across re-fetches
const table = useReactTable({
  data, columns,
  getRowId: (row) => row.uuid,
  getCoreRowModel: getCoreRowModel(),
})
```
