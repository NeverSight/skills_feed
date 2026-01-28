---
name: logic-procedures
description: >
  PL/pgSQL Business Logic Procedures and Best Practices
  Trigger: When writing stored procedures or database logic.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with logic procedures"

## When to Use

Use this skill when:
- Writing PL/pgSQL stored procedures or functions
- Encapsulating business logic in the database
- Creating triggers for automated actions
- Implementing audit logging

---

## Decision Tree

```
Need return value?         → Use FUNCTION
Need transaction control?  → Use PROCEDURE
Need auto-update?          → Use TRIGGER
Need audit trail?          → Use trigger with AUDIT_LOG
Need error handling?       → Use EXCEPTION block
```

---

# PL/pgSQL & Business Logic Guidelines

Encapsulate complex business logic within the database using Stored Procedures and Functions to ensure consistency, reducing round-trips and enforcing data integrity closer to the source.

## 1. Functions vs Procedures

### 1.1 When to use a Function (`FUNCTION`)
- **Deterministic Operations:** Calculations that return a single value or a result set rooted in `READ` operations.
- **Side-effects:** Functions should mostly be side-effect free (avoid modifying data unless explicitly designed as a `VOLATILE` modifier function).
- **Naming:** `fn_verb_noun` (e.g., `fn_calculate_risk_score`).

### 1.2 When to use a Procedure (`PROCEDURE`)
- **Transaction Control:** When you need to `COMMIT` or `ROLLBACK` within the logic (only possible in Procedures).
- **Data Modification:** Orchestrating complex `INSERT`, `UPDATE`, `DELETE` workflows across multiple tables.
- **Naming:** `sp_verb_noun` (e.g., `sp_register_new_user`).

## 2. Structure & Standards

### 2.1 Standard Header & idempotent Creation
Always use `CREATE OR REPLACE` to allow easy redeployment.
Include a standard header block.

```sql
-- =============================================================================
-- PROCEDURE: Register New User
-- AUTHOR:    [Name]
-- PURPOSE:   Orchestrates user creation, profile setup, and initial logging.
-- =============================================================================
CREATE OR REPLACE PROCEDURE sp_register_new_user(
    p_email VARCHAR,
    p_password_hash VARCHAR
)
LANGUAGE plpgsql
AS $$
```

### 2.2 Parameters
- Prefix parameters with `p_` to distinguish them from internal variables (`v_`) and column names.
- Use strict typing.

### 2.3 Variable Declaration
- Declare variables in the `DECLARE` block.
- Prefix internal variables with `v_`.
- Assign default values where appropriate: `v_created_at TIMESTAMP := NOW();`

## 3. Best Practices

### 3.1 Error Handling
Use `EXCEPTION` blocks to handle errors gracefully or re-raise them with context.
Standardize error messages.

```sql
BEGIN
    -- Logic here
EXCEPTION
    WHEN unique_violation THEN
        RAISE EXCEPTION 'User with email % already exists.', p_email;
    WHEN OTHERS THEN
        RAISE NOTICE 'Unexpected error in sp_register_new_user: %', SQLERRM;
        ROLLBACK; -- If applicable
END;
```

### 3.2 Performance in Logic
- **Set-based Operations:** Prefer single SQL statements (`INSERT INTO ... SELECT ...`) over looping (`FOR r IN SELECT ... LOOP ...`) whenever possible.
- **Early Exits:** Check invalid conditions at the very start (`IF ... THEN RETURN; END IF;`) to save processing.

### 3.3 Security in Logic
- **Security Definer:** Be careful with `SECURITY DEFINER` functions; they run with the privileges of the creator. Prefer `SECURITY INVOKER` (default) unless elevation is strictly required.
- **Search Path:** Use `SET search_path = public` (or specific schema) in functions to prevent path hijacking.

## 4. Triggers

### 4.1 When to Use Triggers
- **Audit Logging:** Automatically log changes to sensitive tables.
- **Derived Data:** Update denormalized/cached columns (e.g., `updated_at`).
- **Enforcing Complex Constraints:** When CHECK constraints are insufficient.

### 4.2 Trigger Anti-Patterns
- **Cascading Triggers:** Avoid triggers that fire other triggers, creating hard-to-debug chains.
- **Heavy Logic:** Triggers should be lightweight. Offload complex logic to explicit Procedures.
- **Hidden Side Effects:** Document all triggers clearly; they execute silently.

```sql
-- Example: Auto-update `updated_at` column
CREATE OR REPLACE FUNCTION trg_fn_set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at := NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_employee_updated_at
BEFORE UPDATE ON EMPLOYEE
FOR EACH ROW EXECUTE FUNCTION trg_fn_set_updated_at();
```

## 5. Audit Logging

### 5.1 Logging Pattern
For compliance or debugging, log significant DML operations to an audit table.

```sql
CREATE TABLE AUDIT_LOG (
    id SERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    operation TEXT NOT NULL, -- INSERT, UPDATE, DELETE
    old_data JSONB,
    new_data JSONB,
    changed_by TEXT DEFAULT current_user,
    changed_at TIMESTAMP DEFAULT NOW()
);
```
