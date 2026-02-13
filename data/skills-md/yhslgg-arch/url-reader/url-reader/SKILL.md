---
name: url-reader
description: 智能读取任意URL内容，支持微信公众号、小红书、今日头条、抖音、淘宝、天猫、京东、百度等中国主流平台，自动识别平台类型并提取核心内容。自动保存内容为Markdown，下载图片到本地。
---

# URL Reader - 智能网页内容读取器

一键读取任意URL的内容，自动识别平台类型，智能选择最佳读取策略，**自动保存内容和图片到本地**。

## 默认保存目录

```
/Users/ys/laoyang知识库/nickys/素材/
```

保存格式：
```
素材/
└── 2026-01-30_文章标题/
    ├── content.md      # Markdown内容
    ├── img_01.webp     # 图片1
    ├── img_02.webp     # 图片2
    └── ...
```

## 核心技术方案

### 三层读取策略（自动降级）

```
┌─────────────────────────────────────────────────────────────────┐
│                     URL Reader 技术架构                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  用户输入 URL                                                    │
│       ↓                                                         │
│  ┌─────────────┐                                                │
│  │ 平台识别器   │ → 识别URL所属平台（微信/小红书/淘宝等）           │
│  └─────────────┘                                                │
│       ↓                                                         │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    策略选择器                                ││
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐               ││
│  │  │ 策略1     │  │ 策略2     │  │ 策略3     │               ││
│  │  │ Firecrawl │→│ Jina      │→│ Playwright │               ││
│  │  │ (首选)    │  │ (备选)    │  │ (兜底)    │               ││
│  │  └───────────┘  └───────────┘  └───────────┘               ││
│  └─────────────────────────────────────────────────────────────┘│
│       ↓                                                         │
│  ┌─────────────┐                                                │
│  │ 内容提取器   │ → 提取标题、正文、作者、时间等                   │
│  └─────────────┘                                                │
│       ↓                                                         │
│  ┌─────────────┐                                                │
│  │ 格式化输出   │ → Markdown 格式                                │
│  └─────────────┘                                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 策略1：Firecrawl API（首选）

**特点**：
- AI 驱动的网页抓取
- 自动处理 JavaScript 渲染
- 自动绕过反爬机制
- 直接返回干净的 Markdown
- 支持 96% 的网站

**API 调用**：
```python
from firecrawl import Firecrawl

app = Firecrawl(api_key="fc-YOUR_API_KEY")
result = app.scrape(url, formats=["markdown"])
```

**定价**：
- 免费：500 页/月
- 付费：按量计费

### 策略2：Jina Reader API（备选）

**特点**：
- 完全免费
- 无需 API Key
- 支持动态渲染
- 返回 Markdown 格式

**使用方式**：
```
https://r.jina.ai/{原始URL}
```

### 策略3：Playwright 浏览器自动化（兜底）

**特点**：
- 支持登录态保持
- 可处理任何网站
- 需要首次手动登录

**适用场景**：
- 微信公众号（需要登录）
- 需要登录的平台
- 前两种策略都失败时

## 使用方式

### 方式1：直接对话

```
用户：帮我读取这个链接 https://mp.weixin.qq.com/s/xxxxx
用户：看看这个小红书 https://www.xiaohongshu.com/explore/xxxxx
用户：读一下这个网页 https://example.com/article
```

### 方式2：命令行调用

```bash
/url-reader https://example.com/article
```

## 支持的平台

| 平台 | 域名 | 推荐策略 | 备注 |
|------|------|----------|------|
| 微信公众号 | mp.weixin.qq.com | Firecrawl → Playwright | 可能需要登录 |
| 小红书 | xiaohongshu.com | Firecrawl → Jina | 短链接需解析 |
| 今日头条 | toutiao.com | Firecrawl → Jina | - |
| 抖音 | douyin.com | Firecrawl | 提取视频描述 |
| 淘宝 | taobao.com | Firecrawl → Playwright | 可能需要登录 |
| 天猫 | tmall.com | Firecrawl → Playwright | 可能需要登录 |
| 京东 | jd.com | Firecrawl → Jina | - |
| 百度 | baidu.com | Firecrawl → Jina | - |
| 知乎 | zhihu.com | Firecrawl → Jina | - |
| 微博 | weibo.com | Firecrawl → Playwright | 可能需要登录 |
| B站 | bilibili.com | Firecrawl → Jina | - |
| 通用网站 | * | Firecrawl → Jina | - |

## 工作流程

```
1. 接收 URL
2. 识别平台类型
3. 选择读取策略：
   ├─ 尝试 Firecrawl API
   │   ├─ 成功 → 返回内容
   │   └─ 失败 → 继续
   ├─ 尝试 Jina Reader
   │   ├─ 成功 → 返回内容
   │   └─ 失败 → 继续
   └─ 尝试 Playwright（需要登录态）
       ├─ 有登录态 → 读取内容
       └─ 无登录态 → 提示用户设置
4. 提取核心内容
5. 格式化输出
```

## 输出格式

```markdown
# [文章标题]

**来源**：[平台名称]
**作者**：[作者名称]
**发布时间**：[时间]
**原文链接**：[URL]

---

[正文内容]

---

**互动数据**（如有）：
- 阅读/播放：xxx
- 点赞：xxx
- 评论：xxx
```

## 配置说明

### Firecrawl API Key 配置

1. 访问 https://www.firecrawl.dev/ 注册账号
2. 获取 API Key
3. 配置环境变量：
   ```bash
   export FIRECRAWL_API_KEY="fc-YOUR_API_KEY"
   ```

### Playwright 登录态设置（可选）

用于需要登录的平台（如微信公众号）：

```bash
cd ~/.claude/skills/url-reader
source .venv/bin/activate
python scripts/wechat_reader.py setup
```

## 目录结构

```
url-reader/
├── skill.md              # 本文档
├── metadata.json         # 元数据
├── scripts/
│   ├── url_reader.py     # 主读取器（整合三种策略）
│   ├── firecrawl_reader.py   # Firecrawl 策略
│   ├── jina_reader.py        # Jina 策略
│   ├── wechat_reader.py      # Playwright 策略（微信）
│   └── url_identifier.py     # URL 平台识别器
└── data/
    └── wechat_auth.json  # 微信登录态（自动生成）
```

## 依赖安装

```bash
cd ~/.claude/skills/url-reader
python3 -m venv .venv
source .venv/bin/activate

# 核心依赖
pip install firecrawl-py requests

# Playwright（可选，用于需要登录的平台）
pip install playwright
playwright install chromium
```

## 常见问题

### Q: 为什么有些网站读取失败？

A: 可能原因：
1. 网站有强反爬机制 → 尝试 Playwright
2. 需要登录 → 设置登录态
3. 内容已删除 → 无法读取

### Q: Firecrawl 免费额度用完了怎么办？

A:
1. 自动降级到 Jina Reader（免费）
2. 或升级 Firecrawl 付费计划

### Q: 微信公众号总是读取失败？

A: 微信反爬最严格，建议：
1. 使用 Playwright + 登录态
2. 或手动复制内容

## 版本历史

- **v2.0**：整合 Firecrawl + Jina + Playwright 三层策略
- **v1.1**：添加 Playwright 浏览器自动化
- **v1.0**：基础功能
