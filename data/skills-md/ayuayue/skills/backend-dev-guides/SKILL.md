---
name: backend-dev-guides
description: 后端开发指导技能，提供后端开发工具和框架的使用规范、最佳实践和开发指导。支持 Node.js、Python、Java、Go、PHP 等语言，涵盖项目结构、API 设计、数据库操作、安全实践、性能优化等。
---

# Backend Development Guides

后端开发指导技能，提供后端开发工具和框架的使用规范、最佳实践和开发指导。

## 触发条件

当用户请求以下内容时使用此技能：
- 后端开发相关的工具使用指导
- 后端框架的使用建议
- 后端开发的最佳实践
- API 设计和开发规范
- 数据库操作指导
- 后端代码规范和模式
- 后端项目架构设计
- Go、Java、PHP、Python 等后端语言的开发任务

## 说明

### 支持的技术栈

- **编程语言**: Node.js, Python, Java, Go, PHP 等
- **框架**: Express, NestJS, Django, Spring Boot, Gin, Laravel 等
- **数据库**: MySQL, PostgreSQL, MongoDB, Redis 等
- **工具**: Docker, Git, CI/CD 等

### 开发规范

#### 1. 项目结构
```
backend-project/
├── src/                  # 源代码目录
│   ├── controllers/      # 控制器层
│   ├── services/         # 业务逻辑层
│   ├── models/           # 数据模型
│   ├── repositories/     # 数据访问层
│   ├── middlewares/      # 中间件
│   ├── routes/           # 路由定义
│   ├── utils/            # 工具函数
│   └── config/           # 配置文件
├── tests/                # 测试文件
├── docs/                 # 文档
└── package.json          # 依赖配置
```

#### 2. API 设计规范

- **RESTful 设计**: 遵循 REST 架构风格
  - GET - 获取资源
  - POST - 创建资源
  - PUT - 更新整个资源
  - PATCH - 部分更新资源
  - DELETE - 删除资源

- **命名约定**:
  - URL 使用小写字母和连字符: `/api/users`
  - 使用复数名词表示资源集合
  - 版本控制: `/api/v1/users`

- **响应格式**:
```json
{
  "success": true,
  "data": {},
  "message": "操作成功",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### 3. 错误处理

- 统一错误响应格式
- 使用适当的 HTTP 状态码
- 记录详细错误日志
- 避免暴露敏感信息

```javascript
// 错误处理示例
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = true;
  }
}
```

#### 4. 数据库操作

- 使用 ORM 或查询构建器
- 参数化查询防止 SQL 注入
- 合理使用索引优化查询
- 实现事务管理
- 数据验证和清洗
- **禁止在循环中查询数据库**
- 应该使用批量查询或 JOIN 操作一次性获取数据
- 先收集所有需要的 ID，然后一次性查询
- 使用 IN 子句或批量查询接口

**禁止在循环中查询数据库的示例：**

❌ 错误做法：
```go
// Go 示例
for _, userID := range userIDs {
    user, _ := db.Query("SELECT * FROM users WHERE id = ?", userID)
    // 处理 user...
}
```

```python
# Python 示例
for user_id in user_ids:
    user = db.query("SELECT * FROM users WHERE id = ?", user_id)
    # 处理 user...
}
```

```java
// Java 示例
for (String userId : userIds) {
    User user = userRepository.findById(userId);
    // 处理 user...
}
```

✅ 正确做法：
```go
// Go 批量查询示例
userIDs := []int{1, 2, 3}
users, _ := db.Query("SELECT * FROM users WHERE id IN ?", userIDs)
for _, user := range users {
    // 处理 user...
}
```

```python
# Python 批量查询示例
user_ids = [1, 2, 3]
users = db.query("SELECT * FROM users WHERE id IN ?", user_ids)
for user in users:
    # 处理 user...
}
```

```java
// Java 批量查询示例
List<String> userIds = Arrays.asList("1", "2", "3");
List<User> users = userRepository.findByIds(userIds);
users.forEach(user -> {
    // 处理 user...
});
```

#### 5. 安全实践

- 身份认证和授权
- 输入验证和过滤
- 使用 HTTPS
- 敏感数据加密存储
- 定期安全审计
- 依赖更新和漏洞修复

#### 6. 性能优化

- 数据库查询优化
- 缓存策略 (Redis)
- 异步处理
- 连接池管理
- 日志监控和性能分析

#### 7. 测试规范

- 单元测试覆盖率 > 80%
- 集成测试关键流程
- API 接口测试
- 负载测试

#### 8. 文档要求

- API 文档 (Swagger/OpenAPI)
- README 项目说明
- 代码注释
- 变更日志 (CHANGELOG)

### 代码质量

- 使用 ESLint/Prettier 代码规范
- 遵循 SOLID 原则
- DRY (Don't Repeat Yourself)
- 函数单一职责
- 合理的命名规范
- 类型检查 (TypeScript)

### 代码修改原则

- **最小修改原则**: 修改代码时遵循最小原则，只修改必要的部分
  - 优先修复或添加目标功能，避免改动关联很多地方的功能
  - 尽量保持现有代码结构和逻辑不变
  - 只修改与当前任务直接相关的代码
  - 避免为了"优化"而进行大规模重构
  - 修改前先分析影响范围，确认最小修改方案

**最小修改原则示例：**

❌ 避免的做法：
```python
# 用户要求修复一个登录Bug，结果重写了整个认证系统
def login(username, password):
    # 大量无关改动...
    pass

def register(username, password, email, phone, address, age, gender):  # 新增
    # 修改了很多不相关的模块...
    pass
```

✅ 推荐的做法：
```python
# 用户要求修复一个登录Bug，只修复问题所在
def login(username, password):
    # 只修复登录逻辑中的bug
    if not username:
        return {"error": "用户名不能为空"}
    # 保持其他代码不变
```

### 执行命令限制

- **不要执行测试或编译命令**
- 本地开发环境配置可能不完整或混乱
- 测试依赖可能缺失或配置错误
- 命令执行失败可能导致错误的判断
- 应该只给出执行建议，由用户手动执行

**执行建议示例：**

❌ 不要直接执行：
```bash
npm test  # 不要直接执行测试命令
npm run build  # 不要直接执行编译命令
mvn test  # 不要直接执行Maven测试
```

✅ 给出执行建议：
```
建议您在本地执行以下命令来验证修改：

# 运行测试
npm test

# 或者编译项目
npm run build

# 验证修改是否符合预期
```

### 开发工作流

1. 需求分析和设计
2. 创建功能分支
3. 编写代码和测试
4. 代码审查
5. 合并到主分支
6. 部署和监控

### 部署建议

- 使用 Docker 容器化
- CI/CD 自动化部署
- 环境变量管理
- 健康检查端点
- 日志收集和分析
- 监控告警

### 注意事项

- 避免硬编码配置
- 敏感信息使用环境变量
- 合理设置超时时间
- 实现请求限流
- 备份和恢复策略
- 跨域配置 (CORS)
- 时间和时区处理