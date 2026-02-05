---
name: k8s-crd-design-review
description: |
  Use when reviewing Kubernetes CustomResourceDefinition (CRD) YAML (full manifests or diffs) as the compiled API contract: schema/validation correctness (OpenAPI/CEL), spec vs status boundaries, conditions/observedGeneration conventions, SSA/GitOps list semantics and patchability, printer columns, object-reference modeling (resource relationships: one-to-one, one-to-many), and compatibility/migration risk (breaking-change risk, versioning, rollout). Not for Kubebuilder marker/Go-type selection; use kubebuilder-api-design.
---

# Kubernetes CRD Design Review

Perform a deterministic design + contract review for Kubernetes CRDs (the generated CRD YAML is the compiled API contract).

## Inputs

Accept at least one of:

- CRD YAML (full manifest) or a CRD diff
- Go API types and/or kubebuilder markers used to generate the CRD
- A short description of intended API semantics and controller behavior

If key info is missing, ask for it before concluding compatibility/migration:

- Whether a controller exists, what it owns, and whether it writes `status`
- Whether this is a new API or a change to an existing API
- Served versions, storage version, and existing clients
- Whether objects already exist in clusters (migration needed?)
- Any GitOps/SSA constraints (patch strategy, desired stable identities)

## Workflow (always follow this order)

### 1) Identify scope

- Identify `group`, `kind(s)`, `version(s)`, and whether this is **new** vs **change**.
- Identify controller existence and ownership boundaries.
- If reviewing Go types, confirm which generated CRD YAML(s) correspond to them.

### 2) Contract integrity checks (spec/status + controller operability)

- **Spec vs status boundary**
  - `spec` = user intent / desired state.
  - `status` = controller-observed state.
  - Flag lifecycle/state-machine fields in `spec` if the controller owns transitions.
- **Require `subresources.status` when a controller exists and writes status**
- **Conditions + `observedGeneration`**
  - Recommend `status.conditions` using Kubernetes conventions.
  - Recommend `status.observedGeneration` for tooling/GitOps correctness.
  - Treat Conditions as a **map keyed by `type`** (not a chronological list): avoid duplicate `type` entries and prefer schema markers that enable map semantics for SSA/GitOps.
  - Prefer a single high-signal **summary condition** (`Ready` for long-running resources; `Succeeded` for bounded execution) and keep other Conditions secondary.
  - Prefer **state-style** Condition types (adjectives/past tense like `Ready`, `Degraded`, `Succeeded`). Transition-style names are usually less clear, but can be acceptable for long-running transitions if modeled as an observed state with consistent `True`/`False`/`Unknown` semantics.
  - Avoid state-machine style `status.phase` for new APIs; prefer Conditions.
  - Remember `status` is typically written via the `/status` subresource with separate RBAC.

If needed, load [`./references/conditions-and-status.md`](./references/conditions-and-status.md)

### 3) Schema correctness (prevent invalid stored objects)

Review the OpenAPI v3 schema (prefer the generated CRD YAML/diff):

- Required fields for true invariants
- Enums for constrained strings
- Defaulting and nullable behavior
- Cross-field invalid combinations
  - If the schema cannot express it with basic validation, suggest CEL (`x-kubernetes-validations`) with minimal, targeted rules.

- **Object references & relationships**
  - When a field refers to another Kubernetes object, check that naming and schema follow Kubernetes API conventions:
    - Object references: use `fooRef` / `fooRefs` (structured object(s)), also do this if only the name is needed (please load [`./references/object-references.md`](./references/object-references.md) for more details on the recommended naming conventions)
    - Name-only references are acceptable for existing situations (e.g. `fooName` (string)), do NOT use this for new developemnts.
  - Watch for cross-namespace references (security boundary) and for leaking copied values from the referenced object into `spec`/`status`.

If needed, load [`./references/object-references.md`](./references/object-references.md).
If needed, load [`./references/validation-and-cel.md`](./references/validation-and-cel.md).

### 4) GitOps/SSA ergonomics

Focus on patchability and stable diffs:

- List semantics for arrays of objects
  - If items have stable identity (e.g., `name`, `id`), prefer map-like lists:
    - `x-kubernetes-list-type: map`
    - `x-kubernetes-list-map-keys: ["..."]`
- Identify ordering sensitivity and full-array replacement hazards.

If needed, load [`./references/list-semantics-gitops-ssa.md`](./references/list-semantics-gitops-ssa.md).

### 5) Operator UX (kubectl)

- Review/add `additionalPrinterColumns` for operator-facing UX:
  - Ready / health signal
  - Status message / reason
  - Key spec fields
- Do not duplicate default `AGE`.

If needed, load [`./references/printer-columns.md`](./references/printer-columns.md).

### 6) Compatibility & migration impact (mandatory)

Always include an explicit compatibility assessment.

- Classify change as non-breaking vs potentially breaking.
- Consider more than removals:
  - tightening validation
  - type changes
  - list semantic changes
  - defaulting changes
  - semantic behavior changes
- If version evolution is involved:
  - serving multiple versions
  - conversion webhook need
  - storage version migration reminders
  - deprecation playbook

If needed, load [`./references/versioning-and-migrations.md`](./references/versioning-and-migrations.md).

### 7) Summarize

- Provide ranked risks + why they matter.
- Provide actionable changes + snippets.
- Provide a minimal, PR-sized improvement plan.
- Provide a copy/paste PR review template block.

## Output format (always use this template)

### What’s good

- …

### Top risks (ranked)

1. **…** — why it matters: …
2. **…** — why it matters: …
3. **…** — why it matters: …

### Recommended changes (actionable)

- **Change:** …
  - **Why:** …
  - **Snippet:**
    ```yaml
    # ...
    ```

### Compatibility & migration impact (mandatory)

- **Breaking?** Yes/No
- **Why:** …
- **If breaking or risky:**
  - **Migration / deprecation steps:**
    1. …
    2. …
  - **Rollout plan checklist:**
    - [ ] …
    - [ ] …
  - **Versioning notes:** served versions, storage version, conversion considerations

### Minimal improvement plan (PR-sized)

1. …
2. …
3. …

### PR-ready review template (copy/paste)

Load and reuse the canonical template in [`./references/review-template.md`](./references/review-template.md). If it does not match the context, adapt it but keep the same section headings.
