---
name: python-team
version: 1.0.0
description: 通过自主学习、PM、架构师、高级程序员四角色协同，从自然语言需求自动生成完整Python项目交付物。支持功能扩展、项目重构、技能调用。支持网络搜索、知识整合、版本控制、Python 3.11+特性、UV包管理、loguru日志、项目规模自适应（文件夹/单文件）。支持数据库设计与实现（SQLite、PostgreSQL、MongoDB、向量数据库、图数据库）、数据层抽象（Repository 模式）、数据库切换。适用于软件需求澄清、快速原型开发、项目初始化、功能扩展、代码重构等场景。
---

# Python 团队协同开发 Skill

## 任务目标
- 本 Skill 用于：通过虚拟四角色团队（自主学习→PM→架构师→高级程序员）协同工作，将用户的自然语言需求转化为完整的 Python 项目交付物
- 能力包含：自主学习与知识整合、需求分析与澄清、架构设计（自适应项目规模）、代码实现、功能验证、版本控制、**功能扩展、项目重构、技能识别与调用、数据库设计与实现、数据层抽象**
- 触发条件：用户提出明确的软件开发需求（如"做一个天气查询工具"、"实现一个待办事项系统"、"添加数据导出功能"、"优化代码性能"、"设计用户管理系统"等）

## 前置准备
- 依赖说明：web_search 工具（已集成）
- 包管理工具：**UV**（现代 Python 包管理器，快速、可靠、锁定依赖）
  - 安装：`pip install uv`
  - 项目初始化：`uv init`
  - 依赖管理：`uv add package`
- 文件准备：无需前置文件
- **版本控制机制**：所有文档和代码必须包含版本信息，使用语义化版本（Semantic Versioning，如 v1.0.0），记录版本历史和变更原因

## 操作步骤

### 阶段0：自主学习与知识整合
**目标**：通过网络搜索获取相关领域知识，生成项目背景文档，为后续阶段提供知识支撑

**执行步骤**：
1. **识别关键词**：从用户需求中提取核心技术、领域、工具关键词
   - 技术关键词：如"REST API"、"WebSocket"、"CSV处理"、"数据库"、"ORM"
   - 领域关键词：如"天气查询"、"待办事项"、"数据分析"、"用户管理"
   - 工具关键词：如"Flask"、"pandas"、"UV"、"SQLAlchemy"、"MongoDB"

2. **执行网络搜索**（3-6轮）：
   - 第1轮：搜索"<领域> 最佳实践"，获取通用设计原则
   - 第2轮：搜索"<技术> 框架对比"，如"Flask vs FastAPI 对比"
   - 第3轮：搜索"<功能> 实现方案"，如"Python 天气API调用示例"
   - 第4轮（可选）：搜索"<问题> 常见坑"，如"REST API 常见错误"
   - 第5轮：搜索"Python 3.11+ 新特性"、"框架版本兼容性"、"UV 包管理器最佳实践"、"loguru 日志库最佳实践"
   - 第6轮（新增）：搜索"数据库选型"、"SQLAlchemy vs MongoDB"、"向量数据库对比"、"图数据库对比"、"Repository 模式最佳实践"、"数据库性能优化"

3. **筛选与整合信息**：
   - 评估搜索结果的可信度和时效性
   - 提取关键信息：技术选型依据、设计模式、最佳实践、常见问题、版本特性、UV 使用、数据库选型
   - 整合冲突信息，标注不同方案的优缺点
   - **重点关注**：版本兼容性、长期维护性、学习资源、UV 包管理优势、数据库特性
   - 生成结构化的知识总结

4. **生成 `docs/background.md`**：
   - 参考 [references/background-template.md](references/background-template.md) 的结构
   - 包含：项目背景概述、技术领域知识、最佳实践、工具对比（含版本信息）、常见问题、UV 包管理、**数据库相关知识**
   - **增强**：工具对比维度增加版本兼容性、长期维护性、学习资源
   - **增强**：数据库选型指南（SQLite、PostgreSQL、MongoDB、向量数据库、图数据库）
   - **增强**：数据库设计与实现最佳实践（ORM/ODM、索引策略、性能优化）
   - 确保信息准确、实用、易于理解

### 阶段1：项目经理（PM）- 需求分析与文档化
**目标**：结合背景知识理解用户需求，生成清晰的需求文档，评估项目规模

**执行步骤**：
1. **结合背景知识分析需求**：
   - 阅读 `docs/background.md`，了解领域最佳实践和常见陷阱
   - 识别用户需求中可能遗漏的关键点（基于领域知识）
   - 评估需求的合理性和可行性

2. 识别需求中的模糊点或不完整之处
3. **最多进行2轮澄清交互**（如果需求不明确）：
   - 以"【提问】"开头向用户确认细节
   - 典型问题：功能边界、输入输出格式、非功能要求、技术栈偏好、版本要求、项目规模预期等
   - 示例："做一个天气查询工具" → 澄清"支持哪些城市？数据来源？是否缓存？"
4. **评估项目规模**：
   - **小项目**：< 5 个功能点，< 500 行代码预期
   - **中型项目**：5-10 个功能点，500-2000 行代码预期
   - **大项目**：> 10 个功能点，> 2000 行代码预期
   - 在 `requirements.md` 中明确标注项目规模

5. **数据库需求澄清**（新增）：
   - 确认是否需要数据持久化存储
   - 确认数据类型（关系型、文档型、向量、图）
   - 确认数据规模和并发需求
   - 确认是否需要多数据库支持
   - 确认是否需要数据库切换能力

6. 基于用户反馈、背景知识和项目规模评估，生成 `docs/requirements.md`：
   - 参考 [references/requirements-template.md](references/requirements-template.md) 的结构
   - 包含：功能列表、输入输出说明、非功能性要求、假设与约束、版本要求、项目规模、**数据库需求**
   - **关键**：参考 background.md 中的最佳实践，完善非功能性要求
   - **新增**：明确 Python 3.11+ 版本要求、版本控制策略、UV 包管理要求、项目规模、loguru 日志库要求（强制使用）、数据库选型要求（参考 database-selection-guide.md）
   - 确保每个功能点都清晰可执行
   - 记录版本：v1.0.0（初始版本）

### 阶段2：系统架构师（Architect）- 架构设计
**目标**：基于需求文档、背景知识和项目规模，设计系统架构，生成设计文档和任务清单

**执行步骤**：
1. 阅读 `docs/requirements.md` 和 `background.md`，理解完整需求、领域知识、项目规模和数据库需求
2. **根据项目规模选择架构组织方式**：
   - **小项目**：使用单文件或简单文件夹结构
     ```
     project/
     ├── main.py
     ├── README.md           # 项目根目录
     ├── pyproject.toml
     ├── uv.lock
     └── docs/               # 文档文件夹
         ├── background.md
         ├── requirements.md
         └── architecture.md
     ```
   - **大项目**：使用标准 Python 项目文件夹组织
     ```
     project/
     ├── README.md           # 项目根目录
     ├── pyproject.toml
     ├── uv.lock
     ├── src/
     │   ├── __init__.py
     │   ├── main.py
     │   ├── api/              # API 模块
     │   ├── models/           # 数据模型
     │   ├── services/         # 业务逻辑
     │   ├── repositories/     # 数据访问层（Repository）
     │   └── utils/            # 工具函数
     ├── tests/
     │   └── test_main.py
     └── docs/                  # 文档文件夹
         ├── background.md
         ├── requirements.md
         └── architecture.md
     ```
3. 设计系统架构：
   - **参考 background.md 中的工具对比**，进行技术选型
   - 模块划分与职责分配（根据项目规模）
   - 数据流设计
   - **技术选型（必须说明理由，引用 background.md 中的对比分析）**：
     - 必须详细对比至少2种方案
     - 说明权衡理由（性能 vs 易用性、功能 vs 复杂度）
     - 引用 background.md 中的对比数据（性能、生态、学习曲线、版本兼容性）
     - 明确说明选择方案的优势和不足
   - 接口定义（函数签名、参数说明，**必须包含类型注解**）
   - **参考 background.md 中的最佳实践**，应用设计模式和架构模式
   - **UV 包管理策略**：使用 pyproject.toml 管理依赖，uv.lock 锁定版本
   - **技能识别**：识别项目中可能的可复用技能模块，在 architecture.md 中定义技能接口
4. **设计数据库架构**（新增）：
   - 参考数据库选型指南选择合适的数据库（SQLite、PostgreSQL、MongoDB、ChromaDB、Neo4j 等）
   - 设计数据模型（表结构、索引策略）
   - 设计数据访问层（Repository 模式）
   - 实现数据库抽象层（支持多数据库切换）
   - 生成数据库设计文档和数据层抽象文档
5. 生成以下文件：
   - `docs/architecture.md`：参考 [references/architecture-template.md](references/architecture-template.md)
     - **新增**：数据库设计章节（参考 database-design-template.md）
     - **新增**：数据访问层章节（参考 data-abstraction-template.md）
     - **新增**：根据项目规模选择对应的架构模板
     - **新增**：版本控制章节（版本策略、依赖版本锁定）
     - **新增**：UV 包管理章节（pyproject.toml 配置、uv.lock 策略）
     - **新增**：数据库设计章节（数据库选型、数据模型、索引策略）
     - **新增**：数据访问层章节（Repository 模式、BaseRepository 接口、具体实现）
     - **新增**：技能识别和管理章节（技能列表、接口定义、复用指南）
     - 明确 Python 3.11+ 版本要求
     - 增加技术选型权衡说明
   - `docs/database-design.md`：参考 [references/database-design-template.md](references/database-design-template.md)
     - 数据库选型与配置
     - 数据模型设计
     - 索引策略
     - 数据访问接口定义
   - `docs/data-abstraction.md`：参考 [references/data-abstraction-template.md](references/data-abstraction-template.md)
     - BaseRepository 接口定义
     - SQLAlchemy / MongoDB 实现
     - Repository 工厂
     - 数据库切换策略
   - `README.md`：参考 [references/readme-template.md](references/readme-template.md)，包含基础用法、依赖安装（使用 UV）、运行方式
   - `todo.md`：参考 [references/todo-template.md](references/todo-template.md)，初始状态所有任务标记为 `[ ]`（未完成）
     - **新增**：类型注解相关任务
     - **新增**：UV 包管理任务
     - **新增**：数据库设计与实现任务
     - **新增**：技能识别与管理任务
     - **新增**：根据项目规模调整任务列表

### 阶段3：高级程序员（Senior Dev）- 代码实现
**目标**：基于架构设计、任务清单和背景知识，编写高质量的可执行代码

**执行步骤**：
1. 阅读 `docs/architecture.md`、`docs/database-design.md`、`docs/data-abstraction.md`、`todo.md` 和 `background.md`，理解系统设计、项目规模、数据库设计、数据访问层架构、领域最佳实践和技能定义
2. **根据项目规模组织代码文件**：
   - **小项目**：所有代码在 `main.py` 中
   - **大项目**：
     - `src/__init__.py`：包初始化
     - `src/main.py`：主入口
     - `src/api/`：API 模块
     - `src/models/`：数据模型
     - `src/services/`：业务逻辑
     - `src/repositories/`：数据访问层（Repository）
     - `src/utils/`：工具函数
     - `tests/`：测试文件
3. 编写代码：
   - **必须使用 Python 3.11+ 特性**：
     - 类型注解（Type Hints）：所有函数参数和返回值必须使用类型注解
     - 使用 PEP 585（内置泛型类型）：如 `list[int]` 而非 `List[int]`
     - 使用 PEP 646（类型参数）：如 `def func[T](items: list[T]) -> T:`
     - 使用 match-case 语句（Python 3.10+）进行模式匹配
     - 使用数据类（dataclass）的改进特性
   - 代码结构清晰，包含必要注释
   - **应用 background.md 中的最佳实践**：如错误处理、**使用 loguru 进行日志记录**、代码规范
   - **参考 background.md 中的常见问题**，避免典型陷阱
   - **调用已有技能**：在实现新功能时，优先调用 architecture.md 中定义的技能模块，避免重复开发
   - **实现数据访问层**：
     - 实现 BaseRepository 接口
     - 实现 SQLAlchemyBaseRepository / MongoDBBaseRepository
     - 实现具体实体的 Repository（UserRepository 等）
     - 实现 RepositoryFactory 工厂
   - 实现所有功能点
   - 包含 `if __name__ == "__main__"` 入口
   - 确保代码可直接运行，无需额外配置
   - **类型注解示例**：
     ```python
     def process_data(data: list[dict[str, Any]]) -> dict[str, int]:
         """处理数据并返回统计结果"""
         counts: dict[str, int] = {}
         for item in data:
             key = item.get("key")
             if key:
                 counts[key] = counts.get(key, 0) + 1
         return counts
     ```
   - **技能调用示例**：
     ```python
     from src.utils.helpers import existing_skill

     def new_feature(data: list[Any]) -> dict[str, Any]:
         """新功能实现，调用已有技能"""
         # 直接调用技能
         result = existing_skill(data)
         return result
     ```
   - **Repository 使用示例**：
     ```python
     from src.repositories import UserRepository

     def get_user(user_id: int) -> User | None:
         """获取用户"""
         repo = UserRepository(session)
         return repo.get_by_id(user_id)
     ```
4. **生成 UV 依赖文件**：
   - `pyproject.toml`：使用标准格式，包含项目元数据和依赖
   - **新增数据库依赖**：sqlalchemy、pymongo、chromadb、psycopg2-binary 等
   - **新增迁移工具**：alembic（关系型数据库）、mongomock（MongoDB 测试）
   - `uv.lock`：自动生成，锁定依赖版本
   - 参考模板：[references/uv-lock-template.md](references/uv-lock-template.md)
5. 同步更新 `todo.md`：
   - 将已完成的任务标记为 `[x]`
   - 确保每个任务对应 `requirements.md` 中的一个条目

### 阶段4：质量验证 - 功能测试
**目标**：验证代码是否满足原始需求，生成测试报告

**执行步骤**：
1. 设计测试用例：
   - 覆盖 `requirements.md` 中的所有功能点
   - **参考 background.md 中的常见问题**，设计针对性的测试场景
   - 包含正常场景和边界情况
   - **新增数据库测试**：
     - 测试 CRUD 操作
     - 测试事务处理
     - 测试并发操作
     - 使用内存数据库进行测试（SQLite / mongomock）
   - 记录每个测试用例的输入和预期输出
2. 执行测试（模拟运行）：
   - 分析代码逻辑，验证功能是否正确实现
   - 检查是否符合架构设计
   - **验证 UV 依赖文件**：确保 pyproject.toml 和 uv.lock 正确
   - **验证类型注解完整性**：确保所有关键函数都有类型注解
   - **验证技能调用**：确认新功能正确调用了已有技能
   - **验证 loguru 日志配置**：确保日志正确输出
   - **验证数据访问层**：确认 Repository 接口实现正确
   - **验证数据库操作**：确认 CRUD 操作、查询优化正确
   - **参考 background.md 中的安全考虑**，验证安全措施
3. 生成 `test_report.md`：
   - 参考 [references/test-report-template.md](references/test-report-template.md)
   - 列出：已验证功能、是否通过、潜在风险或未覆盖场景
   - 对每个功能给出明确的通过/不通过判断
   - **引用 background.md 中的知识**，说明测试覆盖的常见问题
   - **新增**：验证 Python 3.11+ 特性使用情况、UV 依赖管理情况、技能调用情况、loguru 日志配置、数据库操作验证

### 阶段5：功能扩展（添加功能）
**目标**：在现有项目基础上添加新功能，识别并复用已有技能

**触发条件**：用户提出"添加功能"、"扩展功能"等需求

**执行步骤**：
1. **读取现有项目**：
   - 阅读 `docs/requirements.md`、`docs/architecture.md`、`docs/database-design.md`、`docs/data-abstraction.md`、`docs/background.md`
   - 读取现有代码文件（main.py 或 src/ 目录）
   - 读取 `pyproject.toml` 了解现有依赖

2. **分析现有架构**：
   - 理解现有功能模块和数据流
   - 识别 architecture.md 中定义的可调用技能
   - **评估数据库扩展需求**：是否需要新增数据表/集合、更新索引
   - 评估新功能对现有系统的影响

3. **设计功能扩展方案**：
   - 明确新功能的需求和接口
   - 优先使用已有技能实现新功能
   - 设计新功能的代码适配方案
   - **设计数据库变更**：新增表/集合、更新 Repository
   - 评估是否需要新增依赖

4. **适配代码**：
   - 调用已有技能模块
   - 编写新功能代码
   - **更新数据访问层**：新增或修改 Repository
   - **编写数据库迁移脚本**（如需要）
   - 确保与现有代码风格一致
   - 添加类型注解和 loguru 日志

5. **更新文档**：
   - 更新 `requirements.md`：添加新功能需求，更新版本号（v1.0.0 → v1.1.0）
   - 更新 `architecture.md`：更新架构设计、技能列表
   - 更新 `docs/database-design.md`：更新数据库设计
   - 更新 `docs/data-abstraction.md`：更新数据访问层
   - 更新 `todo.md`：添加新功能开发任务、数据库扩展任务
   - 更新 `README.md`：更新功能列表和使用说明

6. **测试验证**：
   - 测试新功能
   - 回归测试现有功能
   - **测试数据库变更**：验证新增表/集合、索引、迁移
   - 更新 `test_report.md`
   - 使用 UV 更新依赖（如需要）：`uv add package`

7. **生成扩展计划文档**：
   - 参考 [references/feature-extension-template.md](references/feature-extension-template.md)
   - 记录扩展过程、代码变更、文档更新、数据库变更

### 阶段6：项目重构
**目标**：分析代码质量与性能，执行重构，提升可维护性

**触发条件**：用户提出"重构"、"优化"、"改进代码"等需求

**执行步骤**：
1. **读取现有项目**：
   - 读取所有代码文件
   - 读取所有文档文件
   - 读取 `pyproject.toml` 和 `uv.lock`

2. **分析代码质量与性能**：
   - 分析代码复杂度、重复代码、命名规范
   - 识别性能瓶颈
   - 识别架构问题（高耦合、低内聚）
   - **分析数据库性能**：查询优化、索引优化、连接池
   - 识别可提取为技能的模块

3. **设计重构方案**：
   - 确定重构目标（性能、可读性、可维护性）
   - 设计代码重构方案（提取函数/类、简化逻辑）
   - 设计性能优化方案（算法、缓存、并发）
   - 设计架构优化方案（解耦、接口优化）
   - **设计数据库优化方案**：查询优化、索引优化、连接池优化
   - 识别并定义新的技能模块

4. **执行重构**：
   - 执行代码重构
   - 执行性能优化
   - 执行架构优化
   - **执行数据库优化**：优化查询、更新索引、调整连接池
   - **优化数据访问层**：改进 Repository 实现
   - 更新 architecture.md 中的技能识别章节
   - 使用 UV 更新依赖（如需要）：`uv lock --upgrade`

5. **验证重构结果**：
   - 回归测试
   - 性能测试
   - **数据库性能测试**
   - 功能验证
   - 更新 `test_report.md`

6. **生成重构报告**：
   - 参考 [references/refactoring-plan-template.md](references/refactoring-plan-template.md)
   - 记录重构前后的对比（代码质量、性能、架构、数据库性能）
   - 记录技能识别和管理

---

## 最终交付

### 新项目交付格式
按照以下格式输出所有文件内容（每个文件以 `--- FILE: filename ---` 开头）：

**小项目**（单文件）：
```
--- FILE: README.md ---
<README.md 完整内容>

--- FILE: pyproject.toml ---
<pyproject.toml 完整内容>

--- FILE: uv.lock ---
<uv.lock 完整内容>

--- FILE: main.py ---
<main.py 完整内容>

--- FILE: docs/background.md ---
<docs/background.md 完整内容>

--- FILE: docs/requirements.md ---
<docs/requirements.md 完整内容>

--- FILE: docs/architecture.md ---
<docs/architecture.md 完整内容>

--- FILE: docs/database-design.md ---
<docs/database-design.md 完整内容>

--- FILE: docs/data-abstraction.md ---
<docs/data-abstraction.md 完整内容>

--- FILE: test_report.md ---
<test_report.md 完整内容>
```

**大项目**（文件夹组织）：
```
--- FILE: README.md ---
<README.md 完整内容>

--- FILE: pyproject.toml ---
<pyproject.toml 完整内容>

--- FILE: uv.lock ---
<uv.lock 完整内容>

--- FILE: src/__init__.py ---
<src/__init__.py 完整内容>

--- FILE: src/main.py ---
<src/main.py 完整内容>

--- FILE: src/repositories/__init__.py ---
<src/repositories/__init__.py 完整内容>

--- FILE: src/repositories/base.py ---
<BaseRepository 接口>

--- FILE: src/repositories/user_repo.py ---
<UserRepository 实现>

--- FILE: tests/__init__.py ---
<tests/__init__.py 完整内容>

--- FILE: tests/test_repositories.py ---
<Repository 测试>

--- FILE: docs/background.md ---
<docs/background.md 完整内容>

--- FILE: docs/requirements.md ---
<docs/requirements.md 完整内容>

--- FILE: docs/architecture.md ---
<docs/architecture.md 完整内容>

--- FILE: docs/database-design.md ---
<docs/database-design.md 完整内容>

--- FILE: docs/data-abstraction.md ---
<docs/data-abstraction.md 完整内容>

--- FILE: test_report.md ---
<test_report.md 完整内容>
```

### 功能扩展交付格式
```
--- FILE: docs/requirements.md ---
<更新后的 requirements.md>

--- FILE: docs/architecture.md ---
<更新后的 architecture.md>

--- FILE: docs/database-design.md ---
<更新后的 database-design.md>

--- FILE: docs/data-abstraction.md ---
<更新后的 data-abstraction.md>

--- FILE: main.py 或 src/... ---
<修改后的代码文件>

--- FILE: pyproject.toml ---
<更新后的 pyproject.toml（如有）>

--- FILE: README.md ---
<更新后的 README.md>

--- FILE: feature_extension_plan.md ---
<功能扩展计划文档>
```

### 重构交付格式
```
--- FILE: main.py 或 src/... ---
<重构后的代码文件>

--- FILE: docs/architecture.md ---
<更新后的 architecture.md（包含技能识别）>

--- FILE: docs/database-design.md ---
<更新后的 database-design.md>

--- FILE: docs/data-abstraction.md ---
<更新后的 data-abstraction.md>

--- FILE: refactoring_report.md ---
<重构报告>

--- FILE: test_report.md ---
<更新后的测试报告>
```

---

## 资源索引
- 背景知识模板：见 [references/background-template.md](references/background-template.md)
- 需求文档模板：见 [references/requirements-template.md](references/requirements-template.md)
- 架构文档模板：见 [references/architecture-template.md](references/architecture-template.md)
- UV 锁定文件模板：见 [references/uv-lock-template.md](references/uv-lock-template.md)
- 任务清单模板：见 [references/todo-template.md](references/todo-template.md)
- 测试报告模板：见 [references/test-report-template.md](references/test-report-template.md)
- 项目说明模板：见 [references/readme-template.md](references/readme-template.md)
- 功能扩展模板：见 [references/feature-extension-template.md](references/feature-extension-template.md)
- 重构计划模板：见 [references/refactoring-plan-template.md](references/refactoring-plan-template.md)
- **数据库选型指南**：见 [references/database-selection-guide.md](references/database-selection-guide.md)
- **数据库设计模板**：见 [references/database-design-template.md](references/database-design-template.md)
- **数据层抽象模板**：见 [references/data-abstraction-template.md](references/data-abstraction-template.md)

---

## 注意事项

### 核心要求（强制）
- **UV 包管理**：必须使用 UV 作为包管理工具，使用 `pyproject.toml` 管理依赖，`uv.lock` 锁定版本
- **loguru 日志**：必须使用 loguru 进行日志记录
- **Python 3.11+ 特性**：必须使用类型注解、PEP 585 内置泛型类型
- **项目规模自适应**：PM 阶段评估规模，架构师阶段选择组织方式
- **版本控制机制**：使用语义化版本（vX.Y.Z），记录版本历史
- **技能识别与管理**：在架构阶段识别技能，在实现阶段复用技能
- **数据库设计与实现**：根据需求选择合适的数据库（SQLite、PostgreSQL、MongoDB、向量数据库、图数据库）
- **数据层抽象**：必须实现 Repository 模式，提供统一的 CRUD 接口
- **数据库切换能力**：支持通过配置切换不同数据库实现

### 流程要求
- **自主学习阶段**：必须执行网络搜索，不得跳过
- **需求澄清限制**：PM 阶段最多进行2轮交互，超过则基于已有信息推进
- **无过度设计**：严格按照用户需求实现，不得添加未提及的功能
- **背景知识应用**：各阶段必须参考和应用 background.md 中的知识
- **代码质量**：确保生成代码可直接运行，包含完整的错误处理

### 技术选型（强制）
- 必须详细对比至少2种方案
- 必须说明权衡理由（性能 vs 易用性、功能 vs 复杂度）
- 必须引用 background.md 中的对比数据
- 必须说明选择方案的优势和不足

### 数据库要求（强制）
- **数据库选型**：根据项目需求选择合适的数据库，参考 database-selection-guide.md
- **数据模型设计**：设计合理的数据表/集合结构，定义索引策略
- **数据访问层**：实现 Repository 模式，提供统一的 CRUD 接口
- **类型安全**：所有数据访问函数必须包含类型注解
- **性能优化**：合理的索引策略、连接池配置、查询优化

### 状态同步
- todo.md 必须与 requirements.md 的功能点一一对应
- 测试报告必须覆盖所有功能点，并明确标注通过状态

### 功能扩展
- 优先调用已有技能，避免重复开发
- 确保新功能与现有代码风格一致
- 更新所有相关文档（包括数据库设计文档）
- 执行回归测试
- **数据库扩展**：评估是否需要新增表/集合、更新 Repository、编写迁移脚本

### 重构
- 先分析后执行，避免盲目重构
- 保持功能不变，仅优化内部实现
- **数据库优化**：优化查询、索引、连接池
- 记录重构前后的对比数据
- 识别并提取技能模块

---

## 使用示例

### 示例1：带数据库的用户管理系统（大项目）
- **用户需求**："实现一个用户管理系统，支持用户注册、登录、信息查询"
- **阶段0**：搜索"数据库选型"、"SQLAlchemy vs MongoDB"、"用户认证最佳实践"、"密码加密"、"Python 3.11+ 类型注解"、"UV 包管理"、"Repository 模式"
- **PM 阶段**：
  - 澄清数据规模、并发需求、认证方式、密码存储
  - 明确数据库需求：关系型数据（用户信息），预期 10万用户
  - **评估项目规模**：5 个功能点 → **中型项目** → 选择 **PostgreSQL**（支持高并发）
- **Architect 阶段**：
  - 数据库选型：PostgreSQL（关系型，支持高并发）
  - 设计数据模型：User 表（id, username, email, password_hash, created_at）
  - 设计数据访问层：BaseRepository 接口、SQLAlchemyBaseRepository、UserRepository
  - 设计 RepositoryFactory：支持 PostgreSQL / SQLite 切换
  - 索引策略：username（UNIQUE）、email（UNIQUE）、created_at（INDEX）
  - **选择大项目架构**：src/repositories/ 数据访问层
  - 识别技能模块：密码加密、Token 生成
- **Senior Dev 阶段**：
  - 实现 BaseRepository 接口（CRUD 操作）
  - 实现 SQLAlchemyBaseRepository
  - 实现 UserRepository（get_by_email, get_by_username）
  - 实现 RepositoryFactory
  - 使用 Python 3.11+ 特性、类型注解
  - 使用 loguru 记录日志
  - 生成 `pyproject.toml`（sqlalchemy、psycopg2-binary、alembic）
- **验证阶段**：测试 CRUD 操作、并发操作、数据库性能、类型注解、数据访问层抽象

### 示例2：文档管理系统（MongoDB）
- **用户需求**："实现一个文档管理系统，支持文档的增删改查和全文搜索"
- **PM 阶段**：
  - 澄清文档格式、存储方式、搜索需求
  - 明确数据库需求：文档型数据，需要灵活 schema 和全文搜索
  - **评估项目规模**：4 个功能点 → **小项目** → 选择 **MongoDB**（文档型，灵活 schema）
- **Architect 阶段**：
  - 数据库选型：MongoDB（文档型，支持全文搜索）
  - 设计数据模型：Document 集合（title, content, tags, metadata, created_at）
  - 设计数据访问层：MongoDBBaseRepository、DocumentRepository
  - 索引策略：title（TEXT）、content（TEXT）、tags（MULTIKEY）
- **Senior Dev 阶段**：
  - 实现 MongoDBBaseRepository
  - 实现 DocumentRepository（search_by_keyword）
  - 使用 pymongo、类型注解
- **验证阶段**：测试 CRUD 操作、全文搜索、性能

### 示例3：向量搜索系统（ChromaDB）
- **用户需求**："实现一个向量搜索系统，支持文档的语义搜索"
- **PM 阶段**：
  - 澄清向量维度、相似度度量、数据规模
  - 明确数据库需求：向量搜索，预期 100万向量
  - **评估项目规模**：3 个功能点 → **小项目** → 选择 **ChromaDB**（向量数据库，轻量级）
- **Architect 阶段**：
  - 数据库选型：ChromaDB（向量数据库，专为 LLM 设计）
  - 设计数据模型：ChromaDB 集合（documents, embeddings, metadata）
  - 设计数据访问层：VectorRepository
- **Senior Dev 阶段**：
  - 实现 VectorRepository（add_document, search）
  - 使用 chromadb、类型注解
- **验证阶段**：测试向量添加、相似性搜索、性能

---

## 技能调用机制

### 识别时机
- **架构阶段**（阶段2）：识别可能的可复用技能模块，在 architecture.md 中定义
- **实现阶段**（阶段3）：实现新功能时，优先调用已定义的技能
- **扩展阶段**（阶段5）：添加功能时，复用已有技能
- **重构阶段**（阶段6）：重构时，提取新的技能模块

### 技能接口规范
所有技能必须包含：
1. **完整的类型注解**：函数参数和返回值必须使用类型注解
2. **清晰的文档字符串**：说明功能、参数、返回值、使用场景
3. **示例代码**：在 architecture.md 中提供调用示例
4. **依赖声明**：明确依赖的其他技能或库

### 复用原则
1. **优先复用**：实现新功能时，优先调用已有技能
2. **接口稳定**：技能接口应保持稳定，避免频繁修改
3. **单一职责**：技能应具有单一职责，功能清晰
4. **可测试性**：技能应易于单独测试

### 数据访问技能
以下数据访问层模块可作为技能复用：
- **BaseRepository 接口**：通用的 CRUD 接口
- **SQLAlchemyBaseRepository**：关系型数据库的通用实现
- **MongoDBBaseRepository**：MongoDB 的通用实现
- **RepositoryFactory**：数据库切换工厂
