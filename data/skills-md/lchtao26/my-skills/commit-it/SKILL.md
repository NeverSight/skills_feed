---
name: commit-it
description: Generate git commit messages following Angular Conventional Commit format, written in Chinese with technical terms in English. Use when committing git changes, staging files, or when the user asks for help with commit messages.
---

# commit-it

## Commit Message Format

Follow Angular Conventional Commit specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type

Use one of these types:
- `feat`: 新功能 (new feature)
- `fix`: 修复 bug (bug fix)
- `docs`: 文档变更 (documentation changes)
- `style`: 代码格式变更，不影响代码运行 (formatting, missing semicolons, etc.)
- `refactor`: 重构代码 (code refactoring)
- `perf`: 性能优化 (performance improvements)
- `test`: 添加或修改测试 (adding or updating tests)
- `chore`: 构建过程或辅助工具的变动 (maintenance tasks)
- `ci`: CI 配置文件和脚本的变更 (CI configuration changes)
- `build`: 构建系统或外部依赖的变更 (build system changes)
- `revert`: 回退之前的 commit (revert a previous commit)

### Scope

Optional scope indicating the area affected (e.g., `auth`, `api`, `ui`, `db`).

### Subject

Brief description in Chinese (max 50 characters). Technical terms remain in English.

### Body

Optional detailed description in Chinese. Explain what and why, not how.

### Footer

Optional footer for breaking changes or issue references.

## Language Guidelines

- Write commit messages in **Chinese**
- Keep **technical jargon** in English (e.g., API, JWT, middleware, component, hook)
- Keep **code references** in English (e.g., function names, class names, file paths)

## Examples

**Example 1: New feature**
```
feat(auth): 添加 JWT token 认证功能

实现用户登录接口和 token 验证中间件
支持 refresh token 机制
```

**Example 2: Bug fix**
```
fix(api): 修复日期时区转换错误

报告生成时统一使用 UTC 时间戳
修复时区显示不一致的问题
```

**Example 3: Refactoring**
```
refactor(ui): 重构用户列表组件

将 UserList 组件拆分为更小的子组件
优化渲染性能，减少不必要的 re-render
```

**Example 4: Documentation**
```
docs: 更新 API 使用文档

添加 authentication 和 authorization 章节
补充 request/response 示例
```

**Example 5: Performance**
```
perf(db): 优化数据库查询性能

为 user 表添加索引
使用 connection pooling 减少连接开销
```

## Workflow

1. Analyze staged changes: `git diff --cached`
2. Determine the appropriate type and scope
3. Write commit message following the format
4. Use Chinese for descriptions, English for technical terms
5. Keep subject concise (max 50 characters)
6. Add body if more context is needed
7. Execute the commit: `git commit -m "<generated message>"`
