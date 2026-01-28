---
name: woltz-react-rich-domain
description: React hooks and components for @woltz/rich-domain. Use when building frontend UIs with DataTable, Kanban, Timeline, or Criteria-based filtering.
---

# @woltz/react-rich-domain

React integration for @woltz/rich-domain with hooks, components, and React Query integration.

## Installation

```bash
npm install @woltz/react-rich-domain @tanstack/react-query
```

## Quick Start

### 1. Setup QueryClient

```typescript
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <YourApp />
    </QueryClientProvider>
  );
}
```

### 2. Create a Data Table

```typescript
import { useCriteriaTable, DataTableCriteria } from "@woltz/react-rich-domain";
import { ColumnDef } from "@tanstack/react-table";

interface User {
  id: string;
  name: string;
  email: string;
  status: "active" | "inactive";
}

const columns: ColumnDef<User>[] = [
  { accessorKey: "name", header: "Name" },
  { accessorKey: "email", header: "Email" },
  { accessorKey: "status", header: "Status" },
];

export function UserTable() {
  const { table, filterProps, searchProps } = useCriteriaTable({
    columns,
    queryKey: ["users"],
    queryFn: async (criteria) => {
      const res = await fetch("/api/users?" + criteria.toQueryString());
      return res.json();
    },
    filterFields: [
      {
        field: "status",
        type: "string",
        fieldLabel: "Status",
        options: [
          { label: "Active", value: "active" },
          { label: "Inactive", value: "inactive" },
        ],
      },
    ],
  });

  return (
    <DataTableCriteria
      table={table}
      filterProps={filterProps}
      {...searchProps}
      showColumnToggle
    />
  );
}
```

### 3. Create a Kanban Board

```typescript
import { useCriteriaKanban, DataKanbanCriteria } from "@woltz/react-rich-domain";

interface Task {
  id: string;
  title: string;
  status: "todo" | "doing" | "done";
}

const columns = [
  { id: "todo", title: "To Do", criteria: (c) => c.where("status", "equals", "todo") },
  { id: "doing", title: "In Progress", criteria: (c) => c.where("status", "equals", "doing") },
  { id: "done", title: "Done", criteria: (c) => c.where("status", "equals", "done") },
];

export function TaskBoard() {
  const kanban = useCriteriaKanban<Task>("tasks", fetchTasks, {
    columns,
    getItemId: (task) => task.id,
    groupField: "status",
    onCardMove: async ({ cardId, toColumn }) => {
      await updateTask(cardId, { status: toColumn.id });
    },
  });

  return (
    <DataKanbanCriteria
      kanban={kanban}
      renderCard={(task) => <div>{task.title}</div>}
      showItemCount
    />
  );
}
```

## Available Hooks

| Hook                       | Purpose                                   |
| -------------------------- | ----------------------------------------- |
| `useCriteria`              | Manage filter, sort, pagination state     |
| `useCriteriaQuery`         | Criteria + React Query for paginated data |
| `useCriteriaInfiniteQuery` | Infinite scroll with Criteria             |
| `useCriteriaTable`         | TanStack Table + Criteria integration     |
| `useCriteriaKanban`        | Kanban board with drag-and-drop           |
| `useCriteriaTimeline`      | Timeline view with date grouping          |

## Available Components

| Component              | Purpose                                  |
| ---------------------- | ---------------------------------------- |
| `DataTableCriteria`    | Full-featured data table with filtering  |
| `DataKanbanCriteria`   | Kanban board with drag-and-drop          |
| `DataTimelineCriteria` | Timeline view with grouped items         |
| `DataViewToolbar`      | Search, filter, export toolbar           |
| `Filter`               | Standalone filter dropdown UI            |
| `Sorting`              | Sorting UI with drag-and-drop reordering |

## References

For detailed documentation:

- [Hooks](./references/hooks.md) - useCriteria, useCriteriaQuery, useCriteriaTable, useCriteriaKanban, useCriteriaTimeline
- [Components](./references/components.md) - DataTableCriteria, DataKanbanCriteria, DataTimelineCriteria
- [Filter Component](./references/filter-component.md) - Standalone filter UI with operators by type
- [Sorting Component](./references/sorting-component.md) - Sorting UI with drag-and-drop reordering
- [Filtering](./references/filtering.md) - Filter fields, operators, and programmatic management
- [State Persistence](./references/state-persistence.md) - URL sync and localStorage

**Load references based on context - don't read all at once.**
