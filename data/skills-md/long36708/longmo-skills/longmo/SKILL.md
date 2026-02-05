---
name: longmo
description: Longmo's opinionated tooling and conventions for JavaScript/TypeScript projects. Use when setting up new projects, configuring ESLint/Prettier alternatives, monorepos, library publishing, or when the user mentions Longmo's preferences.
metadata:
  author: Longmo
  version: "2026.2.1"
---

# Longmo's Preferences

| Category             | Preference                                                                    |
|----------------------|-------------------------------------------------------------------------------|
| Package Manager      | pnpm (with `@antfu/ni` for unified commands)                                  |
| Language             | TypeScript (strict mode, ESM only)                                            |
| Linting & Formatting | `@antfu/eslint-config` (no Prettier)  + `eslint-plugin-oxlint` + `commitlint` |
| Testing              | Vitest                                                                        |
| Git Hooks            | lefthook                                                                      |
| Bundler (Libraries)  | tsdown                                                                        |
| Documentation        | VitePress                                                                     |

---

## Core Conventions

### @antfu/ni Commands

| Command                    | Description                                |
|----------------------------|--------------------------------------------|
| `ni`                       | Install dependencies                       |
| `ni <pkg>` / `ni -D <pkg>` | Add dependency / dev dependency            |
| `nr <script>`              | Run script                                 |
| `nu`                       | Upgrade dependencies                       |
| `nun <pkg>`                | Uninstall dependency                       |
| `nci`                      | Clean install (`pnpm i --frozen-lockfile`) |
| `nlx <pkg>`                | Execute package (`npx`)                    |

### TypeScript Config

```json
{
	"compilerOptions": {
		"target": "ESNext",
		"module": "ESNext",
		"moduleResolution": "bundler",
		"strict": true,
		"esModuleInterop": true,
		"skipLibCheck": true,
		"resolveJsonModule": true,
		"isolatedModules": true,
		"noEmit": true
	}
}
```

### ESLint Setup

```js
// eslint.config.mjs
import antfu from '@antfu/eslint-config'
import oxlint from 'eslint-plugin-oxlint'

export default [
    ...(await antfu({
        vue: {
            overrides: {
                'vue/html-self-closing': 'off',
            },
        },
    })),
    ...oxlint.configs['flat/all'],
]
```

Fix linting errors with `nr lint --fix`. Do NOT add a separate `lint:fix` script.

For detailed configuration options: [antfu-eslint-config](references/antfu-eslint-config.md)

### Commit Message Guidelines

```ts
// commitlint.config.mjs
export default {
    extends: ['@commitlint/config-conventional'],
    rules: {
        'type-enum': [
            2,
            'always',
            [
                'feat',     // 新功能
                'fix',      // 修复
                'docs',     // 文档
                'style',    // 代码格式（不影响代码运行的变动）
                'refactor', // 重构
                'perf',     // 性能优化
                'test',     // 测试
                'chore',    // 构建过程或辅助工具的变动
                'ci',       // CI配置
                'revert',   // 回滚
                'build',    // 构建系统
            ],
        ],
        'subject-case': [0], // 不限制 subject 大小写
    },
}
```

### Lefthook Configuration

```yaml
# Lefthook 配置文件
# 参考：https://github.com/evilmartians/lefthook
pre-commit:
  parallel: true
  commands:
    # 格式化和检查 Vue 文件
    lint-vue:
      glob: '*.vue'
      run: pnpm exec eslint --cache --fix {staged_files}
      fail_text: "ESLint 检查失败，请修复错误后再提交"

    # 格式化和检查 TypeScript/JavaScript 文件
    lint-ts:
      glob: '*.{ts,tsx,js,jsx}'
      run: pnpm exec eslint --cache --fix {staged_files}
      fail_text: "ESLint 检查失败，请修复错误后再提交"

commit-msg:
  commands:
    commitlint:
      run: pnpm exec commitlint --edit {1}
      fail_text: "提交信息不符合规范，请参考 Conventional Commits 规范"
      skip: 'git log -1 --pretty=%s | grep -q "\[skip ci\]"'

```

### Git Hooks

```json
{
	"scripts": {
		"prepare": "lefthook install"
	}
}
```

> 务必用 lefthook 更新 pnpm-workspace.yaml onlyBuiltDependencies，
> 并在根 package.json 中添加 lefthook pnpm.onlyBuiltDependencies，
> 否则lefthook包的安装后脚本不会被执行，钩子也不会被安装。

### Vitest Conventions

- Test files: `foo.ts` → `foo.test.ts` (same directory)
- Use `describe`/`it` API (not `test`)
- Use `toMatchSnapshot` for complex outputs
- Use `toMatchFileSnapshot` with explicit path for language-specific snapshots

---

## pnpm Catalogs

Use named catalogs in `pnpm-workspace.yaml` for version management:

| Catalog    | Purpose                              |
|------------|--------------------------------------|
| `prod`     | Production dependencies              |
| `inlined`  | Bundler-inlined dependencies         |
| `dev`      | Dev tools (linter, bundler, testing) |
| `frontend` | Frontend libraries                   |

Avoid the default catalog. Catalog names can be adjusted per project needs.

---

## References

| Topic               | Description                                                     | Reference                                                |
|---------------------|-----------------------------------------------------------------|----------------------------------------------------------|
| ESLint Config       | Framework support, formatters, rule overrides, VS Code settings | [antfu-eslint-config](references/antfu-eslint-config.md) |
| Project Setup       | .gitignore, GitHub Actions, VS Code extensions                  | [setting-up](references/setting-up.md)                   |
| App Development     | Vue/Nuxt/UnoCSS conventions and patterns                        | [app-development](references/app-development.md)         |
| Library Development | tsdown bundling, pure ESM publishing                            | [library-development](references/library-development.md) |
| Monorepo            | pnpm workspaces, centralized alias, Turborepo                   | [monorepo](references/monorepo.md)                       |
