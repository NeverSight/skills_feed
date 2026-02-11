---
name: tdesign-vue-next
description: TDesign Vue 3 component library usage guide, covering tdesign-vue-next 1.x series, including basic components, forms, tables, theme customization, dark mode, and AI Chat components
---

# TDesign Vue Next

## S - Scope

- **Target**: `tdesign-vue-next@^1` with Vue 3.3+
- **Cover**: Basic components, layout components, navigation components, input components, data display components, feedback components, theme customization, dark mode, Chat component
- **Avoid**: Undocumented internal APIs, DOM manipulation hacks, other TDesign tech stacks (React/Miniprogram)

### Default assumptions (when not explicitly specified)

- **Language**: TypeScript + `<script setup>` syntax
- **Styling**: Use CSS variables and `ConfigProvider` for theme configuration, avoid directly overriding internal component class names
- **Provider**: Use a single `ConfigProvider` at the app root for unified configuration
- **Icons**: Use `tdesign-icons-vue-next` icon library
- **Imports**: Import components on demand `import { Button } from 'tdesign-vue-next'`

### Scope rules (must follow)

1. Only use APIs documented in TDesign official documentation
2. Do not invent props, events, or component names
3. Never use `@ts-ignore` to bypass type checking; consult official type definitions first for type issues
4. If encountering potential bugs or documentation-behavior inconsistencies, clearly inform users and guide them to submit an Issue
5. Example code must be directly runnable, no pseudo-code or ellipsis placeholders

### Complex triggers (must open corresponding `Reference`)

| Trigger Condition                                                                    | Reference                              |
| ------------------------------------------------------------------------------------ | -------------------------------------- |
| Dynamic forms (`FormItem` add/remove), cross-field validation, async validation      | `references/form-advanced.md`          |
| Server-side sorting/filtering/pagination, virtual scroll, editable table, tree table | `references/table-advanced.md`         |
| Remote search, large datasets, paginated loading, custom rendering                   | `references/select-advanced.md`        |
| Controlled file list, resumable upload, custom upload request                        | `references/upload-advanced.md`        |
| Async node loading, checkStrictly, virtual scroll                                    | `references/tree-advanced.md`          |
| Async loading, dynamic options, custom panel                                         | `references/cascader-advanced.md`      |
| Dialog/Drawer nesting, imperative calls, close interception                          | `references/dialog-drawer-advanced.md` |
| Deep theme customization, dynamic theme switching, component-level style override    | `references/theming-advanced.md`       |
| Dark mode toggle, system preference sync, local dark mode                            | `references/dark-mode.md`              |
| AI chat component, streaming response, custom message rendering                      | `references/chat-advanced.md`          |
| TDesign Vue Next 1.x version differences, upgrade guide                              | `references/tdesign-v1.md`             |

### `Reference` index

| Topic                  | Description                                         | `Reference`                            |
| ---------------------- | --------------------------------------------------- | -------------------------------------- |
| Version Reference      | 1.x version scope, upgrade notes                    | `references/tdesign-v1.md`             |
| Form Advanced          | Dynamic forms, linked validation, async validation  | `references/form-advanced.md`          |
| Table Advanced         | Virtual scroll, server-side data, editable cells    | `references/table-advanced.md`         |
| Select Advanced        | Remote search, pagination, custom options           | `references/select-advanced.md`        |
| Upload Advanced        | Controlled upload, custom request, resumable upload | `references/upload-advanced.md`        |
| Tree Advanced          | Async loading, checkStrictly, virtual scroll        | `references/tree-advanced.md`          |
| Cascader Advanced      | Async loading, dynamic panel                        | `references/cascader-advanced.md`      |
| Dialog/Drawer Advanced | Nested layers, imperative calls                     | `references/dialog-drawer-advanced.md` |
| Theme Customization    | CSS variables, Design Token, dynamic theme          | `references/theming-advanced.md`       |
| Dark Mode              | Mode toggle, system preference, local dark mode     | `references/dark-mode.md`              |
| Chat Component         | AI chat, streaming response, message rendering      | `references/chat-advanced.md`          |

---

## P - Process

### 1) Identify component hierarchy

```
User requirements
  ├── Basic display → Button / Link / Icon / Typography
  ├── Layout structure → Layout / Grid / Space / Divider
  ├── Navigation interaction → Menu / Tabs / Breadcrumb / Steps / Pagination
  ├── Data input → Form / Input / Select / DatePicker / Upload / ...
  ├── Data display → Table / List / Tree / Card / Descriptions / ...
  ├── Feedback → Message / Notification / Dialog / Drawer / Loading
  └── Advanced scenarios → Chat (AI conversation)
```

### 2) Clarify context before making suggestions

Before providing component recommendations, confirm:

- Vue version (3.3+ recommended)
- Whether `ConfigProvider` is configured
- Whether dark mode support is needed
- Whether there are special i18n requirements
- Data volume (affects whether virtual scroll is needed)

### 3) ConfigProvider configuration first

```vue
<template>
  <ConfigProvider :global-config="globalConfig">
    <App />
  </ConfigProvider>
</template>

<script setup lang="ts">
import { ConfigProvider } from "tdesign-vue-next";

const globalConfig = {
  // Global configuration
};
</script>
```

### 4) Component selection rules

| Scenario               | Recommended Component              | Notes                                          |
| ---------------------- | ---------------------------------- | ---------------------------------------------- |
| Simple list display    | `List`                             | Small data, no complex interaction             |
| Complex data table     | `Table`                            | Supports sorting, filtering, pagination        |
| Large data table       | `Table` + `virtual-scroll`         | Enable virtual scroll                          |
| Tree data selection    | `TreeSelect`                       | Single/multiple tree selection                 |
| Cascading selection    | `Cascader`                         | Multi-level linked selection                   |
| Simple dropdown        | `Select`                           | Moderate number of options                     |
| Remote search select   | `Select` + `filterable` + `remote` | Disable local filtering                        |
| File upload            | `Upload`                           | Supports drag, multi-file                      |
| Form collection        | `Form` + `FormItem`                | Unified validation and submit                  |
| Light notification     | `Message`                          | Operation feedback, auto-dismiss               |
| Important notification | `Notification`                     | Requires user confirmation or contains actions |
| Confirmation action    | `Dialog` / `Popconfirm`            | Choose based on context                        |
| Side panel details     | `Drawer`                           | Without interrupting page flow                 |
| AI conversation        | `Chat`                             | Streaming messages, multi-turn dialogue        |

### 5) Form decision chain

```
Need to collect user input?
  ├── Yes → Use Form wrapper
  │     ├── Need dynamic add/remove fields? → See form-advanced.md
  │     ├── Need cross-field linking? → See form-advanced.md
  │     └── Simple form → Use FormItem + rules
  └── No → Use input component directly
```

### 6) Table decision chain

```
Need to display list data?
  ├── Data > 1000 rows? → Enable virtual scroll, see table-advanced.md
  ├── Need server-side pagination/sorting? → See table-advanced.md
  ├── Need editable cells? → See table-advanced.md
  └── Simple table → Use Table + columns + data
```

### 7) Theme customization decision chain

```
Need to customize theme?
  ├── Only modify brand color → ConfigProvider theme prop
  ├── Modify multiple tokens → Override CSS variables
  ├── Deep customization → See theming-advanced.md
  └── Dark mode → See dark-mode.md
```

### 8) Route complex scenarios to `Reference`

When identifying trigger conditions from the Complex triggers table, must:

1. Inform user this is a complex scenario
2. Open the corresponding Reference document
3. Provide suggestions based on recommended patterns in Reference

### 9) Accessibility and performance checks

- Ensure form controls have appropriate `label`
- Enable virtual scroll or pagination for large data scenarios
- Avoid complex calculations in `template`, use `computed`
- Ensure stable `key` for list rendering

---

## O - Output

### Output should include (as needed)

1. **Component recommendation**: Component name and selection rationale
2. **Minimal configuration**: Required ConfigProvider setup
3. **Code example**: Directly runnable `<script setup>` code
4. **Performance tips**: Notes for large data, frequent updates scenarios
5. **Reference path**: Point to corresponding reference docs for complex scenarios
6. **Official documentation link**: Related component's official documentation URL

### Output forbidden

1. Unverified APIs or props
2. Hack code relying on specific internal implementations
3. Incomplete code snippets (missing imports or key configurations)
4. Code for other TDesign tech stacks (React/Miniprogram)
5. Syntax incompatible with user's Vue version

### Regression checklist

- [ ] **ConfigProvider**: Is root component configured, are theme tokens effective
- [ ] **Form**: Are `rules` defined, is validation trigger (`trigger`) correct, is `model` two-way binding correct
- [ ] **Table**: Does `row-key` provide stable unique value, is `columns` cached with `computed`
- [ ] **Select**: Is local filtering disabled for remote search (`filterable` + `:filter` returns true)
- [ ] **Upload**: Is controlled mode `v-model:files` updating correctly, is `action` or `requestMethod` configured
- [ ] **Tree/TreeSelect**: Does `keys` config match data structure, does async load `load` function return Promise
- [ ] **Dialog/Drawer**: `v-model:visible` two-way binding, `destroyOnClose` configured based on scenario
- [ ] **Dark Mode**: Is `theme-mode` attribute added to `<html>` or root element
- [ ] **Icons**: Are icons correctly imported from `tdesign-icons-vue-next`
- [ ] **TypeScript**: Are component props types correct, do event callback parameter types match

---

## Quick Reference

### Installation

```bash
npm install tdesign-vue-next
# Icon library
npm install tdesign-icons-vue-next
```

### Full Import

```ts
// main.ts
import { createApp } from "vue";
import TDesign from "tdesign-vue-next";
import "tdesign-vue-next/es/style/index.css";
import App from "./App.vue";

createApp(App).use(TDesign).mount("#app");
```

### On-demand Import (Recommended)

```ts
// main.ts
import { createApp } from "vue";
import { Button, Input, Form, FormItem } from "tdesign-vue-next";
import "tdesign-vue-next/es/style/index.css";
import App from "./App.vue";

const app = createApp(App);
app.use(Button).use(Input).use(Form).use(FormItem);
app.mount("#app");
```

### Minimal Example

```vue
<template>
  <ConfigProvider>
    <Form :model="formData" :rules="rules" @submit="onSubmit">
      <FormItem label="Username" name="username">
        <Input v-model="formData.username" placeholder="Enter username" />
      </FormItem>
      <FormItem>
        <Button theme="primary" type="submit">Submit</Button>
      </FormItem>
    </Form>
  </ConfigProvider>
</template>

<script setup lang="ts">
import { reactive } from "vue";
import {
  ConfigProvider,
  Form,
  FormItem,
  Input,
  Button,
} from "tdesign-vue-next";
import type { FormRules, SubmitContext } from "tdesign-vue-next";

const formData = reactive({
  username: "",
});

const rules: FormRules<typeof formData> = {
  username: [{ required: true, message: "Username is required" }],
};

const onSubmit = ({ validateResult }: SubmitContext) => {
  if (validateResult === true) {
    console.log("Submit successful", formData);
  }
};
</script>
```

### Official Resources

- Official Documentation: https://tdesign.tencent.com/vue-next/overview
- GitHub: https://github.com/Tencent/tdesign-vue-next
- Design Specifications: https://tdesign.tencent.com/design/values
