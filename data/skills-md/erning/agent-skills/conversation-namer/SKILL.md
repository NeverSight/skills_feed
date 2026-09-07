---
name: conversation-namer
description: >-
  Rename or standardize conversation titles in coding agents using
  MMDD｜TYPE｜Topic. Default to Chinese titles and preview changes before
  renaming; honor existing explicit authorization. Change titles only.
  Project, file, and skill renaming are outside this skill's scope.
---

# Conversation Naming

Rename conversations within the user's selected scope. Use the target coding
agent's actual capabilities; the agent running this skill may differ from the
agent that owns the conversations.

## Scope and capabilities

- Identify the target agent and use the selected conversations, project,
  workspace, or working directory. Resolve "current project" from that agent's
  context and metadata, not an ambiguous display name. If scope cannot be
  determined, ask one short question before preparing the plan.
- Follow the user's filters. Where supported, include pinned conversations and
  exclude archived ones by default; include archived conversations only when
  requested, without unarchiving them. Read all pages needed to cover the
  scope.
- Prefer the target agent's supported management tools, commands, API, or UI.
  Before editing local storage, establish its format and title-update
  mechanism. Do not assume another agent's tools, fields, or storage layout
  apply.
- Collect stable IDs or equally unambiguous locators, current titles, scope,
  original creation times, and enough content or reliable summaries to infer
  topics. Display names and preview row numbers are not reliable locators.
- If only exports or read access are available, explain that limitation before
  showing suggested titles. Do not present a preview as completed renaming.

Change titles only. Preserve project and group names, conversation content,
location, ordering, and pinned or archived state. If the available method has
known side effects on these fields, or cannot be verified to update only
titles, provide a preview and explain the limitation. Do not compensate with
extra move, sort, or state-changing operations.

## Naming rules

Use exactly three fields, separated by the fullwidth vertical bar `｜`
(U+FF5C), with no spaces around the separators:

```text
MMDD｜TYPE｜Topic
```

### Date

- Convert the original creation time to `Asia/Shanghai` and format it as
  `MMDD`, padding month and day with zeroes. For example,
  `2026-09-03T17:30:00Z` gives `0904`.
- `createdAt` here means original creation time, not a required field name.
  Accept `created_at` or a creation record only when its meaning is
  equivalent. Establish timestamp units and source timezone; do not guess for
  ambiguous local times.
- Never substitute `updatedAt`, recent activity, export time, file timestamps,
  today's date, or a date already present in the title. Keep the existing
  title when original creation time cannot be established.

### Type and language

Choose the type from the conversation's main purpose or substantive outcome,
not merely its existing title or final incidental action. Committing a bug fix
at the end does not make that conversation a release task.

| Chinese label (default) | English code | Purpose |
| --- | --- | --- |
| 功能 | FEA | Add functionality or capabilities |
| 设计 | DES | Design behavior, architecture, interfaces, or implementation plans |
| 修复 | FIX | Diagnose or fix defects |
| 优化 | OPT | Improve behavior, performance, or usability |
| 发布 | REL | Prepare, publish, or deliver a release or change |
| 探索 | EXP | Explore approaches, prototype, or test feasibility |
| 文档 | DOC | Write or maintain documentation |
| 研究 | RES | Investigate questions through sources, evidence, or comparisons |

Default to Chinese type labels and Simplified Chinese topics. Use English
codes only when explicitly requested for types or whole titles; use English
topics only when explicitly requested for topics or whole titles. A request
for one field's language does not change the other field. The language of
these instructions, the user request, or the existing conversation does not
change these defaults. Keep the type-label language consistent within each
batch of new titles; individual conversations may use different types.

### Topic

- Use a short, specific phrase suitable for a sidebar or terminal list. Read
  more content when summaries are insufficient. Keep the existing title if the
  topic or type remains uncertain.
- Avoid repeating project or group names and vague topics such as "discussion"
  or "miscellaneous fixes". Preserve useful technical names and identifiers.
- Do not put another `｜` or a line break inside the topic.
- Leave titles unchanged when their date, type, topic, and language already
  meet the requested rules. Replace an existing prefix instead of stacking
  prefixes.

Examples assume creation metadata produces the dates shown and conversation
content supports the topics; do not infer those facts from the old titles
alone.

Default Chinese titles:

| Before | After |
| --- | --- |
| Improve batch text display | 0903｜优化｜批次文字显示 |
| Design alignment checks | 0901｜设计｜界面对齐检查 |
| Prepare v1.0 release | 0813｜发布｜准备 v1.0 发布 |

When the user explicitly requests English titles:

| Before | After |
| --- | --- |
| 优化批次文字显示 | 0903｜OPT｜Batch text display |
| 新功能讨论 | 0901｜DES｜UI alignment check |

## Preview and authorization

By default, show the proposed changes and wait for confirmation before
writing. Use a `Before` / `After` table in retrieval order, preserving and
escaping the actual titles. Add IDs, status columns, or brief notes when
needed to distinguish names or explain skips. Show unchanged titles for
skipped or compliant entries. Retain each row's stable ID, scope, original
title, and proposed title.

- Execute an already approved plan without asking for the same confirmation.
- If the user explicitly skips preview and authorizes applying these rules to
  a defined scope, proceed within that authorization. A generic request to
  standardize titles still follows the default preview process.
- An instruction to apply an exact final title to a specified conversation
  authorizes that change. Directional feedback alone requires an updated plan
  and confirmation; newly requested scope also needs authorization.
- Report an empty scope directly. Explain missing access or ask for unresolved
  scope information instead of inventing preview rows.

## Apply and verify

Update only authorized entries whose titles need changing. Before each write,
recheck the retained stable ID, current title, and scope. If the title or
scope has changed since preparation, skip that entry and report the conflict.
When approval covered only the listed entries, newly discovered conversations
require separate authorization.

Use the established update mechanism. After a timeout or uncertain response,
read the current title before retrying; if it already matches, do not write it
again. Verify the final title by rereading or using the update response's
final value. Stop retrying when success cannot be established or further
action would exceed the authorized scope.

Report renamed, unchanged, skipped, and failed entries with brief reasons
where needed. Do not claim unverified success or append unrelated suggestions,
follow-up invitations, or project-management actions.
