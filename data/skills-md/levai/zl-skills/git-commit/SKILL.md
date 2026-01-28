---
name: git-commit
description: Git 提交信息规范，遵循 Conventional Commits 格式。适用于所有 Git 提交操作，确保提交信息清晰、规范、可追溯。
metadata:
  author: datagradient-ui
  version: "222"
---

# Git 提交规范

## 何时使用

在进行任何 Git 提交操作时都应遵循此规范，确保提交信息清晰、规范、可追溯。

## 提交格式

遵循 Conventional Commits 规范：

```
<type>: <subject>
```

## Type 类型

- `feat`: 新功能222
- `fix`: 修复 bug
- `docs`: 文档变更
- `style`: 代码格式（不影响代码运行）
- `refactor`: 重构（既不是新增功能，也不是修复 bug）
- `perf`: 性能优化
- `test`: 测试相关
- `build`: 构建系统或外部依赖变更
- `ci`: CI 配置文件和脚本变更
- `chore`: 其他变更（如构建过程或辅助工具的变动）
- `revert`: 回滚提交

## Subject 规范

- 可以使用英文或中文
- 不超过 50 字
- 简明描述本次提交内容
- 首字母小写，结尾不加句号

## 示例

```bash
# ✅ GOOD (English)
git commit -m "feat: add flow distribution dialog component"
git commit -m "fix: fix form validation rule not working"
git commit -m "refactor: refactor data model view base class"
git commit -m "docs: update component usage documentation"
git commit -m "style: adjust button spacing"

# ✅ GOOD (Chinese)
git commit -m "feat: 添加流量分配对话框组件"
git commit -m "fix: 修复表单验证规则不生效的问题"
git commit -m "refactor: 重构数据模型视图基类"
git commit -m "docs: 更新组件使用文档"
git commit -m "style: 调整按钮样式间距"

# ❌ BAD
git commit -m "fix bug"
git commit -m "feat: add flow distribution dialog component with model selection and numeric input features supporting two-way binding and automatic calculation"
```

## 提交原则

1. **一次提交只做一件事**：每个提交应该只包含一个逻辑变更
2. **原子性提交**：提交应该是完整且可独立运行的
3. **清晰的描述**：提交信息应该清楚地说明做了什么，为什么这样做

## 多行提交信息

对于复杂变更，可以使用多行格式：

```
<type>: <subject>

<body>

<footer>
```

```bash
# 示例
git commit -m "feat: add data model validation

- Support model name uniqueness check
- Add async validation method
- Optimize error message display

Closes #123"
```

## 常见场景

### 新功能开发

```bash
git commit -m "feat: add user management page"
# 或
git commit -m "feat: 添加用户管理页面"
```

### Bug 修复

```bash
git commit -m "fix: fix list pagination data not refreshing"
# 或
git commit -m "fix: 修复列表分页数据不刷新的问题"
```

### 代码重构

```bash
git commit -m "refactor: extract common form validation logic to utility function"
# 或
git commit -m "refactor: 提取公共表单验证逻辑到工具函数"
```

### 文档更新

```bash
git commit -m "docs: update README with installation instructions"
# 或
git commit -m "docs: 更新 README 添加安装说明"
```

### 样式调整

```bash
git commit -m "style: unify button spacing styles"
# 或
git commit -m "style: 统一按钮间距样式"
```
