---
name: linear-weekly-report
description: Fetches a person's Linear issues via Linear MCP and generates a weekly report in English, Notion /quote format. Use when the user asks for a Linear weekly report, 周报, or to generate a status update for someone (by email, name, or "me").
---

# Linear Weekly Report Generator

Queries a specified user's Linear issues via Linear MCP and generates a weekly report in the "Next Week's Focus / Blockers / Last Week's Highlights" structure, formatted for direct paste into Notion `/quote` blocks.

## Prerequisites

- **Linear MCP** configured (server: `user-Linear`) with access to `get_user` and `list_issues` tools.
- `list_issues` `assignee` parameter supports: User ID, name, email, or `"me"`.
- `updatedAt` supports ISO-8601 duration format, e.g., `-P7D` (past 7 days).

## Workflow

### 1. Parse User Identifier

Extract the target person from user input, supporting:

- Email: `panyanjie@mirrorworld.fun`
- Name: `panyanjie`
- `me`: Currently logged-in Linear user

If needed, call `get_user` first (with `query` as one of the above) to retrieve `displayName` for the title.

### 2. Fetch Issues

Call `list_issues` (Linear MCP):

| Parameter  | Value       | Description                                  |
|------------|-------------|----------------------------------------------|
| `assignee` | User identifier | Email, name, or `"me"`                   |
| `updatedAt`| `-P7D`      | Issues updated in the last 7 days            |
| `orderBy`  | `updatedAt` | Sort by update time                          |
| `limit`    | `50`        | Optional, defaults to 50                     |

If `assignee` by email/name returns nothing, try using the `id` returned by `get_user`.

### 3. Categorize & Summarize

- **Last Week's Highlights**: Issues with status `Done`, `Done (Production)`, etc. Extract title or brief description.
- **Next Week's Focus**: Issues with status `In Progress`, `Todo`, `In Testing (Staging)`, etc. Extract title; merge similar items (e.g., multiple Mobile subtasks).
- **Blockers / Dependencies**: Linear has no direct field for this. Default to `None.`; only include if user explicitly mentions blockers.

#### Brevity Guidelines

**IMPORTANT: Keep reports concise. Control item counts in each section:**

- **Last Week's Highlights**: Max **3-5** key achievements
  - Merge similar bug fixes into 1 item (e.g., "Fixed 8 UI bugs including tooltip, styling, and layout issues")
  - Prioritize: Feature launches, major bug fixes, architectural improvements
  - Omit: Minor styling tweaks, repetitive fixes

- **Next Week's Focus**: Max **3-5** main tasks
  - Merge subtasks into parent task (e.g., instead of "1. Login flow, 2. Referral page...", use "Trading Tournament features (login, referral, leaderboard, etc.)")
  - Prioritize: Major features, high-priority tasks, business-valuable work

Keep each item **brief** (1 line max). Remove prefixes like `[Mobile]`, `ENG-xxxx`, retaining only semantic clarity. **Use English for item text**: Translate or summarize Chinese issue titles into English. **No issue IDs**: Do not include `(ENG-xxxx)`, `(ACADEMY-xx)`, or any Linear identifier in output.

### 4. Role & Title

- Use `displayName` or common name (from `get_user`) after `@`.
- Role (e.g., `Front-end`, `Backend`) is not provided by Linear. Leave as `@name -` or fill based on known info/user input.

## Output Format: Notion /quote

Use `>` + space quote block syntax. Section headers are first-level bullets (start with `-`), specific items are second-level bullets (start with `  -`, 2-space indent), making it easy to paste into Notion and convert to nested bulleted lists.

```
> ▶️ 👤 @{displayName} - {Role}
> 
> - ⏭ Next Week's Focus (Deliverables):
>   - {item 1}
>   - {item 2}
> 
> - 🚧 Blockers / Dependencies:
>   - None.
> 
> - ✅ Last Week's Highlights:
>   - {item 1}
>   - {item 2}
```

- **Output language: English.** Section headers, item text, and "None." must be in English. If the source issue title is in Chinese, translate or briefly summarize in English. Use Chinese only when the user explicitly asks for 中文.
- **No issue IDs.** Do not append `(ENG-xxxx)`, `(ACADEMY-xx)`, or any Linear identifier to items.
- **Use `-` for section headers and `  -` (2-space indent) for items**, so Notion can recognize them as nested list items for easy conversion to bulleted lists.

## Edge Cases & Empty Results

- **`list_issues` returns 0 items**: Reply with e.g. "No issues assigned and updated in the last 7 days", and still output a template with empty Blockers/Highlights and Next Focus showing "—" or "TBD" (**in English**).
- **`get_user` finds no user**: Reply with e.g. "User not found in Linear. Please check email/name or try `me`." (**in English**).

## Output Requirements

**CRITICAL: The weekly report MUST be directly copyable from the chat window.**

1. **Always display the complete report** in a markdown code block (using triple backticks) so users can easily copy it.
2. **Format**: Display the report in a code block labeled as `markdown` or `text` for easy copying.
3. **No clipboard commands**: Do NOT use `pbcopy`, `xclip`, or similar clipboard commands. These often fail and are unreliable.
4. **Instructions**: After displaying the report, remind users: "Copy the content above and paste into Notion. Type `>` + space in Notion to create a quote block, paste the content, then press `Cmd + Shift + 8` to convert to bulleted list."

### Example Output Format

Display the report like this:

````markdown
Here's your weekly report:

```
> ▶️ 👤 @jack - Front-end
> 
> - ⏭ Next Week's Focus (Deliverables):
>   - Trading Tournament features
>   - Bug fixes
> 
> - 🚧 Blockers / Dependencies:
>   - None.
> 
> - ✅ Last Week's Highlights:
>   - Shipped assets feature
```

**How to use in Notion:**
1. Copy the content above
2. Paste the content in notion
````
