---
name: data-engineering-storage-remote-access-integrations-duckdb
description: "Using DuckDB with remote cloud storage via HTTPFS extension, fsspec, and Delta Lake integration. Covers S3, GCS, Azure, and S3-compatible endpoints."
dependsOn: ["@data-engineering-core", "@data-engineering-storage-authentication"]
---

# DuckDB Remote Storage Integration

DuckDB provides multiple ways to access cloud storage (S3, GCS, Azure) from within the database.

## HTTPFS Extension (Native)

The HTTPFS extension enables direct queries on remote files.

```python
import duckdb
from contextlib import contextmanager

@contextmanager
def get_duckdb_connection():
    """Context manager ensures connection cleanup."""
    con = duckdb.connect()
    try:
        con.execute("INSTALL httpfs; LOAD httpfs;")
        yield con
    finally:
        con.close()

# Configure and query
with get_duckdb_connection() as con:
    # S3 configuration
    con.execute("""
        SET s3_region='us-east-1';
        SET s3_access_key_id='AKIA...';
        SET s3_secret_access_key='...';
        -- For temporary creds: SET s3_session_token='...'
        -- For S3-compatible: SET s3_endpoint='http://minio:9000';
    """)

    # Query Parquet directly
    df = con.sql("""
        SELECT category, SUM(value) as total
        FROM read_parquet('s3://bucket/data/*.parquet')
        WHERE date >= '2024-01-01'
        GROUP BY category
    """).pl()

    # Read from GCS (configure via environment or default credentials)
    df = con.sql("SELECT * FROM read_csv('gs://bucket/data.csv')").pl()
```

### Configuration via Environment Variables
Instead of hardcoding credentials, use environment variables:

```python
import os
os.environ['AWS_ACCESS_KEY_ID'] = 'AKIA...'
os.environ['AWS_SECRET_ACCESS_KEY'] = '...'
os.environ['AWS_REGION'] = 'us-east-1'

# DuckDB HTTPFS reads these automatically on first use
import duckdb
con = duckdb.connect()
con.execute("INSTALL httpfs; LOAD httpfs;")
df = con.sql("SELECT * FROM read_parquet('s3://bucket/data.parquet')").pl()
```

## Via fsspec

Register fsspec filesystems for protocols DuckDB doesn't natively support:

```python
import fsspec
import duckdb

# Register GCS (or any fsspec protocol)
duckdb.register_filesystem(fsspec.filesystem('gcs'))

# Now use gcs:// URIs natively
df = duckdb.sql("""
    SELECT * FROM read_parquet('gcs://bucket/data.parquet')
""").pl()
```

## Copy Operations

Copy data between DuckDB tables and cloud storage:

```python
import duckdb

with duckdb.connect() as con:
    # Export table to S3
    con.sql("""
        COPY (SELECT * FROM my_table)
        TO 's3://bucket/output.parquet'
        (FORMAT PARQUET)
    """)

    # Import from S3
    con.sql("""
        CREATE TABLE imported AS
        SELECT * FROM read_parquet('s3://bucket/input.parquet')
    """)
```

## Delta Lake Integration

Read Delta tables from cloud storage:

```python
import duckdb

with duckdb.connect() as con:
    con.execute("INSTALL delta; LOAD delta;")

    # Query Delta table
    df = con.sql("""
        SELECT * FROM delta_scan('s3://bucket/delta-table/')
        WHERE date >= '2024-01-01'
    """).pl()

    # Time travel (read specific version)
    df = con.sql("""
        SELECT * FROM delta_scan('s3://bucket/delta-table/', version => 5)
    """).pl()
```

## Connection Management (FIXED)

```python
# ✅ DO: Use context manager
with duckdb.connect("analytics.db") as con:
    con.sql("CREATE TABLE ...")

# ❌ DON'T: Leak connections
con = duckdb.connect("analytics.db")
con.sql("...")  # Never closed → leak

# ✅ DO: If you must, manually close
con = duckdb.connect("analytics.db")
try:
    con.sql("...")
finally:
    con.close()
```

## Authentication

See `@data-engineering-storage-authentication` for S3, GCS, Azure patterns. DuckDB HTTPFS reads standard environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, etc.) automatically.

## Performance Tips

- ✅ **Predicate pushdown**: Filter in SQL query, not after loading
- ✅ **Column pruning**: Only select needed columns
- ✅ **Parquet format**: Use Parquet (not CSV) for remote queries
- ✅ **Partitioning**: Store data partitioned (e.g., by date) for efficient queries
- ⚠️ **Row group filtering**: Parquet row groups enable scanning subsets
- ⚠️ Use `EXPLAIN` to verify pushdown: `con.sql("EXPLAIN SELECT ...").pl()`

---

## References

- [DuckDB HTTPFS Documentation](https://duckdb.org/docs/extensions/httpfs)
- [DuckDB Delta Lake Extension](https://duckdb.org/docs/extensions/delta)
- `@data-engineering-core` - DuckDB basics
