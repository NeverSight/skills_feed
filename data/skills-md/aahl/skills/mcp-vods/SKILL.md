---
name: mcp-vods
description: 用于追剧/追番的技能，为AI提供搜索影视播放地址的能力，并支持在小米电视上直接播放。当用户想搜索影视、动漫、短剧、综艺等节目信息或更新进度时使用此技能。
---

# 追剧/追番
通过执行Shell命令可以调用工具和获取工具列表。

## 搜索工具
该工具需要在多个源站搜索，比较耗时，需要更多的超时时间，如果遇到超时，可以重新尝试。
- `npx -y mcporter call --stdio 'uvx mcp-vods' vods_search keyword="影视名称"`
- `npx -y mcporter call --stdio 'uvx mcp-vods' vods_search keyword="影视名称" page=2`

## 小米电视投屏工具
- 需要配置环境变量`MITV_LOCAL_IP`或`MITV_LIST_CFG`才能使用此工具。
- `npx -y mcporter call --stdio 'uvx mcp-vods' mitv_play_media url="影视URL" addr="小米电视IP"`

## 安卓电视投屏工具
- 需要配置环境变量`TVBOX_LOCAL_IP`或`TVBOX_LIST_CFG`并在电视上安装TvBox才能使用此工具。
- `npx -y mcporter call --stdio 'uvx mcp-vods' tvbox_play_media url="影视URL" addr="安卓电视IP"`

## 获取工具列表
- `npx -y mcporter list --stdio 'uvx mcp-vods' --schema --all-parameters`
