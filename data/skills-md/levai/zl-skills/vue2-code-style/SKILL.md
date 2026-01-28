---
name: vue2-code-style
description: Vue 2 项目代码风格与开发规范，包含命名规范、代码组织、注释规范、错误处理等。适用于所有代码编写场景，确保代码一致性、可读性和可维护性。
metadata:
  author: datagradient-ui
  version: "1.0"
---

# 代码风格规范

## 何时使用

在编写任何代码时都应遵循此规范，确保代码风格一致、可读性强、易于维护。

## 基本原则

1. **DRY 原则**：保持代码简洁、清晰、可维护，避免重复
2. **完整性**：代码必须完整、可运行，禁止留待办、占位或缺失部分
3. **可读性优先**：确保代码清晰、易维护
4. **避免过度设计**：仅使用必要的库和模式

## 命名规范

### 文件命名

- **组件文件**：PascalCase（如 `FlowDistributionDlg.vue`, `AbsWorkbenchView.ts`）
- **工具文件**：camelCase（如 `validator.ts`, `http.ts`）
- **常量文件**：camelCase（如 `constant.ts`, `config.ts`）

### 代码命名

- **类/组件/接口**：PascalCase（如 `AbsDataModelView`, `IDataModel`）
- **变量/函数/方法**：camelCase（如 `modelName`, `fetchData()`）
- **常量**：UPPER_SNAKE_CASE（如 `MAX_LENGTH`, `API_BASE_URL`）
- **私有成员**：camelCase，前缀 `_`（如 `_internalState`）

## 代码组织

### 导入顺序

```typescript
// 1. Vue/Vuex 相关
import { Component } from 'vue-property-decorator'

// 2. 第三方库
import { isObject } from '@tdio/utils'

// 3. 项目工具函数
import { getRule } from '@/utils/validator'

// 4. 类型定义
import type { IDataModel } from '../types'

// 5. 组件/视图
import AbsWorkbenchView from '../AbsView'
```

### 代码结构

```typescript
// 1. 装饰器
@Component({ ... })
export default class ComponentName extends BaseView {
  // 2. Props
  @Prop() value!: Kv
  
  // 3. Refs
  @Ref() formRef!: ElForm
  
  // 4. 数据属性
  model: Kv = {}
  
  // 5. 计算属性
  get computedValue () {
    return this.model.value
  }
  
  // 6. 方法
  validate () {
    // ...
  }
  
  // 7. 生命周期
  mounted () {
    // ...
  }
}
```

## 注释规范

### 代码注释

```typescript
// ✅ GOOD - 解释复杂逻辑
// 验证模型名称唯一性，需要异步调用接口
async ruleValRepeatVerify (rule, value: string, callback) {
  // ...
}

// ❌ BAD - 无意义的注释
// 设置值
setValue (key, value) {
  this.$set(this.value, key, value)
}
```

### 函数注释

```typescript
// ✅ GOOD - 复杂函数添加注释
/**
 * 生成必填验证规则
 * @param message 错误提示信息
 * @param trigger 触发时机，默认为 'change'
 * @returns 验证规则对象
 */
export const genRequired = (message?: string, trigger?: string): IValidateRuleItem => {
  // ...
}
```

## 错误处理

```typescript
// ✅ GOOD - 明确的错误处理
try {
  await this.saveData(this.model!)
} catch (error) {
  console.error('保存失败:', error)
  this.$message.error('保存失败，请重试')
  throw error
}

// ❌ BAD - 忽略错误
try {
  await this.saveData(this.model!)
} catch (e) {}
```

## 代码变更流程

1. **改动前先简述方案**：说明修改内容和原因
2. **一次只改一个文件**：避免大杂烩式提交
3. **仅修改相关代码**：不要动无关文件
4. **提交前检查**：确保代码可运行，无语法错误

## 最佳实践

1. **使用工具函数**：复用 `getRule`, `genRequired` 等工具函数
2. **类型安全**：充分利用 TypeScript 类型系统
3. **国际化**：使用 `$t()` 进行文本国际化
4. **性能优化**：避免不必要的计算和渲染
5. **代码审查**：提交前进行自我审查
