---
name: flutter-skills
version: 1.0.0
description: Flutter开发完整指南：Clean Architecture架构规范、TDD测试工作流、BLoC状态管理、故障排除与代码生成
dependency:
  python:
    - argparse
---

# Flutter Skills

## 任务目标
- 本 Skill 用于：提供现代 Flutter 开发的完整指南，涵盖架构设计、测试流程、故障排除和代码生成
- 能力包含：Clean Architecture 规范、TDD 工作流、BLoC 状态管理、故障诊断、代码生成脚本、智能助手
- 触发条件：用户询问 Flutter 架构设计、TDD 测试、状态管理、项目结构、代码生成、故障排除或第三方库选型

## 前置准备
- 依赖说明：无额外依赖
- 项目环境：Flutter SDK 3.x、Dart SDK 3.x

## 快速导航

### 📚 文档索引
- **快速查找**：[INDEX.md](INDEX.md) - 所有资源的快速索引
- **场景映射**：[SCENARIOS.md](SCENARIOS.md) - 用户意图到资源的映射

### 🤖 智能助手触发
| 触发方式 | Agent |
|----------|-------|
| "请帮我用 TDD 实现" | [TDD Coach](references/agents/tdd-coach.md) |
| "请审查这段代码" | [Code Reviewer](references/agents/code-reviewer.md) |
| "编写测试" | [Test Writer](references/agents/test-writer.md) |
| "审查架构" | [Architecture Reviewer](references/agents/architecture-reviewer.md) |

## 操作步骤

### 标准流程

1. **架构设计与规划**
   - 阅读 [architecture-guide.md](references/architecture-guide.md)
   - 使用 [INDEX.md](INDEX.md) 快速查找相关资源

2. **功能模块生成（脚本）**
   ```bash
   python scripts/generate_feature.py --feature-name <name>
   python scripts/generate_model.py --model-name <name> --fields <spec>
   python scripts/generate_bloc.py --bloc-name <name> --feature <feature>
   python scripts/generate_test.py --source <file_path>
   ```

3. **TDD 开发流程（Agent + 指导）**
   - 触发 TDD Coach Agent
   - 参考 [testing-guide.md](references/testing-guide.md)
   - 触发 Test Writer Agent 生成测试

4. **代码质量保障（Agent）**
   - 触发 Code Reviewer Agent 审查代码
   - 触发 Architecture Reviewer Agent 审计架构

5. **故障排除（诊断）**
   - 构建错误 → [build-errors.md](references/diagnostic/build-errors.md)
   - 运行时错误 → [runtime-errors.md](references/diagnostic/runtime-errors.md)
   - 状态问题 → [state-debugging.md](references/diagnostic/state-debugging.md)
   - 性能问题 → [performance-profiler.md](references/diagnostic/performance-profiler.md)

### 决策流程

使用 [SCENARIOS.md](SCENARIOS.md) 中的决策树快速定位：

```
用户请求
├─ 创建/生成 → scripts/ + commands-guide.md
├─ TDD 开发 → agents/tdd-coach.md + testing-guide.md
├─ 审查代码 → agents/code-reviewer.md
├─ 审查架构 → agents/architecture-reviewer.md
├─ 编写测试 → agents/test-writer.md
└─ 故障排除 → references/diagnostic/
```

## 资源索引

### 脚本工具（scripts/）
| 脚本 | 功能 |
|------|------|
| [generate_feature.py](scripts/generate_feature.py) | 生成 Feature 结构 |
| [generate_model.py](scripts/generate_model.py) | 生成 Freezed 模型 |
| [generate_bloc.py](scripts/generate_bloc.py) | 生成 BLoC 结构 |
| [generate_test.py](scripts/generate_test.py) | 生成测试模板 |

### 核心参考文档
- [architecture-guide.md](references/architecture-guide.md) - Clean Architecture、BLoC、依赖注入
- [testing-guide.md](references/testing-guide.md) - TDD、测试模式、Mocking
- [packages-guide.md](references/packages-guide.md) - 库选型指南（40+ 库）
- [commands-guide.md](references/commands-guide.md) - Flutter 命令参考

### 详细技能文档（references/skills/）
- **Architecture**（5个）：bloc-architecture, clean-architecture, dependency-injection, error-handling, feature-structure
- **Testing**（5个）：bloc-testing, mocking-patterns, tdd-workflow, unit-testing, widget-testing
- **Generation**（1个）：screen

### 详细命令文档（references/commands/）
- 代码生成：generate-bloc, generate-feature, generate-model, generate-test
- 构建工具：build-runner, clean-rebuild
- 测试工具：flutter-test, flutter-coverage
- 代码质量：flutter-lint

### 诊断指南（references/diagnostic/）
- [build-errors.md](references/diagnostic/build-errors.md) - 构建错误诊断
- [runtime-errors.md](references/diagnostic/runtime-errors.md) - 运行时错误诊断
- [state-debugging.md](references/diagnostic/state-debugging.md) - 状态调试
- [performance-profiler.md](references/diagnostic/performance-profiler.md) - 性能分析

### 智能助手（references/agents/）
- [tdd-coach.md](references/agents/tdd-coach.md) - TDD 流程指导
- [code-reviewer.md](references/agents/code-reviewer.md) - 代码审查
- [test-writer.md](references/agents/test-writer.md) - 测试生成
- [architecture-reviewer.md](references/agents/architecture-reviewer.md) - 架构审计

## 五类能力概览

### 1. Discipline-Enforcing Skills（强制工作流）
强制执行的开发规范和流程。
- [testing-guide.md](references/testing-guide.md) - TDD 流程和测试模式
- [architecture-guide.md](references/architecture-guide.md) - 架构规范
- **相关 Agents**：TDD Coach, Code Reviewer

### 2. Reference Skills（参考指南）
综合性的技术参考文档。
- [architecture-guide.md](references/architecture-guide.md)
- [testing-guide.md](references/testing-guide.md)
- [packages-guide.md](references/packages-guide.md) - 40+ 库的完整指南
- [commands-guide.md](references/commands-guide.md)

### 3. Diagnostic Skills（故障排除）
系统性的问题诊断和故障排除方法。
- [build-errors.md](references/diagnostic/build-errors.md)
- [runtime-errors.md](references/diagnostic/runtime-errors.md)
- [state-debugging.md](references/diagnostic/state-debugging.md)
- [performance-profiler.md](references/diagnostic/performance-profiler.md)

### 4. Commands（命令脚本）
快速自动化操作和脚手架工具。
- `scripts/generate_feature.py`
- `scripts/generate_model.py`
- `scripts/generate_bloc.py`
- `scripts/generate_test.py`

### 5. Agents（智能助手）
自然语言触发的自动化助手。
- **TDD Coach** - 指导 TDD 流程
- **Code Reviewer** - 审查代码质量
- **Test Writer** - 生成测试代码
- **Architecture Reviewer** - 审计架构合规性

## 使用示例

### 示例 1：创建用户认证功能（TDD 流程）
```bash
# 1. 生成结构
python scripts/generate_feature.py --feature-name auth
python scripts/generate_model.py --model-name user --fields id:String,email:String,name:String

# 2. 请求 TDD Coach："请帮我用 TDD 实现用户登录功能"
#    → 智能体扮演 TDD Coach 指导 Red/Green/Refactor 循环

# 3. 请求 Code Reviewer 审查代码

# 4. 生成代码
dart run build_runner build --delete-conflicting-outputs
```

### 示例 2：诊断运行时错误
```
用户: "应用崩溃了，帮我诊断"

智能体:
1. 查阅 [runtime-errors.md](references/diagnostic/runtime-errors.md)
2. 分析错误信息和堆栈跟踪
3. 提供修复建议和预防措施
```

### 示例 3：代码审查
```
用户: "请审查这段代码"

智能体:
1. 触发 Code Reviewer Agent
2. 进行全面审查（架构、代码质量、安全性）
3. 提供问题列表和修复建议
```

## 注意事项

- **Agent 优先**：遇到复杂任务时优先触发对应的 Agent
- **渐进式加载**：先读取核心指南，需要时再读取详细技能
- **场景映射**：使用 [SCENARIOS.md](SCENARIOS.md) 快速定位资源
- **快速索引**：使用 [INDEX.md](INDEX.md) 查找特定主题
- **上下文保持**：在同一会话中保持上下文，避免重复读取

## 技术栈版本

- Flutter SDK: 3.x
- Dart SDK: 3.x
- 关键库版本：见 [packages-guide.md](references/packages-guide.md)

## 项目统计

- 总文档数: 26+
- 脚本工具: 4
- 智能助手: 4
- 详细技能文档: 11
- 详细命令文档: 9
- 诊断指南: 4
- 覆盖库数量: 40+
