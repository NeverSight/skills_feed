---
name: component-creater
description: An autonomous workflow that converts a design file (via URL) into production-ready Shadcn-Vue components. It retrieves the DSL, validates components against the official registry, maps styles to Tailwind CSS, and verifies the output..
version: 1.0.0
license: MIT
authors: [玄子]
---

# Shadcn Vue Component Builder

## 1. Input Parameters

* `design_file_url`: (Required) The URL link to the design file (e.g., Figma link or hosted design asset) to be processed.

## 2. Required Tools (shadcn-vue MCP)

The following tools must be available in the environment:
### 1. `shadcnVue_list_items_in_registries`:
- `Description`: List items from registries. Requires components.json (use init_project if missing).
### 2.`shadcnVue_search_items_in_registries`:
- `Description`: Search for components in registries using fuzzy matching. After finding an item, use get_item_examples_from_registries to see usage examples.
### 3.`shadcnVue_view_items_in_registries`:
- `Description`: View detailed information about specific registry items including the name, description, type and files content. For usage examples, use get_item_examples_from_registries instead.
### 4.`shadcnVue_get_item_examples_from_registries`:
- `Description`: Find usage examples and demos with their complete code. Search for patterns like 'accordion', 'button', 'card', etc. Returns full implementation code with dependencies.
### 5.`shadcnVue_get_add_command_for_items`:
- `Description`: Get the shadcn-vue CLI add command for specific items in a registry. This is useful for adding one or more components to your project.
### 6.`shadcnVue_get_audit_checklist`:
- `Description`: After creating new components or generating new code files, use this tool for a quick checklist to verify that everything is working as expected. Make sure to run the tool after all required steps have been completed.
---

## 3. System Instructions (The Workflow)

You are an expert Frontend Engineer specializing in **Vue 3 (Script Setup)**, **TypeScript**, **Tailwind CSS**, and the **Shadcn-Vue** library.

Your task is to accept a `design_file_url` and output a production-ready Vue component. You must execute the following 5-step workflow strictly in order.

### Step 1: Retrieve Design DSL

**Goal:** Convert the input link into a parsable JSON object.

1. **Execute `get_dsl`:**
* Use the provided `design_file_url` as the argument.
* **CAPTURE OUTPUT**: Look for the file path of the saved JSON (e.g., `.../dsl.json`).


2. **Read DSL Content:**
* Read the content of the file at the path returned by `get_dsl`.
* Parse this content into a JSON object. This object is now your **`dsl_json`** for the rest of the workflow.


### Step 2: Registry Validation, Installation & Context

**Goal:** Identify which DSL nodes map to real Shadcn-Vue components, install them into the project and fetch their documentation.

1. **Fetch the Whitelist:**
* Call shadcnVue mcp tool `shadcnVue_list_items_in_registries` to retrieve the official list of all available components.
* *Reasoning:* We must strictly adhere to the official registry to avoid hallucinating component names.


2. **Analyze DSL, Filter & Install:**
* Traverse the `nodes` tree in the `dsl_json` (obtained in Step 1).
* Extract potential component names from the `name` or `componentInfo` fields.
* **Strict Matching:** Compare these names against the registry whitelist.
* **Fuzzy Fallback:** If a DSL node is named ambiguously (e.g., "PrimaryBtn"), use shadcnVue mcp tool `shadcnVue_search_items_in_registries` to find the correct registry name (e.g., "button").
* **Result:** Create a list of confirmed, unique registry item names (e.g., `['button', 'card', 'input', 'label']`). *Note: Nodes not in the whitelist will be treated as standard HTML elements.*

3. **IMMEDIATE ACTION - Install Components:**
* Generate Command: Call shadcnVue mcp tool  `shadcnVue_get_add_command_for_items` using the list of confirmed component names.
* Execute Command: Take the command string returned by the tool and Immediately execute the final `npx` command in the terminal to install the dependencies.

4. **Build Documentation Context:**
* Using the confirmed list, Call shadcnVue mcp tool `shadcnVue_get_item_examples_from_registries [query=component_name]` for **each** component.
* **CRITICAL PARAMETER RULE**: Pass the list of EXACT component names to the items parameter (e.g., items: ['button', 'card']).
* **PROHIBITED**: DO NOT append words like "example", "demo", "usage", or "component" to the names. (e.g., query='button example' is WRONG; items=['button'] is CORRECT).
* **Action:** Compile the returned examples into a temporary "Knowledge Context".
* **Critical Constraint:** You must use the import paths (e.g., `@/components/ui/button`) and props exactly as shown in these examples.


### Step 3: Structural & Hierarchical Analysis

**Goal:** Map the DSL tree to the Vue Template DOM.

1. **Traverse the Tree:**
* Recursively parse the `dsl_json.nodes`.
* **Mapping Rules:**
* **Shadcn Component:** Map to the component instance (e.g., `<Button>`).
* **Frame/Group:** Map to a container (`div`, `section`, `header`, `footer`).
* **Text:** Map to `<span`, `<p>`, or `<h1>-<h6>`.

2. **Parent-Child Relationships:**
* Respect the `children` array strictly to ensure correct nesting (e.g., `Card` > `CardHeader`).


### Step 4: Style Mapping (The Tailwind Engine)

**Goal:** Convert DSL design tokens into valid Tailwind CSS classes based on the project's CSS configuration.

1. **Analyze Project CSS & DSL Tokens:**
* **Read CSS:** Analyze the content of `src/style.css` provided in the context. Identify defined CSS variables (e.g., `--card-foreground`, `--primary`, `--radius`).
* **Parse DSL:** Analyze the `styles` object in `dsl_json`. Note the `token` field for each paint ID (e.g., `"token": "card-foreground"`).

2. **Visual Mapping (Context-Aware & CSS-Validated):**
* **Colors (Text, Backgrounds, Borders):**
* **Context Logic (Determine Prefix):**
* Node has `textColor`? -> Prefix is **`text-`**
* Node has `fill`? -> Prefix is **`bg-`**
* Node has `stroke` or `borderColor`? -> Prefix is **`border-`**

* **Token matching:**
* Look up the DSL token (e.g., `card-foreground`).
* **Verification:** Confirm this token exists in the project CSS (e.g., as `--card-foreground` or within a `@theme` block).
* **Construction:** Combine Prefix + Token (e.g., `text-` + `card-foreground` = `text-card-foreground`).
* **Fallback:** If (and ONLY if) the DSL provides no token string, use the arbitrary value syntax (e.g., `bg-[#0A0A0A]`).
* **Typography:** Map `font` tokens to `text-{size}`, `font-{weight}`, `leading-{height}`.
* **Layout:** Map `width`, `height`, `padding`, `gap` to standard Tailwind utilities (`w-full`, `p-6`).


### Step 5: Code Generation & Verification

1. **Generate Code:**
* Write the `.vue` file.
* **Constraint:** Ensure the output HTML contains clean, semantic Tailwind classes derived from the mapping step.

2. **Audit (Self-Correction):**
* **Hex Check:** Did I use `text-[#0a0a0a]`? -> **Fix:** Check if `text-card-foreground` applies.
* **Inline Style Check:** Did I use `style="color:..."`? -> **Fix:** Change to semantic class.
* **CSS Validity Check:** Do the generated classes (e.g., `bg-sidebar-primary`) correspond to variables found in the `style.css`? If not, verify if a standard Tailwind class (like `bg-red-500`) was intended.

3. **Audit & Verification：**
* Based on the shadcnVue mcp tool `shadcnVue_get_audit_checklist`: *
* [x] Verified correct component imports.
* [x] Verified correct prop usage (e.g., variants).
* [x] Checked for accessibility attributes.
* [x] Confirmed Tailwind classes match DSL styles.