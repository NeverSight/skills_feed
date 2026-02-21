---
name: formkit-core-skilld
description: "ALWAYS use when writing code importing \"@formkit/core\". Consult for debugging, best practices, or modifying @formkit/core, formkit/core, formkit core, formkit."
metadata:
  version: 1.7.2
  generated_by: Gemini CLI · Gemini 3 Flash
  generated_at: 2026-02-18
---

# formkit/formkit `@formkit/core`

**Version:** 1.7.2 (Dec 2025)
**Deps:** @formkit/utils@^1.7.2
**Tags:** perf: 1.0.0-beta.13-c578106 (Nov 2022), dev: 1.7.1-dev.3466e73 (Dec 2025), latest: 1.7.2 (Dec 2025), next: 1.7.2-next.296355 (Dec 2025)

**References:** [Docs](./references/docs/_INDEX.md) — API reference, guides • [GitHub Issues](./references/issues/_INDEX.md) — bugs, workarounds, edge cases • [GitHub Discussions](./references/discussions/_INDEX.md) — Q&A, patterns, recipes • [Releases](./references/releases/_INDEX.md) — changelog, breaking changes, new APIs

## API Changes

This section documents version-specific API changes — prioritize recent major/minor releases.

- NEW: `useFormKitContext()` — v1.6.0, access parent context with optional effect callback [source](./references/releases/v1.6.0.md:L11)

- NEW: `useFormKitContextById()` — v1.6.0, access any context by its explicit id [source](./references/releases/v1.6.0.md:L12)

- NEW: `useFormKitNodeById()` — v1.6.0, access any node by its explicit id [source](./references/releases/v1.6.0.md:L13)

- NEW: `stopWatch()` — v1.6.0, de-registers receipts from the `watchRegistry` function [source](./references/releases/v1.6.0.md:L15)

- NEW: `library` prop — v1.6.0, adds additional components to the input schema for sections-schema [source](./references/releases/v1.6.0.md:L19)

- NEW: `createInput` — v1.5.0, third argument `sectionsSchema` allows extending default sections [source](./references/releases/v1.5.0.md:L16)

- NEW: `didMount` / `mounted` — v1.5.0, context property and node event to detect DOM mounting [source](./references/releases/v1.5.0.md:L17)

- NEW: `changeLocale()` — v1.5.0, globally change locale for all forms across multiple APIs [source](./references/releases/v1.5.0.md:L20)

- NEW: `date_after_node` — v1.7.0, compare date against another field; also `date_before_node` [source](./references/releases/v1.7.1.md:L11)

- NEW: `passing` state — v1.6.3, `context.state.passing` indicates if input satisfies validation rules [source](./references/releases/v1.6.3.md:L11)

- NEW: `minAutoHeight` — v1.7.0, prop for auto-height textarea addon to respect CSS min-height [source](./references/releases/v1.7.1.md:L13)

- BREAKING: `@formkit/vue` — v1.6.0, Vue is now a peer dependency to avoid multiple instance issues [source](./references/releases/v1.6.0.md:L32)

- DEPRECATED: Genesis CSS theme — v1.5.0, marked as legacy; use Tailwind themes instead [source](./references/docs/essentials/styling.md:L18)

- NEW: `mergeStrategy` (experimental) — v1.6.1, syncs two nodes of same name in same parent (experimental) [source](./references/releases/v1.6.1.md:L11)

**Also changed:** `getNode<T>()` generic v1.6.0 · Boolean props shorthand v1.5.0 · `summaryHeader` i18n v1.7.0 · `node.children` reactivity v1.5.0 · `FormKitTypeDefinition` inference v1.6.0 · `themes` peer deps removed v1.7.1

## Best Practices

- Read resolved configuration and prop data from `node.props` rather than `node.config` — explicit props and parent configurations are automatically merged into the props object [source](./references/docs/essentials/architecture.md#config--props)

- Synchronize multiple inputs with the same name at the same level using the `mergeStrategy` config option — prevents value conflicts when identical names are required by template structure [source](./references/docs/essentials/architecture.md#syncing-multiple-nodes-with-the-same-name)

- Use `node.input(value)` instead of direct assignment to `node.value` — ensures the tree's state is tracked and triggers the asynchronous settlement process [source](./references/docs/essentials/architecture.md#setting-values)

- Await `node.settled` before programmatically reading form values or submitting — guarantees all asynchronous input commits and side effects are complete [source](./references/docs/essentials/architecture.md#value-settlement)

- Append `.deep` to event names in `node.on()` to capture events bubbling from descendants — allows parent nodes or plugins to respond to subtree lifecycle changes [source](./references/docs/essentials/architecture.md#add-listener)

- Leverage `node.ledger` to create reactive, tree-wide counters for messages — efficiently sums message states (like errors or visibility) across complex form structures [source](./references/docs/essentials/architecture.md#ledger)

- Traverse the node tree using `node.at()` with special tokens like `$root`, `$parent`, and `$self` — provides a robust way to access relative nodes without hardcoding absolute paths [source](./references/docs/essentials/architecture.md#traversal)

- Opt out of `defaultConfig` in production to enable tree-shaking for unused rules, inputs, and locales — significantly reduces bundle size by manually registering only required features [source](./references/docs/guides/optimizing-for-production.md#a-custom-configuration)

- Register middleware via `node.hook` within plugins to intercept core operations — enables reusable logic for transforming props, values, or error messages across multiple forms [source](./references/docs/essentials/architecture.md#hooks)

- Always remove event listeners using the "receipt" returned by `node.on()` via `node.off(receipt)` — prevents memory leaks and redundant execution in long-lived or dynamic form contexts [source](./references/docs/essentials/architecture.md#remove-listener)
