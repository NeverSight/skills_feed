---
name: pg-sqill
description: PostgreSQL database helper. Use when writing SQL queries, exploring schema, or working with the database.
allowed-tools: Bash, Read
---

## Database

The application uses PostgreSQL. Connection string is in `DATABASE_URL` environment variable.

To query the database directly:
```bash
export $(cat .env | xargs) && psql $DATABASE_URL -c "YOUR SQL"
```

Note: Table names with uppercase letters require double quotes (e.g., `"Member"`, `"Task"`).

### Schema

```sql
-- Schema not synced. Run sync.sh in the scripts folder.
```

## Tips

- Use `LIMIT 5` when exploring data
- Check column names before writing queries
- Join tables using foreign key relationships shown in schema
