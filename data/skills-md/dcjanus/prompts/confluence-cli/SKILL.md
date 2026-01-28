---
name: confluence-cli
description: 查询、检索与阅读 Confluence 文档/页面。
---

说明：以下调用方式均以当前 `SKILL.md` 文件所在文件夹为 workdir。

1) 常用子命令（覆盖日常场景）
- `space`
  - `list [--start --limit --expand]`
  - `get --space-key [--expand]`
- `page`
  - `get --page-id [--body-format --expand]`
  - `by-title --space-key --title [--body-format --expand]`
  - `children --page-id [--start --limit --expand]`
  - `publish-markdown --parent-id --title --markdown-path [--update-if-exists --body-format --expand]`
- `attachment`
  - `list --page-id [--start --limit --expand]`
  - `download --page-id [--output-dir --name --filter --all --start --limit --expand]`
- `search`
  - `--cql [--start --limit --body-format --expand]`

2) 输出格式
- 所有调用统一在脚本后、子命令前加 `--json`（示例：`./scripts/confluence_cli.py --json page get --page-id ...`）

3) 冷门参数/字段怎么查
- 运行 `./scripts/confluence_cli.py <command> --help` 查看该命令的参数
- 需要更深入的 Confluence API 字段时，可扩展脚本中的 `expand` 参数

4) 附件下载示例
- 下载指定附件（可重复传入 `--name`）：`./scripts/confluence_cli.py attachment download --page-id 3060336952 --output-dir ./attachments --name a.png --name b.png`
- 下载全部附件（自动分页）：`./scripts/confluence_cli.py attachment download --page-id 3060336952 --all --output-dir ./attachments`
- 过滤下载（正则）：`./scripts/confluence_cli.py attachment download --page-id 3060336952 --filter 'image2026-1-19_.*\\.png' --all --output-dir ./attachments`

5) 发布 Markdown 示例
- 发布到父页面（同名则更新）：`./scripts/confluence_cli.py --json page publish-markdown --parent-id 3061931928 --title "批量重置 Offset 功能测试" --markdown-path /path/to/doc.md`

## 资源

- [confluence_cli.py](scripts/confluence_cli.py)：主 CLI 入口，负责读取配置并发起 API 调用。
- [confluence_api_client.py](scripts/confluence_api_client.py)：SDK 封装层，收敛常用 API 调用。
