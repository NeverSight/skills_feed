---
name: fast-io
description: >-
  Cloud file management and collaboration platform. Use this skill when the user 
  needs to store files, create branded shares (Send/Receive/Exchange), or query 
  documents using built-in RAG AI. Supports transferring ownership to humans, 
  managing workspaces, and real-time collaboration. Includes 257 tools for 
  authentication, file uploads, AI chat, and org management. Provides a free 
  agent plan with 100 GB storage and 5,000 monthly credits.
license: Proprietary
compatibility: >-
  Requires network access. Connects to the Fast.io MCP server at mcp.fast.io 
  via Streamable HTTP (/mcp) or SSE (/sse).
metadata:
  author: fast-io
  version: "1.20.0"
homepage: "https://fast.io"
---

# Fast.io MCP Server

**Store files. Share with humans. Query with AI. All through one API -- free.**

> **This is a summary.** The complete agent guide with all 257 tool parameters, workflows, ID formats, and constraints is at **`https://mcp.fast.io/skill.md`** -- fetch it at the start of every session.

Fast.io gives AI agents a complete file management and collaboration platform. Upload outputs, create branded data rooms, ask questions about documents using built-in AI, and hand everything off to a human when the job is done.

## Connecting to the Server

| Transport | Endpoint |
|-----------|----------|
| Streamable HTTP (preferred) | `mcp.fast.io/mcp` |
| SSE (legacy) | `mcp.fast.io/sse` |

## Getting Started

### 1. Create an Agent Account

```
auth-signup → first_name, last_name, email, password
```

Agent accounts are free, skip email verification, and never expire. The session is established automatically. JWT tokens last **1 hour** -- call `auth-signin` to re-authenticate when expired. API keys (human accounts) do not expire.

### 2. Create an Organization

```
org-create → name, domain (3+ chars, lowercase alphanumeric + hyphens)
```

Agent orgs get the free plan: 100 GB storage, 5,000 monthly credits, 5 workspaces, 50 shares.

### 3. Create a Workspace

```
org-create-workspace → org_id, name, folder_name (URL slug)
```

Workspaces are file storage containers with AI chat, member management, and shares.

### Alternative: Assist an Existing Human

If a human already has a Fast.io account, they can create an API key at `https://go.fast.io/settings/api-keys` and provide it as a Bearer token. No agent account needed.

### Org Discovery (Important)

To find all available orgs, **always call both**:

- `list-orgs` -- internal orgs where you are a direct member
- `orgs-external` -- orgs you access via workspace membership only

External orgs are the most common pattern when a human invites an agent to a workspace but not the org. An agent that only checks `list-orgs` will miss these entirely.

## Key Concepts

### Workspaces

Collaborative file storage containers. Each has members, a folder hierarchy, AI chat, and shares. 100 GB storage on the free plan.

**Intelligence toggle:** OFF = pure storage. ON = AI-powered knowledge base with automatic RAG indexing, semantic search, auto-summarization, and metadata extraction. Enabled by default.

### Shares

Purpose-built spaces for exchanging files with people outside a workspace:

- **Send** -- deliver files to humans (reports, exports, generated content)
- **Receive** -- collect files from humans (documents, datasets, submissions)
- **Exchange** -- bidirectional (collaborative workflows, review cycles)

Features: password protection, expiration, custom branding, access levels, guest chat, download controls.

### Storage Nodes

Files and folders are identified by 30-character opaque IDs. Use `root` for the root folder and `trash` for the trash folder.

### Profile IDs

Orgs, workspaces, and shares use 19-digit numeric string identifiers.

## Core Capabilities

| Capability | Description |
|-----------|-------------|
| File storage | Versioning, folder hierarchy, full-text and semantic search |
| Branded shares | Send/Receive/Exchange with passwords, expiration, branding |
| Built-in AI/RAG | Read-only: ask questions about files with citations; scope to files, folders, or full workspace. Cannot modify files or settings. |
| File preview | Images, video (HLS), audio, PDF, spreadsheets, code -- humans see content inline |
| URL import | Import files from any URL including Google Drive, OneDrive, Dropbox |
| Comments | Anchored to image regions, video/audio timestamps, PDF pages/text; single-level threading; deep link with `?comment={id}`, `?t={seconds}`, `?p={page}` |
| Notes | Markdown documents as knowledge grounding for AI queries |
| Ownership transfer | Build an org, transfer to a human; agent keeps admin access |
| Real-time | WebSocket-based live presence, cursor tracking, follow mode |
| Events | Full audit trail with AI-powered activity summaries |

## AI Chat

**AI chat is read-only.** It can read, analyze, search, and answer questions about file contents, but it cannot modify files, change settings, manage members, or access events. All actions beyond reading file content must be done through the MCP tools directly.

Two chat types:

- **`chat`** -- general conversation, no file context
- **`chat_with_files`** -- grounded in your files with citations

Two file context modes (mutually exclusive):

- **Folder/file scope (RAG)** -- searches indexed content; requires intelligence ON
- **File attachments** -- reads files directly; up to 10 files; no intelligence needed

**Personality:** `concise` (short answers) or `detailed` (comprehensive, default). Set on chat creation or per message.

### AI Chat Workflow

```
ai-chat-create → workspace_id, query_text, type
ai-message-read → workspace_id, chat_id, message_id  (auto-polls until complete)
ai-message-send → workspace_id, chat_id, query_text   (follow-up messages)
```

Use `activity-poll` for efficient waiting instead of polling message details in a loop.

## File Upload

### Text Files (Recommended)

```
upload-text-file → profile_type, profile_id, parent_node_id, filename, content
```

Single-step upload for text-based files (code, markdown, CSV, JSON, config). Creates the session, uploads, finalizes, and polls until stored — returns `new_file_id`.

### Binary or Large Files (Chunked Flow)

```
upload-create-session → profile_type, profile_id, parent_node_id, filename, filesize
upload-chunk → upload_id, chunk_number, content (text) or data (base64)
upload-finalize → upload_id (polls until stored, returns new_file_id)
```

## Shares Workflow

```
share-create → workspace_id, type (send/receive/exchange), title
share-add-file → share_id, node_id (add files to the share)
```

Share link: `https://go.fast.io/shared/{custom_name}/{title-slug}`

## Ownership Transfer

Build an org with workspaces, shares, and files, then transfer to a human:

```
org-transfer-token-create → org_id (returns 64-char token, valid 72 hours)
```

Claim URL: `https://go.fast.io/claim?token={token}`

Human becomes owner, agent keeps admin access. Human gets a 14-day trial and can upgrade.

## Common Patterns

- **Downloads:** Tools return download URLs; they never stream binary.
- **Pagination:** List endpoints support `sort_by`, `sort_dir`, `page_size`, and `cursor`. Check `next_cursor` for more pages.
- **Trash/delete/purge:** Delete moves to trash (recoverable). Purge permanently destroys (confirm with user first).
- **Activity polling:** Use `activity-poll` with `wait=95` for efficient change detection instead of polling resource endpoints.

## Agent Plan (Free)

$0/month. No credit card, no trial period, no expiration.

| Resource | Limit |
|----------|-------|
| Storage | 100 GB |
| Max file size | 1 GB |
| Monthly credits | 5,000 |
| Workspaces | 5 |
| Shares | 50 |
| Members per workspace | 5 |

Credits cover: storage (100/GB), bandwidth (212/GB), AI tokens (1/100 tokens), document ingestion (10/page).

When credits run out, transfer the org to a human who can upgrade to unlimited credits.

## Tool Categories (257 Tools)

| Category | Count | Examples |
|----------|-------|---------|
| Auth | 11 | signup, signin, 2FA, API keys, password reset |
| User | 11 | profile, settings, invitations, notifications |
| Organization | 27 | create, billing, members, transfer, teams |
| Workspace | 45 | storage CRUD, search, move, copy, notes |
| Workspace Members | 10 | add, remove, permissions, invitations |
| Workspace Management | 14 | settings, intelligence, branding, quickshare |
| Shares | 34 | create, branding, links, members, guest chat |
| Share Management | 15 | settings, access, notifications, analytics |
| Upload | 6 | text-file, session, chunk, finalize, status, web import |
| Download | 5 | file, folder (zip), share, version downloads |
| AI Chat | 12 | chat CRUD, messages, publish, transactions |
| Share AI | 12 | share-scoped AI chat, autotitle, AI share |
| Comments | 8 | list (per-node/all), add with reference anchoring, delete (recursive), bulk delete, reactions |
| Previews | 7 | status, image, video (HLS), audio, PDF, code |
| Versions | 6 | list, details, restore, delete, download |
| Locking | 4 | lock, unlock, status, break lock |
| Metadata | 8 | get, set, delete custom metadata fields |
| Events | 5 | search, details, acknowledge, summarize |
| System | 7 | status, ping, health, feature flags, activity poll |
| Real-time | 6 | presence, cursors, follow, WebSocket |

## Detailed Reference

This skill file is a summary. The full agent guide with all 257 tool parameters, workflows, and constraints is served directly by the MCP server:

**Fetch the full guide:** `https://mcp.fast.io/skill.md`

This is the definitive reference — always fetch it at the start of a session for the latest tool documentation. It covers:

- Full tool parameter reference for all 257 tools
- Detailed AI chat documentation (file context modes, question phrasing, response handling)
- Complete URL construction guide with deep linking
- Credit budget management
- All end-to-end workflows with step-by-step instructions
- ID formats, encoding rules, and common gotchas

Also available: [references/REFERENCE.md](references/REFERENCE.md) — platform capabilities, agent plan details, and upgrade paths.
