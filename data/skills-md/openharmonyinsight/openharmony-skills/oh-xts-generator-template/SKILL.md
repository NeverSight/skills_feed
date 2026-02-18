---
name: oh-xts-generator-template
description: OpenHarmony XTS 测试用例通用生成模板。支持各子系统测试用例生成，API 定义解析，测试覆盖率分析，代码规范检查。触发关键词：XTS、测试生成、用例生成、测试用例。
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
---

# oh-xts-generator-template

> **OpenHarmony XTS 测试用例通用生成模板**

## 技能概述

oh-xts-generator-template 是一个通用的 OpenHarmony XTS 测试用例生成模板，设计为**可配置、可扩展**的通用框架，适用于各个子系统的测试用例生成。

### 核心特性

1. **通用测试生成流程** - 提供完整的测试用例生成工作流
2. **模块化架构** - 四层模块化设计（L1/L2/L3/L4），按需加载
3. **分层配置系统** - 通用配置 + 子系统特有配置
4. **灵活扩展机制** - 支持各子系统添加特有配置和模板

### 核心功能

| 功能 | 说明 |
|------|------|
| **API定义解析** | 解析 `.d.ts` 文件，提取接口、方法、参数、返回值、错误码 |
| **测试覆盖分析** | 分析现有测试文件，识别已覆盖和未覆盖的API |
| **智能测试生成** | 根据测试策略自动生成符合 XTS 规范的测试用例 |
| **测试设计文档生成** | 同时生成结构化的测试设计文档，包含测试用例说明、预期结果等 |
| **ArkTS 静态语言语法规范校验** | 校验 ArkTS 静态语言语法规范，包括类型注解、字段初始化、语法兼容性等 |
| **代码规范检查** | 确保生成的代码符合 XTS 测试规范 |
| **编译问题解决** | subagent 执行编译，自动修复语法错误，监听编译完成状态 |

## 适用场景

- ✅ 为新 API 生成完整的测试套件
- ✅ 同时生成测试用例和测试设计文档
- ✅ 分析现有测试的覆盖情况
- ✅ 补充缺失的测试用例和测试设计
- ✅ 验证测试代码规范性
- ✅ 各子系统定制化测试生成

## 快速开始

> 📖 **详细使用方式**: [docs/USAGE.md](./docs/USAGE.md)

### 三种使用方式概览

| 方式 | 适用场景 | 链接 |
|------|---------|------|
| 方式1：通用模板 | 新手、简单任务 | [USAGE.md](./docs/USAGE.md#方式1通用模板推荐新手) |
| 方式2：子系统配置 | 大多数任务（推荐） | [USAGE.md](./docs/USAGE.md#方式2子系统配置推荐) |
| 方式3：自定义配置 | 高级用户、特殊需求 | [USAGE.md](./docs/USAGE.md#方式3自定义配置) |

## 核心工作流程

```
1. 确定子系统配置
    ├─ 检查是否存在子系统配置文件
    ├─ 加载通用配置 (_common.md)
    └─ 加载子系统配置 ({Subsystem}/_common.md)

2. 解析 API 定义 (.d.ts + 文档)
    ├─ 读取 API 声明文件 (.d.ts)
    ├─ 查找并解析 API 文档
    └─ 综合分析

3. 参考已有用例（强制）
    ├─ 扫描指定路径的已有测试文件
    ├─ 分析代码风格和规范
    └─ 提取共性模式

4. 分析现有测试（可选）
    ├─ 扫描测试文件
    ├─ 识别已覆盖的API
    └─ 计算测试覆盖率

5. 生成测试用例
    ├─ 应用子系统特有规则
    ├─ 使用子系统特有模板
    └─ 应用已有用例的代码风格

6. 同步生成测试设计文档（强制）
    ├─ 为每个测试用例生成详细设计说明
    ├─ 包含测试场景、测试步骤、预期结果
    ├─ 生成结构化 Markdown 文档
    └─ 与测试用例文件对应命名

7. 添加 @tc 注释块（强制）
    ├─ @tc.name：小驼峰命名，与 it() 参数一致
    ├─ @tc.number：{describe名}_{序号}
    ├─ @tc.desc：{API名} {错误码/场景} test.
    └─ 验证字段值与 it() 参数的一致性

 8. 格式化和验证
     ├─ 应用代码模板
     ├─ 检查语法规范
     │   ├─ 8.1 动态语法检查（生成动态 XTS 用例时）
     │   │   └─ 参考规范文档：`references/ArkTS_Dynamic_Syntax_Rules.md`
     │   └─ 8.2 静态语法检查（生成静态 XTS 用例时）
     │       └─ 参考规范文档：`references/arkts-static-spec/`
     ├─ 验证断言方法
     └─ 输出校验结果和修改建议

9. 注册测试套（新增文件时必须）
    ├─ 查找 List.test.ets 文件
    ├─ 添加 import 语句
    └─ 在 testsuite() 函数中调用

 10. 编译验证（重要）
     ├─ 检测运行环境（Linux/Windows）
     ├─ 根据环境选择编译方案
     ├─ Linux 环境：使用 subagent 执行编译，监听进程，自动修复语法错误
     ├─ Windows 环境：根据关键词自动选择动态或静态编译模式
     └─ **详细编译流程**：参见注意事项第7条"编译环境检测"

11. 输出更新文件列表、测试设计文档和覆盖率对比

> 📖 **详细的工作流程说明请查看**: [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)

## 配置扩展

> 📖 **详细配置说明**: [docs/CONFIG.md](./docs/CONFIG.md)

### 配置优先级

```
用户自定义配置 > 子系统配置 > 通用配置
```

## 输出规范

### 测试用例编号(`@tc.number`)

```
格式: SUB_[子系统]_[模块]_[API]_[类型]_[序号]

类型标识：
- PARAM    参数测试
- ERROR    错误码测试
- RETURN   返回值测试
- BOUNDARY 边界值测试
```

### 测试设计文档规范（强制）

**文件命名规则**：
```
格式: {测试文件名}.design.md
示例: Component.onClick.test.ets -> Component.onClick.test.design.md
```

**文档模板和生成规则**：
- 标准版模板：`modules/L3_Generation/design_doc_generator.md`
- 简化版模板：`modules/L3_Generation/design_doc_templates.md`


### 测试设计文档生成规则

**1. 同步生成原则**
- 生成每个测试用例时，必须同步生成对应的测试设计文档
- 测试设计文档与测试用例一一对应
- 文档内容必须与测试用例实现保持一致

**2. 文档内容完整性**
- 必须包含所有测试场景的详细说明
- 必须包含测试步骤和预期结果
- 必须说明测试环境和前置条件
- 必须记录变更历史

**3. 文档格式规范性**
- 使用 Markdown 格式
- 遵循统一的模板结构
- 使用表格组织关键信息
- 保持版本信息更新

**4. 文档更新机制**
- 测试用例修改时，必须同步更新测试设计文档
- 文档版本号必须递增
- 变更内容必须记录在变更记录中

### 任务完成输出

每次完成任务后，**必须**输出：

```markdown
## 任务完成摘要

### 新增测试文件
- `path/to/file1.test.ets` - 文件说明

### 新增测试设计文档
- `path/to/file1.test.design.md` - 设计文档说明

### 修改文件
- `path/to/file2.ets` - 修改说明

### 测试覆盖统计
- 新增测试用例数：XX 个
- 新增测试设计文档：XX 个
- 覆盖的 API：XX 个
```

> 📖 **完整的使用方式请查看**: [docs/USAGE.md](./docs/USAGE.md)

## 重要注意事项

### 1. @tc 注释块规范（强制）

- 所有测试用例（`it()` 函数）**必须**在前面添加标准的 `@tc` 注释块
- `@tc.name`：必须使用小驼峰命名（camelCase），必须与 `it()` 第一个参数完全一致
  - 详见：[references/subsystems/_common.md](./references/subsystems/_common.md) 命名规范
- `@tc.number`：格式为 `{describe名}_{序号}`，序号从001开始补零对齐
- `@tc.desc`：格式为 `{API名} {错误码/场景} test.`，必须以 `. ` 结尾
- `@tc.type`、`@tc.size`、`@tc.level`：必须与 `it()` 第二个参数中的值一致

### 2. hypium 导入规范（强制）

- 基本导入：`describe, it, expect`（必需）
- 类型导入：`TestType, Level, Size`（必需）
- 条件导入：`beforeAll, afterAll`（根据代码需要）
- 自动检测并补充缺失的导入

### 3. 工程文件修改限制（强制）

- **严格禁止修改**工程目录中的配置文件
- **仅允许修改**：`entry/src/ohosTest/ets/test/` 目录中的测试文件
- **违反限制的后果**：可能导致工程结构被破坏、编译失败

### 4. 清理操作安全注意事项（强制）

**⚠️ 关键警告**：预编译清理操作必须谨慎执行，避免误删系统编译环境。

**安全清理要求**：
1. **确认当前目录**：执行清理命令前必须确认当前工作目录
   ```bash
   cd {OH_ROOT}/test/xts/acts/testfwk/{test_suite}
   pwd  # 必须确认当前目录
   ```

2. **使用显式路径删除**：删除命令必须使用显式路径（`./` 前缀或绝对路径）
   ```bash
   # ✅ 正确：使用显式相对路径
   rm -rf ./.hvigor ./build ./entry/build ./oh_modules
   rm -f ./oh-package-lock.json5 ./local.properties

   # ❌ 错误：不使用路径前缀（可能误删 OH_ROOT/build）
   rm -rf build
   ```

3. **分步清理验证**：
   - 步骤1：清理测试套缓存并验证
   - 步骤2：清理 OH_ROOT/out 目录
   - 步骤3：验证 OH_ROOT/build 目录安全

4. **禁止操作**：
   - ❌ 在 OH_ROOT 目录执行 `rm -rf build`
   - ❌ 一次性清理多个目录
   - ❌ 不验证当前目录就执行删除

**参考文档**：`modules/L4_Build/linux_prebuild_cleanup.md` 1.3 节

### 5. XTS Wiki 文档参考（强制）

- 生成 XTS 测试用例时，**必须**参考 Wiki 文档中的规范
- Wiki 文档规范 > Template 配置 > 通用模板

### 6. ArkTS 语法类型识别（重要）

- **API 类型判断**：必须读取 `.d.ts` 文件中**最后一段 JSDOC** 的 `@since` 标签
- **工程类型识别**：读取 `build-profile.json5` 检查 `arkTSVersion` 字段
- **兼容性检查**：生成测试用例前，必须检查工程语法类型与 API 类型是否匹配

### 7. ArkTS 静态语言语法规范校验（可选）

**触发条件**：用户明确要求生成静态 XTS 用例时自动启用

**规范文档**：`references/arkts-static-spec/`

### 8. 编译环境检测（强制）

#### 7.1 Linux 环境编译

**基础要求**：
- 使用 `build.sh` 脚本编译，**不要使用 `hvigorw`**
- 环境检测：`uname -s`

**编译流程**：
1. **预编译清理**（强制）：
   - 使用 `cleanup_group.sh` 脚本
   - 清理目的：确保编译结果包含所有最新代码
   - ⚠️ 安全注意事项：见第 3.1 节清理操作安全说明

2. **静态测试套预置条件**（编译静态套时）：
   - 校验 hvigor 版本：`"6.0.0-arkts1.2-ohosTest-25072102"`
   - 版本匹配：跳过工具替换；版本不匹配：执行替换流程
   - 工具替换：清理 SDK 缓存 → 清理旧工具 → 下载新工具 → 移动到预置目录

3. **编译执行**：
   - 使用 general subagent 执行（避免主流程中断）
   - 监听编译进程直至完成
   - **语法错误**：自动分析并修复，重试编译
   - **配置错误**：暂停并向用户确认后才修改

#### 7.2 Windows 环境编译

根据关键词自动选择编译模式：

##### 7.2.1 ArkTS 动态 XTS 编译（默认）
- **编译方式**：DevEco Studio IDE 或 `hvigorw.bat`
- **编译目标**：`Build → Build OhosTest Hap(s)`
- **参考文档**：`modules/L4_Build/build_workflow_windows.md` 第三章

##### 7.2.2 ArkTS 静态 XTS 编译（arkts-sta）
- **适用场景**：基于 ArkTS 静态强类型语法的 XTS 测试 工程
- **触发关键词**：当用户提到以下任一关键词时自动启用：
  - **技术术语**：`arkts-sta`、`ArkTS静态`、`arkts static`、`ArkTS static`
  - **通用表述**：`静态xts`、`静态 XTS`、`static arkts`、`static xts`
  - **操作描述**：`编译静态`、`静态编译`、`静态工程编译`、`Windows静态编译`
- **编译方式**：PowerShell 脚本或 `hvigorw.bat` 命令行工具
- **Java 环境**：**必需**配置 JAVA_HOME 环境变量
- **编译特点**：
  - 严格的静态类型检查
  - 所有类型必须有显式注解
  - 禁止使用 any 类型
  - 所有字段必须初始化
- **参考文档**：`modules/L4_Build/build_workflow_windows.md` 第十章

> **⚠️ 重要提示**：
> - 默认使用动态编译模式
> - 仅在用户明确提到静态相关关键词时启用静态编译模式
> - 静态编译需要配置 Java 环境变量（JAVA_HOME）

> 📖 **详细的编译文档**: [modules/L4_Build/](./modules/L4_Build/)

## 故障排除

> 📖 **详细故障排除指南**: [docs/TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md)

**常见问题**：
- Q1: 生成的测试用例无法编译
- Q2: 测试用例命名不符合规范
- Q3: 测试设计文档与测试用例不一致
- Q4: Linux 环境编译失败
- Q5: 测试用例执行失败
- Q6: 子系统配置文件未找到
- Q7: 测试覆盖率分析不准确

## 版本信息

- **当前版本**: 1.20.2
- **创建日期**: 2025-01-31
- **最后更新**: 2026-02-12
- **兼容性**: OpenHarmony API 10+
- **基于**: OH_XTS_GENERATOR v1.7.0

## 版本历史

详细的版本历史记录请查看 [CHANGELOG.md](./CHANGELOG.md)

**最近更新**：
- v1.20.2 (2026-02-12): 简化重复内容，优化文档结构
- v1.20.1 (2026-02-12): 优化核心工作流程和注意事项的重复内容
- v1.20.0 (2026-02-11): 强化清理操作安全注意事项
- v1.19.0 (2026-02-11): 强化预编译清理的强制执行
- v1.18.0 (2026-02-11): 添加 hvigor 工具版本校验机制

## 参考文档

### 详细文档

- **模块化架构详解**: [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)
- **配置扩展机制**: [docs/CONFIG.md](./docs/CONFIG.md)
- **使用方式详解**: [docs/USAGE.md](./docs/USAGE.md)
- **故障排除**: [docs/TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md)

### 子模块文档

- **L1_Framework**: [modules/L1_Framework/](./modules/L1_Framework/)
- **L2_Analysis**: [modules/L2_Analysis/](./modules/L2_Analysis/)
- **L3_Generation**: [modules/L3_Generation/](./modules/L3_Generation/)
- **L4_Build**: [modules/L4_Build/](./modules/L4_Build/)

### 通用配置

- **通用配置**: [references/subsystems/_common.md](./references/subsystems/_common.md)

