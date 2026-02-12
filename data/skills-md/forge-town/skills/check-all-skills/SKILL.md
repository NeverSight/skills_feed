---
name: check-all-skills
description: 批量检查Skill是否符合最佳实践规范；自动验证命名、前言区、结构、文件清理、依赖等维度；支持单个或批量检查；生成详细检查报告；适用于Skill开发完成后的质量验证
---

# Skill 合规性检查工具

## 任务目标
- 本 Skill 用于:检查一个或多个 Skill 是否符合最佳实践规范
- 能力包含:读取 Skill 文件、验证命名、前言区、目录结构、文件清理、依赖元数据等维度、生成检查报告
- 触发条件:用户需要验证 Skill 质量时，如 "检查所有 skill 是否符合规范"、"验证 skill 目录结构"、"检查这个 skill 是否符合要求"

## 前置准备
- 无特殊依赖

## 操作步骤

### 标准流程

#### 步骤 1：读取检查规范
- 阅读 [references/checklist.md](references/checklist.md)，了解完整的 19 项检查清单
- 阅读 [references/quality-standards.md](references/quality-standards.md)，了解各项检查的背景说明

#### 步骤 2：检查单个 Skill
- 阅读目标 Skill 的 `SKILL.md` 文件
- 检查目录结构和文件列表
- 按照 checklist.md 中的 19 项检查清单逐项验证：
  1. 命名规范检查（3 项）：目录名格式、目录名后缀、最佳实践后缀
  2. 前言区检查（5 项）：name 字段存在、name 与目录名一致、description 存在、description 单行、description 长度
  3. 目录结构检查（3 项）：SKILL.md 存在、固定结构目录、空目录检查
  4. 文件清理检查（1 项）：临时文件清理
  5. 依赖元数据检查（2 项）：dependency.python 格式、dependency.system 格式
  6. README.md 记录检查（5 项）：README.md 存在、skills/ 目录存在、Skill 在 skills/ 中、Skill 已记录、记录格式正确

#### 步骤 3：批量检查多个 Skill（自动遍历）
- 检查 Skills 是否位于 `skills/` 目录下
- 使用目录遍历命令列出目标目录下所有 Skill：
  ```bash
  find /workspace/projects/skills -maxdepth 1 -name "SKILL.md" -exec dirname {} \;
  ```
- 获取所有 Skill 目录列表后，对每个 Skill 重复步骤 2 的检查流程

#### 步骤 4：生成检查报告
- 汇总所有检查结果
- 对每个 Skill 生成报告，包含：
  - 19 项检查的明细（pass/warning/error）
  - 总体状态（pass/warning/error）
  - 修复建议
- 提供总体统计：Skill 数量、通过率、最常见问题

#### 步骤 5：问题修复（可选）
- 如果检查发现问题，根据用户需求执行修复：
  - **自动修复**：对于可安全自动修复的问题（如删除临时文件、删除空目录），直接执行修复
  - **人工确认**：对于需要判断的问题（如重命名目录、修改 description、修改 name 字段），提供修复建议，等待用户确认
- 参考 [references/quality-standards.md](references/quality-standards.md) 中的检查级别说明和修复建议
- 修复后重新验证，确认问题已解决且没有引入新问题

## 资源索引
- 检查清单:见 [references/checklist.md](references/checklist.md)
  - 内容:完整的 19 项 Skill 检查清单（命名规范、前言区、目录结构、文件清理、依赖元数据、README.md 记录）
  - 何时读取:开始检查前阅读，检查过程中逐项对照
- 质量标准:见 [references/quality-standards.md](references/quality-standards.md)
  - 内容:各项检查的背景说明、通过标准定义、检查级别说明（pass/warning/error）
  - 何时读取:理解检查项背景、确定修复优先级时参考

## 注意事项
- 批量检查时，建议分批处理大量 Skills
- 修复问题后必须重新验证

## 使用示例

### 示例 1：检查单个 Skill
用户："检查 check-all-skills 这个 skill 是否符合规范"

执行步骤：
1. 读取检查规范
2. 读取 `/workspace/projects/check-all-skills/SKILL.md`
3. 检查目录结构
4. 逐项验证检查清单
5. 输出检查报告

### 示例 2：批量检查多个 Skill（自动遍历）
用户："检查 /workspace/projects 目录下所有 skill 是否符合规范"

执行步骤：
1. 读取检查规范
2. 使用步骤 3 中的命令列出该目录下所有 Skills
3. 对每个 Skill 执行步骤 2 的检查流程
4. 生成汇总报告

### 示例 3：检查并自动修复问题
用户："检查所有 skill 是否符合规范，发现问题自动修复"

执行步骤：
1. 读取检查规范和问题修复指南
2. 使用步骤 3 中的命令识别当前工作目录下的所有 Skills
3. 对每个 Skill 执行步骤 2 的检查流程
4. 根据步骤 5 执行修复：
   - 可自动修复的：直接执行修复
   - 需要确认的：提供修复建议，询问用户是否同意
5. 修复后重新验证
6. 生成修复报告

### 示例 4：检查特定维度
用户："检查 check-all-skills 的命名和目录结构是否符合规范"

执行步骤：
1. 仅检查命名规范相关项目
2. 仅检查目录结构相关项目
3. 输出这两类检查的结果
