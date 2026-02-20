---
name: pythonic-style
version: 1.0.0
description: Python代码风格优化与Pythonic惯用法指导；基于《One Python Craftsman》完整内容和"Friendly Python"理念，涵盖变量命名、控制流、数据类型、容器类型、函数设计、异常处理、装饰器、文件操作、SOLID原则；提供用户友好和维护友好的设计模式、审查清单和140+实战模板
---

# Pythonic Code Style

## 任务目标
- 本 Skill 用于：分析和改进 Python 代码风格，使其更符合 Python 语言特性和最佳实践
- 能力包含：
  - **代码风格分析**：识别非 Pythonic 模式，提供改进建议
  - **Pythonic 惯用法**：列表推导、生成器、上下文管理器、装饰器、元类等
  - **设计模式应用**：SOLID 原则、描述符协议、迭代器协议等
  - **性能优化**：内存优化、计算优化、I/O 优化、并发模式、缓存策略
  - **重构指导**：代码异味检测、重构技巧、重构模式、重构流程
  - **实战模板**：提供可直接使用的代码模板（140+ 个）

- 触发条件：
  - 用户展示代码并请求"如何更 Python 地实现"
  - 用户询问"这段代码是否 Pythonic"
  - 用户需要代码审查和风格改进建议
  - 用户询问 Python 特定语法的最佳实践
  - 用户需要性能优化或重构建议
  - 用户请求高级 Python 模式或设计模式

## 核心理念

### Friendly Python = User-Friendly + Maintainer-Friendly

```
┌──────────────────────────────────────────────────────────┐
│           FRIENDLY PYTHON = User-Friendly Python         │
├────────────────────────────────┬─────────────────────────┤
│   User-Friendly               │   Maintainer-Friendly     │
│   ─────────────────           │   ─────────────────      │
│   • Sensible defaults         │   • Single change point  │
│   • Minimal required params   │   • Registry over if-else│
│   • Hidden resource mgmt      │   • Explicit over magic  │
│   • Simple → complex path     │   • Readable & debuggable│
└────────────────────────────────┴─────────────────────────┘
```

### 设计原则

#### 1. 用户友好 (User-Friendly)
- **默认提供合理值**：让快速启动无需阅读文档
- **最少必需参数**：隐藏复杂的对象组装
- **透明的资源管理**：使用上下文管理器或统一入口
- **简单到复杂**：简单路径是默认，复杂需求可显式扩展

#### 2. 维护友好 (Maintainer-Friendly)
- **单点修改**：添加新策略/命令/实现时，收敛到一个修改点
- **注册表替代 if-else**：使用注册表/插件表替代条件分支链
- **谨慎使用魔法**：自动扫描和动态导入需要评估可读性和可调试性

#### 3. 构建模式
- **避免半成品对象**：不推荐"实例化后加载"；使用 `classmethod` 构建
- **多源多入口**：env/file/显式使用不同的构建入口，不在 `__init__` 用标志
- **减少导入负担**：不暴露不必要的命名到包顶层

#### 4. 生态扩展
- **使用扩展点**：hook、adapter、auth、middleware
- **避免猴子补丁**：改用注册、协议、继承
- **包装而非重写**：扩展功能而非覆盖全部

#### 5. 明确性
- **避免 `__getattr__**：优先显式字段和描述符
- **谨慎使用元类**：只在必要时使用
- **显式优于隐式**：优先可读性而非炫技

## 操作步骤

```
┌─────────────────────────────────────────────────────────────┐
│  1. UNDERSTAND: 理解需求与现有代码                          │
├─────────────────────────────────────────────────────────────┤
│  2. ANALYZE: 分析代码风格问题，识别非 Pythonic 模式         │
├─────────────────────────────────────────────────────────────┤
│  3. IMPROVE: 应用 Pythonic 惯用法和设计模式                 │
├─────────────────────────────────────────────────────────────┤
│  4. REVIEW: 根据审查清单检查改进方案                        │
├─────────────────────────────────────────────────────────────┤
│  5. REFINE: 优化细节，提供替代方案和权衡分析                │
└─────────────────────────────────────────────────────────────┘
```

### 标准流程：
1. **代码分析**
   - 阅读用户提供的代码，识别非 Pythonic 的模式
   - 参考 [references/python-rules.md](references/python-rules.md) 中的 Python 之禅和规范
   - 关注：命名规范、控制流、数据类型使用、函数设计、异常处理等

2. **Pythonic 改进**
   - 根据问题类型选择合适的参考文档
   - **基础改进**：[references/control-flow.md](references/control-flow.md)、[references/data-types.md](references/data-types.md)、[references/functions.md](references/functions.md)
   - **高级特性**：[references/decorators.md](references/decorators.md)、[references/advanced-patterns.md](references/advanced-patterns.md)
   - **性能优化**：[references/performance-tips.md](references/performance-tips.md)
   - **重构指导**：[references/refactoring-guide.md](references/refactoring-guide.md)
   - 应用 Pythonic 惯用法：列表推导、生成器、上下文管理器、装饰器等
   - 参考 [assets/templates/](assets/templates/) 中的标准模板

3. **代码对比与解释**
   - 展示改进前后的代码对比
   - 解释改进的理由和遵循的 Pythonic 原则
   - 说明性能、可读性和维护性的提升
   - 必要时提供替代方案和权衡分析

4. **最佳实践与进阶建议**
   - 根据 [references/solid-principles.md](references/solid-principles.md) 提供设计原则建议
   - 参考 [references/edge-cases.md](references/edge-cases.md) 处理边界情况
   - 提供相关 Pythonic 模式的学习资源和进一步优化方向

### 可选分支：
- **基础风格问题**：使用基础参考文档提供改进建议
- **高级特性应用**：推荐使用描述符、元类、迭代器协议等高级模式
- **性能优化需求**：结合性能优化参考文档提供建议
- **重构需求**：使用重构指南提供系统性改进方案
- **代码已经较好**：识别可进一步优化的细节，提供高级优化建议

## 审查清单

使用此清单进行代码审查或自查：

| 检查项 | 问题 |
|--------|------|
| 🔧 **扩展性** | 新增功能是否只需修改一处代码？ |
| 🎯 **默认值** | API 是否有合理的默认值？是否隐藏了不必要的对象？ |
| 📈 **复杂度** | 复杂度是否遵循"简单到复杂"，默认路径是否最轻量？ |
| 🔌 **扩展点** | 是否优先使用生态系统的扩展点？ |
| 👁️ **明确性** | 是否为了炫技而牺牲了明确性和可维护性？ |
| 🔄 **移植代码** | 移植代码时是否重新设计了调用模式？ |

## 推荐与避免的模式

### 推荐使用的模式

| 场景 | 推荐做法 |
|------|----------|
| 多种实现方式 | 注册表模式 + 装饰器注册 |
| 资源管理 | 上下文管理器 (`with`) |
| 多种输入来源 | `@classmethod` 构造器 |
| 配置字段 | 描述符 (Descriptor) |
| 扩展第三方库 | 官方扩展点 (hook/adapter/auth) |
| 异步操作 | async/await + try/except/finally |
| CLI 工具 | argparse + Command 类 |
| 复杂对象构建 | Builder 模式 |
| 策略选择 | 注册表/字典查找 |
| 循环导入 | 延迟导入/重构模块 |

### 避免使用的模式

| 反模式 | 问题 |
|--------|------|
| 大量 if-else 分支 | 添加功能需要修改多处 |
| `__init__` 中使用标志控制路径 | 互斥参数不明确 |
| `__getattr__` 回退 | 削弱可发现性和类型检查 |
| 过度使用元类 | 污染用户的心智模型 |
| 自定义包装回原库 | 属性重复，维护负担 |
| JS 风格的回调 | 不 Pythonic |
| 全局状态 | 难以测试和维护 |
| 过度继承 | 组合优于继承 |
| 硬编码配置 | 缺乏灵活性 |
| 裸 except | 吞掉所有异常 |

## 响应格式

解决代码风格问题时，使用以下格式：

```markdown
## Summary
[完成的工作总结]

## Changes Made
- [改进点 1]: [说明]
- [改进点 2]: [说明]

## Design Decisions
- [为什么选择某些模式]

## Review Checklist
- [x] 单点扩展性
- [x] 合理默认值
- [x] 渐进式复杂度
- [x] 正确使用扩展点
- [x] 明确性优于魔法

## Suggestions (if any)
- [可以进一步改进的地方]
```

## 资源索引

### 基础参考
- **友好模式**：见 [references/friendly-patterns.md](references/friendly-patterns.md)（Friendly Python 理念、用户友好模式、维护友好模式、构建模式、注册表模式、上下文管理器）
- **Python 规则**：见 [references/python-rules.md](references/python-rules.md)（Python 之禅、PEP 8 规范）
- **变量命名**：见 [references/variables-naming.md](references/variables-naming.md)（命名原则、布尔变量命名、循环变量命名、临时变量）
- **控制流**：见 [references/control-flow.md](references/control-flow.md)（if-else 优化、卫语句、提前返回、海象运算符、循环优化、match-case）
- **数字和字符串**：见 [references/data-types.md](references/data-types.md)（数字操作、字符串处理、格式化、正则表达式、类型转换）
- **容器类型**：见 [references/container-types.md](references/container-types.md)（列表、字典、集合、元组最佳实践、推导式、collections 模块）
- **函数设计**：见 [references/functions.md](references/functions.md)（函数设计原则、参数设计、返回值设计、类型提示、高阶函数）
- **异常处理**：见 [references/exceptions.md](references/exceptions.md)（异常处理最佳实践、上下文管理器）
- **装饰器**：见 [references/decorators.md](references/decorators.md)（装饰器深入应用、类装饰器、参数化装饰器）
- **循环导入**：见 [references/cyclic-imports.md](references/cyclic-imports.md)（循环导入的定义、原因、后果和解决方法）
- **文件操作**：见 [references/file-operations.md](references/file-operations.md)（文件读写、路径处理、pathlib）

### 进阶参考
- **SOLID 原则**：见 [references/solid-principles.md](references/solid-principles.md)（面向对象设计原则、设计模式）
- **高级模式**：见 [references/advanced-patterns.md](references/advanced-patterns.md)（元类、描述符、迭代器协议、并发、魔术方法）
- **性能优化**：见 [references/performance-tips.md](references/performance-tips.md)（性能分析、内存优化、计算优化、并发、缓存）
- **重构指南**：见 [references/refactoring-guide.md](references/refactoring-guide.md)（代码异味、重构技巧、重构模式、重构工具）
- **边界情况**：见 [references/edge-cases.md](references/edge-cases.md)（异常和边界情况处理）

### 代码模板
- **基础模板**：见 [assets/templates/naming-patterns.py](assets/templates/naming-patterns.py)、[assets/templates/control-flow-patterns.py](assets/templates/control-flow-patterns.py)、[assets/templates/string-number-operations.py](assets/templates/string-number-operations.py)、[assets/templates/container-operations.py](assets/templates/container-operations.py)、[assets/templates/exception-handling.py](assets/templates/exception-handling.py)
- **高级模板**：见 [assets/templates/advanced-patterns.py](assets/templates/advanced-patterns.py)（元类、描述符、迭代器、装饰器、并发等高级模式）
- **性能模板**：见 [assets/templates/performance-patterns.py](assets/templates/performance-patterns.py)（缓存、批处理、惰性求值、并行处理等性能模式）

## 核心原则

基于 Python 之禅和 Friendly Python 的核心价值观：
- **优美胜于丑陋**：优先选择简洁、优雅的解决方案
- **明了胜于晦涩**：代码应该清晰易懂，避免过度设计
- **简洁胜于复杂**：用最少的代码完成任务，避免不必要的复杂性
- **复杂胜于凌乱**：使用有组织的复杂结构，而非混乱的代码
- **扁平胜于嵌套**：减少嵌套层级，提高代码可读性
- **间隔胜于紧凑**：合理的空行和空格，让代码更易读
- **可读性很重要**：代码是给人读的，清晰度优先
- **实用性胜于纯粹性**：考虑实际应用场景和性能需求
- **用户友好 + 维护友好**：API 易于使用，代码易于维护

### 实现方式说明

本 Skill 的所有功能由智能体通过自然语言指导完成，无需脚本执行：
- **代码分析与改进**：智能体直接分析代码并提供 Pythonic 改进建议
- **模板推荐**：从 `assets/templates/` 中选择合适的模板并展示使用方法
- **最佳实践指导**：基于参考文档提供详细的指导和示例

## 使用示例

### 示例 1：友好模式应用
- **功能说明**：应用注册表模式替代 if-else 分支，提高代码可扩展性
- **执行方式**：分析现有代码结构，重构为注册表模式
- **参考文档**：[references/friendly-patterns.md](references/friendly-patterns.md)
- **关键要点**：
  - 识别大量 if-else 分支
  - 使用注册表装饰器替代条件链
  - 新增功能只需注册，无需修改核心代码
  - 保持代码的可读性和可维护性

### 示例 2：基础循环改进
- **功能说明**：将传统的 for 循环转换为列表推导或生成器表达式
- **执行方式**：智能体分析代码并提供改进建议
- **参考文档**：[references/control-flow.md](references/control-flow.md)
- **关键要点**：
  - 识别可转换的循环模式
  - 使用列表推导简化代码
  - 使用生成器表达式处理大数据
  - 保持代码可读性

### 示例 2：命名规范优化
- **功能说明**：改进变量、函数、类的命名
- **执行方式**：提供更清晰、更具描述性的命名建议
- **参考文档**：[references/variables-naming.md](references/variables-naming.md)
- **模板参考**：[assets/templates/naming-patterns.py](assets/templates/naming-patterns.py)
- **关键要点**：
  - 使用有意义的名称
  - 遵循命名约定（snake_case、CamelCase）
  - 避免缩写和歧义
  - 使用动词命名函数，名词命名类

### 示例 3：异常处理改进
- **功能说明**：改进异常处理方式和资源管理
- **执行方式**：推荐使用更 Python 的异常处理模式
- **参考文档**：[references/exceptions.md](references/exceptions.md)
- **模板参考**：[assets/templates/exception-handling.py](assets/templates/exception-handling.py)
- **关键要点**：
  - 捕获特定的异常类型
  - 使用上下文管理器管理资源
  - 提供有用的错误消息
  - 避免裸 except

### 示例 4：函数设计优化
- **功能说明**：优化函数设计和参数传递
- **执行方式**：提供函数重写建议
- **参考文档**：[references/functions.md](references/functions.md)
- **关键要点**：
  - 遵循单一职责原则
  - 合理使用默认参数和可变参数
  - 使用类型提示提高可读性
  - 返回一致的结果类型

### 示例 5：高级模式应用
- **功能说明**：应用元类、描述符、迭代器协议等高级模式
- **执行方式**：分析需求并推荐合适的高级模式
- **参考文档**：[references/advanced-patterns.md](references/advanced-patterns.md)
- **模板参考**：[assets/templates/advanced-patterns.py](assets/templates/advanced-patterns.py)
- **关键要点**：
  - 理解适用场景和权衡
  - 正确实现协议和魔术方法
  - 保持代码可读性和可维护性
  - 避免过度设计

### 示例 6：性能优化
- **功能说明**：提供性能优化建议
- **执行方式**：分析代码并提供优化方案
- **参考文档**：[references/performance-tips.md](references/performance-tips.md)
- **模板参考**：[assets/templates/performance-patterns.py](assets/templates/performance-patterns.py)
- **关键要点**：
  - 使用性能分析工具识别瓶颈
  - 选择合适的数据结构和算法
  - 使用缓存和批处理
  - 考虑并发和异步处理

### 示例 7：代码重构
- **功能说明**：系统性地改进代码结构和质量
- **执行方式**：提供重构方案和步骤
- **参考文档**：[references/refactoring-guide.md](references/refactoring-guide.md)
- **关键要点**：
  - 识别代码异味
  - 小步重构，保持测试通过
  - 提取方法和类，减少重复
  - 简化条件和复杂逻辑

## 注意事项
- 优先使用 Python 内置功能和标准库，避免重复造轮子
- Pythonic 不等于最简代码，要在简洁和可读性之间平衡
- 遵循 PEP 8 代码风格规范
- 充分利用 Python 的动态特性和语法糖
- 考虑代码的性能和维护性，避免过度优化
- 理解 SOLID 原则，编写可维护的面向对象代码
- 正确处理边界情况和异常
- 高级模式使用时考虑适用场景和可维护性
- 性能优化前先测量，避免过早优化
- 重构时保持测试通过，逐步改进
- 遵循 "用户友好 + 维护友好" 的设计理念
- 使用审查清单确保代码质量
- 优先选择推荐模式，避免反模式
