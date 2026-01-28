---
name: gitsite-content-manager
description: 自动管理 GitSite 静态网站生成器项目的 blogs、books 和 pages 内容。当用户需要创建博客文章、书籍章节、书籍或静态页面时使用此 skill。该 skill 会自动创建正确的目录结构、生成带有完整 frontmatter 的 Markdown 模板文件，并提供内容管理的 Python 脚本。适用于使用 GitSite CLI 构建的静态网站项目。
---

# GitSite Content Manager

## Overview

此 skill 专为使用 GitSite 静态网站生成器的项目设计，用于自动化管理网站内容（blogs、books 和 pages）。GitSite 使用特定的目录结构和 YAML 配置文件，每次手动创建内容时容易忘记正确的配置格式和文件位置。此 skill 确保内容创建的一致性和正确性。

## Quick Start

当用户请求创建以下任何内容时，使用此 skill：
- 创建新的博客文章
- 创建新的书籍
- 创建新的书籍章节
- 创建新的静态页面

## Content Creation Workflow

### 1. 创建博客文章 (Blog Post)

**目录结构：**
```
source/blogs/tech/
└── YYYY-MM-DD-post-slug/
    └── README.md
```

**使用 Python 脚本创建：**
```bash
python3 .claude/skills/gitsite-content-manager/scripts/manage_content.py blog \
  --title "My Blog Post Title" \
  --date "2025-01-15" \
  --description "A description of the post" \
  --tags tech tutorial \
  --author "Orangon"
```

**手动创建步骤：**
1. 在 `source/blogs/tech/` 下创建日期目录，格式：`YYYY-MM-DD-title-slug/`
2. 创建 `README.md` 文件，包含以下 frontmatter：
```yaml
---
title: "Blog Post Title"
date: 2025-01-15
description: "Blog post description"
tags:
  - tech
  - tutorial
author: Orangon
---

# Blog Post Title

<!-- Write your blog post content here -->

## Introduction

<!-- Add your introduction -->

## Main Content

<!-- Add your main content -->

## Conclusion

<!-- Add your conclusion -->
```

### 2. 创建书籍 (Book)

**目录结构：**
```
source/books/
└── book-name/
    ├── book.yml
    ├── index.md
    └── 01-Chapter-One/
        └── README.md
```

**使用 Python 脚本创建：**
```bash
python3 .claude/skills/gitsite-content-manager/scripts/manage_content.py book \
  --name "My-Book" \
  --title "My Book Title" \
  --description "Book description" \
  --author "Orangon"
```

**手动创建步骤：**
1. 在 `source/books/` 下创建书籍目录
2. 创建 `book.yml` 配置文件：
```yaml
title: My Book Title
description: Book description
author: Orangon
```
3. 创建 `index.md` 作为书籍索引页面

### 3. 创建书籍章节 (Book Chapter)

**使用 Python 脚本创建：**
```bash
python3 .claude/skills/gitsite-content-manager/scripts/manage_content.py chapter \
  --book "My-Book" \
  --number "01" \
  --title "Chapter One" \
  --description "Chapter description"
```

**手动创建步骤：**
1. 在书籍目录下创建章节目录，格式：`XX-Chapter-Title/`
2. 创建 `README.md` 文件：
```yaml
---
title: "Chapter One"
description: "Chapter description"
---

# 01. Chapter One

<!-- Write your chapter content here -->

## Overview

<!-- Add chapter overview -->

## Main Content

<!-- Add your main content -->

## Summary

<!-- Add chapter summary -->

## References

<!-- Add references if needed -->
```

### 4. 创建静态页面 (Page)

**目录结构：**
```
source/pages/
└── page-name/
    └── README.md
```

**使用 Python 脚本创建：**
```bash
python3 .claude/skills/gitsite-content-manager/scripts/manage_content.py page \
  --name "about" \
  --title "About Us" \
  --description "About page description"
```

**手动创建步骤：**
1. 在 `source/pages/` 下创建页面目录
2. 创建 `README.md` 文件：
```yaml
---
title: "About Us"
description: "About page description"
---

# About Us

<!-- Write your page content here -->
```

## Templates

使用 `assets/templates/` 中的模板文件作为内容创建的基础：

- `blog_post.md` - 博客文章模板
- `book_chapter.md` - 书籍章节模板
- `page.md` - 静态页面模板

这些模板包含完整的 frontmatter 结构和内容大纲。

## Important Notes

### 目录命名规范

1. **博客文章**：使用日期格式 `YYYY-MM-DD-title-slug/`
2. **书籍章节**：使用编号前缀 `XX-Chapter-Title/` (如 `01-Introduction/`)
3. **书籍目录**：使用 kebab-case 命名 (如 `AI-Coding/`)
4. **页面目录**：使用 kebab-case 命名 (如 `about-me/`)

### Frontmatter 格式

所有内容文件必须包含 YAML frontmatter，基本格式：
```yaml
---
title: "Content Title"
description: "Content description"
---
```

博客文章额外需要：
- `date`: 发布日期
- `tags`: 标签列表
- `author`: 作者名称

### 配置文件位置

- **网站配置**：`source/site.yml` (主配置)
- **博客配置**：`source/blogs/tech/blog.yml`
- **书籍配置**：`source/books/[book-name]/book.yml`
- **页面配置**：无需单独配置文件

### URL 生成规则

GitSite 自动根据目录结构生成 URL：
- 博客：`/blogs/tech/YYYY-MM-DD-title-slug/index.html`
- 书籍：`/books/book-name/XX-Chapter-Title/index.html`
- 页面：`/pages/page-name/index.html`

## Verification

创建内容后，验证构建是否成功：

```bash
# 构建网站
gitsite-cli build -o _site -v

# 或启动开发服务器预览
gitsite-cli serve
```

检查生成的 HTML 文件是否存在于 `_site/` 目录中。

## Common Pitfalls

1. **忘记创建 book.yml**：书籍目录必须有 `book.yml` 配置文件
2. **目录命名错误**：使用空格或特殊字符会导致构建失败
3. **缺少 README.md**：每个内容目录必须有 `README.md` 文件
4. **Frontmatter 格式错误**：YAML 格式必须正确，注意引号和缩进
5. **日期格式错误**：博客日期必须使用 `YYYY-MM-DD` 格式

## Resources

### scripts/manage_content.py

Python 脚本提供命令行接口用于创建各种类型的内容。支持以下命令：
- `blog` - 创建博客文章
- `book` - 创建书籍
- `chapter` - 创建书籍章节
- `page` - 创建静态页面

使用 `--help` 查看完整参数说明。

### assets/templates/

包含各类内容模板文件，可直接复制使用或作为参考：
- `blog_post.md` - 完整的博客文章模板
- `book_chapter.md` - 完整的书籍章节模板
- `page.md` - 完整的静态页面模板

模板文件使用 `{{variable}}` 占位符，使用时需要替换为实际内容。
