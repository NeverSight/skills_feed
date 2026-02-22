---
name: work-management
description: "Query, monitor, and analyze jobs on IBM i using SQL table functions via ibmi-mcp-server. Use when user asks about: (1) finding jobs by status, user, subsystem, or type, (2) monitoring active job performance (CPU, I/O, memory), (3) detecting long-running SQL statements, (4) analyzing lock contention, (5) checking job queues, (6) replacing WRKACTJOB, WRKUSRJOB, WRKSBSJOB, WRKSBMJOB commands, or (7) any IBM i work management task."
---

# IBM i Work Management & Job Monitoring

Query, monitor, and analyze jobs on IBM i using SQL table functions `QSYS2.JOB_INFO` and `QSYS2.ACTIVE_JOB_INFO`.

## Available Tools

The `ibmi-mcp-server` should already be connected with two available tools:
- `describe_sql_object`
- `execute_sql`

Use the `describe_sql_object` tool to get information on any IBM i Object, for example, to column information for a given table, or Function. If you need to write your own SQL statement, make sure to validate SQL objects being referenced with this tool.

Use the `execute_sql` tool to run SQL statements on the IBM i system. This tool only runs read only (`SELECT`) statements. 


## Service Selection Guide

### QSYS2.JOB_INFO
**Purpose:** Find jobs across all states (active, queued, completed)

**Use for:**
- Jobs waiting on job queues (`*JOBQ`)
- Completed jobs with output (`*OUTQ`)
- Jobs by user, submitter, or subsystem
- Job configuration and attributes
- Replacing: WRKUSRJOB, WRKSBSJOB, WRKSBMJOB

### QSYS2.ACTIVE_JOB_INFO
**Purpose:** Monitor active jobs with performance metrics

**Use for:**
- Real-time performance (CPU, I/O, memory)
- Elapsed statistics tracking (delta measurements)
- Long-running SQL statement detection
- Resource consumption analysis
- Lock contention monitoring
- SQL activity and cursor analysis
- Replacing: WRKACTJOB

## Key Capabilities

### Job Discovery & Filtering
- **By Status** - Find active, queued, or completed jobs
- **By User** - Current user, specific users, or all users
- **By Type** - Interactive, batch, system, prestart, etc.
- **By Subsystem** - QBATCH, QUSRWRK, QSYSWRK, etc.
- **By Submitter** - Jobs from current session, user, or workstation
- **By Name** - Specific job names or generic patterns

### Performance Monitoring
- **CPU Usage** - Current CPU time and elapsed CPU during interval
- **Memory** - Temporary storage, QTEMP usage, peak storage
- **I/O Activity** - Total, async, and sync disk operations
- **Lock Analysis** - Database and non-database lock waits
- **Response Time** - Interactive job response metrics

### SQL Activity Analysis
- **Active Statements** - Currently executing SQL with execution time
- **Statement Details** - SQL text, status, object information
- **Cursor Metrics** - Open, full open, pseudo open/closed counts
- **Query Engine** - CQE vs SQE cursor usage and storage
- **Connection Info** - Client IP, host, interface, port

### Resource Tracking
- **Storage Limits** - Max temporary storage and current usage
- **CPU Limits** - Maximum processing time allowed
- **Thread Info** - Active thread count and limits
- **Queue Status** - Job queue priority and position
- **Workload Groups** - Workload management group membership

## Common Use Cases

### 1. Current Job Monitoring
Get detailed information about your current connection's job

### 2. Performance Troubleshooting
- Identify top CPU consumers across subsystems
- Find jobs using excessive temporary storage
- Detect long-running SQL statements
- Analyze lock contention patterns

### 3. Queue Management
- View jobs waiting on job queues with priorities
- Track job queue status (held, released, scheduled)
- Monitor job scheduling times

### 4. User Activity Tracking
- List all jobs for specific users
- Find jobs submitted by current user or workstation
- Track active vs queued jobs by user

### 5. Storage Analysis
- Identify jobs with high QTEMP usage
- Monitor temporary storage trends
- Track peak storage consumption

### 6. SQL Performance
- Find active SQL statements and execution time
- Analyze cursor usage (CQE vs SQE)
- Monitor SQL Server Mode connections
- Track query optimizer activity

### 7. System Administration
- Get system job information (like SCPF for IPL time)
- Monitor QSQSRVR and host server jobs
- Track prestart job statistics
- Analyze workload group utilization

### 8. Elapsed Statistics
Set baseline and measure performance deltas over time intervals

### 9. Job Type Analysis
Filter by interactive, batch, prestart, or system jobs

### 10. Lock Contention
Identify jobs experiencing database and non-database lock waits

## Filter Parameters (Performance Critical)

**Always use UDTF filter parameters** (not WHERE clause) for optimal performance:

### JOB_INFO Filters
- `JOB_STATUS_FILTER` - `*ALL`, `*ACTIVE`, `*JOBQ`, `*OUTQ`
- `JOB_TYPE_FILTER` - `*ALL`, `*BATCH`, `*INTERACT`
- `JOB_SUBSYSTEM_FILTER` - Subsystem name or `*ALL`
- `JOB_USER_FILTER` - User name, `*ALL`, `*USER`, or USER special register
- `JOB_SUBMITTER_FILTER` - `*ALL`, `*JOB`, `*USER`, `*WRKSTN`
- `JOB_NAME_FILTER` - Job name or `*ALL`

### ACTIVE_JOB_INFO Filters
- `RESET_STATISTICS` - `YES`/`NO` (establish measurement baseline)
- `SUBSYSTEM_LIST_FILTER` - Comma-separated subsystems (max 25)
- `JOB_NAME_FILTER` - `*`, `*ALL`, `*CURRENT`, `*SBS`, `*SYS`, or job name
- `CURRENT_USER_LIST_FILTER` - Comma-separated users (max 10)
- `DETAILED_INFO` - `NONE`, `WORK`, `QTEMP`, `FULL`, `ALL`

## DETAILED_INFO Levels

| Level | Returns | Authorization | Use Case |
|-------|---------|---------------|----------|
| `NONE` | Basic job info | None | Quick overview |
| `WORK` | + Work management | None | Job config, queues |
| `QTEMP` | + QTEMP_SIZE | *JOBCTL | Storage analysis |
| `FULL` | All except QTEMP/HOST | Special auth for SQL cols | Complete performance data |
| `ALL` | Complete | Special auth for SQL cols | Full SQL activity detail |

**SQL Column Auth:** QIBM_DB_SQLADM or QIBM_DB_SYSMON function usage identifiers

## Essential Columns

### JOB_INFO
Job identity, status, type, subsystem, queue info, timing, completion status, configuration, regional settings, logging, output queues

### ACTIVE_JOB_INFO
Job identity, status, function, CPU usage, memory, I/O counts, elapsed statistics, SQL statement details, cursor metrics, lock waits, client connection info, QTEMP size

## CL Command Migration

| CL Command | SQL Service |
|------------|-------------|
| WRKACTJOB | ACTIVE_JOB_INFO() |
| WRKUSRJOB | JOB_INFO() + filter system jobs |
| WRKSBSJOB | JOB_INFO(JOB_SUBSYSTEM_FILTER) |
| WRKSBMJOB | JOB_INFO(JOB_SUBMITTER_FILTER) |

## Best Practices

1. **Use UDTF filters** - Always filter with parameters, not WHERE clause
2. **Start minimal** - Use DETAILED_INFO => 'NONE', add detail as needed
3. **Filter subsystems** - Specify subsystems to reduce rows scanned
4. **Measure deltas** - Use RESET_STATISTICS for elapsed metrics
5. **Exclude system jobs** - Filter JOB_TYPE <> 'SYS' for user jobs
6. **Limit results** - Use LIMIT clause on large systems
7. **Combine services** - Join with JOBLOG_INFO, PRESTART_JOB_INFO, etc.
8. **Check active SQL** - Filter SQL_STATEMENT_STATUS = 'ACTIVE' for running queries

## Quick Examples

### Get current job info
```sql
SELECT * FROM TABLE(QSYS2.ACTIVE_JOB_INFO(JOB_NAME_FILTER => '*')) X;
```

### Find top CPU consumers
```sql
SELECT JOB_NAME, AUTHORIZATION_NAME, CPU_TIME
  FROM TABLE(QSYS2.ACTIVE_JOB_INFO(SUBSYSTEM_LIST_FILTER => 'QUSRWRK,QBATCH'))
  ORDER BY CPU_TIME DESC LIMIT 10;
```

### Find jobs on job queue
```sql
SELECT * FROM TABLE(QSYS2.JOB_INFO(JOB_STATUS_FILTER => '*JOBQ')) X;
```

### Find long-running SQL statements
```sql
SELECT JOB_NAME, AUTHORIZATION_NAME,
       TIMESTAMPDIFF(2, CAST(CURRENT_TIMESTAMP - SQL_STATEMENT_START_TIMESTAMP AS CHAR(22))) AS SECONDS,
       SQL_STATEMENT_TEXT
  FROM TABLE(QSYS2.ACTIVE_JOB_INFO(DETAILED_INFO => 'ALL'))
  WHERE SQL_STATEMENT_STATUS = 'ACTIVE'
  ORDER BY SECONDS DESC;
```

### Find jobs for a specific user
```sql
SELECT * FROM TABLE(QSYS2.JOB_INFO(JOB_USER_FILTER => 'USERNAME')) X;
```

## Reference Documentation

- [JOB_INFO Reference](./references/job-info-docs.md) - Complete parameters and columns
- [ACTIVE_JOB_INFO Reference](./references/active-job-info-docs.md) - Complete parameters and columns
- [Example SQL Patterns](./references/work-management-and-jobs.sql) - Working query examples
- [IBM ACTIVE_JOB_INFO](https://www.ibm.com/support/pages/node/1128579) - Enhancement history
- [IBM JOB_INFO](https://www.ibm.com/support/pages/node/1128615) - Enhancement history

