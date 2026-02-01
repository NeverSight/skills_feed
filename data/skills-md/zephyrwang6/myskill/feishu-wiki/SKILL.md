---
name: feishu-wiki
description: 飞书知识库文档管理工具。支持查看知识库目录结构、创建和保存文档到飞书知识库。当用户说"保存到飞书"、"写入飞书知识库"、"发布到飞书"、"查看飞书目录"、"飞书知识库结构"时触发。适用于将 Obsidian 文档同步到飞书知识库，或在飞书中创建新文档。
---

# 飞书知识库管理

将 Markdown 文档保存到飞书知识库，支持查看目录结构和指定保存位置。

## 快速开始

### 查看目录结构

```bash
python scripts/list_wiki.py
```

输出示例：
```
📁 草稿箱 (YylJw806IinEJmkwOWVcv8HInph)
  📄 文章标题 (R6wxwODL7iCoQyknQsdcJleanFh)
  📁 分类文件夹 (ZXigwaUIViNr20k9KOKcEKgVnrg)
    📄 子文档 (GdaewKgtEicJcak37QmcgFsMnJc)
```

### 保存文档

保存 Markdown 文件到默认位置（草稿箱）：
```bash
python scripts/save_to_wiki.py --file /path/to/document.md
```

保存到指定父节点：
```bash
python scripts/save_to_wiki.py --file /path/to/document.md --parent TOKEN
```

直接指定标题和内容：
```bash
python scripts/save_to_wiki.py --title "文档标题" --content "文档内容"
```

## 工作流程

当用户请求保存文档到飞书时：

1. **先查看目录结构**
   - 运行 `list_wiki.py` 获取当前知识库目录
   - 向用户展示可选的保存位置

2. **确定保存位置**
   - 如果用户指定了位置（如"保存到 xxx 下"），使用对应的 token
   - 如果未指定，默认保存到草稿箱

3. **执行保存**
   - 运行 `save_to_wiki.py` 保存文档
   - 返回文档链接给用户

## 支持的 Markdown 格式

| 格式 | 转换结果 |
|------|---------|
| `# 标题` | 一级标题 |
| `## 标题` | 二级标题 |
| `### 标题` | 三级标题 |
| `#### 标题` | 四级标题 |
| 普通段落 | 文本块 |
| `- 项目` | 无序列表 |
| `1. 项目` | 有序列表 |

粗体、斜体、链接等格式会转换为纯文本。

## 知识库配置

当前配置的知识库：
- 根节点: 草稿箱 (`YylJw806IinEJmkwOWVcv8HInph`)
- Space ID: `7591325128043121630`

如需修改配置，编辑脚本中的常量。

## 常见用法示例

用户说 | 操作
------|-----
"保存到飞书" | 保存当前文档到草稿箱
"保存到飞书的 xxx 目录下" | 先查目录获取 token，再保存到指定位置
"查看飞书知识库目录" | 运行 list_wiki.py 展示目录结构
"把这篇文章发布到飞书" | 保存指定文档到飞书
