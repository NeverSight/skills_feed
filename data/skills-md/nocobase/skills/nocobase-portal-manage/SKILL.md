---
name: nocobase-portal-manage
description: "NocoBase 2 only; never use in a NocoBase 3 project. PRIMARY ENTRY. Default dispatcher for every NocoBase UI authoring request, including pages, menus, blocks, fields, actions, layouts, reactions, KPI interfaces, dashboards, and charts, even when the user does not mention a Portal. Resolve an enabled Portal from structured `nb portal list -j` output before loading any downstream UI implementation skill: exact `name` when specified; otherwise zero stops, exactly one is automatic, and multiple Portals require explicit selection even when one has `isDefault: true`; show the default marker as informational only. Read the type only from `portalType`; explicitly invoke `nocobase-ui-builder` only for a resolved no-code Portal and require `nocobase-ai-builder` for AI Portal source development. Also use direct `nb portal` commands for explicit Portal lifecycle, source storage, sync, deployment, diagnosis, and destroy tasks."
argument-hint: "[action: build|list|info|create|config|pull|push|deploy|dev|destroy|diagnose] [portal?] [env?: name]"
allowed-tools: Bash, Read, Write, Grep, Glob
owner: platform-tools
version: 1.0.0
last-reviewed: 2026-07-28
risk-level: medium
---

# Goal

Dispatch all ordinary NocoBase UI authoring to one explicitly resolved Portal and manage Portal workspaces, preserving env selection, source storage configuration, and clear readback after changes.

# Scope

- Inspect Portal inventory and details.
- Start every ordinary NocoBase page, menu, block, field, action, layout, and reaction request by resolving the target env and Portal.
- Use the `nocobase-ui-builder` skill to build no-code Portal UI.
- Use the `nocobase-ai-builder` skill for AI Portal source development after locating or pulling the corresponding Portal source directory.
- Create Portal workspaces from templates.
- Configure Portal source storage, including Git repo, branch, and path.
- Pull and push Portal source between local workspace, NocoBase storage, and Git source storage.
- Deploy a Portal or start Portal development mode.
- Diagnose common Portal CLI and Git source storage failures.
- Destroy a Portal only when explicitly requested and confirmed.

# Non-Goals

- Do not directly author no-code Modern UI pages, blocks, menus, reactions, or page content inside this skill; use the `nocobase-ui-builder` skill while preserving Portal env and workspace context.
- Do not implement AI Portal source changes directly inside this skill; resolve or pull the source directory and hand the same request to `nocobase-ai-builder`.
- Do not manage app runtime lifecycle, CLI self-update, env setup, or installed skills update; hand off to `nocobase-env-manage`.
- Do not manage backup restore or migration publishing; hand off to `nocobase-publish-manage`.
- Do not infer Portal type from user wording, templates, source layout, current directory, or local files; use the selected record's `portalType` only.
- Once an AI Portal is selected for an ordinary UI build, that build request authorizes implementing and testing the change in its source project; do not ask for separate source-code authorization.
- Do not mutate databases or NocoBase internals outside the public `nb portal` command surface.
- Do not run wrapper scripts, Docker fallback commands, or direct SQL as a substitute for `nb portal`.
- Do not treat the absence of `nb portal` as permission to emulate Portal lifecycle, source storage, sync, deploy, or destroy operations through private APIs.

# Hard Rules

- Before executing any `nb portal ...` command, confirm the installed CLI exposes the Portal command surface with `nb portal --help`, `nb --help`, or an equivalent local command-help check.
- Use direct `nb portal` commands for Portal lifecycle, source storage, sync, deploy, and diagnosis operations when that command surface exists.
- If `nb portal` is unavailable, report lifecycle/source/deploy/destroy tasks as blocked by the installed CLI version and hand CLI update/env work to `nocobase-env-manage`; do not switch transports.
- Treat this skill as the entry point for every ordinary NocoBase UI authoring request, even if it does not contain the word "Portal".
- Before any ordinary UI authoring write, inspect structured Portal inventory with `nb portal list -j`; count only records where `enabled === true`.
- Treat `isDefault` / default marker from `nb portal list -j` as informational readback only. Include it when listing choices or reporting readback, but never use it to select among multiple enabled Portals.
- When the user specifies a Portal, match its CLI `name` exactly across structured records. Continue only when exactly one record matches and it has `enabled === true`; a missing, disabled, or non-unique match must stop without substitution.
- When the user does not specify a Portal: zero enabled Portals must stop the UI build without automatically creating one; exactly one is selected automatically; multiple Portals must be listed by `name` and `portalType` for explicit user selection.
- When multiple enabled Portals exist, do not auto-select the record with `isDefault === true`; list it with a default marker and ask for the target Portal explicitly.
- Do not infer a target among multiple Portals from cwd, active files, a nearby or recent `portal.config.json`, `localPath`, sync state, title similarity, or Portal type preference.
- Determine the selected Portal's implementation path only from its `portalType`; do not infer type from the request, template, source tree, or local workspace.
- Use `portal.config.json`, `localPath`, and other local workspace information only after an AI Portal is selected, and only to locate its source project before invoking `nocobase-ai-builder`.
- When the selected record has `portalType === "ai"`, loading and executing `nocobase-ai-builder` is mandatory. If `nb portal list -j` or `nb portal info <portal> -j` reports an empty `developmentPath` / `localPath` / local source path, run `nb portal pull <portal>` first, then read back the Portal info/list again and enter the pulled development directory. Pass the resolved Portal name, environment, local source path, and original user request; do not substitute an ad hoc source-edit workflow.
- Do not use source storage configuration as an AI Portal working directory. `sourceStorage`, `git_repo`, `git_branch`, `git_path`, `--git-path`, repository subdirectories, and deployment/storage paths are remote storage configuration for pull/push/deploy; they are not the local development directory. Source edits happen only in the selected Portal's existing `developmentPath` / `localPath` or in the local directory returned after `nb portal pull <portal>` readback.
- Treat `nb portal` as runtime-unavailable when the command is unknown or when `nb portal list -j` returns the explicit endpoint-absence signatures `404` / `Not Found`. For ordinary UI authoring only, this enters the legacy capability probe below; Portal lifecycle/source/deploy operations remain blocked.
- When Portal inventory is runtime-unavailable, do not use `flow-surfaces list-navigation-targets` as Portal inventory or infer no-code versus AI. Run `nb api flow-surfaces list-navigation-targets -j` only to inspect `capabilities.multiPortal`: `false` enables the legacy UI Builder lane and `true` stops.
- Older pre-Portal runtimes may not expose `list-navigation-targets`. When that action is explicitly unknown or returns `404` / `Not Found`, and the user did not name a Portal, allow the legacy UI Builder lane only after both checks succeed: `nb api flow-surfaces --help` exposes `apply-blueprint` and `list-templates`, and `nb api flow-surfaces list-templates --body '{}' -j` returns a structured success response. This is the verified legacy Flow Surfaces signature. Auth errors, `5xx`, malformed output, a missing core action, or a failed read probe must stop; never reinterpret them as legacy evidence.
- Use the current configured CLI env unless the user provides an explicit env.
- When passing an explicit env that may differ from the current env, include `--yes` only when the user requested non-interactive execution or explicitly confirmed the target env.
- Before `destroy`, require explicit confirmation from the user.
- Before `pull --force`, `create --force`, or any operation that overwrites local Portal source, require explicit confirmation.
- For one-Portal-per-repository Git workflows, prefer `--git-path .`.
- Use subdirectory `--git-path` values only when the user wants multiple Portals or other content in the same Git repository.
- Never enter or edit a `--git-path` / `git_path` value as if it were the local Portal project. It is a repository-relative storage path, not the pulled development directory.
- If an existing `portal.config.json` or remote Portal record already has a configured Git path, do not assume the current CLI default rewrites it; change it explicitly with `nb portal config <portal> --git-path .` when requested.
- For `push`, use the user's requested commit message when provided; otherwise let CLI defaults apply.
- Do not automatically run `push` or `deploy` after source or UI changes. Execute `push` only when the user emphasizes pushing/syncing/committing Portal source. Execute `deploy` only when the user emphasizes deployment/publishing/releasing the Portal. A deploy request does not imply a prior push.
- Treat `push` and `deploy` as independent actions when both are explicitly requested. A failed `push` must be reported, but it must not automatically block an explicitly requested `deploy` unless the user said deployment is conditional on push success, such as "push successfully then deploy", "only deploy after push succeeds", or equivalent wording.
- On command failure, report the relevant CLI output and the next concrete recovery command instead of switching transports.

# Supported Tasks

- `list`
- `info`
- `create`
- `config`
- `pull`
- `push`
- `deploy`
- `dev`
- `destroy`
- `diagnose`
- `build`

# Input Contract

| Input | Required | Default | Validation | Clarification Question |
|---|---|---|---|---|
| `action` | yes | inferred | one of `build/list/info/create/config/pull/push/deploy/dev/destroy/diagnose` | "Which Portal action should I run?" |
| `portal` | lifecycle actions except `list`; optional for `build` | the only enabled Portal for `build` | exact CLI `name` | "Which Portal should I target?" |
| `runtime_env_name` | no | current env | configured CLI env name | "Which env should I target?" |
| `template` | create only | CLI default | npm package, local path, or `file://` URL | "Which Portal template should I use?" |
| `title` | create only | generated from slug | non-empty string | "What display title should this Portal use?" |
| `source_storage` | create/config only | `nocobase` for create, existing config for config | `nocobase` or `git` | "Should source storage be `nocobase` or `git`?" |
| `git_repo` | git create/config | none | full Git remote URL | "Which Git remote URL should store the Portal source?" |
| `git_branch` | no | `main` | non-empty branch name | "Which Git branch should be used?" |
| `git_path` | no | `.` | relative path inside repository, no `..` | "Which repository path should store the Portal source?" |
| `message` | push only | CLI default | non-empty commit message | "What commit message should I use?" |
| `force` | destructive/overwrite actions | `false` | requires explicit confirmation | "Confirm overwrite/destruction before I continue." |

Rules:

- If required inputs for a mutating action are missing, stop and ask one concise clarification question.
- If the user says "you decide", use the documented defaults and direct `nb portal` behavior.
- Do not ask for optional inputs that have safe CLI defaults unless the choice materially affects data, source, or deployment outcome.

# Mandatory Clarification Gate

- Max clarification rounds: `2`.
- Max questions per round: `3`.
- Before mutation, resolve `action`, `portal`, env target when explicit, and any required Git fields.
- Before `destroy`, ask for secondary confirmation.
- Before `pull --force` or `create --force`, ask for secondary confirmation.
- Before configuring Git storage without `git_repo`, ask for the Git remote URL.
- If a Git source storage failure mentions an empty remote, missing branch, or missing configured Git path, diagnose from [Git Source Storage](references/git-source-storage.md) before recommending manual Git commands.

# Workflow

## Ordinary UI Build Workflow

Use this path for every ordinary NocoBase page, menu, block, field, action, layout, or reaction request, including requests that never say "Portal".

1. Inspect the current env with `nb env current` and `nb env info`.
2. Detect Portal CLI support with `nb portal --help` or equivalent command-help output.
3. If `nb portal` is unavailable:
   - For create/config/pull/push/deploy/dev/destroy/list/info requests, stop and report the missing CLI capability; recommend `nocobase-env-manage` for CLI/runtime upgrade or environment diagnosis.
   - For ordinary UI authoring, call `nb api flow-surfaces list-navigation-targets -j` only as a capability check. If `capabilities.multiPortal` is explicitly `false`, use the `nocobase-ui-builder` legacy lane. If it is `true`, stop. If the action is explicitly unknown or returns `404` / `Not Found`, use the verified legacy Flow Surfaces probe defined in Hard Rules; continue only when that full probe succeeds. Other missing, unclear, or failed results stop with CLI/runtime guidance.
   - Never treat navigation targets as no-code/AI Portal inventory.
4. Inspect structured Portal inventory with `nb portal list -j` when the command surface is available, and retain only records where `enabled === true`. If this inventory call returns explicit endpoint absence (`404` / `Not Found`), treat Portal inventory as runtime-unavailable and apply step 3 for ordinary UI authoring; do not do so for auth errors, `5xx`, or malformed output.
5. Resolve the target Portal:
   - If the user supplied a Portal name, require exactly one record whose `name` is an exact match and whose `enabled` value is `true`. A missing, disabled, or non-unique match stops the build.
   - If no Portal was supplied and zero enabled Portals exist, stop and tell the user to explicitly create a Portal first. Do not create one automatically.
   - If no Portal was supplied and exactly one enabled Portal exists, select it automatically.
   - If no Portal was supplied and multiple Portals exist, list each `name`, `portalType`, and default status when present, ask for an explicit selection, and do no UI write. A single `isDefault === true` record does not break the tie.
   - Do not infer the target from cwd, active files, `portal.config.json`, `localPath`, sync state, title similarity, or type preference.
6. Read the selected record's `portalType`. It is the only source for no-code versus AI routing.
7. If it is a no-code Portal, use the `nocobase-ui-builder` skill for page, menu, block, field, action, and permission authoring.
8. If it is an AI Portal, use `nb portal info <portal> -j`, the selected list record's `developmentPath`, `localPath`, `portal.config.json`, or local workspace state only to locate the already selected Portal's local source project. If that local development path is empty or missing, run `nb portal pull <portal>` first, then read back with `nb portal info <portal> -j` or `nb portal list -j` and enter the pulled development directory. Ignore `sourceStorage`, `git_repo`, `git_branch`, `git_path`, `--git-path`, and deployment/storage paths as edit locations; those only describe where the Portal source is stored for pull/push/deploy. Then load and execute `nocobase-ai-builder` with the resolved Portal name, environment, source path, and original request. The original request authorizes implementation and verification; do not ask for separate code-edit authorization.
9. If `portalType` is absent or unsupported, stop instead of guessing.
10. After UI changes, do not automatically run `nb portal push` or `nb portal deploy`. Use `nb portal dev` only when needed for local verification or when requested. Run `push` only for explicit source-push intent, and run `deploy` only for explicit deployment intent.

Explicit `action=create` requests continue through the Portal Command Workflow. The zero-Portal stop above applies only to ordinary UI builds and must not suppress an explicit lifecycle request to create a Portal.

## Portal Command Workflow

1. Infer the Portal action and target env from the user's request.
2. Read [Runtime Contract](references/runtime-contract.md) before executing an unfamiliar command shape or when building a command with flags.
3. For Git source storage setup or failures, read [Git Source Storage](references/git-source-storage.md).
4. Check whether `nb portal` is available before trying the action.
5. If `nb portal` is unavailable, stop without fallback mutation and report the missing command surface plus the next `nocobase-env-manage` handoff.
6. Ask only for missing required inputs or required confirmations.
7. Execute the direct `nb portal` command.
8. For write actions except `dev`, read back with `nb portal info <portal>` when available; otherwise use `nb portal list -j`.
9. For `push`, report whether source changes were committed or the CLI reported no changes.
10. For combined `push` + `deploy` requests, execute the requested actions independently in order. If `push` fails, record the failure and continue to the requested `deploy` after any required deploy confirmation, unless the user made deploy conditional on push success. If the request only says deploy, do not insert a push step.
11. For failures, return the failed command, key CLI output, likely cause, and one next command.

# Action Routing

- Use `list` for "show portals", "有哪些 portal", "portal 列表".
- Use `info` for "portal details", "查看 portal 配置", "当前 git 配置".
- Use `create` for "创建 portal", "new Portal workspace", "from template".
- Use `config` for "配置 portal git", "改 source storage", "set git repo/branch/path".
- Use `pull` for "拉取 portal 源码", "sync remote to local".
- Use `push` only for explicit source-push intent such as "推送 portal 源码", "push source", "portal push", "commit source to Git", or "sync Portal source". Do not infer push from a generic build, finish, publish, deploy, or release request.
- Use `deploy` only for explicit deployment intent such as "部署 portal", "deploy", "publish online", or "release Portal". Do not run `push` first unless the user also explicitly asks to push source.
- Use `dev` for "启动 portal dev", "local portal development".
- Use `destroy` only for explicit delete/destroy intent.
- Use `diagnose` when the user provides an error log or asks why a Portal command failed.
- Use `build` for every ordinary NocoBase page, menu, block, field, action, layout, or reaction request, whether or not it mentions a Portal.
- When a UI request omits the Portal name, inspect structured env inventory first: zero stops, exactly one is automatic, and multiple require explicit selection even when one is marked default.
- For no-code Portal build requests, use the `nocobase-ui-builder` skill for UI authoring.
- For AI Portal build requests, locate the Portal local source directory; if the CLI reports no development path yet, run `nb portal pull <portal>` first, then execute `nocobase-ai-builder` in the pulled directory. Do not develop inside source storage paths such as `git_path` / `--git-path`.

# Reference Loading Map

| Reference | Use When | Notes |
|---|---|---|
| [Runtime Contract](references/runtime-contract.md) | Building or checking direct `nb portal` command invocations | Contains command map, env flag placement, and readback rules. |
| [Git Source Storage](references/git-source-storage.md) | Configuring Git source storage or diagnosing Git push/pull failures | Covers root path default, empty repositories, and branch/path recovery. |
| [Test Playbook](references/test-playbook.md) | Validating the skill or planning capability checks | Read before adding tests or forward-testing the skill. |

# Safety Gate

High-impact actions:

- `nb portal destroy`
- `nb portal pull --force`
- `nb portal create --force`
- configuring Git source storage for a shared or production Portal
- `nb portal deploy` to a production-like env

Secondary confirmation templates:

- Destroy: `Confirm execution: destroy Portal <portal> in env <env>. Expected impact: Portal record/workspace may be removed. Reply confirm to continue.`
- Overwrite local source: `Confirm execution: overwrite local Portal source for <portal> in env <env>. Reply confirm to continue.`
- Production deploy: `Confirm execution: deploy Portal <portal> to env <env>. Reply confirm to continue.`

Rollback guidance:

- Failed `config`: inspect with `nb portal info <portal>` and re-run `nb portal config` with the previous values if known.
- Failed `pull --force`: local overwritten files may require restoration from Git or backup; do not invent a rollback.
- Failed `push`: inspect the Git error and retry only after branch, auth, repo, or path issue is corrected.
- Failed `deploy`: report CLI output and run `nb portal info <portal>` or deployment-specific readback if available.

# Verification Checklist

- Action and Portal target are resolved when the command surface supports the requested operation.
- Direct `nb portal` command is used when `nb portal` is available.
- `nb portal` availability is checked before Portal command execution.
- Explicit env handling is preserved.
- Required confirmations are collected before destructive or overwrite actions.
- Git source storage commands include a full remote URL when required.
- Default Git path uses `.` for one-Portal-per-repository workflows.
- Write actions have readback with `nb portal info` or `nb portal list -j`.
- Ordinary UI build requests use `nb portal list -j`, filter `enabled === true`, preserve `isDefault` for display/readback only, and resolve exactly one Portal before choosing an implementation path.
- Explicit Portal names match `name` exactly; multiple Portals never use local context for selection.
- Multiple Portals never use default status for selection; default status is shown to the user as a marker only.
- Portal type comes only from `portalType`.
- No-code Portal UI authoring uses the `nocobase-ui-builder` skill.
- AI Portal UI authoring uses `nocobase-ai-builder` in the corresponding Portal local source directory, pulling it with `nb portal pull <portal>` first when `developmentPath` / `localPath` is empty, and never treats source storage paths such as `git_path` / `--git-path` as edit directories.
- `push` and `deploy` are never auto-added after UI/source edits. A source-push request executes only push; a deployment request executes only deploy; an explicit combined request executes both independently.
- Combined `push` + `deploy` requests preserve both requested actions independently; `push` failure is reported but does not block `deploy` unless deploy was explicitly conditional on push success.
- Failure output includes the failed command and relevant CLI lines.
- Final answer reports commands, result, readback status, assumptions, and remaining risks.

# Minimal Test Scenarios

1. `list` uses `nb portal list -j` and does not ask for a Portal name.
2. `config` with Git storage requires `git_repo` and defaults `git_path` to `.`.
3. `push` with an empty Git repository reports branch creation support or actionable recovery.
4. A plain deployment request executes `deploy` only and does not insert a push step.
5. A plain source-push request executes `push` only and does not deploy.
6. Combined `push` + `deploy` continues to deploy after a push failure when the user requested both actions independently; it stops before deploy only when the user made deploy conditional on push success.
7. `pull --force` blocks until explicit confirmation.
8. `destroy` blocks until explicit confirmation.
9. Zero enabled Portals stop ordinary UI authoring without implicit creation.
10. Exactly one no-code Portal uses the `nocobase-ui-builder` skill.
11. Exactly one AI Portal resolves its local source directory, or runs `nb portal pull <portal>` first when no development path exists, then invokes `nocobase-ai-builder` with the original request.
12. Multiple Portals list `name`, `portalType`, and default status when available, and require explicit selection without cwd, default-marker, or local-file inference.
13. Explicit missing, disabled, or non-unique Portal names stop without substitution.
14. App start/update request is handed off to `nocobase-env-manage`.
15. Missing `nb portal` blocks lifecycle/source/deploy actions with a clear CLI capability report and does not use private API fallbacks.
16. Missing Portal runtime support permits the legacy UI Builder lane when `list-navigation-targets` explicitly returns `capabilities.multiPortal: false`, or when the action is explicitly absent and the verified legacy Flow Surfaces signature succeeds. `true`, auth errors, `5xx`, malformed output, or a failed core probe stop.

# Output Contract

For direct Portal command tasks, always return:

- `request`
- `capability`
- `commands`
- `env`
- `portal`
- `default`
- `result`
- `readback`
- `assumptions`
- `next_steps`

For natural UI build tasks, return:

- `request`
- `env`
- `portal`
- `default`
- `capability`
- `portal_type`
- `implementation_path`
- `build_summary`
- `verification`
- `next_steps`

# References

- [Runtime Contract](references/runtime-contract.md)
- [Git Source Storage](references/git-source-storage.md)
- [Test Playbook](references/test-playbook.md)
- [NocoBase Portal CLI docs](https://docs.nocobase.com/api/cli/portal): official command reference. [verified: 2026-07-28]
