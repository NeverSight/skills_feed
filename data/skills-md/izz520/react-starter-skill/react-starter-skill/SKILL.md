---
name: react-starter-skill
description: |
  React + Vite + Tailwind CSS v4 + React Query + Zustand + React Router + Lingui + shadcn + lucide-react 项目脚手架。Use when creating new React projects, initializing frontend projects, or scaffolding React + Vite applications. Triggers on requests like "创建React项目", "初始化前端项目", "搭建React脚手架", "create a new React app", "scaffold a frontend project".
---

# React Starter Skill

Scaffold modern React projects with a production-ready tech stack.

**Tech Stack:** React, Vite, Tailwind CSS v4, TanStack Query, Zustand, React Router, Lingui, shadcn/ui, lucide-react

## Quick Start

### 1. Detect Package Manager

Check which package manager is installed on the user's system. Use the first available in this priority order:
1. `pnpm` (preferred)
2. `yarn`
3. `npm`

### 2. Create Project

```bash
mkdir <project-name> && cd <project-name>
<pkg> create vite . --template react-ts
```

> Replace `<pkg>` with the detected package manager (`pnpm`, `yarn`, or `npm`).

### 3. Remove ESLint (use Biome instead)

The Vite template includes ESLint by default. Remove it since we use Biome:

```bash
# Remove ESLint config file
rm -f eslint.config.js .eslintrc* .eslintignore

# Remove ESLint dependencies from package.json
<pkg> remove eslint eslint-plugin-react-hooks eslint-plugin-react-refresh @eslint/js globals typescript-eslint 2>/dev/null || true
```

### 4. Install Dependencies

See [dependencies.md](references/dependencies.md)

### 5. Create Directory Structure

See [project-structure.md](references/project-structure.md)

### 6. Add Configuration Files

See [config-files.md](references/config-files.md)

### 7. Add Code Patterns

See [code-patterns.md](references/code-patterns.md)

### 8. Initialize i18n (Extract, Translate, Compile)

**CRITICAL: This step is REQUIRED before the project can run.** The `I18nProvider` imports compiled message files that don't exist until you complete all three sub-steps below.

#### 7.1 Extract messages

```bash
<pkg> run i18n:extract
```

This generates PO files in `src/locales/{locale}/messages.po`.

#### 7.2 Translate PO files

**You MUST translate each locale's PO file now.** Do the following:

1. Read each PO file: `src/locales/{locale}/messages.po`
2. For every entry where `msgstr ""` is empty, translate the `msgid` to the target language
3. Update the file with translations using the Edit tool

**Locale to language mapping (matches `constants/languages.ts`):**
- `en` → English
- `es` → Spanish (Español)
- `ja` → Japanese (日本語)
- `ko` → Korean (한국어)
- `vi` → Vietnamese (Tiếng Việt)
- `tw` → Traditional Chinese (繁體中文)
- `fr` → French (Français)
- `pt` → Portuguese (Português)

**Example transformation:**
```po
# Before
msgid "Hello"
msgstr ""

# After (for ja)
msgid "Hello"
msgstr "こんにちは"
```

#### 7.3 Compile messages

After translating all PO files:

```bash
<pkg> run i18n:compile
```

This generates `src/locales/{locale}/messages.ts` files required by `I18nProvider`.

### 9. Verify Project

```bash
<pkg> run dev
```

The project should now start without errors.

## References

| File | Description |
|------|-------------|
| [dependencies.md](references/dependencies.md) | All npm packages |
| [project-structure.md](references/project-structure.md) | Full directory structure |
| [config-files.md](references/config-files.md) | Vite, Tailwind, Lingui, TypeScript configs |
| [code-patterns.md](references/code-patterns.md) | Axios, Zustand, Provider, Router patterns |