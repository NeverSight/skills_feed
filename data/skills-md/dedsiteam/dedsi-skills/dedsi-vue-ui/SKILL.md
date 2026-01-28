---
name: dedsi-vue-ui
displayName: Dedsi Vue UI 组件库
description: Dedsi-Vue-UI 是一个基于 Vue 3 + TypeScript 的现代化 UI 组件库，提供了 37+ 个高质量组件，涵盖基础、布局、导航、数据展示和反馈等场景。
version: 0.0.9
category: vue-components
tags:
  - vue3
  - typescript
  - ui-components
  - component-library
author: Dedsi
repository: https://github.com/Dedsi-Vue-UI
license: MIT
framework: vue@3.5.26
language: typescript@5.9.3

# 统计信息
stats:
  totalComponents: 60
  implementedComponents: 37
  unimplementedComponents: 23
  categories: 6

# 支持的组件类别
categories:
  - name: 基础组件
    count: 10
  - name: 布局组件
    count: 3
  - name: 导航组件
    count: 3
  - name: 数据展示组件
    count: 7
  - name: 反馈组件
    count: 9
  - name: 其他组件
    count: 5

# 核心特性
features:
  - Vue 3 Composition API
  - TypeScript 类型支持
  - 组件命名前缀: Dedsi
  - 响应式设计
  - 主题定制
  - 国际化支持
---

# Dedsi-Vue-UI 组件库 SKILL 文档

> 帮助 AI 理解和使用 Dedsi-Vue-UI 组件库的详细指南

## 目录

- [概述](#概述)
- [安装使用](#安装使用)
- [基础组件](#基础组件)
- [布局组件](#布局组件)
- [导航组件](#导航组件)
- [数据展示组件](#数据展示组件)
- [反馈组件](#反馈组件)
- [其他组件](#其他组件)

---

## 概述

Dedsi-Vue-UI 是一个基于 Vue 3 的组件库，提供了丰富的 UI 组件。所有组件都使用 `Dedsi` 前缀命名。

### 核心特性

- **Vue 3 Composition API**：充分利用 Vue 3 的新特性
- **TypeScript 支持**：完整的类型定义和类型推断
- **组件化设计**：高复用性和可组合性
- **响应式布局**：支持多种屏幕尺寸
- **主题定制**：支持自定义主题和样式

### 组件命名规则

- **单文件组件**：`Dedsi` + 功能名称（如 `DedsiAlert`、`DedsiButton`）
- **组合组件**：主组件 + 子组件（如 `DedsiMenu` + `DedsiMenuItem`）

### 组件使用规范

**重要**：在模板中使用组件时，必须使用 `components` 数组中注册的 `name` 值（kebab-case 格式），而不是 PascalCase 的组件类名。

| 组件类名（TypeScript 导入） | 模板中使用（name 值） |
|--------------------------|-------------------|
| `DedsiTable` | `dedsi-table` |
| `DedsiButton` | `dedsi-button` |
| `DedsiTag` | `dedsi-tag` |
| `DedsiSplit` | `dedsi-split` |
| `DedsiSpace` | `dedsi-space` |
| `DedsiAlert` | `dedsi-alert` |
| `DedsiTooltip` | `dedsi-tooltip` |
| `DedsiTabs` | `dedsi-tabs` |
| `DedsiTabPane` | `dedsi-tab-pane` |
| `DedsiQRCode` | `dedsi-qrcode` |
| `DedsiPopconfirm` | `dedsi-popconfirm` |
| `DedsiPopover` | `dedsi-popover` |
| `DedsiPopper` | `dedsi-popper` |
| `DedsiImage` | `dedsi-image` |
| `DedsiCard` | `dedsi-card` |
| `DedsiBadge` | `dedsi-badge` |
| `DedsiAvatar` | `dedsi-avatar` |
| `DedsiBreadcrumb` | `dedsi-breadcrumb` |
| `DedsiBreadcrumbItem` | `dedsi-breadcrumb-item` |
| `DedsiDivider` | `dedsi-divider` |
| `DedsiSegmented` | `dedsi-segmented` |
| `DedsiStatistic` | `dedsi-statistic` |
| `DedsiNumberConverter` | `dedsi-number-converter` |
| `DedsiTypography` | `dedsi-typography` |
| `DedsiDropdown` | `dedsi-dropdown` |
| `DedsiCountdown` | `dedsi-countdown` |
| `DedsiEmpty` | `dedsi-empty` |
| `DedsiResult` | `dedsi-result` |
| `DedsiDialog` | `dedsi-dialog` |
| `DedsiModal` | `dedsi-modal` |
| `DedsiMarquee` | `dedsi-marquee` |
| `DedsiScrollbar` | `dedsi-scrollbar` |
| `DedsiSkeleton` | `dedsi-skeleton` |
| `DedsiMenu` | `dedsi-menu` |
| `DedsiDrawer` | `dedsi-drawer` |
| `DedsiMenuItem` | `dedsi-menu-item` |
| `DedsiSubMenu` | `dedsi-sub-menu` |
| `DedsiRow` | `dedsi-row` |
| `DedsiCol` | `dedsi-col` |
| `DedsiForm` | `dedsi-form` |
| `DedsiFormItem` | `dedsi-form-item` |
| `DedsiInput` | `dedsi-input` |
| `DedsiInputNumber` | `dedsi-input-number` |
| `DedsiTextarea` | `dedsi-textarea` |
| `DedsiInputPassword` | `dedsi-input-password` |
| `DedsiSelect` | `dedsi-select` |
| `DedsiSelectOption` | `dedsi-select-option` |
| `DedsiDatePicker` | `dedsi-date-picker` |
| `DedsiTimePicker` | `dedsi-time-picker` |
| `DedsiTimeRangePicker` | `dedsi-time-range-picker` |
| `DedsiMonthPicker` | `dedsi-month-picker` |
| `DedsiRangePicker` | `dedsi-range-picker` |
| `DedsiRadio` | `dedsi-radio` |
| `DedsiRadioGroup` | `dedsi-radio-group` |
| `DedsiRadioButton` | `dedsi-radio-button` |
| `DedsiCheckbox` | `dedsi-checkbox` |
| `DedsiCheckboxGroup` | `dedsi-checkbox-group` |
| `DedsiSwitch` | `dedsi-switch` |
| `DedsiSlider` | `dedsi-slider` |
| `DedsiRate` | `dedsi-rate` |
| `DedsiUpload` | `dedsi-upload` |
| `DedsiTransfer` | `dedsi-transfer` |
| `DedsiAutoComplete` | `dedsi-auto-complete` |
| `DedsiCascader` | `dedsi-cascader` |
| `DedsiTreeSelect` | `dedsi-tree-select` |
| `DedsiMentions` | `dedsi-mentions` |

**使用示例**：
```vue
<template>
  <!-- ✅ 正确：使用 kebab-case 的 name 值 -->
  <dedsi-button>点击</dedsi-button>
  <dedsi-table :data="data" :columns="columns" />
  <dedsi-alert type="success" title="成功" />

  <!-- ❌ 错误：不要使用 PascalCase -->
  <DedsiButton>点击</DedsiButton>
  <DedsiTable :data="data" :columns="columns" />
</template>

<script setup lang="ts">
// ✅ 导入时使用 PascalCase
import { DedsiButton, DedsiTable, DedsiAlert } from 'dedsi-vue-ui'
</script>
```

### Props 定义规范

- 使用 Vue 3 Composition API 的 `defineProps`
- 支持类型推断和默认值
- 必需参数明确标注（`required: true` 或无默认值）
- 类型注解使用 TypeScript 联合类型：`type: 'primary' | 'success' | 'warning'`

### 事件命名规范

- 使用 Vue 3 标准事件：`update:propName` 用于双向绑定
- 事件名使用 kebab-case：`@page-change`、`@update:visible`
- 事件回调参数类型明确：`(page: number) => void`

### 插槽使用规范

- 插槽名使用 kebab-case
- 支持默认插槽和具名插槽
- 作用域插槽提供参数：`{ row, value }`

---

## 安装使用

```bash
npm install dedsi-vue-ui
```

```typescript
import { DedsiAlert, DedsiButton } from 'dedsi-vue-ui'

app.use(DedsiAlert)
app.use(DedsiButton)
```

---

## 基础组件

### DedsiAlert - 警告提示

**功能**：展现需要关注的信息，支持多种类型和关闭操作
**Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| title | string | - | 否 | 标题文本 |
| description | string | - | 否 | 辅助性文字描述 |
| type | 'success' \| 'info' \| 'warning' \| 'error' | 'info' | 否 | 警告类型，影响颜色和图标 |
| closable | boolean | false | 否 | 是否显示关闭按钮 |
| closeText | string | - | 否 | 关闭按钮的自定义文本 |
| showIcon | boolean | false | 否 | 是否显示左侧图标 |
| center | boolean | false | 否 | 文字是否居中显示 |

**Events**：
| 事件名 | 参数 | 说明 |
|--------|------|------|
| close | (event: MouseEvent) | 点击关闭按钮时触发 |

**Slots**：
| 插槽名 | 说明 |
|--------|------|
| default | 默认内容，通常放置描述文字 |
| title | 自定义标题内容 |
| icon | 自定义图标 |
| close | 自定义关闭按钮 |

**使用示例**：
```vue
<!-- 基础用法 -->
<DedsiAlert type="success" title="成功提示" description="操作已完成" />

<!-- 可关闭 -->
<DedsiAlert
  type="warning"
  title="警告"
  description="请注意查看"
  :closable="true"
  @close="handleClose"
/>

<!-- 自定义内容 -->
<DedsiAlert type="error">
  <template #title>错误</template>
  <p>发生错误，请重试</p>
</DedsiAlert>
```

---

### DedsiAvatar - 头像

**功能**：用来代表用户或事物，支持图片、图标或字符
**Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| src | string | - | 否 | 图片类资源的地址 |
| size | 'large' \| 'default' \| 'small' \| number | 'default' | 否 | 头像大小，可预设或自定义像素 |
| shape | 'circle' \| 'square' | 'circle' | 否 | 头像形状 |
| icon | any | - | 否 | 设置头像的图标组件 |
| alt | string | - | 否 | 图片无法显示时的替代文本 |
| fit | 'fill' \| 'contain' \| 'cover' \| 'none' \| 'scale-down' | 'cover' | 否 | 图片填充模式 |

**Events**：
| 事件名 | 参数 | 说明 |
|--------|------|------|
| error | (event: Event) | 图片加载失败时触发 |

**Slots**：
| 插槽名 | 说明 |
|--------|------|
| default | 自定义头像内容（如文字） |
| icon | 自定义图标 |

**使用示例**：
```vue
<!-- 图片头像 -->
<DedsiAvatar src="https://example.com/avatar.png" size="large" />

<!-- 文字头像 -->
<DedsiAvatar shape="square">User</DedsiAvatar>

<!-- 图标头像 -->
<DedsiAvatar>
  <template #icon><UserIcon /></template>
</DedsiAvatar>
```

---

### DedsiBadge - 徽标数

**功能**：用于展示通知数量或状态标记
**Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| value | string \| number | '' | 否 | 显示的数值或文字 |
| max | number | 99 | 否 | 最大值，超过显示为 max+ |
| isDot | boolean | false | 否 | 是否显示为小红点 |
| hidden | boolean | false | 否 | 是否隐藏 Badge |
| type | 'primary' \| 'success' \| 'warning' \| 'danger' | 'danger' | 否 | 徽标类型，影响颜色 |

**使用示例**：
```vue
<!-- 数字徽标 -->
<DedsiBadge :value="5">
  <DedsiButton>消息</DedsiButton>
</DedsiBadge>

<!-- 最大值 -->
<DedsiBadge :value="100" :max="99">
  <DedsiButton>通知</DedsiButton>
</DedsiBadge>

<!-- 小圆点 -->
<DedsiBadge isDot>
  <DedsiButton>状态</DedsiButton>
</DedsiBadge>
```

---

### DedsiBreadcrumb - 面包屑

**功能**：显示当前页面在系统层级结构中的位置
**DedsiBreadcrumb Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| separator | string | '/' | 否 | 分隔符自定义 |

**DedsiBreadcrumbItem Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| to | string \| object | - | 否 | 路由跳转目标，同 Vue Router |
| replace | boolean | false | 否 | 是否使用 replace 模式跳转 |

**Slots**：
| 插槽名 | 组件 | 说明 |
|--------|------|------|
| separator | DedsiBreadcrumbItem | 自定义分隔符内容 |
| default | DedsiBreadcrumb | 面包屑项列表 |

**使用示例**：
```vue
<DedsiBreadcrumb separator=">">
  <DedsiBreadcrumbItem to="/">首页</DedsiBreadcrumbItem>
  <DedsiBreadcrumbItem to="/components">组件</DedsiBreadcrumbItem>
  <DedsiBreadcrumbItem>面包屑</DedsiBreadcrumbItem>
</DedsiBreadcrumb>
```

---

### DedsiCard - 卡片

**功能**：通用卡片容器，可包含标题、额外操作、内容和底部
**Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| title | string | - | 否 | 卡片标题 |
| bordered | boolean | true | 否 | 是否有边框 |
| hoverable | boolean | false | 否 | 鼠标悬停时是否可浮起 |
| noShadow | boolean | true | 否 | 是否无阴影 |
| shadow | 'always' \| 'hover' \| 'never' | 'hover' | 否 | 阴影显示时机 |
| bodyStyle | Record<string, any> | - | 否 | 内容区域自定义样式对象 |

**Slots**：
| 插槽名 | 说明 |
|--------|------|
| default | 卡片内容 |
| title | 自定义标题 |
| extra | 标题旁的额外操作区 |
| footer | 底部内容 |

**使用示例**：
```vue
<!-- 基础卡片 -->
<DedsiCard title="卡片标题">
  <p>卡片内容</p>
</DedsiCard>

<!-- 带额外操作 -->
<DedsiCard>
  <template #title>
    <span>标题</span>
  </template>
  <template #extra>
    <DedsiButton>更多</DedsiButton>
  </template>
  <p>内容</p>
</DedsiCard>
```

---

### DedsiDivider - 分割线

**功能**：区隔内容的分割线，可包含文字
**Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| direction | 'horizontal' \| 'vertical' | 'horizontal' | 否 | 分割线方向 |
| contentPosition | 'left' \| 'center' \| 'right' | 'center' | 否 | 文本内容位置（仅水平） |
| dashed | boolean | false | 否 | 是否为虚线 |

**使用示例**：
```vue
<!-- 水平分割线 -->
<DedsiDivider>文本</DedsiDivider>

<!-- 虚线 -->
<DedsiDivider dashed />

<!-- 垂直分割线 -->
<DedsiSpace>
  <span>文本1</span>
  <DedsiDivider direction="vertical" />
  <span>文本2</span>
</DedsiSpace>
```

---

### DedsiEmpty - 空状态

**功能**：空状态时的占位展示
**Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| image | string | - | 否 | 空状态图片地址 |
| imageSize | number \| string | 120 | 否 | 图片大小 |
| description | string | '暂无数据' | 否 | 描述文本 |

**Slots**：
| 插槽名 | 说明 |
|--------|------|
| default | 底部内容 |
| image | 自定义图片 |
| description | 自定义描述 |

**使用示例**：
```vue
<!-- 基础用法 -->
<DedsiEmpty description="暂无数据" />

<!-- 自定义内容 -->
<DedsiEmpty>
  <DedsiButton>创建</DedsiButton>
</DedsiEmpty>
```

---

### DedsiTag - 标签

**功能**：进行标记和分类
**Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| type | 'default' \| 'primary' \| 'success' \| 'warning' \| 'danger' | 'default' | 否 | 标签类型 |
| size | 'large' \| 'default' \| 'small' | 'default' | 否 | 标签尺寸 |
| closable | boolean | false | 否 | 是否可关闭 |
| round | boolean | false | 否 | 是否为圆角 |
| color | string | - | 否 | 自定义文字颜色 |
| backgroundColor | string | - | 否 | 自定义背景色 |
| borderColor | string | - | 否 | 自定义边框颜色 |

**Events**：
| 事件名 | 参数 | 说明 |
|--------|------|------|
| close | (event: MouseEvent) | 关闭时触发 |

**使用示例**：
```vue
<!-- 基础标签 -->
<DedsiTag type="success">成功</DedsiTag>

<!-- 可关闭 -->
<DedsiTag closable @close="handleClose">可关闭</DedsiTag>

<!-- 自定义颜色 -->
<DedsiTag color="#f50" backgroundColor="#fff1f0">自定义</DedsiTag>
```

---

### DedsiSpace - 间距

**功能**：设置组件之间的间距
**Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| direction | 'horizontal' \| 'vertical' | 'horizontal' | 否 | 间距方向 |
| size | 'small' \| 'middle' \| 'large' \| number \| [number, number] | 'small' | 否 | 间距大小，支持数组 [水平, 垂直] |
| wrap | boolean | false | 否 | 是否自动换行 |
| align | 'start' \| 'end' \| 'center' \| 'baseline' | - | 否 | 对齐方式 |

**使用示例**：
```vue
<!-- 水平间距 -->
<DedsiSpace :size="middle">
  <DedsiButton>按钮1</DedsiButton>
  <DedsiButton>按钮2</DedsiButton>
</DedsiSpace>

<!-- 垂直间距 -->
<DedsiSpace direction="vertical" :size="20">
  <div>内容1</div>
  <div>内容2</div>
</DedsiSpace>
```

---

### DedsiSplit - 分割布局

**功能**：左右分割的布局容器
**Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| align | 'top' \| 'center' \| 'bottom' \| 'baseline' | 'center' | 否 | 左右内容的对齐方式 |
| padding | string \| number | - | 否 | 内边距 |
| gap | string \| number | - | 否 | 左右间距 |

**Slots**：
| 插槽名 | 说明 |
|--------|------|
| default | 左侧内容（无 right 插槽时使用） |
| left | 左侧内容 |
| right | 右侧内容 |

**使用示例**：
```vue
<DedsiSplit :gap="20">
  <template #left>
    <p>左侧内容</p>
  </template>
  <template #right>
    <p>右侧内容</p>
  </template>
</DedsiSplit>
```

---

## 布局组件

### DedsiRow / DedsiCol - 栅格布局

**功能**：24 栅格响应式布局系统
**DedsiRow Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| gutter | number \| [number, number] | - | 否 | 栅格间隔，可设为 [水平间距, 垂直间距] |
| justify | 'start' \| 'end' \| 'center' \| 'space-around' \| 'space-between' | - | 否 | 水平排列方式 |
| align | 'top' \| 'middle' \| 'bottom' | - | 否 | 垂直对齐方式 |

**DedsiCol Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| span | number | 24 | 否 | 栅格占位格数（0-24） |
| offset | number | 0 | 否 | 栅格左侧间隔格数 |
| xs | number \| object | - | 否 | <576px 响应式栅格 |
| sm | number \| object | - | 否 | ≥576px 响应式栅格 |
| md | number \| object | - | 否 | ≥768px 响应式栅格 |
| lg | number \| object | - | 否 | ≥992px 响应式栅格 |
| xl | number \| object | - | 否 | ≥1200px 响应式栅格 |

**响应式对象格式**：
```typescript
{
  span: number,    // 栅格占位格数
  offset: number   // 栅格左侧间隔格数
}
```

**使用示例**：
```vue
<!-- 基础用法 -->
<DedsiRow :gutter="16">
  <DedsiCol :span="12">col-12</DedsiCol>
  <DedsiCol :span="12">col-12</DedsiCol>
</DedsiRow>

<!-- 偏移 -->
<DedsiRow>
  <DedsiCol :span="8" :offset="8">col-8 offset-8</DedsiCol>
</DedsiRow>

<!-- 响应式 -->
<DedsiRow>
  <DedsiCol :xs="24" :sm="12" :md="8">响应式</DedsiCol>
  <DedsiCol :xs="24" :sm="12" :md="8">响应式</DedsiCol>
  <DedsiCol :xs="24" :sm="12" :md="8">响应式</DedsiCol>
</DedsiRow>
```

---

### DedsiScrollbar - 滚动条

**功能**：自定义滚动条样式
**Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| height | string \| number | - | 否 | 容器高度 |
| maxHeight | string \| number | - | 否 | 容器最大高度 |
| native | boolean | false | 否 | 是否使用原生滚动条 |
| wrapStyle | any | - | 否 | 容器的自定义样式 |
| viewStyle | any | - | 否 | 视图的自定义样式 |
| wrapClass | string | - | 否 | 容器的自定义类名 |
| viewClass | string | - | 否 | 视图的自定义类名 |
| always | boolean | false | 否 | 是否一直显示滚动条 |
| minSize | number | 20 | 否 | 滚动条最小尺寸 |

**暴露方法**（通过 ref）：
| 方法名 | 参数 | 说明 |
|--------|------|------|
| wrapRef | - | 获取容器 DOM 引用 |
| update | () | 手动更新滚动条 |
| scrollTo | (options: ScrollToOptions) | 滚动到指定位置 |
| setScrollTop | (val: number) | 设置垂直滚动距离 |
| setScrollLeft | (val: number) | 设置水平滚动距离 |

**使用示例**：
```vue
<template>
  <DedsiScrollbar ref="scrollbar" height="400px">
    <div v-for="i in 100" :key="i">内容 {{ i }}</div>
  </DedsiScrollbar>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const scrollbar = ref()

// 滚动到顶部
const scrollToTop = () => {
  scrollbar.value?.setScrollTop(0)
}
</script>
```

---

### DedsiSkeleton - 骨架屏

**功能**：在数据加载时展示占位效果
**Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| loading | boolean | true | 否 | 是否显示骨架屏 |
| active | boolean | true | 否 | 是否开启动画效果 |
| avatar | boolean | false | 否 | 是否显示头像占位 |
| avatarSize | number \| 'small' \| 'large' \| 'default' | 'default' | 否 | 头像大小 |
| avatarShape | 'circle' \| 'square' | 'circle' | 否 | 头像形状 |
| title | boolean | true | 否 | 是否显示标题占位 |
| titleWidth | number \| string | - | 否 | 标题占位宽度 |
| paragraph | boolean \| object | true | 否 | 段落配置，true 或 { rows: number, width?: array } |

**Slots**：
| 插槽名 | 说明 |
|--------|------|
| default | 加载完成后的实际内容 |
| template | 自定义骨架屏模板 |

**使用示例**：
```vue
<!-- 基础用法 -->
<DedsiSkeleton :loading="loading">
  <div>实际内容</div>
</DedsiSkeleton>

<!-- 复杂配置 -->
<DedsiSkeleton
  :loading="loading"
  :avatar="true"
  avatarSize="large"
  :paragraph="{ rows: 4 }"
>
  <UserProfile />
</DedsiSkeleton>
```

---

## 导航组件

### DedsiMenu - 导航菜单

**功能**：导航菜单，支持多级嵌套和折叠
**DedsiMenu Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| items | MenuItem[] | 是 | - | 菜单项数据数组 |
| mode | 'vertical' \| 'horizontal' \| 'inline' | 'inline' | 否 | 菜单模式 |
| theme | 'light' \| 'dark' | 'light' | 否 | 菜单主题 |
| selectedKeys | string[] | [] | 否 | 当前选中的菜单项 key 数组 |
| openKeys | string[] | [] | 否 | 当前展开的子菜单 key 数组 |
| collapsed | boolean | false | 否 | 是否收起菜单（仅 inline） |

**MenuItem 接口**：
```typescript
interface MenuItem {
  key: string              // 唯一标识
  label: string            // 菜单项标题
  icon?: any              // 图标组件
  disabled?: boolean      // 是否禁用
  children?: MenuItem[]   // 子菜单项
}
```

**Events**：
| 事件名 | 参数 | 说明 |
|--------|------|------|
| update:selectedKeys | (keys: string[]) | 选中项变化 |
| update:openKeys | (keys: string[]) | 展开项变化 |
| click | (item: MenuItem) | 点击菜单项 |

**使用示例**：
```vue
<template>
  <DedsiMenu
    :items="menuItems"
    v-model:selectedKeys="selectedKeys"
    v-model:openKeys="openKeys"
    mode="inline"
    theme="dark"
    @click="handleMenuClick"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'

const selectedKeys = ref(['home'])
const openKeys = ref([])

const menuItems = [
  {
    key: 'home',
    label: '首页',
    icon: HomeIcon
  },
  {
    key: 'components',
    label: '组件',
    icon: ComponentIcon,
    children: [
      { key: 'basic', label: '基础组件' },
      { key: 'layout', label: '布局组件' }
    ]
  }
]

const handleMenuClick = (item: any) => {
  console.log('点击菜单', item)
}
</script>
```

---

### DedsiTabs - 标签页

**功能**：选项卡切换组件
**DedsiTabs Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| modelValue / activeKey | string \| number | - | 否 | 当前激活的标签页 key |
| type | 'line' \| 'card' \| 'editable-card' | 'line' | 否 | 标签页类型 |
| hideAdd | boolean | false | 否 | 是否隐藏添加按钮（editable-card） |
| size | 'default' \| 'small' | 'default' | 否 | 标签页尺寸 |
| tabBarGutter | number | - | 否 | 标签之间的间距 |

**DedsiTabPane Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| label | string | 是 | - | 标签文本 |
| name | string \| number | 是 | - | 标签的唯一标识 |
| disabled | boolean | false | 否 | 是否禁用 |
| closable | boolean | true | 否 | 是否可关闭（editable-card） |

**Events**：
| 事件名 | 参数 | 说明 |
|--------|------|------|
| update:modelValue | (name: string \| number) | 激活标签变化 |
| update:activeKey | (name: string \| number) | 激活标签变化 |
| tab-click | (name: string \| number) | 点击标签 |
| change | (name: string \| number) | 切换标签 |
| refresh | (name: string \| number) | 刷新标签（editable-card） |
| edit | (targetKey: string \| number, action: 'add' \| 'remove') | 添加/删除标签 |

**Slots**：
| 插槽名 | 组件 | 说明 |
|--------|------|------|
| default | DedsiTabs | 标签页内容（DedsiTabPane） |
| extra | DedsiTabs | 标签栏右侧额外操作区 |

**使用示例**：
```vue
<!-- 基础用法 -->
<DedsiTabs v-model:activeKey="activeKey">
  <DedsiTabPane name="1" label="标签1">内容1</DedsiTabPane>
  <DedsiTabPane name="2" label="标签2">内容2</DedsiTabPane>
</DedsiTabs>

<!-- 卡片类型 -->
<DedsiTabs type="card">
  <DedsiTabPane name="1" label="标签1">内容1</DedsiTabPane>
</DedsiTabs>

<!-- 可编辑 -->
<DedsiTabs v-model:activeKey="activeKey" type="editable-card" @edit="handleEdit">
  <DedsiTabPane v-for="tab in tabs" :key="tab.key" :name="tab.key" :label="tab.label">
    {{ tab.content }}
  </DedsiTabPane>
</DedsiTabs>
```

---

### DedsiDropdown - 下拉菜单

**功能**：下拉菜单，支持点击和悬停触发
**Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| menu | DropdownMenuItem[] | 是 | - | 菜单项数组 |
| trigger | 'hover' \| 'click' | 'hover' | 否 | 触发方式 |
| placement | 'bottomLeft' \| 'bottomCenter' \| 'bottomRight' \| 'topLeft' \| ... | 'bottomLeft' | 否 | 菜单位置 |
| disabled | boolean | false | 否 | 是否禁用 |

**DropdownMenuItem 接口**：
```typescript
interface DropdownMenuItem {
  key: string | number     // 唯一标识
  label?: string           // 菜单项文本
  icon?: any              // 图标组件
  disabled?: boolean      // 是否禁用
  danger?: boolean        // 是否危险操作（红色）
  type?: 'item' | 'divider'  // 类型：菜单项或分割线
}
```

**Events**：
| 事件名 | 参数 | 说明 |
|--------|------|------|
| select | (key: string \| number) | 选择菜单项时触发 |

**使用示例**：
```vue
<template>
  <DedsiDropdown :menu="menuItems" @select="handleSelect">
    <DedsiButton>下拉菜单</DedsiButton>
  </DedsiDropdown>
</template>

<script setup lang="ts">
const menuItems = [
  { key: '1', label: '菜单项1', icon: EditIcon },
  { key: '2', label: '菜单项2', icon: DeleteIcon, danger: true },
  { type: 'divider' },
  { key: '3', label: '菜单项3', disabled: true }
]

const handleSelect = (key: string | number) => {
  console.log('选择了', key)
}
</script>
```

---

## 数据展示组件

### DedsiStatistic - 统计数值

**功能**：展示统计数值，支持数字动画
**Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| title | string | - | 否 | 数值的标题 |
| value | number | 是 | - | 数值内容 |
| precision | number | 0 | 否 | 数值精度（小数位数） |
| prefix | string | - | 否 | 前缀 |
| suffix | string | - | 否 | 后缀 |
| showGroup | boolean | true | 否 | 是否显示千分位分隔符 |
| duration | number | 1500 | 否 | 数字动画持续时间（ms） |
| animation | boolean | true | 否 | 是否开启动画 |
| contentStyle | Record<string, string> | - | 否 | 数值内容的自定义样式 |

**Slots**：
| 插槽名 | 说明 |
|--------|------|
| title | 自定义标题 |
| prefix | 自定义前缀 |
| suffix | 自定义后缀 |

**使用示例**：
```vue
<!-- 基础用法 -->
<DedsiStatistic title="总用户数" :value="12345" />

<!-- 带前后缀 -->
<DedsiStatistic title="账户余额" :value="1234.56" prefix="¥" :precision="2" />

<!-- 自定义样式 -->
<DedsiStatistic
  title="成交量"
  :value="12345"
  :contentStyle="{ color: '#3f8600', fontSize: '24px' }"
/>
```

---

### DedsiNumberConverter - 数字转换

**功能**：将数字转换为万/千万/亿单位显示
**Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| value | number \| string | 是 | - | 要转换的数值 |
| targetUnit | 'none' \| 'wan' \| 'qianwan' \| 'yi' \| 'auto' | 'auto' | 否 | 目标单位，auto 自动选择 |
| precision | number | 2 | 否 | 保留小数位数 |
| suffix | string | '' | 否 | 单位后缀（如"元"、"人"） |

**使用示例**：
```vue
<!-- 自动转换 -->
<DedsiNumberConverter :value="12345" />
<!-- 显示：1.23万 -->

<!-- 指定单位 -->
<DedsiNumberConverter :value="12345" targetUnit="wan" suffix="元" />
<!-- 显示：1.23万元 -->

<!-- 千万级别 -->
<DedsiNumberConverter :value="12345678" targetUnit="qianwan" />
<!-- 显示：1234.57千万 -->
```

---

### DedsiCountdown - 倒计时

**功能**：实时倒计时展示
**Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| title | string | - | 否 | 标题 |
| value | number \| string \| Date | 是 | - | 目标时间（时间戳或日期对象） |
| format | string | 'HH:mm:ss' | 否 | 时间格式化模板 |
| prefix | string | - | 否 | 前缀文本 |
| suffix | string | - | 否 | 后缀文本 |
| valueStyle | Record<string, string> | - | 否 | 数值的自定义样式 |

**Events**：
| 事件名 | 参数 | 说明 |
|--------|------|------|
| finish | () | 倒计时结束时触发 |
| change | (value: number) | 时间变化时触发，返回剩余毫秒数 |

**Slots**：
| 插槽名 | 说明 |
|--------|------|
| title | 自定义标题 |
| prefix | 自定义前缀 |
| suffix | 自定义后缀 |

**使用示例**：
```vue
<!-- 基础用法 -->
<DedsiCountdown :value="Date.now() + 10000000" />

<!-- 自定义格式 -->
<DedsiCountdown
  title="活动倒计时"
  :value="targetTime"
  format="DD天 HH:mm:ss"
  suffix="后结束"
  @finish="handleFinish"
/>
```

---

### DedsiTable - 表格

**功能**：表格展示，支持分页和自定义列渲染
**Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| data | Record<string, any>[] | 是 | - | 表格数据数组 |
| columns | Column[] | 是 | - | 列配置数组 |
| total | number | 是 | - | 数据总条数 |
| pageSize | number | 10 | 否 | 每页显示条数 |
| bordered | boolean | false | 否 | 是否显示边框 |
| showIndex | boolean | false | 否 | 是否显示序号列 |
| indexColumnTitle | string | '序号' | 否 | 序号列的标题 |
| pagination | boolean | true | 否 | 是否显示分页器 |

**Column 接口**：
```typescript
interface Column {
  key: string                        // 列的唯一标识，用于插槽匹配
  title: string                      // 列标题
  width?: string                     // 列宽度（CSS 值）
  align?: 'left' | 'center' | 'right'  // 对齐方式
}
```

**Events**：
| 事件名 | 参数 | 说明 |
|--------|------|------|
| page-change | (page: number) | 页码变化 |
| page-size-change | (pageSize: number) | 每页条数变化 |

**Slots**：
| 插槽名 | 参数 | 说明 |
|--------|------|------|
| [column.key] | { row: any, value: any } | 自定义列内容，插槽名为列的 key |

**使用示例**：
```vue
<template>
  <DedsiTable
    :data="tableData"
    :columns="columns"
    :total="total"
    :pageSize="20"
    :showIndex="true"
    @page-change="handlePageChange"
  >
    <!-- 自定义操作列 -->
    <template #actions="{ row }">
      <DedsiButton @click="edit(row)">编辑</DedsiButton>
      <DedsiButton @click="del(row)">删除</DedsiButton>
    </template>

    <!-- 自定义状态列 -->
    <template #status="{ value }">
      <DedsiTag :type="value === 1 ? 'success' : 'danger'">
        {{ value === 1 ? '启用' : '禁用' }}
      </DedsiTag>
    </template>
  </DedsiTable>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const tableData = ref([
  { name: '张三', age: 25, status: 1 },
  { name: '李四', age: 30, status: 0 }
])

const total = ref(100)

const columns = [
  { key: 'name', title: '姓名', width: '200px' },
  { key: 'age', title: '年龄', align: 'center' },
  { key: 'status', title: '状态', align: 'center' },
  { key: 'actions', title: '操作', width: '200px' }
]

const handlePageChange = (page: number) => {
  console.log('当前页', page)
}
</script>
```

---

### DedsiTypography - 排版

**功能**：文本排版组件，支持复制、编辑、省略等功能
**Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| tag | string | 'span' | 否 | 渲染的 HTML 标签 |
| type | 'secondary' \| 'success' \| 'warning' \| 'danger' | - | 否 | 文字颜色类型 |
| disabled | boolean | false | 否 | 是否禁用样式 |
| mark | boolean | false | 否 | 是否标记样式（黄色背景） |
| code | boolean | false | 否 | 是否行内代码样式 |
| delete | boolean | false | 否 | 是否删除线 |
| underline | boolean | false | 否 | 是否下划线 |
| strong | boolean | false | 否 | 是否加粗 |
| copyable | boolean \| string | false | 否 | 是否可复制，可设置复制提示文本 |
| editable | boolean | false | 否 | 是否可编辑 |
| ellipsis | boolean \| { rows: number } | false | 否 | 是否省略，可设置省略行数 |

**Events**：
| 事件名 | 参数 | 说明 |
|--------|------|------|
| update:modelValue | (value: string) | 内容值变化 |
| change | (value: string) | 编辑完成时触发 |

**使用示例**：
```vue
<!-- 基础文本 -->
<DedsiTypography>普通文本</DedsiTypography>

<!-- 次要文本 -->
<DedsiTypography type="secondary">次要文本</DedsiTypography>

<!-- 可复制 -->
<DedsiTypography copyable>这段文字可以复制</DedsiTypography>

<!-- 可编辑 -->
<DedsiTypography editable v-model="text">{{ text }}</DedsiTypography>

<!-- 省略 -->
<DedsiTypography :ellipsis="{ rows: 2 }">
  这是一段很长的文字内容，超过两行后会显示省略号...
</DedsiTypography>

<!-- 组合使用 -->
<DedsiTypography strong underline>
  <DedsiTypography code>重要</DedsiTypography>
  提示
</DedsiTypography>
```

---

### DedsiImage - 图片

**功能**：图片预览，支持缩放、旋转、多图切换
**Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| src | string | 是 | - | 图片地址 |
| alt | string | - | 否 | 替代文本 |
| width | string \| number | '100%' | 否 | 图片宽度 |
| height | string \| number | 'auto' | 否 | 图片高度 |
| fit | 'fill' \| 'contain' \| 'cover' \| 'none' \| 'scale-down' | 'cover' | 否 | 图片填充模式 |
| preview | boolean | true | 否 | 是否可预览 |
| previewSrcList | string[] | [] | 否 | 预览图片列表 |

**使用示例**：
```vue
<!-- 基础用法 -->
<DedsiImage
  src="https://example.com/image.jpg"
  width="200px"
  height="200px"
/>

<!-- 多图预览 -->
<DedsiImage
  :src="currentImage"
  :previewSrcList="imageList"
  fit="cover"
/>
```

---

### DedsiQRCode - 二维码

**功能**：生成二维码
**Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| value | string | 是 | - | 二维码内容 |
| size | number | 160 | 否 | 二维码尺寸（px） |
| color | string | '#000000' | 否 | 前景色 |
| backgroundColor | string | '#ffffff' | 否 | 背景色 |
| margin | number | 2 | 否 | 边距 |
| errorCorrectionLevel | 'L' \| 'M' \| 'Q' \| 'H' | 'M' | 否 | 容错级别 |

**Slots**：
| 插槽名 | 说明 |
|--------|------|
| loading | 加载状态内容 |
| error | 错误状态内容 |

**使用示例**：
```vue
<!-- 基础用法 -->
<DedsiQRCode value="https://example.com" />

<!-- 自定义样式 -->
<DedsiQRCode
  value="https://example.com"
  :size="200"
  color="#1890ff"
  backgroundColor="#f0f0f0"
  errorCorrectionLevel="H"
/>
```

---

## 反馈组件

### DedsiDialog - 对话框

**功能**：模态对话框，带有确认/取消按钮
**Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| visible | boolean | false | 是 | 是否可见 |
| title | string | - | 否 | 对话框标题 |
| width | number \| string | 520 | 否 | 对话框宽度 |
| centered | boolean | false | 否 | 是否垂直居中 |
| closable | boolean | true | 否 | 是否显示关闭按钮 |
| maskClosable | boolean | true | 否 | 点击蒙层是否关闭对话框 |
| okText | string | '确定' | 否 | 确认按钮文本 |
| cancelText | string | '取消' | 否 | 取消按钮文本 |
| confirmLoading | boolean | false | 否 | 确认按钮的 loading 状态 |
| footerHidden | boolean | false | 否 | 是否隐藏底部按钮区 |
| type | 'info' \| 'success' \| 'warning' \| 'error' | - | 否 | 对话框类型，显示对应图标 |

**Events**：
| 事件名 | 参数 | 说明 |
|--------|------|------|
| update:visible | (visible: boolean) | 显示状态变化 |
| ok | () | 点击确认按钮 |
| cancel | () | 点击取消按钮 |
| close | () | 关闭对话框时 |

**Slots**：
| 插槽名 | 说明 |
|--------|------|
| default | 对话框内容 |
| title | 自定义标题 |
| footer | 自定义底部 |

**使用示例**：
```vue
<template>
  <DedsiDialog
    v-model:visible="visible"
    title="对话框"
    :confirmLoading="loading"
    @ok="handleOk"
    @cancel="handleCancel"
  >
    <p>对话框内容</p>
  </DedsiDialog>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const visible = ref(false)
const loading = ref(false)

const handleOk = () => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
    visible.value = false
  }, 1000)
}

const handleCancel = () => {
  visible.value = false
}
</script>
```

---

### DedsiModal - 模态框

**功能**：基础模态框
**Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| visible | boolean | false | 是 | 是否可见 |
| title | string | - | 否 | 标题 |
| width | number \| string | 520 | 否 | 宽度 |
| centered | boolean | false | 否 | 是否垂直居中 |
| closable | boolean | true | 否 | 是否显示关闭按钮 |
| mask | boolean | true | 否 | 是否显示遮罩层 |
| maskClosable | boolean | true | 否 | 点击遮罩是否关闭 |

**Events**：
| 事件名 | 参数 | 说明 |
|--------|------|------|
| update:visible | (visible: boolean) | 显示状态变化 |
| cancel | () | 点击取消或关闭 |

**Slots**：
| 插槽名 | 说明 |
|--------|------|
| default | 内容 |
| title | 自定义标题 |

---

### DedsiDrawer - 抽屉

**功能**：从屏幕边缘滑出的浮层面板
**Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| visible | boolean | false | 是 | 是否可见 |
| title | string | - | 否 | 标题 |
| placement | 'left' \| 'right' \| 'top' \| 'bottom' | 'right' | 否 | 位置 |
| width | number \| string | 378 | 否 | 宽度（left/right） |
| height | number \| string | 378 | 否 | 高度（top/bottom） |
| closable | boolean | true | 否 | 是否显示关闭按钮 |
| mask | boolean | true | 否 | 是否显示遮罩 |
| maskClosable | boolean | true | 否 | 点击遮罩是否关闭 |

**Events**：
| 事件名 | 参数 | 说明 |
|--------|------|------|
| update:visible | (visible: boolean) | 显示状态变化 |
| close | () | 关闭时触发 |

**Slots**：
| 插槽名 | 说明 |
|--------|------|
| default | 内容 |
| title | 自定义标题 |
| footer | 底部内容 |

**使用示例**：
```vue
<template>
  <DedsiDrawer
    v-model:visible="visible"
    title="抽屉标题"
    placement="right"
    :width="600"
  >
    <p>抽屉内容</p>
    <template #footer>
      <DedsiButton @click="visible = false">关闭</DedsiButton>
    </template>
  </DedsiDrawer>
</template>
```

---

### DedsiMessage - 全局提示

**功能**：全局提示消息，通常命令式调用
**Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| content | string | 是 | - | 提示内容 |
| type | 'info' \| 'success' \| 'warning' \| 'error' \| 'loading' | 'info' | 否 | 提示类型 |
| duration | number | 3000 | 否 | 持续时间（ms），0 为不自动关闭 |
| onClose | () => void | - | 否 | 关闭回调 |

**暴露方法**：
| 方法名 | 说明 |
|--------|------|
| close | 主动关闭提示 |

**使用示例**：
```vue
<!-- 声明式使用 -->
<DedsiMessage content="这是一条消息" type="success" :duration="2000" />

<!-- 命令式使用（推荐） -->
<script setup lang="ts">
import { getCurrentInstance } from 'vue'

const instance = getCurrentInstance()

// 显示不同类型的消息
const showMessage = () => {
  instance?.proxy?.$message.info('普通消息')
  instance?.proxy?.$message.success('成功消息')
  instance?.proxy?.$message.warning('警告消息')
  instance?.proxy?.$message.error('错误消息')
  instance?.proxy?.$message.loading('加载中...')

  // 手动关闭
  const msg = instance?.proxy?.$message.info('不会自动关闭', 0)
  setTimeout(() => {
    msg?.close()
  }, 5000)
}
</script>
```

---

### DedsiPopconfirm - 气泡确认框

**功能**：点击元素触发气泡确认框
**Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| title | string | 是 | - | 确认框标题 |
| confirmText | string | '确定' | 否 | 确认按钮文本 |
| cancelText | string | '取消' | 否 | 取消按钮文本 |
| placement | 'top' \| 'bottom' \| 'left' \| 'right' \| ... | 'top' | 否 | 位置 |
| disabled | boolean | false | 否 | 是否禁用 |

**Events**：
| 事件名 | 参数 | 说明 |
|--------|------|------|
| confirm | () | 点击确认 |
| cancel | () | 点击取消 |

**使用示例**：
```vue
<DedsiPopconfirm
  title="确定要删除吗？"
  @confirm="handleDelete"
  @cancel="handleCancel"
>
  <DedsiButton danger>删除</DedsiButton>
</DedsiPopconfirm>
```

---

### DedsiPopover - 气泡卡片

**功能**：点击或悬停时显示气泡卡片
**Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| title | string | - | 否 | 标题 |
| content | string | - | 否 | 内容 |
| placement | 'top' \| 'bottom' \| 'left' \| 'right' \| ... | 'top' | 否 | 位置 |
| trigger | 'hover' \| 'click' | 'hover' | 否 | 触发方式 |
| disabled | boolean | false | 否 | 是否禁用 |

**Slots**：
| 插槽名 | 说明 |
|--------|------|
| default | 触发元素 |
| content | 自定义内容 |
| title | 自定义标题 |

**使用示例**：
```vue
<!-- 基础用法 -->
<DedsiPopover content="这是内容" title="标题">
  <DedsiButton>悬停显示</DedsiButton>
</DedsiPopover>

<!-- 自定义内容 -->
<DedsiPopover>
  <template #content>
    <div>自定义内容</div>
    <DedsiButton>操作</DedsiButton>
  </template>
  <DedsiButton>点击显示</DedsiButton>
</DedsiPopover>
```

---

### DedsiTooltip - 文字提示

**功能**：简单的文字提示气泡
**Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| content | string | 是 | - | 提示内容 |
| placement | 'top' \| 'bottom' \| 'left' \| 'right' \| ... | 'top' | 否 | 位置 |
| disabled | boolean | false | 否 | 是否禁用 |

**使用示例**：
```vue
<DedsiTooltip content="这是提示文字">
  <DedsiButton>悬停查看提示</DedsiButton>
</DedsiTooltip>
```

---

### DedsiResult - 结果

**功能**：反馈各类操作结果
**Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| status | 'success' \| 'error' \| 'info' \| 'warning' \| '404' \| '403' \| '500' | - | 否 | 结果状态 |
| title | string | - | 否 | 标题 |
| subTitle | string | - | 否 | 副标题 |
| icon | string | - | 否 | 自定义图标组件 |

**Slots**：
| 插槽名 | 说明 |
|--------|------|
| default | 额外内容 |
| icon | 自定义图标 |
| title | 自定义标题 |
| subTitle | 自定义副标题 |
| extra | 底部操作区 |

**使用示例**：
```vue
<!-- 成功结果 -->
<DedsiResult status="success" title="操作成功" subTitle="预计2小时内到达">
  <template #extra>
    <DedsiButton type="primary">返回首页</DedsiButton>
  </template>
</DedsiResult>

<!-- 404 页面 -->
<DedsiResult status="404" title="404" subTitle="抱歉，您访问的页面不存在">
  <template #extra>
    <DedsiButton type="primary">返回首页</DedsiButton>
  </template>
</DedsiResult>
```

---

### DedsiPopper - 基础气泡

**功能**：基础气泡组件，用于构建其他气泡类组件
**Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| placement | 'top' \| 'bottom' \| 'left' \| 'right' \| ... | 'top' | 否 | 位置 |
| trigger | 'hover' \| 'click' | 'hover' | 否 | 触发方式 |
| disabled | boolean | false | 否 | 是否禁用 |
| offset | number | 12 | 否 | 偏移量（px） |
| transitionName | string | 'dedsi-popper-fade' | 否 | 过渡动画名称 |
| popperClass | string | - | 否 | 自定义类名 |
| showArrow | boolean | true | 否 | 是否显示箭头 |
| background | string | '#fff' | 否 | 背景色 |
| color | string | - | 否 | 文字颜色 |
| borderRadius | string | '8px' | 否 | 圆角 |
| boxShadow | string | - | 否 | 阴影 |
| padding | string | '12px' | 否 | 内边距 |

**Events**：
| 事件名 | 参数 | 说明 |
|--------|------|------|
| update:visible | (visible: boolean) | 显示状态变化 |

**暴露方法**：
| 方法名 | 说明 |
|--------|------|
| close | 关闭气泡 |
| updatePosition | 更新位置 |

**Slots**：
| 插槽名 | 说明 |
|--------|------|
| default | 触发元素 |
| content | 气泡内容 |

---

## 其他组件

### DedsiSegmented - 分段器

**功能**：分段控制器，用于切换显示不同内容
**Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| modelValue | string \| number | 是 | - | 当前值 |
| options | SegmentedOption[] | 是 | - | 选项数组 |
| block | boolean | false | 否 | 是否撑满容器宽度 |
| size | 'large' \| 'default' \| 'small' | 'default' | 否 | 尺寸 |
| disabled | boolean | false | 否 | 是否禁用 |

**SegmentedOption 接口**：
```typescript
interface SegmentedOption {
  label: string           // 选项文本
  value: string | number  // 选项值
  icon?: any             // 图标
  disabled?: boolean     // 是否禁用
}
```

**Events**：
| 事件名 | 参数 | 说明 |
|--------|------|------|
| update:modelValue | (value: string \| number) | 值变化 |
| change | (value: string \| number) | 选项变化 |

**使用示例**：
```vue
<template>
  <DedsiSegmented
    v-model="value"
    :options="options"
    @change="handleChange"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'

const value = ref('day')

const options = [
  { label: '日', value: 'day' },
  { label: '周', value: 'week' },
  { label: '月', value: 'month' },
  { label: '年', value: 'year' }
]

const handleChange = (val: string | number) => {
  console.log('切换到', val)
}
</script>
```

---

### DedsiMarquee - 跑马灯

**功能**：文字/内容滚动展示
**Props**：
| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| speed | number | 50 | 否 | 滚动速度（px/s） |
| direction | 'ltr' \| 'rtl' | 'rtl' | 否 | 滚动方向：ltr 从左到右，rtl 从右到左 |
| pauseOnHover | boolean | true | 否 | 鼠标悬停时是否暂停 |

**使用示例**：
```vue
<DedsiMarquee :speed="100" direction="ltr">
  <span>这是一条滚动的公告信息</span>
</DedsiMarquee>
```

---

## 未实现组件

以下组件的目录存在但尚未实现（没有对应的 .vue 文件）：

### 表单组件
- **DedsiButton** - 按钮
- **DedsiForm** / **DedsiFormItem** - 表单
- **DedsiInput** / **DedsiInputNumber** / **DedsiInputPassword** / **DedsiTextarea** - 输入框系列
- **DedsiCheckbox** / **DedsiCheckboxGroup** - 复选框
- **DedsiRadio** / **DedsiRadioGroup** - 单选框
- **DedsiSelect** - 选择器
- **DedsiSwitch** - 开关
- **DedsiSlider** - 滑动输入条
- **DedsiRate** - 评分

### 数据选择组件
- **DedsiAutoComplete** - 自动完成
- **DedsiCascader** - 级联选择
- **DedsiDatePicker** / **DedsiMonthPicker** / **DedsiRangePicker** - 日期选择器系列
- **DedsiTimePicker** / **DedsiTimeRangePicker** - 时间选择器系列
- **DedsiTreeSelect** - 树选择
- **DedsiTransfer** - 穿梭框
- **DedsiMentions** - 提及

### 其他
- **DedsiUpload** - 上传

---

## 最佳实践

### 1. 组件导入

推荐使用按需导入以减小打包体积：
```typescript
import { DedsiAlert, DedsiButton, DedsiTable } from 'dedsi-vue-ui'

app.use(DedsiAlert)
app.use(DedsiButton)
app.use(DedsiTable)
```

**避免全量导入**（除非确实需要全部组件）：
```typescript
// ❌ 不推荐：会导入所有组件
import DedsiVueUI from 'dedsi-vue-ui'
app.use(DedsiVueUI)
```

### 2. 事件处理

所有组件的事件都使用 Vue 3 标准事件命名：
```vue
<!-- ✅ 推荐：使用 kebab-case 事件名 -->
<DedsiDialog @update:visible="handleVisibleChange" />
<DedsiTable @page-change="handlePageChange" />
<DedsiTabs @update:activeKey="handleTabChange" />

<!-- ❌ 避免：使用 camelCase -->
<DedsiDialog @visibleChange="..." />
<DedsiDialog @onVisibleChange="..." />
```

**事件回调类型定义**：
```typescript
const handleVisibleChange = (visible: boolean) => {
  console.log('对话框显示状态:', visible)
}

const handlePageChange = (page: number) => {
  console.log('当前页码:', page)
}
```

### 3. 双向绑定

使用 `v-model` 进行双向绑定，遵循 Vue 3 规范：
```vue
<!-- 带参数的 v-model（推荐） -->
<DedsiTabs v-model:activeKey="activeKey" />
<DedsiMenu v-model:selectedKeys="selectedKeys" />
<DedsiMenu v-model:openKeys="openKeys" />

<!-- 不带参数的 v-model（默认 modelValue） -->
<DedsiSegmented v-model="value" />
<DedsiInput v-model="inputValue" />

<!-- 完整等价形式 -->
<DedsiTabs
  :activeKey="activeKey"
  @update:activeKey="val => activeKey = val"
/>
```

### 4. 类型安全

**推荐使用 TypeScript** 以获得完整的类型提示和检查：
```typescript
// 导入类型定义
import type {
  MenuItem,
  Column,
  DropdownMenuItem,
  SegmentedOption
} from 'dedsi-vue-ui'

// 使用类型定义
const menuItems: MenuItem[] = [
  { key: 'home', label: '首页', icon: HomeIcon }
]

const columns: Column[] = [
  { key: 'name', title: '姓名', width: '200px' }
]
```

### 5. 插槽使用

**具名插槽**：
```vue
<DedsiCard>
  <template #title>
    <span>自定义标题</span>
  </template>
  <template #extra>
    <DedsiButton>更多</DedsiButton>
  </template>
  <p>卡片内容</p>
</DedsiCard>
```

**作用域插槽**：
```vue
<DedsiTable :data="data" :columns="columns">
  <template #name="{ row, value }">
    <a @click="handleClick(row)">{{ value }}</a>
  </template>
</DedsiTable>
```

### 6. 样式定制

**通过 props 修改样式**：
```vue
<!-- 使用组件提供的样式 props -->
<DedsiCard :bodyStyle="{ padding: '20px' }" />
<DedsiStatistic :contentStyle="{ color: '#3f8600' }" />
```

**通过 CSS 覆盖**（谨慎使用）：
```vue
<style scoped>
/* 使用深度选择器覆盖组件内部样式 */
.custom-card :deep(.dedsi-card-body) {
  padding: 30px;
}
</style>
```

### 7. 性能优化

**合理使用 v-once**：
```vue
<!-- 静态内容使用 v-once 避免不必要的更新 -->
<DedsiCard v-once>
  <h1>静态标题</h1>
</DedsiCard>
```

**避免不必要的响应式**：
```typescript
// ✅ 使用 shallowRef 对于大型对象
const largeData = shallowRef<DataType[]>(...)

// ✅ 使用 markRaw 跳过组件的响应式转换
import { markRaw } from 'vue'
const iconComponent = markRaw(CustomIcon)
```

### 8. 常见问题

**Q: 组件样式不生效？**
A: 检查是否正确导入了组件样式文件，确保 CSS 已被加载。

**Q: TypeScript 报错找不到模块？**
A: 确保安装了类型定义，并在 `tsconfig.json` 中正确配置：
```json
{
  "compilerOptions": {
    "types": ["dedsi-vue-ui"]
  }
}
```

**Q: 组件无法按需导入？**
A: 检查是否配置了正确的构建工具（如 Vite、Webpack）以支持按需导入。

**Q: 如何自定义主题？**
A: 参考 CSS 变量文档，通过覆盖 CSS 变量来定制主题：
```css
:root {
  --dedsi-primary-color: #1890ff;
  --dedsi-border-radius: 4px;
}
```

---

## 组件分类索引

### 基础组件 (10)
- DedsiAlert - 警告提示
- DedsiAvatar - 头像
- DedsiBadge - 徽标数
- DedsiBreadcrumb - 面包屑
- DedsiCard - 卡片
- DedsiDivider - 分割线
- DedsiEmpty - 空状态
- DedsiTag - 标签
- DedsiSpace - 间距
- DedsiSplit - 分割布局

### 布局组件 (3)
- DedsiRow/DedsiCol - 栅格布局
- DedsiScrollbar - 滚动条
- DedsiSkeleton - 骨架屏

### 导航组件 (3)
- DedsiMenu - 导航菜单
- DedsiTabs - 标签页
- DedsiDropdown - 下拉菜单

### 数据展示组件 (7)
- DedsiStatistic - 统计数值
- DedsiNumberConverter - 数字转换
- DedsiCountdown - 倒计时
- DedsiTable - 表格
- DedsiTypography - 排版
- DedsiImage - 图片
- DedsiQRCode - 二维码

### 反馈组件 (9)
- DedsiDialog - 对话框
- DedsiModal - 模态框
- DedsiDrawer - 抽屉
- DedsiMessage - 全局提示
- DedsiPopconfirm - 气泡确认框
- DedsiPopover - 气泡卡片
- DedsiTooltip - 文字提示
- DedsiResult - 结果
- DedsiPopper - 基础气泡

### 其他组件 (2)
- DedsiSegmented - 分段器
- DedsiMarquee - 跑马灯

---

## 统计信息

- **已实现组件**：37 个
- **未实现组件**：23 个
- **总计**：60 个

---

## 附录

### TypeScript 类型定义速查

#### 常用接口类型

```typescript
// 菜单项类型（DedsiMenu, DedsiDropdown）
interface MenuItem {
  key: string
  label: string
  icon?: any
  disabled?: boolean
  children?: MenuItem[]
}

// 表格列类型（DedsiTable）
interface Column {
  key: string
  title: string
  width?: string
  align?: 'left' | 'center' | 'right'
}

// 下拉菜单项类型（DedsiDropdown）
interface DropdownMenuItem {
  key: string | number
  label?: string
  icon?: any
  disabled?: boolean
  danger?: boolean
  type?: 'item' | 'divider'
}

// 分段器选项类型（DedsiSegmented）
interface SegmentedOption {
  label: string
  value: string | number
  icon?: any
  disabled?: boolean
}

// 面包屑路由类型（DedsiBreadcrumbItem）
type RouteLocationRaw = string | {
  path?: string
  name?: string
  params?: Record<string, any>
  query?: Record<string, any>
}
```

### Props 类型联合值速查

```typescript
// Alert 类型
type AlertType = 'success' | 'info' | 'warning' | 'error'

// Avatar 尺寸
type AvatarSize = 'large' | 'default' | 'small' | number

// Avatar 形状
type AvatarShape = 'circle' | 'square'

// Badge 类型
type BadgeType = 'primary' | 'success' | 'warning' | 'danger'

// Button 尺寸
type ButtonSize = 'large' | 'default' | 'small'

// Card 阴影
type CardShadow = 'always' | 'hover' | 'never'

// Divider 方向
type DividerDirection = 'horizontal' | 'vertical'

// Menu 模式
type MenuMode = 'vertical' | 'horizontal' | 'inline'

// Menu 主题
type MenuTheme = 'light' | 'dark'

// Space 方向
type SpaceDirection = 'horizontal' | 'vertical'

// Space 尺寸
type SpaceSize = 'small' | 'middle' | 'large' | number | [number, number]

// Tabs 类型
type TabsType = 'line' | 'card' | 'editable-card'

// Tag 类型
type TagType = 'default' | 'primary' | 'success' | 'warning' | 'danger'

// Tooltip/Popover 放置位置
type Placement =
  | 'top' | 'topLeft' | 'topRight' | 'topCenter'
  | 'bottom' | 'bottomLeft' | 'bottomRight' | 'bottomCenter'
  | 'left' | 'leftTop' | 'leftBottom'
  | 'right' | 'rightTop' | 'rightBottom'

// Result 状态
type ResultStatus = 'success' | 'error' | 'info' | 'warning' | '404' | '403' | '500'

// NumberConverter 单位
type NumberConverterUnit = 'none' | 'wan' | 'qianwan' | 'yi' | 'auto'

// Drawer 位置
type DrawerPlacement = 'left' | 'right' | 'top' | 'bottom'

// QRCode 容错级别
type QRCodeErrorLevel = 'L' | 'M' | 'Q' | 'H'
```

---

**文档元数据**：

| 项目 | 值 |
|------|------|
| 文档名称 | Dedsi-Vue-UI 组件库 SKILL 文档 |
| 文档版本 | 1.0.0 |
| 组件库版本 | 0.0.9 |
| 创建时间 | 2025-01-20 |
| 最后更新 | 2025-01-20 |
| 维护者 | Dedsi Team |
| 许可证 | MIT |
| Vue 版本 | 3.5.26 |
| TypeScript 版本 | 5.9.3 |
| 文档格式 | Markdown + YAML Front Matter |
| 文档规范 | SKILL v1.0 |
