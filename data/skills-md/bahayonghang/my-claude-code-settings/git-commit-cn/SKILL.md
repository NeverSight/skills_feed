---
name: git-commit-cn
description: 生成符合约定式提交规范的中文 Git 提交信息。当用户请求创建 Git 提交、生成 commit 信息、或提及"提交代码"、"git commit"、"中文提交"时使用。自动分析代码变更,生成规范的中文提交信息,包含正确的类型前缀(feat/fix/docs等)和清晰的描述。
category: development-tools
tags: [git, commit-message, conventional-commits, chinese]
---

# Git Commit 中文提交信息生成

自动生成符合约定式提交(Conventional Commits)规范的中文 Git 提交信息。

## 核心工作流程

### 1. 分析代码变更

首先检查代码变更情况:

```bash
# 查看未暂存的变更
git diff

# 查看已暂存的变更
git diff --staged

# 查看状态
git status
```

### 2. 确定提交类型

根据变更内容确定提交类型:

- **feat**: 新增功能或特性
- **fix**: 修复 bug 或错误
- **docs**: 仅文档变更
- **style**: 代码格式调整(不影响功能)
- **refactor**: 代码重构
- **perf**: 性能优化
- **test**: 测试相关
- **build**: 构建系统或依赖变更
- **ci**: CI/CD 配置变更
- **chore**: 其他杂项变更

详细说明和示例见 [references/commit-types.md](references/commit-types.md)

### 3. 生成提交信息

**格式要求**:

```
<类型>: <简短描述>

[可选的详细描述]

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**简短描述规范**:
- 使用动词开头: 添加、修复、更新、删除、优化、重构
- 不超过 50 个字符
- 描述做了什么,不是为什么
- 结尾不使用标点符号

**示例**:

单行提交:
```
feat: 添加用户头像上传功能
```

多行提交:
```
feat: 添加用户头像上传功能

支持 JPG/PNG/WebP 格式,最大 5MB
自动生成 200x200 和 48x48 缩略图

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### 4. 执行提交

使用 HEREDOC 格式提交,确保格式正确:

```bash
git commit -m "$(cat <<'EOF'
feat: 添加用户管理功能

实现用户列表、添加、编辑、删除功能
集成角色权限管理

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

## 最佳实践

### 变更分组

将相关变更分组提交,每个提交只做一件事:

✅ 好的做法:
```
git add src/auth/
git commit -m "feat: 添加 OAuth2 登录支持"

git add docs/api.md
git commit -m "docs: 更新认证 API 文档"
```

❌ 不好的做法:
```
git add .
git commit -m "feat: 添加登录功能和更新文档"
```

### 带作用域的提交

对于大型项目,使用作用域标识变更范围:

```
feat(auth): 添加双因素认证
fix(ui): 修复移动端菜单样式
docs(api): 更新用户 API 文档
```

### 破坏性变更标记

如果变更不兼容旧版本,使用 BREAKING CHANGE:

```bash
git commit -m "$(cat <<'EOF'
feat: 重构用户认证 API

从 Session 改为 JWT Token 认证

BREAKING CHANGE: 旧的 /api/login 接口已移除,
请使用新的 /api/auth/token 接口

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

## 常见场景

### 新功能开发

```bash
# 添加并提交
git add src/features/upload/
git commit -m "feat: 添加文件批量上传功能"
```

### Bug 修复

```bash
git add src/components/LoginForm.tsx
git commit -m "fix: 修复登录表单验证码刷新问题"
```

### 多文件变更

```bash
git add src/ tests/ docs/
git commit -m "$(cat <<'EOF'
feat: 添加用户积分系统

- 实现积分获取和消费逻辑
- 添加积分历史记录
- 完善单元测试
- 更新 API 文档

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

### 依赖更新

```bash
git add package.json package-lock.json
git commit -m "build: 升级 React 到 18.3.0"
```

## 注意事项

1. **提交前检查**: 使用 `git status` 和 `git diff` 确认变更内容
2. **分批提交**: 相关变更一起提交,不相关的分开提交
3. **清晰描述**: 让其他人看到 commit 信息就知道做了什么
4. **避免通用描述**: 不使用"修复 bug"、"更新代码"等模糊描述
5. **使用 HEREDOC**: 多行提交信息使用 HEREDOC 格式确保正确

## 参考资源

- [references/commit-types.md](references/commit-types.md) - 完整的提交类型和示例
