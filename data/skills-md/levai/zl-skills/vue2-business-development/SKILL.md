---
name: vue2-business-development
description: Vue 2 项目从规范到业务开发的完整工作流程，包括创建新业务模块、开发CRUD页面、实现业务功能、遵循项目规范等。适用于开发新功能、创建新模块、实现业务需求等场景。
metadata:
  author: datagradient-ui
  version: "1.0"
---

# 业务开发完整指南

## 何时使用

当需要开发新业务功能或创建新业务模块时使用此技能，包括：

- 创建新的业务模块（如数据资产管理、数据质量等）
- 开发新的 CRUD 页面
- 实现业务功能需求
- 添加新的路由和菜单
- 创建 Vuex store 和组件

## 开发流程概览

```
1. 理解需求 → 2. 设计数据结构 → 3. 创建路由 → 4. 创建 Store → 5. 创建视图组件 → 6. 实现业务逻辑 → 7. 测试与提交
```

## 快速开始

### 1. 创建新业务模块

#### 步骤 1: 添加路由配置

在 `src/router/routes/` 目录下创建模块路由文件：

```typescript
// src/router/routes/myModule/index.ts
import { RouteConfig } from '@/router/types'
import { Layout } from '@/layout'
import { PidValue } from '@/router/constant'

// 模块首页
export const MyModuleOverview: RouteConfig = {
  path: 'myModule',
  component: Layout,
  meta: {
    name: 'My Module',
    icon: 'top-nav-icon',
    globalKey: 'myModule',
    globalModel: 'myModule',
    pid: PidValue.UNKNOWN
  },
  children: [
    {
      path: 'overview',
      component: () => import('@/views/myModule/overview/index.vue'),
      meta: { name: '概览', affix: true }
    },
    {
      path: 'list',
      component: () => import('@/views/myModule/list/index.vue'),
      meta: { name: '列表管理' }
    }
  ]
}
```

#### 步骤 2: 注册路由

在 `src/router/routes/index.ts` 中导入并注册：

```typescript
import { MyModuleOverview } from './myModule'

const myModuleMenu = {
  path: 'myModule',
  component: Layout,
  meta: {
    name: 'My Module',
    icon: 'top-nav-icon',
    globalKey: 'myModule',
    globalModel: 'myModule'
  },
  children: [
    MyModuleOverview
  ]
}

export const asyncRoutes = [
  // ...
  myModuleMenu
]
```

#### 步骤 3: 添加模块常量

在 `src/router/constant.ts` 中添加模块标识：

```typescript
export enum PidValue {
  // ...
  MY_MODULE = 100 // 新模块ID
}

export enum ModuleHomePath {
  // ...
  MY_MODULE = '/myModule' // 模块首页路径
}
```

### 2. 创建 Vuex Store

#### Store 结构

```typescript
// src/components/MyModule/store/index.ts
import { VuexModule } from '@/store'
import { IListParams, IListResult } from '@/types'

interface State {
  list: any[]
  detail: any
  loading: boolean
}

const state: State = {
  list: [],
  detail: {},
  loading: false
}

const actions = {
  async fetchList ({ commit }, params: IListParams) {
    commit('SET_LOADING', true)
    try {
      const res = await http.get('/api/my-module/list', { params })
      commit('SET_LIST', res.data)
      return res
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  async fetchDetail ({ commit }, id: number) {
    const res = await http.get(`/api/my-module/${id}`)
    commit('SET_DETAIL', res.data)
    return res
  },
  
  async addItem ({ commit }, data: any) {
    return await http.post('/api/my-module', data)
  },
  
  async updateItem ({ commit }, { id, ...data }: any) {
    return await http.put(`/api/my-module/${id}`, data)
  },
  
  async deleteItem ({ commit }, id: number) {
    return await http.delete(`/api/my-module/${id}`)
  }
}

const mutations = {
  SET_LIST (state: State, list: any[]) {
    state.list = list
  },
  SET_DETAIL (state: State, detail: any) {
    state.detail = detail
  },
  SET_LOADING (state: State, loading: boolean) {
    state.loading = loading
  }
}

const store: VuexModule<State> = {
  name: 'myModule',
  namespaced: true,
  state,
  actions,
  mutations
}

export default store
```

#### 创建 AbsView 基类

```typescript
// src/components/MyModule/AbsView/AbsMyModuleView.ts
import { Component, Vue } from 'vue-property-decorator'
import { namespace } from 'vuex-class'
import { StoreProvide } from '@/utils/decorators'
import store from '../store'

const $store = namespace('myModule')

@Component
@StoreProvide([store])
export default class AbsMyModuleView extends Vue {
  @$store.Action('fetchList')
  fetchList!: IGenericAction<IListParams, IListResult<any[]>>

  @$store.Action('fetchDetail')
  fetchDetail!: IGenericAction<{ id: number }, any>

  @$store.Action('addItem')
  addItem!: IGenericAction<any, boolean>

  @$store.Action('updateItem')
  updateItem!: IGenericAction<any, boolean>

  @$store.Action('deleteItem')
  deleteItem!: IGenericAction<{ id: number }, boolean>
}
```

### 3. 创建 CRUD 页面

参考 `crud-pages` 技能创建标准 CRUD 页面：

```vue
<template>
  <div class="main-wrapper">
    <GridList
      ref="list"
      :show-pagination="true"
      :store-load-list="fetchList"
      :chain-query="chainQuery"
    >
      <!-- 搜索表单 -->
      <template slot="form" slot-scope="{ $ctx, query }">
        <el-form :inline="true" @submit.native.prevent>
          <el-form-item class="master-btns">
            <el-button 
              v-acl="`/myModule|${PERMISSION_FLAG.ADD}`" 
              type="primary" 
              @click="handleAdd"
            >
              新增
            </el-button>
          </el-form-item>
          <el-form-item>
            <Search 
              v-model.trim="query.searchValue" 
              :search-key="['名称']" 
              :on-search="() => $ctx.load({ pager: { page: 1 } })" 
            />
          </el-form-item>
        </el-form>
      </template>

      <!-- 表格 -->
      <template slot="table" slot-scope="{ grid }">
        <el-table :data="grid.list" stripe>
          <el-table-column prop="name" label="名称" />
          <el-table-column label="操作" fixed="right" width="200" class-name="col-actions">
            <template slot-scope="{ row }">
              <el-button type="text" size="small" @click="handleEdit(row)">编辑</el-button>
              <el-button type="text" size="small" @click="handleDelete(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </template>
    </GridList>

    <!-- 对话框 -->
    <AbsFormDialog :entity.sync="formDlg" size="normal">
      <template v-slot="{ model, rules }">
        <el-form class="v-form" :model="model" :rules="rules">
          <el-form-item prop="name" label="名称">
            <el-input v-model.trim="model.name" class="v-form--ctl" />
          </el-form-item>
        </el-form>
      </template>
    </AbsFormDialog>
  </div>
</template>

<script lang="ts">
import { Component } from 'vue-property-decorator'
import { GridList, AbsFormDialog, DialogModelService } from '@tdio/tdui'
import AbsMyModuleView from '@/components/MyModule/AbsView/AbsMyModuleView'
import { genRequired } from '@/utils/validator'
import { PERMISSION_FLAG } from '@/components/ACLs/model'

@Component({
  components: {
    GridList,
    AbsFormDialog
  },
  data () {
    return {
      PERMISSION_FLAG
    }
  }
})
export default class MyModuleList extends AbsMyModuleView {
  loadData (params?: Partial<IListParams>) {
    (this.$refs.list as any).load(params)
  }

  chainQuery (query: IQuery) {
    return query
  }

  handleAdd () {
    this.formDlg.show({}, '新增')
  }

  handleEdit (row: Kv) {
    const { id } = row
    this.fetchDetail({ id }).then(data => {
      if (data) {
        this.formDlg.show(data, '编辑')
      }
    })
  }

  handleDelete (row: Kv) {
    const { id } = row
    this.$confirm('确认删除？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(async () => {
      await this.deleteItem({ id })
      this.$message.success($t('Action Success'))
      this.loadData()
    }).catch(() => {})
  }

  formDlg = new DialogModelService<MyModuleList, any>(
    $this => ({
      rules: {
        name: [genRequired('请输入名称')]
      },
      onSubmit () {
        const { data } = this
        if (data.id) {
          return $this.updateItem(data).then(res => {
            if (res) {
              $this.$message.success($t('Action Success'))
              $this.loadData()
              this.hide()
            }
          })
        } else {
          return $this.addItem(data).then(res => {
            if (res) {
              $this.$message.success($t('Action Success'))
              $this.loadData()
              this.hide()
            }
          })
        }
      }
    })
  )
}
</script>
```

## 项目规范检查清单

在开发过程中，确保遵循以下规范：

### 代码规范

- [ ] 遵循 TypeScript 类型定义规范
- [ ] 使用 Vue 组件开发规范
- [ ] 遵循代码风格规范
- [ ] 使用统一的命名规范

### Git 提交

- [ ] 提交信息遵循 Git 提交规范
- [ ] 提交类型正确（feat/fix/refactor等）
- [ ] 提交信息使用中文

### 业务开发

- [ ] CRUD 页面遵循标准模式
- [ ] 权限控制正确实现
- [ ] 表单验证规则完整
- [ ] 错误处理完善
- [ ] 国际化文本使用 `$t()`

## 常见业务场景

### 场景 1: 数据管理模块

1. 创建路由配置
2. 创建 Vuex store（包含列表、详情、增删改查）
3. 创建 AbsView 基类
4. 创建列表页面（使用 GridList）
5. 创建表单对话框（使用 DialogModelService）
6. 添加权限控制

### 场景 2: 工作流配置

1. 创建路由和菜单
2. 创建配置页面
3. 实现配置保存逻辑
4. 添加配置验证

### 场景 3: 数据展示页面

1. 创建概览页面
2. 使用图表组件展示数据
3. 实现数据刷新逻辑

## 参考资源

- Vue 组件开发：参考 `vue-development` 技能
- TypeScript 规范：参考 `typescript-standards` 技能
- CRUD 页面：参考 `crud-pages` 技能
- Git 提交：参考 `git-commit` 技能
- 代码风格：参考 `code-style` 技能

详细开发指南请参考 [references/DEVELOPMENT_GUIDE.md](references/DEVELOPMENT_GUIDE.md)
