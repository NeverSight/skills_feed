---
name: data-engineering
description: Data pipeline architecture, ETL/ELT patterns, data modeling, and production data platform design
sasmp_version: "1.3.0"
bonded_agent: 01-data-engineer
bond_type: PRIMARY_BOND
skill_version: "2.0.0"
last_updated: "2025-01"
complexity: foundational
estimated_mastery_hours: 100
prerequisites: [python-programming, sql-databases]
unlocks: [etl-tools, big-data, data-warehousing]
---

# Data Engineering Fundamentals

Core data engineering concepts, patterns, and practices for building production data platforms.

## Quick Start

```python
# Production Data Pipeline Pattern
from dataclasses import dataclass
from datetime import datetime
from typing import Generator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PipelineConfig:
    source: str
    destination: str
    batch_size: int = 10000
    retry_count: int = 3

class DataPipeline:
    """Production-ready data pipeline with error handling."""

    def __init__(self, config: PipelineConfig):
        self.config = config
        self.metrics = {"extracted": 0, "transformed": 0, "loaded": 0, "errors": 0}

    def extract(self) -> Generator[dict, None, None]:
        """Extract data in batches from source."""
        logger.info(f"Extracting from {self.config.source}")
        offset = 0
        while True:
            batch = self._fetch_batch(offset, self.config.batch_size)
            if not batch:
                break
            self.metrics["extracted"] += len(batch)
            yield batch
            offset += self.config.batch_size

    def transform(self, batch: list[dict]) -> list[dict]:
        """Apply transformations with validation."""
        transformed = []
        for record in batch:
            try:
                cleaned = self._clean_record(record)
                enriched = self._enrich_record(cleaned)
                transformed.append(enriched)
            except Exception as e:
                logger.warning(f"Transform error: {e}")
                self.metrics["errors"] += 1
        self.metrics["transformed"] += len(transformed)
        return transformed

    def load(self, batch: list[dict]) -> None:
        """Load to destination with retry logic."""
        for attempt in range(self.config.retry_count):
            try:
                self._write_batch(batch)
                self.metrics["loaded"] += len(batch)
                return
            except Exception as e:
                if attempt == self.config.retry_count - 1:
                    raise
                logger.warning(f"Load attempt {attempt + 1} failed: {e}")

    def run(self) -> dict:
        """Execute full ETL pipeline."""
        start_time = datetime.now()
        logger.info("Pipeline started")

        for batch in self.extract():
            transformed = self.transform(batch)
            if transformed:
                self.load(transformed)

        duration = (datetime.now() - start_time).total_seconds()
        self.metrics["duration_seconds"] = duration
        logger.info(f"Pipeline completed: {self.metrics}")
        return self.metrics
```

## Core Concepts

### 1. Data Architecture Patterns

```
┌─────────────────────────────────────────────────────────────────┐
│                    Modern Data Architecture                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Sources          Ingestion        Storage         Consumption  │
│  ────────         ─────────        ───────         ───────────  │
│  ┌──────┐        ┌─────────┐      ┌───────┐       ┌──────────┐ │
│  │ APIs │───────▶│ Airbyte │─────▶│ Raw   │──────▶│ BI Tools │ │
│  │ DBs  │        │ Fivetran│      │ Layer │       │ Dashboards│ │
│  │ Files│        │ Kafka   │      │ (S3)  │       └──────────┘ │
│  │ SaaS │        └─────────┘      └───┬───┘                    │
│  └──────┘                             │                         │
│                                       ▼                         │
│                               ┌───────────────┐                 │
│                               │  Transform    │                 │
│                               │  (dbt/Spark)  │                 │
│                               └───────┬───────┘                 │
│                                       │                         │
│                                       ▼                         │
│                               ┌───────────────┐   ┌──────────┐ │
│                               │   Warehouse   │──▶│ ML/AI    │ │
│                               │  (Snowflake)  │   │ Pipelines│ │
│                               └───────────────┘   └──────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2. ETL vs ELT

```python
# ETL Pattern (Transform before load)
# Best for: Sensitive data, complex transformations, limited storage

def etl_pipeline():
    raw_data = extract_from_source()
    cleaned_data = transform_and_clean(raw_data)  # Transform first
    load_to_destination(cleaned_data)

# ELT Pattern (Load then transform)
# Best for: Cloud warehouses, large scale, exploratory analysis

def elt_pipeline():
    raw_data = extract_from_source()
    load_to_staging(raw_data)  # Load raw first
    # Transform in warehouse with SQL/dbt
    run_dbt_models()
```

### 3. Data Quality Framework

```python
from dataclasses import dataclass
from typing import Callable, Any
import pandas as pd

@dataclass
class DataQualityCheck:
    name: str
    check_fn: Callable[[pd.DataFrame], bool]
    severity: str  # "error" or "warning"

class DataQualityValidator:
    def __init__(self, checks: list[DataQualityCheck]):
        self.checks = checks
        self.results = []

    def validate(self, df: pd.DataFrame) -> bool:
        all_passed = True
        for check in self.checks:
            passed = check.check_fn(df)
            self.results.append({
                "check": check.name,
                "passed": passed,
                "severity": check.severity
            })
            if not passed and check.severity == "error":
                all_passed = False
        return all_passed

# Define checks
checks = [
    DataQualityCheck(
        name="no_nulls_in_id",
        check_fn=lambda df: df["id"].notna().all(),
        severity="error"
    ),
    DataQualityCheck(
        name="positive_amounts",
        check_fn=lambda df: (df["amount"] > 0).all(),
        severity="error"
    ),
    DataQualityCheck(
        name="valid_dates",
        check_fn=lambda df: pd.to_datetime(df["date"], errors="coerce").notna().all(),
        severity="warning"
    ),
]

validator = DataQualityValidator(checks)
if not validator.validate(df):
    raise ValueError(f"Data quality checks failed: {validator.results}")
```

### 4. Idempotent Operations

```python
from datetime import date

def idempotent_load(df: pd.DataFrame, table: str, partition_date: date):
    """
    Idempotent load: can be re-run safely without duplicates.
    Uses delete-then-insert pattern.
    """
    # Delete existing data for this partition
    db.execute(f"""
        DELETE FROM {table}
        WHERE partition_date = %(date)s
    """, {"date": partition_date})

    # Insert new data
    df["partition_date"] = partition_date
    df.to_sql(table, db, if_exists="append", index=False)

# Alternative: MERGE/UPSERT pattern
def upsert_records(df: pd.DataFrame, table: str, key_columns: list[str]):
    """Upsert: Update existing, insert new."""
    temp_table = f"{table}_staging"
    df.to_sql(temp_table, db, if_exists="replace", index=False)

    key_match = " AND ".join([f"t.{k} = s.{k}" for k in key_columns])

    db.execute(f"""
        MERGE INTO {table} t
        USING {temp_table} s ON {key_match}
        WHEN MATCHED THEN UPDATE SET ...
        WHEN NOT MATCHED THEN INSERT ...
    """)
```

## Tools & Technologies

| Tool | Purpose | Version (2025) |
|------|---------|----------------|
| **Python** | Pipeline development | 3.12+ |
| **SQL** | Data transformation | - |
| **Airflow** | Orchestration | 2.8+ |
| **dbt** | SQL transformations | 1.7+ |
| **Spark** | Large-scale processing | 3.5+ |
| **Airbyte** | Data integration | 0.55+ |
| **Great Expectations** | Data quality | 0.18+ |

## Troubleshooting Guide

| Issue | Symptoms | Root Cause | Fix |
|-------|----------|------------|-----|
| **Duplicate Data** | Count mismatch | Non-idempotent load | Use MERGE, add dedup |
| **Schema Drift** | Pipeline failure | Source schema changed | Schema validation, alerts |
| **Data Freshness** | Stale data | Pipeline delays | Monitor SLAs, alerting |
| **Memory Error** | OOM in pipeline | Large batch size | Chunked processing |

## Best Practices

```python
# ✅ DO: Make pipelines idempotent
delete_and_insert(partition_date)

# ✅ DO: Add observability
logger.info(f"Processed {count} records", extra={"metric": "records_processed"})

# ✅ DO: Validate data at boundaries
validate_schema(df, expected_schema)
validate_constraints(df)

# ✅ DO: Use incremental processing
WHERE updated_at > last_run_timestamp

# ❌ DON'T: Process all data every run
# ❌ DON'T: Skip data quality checks
# ❌ DON'T: Ignore schema changes
```

## Resources

- [Data Engineering Wiki](https://dataengineering.wiki/)
- [Fundamentals of Data Engineering (Book)](https://www.oreilly.com/library/view/fundamentals-of-data/9781098108298/)
- [dbt Best Practices](https://docs.getdbt.com/guides/best-practices)

---

**Skill Certification Checklist:**
- [ ] Can design end-to-end data pipelines
- [ ] Can implement idempotent data loads
- [ ] Can set up data quality validation
- [ ] Can choose appropriate ETL vs ELT patterns
- [ ] Can monitor and troubleshoot pipelines
