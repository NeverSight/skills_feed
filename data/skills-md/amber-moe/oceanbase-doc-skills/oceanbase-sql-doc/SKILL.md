---
name: oceanbase-sql-doc
description: Write and format OceanBase database SQL statement documentation following official style guidelines. Use when creating or editing SQL reference documentation for OceanBase database.
license: MIT
metadata:
  audience: technical-writers
  domain: database-documentation
---

# OceanBase SQL Documentation Skill

This skill provides guidelines for writing OceanBase database SQL statement documentation following the official documentation standards.

## When to use

Use this skill when:

- Writing SQL statement reference documentation
- Editing existing SQL documentation
- Creating examples for SQL statements
- Formatting SQL syntax documentation

## Document structure

### Meta information table

All documents must start with a meta information table (not YAML frontmatter):

| Description   |                 |
|---------------|-----------------|
| description   | 文档的内容描述。注意：句尾需要统一加句号。 |
| keywords      | 关键词，多个关键词之间用英文逗号隔开 |
| dir-name      | 这里填写希望在国内站文档中心目录上展示的名称 |
| dir-name-en   | 这里填写希望在海外站文档中心目录上展示的名称 |
| tenant-type   | MySQL Mode 或 Oracle Mode（两种模式均适用则不填写） |
| ddl-type      | Online DDL 或 Offline DDL（仅适用于内核 SQL 语句相关文档） |
| machine-translation | 标识机器翻译的文档（如有） |

**Default**: Only fill in necessary fields (description, keywords). Fill tenant-type only when applicable.

### Standard sections

1. **Purpose** - Brief description of what the statement does
2. **Syntax** - SQL syntax definition (without semicolon)
3. **Parameters** - Parameter descriptions in table format
4. **Examples** - Executable SQL examples with results
5. **References** - Links to related documentation

## Formatting rules

### Syntax section

- Syntax definitions end WITHOUT semicolons
- Syntax is for format/structure explanation, not executable statements
- Use code blocks with `sql` language tag

Example:

```sql
ALTER SYSTEM KILL SESSION 'session_id, serial#';
```

### Examples section

**SQL Statements:**

- Prefix SQL statements with `obclient>` or `obclient [SCHEMA]>` prompt
- Include semicolons in executable statements
- Place SQL statements in separate code blocks

**Query Results:**

- Place query results in separate code blocks
- Connect SQL and results with text like "查询结果如下：" or "Query results:"
- Do NOT include "Query OK" messages unless helpful
- Do NOT include "Query OK, 0 rows affected" or similar unless meaningful

**Example Format:**

```sql
obclient [KILL_USER]> SHOW PROCESSLIST;
```

查询结果如下：

```
+------------+-----------+----------------------+-----------+---------+------+--------+------------------+
| ID         | USER      | HOST                 | DB        | COMMAND | TIME | STATE  | INFO             |
+------------+-----------+----------------------+-----------+---------+------+--------+------------------+
| 3221487726 | KILL_USER | 100.xx.xxx.xxx:34803 | KILL_USER | Query   |    0 | ACTIVE | SHOW PROCESSLIST |
+------------+-----------+----------------------+-----------+---------+------+--------+------------------+
1 row in set
```

### Naming conventions

- Use meaningful names in examples (not simple names like `t1`, `tg1`)
- Table groups: `order_tg`, `product_tg`
- Tables: `order_table`, `user_info`
- Databases: Use business-meaningful names
- This helps users understand real-world application scenarios

### Notice boxes

**说明 (Explain):**

<main id="notice" type='explain'>
  <h4>说明</h4>
  <p>用于解释复杂概念、提供背景信息或详细说明。使用此格式传达重要解释性内容。</p>
</main>

**注意 (Notice):**

<main id="notice" type='notice'>
  <h4>注意</h4>
  <p>用于突出显示警告、限制或重要提示。强调用户需特别关注的信息。</p>
</main>

### Spacing rules

- Space between title and body text
- Space between body text and code blocks/tables
- Space between sections

## Quality checklist

Before finalizing documentation:

- [ ] Meta information table is properly formatted
- [ ] Syntax section has no semicolons
- [ ] Examples use `obclient>` prefix
- [ ] SQL statements and results are in separate code blocks
- [ ] Example names are meaningful and business-oriented
- [ ] Notice boxes use correct format
- [ ] Proper spacing throughout document
- [ ] No unnecessary "Query OK" messages
- [ ] All code blocks have appropriate language tags

## Common patterns

### Parameter tables

Use table format for parameters:

| Parameter | Description |
|-----------------|------------------------------------------------------------|
| session_id | The Client Session ID of the current session. This ID is the unique identifier of the session in the client. <main id="notice" type='explain'><h4>Note</h4><p>You can execute the <code>SHOW PROCESSLIST;</code> or <code>SHOW FULL PROCESSLIST</code> statement to view the <code>session_id</code>. </p></main> |

### Reference links

Format references as:

```markdown
For more information about how to query the quantity and IDs of sessions in the current database, see [View tenant sessions](../../../../../1200.database-proxy/1500.view-tenant-sessions.md).
```

## Testing against test cases

When sql_parser files and test cases differ:

- **Always follow test cases** - they reflect actual production functionality
- Test cases show what users can actually use
- Document the real, working syntax, not theoretical parser definitions
