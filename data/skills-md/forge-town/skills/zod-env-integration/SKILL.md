---
name: zod-env-integration
description: Generate Zod-based environment variable management code from .env.example files. Use when you need to create type-safe env management, standardize env handling, or generate env schemas.
---

# Zod 环境变量集成

提供生成基于 Zod 验证的类型安全环境变量管理代码的指导和模板。包含创建 schema、getter 函数和桶导出的示例和最佳实践。

## 工作原理

1. 在项目根目录准备 .env.example 文件
2. 对于单环境：生成 `integrations/env/` 包含 schema、getter 和导出
3. 对于多环境：为每个环境生成独立的 `integrations/{env}-env/` 目录
4. 按照代码生成指南创建 Zod schema
5. 实现带有适当错误处理的 getter 函数
6. 创建桶导出以实现干净的导入
7. 在应用程序中使用生成的代码

## 使用方法

此技能提供文档和示例。按照参考指南中的步骤操作：

- [代码生成指南](references/code-generation-guide.md) - 生成代码的详细规则
- [使用指南](references/usage-guide.md) - 如何使用生成的代码
- [.env.example 模板](references/.env.example.template) - .env 文件的模板

**示例：**

```bash
# 在项目中创建 .env.example
cp skills/zod-env-integration/references/.env.example.template .env.example

# 按照指南手动创建集成代码
```

## 输出

**单环境：**
创建 `integrations/env/` 目录包含：
- `envSchema.ts` - Zod schema 和类型
- `getEnv.ts` - Getter 函数
- `index.ts` - 桶导出

**多环境：**
为每个环境创建独立的目录：
- `integrations/server-env/` - 服务端环境集成
- `integrations/client-env/` - 客户端环境集成
每个目录都有自己的 schema、getter 和导出。

## 呈现结果

环境变量集成代码创建成功！

**单环境生成的文件：**
- integrations/env/envSchema.ts
- integrations/env/getEnv.ts
- integrations/env/index.ts

**多环境生成的文件：**
- integrations/server-env/envSchema.ts
- integrations/server-env/getServerEnv.ts
- integrations/server-env/index.ts
- integrations/client-env/envSchema.ts
- integrations/client-env/getClientEnv.ts
- integrations/client-env/index.ts

## 故障排除

- **缺少 .env.example**：从 references/.env.example.template 复制模板
- **未安装 Zod**：在项目中运行 `pnpm install zod`
- **类型错误**：检查代码生成指南中的正确 schema 语法
- **导入错误**：确保 index.ts 中的桶导出正确
