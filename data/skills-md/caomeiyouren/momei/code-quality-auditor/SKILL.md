---
name: code-quality-auditor
description: 融合 Lint、类型检查、规范审查与安全审计的综合质量门禁。
version: 1.0.0
author: GitHub Copilot
---

# Code Quality Auditor Skill (代码质量审计技能)

## 核心职责 (Responsibilities)

### 1. 自动化质量验证 (Automation)
-   **静态检查**: 执行 `pnpm lint` 检查代码风格。
-   **类型闭环**: 执行 `pnpm typecheck` 确保无 `any` 和类型断裂。
-   **样式校验**: 执行 `pnpm lint:css` 确保 BEM 规范。

### 2. 安全审计 (Security) 🛡️
-   **漏洞扫描**: 检查 SQL 注入、XSS、CSRF 和未授权访问风险。
-   **密钥检查**: 严禁代码中出现硬编码的 API Key、Token 或密钥。
-   **鉴权逻辑**: 检查是否正确使用了 `isAdmin()` 等权限校验函数。

### 3. 规范对齐 (Standards)
-   **命名规范**: 检查文件 kebab-case、国际化 snake_case 等命名。
-   **i18n**: 检查 UI 文本是否全部被 `$t()` 包裹。
-   **代码味道**: 识别过长函数、死代码和重复逻辑。

## 指令 (Instructions)

1.  **路径感知与工作树隔离**: 审计工作应在具体的改动目录中执行。对于 `master` 分支的审计应侧重于 Hotfix，而日常审计应在 `dev` 或 `test` 工作树中进行。
2.  **阻塞式交付**: 如果 `lint` 或 `typecheck` 失败，必须标记为“阻塞”，禁止进入提交环节。
3.  **分级反馈**: 提供 `Blocker` (死档问题), `Warning` (风格问题), `Suggest` (重构建议)。
3.  **零容忍 any**: 在 TypeScript 开发中，严禁无故使用 `any`。

## 使用示例 (Usage Example)

动作: 运行 `pnpm lint && pnpm typecheck`，解析所有警告并在代码修改中一次性修复。
