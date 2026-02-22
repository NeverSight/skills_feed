---
name: "arkts-code-linter"
description: "基于华为 HarmonyOS NEXT 官方文档和 ArkTS 规范的代码检查工具。自动检测代码中的规范违规、性能问题和潜在错误，确保代码符合 HarmonyOS 应用开发最佳实践。"
---

# ArkTS Code Linter - HarmonyOS NEXT 规范检查工具

## 功能概述

本工具基于 [华为 HarmonyOS NEXT 官方开发文档](https://developer.huawei.com/consumer/cn/doc/) 和项目规范，提供全面的 ArkTS 代码检查功能。

## 核心检查规则

### 1. 语言规范检查 (强制)

#### 1.1 严格类型安全
- **禁止 `any` 类型**：所有变量和函数返回值必须显式声明类型
- **禁止 `unknown` 类型**：特殊情况需添加注释说明
- **空安全检查**：必须处理 `null` 和 `undefined`
- **ESObject 使用规范**：仅在与 JS 库交互时使用，使用后立即转换

#### 1.2 语法限制
- **类字段初始化**：必须在声明时或构造函数中初始化
- **模块化规范**：使用 ES6 `import`/`export`，禁止 CommonJS `require`
- **类型声明**：禁止内联对象字面量作为类型，必须使用具名 `interface`/`type`
- **JSON 解析**：`JSON.parse()` 后必须转为显式结构类型

### 2. ArkUI 开发规范

#### 2.1 组件化设计
- **装饰器检查**：`@Component`、`@Entry` 使用规范
- **Builder 语法**：`@Builder` 内禁止 `return` 早退和普通语句块
- **组件拆分**：单个文件不超过 500 行

#### 2.2 状态管理
- **装饰器选择**：`@State`、`@Prop`、`@Link`、`@Provide`/`@Consume` 正确使用
- **状态更新**：必须通过赋值更新，禁止直接修改对象属性

#### 2.3 布局与样式
- **单位规范**：使用 `vp`/`fp`，禁止硬编码 `px`
- **布局性能**：减少 `Stack`/`Flex` 嵌套，优先使用 `RelativeContainer`
- **列表渲染**：必须使用 `LazyForEach` 并提供唯一 `keyGenerator`

### 3. 性能优化检查

#### 3.1 渲染性能
- **LazyForEach**：长列表必须使用懒加载
- **条件渲染**：频繁切换使用 `visibility` 而非 `if/else`
- **图片优化**：大图使用 `sourceSize` 属性

#### 3.2 并发与异步
- **主线程减负**：耗时操作移至 `TaskPool` 或 `Worker`
- **异步规范**：使用 Promise 或 async/await

#### 3.3 内存管理
- **资源释放**：`aboutToDisappear` 中注销监听和定时器
- **上下文泄漏**：禁止持有 `AbilityContext` 或 UI 组件引用

### 4. 项目架构规范

#### 4.1 目录结构
```
entry/src/main/ets/
├── pages/          # 页面入口 (@Entry)
├── components/     # 公共 UI 组件
├── model/          # 数据模型
├── utils/          # 工具类
├── service/        # 业务逻辑服务
└── resources/      # 静态资源
```

#### 4.2 命名规范
- **类/接口/组件**：PascalCase
- **变量/函数**：camelCase
- **常量/枚举**：UPPER_SNAKE_CASE

## 使用方法

### 命令行检查

```bash
# 检查单个文件
arkts-linter check src/main/ets/pages/Index.ets

# 检查整个目录
arkts-linter check src/main/ets/

# 自动修复可修复的问题
arkts-linter fix src/main/ets/pages/Index.ets
```

### 配置规则

在项目根目录创建 `.arktslintrc.json`：

```json
{
  "rules": {
    "no-any": "error",
    "no-unknown": "error",
    "static-method-this": "error",
    "component-syntax": "error",
    "indent": ["error", 2],
    "naming-convention": "error",
    "proper-decorator-use": "error",
    "component-root-node": "error",
    "state-management": "warning",
    "lazy-for-each": "error",
    "no-px-unit": "error",
    "use-vp-fp": "error"
  },
  "ignore": [
    "node_modules/**",
    "build/**",
    "oh_modules/**",
    "*.test.ets"
  ]
}
```

## 规则说明

| 规则名称 | 描述 | 严重程度 | 可修复 |
|---------|------|---------|--------|
| no-any | 禁止使用 any 类型 | error | false |
| no-unknown | 禁止使用 unknown 类型 | error | false |
| static-method-this | 静态方法中禁止使用 this | error | true |
| no-untyped-objects | 禁止无类型对象字面量 | error | false |
| component-syntax | 组件语法规范检查 | error | false |
| proper-decorator-use | 装饰器正确使用 | error | false |
| component-root-node | 组件根节点规则 | error | false |
| state-management | 状态管理最佳实践 | warning | false |
| lazy-for-each | 列表必须使用 LazyForEach | error | false |
| no-px-unit | 禁止硬编码 px 单位 | error | true |
| use-vp-fp | 必须使用 vp/fp 单位 | error | true |
| indent | 缩进规范 | error | true |
| naming-convention | 命名规范检查 | error | false |

## 忽略特定代码

```typescript
// 忽略单行
// @arktslint-ignore no-any
const data: any = getData();

// 忽略多行
// @arktslint-ignore no-any, no-unknown
const data: any = getData();
const info: unknown = getInfo();

// 忽略整个文件
// @arktslint-ignore-file
```

## 参考文档

- [HarmonyOS NEXT 开发文档](https://developer.huawei.com/consumer/cn/doc/)
- [ArkTS 语言规范](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides-V5/arkts-basics-V5)
- [ArkUI 开发指南](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides-V5/arkui-overview-V5)
- [性能优化最佳实践](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides-V5/performance-overview-V5)

## 许可证

MIT License
