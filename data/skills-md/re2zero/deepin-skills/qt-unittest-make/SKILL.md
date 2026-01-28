---
name: qt-unittest-make
description: Use when users request generating unit tests for Qt modules or classes, completing test cases, or creating test files. Supports module batch generation and incremental completion.
---

# Qt Unit Test Generator

## Overview

**Core principle**: 使用 LSP 精确分析类结构，生成 100% 函数覆盖率的测试用例，并强制验证构建成功。

**架构模式**: Skill 路由 + 子 Agent 全栈执行。子 Agent 负责所有具体工作，Skill 仅负责调用和结果反馈。

**关键特性**: 智能 CMake 合并、增量更新支持、严格的构建验证、详细的错误处理。

## Iron Laws

1. **仅使用 Google Test**: 测试框架固定为 GTest，不支持 Qt Test
2. **100% 函数覆盖率**: 每个 public/protected 函数必须至少一个测试用例
3. **智能 CMake 合并**: 根据项目实际情况优化合并，确保通用性
4. **支持增量更新**: 对比现有测试，补全未覆盖函数
5. **必须验证构建**: 生成后必须编译成功才能报告完成
6. **编译失败必须修正**: 每个错误最多重试 3 次，最大循环 10 次

## When to Use

**触发条件**:
- 用户请求为模块生成单元测试：`为 src/lib/ui 模块创建单元测试`
- 用户请求为类生成测试：`为 MyClass 生成测试`
- 用户请求补全测试：`为 MyClass 补全测试`

**不使用此技能时**:
- 用户请求生成测试框架（使用 `qt-unittest-build`）
- 用户请求修复测试失败（使用 `systematic-debugging`）
- 用户请求分析测试覆盖率（使用其他工具）

## 执行流程

### 步骤 1: 检查测试框架

验证 `autotests/CMakeLists.txt` 和 `autotests/3rdparty/stub/` 存在。如不存在，提示用户先运行 `qt-unittest-build`。

### 步骤 2: 分析类结构

**模块批量生成**: glob 扫描目录所有 `.h/.hpp`，提取类名。

**单个类**: 直接分析指定类。

使用 LSP 工具：
- `lsp_document_symbols` - 提取类结构
- `lsp_goto_definition` - 读取函数实现
- `lsp_find_references` - 查找依赖

### 步骤 3: 调用子 Agent（MUST DO）

**重要**: 必须调用子 Agent，不能跳过！

**子 Agent 位置**: `agent/unittest-generator.md`

**调用方式**:

使用 `task` 工具调用子 Agent：

```
task(
    description="生成单元测试代码",
    prompt="完整的任务说明，包括：
- 目标模块或类
- 测试框架要求（Google Test）
- 函数覆盖率要求（100%）
- 验证构建要求",
    subagent_type="general"
)
```

**为什么需要子 Agent**:
- **独立上下文**: 为单个类或小模块生成测试时，独立上下文避免污染
- **并行执行**: 为多个类批量生成测试时，可以 fork 多个子 Agent 并行执行，提高效率
- **任务隔离**: 子 Agent 失败不影响主 Agent，便于错误处理

**调用时机**:
- **模块批量生成**: 为每个类调用一个子 Agent（并行）
- **单个类生成**: 调用一个子 Agent
- **增量更新**: 调用子 Agent 分析差异

### 步骤 4: 等待子 Agent 完成

监听子 Agent 的执行结果：
- 收集生成的测试文件
- 检查验证构建结果
- 记录遇到的错误（如果有）

### 步骤 5: 反馈用户

根据子 Agent 的结果反馈用户：
- 如果成功：报告生成的测试文件和覆盖率
- 如果失败：报告详细的错误信息和修正建议

## Red Flags

- ❌ 使用 Qt Test 框架
- ❌ 覆盖率不足 100%
- ❌ 硬编码 CMake 模板
- ❌ 不验证构建
- ❌ 不支持增量更新
- ❌ 编译失败仍报告完成
- ❌ 跳过子 Agent 调用（直接手动工作）

## Quick Reference

**测试文件命名**: `test_myclass.cpp`

**测试类命名**: `MyClassTest`

**测试用例命名**: `{Feature}_{Scenario}_{ExpectedResult}`

**LSP 工具**: `lsp_document_symbols`, `lsp_goto_definition`, `lsp_find_references`

**Stub 模式**: `&Class::method`, `VADDR(Class, method)`, `static_cast<...>`

**编译重试逻辑**: 每个错误最多重试 3 次，最大循环 10 次

## 子 Agent 调用

**必须使用 task 工具调用子 Agent**:

```
task(
    description="生成单元测试代码",
    prompt="完整任务描述，包括目标、要求、验证流程",
    subagent_type="general"
)
```

**子 Agent 执行内容**:
- 分析项目结构（LSP）
- 生成测试文件（100% 覆盖率）
- 智能合并 CMake
- 验证构建（每个错误重试 3 次，最大循环 10 次）

**为什么需要子 Agent**:
- 独立上下文，防止污染
- 并行执行，提高效率
- 任务隔离，便于错误处理

## 常见错误

| 错误 | 原因 | 修复 |
|------|------|------|
| 测试框架不存在 | 未运行 qt-unittest-build | 提示用户先运行框架构建技能 |
| 覆盖率不足 | 未分析所有函数 | 确保 lsp_document_symbols 提取完整 |
| CMake 合并失败 | 硬编码模板 | 使用 AI 智能合并，根据项目实际情况优化 |
| 编译失败 | Stub 签名错误 | 使用 LSP 获取精确签名 |
| 编译失败仍报告完成 | 跳过验证或验证不严谨 | 必须编译成功才能报告用户 |
| 多个错误未修正 | 全局重试 3 次不足 | 每个错误重试 3 次，最大循环 10 次 |

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "直接手动工作更快" | 手动工作无法保证 100% 覆盖率和构建验证，子 Agent 是强制要求 |
| "跳过子 Agent 调用" | 违反技能的铁律，必须调用子 Agent |
| "编译失败也可以报告完成" | 违反强制构建验证要求，必须编译成功才能报告 |
| "全局重试 3 次就够了" | 每个错误重试 3 次，不是全局 3 次 |
| "覆盖率 80% 就可以了" | 铁律要求 100% 函数覆盖率，无例外 |
| "Qt Test 也一样" | 技能固定使用 Google Test，不支持 Qt Test |
