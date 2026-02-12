---
name: greptimedb-pipeline
description: Guide for creating GreptimeDB Pipeline, by which user can add a process layer to GreptimeDB between ingestion and storage, to transform data.
---

# GreptimeDB Pipeline Guide

Create GreptimeDB pipeline definition to transform data into specific structured
table, including data extraction, processing, type parsing, datetime handling
and more.

## The workflow

To create GreptimeDB pipeline, we should follow these phases:

### Phase 1. Understanding GreptimeDB Pipeline

First, we should read greptimedb pipeline definitions and how it works from
GreptimeDB's documentation.

There are pages available, use WebFetch to load and understand them:

1. High level information of how to use custom pipeline
   https://docs.greptime.com/user-guide/logs/use-custom-pipelines/
2. Details about pipeline elements and docs for each processor, transform and
   dispatcher
   https://docs.greptime.com/reference/pipeline/pipeline-config/

We will always create version 2 pipeline.

### Phase 2. Create an initial pipeline that works

Ask user to provide a sample input data. It can be one of:

1. text data line
2. ndjson data line
3. an array of json data

And try to understand what type of information that user want to extract from
the sample data.

For text data line, we should try to split it by any potential field separator
like space or tab. Find out the datetime part and use `date` processor to parse
it. Try to name each field by its meaning. If it's impossible to understand the
text line, we try to use a field called `message` for all the line.

For ndjson and json, we will find out a datetime field and use `date` processor
on it to generate the time index. And we will use json key for all other fields.

Provide user a sample of how the initial pipeline definition will look like, as
well as how the parsed data to be like. We can use a markdown table to show each
field name, data type in greptimedb and values:

| Field name 1 (Data type) | Field name 2 (Data type) | ... |
|--------------------------|--------------------------|-----|
| Value 1                  | Value 2                  | ... |
| Value 1                  | Value 2                  | ... |

### Phase 3. Work on special requirements and verify

The user may have more requirements on particular field, use processor to
address them.

If the user want to dispatch data into multiple tables, or using different
pipeline to process, there is `dispatch` available to handle this. User can
provide table suffix for dispatched data.

If the user requirements are complex enough for declarative processors, there is
also an advanced VRL processor for remapping data. Check reference for more
information.

If the greptimedb-mcp-server is available, there is a `dryrun-pipeline` tool by
which we can provide pipeline definition and sample data to test against
GreptimeDB's implementation. The output is a table encoded as json.

### Phase 4. Check index and table options

The Pipeline system also allow user to specify various index on the result
table. We will understand how user will query the table and provide suggestion
on index.

Advanced table options can be customized by `.greptime_` variables. Use them if
user want to customize TTL, append_mode and etc.

## Reference

1. GreptimeDB Index Options:
   https://docs.greptime.com/user-guide/manage-data/data-index/
1. VRL, the advanced processing language from Vector:
   https://vector.dev/docs/reference/vrl/
1. Using Table Options from Pipeline/VRL:
   https://docs.greptime.com/reference/pipeline/write-log-api/#set-table-options
