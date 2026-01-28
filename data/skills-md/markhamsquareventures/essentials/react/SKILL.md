---
name: react
description: How to work effectively with React, always use when developing frontend components
---

# React

## Instructions

This project uses React 19 with TypeScript and the React Compiler enabled via `babel-plugin-react-compiler`.

### Component Structure

- Pages live in `resources/js/pages/` and are rendered via Inertia
- Shared components live in `resources/js/components/`
- UI primitives (shadcn/ui) live in `resources/js/components/ui/`
- Custom hooks live in `resources/js/hooks/`

### Page Props from Controllers

Always receive page data as props from the Laravel controller via Inertia. Do NOT fetch data client-side or use `useEffect` to load page data.

<code-snippet name="Controller Passing Props" lang="php">
// In Laravel controller
public function edit(Project $project): Response
{
    return Inertia::render('projects/edit', [
        'project' => $project->load('client'),
        'clients' => Client::orderBy('name')->get(),
    ]);
}
</code-snippet>

<code-snippet name="Page Receiving Props" lang="tsx">
// In React page component
import { Project, Client } from '@/types';

interface EditProjectProps {
    project: Project;
    clients: Client[];
}

export default function EditProject({ project, clients }: EditProjectProps) {
    return (
        <Form action={update({ project: project.id }).url} method="patch">
            {/* Form fields using project and clients data */}
        </Form>
    );
}
</code-snippet>

This pattern ensures:
- **State consistency** - The server is the single source of truth; no client-side caching or stale data issues
- Data is loaded server-side before the page renders
- No loading states needed for initial page data
- SEO-friendly server-rendered content
- Type-safe props matching controller output

### TypeScript Conventions

- All component props should be typed explicitly
- Use interfaces for object shapes, defined in `resources/js/types/index.d.ts`
- Prefer `React.ComponentProps<"element">` for extending native element props
- Use path aliases: `@/components`, `@/hooks`, `@/lib`, `@/types`

<code-snippet name="Typed Component Example" lang="tsx">
import { cn } from '@/lib/utils';

interface CardProps {
    title: string;
    description?: string;
    className?: string;
    children: React.ReactNode;
}

export function Card({ title, description, className, children }: CardProps) {
    return (
        <div className={cn('rounded-lg border p-4', className)}>
            <h3 className="font-semibold">{title}</h3>
            {description && <p className="text-muted-foreground">{description}</p>}
            {children}
        </div>
    );
}
</code-snippet>

### React 19 + React Compiler

- The React Compiler automatically memoizes components and hooks
- Do NOT manually add `useMemo`, `useCallback`, or `React.memo` unless profiling shows a specific need
- Write straightforward code and let the compiler optimize

### State Management

- Use React's built-in `useState` and `useReducer` for local state
- Use Inertia's shared data for server-provided state (accessed via `usePage()`)
- For form state, use the Inertia `<Form>` component (see inertia skill)

<code-snippet name="Accessing Shared Data" lang="tsx">
import { usePage } from '@inertiajs/react';
import { SharedData } from '@/types';

export function UserGreeting() {
    const { auth } = usePage<SharedData>().props;

    return <span>Hello, {auth.user.name}</span>;
}
</code-snippet>

### Event Handlers

- Use inline arrow functions for simple handlers
- Extract to named functions only when logic is complex or reused

### Conditional Rendering

- Use early returns for guard clauses
- Prefer `&&` for simple conditionals, ternaries for if/else
- Use separate components for complex conditional logic

<code-snippet name="Conditional Rendering Patterns" lang="tsx">
// Early return for loading state
function DataDisplay({ data, isLoading }: Props) {
    if (isLoading) {
        return <Skeleton />;
    }

    return (
        <div>
            {data.items.length > 0 && <ItemList items={data.items} />}
            {data.error ? <ErrorMessage error={data.error} /> : <SuccessIndicator />}
        </div>
    );
}
</code-snippet>

### File Naming

- Components: PascalCase (`UserCard.tsx`)
- Hooks: camelCase with `use` prefix (`useClipboard.ts`)
- Utilities: camelCase (`formatDate.ts`)
- Pages: kebab-case matching the route (`edit.tsx`, `create.tsx`, `index.tsx`)
