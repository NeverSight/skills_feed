---
name: six-layer-architect
version: 1.0.0
description: 基于六层架构（前端UI/前端服务/前端API/后端API/后端服务/数据层）生成全栈实现方案，适用于功能需求开发、代码生成、架构校验、安全审查
dependency:
  python:
    - jinja2>=3.1.0
    - pydantic>=2.0.0
---

# 六层架构全栈生成器

## 任务目标
- 本 Skill 用于：根据用户提供的功能意图（如"支持用户上传头像"），自动生成符合六层架构规范的完整实现方案
- 能力包含：需求解析与领域识别、逐层代码生成、跨层一致性校验、架构与安全提醒
- 触发条件：用户提出功能需求（如"允许用户上传头像"、"实现用户登录"、"添加评论功能"等）

## 前置准备
无特殊依赖，所有模板和参考文档已内置在 Skill 中

## 操作步骤

### 步骤 1：需求解析与分层映射
1. **识别功能领域**
   - 分析用户描述，识别所属业务领域（用户管理、文件上传、内容发布等）
   - 确定核心数据实体（如 User、Avatar、Comment）

2. **追踪数据流向**
   - 输入：UI 层的字段名和类型（如 `avatarFile: File`）
   - 处理：前端服务层的状态、API 层的接口定义
   - 存储：后端服务层的业务逻辑、数据层的持久化字段
   - 输出：返回给前端的响应格式

3. **确定涉及的层级**
   - 简单功能可能只涉及 3-4 层
   - 复杂功能通常涉及全部六层

### 步骤 2：逐层生成实现方案
按数据流顺序（从前端到后端）生成每一层的代码：

#### 前端各层

**UI 层（Vue 3 + Tailwind）**
- 使用 `<script setup>` 语法和组合式 API
- 使用 Tailwind CSS 类名进行样式设计
- 表单使用 `<input type="file">` + `<button>`，配合 `@change` 事件
- 错误提示使用 SweetAlert2（`Swal.fire()`）
- 响应式数据使用 `ref` 和 `reactive`
- 参考：`references/architecture_layers.md` 的 UI 层职责说明

**前端服务层（Pinia Store）**
- 使用 `defineStore` 定义状态
- 决定是否需要持久化（`usePersist` 插件）
- 封装业务逻辑（如 `uploadAvatar()`）
- 参考：`references/architecture_layers.md` 的前端服务层职责说明

**前端 API 层（Axios + TypeScript）**
- 封装 API 函数（如 `uploadAvatar(file: File)`）
- 定义 TypeScript 接口（`src/types/user.ts`）
- 使用 `FormData` 处理文件上传
- 统一错误处理（基于 HTTP 状态码）
- 参考：`references/architecture_layers.md` 的前端 API 层职责说明

#### 后端各层

**后端 API 层（FastAPI + Pydantic）**
- 定义路由（如 `@app.post("/users/avatar")`）
- 使用 Pydantic 模型定义请求/响应结构
- 使用 `Form()` 和 `File()` 接收表单数据
- 返回标准化响应（`{ code: 200, data: {...} }`）
- 参考：`references/architecture_layers.md` 的后端 API 层职责说明

**后端服务层（Service 类）**
- 验证文件类型/大小
- 生成唯一文件名（UUID + 原始扩展名）
- 保存到本地或云存储
- 更新数据库记录
- 参考：`references/architecture_layers.md` 的后端服务层职责说明

**数据层（SQLAlchemy + PostgreSQL）**
- 定义 SQLAlchemy 模型（增加 `avatar_url` 字段）
- 使用 Alembic 生成迁移命令：
  ```bash
  alembic revision --autogenerate -m "Add avatar_url to User model"
  alembic upgrade head
  ```
- 参考：`references/architecture_layers.md` 的数据层职责说明

### 步骤 3：跨层一致性校验
检查以下一致性：

**字段名一致性**
- UI 层：`avatarFile`
- 前端服务层：`state.avatarFile`
- 前端 API 层：`formData.append('avatarFile', file)`
- 后端 API 层：`file: UploadFile = File(...)`
- 数据层：`avatar_url: Column(String(256))`
- ⚠️ 注意：字段名在前后端传输时需要映射（`avatarFile` → `avatar_url`）

**类型匹配**
- 前端 TypeScript：`avatarUrl: string`
- 后端 Pydantic：`avatar_url: str`
- 数据库：`VARCHAR(256)` 或 `TEXT`

**错误处理贯通**
- 后端返回：400 Bad Request（文件类型错误）
- 前端 API 层：根据 `response.status` 判断
- UI 层：调用 `Swal.fire({ icon: 'error', ... })` 显示错误

**类型一致性（前后端 Schema 同步）**
确保前端 TypeScript 类型与后端 Pydantic schema 完全一致：

| TypeScript 类型 | Pydantic 类型 | 说明 |
|----------------|---------------|------|
| `string` | `str` | 字符串 |
| `number` | `int` / `float` | 数字 |
| `boolean` | `bool` | 布尔值 |
| `Date` | `datetime` | 日期时间 |
| `string` (URL) | `HttpUrl` | URL 类型 |
| `string` (Email) | `EmailStr` | 邮箱类型 |
| `Array<T>` | `List[T]` | 数组/列表 |
| `T \| null` | `Optional[T]` | 可选类型 |
| `T \| U \| V` | `Union[T, U, V]` | 联合类型 |

**类型同步最佳实践**：
1. **接口定义同步**：前端 TypeScript 接口与后端 Pydantic 模型字段名和类型必须一一对应
   ```typescript
   // 前端 TypeScript
   export interface User {
     id: number
     email: string
     avatar_url: string | null
     created_at: string  // ISO 8601 格式
   }
   ```
   ```python
   # 后端 Pydantic
   class UserResponse(BaseModel):
       id: int
       email: str
       avatar_url: Optional[str] = None
       created_at: datetime
   ```

2. **字段名映射规则**：
   - 前端使用蛇形命名（snake_case）与后端保持一致
   - 避免在 TypeScript 中使用驼峰命名，减少字段转换成本
   - 前后端共享的字段必须名称相同

3. **空值处理**：
   - 前端 `null` / `undefined` → 后端 `None`
   - 使用 `Optional[T]` 表示可为空
   - 前端访问可选字段时使用可选链 `?.`

4. **日期时间格式**：
   - 前端发送：ISO 8601 格式字符串（如 `2024-01-01T00:00:00Z`）
   - 后端接收：Pydantic 自动解析为 `datetime` 对象
   - 后端返回：JSON 序列化为 ISO 8601 格式
   - 前端显示：使用 `new Date()` 解析或格式化库

5. **枚举类型同步**：
   ```typescript
   // 前端 TypeScript
   export enum UserRole {
     ADMIN = 'admin',
     USER = 'user',
     GUEST = 'guest'
   }
   ```
   ```python
   # 后端 Pydantic
   from enum import Enum
   
   class UserRole(str, Enum):
       ADMIN = 'admin'
       USER = 'user'
       GUEST = 'guest'
   ```

6. **验证规则同步**：
   - 前端：HTML 表单验证（`required`, `minlength`, `pattern`）
   - 后端：Pydantic 验证器（`@validator`, `Field(..., min_length=1)`）
   - 前后端验证规则保持一致

参考：`references/architecture_layers.md` 的类型映射规则，`references/code_patterns.md` 的类型同步模式

### 步骤 4：架构与安全提醒
根据功能特点提醒以下事项：

**文件上传安全**
- 限制 MIME 类型（如 `image/jpeg, image/png`）
- 限制文件大小（如 5MB）
- 防路径遍历（使用 `os.path.basename()`）
- 文件名随机化（UUID + 时间戳）

**权限控制**
- 使用 JWT 验证当前用户
- 检查用户是否有权限修改目标资源（只能改自己的头像）
- 在后端 API 层添加 `@Depends(get_current_user)`

**响应格式规范**
- 统一使用全局响应模型（`code, data, message`）
- 成功：200，失败：400/401/403/500
- 详细错误信息放在 `message` 字段

**数据库迁移**
- 使用 Alembic 管理数据库变更
- 不要直接修改生产数据库
- 迁移脚本需要经过测试

### 步骤 5：输出格式化
按照以下格式输出：

- 使用 Markdown 格式
- 每层用 `###` 标题分隔（如 `### UI 层（Vue 3 + Tailwind）`）
- 代码块标注语言（`vue`、`typescript`、`python`、`bash`）
- 关键提醒用 `💡` 或 `⚠️` 标注
- 文件路径使用代码样式（如 `src/components/AvatarUpload.vue`）
- 不虚构未提供的信息，但可基于最佳实践建议

## 资源索引

**必要脚本**
- 见 [scripts/generate_code.py](scripts/generate_code.py)（用途：生成各层代码模板，参数：`--layer` 指定层级，`--context` 提供上下文信息）

**领域参考**
- 见 [references/architecture_layers.md](references/architecture_layers.md)（何时读取：需要了解每层职责和约束时）
- 见 [references/code_patterns.md](references/code_patterns.md)（何时读取：需要参考常见代码模式时）
- 见 [references/security_checklist.md](references/security_checklist.md)（何时读取：进行安全检查时）

**输出资产**
- 见 [assets/templates/](assets/templates/)（直接用于生成各层代码模板）

## 注意事项
- 仅在需要时读取参考文档，保持上下文简洁
- 生成的代码应可直接复制使用，避免占位符
- 跨层一致性校验是关键步骤，必须确保字段名和类型匹配
- 安全提醒应根据功能特点定制，不能泛泛而谈
- 充分利用智能体的自然语言理解和推理能力，避免过度依赖脚本

## 使用示例

**示例 1：用户头像上传**
- 功能说明：允许用户上传头像并在个人页显示
- 执行方式：混合（智能体解析需求 + 脚本生成代码模板）
- 关键步骤：
  1. 智能体识别领域：用户资料管理
  2. 生成 UI 层：Vue 组件（文件选择 + 预览）
  3. 生成前端 API 层：`uploadAvatar()` 函数
  4. 生成后端 API 层：FastAPI 路由 `POST /users/avatar`
  5. 生成数据层：SQLAlchemy 模型 + Alembic 迁移
  6. 一致性校验：`avatarFile` → `avatar_url` 映射

**示例 2：用户登录**
- 功能说明：用户使用邮箱和密码登录
- 执行方式：混合
- 关键步骤：
  1. 智能体识别领域：身份认证
  2. 生成 UI 层：登录表单（邮箱 + 密码）
  3. 生成前端服务层：Pinia store（`useAuthStore`）
  4. 生成前端 API 层：`login(email, password)` 函数
  5. 生成后端服务层：密码哈希 + JWT 生成
  6. 安全提醒：密码存储使用 bcrypt，JWT 过期时间

**示例 3：评论功能**
- 功能说明：用户对文章发表评论
- 执行方式：混合
- 关键步骤：
  1. 智能体识别领域：内容互动
  2. 生成数据层：Comment 模型（user_id, article_id, content）
  3. 生成后端服务层：创建评论、验证权限
  4. 生成前端 API 层：`createComment()` 函数
  5. 生成 UI 层：评论表单 + 评论列表
  6. 一致性校验：`commentText` → `content` 字段名映射
