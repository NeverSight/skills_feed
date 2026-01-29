---
name: public-components-skill
description: 专为前端开发设计的AI技能，专门用于理解和使用@arim-aisdc/public-components组件库
---

# Public Components Library Skill

这是一个专为前端开发设计的 AI 技能，专门用于理解和使用 `@arim-aisdc/public-components` 组件库。该技能涵盖了组件库的所有核心功能、使用模式、主题配置和最佳实践。

## When to use

**自动触发条件：** 当用户提到以下任何关键词时，AI 应自动加载此技能：

### 核心组件关键词
- `@arim-aisdc/public-components` - 组件库包名
- `TableMax` - 高级表格组件
- `ConfigProvider` - 全局配置提供者
- `PermissionProvider`、`Restricted`、`PermissionContext` - 权限控制
- `ThemeProvider` - 主题提供者
- `CustomForm` - 自定义表单
- `QueryFilter` - 查询筛选器
- `SchemaForm` - Schema驱动表单
- `BaseInfo` - 基础信息展示
- `CenterModal` - 居中弹窗
- `DrawerCom` - 抽屉组件
- `SplitPane`、`SplitterPane` - 分割面板
- `CacheTabs` - 缓存标签页
- `DraggableBox` - 可拖拽盒子
- `Empty` - 空状态组件
- `Icon` - 图标组件
- `ColorSelector` - 颜色选择器
- `MessageTip`、`ModalTip` - 全局提示
- `MicroComponent` - 微组件

### Filter 组件系列
- `FilterSelect` - 选择器筛选
- `FilterInputNumber` - 数值筛选
- `FilterSlider` - 滑块筛选
- `FilterSwitch` - 开关筛选
- `FilterColor` - 颜色筛选
- `FilterRadio` - 单选筛选
- `ConditionExpression` - 条件表达式

### Hooks 关键词
- `useTranslation` - 国际化翻译
- `useEventBus` - 事件总线
- `usePageCacheState` - 页面缓存状态
- `useCenterModalState` - 弹窗状态管理
- `useConfig` - 配置获取

### 国际化关键词
- `public_zhCN` - 中文语言包
- `public_enUS` - 英文语言包
- `public_viVN` - 越南文语言包

### 类型和枚举关键词
- `TableMaxProps`、`TableMaxColumnType` - 表格类型
- `FilterType`、`InputType` - 筛选和输入类型
- `CustomFormItemType` - 表单项类型
- `ColumnVisibleConfigType`、`ColumnPinningConfigType` - 列配置类型
- `ProFieldValueTypeEnum`、`DataSourceTypeEnum` - Schema表单类型

**手动使用场景：** 当用户需要：

- 使用 @arim-aisdc/public-components 组件库开发前端应用
- 配置 TableMax 高级表格（分页、筛选、排序、编辑、导出等）
- 构建复杂表单（CustomForm、QueryFilter、SchemaForm）
- 设置主题、权限、国际化等全局配置
- 实现拖拽、分割面板等交互功能
- 处理权限控制和条件渲染
- 解决组件库使用中的常见问题
- 实现表格 CRUD 操作、虚拟滚动、行拖拽等高级功能
- 自定义主题变量和样式
- 实现多语言国际化

## Instructions

### 核心组件能力

#### 1. TableMax 高级表格组件

这是组件库的核心组件，基于 TanStack React Table 构建，功能极其强大：

**核心特性:**

- **数据管理**: 支持前端/后端分页、排序、筛选
- **交互功能**: 行选择、行拖拽、列拖拽、行编辑
- **展示优化**: 虚拟列表、列固定、列宽调整、紧凑模式
- **数据操作**: 导出 Excel、上传数据、刷新、删除
- **缓存机制**: 自动缓存用户的列设置、筛选条件、排序状态

**完整 API 参数:**

```typescript
<TableMax
  // 基础配置
  tableId="unique-table-id" // 【必须】用于缓存，必须唯一
  columns={columns} // 【必须】列配置
  datas={data} // 【必须】表格数据
  // 分页配置
  totalCount={1000} // 数据总条数
  pageSize={20} // 每页条数
  skipCount={0} // 数据从第几条开始
  showSizeChanger={true} // 是否显示每页条数选择器
  changePagination={handlePagination} // 分页变化回调
  pageSizeOptions={[10, 20, 50, 100]} // 自定义每页条数选项
  showLessItems={false} // 翻页组件显示较少页码
  // 列配置
  columnVisibleConfig={{ name: true }} // 控制列显示隐藏
  columnPinningConfig={{
    // 列固定配置
    left: ['selection', 'name'],
    right: ['actions'],
  }}
  disableColumnDrag={false} // 禁止列拖拽
  columnResizeMode="onEnd" // 列宽调整时机: "onEnd" | "onChange"
  // 选择功能
  canSelection={true} // 是否支持多选
  defaultSelectedRowIds={[1, 2]} // 默认选中的行ID数组
  defaultSelectedRowId="1" // 默认选中的行ID（单选）
  selectionWithoutChecked={false} // 多选不显示勾选框
  canSelectionUseShift={true} // 是否支持Shift多选
  enableRowSelection={true} // 行是否可选
  selectRowWhenClick={true} // 点击行时是否选中
  onRowCheckboxClick={handleRowCheckboxClick} // 行checkbox点击回调
  onSelectChange={handleSelectChange} // 行选择变化回调
  rowSelectionChange={handleRowSelectionChange} // 行多选变化回调
  selectedRowChange={handleSelectedRowChange} // 【已废弃】行单选回调
  onSelectAllChange={handleSelectAllChange} // 全选回调
  // 拖拽功能
  canRowDrag={true} // 是否支持行拖拽
  disableDragRowIds={[1, 2]} // 禁止拖拽的行ID
  dragBeforeStart={() => true} // 拖拽开始前回调
  dragBeforeEnd={dragValidator} // 拖拽结束前验证
  rowOrderChange={handleRowOrderChange} // 行拖拽顺序变化回调
  // 筛选功能
  canFilter={true} // 是否支持筛选
  defaultEnableFilters={false} // 默认是否开启筛选
  defaultColumnFilters={[]} // 默认筛选条件
  manualFiltering={false} // 是否后端筛选
  onFilteringChange={handleFilteringChange} // 筛选变化回调（推荐）
  manualFilteringChange={manualFilterHandler} // 【已废弃】后端筛选回调
  getColumnFiltersData={getFilterData} // 【已废弃】筛选参数变化回调
  getDynamicFilterOptionsFn={getDynamicOptions} // 动态筛选选项获取函数
  openNullValueFilter={true} // 开启空值过滤
  // 排序功能
  canSorting={true} // 是否支持排序
  enableMultiSort={false} // 是否支持多列排序
  manualSorting={false} // 是否后端排序
  onSortingChange={handleSortingChange} // 排序变化回调（推荐）
  manualSortingChange={manualSortHandler} // 【已废弃】后端排序回调
  // 编辑功能
  canEditting={true} // 是否支持编辑
  canEditRowWhenDClick={false} // 是否双击行进入编辑
  saveEditing={handleSaveEditing} // 保存编辑内容回调
  onEditValueChange={handleEditValueChange} // 编辑值变化回调
  // 展示配置
  rowHeight={42} // 行高度
  defaultHeaderRowNum={1} // 表头默认行数
  defaultCompactMode={false} // 是否默认紧凑模式
  canCompact={true} // 是否显示紧凑模式按钮
  enableVirtualList={false} // 是否开启虚拟列表
  openVirtualColumns={false} // 开启虚拟列
  openVirtualRows={false} // 开启虚拟行
  autoHeight={false} // 高度是否自动占满父级
  tooltip={true} // 单元格是否显示tooltip
  // 数据操作
  canRefresh={true} // 是否显示刷新按钮
  refreshFun={handleRefresh} // 刷新回调
  canUpload={false} // 是否显示上传按钮
  uploadProps={{}} // 上传组件属性
  canDownload={false} // 是否显示下载按钮
  downloadProps={{}} // 下载配置
  canDelete={false} // 是否显示删除按钮
  deleteFun={handleDelete} // 删除回调
  canExport={false} // 是否导出表格数据
  exportConfig={{}} // 导出配置
  request={customRequest} // 自定义请求函数（用于下载）
  // 缓存配置
  version="1.0.0" // 缓存版本
  openMemo={true} // 是否开启memo缓存
  // 总计行
  hasTotalRow={false} // 是否有总计行
  totalDatas={[]} // 总计行数据
  // 序号列
  openIndexColumn={false} // 开启序号列
  // 自定义渲染
  renderOperate={customRender} // 自定义表格顶部所有内容
  tableTitle="表格标题" // 表格顶部左侧标题
  renderOperateLeft={customLeftRender} // 自定义表格顶部左侧内容
  renderOperateRight={customRightRender} // 自定义表格顶部右侧内容
  renderSubComponent={subComponentRender} // 子表渲染组件
  getRowCanExpand={() => true} // 行是否可展开
  // 样式配置
  rowClassName={rowClassGetter} // 行类名函数
  cellClassName={cellClassGetter} // 单元格类名函数
  rowStyle={{}} // 行内样式
  getCellProps={cellPropsGetter} // 单元格属性获取函数
  getHeaderCellProps={headerPropsGetter} // 表头单元格属性获取函数
  // 事件处理
  onRowMouseEnter={handleRowMouseEnter} // 鼠标进入行事件
  onRowMouseLeave={handleRowMouseLeave} // 鼠标离开行事件
  onRowMouseClick={handleRowMouseClick} // 鼠标点击行事件
  onRowMouseDoubleClick={handleRowDblClick} // 鼠标双击行事件
  getContextMenu={getContextMenu} // 获取右键菜单
  onClickContextMenu={handleContextMenuClick} // 点击菜单选项
  getRowHoverTipConfig={getHoverTip} // 获取行hover提示配置
  // 其他配置
  rowKey="id" // 行唯一标识字段
  canSetting={true} // 是否显示设置按钮
  loading={false} // 加载状态
  defaultHighLightRowId="1" // 默认高亮行ID
  // 【已废弃】属性
  theme="light" // 【已废弃】主题
  defaultScrollY={600} // 【已废弃】表格内容区高度
  emptyDataHeight={300} // 【已废弃】空数据高度
/>
```

**完整列配置参数:**

```typescript
const columns: TableMaxColumnType[] = [
  {
    // 基础配置
    id: 'name', // 【必须】列唯一标识
    header: '姓名', // 表头文案或渲染函数
    accessorKey: 'name', // 数据字段名
    accessorFn: (row, index) => row.name, // 自定义取值函数
    size: 120, // 列宽度
    parent: false, // 是否为父列（分组）
    child: false, // 是否为子列
    columns: [], // 子列配置（分组用）

    // 筛选配置
    filterType: FilterType.Input, // 筛选组件类型
    filterOptions: [
      // 筛选可选值
      { label: '选项1', value: '1' },
      { label: '选项2', value: '2' },
    ],
    filterKey: 'customFilterKey', // 自定义筛选值key
    enableColumnFilter: true, // 是否可筛选
    filterFn: customFilterFunction, // 自定义筛选函数
    filterComProps: {
      // 筛选组件属性配置
      showTime: true, // 时间筛选是否显示时分秒
      format: 'YYYY-MM-DD', // 时间格式
      picker: 'date', // 时间选择器类型
      rangePresets: [
        // 时间快捷选项
        { label: '最近7天', value: [dayjs().subtract(7, 'day'), dayjs()] },
      ],
    },
    dynamicFilterOptionsLabelField: 'name', // 动态选项标签字段
    dynamicFilterOptionsValueField: 'id', // 动态选项值字段
    dynamicFilterOptionsLabelFn: option => option.name, // 动态选项标签函数
    getFilterOptionsFn: getFilterOptions, // 动态获取筛选选项
    isFilterOptionsFrontSearch: false, // 筛选选项是否前端搜索

    // 编辑配置
    editable: true, // 是否可编辑
    editComType: InputType.Input, // 编辑组件类型
    editOptions: [
      // 编辑选项（select用）
      { label: '选项1', value: '1' },
      { label: '选项2', value: '2' },
    ],
    getEditOptionsFn: getEditOptions, // 动态获取编辑选项
    editComDisabled: false, // 编辑组件是否禁用
    required: true, // 编辑时是否必填
    unitsChangeFn: value => value, // 单位转换函数

    // 排序配置
    enableSorting: true, // 是否可排序
    sortingFn: customSortFunction, // 自定义排序函数
    sortUndefined: false, // undefined值处理方式
    sortingKey: 'customSortKey', // 自定义排序key

    // 样式配置
    tooltip: true, // 是否显示tooltip
    ellipsis: false, // 【已废弃】是否省略显示
    columnClassName: ['custom-col'], // 列类名
    enableResizing: true, // 是否可调整列宽

    // 元数据配置
    meta: {
      isDate: true, // 是否为日期字段
      dateFormat: 'YYYY-MM-DD', // 日期格式
    },

    // 其他配置
    openMemo: true, // 是否缓存单元格
    disabledExport: false, // 是否禁止导出
    exportValueFormat: value => formatValue(value), // 导出值格式化函数
  },
];
```

**列配置模式:**

```typescript
const columns: TableMaxColumnType[] = [
  {
    id: 'name',
    header: '姓名',
    accessorKey: 'name',
    size: 120,
    enableSorting: true,
    enableColumnFilter: true,
    filterType: FilterType.Input, // 筛选组件类型
    editable: true, // 可编辑
    editComType: InputType.Input, // 编辑组件类型
    tooltip: true, // 显示tooltip
  },
];
```

#### 2. ConfigProvider 全局配置

提供全局配置能力，是使用组件库的基础：

```typescript
<ConfigProvider
  config={{
    // 基础配置
    theme: 'dark', // 主题：'light' | 'dark'
    userId: 'user123', // 用户ID，用于缓存隔离
    tableKeyPrefixCls: 'my-app', // 表格缓存前缀，默认'TableMax'
    locale: public_zhCN, // 国际化语言配置
    dateFormat: 'YYYY-MM-DD HH:mm', // 日期格式

    // 主题配置
    themePackageName: 'DefaultThemePackage', // 主题包名称
    variablesJson: {
      // 主题变量配置
      '--global-primary-color': '#1890ff',
      '--table-row-hover-bgc': '#f0f0f0',
    },
    autoSetCssVars: true, // 是否自动设置CSS变量
    root: '#root', // 项目根节点选择器
    getRootContainer: () => document.getElementById('root'), // 获取根容器函数

    // TableMax 全局配置
    tableMax: {
      canExport: true, // 全局导出权限
      pageSizeOptions: [10, 20, 50, 100], // 全局分页选项
      cacheMaxAge: 3600000, // 缓存过期时间（毫秒）
      openMemo: true, // 是否开启memo缓存
      canSelectionUseShift: true, // Shift多选
      openNullValueFilter: true, // 空值过滤
      openIndexColumn: false, // 序号列
    },
    tableMaxNewPagination: false, // 是否使用新翻页组件

    // 自定义配置
    renderEmpty: theme => <CustomEmpty theme={theme} />, // 自定义空状态组件
    request: customRequest, // 自定义请求函数（用于下载等）

    // KeepAlive 配置
    keepAliveActivateKey: 1, // 激活key
    keepAliveUnactivateKey: 2, // 非激活key
  }}
>
  <App />
</ConfigProvider>
```

**默认配置值：**

```typescript
const DEFAULT_CONTEXT = {
  theme: 'light',
  userId: '',
  tableKeyPrefixCls: 'TableMax',
  locale: public_zhCN,
  dateFormat: 'YYYY-MM-DD HH:mm',
};
```

#### 3. Permission 权限控制

提供细粒度的权限控制能力：

```typescript
// 权限提供者
<PermissionProvider
  permissions={['user:read', 'user:write', 'admin']}
>
  <App />
</PermissionProvider>

// 权限限制组件
<Restricted
  permissions={['user:write']}              // 需要的权限列表
  fallback={<NoPermission />}               // 无权限时的fallback组件（可选）
>
  <Button>编辑用户</Button>
</Restricted>

// 使用Context直接访问
import { PermissionContext } from '@arim-aisdc/public-components';

const { hasPermission, permissions, currentUser } = useContext(PermissionContext);

// 检查权限
if (hasPermission('user:write')) {
  // 有权限时的操作
}

// 检查多个权限
if (hasPermission(['user:read', 'user:write'])) {
  // 有所有权限时的操作
}
```

**权限类型定义：**

```typescript
type Permission = string;

// 常见权限模式
('user:read'); // 用户读取权限
('user:write'); // 用户写入权限
('user:delete'); // 用户删除权限
('admin:system'); // 系统管理权限
('data:export'); // 数据导出权限
```

#### 4. Filter 组件系列

提供各种筛选组件，用于表格筛选或表单筛选：

```typescript
// 选择器筛选
<FilterSelect
  value={value}                                   // 当前值
  onChange={setValue}                               // 值变化回调
  options={[                                      // 选项列表
    { label: '选项1', value: '1' },
    { label: '选项2', value: '2' }
  ]}
  placeholder="请选择"                            // placeholder
  allowClear={true}                               // 是否可清除
  showSearch={true}                               // 是否支持搜索
  mode="multiple"                                 // 多选模式
  maxTagCount={3}                                 // 最多显示tag数量
/>

// 数值范围筛选
<FilterInputNumber
  value={value}                                   // 当前值（单值或数组）
  onChange={setValue}                               // 值变化回调
  min={0}                                        // 最小值
  max={100}                                      // 最大值
  step={1}                                       // 步长
  precision={2}                                   // 保留小数位数
  placeholder="请输入数值"                         // placeholder
  isShowInterval={true}                            // 是否显示为区间输入
  suffix="元"                                     // 后缀单位
/>

// 滑块筛选
<FilterSlider
  value={value}                                   // 当前值
  onChange={setValue}                               // 值变化回调
  range={[0, 100]}                                // 滑块范围
  min={0}                                        // 最小值
  max={100}                                      // 最大值
  step={1}                                       // 步长
  marks={{                                        // 刻度标记
    0: '0%',
    50: '50%',
    100: '100%'
  }}
  tooltipVisible={true}                            // 是否显示tooltip
/>

// 开关筛选
<FilterSwitch
  value={value}                                   // 当前值
  onChange={setValue}                               // 值变化回调
  checkedChildren="开启"                           // 选中时文字
  unCheckedChildren="关闭"                         // 未选中时文字
  disabled={false}                                // 是否禁用
/>

// 颜色筛选
<FilterColor
  value={value}                                   // 当前值
  onChange={setValue}                               // 值变化回调
  showText={true}                                 // 是否显示文字
  allowClear={true}                               // 是否可清除
  presets={[                                      // 预设颜色
    { label: '红色', value: '#ff0000' },
    { label: '蓝色', value: '#0000ff' }
  ]}
/>

// 单选筛选
<FilterRadio
  value={value}                                   // 当前值
  onChange={setValue}                               // 值变化回调
  options={[                                      // 选项列表
    { label: '选项1', value: '1' },
    { label: '选项2', value: '2' }
  ]}
  optionType="button"                              // 选项类型：'default' | 'button'
  disabled={false}                                // 是否禁用
/>
```

**筛选组件通用属性：**

```typescript
// 所有筛选组件都支持的属性
interface FilterComponentProps {
  value: any; // 当前值
  onChange: (value: any) => void; // 值变化回调
  placeholder?: string; // placeholder
  disabled?: boolean; // 是否禁用
  allowClear?: boolean; // 是否可清除
  className?: string; // 自定义类名
  style?: React.CSSProperties; // 自定义样式
}
```

#### 5. ConditionExpression 条件表达式

用于构建复杂的查询条件，支持多条件组合和多分组：

```typescript
<ConditionExpression
  value={conditions} // 条件表达式值
  onChange={setConditions} // 值变化回调
  showParameter={true} // 是否显示参数选择框
  parameterOptions={[
    // 参数选项
    { label: '姓名', value: 'name' },
    { label: '年龄', value: 'age' },
    { label: '创建时间', value: 'createTime' },
  ]}
  labelInValue={false} // Select的labelInValue属性
  canFrontFilter={true} // 是否支持前端筛选
  frontendFilterOptionFun={(input, option) => {
    // 自定义前端筛选函数
    return option.label.toLowerCase().includes(input.toLowerCase());
  }}
/>
```

**数据结构定义：**

```typescript
// 条件项类型
type conditionItemType = {
  arguments?: any; // 参数值
  operator?: any; // 操作符：'=', '!=', '>', '>=', '<', '<=', 'Between', 'In'等
  argumentsValue?: any; // 参数具体值
  logicOperator?: string | null; // 逻辑操作符：'and', 'or', null
};

// 条件表达式项类型
type conditionExpressionItemType = {
  conditionItem: conditionItemType[]; // 条件项数组
  logicOperator?: string | null; // 与下一组的连接符：'and', 'or', null
};

// 组件Props类型
type ConditionExpressionPropsType = {
  value?: conditionExpressionItemType[]; // 组件的值
  onChange?: (value: conditionExpressionItemType[]) => void; // 值变化回调
  showParameter?: boolean; // 第一个参数是否展示
  parameterOptions?: { label: any; value: any }[]; // 参数选项
  labelInValue?: boolean; // Select的labelInValue属性
  canFrontFilter?: boolean; // 是否支持前端筛选
  frontendFilterOptionFun?: (input: any, option: any) => boolean; // 前端筛选函数
};

// 默认值结构
const defaultConditions = [
  {
    conditionItem: [
      {
        arguments: null,
        operator: '=',
        argumentsValue: null,
        logicOperator: null,
      },
    ],
    logicOperator: null,
  },
];
```

**操作符说明：**

```typescript
const operatorOptions = [
  { label: '=', value: '=' },
  { label: '!=', value: '!=' },
  { label: '>', value: '>' },
  { label: '>=', value: '>=' },
  { label: '<', value: '<' },
  { label: '<=', value: '<=' },
  { label: '在...之间', value: 'Between' }, // 需要两个值，用逗号分隔
  { label: '不在...之间', value: 'NotBetween' },
  { label: '包含', value: 'In' }, // 需要多个值，用逗号分隔
  { label: '不包含', value: 'NotIn' },
];

// 特殊操作符提示
const tooltipList = ['Between', 'NotBetween', 'In', 'NotIn'];
const tooltipTitle = '请使用逗号隔开多个参数值，如：1,2';
```

#### 6. ThemeProvider 主题系统

支持明暗主题切换和自定义主题变量：

```typescript
<ThemeProvider
  theme="dark" // 主题类型：'light' | 'dark'
  variablesConfig={{
    // 自定义主题变量
    '--global-primary-color': '#1890ff',
    '--global-default-text-color': '#ffffff',
    '--table-row-hover-bgc': '#f0f0f0',
    '--global-curd-input-background-color': '#494c5d',
  }}
>
  <App />
</ThemeProvider>
```

**主题类型定义：**

```typescript
type ThemeType = 'light' | 'dark';

type VariablesConfigType = {
  [key: string]: string | number; // CSS变量键值对
};

type ThemeProviderPropsType = {
  theme: ThemeType; // 主题类型
  variablesConfig?: VariablesConfigType; // 自定义主题变量配置
  children?: ReactNode; // 子组件
};
```

**内置主题变量：**

```css
/* 主要颜色变量 */
--global-primary-color              /* 全局主色 */
--global-curd-input-background-color /* 输入框背景色 */
--global-desc-text-disabled-color    /* 禁用文字颜色 */
--scrollThumb                       /* 滚动条颜色 */
--rowHoverBackgroundColor           /* 行hover背景色 */

/* 表格颜色变量 */
--tableColor1                      /* 表格字体颜色 */
--tableColor2                      /* 表格边框颜色 */
--tableColor3                      /* 表格边框颜色 */
--selectTableRow                    /* 选中行颜色 */
--tableTooltipBgc                  /* 表格tooltip背景色 */

/* 布局颜色变量 */
--globalColor0 ~ globalColor17    /* 布局颜色系列 */
--splite-line                       /* 分割线颜色 */
--global-tip-text-color            /* 提示文字颜色 */
```

### 7. Empty 空状态组件

用于显示空数据状态：

```typescript
<Empty
  emptyDarkImage={customDarkImage}              // 自定义暗色主题空状态图片
  emptyLightImage={customLightImage}            // 自定义亮色主题空状态图片
  text="暂无数据"                               // 自定义文本
/>

// 使用ConfigProvider的默认空状态
<Empty />
```

### 8. SchemaForm Schema驱动表单

基于 ProComponents 的 Schema 驱动表单，支持动态表单配置和多种数据源。

```typescript
import { SchemaForm, ProFieldValueTypeEnum, DataSourceTypeEnum } from '@arim-aisdc/public-components';

<SchemaForm
  layoutType="ModalForm"                        // 布局类型：'ModalForm' | 'DrawerForm' | 'Form'
  title="创建用户"                              // 表单标题
  open={visible}                                // 是否显示
  onOpenChange={setVisible}                     // 显示状态变化回调
  columns={[                                    // 表单列配置
    {
      title: '用户名',
      dataIndex: 'username',
      valueType: ProFieldValueTypeEnum.Text,    // 字段类型
      formItemProps: {
        rules: [{ required: true, message: '请输入用户名' }],
      },
    },
    {
      title: '角色',
      dataIndex: 'role',
      valueType: ProFieldValueTypeEnum.Select,
      dataSourceType: DataSourceTypeEnum.Remote, // 数据源类型
      request: async () => {                     // 远程数据请求
        const roles = await fetchRoles();
        return roles.map(r => ({ label: r.name, value: r.id }));
      },
    },
  ]}
  onFinish={async (values) => {                 // 提交回调
    await createUser(values);
    return true;
  }}
/>
```

**ProFieldValueTypeEnum 字段类型：**
- Text - 文本输入
- Select - 下拉选择
- Radio - 单选
- Checkbox - 复选
- DatePicker - 日期选择
- DateTimePicker - 日期时间选择
- DateRangePicker - 日期范围
- TextArea - 文本域
- Digit - 数字输入
- Money - 金额输入
- Password - 密码输入
- Switch - 开关

**DataSourceTypeEnum 数据源类型：**
- Static - 静态数据
- Remote - 远程数据

### 9. 其他核心组件

```typescript
// CenterModal 居中弹窗（支持拖拽和调整大小）
<CenterModal
  visible={visible}                             // 是否显示
  title="标题"                                 // 弹窗标题
  onOk={handleOk}                             // 确认回调
  onCancel={handleCancel}                       // 取消回调
  okText="确认"                                // 确认按钮文字
  cancelText="取消"                             // 取消按钮文字
  width={520}                                 // 弹窗宽度
  maskClosable={false}                         // 点击遮罩是否关闭
  destroyOnClose={true}                        // 关闭时销毁
  draggable={true}                             // 是否可拖拽
  resizable={true}                             // 是否可调整大小
/>

// Drawer 抽屉组件
<DrawerCom
  visible={visible}                             // 是否显示
  title="标题"                                 // 抽屉标题
  placement="right"                            // 位置：'left' | 'right' | 'top' | 'bottom'
  onClose={handleClose}                         // 关闭回调
  width={300}                                 // 宽度（left/right时）
  height={300}                                // 高度（top/bottom时）
  mask={true}                                 // 是否显示遮罩
  maskClosable={false}                        // 点击遮罩是否关闭
/>

// SplitPane 分割面板
<SplitPane
  defaultSize="50%"                            // 默认尺寸
  minSize="10%"                               // 最小尺寸
  maxSize="90%"                               // 最大尺寸
  split="vertical"                             // 分割方向：'vertical' | 'horizontal'
  onDragFinished={handleResize}                // 拖拽完成回调
>
  <SplitPane left>
    左侧内容
  </SplitPane>
  <SplitPane right>
    右侧内容
  </SplitPane>
</SplitPane>

// QueryFilter 查询筛选器
<QueryFilter
  fields={filterFields}                         // 筛选字段配置
  initialValues={initialFilterValues}            // 初始筛选值
  onSubmit={handleSubmit}                       // 提交回调
  onReset={handleReset}                        // 重置回调
  layout="inline"                              // 布局方式
  submitText="查询"                             // 提交按钮文字
  resetText="重置"                             // 重置按钮文字
/>

// DraggableBox 可拖拽盒子
<DraggableBox
  position={{ x: 100, y: 100 }}            // 初始位置
  onDrag={handleDrag}                         // 拖拽中回调
  onDragEnd={handleDragEnd}                   // 拖拽结束回调
  bounds="parent"                              // 边界限制
  disabled={false}                             // 是否禁用拖拽
>
  拖拽内容
</DraggableBox>

// Icon 图标组件
<Icon
  prefix="other"                              // 图标前缀
  name="add"                                  // 图标名称
  size={16}                                   // 图标大小
  color="#1890ff"                               // 图标颜色
  className="custom-icon"                      // 自定义类名
  onClick={handleClick}                        // 点击回调
/>

// CacheTabs 缓存标签页
<CacheTabs
  activeKey={activeKey}                       // 当前激活标签
  onChange={handleChange}                       // 标签变化回调
  items={tabItems}                             // 标签配置
  type="card"                                 // 标签类型
  size="default"                               // 标签大小
  tabBarExtraContent={extraContent}             // 标签栏额外内容
/>

// BaseInfo 基础信息展示
<BaseInfo
  data={infoData}                             // 展示数据
  columns={infoColumns}                        // 信息列配置
  layout="vertical"                            // 布局方式
  labelWidth={120}                             // label宽度
  bordered={true}                              // 是否显示边框
  size="default"                              // 尺寸大小
/>
```

## Hooks 能力

### 1. useTranslation 国际化翻译

强大的国际化翻译 Hook，支持嵌套键查找、占位符替换和数组翻译辅助函数。

```typescript
import { useTranslation } from '@arim-aisdc/public-components';

const [t, localeCode] = useTranslation();

// 基础翻译
const title = t('global.title'); // 获取翻译文本

// 嵌套键翻译
const message = t('user.profile.name'); // 支持点号分隔的嵌套键

// 占位符替换
const greeting = t('global.welcome', 'John', '2024'); // "欢迎 {0} 在 {1} 年加入"

// 获取当前语言代码
console.log(localeCode); // 'zh-CN' | 'en-US' | 'vi-VN'
```

**数组翻译辅助函数：**

```typescript
// tA - 通用数组翻译（自定义字段）
const translatedData = t.tA(data, {
  fieldKey: 'type', // 指定哪个字段作为翻译键
  labelKey: 'typeName', // 指定哪个字段保存翻译后的值
  groupPrefix: 'status', // 可选的分组前缀
});

// tT - 翻译 TableMax 列配置
const columns = t.tT([
  { id: 'name', accessorKey: 'name' },
  { id: 'age', accessorKey: 'age' },
]);
// 自动将 header 设置为 t(`apiField.${accessorKey}`)

// tQ - 翻译 QueryFilter 配置
const filterFields = t.tQ([
  { field: 'name', formType: 'text' },
  { field: 'status', formType: 'select' },
]);
// 自动设置 label 和 inputTips

// tF - 翻译 CustomForm 配置
const formFields = t.tF([
  { field: 'name', formType: CustomFormItemType.Text },
  { field: 'email', formType: CustomFormItemType.Text },
]);

// tB - 翻译 BaseInfo 配置
const infoFields = t.tB([
  { field: 'name', value: 'John' },
  { field: 'age', value: 25 },
]);
// 自动将 text 设置为 t(`apiField.${field}`)
```

**自定义语言包：**

```typescript
const customLocales = {
  'zh-CN': {
    myApp: {
      title: '我的应用',
      welcome: '欢迎使用',
    },
  },
  'en-US': {
    myApp: {
      title: 'My App',
      welcome: 'Welcome',
    },
  },
};

const [t] = useTranslation(customLocales);
const title = t('myApp.title'); // 自动合并自定义语言包
```

### 2. useEventBus 事件总线

全局事件总线 Hook，用于跨组件通信。

```typescript
import { useEventBus, events } from '@arim-aisdc/public-components';

// 发送事件（任何地方）
events.emit('data-changed', { id: 1, name: 'test' });
events.emit('user-login', { userId: '123', username: 'john' });

// 监听事件（在组件中）
useEventBus('data-changed', data => {
  console.log('数据变化:', data);
  // 自动在组件卸载时清理监听器
});

// 一次性监听
events.once('init-complete', () => {
  console.log('初始化完成');
});

// 手动移除监听器
const handler = data => console.log(data);
events.on('my-event', handler);
events.off('my-event', handler);

// 调用所有监听器并返回结果数组
const results = events.invoke('calculate', 10, 20);
```

### 3. usePageCacheState 页面缓存状态

自动缓存页面状态到 localStorage/sessionStorage，刷新页面后自动恢复。

```typescript
import { usePageCacheState } from '@arim-aisdc/public-components';

// 基础用法
const [state, setState] = usePageCacheState('page-key', { count: 0 });

// 更新状态（自动缓存）
setState({ count: 1 });

// 支持嵌套字段更新
const [formData, setFormData] = usePageCacheState('form-data', {
  user: { name: '', age: 0 },
  settings: { theme: 'light' },
});

setFormData({ user: { name: 'John' } }); // 深度合并

// 初始化状态（重置为初始值）
const [state, setState, initState] = usePageCacheState('key', initialValue);
initState();

// 清除缓存
const [state, setState, initState, clearState] = usePageCacheState('key', initialValue);
clearState();
```

**缓存特性：**
- 自动缓存到 localStorage
- 缓存有效期：1小时
- 支持深度合并嵌套对象
- 组件卸载时保留缓存
- 刷新页面自动恢复状态

### 4. useCenterModalState 弹窗状态管理

简化 CenterModal 状态管理的 Hook。

```typescript
import { useCenterModalState, CenterModal } from '@arim-aisdc/public-components';

const [modalProps, setModalProps, closeModal] = useCenterModalState();

// 打开弹窗
const openModal = () => {
  setModalProps({
    visible: true,
    title: '编辑用户',
    width: 600,
    // 其他 CenterModal 属性
  });
};

// 关闭弹窗
const handleOk = () => {
  // 处理确认逻辑
  closeModal();
};

// 渲染弹窗
<CenterModal
  {...modalProps}
  onOk={handleOk}
  onCancel={closeModal}
>
  弹窗内容
</CenterModal>
```

### 5. useConfig 配置获取

获取 ConfigProvider 提供的全局配置。

```typescript
import { useConfig } from '@arim-aisdc/public-components';

const config = useConfig();

// 访问配置
const theme = config.theme; // 'light' | 'dark'
const locale = config.locale; // 语言包对象
const userId = config.userId; // 用户ID
const dateFormat = config.dateFormat; // 日期格式
const tableMaxConfig = config.tableMax; // TableMax 全局配置
```

### 核心使用模式

#### 1. 表格 CRUD 操作模式

```typescript
// 1. 定义列配置
const columns = useMemo(
  () => [
    {
      id: 'id',
      header: 'ID',
      accessorKey: 'id',
      size: 80,
    },
    {
      id: 'name',
      header: '姓名',
      accessorKey: 'name',
      editable: true,
      filterType: FilterType.Input,
    },
  ],
  [],
);

// 2. 处理数据变更
const handlePagination = useCallback(({ skipCount, pageSize }) => {
  fetchData({ skipCount, pageSize });
}, []);

const handleSort = useCallback((sortValueArr, sortValueStr, sortedData) => {
  fetchData({ sort: sortValueStr });
}, []);

const handleFilter = useCallback(({ filters, formatFiltersV2 }) => {
  fetchData({ filters: formatFiltersV2 });
}, []);

// 3. 渲染表格
<TableMax
  tableId="user-table"
  columns={columns}
  datas={users}
  totalCount={total}
  pageSize={pageSize}
  skipCount={skipCount}
  canSelection={true}
  canEditting={true}
  canFilter={true}
  manualSorting={true}
  manualFiltering={true}
  changePagination={handlePagination}
  onSortingChange={handleSort}
  onFilteringChange={handleFilter}
/>;
```

#### 2. CustomForm 表单配置模式

```typescript
import { CustomForm, CustomFormItemType, CustomSearchFieldType } from '@arim-aisdc/public-components';

const formFields: CustomSearchFieldType[] = [
  {
    field: 'name', // 【必须】字段名
    label: '姓名', // 字段标签
    formType: CustomFormItemType.Text, // 表单类型
    defaultValue: '', // 默认值
    inputTips: '请输入姓名', // placeholder
    required: true, // 是否必填
    maxLength: 50, // 最大长度（文本域）
    span: 8, // 栅格占位格数
    tooltip: '姓名用于用户标识', // tooltip提示
  },
  {
    field: 'status',
    label: '状态',
    formType: CustomFormItemType.Select,
    defaultValue: 'active',
    setting: [
      // 下拉选项配置
      { label: '启用', value: 'active' },
      { label: '禁用', value: 'inactive' },
    ],
    showSearch: true, // 是否支持搜索
    mode: 'multiple', // 多选模式
    maxTagCount: 3, // 最多显示tag数量
    required: true,
  },
  {
    field: 'age',
    label: '年龄',
    formType: CustomFormItemType.Number,
    defaultValue: 18,
    min: 0, // 最小值
    max: 120, // 最大值
    step: 1, // 步长
    precision: 0, // 保留小数位数
    unit: '岁', // 单位
    required: true,
  },
  {
    field: 'createTime',
    label: '创建时间',
    formType: CustomFormItemType.DateTime,
    defaultValue: null,
    picker: 'date', // 时间选择器类型
    showTime: true, // 是否显示时间
    format: 'YYYY-MM-DD HH:mm:ss', // 显示格式
    allowClear: true, // 是否可清除
    disabledDate: current => {
      // 禁用日期
      return current && current > dayjs().endOfDay();
    },
  },
  {
    field: 'description',
    label: '描述',
    formType: CustomFormItemType.TextArea,
    defaultValue: '',
    rows: 4, // 文本域行数
    maxLength: 500,
    isShowToolTip: true, // 是否显示tooltip
  },
  {
    field: 'condition',
    label: '条件表达式',
    formType: CustomFormItemType.ConditionExpression,
    showParameter: true, // 是否显示参数选择框
    parameterOptions: [
      // 参数选项
      { label: '姓名', value: 'name' },
      { label: '年龄', value: 'age' },
    ],
    canFrontFilter: true,
  },
  {
    field: 'avatar',
    label: '头像',
    formType: CustomFormItemType.UploadImg,
    defaultValue: '',
    baseUrl: '/api/upload', // 上传地址
    token: 'your-upload-token', // 上传token
    method: 'POST', // 上传方法
  },
];

<CustomForm
  data={formFields} // 【必须】表单字段配置
  initialValues={initialData} // 初始值
  handleSubmit={handleSubmit} // 【必须】提交回调
  handleCancel={handleCancel} // 取消回调
  layout="horizontal" // 布局方式：'horizontal' | 'inline' | 'vertical'
  labelCol="120px" // label宽度
  span={24} // 栅格配置
  showButton={true} // 是否显示按钮
  isOkText="提交" // 确认按钮文字
  cancelText="取消" // 取消按钮文字
  submitLoading={false} // 提交loading状态
  labelAlign="right" // label对齐方式
  btnSpan={24} // 按钮栅格占位
  usage="submit" // 用途：'filter' | 'submit'
/>;
```

**表单类型枚举：**

```typescript
enum CustomFormItemType {
  Text = 'text', // 文本输入
  TextArea = 'textArea', // 文本域
  Number = 'number', // 数字输入
  Switch = 'switch', // 开关
  Select = 'select', // 选择器
  Cascader = 'cascader', // 级联选择
  RemoteCascader = 'remoteCascader', // 远程级联选择
  DateTime = 'datetime', // 日期时间
  DateRang = 'daterang', // 日期范围
  Interval = 'interval', // 区间输入
  Radio = 'radio', // 单选
  StartEnd = 'start-end', // 起止输入
  AutoComplete = 'autoComplete', // 自动完成
  MinMax = 'min-max', // 最小最大值
  CheckBox = 'checkbox', // 复选框
  Color = 'color', // 颜色选择
  ConditionExpression = 'conditionExpression', // 条件表达式
  RemoteSelect = 'remoteSelect', // 远程选择
  UploadImg = 'uploadImg', // 图片上传
}
```

#### 3. 主题配置模式

```typescript
// 在应用入口配置主题
const App = () => {
  return (
    <ConfigProvider
      config={{
        theme: 'dark',
        userId: getCurrentUserId(),
        variablesJson: {
          '--global-primary-color': '#1890ff',
          '--table-row-hover-bgc': '#1f1f1f',
        },
      }}
    >
      <ThemeProvider theme="dark">
        <Router>
          <Routes>
            <Route path="/" element={<HomePage />} />
          </Routes>
        </Router>
      </ThemeProvider>
    </ConfigProvider>
  );
};
```

### 最佳实践指导

#### 1. 性能优化

- 使用 `useMemo` 缓存列配置
- 使用 `useCallback` 缓存事件处理函数
- 大数据量时开启虚拟列表 `enableVirtualList={true}`
- 合理设置缓存时间 `cacheMaxAge`

#### 2. 缓存策略

- 每个表格必须设置唯一的 `tableId`
- 通过 `ConfigProvider` 设置用户 ID 实现缓存隔离
- 使用 `version` 参数控制缓存版本

#### 3. 国际化配置

```typescript
// 支持的语言
import {
  public_zhCN, // 中文
  public_enUS, // 英文
  public_viVN, // 越南文
} from '@arim-aisdc/public-components';
```

#### 4. 错误处理

- 使用 `to` 工具函数处理 Promise 错误
- 表格操作时添加 loading 状态
- 合理处理空数据状态

### 常见问题解决方案

#### 1. 表格缓存问题

```typescript
// 清除特定表格缓存
localStorage.removeItem(`${tableKeyPrefixCls}-${pathname}-${tableId}-${userId}`);

// 升级缓存版本
<TableMax version="1.0.1" />;
```

#### 2. 主题变量覆盖

```typescript
// 通过CSS变量覆盖主题
:root {
  --global-primary-color: #custom-color;
  --table-row-hover-bgc: #custom-hover;
}
```

#### 3. 权限控制集成

```typescript
// 与后端权限系统集成
const userPermissions = await fetchUserPermissions();
<PermissionProvider permissions={userPermissions}>
  <App />
</PermissionProvider>;
```

### 技术栈兼容性

- **React**: 17.0.1+
- **Ant Design**: 5.27.3+
- **TypeScript**: 支持，但 strict 模式关闭
- **构建工具**: Father (打包) + Dumi (文档)
- **样式**: Less + CSS 变量

### 工具函数

组件库提供了一些实用的工具函数：

```typescript
import { getTextWidth, to, judgeHasPermission } from '@arim-aisdc/public-components';

// 1. getTextWidth - 计算文本宽度
const width = getTextWidth('Hello World', 14); // 返回像素宽度
// 用途：动态计算列宽、文本截断判断

// 2. to - Promise 错误处理（Go 风格）
const [error, data] = await to(fetchUserData());
if (error) {
  console.error('请求失败:', error);
  return;
}
console.log('数据:', data);

// 3. judgeHasPermission - 权限数组比较
const hasPermission = judgeHasPermission(
  ['user:read', 'user:write'], // 需要的权限
  ['user:read', 'user:write', 'admin'] // 用户拥有的权限
);
// 返回 true（用户拥有所有需要的权限）
```

## 重要提醒

**AI 助手使用指南：**

1. **自动触发检测** - 当检测到上述关键词时，立即加载此技能
2. **优先使用本技能** - 优先遵循本技能的 API 模式和最佳实践
3. **缓存唯一性** - 确保总是提醒用户为 TableMax 提供唯一的 tableId
4. **全局配置** - 确保总是检查 ConfigProvider 的正确配置
5. **性能建议** - 根据使用场景主动提供性能优化建议
6. **类型安全** - 使用正确的类型定义（TableMaxProps、TableMaxColumnType、CustomFormItemType 等）
7. **国际化支持** - 优先使用 useTranslation 的辅助函数（tT、tQ、tF、tB）进行配置翻译
8. **错误处理** - 推荐使用 to() 工具函数进行 Promise 错误处理

**开发者使用提醒：**

1. **TableMax 必须配置**：
   - 总是为 TableMax 组件提供唯一的 tableId
   - 根据数据量选择是否开启虚拟滚动（enableVirtualList）
   - 后端分页时设置 manualSorting 和 manualFiltering 为 true

2. **全局配置最佳实践**：
   - 在应用根组件配置 ConfigProvider
   - 设置 userId 以实现用户级缓存隔离
   - 配置 tableKeyPrefixCls 避免缓存冲突
   - 使用 ThemeProvider 实现主题切换

3. **性能优化策略**：
   - 使用 useMemo 缓存列配置
   - 使用 useCallback 缓存事件处理函数
   - 大数据量（>1000行）开启虚拟列表
   - 合理设置 cacheMaxAge 控制缓存时间

4. **权限控制集成**：
   - 使用 PermissionProvider 包裹应用根组件
   - 使用 Restricted 组件进行条件渲染
   - 使用 judgeHasPermission 工具函数进行权限判断

5. **国际化配置**：
   - 在 ConfigProvider 中配置 locale
   - 使用 useTranslation 的辅助函数简化配置翻译
   - 支持自定义语言包扩展

**常见问题快速解决：**

1. **表格缓存问题**：清除 localStorage 中的表格缓存或升级 version
2. **主题不生效**：检查 ConfigProvider 的 autoSetCssVars 是否为 true
3. **权限不生效**：确保 PermissionProvider 包裹了需要权限控制的组件
4. **国际化不生效**：检查 ConfigProvider 的 locale 配置是否正确
5. **虚拟滚动问题**：确保设置了正确的 rowHeight

**技能版本信息：**

- 组件库版本：@arim-aisdc/public-components v2.3.77
- 技能创建时间：2026-01-29
- 技能维护：此技能应随组件库版本更新而更新
- 最后更新：2026-01-29

**组件库核心依赖：**

- React: >=17.0.1
- Ant Design: ^5.27.3
- @tanstack/react-table: ^8.9.1（TableMax 核心）
- @tanstack/react-virtual: ^3.13.12（虚拟滚动）
- dayjs: ^1.11.11（日期处理）
- react-dnd: ^16.0.1（拖拽功能）
- xlsx: ^0.18.5（Excel 导出）

这个技能将帮助 AI 模型更好地理解和使用这个组件库，提供准确、高效的前端开发解决方案。
