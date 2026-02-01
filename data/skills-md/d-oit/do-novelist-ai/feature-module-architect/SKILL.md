---
name: feature-module-architect
description:
  Scaffolds feature modules following feature-based architecture with colocation
  principle and 500 LOC file limit. Use when creating new features or
  refactoring large files into modular structure.
---

# Feature Module Architect

## Quick Start

This skill scaffolds feature modules following project architecture:

1. **Feature structure**: Standard directory layout with components, hooks,
   services, types, utils
2. **File size limit**: 500 LOC maximum per file (hard limit)
3. **Colocation**: Keep related code together within feature directory
4. **Public API**: Export only what other features need via `index.ts`

### When to Use

- Creating new feature modules
- Refactoring files exceeding 500 LOC
- Organizing scattered feature code
- Need feature architecture guidance

## Standard Feature Structure

```
src/features/{feature-name}/
├── components/           # React components for this feature
│   ├── FeatureComponent.tsx
│   ├── FeatureComponent.test.tsx
│   └── index.ts
├── hooks/               # Custom React hooks
│   ├── useFeatureData.ts
│   ├── useFeatureData.test.ts
│   └── index.ts
├── services/            # Business logic and API calls
│   ├── featureService.ts
│   ├── featureService.test.ts
│   └── index.ts
├── types/               # TypeScript interfaces and types
│   ├── feature.types.ts
│   └── index.ts
├── utils/               # Pure utility functions
│   ├── featureUtils.ts
│   ├── featureUtils.test.ts
│   └── index.ts
└── index.ts             # Public API (exports for other features)
```

## Existing Feature Examples

**AI Generation** (`src/features/ai-generation/`):

- Components: GenerationForm, GenerationHistory
- Hooks: useGeneration, useAIProvider
- Services: generationService, aiGatewayClient
- Types: GenerationRequest, GenerationResponse

**Project Management** (`src/features/project-management/`):

- Components: ProjectCard, ProjectList, ProjectForm
- Hooks: useProjects, useProjectMutations
- Services: projectService
- Types: Project, ProjectMetadata

**World Building** (`src/features/world-building/`):

- Components: WorldMap, LocationEditor
- Hooks: useWorldState
- Services: worldService
- Types: WorldElement, Location

## File Size Enforcement

**Hard Limit**: 500 LOC per file (from AGENTS.md)

Check file sizes:

```bash
# Count lines in all TypeScript files
wc -l src/features/**/*.ts src/features/**/*.tsx

# Find files exceeding 500 LOC
find src/features -name "*.ts" -o -name "*.tsx" | xargs wc -l | awk '$1 > 500'
```

### Refactoring Strategy

When a file exceeds 500 LOC, split by responsibility:

**Before** (600 LOC component):

```typescript
// ProjectDashboard.tsx (600 LOC) ❌
export const ProjectDashboard: React.FC = () => {
  // 100 LOC of state/hooks
  // 200 LOC of handlers
  // 300 LOC of JSX
};
```

**After** (split into 3 files, each <200 LOC):

```typescript
// useProjectDashboard.ts (100 LOC)
export function useProjectDashboard() {
  // State and effects
}

// projectDashboardHandlers.ts (100 LOC)
export function createHandlers(projects: Project[]) {
  // Event handlers
}

// ProjectDashboard.tsx (150 LOC)
export const ProjectDashboard: React.FC = () => {
  const state = useProjectDashboard();
  const handlers = createHandlers(state.projects);
  return <div>{/* JSX */}</div>;
};
```

## Colocation Principle

Keep related code together:

✅ **Good** - Feature-specific code within feature:

```
src/features/ai-generation/
├── components/GenerationForm.tsx
├── hooks/useGeneration.ts          # Only used by GenerationForm
└── types/generation.types.ts        # Only used by this feature
```

❌ **Bad** - Scattered across global directories:

```
src/
├── components/GenerationForm.tsx
├── hooks/useGeneration.ts           # Generic hooks directory
└── types/generation.types.ts        # Generic types directory
```

## Public API Pattern

Each feature exports a public API via `index.ts`:

```typescript
// src/features/ai-generation/index.ts
export { GenerationForm } from './components/GenerationForm';
export { useGeneration } from './hooks/useGeneration';
export type {
  GenerationRequest,
  GenerationResponse,
} from './types/generation.types';

// Keep internal utilities private (don't export)
```

**Usage by other features**:

```typescript
// ✅ Import from feature public API
import { GenerationForm, useGeneration } from '@/features/ai-generation';

// ❌ Import from internal paths (breaks encapsulation)
import { GenerationForm } from '@/features/ai-generation/components/GenerationForm';
```

## Component Organization

### Small Components (<100 LOC)

Keep component and styles together:

```typescript
// Button.tsx (80 LOC)
export const Button: React.FC<ButtonProps> = ({ children, ...props }) => {
  return (
    <button
      className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
      {...props}
    >
      {children}
    </button>
  );
};
```

### Large Components (>100 LOC)

Extract hooks and handlers:

```typescript
// useProjectForm.ts
export function useProjectForm(initialValues: Project) {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState({});

  const handleChange = (field: string, value: any) => {
    setValues(prev => ({ ...prev, [field]: value }));
  };

  return { values, errors, handleChange };
}

// ProjectForm.tsx (<150 LOC)
export const ProjectForm: React.FC<ProjectFormProps> = ({ initialValues }) => {
  const { values, errors, handleChange } = useProjectForm(initialValues);

  return (
    <form>
      {/* JSX using values, errors, handleChange */}
    </form>
  );
};
```

## Scaffolding Checklist

When creating a new feature:

- [ ] Create feature directory: `src/features/{feature-name}/`
- [ ] Add `components/` with index.ts
- [ ] Add `hooks/` with index.ts (if needed)
- [ ] Add `services/` with index.ts
- [ ] Add `types/` with index.ts
- [ ] Add `utils/` with index.ts (if needed)
- [ ] Create root `index.ts` with public API exports
- [ ] Add test files next to implementation files
- [ ] Verify no file exceeds 500 LOC
- [ ] Update feature integration points

## Common Patterns

### Service Pattern

```typescript
// src/features/projects/services/projectService.ts
import { db } from '@/lib/database';
import type { Project } from '../types/project.types';

export const projectService = {
  async getAll(): Promise<Project[]> {
    return db.select().from('projects');
  },

  async getById(id: string): Promise<Project | null> {
    const result = await db.select().from('projects').where('id', id);
    return result[0] ?? null;
  },

  async create(data: Omit<Project, 'id'>): Promise<Project> {
    const id = crypto.randomUUID();
    await db.insert({ id, ...data }).into('projects');
    return { id, ...data };
  },
};
```

### Hook Pattern

```typescript
// src/features/projects/hooks/useProjects.ts
import { useQuery } from '@tanstack/react-query';
import { projectService } from '../services/projectService';

export function useProjects() {
  return useQuery({
    queryKey: ['projects'],
    queryFn: () => projectService.getAll(),
  });
}
```

### Type Pattern

```typescript
// src/features/projects/types/project.types.ts
export interface Project {
  id: string;
  title: string;
  description?: string;
  genre: ProjectGenre;
  createdAt: number;
  updatedAt: number;
}

export type ProjectGenre = 'fantasy' | 'scifi' | 'mystery' | 'romance';

export interface ProjectMetadata {
  wordCount: number;
  chapterCount: number;
}
```

## Success Criteria

- All files under 500 LOC
- Feature code colocated within feature directory
- Public API clearly defined in root `index.ts`
- Test files next to implementation files
- Consistent directory structure across features
- No cross-feature internal imports

## References

- AGENTS.md - Colocation principle and file size limits
- Existing features in `src/features/` - Reference implementations
