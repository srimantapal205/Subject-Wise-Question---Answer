# 🔹 SECTION 1: Databricks & Delta Live Tables (DLT) – 25 Q&A

### 1. What is Delta Live Tables (DLT)?

**Answer:**
DLT is a declarative framework in Databricks used to build reliable, maintainable, and testable data pipelines using SQL or PySpark. It manages data quality, orchestration, and monitoring automatically.

---

### 2. Difference between DLT and traditional Databricks jobs?

**Answer:**
DLT is declarative and pipeline-driven, while Databricks jobs are imperative. DLT handles dependency resolution, retries, and quality checks automatically.

---

### 3. What are LIVE tables in DLT?

**Answer:**
LIVE tables are managed tables created and maintained by DLT pipelines with built-in lineage, monitoring, and data quality enforcement.

---

### 4. What is the difference between LIVE TABLE and STREAMING LIVE TABLE?

**Answer:**

* **LIVE TABLE** → Batch processing
* **STREAMING LIVE TABLE** → Continuous/streaming ingestion

---

### 5. What is APPLY CHANGES INTO in DLT?

**Answer:**
It enables CDC (Slowly Changing Dimensions) handling using merge semantics, often used with change data feeds.

---

### 6. How do you enforce data quality in DLT?

**Answer:**
Using **EXPECT**, **EXPECT_OR_DROP**, and **EXPECT_OR_FAIL** constraints.

---

### 7. What happens when EXPECT_OR_FAIL fails?

**Answer:**
The pipeline stops execution immediately.

---

### 8. What is DLT pipeline mode?

**Answer:**

* **Triggered** → Batch execution
* **Continuous** → Streaming execution

---

### 9. How does DLT manage dependencies?

**Answer:**
DLT automatically builds DAGs based on table references.

---

### 10. How is schema evolution handled in DLT?

**Answer:**
DLT supports automatic schema evolution with Delta Lake.

---

### 11. Can DLT be written in SQL and PySpark together?

**Answer:**
Yes, both can coexist in the same pipeline.

---

### 12. How do you monitor DLT pipelines?

**Answer:**
Using the Databricks DLT UI, event logs, and system tables.

---

### 13. What is DLT event log?

**Answer:**
A system table storing pipeline execution metadata.

---

### 14. How does DLT ensure idempotency?

**Answer:**
Using Delta transaction logs and checkpointing.

---

### 15. What is materialized view vs live table?

**Answer:**
Materialized views are optimized for query performance; live tables focus on pipeline reliability.

---

### 16. Can DLT read from Kafka?

**Answer:**
Yes, via Structured Streaming.

---

### 17. What is the role of checkpoints in DLT?

**Answer:**
They track progress and enable fault tolerance.

---

### 18. How do you deploy DLT across environments?

**Answer:**
Using parameterized pipelines and CI/CD.

---

### 19. What happens if upstream table fails?

**Answer:**
Downstream tables do not execute.

---

### 20. How do you optimize DLT pipelines?

**Answer:**

* Partitioning
* Z-Ordering
* Cluster sizing
* Auto-scaling

---

### 21. Difference between bronze, silver, gold in DLT?

**Answer:**

* **Bronze** → Raw
* **Silver** → Cleaned
* **Gold** → Aggregated/business-ready

---

### 22. Can DLT write to external tables?

**Answer:**
Yes, but managed tables are recommended.

---

### 23. How do you handle late arriving data?

**Answer:**
Using watermarking in streaming tables.

---

### 24. Is DLT suitable for real-time workloads?

**Answer:**
Yes, with Structured Streaming.

---

### 25. DLT vs ADF?

**Answer:**
DLT is transformation-focused; ADF is orchestration-focused.

---

# 🔹 SECTION 2: Structured Streaming – 20 Q&A

### 26. What is Structured Streaming?

**Answer:**
A scalable stream processing engine built on Spark SQL.

---

### 27. Micro-batch vs Continuous mode?

**Answer:**

* Micro-batch → Default, reliable
* Continuous → Low latency, limited operations

---

### 28. What is watermarking?

**Answer:**
It defines how long to wait for late data.

---

### 29. What is stateful streaming?

**Answer:**
Streaming operations that maintain state across batches.

---

### 30. How is fault tolerance achieved?

**Answer:**
Using checkpoints and WAL.

---

### 31. What is exactly-once processing?

**Answer:**
Each record is processed once even after failures.

---

### 32. How do you handle duplicates?

**Answer:**
Using `dropDuplicates()` with watermark.

---

### 33. Kafka offset management?

**Answer:**
Offsets are stored in checkpoints.

---

### 34. Output modes in streaming?

**Answer:**

* Append
* Update
* Complete

---

### 35. What is trigger?

**Answer:**
Controls batch execution frequency.

---

### 36. What is foreachBatch?

**Answer:**
Allows custom logic per micro-batch.

---

### 37. How do you join two streams?

**Answer:**
Using stream-stream joins with watermark.

---

### 38. What is backpressure?

**Answer:**
Controlling ingestion rate to avoid overload.

---

### 39. Streaming file source vs Kafka?

**Answer:**
Kafka is real-time; file source is near-real-time.

---

### 40. What is state store?

**Answer:**
Storage for streaming aggregation state.

---

### 41. How do you scale streaming jobs?

**Answer:**
Auto-scaling and partition tuning.

---

### 42. Handling schema evolution in streaming?

**Answer:**
Enable `mergeSchema`.

---

### 43. What is trigger once?

**Answer:**
Processes all available data once and stops.

---

### 44. Can streaming write to Delta?

**Answer:**
Yes, natively supported.

---

### 45. How do you monitor lag?

**Answer:**
Using streaming query progress metrics.

---

# 🔹 SECTION 3: PySpark & Python – 20 Q&A

### 46. Difference between RDD, DataFrame, Dataset?

**Answer:**
DataFrame/Dataset are optimized and schema-based.

---

### 47. When to use UDF?

**Answer:**
Only when built-in functions don’t suffice.

---

### 48. Pandas UDF vs normal UDF?

**Answer:**
Pandas UDFs are vectorized and faster.

---

### 49. What is broadcast join?

**Answer:**
Small table is broadcast to all executors.

---

### 50. What is lazy evaluation?

**Answer:**
Spark builds DAG but executes only on action.

---

### 51. Narrow vs wide transformation?

**Answer:**
Wide transformations cause shuffle.

---

### 52. How do you reduce shuffle?

**Answer:**

* Repartition wisely
* Broadcast joins

---

### 53. What is cache vs persist?

**Answer:**
Cache uses memory; persist supports multiple storage levels.

---

### 54. Difference between coalesce and repartition?

**Answer:**
Repartition causes shuffle; coalesce doesn’t.

---

### 55. How to optimize joins?

**Answer:**
Use broadcast, partition pruning, and correct join type.

---

### 56. What is Spark UI used for?

**Answer:**
Monitoring jobs, stages, and performance.

---

### 57. Python GIL impact?

**Answer:**
Spark runs Python in parallel via executors.

---

### 58. What is accumulator?

**Answer:**
Used for global counters.

---

### 59. What is checkpointing?

**Answer:**
Cuts lineage for fault tolerance.

---

### 60. How do you handle skew?

**Answer:**
Salting keys or adaptive query execution.

---

### 61. Difference between map and mapPartitions?

**Answer:**
mapPartitions is faster for large data.

---

### 62. How do you debug PySpark jobs?

**Answer:**
Logs, Spark UI, explain plans.

---

### 63. What is Catalyst optimizer?

**Answer:**
Optimizes logical and physical plans.

---

### 64. What is Tungsten?

**Answer:**
Memory and CPU optimization engine.

---

### 65. Best practices for PySpark?

**Answer:**
Avoid UDFs, reduce shuffle, use built-in functions.

---

# 🔹 SECTION 4: SQL (Databricks / Spark SQL) – 15 Q&A

### 66. What is Z-Ordering?

**Answer:**
Optimizes data skipping for selective queries.

---

### 67. What is partition pruning?

**Answer:**
Reading only required partitions.

---

### 68. Window functions use cases?

**Answer:**
Ranking, running totals, deduplication.

---

### 69. CTE vs subquery?

**Answer:**
CTE improves readability and reuse.

---

### 70. How do you optimize SQL queries?

**Answer:**
Indexes, partitions, explain plans.

---

### 71. What is Delta Lake?

**Answer:**
Storage layer providing ACID transactions.

---

### 72. What is time travel?

**Answer:**
Query historical versions of data.

---

### 73. OPTIMIZE vs VACUUM?

**Answer:**
OPTIMIZE compacts files; VACUUM deletes old files.

---

### 74. Explain MERGE INTO?

**Answer:**
Upsert operation for CDC.

---

### 75. How do you deduplicate data?

**Answer:**
Using ROW_NUMBER and window functions.

---

### 76. What is data skipping?

**Answer:**
Skipping files using metadata stats.

---

### 77. What is adaptive query execution?

**Answer:**
Optimizes query plan at runtime.

---

### 78. Difference between UNION and UNION ALL?

**Answer:**
UNION removes duplicates.

---

### 79. How do you handle nulls?

**Answer:**
COALESCE, NVL.

---

### 80. Explain explain plan?

**Answer:**
Shows logical and physical execution.

---

# 🔹 SECTION 5: Azure Data Services – 15 Q&A

### 81. Role of ADF in architecture?

**Answer:**
Orchestration and ingestion.

---

### 82. ADF vs Databricks?

**Answer:**
ADF orchestrates; Databricks processes.

---

### 83. What is ADLS Gen2?

**Answer:**
Scalable, secure data lake storage.

---

### 84. Security in ADLS?

**Answer:**
RBAC, ACLs, encryption.

---

### 85. What is Synapse used for?

**Answer:**
Analytics and data warehousing.

---

### 86. When to use Stream Analytics?

**Answer:**
Lightweight real-time transformations.

---

### 87. How do you trigger Databricks from ADF?

**Answer:**
Using Databricks activity.

---

### 88. How do you handle secrets?

**Answer:**
Azure Key Vault.

---

### 89. Difference between managed and external tables?

**Answer:**
Managed tables controlled by Databricks.

---

### 90. Data ingestion patterns in Azure?

**Answer:**
Batch, streaming, CDC.

---

### 91. How do you design fault-tolerant pipelines?

**Answer:**
Retries, checkpoints, idempotent writes.

---

### 92. What is event-based trigger?

**Answer:**
Triggered by blob arrival.

---

### 93. How do you manage environments?

**Answer:**
Separate resource groups and workspaces.

---

### 94. Cost optimization strategies?

**Answer:**
Auto-terminate clusters, spot instances.

---

### 95. Monitoring tools in Azure?

**Answer:**
Log Analytics, Azure Monitor.

---

# 🔹 SECTION 6: Unity Catalog & Optimization – 15 Q&A

### 96. What is Unity Catalog?

**Answer:**
Centralized governance for data and AI assets.

---

### 97. Benefits of Unity Catalog?

**Answer:**
Fine-grained access control and lineage.

---

### 98. How does Unity Catalog improve security?

**Answer:**
Table, column, row-level security.

---

### 99. Difference between Hive Metastore and Unity Catalog?

**Answer:**
Unity Catalog is centralized and cross-workspace.

---

### 100. How do you manage permissions?

**Answer:**
Using GRANT/REVOKE.

---

### 101. What is lineage tracking?

**Answer:**
Tracking data flow from source to target.

---

### 102. How do you optimize Databricks for high volume?

**Answer:**
Auto-scaling, optimized clusters, caching.

---

### 103. What is Photon?

**Answer:**
Vectorized execution engine for faster queries.

---

### 104. Handling small files problem?

**Answer:**
OPTIMIZE and auto-compaction.

---

### 105. What is data skipping index?

**Answer:**
Metadata-based file pruning.

---

### 106. How do you tune Spark jobs?

**Answer:**
Executor memory, shuffle partitions.

---

### 107. Best practices for real-time pipelines?

**Answer:**
Watermarking, idempotent writes, monitoring.

---

### 108. How do you ensure SLA?

**Answer:**
Alerts, auto-scaling, retries.

---

### 109. How do you design multi-tenant data platforms?

**Answer:**
Unity Catalog + RBAC + isolated schemas.

---

### 110. What makes you confident handling high-volume real-time data?

**Answer:**
Experience with streaming, optimization, governance, and monitoring at scale.

---

# Below are **end-to-end, production-style coding examples** 

* **Databricks Delta Live Tables (DLT)**
* **Structured Streaming**
* **PySpark + Python**
* **Spark SQL**
* **Azure Data Services (ADF, ADLS, Synapse pattern)**
* **Unity Catalog**
* **Performance optimization for high-volume real-time pipelines**

---

## 1️⃣ High-Level Real-Time Architecture (Context)

```
Event Source (Kafka / Event Hub)
        ↓
Structured Streaming
        ↓
DLT Bronze (Raw)
        ↓
DLT Silver (Clean + Dedup)
        ↓
DLT Gold (Aggregations)
        ↓
Synapse / BI / APIs
```

Storage: **ADLS Gen2**
Governance: **Unity Catalog**
Orchestration: **ADF triggers Databricks DLT pipeline**

---

## 2️⃣ Unity Catalog Setup (One-Time)

```sql
-- Create catalog
CREATE CATALOG realtime_catalog;

-- Create schema
CREATE SCHEMA realtime_catalog.iot;

-- Grant access
GRANT USE CATALOG ON CATALOG realtime_catalog TO `data_engineers`;
GRANT USE SCHEMA ON SCHEMA realtime_catalog.iot TO `data_engineers`;
```

✅ Enables **centralized governance, lineage, and security**

---

## 3️⃣ Structured Streaming Ingestion (Bronze Layer – DLT)

### PySpark – Streaming from Kafka/Event Hub

```python
import dlt
from pyspark.sql.functions import *
from pyspark.sql.types import *

@dlt.table(
    name="bronze_events",
    comment="Raw streaming events from source",
    table_properties={"quality": "bronze"}
)
def bronze_events():
    return (
        spark.readStream
            .format("kafka")
            .option("kafka.bootstrap.servers", "broker:9092")
            .option("subscribe", "iot-events")
            .option("startingOffsets", "latest")
            .load()
            .selectExpr("CAST(value AS STRING) as json")
            .select(from_json(col("json"), schema_of_json("""{
                "device_id": "string",
                "event_time": "timestamp",
                "temperature": "double"
            }""")).alias("data"))
            .select("data.*")
    )
```

🔹 **Why this matters in interview**

* Streaming ingestion
* Schema enforcement
* Bronze pattern

---

## 4️⃣ Data Quality & Deduplication (Silver Layer – DLT)

```python
@dlt.table(
    name="silver_events",
    comment="Cleaned and deduplicated events",
    table_properties={"quality": "silver"}
)
@dlt.expect_or_drop("valid_device", "device_id IS NOT NULL")
@dlt.expect("valid_temperature", "temperature BETWEEN -40 AND 100")
def silver_events():
    return (
        dlt.read_stream("bronze_events")
           .withWatermark("event_time", "10 minutes")
           .dropDuplicates(["device_id", "event_time"])
    )
```

✅ Uses:

* **EXPECT / EXPECT_OR_DROP**
* **Watermarking**
* **Exactly-once semantics**

---

## 5️⃣ Business Aggregations (Gold Layer – DLT)

```python
@dlt.table(
    name="gold_device_metrics",
    comment="Aggregated metrics per device",
    table_properties={"quality": "gold"}
)
def gold_device_metrics():
    return (
        dlt.read_stream("silver_events")
           .groupBy(
               window(col("event_time"), "5 minutes"),
               col("device_id")
           )
           .agg(
               avg("temperature").alias("avg_temp"),
               max("temperature").alias("max_temp"),
               count("*").alias("event_count")
           )
    )
```

📊 Perfect **real-time analytics output**

---

## 6️⃣ SQL Version (DLT SQL Pipeline)

```sql
CREATE STREAMING LIVE TABLE silver_events_sql
(
  CONSTRAINT valid_device EXPECT (device_id IS NOT NULL),
  CONSTRAINT valid_temp EXPECT (temperature BETWEEN -40 AND 100)
)
AS
SELECT DISTINCT
    device_id,
    event_time,
    temperature
FROM STREAM(LIVE.bronze_events);
```

💡 Interview tip: **mention SQL + PySpark coexistence**

---

## 7️⃣ CDC / UPSERT using APPLY CHANGES INTO (DLT)

```sql
APPLY CHANGES INTO LIVE.device_state
FROM STREAM(LIVE.silver_events)
KEYS (device_id)
SEQUENCE BY event_time
COLUMNS *
```

✅ Handles **late data + CDC** automatically

---

## 8️⃣ Performance Optimization – MUST KNOW

### 🔹 Partitioning + Z-Ordering

```sql
OPTIMIZE realtime_catalog.iot.gold_device_metrics
ZORDER BY (device_id);
```

---

### 🔹 Auto Compaction & Optimize Write

```python
spark.conf.set("spark.databricks.delta.optimizeWrite.enabled", "true")
spark.conf.set("spark.databricks.delta.autoCompact.enabled", "true")
```

---

### 🔹 Broadcast Join Optimization

```python
from pyspark.sql.functions import broadcast

enriched_df = silver_df.join(
    broadcast(device_dim),
    "device_id",
    "left"
)
```

---

### 🔹 Adaptive Query Execution

```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
```

---

## 9️⃣ Writing Streaming Output to ADLS (Delta)

```python
(
    gold_df.writeStream
        .format("delta")
        .outputMode("append")
        .option("checkpointLocation", "abfss://chk@storage.dfs.core.windows.net/gold/")
        .start("abfss://gold@storage.dfs.core.windows.net/device_metrics/")
)
```

✔ Fault-tolerant
✔ Exactly-once
✔ Cloud-native

---

## 🔟 ADF → Databricks DLT Trigger (Concept)

ADF pipeline:

* **Web Activity / Databricks Activity**
* Pass parameters like:

  * environment
  * storage path
  * pipeline mode (triggered / continuous)

DLT handles **processing**, ADF handles **orchestration**

---

## 1️⃣1️⃣ Monitoring & Debugging (Interview Favorite)

```python
for q in spark.streams.active:
    q.lastProgress
```

Key Metrics:

* inputRowsPerSecond
* processedRowsPerSecond
* stateOperators

---

## 1️⃣2️⃣ Typical Interview Explanation (How to Answer)

> “I use Structured Streaming with DLT for real-time ingestion, enforce quality at Silver using expectations, aggregate at Gold, govern everything using Unity Catalog, and optimize using Z-Ordering, Photon, AQE, and broadcast joins.”

---

## 1️⃣3️⃣ BONUS: Spark SQL Window + Dedup (Classic Question)

```sql
SELECT *
FROM (
  SELECT *,
         ROW_NUMBER() OVER (
           PARTITION BY device_id, event_time
           ORDER BY event_time DESC
         ) rn
  FROM realtime_catalog.iot.silver_events
)
WHERE rn = 1;
```
