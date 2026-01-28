---
name: oceanbase-formatting
description: Apply OceanBase documentation formatting standards including meta tables, notice boxes, spacing, and markdown lint compliance. Use when formatting or reviewing OceanBase documentation.
license: MIT
metadata:
  audience: technical-writers
  domain: documentation-formatting
---

# OceanBase Documentation Formatting

This skill ensures all OceanBase documentation follows consistent formatting standards and markdown lint rules.

## Meta information format

**Always use table format, NOT YAML frontmatter:**

| Description   |                 |
|---------------|-----------------|
| description   | 文档的内容描述。注意：句尾需要统一加句号。 |
| keywords      | 关键词，多个关键词之间用英文逗号隔开 |
| dir-name      | 这里填写希望在国内站文档中心目录上展示的名称 |
| dir-name-en   | 这里填写希望在海外站文档中心目录上展示的名称 |
| tenant-type   | MySQL Mode 或 Oracle Mode（两种模式均适用则不填写） |
| ddl-type      | Online DDL 或 Offline DDL（仅适用于内核 SQL 语句相关文档） |
| machine-translation | 标识机器翻译的文档（如有） |

**Important:**

- Default: Only fill description and keywords
- Fill tenant-type only when document applies to specific mode
- Do NOT delete machine-translation field if present
- All descriptions must end with period (句号)

## Notice boxes

### 说明 (Explain) - For explanations

Use for explaining complex concepts, providing background, or detailed clarifications:

<main id="notice" type='explain'>
  <h4>说明</h4>
  <p>不支持 <code>CREATE TABLE AS SELECT</code>。</p>
</main>

### 注意 (Notice) - For warnings

Use for warnings, limitations, or important alerts:

<main id="notice" type='notice'>
  <h4>注意</h4>
  <p>不支持修改关联 OCP 的 <strong>OCP 名</strong> 和 <strong>服务地址</strong>。</p>
</main>

**Formatting:**

- Use single quotes for `type` attribute: `type='explain'` or `type='notice'`
- Use `<h4>` for heading
- Use `<p>` for content
- Use `<code>` for inline code
- Use `<strong>` for emphasis

## Spacing rules

Follow these spacing requirements:

1. **Title and body**: Space between title and body text
2. **Body and code blocks**: Space between body text and code blocks
3. **Body and tables**: Space between body text and tables
4. **Sections**: Space between major sections

**Example:**

```markdown
## Syntax

```sql
ALTER SYSTEM KILL SESSION 'session_id';
```

## Parameters

```

## Markdown lint compliance

- Use proper heading hierarchy (#, ##, ###)
- Code blocks must specify language: ```sql, ```json, etc.
- Tables should have proper alignment
- Lists should use consistent formatting
- No trailing whitespace
- Proper line breaks

## Video cards

For video content:

<div role="videolist">
      <a role='video' data-code='在 boss 后台获取视频的 code' href='视频地址'>
          <img src='图标地址'/>
          填写需要在卡片里展示的文案
      </a>
      <a role='link' href='链接地址'>
          <img src='图标地址'/>
          填写需要在卡片里展示的文案
      </a>
</div>

## Download cards

For download links:

<div role="videolist">
      <a role='link' href='链接地址'>
          <img src='图标地址'/>
          填写需要在卡片里展示的文案
      </a>
</div>

**Download icon URL:**

```text
https://obbusiness-private.oss-cn-shanghai.aliyuncs.com/doc/img/download.png
```

**Notes:**

- Use `role='link'` for direct file downloads
- Each `<a>` tag represents one card
- Use the provided download icon URL for download cards

## Code block formatting

### For existing code (code references)

Use this format when referencing existing code:

```text
startLine:endLine:filepath
// code content here
```

**Requirements:**

- Include startLine and endLine (required)
- Include full filepath (required)
- Include at least 1 line of actual code
- Do NOT add language tags
- Do NOT indent triple backticks

### For new code (markdown code blocks)

Use standard markdown with language tag:

```sql
ALTER SYSTEM KILL SESSION 'session_id';
```

**Requirements:**

- Always specify language
- No line numbers
- Do NOT indent triple backticks

## Table formatting

- Include header row
- Use proper alignment
- Keep content concise
- Use code formatting for technical terms in cells

Example:

| Parameter | Description |
|-----------------|------------------------------------------------------------|
| session_id | The Client Session ID of the current session. |

## Quality checks

Before finalizing:

- [ ] Meta table format (not YAML)
- [ ] Notice boxes use correct format
- [ ] Proper spacing throughout
- [ ] Markdown lint compliant
- [ ] Code blocks have language tags
- [ ] Tables properly formatted
- [ ] No trailing whitespace
