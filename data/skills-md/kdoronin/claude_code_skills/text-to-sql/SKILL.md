---
name: text-to-sql
description: |
  Setup and use text-to-SQL capabilities for SQL databases (SQLite, PostgreSQL, MySQL, MariaDB, etc.).
  Use when: (1) User wants to query databases using natural language,
  (2) User asks to setup text-to-sql project, (3) User mentions extracting
  data from database, (4) User has .sqlite/.db file or database credentials and
  wants to work with data. This skill sets up project structure, extracts
  database schema, and enables natural language to SQL conversion.
---

# Text-to-SQL Skill

Convert natural language questions into SQL queries and execute them against SQL databases.

## Phase 1: Project Setup

### Step 1: Ask about database connection

Ask user which database type they want to use:

**Option A: SQLite** (file-based, no credentials needed)
- User provides path to `.sqlite` or `.db` file
- Or places file in `database/` folder

**Option B: Server database** (PostgreSQL, MySQL, MariaDB, etc.)
- User creates `.env` file with connection details
- Supported: PostgreSQL, MySQL, MariaDB, and other SQL databases

### Step 2: Initialize project structure

Run the init script OR manually create structure:

**Option A: Use init script**
```bash
python scripts/init_project.py --target /path/to/project
```

**Option B: Manual setup**
```bash
mkdir -p database output/queries output/reports
```

Copy from skill folders to project root:
- `scripts/*.py` → project root (db_extractor.py, query_runner.py, list_databases.py, sql_helper.py)
- `assets/example.env` → project root
- `assets/requirements.txt` → project root
- `assets/.gitignore` → project root

Install dependencies:
```bash
pip install -r requirements.txt
```

### Step 3: Configure connection

**For SQLite:**
```bash
# Place database file
cp /path/to/database.sqlite database/

# Extract schema
python db_extractor.py --sqlite database/YOUR_DB.sqlite
```

**For server databases (PostgreSQL, MySQL, etc.):**

Copy and edit the template:
```bash
cp example.env .env
# Edit .env with actual credentials
```

The `example.env` template contains:
```env
DB_TYPE=postgresql  # postgresql, mysql, mariadb
DB_HOST=localhost
DB_PORT=5432        # 5432 for PostgreSQL, 3306 for MySQL
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_database_name
```

Then extract schema:
```bash
python db_extractor.py --database your_database_name
```

### Step 4: Verify setup

After extraction, these files should exist in `output/`:
- `connection.json` - current connection config
- `text_to_sql_context.md` - schema for LLM queries
- `schema_info.json` - full schema data
- `database_documentation.md` - human-readable docs

---

## Phase 2: Query Workflow

When user asks a data question:

### Step 1: Read schema context

Read `output/text_to_sql_context.md` to understand:
- Available tables and columns
- Data types and relationships
- Enum values for filtering

### Step 2: Generate and save SQL

Create SQL file based on user question. See [sql_patterns.md](references/sql_patterns.md) for common query patterns.

```bash
# Save to output/queries/descriptive_name.sql
```

### Step 3: Execute query

Get run command from `output/connection.json`, then:

```bash
# SQLite example
python query_runner.py --sqlite database/DB.sqlite -f output/queries/query.sql -o result.csv

# MySQL example
python query_runner.py -f output/queries/query.sql -o result.csv
```

### Step 4: Report results

Tell user: "Results saved to `output/reports/result.csv`"

---

## Quick Reference

### Commands

```bash
# List databases
python list_databases.py

# Extract schema (SQLite)
python db_extractor.py --sqlite database/file.sqlite

# Extract schema (MySQL)
python db_extractor.py --database db_name

# Run query (SQLite)
python query_runner.py --sqlite database/file.sqlite "SELECT * FROM table LIMIT 10"
python query_runner.py --sqlite database/file.sqlite -f query.sql -o result.csv

# Run query (MySQL)
python query_runner.py "SELECT * FROM table LIMIT 10"
python query_runner.py -f query.sql -o result.csv

# Output formats
--format csv   # default
--format xlsx  # Excel
--format json  # JSON
--format md    # Markdown
```

### Project Structure

```
project/
├── .env                    # MySQL credentials (if using MySQL)
├── database/               # SQLite files go here
│   └── your_db.sqlite
├── output/
│   ├── connection.json     # Current DB connection
│   ├── text_to_sql_context.md  # Schema for LLM
│   ├── queries/            # Saved SQL queries
│   └── reports/            # Query results (CSV, XLSX, JSON)
├── db_extractor.py
├── query_runner.py
├── list_databases.py
└── sql_helper.py
```

---

## Example Workflow

**User:** "I have a SQLite database with e-commerce data. Help me analyze it."

**Setup:**
1. Ask user for SQLite file path
2. Copy file to `database/`
3. Run `python db_extractor.py --sqlite database/file.sqlite`
4. Read generated `output/text_to_sql_context.md`

**User:** "Show me top 10 sellers by revenue"

**Query:**
1. Read schema from `output/text_to_sql_context.md`
2. Generate SQL:
   ```sql
   SELECT seller_id, SUM(price) as revenue
   FROM order_items
   GROUP BY seller_id
   ORDER BY revenue DESC
   LIMIT 10;
   ```
3. Save to `output/queries/top_sellers.sql`
4. Execute: `python query_runner.py --sqlite database/file.sqlite -f output/queries/top_sellers.sql -o top_sellers.csv`
5. Report: "Results saved to `output/reports/top_sellers.csv`"
