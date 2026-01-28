---
name: big-data
description: Apache Spark, Hadoop, distributed computing, and large-scale data processing for petabyte-scale workloads
sasmp_version: "1.3.0"
bonded_agent: 01-data-engineer
bond_type: PRIMARY_BOND
skill_version: "2.0.0"
last_updated: "2025-01"
complexity: advanced
estimated_mastery_hours: 160
prerequisites: [python-programming, sql-databases]
unlocks: [data-warehousing, mlops, machine-learning]
---

# Big Data & Distributed Computing

Production-grade big data processing with Apache Spark, distributed systems patterns, and petabyte-scale data engineering.

## Quick Start

```python
# PySpark 3.5+ modern DataFrame API
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Initialize Spark with optimal settings
spark = (SparkSession.builder
    .appName("ProductionETL")
    .config("spark.sql.adaptive.enabled", "true")
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
    .getOrCreate())

# Efficient data loading with schema enforcement
from pyspark.sql.types import StructType, StructField, StringType, LongType, TimestampType

schema = StructType([
    StructField("event_id", StringType(), False),
    StructField("user_id", LongType(), False),
    StructField("event_type", StringType(), False),
    StructField("timestamp", TimestampType(), False),
    StructField("properties", StringType(), True)
])

df = (spark.read
    .schema(schema)
    .parquet("s3://bucket/events/")
    .filter(F.col("timestamp") >= F.current_date() - 30))

# Complex aggregation with window functions
window_spec = Window.partitionBy("user_id").orderBy("timestamp")

result = (df
    .withColumn("event_rank", F.row_number().over(window_spec))
    .withColumn("session_id", F.sum(
        F.when(
            F.col("timestamp") - F.lag("timestamp").over(window_spec) > F.expr("INTERVAL 30 MINUTES"),
            1
        ).otherwise(0)
    ).over(window_spec))
    .groupBy("user_id", "session_id")
    .agg(
        F.count("*").alias("event_count"),
        F.min("timestamp").alias("session_start"),
        F.max("timestamp").alias("session_end")
    ))

result.write.mode("overwrite").parquet("s3://bucket/sessions/")
```

## Core Concepts

### 1. Spark Architecture Deep Dive

```
┌─────────────────────────────────────────────────────────┐
│                    Driver Program                        │
│  ┌─────────────────────────────────────────────────┐   │
│  │              SparkContext/SparkSession           │   │
│  │  - Creates execution plan (DAG)                  │   │
│  │  - Coordinates with Cluster Manager              │   │
│  │  - Schedules tasks                               │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              Cluster Manager (YARN/K8s/Standalone)      │
└─────────────────────────────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │ Executor │    │ Executor │    │ Executor │
    │ ┌──────┐ │    │ ┌──────┐ │    │ ┌──────┐ │
    │ │Task 1│ │    │ │Task 2│ │    │ │Task 3│ │
    │ │Task 4│ │    │ │Task 5│ │    │ │Task 6│ │
    │ └──────┘ │    │ └──────┘ │    │ └──────┘ │
    │  Cache   │    │  Cache   │    │  Cache   │
    └──────────┘    └──────────┘    └──────────┘
```

### 2. Partition Optimization

```python
from pyspark.sql import functions as F

# Check current partitioning
print(f"Partitions: {df.rdd.getNumPartitions()}")

# Rule of thumb: 128MB per partition, 2-4 partitions per core
# For 100GB data on 10 executors with 4 cores each:
# 100GB / 128MB ≈ 800 partitions, or 40 cores * 4 = 160 partitions
# Use: 200-400 partitions

# Repartition by key (for joins)
df_repartitioned = df.repartition(200, "user_id")

# Coalesce (reduce partitions without shuffle)
df_coalesced = df.coalesce(100)

# Optimal write partitioning
df.repartition(F.year("date"), F.month("date")) \
  .write \
  .partitionBy("year", "month") \
  .mode("overwrite") \
  .parquet("s3://bucket/output/")

# Bucketing for repeated joins
df.write \
  .bucketBy(256, "user_id") \
  .sortBy("user_id") \
  .saveAsTable("bucketed_events")
```

### 3. Join Optimization Strategies

```python
from pyspark.sql import functions as F

# Broadcast join (small table < 10MB default, configurable to 100MB)
small_df = spark.read.parquet("s3://bucket/dim_product/")  # 5MB
large_df = spark.read.parquet("s3://bucket/fact_sales/")   # 500GB

# Explicit broadcast hint
from pyspark.sql.functions import broadcast
result = large_df.join(broadcast(small_df), "product_id")

# Increase broadcast threshold
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 100 * 1024 * 1024)  # 100MB

# Sort-Merge Join (for large tables)
# Both tables sorted and partitioned by join key
users = spark.read.parquet("users/").repartition(200, "user_id").sortWithinPartitions("user_id")
orders = spark.read.parquet("orders/").repartition(200, "user_id").sortWithinPartitions("user_id")
result = users.join(orders, "user_id")

# Skewed join handling (salting technique)
# If user_id has skew (some users have millions of rows)
salt_range = 10
salted_users = (users
    .withColumn("salt", F.explode(F.array([F.lit(i) for i in range(salt_range)])))
    .withColumn("salted_key", F.concat("user_id", F.lit("_"), "salt")))

salted_orders = (orders
    .withColumn("salt", (F.rand() * salt_range).cast("int"))
    .withColumn("salted_key", F.concat("user_id", F.lit("_"), "salt")))

result = salted_users.join(salted_orders, "salted_key").drop("salt", "salted_key")
```

### 4. Caching & Persistence

```python
from pyspark import StorageLevel

# Caching strategies
df.cache()  # MEMORY_AND_DISK by default in Spark 3.x
df.persist(StorageLevel.MEMORY_ONLY)  # Fastest, may recompute if evicted
df.persist(StorageLevel.MEMORY_AND_DISK_SER)  # Compressed, slower but less memory
df.persist(StorageLevel.DISK_ONLY)  # For very large intermediate datasets

# When to cache:
# - Reused DataFrames (used in multiple actions)
# - After expensive transformations (joins, aggregations)
# - Before iterative algorithms

# Cache usage pattern
expensive_df = (spark.read.parquet("s3://bucket/large/")
    .filter(F.col("status") == "active")
    .join(broadcast(dim_df), "dim_key")
    .groupBy("category")
    .agg(F.sum("amount").alias("total")))

expensive_df.cache()
expensive_df.count()  # Materialize cache

# Use cached DataFrame multiple times
top_categories = expensive_df.orderBy(F.desc("total")).limit(10)
summary = expensive_df.agg(F.avg("total"), F.max("total"))

# Release cache when done
expensive_df.unpersist()
```

### 5. Structured Streaming

```python
from pyspark.sql import functions as F
from pyspark.sql.types import *

# Read from Kafka
kafka_df = (spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "broker1:9092,broker2:9092")
    .option("subscribe", "events")
    .option("startingOffsets", "latest")
    .option("maxOffsetsPerTrigger", 100000)
    .load())

# Parse JSON payload
event_schema = StructType([
    StructField("event_id", StringType()),
    StructField("user_id", LongType()),
    StructField("event_type", StringType()),
    StructField("timestamp", TimestampType())
])

parsed_df = (kafka_df
    .select(F.from_json(F.col("value").cast("string"), event_schema).alias("data"))
    .select("data.*")
    .withWatermark("timestamp", "10 minutes"))

# Windowed aggregation
windowed_counts = (parsed_df
    .groupBy(
        F.window("timestamp", "5 minutes", "1 minute"),
        "event_type"
    )
    .count())

# Write to Delta Lake with checkpointing
query = (windowed_counts.writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "s3://bucket/checkpoints/events/")
    .trigger(processingTime="1 minute")
    .start("s3://bucket/streaming_output/"))

# Monitor stream
query.awaitTermination()
```

## Tools & Technologies

| Tool | Purpose | Version (2025) |
|------|---------|----------------|
| **Apache Spark** | Distributed processing | 3.5+ |
| **Delta Lake** | ACID transactions | 3.0+ |
| **Apache Iceberg** | Table format | 1.4+ |
| **Apache Flink** | Stream processing | 1.18+ |
| **Databricks** | Managed Spark platform | Latest |
| **AWS EMR** | Managed Hadoop/Spark | 7.0+ |
| **Trino** | Interactive queries | 400+ |
| **dbt** | Transform layer | 1.7+ |

## Learning Path

### Phase 1: Foundations (Weeks 1-3)
```
Week 1: Distributed computing concepts, MapReduce
Week 2: Spark architecture, RDDs, DataFrames
Week 3: Spark SQL, basic transformations
```

### Phase 2: Intermediate (Weeks 4-6)
```
Week 4: Joins, aggregations, window functions
Week 5: Partitioning, bucketing, caching
Week 6: Performance tuning, Spark UI analysis
```

### Phase 3: Advanced (Weeks 7-10)
```
Week 7: Structured Streaming
Week 8: Delta Lake / Iceberg table formats
Week 9: Cluster sizing, cost optimization
Week 10: Advanced optimizations (AQE, skew handling)
```

### Phase 4: Production (Weeks 11-14)
```
Week 11: Deployment on EMR/Databricks
Week 12: Monitoring, alerting, debugging
Week 13: CI/CD for Spark jobs
Week 14: Multi-cluster architectures
```

## Production Patterns

### Delta Lake UPSERT (Merge)

```python
from delta.tables import DeltaTable

# Incremental UPSERT pattern
delta_table = DeltaTable.forPath(spark, "s3://bucket/users/")
updates_df = spark.read.parquet("s3://bucket/updates/")

delta_table.alias("target").merge(
    updates_df.alias("source"),
    "target.user_id = source.user_id"
).whenMatchedUpdate(set={
    "email": "source.email",
    "updated_at": "source.updated_at"
}).whenNotMatchedInsertAll().execute()

# Optimize after merge
delta_table.optimize().executeCompaction()
delta_table.vacuum(retentionHours=168)  # 7 days
```

### Cost-Effective Cluster Configuration

```python
# spark-submit configuration for 1TB processing job
"""
spark-submit \
    --master yarn \
    --deploy-mode cluster \
    --num-executors 50 \
    --executor-cores 4 \
    --executor-memory 16g \
    --driver-memory 8g \
    --conf spark.sql.adaptive.enabled=true \
    --conf spark.sql.adaptive.coalescePartitions.enabled=true \
    --conf spark.sql.shuffle.partitions=400 \
    --conf spark.dynamicAllocation.enabled=true \
    --conf spark.dynamicAllocation.minExecutors=10 \
    --conf spark.dynamicAllocation.maxExecutors=100 \
    --conf spark.speculation=true \
    job.py
"""

# Sizing guidelines:
# - Executor memory: 16-32GB (avoid GC overhead)
# - Executor cores: 4-5 (parallelism per executor)
# - Total cores: 2-4x data size in GB
# - Partitions: 2-4x total cores
```

## Troubleshooting Guide

### Common Failure Modes

| Issue | Symptoms | Root Cause | Fix |
|-------|----------|------------|-----|
| **OOM Error** | "Container killed by YARN" | Too much data per partition | Increase partitions, reduce broadcast |
| **Shuffle Spill** | Slow stage, disk I/O | Insufficient memory | Increase `spark.memory.fraction` |
| **Skewed Tasks** | One task much slower | Data skew on key | Use salting, AQE skew handling |
| **GC Overhead** | "GC overhead limit exceeded" | Too many small objects | Use Kryo serialization, reduce UDFs |
| **Driver OOM** | Driver crash | collect(), large broadcast | Avoid collect, stream results |

### Debug Checklist

```python
# 1. Check Spark UI (port 4040/18080)
# - Stages: Look for skewed tasks (max >> median)
# - Storage: Check cached data size
# - Environment: Verify configuration

# 2. Analyze execution plan
df.explain(mode="extended")

# 3. Check partition distribution
df.groupBy(F.spark_partition_id()).count().show()

# 4. Profile data skew
df.groupBy("key_column").count().orderBy(F.desc("count")).show(20)

# 5. Monitor job metrics
spark.sparkContext.setLogLevel("WARN")

# 6. Enable detailed metrics
spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
spark.conf.set("spark.eventLog.enabled", "true")
```

### Reading Spark UI

```
Stage Analysis:
├── Duration: Total time for stage
├── Tasks: Number of parallel tasks
│   ├── Median: Typical task duration
│   ├── Max: Slowest task (check for skew)
│   └── Failed: Retry count
├── Input: Data read
├── Shuffle Read: Data from other stages
├── Shuffle Write: Data for downstream stages
└── Spill: Disk spill (indicates memory pressure)

Key Metrics:
├── GC Time > 10%: Memory issue
├── Shuffle Write > Input: Exploding join
├── Max/Median > 2x: Data skew
└── Spill > 0: Increase partitions or memory
```

## Unit Test Template

```python
import pytest
from pyspark.sql import SparkSession
from chispa.dataframe_comparer import assert_df_equality
import pyspark.sql.functions as F

@pytest.fixture(scope="session")
def spark():
    """Session-scoped Spark for tests."""
    return (SparkSession.builder
        .master("local[2]")
        .appName("UnitTests")
        .config("spark.sql.shuffle.partitions", 2)
        .getOrCreate())

@pytest.fixture
def sample_data(spark):
    return spark.createDataFrame([
        (1, "user1", 100.0),
        (2, "user2", 200.0),
        (3, "user1", 150.0),
    ], ["id", "user_id", "amount"])

class TestAggregations:

    def test_user_totals(self, spark, sample_data):
        # Arrange
        expected = spark.createDataFrame([
            ("user1", 250.0),
            ("user2", 200.0),
        ], ["user_id", "total"])

        # Act
        result = sample_data.groupBy("user_id").agg(
            F.sum("amount").alias("total")
        )

        # Assert
        assert_df_equality(result, expected, ignore_row_order=True)

    def test_handles_empty_dataframe(self, spark):
        # Arrange
        empty_df = spark.createDataFrame([], "id INT, amount DOUBLE")

        # Act
        result = empty_df.agg(F.sum("amount").alias("total")).collect()

        # Assert
        assert result[0]["total"] is None

    def test_window_functions(self, spark, sample_data):
        # Arrange
        from pyspark.sql.window import Window
        window = Window.partitionBy("user_id").orderBy("id")

        # Act
        result = sample_data.withColumn(
            "running_total",
            F.sum("amount").over(window)
        ).filter(F.col("user_id") == "user1")

        # Assert
        totals = [row["running_total"] for row in result.collect()]
        assert totals == [100.0, 250.0]
```

## Best Practices

### Performance
```python
# ✅ DO: Use DataFrame API over RDD
df.filter(F.col("status") == "active")  # Catalyst optimized

# ❌ DON'T: Use RDD transformations
rdd.filter(lambda x: x["status"] == "active")  # No optimization

# ✅ DO: Use built-in functions
df.withColumn("upper_name", F.upper("name"))

# ❌ DON'T: Use Python UDFs (slow serialization)
@udf
def upper_name(name):
    return name.upper()

# ✅ DO: Broadcast small lookups
df.join(broadcast(small_df), "key")

# ✅ DO: Persist wisely
intermediate.cache()
intermediate.count()  # Force materialization
# ... use intermediate multiple times ...
intermediate.unpersist()
```

### Code Organization
```python
# ✅ DO: Chain transformations fluently
result = (df
    .filter(condition)
    .withColumn("new_col", F.expr("..."))
    .groupBy("key")
    .agg(F.sum("value")))

# ✅ DO: Use descriptive column aliases
.agg(
    F.count("*").alias("event_count"),
    F.avg("amount").alias("avg_amount")
)

# ✅ DO: Parameterize for reusability
def add_date_features(df, date_col):
    return (df
        .withColumn("year", F.year(date_col))
        .withColumn("month", F.month(date_col))
        .withColumn("day_of_week", F.dayofweek(date_col)))
```

## Resources

### Official Documentation
- [Spark Documentation](https://spark.apache.org/docs/latest/)
- [Delta Lake Guide](https://docs.delta.io/)
- [Databricks Learning](https://www.databricks.com/learn)

### Performance Tuning
- [Spark Performance Tuning Guide](https://spark.apache.org/docs/latest/tuning.html)
- [Adaptive Query Execution](https://spark.apache.org/docs/latest/sql-performance-tuning.html)

### Books
- "Learning Spark 2nd Edition" by Damji et al.
- "Spark: The Definitive Guide" by Chambers & Zaharia
- "High Performance Spark" by Karau & Warren

## Next Skills

After mastering Big Data:
- → `data-warehousing` - Design dimensional models
- → `mlops` - Deploy ML at scale
- → `streaming` - Real-time with Flink/Kafka
- → `cloud-platforms` - AWS EMR, Databricks

---

**Skill Certification Checklist:**
- [ ] Can optimize Spark jobs using EXPLAIN and Spark UI
- [ ] Can implement efficient joins with broadcast and bucketing
- [ ] Can handle data skew with salting techniques
- [ ] Can build streaming pipelines with Structured Streaming
- [ ] Can use Delta Lake for ACID operations
