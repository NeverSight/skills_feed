---
name: vue2-typescript-standards
description: Vue 2 项目 TypeScript 编码规范与类型定义标准。适用于编写 TypeScript 代码、定义类型接口、使用装饰器模式、工具函数开发等场景。
metadata:
  author: datagradient-ui
  version: "1.0"
---

# TypeScript 编码规范

## 何时使用

当需要编写或修改 TypeScript 代码时使用此规范，特别是：

- 定义类型接口和类型别名
- 使用装饰器模式
- 编写工具函数
- 处理类型导入和导出

## 类型定义

### 基本类型

```typescript
// ✅ GOOD - 明确类型
const modelName: string = 'test'
const count: number = 0
const isEdit: boolean = false

// ❌ BAD - 使用 any
const data: any = {}
```

### 接口与类型别名

```typescript
// ✅ GOOD - 使用接口定义对象结构
interface IDataModel {
  id: number
  name: string
  status: 'active' | 'inactive'
}

// ✅ GOOD - 使用类型别名
type Kv = Record<string, any>
type IGenericAction<T, R> = (params: T) => Promise<R>
```

### 泛型使用

```typescript
// ✅ GOOD - 使用泛型提高复用性
export default class AbsDataModelView <T = any> extends Vue {
  model: T | null = null
}

// ✅ GOOD - 函数泛型
function fetchData<T>(url: string): Promise<T> {
  return http.get<T>(url)
}
```

## 装饰器模式

### 类装饰器

```typescript
// ✅ GOOD
@Component
@StoreProvide([store])
export default class AbsDataModelView extends Vue {
  // ...
}
```

### 方法装饰器

```typescript
// ✅ GOOD - Vuex Action
@$store.Action('fetchDataModelPageList')
fetchDataModelPageList!: IGenericAction<IListParams, IListResult<IDataModelResultItem[]>>

// ✅ GOOD - Vuex State
@$store.State('dataModelList')
dataModelList!: IDataModelResultItem[]
```

## 工具函数

### 函数导出

```typescript
// ✅ GOOD - 命名导出
export const genRequired = (message?: string): IValidateRuleItem => {
  // ...
}

export const getRule = (type: string, message?: string): IValidateRuleItem => {
  // ...
}

// ✅ GOOD - 默认导出
export default class BaseWidget extends Vue {
  // ...
}
```

### 函数参数

```typescript
// ✅ GOOD - 可选参数使用 ?
function validate (rule: any, value: string, callback: Function): void {
  // ...
}

// ✅ GOOD - 默认参数
function createValidator (fn: (value: any) => boolean, message: string = '验证失败') {
  // ...
}
```

## 命名规范

- **类/接口/类型**：PascalCase（如 `AbsDataModelView`, `IDataModel`）
- **变量/函数**：camelCase（如 `modelName`, `fetchData()`）
- **常量**：UPPER_SNAKE_CASE（如 `MAX_LENGTH`, `API_BASE_URL`）
- **私有成员**：camelCase，前缀 `_`（如 `_internalState`）

## 导入规范

### 导入顺序

```typescript
// 1. Vue 相关
import { Component, Vue } from 'vue-property-decorator'
import { namespace } from 'vuex-class'

// 2. 第三方库
import { isObject, assign } from '@tdio/utils'

// 3. 项目工具
import { getRule, genRequired } from '@/utils/validator'
import { $t } from '@/lang'

// 4. 类型定义
import type { IDataModel } from '../types/dataModel'

// 5. 组件/视图
import AbsWorkbenchView from '../../AbsView/AbsWorkbenchView'
```

### 类型导入

```typescript
// ✅ GOOD - 使用 type 关键字
import type {
  IDataModelResultItem,
  IDataTypeItem
} from '../types/dataModel'

// ✅ GOOD - 混合导入
import { Component } from 'vue-property-decorator'
import type { Vue } from 'vue'
```

## 错误处理

```typescript
// ✅ GOOD - 明确的错误类型
try {
  await fetchData()
} catch (error) {
  console.error('Failed to fetch data:', error)
  throw new Error('数据获取失败')
}

// ❌ BAD - 忽略错误
try {
  await fetchData()
} catch (e) {}
```

## 最佳实践

1. **避免 any**：尽量使用具体类型，必要时使用 `unknown`
2. **类型推断**：充分利用 TypeScript 类型推断
3. **严格模式**：启用严格类型检查
4. **类型守卫**：使用类型守卫缩小类型范围
5. **注释**：复杂类型或逻辑应添加注释说明
