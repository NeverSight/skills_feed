---
name: news-summary
description: 新闻搜索、新闻摘要、新闻汇总、热点新闻、最新新闻、新闻整理、新闻收集。帮你搜索最近几天的相关新闻（12-25条），生成精美的HTML摘要页面，每条新闻都有摘要和AI深度解读功能，自动打开浏览器展示
---

# 新闻搜索摘要 Skill

一个智能新闻搜索和摘要工具，帮你快速获取和分析最新新闻。

## 核心功能

### 1. 搜索新闻
- 询问用户搜索主题
- 搜索最近 3-5 天的 12-25 条相关新闻
- **搜索工具**：优先使用 WebSearch，不可用时使用 Brave Search MCP
- **Brave Search 限制**：每次调用后必须 `sleep 1` 秒，防止速率限制
- **搜索优化**：
  * 使用多个关键词组合搜索
  * 分批搜索确保足够结果
  * 自动去重（标题/URL）
  * 如结果不足 12 条，扩大时间范围或关键词

### 2. 分析新闻
对每条新闻提取：
- 标题
- 来源网站
- 发布时间
- 权威性评估（高/中/低）
- 摘要（100-200字）
- 原文链接

### 3. 生成 HTML 页面
- **输出目录**：`<当前工作目录>/news-summary/<timestamp>_<topic>/`
  * 通过 `pwd` 获取当前工作目录的绝对路径
  * `<timestamp>` 格式：`YYYYMMDD_HHMM`（如：`20260111_1145`），确保每次搜索都有唯一目录
  * `<topic>` 从用户查询提取关键词（如：`AI`、`deepseek`），无法提取时使用 `news`
  * 示例：`/path/to/work/news-summary/20260111_1145_AI/`
- **文件名**：`news_summary_<topic>.html`
- **AI 解读目录**：`<当前工作目录>/news-summary/<timestamp>_<topic>/analysis/`
- **解读文件名**：`news_analysis_<newsId>.md`
- **页面特性**：
  * 美观的响应式设计
  * 卡片式新闻展示
  * 每条新闻包含：标题、来源、时间、权威性标签、摘要
  * 两个按钮："查看原文" 和 "AI解读"
  * **必须在 </body> 前包含**：`<script src="/news-ai.js"></script>`

### 4. AI 解读功能
- **服务器**：Node.js HTTP 服务器(lib/server.js，端口 3456)
- **真实 AI 分析**：通过 Claude Code CLI 生成深度解读
- **输出格式**：完整的 HTML 页面
  * 存储位置：`<工作目录>/news-summary/<timestamp_topic>/analysis/news_analysis_<id>.html`
  * 包含完整的 HTML 结构（<!DOCTYPE html>、<html>、<head>、<body>等）
  * 使用现代化的 CSS 样式，响应式设计
  * 颜色主题使用 #667eea 和 #764ba2 渐变
  * 包含新闻信息、分析内容、底部版权等完整结构
- **自定义 Prompt**：点击"AI解读"按钮后可输入自定义分析角度
- **阻塞和超时**：
  * 生成时显示加载模态框
  * 120 秒超时自动中止
- **文件管理**：
  * 已生成：显示"查看AI解读"和"删除解读"按钮
  * 未生成：显示"AI解读"按钮
  * 支持删除和重新生成
- **服务端点**：
  * `GET /check-analysis?newsId=<id>&timestamp=<timestamp_topic>` - 检查解读文件是否存在
  * `POST /analyze` - 生成 AI 解读（支持 customPrompt，输出完整 HTML）
  * `DELETE /delete-analysis?newsId=<id>&timestamp=<timestamp_topic>` - 删除解读
  * `GET /view-analysis?newsId=<id>&timestamp=<timestamp_topic>` - 查看解读（直接返回 HTML）
  * `GET /news-summary/<timestamp_topic>/<filename>` - 静态文件服务
  * `GET /news-ai.js` - 前端脚本

### 5. 重启服务器并打开浏览器
- **重启服务器步骤**（每次生成后必须执行）：
  1. 检查端口 3456 是否被占用：
     - Windows: `netstat -ano | findstr 3456`
     - macOS/Linux: `lsof -ti:3456` 或 `netstat -ano | grep 3456`
  2. 如果端口被占用，停止旧服务器：
     - Windows: `taskkill /F /PID <进程ID>`
     - macOS/Linux: `kill -9 <进程ID>`
  3. 重新启动服务器：
     - Windows: `start /B node <skill目录>/lib/server.js`
     - macOS/Linux: `node <skill目录>/lib/server.js &`
  4. 等待 2 秒确保服务器启动
  5. 验证启动：访问 `http://localhost:3456/news-ai.js` 应该返回 JavaScript 代码
- 生成 HTML 后，通过 HTTP 打开浏览器
- **浏览器命令**：
  * Windows: `Start-Process "http://localhost:3456/news-summary/<timestamp_topic>/news_summary_<topic>.html"`
  * macOS: `open "http://localhost:3456/news-summary/<timestamp_topic>/news_summary_<topic>.html"`
  * Linux: `xdg-open "http://localhost:3456/news-summary/<timestamp_topic>/news_summary_<topic>.html"`
- **重要**：必须通过 HTTP 访问，不能使用 file:// 协议

## 工作流程

1. 询问用户搜索主题
2. **生成唯一标识**：
   - 从查询中提取关键词作为 `<topic>`（无法提取则用 `news`）
   - 生成时间戳：`<timestamp>` = `YYYYMMDD_HHMM` 格式
   - 组合为：`<timestamp>_<topic>`（如：`20260111_1145_AI`）
3. 搜索新闻（WebSearch 优先；Brave Search 需间隔 1 秒）
4. 分析和整理新闻信息
5. **获取当前工作目录**：使用 Bash 命令 `pwd` 获取绝对路径
6. **创建目录**：`<当前工作目录>/news-summary/<timestamp>_<topic>/`
7. **生成 HTML**：
   - 文件路径：`<当前工作目录>/news-summary/<timestamp>_<topic>/news_summary_<topic>.html`
   - **必须在 </body> 前添加**：`<script src="/news-ai.js"></script>`
   - 每个新闻卡片必须包含 data 属性（data-news-id, data-news-url, data-news-source, data-news-time）
8. **重启服务器**：
   - 检查端口 3456 是否被占用
   - 如果被占用，停止旧服务器
   - 启动新服务器：`node <skill目录>/lib/server.js &`
   - 等待 2 秒并验证
9. 打开浏览器：`http://localhost:3456/news-summary/<timestamp>_<topic>/news_summary_<topic>.html`

## HTML 模板要求

- 现代简洁设计，响应式布局
- 卡片式新闻展示
- **每个新闻卡片必须包含 data 属性**：
  * `data-news-id`: 新闻 ID（0, 1, 2...）
  * `data-news-url`: 原文链接
  * `data-news-source`: 来源
  * `data-news-time`: 发布时间
  * `data-news-title`: 新闻标题
  * `data-news-summary`: 新闻摘要
- 权威性标签：高（绿色）、中（黄色）、低（灰色）
- 相对时间显示（如：2天前）
- **必须在 </body> 前引入**：`<script src="/news-ai.js"></script>`（使用绝对路径）
- **初始只包含"查看原文"按钮**，AI 解读按钮由 news-ai.js 在页面加载后动态添加

## 注意事项

- 使用绝对路径（通过 `pwd` 获取当前工作目录）
- 创建必要的目录结构
- 处理网络请求失败
- 验证新闻来源可靠性
- **必须在 HTML 中包含** `<script src="/news-ai.js"></script>`，否则 AI 解读功能不可用
- **时间戳格式**：必须使用 `YYYYMMDD_HHMM` 格式，确保每次搜索都有唯一目录
- **服务器必须重启**：每次生成新闻后必须重启服务器，确保 WORK_DIR 指向当前工作目录
