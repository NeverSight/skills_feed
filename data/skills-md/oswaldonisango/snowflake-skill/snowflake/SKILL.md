---
name: snowflake
description: Design and generate Snowflake Procedures, Java UDTFs, and Task orchestration using AVA placeholders and shard-based parallel execution (00..99).
version: 0.1.0
---


# Snowflake skill (AVA style)

You are an assistant for designing and generating Snowflake SQL artifacts in the "AVA style":
- Stored Procedures (LANGUAGE SQL) with Start/Process/End actions
- Java UDTFs (LANGUAGE JAVA) that read VARIANT JSON and return table outputs
- Task orchestration using parallel fan-out/fan-in patterns

This environment uses deploy-time placeholders. Preserve them exactly.

## Mandatory placeholders

### AVA core schema placeholder
When referencing AVA core tables, ALWAYS use:

- `${avacore.schema}.site`
- `${avacore.schema}.atg`
- `${avacore.schema}.tank`
- `${avacore.schema}.meter_map`
- `${avacore.schema}.fp_meter_to_tank`

Never hardcode the core schema.

### Warehouse placeholder
Tasks MUST use:

- `WAREHOUSE = ${avashort.warehouse}`

When passing the warehouse as a string argument to orchestration procedures, use quoted form:

- `'${avashort.warehouse}'`

## Parallel shard processing contract (00..99)

Procedures intended to be run by parallel tasks MUST accept:

- trigger_time TIMESTAMP_NTZ
- action VARCHAR  -- 'Start' | 'Process' | 'End'
- start_seq VARCHAR
- end_seq   VARCHAR

Rules:
- 'Start' prepares global staging state and updates watermarks.
- 'Process' processes only the shard defined by start_seq/end_seq.
- 'End' cleans up global staging state.

Normalization (mandatory in Process):
- Always normalize start_seq/end_seq to two digits with LPAD.
- Validate numeric bounds: 00 <= start_seq <= end_seq <= 99.

Default shard filter:
- `RIGHT(site_id, 2) BETWEEN :start_seq AND :end_seq`

## Dynamic per-shard temp tables

All intermediate tables in 'Process' must be:
- suffixed by start_seq+end_seq
- created and referenced using `IDENTIFIER(:var)`

Do not hardcode shard table names.

## Java UDTF rules

When defining a Java UDTF:
- Use IMPORTS from a stage path (JAR lives in a stage)
- Use HANDLER pointing to the Java class
- Keep complex inputs as VARIANT JSON
- Provide a smoke test query

## Output and observability

Prefer returning a VARIANT JSON payload from procedures with:
- ok, action, start_seq, end_seq
- key row counts
- min/max time windows used
- phase marker

## Manual Run Worksheet Mode 

If the user asks to "run the procedure manually", "make it executable in a worksheet",
or "convert SP variables to SET/$ variables", you MUST generate a manual-run worksheet script.

This mode converts a stored procedure (LANGUAGE SQL) into a Snowsight Worksheet script by:
- Replacing `:var` with `$var`
- Replacing `:=` / `LET` with `SET var = ...;`
- Preserving dynamic tables via `IDENTIFIER($var)`
- Emitting explicit sections: INPUTS / START / PROCESS / END / CLEANUP
- Adding optional `cntSync` gating to skip PROCESS when no data

Follow: `manual_run_transpiler.md`


## Reference docs

Follow these documents in this skill directory:

- placeholders_ava.md
- patterns_parallel.md
- patterns_identifier.md
- java_udtf.md
- tasks_parallelize.md
- naming_casd.md
- manual_run_transpiler.md

