---
name: revit-api
description: "Revit 2026 API 文档查询与参考。当用户询问 Revit API 类、方法、属性、枚举用法，查找 Revit 开发相关 API，或需要确认 API 签名和参数时触发。覆盖场景：(1) 查询特定类/接口的成员和用法 (2) 搜索实现某功能需要的 API (3) 查看方法签名和参数说明 (4) 了解命名空间结构和继承关系 (5) 确认 Revit API 的正确调用方式。关键词：RevitAPI, Autodesk.Revit, Element, Document, Transaction, FilteredElementCollector, ExternalCommand, ExternalApplication, Wall, Floor, FamilyInstance, FamilySymbol, Parameter, BuiltInParameter, BuiltInCategory, Selection, GeometryElement, Solid, Face, CurveLoop, Level, View, ViewSheet, XYZ, Line, Arc, IExternalCommand, IExternalApplication, UIApplication, UIDocument, Ribbon, PushButton, ExtensibleStorage, SubTransaction, TransactionGroup, ElementId, Reference, TaskDialog。"
license: MIT
metadata:
  author: hopesy
  version: "1.1.1"
---

# Revit 2026 API 参考

基于 RevitAPI.dll v26.0.4.0 的完整 API 文档，覆盖 **30 个命名空间**、**2724 个类型**。

## 查询流程

### 第 0 步：需求预研（模糊问题必须执行）

当用户提出的问题**不包含明确的类名、方法名或命名空间**时（如"实现 DMU"、"链接更新阶段"、"怎么监听模型变化"、"做一个参数化族"），必须先完成预研，再进入后续查询。

**判断标准**：用户问题中是否包含可直接搜索的 Revit API 标识符（如 `IUpdater`、`DocumentChanged`、`FilteredElementCollector`）。如果没有，执行以下步骤：

1. **解析业务意图**：将用户的模糊需求拆解为具体的技术概念。
   - 示例："实现 DMU" → Dynamic Model Update 机制 → 需要 `IUpdater` 接口、`UpdaterRegistry` 类
   - 示例："链接更新阶段" → Revit 链接文档的加载/更新事件 → 需要 `LinkedFileStatus`、`RevitLinkType`、`TransmissionData`

2. **网络搜索验证**：使用 WebSearch 搜索 `Revit API + <技术概念>` 确认涉及的核心类和命名空间。
   ```
   搜索示例："Revit API Dynamic Model Update IUpdater"
   搜索示例："Revit API linked file update phase event"
   ```

3. **提取关键词列表**：从搜索结果中提取 2-5 个具体的类名/接口名/方法名，作为后续查询的输入。

4. **进入第 1 步**：带着明确的 API 标识符继续。

> **重要**：禁止跳过预研直接凭经验回答模糊问题。即使你认为自己知道答案，也必须通过预研确认后再用本知识库验证。

### 第 1 步：判断问题类型

| 问题类型 | 示例 | 执行路径 |
|----------|------|----------|
| 查询特定 API | "XX 类怎么用"、"XX 方法的参数" | 路径 A |
| 浏览命名空间 | "XX 命名空间有什么"、"XX 模块的类" | 路径 B |
| 查找成员归属 | "哪个类有 XX 方法"、"XX 属性在哪里" | 路径 C |
| 通用开发问题 | "怎么创建墙"、"事务怎么用" | 路径 D |

### 第 2 步：执行对应路径

#### 路径 A：搜索特定 API（最常用）

1. 先搜索定位：

```bash
python scripts/search_api.py search "关键词"
```

2. 查看类的成员概览：

```bash
python scripts/search_api.py class "Autodesk.Revit.DB.ClassName"
```

3. 需要完整文档时（签名、Remarks、继承链）：

```bash
python scripts/extract_page.py --type "Autodesk.Revit.DB.ClassName"
```

4. 查看成员级详情（属性/方法签名）：

```bash
python scripts/extract_page.py --id "P:Autodesk.Revit.DB.Wall.Flipped"
python scripts/extract_page.py --id "M:Autodesk.Revit.DB.Wall.Flip"
python scripts/extract_page.py --id "M:Autodesk.Revit.DB.FilteredElementCollector.#ctor(Autodesk.Revit.DB.Document)"
python scripts/extract_page.py --id "Overload:Autodesk.Revit.DB.FilteredElementCollector.#ctor"
```

5. 当 `member` 命令返回空结果时，优先检查是否把“类型名”当成了“成员名”：

```bash
python scripts/search_api.py member "FilteredElementCollector"  # 会提示改用 class/search
python scripts/search_api.py class "Autodesk.Revit.DB.FilteredElementCollector"
```

#### 路径 B：浏览命名空间

1. 列出所有命名空间：

```bash
python scripts/search_api.py namespaces
```

2. 查看特定命名空间的类型列表：

```bash
python scripts/search_api.py namespace "Autodesk.Revit.DB"
```

3. 或直接读取 [references/namespace-overview.md](references/namespace-overview.md) 获取完整导航。

#### 路径 C：查找成员归属

1. 跨类搜索成员名称：

```bash
python scripts/search_api.py member "GetParameters"
```

2. 从结果中定位目标类后，按路径 A 的第 2-4 步获取详情。

#### 路径 D：开发模式速查

1. 直接读取 [references/core-patterns.md](references/core-patterns.md)，包含 11 个核心模式的 C# 代码示例。
2. 若需进一步查看模式中涉及的 API 细节，按路径 A 继续查询。

### 第 3 步：组织回答

1. 优先展示与用户问题直接相关的 API 签名和用法。
2. 附带简要的代码示例（参考 core-patterns.md 中的模式）。
3. 如有相关联的类或方法，补充提示。

## 核心类速查

| 类 | 命名空间 | 用途 |
|---|---|---|
| `Document` | DB | 当前 Revit 文档，所有操作的入口 |
| `Element` | DB | 所有模型元素的基类 |
| `ElementId` | DB | 元素的唯一标识符 |
| `FilteredElementCollector` | DB | 元素查询/过滤器（必学） |
| `Transaction` | DB | 模型修改的事务管理 |
| `Wall` | DB | 墙体元素 |
| `Floor` | DB | 楼板元素 |
| `FamilyInstance` | DB | 族实例（门窗等） |
| `FamilySymbol` | DB | 族类型定义 |
| `Parameter` | DB | 元素参数读写 |
| `XYZ` | DB | 三维坐标点 |
| `Line` / `Arc` / `CurveLoop` | DB | 几何曲线 |
| `Solid` / `Face` / `Edge` | DB | 几何实体 |
| `Level` | DB | 标高 |
| `View` / `ViewPlan` / `View3D` | DB | 视图 |
| `UIApplication` | UI | UI 层应用对象 |
| `UIDocument` | UI | UI 层文档（选择交互） |
| `ExternalCommandData` | UI | Command 执行上下文 |
| `TaskDialog` | UI | 消息对话框 |
| `Selection` | UI.Selection | 用户选择交互 |

## 命名空间导航

**核心（每天用）**:
- `Autodesk.Revit.DB` — 数据库核心：元素、几何、参数、事务
- `Autodesk.Revit.UI` — 用户界面：Ribbon、对话框、选择
- `Autodesk.Revit.ApplicationServices` — 应用服务：Application、ControlledApplication
- `Autodesk.Revit.Creation` — 工厂方法：创建文档、几何对象
- `Autodesk.Revit.Attributes` — 特性标记：Transaction、Regeneration

**专业领域**:
- `DB.Architecture` — 建筑：房间、楼梯、栏杆
- `DB.Structure` — 结构：梁、柱、基础
- `DB.Mechanical` — 暖通：风管、设备
- `DB.Electrical` — 电气：线路、配电盘
- `DB.Plumbing` — 给排水：管道、卫浴

**高级**:
- `DB.ExtensibleStorage` — 自定义数据存储
- `DB.ExternalService` — 外部服务框架
- `DB.Events` / `UI.Events` — 事件系统
- `DB.DirectContext3D` — 自定义 3D 渲染
- `DB.Visual` — 材质与渲染外观
- `Autodesk.Revit.Exceptions` — 异常类型

## 禁止事项

- 禁止对模糊问题跳过第 0 步预研，直接凭记忆回答 API 细节
- 禁止在未经搜索验证的情况下猜测 API 名称或签名，必须通过预研 + 脚本查询确认
- 禁止直接编辑 `data/` 目录下的 JSON 数据文件
- 禁止向用户提供未在文档中出现的 API 用法，若文档不足应明确说明
- 禁止混淆不同 Revit 版本的 API，本文档仅覆盖 Revit 2026（v26.0.4.0）

## 注意事项

- 所有脚本基于 Python 标准库，无需额外安装依赖
- 脚本路径相对于此 skill 目录，使用 `scripts/` 前缀
- 数据已预提取为按命名空间的 JSON 文件（`data/pages/*.json`），无需原始 HTML
- 索引文件 `data/api_index.json` 由 `build_index.py` 生成
- `extract_page.py` 支持 `--id` 参数直接查询成员级文档（前缀：T=类型, P=属性, M=方法, E=事件）

## 脚本增强（v1.1.1）

- `extract_page.py` 支持 `Overload:` 前缀，能自动展开到一个可渲染重载并列出全部重载 ID。
- 当 `_lookup` 缺失或不完整时，`extract_page.py` 会尝试从 Help ID 推断命名空间并直查 `data/pages/<namespace>.json`。
- `extract_page.py` 查询失败时会输出同命名空间的候选 ID，便于快速修正拼写/参数签名。
- `search_api.py member` 在无成员命中时，会提示可能的类型候选和替代命令（`class`/`search`）。
