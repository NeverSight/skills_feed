---
name: kubebuilder-api-design
description: Use when authoring or modifying Kubebuilder Go API types and +kubebuilder markers so generation (`make generate`/`make manifests`) emits the intended CRD schema (validation/defaults, required/optional, list semantics, printer columns, subresources), or when asked which marker/type to use.
---

# Kubebuilder API Design (Go)

Design Kubernetes APIs with Kubebuilder in Go (primarily for Kubernetes operators): CRD type definitions, schema markers, status/conditions, and the core scaffold/regenerate workflow.

Default scope: API design + CRD generation. Do not implement controller/webhook business logic unless explicitly requested.

## Tooling assumptions (what needs to exist for generation)

This skill can help with pure API design (Go types + markers) without running anything, but **to scaffold and to regenerate CRDs/manifests** the user’s environment/project typically needs:

- `go` toolchain (matching the project’s `go.mod` requirements)
- `kubebuilder` CLI (or Operator SDK if they wrap Kubebuilder)
- `make` (Kubebuilder projects drive generation via `Makefile`)

Notes:

- `controller-gen` is usually installed automatically by the project’s Makefile target(s) (pinned version), so it’s not always a separate prerequisite.
- Cluster tooling (`kubectl`, `kind`, etc.) is only needed if they want to run/test against a cluster; keep this out of scope unless explicitly requested.

### Relationship to `k8s-crd-design-review`

Treat the generated CRD YAML as the *compiled API contract*. After shaping Go types + markers and running generation, run a design review on the generated CRD YAML (or diff) using [`../k8s-crd-design-review/SKILL.md`](../k8s-crd-design-review/SKILL.md).

SSA / GitOps note: list semantics are part of the API contract.

- Use list semantics markers (`+listType=set|map`, `+listMapKey=...`) early so generated CRDs behave well under SSA and produce stable diffs.
- Deeper guidance lives in [`../k8s-crd-design-review/references/list-semantics-gitops-ssa.md`](../k8s-crd-design-review/references/list-semantics-gitops-ssa.md).

## Versioning / multi-version CRDs (pointer)

If the user is designing a multi-version API (e.g., `v1alpha1` → `v1beta1` → `v1`) or needs conversion webhooks:

- Follow Kubebuilder’s multiversion tutorial for the mechanics: [`book.kubebuilder.io/multiversion-tutorial/tutorial.html`](https://book.kubebuilder.io/multiversion-tutorial/tutorial.html).
- Keep this skill focused on “Go types + markers + generation”. For compatibility review and migration planning, hand off to [`../k8s-crd-design-review/SKILL.md`](../k8s-crd-design-review/SKILL.md) (especially [`../k8s-crd-design-review/references/versioning-and-migrations.md`](../k8s-crd-design-review/references/versioning-and-migrations.md)).

## Designing relations (object references) in Spec/Status

When a CRD needs to point at another Kubernetes object (or one of its fields/keys), **treat “references” as API design, not a convenience import**.

### Prefer well-scoped, API-owned reference types (avoid generic core types)

Avoid embedding generic Kubernetes reference structs like `corev1.LocalObjectReference` or `corev1.ObjectReference` in *new* APIs.

Kubernetes upstream explicitly discourages new uses of [corev1.LocalObjectReference](https://github.com/kubernetes/api/blob/ab936f91c7907abe4a7e106255c2f0b877f633ef/core/v1/types.go#L7443C1-L7468C2) and [corev1.ObjectReference](https://github.com/kubernetes/api/blob/ab936f91c7907abe4a7e106255c2f0b877f633ef/core/v1/types.go#L7388C1-L7441C2) because it is underspecified and hard to validate/document per usage:

- Key takeaway: “**Instead of using these generic types, create a locally provided and used type that is well-focused on your reference.**”

This guidance applies equally to other overly-generic reference types you may find in older APIs (they tend to have unclear semantics, inconsistent validation, and awkward defaults).

### Pattern: define a dedicated `<Thing>Ref` type per relationship

Define a small, *purpose-built* struct for each relationship, tailored to your CRD:

- Make required fields actually required (don’t mirror upstream backward-compatibility tricks like `omitempty` + default empty string)
- Encode the relationship’s real constraints in schema (name format, allowed kinds, namespace rules)
- Add per-field documentation that matches the domain (so `kubectl explain` is useful)

Example (same-namespace reference by name):

```go
// ConfigMapRef identifies a ConfigMap in the same namespace.
// The referenced ConfigMap must exist before this resource becomes Ready.
type ConfigMapRef struct {
    // Name is the name of the referenced ConfigMap.
    // +kubebuilder:validation:MinLength=1
    // Consider adding a stricter pattern if you want to enforce DNS-1123 label.
    Name string `json:"name"`
}
```

Example (namespace + name, if cross-namespace is allowed by design):

```go
// SecretRef identifies a Secret.
// If Namespace is omitted, it defaults to the resource namespace.
type SecretRef struct {
    // +kubebuilder:validation:MinLength=1
    Name string `json:"name"`

    // +optional
    // +kubebuilder:validation:MinLength=1
    Namespace string `json:"namespace,omitempty"`
}
```

### Decide (and document) the reference semantics up front

For each relation, explicitly choose and document:

- **Scope**: same-namespace only vs cross-namespace (cross-namespace typically needs extra authorization/guardrails)
- **Identity**: name only vs name+namespace vs (rarely) UID/resourceVersion (most APIs should stick to name/namespace)
- **Allowed targets**: fixed Kind (recommended) vs “one-of” kinds (if so, model it explicitly)
- **Lifecycle behavior**: what happens if the target is missing, renamed, deleted, or recreated
- **Status mirroring**: if you surface resolved details (e.g., observed UID), put them in `Status` not `Spec`

If the user asks for “a reference to an arbitrary object”, push back and narrow it: require a specific Kind or a small, explicit set of Kinds, then reflect that in the API type.

## Workflow

### Step 0 — Gather inputs (ask only what’s needed)

1. API identity: Group, Version, Kind, Plural, Scope (Namespaced vs Cluster)
2. Desired Spec fields (including which are required) and any immutability expectations
3. Status needs: conditions? observedGeneration? summary fields?
4. Any constraints: enum values, ranges, patterns, max items, uniqueness, references to other objects

When the user mentions relations/references, capture:

- target kind(s) and whether cross-namespace is allowed
- whether the reference is required
- whether they need to reference a whole object or a sub-field (e.g., secretKeyRef)
- expected behavior when the target does not exist or changes

If the user already has YAML for the CRD, treat it as the contract and map it into Go types + markers.

### Step 1 — Draft the Go API types

Create:

- `type <Kind>Spec struct { ... }`
- `type <Kind>Status struct { ... }`
- `type <Kind> struct { metav1.TypeMeta; metav1.ObjectMeta; Spec; Status }`
- `type <Kind>List struct { metav1.TypeMeta; metav1.ListMeta; Items []<Kind> }`

Rules of thumb:

- Use pointers for optional scalars and optional structs to preserve “unset vs zero”.
- Prefer Kubernetes-native types when relevant (`metav1.Time`, `resource.Quantity`, `intstr.IntOrString`).
- Keep `Status` separate from `Spec`. Include `ObservedGeneration` and `Conditions` when useful.
- For relations, prefer API-owned `<Thing>Ref` structs over embedding generic Kubernetes reference types (see “Designing relations”).

Read [`./references/go-type-patterns.md`](./references/go-type-patterns.md) for common Go/Kubernetes type choices.

### Step 2 — Add Kubebuilder markers (validation, defaults, printing)

Add markers to match the desired API contract:

- Root + subresources:
  - `+kubebuilder:object:root=true`
  - `+kubebuilder:subresource:status`
- Validation + defaults on fields (min/max, pattern, enum, length, items, etc.)
- List semantics for SSA and correctness (`listType=set|map`, `listMapKey=...`)
- Printer columns that reflect the most important status/spec at a glance

Read [`./references/kubebuilder-markers.md`](./references/kubebuilder-markers.md).

For a compact “what marker do I need?” cheat-sheet (root markers, field validation/defaults, list semantics, and printer columns), see [`./references/api_reference.md`](./references/api_reference.md).

### Step 3 — Shape Status + Conditions

Prefer `[]metav1.Condition` unless you have a strong reason to roll your own condition type. Include helper summary fields only if they serve UX.

Read [`./references/status-and-conditions.md`](./references/status-and-conditions.md) (Kubebuilder/Go implementation appendix). For canonical conceptual semantics and review heuristics, defer to [`k8s-crd-design-review/references/conditions-and-status.md`](../k8s-crd-design-review/references/conditions-and-status.md).

### Step 3.5 — Kubebuilder workflow essentials (scaffolding + generation)

When the user needs help with Kubebuilder scaffolding and regeneration steps (but not controller/webhook business logic), follow the short checklist in [`./references/kubebuilder-workflow-essentials.md`](./references/kubebuilder-workflow-essentials.md).

### Step 4 — Provide a “generate + verify” checklist (don’t implement)

Give the user the standard Kubebuilder steps to regenerate CRDs and verify the schema, without writing controller logic:

- Run `make generate` / `make manifests`
- Inspect the generated CRD YAML and confirm:
  - required fields match expectations
  - defaults appear where intended
  - list semantics and map keys are correct
  - printer columns render

Then (recommended): run a contract review pass against the generated CRD YAML (or diff) using [`../k8s-crd-design-review/SKILL.md`](../k8s-crd-design-review/SKILL.md), focusing on compatibility/migration impact, lifecycle/status semantics, and SSA/GitOps ergonomics.

When the user needs more API-shape guidance, point them to the [offical long read of the Kubernetes API conventions](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md).

## Output format

When delivering code, output a single Go snippet per file:

1. package + imports
2. markers
3. `Spec`, `Status`
4. root object + list
5. any type aliases and nested structs

Use concise comments. Put rationale (why a pointer, why listType map, etc.) in short bullet notes after the code.

## Resources

### Kubebuilder book (upstream docs mirror in this repo)

If you need canonical Kubebuilder explanations (beyond this skill’s cheat-sheets), prefer these pages:

- Markers overview + syntax: [`book.kubebuilder.io/reference/markers.html`](https://book.kubebuilder.io/reference/markers.html)
- CRD generation + subresources + storageversion: [`book.kubebuilder.io/reference/generating-crd.html`](https://book.kubebuilder.io/reference/generating-crd.html)
- Operator API example uses `Conditions` with map-like list semantics: [`book.kubebuilder.io/getting-started.html`](https://book.kubebuilder.io/getting-started.html)
- “Designing an API” (types like `resource.Quantity`, `metav1.Time`): [`book.kubebuilder.io/cronjob-tutorial/api-design.html`](https://book.kubebuilder.io/cronjob-tutorial/api-design.html)

### references/
Load these only when needed (to keep context small):

- [`./references/go-type-patterns.md`](./references/go-type-patterns.md)
- [`./references/kubebuilder-markers.md`](./references/kubebuilder-markers.md)
- [`./references/api_reference.md`](./references/api_reference.md)
- [`./references/status-and-conditions.md`](./references/status-and-conditions.md) (Kubebuilder/Go implementation appendix; conceptual semantics live in [`../k8s-crd-design-review/references/conditions-and-status.md`](../k8s-crd-design-review/references/conditions-and-status.md))
- [`./references/kubebuilder-workflow-essentials.md`](./references/kubebuilder-workflow-essentials.md)

---

This skill currently only bundles `references/`. Add `scripts/` or `assets/` later if you want automation helpers or boilerplate templates.
