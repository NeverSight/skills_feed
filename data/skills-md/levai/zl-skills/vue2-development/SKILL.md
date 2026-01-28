---
name: vue2-development
description: Vue 2 + TypeScript 组件开发规范，使用 vue-property-decorator 类组件模式。适用于开发 Vue 单文件组件、表单组件、对话框组件等场景。
metadata:
  author: datagradient-ui
  version: "1.1"
---

# Vue 组件开发规范

## 何时使用

当需要开发或修改 Vue 组件时使用此规范，特别是：
- 创建新的 `.vue` 单文件组件
- 开发表单组件和对话框
- 使用装饰器模式定义组件
- 实现表单验证逻辑

## 组件结构

使用 Vue 2 + TypeScript + vue-property-decorator 的类组件模式。

### 标准模板

```vue
<template>
  <!-- 模板内容 -->
</template>

<script lang="ts">
// 1. 导入依赖
import { Component } from 'vue-property-decorator'
import { namespace } from 'vuex-class'

// 2. 导入工具函数
import { getRule, genRequired } from '@/utils/validator'

// 3. 导入组件
import AbsWorkbenchView from '../../AbsView/AbsWorkbenchView'

// 4. 组件装饰器
@Component({
  components: {
    // 组件注册
  },
  methods: {
    // 工具方法
  }
})
export default class ComponentName extends AbsWorkbenchView {
  // 组件逻辑
}
</script>

<style lang="scss" scoped>
/* 样式 */
</style>
```

## 装饰器使用

### Props 定义

```typescript
// ✅ GOOD
@Prop({ default: {} })
value!: Kv

@Prop()
readonly edit!: boolean

// ❌ BAD
@Prop() value
```

### Refs 定义

```typescript
// ✅ GOOD
@Ref()
formRef!: ElForm
```

### Watch 使用

```typescript
// ✅ GOOD
@Watch('value', { immediate: true })
setModel (newVal: Kv, oldVal: Kv) {
  if (!isEqual(newVal, oldVal)) {
    this.model = newVal
  }
}
```

### Vuex 绑定

```typescript
// ✅ GOOD
const $store = namespace('dataTag/dataModel')

@$store.Action('fetchDataModelPageList')
fetchDataModelPageList!: IGenericAction<IListParams, IListResult<IDataModelResultItem[]>>

@$store.State('dataModelList')
dataModelList!: IDataModelResultItem[]
```

## 表单验证

### 验证规则定义

```typescript
// ✅ GOOD
rules: Kv = {
  modelName: [
    getRule('required', '请输入模型名称'),
    {
      max: 50,
      message: '模型名称不得超过50个字符！'
    },
    {
      pattern: /^[a-zA-Z0-9_\u4e00-\u9fa5]+$/g,
      message: '仅支持中文、字母、数字和下划线'
    },
    {
      validator: this.ruleValRepeatVerify,
      trigger: 'blur'
    }
  ]
}

// 使用 genRequired
codeNameCn: [
  genRequired('请输入中文名称'),
  {
    pattern: /^[0-9_\u4e00-\u9fa5]+$/g,
    message: '中文名称只能包括中文、数字、下划线'
  }
]
```

### 验证方法

```typescript
// ✅ GOOD
validate () {
  return this.formRef.validate()
}

async ruleValRepeatVerify (rule, value: string, callback) {
  if (value) {
    const obj = {
      fieldCode: 1,
      id: Number(this.$route.query.id),
      value: this.model.modelName
    }
    await this.checkModelName(obj).then(res => {
      if (res) {
        callback(new Error('该名称已存在'))
      }
    })
  }
  callback()
}
```

## 命名规范

- **组件文件**：PascalCase（如 `FlowDistributionDlg.vue`）
- **组件类名**：PascalCase（如 `FlowDistributionDlg`）
- **属性/方法**：camelCase（如 `modelName`, `validate()`）

## 样式规范

- 使用 `scoped` 避免样式污染
- 使用 SCSS 预处理器
- 类名使用 kebab-case

```vue
<style lang="scss" scoped>
.model-flow-box {
  display: flex;
  justify-content: space-around;
  
  p {
    margin-bottom: 8px;
  }
}
</style>
```

## 最佳实践

1. **继承基类**：组件应继承对应的 AbsView 基类（如 `AbsWorkbenchView`, `AbsDataModelView`）
2. **类型定义**：使用 TypeScript 类型注解，避免使用 `any`
3. **国际化**：使用 `$t()` 进行文本国际化
4. **错误处理**：异步操作应包含错误处理逻辑
5. **代码复用**：提取公共逻辑到工具函数或基类

## 参考

详细规范请参考 [references/COMPONENT_GUIDE.md](references/COMPONENT_GUIDE.md)
