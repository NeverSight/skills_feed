---
name: vueuse-axios-conventions
description: Documentation of the project's standardized approach to using `@vueuse/integrations/useAxios`. Focuses on minimizing boilerplate, leveraging global error handling, utilizing built-in state management, and enforcing consistent naming conventions.
---

# VueUse Axios Conventions (EMID Project)

This skill documents the standardized patterns for data fetching and state management using `useAxios` in the EMID frontend.

## 1. Centralized Error Handling

**NEVER** use manual `try-catch` blocks or `ElMessage.error` for API errors in components. The `axiosInstance` in `src/utils/http.ts` includes a global interceptor that:

- Automatically formats error messages.
- Displays them via `ElMessage.error`.
- Logs details to the console for debugging.

**Incorrect:**

```typescript
try {
  await execute();
} catch (error) {
  ElMessage.error("Failed to fetch");
}
```

**Correct:**

```typescript
// Error is handled automatically by http.ts
await execute().catch(() => undefined);
```

## 2. Naming Conventions

Use **semantic, verb+noun** names. **NEVER** use the `execute` prefix (e.g., `executeDelete`, `executeFetch`).

### Rule: Only rename when there are multiple useAxios calls in the same component

| Property    | Only 1 in component | Multiple in component                                                |
| ----------- | ------------------- | -------------------------------------------------------------------- |
| `data`      | Keep `data`         | Rename to content meaning: `detail`, `materials`, `drafts`           |
| `execute`   | Keep `execute`      | Rename to semantic verb: `fetchDetail`, `deleteDraft`, `uploadFile`  |
| `isLoading` | Keep `isLoading`    | Rename to scenario: `isSubmitting`, `isDownloading`, `draftsLoading` |

**Incorrect:**

```typescript
const { execute: executeFetch } = useAxios(...)
const { execute: executeDeleteDraft } = useAxios(...)
const { data: detailsData } = useAxios(...)
const { data: dataStatsRes } = useAxios(...)
```

**Correct:**

```typescript
// Single useAxios — no rename needed
const { data, execute, isLoading } = useAxios(...)

// Multiple useAxios — use semantic names
const { data: detail, execute: fetchDetail } = useAxios(...)
const { execute: deleteDraft } = useAxios(...)
const { data: materials, execute: fetchMaterials, isLoading: materialsLoading } = useAxios(...)
```

## 3. Simplified Signature & Defaults

`useAxios` defaults to `immediate: true` when only a URL and instance are passed. **But** providing an options object replaces the defaults, making `immediate` become `undefined` (falsy).

- **Always declare `immediate: true` explicitly** when passing an options object and wanting auto-execution.
- **Omit `immediate: false`** when the intent is obvious from context (e.g., mutations with empty URL).

```typescript
// Auto-fetch on mount — must declare immediate explicitly since options object is provided
const { data, isLoading } = useAxios<T>("/url", axiosInstance, {
  immediate: true,
  initialData: { results: [], count: 0 },
});

// Auto-fetch — no options object, immediate defaults to true
const { data } = useAxios<T>("/url", axiosInstance);

// Manual execution — immediate defaults to false when options aren't provided
// because the empty URL signals manual use
const { execute: submitMaterial, isLoading: isSubmitting } = useAxios<T>(
  "",
  axiosInstance,
);
const { execute: deleteDraft } = useAxios(
  "",
  { method: "DELETE" },
  axiosInstance,
);
```

## 4. Leverage Internal Loading States

Always use the `isLoading` property returned by `useAxios` instead of defining a separate `loading` ref.

```typescript
const { isLoading: isSubmitting } = useAxios("/url", axiosInstance);

// In template:
// <el-button :loading="isSubmitting">Submit</el-button>
```

## 5. Use initialData to Simplify Templates

When fetching objects or lists, provide `initialData` to pre-populate the `data` ref. This eliminates repeated optional chaining (`?.`) in Vue templates.

```typescript
const { data } = useAxios<PaginatedResponse>("/url", axiosInstance, {
  immediate: true,
  initialData: { results: [], count: 0 },
});

// In template — no need for data?.results
// <el-table :data="data.results">
// <el-pagination :total="data.count">
```

## 6. Callbacks: onSuccess and onError

Use `onSuccess` for post-request logic (closing modals, toasts, state updates). Use `onError` for navigation on failure (e.g., redirect to home on 404).

```typescript
// onSuccess — handle side effects after successful request
const { execute: updateFiles } = useAxios<FileUpload[]>(
  "/upload/file/update/",
  { method: "POST" },
  axiosInstance,
  {
    onSuccess: (files) => {
      ElMessage.success("Upload success!");
      categoryRef.value = [...categoryRef.value, ...files];
      isDialogVisible.value = false;
    },
  },
);

// onError — redirect on failure
const { data: detail, execute: fetchDetail } = useAxios<MaterialDetail>(
  "",
  axiosInstance,
  {
    onSuccess: ({ expSerial }) => {
      /* process data */
    },
    onError: () => router.push("/"),
  },
);
```

## 7. Using execute() Return Value

`execute()` returns `StrictUseAxiosReturn`, which gives you access to `data`, `error`, etc. **Use this instead of a separate `data` ref** when you need an inline result.

```typescript
// ✅ Use return value — avoids needing a separate data ref
const { execute: uploadFile } = useAxios<FileUpload>(
  "/upload/file/",
  { method: "POST" },
  axiosInstance,
  {
    abortPrevious: false,
  },
);

const handleFileUpload = async ({ file }: UploadRequestOptions) => {
  const formData = new FormData();
  formData.append("file", file);
  const { data } = await uploadFile({ data: formData });
  return data.value!;
};

// ✅ Use return value in submit flow
const response = await submitMaterial(url, { method, data }).catch(
  () => undefined,
);
if (!response) return;
router.push(`/details/${response.data.value.id}`);
```

## 8. Static vs. Dynamic Configuration

### A. Define behavior at initialization (Static)

- **Hooks & Callbacks**: `onSuccess`, `onError`
- **Behavior**: `immediate`, `initialData`, `abortPrevious`
- **Base Request Config**: Fixed `headers`, `method`, or the base `url`

### B. Pass only variables to execute (Dynamic)

- **Request Body**: `data` (for POST/PUT)
- **Query Params**: `params`
- **URL Overrides**: Dynamic URL or one-off configs

```typescript
// 1. Static config at initialization
const { execute: searchImages } = useAxios<Response>(
  "/services/",
  { method: "POST" },
  axiosInstance,
  {
    onSuccess: ({ images }) => (serialImages.value = images),
  },
);

// 2. Dynamic data at execution time
const onSearch = () =>
  searchImages({
    data: { filters: JSON.stringify(filterItems.value) },
  }).catch(() => undefined);
```

## 9. Paginated List Pattern

For components with paginated tables, use `params` with `reactive` + `watch` to auto-refetch:

```typescript
const params = reactive({ page: 1, pageSize: 10 });

const {
  data,
  execute: fetchData,
  isLoading,
} = useAxios<PaginatedResponse>("/items/", { params }, axiosInstance, {
  immediate: true,
  initialData: { results: [], count: 0 },
});

// Auto-refetch when params change
watch(params, () => fetchData().catch(() => undefined));
```

## 10. Mutation with Refresh Pattern

For delete/update operations that need to refresh a list afterward:

```typescript
const { execute: deleteItem } = useAxios(
  "",
  { method: "DELETE" },
  axiosInstance,
  {
    onSuccess: () => {
      ElMessage.success("Deleted");
      if (data.value.results.length === 1 && params.page > 1) params.page -= 1;
      else fetchData().catch(() => undefined);
    },
  },
);

const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm("确认删除?", "提示", { type: "warning" });
    await deleteItem(`/items/${id}/`);
  } catch {
    // Only swallow 'cancel'
  }
};
```
