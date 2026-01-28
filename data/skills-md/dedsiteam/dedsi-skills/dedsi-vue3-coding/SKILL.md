---
name: dedsi-vue3-coding
description: Vue 3 coding guidelines and best practices with Dedsi UI components
---

# Dedsi Vue3 Coding Skills

## 1. 技术栈 (Technology Stack)
- **Framework**: Vue 3 (Composition API)
- **Language**: TypeScript
- **UI Library**: Dedsi UI
  - Prefix: `dedsi-` (e.g., `dedsi-button`, `dedsi-table`)
- **Icons**: `@ant-design/icons-vue`
- **Date Handling**: `dayjs`
- **HTTP Client**: Custom `AxiosRequest` wrapper

## 2. 项目结构 (Project Structure)
- `src/apiServices/`: API 服务层，包含接口定义和 DTO 类型。
  - `identitys/`: 身份认证相关服务 (User, Role, Permission 等)。
  - `index.ts`: 导出所有服务。
  - `types.ts`: 定义请求/响应接口 (DTO)。
- `src/views/`: 页面视图层。
  - `user/index.vue`: 标准的 CURD 页面示例。

## 3. 开发规范 (Development Guidelines)

### 3.1 API Service Layer
- **位置**: `src/apiServices/{module}/`
- **类定义**: 使用 class 定义 Service，内部实例化 `AxiosRequest`。
- **单例导出**: 导出 Service 的实例 (e.g., `export const userApiService = new UserApiService()`).
- **类型定义**: DTO (Data Transfer Objects) 必须定义在同级或公共的 `types.ts` 中。
- **标准方法**:
  - `pagedQuery(data: InputDto)`: 分页查询
  - `get(id: string)`: 获取详情
  - `create(data: CreateResult)`: 创建
  - `update(id: string, data: UpdateRequest)`: 更新
  - `delete(id: string)`: 删除

**Example:**
```typescript
export class UserApiService {
    private request = new AxiosRequest(IdentityApiServiceUrl)

    public pagedQuery(data: UserPagedInputDto) {
        return this.request.post<UserPagedResultDto, UserPagedInputDto>('/api/Identity/User/PagedQuery', data)
    }
}
```

### 3.2 View Components
页面开发需遵循 Composition API (`<script setup lang="ts">`) 风格。

#### 页面布局结构
1. **Search Card**: 顶部搜索栏，使用 `dedsi-card` 包裹 `dedsi-form` (layout="inline")。
2. **Table Card**: 数据表格，使用 `dedsi-card` 包裹 `dedsi-table`。
3. **Modal**: 新增/编辑弹窗，使用 `dedsi-modal` 包裹 `dedsi-form` (layout="vertical")。

#### 核心状态定义
```typescript
// 表格数据
const tableLoading = ref(false)
const tableData = ref<Dto[]>()

// 分页配置
const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0
})

// 查询参数
const queryParam = reactive<Partial<InputDto>>({ ... })

// 弹窗表单
const modalVisible = ref(false)
const formState = reactive<any>({ ... })
```

#### 常用组件对照表
| Standard Component | Dedsi Component | Key Props/Events |
|-------------------|-----------------|------------------|
| Card              | `dedsi-card`    | `:bordered="false"` |
| Button            | `dedsi-button`  | `type="primary"`, `@click` |
| Table             | `dedsi-table`   | `:columns`, `:data`, `:total`, `:pageSize`, ':loading', `@page-change`, `@page-size-change` |
| Form              | `dedsi-form`    | `:model`, `layout`, `@finish` |
| Input             | `dedsi-input`   | `v-model` |
| Modal             | `dedsi-modal`   | `v-model:visible`, `@cancel` |
| Message           | `DedsiMessage`  | `DedsiMessage.success()`, `DedsiMessage.error()` |
| Space             | `dedsi-space`   | 用于按钮组间距 |

## 4. 最佳实践 (Best Practices)

1. **Table Columns 定义**:
   - 时间字段使用 `customRender` + `dayjs` 格式化。
   - 操作列使用 `template #action` 插槽。

2. **数据加载 (Fetch Data)**:
   - 统一封装 `fetchData` 方法。
   - `try-catch` 包裹 API 请求。
   - `finally` 中重置 `tableLoading.value = false`。

3. **表单处理**:
   - 编辑时使用 `Object.assign(formState, detail)` 回填数据。
   - 新增时需重置 `formState`。
   - 提交时根据是否有 `id` 判断是 Create 还是 Update。

4. **删除操作**:
   - 使用 `dedsi-popconfirm` 包裹删除按钮，防止误操作。

## 5. 代码模板 (Code Snippets)

### Service Template
```typescript
import { AxiosRequest } from '../../utils/axiosRequest'
// import types...

export class MyApiService {
    private request = new AxiosRequest(ServiceUrl)

    public pagedQuery(data: PagedInputDto) {
        return this.request.post<PagedResultDto, PagedInputDto>('/api/Path/PagedQuery', data)
    }
}
export const myApiService = new MyApiService()
```

### View Script Template
```typescript
<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { myApiService } from '@/apiServices'
import { DedsiMessage } from 'dedsi-vue-ui'

// State & Methods...
const fetchData = async () => {
    tableLoading.value = true
    try {
        const res = await myApiService.pagedQuery({ ...queryParam, pageIndex: pagination.current, pageSize: pagination.pageSize })
        tableData.value = res.items
        pagination.total = res.totalCount
    } finally {
        tableLoading.value = false
    }
}
</script>
```
