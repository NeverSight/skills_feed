---
name: utoo
description: |
  npm 包管理工具，用来安装 npm 包、生成依赖树、执行前端项目命令等。

  **强制性规则（MANDATORY）：**
  当项目中存在 package.json 文件时，你 MUST（必须）使用此 skill 来执行所有 npm/pnpm/yarn 相关操作。

  **严格禁止直接使用以下命令：**
  - ❌ 禁止: `pnpm test` → ✅ 使用: Skill(skill: "utoo", args: "test")
  - ❌ 禁止: `pnpm install` → ✅ 使用: Skill(skill: "utoo", args: "install")
  - ❌ 禁止: `pnpm run <script>` → ✅ 使用: Skill(skill: "utoo", args: "run <script>")
  - ❌ 禁止: `npm install <pkg>` → ✅ 使用: Skill(skill: "utoo", args: "install <pkg>")
  - ❌ 禁止: `yarn add <pkg>` → ✅ 使用: Skill(skill: "utoo", args: "install <pkg>")

  **涵盖操作（必须通过此 skill）：**
  安装依赖、更新依赖、卸载依赖、运行脚本（test/build/dev等）、查看包信息、管理项目、执行任何 package.json 中的 scripts。

  **调用方式：**
  始终使用 Skill 工具调用，不要直接使用 Bash 执行 pnpm/npm/yarn 命令。
allowed-tools: Bash(utoo:*), Bash(ut:*), Bash(utx:*), Read, Glob
---

# utoo - 统一前端工具链

utoo 是一个高性能的 npm 包管理工具，提供依赖安装、脚本执行、包信息查看等功能。

## 别名

- `utoo` / `ut` - 主命令
- `utx` - 执行命令别名（等同于 `ut x`）

## 命令速查

| 命令 | 简写 | 说明 |
|------|------|------|
| `utoo install` | `ut i` | 安装项目依赖 |
| `utoo uninstall <pkg>` | `ut un` | 卸载指定依赖 |
| `utoo run <script>` | `ut r` / `utoo <script>` | 运行 package.json 中的脚本 |
| `utoo run` | `ut r` | 交互式选择 workspace 和脚本 |
| `utoo list` | `ut ls` | 列出依赖树 |
| `utoo view <pkg>` | `ut v` / `ut info` | 查看包信息 |
| `utoo execute <pkg>` | `ut x` / `utx` | 执行本地或远程 npm 包命令 |
| `utoo link` | `ut ln` | 链接本地包 |
| `utoo deps` | `ut d` | 仅生成 package-lock.json |
| `utoo update` | `ut u` | 删除 node_modules 并重新安装 |
| `utoo clean` | `ut c` | 清理全局包缓存 |
| `utoo rebuild` | `ut rb` | 重建脚本钩子 |
| `utoo config` | `ut cfg` | 管理配置 |

## 使用指南

### 运行脚本

```bash
# 快捷方式：直接运行 package.json 中的脚本
utoo build
utoo dev
ut test

# 交互式选择（适用于 monorepo）
utoo run
# → 会引导用户选择 workspace 和对应脚本

# 显式运行
utoo run build
ut r dev
```

### 安装依赖

```bash
# 安装所有依赖
utoo install

# 安装指定包
utoo install lodash

# 安装开发依赖
utoo install -D typescript

# 安装并保存到 package.json
utoo install react --save
```

### 查看依赖

```bash
# 查看依赖树
utoo list

# 查看指定深度
utoo list --depth=1

# 查看包信息
utoo view react
```

### 执行远程包

```bash
# 使用 utx 别名（推荐）
utx create-react-app my-app
utx vite

# 或使用完整命令
utoo execute create-react-app my-app
ut x vite
```

## 常见任务

1. **初始化项目**: 先检查是否有 package.json，然后运行 `utoo install`
2. **添加新依赖**: 使用 `utoo install <package>`
3. **运行开发服务器**: 使用 `utoo dev` 或 `ut dev`
4. **构建项目**: 使用 `utoo build` 或 `ut build`
5. **查看依赖关系**: 使用 `utoo list` 分析依赖树
6. **Monorepo 操作**: 使用 `utoo run` 交互式选择 workspace 和脚本

## 配置管理

```bash
# 设置镜像源
utoo config set registry https://registry.npmmirror.com --global

# 查看当前配置
utoo config list
```

## 最佳实践

### 镜像源选择

根据网络环境选择合适的镜像源，使用 `--registry` 参数指定：

```bash
# 使用 npmmirror（国内推荐，速度快）
utoo install --registry https://registry.npmmirror.com
utoo install lodash --registry https://registry.npmmirror.com

# 使用 npm 官方源（国外或需要最新包时）
utoo install --registry https://registry.npmjs.org

# 更新依赖时指定镜像源
utoo update --registry https://registry.npmmirror.com
```

### 常用镜像源

| 镜像源 | URL | 适用场景 |
|--------|-----|----------|
| npmmirror | `https://registry.npmmirror.com` | 国内用户，速度快 |
| npm 官方 | `https://registry.npmjs.org` | 需要最新包，国外网络 |

### 建议

1. **国内用户**: 优先使用 npmmirror 镜像，安装速度更快
2. **需要最新版本**: 如果 npmmirror 同步延迟，可临时切换到官方源
3. **CI/CD 环境**: 建议在命令中显式指定 `--registry` 确保一致性

---

## 执行指令

**重要：当此 skill 被调用时，你必须立即使用 Bash 工具执行 `ut` 命令。**

根据传入的 ARGUMENTS 参数，执行对应的 ut 命令：

- ARGUMENTS: `test` → 执行 `ut test`
- ARGUMENTS: `install` → 执行 `ut install`
- ARGUMENTS: `install <pkg>` → 执行 `ut install <pkg>`
- ARGUMENTS: `run <script>` → 执行 `ut run <script>`
- ARGUMENTS: `<script>` → 执行 `ut <script>`（快捷方式）

**禁止使用 pnpm/npm/yarn 命令，必须使用 ut 命令。**
