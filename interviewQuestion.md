
# 1. SQL — Second highest salary

Use window functions (robust) or `LIMIT`/`OFFSET` depending on SQL dialect.

**Example (ANSI SQL / Postgres / SQL Server with TOP):**

```sql
-- Using window function (works in most engines)
SELECT DISTINCT salary
FROM (
  SELECT salary,
         DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
  FROM employee
) t
WHERE rnk = 2;
```

**Explanation:** `DENSE_RANK()` ranks salaries; pick rank 2. `DISTINCT` in outer ensures single value.

---

# 2. Handling NULLs in SQL joins

NULLs can affect join behavior when joining on nullable columns. Strategies:

* Use `IS NULL`/`IS NOT DISTINCT FROM` (Postgres) to match NULLs.
* Coalesce keys to default values (`COALESCE`) when safe.
* Use outer joins to preserve unmatched rows.

**Example — match rows even when join key NULL (Postgres):**

```sql
SELECT a.*, b.*
FROM table_a a
LEFT JOIN table_b b
  ON (a.key = b.key OR (a.key IS NULL AND b.key IS NULL));
```

**Explanation:** Default equality `=` treats NULL as unknown; explicit `IS NULL` check lets NULL keys match.

---

# 3. Python script to read CSV into DataFrame

Using `pandas` (common) and `pyarrow`/`dtypes` options for large files.

```python
import pandas as pd

df = pd.read_csv('data/input.csv', dtype={'id': 'Int64'}, parse_dates=['created_at'])
print(df.head())
```

**Explanation:** `parse_dates` converts timestamps; `dtype` with nullable Int (`Int64`) handles missing ints.

---

# 4. Exceptions in Python with try-except

Use `try`/`except` blocks, optionally `else` and `finally`.

```python
try:
    result = 10 / x
except ZeroDivisionError as e:
    print("Division by zero:", e)
except (TypeError, ValueError) as e:
    print("Bad input:", e)
else:
    print("Success:", result)
finally:
    print("Cleanup actions here")
```

**Explanation:** `except` catches errors, `else` runs if no exception, `finally` always runs (cleanup).

---

# 5. Efficient joins of two large DataFrames in PySpark

Best practices:

* Broadcast the smaller DF (`broadcast(df_small)`) when one side is small.
* Repartition by join key(s) to avoid data skew (e.g., `df.repartition("key")`).
* Use bucketing (Hive tables) if repeated joins on same keys.
* Filter/pushdown before join to reduce size.
* Use `join` with appropriate join type and condition.

**Example:**

```python
from pyspark.sql.functions import broadcast

# If df_small << df_large
joined = df_large.join(broadcast(df_small), on="customer_id", how="inner")

# If both large: repartition on join keys
df1 = df1.repartition("customer_id")
df2 = df2.repartition("customer_id")
joined = df1.join(df2, on="customer_id")
```

---

# 6. PySpark — top 3 customers by revenue per region

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as _sum, row_number
from pyspark.sql.window import Window

spark = SparkSession.builder.getOrCreate()

# sample schemas: orders(customer_id, region, revenue)
orders = spark.read.parquet("/mnt/data/orders.parquet")

# compute revenue per customer per region
rev = orders.groupBy("region", "customer_id").agg(_sum("revenue").alias("total_revenue"))

# window to rank per region
w = Window.partitionBy("region").orderBy(rev["total_revenue"].desc())
top3 = rev.withColumn("rank", row_number().over(w)).filter("rank <= 3").orderBy("region", "rank")

top3.show(truncate=False)
```

**Explanation:** Aggregate first, then use a window `row_number()` partitioned by `region` to pick top 3.

---

# 7. Partitioning vs Bucketing in PySpark

* **Partitioning**: splits data into separate folders based on column values (e.g., `.../region=US/`). Good for pruning at read time. Works at file-system level. Fast for selective queries on partition columns.
* **Bucketing**: groups data into fixed number of files (buckets) based on a hash of a column. Stored in table metadata (Hive/Delta). Good for efficient joins on bucketed columns because matching buckets can be joined without shuffle (when both tables use same bucket count & column).

**Summary table:**

* Partitioning → reduces file scan via folder pruning; good for high-cardinality? typically low- to medium-cardinality.
* Bucketing → reduces shuffle for joins when properly aligned; requires planning.

---

# 8. Implementing Slowly Changing Dimensions (SCD)

Common types:

* **SCD Type 1**: overwrite attribute (no history).
* **SCD Type 2**: keep full history (add new row, set `effective_from`, `effective_to`, `is_current`).
* **SCD Type 3**: keep limited history in columns (prev\_value column).

**SCD Type 2 pattern (pseudocode):**

1. Identify incoming rows (staging) and existing dimension rows.
2. For changed attributes:

   * Update existing row `is_current = false` and set `effective_to`.
   * Insert new row with updated attributes, `is_current = true`, new `effective_from`.
3. Insert new business keys that don’t exist.

**PySpark example (simplified):**

```python
from pyspark.sql.functions import lit, current_timestamp

stg = spark.table("staging_customers")
dim = spark.table("dim_customers")  # has customer_id, attr..., is_current, effective_from, effective_to

# find changed rows by joining keys and comparing attributes (left as exercise)
# then update dim by marking old rows non-current and inserting new current rows.
```

**Explanation:** Use `MERGE` into Delta Lake (preferred) for atomic SCD 2 operations — `MERGE` lets you update matched rows and insert new rows in the same operation.

---

# 9. Star schema vs Snowflake schema

* **Star schema**: central fact table joined to denormalized dimension tables (flat). Simpler, faster for queries/BI.
* **Snowflake schema**: dimensions normalized into multiple related tables (hierarchies normalized). Saves storage but complicates joins and queries.

**When to use:**

* Use star for BI/reporting performance.
* Use snowflake if you need strict normalization to avoid redundancy or maintain complex hierarchies.

---

# 10. Designing a fact table for e-commerce

**Key elements:**

* Grain: define lowest-level event (e.g., one row = one order line item).
* Keys: `order_id`, `order_line_id`, `product_id`, `customer_id`, `time_id`, `promotion_id`.
* Measures: `quantity`, `unit_price`, `discount`, `line_total`, `cost`.
* Foreign keys to dimensions: `dim_product`, `dim_customer`, `dim_time`, `dim_store`.
* Add surrogate keys, partition by `time_id` or `order_date`, cluster or sort by `customer_id` for query performance.

**Example (columns):** `fact_order_line(order_line_sk, order_sk, product_sk, customer_sk, time_sk, quantity, unit_price, discount_amt, line_revenue)`

---

# 11. Build ETL pipeline with Azure Data Factory (ADF)

High-level steps:

1. **Ingest**: Use Copy Activity to move files from sources (on-prem, APIs, blob, ADLS).
2. **Transform**: Use Mapping Data Flows or Databricks (Notebook) activity for complex transforms.
3. **Orchestration**: Create ADF pipelines with activities, Set up parameters, variables.
4. **Scheduling/Triggers**: time, event, or custom triggers.
5. **Monitoring**: Configure alerts and use ADF monitoring UI.
6. **CI/CD**: Use ARM templates / Git integration.

**Example pipeline:** Ingest raw CSV → Databricks notebook to clean/transform → Write to Delta in ADLS → Load into Synapse dedicated pool or serverless for reporting.

---

# 12. ADF trigger types and use cases

* **Schedule trigger**: run pipeline on a schedule (cron-like). Use for nightly batches.
* **Tumblr?** (typo) — likely meant **Tumbling window trigger**: for periodic, windowed runs with retry/late arrival handling. Use for time-sliced processing (e.g., hourly windows).
* **Event trigger**: responds to storage events (Blob create). Use for file arrival.
* **Manual/On-demand**: start pipeline manually or via REST API.

**When to use:** If you need windowed, consistent processing with watermarks use Tumbling Window; for ad-hoc or dev use manual; for file-driven ingestion use event triggers; for simple periodic runs use schedule triggers.

---

# 13. Azure Databricks architecture & Delta Lake integration

**Databricks core pieces:**

* **Workspace** (notebooks, jobs).
* **Clusters**: managed Spark clusters.
* **Jobs**: scheduled runs.
* **Repos/CI** integration.

**Delta Lake integration:**

* Delta is a storage layer (on ADLS / Blob) that adds ACID transactions, schema enforcement/evolution, time travel, and performant upserts/merges.
* Databricks reads/writes Delta tables with `spark.read.format("delta")` and `delta`-optimized operations (`MERGE INTO`, `OPTIMIZE`, `VACUUM`).
* Databricks + Delta supports efficient ETL, streaming + batch (unified), and SCD implementations via `MERGE`.

---

# 14. PySpark — streaming from Event Hub in Databricks

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, DoubleType, TimestampType

spark = SparkSession.builder.getOrCreate()

ehConf = {
  "eventhubs.connectionString": "<EVENT_HUBS_CONNECTION_STRING>"
}

raw = spark.readStream.format("eventhubs").options(**ehConf).load()

# Event Hubs body is binary; decode JSON payload
schema = StructType().add("order_id", StringType()).add("amount", DoubleType()).add("created_at", TimestampType())

df = raw.selectExpr("cast(body as string) as json_str") \
        .select(from_json(col("json_str"), schema).alias("data")) \
        .select("data.*")

# Write to Delta table
df.writeStream \
  .format("delta") \
  .outputMode("append") \
  .option("checkpointLocation", "/mnt/delta/checkpoints/eventhub") \
  .start("/mnt/delta/streaming_orders")
```

**Explanation:** Use the Event Hubs connector; decode `body` then write to Delta with checkpointing for fault tolerance.

---

# 15. Optimize query performance in Azure Synapse Analytics

Key tactics:

* Use proper distribution (`HASH` on join key) for dedicated SQL pool.
* Choose proper indexing (clustered columnstore index for large fact tables).
* Use statistics and `CREATE STATISTICS` for optimizer.
* Avoid `SELECT *`; push predicates early; use partition elimination.
* Materialized views for expensive aggregations.
* Move transformations into dedicated pools only when necessary; use serverless for ad-hoc exploration.
* Use resource classes and workload isolation.

---

# 16. Design a data warehouse for retail in Synapse

High-level design:

* **Landing zone** (ADLS) → raw files.
* **Bronze** (raw Delta tables).
* **Silver** (cleaned/joined tables).
* **Gold** (aggregated fact & dimensional models).
* Use Synapse dedicated pool for curated star-schema star facts and reporting. Partition facts by date and distribute by customer/product for joins. Use dimensional tables (product, store, time). Set retention & archival policies.

---

# 17. Best practices securing data in ADLS

* Use **RBAC** and POSIX ACLs (ABFS) to limit access.
* Use **Azure AD** authentication and managed identities.
* Encrypt data at rest (Azure-managed keys) and optionally customer-managed keys (CMK).
* Secure network: secure endpoints via virtual network service endpoints or private endpoints.
* Audit access logs, enable diagnostic logs.
* Use firewall rules, NSG, and restrict storage account access.
* Scan data for sensitive info (Purview) and mask PII.

---

# 18. Access control and secrets with Azure Key Vault

* Store secrets, keys, and certificates in Key Vault.
* Grant ADF, Databricks, Synapse managed identities access via Key Vault access policies or RBAC.
* Use Key Vault-backed linked services (ADF) or Databricks Secret Scopes to retrieve secrets at runtime.
* Rotate keys/secrets and monitor access logs.
* Use managed identities (no hardcoded keys) for secure service-to-service authentication.

---

# 19. PySpark — load data from ADLS into a Delta table

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

# Read CSV from ADLS (assuming credentials are configured / mounted)
df = spark.read.option("header", True).csv("abfss://container@account.dfs.core.windows.net/path/data.csv")

# Write to Delta
df.write.format("delta").mode("overwrite").save("/mnt/delta/my_table")

# Optionally register in metastore
spark.sql("CREATE TABLE IF NOT EXISTS my_db.my_table USING DELTA LOCATION '/mnt/delta/my_table'")
```

**Explanation:** Use ABFS paths or mount ADLS into Databricks and write Delta for ACID and efficient reads.

---

# 20. Data lineage & governance in Microsoft Purview

* **Scan** data sources (ADLS, Synapse, SQL DB) with Purview scanners to build catalog and metadata.
* **Classify** sensitive data using built-in classifiers (PII, etc.).
* **Lineage**: Purview collects automated lineage from supported sources (e.g., Synapse, ADF, Databricks when integrated) and shows data flow.
* **Business glossary** and asset tagging to standardize definitions.
* **Access policies** and integration with Azure RBAC for governance.

---

# 21. Real-time analytics pipeline: Event Hub → Stream Analytics → Synapse

Flow:

1. **Event Hub** ingests event streams.
2. **Stream Analytics job** reads from Event Hub, performs windowed aggregations and outputs to Synapse (or Power BI).
3. **Synapse** stores results in dedicated pools or sinks into ADLS for analytics.

**Components:** Use Stream Analytics outputs: Synapse dedicated SQL pool (for reporting) or blob/ADLS then Synapse external tables.

---

# 22. Handling late-arriving data in batch ETL

* Implement **watermarking** and window-late logic when possible.
* Use **reprocessing** by re-running historical windows (idempotent loads).
* Maintain **staging** and process with `MERGE` (Delta) to upsert late records.
* Track `ingestion_time` and `event_time` and maintain a lateness threshold; backfill data beyond threshold with manual processes.

---

# 23. SQL — customer churn rate over last 6 months

Churn rate = (churned\_customers / active\_customers at start) \* 100. Example assumes `events` table with `customer_id`, `event_date`, `event_type` ('purchase' or 'no\_purchase') or use last activity.

```sql
WITH last_6m AS (
  SELECT customer_id,
         MAX(activity_date) AS last_activity
  FROM customer_activity
  WHERE activity_date >= DATEADD(month, -6, CURRENT_DATE)
  GROUP BY customer_id
),
churned AS (
  SELECT customer_id
  FROM last_6m
  WHERE last_activity < DATEADD(month, -1, CURRENT_DATE)  -- example churn definition
)
SELECT
  (SELECT COUNT(*) FROM churned) * 100.0 / (SELECT COUNT(*) FROM last_6m) AS churn_pct;
```

**Explanation:** Define churn carefully (e.g., no activity in last N days). Adjust timeframe per business rules.

---

# 24. Incremental loading in ADF

Methods:

* **Watermark column** (e.g., `modified_at`) stored in metadata table or pipeline variable; query source `WHERE modified_at > last_watermark`.
* **Change data capture (CDC)** where supported (SQL CDC).
* **Tumbling window** with watermark for time-based batches.
* **Lookup & incremental copy** pattern: ADF Lookup gets last watermark; Copy activity uses query with watermark.

**Example flow:** Pipeline reads watermark from control table → Copy activity with query `WHERE modified_at > @lastWatermark` → Update watermark after successful copy.

---

# 25. Python script to validate data quality and detect anomalies

Using `pandas` and simple checks; for anomalies, use z-score or isolation forest.

```python
import pandas as pd
from sklearn.ensemble import IsolationForest
import numpy as np

df = pd.read_csv("data.csv")

# Basic checks
null_counts = df.isnull().sum()
duplicates = df.duplicated().sum()
print("Nulls:\n", null_counts)
print("Duplicates:", duplicates)

# Numeric range check
assert df['price'].between(0, 10000).all(), "Price out of range"

# Anomaly detection on numeric columns
num = df.select_dtypes(include=[np.number]).fillna(0)
clf = IsolationForest(random_state=42, contamination=0.01).fit(num)
df['anomaly'] = clf.predict(num)  # -1 anomaly, 1 normal
anomalies = df[df['anomaly'] == -1]
print("Anomalies found:", len(anomalies))
```

**Explanation:** Combine schema checks, null/duplicate detection, domain/range validations and ML-based anomaly detection.

---

# 26. Schema evolution in Delta Lake

Delta supports schema evolution and enforcement:

* Use `mergeSchema` or `overwriteSchema` options when writing to allow new columns.
* Example `df.write.format("delta").mode("append").option("mergeSchema", "true").save(path)`.
* Use `ALTER TABLE ... ADD COLUMNS` for explicit schema change in metastore.

**Caution:** Evolve columns carefully; avoid silent type changes that break consumers.

---

# 27. Pipeline to handle batch + streaming

Use **Lambda / Unified (Kappa) architecture**:

* **Unified**: Prefer a single system (Databricks + Delta) for both streaming and batch (Delta + Structured Streaming + Batch jobs).
* Ingest streaming data into a raw Delta table (append). Use streaming jobs to compute near-real-time aggregates and batch jobs to recompute historical aggregates or fix late data.
* Design idempotent writes and use `MERGE` for correctness.

**Example:** Event hub → streaming write to `bronze` Delta → continuous streaming transform to `silver` → batch job runs periodically to reconcile and compact.

---

# 28. PySpark — window functions to rank sales

```python
from pyspark.sql.functions import row_number, rank, dense_rank, sum as _sum, col
from pyspark.sql.window import Window

sales = spark.table("sales")  # columns: sale_date, store_id, product_id, revenue

w = Window.partitionBy("store_id").orderBy(col("revenue").desc())

sales_with_rank = sales.withColumn("row_num", row_number().over(w)) \
                       .withColumn("rank", rank().over(w)) \
                       .withColumn("dense_rank", dense_rank().over(w))

sales_with_rank.filter("row_num <= 10").show()
```

**Explanation:** `row_number()` gives unique position, `rank()` leaves gaps for ties, `dense_rank()` does not.

---

# 29. Optimize storage & query performance in Synapse dedicated pool

* Use **hashed distribution** for large fact tables on join keys.
* Use **clustered columnstore indexes** for large analytics tables.
* Partition large tables (date-based).
* Use materialized views for heavy aggregations.
* Compress data and avoid small files; control distribution skew.
* Monitor query plan via `EXPLAIN` and tune statistics.

---

# 30. End-to-end pipeline: multiple sources → Databricks → Synapse

High-level blueprint:

1. **Ingest**: Use ADF or Event Hub to ingest files and streaming data into ADLS Gen2 (bronze).
2. **Transform** in Databricks:

   * Use Delta tables for bronze → silver → gold layers.
   * Use notebooks or jobs; implement SCD via Delta `MERGE`.
   * Use partitioning and `OPTIMIZE` where needed.
3. **Load into Synapse**:

   * For reporting, either copy curated gold tables into Synapse dedicated pool (via PolyBase or ADF Copy activity) or expose via serverless SQL pools over ADLS.
   * Use dedicated distribution & indexes for analytics.
4. **Orchestration**: Use ADF or Databricks Jobs to orchestrate runs; CI/CD via DevOps.
5. **Monitoring & Governance**: Purview for lineage; Monitor via Databricks and Synapse monitoring tools.
6. **Security**: Managed identities, Key Vault for secrets, private endpoints.

**Concrete example flow:**

* ADF pipeline: Copy API → ADLS `/raw/`
* Databricks Notebook Job: Read `/raw/` → transform → write Delta `/delta/gold/orders`
* ADF Copy: read `/delta/gold/orders` → write to Synapse dedicated pool table `dbo.fact_orders`
* Expose `fact_orders` to Power BI for reports.

---