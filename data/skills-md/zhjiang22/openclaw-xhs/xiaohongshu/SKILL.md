---
name: xiaohongshu
description: |
  小红书内容工具。使用场景：
  - 搜索小红书内容
  - 获取首页推荐列表
  - 获取帖子详情（包括互动数据和评论）
  - 发表评论到帖子
  - 获取用户个人主页
  - "跟踪一下小红书上的XX热点"
  - "分析小红书上关于XX的讨论"
  - "小红书XX话题报告"
  - "生成XX的小红书舆情报告"
---

# 小红书 MCP Skill

基于 [xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) 封装。

> **完整文档请查看 [README.md](README.md)**

## 快速参考

| 脚本 | 用途 |
|------|------|
| `install-check.sh` | 检查依赖是否安装 |
| `start-mcp.sh` | 启动 MCP 服务 |
| `stop-mcp.sh` | 停止 MCP 服务 |
| `status.sh` | 检查登录状态 |
| `search.sh <关键词>` | 搜索内容 |
| `recommend.sh` | 获取推荐列表 |
| `post-detail.sh <note_id> <xsec_token>` | 获取帖子详情 |
| `comment.sh <note_id> <xsec_token> <内容>` | 发表评论 |
| `user-profile.sh <user_id>` | 获取用户主页 |
| `track-topic.sh <话题> [选项]` | 热点跟踪报告 |
| `mcp-call.sh <tool> [args]` | 通用工具调用 |

## 快速开始

```bash
cd scripts/

# 1. 检查依赖
./install-check.sh

# 2. 启动服务
./start-mcp.sh

# 3. 检查状态
./status.sh

# 4. 搜索内容
./search.sh "春节旅游"
```

## MCP 工具

| 工具名 | 描述 |
|--------|------|
| `check_login_status` | 检查登录状态 |
| `search_feeds` | 搜索内容 |
| `list_feeds` | 获取首页推荐 |
| `get_feed_detail` | 获取帖子详情和评论 |
| `post_comment_to_feed` | 发表评论 |
| `reply_comment_in_feed` | 回复评论 |
| `user_profile` | 获取用户主页 |
| `like_feed` | 点赞/取消 |
| `favorite_feed` | 收藏/取消 |
| `publish_content` | 发布图文笔记 |
| `publish_with_video` | 发布视频笔记 |

## 热点跟踪

```bash
./track-topic.sh "DeepSeek" --limit 5
./track-topic.sh "春节旅游" --limit 10 --output report.md
./track-topic.sh "iPhone 16" --limit 5 --feishu
```

## 注意事项

- 首次运行会下载 headless 浏览器（~150MB）
- 同一账号避免多客户端同时使用
- 发布限制：标题≤20字符，正文≤1000字符，日发布≤50条
- Linux 服务器需要从本地获取 cookies，详见 [README.md](README.md)
