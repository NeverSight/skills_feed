---
name: data-engineering-quality
description: "Data quality testing and validation with Great Expectations and Pandera. Schema validation, data quality tests, profiling, and automated validation in pipelines."
dependsOn: ["@data-engineering-core"]
---

# Data Quality and Testing

Data validation and testing frameworks for ensuring pipeline correctness and data quality: Great Expectations (enterprise) and Pandera (lightweight). Integrates with orchestration tools for automated validation.

## Quick Comparison

| Feature | Great Expectations | Pandera |
|---------|-------------------|---------|
| **Approach** | Declarative "expectations" | Schema definitions with checks |
| **DataFrame Support** | Pandas, Spark, SQL, BigQuery | Pandas, Polars, PySpark, Dask |
| **Validation Output** | JSON results with detailed diagnostics | Boolean or exception |
| **Best For** | Enterprise data platforms, comprehensive profiling | Python-centric pipelines, lightweight |
| **Learning Curve** | Steeper (concepts: DataContext, Checkpoints) | Lower (Python decorators/classes) |
| **Integration** | CI/CD, Airflow, Prefect, Dagster | pytest, FastAPI, any Python code |

## When to Use Which?

- **Great Expectations**: You need comprehensive data documentation (data docs), profiling, and validation with rich reporting. Organizations with dedicated data quality teams.

- **Pandera**: You're already in Python/Pandas/Polars ecosystem and want simple schema validation with type hints. Quick checks in ETL scripts or API responses.

## Skill Dependencies

- `@data-engineering-core` - Polars, DuckDB, Pandas basics
- `@data-engineering-orchestration` - Integrate validation into workflows

---

## Great Expectations (GX)

### Installation
```bash
pip install great_expectations
# For specific backends
pip install "great_expectations[spark]"
```

### Quickstart
```python
import great_expectations as gx
import pandas as pd

# Initialize context (creates gx/ directory if first time)
context = gx.get_context()

# Create expectation suite
context.create_expectation_suite("my_suite")

# Get validator
validator = context.get_validator(
    batch_request={
        "datasource_name": "pandas",
        "data_asset_name": "my_data",
    },
    expectation_suite_name="my_suite"
)

# Define expectations
validator.expect_column_values_to_not_be_null("id")
validator.expect_column_values_to_be_between("value", min_value=0, max_value=1000)
validator.expect_column_values_to_be_in_set("category", value_set=["A", "B", "C"])
validator.expect_column_values_to_match_strftime_format("date", strftime_format="%Y-%m-%d")

# Validate
result = validator.validate()
print(f"Success: {result.success}")
if not result.success:
    print(f"Failed expectations: {result.results}")
```

### Data Sources & Connectors
```yaml
# gx/contexts/<context>/datasources/pandas_datasource.yml
datasources:
  pandas_datasource:
    class_name: Datasource
    module_name: great_expectations.datasource
    execution_engine:
      module_name: great_expectations.execution_engine
      class_name: PandasExecutionEngine
    data_connectors:
      default_runtime_data_connector_name:
        class_name: RuntimeDataConnector
        batch_identifiers:
          - runtime_batch_identifier_name
```

### Checkpoints (Validation Automation)
```python
# Create checkpoint
checkpoint_config = {
    "name": "my_checkpoint",
    "config_version": 1.0,
    "class_name": "SimpleCheckpoint",
    "validations": [
        {
            "batch_request": {
                "datasource_name": "pandas",
                "data_connector_name": "default_runtime_data_connector_name",
                "data_asset_name": "my_data",
            },
            "expectation_suite_name": "my_suite"
        }
    ]
}

context.add_checkpoint(**checkpoint_config)

# Run checkpoint
results = context.run_checkpoint(checkpoint_name="my_checkpoint")
```

### Integration with Orchestrators

**Prefect**:
```python
from prefect import flow, task
import great_expectations as gx

@task
def validate_data(df: pd.DataFrame, suite_name: str) -> bool:
    context = gx.get_context()
    validator = context.get_validator(
        batch_request={
            "datasource_name": "pandas",
            "data_asset_name": "validation_data"
        },
        expectation_suite_name=suite_name
    )
    validator.add_batch(df, batch_identifier="batch_1")
    result = validator.validate()
    return result.success

@flow
def pipeline_with_validation():
    df = extract()
    if validate_data(df, "my_suite"):
        transformed = transform(df)
        load(transformed)
    else:
        raise ValueError("Data validation failed")
```

**Dagster**:
```python
from dagster import asset
import great_expectations as gx

@asset
def validated_asset(df: pd.DataFrame) -> pd.DataFrame:
    context = gx.get_context()
    validator = context.add_or_edit_expectation_suite("asset_suite")
    # ... define expectations

    validator.add_batch(df)
    result = validator.validate()
    if not result.success:
        raise Exception(f"Validation failed: {result}")
    return df
```

---

## Pandera: Lightweight Schema Validation

### Installation
```bash
pip install pandera[pandas]     # For pandas
pip install pandera[polars]     # For Polars
pip install pandera[pyspark]    # For PySpark
```

### Basic Usage
```python
import pandera as pa
import pandas as pd

# Define schema
schema = pa.DataFrameSchema({
    "id": pa.Column(pa.Int, checks=pa.Check.gt(0)),
    "category": pa.Column(pa.String, checks=pa.Check.isin(["A", "B", "C"])),
    "value": pa.Column(pa.Float, checks=[
        pa.Check.gt(0),
        pa.Check.lt(10000)
    ]),
    "date": pa.Column(pa.DateTime)
})

# Validate DataFrame
df = pd.DataFrame({
    "id": [1, 2, 3],
    "category": ["A", "B", "A"],
    "value": [100.0, 200.0, 150.0],
    "date": pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"])
})

validated = schema.validate(df)  # Raises SchemaError if invalid
print("Validation passed!")

# Decorator pattern
@schema.validate
def process_data(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("category")["value"].sum().reset_index()
```

### Custom Checks
```python
# Custom validation function
def custom_check(series: pd.Series) -> bool:
    return (series > 0).all()

schema = pa.DataFrameSchema({
    "value": pa.Column(pa.Float, checks=custom_check)
})

# Or lambda
schema = pa.DataFrameSchema({
    "value": pa.Column(pa.Float, checks=pa.Check(lambda x: x > 0))
})
```

### Polars Integration
```python
import pandera.polars as pa
import polars as pl

schema = pa.DataFrameSchema({
    "id": pa.Column(pl.Int64, pa.Check.gt(0)),
    "value": pa.Column(pa.Float64, pa.Check.in_range(0, 1000))
})

df = pl.DataFrame({"id": [1, 2], "value": [100.0, 200.0]})
validated = schema.validate(df)
```

---

## Best Practices

1. ✅ **Validate early** - Check data quality immediately after extraction
2. ✅ **Fail fast** - Stop pipeline on validation failure (or route to quarantine)
3. ✅ **Version your schemas** - Store schema definitions in version control
4. ✅ **Use both static and runtime checks** - Static schema + dynamic checks (ranges, uniqueness)
5. ✅ **Integrate with orchestration** - Use Prefect/Dagster task dependencies for validation steps
6. ❌ **Don't** validate only at the end - catch issues early
7. ❌ **Don't** use `try/except` to ignore validation errors (unless intentional quarantine)

## Testing Patterns

### pytest Integration
```python
import pytest
import pandas as pd
import pandera as pa

schema = pa.DataFrameSchema({
    "id": pa.Column(pa.Int, pa.Check.gt(0)),
    "value": pa.Column(pa.Float)
})

def test_transformation_output():
    df = transform_function(source_df)
    schema.validate(df)  # Will raise if invalid

@pytest.fixture
def sample_data():
    return pd.DataFrame({"id": [1, 2], "value": [10.0, 20.0]})

def test_pipeline(sample_data):
    result = pipeline.run(sample_data)
    assert len(result) > 0
```

---

## References

- [Great Expectations Documentation](https://docs.greatexpectations.io/)
- [Pandera Documentation](https://pandera.pydata.org/)
- [pandera-polars](https://pandera.pydata.org/pandera-polars-docs/)
- `@data-engineering-core` - Pipeline patterns with validation
