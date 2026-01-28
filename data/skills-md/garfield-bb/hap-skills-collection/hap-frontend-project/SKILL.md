---
name: hap-frontend-project
description: Use when user mentions "building website with HAP", "HAP frontend project", "HAP as database", "enterprise website", "官网", "通过 HAP 搭建", "用 HAP 做网站", "HAP 网站", "搭建官网", "企业官网", "前后端分离", "内容管理系统", "HAP 前端", "HAP 官网" - provides complete HAP + frontend project setup guide including HAP backend configuration, frontend project structure, API integration, and data rendering.
---

# HAP 前后端项目搭建指南

## 触发条件（MANDATORY）

<EXTREMELY_IMPORTANT>
**当用户提到以下任何情况时，必须使用此技能：**

- ✅ "通过 HAP 搭建官网"
- ✅ "用 HAP 做网站"
- ✅ "HAP 前端项目"
- ✅ "HAP 作为数据库" + "网站"相关需求
- ✅ "企业官网" + "HAP"相关需求
- ✅ "搭建网站" + "HAP"相关需求
- ✅ "官网" + "HAP"相关需求
- ✅ "HAP 网站"
- ✅ "HAP 官网"
- ✅ "前后端分离" + "HAP"相关需求
- ✅ "内容管理系统" + "HAP"相关需求

**技能优先级：**
- 如果用户明确提到"HAP" + "网站/官网/前端"，必须优先使用此技能
- 如果用户提到"搭建网站"但没有提到技术栈，可以询问是否使用 HAP

**This is MANDATORY. No exceptions.**
</EXTREMELY_IMPORTANT>

---

## Overview

本技能提供使用**明道云 HAP（高级应用平台）**作为后台内容管理系统，搭建完整前后端分离项目的完整工作流。适用于企业官网、内容管理网站、数据展示平台、表单收集系统等多种场景。

**核心能力：**
- ✅ HAP 后台数据结构设计与配置
- ✅ 前端项目架构搭建（HTML/CSS/JS）
- ✅ HAP API V3 集成与数据交互
- ✅ 完整的开发工作流和最佳实践
- ✅ 自动启动本地开发服务器

**适用场景：**
- 企业官网（产品展示、新闻资讯、案例展示）
- 内容管理网站（博客、文档库、知识库）
- 数据展示平台（数据看板、报表展示）
- 表单收集系统（在线预约、问卷调查、询价订单）
- 营销落地页（活动页面、促销页面）

---

## HAP 产品线说明

### 🌐 多产品线支持

HAP 支持多个产品线和私有部署，在前端项目中调用 API 时需要配置正确的 **API Host**：

| 产品线 | API Host | 说明 |
|--------|----------|------|
| **明道云 HAP** | `https://api.mingdao.com` | 官方 SaaS 服务 |
| **Nocoly HAP** | `https://www.nocoly.com` | Nocoly SaaS 服务 |
| **私有部署 HAP** | `https://your-domain.com/api` | ⚠️ **注意：私有部署需要在域名后加 `/api`** |

**示例**：
- 明道云：`https://api.mingdao.com/v3/open/worksheet/getFilterRows`
- 私有部署：`https://p-demo.mingdaoyun.cn/api/v3/open/worksheet/getFilterRows` ← 注意 `/api`

**配置建议**：
- 在项目配置文件中设置 `API_BASE_URL`
- 根据用户的 MCP 配置自动判断使用哪个 host
- 如果用户未提供，需询问使用哪个产品线

---

## 工作流程

### 阶段 1: 需求理解与结构评估

**目标：** 理解用户需求，评估现有 HAP 应用结构

**必须执行：**
1. **读取应用结构**
   ```javascript
   // 获取应用工作表列表
   mcp__hap_mcp____get_app_worksheets_list({
       responseFormat: 'md'
   })
   
   // 获取特定工作表结构
   mcp__hap_mcp____get_worksheet_structure({
       worksheet_id: '工作表ID',
       responseFormat: 'md',
       ai_description: '工作表: <工作表名称>'
   })
   ```

2. **结构差距评估**
   - 识别业务对象（产品、案例、新闻等）
   - 判断现有结构可复用性
   - 识别缺失的工作表和字段

3. **输出评估报告**
   - ✅ 可复用结构清单
   - ➕ 建议新增内容
   - 🚫 不执行的操作（仅分析阶段）

**关键原则：**
- ⚠️ 此阶段**仅做分析，不得执行任何写操作**
- ✅ 必须先读取应用现有结构
- ✅ 必须评估是否满足需求

---

### 阶段 2: 用户确认（强制）

**目标：** 获得用户明确同意后再执行结构变更

**触发条件：**
- 🔴 需要新增工作表
- 🔴 需要新增字段到现有工作表
- 🔴 需要写入示例数据
- 🔴 需要修改现有字段配置

**确认方式：**
使用 `AskUserQuestion` 工具，清晰列出建议的操作：

```javascript
AskUserQuestion({
    questions: [{
        question: "根据业务需求分析，当前应用缺少「新闻资讯」相关数据表。是否允许创建新的工作表？",
        header: "新增工作表",
        multiSelect: false,
        options: [
            {
                label: "同意创建(推荐)",
                description: "创建「新闻资讯」工作表，包含标题、封面图、发布时间、内容等字段，并添加 5 条示例数据"
            },
            {
                label: "仅创建表结构",
                description: "只创建工作表和字段，不添加示例数据。前端页面可能显示为空"
            },
            {
                label: "暂不创建",
                description: "跳过此工作表，使用现有数据完成开发。新闻模块将无法展示"
            }
        ]
    }]
})
```

**禁止行为：**
- ❌ 未确认即新增工作表
- ❌ 未确认即新增字段
- ❌ 未确认即写入数据
- ❌ 假设用户意图

---

### 阶段 3: HAP 后台配置

**目标：** 在 HAP 中创建/补充数据结构和示例数据

**执行顺序：**
1. **创建新工作表**（如用户同意）
   ```javascript
   mcp__hap_mcp____create_worksheet({
       name: '新闻资讯',
       alias: 'news',
       fields: [
           { name: '标题', type: 'Text', isTitle: true, required: true },
           { name: '封面图', type: 'Attachment', required: false },
           { name: '发布时间', type: 'Date', required: false },
           { name: '内容', type: 'Text', required: false },
           { name: '是否发布', type: 'Checkbox', required: false }
       ],
       ai_description: '工作表: 新闻资讯'
   })
   ```

2. **补充字段到现有工作表**（如用户同意）
   ```javascript
   mcp__hap_mcp____update_worksheet({
       worksheet_id: '现有工作表ID',
       addFields: [
           { name: '封面图', type: 'Attachment' },
           { name: '详情', type: 'Text' }
       ],
       ai_description: '工作表: <工作表名称>'
   })
   ```

3. **添加示例数据**（如用户同意）
   ```javascript
   // 🔴 重要：附件字段必须填充图片 URL
   mcp__hap_mcp____batch_create_records({
       worksheet_id: '工作表ID',
       rows: [
           {
               fields: [
                   { id: '标题字段ID', value: '示例新闻标题' },
                   { id: '封面图字段ID', value: [{
                       name: 'news.jpg',
                       url: 'https://m1.mingdaoyun.cn/doc/20251205/095p6B8tbW3x9v1A5lc41O8QdYaua101bM8Wb7442Q2ZfKb21m8deM1U0r4UaC9h.png?e=1765001146299&token=...'
                   }] },
                   { id: '发布时间字段ID', value: '2024-12-01' },
                   { id: '内容字段ID', value: '新闻内容...' },
                   { id: '是否发布字段ID', value: '1' }
               ]
           }
           // ... 至少 5 条示例数据
       ],
       triggerWorkflow: false,
       ai_description: '工作表: 新闻资讯'
   })
   ```

**关键要求：**
- ✅ 每个新增工作表必须至少添加 **5 条示例数据**
- 🔴 **附件字段必须填充图片 URL**（使用文档提供的测试图片 URL）
- ❌ 绝不允许附件字段为空数组 `[]` 或空字符串 `''`
- ⚠️ SingleSelect/MultipleSelect 筛选必须使用 key（UUID），不能使用显示文本

**测试图片 URL（8个）：**
详见 `references/hap-as-database-guide.md` 第 1.3 节

---

### 阶段 4: 获取 API 凭证

**目标：** 获取 HAP API 认证信息

**方法一：通过 MCP 配置提取（推荐）**
```json
{
  "mcpServers": {
    "hap-mcp-应用名": {
      "url": "https://api.mingdao.com/mcp?HAP-Appkey=xxx&HAP-Sign=xxx"
    }
  }
}
```

从 URL 参数中提取：
- `HAP-Appkey`: 从 URL 参数提取
- `HAP-Sign`: 从 URL 参数提取

**方法二：手动获取**
1. 登录明道云 → 应用 → 设置 → API 密钥
2. 复制 Appkey 和 Sign

**获取工作表 ID 和字段 ID：**
- 通过 MCP: `get_worksheet_structure`
- 通过 API: `/v3/app/worksheets/{worksheetId}/structure`
- 浏览器审查元素: 查找 `data-controlid` 属性

---

### 阶段 5: 前端项目搭建

**目标：** 创建完整的前端项目结构

**项目结构：**
```
project-name/
├── index.html          # 主页面
├── css/
│   └── style.css       # 样式文件
├── js/
│   ├── config.js       # HAP 配置（Appkey、Sign、字段映射）
│   ├── api.js          # API 封装（请求、分页、筛选）
│   └── main.js         # 应用逻辑（渲染、事件处理）
├── images/             # 图片资源（可选）
└── README.md           # 项目说明
```

**核心文件模板：**

**1. js/config.js**
```javascript
const CONFIG = {
    API_BASE_URL: 'https://api.mingdao.com',
    HAP_APPKEY: '你的HAP_APPKEY',
    HAP_SIGN: '你的HAP_SIGN',
    WORKSHEETS: {
        PRODUCTS: '产品表ID',
        NEWS: '新闻表ID'
    },
    PRODUCT_FIELDS: {
        NAME: '产品名称字段ID',
        IMAGE: '产品图片字段ID',
        PRICE: '参考价格字段ID'
    }
};
```

**2. js/api.js**
- 通用请求方法（处理认证、错误）
- `getRows()` - 获取记录列表（支持分页、筛选、排序）
- `getRecord()` - 获取单条记录详情
- `getFieldValue()` - 通用字段值解析函数（支持所有字段类型）

**3. js/main.js**
- 应用初始化
- 数据加载与渲染
- 事件处理
- 错误处理

**4. index.html**
- 语义化 HTML 结构
- 响应式设计支持
- SEO 优化

**5. css/style.css**
- 现代、专业的视觉设计
- 响应式布局
- 微交互和动画

**详细代码模板：** 参考 `references/hap-as-database-guide.md` 第 2-6 节

---

### 阶段 6: API 集成

**目标：** 实现前端与 HAP API V3 的数据交互

**核心要点：**

1. **CORS 跨域请求**
   ```javascript
   headers: {
       'HAP-Appkey': CONFIG.HAP_APPKEY,
       'HAP-Sign': CONFIG.HAP_SIGN,
       'Content-Type': 'application/json'
   }
   ```

2. **分页查询**
   ```javascript
   API.getRows(worksheetId, {
       pageIndex: 1,
       pageSize: 20,
       includeTotalCount: true,
       filter: { /* 筛选条件 */ },
       sorts: [ /* 排序 */ ]
   })
   ```

3. **字段值解析**
   - 附件字段：使用 `downloadUrl`
   - 选项字段：提取 `value` 属性
   - 关联记录：提取 `name` 或 `sid`
   - 检查框：判断 `=== '1'`

**详细 API 使用规范：** 参考 `references/hap-api-usage-guide.md`

---

### 阶段 7: 数据渲染

**目标：** 实现动态数据渲染和用户交互

**核心要求：**
- ✅ 动态生成 DOM（使用模板字符串）
- ✅ 处理空数据状态（友好提示）
- ✅ 图片加载失败处理（占位图）
- ✅ 数据格式化（价格、日期等）
- ✅ 响应式布局
- ✅ 加载状态提示
- ✅ 错误处理和用户提示

**示例：**
```javascript
async loadProducts() {
    try {
        this.showLoading();
        const data = await API.getRows(CONFIG.WORKSHEETS.PRODUCTS, {
            pageSize: 20,
            filter: {
                type: 'group',
                logic: 'AND',
                children: [{
                    type: 'condition',
                    field: CONFIG.PRODUCT_FIELDS.PUBLISHED,
                    operator: 'eq',
                    value: ['1']
                }]
            }
        });
        this.renderProducts(data.rows);
    } catch (error) {
        this.showError('加载失败，请刷新重试');
    } finally {
        this.hideLoading();
    }
}
```

---

### 阶段 8: 启动开发服务器

**目标：** 自动启动本地开发服务器，供用户预览

**启动方式（按优先级）：**

1. **Python HTTP Server（推荐）**
   ```bash
   python -m http.server 8000
   ```

2. **npx serve**
   ```bash
   npx serve -p 8000
   ```

3. **PHP 内置服务器**
   ```bash
   php -S localhost:8000
   ```

**执行要求：**
- ✅ 使用 `run_in_background: true` 参数
- ✅ 立即向用户输出访问地址
- ✅ 端口被占用时尝试其他端口（8001、8080、3000）

**输出示例：**
```
✅ 项目搭建完成！
🚀 本地服务器已启动
📍 访问地址: http://localhost:8000
💡 提示: 在浏览器中打开上述地址即可预览网站
```

---

## 核心原则（必须遵守）

### 1. 数据来源原则（必须动态）

✅ **允许静态的内容：**
- 导航菜单文案
- 页脚信息
- UI 占位文本
- 固定的展示标题

❌ **禁止静态的内容（必须从 HAP 获取）：**
- 产品列表和详情
- 案例展示
- 新闻资讯
- 轮播图内容
- 价格信息
- 任何业务相关的展示数据

### 2. 只增不删原则（红线）

**✅ 允许的操作：**
- 新增工作表（需确认）
- 新增字段（需确认）
- 新增示例数据（需确认）

**❌ 严禁的操作：**
- 删除任何已有工作表
- 删除任何已有字段
- 修改已有字段的别名（除非用户明确要求）
- 修改已有数据（除非用户明确要求）

### 3. 示例数据强制要求

- ✅ 每个新增工作表必须至少添加 **5 条示例数据**
- 🔴 **附件字段必须填充图片 URL**（最重要！）
- ✅ 示例数据必须符合字段类型
- ✅ 示例数据必须可直接用于前端预览

### 4. SingleSelect/MultipleSelect 筛选规范

**🔴 重要警告：筛选必须使用 key（UUID），不能使用显示文本！**

```javascript
// ❌ 错误：使用显示文本
value: ['现代简约']  // 筛选失败！

// ✅ 正确：使用 key
value: ['a1b2c3d4-e5f6-7890-abcd-ef1234567890']  // 筛选成功

// 获取 key 的方法：
// 1. 调用 get_worksheet_structure 获取字段的 options
// 2. 从 options 中找到匹配的 key
```

---

## 常见问题

### Q1: 如何获取字段 ID？

**方法 1: 使用 MCP（推荐）**
```javascript
mcp__hap_mcp____get_worksheet_structure({
    worksheet_id: '工作表ID',
    responseFormat: 'md'
})
```

**方法 2: API 查询**
```javascript
fetch('https://api.mingdao.com/v3/app/worksheets/{worksheetId}/structure', {
    headers: {
        'HAP-Appkey': 'xxx',
        'HAP-Sign': 'xxx'
    }
})
```

**方法 3: 浏览器审查元素**
- 打开 HAP 工作表
- F12 检查元素
- 查找 `data-controlid` 属性

### Q2: 附件字段如何处理？

```javascript
// 附件字段返回格式
const attachments = row[fieldId]; // Array
// [{downloadUrl: 'https://...', fileName: '图片.jpg'}]

// 获取第一个附件 URL
const imageUrl = attachments[0]?.downloadUrl || '';

// 使用 HAP CDN 参数优化
const thumbnailUrl = `${imageUrl}?imageView2/2/w/300`;
```

### Q3: 如何保护 API 密钥安全？

**开发环境：** 可直接使用（localhost 不会泄露）

**生产环境：**
- 方案 1：使用后端代理（Node.js、PHP 等）
- 方案 2：使用 Serverless Functions（Vercel、Netlify）
- 方案 3：限制 HAP API 密钥权限（只读权限）

### Q4: 数据量大时如何优化性能？

1. **分页加载**: 设置合理的 pageSize（建议 20-50）
2. **字段筛选**: 只获取需要的字段
3. **前端缓存**: 使用 localStorage 或内存缓存
4. **懒加载**: 滚动到底部时加载更多
5. **防抖处理**: 搜索框使用 debounce

---

## 参考资源

### 核心文档

- **`references/hap-as-database-guide.md`** - 完整的 HAP 前后端项目搭建指南
  - 项目概述和架构说明
  - 详细步骤（HAP 配置、前端搭建、API 集成）
  - 核心概念和最佳实践
  - 常见问题和解决方案

- **`references/hap-api-usage-guide.md`** - HAP API V3 使用规范
  - API 端点和鉴权配置
  - 筛选器（Filter）语法详解
  - 字段类型处理和数据格式转换
  - 完整的代码示例

### 相关技能

- **HAP MCP 使用指南** - 了解如何使用 HAP MCP 进行应用管理和数据操作
- **HAP 视图插件开发指南** - 如需开发 HAP 视图插件（与本技能不同）

---

## 工作流检查清单

在执行本技能时，请确保完成以下所有步骤：

- [ ] **阶段 1**: 读取应用结构并评估差距
- [ ] **阶段 2**: 获得用户确认（如需要新增结构）
- [ ] **阶段 3**: 创建/补充 HAP 数据结构
- [ ] **阶段 3**: 添加示例数据（附件字段必须填充图片 URL）
- [ ] **阶段 4**: 获取 API 凭证（Appkey、Sign、工作表 ID、字段 ID）
- [ ] **阶段 5**: 创建前端项目结构（HTML、CSS、JS）
- [ ] **阶段 5**: 编写配置文件（config.js）
- [ ] **阶段 5**: 编写 API 封装（api.js）
- [ ] **阶段 5**: 编写应用逻辑（main.js）
- [ ] **阶段 6**: 实现 API 集成和数据交互
- [ ] **阶段 7**: 实现数据渲染和用户交互
- [ ] **阶段 8**: 启动本地开发服务器并提供访问地址

---

## 注意事项

1. **必须动态获取数据**: 业务数据必须从 HAP API 获取，不能写死在代码中
2. **用户确认机制**: 任何结构变更必须征得用户明确同意
3. **只增不删原则**: 绝不删除现有工作表、字段或数据
4. **附件字段填充**: 示例数据的附件字段必须填充图片 URL
5. **筛选使用 key**: SingleSelect/MultipleSelect 筛选必须使用选项的 key（UUID）
6. **自动启动服务器**: 完成项目搭建后必须自动启动本地开发服务器

---

**技能版本**: v1.0  
**最后更新**: 2026-01-11  
**适用场景**: HAP 前后端分离项目搭建
