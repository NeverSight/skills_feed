---
name: vben-admin
description: Vben Admin 5.x 前端开发规范。当创建页面、组件、API 接口或前端功能时自动使用。
---

# Vben Admin 开发规范

本项目使用 Vben Admin 5.x (Ant Design Vue) + TypeScript + Vite 技术栈。

## 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Vue | 3.5.x | UI 框架 |
| TypeScript | 5.x | 类型系统 |
| Ant Design Vue | 4.x | 组件库 |
| Vite | 7.x | 构建工具 |
| Pinia | 3.x | 状态管理 |
| Vue Router | 4.x | 路由 |
| Axios | - | HTTP 客户端 |

## 目录结构

```
frontend/apps/web-antd/src/
├── api/                      # API 接口
│   └── {module}/
│       └── index.ts
├── views/                    # 页面视图
│   └── {module}/
│       ├── index.vue         # 列表页
│       ├── detail.vue        # 详情页
│       └── form.vue          # 表单页
├── components/               # 公共组件
├── stores/                   # 状态管理
│   └── {module}.ts
├── router/                   # 路由配置
│   └── routes/
│       └── {module}.ts
├── hooks/                    # 自定义 Hooks
├── utils/                    # 工具函数
└── types/                    # 类型定义
    └── {module}.ts
```

## 代码模板

### API 接口

```typescript
// api/{module}/index.ts
import { defHttp } from '@vben/request';
import type { {EntityName}, {EntityName}ListParams, {EntityName}FormData } from '@/types/{module}';

/**
 * {模块}API
 */
enum Api {
  List = '/api/{module}',
  Detail = '/api/{module}/',
  Create = '/api/{module}',
  Update = '/api/{module}/',
  Delete = '/api/{module}/',
}

/**
 * 获取{实体}列表
 */
export function get{EntityName}List(params: {EntityName}ListParams) {
  return defHttp.get<{EntityName}[]>({
    url: Api.List,
    params,
  });
}

/**
 * 获取{实体}详情
 */
export function get{EntityName}Detail(id: number) {
  return defHttp.get<{EntityName}>({
    url: `${Api.Detail}${id}`,
  });
}

/**
 * 创建{实体}
 */
export function create{EntityName}(data: {EntityName}FormData) {
  return defHttp.post<{EntityName}>({
    url: Api.Create,
    data,
  });
}

/**
 * 更新{实体}
 */
export function update{EntityName}(id: number, data: {EntityName}FormData) {
  return defHttp.put<{EntityName}>({
    url: `${Api.Update}${id}`,
    data,
  });
}

/**
 * 删除{实体}
 */
export function delete{EntityName}(id: number) {
  return defHttp.delete({
    url: `${Api.Delete}${id}`,
  });
}
```

### 类型定义

```typescript
// types/{module}.ts

/**
 * {实体}类型
 */
export interface {EntityName} {
  /** ID */
  id: number;
  /** 名称 */
  name: string;
  /** 创建时间 */
  createdAt: string;
  /** 更新时间 */
  updatedAt: string;
}

/**
 * {实体}列表查询参数
 */
export interface {EntityName}ListParams {
  /** 页码 */
  page?: number;
  /** 每页数量 */
  size?: number;
  /** 关键词 */
  keyword?: string;
}

/**
 * {实体}表单数据
 */
export interface {EntityName}FormData {
  /** 名称 */
  name: string;
}
```

### 列表页

```vue
<!-- views/{module}/index.vue -->
<template>
  <Page>
    <template #header>
      <PageHeader title="{模块名称}" />
    </template>

    <!-- 搜索区域 -->
    <Card class="mb-4">
      <Form :model="searchForm" layout="inline">
        <FormItem label="关键词">
          <Input v-model:value="searchForm.keyword" placeholder="请输入关键词" />
        </FormItem>
        <FormItem>
          <Space>
            <Button type="primary" @click="handleSearch">查询</Button>
            <Button @click="handleReset">重置</Button>
          </Space>
        </FormItem>
      </Form>
    </Card>

    <!-- 操作区域 -->
    <Card>
      <template #title>
        <Button type="primary" @click="handleCreate">
          <PlusOutlined /> 新增
        </Button>
      </template>

      <!-- 表格 -->
      <Table
        :columns="columns"
        :data-source="dataSource"
        :loading="loading"
        :pagination="pagination"
        @change="handleTableChange"
      >
        <template #action="{ record }">
          <Space>
            <Button type="link" @click="handleEdit(record)">编辑</Button>
            <Popconfirm title="确定删除吗？" @confirm="handleDelete(record.id)">
              <Button type="link" danger>删除</Button>
            </Popconfirm>
          </Space>
        </template>
      </Table>
    </Card>
  </Page>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { message } from 'ant-design-vue';
import { PlusOutlined } from '@ant-design/icons-vue';
import { Page, PageHeader } from '@vben/components';
import { get{EntityName}List, delete{EntityName} } from '@/api/{module}';
import type { {EntityName} } from '@/types/{module}';

/**
 * {模块}列表页
 */
defineOptions({ name: '{EntityName}List' });

const router = useRouter();

// 搜索表单
const searchForm = reactive({
  keyword: '',
});

// 表格数据
const loading = ref(false);
const dataSource = ref<{EntityName}[]>([]);
const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
});

// 表格列配置
const columns = [
  { title: 'ID', dataIndex: 'id', width: 80 },
  { title: '名称', dataIndex: 'name' },
  { title: '创建时间', dataIndex: 'createdAt', width: 180 },
  { title: '操作', key: 'action', width: 150, slots: { customRender: 'action' } },
];

/**
 * 加载数据
 */
async function loadData() {
  loading.value = true;
  try {
    const res = await get{EntityName}List({
      page: pagination.current,
      size: pagination.pageSize,
      ...searchForm,
    });
    dataSource.value = res.content;
    pagination.total = res.totalElements;
  } finally {
    loading.value = false;
  }
}

/**
 * 搜索
 */
function handleSearch() {
  pagination.current = 1;
  loadData();
}

/**
 * 重置
 */
function handleReset() {
  searchForm.keyword = '';
  handleSearch();
}

/**
 * 表格变化
 */
function handleTableChange(pag: any) {
  pagination.current = pag.current;
  pagination.pageSize = pag.pageSize;
  loadData();
}

/**
 * 新增
 */
function handleCreate() {
  router.push('/{module}/form');
}

/**
 * 编辑
 */
function handleEdit(record: {EntityName}) {
  router.push(`/{module}/form/${record.id}`);
}

/**
 * 删除
 */
async function handleDelete(id: number) {
  await delete{EntityName}(id);
  message.success('删除成功');
  loadData();
}

onMounted(() => {
  loadData();
});
</script>
```

### 表单页

```vue
<!-- views/{module}/form.vue -->
<template>
  <Page>
    <template #header>
      <PageHeader :title="isEdit ? '编辑{模块}' : '新增{模块}'" @back="handleBack" />
    </template>

    <Card>
      <Form
        ref="formRef"
        :model="formData"
        :rules="rules"
        :label-col="{ span: 4 }"
        :wrapper-col="{ span: 12 }"
      >
        <FormItem label="名称" name="name">
          <Input v-model:value="formData.name" placeholder="请输入名称" />
        </FormItem>

        <FormItem :wrapper-col="{ offset: 4, span: 12 }">
          <Space>
            <Button type="primary" :loading="submitting" @click="handleSubmit">
              保存
            </Button>
            <Button @click="handleBack">取消</Button>
          </Space>
        </FormItem>
      </Form>
    </Card>
  </Page>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { message } from 'ant-design-vue';
import { Page, PageHeader } from '@vben/components';
import { get{EntityName}Detail, create{EntityName}, update{EntityName} } from '@/api/{module}';
import type { {EntityName}FormData } from '@/types/{module}';

/**
 * {模块}表单页
 */
defineOptions({ name: '{EntityName}Form' });

const route = useRoute();
const router = useRouter();
const formRef = ref();

// 是否编辑模式
const isEdit = computed(() => !!route.params.id);
const editId = computed(() => Number(route.params.id));

// 表单数据
const formData = reactive<{EntityName}FormData>({
  name: '',
});

// 表单验证规则
const rules = {
  name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
};

// 提交状态
const submitting = ref(false);

/**
 * 加载详情
 */
async function loadDetail() {
  if (!isEdit.value) return;
  const res = await get{EntityName}Detail(editId.value);
  Object.assign(formData, res);
}

/**
 * 提交表单
 */
async function handleSubmit() {
  await formRef.value?.validate();
  submitting.value = true;
  try {
    if (isEdit.value) {
      await update{EntityName}(editId.value, formData);
      message.success('更新成功');
    } else {
      await create{EntityName}(formData);
      message.success('创建成功');
    }
    handleBack();
  } finally {
    submitting.value = false;
  }
}

/**
 * 返回列表
 */
function handleBack() {
  router.push('/{module}');
}

onMounted(() => {
  loadDetail();
});
</script>
```

### 路由配置

```typescript
// router/routes/{module}.ts
import type { RouteRecordRaw } from 'vue-router';

/**
 * {模块}路由
 */
const routes: RouteRecordRaw[] = [
  {
    path: '/{module}',
    name: '{EntityName}',
    meta: {
      title: '{模块名称}',
      icon: 'ant-design:appstore-outlined',
    },
    children: [
      {
        path: '',
        name: '{EntityName}List',
        component: () => import('@/views/{module}/index.vue'),
        meta: {
          title: '{模块}列表',
        },
      },
      {
        path: 'form/:id?',
        name: '{EntityName}Form',
        component: () => import('@/views/{module}/form.vue'),
        meta: {
          title: '{模块}表单',
          hideMenu: true,
        },
      },
    ],
  },
];

export default routes;
```

## 命名规范

| 位置 | 规范 | 示例 |
|------|------|------|
| 文件夹 | kebab-case | `user-management/` |
| 组件文件 | PascalCase.vue | `UserList.vue` |
| 工具文件 | camelCase.ts | `formatDate.ts` |
| 类型文件 | camelCase.ts | `user.ts` |
| 组件名 | PascalCase | `UserList` |
| 变量名 | camelCase | `userName` |
| 常量名 | UPPER_SNAKE | `MAX_PAGE_SIZE` |
| 事件名 | handle + 动作 | `handleSubmit` |

## 最佳实践

1. **TypeScript**: 所有文件使用 TypeScript，定义完整类型
2. **组合式 API**: 使用 `<script setup lang="ts">`
3. **中文注释**: 所有函数、变量添加中文注释
4. **API 封装**: 统一使用 `defHttp` 封装请求
5. **类型定义**: 接口数据类型放在 `types/` 目录
6. **组件命名**: 使用 `defineOptions({ name: 'XxxComponent' })`

---
> 项目: 应急管理系统 (yingjiguanli)
> 技术栈: Vben Admin 5.x + Vue 3 + TypeScript
