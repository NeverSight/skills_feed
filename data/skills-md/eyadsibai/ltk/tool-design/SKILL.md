---
name: tool-design
description: Use when designing agent tools, creating tool descriptions, implementing MCP tools, or asking about "tool design", "agent tools", "tool descriptions", "MCP", "function calling", "tool consolidation"
version: 1.0.0
---

# Tool Design for Agents

Tools define the contract between deterministic systems and non-deterministic agents. Poor tool design creates failure modes that no amount of prompt engineering can fix.

## The Consolidation Principle

If a human engineer cannot definitively say which tool should be used, an agent cannot do better.

**Instead of**: `list_users`, `list_events`, `create_event`
**Use**: `schedule_event` (finds availability and schedules)

## Tool Description Structure

Answer four questions:

1. **What** does the tool do?
2. **When** should it be used?
3. **What inputs** does it accept?
4. **What** does it return?

## Well-Designed Tool Example

```python
def get_customer(customer_id: str, format: str = "concise"):
    """
    Retrieve customer information by ID.

    Use when:
    - User asks about specific customer details
    - Need customer context for decision-making
    - Verifying customer identity

    Args:
        customer_id: Format "CUST-######" (e.g., "CUST-000001")
        format: "concise" for key fields, "detailed" for complete record

    Returns:
        Customer object with requested fields

    Errors:
        NOT_FOUND: Customer ID not found
        INVALID_FORMAT: ID must match CUST-###### pattern
    """
```

## Poor Tool Design (Anti-pattern)

```python
def search(query):
    """Search the database."""
    pass
```

**Problems**: Vague name, missing parameters, no return description, no usage context, no error handling.

## Architectural Reduction

Production evidence shows: fewer, primitive tools can outperform sophisticated multi-tool architectures.

**File System Agent Pattern**: Provide direct file system access instead of custom tools. Agent uses grep, cat, find to explore. Works because file systems are well-understood abstractions.

**When reduction works**:

- Data layer well-documented
- Model has sufficient reasoning
- Specialized tools were constraining
- Spending more time maintaining scaffolding than improving

## MCP Tool Naming

Always use fully qualified names:

```python
# Correct
"Use the BigQuery:bigquery_schema tool..."

# Incorrect (may fail)
"Use the bigquery_schema tool..."
```

## Response Format Optimization

```python
format: str = "concise"  # "concise" | "detailed"
```

Let agents control verbosity. Concise for confirmations, detailed when full context needed.

## Error Message Design

Design for agent recovery:

```python
{
    "error": "NOT_FOUND",
    "message": "Customer CUST-000001 not found",
    "suggestion": "Verify customer ID format (CUST-######)"
}
```

## Tool Collection Guidelines

- 10-20 tools for most applications
- Use namespacing for larger collections
- Ensure each tool has unambiguous purpose
- Test with actual agent interactions

## Anti-Patterns

- **Vague descriptions**: "Search the database"
- **Cryptic parameters**: `x`, `val`, `param1`
- **Missing error handling**: Generic errors
- **Inconsistent naming**: `id` vs `identifier` vs `customer_id`

## Best Practices

1. Write descriptions answering what, when, returns
2. Use consolidation to reduce ambiguity
3. Implement response format options
4. Design error messages for recovery
5. Establish consistent naming conventions
6. Test with actual agent interactions
7. Question if tools enable or constrain reasoning
8. Build minimal architectures for model improvements
