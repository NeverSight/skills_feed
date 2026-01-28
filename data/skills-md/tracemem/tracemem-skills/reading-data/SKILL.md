---
name: reading-data
description: Instructions for reading data from TraceMem memory.
---

# Skill: TraceMem Reading Data (Data Products)

## Purpose
This skill teaches how to safely and correctly read data using TraceMem Data Products. Direct database selection or API calls are prohibited; all data access must be mediated by TraceMem.

## When to Use
- When you need to retrieve information (database rows, API results, resource state).
- When you need to search or query for specific records.

## When NOT to Use
- Do not use for writing data (use `decision_write` / `insert` product).
- Do not try to use standard SQL libraries or HTTP clients for governed data.

## Core Rules
- **Data Products Only**: You must access data via a named "Data Product".
- **Operation Specificity**: A Data Product usually supports only ONE operation. Use a "read" product (e.g., `customers_read`) for reading.
- **Purpose is Mandatory**: You must declare a `purpose` string for every read. This purpose must be in the product's `allowed_purposes` list.
- **Least Privilege**: Only request the data you strictly need.

## Correct Usage Pattern

1. **Identify the Product**:
   Use `products_list` to find the correct Data Product for your need (e.g., `orders_read_v1`). Check its schema and `allowed_purposes`.

2. **Execute Read**:
   Call `decision_read` with:
   - `decision_id`: Your current open decision.
   - `product`: The name of the data product.
   - `purpose`: A valid purpose string (e.g., `verification`).
   - `query`: The key-value filter (e.g., `{"user_id": "123"}`).

3. **Handle Results**:
   The response contains `records` (list) and `summary`.
   
   *Example*:
   ```json
   {
     "records": [{"id": 1, "status": "active"}],
     "summary": {"rows": 1}
   }
   ```

## Common Mistakes
- **Implicit Purpose**: Failing to provide a purpose or guessing one not in the allowed list.
- **Wrong Product**: Trying to read from a product designed for `insert`.
- **Unbounded Queries**: Querying without filters (TraceMem may limit result sets by default).

## Safety Notes
- **Audit Trails**: Your query parameters and the summary of what you read are recorded in the immutable trace.
- **Sensitive Data**: Avoid putting PII in the *query* parameters if possible, unless the Data Product is explicitly designed for PII lookups.
- **Read-Before-Write**: Always read the current state of an object before attempting to modify it, to ensure your decision is based on fresh data.
