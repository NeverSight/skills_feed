---
name: nocobase-ai-knowledge-base-manager
description: "NocoBase 2 only; never use in a NocoBase 3 project. Use when users need to check Professional+ knowledge-base capability, consent to enabling an installed-disabled KB plugin, or manage NocoBase vector databases, Local/Readonly/External knowledge bases, documents, retrieval tests, and binding preparation through nb api kb."
argument-hint: "[action: preflight|inspect|create|update|upload|revectorize|test|prepare-binding|delete] [target: capability|vector-db|knowledge-base|document|employee] [mode?: direct-cli|ui] [env?: name]"
allowed-tools: Bash, Read, Grep
owner: platform-tools
version: 2.0.3
last-reviewed: 2026-08-04
risk-level: high
---

# Goal

Provide an edition-aware, capability-first workflow for NocoBase AI knowledge bases. State the Professional Edition or higher requirement before work, prove entitlement/plugin/runtime capability without guessing the edition, offer to enable an installed-disabled required plugin and do so after explicit user consent through plugin management, then safely manage vector databases, knowledge bases, documents, retrieval tests, and employee-binding inputs.

# Required Dependencies

- `@nocobase/plugin-ai-knowledge-base` is a commercial plugin with minimum edition level Professional; Enterprise is also supported, while Community and Standard are not.
- `@nocobase/plugin-ai` must be enabled before the knowledge-base plugin can operate.
- Run `nocobase-ai-manager` only after this skill's capability preflight passes and the selected KB type needs LLM/embedding prerequisites.
- Local document workflows also require an available file storage; ZIP/background processing depends on the active async-task capability.
- `nocobase-ai-employee` owns the final employee record write after this skill prepares and verifies binding inputs.

# Scope

- Classify knowledge-base entitlement, plugin installation/enablement, API capability, and ACL separately.
- When a required plugin is installed but disabled, ask whether to enable the exact package in the exact environment; after explicit consent, use `nocobase-plugin-manage`, verify post-state, refresh runtime metadata, and continue preflight.
- Discover, test, create, update, verify, and safely delete PGVector database configurations.
- Recommend and maintain `LOCAL`, `READONLY`, and `EXTERNAL` knowledge bases.
- List, get, upload, independently re-vectorize/retry, and safely delete documents.
- Run independent semantic hit tests.
- Prepare a verified AI employee binding handoff with enabled KB keys and retrieval defaults.
- Enforce immutable fields, asynchronous completion boundaries, protected secrets, and reverse dependency cleanup.

# Non-Goals

- Do not claim the current edition from a missing `kb` command, missing license key, `nb env info`, or `nb license status`.
- Do not install, synchronize, or disable plugins in this skill. Enable an installed-disabled required plugin only after explicit user consent and only through `nocobase-plugin-manage`; do not merely tell the user to run the command when that workflow is available.
- Do not configure saved LLM services; use `nocobase-ai-manager` after capability preflight.
- Do not write AI employee records directly; use `nocobase-ai-employee` for the final binding/unbinding update.
- Do not manage knowledge-base segments, hidden vector-store change actions, or dedicated async-task commands.
- Do not automatically poll upload, ZIP import, segmentation, or vectorization completion.
- Do not ask whether to vectorize after a successful upload; upload already starts or queues it.
- Do not bypass ACL, dependency protection, existing-table confirmation, or immutable-field rules.

# Input Contract

| Input | Required | Default | Validation | Clarification Question |
|---|---|---|---|---|
| `action` | yes | `preflight` for a KB-intent request, otherwise `inspect` | one of `preflight/inspect/create/update/upload/revectorize/test/prepare-binding/delete` | "Which knowledge-base action should I perform?" |
| `target` | mutation: yes | `capability` for preflight | one of `capability/vector-db/knowledge-base/document/employee` | "Which resource type should I manage?" |
| `env` | no | current env from `nb env list` | configured, reachable, authenticated | "Which NocoBase CLI environment should I target?" |
| `identifier` | update/upload/revectorize/test/prepare-binding/delete: yes | none | exact vector key, KB key/id, document id, or employee username | "What is the exact target identifier?" |
| `knowledgeBaseType` | create: yes | recommend `LOCAL`; never mutate on recommendation alone | one of `LOCAL/READONLY/EXTERNAL` | "Should NocoBase manage documents (Local), read external PGVector data (Readonly), or use an external provider?" |
| `configurationMode` | vector-db create/update: yes | none; never choose implicitly | one of `direct-cli/ui` | "Should this vector database connection use direct CLI parameters or the NocoBase UI flow?" |
| `payload` | direct-CLI create/update or test/prepare-binding: yes | documented product defaults only when user accepts them | type-specific allowed fields and ranges | "Which vector, KB, retrieval, or binding values should be used?" |
| `file` | upload: yes | none | readable supported file or ZIP; KB must be `LOCAL` | "Which file should be uploaded to which Local knowledge base?" |
| `pluginEnableConsent` | required when a required plugin is `installed-disabled` | none; never assume consent | explicit approval for exact package name(s) and environment | "The required plugin is installed but disabled in `<env>`. Should I enable `<package>` now and continue the knowledge-base preflight?" |
| `confirmation` | high-risk action: yes | none | fresh exact-target confirmation after impact is shown | "Confirm this exact destructive or dependency-changing operation?" |

Rules:

- If required input is missing, stop mutation and ask the user for the missing values.
- For every KB-intent request, state the minimum edition requirement before capability probing.
- If the user says "you decide", run preflight/inspection and recommend `LOCAL` for normal managed-document use; do not create or mutate.
- Resolve identifiers from real list/get results; never guess IDs or keys.
- Before creating or changing a vector database connection, require an explicit `direct-cli` or `ui` choice; do not choose for the user.
- For `ui`, use the AI manager's documented UI-mode workflow, stop for user completion, and independently verify safe vector database fields before continuing.
- Do not stop at a manual-enable instruction when a required plugin is installed but disabled and plugin management is available; ask for consent and execute the enablement after approval.
- If enablement is declined, stop before KB mutation and report that the plugin remains disabled.
- Ordinary upload success, ZIP task submission, re-vectorization acceptance, hit-test results, and completion are distinct outcomes.
- Every delete requires its own fresh confirmation immediately before that exact `destroy`.

# Mandatory Clarification Gate

- Max clarification rounds: `2`.
- Max questions per round: `3`.
- Before enabling a required plugin, show the exact environment and package name(s), explain that plugin runtime state will change, and require explicit user consent.
- Consent to enable one package does not authorize enabling any other package; include `@nocobase/plugin-ai` in the same request only when it is also installed-disabled and required.
- After consent, use `nocobase-plugin-manage` in safe mode, require plugin-list readback, refresh the environment, and re-run KB API/ACL checks. If consent is declined or enablement fails, stop before KB mutation.
- Before vector database create/update, require `configurationMode`. For `ui`, hand off to `nocobase-ai-manager` only after KB capability passes; for `direct-cli`, continue in this skill.
- Before `skipTableExistedCheck=true`, require the server's `TABLE_ALREADY_EXISTS` response plus explicit table-reuse confirmation.
- Before immutable-field or vector dependency changes, stop or show the exact migration/retrieval impact and obtain confirmation as applicable.
- Before every vector database, KB, or document delete, show exact target, environment, dependencies, data impact, and rollback limits, then obtain fresh confirmation immediately before that one destroy.
- If entitlement evidence is unknown, continue only when the exact KB plugin is installed/enabled, generated KB commands work, a safe KB read succeeds, and ACL is allowed. Unknown or conflicting plugin/runtime/ACL evidence must stop mutation.

# Workflow

1. Resolve the target environment and immediately disclose: `@nocobase/plugin-ai-knowledge-base` requires NocoBase Professional Edition or higher.
2. Read [edition and capability preflight](references/edition-and-capability.md). Check supported license evidence when available, installed/enabled plugin state, base AI dependency, runtime refresh, generated `kb` help, and a safe read.
3. If `@nocobase/plugin-ai-knowledge-base` or its base `@nocobase/plugin-ai` dependency is installed but disabled, show the exact package name(s) and environment and ask whether to enable them. If approved, invoke `nocobase-plugin-manage` with `action=enable`, verify enabled post-state, run runtime refresh, and continue preflight. If declined or failed, stop without KB mutation; do not send the user away to run the enable command manually.
4. If runtime capability is still not available after applicable consent-based enablement and refresh, stop before LLM, embedding, storage, PGVector, KB, document, or employee mutations. Do not guess Community Edition from weak evidence.
5. Inspect current vector databases, knowledge bases, documents, storage, and requested employee context; read the [command map](references/command-map.md).
6. Select the KB type. Recommend `LOCAL` for normal managed documents; use `READONLY` only for externally maintained PGVector data and `EXTERNAL` only when a provider exists.
7. For `LOCAL`/`READONLY`, run `nocobase-ai-manager` and consume an enabled service, chat-only saved model configuration, and separately discovered embedding model. For `LOCAL`, also resolve file storage.
8. For PGVector create/update, first require a `direct-cli` or `ui` choice. In `ui` mode, hand off to `nocobase-ai-manager` after capability passes, stop for user completion, and consume its independent safe-field readback. In `direct-cli` mode, follow [vector database workflow](references/vector-databases.md): provider discovery, protected connection test, create/update, table-reuse guard, dependency impact, and safe readback.
9. For KB create/update, follow [knowledge bases and documents](references/knowledge-bases-and-documents.md): type fields, immutable key/storage rules, segment defaults, vector-change impact, one write, and readback.
10. For upload, validate Local type and file constraints, perform one multipart upload, then report accepted automatic background processing without polling or completion claims.
11. Run document `vectorization` only for an independently requested retry/rebuild. Run hit test only when explicitly requested; neither is an automatic upload follow-up.
12. For employee binding, follow [AI employee binding](references/ai-employee-binding.md), prepare exact enabled keys, prompt/default/range requirements, and hand off the final write to `nocobase-ai-employee`.
13. For cleanup, use reverse dependency order and obtain a separate fresh confirmation before each destructive step.
14. Report preflight evidence, consent and plugin post-state when applicable, writes, readbacks, accepted asynchronous work, partial success, rollback limits, and remaining handoffs separately.

# Reference Loading Map

| Reference | Use When | Notes |
|---|---|---|
| [Edition and capability preflight](references/edition-and-capability.md) | Any request involves KB resources, documents, retrieval, or binding. | Professional+ disclosure, evidence hierarchy, states, and stop/continue matrix. |
| [Command map](references/command-map.md) | Selecting license, plugin, runtime, KB, storage, document, or handoff commands. | Includes excluded surface. |
| [Vector databases](references/vector-databases.md) | Testing or changing PGVector configuration. | Secrets, table validation/reuse, dependencies, readback. |
| [Knowledge bases and documents](references/knowledge-bases-and-documents.md) | Selecting KB type, creating/updating KBs, uploading, retrying, testing, or deleting. | Immutable fields, file constraints, background semantics, and defaults. |
| [AI employee binding](references/ai-employee-binding.md) | Preparing a binding or unbinding request. | Final employee write is delegated to the AI employee skill. |

# Safety Gate

High-impact actions are the high-risk actions listed below:

- every vector database, knowledge base, and document deletion;
- reusing an existing PGVector table;
- changing vector database, LLM service, embedding model, or external vector-store configuration;
- attempting to change immutable KB key or Local storage;
- exposing database passwords or `vectorStoreProps[].value`;
- Plugin enablement without explicit exact-package/environment consent;
- proceeding despite unlicensed, disabled, unavailable, conflicting, or unknown capability evidence;
- changing employee KB answer sources without AI employee skill confirmation.

Secondary confirmation template:

- "Confirm execution: `<action>` on `<resource identifier>` in `<env>`. Expected impact: `<table/data/retrieval/employee dependency impact>`. Type `confirm` to continue."

Rollback guidance:

- Create mismatch: deleting a new vector/KB object requires a separate fresh confirmation.
- Update mismatch: restore previous non-secret writable fields; secrets must be re-supplied.
- Immutable key/storage change: do not patch; plan a new KB and explicit migration instead.
- Upload, ZIP task submission, and accepted background processing may not be reversible.
- Dependency-blocked deletion: preserve the object; never bypass the guard.
- Plugin enablement failure: preserve the observed post-state, do not auto-disable or retry indefinitely, and ask before any rollback disable operation.

# Verification Checklist

- Professional+ minimum requirement was stated before KB work.
- Entitlement, plugin state, runtime capability, and ACL were reported separately.
- No edition was inferred solely from missing commands or license metadata.
- Installed-disabled required plugins triggered an exact package/environment consent question rather than a manual-only instruction.
- Approved enablement used `nocobase-plugin-manage`; post-state showed enabled before runtime/API/ACL checks resumed.
- `@nocobase/plugin-ai` and KB plugin runtime capability were verified before mutation.
- Declined or failed enablement stopped before KB mutation.
- Required LLM/embedding readiness was consumed only after capability passed.
- Saved service `enabledModels` contains chat models only; embedding is separate.
- Target KB type and all conditional fields are valid.
- KB key and Local storage immutability are enforced.
- Segment options satisfy `chunkOverlap < chunkSize`.
- Every vector database create/update had an explicit `direct-cli` or `ui` choice; UI mode paused for user completion and passed independent safe-field readback.
- PGVector connection test succeeds before direct-CLI create/update.
- Existing-table reuse occurs only after `TABLE_ALREADY_EXISTS` and explicit confirmation.
- Every vector/KB create or update has safe readback.
- Upload result is reported as accepted/queued, not completed; supported file/PDF/ZIP constraints were checked.
- Re-vectorization and hit tests run only when independently requested.
- Binding handoff includes available capability, enabled keys, prompt placeholder, and retrieval ranges.
- Every destroy received fresh exact-target confirmation immediately before execution.
- Secrets are absent from summaries and output.
- At least one allowed case and one blocked case are reported correctly.
- Errors, partial success, asynchronous uncertainty, rollback limits, and handoffs are separated.

# Minimal Test Scenarios

1. Capability success: licensed or operational development environment, enabled plugin, generated KB API, and safe read all succeed.
2. Disabled-plugin consent accepted: ask whether to enable the exact installed-disabled package in the target environment, enable it through plugin management after approval, verify enabled post-state, refresh runtime metadata, and continue KB API/ACL checks.
3. Disabled-plugin consent declined: preserve disabled state, perform no KB mutation, and report the blocked next step without instructing the user to run the command manually.
4. Explicit entitlement block: commercial plugin list excludes the KB package and no mutation occurs.
5. Unknown entitlement but operational plugin: runtime capability succeeds, edition remains unverified, and safe KB work may continue with the Professional+ disclosure.
6. Local happy path: prepare storage/LLM/embedding/PGVector, create KB, upload a supported file, and report automatic background processing without polling.
7. Vector UI mode: after capability passes, hand off the UI flow to the AI manager, wait for explicit user completion, and verify the vector database safe fields before KB work continues.
8. Invalid update: attempt to change KB key or Local storage and verify the write is refused with migration guidance.
9. Employee bind: prepare a valid handoff, then delegate the final switch/prompt/retrieval write to the AI employee skill.
10. Auth/capability failure: distinguish 401/403 from license/plugin absence and stop before mutation.
11. High-risk cleanup: require independent fresh confirmation before each document, KB, and vector database delete.

# Output Contract

Final response must include:

- target environment, requested action, resource type, and identifiers;
- minimum edition statement and package name;
- entitlement, plugin pre-state, enablement consent/result, plugin post-state, runtime/API capability, and ACL evidence;
- selected vector database `direct-cli` or `ui` mode and UI completion/readback when applicable;
- prerequisite LLM/embedding/storage/vector results consumed;
- commands executed without secret values;
- safe-field readback for configuration writes;
- upload/task/re-vectorization/hit-test outcome with asynchronous boundaries;
- employee binding handoff when relevant;
- guarded operations, dependency errors, partial success, rollback limits, and remaining work;
- defaults or assumptions applied.

# References

- [NocoBase knowledge-base documentation](https://docs.nocobase.com/ai-employees/knowledge-base/): use for current KB types, vector configuration, documents, RAG, and product behavior. [verified: 2026-08-01]
- [NocoBase CLI documentation](https://docs.nocobase.com/api/cli/): use for current env, license-plugin, plugin-list, and generated API commands. [verified: 2026-08-01]
- [Edition and capability preflight](references/edition-and-capability.md): use for Professional+ gating and evidence classification.
- [Command map](references/command-map.md): use for supported command selection.
- [Vector databases](references/vector-databases.md): use for PGVector safety and lifecycle.
- [Knowledge bases and documents](references/knowledge-bases-and-documents.md): use for type selection, immutable fields, documents, and background processing.
- [AI employee binding](references/ai-employee-binding.md): use for validated binding handoff.
