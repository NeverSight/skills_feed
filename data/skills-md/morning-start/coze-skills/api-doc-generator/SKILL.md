---
name: api-doc-generator
version: 1.0.0
description: 自动分析项目代码并生成符合标准格式的API文档；支持Flask/FastAPI/Express等框架；自动划分功能模块和层级结构；生成包含概述、认证、端点详情、错误处理等完整章节的文档
dependency:
  python:
    - ast
---

# API 文档自动生成器

## 任务目标
- 本 Skill 用于：从项目代码中自动提取API信息并生成完整的API文档
- 能力包含：代码扫描、路由识别、模块划分、文档结构化、内容填充
- 触发条件：用户要求"生成API文档"、"分析项目API"、"编写接口文档"等

## 前置准备

### 依赖说明
本 Skill 仅使用 Python 标准库（ast, re, json, pathlib等），无需额外安装依赖。

### 非标准文件/文件夹准备
无需前置创建，输出目录将在文档生成时自动创建。

## 操作步骤

### 标准流程

1. **步骤1：扫描项目API**
   - 调用 `scripts/api_scanner.py` 扫描项目代码
   - 参数：
     - `--project-dir`: 项目根目录（必需）
     - `--framework`: 框架类型（auto/flask/fastapi/express，默认auto）
     - `--output`: 输出JSON文件路径（默认api_scan_result.json）
   - 输出：包含所有API端点信息的JSON文件

2. **步骤2：模块划分与层级分析**
   - 调用 `scripts/module_classifier.py` 分析API结构
   - 参数：
     - `--input`: 上一步输出的JSON文件路径
     - `--output`: 输出JSON文件路径（默认api_modules.json）
   - 输出：带模块分组和层级信息的API清单

3. **步骤3：生成文档结构**
   - 在项目根目录下创建 `api/` 文件夹
   - 根据 `references/doc-structure.md` 中的规范创建文档框架：
     - `api/overview.md` - API概述
     - `api/authentication.md` - 认证方式
     - `api/base-info.md` - 基础信息
     - `api/endpoints/` - 端点详情（按模块组织）
     - `api/error-handling.md` - 错误处理
     - `api/rate-limiting.md` - 速率限制
     - `api/changelog.md` - 变更日志
     - `api/support.md` - 支持与反馈

4. **步骤4：填充文档内容**
   - 根据模块划分结果，为每个模块创建独立的端点文档
   - 使用 `assets/templates/` 中的模板填充内容
   - 补充说明文字、示例代码、注意事项等

### 可选分支

- **当项目使用Flask框架**：在步骤1中明确指定 `--framework flask` 以提高识别准确率
- **当项目使用FastAPI框架**：在步骤1中明确指定 `--framework fastapi` 以利用类型注解信息
- **当项目使用Express框架**：在步骤1中明确指定 `--framework express` 以识别JavaScript路由
- **当需要自定义模块分组**：在步骤2后，手动调整模块分组逻辑再生成文档

## 资源索引

### 必要脚本
- 见 [scripts/api_scanner.py](scripts/api_scanner.py)
  - 用途：扫描项目代码，提取API路由和参数信息
  - 参数：--project-dir, --framework, --output
- 见 [scripts/module_classifier.py](scripts/module_classifier.py)
  - 用途：基于路由路径自动划分模块和层级结构
  - 参数：--input, --output

### 领域参考
- 见 [references/doc-structure.md](references/doc-structure.md)
  - 何时读取：在步骤3生成文档结构时参考
  - 内容：API文档的标准章节结构和格式规范
- 见 [references/framework-patterns.md](references/framework-patterns.md)
  - 何时读取：理解脚本如何识别不同框架的路由定义
  - 内容：各Web框架的路由定义模式和识别规则

### 输出资产
- 见 [assets/templates/](assets/templates/)
  - 用途：提供各章节和端点的文档模板
  - 包含：overview-template.md, endpoint-template.md, module-template.md

## 注意事项

- 脚本使用正则表达式和AST解析识别路由，对于复杂的动态路由可能无法完全识别，需要手动补充
- 参数提取依赖于代码注释和类型注解，建议在代码中完善文档字符串
- 模块划分基于路径的第一段，对于特殊结构可能需要手动调整
- 生成文档后，建议人工审核并补充业务说明、使用示例等
- 仅在需要时读取参考文档，保持上下文简洁

## 使用示例

### 示例1：Flask项目文档生成

```
# 1. 扫描Flask项目
python scripts/api_scanner.py \
  --project-dir /path/to/flask/project \
  --framework flask \
  --output api_scan_result.json

# 2. 划分模块
python scripts/module_classifier.py \
  --input api_scan_result.json \
  --output api_modules.json

# 3-4. 智能体根据模板生成完整文档
```

### 示例2：FastAPI项目文档生成

```
# FastAPI项目会自动识别类型注解和Pydantic模型
python scripts/api_scanner.py \
  --project-dir /path/to/fastapi/project \
  --framework fastapi

python scripts/module_classifier.py \
  --input api_scan_result.json
```

### 示例3：Express项目文档生成

```
# Node.js Express项目
python scripts/api_scanner.py \
  --project-dir /path/to/express/project \
  --framework express

python scripts/module_classifier.py \
  --input api_scan_result.json
```
