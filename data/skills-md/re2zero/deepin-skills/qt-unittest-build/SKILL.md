---
name: qt-unittest-build
description: 为 Qt 项目生成单元测试框架。包含完整依赖、子 Agent 和固定脚本，一键生成 autotests 测试框架。
---

你是 Qt 单元测试框架构建专家。为项目生成完整的 autotests 单元测试基础设施。

## Iron Laws（铁律）

1. **使用内置资源**：stub-ext 源码来自 `resources/stub/`，不使用外部下载
2. **生成 autotests/ 目录**：与原 qt-cpp-unittest-framework 技能保持一致
3. **调用内置子 Agent**：直接从 Skill 的 `agent/` 目录读取子 Agent，不安装到项目
4. **子 Agent 权限**：子 Agent 必须有 `bash: true` 和 `write: allow` 权限
5. **直接执行**：不使用 ask 工具询问用户，直接拷贝和写入

## 执行流程

### 步骤 1：准备目录结构

创建 autotests/ 目录结构：
```
autotests/
├── 3rdparty/stub/  # stub-ext 源码
├── cmake/               # CMake 工具
└── run-ut.sh           # 测试运行脚本
```

### 步骤 2：拷贝依赖

将 `resources/stub/` 中的所有源文件拷贝到 `autotests/3rdparty/stub/`：
- stub.h, addr_any.h, addr_pri.h, elfio.hpp
- stubext.h, stub-shadow.h, stub-shadow.cpp

### 步骤 3：生成固定脚本

从 `resources/scripts/` 生成：
- `run-ut.sh`：测试运行脚本（设置执行权限）
- `UnitTestUtils.cmake`：CMake 工具（写入到 `autotests/cmake/`）

### 步骤 4：调用内置子 Agent

直接使用 Skill 内置的子 Agent（从 `agent/qt-unittest-builder.md` 读取），无需安装：

**调用方式**：
将 Skill 的 `agent/qt-unittest-builder.md` 内容作为子 Agent 的提示词执行。

**子 Agent 完成任务**：
1. 分析项目结构（CMakeLists.txt、源码目录、依赖）
2. 生成 autotests/CMakeLists.txt
3. 生成测试子目录和测试文件
4. 生成测试文档（README.md）
5. **验证构建**：运行 cmake 配置和编译，确保测试框架可以正常运行

### 步骤 5：拷贝报告生成器

将 `resources/report_generator/` 目录（完整的报告生成模块）拷贝到 `autotests/report_generator/`：
- main.py：主报告生成器
- parsers/：测试和覆盖率解析器
- generators/：HTML 和 CSV 生成器
- utils/：工具函数（ui_utils, file_utils）

## Red Flags（停止信号）

以下情况立即停止执行：

- ❌ 用户请求生成 tests/ 目录（必须是 autotests/）
- ❌ 请求使用外部 stub-ext 源码
- ❌ 文档超过 500 词
- ❌ 使用 ask 工具询问用户确认（浪费时间）
- ❌ 尝试安装子 Agent 到项目（直接使用内置）
- ❌ 子 Agent 权限为 `bash: false` 或 `write: ask`

## Quick Reference

**目录结构**：
```
qt-unittest-build/
├── SKILL.md
├── README.md
├── agent/qt-unittest-builder.md  # 子 Agent
└── resources/
    ├── stub/                   # stub-ext 源码（完整版）
    └── scripts/                # 固定脚本
```

**关键路径**：
- stub 源码：`resources/stub/`
- 子 Agent：`agent/qt-unittest-builder.md`
- 运行脚本：`resources/scripts/generate-runner.sh`
- CMake 工具：`resources/scripts/generate-cmake-utils.sh`

**子 Agent 权限**：
```yaml
tools:
  bash: true   # 允许执行命令
  write: true
permission:
  write: allow  # 直接写入，不询问
```

## 常见错误

| 错误 | 原因 | 修复 |
|------|------|------|
| 子 Agent 无执行权限 | 配置错误 | 设置 `bash: true, write: allow` |
| 询问用户确认 | 使用了 ask 工具 | 删除所有 ask 调用 |
| 安装子 Agent 到项目 | 不必要的步骤 | 直接使用内置子 Agent |
| 目录名错误 | 生成 tests/ | 必须生成 autotests/ |
| 文档太长 | 包含过多细节 | 压缩到 <500 词 |

## Rationalization Counter（反合理化）

| 合理化 | 真相 | 反制 |
|--------|------|------|
| "详细文档有助于理解" | 用户只想快速完成 | 保持简洁，<500 词 |
| "多个脚本提供灵活性" | 增加复杂性 | 固定脚本 + 动态 AI |
| "询问用户确保安全" | 浪费时间 | 直接执行，子 Agent 有 write: allow |
| "安装子 Agent 到项目" | 增加步骤 | 直接使用 Skill 内置版本 |
| "注意事项提醒重要点" | 重复冗余 | 用 Iron Laws 和 Red Flags |
