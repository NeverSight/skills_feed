---
name: gitflow
description: Gitflow 工作流规则，包括分支策略、版本控制、PR 规则和发布流程。当需要管理复杂的分支策略、进行发布或热修复时使用此 skill。
---

# Gitflow 工作流规则

## 主分支

### main（或master）

- 包含生产就绪代码
- 永远不要直接提交到main分支
- 只接受来自以下分支的合并：
  - hotfix/* 分支
  - release/* 分支
- 每次合并后必须使用版本号标记

### develop

- 主开发分支
- 包含最新交付的开发变更
- 功能分支的源分支
- 永远不要直接提交到develop分支

## 支持分支

### feature/*

- 从develop分支创建
- 合并回：develop
- 命名约定：feature/[issue-id]-描述性名称
- 示例：feature/123-user-authentication
- 创建PR前必须与develop分支保持同步
- 合并后删除

### release/*

- 从develop分支创建
- 合并回：main 和 develop
- 命名约定：release/vX.Y.Z
- 示例：release/v1.2.0
- 仅进行bug修复、文档编写及与发布相关的任务
- 不添加新功能
- 合并后删除

### hotfix/*

- 从main分支创建
- 合并回：main 和 develop
- 命名约定：hotfix/vX.Y.Z
- 示例：hotfix/v1.2.1
- 仅用于紧急生产环境修复
- 合并后删除

## 提交信息

- 格式：`type(scope): description`
- 类型：
  - feat: 新功能
  - fix: Bug修复
  - docs: 文档变更
  - style: 格式调整、缺失分号等
  - refactor: 代码重构
  - test: 添加测试
  - chore: 维护任务

## 版本控制

### 语义化版本

- MAJOR版本用于不兼容的API变更
- MINOR版本用于向后兼容的功能性变更
- PATCH版本用于向后兼容的bug修复

## Pull Request规则

1. 所有变更必须通过Pull Request进行
2. 所需批准：至少1个
3. CI检查必须通过
4. 不允许直接提交到受保护分支（main, develop）
5. 合并前分支必须保持最新
6. 合并后删除分支

## 分支保护规则

### main和develop

- 要求Pull Request审核
- 要求状态检查通过
- 要求分支保持最新
- 限制规则包括管理员
- 禁止强制推送
- 禁止删除

## 发布流程

1. 从develop创建release分支
2. 更新版本号
3. 修复任何与发布相关的问题
4. 创建PR到main
5. 合并到main后：
   - 标记发布
   - 合并回develop
   - 删除release分支

## 热修复流程

1. 从main创建hotfix分支
2. 修复问题
3. 更新patch版本号
4. 创建PR到main
5. 合并到main后：
   - 标记发布
   - 合并回develop
   - 删除hotfix分支
