---
name: nocobase-ai-manager
description: "NocoBase 2 only; never use in a NocoBase 3 project. Use when users need to inspect or maintain NocoBase core AI prerequisites through nb api, including LLM providers, saved services, CLI-versus-UI configuration routing, chat models, embedding discovery, secure credentials, and dependency-safe changes."
argument-hint: "[action: inspect|configure|update|delete|verify] [target: llm-provider|llm-service|vector-db] [mode?: direct-cli|ui] [consumer?: core-ai|employee|knowledge-base] [env?: name]"
allowed-tools: Bash, Read, Grep
owner: platform-tools
version: 2.0.2
last-reviewed: 2026-08-04
risk-level: high
---

# Goal

Prepare and maintain the core NocoBase AI runtime and saved LLM services required by AI employees and, after the commercial capability gate has passed, knowledge bases. Require explicit direct-CLI-versus-UI routing for LLM service and vector database connection configuration, and keep chat-model configuration, embedding-model discovery, credentials, dependency checks, and verification separate and explicit.

# Scope

- Confirm the target `nb` environment, authentication, runtime refresh, and generated `ai` command surface.
- Discover LLM providers, unsaved provider models, saved services, chat models, and embedding models.
- Test provider settings and create, update, enable, disable, verify, or safely delete saved LLM services.
- Before creating or changing an LLM service or vector database connection configuration, require the user to choose direct CLI parameters or the documented UI flow; verify user-completed UI work before follow-up.
- Produce a structured core-AI readiness result for `nocobase-ai-employee`.
- Produce conditional LLM/embedding prerequisites for `nocobase-ai-knowledge-base-manager` only after that skill has confirmed knowledge-base capability.
- Check employee and knowledge-base dependencies before disruptive LLM service changes.

# Non-Goals

- Do not maintain AI employee records; use `nocobase-ai-employee`.
- Do not write vector database, knowledge-base, or document configurations. For vector database connection work, own the mode choice and UI-flow safety only; hand direct CLI configuration and KB capability checks to `nocobase-ai-knowledge-base-manager`.
- Do not treat a missing `kb` command as proof of Community Edition.
- Do not manage AI tools, skills, global settings, roles, employee templates, or move operations.
- Do not enable or disable plugins directly; use the plugin-management workflow.
- Do not use curl, direct database mutation, hidden actions, or values copied from secret-bearing responses when a supported `nb api` command exists.

# Input Contract

| Input | Required | Default | Validation | Clarification Question |
|---|---|---|---|---|
| `action` | yes | `inspect` | one of `inspect/configure/update/delete/verify` | "Which AI prerequisite action should I perform?" |
| `target` | mutation: yes | `llm-provider` for inspect | one of `llm-provider/llm-service/vector-db`; `vector-db` is routing/UI only | "Should I inspect providers, manage a saved LLM service, or route a vector database connection configuration?" |
| `consumer` | no | `core-ai` | one of `core-ai/employee/knowledge-base` | "Is this readiness check for core AI, an AI employee, or a knowledge base?" |
| `env` | no | current env from `nb env list` | configured, reachable, authenticated | "Which NocoBase CLI environment should I target?" |
| `identifier` | update/delete/verify: yes as applicable | none | exact saved LLM service `name` or vector database identifier for UI update | "What is the exact service name or vector database identifier?" |
| `configurationMode` | configure/update of `llm-service` or `vector-db`: yes | none; never choose implicitly | one of `direct-cli/ui` | "Should this configuration use direct CLI parameters or the NocoBase UI flow?" |
| `payload` | direct-CLI configure/update of `llm-service`: yes | none | allowed fields only; secrets supplied by the user | "Which provider, chat models, options, and enabled state should be used?" |
| `knowledgeBaseCapability` | `consumer=knowledge-base` or `target=vector-db`: yes before mutation/UI opening | none | readiness result from `nocobase-ai-knowledge-base-manager` with `runtimeCapability=available` | "Has the knowledge-base edition/plugin capability preflight passed?" |
| `confirmation` | high-risk action: yes | none | fresh explicit confirmation after exact target and impact are shown | "Confirm this exact disruptive LLM service change?" |

Rules:

- If required input or capability evidence is missing, stop mutation and ask clarification.
- If the user says "you decide", inspect and recommend only; do not create, update, disable, or delete.
- Never invent credentials, provider keys, service names, model identifiers, base URLs, or hidden IDs.
- Before creating or changing an LLM service or vector database connection configuration, ask the user to choose `direct-cli` or `ui`; do not choose on the user's behalf.
- In UI mode, use only documented `--ui` flags and optional provider selection. Never include request-body fields, credentials, or secrets.
- A `--ui` command only opens a form. Stop after opening it, resume only after the user reports completion, and independently verify safe fields before any dependent operation.
- `enabledModels.models` accepts only large-language/chat models. Never place an embedding model there.
- Discover embedding models separately and return them only for knowledge-base configuration.
- Do not silently convert create into update.

# Mandatory Clarification Gate

- Max clarification rounds: `2`.
- Max questions per round: `3`.
- Before mutation, confirm environment, exact service/resource identifier, provider, intended chat models, enabled state, secret source, consumer, and dependency impact.
- Before configure/update of an LLM service or vector database connection, require an explicit `configurationMode`. For `ui`, verify current help exposes `--ui`; after opening the form, wait for explicit user completion and then perform independent readback.
- For `target=vector-db`, require current KB capability before opening the UI or handing direct CLI work to the KB manager.
- For a knowledge-base consumer, require a current capability result from `nocobase-ai-knowledge-base-manager`; this skill does not perform or bypass the commercial edition gate.
- Before disable, provider replacement, chat-model removal, or delete, inspect all readable employee and knowledge-base dependencies.
- If knowledge-base dependencies cannot be inspected, treat dependency state as `unknown` and block disruptive service changes.
- Before every service deletion, show the exact service, environment, dependencies, and irreversibility, then obtain a fresh secondary confirmation immediately before `destroy`.
- Never execute a secret-bearing command until protected temporary-file handling is ready.

# Workflow

1. Resolve the target environment with `nb env list`; use `nb env info <env>` only for environment, API, database, and authentication context, not edition detection.
2. Run `nb env update <env> --verbose`, then verify `nb api ai --help`, `nb api ai llm-providers --help`, and `nb api ai llm-services --help`.
3. Read the [command map](references/command-map.md) and [UI-mode workflow](references/ui-mode.md), then select only commands confirmed by current help.
4. Before creating or changing an LLM service or vector database connection, ask the user to choose `direct-cli` or `ui`; never infer a mode.
5. For `ui`, require current help to expose `--ui`. For vector databases, also require an available KB capability result. Run only the documented UI command with at most its optional provider flag, stop while the user completes the form, then independently read back safe fields before continuing.
6. For `target=vector-db` with `direct-cli`, hand off to `nocobase-ai-knowledge-base-manager`; this skill does not write vector database configuration.
7. Inspect providers and models. Classify every discovered model as chat/LLM or embedding before building any direct LLM-service write.
8. For new or changed direct-CLI provider settings, use a protected body file, discover unsaved models, and run `test-flight` with a chat model before saving.
9. Query the exact service name. If absent, create; if present and equivalent on safe fields, report satisfied; if different, show the safe diff and ask update or skip.
10. When `consumer=knowledge-base`, consume the passed capability result and discover embedding models separately. Never add them to the saved service's `enabledModels`.
11. Before disable, provider/model replacement, or delete, inspect employee references. Inspect knowledge-base references only through an available KB capability; if that dependency read is unavailable, stop the disruptive mutation.
12. Execute one requested mutation at a time. Suppress secret-bearing response output and never echo provider `options`.
13. Read back safe fields and verify `name`, `title`, `provider`, `enabled`, and chat-only `enabledModels`.
14. Return a structured readiness contract separating `coreAI` from conditional `knowledgeBasePrerequisites`, including configuration mode and UI completion/readback when applicable.
15. Remove protected temporary files on success, failure, interruption, or rollback.

# Reference Loading Map

| Reference | Use When | Notes |
|---|---|---|
| [Command map](references/command-map.md) | Selecting exact environment, provider, service, model, employee, or KB dependency commands. | Includes excluded command surface and capability boundaries. |
| [UI-mode workflow](references/ui-mode.md) | Creating or changing an LLM service or vector database connection through the UI. | Defines mode selection, supported `--ui` commands, required pause, and independent readback. |
| [LLM service workflow](references/llm-services.md) | Testing, creating, updating, disabling, deleting, or verifying a saved service. | Defines chat/embedding separation, idempotency, readiness, and dependency behavior. |
| [Security and troubleshooting](references/security-and-troubleshooting.md) | Handling credentials or runtime, auth, provider, capability, timeout, or rollback failures. | Defines protected files and safe output. |

# Safety Gate

High-impact actions are the high-risk actions listed below:

- every LLM service deletion, including rollback or cleanup deletion;
- disabling a service used by employees or knowledge bases;
- changing provider, credentials, or enabled chat models on a referenced service;
- proceeding when knowledge-base dependency state is unreadable;
- continuing after a UI form opens without explicit user completion and independent readback;
- exposing provider `options`, API keys, access tokens, UI credentials, or secret-bearing response bodies.

Secondary confirmation template:

- "Confirm execution: `<action>` on LLM service `<name>` in `<env>`. Expected impact: `<employee/knowledge-base dependency and availability impact>`. Type `confirm` to continue."

Rollback guidance:

- Create verification failure: preserve evidence; deleting the new service requires a separate fresh confirmation.
- Update mismatch: restore the previous safe fields; credentials must be re-supplied and must not be recovered from logs.
- Delete: restoration is impossible without the original provider secrets and model configuration.
- UI result absent or mismatched: stop and report actual state; do not infer success or switch to direct CLI without a new explicit mode choice.
- Unknown KB dependency state: do not mutate; restore capability visibility first instead of guessing.

# Verification Checklist

- Target environment, API base URL, and authentication context are confirmed.
- Runtime refresh completed and required `ai` command groups exist.
- Before every LLM service or vector database connection create/update, the user explicitly selected `direct-cli` or `ui`.
- UI mode was available in current help, contained no request-body/secret flags, paused for user completion, and passed independent safe-field readback.
- Provider and requested model identifiers were discovered from the target environment.
- Every requested `enabledModels.models[]` item is a chat/LLM model.
- No embedding model appears in `enabledModels`.
- Knowledge-base consumers supplied an available capability result before LLM/embedding mutation.
- Changed provider settings passed `test-flight` with a chat model.
- Write payload contains only documented writable service fields and excludes `modelOptions`.
- Every create/update has independent safe-field readback.
- Employee dependencies were inspected before disruptive changes.
- KB dependencies were inspected, or the disruptive action was blocked because that state was unknown.
- Every `destroy` received fresh confirmation for that exact service immediately before execution.
- Secrets and full `options` are absent from command summaries and final output.
- At least one allowed configuration and one denied case are reported correctly.
- Errors, partial success, rollback limits, and remaining handoffs are separated.

# Minimal Test Scenarios

1. Inspect-only: refresh runtime and list providers and saved services without mutation.
2. UI mode: open an LLM service or capability-approved vector database form, stop for explicit user completion, and independently verify safe fields before follow-up.
3. Configure: test unsaved settings, save chat-only `enabledModels`, read back, and separately report embedding models for an already capability-approved KB consumer.
4. Missing input: omit provider credentials, service name, mode choice, or required KB capability evidence and verify mutation is blocked.
5. Auth/runtime failure: refresh or `ai` help fails and the skill stops with actionable recovery guidance.
6. Dependency safety: KB dependency visibility is unavailable during a service delete and the delete is blocked even if employee references are empty.
7. High-risk delete: a dependency-free service is destroyed only after fresh exact-target confirmation and absence verification.

# Output Contract

Final response must include:

- target environment, requested action, target, and consumer;
- runtime/help capability checked;
- selected `direct-cli` or `ui` mode and, for UI, the user's completion report plus independent readback result;
- provider, service name, chat models, and separately discovered embedding models;
- commands executed without secret values;
- safe-field readback;
- structured `coreAI` and conditional `knowledgeBasePrerequisites` readiness;
- dependency status, including any unknown KB visibility;
- guarded actions, partial success, rollback limits, and handoffs;
- defaults or assumptions applied.

# References

- [NocoBase official documentation](https://docs.nocobase.com/): use when checking current AI plugin and CLI behavior. [verified: 2026-08-01]
- [Command map](references/command-map.md): use for the supported `nb env` and `nb api ai` surface.
- [UI-mode workflow](references/ui-mode.md): use for explicit mode selection, supported `--ui` commands, required user-completion pause, and post-UI verification.
- [LLM service workflow](references/llm-services.md): use for provider discovery, testing, CRUD, readiness, and dependency checks.
- [Security and troubleshooting](references/security-and-troubleshooting.md): use for secret handling, capability failures, safe output, and rollback.
