---
name: tlyboy-starter
description: "Helps initialize and scaffold new projects based on Guany's personal preferences and starter templates. Use when the user asks to initialize, scaffold, or set up a new project, create a project from template, or start a new app. Actions: init, scaffold, setup, create, generate, start, new. Topics: starter, boilerplate, template, project setup, degit."
---

# Starter

Initialize new projects using Guany's starter templates via `degit`.

## Starter Templates

Create a project from a starter template:

```bash
npx degit tlyboy/<template> <project-name>
```

### Frontend

| Template | Command                                         |
| -------- | ----------------------------------------------- |
| Vue      | `npx degit tlyboy/vue-starter <project-name>`   |
| React    | `npx degit tlyboy/react-starter <project-name>` |
| Nuxt     | `npx degit tlyboy/nuxt-starter <project-name>`  |
| Next.js  | `npx degit tlyboy/next-starter <project-name>`  |

### UI Library

| Template            | Command                                                     |
| ------------------- | ----------------------------------------------------------- |
| shadcn + Vue        | `npx degit tlyboy/shadcn-vue-starter <project-name>`        |
| shadcn + React      | `npx degit tlyboy/shadcn-react-starter <project-name>`      |
| shadcn + Nuxt       | `npx degit tlyboy/shadcn-nuxt-starter <project-name>`       |
| shadcn + Next.js    | `npx degit tlyboy/shadcn-next-starter <project-name>`       |
| Element Plus + Vue  | `npx degit tlyboy/element-plus-vue-starter <project-name>`  |
| Element Plus + Nuxt | `npx degit tlyboy/element-plus-nuxt-starter <project-name>` |
| Vant + Vue          | `npx degit tlyboy/vant-vue-starter <project-name>`          |

### Desktop (Tauri)

| Template               | Command                                                      |
| ---------------------- | ------------------------------------------------------------ |
| Tauri + Vue            | `npx degit tlyboy/tauri-vue-starter <project-name>`          |
| Tauri + React          | `npx degit tlyboy/tauri-react-starter <project-name>`        |
| Tauri + shadcn + React | `npx degit tlyboy/tauri-shadcn-react-starter <project-name>` |

### Backend & Server

| Template | Command                                         |
| -------- | ----------------------------------------------- |
| Nitro    | `npx degit tlyboy/nitro-starter <project-name>` |
| Bun      | `npx degit tlyboy/bun-starter <project-name>`   |

### MCP (Model Context Protocol)

| Template   | Command                                              |
| ---------- | ---------------------------------------------------- |
| MCP Server | `npx degit tlyboy/mcp-server-starter <project-name>` |
| MCP Client | `npx degit tlyboy/mcp-client-starter <project-name>` |

### Other

| Template                            | Command                                                           |
| ----------------------------------- | ----------------------------------------------------------------- |
| VitePress                           | `npx degit tlyboy/vitepress-starter <project-name>`               |
| Slidev                              | `npx degit tlyboy/slidev-starter <project-name>`                  |
| uni-app                             | `npx degit tlyboy/uni-starter <project-name>`                     |
| Docker Compose (Caddy)              | `npx degit tlyboy/compose-starter/caddy <project-name>`           |
| Docker Compose (Caddy + Cloudflare) | `npx degit tlyboy/compose-starter/caddy-cf <project-name>`        |
| Docker Compose (Caddy + Aliyun)     | `npx degit tlyboy/compose-starter/caddy-ali <project-name>`       |
| Docker Compose (MySQL)              | `npx degit tlyboy/compose-starter/mysql <project-name>`           |
| Docker Compose (Redis)              | `npx degit tlyboy/compose-starter/redis <project-name>`           |
| Docker Compose (Nginx)              | `npx degit tlyboy/compose-starter/nginx <project-name>`           |
| Docker Compose (n8n)                | `npx degit tlyboy/compose-starter/n8n <project-name>`             |
| Docker Compose (Open WebUI)         | `npx degit tlyboy/compose-starter/open-webui <project-name>`      |
| Docker Compose (Open WebUI + CUDA)  | `npx degit tlyboy/compose-starter/open-webui-cuda <project-name>` |
| Docker Compose (Verdaccio)          | `npx degit tlyboy/compose-starter/verdaccio <project-name>`       |

## Instructions

1. When the user asks to create or initialize a project, determine the project type (or ask).
2. Suggest the matching `npx degit tlyboy/<template> <project-name>` command.
3. After degit, run `ni` to install dependencies.
4. If the user needs a custom setup that doesn't match any template, use the config references in `templates/` (`.editorconfig`, `.prettierrc`) as a baseline.

## Config References

The `templates/` directory contains baseline config files and project scaffolding reflecting Guany's preferences:

- **`.editorconfig`** - 2-space indent, LF, UTF-8, trim trailing whitespace, insert final newline
- **`.prettierrc`** - No semicolons, single quotes
- **`.vscode/settings.json`** - Prettier as default formatter, format on save
- **`.vscode/extensions.json`** - Recommended extensions (EditorConfig, Prettier)
- **`LICENSE`** - MIT License, `{{year}}` replaced with current year
- **`CODE_OF_CONDUCT.md`** - Contributor Covenant v2.1
- **`README.md`** - Project README template (English) with emoji prefix, uses pnpm commands
- **`README.zh-CN.md`** - Project README template (Chinese) with emoji prefix, uses pnpm commands
