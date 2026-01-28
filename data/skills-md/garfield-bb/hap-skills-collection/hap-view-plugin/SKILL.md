---
name: hap-view-plugin
description: 创建和开发明道云 HAP 自定义视图插件的技能。此技能应该在使用者需要开发 HAP 自定义视图插件、初始化本地开发环境、安装依赖、启动调试时使用。
license: MIT
---

# HAP 自定义视图插件开发技能

此技能提供创建和开发明道云 HAP 自定义视图插件的完整工作流程和开发规范。

## 关于此技能

此技能专门用于开发明道云 HAP（High-performance Application Platform）自定义视图插件。通过集成的脚手架工具，可以快速创建 React 基础示例模板项目，安装依赖并启动开发环境。

### 前置条件

在使用此技能前，确保：
1. 已安装 16.20 或更高版本的 Node.js
2. 拥有明道云开发者账号和插件开发权限
3. 了解基本的 React 开发知识

### 开发环境配置

#### Cursor 编辑器配置

下载 `mdye-cursorrules.md` 文件并复制其中内容到视图开发项目根目录下的 `.cursorrules` 文件中，即可在 Cursor 编辑器中获得明道云视图插件开发的智能提示和代码规范检查。

#### 教学 DEMO

请下载明道云视图插件开发教学 DEMO，此插件为开发者提供直观、可交互的 API 使用实例。

### 核心功能

#### 1. 安装 mdye-cli 工具
- 全局安装插件开发专用的命令行工具
- 验证工具安装是否成功

#### 2. 初始化本地项目
- 创建唯一的插件项目文件夹
- 使用 React 基础示例模板
- 生成项目配置文件

#### 3. 安装项目依赖
- 安装项目所需的 npm 依赖包
- 配置开发环境

#### 4. 启动开发环境
- 启动本地开发服务器
- 支持热重载和实时预览
- 提供线上调试能力

## 开发工作流程

### 步骤 1：检查并安装 mdye-cli 工具

**首先检查是否已安装：**
```bash
mdye --version
```

如果显示版本号，说明已安装，可以跳过安装步骤。

**如果未安装，根据系统安装：**

**Mac OS 用户：**
```bash
sudo npm install -g mdye-cli
```

**Windows/Linux 用户：**
```bash
npm install -g mdye-cli
```

**验证安装：**
```bash
mdye --version
```

### 步骤 2：初始化本地项目

**创建项目命令：**
```bash
mdye init view --id 693d2fed8474b99be3d3c12e-69563e5df03728c888c04f05 --template React
```

**参数说明：**
- `--id`: 插件 ID（示例 ID，实际使用时需要替换）
- `--template React`: 使用 React 基础示例模板

**项目结构：**
```
mdye_view_69563e5df03728c888c04f05/
├── package.json
├── mdye.json
├── src/
│   ├── index.jsx
│   ├── App.jsx
│   └── styles.less
└── .gitignore
```

### 步骤 3：进入项目目录并安装依赖

**进入项目目录：**
```bash
cd mdye_view_69563e5df03728c888c04f05
```

**安装依赖：**
```bash
npm i
```

### 步骤 4：启动开发环境

**启动命令：**
```bash
mdye start
```

**启动后：**
- 开发服务器将在 `http://localhost:3000/` 启动
- 将调试地址 `http://localhost:3000/bundle.js` 粘贴到明道云视图配置开发调试输入框
- 支持实时编辑和热重载

## HAP 产品线说明

### 🌐 多产品线支持

HAP 支持多个产品线和私有部署，在视图插件中调用 API 时需要注意 **host 配置**：

| 产品线 | API Host | 说明 |
|--------|----------|------|
| **明道云 HAP** | `https://api.mingdao.com` | 官方 SaaS 服务 |
| **Nocoly HAP** | `https://www.nocoly.com` | Nocoly SaaS 服务 |
| **私有部署 HAP** | `https://your-domain.com/api` | ⚠️ **注意：私有部署需要在域名后加 `/api`** |

**示例**：
- 明道云：`https://api.mingdao.com/v3/open/worksheet/getFilterRows`
- 私有部署：`https://p-demo.mingdaoyun.cn/api/v3/open/worksheet/getFilterRows` ← 注意 `/api`

**建议**：视图插件应该从 `window.mdye.env` 中获取 host 配置，而不是硬编码。

---

## API 使用指南

### 1. 环境变量及配置获取

#### 1.1 获取 env 环境变量

```javascript
// 使用辅助函数安全获取env中的配置项
function getEnvValue(env, key, defaultValue = null) {
  if (!env || !key) return defaultValue;

  const value = env[key];

  // 处理数组类型(字段选择器)
  if (Array.isArray(value)) {
    return value.length > 0 ? value[0] : defaultValue;
  }

  // 处理普通值
  return value !== undefined ? value : defaultValue;
}

// 使用示例
const titleFieldId = getEnvValue(env, 'title');
const maxRecords = getEnvValue(env, 'maxRecords', '50');
```

#### 1.2 获取 config 配置

```javascript
import { config } from "mdye";

// 获取应用、工作表、视图的ID
const { appId, worksheetId, viewId, controls } = config;

// 获取字段控件信息
const fieldControl = _.find(controls, { controlId: fieldId });
```

### 2. 数据获取 API

#### 2.1 获取工作表数据 (getFilterRows)

```javascript
import { api } from "mdye";

async function loadRecords() {
  const result = await api.getFilterRows({
    worksheetId,     // 必填-工作表ID
    viewId,          // 必填-视图ID
    pageIndex: 1,    // 可选-页码
    pageSize: 50,    // 可选-每页记录数
    sortId: "fieldId", // 可选-排序字段
    isAsc: true,     // 可选-升序排序
    // 获取关联字段数据
    requestParams: {
      plugin_detail_control: relationFieldId
    }
  });

  return result.data; // 记录数组
}
```

#### 2.2 获取记录详情 (getRowDetail)

```javascript
async function getRecordDetail(rowId) {
  const result = await api.getRowDetail({
    appId,
    worksheetId,
    viewId,
    rowId
  });

  return result.data;
}
```

#### 2.3 获取关联记录 (getRowRelationRows)

```javascript
async function loadRelationRows({ controlId, rowId }) {
  const result = await api.getRowRelationRows({
    worksheetId,
    controlId,       // 关联字段ID
    rowId,           // 主记录ID
    pageIndex: 1,
    pageSize: 10
  });

  return result.data;
}
```

### 3. 数据操作 API

#### 3.1 新增记录 (addWorksheetRow)

```javascript
async function addRecord(fieldsData) {
  const response = await api.addWorksheetRow({
    appId,
    worksheetId,
    receiveControls: [
      {
        controlId: "fieldId1",
        type: 2,
        value: "测试文本"
      }
    ]
  });
  return response;
}
```

#### 3.2 更新记录 (updateWorksheetRow)

```javascript
async function updateRecord(rowId, fieldId, newValue) {
  const response = await api.updateWorksheetRow({
    appId,
    worksheetId,
    rowId,
    newOldControl: [
      {
        controlId: fieldId,
        type: 2,
        value: newValue
      }
    ]
  });
  return response;
}
```

#### 3.3 删除记录 (deleteWorksheetRow)

```javascript
async function deleteRecord(rowId) {
  const response = await api.deleteWorksheetRow({
    appId,
    worksheetId,
    rowIds: [rowId]
  });
  return response;
}
```

### 4. 工具函数 (utils)

#### 4.1 打开记录详情（推荐使用！）

**使用 `utils.openRecordInfo` 打开明道云原生行记录组件是最佳实践:**

优势:
- ✅ 原生体验,与明道云界面一致
- ✅ 功能完整:支持编辑、删除、讨论、日志、附件等所有功能
- ✅ 自动处理权限验证
- ✅ 无需自己开发弹窗 UI
- ✅ 返回操作结果,方便进行数据同步

**基础用法:**

```javascript
import { utils } from "mdye";

// 打开记录详情
const handleRecordClick = async (recordId) => {
  try {
    const result = await utils.openRecordInfo({
      appId,
      worksheetId,
      viewId,
      recordId
    });

    // 处理返回结果
    if (result) {
      console.log('操作结果:', result);

      // 根据操作类型处理
      switch (result.action) {
        case 'update':
          // 记录被更新,刷新数据
          console.log('记录已更新:', result.value);
          loadRecords(); // 重新加载数据
          break;
        case 'delete':
          // 记录被删除,刷新列表
          console.log('记录已删除');
          loadRecords(); // 重新加载数据
          break;
        case 'close':
          // 用户关闭弹窗(无修改)
          console.log('用户关闭了弹窗');
          break;
      }
    }
  } catch (error) {
    console.error('打开记录详情失败:', error);
  }
};
```

**返回值说明:**

```javascript
{
  action: 'update' | 'delete' | 'close',  // 操作类型
  value: object | null                     // 更新后的记录数据(仅 action='update' 时)
}
```

**完整的 React Hook 示例(包含自动刷新):**

```javascript
import React, { useEffect, useState } from 'react';
import { config, api, utils } from 'mdye';

function RecordsList() {
  const { appId, worksheetId, viewId } = config;
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(false);

  // 加载记录列表
  const loadRecords = async () => {
    try {
      setLoading(true);
      const result = await api.getFilterRows({
        worksheetId,
        viewId,
        pageSize: 100,
        pageIndex: 1
      });
      setRecords(result.data || []);
    } catch (error) {
      console.error('加载记录失败:', error);
    } finally {
      setLoading(false);
    }
  };

  // 打开记录详情
  const handleRecordClick = async (recordId) => {
    try {
      const result = await utils.openRecordInfo({
        appId,
        worksheetId,
        viewId,
        recordId
      });

      // 自动刷新列表
      if (result?.action === 'update' || result?.action === 'delete') {
        loadRecords(); // 刷新数据
      }
    } catch (error) {
      console.error('打开记录详情失败:', error);
    }
  };

  // 初始加载
  useEffect(() => {
    loadRecords();
  }, []);

  return (
    <div>
      {loading ? (
        <div>加载中...</div>
      ) : (
        <div>
          {records.map(record => (
            <div
              key={record.rowid}
              onClick={() => handleRecordClick(record.rowid)}
              style={{ cursor: 'pointer' }}
            >
              {record.title}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

**性能优化建议:**

```javascript
// 1. 使用 useCallback 避免重复创建函数
const handleRecordClick = useCallback(async (recordId) => {
  const result = await utils.openRecordInfo({
    appId, worksheetId, viewId, recordId
  });
  if (result?.action === 'update' || result?.action === 'delete') {
    loadRecords();
  }
}, [appId, worksheetId, viewId]);

// 2. 只在需要时刷新
const handleRecordClick = async (recordId) => {
  const result = await utils.openRecordInfo({
    appId, worksheetId, viewId, recordId
  });

  // 根据具体操作决定是否刷新
  if (result?.action === 'update') {
    // 局部更新(性能更好)
    setRecords(prev =>
      prev.map(r => r.rowid === recordId ? result.value : r)
    );
  } else if (result?.action === 'delete') {
    // 从列表中移除
    setRecords(prev => prev.filter(r => r.rowid !== recordId));
  }
};
```

#### 4.2 打开新建记录窗口

```javascript
utils.openNewRecord({
  appId,
  worksheetId
}).then(newRecord => {
  if (newRecord) {
    addLocalRecord(newRecord);
  }
});
```

#### 4.3 选择用户

```javascript
const users = await utils.selectUsers({
  projectId: "orgId1",
  unique: false  // 是否单选
});
```

#### 4.4 选择部门

```javascript
const departments = await utils.selectDepartments({
  projectId: "orgId1",
  unique: false
});
```

#### 4.5 选择位置

```javascript
const location = await utils.selectLocation({
  distance: 1000,
  defaultPosition: { lat: 39.915, lng: 116.404 },
  multiple: false
});
```

#### 4.6 选择记录

```javascript
const records = await utils.selectRecord({
  projectId: "orgId1",
  relateSheetId: "worksheetId1",
  multiple: true
});
```

### 5. 事件监听

#### 5.1 筛选条件变更事件

```javascript
import { md_emitter } from "mdye";

useEffect(() => {
  const handleFiltersUpdate = (newFilters) => {
    console.log('筛选条件已更新:', newFilters);
    // 重新获取数据
  };

  md_emitter.addListener('filters-update', handleFiltersUpdate);

  return () => {
    md_emitter.removeListener('filters-update', handleFiltersUpdate);
  };
}, []);
```

#### 5.2 新增记录事件

```javascript
useEffect(() => {
  const handleNewRecord = (newRecord) => {
    console.log('新增记录:', newRecord);
    setRecords(prev => [...prev, newRecord]);
  };

  md_emitter.addListener('new-record', handleNewRecord);

  return () => {
    md_emitter.removeListener('new-record', handleNewRecord);
  };
}, []);
```

## 特殊字段类型处理

### ⚠️ 重要提示:字段类型编号

**明道云字段类型编号与文档中的枚举值不完全一致,开发时务必注意:**

根据明道云 API V3 版本的实际字段类型定义:
- **Type 9** = 单选 (SingleSelect) ⚠️ 注意不是 type 11
- **Type 10** = 多选 (MultipleSelect)
- **Type 11** = 下拉 (Dropdown)

### 完整字段类型对照表(V3 实用版)

| 类型编号 | 枚举名称 | 字段类型 | API 创建 | API 返回 |
|---------|---------|---------|---------|---------|
| 2 | Text | 文本框 | ✅ | ✅ |
| 3 | PhoneNumber | 手机 | ❌ | ✅ |
| 4 | LandlinePhone | 座机 | ❌ | ✅ |
| 5 | Email | 邮箱 | ❌ | ✅ |
| 6 | Number | 数值 | ✅ | ✅ |
| 7 | Certificate | 证件 | ❌ | ✅ |
| 8 | Currency | 金额 | ❌ | ✅ |
| **9** | **SingleSelect** | **单选** | ✅ | ✅ |
| 10 | MultipleSelect | 多选 | ✅ | ✅ |
| 11 | Dropdown | 下拉 | ❌ | ✅ |
| 14 | Attachment | 附件 | ✅ | ✅ |
| 15 | Date | 日期 | ✅ | ✅ |
| 16 | DateTime | 时间 | ✅ | ✅ |
| 19/23/24 | Region | 地区 | ❌ | ✅ |
| 21 | DynamicLink | 自由链接 | ❌ | ✅ |
| 22 | Divider | 分段 | ❌ | ❌ |
| 25 | AmountInWords | 大写金额 | ❌ | ✅ |
| 26 | Collaborator | 成员 | ✅ | ✅ |
| 27 | Department | 部门 | ❌ | ✅ |
| 28 | Rating | 等级 | ❌ | ✅ |
| 29 | Relation | 连接他表 | ✅ | ✅ |
| 30 | Lookup | 他表字段 | ❌ | ✅ |
| 31 | Formula | 公式 | ❌ | ✅ |
| 32 | Concatenate | 文本拼接 | ❌ | ✅ |
| 33 | AutoNumber | 自动编号 | ❌ | ✅ |
| 34 | SubTable | 子表 | ❌ | ✅ |
| 35 | CascadingSelect | 级联选择 | ❌ | ✅ |
| 36 | Checkbox | 检查框 | ❌ | ✅ |
| 37 | Rollup | 汇总 | ❌ | ✅ |
| 38 | DateFormula | 公式(日期) | ❌ | ✅ |
| 39 | CodeScan | 扫码 | ❌ | ✅ |
| 40 | Location | 定位 | ❌ | ✅ |
| 41 | RichText | 富文本 | ❌ | ✅ |
| 42 | Signature | 签名 | ❌ | ✅ |
| 43 | OCR | 文字识别 | ❌ | ✅ |
| 44 | Role | 角色 | ❌ | ✅ |
| 45 | Embed | 嵌入 | ❌ | ❌ |
| 46 | Time | 时间 | ✅ | ✅ |
| 47 | Barcode | 条码 | ❌ | ✅ |
| 48 | OrgRole | 组织角色 | ❌ | ✅ |

### 常见错误示例

❌ **错误写法:**
```javascript
// 只查找 type 10 和 11,会遗漏 type 9 的单选字段
const selectField = controls?.find(ctrl =>
  ctrl.controlName?.includes('状态') && (ctrl.type === 10 || ctrl.type === 11)
);
```

✅ **正确写法:**
```javascript
// 包含 type 9, 10, 11 所有选项字段类型
const selectField = controls?.find(ctrl =>
  ctrl.controlName?.includes('状态') && (ctrl.type === 9 || ctrl.type === 10 || ctrl.type === 11)
);
```

### 字段解析函数

#### 单选字段

```javascript
function parseSingleSelect(value, control) {
  try {
    if (!value) return { key: "", text: "" };

    const keys = typeof value === 'string'
      ? JSON.parse(value)
      : (Array.isArray(value) ? value : []);

    const selectedKey = keys[0] || "";

    let selectedText = "";
    if (control && control.options) {
      const option = control.options.find(opt => opt.key === selectedKey);
      selectedText = option ? option.value : "";
    }

    return { key: selectedKey, text: selectedText };
  } catch (err) {
    console.error("解析单选字段失败:", err);
    return { key: "", text: "" };
  }
}
```

#### 多选字段

```javascript
function parseMultiSelect(value, control) {
  try {
    if (!value) return [];

    const keys = typeof value === 'string'
      ? JSON.parse(value)
      : (Array.isArray(value) ? value : []);

    const result = [];
    if (control && control.options) {
      keys.forEach(key => {
        const option = control.options.find(opt => opt.key === key);
        if (option) {
          result.push({ key: key, text: option.value });
        }
      });
    }

    return result;
  } catch (err) {
    console.error("解析多选字段失败:", err);
    return [];
  }
}
```

#### 成员字段

```javascript
function parseMembers(value) {
  try {
    if (!value) return [];
    return typeof value === 'string' ? JSON.parse(value) : value;
  } catch (err) {
    return [];
  }
}
```

#### 附件字段

```javascript
function parseAttachments(value) {
  try {
    if (!value) return [];
    return typeof value === 'string' ? JSON.parse(value) : value;
  } catch (err) {
    return [];
  }
}
```

#### 定位字段

```javascript
function parseLocation(value) {
  try {
    if (!value) return { title: "", address: "", x: 0, y: 0 };
    return typeof value === 'string' ? JSON.parse(value) : value;
  } catch (err) {
    return { title: "", address: "", x: 0, y: 0 };
  }
}
```

#### 关联记录字段（⚠️ 重要！）

**关联字段 (type 29) 的特殊处理规则:**

关联字段根据 `enumDefault` 或 `subType` 属性分为两种类型,返回数据格式完全不同:

1. **单条关联** (enumDefault=1 或 subType=1)
   - 返回格式: JSON 数组字符串
   - 示例: `"[{\"sid\":\"...\",\"name\":\"客户名称\",\"sourcevalue\":\"...\"}]"`
   - 处理方式: 直接解析 JSON 字符串即可

2. **多条关联** (enumDefault=2 或 subType=2)
   - 返回格式: 数字(表示关联记录的数量)
   - 示例: `2` (表示关联了 2 条记录)
   - 处理方式: **必须调用 `getRowRelationRows` API** 才能获取实际数据

**完整处理示例:**

```javascript
// 1. 判断是否为多条关联
function isMultipleRelation(value) {
  return typeof value === 'number' || (!isNaN(value) && value !== '');
}

// 2. 解析单条关联数据
function parseRelationData(value) {
  try {
    if (!value) return [];

    const relations = typeof value === 'string' ? JSON.parse(value) : value;
    if (!Array.isArray(relations)) return [];

    return relations.map(item => {
      let sourceValue = {};
      if (item.sourcevalue) {
        try {
          sourceValue = typeof item.sourcevalue === 'string'
            ? JSON.parse(item.sourcevalue)
            : item.sourcevalue;
        } catch (e) {
          console.error("解析sourcevalue失败:", e);
        }
      }

      return {
        sid: item.sid || '',
        name: item.name || '',
        rowid: sourceValue.rowid || '',
        ...item
      };
    });
  } catch (err) {
    console.error("解析关联记录字段失败:", err);
    return [];
  }
}

// 3. 完整使用示例（包含单条和多条处理）
async function loadOrdersWithProducts() {
  const result = await api.getFilterRows({
    worksheetId,
    viewId,
    pageSize: 1000,
    pageIndex: 1
  });

  // 使用 Promise.all 并行处理所有订单
  const ordersData = await Promise.all(
    result.data.map(async (row) => {
      // 获取关联产品字段值
      const productsValue = row['relationFieldId'];
      let products = [];

      // 判断是单条还是多条关联
      if (isMultipleRelation(productsValue)) {
        // 多条关联:调用 API 获取详情
        try {
          const relationResult = await api.getRowRelationRows({
            worksheetId,
            controlId: 'relationFieldId',  // 关联字段ID
            rowId: row.rowid,
            pageSize: 100,
            pageIndex: 1
          });

          if (relationResult && relationResult.data) {
            products = relationResult.data.map(item => ({
              name: item['productNameFieldId'],    // 产品名称字段ID
              code: item['productCodeFieldId'],    // 产品编码字段ID
              price: item['productPriceFieldId'],  // 产品单价字段ID
              rowid: item.rowid
            }));
          }
        } catch (error) {
          console.error('获取多条关联失败:', error);
        }
      } else {
        // 单条关联:直接解析
        products = parseRelationData(productsValue);
      }

      return {
        id: row.rowid,
        products: products,
        productsCount: isMultipleRelation(productsValue)
          ? Number(productsValue)
          : products.length
      };
    })
  );

  return ordersData;
}
```

**字段配置示例:**

```javascript
// 在 config.controls 中查看关联字段配置
const relationControl = controls.find(ctrl => ctrl.controlId === 'relationFieldId');

// 单条关联配置
{
  "controlId": "692ed1d0f34d7ea4df717c67",
  "type": 29,
  "controlName": "关联客户",
  "enumDefault": 1,  // 或 subType: 1
  // ... 其他属性
}

// 多条关联配置
{
  "controlId": "692ed1d0f34d7ea4df717c6e",
  "type": 29,
  "controlName": "关联产品",
  "enumDefault": 2,  // 或 subType: 2
  // ... 其他属性
}
```

### 自动获取字段值的工具函数

```javascript
function getFieldValue(fieldId, record, controls) {
  if (!fieldId || !record) return null;

  const rawValue = record[fieldId];
  if (rawValue === undefined) return null;

  const control = controls.find(ctrl => ctrl.controlId === fieldId);
  if (!control) return rawValue;

  const fieldType = getFieldTypeByControlType(control.type);

  switch (fieldType) {
    case 'text':
    case 'email':
    case 'phone':
      return rawValue;

    case 'number':
      return parseFloat(rawValue) || 0;

    case 'select':
      return parseSingleSelect(rawValue, control);

    case 'multiselect':
      return parseMultiSelect(rawValue, control);

    case 'user':
      return parseMembers(rawValue);

    case 'department':
      return parseDepartments(rawValue);

    case 'attachment':
      return parseAttachments(rawValue);

    case 'location':
      return parseLocation(rawValue);

    case 'boolean':
      return rawValue === "1" || rawValue === 1 || rawValue === true;

    case 'relation':
      return parseRelationData(rawValue);

    default:
      return rawValue;
  }
}

function getFieldTypeByControlType(controlType) {
  const typeMap = {
    2: 'text',           // 文本框
    3: 'phone',          // 手机
    4: 'phone',          // 座机
    5: 'email',          // 邮箱
    6: 'number',         // 数值
    7: 'certificate',    // 证件
    8: 'number',         // 金额
    9: 'select',         // 单选 ⚠️ 重要:type 9 是单选
    10: 'multiselect',   // 多选
    11: 'select',        // 下拉
    14: 'attachment',    // 附件
    15: 'date',          // 日期
    16: 'datetime',      // 时间
    19: 'region',        // 地区
    23: 'region',        // 地区
    24: 'region',        // 地区
    26: 'user',          // 成员
    27: 'department',    // 部门
    28: 'rating',        // 等级
    29: 'relation',      // 连接他表
    36: 'boolean',       // 检查框
    40: 'location',      // 定位
    41: 'richtext',      // 富文本
    42: 'signature',     // 签名
    46: 'time',          // 时间
    48: 'role',          // 组织角色
  };
  return typeMap[controlType] || 'unknown';
}
```

## mdye 命令行工具

### 基本命令

```bash
# 查看版本
mdye --version

# 授权登录
mdye auth

# 初始化项目
mdye init view --id <id> --template <template-name>

# 启动开发
mdye start

# 构建项目
mdye build

# 提交插件
mdye push -m "提交说明"

# 查看当前用户
mdye whoami

# 注销
mdye logout

# 同步插件参数配置
mdye sync-params -f <file-path>
```

### 插件发布流程（重要！）

插件开发完成后，需要按以下步骤提交发布到明道云平台。发布成功后，本插件在组织下所有应用均可使用。

#### 第1步：构建项目

执行以下命令将本地项目打包：

```bash
cd your_plugin_project
mdye build
```

**构建过程说明：**
- Webpack 会编译并打包所有源代码
- 生成优化后的 `bundle.js` 文件
- 通常需要 1-2 秒完成编译
- 成功后会显示 "构建代码完成" 和 bundle 文件大小

**构建输出示例：**
```
[21:20:33] 开始构建代码
ℹ Compiling Webpack
✔ Webpack: Compiled successfully in 1.94s
asset bundle.js 228 KiB [emitted] [minimized] (name: main)
webpack 5.98.0 compiled successfully in 1947 ms
[21:20:35] 构建代码完成
```

#### 第2步：提交并发布

执行以下命令将本地项目提交并推送到线上待发布插件列表：

```bash
mdye push -m "提交说明"
```

**提交说明编写建议：**

建议在提交信息中包含以下内容：
1. **功能特性**：列出插件的主要功能
2. **技术实现**：说明关键技术点和优化
3. **版本说明**：首次发布/功能更新/Bug修复

**完整示例：**

```bash
mdye push -m "订单状态视图插件首次发布

功能特性:
- 按订单状态分类展示(待付款/已付款/已发货/已完成/已取消)
- 完整订单信息展示(订单编号/客户/联系人/日期/金额/负责人)
- 多条关联产品信息展示(产品名称/编号/分类/单价)
- 点击订单卡片打开原生行记录弹窗
- 支持编辑/删除订单并自动刷新列表
- 响应式网格布局和流畅动画效果

技术实现:
- 正确处理单选字段(type 9)和关联记录字段(type 29)
- 使用 getRowRelationRows API 处理多条关联
- 使用 utils.openRecordInfo 实现原生交互
- Promise.all 并行加载提升性能"
```

#### 第3步：登录认证

提交时需要登录账户，按提示输入：
- 用户名（手机号或邮箱地址）
- 密码

如果已登录，可以通过 `mdye whoami` 查看当前登录用户。

#### 第4步：确认发布成功

发布成功后会显示插件信息：

```
[21:20:54] 文件上传成功
[21:20:55] push成功
┌──────────────────────────────────────────────────────────┐
│  ---- 插件信息 ----                                       │
│                                                           │
│  插件名称: 自定义视图                                     │
│  视图名称: 自定义视图                                     │
│  视图地址: https://www.mingdao.com/worksheet/...         │
│  提交信息: 订单状态视图插件首次发布                       │
│  提交人: 用户名                                           │
└──────────────────────────────────────────────────────────┘
```

#### 发布后的状态

✅ **插件已发布** - 可以在组织内所有应用中使用
✅ **视图地址** - 可以通过返回的 URL 直接访问插件
✅ **组织共享** - 组织内其他成员可以使用该插件

#### 常见问题

**问题1: 构建失败**
- 检查代码语法错误
- 确保所有依赖已正确安装 (`npm install`)
- 查看错误日志定位问题

**问题2: 推送失败**
- 确认已登录：`mdye whoami`
- 检查网络连接
- 验证账号权限是否支持插件开发

**问题3: 登录超时**
- 重新登录：`mdye auth`
- 输入正确的手机号/邮箱和密码

### 本地项目结构

```
plugin_project/
├── .config/          # 配置文件目录
├── src/              # 源代码目录
│   ├── components/   # 组件目录
│   ├── utils/        # 工具函数目录
│   ├── App.js        # 主应用组件
│   ├── index.js      # 入口文件
│   └── style.less    # 样式文件
├── mdye.json         # 插件配置文件
└── package.json      # 项目依赖配置
```

## 最佳实践

### 1. 项目组织
- 保持项目结构清晰
- 合理划分组件和模块
- 使用有意义的文件命名

### 2. 代码质量
- 遵循 React 最佳实践
- 使用 ESLint 和 Prettier
- 编写清晰的注释和文档

### 3. 性能优化
- 使用 React.memo 优化渲染
- 避免不必要的重渲染
- 优化状态管理
- 使用代码分割

### 4. 安全注意事项
- 避免硬编码敏感信息
- 使用环境变量管理配置
- 验证用户输入
- 防止 XSS 攻击

## 常见问题解决

### 问题 1：选项字段显示 key 而不是文本

**问题描述:** 单选或多选字段显示的是 UUID 格式的 key (如 `42ad38bf-d3e6-441f-a960-670e704abe4a`),而不是选项的显示文本。

**原因分析:**
1. 明道云选项字段返回的原始值是 JSON 格式的 key 数组,如 `"[\"42ad38bf-d3e6-441f-a960-670e704abe4a\"]"`
2. 需要从 `config.controls` 中找到对应字段的 `options`,然后根据 key 匹配出 value

**解决方案:**
```javascript
// 1. 获取字段控件定义(包含options)
const control = config.controls.find(ctrl => ctrl.controlId === fieldId);

// 2. 解析选项字段
function parseSingleSelect(value, control) {
  try {
    if (!value) return { key: "", text: "" };

    // 解析 JSON 字符串得到 key 数组
    let keys = [];
    if (typeof value === 'string') {
      try {
        keys = JSON.parse(value); // ["42ad38bf-..."]
      } catch {
        keys = [value];
      }
    } else if (Array.isArray(value)) {
      keys = value;
    }

    const selectedKey = keys[0] || "";

    // 从 options 中查找对应的显示文本
    let selectedText = "";
    if (control && control.options) {
      const option = control.options.find(opt => opt.key === selectedKey);
      selectedText = option ? option.value : selectedKey;
    }

    return { key: selectedKey, text: selectedText };
  } catch (err) {
    console.error("解析单选字段失败:", err, value);
    return { key: "", text: "" };
  }
}
```

### 问题 2：找不到单选字段

**问题描述:** 使用 `controls.find()` 查找单选字段时,返回 `undefined`。

**原因分析:**
- 单选字段的 type 是 **9** 而不是 11
- type 10 是多选,type 11 是下拉
- 如果只检查 `ctrl.type === 11`,会遗漏 type 9 的单选字段

**解决方案:**
```javascript
// ✅ 正确:包含所有选项字段类型
const selectField = controls?.find(ctrl =>
  ctrl.controlName?.includes('状态') &&
  (ctrl.type === 9 || ctrl.type === 10 || ctrl.type === 11)
);

// ❌ 错误:会遗漏 type 9
const selectField = controls?.find(ctrl =>
  ctrl.controlName?.includes('状态') &&
  (ctrl.type === 10 || ctrl.type === 11)
);
```

### 问题 3：多条关联字段只显示数字

**问题描述:** 关联字段显示的是数字(如 `2`、`3`),而不是实际的关联记录信息。

**原因分析:**
1. 多条关联字段 (enumDefault=2 或 subType=2) 返回的原始值是数字,表示关联记录的数量
2. 与单条关联不同,多条关联不会直接返回 JSON 数组字符串
3. 必须调用 `getRowRelationRows` API 才能获取实际的关联记录数据

**解决方案:**

```javascript
// 1. 判断是否为多条关联
function isMultipleRelation(value) {
  return typeof value === 'number' || (!isNaN(value) && value !== '');
}

// 2. 处理关联字段(支持单条和多条)
async function handleRelationField(worksheetId, controlId, rowId, fieldValue) {
  let relationData = [];

  if (isMultipleRelation(fieldValue)) {
    // 多条关联:调用 API 获取详情
    try {
      const result = await api.getRowRelationRows({
        worksheetId,
        controlId,
        rowId,
        pageSize: 100,
        pageIndex: 1
      });

      if (result && result.data) {
        relationData = result.data.map(item => ({
          rowid: item.rowid,
          name: item['titleFieldId'],  // 使用实际的标题字段ID
          // 解析其他需要的字段
        }));
      }
    } catch (error) {
      console.error('获取多条关联失败:', error);
    }
  } else {
    // 单条关联:直接解析
    relationData = parseRelationData(fieldValue);
  }

  return relationData;
}

// 3. 完整使用示例
async function loadRecordsWithRelations() {
  const result = await api.getFilterRows({
    worksheetId,
    viewId,
    pageSize: 100,
    pageIndex: 1
  });

  // 使用 Promise.all 并行处理
  const records = await Promise.all(
    result.data.map(async (row) => {
      const relationValue = row['relationFieldId'];

      const relations = await handleRelationField(
        worksheetId,
        'relationFieldId',
        row.rowid,
        relationValue
      );

      return {
        ...row,
        relations: relations
      };
    })
  );

  return records;
}
```

**如何判断字段是单条还是多条关联:**

```javascript
// 方法1: 查看字段配置
const control = config.controls.find(ctrl => ctrl.controlId === 'relationFieldId');
if (control) {
  const isSingle = control.enumDefault === 1 || control.subType === 1;
  const isMultiple = control.enumDefault === 2 || control.subType === 2;
  console.log('单条关联:', isSingle, '多条关联:', isMultiple);
}

// 方法2: 根据返回值类型判断
const value = row['relationFieldId'];
if (typeof value === 'number' || !isNaN(value)) {
  console.log('这是多条关联,需要调用 getRowRelationRows');
} else if (typeof value === 'string') {
  console.log('这是单条关联,可以直接解析 JSON');
}
```

### 问题 4：npm 安装失败
- 检查网络连接
- 清理 npm 缓存：`npm cache clean --force`
- 使用淘宝镜像：`npm config set registry https://registry.npmmirror.com`

### 问题 2：mdye 命令不存在
- 重新安装 mdye-cli
- 检查 PATH 环境变量
- 使用 `which mdye` 检查安装位置

### 问题 3：项目启动失败
- 检查端口是否被占用
- 检查依赖是否完整安装
- 查看错误日志信息

### 问题 4：插件 ID 冲突
- 使用新的唯一后缀
- 删除旧的冲突项目
- 重新初始化项目

## 🤖 AI 助手执行指南

当用户请求开发明道云视图插件时,AI 必须按照以下流程执行:

### 1. 前置环境检查(必须执行)

**Step 1.1: 检查 Node.js 版本**

```bash
node --version
```

- ✅ 如果版本 >= 16.20: 继续下一步
- ❌ 如果版本 < 16.20 或未安装:
  - 告知用户需要安装 Node.js 16.20 或更高版本
  - 提供安装链接: https://nodejs.org/
  - 等待用户安装完成后再继续

**Step 1.2: 检查 mdye-cli 是否已安装**

```bash
mdye --version
```

- ✅ 如果显示版本号: mdye-cli 已安装,跳过安装步骤
- ❌ 如果命令不存在: **自动帮用户安装 mdye-cli**

**Step 1.3: 自动安装 mdye-cli(如果未安装)**

**Mac OS 用户:**
```bash
sudo npm install -g mdye-cli
```

**Windows/Linux 用户:**
```bash
npm install -g mdye-cli
```

**安装后验证:**
```bash
mdye --version
```

**告知用户:**
```
✅ mdye-cli 工具已安装

📋 安装信息:
- 工具名称: mdye-cli
- 版本: [显示版本号]
- 用途: 明道云视图插件开发专用命令行工具

💡 下一步:
- 现在可以开始创建视图插件项目了
```

### 2. 模板选择(根据需求自动选择)

根据用户需求选择合适的模板:

| 用户需求 | 推荐模板 | 说明 |
|---------|---------|------|
| 简单展示、学习示例 | `--template React` | React 基础模板,适合快速上手 |
| 需要 UI 组件库 | `--template React-Tailwind` | 包含 Tailwind CSS,适合快速构建界面 |
| 复杂业务逻辑 | `--template React` | 基础模板,可自行添加需要的库 |
| Vue 技术栈 | `--template Vue` | Vue 模板(如果可用) |

**默认推荐**: `--template React-Tailwind`(适合大多数场景)

### 3. 项目初始化(自动执行)

**Step 3.1: 询问或生成插件 ID**

- 如果用户提供了插件 ID: 直接使用
- 如果用户未提供: 使用示例 ID 或询问用户

**Step 3.2: 初始化项目**

```bash
mdye init view --id [插件ID] --template React-Tailwind
```

**Step 3.3: 进入项目目录并安装依赖**

```bash
cd mdye_view_[插件后缀]/
npm i
```

**如果 npm 安装失败:**
- 建议使用淘宝镜像: `npm config set registry https://registry.npmmirror.com`
- 清理缓存: `npm cache clean --force`
- 重新安装: `npm i`

### 4. 启动开发环境(自动执行)

```bash
mdye start
```

**启动后告知用户:**
```
✅ 视图插件开发环境已启动！

📋 项目信息:
- 项目目录: mdye_view_[插件后缀]/
- 开发服务器: http://localhost:3000/
- 调试地址: http://localhost:3000/bundle.js

💡 下一步:
1. 将调试地址粘贴到明道云视图配置的开发调试输入框
2. 在项目中编辑代码,支持热重载
3. 开发完成后运行 `npm run build` 生成发布包

📖 开发指南:
- 主入口文件: src/index.jsx
- 样式文件: src/styles.less
- API 使用: 参考技能文档中的 API 使用指南
```

### 5. 开发过程中的辅助

**用户请求数据查询时:**
- 使用 `api.getFilterRows()` 获取工作表数据
- 正确处理关联字段(参考"常见问题"部分)
- 处理选项字段(使用 key 值而非 value)

**用户请求数据操作时:**
- 使用 `api.addWorksheetRow()` 新增记录
- 使用 `api.updateWorksheetRow()` 更新记录
- 使用 `api.deleteWorksheetRows()` 删除记录

**用户遇到问题时:**
- 参考"常见问题与解决方案"部分
- 提供详细的诊断步骤和解决方案

### 6. AI 执行原则

- ✅ **主动检查**: 开发前必须检查 Node.js 和 mdye-cli
- ✅ **自动安装**: 检测到工具未安装时,自动帮用户安装
- ✅ **选择模板**: 根据用户需求自动选择合适的模板
- ✅ **完整流程**: 从环境检查到启动开发环境,一气呵成
- ✅ **错误处理**: 遇到错误时提供详细诊断和解决方案
- ❌ **不要跳过**: 不要跳过前置环境检查步骤
- ❌ **不要假设**: 不要假设用户已安装所有工具

---

## 参考资源

- 明道云开发者文档
- React 官方文档
- Node.js 官方文档
- 明道云开发者社区

---

**注意：** 此技能提供的是开发工作流程指导和 API 使用规范，实际开发中请根据具体需求调整配置和代码。
