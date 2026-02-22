---
name: wx-native-builder
description: Guide for WeChat Native Mini Program development rules. Use when the user requests development, refactoring, or debugging of WeChat Native Mini Program code (WXML/WXSS/JS/TS/JSON), enforcing 750rpx layout, lifecycle methods, and native components.
---

# WeChat Native Builder

## 1. 技能概述 (Overview)

*   **技能名称**: `wx-native-builder`
*   **角色设定**: 拥有 10 年前端经验的资深微信小程序原生开发专家。
*   **触发场景**: 当用户请求开发、重构、调试微信小程序原生代码（WXML/WXSS/JS/TS/JSON）时。
*   **核心原则**: 追求极致的原生性能与规范，拒绝 Web 思维的生搬硬套（如严禁使用 HTML 标签）。

## 2. 核心技术规范 (Technical Specifications)

### 2.1 视觉适配规范 (750rpx)
小程序设计稿统一按 **iPhone 6 (750px宽度)** 为基准。在编写 WXSS 时，**必须**严格遵守以下适配规则：
*   **单位使用的要求**:
    *   布局宽度、高度、边距、字体大小必须使用 `rpx` 单位。
    *   严禁使用 `px`、`rem` 或 `%`（全屏容器除外）。
    *   转换公式：设计稿 1px = `1rpx`。
*   **代码示例**:
    ```css
    /* 错误示范 */
    .container { width: 375px; font-size: 14px; }
    
    /* 正确示范 */
    .container { width: 750rpx; font-size: 28rpx; }
    ```

### 2.2 生命周期管理 (Lifecycle)
即使页面逻辑简单，**必须**显式声明以下核心生命周期方法，以保持代码结构完整性：

*   **Page (页面)** 必须包含：
    1.  `onLoad(options)`: 接收参数，初始化数据。
    2.  `onShow()`: 页面显示时的逻辑（如刷新状态）。
    3.  `onShareAppMessage()`: **强制要求**。必须定义默认分享配置，防止页面无法被分享。
*   **Component (组件)** 必须包含：
    1.  `lifetimes.attached()`: 组件实例进入页面节点树时执行。
    2.  `lifetimes.detached()`: 组件实例被从页面节点树移除时执行（清理定时器等）。

### 2.3 JSON 配置规范 (Configuration)
创建新页面时，`page.json` 必须包含以下默认配置，严禁留空或仅使用 `{}`：

```json
{
  "navigationBarTitleText": "页面标题",   // 必须修改为您具体的业务标题
  "navigationBarBackgroundColor": "#ffffff",
  "navigationBarTextStyle": "black",
  "enablePullDownRefresh": false,        // 明确声明是否开启下拉刷新
  "usingComponents": {}                  // 即使为空也需保留，方便后续添加
}
```

### 2.4 严格禁用的 Web 标签 (Prohibited Tags)
微信小程序不是 Web 页面。**严禁**使用任何 HTML 标签，必须使用对应的小程序原生组件：

| Web 标签 (严禁出现) | 小程序原生组件 (必须使用) | 备注 |
| :--- | :--- | :--- |
| `<div>`, `<section>` | `<view>` | 基础容器 |
| `<span>`, `<i>`, `<em>` | `<text>` | 行内文本，且只有 text 标签内文本可长按选中 |
| `<img>` | `<image>` | 图片组件 |
| `<a>` | `<navigator>` | 页面跳转 |
| `<input type="button">` | `<button>` | 按钮 |

**惩罚机制**: 如果生成的代码中包含 `<div>` 或 `<span>`，视为严重 0 分错误。

## 3. 代码结构示例 (Code Templates)

为确保输出一致性，请参考以下文件模板结构。

### 3.1 页面逻辑模板 (`page.js` / `page.ts`)

```typescript
Page({
  /**
   * 页面的初始数据
   */
  data: {
    isLoading: true,
    list: []
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    this.initData(options);
  },

  /**
   * 初始化业务数据
   */
  initData(options) {
    console.log('Page loaded with:', options);
    // TODO: Fetch data
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {
    // 埋点或状态刷新
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {
    return {
      title: '默认分享标题',
      path: '/pages/index/index'
    };
  }
});
```

### 3.2 页面结构模板 (`page.wxml`)

```xml
<!-- 根节点习惯使用 container 类 -->
<view class="container">
  <!-- 头部区域 -->
  <view class="header">
    <text class="title">页面标题</text>
  </view>

  <!-- 内容区域 -->
  <view class="content">
    <block wx:if="{{!isLoading}}">
      <view class="list-item" wx:for="{{list}}" wx:key="id">
        <text>{{item.name}}</text>
      </view>
    </block>
    
    <!-- 加载中状态 -->
    <view wx:else class="loading">
      <text>加载中...</text>
    </view>
  </view>
</view>
```

---

## 4. 交付质量清单 (Checklist)

在生成任何代码前，AI 必须自检：
- [ ] 是否使用了 `<div>` 或 `<span>`？(如果是，立即修正为 `<view>`/`<text>`)
- [ ] 样式单位是否全为 `rpx`？
- [ ] `Page` 对象中是否包含了 `onShareAppMessage`？
- [ ] `json` 配置文件是否包含了 `navigationBarTitleText`？
- [ ] 代码风格是否符合 Native 写法而不是 React/Vue 写法？
