---
name: journal
description: Guide for using the AI's persistent journal database
license: MIT
---

# Journal

You have access to a journal, which is a SQLite database at ~/AI/journal.db . Use the `sqlite3` CLI for this.

To insert a journal entry:

```sql
insert into entries (content) values ('your journal entry');
```

You can use full-text search on the content of the entries using a query like this:

```sql
select e.id, e.created, e.updated, highlight(entries_fts, 0, '␟', '␟') as content
from entries e
	join entries_fts on (e.rowid = entries_fts.rowid)
where entries_fts.content match 'your search query'
order by bm25(entries_fts);
```

You usually don't need to know about the schema, but it's in ./schema.sql if you need it.
