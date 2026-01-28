---
name: codebase-understanding
description: 自底向上分析代码库并生成层级化 README.md 文档树。从叶子目录开始分析，为每个目录生成包含文件、类、函数一句话描述的 README.md，逐层向上汇总形成完整的代码库文档体系。支持状态持久化和断点续传，适用于理解新项目、生成技术文档、分析代码结构等场景。当用户需要理解代码库结构、分析功能实现、生成代码文档时使用此技能。
---

# Codebase Understanding

## 概述

本技能提供自底向上的代码库分析方法，通过为每个目录生成 README.md 文档，形成树状的代码理解体系。

**核心特性**:
- **自底向上**: 从叶子目录开始分析，逐层向上汇总
- **一句话描述**: 每个类、函数用一句话概括功能
- **状态持久化**: 支持断点续传，中断后可继续分析
- **增量更新**: 只分析修改过的文件，提高效率

## 使用场景

### 1. 理解新项目

**用户请求示例**:
- "帮我理解这个项目的代码结构"
- "这个代码库是做什么的？有哪些主要模块？"
- "我刚接手这个项目，需要了解整体架构"

**操作步骤**:
1. 使用 Glob 工具扫描源代码目录结构
2. 初始化 `.analysis-state.json` 状态文件
3. 从叶子目录开始分析并生成 README.md
4. 逐层向上生成父目录的 README.md
5. 最后生成根目录的源代码概览 README.md

### 2. 生成技术文档

**用户请求示例**:
- "为这个项目生成完整的代码文档"
- "需要一份代码库的参考文档"
- "生成 API 文档和架构说明"

**操作步骤**:
1. 检查是否已有分析状态，如果有则继续
2. 完成所有目录的 README.md 生成
3. 在根目录生成整体架构文档
4. 提供关键文件和函数的索引

### 3. 分析功能实现

**用户请求示例**:
- "这个功能在哪里实现的？"
- "查找处理用户登录的代码"
- "追踪订单创建的完整流程"

**操作步骤**:
1. 使用 Grep 工具搜索关键词（如 "login", "authentication"）
2. 读取相关文件，理解功能实现
3. 追踪函数调用链
4. 在对应目录的 README.md 中标注关键流程

## 工作流程

### 阶段 1: 准备和扫描

```bash
# 1. 识别源代码目录
src_dirs = ["src", "lib", "app", "server"]

# 2. 扫描目录树结构
使用 Bash 工具: find src -type d | sort

# 3. 初始化或加载状态文件
如果 .analysis-state.json 存在 → 加载状态
如果不存在 → 创建新的状态文件
```

**状态文件结构**: 见 [references/state-management.md](references/state-management.md)

### 阶段 2: 分析叶子目录

叶子目录 = 不包含子目录的目录（只有源代码文件）

**步骤**:

1. **列出目录下所有文件**
   ```javascript
   Glob: **/*.{js,ts,py,java,go,rs,cpp,c,h}
   ```

2. **对每个文件执行分析**
   - 读取文件内容: `Read(path/to/file)`
   - 识别类定义、函数定义
   - 提取函数签名（函数名、参数、返回类型）
   - 分析函数体，理解功能

   **详细方法**: 见 [references/file-analysis.md](references/file-analysis.md)

3. **生成一句话描述**
   - 模板: `[动词] + [对象] + [方式] + [结果]`
   - 示例: `验证用户邮箱和密码并返回用户对象`

4. **生成 README.md**
   - 使用模板: [assets/leaf-readme-template.md](assets/leaf-readme-template.md)
   - 写入文件: `Write(path/to/README.md, content)`

5. **更新状态**
   ```json
   {
     "src/utils/auth": {
       "status": "completed",
       "readmeGenerated": true,
       "files": ["login.js", "register.js"],
       "fileHashes": { "login.js": "abc123", ... }
     }
   }
   ```

**并行处理**: 多个叶子目录可以并行分析，提高效率。

### 阶段 3: 分析分支目录

分支目录 = 包含子目录的目录

**步骤**:

1. **读取所有子目录的 README.md**
   ```javascript
   for (subdir of subdirs) {
     readme = Read(subdir/README.md);
     提取"目录概述"部分;
   }
   ```

2. **分析当前目录的文件**（如果有）
   - 同叶子目录的文件分析方法

3. **生成 README.md**
   - 使用模板: [assets/branch-readme-template.md](assets/branch-readme-template.md)
   - 包含子目录概述摘要
   - 包含当前目录文件分析

4. **更新状态**
   ```json
   {
     "src/services": {
       "status": "completed",
       "subdirs": ["user", "order", "payment"],
       "completedSubdirs": ["user", "order", "payment"]
     }
   }
   ```

**依赖关系**: 必须等待所有子目录完成后再分析父目录。

### 阶段 4: 生成根目录文档

**步骤**:

1. **收集所有一级目录的概述**
2. **分析技术栈**
   - 读取 package.json / requirements.txt / pom.xml
   - 识别主要依赖和框架
3. **生成架构图**
   - 识别分层结构
   - 绘制模块关系图
4. **生成 README.md**
   - 使用模板: [assets/root-readme-template.md](assets/root-readme-template.md)

## 状态管理和断点续传

### 状态文件位置

```
项目根目录/.analysis-state.json
```

### 状态检查和恢复

**开始分析前**:
```javascript
if (exists('.analysis-state.json')) {
  state = load('.analysis-state.json');
  print("发现已有分析状态:");
  print(`已完成: ${state.stats.analyzedDirectories}/${state.stats.totalDirectories}`);
  print("从上次中断处继续...");
} else {
  print("首次分析，初始化状态文件...");
  state = init();
}
```

**继续中断的分析**:
```javascript
pending_dirs = state.get_pending_directories();
for (dir of pending_dirs) {
  if (state.should_analyze(dir)) {
    analyze_directory(dir);
  }
}
```

### 增量更新策略

当重新分析时：
1. 计算文件的 MD5 哈希
2. 与状态文件中保存的哈希对比
3. 如果哈希不同 → 文件已修改，重新分析
4. 如果哈希相同 → 跳过，使用已有结果

**详细说明**: 见 [references/state-management.md](references/state-management.md)

## 语言支持

### JavaScript / TypeScript

**识别模式**:
```javascript
export class UserService { }
export function createUser() { }
export const validate = () => { }
```

**提取**: 类名、函数名、参数、返回类型、async 标记

### Python

**识别模式**:
```python
class UserService:
def create_user():
async def fetch_data():
```

**提取**: 类名、函数名、参数、返回类型、装饰器

### Java

**识别模式**:
```java
public class UserService { }
public void createUser() { }
```

**提取**: 类名、方法名、参数、返回类型、注解

### Go

**识别模式**:
```go
type UserService struct { }
func CreateUser() { }
func (s *UserService) Method() { }
```

**提取**: 类型名、函数名、方法名、参数、返回类型

**详细方法**: 见 [references/file-analysis.md](references/file-analysis.md)

## 函数描述规范

### 一句话描述模板

| 函数类型 | 模板 | 示例 |
|---------|------|------|
| 数据处理 | `[动词] + [对象] + [方式] + [结果]` | 验证用户邮箱并返回验证结果 |
| 查询获取 | `从 [数据源] 查询 [条件]` | 从数据库获取用户信息 |
| 操作执行 | `[动词] + [对象] + [结果]` | 发送验证邮件到用户邮箱 |
| 工具辅助 | `[动词] + [对象] + [转换]` | 格式化日期为本地化字符串 |

### 质量标准

✅ **好的描述**:
- 验证用户登录凭证并返回 JWT token
- 计算购物车中商品的总折扣金额
- 从 Redis 获取用户会话信息

❌ **不好的描述**:
- 处理数据（太模糊）
- helper 函数（没有说明功能）
- get, set（缺少上下文）

## 输出文档结构

分析完成后，项目中的每个目录都有一个 README.md：

```
project/
├── README.md (根目录概览)
├── src/
│   ├── README.md (src 概述)
│   ├── utils/
│   │   ├── README.md (utils 目录说明)
│   │   ├── auth/
│   │   │   ├── README.md (auth 模块详细说明)
│   │   │   ├── login.js
│   │   │   └── register.js
│   │   └── date/
│   │       ├── README.md (date 模块详细说明)
│   │       └── helpers.js
│   └── services/
│       ├── README.md (services 说明)
│       ├── user/
│       │   ├── README.md (user 服务说明)
│       │   └── service.js
│       └── order/
│           ├── README.md (order 服务说明)
│           └── service.js
```

每个 README.md 包含该层级的相关信息，形成完整的文档树。

## 最佳实践

### 1. 并行处理

- 叶子目录可以并行分析
- 使用 Task 工具启动多个 Explore agent 并行工作
- 父目录必须等待子目录完成

### 2. 进度追踪

使用 TodoWrite 工具实时更新进度：
```javascript
TodoWrite([
  { content: "分析 src/utils/auth/", status: "in_progress" },
  { content: "分析 src/utils/date/", status: "pending" },
  { content: "生成 src/utils/ README.md", status: "pending" }
]);
```

### 3. 错误处理

遇到错误时：
1. 记录错误到状态文件
2. 标记目录为 "failed"
3. 继续处理其他目录
4. 最后提供错误报告

### 4. 性能优化

- 使用 Glob 而不是 find 命令搜索文件
- 批量读取文件减少 I/O 操作
- 并行处理独立的目录
- 使用文件哈希避免重复分析

### 5. 质量检查

生成 README.md 后检查：
- ✅ 所有文件都已分析
- ✅ 所有类和函数都有描述
- ✅ 描述简洁准确
- ✅ Markdown 格式正确

## 执行示例

### 示例 1: 分析小型项目

```javascript
// 1. 扫描目录
dirs = Glob("src/**")
// ["src/utils", "src/services", "src/models"]

// 2. 识别叶子目录
leaf_dirs = ["src/utils/auth", "src/utils/format", "src/services/user"]

// 3. 并行分析叶子目录
for (dir of leaf_dirs) {
  analyze_leaf_directory(dir);
}

// 4. 分析父目录
analyze_branch_directory("src/utils");
analyze_branch_directory("src/services");

// 5. 生成根目录
generate_root_readme("src");
```

### 示例 2: 继续中断的分析

```javascript
// 1. 加载状态
state = load_state(".analysis-state.json");

// 2. 获取待处理目录
pending = state.get_pending_directories();
// ["src/services/order", "src/services/payment"]

// 3. 继续分析
for (dir of pending) {
  analyze_directory(dir);
}

// 4. 完成剩余父目录
if (all_subdirs_completed("src/services")) {
  analyze_branch_directory("src/services");
}
```

## 常见问题

### Q: 分析中断了怎么办？

A: 状态文件会保存所有进度。下次运行时会自动从上次中断处继续。

### Q: 代码修改后需要重新分析吗？

A: 系统会检测文件哈希，只分析修改过的文件，未修改的文件会跳过。

### Q: 如何只分析特定目录？

A: 可以在状态文件中标记其他目录为 "skipped"，或直接指定要分析的目录路径。

### Q: 生成的 README.md 会覆盖已有文件吗？

A: 会。建议将生成的 README.md 重命名或备份，避免覆盖手动编写的重要文档。

## 资源

### references/

- **state-management.md**: 状态管理和断点续传的详细实现
- **file-analysis.md**: 文件分析方法和语言特定模式

### assets/

- **leaf-readme-template.md**: 叶子目录 README 模板
- **branch-readme-template.md**: 分支目录 README 模板
- **root-readme-template.md**: 根目录 README 模板
