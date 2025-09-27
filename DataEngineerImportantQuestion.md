# Interview Q&A — Data Engineering / Azure / PySpark (detailed answers & code)
---

### 1) Find the **second highest salary** from an employee table (SQL)

**Approaches (choose depending on SQL dialect & requirements):**

**A. `ROW_NUMBER()` / `DENSE_RANK()` (portable, handles ties):**

```sql
-- returns second distinct highest salary (skip duplicates)
SELECT salary
FROM (
  SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
  FROM employee
) t
WHERE rnk = 2;
```

**B. Subquery (classic):**

```sql
SELECT MAX(salary) AS second_highest
FROM employee
WHERE salary < (SELECT MAX(salary) FROM employee);
```

**Notes:**

* Use `DENSE_RANK()` when you want the second *distinct* salary even if top salary appears many times.
* Use `ROW_NUMBER()` if you want the second row in a sorted list (not recommended for distinct-salary semantics).
* Consider `NULL` salaries: filter `WHERE salary IS NOT NULL` if needed.

---

### 2) How do you handle **NULL values in SQL joins**?

**Key ideas:**

* **NULLs don’t match to anything** in equality comparisons (`NULL = NULL` is `UNKNOWN`). So inner/outer joins behave based on presence/absence of rows, not NULL equality.
* **When join key may be NULL**:

  * Use `COALESCE(a.key, -1)` or some sentinel on both sides if you need NULLs to match — only if sentinel is safe.
  * Use `IS NULL` conditions explicitly to join rows where both sides are NULL:

    ```sql
    ON (a.key = b.key) OR (a.key IS NULL AND b.key IS NULL)
    ```
* **Outer joins**: Use `LEFT/RIGHT/FULL OUTER JOIN` to preserve rows that don’t have matches; handle NULLs in SELECT (via `COALESCE`) to provide defaults.
* **Filtering null-produced rows**: After `LEFT JOIN`, filter unmatched rows with `WHERE b.key IS NULL` to find non-matches.
* **Performance**: Extra `OR` conditions (`IS NULL`) may hamper index usage. Prefer data-cleaning or sentinel normalization upstream when possible.

---

### 3) Python script to read a CSV file and load it into a DataFrame (pandas)

```python
import pandas as pd

# read CSV into pandas DataFrame
df = pd.read_csv("data/input.csv",
                 sep=",",            # delimiter
                 parse_dates=["order_date"],  # parse date columns
                 dtype={"customer_id": int},  # explicit types
                 na_values=["", "NULL", "NA"]
                )

# basic checks
print(df.shape)
print(df.dtypes)
print(df.head())

# optional: write to parquet
df.to_parquet("data/output.parquet", index=False)
```

**Notes:** set `chunksize=` for very large files and process in batches to avoid memory issues.

---

### 4) How do you handle exceptions in Python using `try-except` blocks?

**Pattern & best practices:**

```python
try:
    # risky operation
    result = 10 / x
except ZeroDivisionError as e:
    # handle specific exception
    print("Cannot divide by zero:", e)
    result = None
except (TypeError, ValueError) as e:
    # multiple exceptions
    print("Invalid type or value:", e)
    raise  # re-raise if you cannot handle
except Exception as e:
    # catch-all (use sparingly)
    print("Unexpected error:", e)
finally:
    # always-run cleanup
    cleanup_resources()
```

**Best practices:**

* Catch **specific exceptions** rather than broad `Exception`.
* Use `finally` or context managers (`with`) for resource cleanup.
* Re-raise exceptions when higher layers should handle them.
* Add meaningful logging including stack traces (`logging.exception()`).

---

### 5) In PySpark, how would you perform a **join between two large DataFrames efficiently**?

**Strategies:**

* **Broadcast small table**: If one side is small (fits in driver memory), `broadcast()` the smaller DF:

  ```python
  from pyspark.sql.functions import broadcast
  df = large_df.join(broadcast(small_df), on="id", how="inner")
  ```
* **Partitioning & bucketing**:

  * Repartition both DataFrames by join key so matching keys land on the same executors: `df.repartition("key")`.
  * Use **bucketing** + saving as parquet/delta with buckets (helps repeated joins).
* **Avoid wide shuffles**: Reduce data footprint before join (select only needed columns, filter early).
* **Use appropriate join type**: e.g., for existence checks use `semi/anti` joins.
* **Skew handling**:

  * Detect hot keys; use salting or split/join patterns for skewed keys.
* **Use persisted cache**: If reused, persist intermediate DataFrames with correct storage level.

---

### 6) PySpark code: **Top 3 customers with highest revenue per region**

```python
from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, sum as _sum, desc

spark = SparkSession.builder.getOrCreate()

# sample: sales_df columns: customer_id, region, revenue
sales_df = spark.table("sales")  # or read from source

# aggregate revenue per customer per region
agg = (sales_df
       .groupBy("region", "customer_id")
       .agg(_sum("revenue").alias("total_revenue")))

# window partition by region order by revenue desc
w = Window.partitionBy("region").orderBy(desc("total_revenue"))

top3 = (agg.withColumn("rank", row_number().over(w))
          .filter("rank <= 3")
          .orderBy("region", "rank"))

top3.show()
```

**Notes:** If you have millions of customers per region, consider pre-aggregating and filtering in distributed manner; use `rank()` if you want ties to have same rank.

---

### 7) Difference between **partitioning** and **bucketing** in PySpark

* **Partitioning**:

  * Physical directory-level partitioning (e.g., `.../region=AP/`).
  * Great for pruning reads with filters (`WHERE region='AP'`).
  * Leads to many small files if over-partitioned.
* **Bucketing**:

  * Logical hashing of rows into fixed number of buckets, saved inside files.
  * Useful for efficient joins when both tables are bucketed by the same column and bucket count — Spark can perform **bucketed joins** without full shuffle.
  * Buckets are stable across writes and avoid explosion of small directories.
    **When to use**:
* Partition for high-cardinality filterable columns (date, region).
* Bucket for join keys used repeatedly and when you want shuffle-reduction but can't partition by that key.

---

### 8) Implementing **Slowly Changing Dimensions (SCD)** in a data warehouse

**Common types:**

* **SCD Type 1**: Overwrite attribute (no history). Use when history not required.
* **SCD Type 2**: Preserve history by creating new row for changes. Commonly used with `effective_from`, `effective_to`, `is_current` flags, and surrogate key.
* **SCD Type 3**: Keep limited history in columns (e.g., `previous_value`).

**SCD Type 2 (example approach using MERGE / upsert):**

1. Maintain dimension with surrogate key, business key, attributes, `start_date`, `end_date`, `is_current`.
2. For each batch:

   * Find rows where business key exists and attributes changed -> update old row `end_date = now, is_current = false`; insert new row with new surrogate key, `start_date = now, is_current = true`.
   * Insert rows where business key not found.
3. Implement via `MERGE` (SQL) or `Delta Lake MERGE` on primary key + attribute hash.

```sql
-- Pseudocode for MERGE (Delta / SQL)
MERGE INTO dim_customer tgt
USING stg_customer src
ON tgt.business_key = src.business_key AND tgt.is_current = TRUE
WHEN MATCHED AND (tgt.attr1 <> src.attr1 OR tgt.attr2 <> src.attr2) THEN
  UPDATE SET tgt.is_current = FALSE, tgt.end_date = src.batch_date
WHEN NOT MATCHED THEN
  INSERT (...) VALUES (...);
-- then insert the new "current" rows for changed records
```

**Best practices:** use hashing on attribute set to detect changes efficiently; make operations idempotent.

---

### 9) Star schema vs Snowflake schema (data modeling)

* **Star schema**:

  * Central **fact table** with foreign keys to denormalized **dimension tables**.
  * Simple, fast for BI queries, fewer joins.
  * Example: `fact_sales` + `dim_customer`, `dim_date`, `dim_product`.
* **Snowflake schema**:

  * Dimensions normalized into multiple related tables (e.g., `dim_location` split into `dim_city`, `dim_state`).
  * Reduces redundancy, but increases joins and complexity.
    **When to use**:
* *Star* is preferred for performance and simplicity in analytics.
* *Snowflake* may be used to save space or maintain normalized master data — but often ETL denormalizes to star for reporting.

---

### 10) Designing a **fact table** for an e-commerce platform

**Decisions:**

* **Grain**: one row = one order line (order_id + product_id + quantity) OR one payment transaction depending on needs.
* **Measures**: `line_total`, `quantity`, `unit_price`, `discount`, `cost`, `tax`, `shipping_cost`.
* **Dimensions (FKs)**: `dim_date_key`, `dim_customer_key`, `dim_product_key`, `dim_store_key`, `dim_promotion_key`, `dim_payment_type_key`.
* **Surrogate keys**: use integers for foreign keys.
* **Add metadata**: `created_at`, `etl_load_date`.
* **Design considerations**:

  * Add degenerate dimensions (e.g., `order_number`) in fact if needed.
  * Capture currency, exchange rate if multi-currency.
  * Partition on `order_date` for performance.
  * Use columnstore indexes (Synapse) or Delta with Z-ordering for query performance.

---

### 11) Build an **ETL pipeline** using Azure Data Factory (ADF)

**High-level steps:**

1. **Create Linked Services**: connect to sources (S3, SQL, ADLS) and sinks (Azure SQL, Synapse).
2. **Create Datasets**: define schema/file format for source and sink.
3. **Create Pipelines** composed of activities:

   * **Copy Activity** for ingestion.
   * **Mapping Data Flow** for transformations (or call Databricks notebooks for complex logic).
   * **Lookup / Stored Proc / Web** activities for orchestration.
4. **Parameterize** pipelines for reusability (file path, date).
5. **Triggers**: schedule/tumbling window/event-based triggers to run pipelines.
6. **Monitoring**: enable logging, use ADF monitoring pages, configure alerts.
7. **CI/CD**: integrate ADF with Git (Azure DevOps/GitHub) and automate deployments to dev/test/prod.

**Best practices**: use staging storage, incremental loads with watermarks, idempotent writes, parameterize for environment-specific settings, enable retry/backoff.

---

### 12) Different **types of triggers** in ADF and when to use them

* **Schedule trigger**: run at specific times/recurrence. Use for daily/hourly jobs.
* **Tumbling Window trigger**: periodic, with guaranteed non-overlapping windows and window-level retry — good for windowed batch windows (e.g., hourly partitions).
* **Event trigger**: fire pipeline on storage events (e.g., blob created). Use for near real-time when files land in ADLS/S3.
* **Manual trigger**: start on-demand from UI or REST API.
  **When to use**: Use tumbling windows for deterministic, time-windowed workloads; event triggers for file-driven ETL; schedule triggers for cron-like jobs.

---

### 13) Architecture of **Azure Databricks** and integration with **Delta Lake**

**Azure Databricks architecture (brief):**

* Managed Apache Spark service with workspaces, clusters (driver + executors), notebooks, jobs, and Repos.
* Collaborative environment with shared notebooks and integrated workspace.
  **Delta Lake integration:**
* Delta Lake adds ACID transactions, schema enforcement/evolution, time travel, and performant file layout (parquet + transaction logs).
* Databricks provides native Delta optimizations (`OPTIMIZE`, `ZORDER`, `VACUUM`).
  **Integration points:**
* Use Delta as the unified storage format on ADLS Gen2/Blob.
* Databricks jobs read/write Delta tables, perform MERGE for upserts, and enable streaming and batch with the same tables.
* Security: integrate with Azure AD, Managed Identities, and mount ADLS via credential passthrough or service principal.

---

### 14) PySpark code to process streaming data from Event Hub in Databricks

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, DoubleType, TimestampType

spark = SparkSession.builder.getOrCreate()

# Event Hubs connection configuration (map)
ehConf = {
  "eventhubs.connectionString": "<EVENT_HUBS_CONNECTION_STRING>"  # put into secret scope in prod
}

# read stream
raw = (spark.readStream
       .format("eventhubs")
       .options(**ehConf)
       .load())

# EventHub body is in 'body' column (binary)
schema = StructType([
    ("order_id", StringType()),
    ("customer_id", StringType()),
    ("amount", DoubleType()),
    ("event_time", TimestampType())
])

json_df = (raw.selectExpr("cast(body as string) as body")
             .select(from_json(col("body"), schema).alias("data"))
             .select("data.*"))

# simple aggregation: total revenue per minute
agg = (json_df
       .withWatermark("event_time", "2 minutes")
       .groupBy(window(col("event_time"), "1 minute"), col("customer_id"))
       .sum("amount"))

# write to Delta table
query = (agg.writeStream
         .format("delta")
         .outputMode("update")
         .option("checkpointLocation", "/mnt/checkpoints/eventhub_to_delta")
         .option("mergeSchema", "true")
         .option("path", "/mnt/delta/streaming/agg_revenue")
         .start())

query.awaitTermination()
```

**Notes:** store connection strings in Databricks secrets, set checkpointing, use watermark for late data handling.

---

### 15) How to **optimize query performance** in Azure Synapse Analytics

**Dedicated SQL pool tips:**

* **Choose distribution**: `HASH` on join key for large tables; `REPLICATE` for small lookup tables; `ROUND_ROBIN` for initial loads.
* **Clustered Columnstore Index** on large fact tables for analytics compression and speed.
* **Partitioning** large tables by date.
* **Statistics**: update statistics frequently; use `CREATE STATISTICS` as needed.
* **Materialized views** for expensive aggregations.
* **Result set caching** for repeated queries.
* **Minimize data movement**: aim to co-locate join keys and use hash distribution to reduce network shuffle.
* **Resource classes & workload management**: assign appropriate resource classes to heavy queries.
* **Avoid scalar UDFs** in hot paths; prefer inline table-valued functions.

---

### 16) Designing a **data warehouse** for a retail business using Synapse

**High-level design:**

* **Landing zone**: ingest raw files to ADLS Gen2.
* **Staging**: raw->staging (parquet/delta), basic validations.
* **Historical zone**: Delta / Synapse dedicated pool tables for curated data.
* **Model**: star schema with fact tables (`fact_sales`, `fact_inventory`) and dimension tables (`dim_date`, `dim_product`, `dim_customer`, `dim_store`).
* **ETL orchestration**: use ADF/Databricks to transform and load to Synapse.
* **Partitions & distributions**: partition facts by date; use hash distribution on `product_id` or `customer_id` depending on query patterns.
* **Reporting**: Power BI connecting to Synapse or Synapse serverless SQL for ad hoc queries.
* **Governance/security**: Azure AD, Private Endpoints, Key Vault for secrets, Purview for catalog and lineage.

---

### 17) Best practices for **securing data in Azure Data Lake Storage (ADLS)**

* **Network**: Use VNet service endpoints or Private Endpoint to restrict access.
* **Authentication**: Use Azure AD + Managed Identities; avoid account keys.
* **Access control**: use RBAC at subscription/resource level AND POSIX ACLs at file/folder level.
* **Encryption**: Server-side encryption (SSE) with Microsoft-managed keys (default) or Customer-managed keys (CMK).
* **Logging & monitoring**: enable diagnostic logs, Azure Monitor, and alerting.
* **Data classification & masking**: integrate with Purview for classification; apply data masking where needed.
* **Least privilege**: assign minimal permissions and use role separation.
* **Compliance**: maintain audit trails and retention policies.

---

### 18) Manage **access control and secrets** using Azure Key Vault

* **Store secrets/certs/keys** (connection strings, passwords) in Key Vault.
* **Access control**:

  * Use Azure RBAC for Key Vault management ops.
  * Use Key Vault access policies or RBAC roles for secret access (depending on vault config).
* **Access from workloads**:

  * Use Managed Identity (system-assigned or user-assigned) for Databricks/VMs/Functions to obtain secrets without credentials.
  * Use SDKs or REST API to fetch secrets (or Key Vault-backed secret scopes in Databricks).
* **Rotation & versioning**: enable secret versioning and automation for rotation.
* **Auditing**: enable logging to monitor secret access.

---

### 19) PySpark script to load data from ADLS into a Delta table

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

# read CSV from ADLS (use service principal / managed identity config)
df = (spark.read
      .option("header", "true")
      .option("inferSchema", "true")
      .csv("abfss://container@storageaccount.dfs.core.windows.net/path/to/data/"))

# transform as required
df = df.withColumnRenamed("old_col", "new_col")

# write to delta table
(df.write
   .format("delta")
   .mode("overwrite")              # or "append" for incremental
   .option("mergeSchema", "true")
   .save("/mnt/delta/ecommerce/orders"))

# register in metastore
spark.sql("CREATE TABLE IF NOT EXISTS ecommerce.orders USING DELTA LOCATION '/mnt/delta/ecommerce/orders'")
```

**Notes:** mount storage with correct credentials, prefer `spark.conf` for auth or use credential passthrough.

---

### 20) Implement data lineage and governance in **Microsoft Purview**

**Steps:**

1. **Register data sources** (ADLS, Synapse, Azure SQL, Power BI) in Purview.
2. **Scan** sources to harvest metadata and build asset catalog.
3. **Classify & label** data using built-in classifiers or custom classifiers.
4. **Glossary**: create business terms and map to assets for consistent meaning.
5. **Lineage capture**: Purview automatically captures scan lineage and can integrate with ETL tools (Databricks, ADF). For custom pipelines, send lineage metadata via REST APIs.
6. **Access policies & RBAC**: integrate with Azure AD for access control and use Purview to discover data owners.
7. **Search & discovery**: enable users to find data and understand its provenance and quality.
   **Best practices:** scan regularly, keep metadata up-to-date, document owners, and combine Purview with monitoring/alerting.

---

### 21) Build a **real-time analytics pipeline** using Event Hub, Stream Analytics, and Synapse

**Architecture (high-level):**

1. **Producers**: apps, IoT send events to **Event Hubs**.
2. **Stream processing**: **Azure Stream Analytics (ASA)** reads from Event Hub, performs real-time aggregations/windowing and writes outputs to:

   * **Synapse (Dedicated SQL pool)** for reporting,
   * **Power BI** for dashboards,
   * **Blob/ADLS/Delta** for storage.
3. **Long-term store & BI**: use Synapse or Delta Lake for enriched data and historical analytics.
   **Implementation notes:**

* Use ASA for SQL-like stream queries when low-latency and simple transforms suffice.
* For complex transforms, use Databricks Structured Streaming reading from Event Hubs, then write to Delta / Synapse.
* Ensure checkpointing, idempotent sinks, and monitoring.

---

### 22) How to handle **late-arriving data** in a batch ETL pipeline

**Strategies:**

* **Watermarking & windows**: design windows with allowed lateness, reprocess windows when late data arrives.
* **Staging & incremental reprocessing**: write raw events to a staging area (append-only), and recompute aggregates for affected time windows.
* **Idempotent upserts**: use MERGE to update fact/aggregate tables based on event timestamps.
* **Tombstones / correction events**: handle deletes/updates from source by replaying with proper flags.
* **Alerting**: detect delayed partitions and trigger backfills.
  **Choice depends on SLA**: small acceptable reprocessing vs full re-computation.

---

### 23) SQL query to calculate **customer churn rate** over the last 6 months

**Definition**: churn = % customers active in prior period who are not active in current period. Example: monthly churn.

```sql
-- Assuming table customer_activity(customer_id, activity_date)
WITH months AS (
  SELECT DISTINCT DATE_TRUNC('month', activity_date) AS month_start
  FROM customer_activity
  WHERE activity_date >= DATEADD(month, -7, CURRENT_DATE)  -- last 7 months to compute 6 intervals
),
cust_month AS (
  SELECT customer_id,
         DATE_TRUNC('month', activity_date) AS month_start
  FROM customer_activity
  WHERE activity_date >= DATEADD(month, -7, CURRENT_DATE)
  GROUP BY customer_id, DATE_TRUNC('month', activity_date)
),
churn_calc AS (
  SELECT m.month_start,
         COUNT(DISTINCT cm_prev.customer_id) AS prev_active,
         COUNT(DISTINCT cm_prev.customer_id) 
           - COUNT(DISTINCT cm_curr.customer_id) AS churned_customers
  FROM months m
  LEFT JOIN cust_month cm_prev
    ON cm_prev.month_start = DATEADD(month, -1, m.month_start)
  LEFT JOIN cust_month cm_curr
    ON cm_curr.month_start = m.month_start
    AND cm_curr.customer_id = cm_prev.customer_id
  GROUP BY m.month_start
)
SELECT month_start,
       churned_customers,
       prev_active,
       CASE WHEN prev_active = 0 THEN 0
            ELSE CAST(churned_customers AS FLOAT)/prev_active END AS churn_rate
FROM churn_calc
ORDER BY month_start DESC
LIMIT 6;
```

**Notes:** Adjust activity definition (order placed, login, purchase) to match business definition of “active”.

---

### 24) Implement **incremental data loading** in ADF pipelines

**Approaches:**

* **Watermark column**: keep a `last_max_time` (e.g., `modified_at`) and use it in source query to fetch only newer rows.
* **Change Data Capture (CDC)**: use CDC-enabled sources (SQL Server, Azure SQL) to read changes.
* **Delta Lake**: use Delta time travel/`MERGE` for upserts in sink.
* **Mapping Data Flows**: use `Alter Row` + `Surrogate Key` patterns to upsert in target.
* **Idempotency**: use `MERGE` in sink or run dedupe logic to avoid duplicates.
  **Example flow**: Lookup last watermark -> Copy activity with SQL query `WHERE modified_at > @watermark` -> Load to staging -> MERGE/update target -> Update watermark.

---

### 25) Python script to validate data quality and detect anomalies

```python
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

# load
df = pd.read_csv("data/input.csv")

# basic checks
dq_report = {}
dq_report['null_counts'] = df.isnull().sum().to_dict()
dq_report['num_rows'] = len(df)
dq_report['duplicates'] = df.duplicated().sum()

# simple numeric validation: range checks
if 'amount' in df.columns:
    dq_report['amount_min'] = df['amount'].min()
    dq_report['amount_max'] = df['amount'].max()

# anomaly detection (Isolation Forest) on numeric features
num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
if num_cols:
    clf = IsolationForest(contamination=0.01, random_state=42)
    X = df[num_cols].fillna(0)
    preds = clf.fit_predict(X)
    df['anomaly'] = (preds == -1)
    anomalies = df[df['anomaly']]
else:
    anomalies = pd.DataFrame()

print("DQ report:", dq_report)
print("Anomalies found:", len(anomalies))
# export report
dq_report_df = pd.DataFrame([dq_report])
dq_report_df.to_csv("data/dq_report.csv", index=False)
anomalies.to_csv("data/anomalies.csv", index=False)
```

**Notes:** Choose algorithm based on data volume. For time-series use seasonal decomposition or z-score on residuals.

---

### 26) Perform **schema evolution** in Delta Lake

**Approaches:**

* **Merge schema on write**:

  ```python
  df.write.format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .save(delta_path)
  ```
* **Alter table**: use `ALTER TABLE` to add columns.
* **MERGE operations**: set `mergeSchema=true` when merging new data with additional columns into existing Delta table.
  **Best practices:** keep schema changes controlled, use evolution only when necessary, and track downstream consumers.

---

### 27) Design a data pipeline to handle **both batch and streaming** data

**Recommended approach:** Use **Delta Lake** as unified storage and Databricks Structured Streaming plus batch jobs (Kappa-style hybrid).

* **Ingest**: streaming sources (Event Hubs/Kafka) -> Structured Streaming -> write to Delta (append). Batch files -> batch job -> write to Delta.
* **Serving**: read Delta tables for BI/analytics (consistent schema).
* **Transform**: use incremental streaming jobs and scheduled batch jobs that operate on same Delta tables. Use `MERGE` and versioning for updates.
  **Benefits:** Single storage format, ACID guarantees, time travel for consistency, simplified architecture.

---

### 28) PySpark code: **window functions** for ranking sales data

```python
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, rank, dense_rank, desc

# sales_df columns: sale_date, product_id, region, revenue
w = Window.partitionBy("region").orderBy(desc("revenue"))

ranked = sales_df.withColumn("row_num", row_number().over(w)) \
                 .withColumn("rank", rank().over(w)) \
                 .withColumn("dense_rank", dense_rank().over(w))

ranked.filter("row_num <= 10").show()
```

**Use cases:** `row_number()` for unique ranking, `rank()` preserves gaps on ties, `dense_rank()` has no gaps.

---

### 29) Optimize **storage and query performance** in a Synapse dedicated pool

* **Distribution strategy**: choose `HASH` for large table joins on a key, `REPLICATE` for small lookups.
* **Partitioning**: partition tables by date for pruneable queries.
* **Clustered Columnstore Index**: use for large fact tables.
* **Statistics & compression**: keep stats updated and use appropriate compression.
* **Materialized views** for recurring expensive aggregations.
* **Avoid SELECT *:** project only needed columns; use predicate pushdown.
* **Reduce small files** in external storage; merge into larger files for efficient reading.
* **Use result set caching** and set up workload management for concurrency.

---

### 30) End-to-end pipeline: ingest from multiple sources → transform in Databricks → load into Synapse for reporting

**Architecture & components:**

1. **Ingest**:

   * Real-time: Event Hubs -> Databricks Structured Streaming.
   * Batch: SFTP / APIs / RDBMS -> ADF Copy -> ADLS raw zone.
2. **Raw landing**: store original files in ADLS (partitioned).
3. **ETL/Transform** (Databricks):

   * Use notebooks/jobs to read raw, clean, deduplicate, join sources.
   * Write curated data as Delta tables (`/mnt/delta/curated/...`).
   * Use Delta `MERGE` for upserts and SCD handling.
   * Implement unit tests and schema checks.
4. **Load to Synapse**:

   * Export curated datasets to Synapse (bulk-copy) or create external tables over ADLS parquet/delta if using serverless.
   * Use `COPY INTO` or PolyBase for efficient loads into dedicated pool.
5. **Modeling & Reporting**:

   * Build star schema fact/dim tables in Synapse, create materialized views and indexes.
   * Connect Power BI to Synapse for dashboards.
6. **Orchestration**:

   * Use ADF or Databricks jobs for end-to-end orchestration, with parameterized pipelines and triggers.
7. **Monitoring & Governance**:

   * Monitor with Azure Monitor, Databricks Jobs UI, and Purview for lineage.
   * Manage secrets via Key Vault, access via managed identities.
8. **Scalability & Cost**:

   * Use autoscaling clusters in Databricks, control Synapse resource classes, and use partitioning to reduce cost of scans.

---

