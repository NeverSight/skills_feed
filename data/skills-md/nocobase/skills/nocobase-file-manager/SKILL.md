---
name: nocobase-file-manager
description: "NocoBase 2 only; never use in a NocoBase 3 project. Manage NocoBase file storage engines, file collections, their business relations, and file records through nb CLI. Use when the primary task concerns NocoBase file storage configuration, file-model setup, access or retention behavior, or storage/file-record lifecycle."
argument-hint: "[action: inspect|create|update|verify|finalize|delete] [target: storage|file-collection|relation|file-record] [env?: name]"
allowed-tools: Bash(nb:*) Read Grep
compatibility: "Requires the nb CLI, a configured and authenticated NocoBase environment, and network access to that environment."
owner: platform-tools
version: 1.1.0
last-reviewed: 2026-07-30
risk-level: high
---

# Goal

Configure and use NocoBase file storage safely from the user's point of view: choose a storage engine, create or update it, model first-class file collections, relate business records to those files, and verify storage and file lifecycle behavior through supported `nb api` commands.

# Scope

- Inspect, create, update, verify, and safely delete `local`, `s3`, `ali-oss`, `tx-cos`, and optional `s3-compatible` (S3 Pro) storage records.
- Explain NocoBase URL, original URL, public access, signed URL, upload rules, renaming, default storage, and physical-file retention.
- Inspect, create, and verify a `template: "file"` collection and ordinary relation fields that point to it.
- Inspect, create metadata for, update, list, and safely delete records in file collections.
- Use `nb api resource` for ordinary resource CRUD and the high-level data-modeling commands for file collections and relations.
- Read the live file-manager Swagger before relying on optional or version-specific actions.

# Non-Goals

- Do not create new fields with the deprecated `attachment` interface or model new business data against the shared `attachments` collection.
- Do not handle generic collection/relation modeling whose primary intent is unrelated to file storage.
- Do not delete file collections or relation fields; use the data-modeling workflow after their dependencies and migration impact are explicitly scoped.
- Do not migrate physical objects between storage backends, rewrite historical object keys, or mutate the database directly.
- Do not configure an object-storage provider's bucket, IAM policy, DNS, CDN, or CORS outside NocoBase.
- Do not invent a binary-upload `nb api resource` flag; generic resource create accepts JSON records, not local file bytes.
- Do not use curl or direct HTTP while an applicable `nb api` command exists.
- Do not expose, echo, or persist plaintext access keys in command arguments, logs, generated files, or final output.

# Input Contract

| Input | Required | Default | Validation | Clarification Question |
|---|---|---|---|---|
| `action` | yes | `inspect` | one of `inspect/create/update/verify/finalize/delete` and valid for the selected target | "Which file-manager action should I perform?" |
| `target` | mutation: yes | infer for unambiguous inspect/verify only | one of `storage/file-collection/relation/file-record` | "Which storage, file collection, relation, or file record should I manage?" |
| `env` | no | current CLI environment | configured, reachable, and authenticated | "Which NocoBase CLI environment should I target?" |
| `identifier` | single-target inspect/update/verify/delete: yes | none | exact storage ID/name, collection name plus field name, or file-record primary key; optional for list inspection | "What is the exact target identifier?" |
| `storageType` | storage create: yes | none | one of `local/s3/ali-oss/tx-cos/s3-compatible`; type must be registered | "Which storage engine type should be configured?" |
| `storageValues` | storage create/update: yes | none | engine-specific fields; secrets must use `{{env.VARIABLE_NAME}}` placeholders | "Which non-secret settings and environment-variable placeholders should be used?" |
| `relationSpec` | relation create: yes | none | source business collection, target file collection, field names, and one of `m2o/o2m/m2m` from real ownership/reuse needs | "Which business collection owns or reuses which file collection?" |
| `fileMetadata` | file-record finalize: yes | none | authoritative metadata from a verified external/direct upload; never a local-file path presented as an upload | "What authoritative metadata did the completed external upload return?" |
| `confirmation` | high-risk mutation: yes | none | fresh confirmation after exact target and impact are shown | "Confirm this exact destructive or access-changing operation?" |

Rules:

- Valid action-target combinations are:
  - `storage`: `inspect/create/update/verify/delete`;
  - `file-collection`: `inspect/create/verify`;
  - `relation`: `inspect/create/verify`;
  - `file-record`: `inspect/finalize/update/verify/delete`.
- Reject any other combination instead of reinterpreting it as a nearby operation.
- If a required input or capability is missing, stop mutation and ask for it.
- If the user says "you decide", inspect only; do not create storage, change access, alter defaults, create relations, or delete records.
- Resolve identifiers from live list/get results. Never guess storage IDs, collection names, field names, or record IDs.
- Never translate a request for files into `interface: "attachment"`. Create a file collection first, then create an ordinary relation to it.
- Treat `nb api resource create --resource <fileCollection>` as metadata finalization only when the object already exists in storage; it is not a binary upload.

# Mandatory Clarification Gate

- Max clarification rounds: `2`.
- Max questions per round: `3`.
- Before any mutation, confirm environment, exact target, current state, intended result, and required plugin capability.
- Before storage create/update, confirm that credential values are environment placeholders such as `{{env.FILE_S3_SECRET_ACCESS_KEY}}`, never plaintext.
- Before changing `default`, URL mode, public access, signed-URL behavior, storage binding, `paranoid`, rename mode, path, or upload rules, show the exact access or lifecycle impact and obtain fresh secondary confirmation.
- Before every storage or file-record deletion, show the exact target, referencing file collections/records, physical-object impact, and rollback limit, then obtain fresh secondary confirmation immediately before that deletion.
- If live Swagger, `nb api resource`, data-modeling commands, authentication, or the required storage type is unavailable, stop before writing.

# Workflow

1. Resolve the action-target combination, environment, exact identifier, required inputs, and installed capability. Reject unsupported combinations before any mutation.
2. Run `nb env current`, `nb env update <env> --verbose`, and only the relevant `--help` commands. Fetch `plugins/file-manager` Swagger only for optional or version-specific behavior.
3. Load references by task:
   - storage inspection/configuration: [command map](references/command-map.md), plus [storage engines](references/storage-engines.md) only when choosing or configuring an engine;
   - file collection/relation work: [command map](references/command-map.md) and [file modeling](references/file-modeling.md);
   - file-record CRUD: the file-record section of [command map](references/command-map.md);
   - access, lifecycle, deletion, or troubleshooting: [operations and safety](references/operations-and-safety.md) plus the relevant command section.
4. Inspect only the current state needed for the chosen target. Exclude secret-bearing storage fields, resolve identifiers uniquely, and capture safe rollback state before mutation.
5. Execute the selected supported operation: storage CRUD, file collection/relation creation, or file-record inspect/finalize/update/delete. Never delete a file collection or relation field through this skill.
6. If the user asks to upload local bytes, inspect live Swagger/CLI help. When no generated multipart command exists, direct them to the NocoBase UI or report the external/direct-upload requirement; do not treat JSON record creation as upload.
7. Read back every write and verify only the applicable collection template, storage, relation keys, file `storageId`, URL behavior, rules, and physical-deletion expectations.
8. Report API success separately from object-storage reachability or asynchronous external behavior.

# Reference Loading Map

| Reference | Use When | Notes |
|---|---|---|
| [Command map](references/command-map.md) | Selecting exact `nb api resource`, Swagger, or data-modeling commands. | Defines supported CLI boundaries and readback sequences. |
| [Storage engines](references/storage-engines.md) | Choosing or configuring local/cloud/S3 Pro storage. | Includes case-sensitive option names and safe defaults. |
| [File modeling](references/file-modeling.md) | Creating or verifying a file collection/relation, or interpreting file-record semantics. | Enforces the no-attachment-field rule. |
| [Operations and safety](references/operations-and-safety.md) | Changing access/lifecycle settings, deleting, or troubleshooting. | Covers stable URLs, permissions, CORS, default and retention behavior. |

# Safety Gate

High-impact actions:

- deleting a storage engine or file record;
- changing the default storage or a file collection's storage binding;
- changing NocoBase URL/original URL, public access, or S3 Pro signed-URL behavior;
- changing `paranoid`, rename mode `none`, storage path, MIME rules, or size limits;
- creating/updating credential-bearing storage options;
- finalizing a file record for an externally uploaded object.

File collection and relation deletion are outside this skill and must not be inferred from the generic `delete` action.

Secondary confirmation template:

- "Confirm execution: `<action>` on `<exact target>` in `<env>`. Expected impact: `<access, upload, relation, record, and physical-object impact>`. Rollback: `<available or unavailable>`. Type `confirm` to continue."

Rollback guidance:

- For create failures, preserve the storage or file record until its dependencies and physical objects are understood; deletion needs its own fresh confirmation.
- For update mismatch, restore the safe fields captured before mutation. Credential values must be re-supplied as environment placeholders.
- A deleted physical object is not restored by recreating its database record. Use an object-store version/snapshot or backup when available.
- Changing a file collection's storage affects later uploads; existing records retain their own `storageId`. Roll back the collection binding separately from historical records.
- Never claim rollback of an external upload, bucket ACL, CORS rule, CDN cache, or object-store operation performed outside NocoBase.

# Verification Checklist

- Target environment is current, reachable, authenticated, and confirmed.
- File manager is enabled; S3 Pro is enabled before using `s3-compatible`.
- Live storage type, ID, system name, safe fields, and default state are uniquely resolved.
- No plaintext credential appears in argv, logs, temporary files, readback, or output.
- Storage create/update is read back through `nb api resource` with `options` and `settings` excluded.
- Exactly the intended storage is default after a default change.
- File collection readback reports `template: "file"` and the intended storage system name.
- Business collection uses an ordinary `m2o`, `o2m`, or `m2m` relation targeting the file collection; no new `attachment` interface exists.
- Relation direction, foreign key, through table, reverse field, and readable title field match the intended ownership.
- Upload rules use bytes for size and valid MIME patterns; a denied file type/size remains denied.
- File record `storageId`, filename/path semantics, stable URL/original URL choice, and preview behavior match the engine.
- Every write has immediate readback and at least one allowed and one guarded/denied behavior is checked.
- Before deletion, referencing collections and records are inspected and physical-object impact is stated.
- Errors, partial success, external-provider uncertainty, rollback limits, and remaining work are reported separately.

# Minimal Test Scenarios

1. Inspect-only: list safe storage fields and file collections without exposing options or mutating data.
2. Happy path: create a local storage with safe values, create a file collection, add an `o2m`/`m2o` relation pair, and read all objects back.
3. Missing/invalid input: omit storage type, relation ownership, or exact identifier, or request an invalid action-target pair, and verify mutation is blocked.
4. Auth/capability failure: file-manager/S3 Pro, Swagger, or API authorization is unavailable and the skill stops with recovery guidance.
5. High-risk case: request an access-mode/default change or deletion and verify fresh exact-target confirmation is required immediately before execution.

# Output Contract

Final response must include:

- target environment, requested action, exact storage/collection/field/record identifiers;
- engine choice and non-secret configuration summary, when applicable;
- commands executed with secrets redacted or represented only as environment placeholders;
- storage, file collection, relation, and file-record readback as applicable;
- URL/access mode, upload rules, retention, and physical-object impact;
- guarded operations, denied cases, partial success, external-provider uncertainty, and rollback limits;
- defaults and assumptions applied, including any CLI binary-upload capability gap.

# References

- [NocoBase file manager documentation](https://docs.nocobase.com/handbook/file-manager): use when checking current user-facing storage and file collection behavior. [verified: 2026-07-30]
- [NocoBase repository](https://github.com/nocobase/nocobase): use when checking the current open-source implementation and Swagger contract. [verified: 2026-07-30]
- [Command map](references/command-map.md): use for exact supported CLI operations and readback.
- [Storage engines](references/storage-engines.md): use for engine selection and payload fields.
- [File modeling](references/file-modeling.md): use for file collections, relations, and record semantics.
- [Operations and safety](references/operations-and-safety.md): use for access, deletion, retention, and troubleshooting.
