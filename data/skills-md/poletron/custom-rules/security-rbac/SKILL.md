---
name: security-rbac
description: >
  Database Security, RBAC, and Access Control policies
  Trigger: When implementing role-based access control.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with security rbac"

## When to Use

Use this skill when:
- Implementing role-based access control
- Setting up Row Level Security (RLS)
- Protecting sensitive data
- Managing database permissions

---

## Decision Tree

```
Need access control?       → Define ROLE hierarchy
Need row isolation?        → Enable RLS with policies
Need sensitive data?       → Encrypt with pgcrypto
Need audit compliance?     → Create AUDIT_LOG table
Need secure connections?   → Enforce SSL/TLS
```

---

# Database Security & RBAC Standards

Security must be implemented at the database layer (Defense in Depth), ensuring that even if the application layer is compromised, the data remains protected by strict access controls.

## 1. Role-Based Access Control (RBAC)

### 1.1 Standard Roles
Implement a hierarchy of roles to categorize users. Avoid assigning permissions to individual users; assign them to Roles.

- **`ROLE_ADMIN`:** Full DDL/DML access. Capable of altering schema.
- **`ROLE_APP_BACKEND`:** The role used by the API. Can `SELECT`, `INSERT`, `UPDATE`, `DELETE` on operational tables but cannot alter schema.
- **`ROLE_READ_ONLY`:** For reporting/analytics tools. `SELECT` only.
- **`ROLE_GUEST` / `ROLE_ANON`:** For unauthenticated public access (if applicable).

### 1.2 Granting Permissions
- **Least Privilege:** Start with **no** permissions. Grant only what is absolutely necessary.
- **Grant Statements:**
    ```sql
    GRANT SELECT, INSERT, UPDATE ON TABLE users TO ROLE_APP_BACKEND;
    GRANT USAGE, SELECT ON SEQUENCE users_id_seq TO ROLE_APP_BACKEND;
    ```
- **Revoke:** Explicitly `REVOKE ALL` from `PUBLIC` on sensitive tables to prevent accidental default access.

## 2. Row Level Security (RLS)

Use RLS to strictly enforce data isolation at the row level based on the current user context.

### 2.1 Implementing RLS
1.  **Enable RLS:**
    ```sql
    ALTER TABLE sensitive_documents ENABLE ROW LEVEL SECURITY;
    ```
2.  **Create Policy:**
    ```sql
    CREATE POLICY user_access_policy ON sensitive_documents
    FOR ALL
    USING (owner_id = current_setting('app.current_user_id')::INT);
    ```

### 2.2 Application Context
Ensure the application sets the context variable (e.g., `app.current_user_id`) at the start of every transaction to allow RLS to function correctly.

## 3. Data Protection

### 3.1 Sensitive Data
- **Passwords:** NEVER store plain-text passwords. Use `bcrypt` or `argon2` hashes.
- **PII:** Identify Personally Identifiable Information (Emails, Phones, IDs).
    - Consider separate schemas or tables for PII with stricter access controls.
    - Encrypt highly sensitive columns (e.g., Credit Card tokens) at rest if the database supports it (e.g., `pgcrypto`).

### 3.2 SQL Injection Prevention
- **Prepared Statements:** ALL application code must use Parameterized Queries/Prepared Statements.
- **Dynamic SQL:** In PL/pgSQL, use `EXECUTE ... USING ...` to safely bind parameters in dynamic strings. Avoid simple string concatenation.

## 4. Audit & Compliance

### 4.1 Audit Logging Tables
Track sensitive operations for compliance (GDPR, SOC2, etc.).
- Log: WHO changed WHAT, WHEN, and the OLD/NEW values.
- Store in a separate `audit` schema with restricted access.

### 4.2 Immutable Logs
- Make audit tables append-only: revoke `UPDATE` and `DELETE` from all application roles.
- Consider log shipping or write-ahead log archiving for tamper-proofing.

## 5. Connection Security

### 5.1 Connection Pooling
- Application connections should use a pool (e.g., PgBouncer).
- Each pool should connect using the `ROLE_APP_BACKEND` role, not a superuser.

### 5.2 SSL/TLS
- Enforce encrypted connections: `sslmode=require` or `verify-full`.
- Ensure certificates are properly managed and rotated.
