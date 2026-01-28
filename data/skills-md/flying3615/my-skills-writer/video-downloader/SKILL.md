---
name: video-downloader
description: 使用 nre 工具根据提供的链接和电影名称下载视频。
---

# Video Downloader Skill

该 Skill 允许 AI 助手响应用户的视频下载请求。当用户提供视频链接和电影/视频名称时，助手将自动执行下载任务。

## 触发条件

当用户发送类似以下内容的请求时：
- "帮我下载这个视频 [URL]，名字叫 [名称]"
- "下载电影 [名称]：[URL]"

## 操作步骤

1. **提取信息**：从用户输入中提取 `视频链接` (URL) 和 `电影名称` (Save Name)。
2. **定位目录**：进入指定的下载目录（默认为项目根目录或特定的 downloads 文件夹）。
3. **执行命令**：使用 `nre` 工具进行下载，默认设置线程数为 16。

## 命令模板

助手应生成的指令如下：

```bash
nre "[URL]" --save-name "[电影名称]" --thread-count 16
```

## 示例

**用户**: "下载这个：https://example.com/movie.m3u8，名字叫 '我的电影'"

**助手**: (执行中...)
```bash
nre "https://example.com/movie.m3u8" --save-name "我的电影" --thread-count 16
```

## 注意事项

- **工具要求**：确保 `nre` 工具在环境中已安装并可调用。
- **安装引导**：如果系统未安装 `nre` (N_m3u8DL-RE)，请指导用户前往 [N_m3u8DL-RE GitHub 仓库](https://github.com/nilaoda/N_m3u8DL-RE) 查看安装和使用说明。
- **名称处理**：处理电影名称中的特殊字符或空格，确保在命令中正确引用。
