---
name: filter-sphere
description: Integrate Filter Sphere into a project - schema-driven filtering for Zod-typed data. Use when building filtering UIs, data tables with filters, or adding sort/filter logic to any TypeScript application.
---

# Filter Sphere - Schema-driven Filtering

Build advanced filtering interfaces powered by Zod schemas.

## Quick Start

```bash
# React filter UI
pnpm add @fn-sphere/filter zod
```

## Core Concepts

### Basic Setup

```tsx
import {
  FilterSphereProvider,
  FilterBuilder,
  useFilterSphere,
} from "@fn-sphere/filter";
import { z } from "zod";

// 1. Define your data schema with Zod
const schema = z.object({
  name: z.string().describe("Name"),
  age: z.number().describe("Age"),
});

export function FilterBuilder() {
  // 2. use the `useFilterSphere` hook to get the context and predicate
  const { filterRule, predicate, context } = useFilterSphere({
    schema,
    onRuleChange: ({ filterRule }) => {
      console.log("Filter rule changed:", filterRule);
    },
  });

  const data = [
    /* ... */
  ];

  // 4. use the `predicate` to filter the data
  const filteredData = data.filter(predicate);

  return (
    // 3. display the `FilterBuilder` inside the `FilterSphereProvider`
    <FilterSphereProvider context={context}>
      <FilterBuilder />
    </FilterSphereProvider>
  );
}
```

## Project Structure (Recommended)

```
filter-sphere/
  index.tsx      # Main component wiring everything together
  schema.ts      # Zod schema, default rules, custom functions
  theme.tsx      # Theme via createFilterTheme
  locale.ts      # (Optional) i18n with getLocaleText
```

## Core References

| Topic                  | Reference                                                                         |
| ---------------------- | --------------------------------------------------------------------------------- |
| Introduction           | [Introduction](https://www.waterwater.moe/fn-sphere/guides/introduction/)         |
| Getting Started        | [Getting Started](https://www.waterwater.moe/fn-sphere/guides/getting-started/)   |
| Best Practices         | [Best Practices](https://www.waterwater.moe/fn-sphere/guides/best-practices/)     |
| Work with AI           | [Work with AI](https://www.waterwater.moe/fn-sphere/guides/work-with-ai/)         |
| Customizing Filters    | [Customizing Filters](https://www.waterwater.moe/fn-sphere/customization/filter/) |
| Customizing Theme      | [Customizing Theme](https://www.waterwater.moe/fn-sphere/customization/theme/)    |
| Customizing Data Input | [Data Input](https://www.waterwater.moe/fn-sphere/customization/data-input/)      |
| Persistence            | [Persistence](https://www.waterwater.moe/fn-sphere/customization/persistence/)    |
| Preset Filters         | [Preset Filters](https://www.waterwater.moe/fn-sphere/reference/presets/)         |
| Example                | [Example](https://www.waterwater.moe/fn-sphere/reference/example/)                |

## Resources

- Repository: https://github.com/lawvs/fn-sphere
- Documentation: https://www.waterwater.moe/fn-sphere/
