---
name: building-with-sqlalchemy-orm
description: |
  Build production database layers with SQLAlchemy ORM and PostgreSQL.
  This skill should be used when teaching students to define data models, manage sessions, perform CRUD operations, and connect to PostgreSQL/Neon databases.
allowed-tools: Read, Grep, Glob, Bash
---

# Building with SQLAlchemy ORM

Build production-grade database applications with SQLAlchemy ORM 2.0+, generic PostgreSQL patterns, and Neon-specific serverless considerations.

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing models, database setup, connection patterns |
| **Conversation** | Student's specific use case (what they're building), constraints |
| **Skill References** | Domain patterns from `references/` (API docs, best practices, architecture) |
| **User Guidelines** | Project conventions, proficiency level |

Only ask student for THEIR requirements (domain expertise is embedded in this skill).

---

## Persona

You are a Python database architect with production experience building applications with SQLAlchemy ORM. You understand both the generic PostgreSQL patterns (applicable everywhere) and Neon-specific serverless considerations (autoscaling, scale-to-zero, branching). You've built multi-table applications with proper transaction handling, relationships, and connection pooling.

---

## When to Use

- **Building database models** from requirements (defining tables as Python classes)
- **Implementing CRUD operations** safely with transactions
- **Managing relationships** between tables (foreign keys, joins)
- **Querying data** with filters, ordering, and complex joins
- **Connecting to PostgreSQL** or Neon with proper configuration
- **Teaching database fundamentals** to beginners learning persistence

---

## Core Concepts

### 1. Models as Classes (ORM Abstraction)

SQLAlchemy maps Python classes to database tables:

```python
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True)
    description = Column(String(200))
    amount = Column(Float)
    category_id = Column(Integer, ForeignKey('categories.id'))
```

**Why this matters**: You write Python. SQLAlchemy generates SQL. You don't write SQL by hand.

### 2. Sessions as Transactions (Unit of Work)

A session groups database operations into an atomic transaction:

```python
with Session(engine) as session:
    new_expense = Expense(description="Groceries", amount=45.50, category_id=1)
    session.add(new_expense)
    session.commit()  # All or nothing
```

**Why this matters**: If anything fails, nothing is committed. Guarantees database consistency.

### 3. Relationships (Foreign Keys as Navigation)

Define relationships in Python instead of manual joins:

```python
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    expenses = relationship("Expense", back_populates="category")

class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True)
    category = relationship("Category", back_populates="expenses")
```

Usage:
```python
category = session.query(Category).first()
print(category.expenses)  # All expenses in this category
```

### 4. Queries (Filtering, Ordering, Joining)

Construct queries safely without writing raw SQL:

```python
# Filter: expenses > $50
expensive = session.query(Expense).filter(Expense.amount > 50).all()

# Order: sorted by amount descending
sorted_expenses = session.query(Expense).order_by(Expense.amount.desc()).all()

# Join: expenses with their categories
results = session.query(Expense, Category).join(Category).all()
```

### 5. Neon Connection Specifics

Neon is serverless PostgreSQL with auto-scaling and branching. Key differences:

- **Connection string**: `postgresql+psycopg2://user:pass@host/dbname?sslmode=require`
- **Always use SSL**: `?sslmode=require` (Neon enforces this)
- **Environment variables**: Store credentials in `.env` (never hardcode)
- **Auto-pause**: Neon pauses compute when idle—connection pools help with this

---

## Decision Logic

| Scenario | Pattern | Why |
|----------|---------|-----|
| **First database model** | Single table, one Column type | Simplest mental model before relationships |
| **Need to link data** | Use relationship() + ForeignKey | ORM handles complex joins for you |
| **Many concurrent requests** | Connection pooling with pool_size | Neon scales compute; pooling maximizes it |
| **Data consistency critical** | Transactions with try/except | Rollback on error; guarantees atomicity |
| **Want to scale to zero** | Neon serverless + pool with echo_pool | Auto-pause when idle; wake on first request |
| **Debugging queries** | Enable echo=True in engine | See generated SQL |

---

## Workflow: Building Budget Tracker

### Step 1: Define Models

```python
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import declarative_base, relationship, Session
from datetime import datetime

Base = declarative_base()

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    expenses = relationship("Expense", back_populates="category")

class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True)
    description = Column(String(200))
    amount = Column(Float)
    date = Column(DateTime, default=datetime.utcnow)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", back_populates="expenses")
```

### Step 2: Create Engine and Tables

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Connection string from environment
DATABASE_URL = os.getenv("DATABASE_URL")
# Format: postgresql+psycopg2://user:password@host/dbname?sslmode=require

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
```

### Step 3: Implement CRUD

```python
def create_expense(session, description, amount, category_id):
    """Create a new expense."""
    try:
        expense = Expense(
            description=description,
            amount=amount,
            category_id=category_id
        )
        session.add(expense)
        session.commit()
        return expense
    except Exception as e:
        session.rollback()
        print(f"Error creating expense: {e}")
        return None

def read_expenses(session, category_id=None):
    """Read expenses, optionally filtered by category."""
    query = session.query(Expense)
    if category_id:
        query = query.filter(Expense.category_id == category_id)
    return query.all()

def update_expense(session, expense_id, amount=None, description=None):
    """Update an expense."""
    expense = session.query(Expense).filter(Expense.id == expense_id).first()
    if expense:
        if amount is not None:
            expense.amount = amount
        if description is not None:
            expense.description = description
        session.commit()
        return expense
    return None

def delete_expense(session, expense_id):
    """Delete an expense."""
    expense = session.query(Expense).filter(Expense.id == expense_id).first()
    if expense:
        session.delete(expense)
        session.commit()
        return True
    return False
```

### Step 4: Query with Relationships

```python
# Get all expenses for a category
category = session.query(Category).filter_by(name="Food").first()
print(category.expenses)  # Uses relationship

# Total spent by category
totals = session.query(
    Category.name,
    func.sum(Expense.amount).label('total')
).join(Expense).group_by(Category.name).all()

for name, total in totals:
    print(f"{name}: ${total:.2f}")
```

### Step 5: Handle Transactions Safely

```python
def transfer_expense(session, expense_id, new_category_id):
    """Move expense to different category (must succeed fully or not at all)."""
    try:
        expense = session.query(Expense).filter(Expense.id == expense_id).first()
        if not expense:
            raise ValueError(f"Expense {expense_id} not found")

        expense.category_id = new_category_id
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"Transaction failed, rolled back: {e}")
        return False
```

### Step 6: Connect to Neon

**Environment file (.env)**:
```
DATABASE_URL=postgresql+psycopg2://user:password@ep-ABC123.neon.tech/dbname?sslmode=require
```

**Connection with pool configuration**:
```python
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before use
    echo=False  # Set to True for debugging
)
```

---

## MCP Integration

To connect SQLAlchemy database operations to AI agents:

```python
# Define an MCP tool that the agent can use
def query_expenses_by_category(category_name: str) -> list:
    """Agent can ask: 'How much did I spend on groceries?'"""
    with Session(engine) as session:
        return session.query(Expense).join(Category).filter(
            Category.name == category_name
        ).all()

def summarize_spending(start_date, end_date) -> dict:
    """Agent can generate reports."""
    with Session(engine) as session:
        return session.query(
            Category.name,
            func.sum(Expense.amount).label('total'),
            func.count(Expense.id).label('count')
        ).join(Expense).filter(
            Expense.date.between(start_date, end_date)
        ).group_by(Category.name).all()
```

Register these as MCP tools so the agent (Budget Manager) can use them.

---

## Safety & Guardrails

### NEVER
- ❌ Hardcode credentials in Python files
- ❌ Skip error handling around transactions
- ❌ Trust user input without validation
- ❌ Commit secrets to git
- ❌ Skip connection pooling for production

### ALWAYS
- ✅ Use environment variables for connection strings (`.env` file)
- ✅ Wrap transactions in try/except blocks with rollback
- ✅ Validate and sanitize all user input before database operations
- ✅ Use `session.commit()` explicitly (never auto-commit)
- ✅ Use `session.rollback()` on errors
- ✅ Enable `pool_pre_ping=True` to check connection health
- ✅ Use `?sslmode=require` with Neon (enforced anyway)

### Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Forgetting `session.commit()` | Changes not saved | Always call commit() or use context manager |
| Not rolling back on error | Partial data in database | Wrap in try/except with rollback() |
| Hardcoding credentials | Security breach | Use environment variables |
| No connection pooling | Neon compute scaling inefficient | Set `pool_size` parameter |
| Raw user input in queries | SQL injection | Use parameterized queries (ORM does this) |

---

## Budget Tracker Example (Complete)

See `references/budget-tracker-complete.py` for a fully working Budget Tracker application with:
- Model definitions
- Database setup
- CRUD functions
- Transaction handling
- Neon connection
- Example usage

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `ModuleNotFoundError: No module named 'sqlalchemy'` | Not installed | `pip install sqlalchemy` or `uv add sqlalchemy` |
| `ModuleNotFoundError: No module named 'psycopg2'` | PostgreSQL driver missing | `pip install psycopg2-binary` or `uv add psycopg2-binary` |
| `OperationalError: could not connect to server` | Wrong connection string or Neon offline | Check `DATABASE_URL` format, verify Neon project is running |
| `IntegrityError: duplicate key value` | Inserting duplicate unique field | Check if value already exists, use update instead |
| `ForeignKeyError: could not create foreign key` | Category doesn't exist | Create category first, or use valid category_id |
| Queries are slow | No indexes, missing relationships | Check `references/architecture.md` for indexing patterns |

---

## Resources

- **Official Docs**: https://docs.sqlalchemy.org/en/20/orm/quickstart.html
- **Neon Docs**: https://neon.com/docs/
- **PostgreSQL Types**: https://www.postgresql.org/docs/current/datatype.html
