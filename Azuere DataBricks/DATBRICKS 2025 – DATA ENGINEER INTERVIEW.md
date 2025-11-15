
# ✅ **DATBRICKS 2025 – DATA ENGINEER INTERVIEW Q&A **

**All answers are updated to 2025 capabilities (Unity Catalog, Photon, Delta 3.0, DBRX, DLT, Workflows).**

---

### **1. What is Databricks Lakehouse Platform?**

### **Answer:**

Databricks Lakehouse combines **data lake + data warehouse** features in a **single platform** using **Delta Lake** as the storage layer.

### **Example:**

A retail company stores raw data in ADLS → Bronze → Silver → Gold.
Same data is used for:

* BI queries (Power BI, Databricks SQL Warehouse)
* ML models (customer churn)
* Streaming pipelines (real-time orders)

All from **one copy of the data**.

---

### **2. What is Unity Catalog? Why is it important?**

### **Answer:**

Unity Catalog (UC) is the **central governance layer** for Databricks providing:

* Centralized **security** (table/column/row/column masking)
* Centralized **lineage**
* Centralized **audit logging**
* **Shared metastore** across workspaces
* **Data discovery** with catalog → schema → table hierarchy

### Example:

```
catalog: ecommerce
schema: bronze
table: customer_raw
```

One governance model for **Spark, SQL, ML, and Workflows**.

---

### **3. Key differences between Managed Tables vs External Tables in Databricks?**

| Feature       | Managed Table            | External Table                            |
| ------------- | ------------------------ | ----------------------------------------- |
| Data Location | Controlled by Databricks | Stored externally (ADLS/S3)               |
| Drop Table    | Deletes metadata + data  | Deletes metadata only                     |
| Governance    | Full UC support          | Supported but location must be registered |
| Backup        | Harder                   | Easier since data external                |

### Example:

```
CREATE TABLE sales_gold.orders_managed (...) ;
CREATE TABLE sales_gold.orders_external LOCATION '/mnt/data/orders';
```

---

### **4. What is Delta Lake?**

### **Answer:**

Delta Lake is a **transactional storage layer** providing:

* ACID
* Time Travel
* Schema Enforcement
* Schema Evolution
* DML (MERGE/UPDATE/DELETE)
* Automatic file compaction + Z-ordering
* Streaming read/write support

---

### **5. What is Delta Lake Time Travel? Give example.**

### **Example SQL:**

```
SELECT * FROM orders VERSION AS OF 5;
SELECT * FROM orders TIMESTAMP AS OF "2025-01-01";
```

Usage:

* Recovery from corruption
* Compare historical data
* Roll back accidental deletes/updates

---

### **6. What is Delta Change Data Feed (CDF)?**

### **Answer:**

CDF tracks **row-level changes** (INSERT, UPDATE, DELETE) since last read.
Enabled with:

```
ALTER TABLE orders SET TBLPROPERTIES (delta.enableChangeDataFeed = true);
```

### Example Use:

ETL pipeline only loads changed rows into downstream Gold tables.

---

### **7. What is the difference between Auto Loader vs COPY INTO?**

| Feature        | Auto Loader        | COPY INTO                     |
| -------------- | ------------------ | ----------------------------- |
| Ingestion Type | Streaming or Batch | Batch only                    |
| Scalability    | Very high          | Medium                        |
| Tracking       | File metadata log  | Load history maintained       |
| Best For       | Large pipelines    | One-time or small batch loads |

### Example Auto Loader:

```
spark.readStream.format("cloudFiles")
.option("cloudFiles.format", "csv")
.load("/bronze/raw")
```

---

### **8. Explain Medallion Architecture (Bronze/Silver/Gold).**

### **Bronze:** Raw ingestion

### **Silver:** Cleaned + validated

### **Gold:** Business-ready (aggregated fact/dim tables)

### Example Gold Table:

```
fact_sales_daily
dim_customer
dim_product
```

---

### **9. What is Photon Engine?**

### **Answer:**

Photon is a **vectorized execution engine** built in **C++** for:

* Low latency SQL
* BI workloads
* ETL pipelines

It accelerates query execution in **Databricks SQL Warehouse**.

---

### **10. What is a SQL Warehouse in Databricks?**

### **Answer:**

A SQL Warehouse is a **compute cluster optimized for SQL analytics**.
Supports:

* Auto-suspend
* Auto-scaling
* Photon engine
* DBSQL dashboards, alerts

---

### **11. Explain Databricks Workflows (2025).**

### **Answer:**

Successor to ADF / Airflow.
Supports:

* Task orchestration
* Jobs scheduling
* Notebook + Python + SQL Task
* Dependency management
* Alerts & notifications
* Parameter passing
* Git integration

---

### **12. Difference between Jobs Cluster vs All-purpose Cluster**

| Feature          | Jobs Cluster   | All-purpose |
| ---------------- | -------------- | ----------- |
| Purpose          | ETL/production | Development |
| Auto-termination | Yes            | Optional    |
| Price            | Cheaper        | Expensive   |
| Reusability      | No             | Yes         |

---

### **13. What is DLT (Delta Live Tables)?**

### **Answer:**

DLT is a declarative ETL framework with features:

* Data quality rules (Expectations)
* Automated lineage
* Incremental compute
* Auto-orchestration
* Managed tables

### Example:

```
@dlt.table
def silver_orders():
    return dlt.read("bronze_orders")
            .withColumn("amount", col("qty") * col("price"))
```

---

### **14. Modes in DLT Pipeline**

* **Triggered Once**
* **Continuous**
* **Batch / Triggered**
* **Enhanced Autoscaling (2025)**

---

### **15. Compare dlt.table vs dlt.view**

| dlt.table         | dlt.view              |
| ----------------- | --------------------- |
| Materializes data | Logical only          |
| Stored in UC      | Not stored physically |

---

### **16. What is DBRX?**

### **Answer:**

DBRX is Databricks’ **Generative AI model** for:

* SQL generation
* Code transformation
* Data quality pattern detection
* Auto ETL generation

---

### **17. How does Databricks support Streaming ETL?**

Using:

* Delta Live Tables
* Structured Streaming
* Auto Loader
* Streaming Write to Delta
* State Store

### Example:

```
df.writeStream.format("delta")
  .outputMode("append")
  .trigger(once=True)
  .start("/silver/events")
```

---

### **18. Explain MERGE INTO in Delta Lake**

```
MERGE INTO target t
USING source s
ON t.order_id = s.order_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
```

Used for SCD Type 2, upserts.

---

### **19. What is OPTIMIZE in Delta?**

Compacts small files → big files.

```
OPTIMIZE sales ZORDER BY customer_id;
```

---

### **20. What is Z-Ordering?**

A multi-dimensional clustering technique.
Speeds up query filters.

---

### **21. What is Column Masking in Unity Catalog?**

```
CREATE MASKING POLICY mask_email AS
  (email STRING) RETURN
    CONCAT('xxx@', SPLIT(email, '@')[1])
```

---

### **22. What is Row-Level Security?**

```
CREATE FUNCTION rls() RETURN user() IN ("admin","manager");
```

---

### **23. How to handle Schema Drift?**

Using:

* Auto Loader schema evolution

```
.option("cloudFiles.inferColumnTypes", "true")
.option("cloudFiles.schemaLocation", "/schemas")
```

---

### **24. What is a Delta Live Table Expectation?**

```
@dlt.expect("valid_price", "price > 0")
```

Enforces data quality.

---

### **25. What is a Feature Store in Databricks?**

A centralized store to manage ML features with versioning and lineage.

---

### **26. What is Databricks Serverless SQL?**

No cluster management; Databricks auto-manages compute.
Faster + cheaper for BI.

---

### **27. What is Vector Search (2025)?**

Databricks built-in vector database for RAG pipelines.

---

### **28. What is Cluster Pool?**

Helps reduce cluster startup time.

---

### **29. What is MLflow?**

Tracks:

* experiments
* model versions
* parameters
* metrics

---

### **30. What are Table Constraints?**

```
ALTER TABLE sales ADD CONSTRAINT valid_amount CHECK (amount > 0);
```

---

### **31. What does “Data Lineage” show?**

Shows end-to-end flow:

* What read this table
* What wrote this table
* Notebooks involved
* ETL pipelines

---

### **32. Explain SCIM in Databricks**

Used to sync users & groups from Azure AD/Okta.

---

### **33. What are Lakehouse Monitoring Metrics?**

Alerts for:

* Pipeline failures
* Missing files
* Drift detection
* Quality failures

---

### **34. What is AI Functions in SQL (2025)?**

Example:

```
SELECT ai_summarize(description) FROM tickets;
```

---

### **35. What is a Deep Clone in Delta?**

```
CREATE OR REPLACE TABLE t_clone DEEP CLONE original;
```

Copies data + metadata.

---

### **36. What is Shallow Clone?**

Copies metadata only.

---

### **37. What is Python UDF vs Pandas UDF?**

| Python UDF  | Pandas UDF |
| ----------- | ---------- |
| Row-by-row  | Vectorized |
| Slow        | Faster     |
| Python only | Uses Arrow |

---

### **38. Explain Databricks Repos.**

Git integration for DevOps workflow (GitHub/Azure DevOps/Bitbucket).

---

### **39. What is Lakehouse Federation (2025)?**

Query MySQL, PostgreSQL, Snowflake directly from Databricks.
No data ingestion required.

---

### **40. What is Delta Sharing?**

Open protocol to share data across clouds/vendors securely.

---
Great — continuing with **Questions 41 to 120** (80 more questions) with detailed example answers.
This completes **120+ Databricks 2025 Data Engineer Interview Q&A**.

---
---

### **41. What is SCD Type 2 and how do you implement it in Delta?**

SCD Type 2 tracks full history of records.

### Example MERGE:

```sql
MERGE INTO dim_customer tgt
USING updates src
ON tgt.customer_id = src.customer_id AND tgt.current_flag = true
WHEN MATCHED AND tgt.hash <> src.hash THEN
  UPDATE SET current_flag = false, end_date = current_timestamp()
WHEN NOT MATCHED THEN
  INSERT (customer_id, name, hash, current_flag, start_date)
  VALUES (src.customer_id, src.name, src.hash, true, current_timestamp());
```

---

### **42. How do you detect schema drift in streaming pipelines?**

With Auto Loader:

```python
.option("cloudFiles.schemaLocation", "/mnt/schema")
.option("cloudFiles.inferColumnTypes", "true")
.option("mergeSchema", "true")
```

Databricks logs column drift to schema evolution history.

---

### **43. What is Databricks Asset Bundles (2025)?**

A packaging format for CI/CD that bundles:

* Notebooks
* Jobs
* Models
* DLT pipelines
* Permissions
* SQL objects

As a deployable unit (like Terraform module for Databricks).

---

### **44. What is a Unity Catalog Volume?**

A managed file system inside UC for:

* ML models
* Documents
* Feature files
* Unstructured data

Unlike tables, Volumes do not require Delta format.

---

### **45. How do you create a Volume?**

```sql
CREATE VOLUME finance.raw_data;
```

---

### **46. How do you access Volume files?**

```python
df = spark.read.csv("/Volumes/finance/raw_data/2025/*.csv")
```

---

### **47. What is a Databricks Cluster Policy?**

Rules that control:

* Max workers
* Node types
* Spark versions
* Access
* Tags

Used to enforce cost governance.

---

### **48. What is Credential Passthrough?**

Allows users to access ADLS/S3 using their own identity.

---

### **49. Difference between Mounting ADLS vs Direct Access?**

| Mounting               | Direct Access                      |
| ---------------------- | ---------------------------------- |
| Uses service principal | Uses ABAC (UC storage credentials) |
| Legacy                 | Recommended                        |
| Not compatible with UC | Compatible                         |

---

### **50. What is a Storage Credential in UC?**

A managed identity / service principal that UC uses to access cloud storage.

```sql
CREATE STORAGE CREDENTIAL my_sp
WITH AZURE_SERVICE_PRINCIPAL (client_id='xx', tenant_id='yy')
SECRET 'sp-secret';
```

---

### **51. What is an External Location in UC?**

Maps a cloud path to a credential.

```sql
CREATE EXTERNAL LOCATION ext_sales
URL 'abfss://raw@dlake.dfs.core.windows.net/sales'
WITH (STORAGE CREDENTIAL my_sp);
```

---

### **52. What is Delta Write Isolation Level?**

Delta uses **Serializable isolation** internally.
Ensures no conflicting writes.

---

### **53. What is Data Skipping?**

Delta stores min/max statistics in metadata → improves filtering.

---

### **54. Explain File Compaction in Delta Lake.**

Small files merged into large optimized Parquet files.

Triggered by:

```
OPTIMIZE table_name;
```

---

### **55. What is Dynamic File Pruning?**

Spark only reads files that match join/filter predicates.

---

### **56. What is a Delta Transaction Log (DeltaLog)?**

Located in `_delta_log/` folder. Stores:

* Commit logs
* Schema updates
* File additions/deletions
* Stats
* CDF info

---

### **57. Explain Delta Log Structure**

Files:

* **00000.json** → first commit
* **00001.json** → next commit
* **00000.checkpoint.parquet** every 10 commits

---

### **58. How do you read the Delta log manually?**

```python
spark.read.json("/path/_delta_log/*.json").show()
```

---

### **59. How to optimize Delta for Streaming Writes?**

* Use Auto Optimize
* Enable Liquid Clustering (2025)
* Avoid `merge` in streaming
* Use Trigger Available Now

---

### **60. What is Liquid Clustering (2025)?**

New clustering method replacing Z-order.
Automatically reorganizes data for large tables.

---

### **61. How do you enable Liquid Clustering?**

```sql
ALTER TABLE sales
SET TBLPROPERTIES ('delta.liquidClustering.enabled' = true);
```

---

### **62. What is a Predictive Optimizer (2025)?**

Databricks ML-powered optimizer that adjusts:

* File sizes
* Clustering
* Cache usage
* Job scheduling

Automatically monitors workloads.

---

### **63. Explain Photon Vectorized Execution**

Uses SIMD CPU instructions → faster operations for:

* Filters
* Aggregations
* Sorting
* Joins

---

### **64. What is Adaptive Query Execution (AQE)?**

Dynamic execution plan adjustments:

* Join reordering
* Changing join type
* Skew handling
* Coalesce shuffle partitions

---

### **65. What is Join Skew Optimization?**

Spark optimizes skewed data by:

* Splitting large partitions
* Broadcasting small partitions
* Using AQE

---

### **66. How to handle skew?**

* `broadcast()`
* Salting
* Range partitioning
* AQE

---

### **67. Explain Autotune (2025)**

Databricks automatically tunes:

* Shuffle partitions
* Cache settings
* Cluster size
* Delta clustering
* Photon acceleration

---

### **68. What is Serverless Workflows (2025)?**

Run jobs without managing clusters.
Pay per second execution.

---

### **69. Difference: Databricks Workflow vs DLT**

| Workflow             | DLT                   |
| -------------------- | --------------------- |
| Orchestration        | ETL & quality         |
| Any task             | Table pipelines only  |
| No auto expectations | Supports expectations |

---

### **70. How to schedule a notebook in Workflows?**

UI → Workflows → New job → Add Notebook task.

---

### **71. How to create Job Parameters?**

In job config:

```
job_cluster_id={{cluster_id}}
date={{ds}}
```

In notebook:

```python
dbutils.widgets.get("date")
```

---

### **72. What are SQL Alerts?**

Trigger on:

* Low sales
* Missing data
* Late batch
* Failed KPIs

---

### **73. What is a SQL Endpoint?**

Legacy term for SQL Warehouse before 2024.

---

### **74. What is Data Observability?**

Monitoring data for:

* Freshness
* Volume anomalies
* Schema drift
* Quality errors

---

### **75. How to implement Data Quality Rules?**

Using DLT expectations or SQL constraints.

---

### **76. Example Quality Rule in SQL**

```sql
ALTER TABLE sales
ADD CONSTRAINT positive_amount CHECK (amount > 0);
```

---

### **77. Example Quality Rule in DLT**

```python
@dlt.expect_or_drop("valid_price", "price > 0")
```

---

### **78. What is Auto Optimize?**

Automatically:

* Compacts files
* Z-orders
* Writes optimized parquet blocks

---

### **79. How do you enable Auto Optimize?**

```
SET spark.databricks.delta.optimizeWrite.enabled=true;
```

---

### **80. What is Databricks SQL Functions 2025?**

Examples:

* `ai_summarize()`
* `ai_gen()`
* `vector_similarity()`
* `array_distinct()`

---

### **81. What is MLflow Model Registry?**

Stores:

* Staging
* Production
* Archived model versions

---

### **82. What is Feature Engineering in Databricks?**

Builds:

* Feature tables
* Lookup tables
* Encodings
* Aggregations

---

### **83. Explain Vector Search Index**

Used for RAG.
Example:

```sql
CREATE VECTOR INDEX idx_desc
ON product_embeddings (embedding);
```

---

### **84. What is Delta Live Metrics?**

Shows:

* Input rows
* Output rows
* Failed expectations
* Backfill progress

---

### **85. Example Streaming Autoloader Code**

```python
spark.readStream.format("cloudFiles")
  .option("cloudFiles.format", "json")
  .load("/raw")
```

---

### **86. Explain Trigger.AvailableNow (Structured Streaming)**

Runs once and exits after processing all available data.

---

### **87. How does Checkpointing work?**

Stores:

* Offsets
* State store
* Commit logs

---

### **88. What is a State Store in Streaming?**

Used for aggregations, joins.

---

### **89. Sliding Window vs Tumbling Window**

Tumbling → fixed non-overlapping
Sliding → overlapping

---

### **90. Example Window Aggregation**

```sql
SELECT window(timestamp, "10 minutes"), SUM(amount)
FROM transactions
GROUP BY window(timestamp, "10 minutes")
```

---

### **91. How to read a table in streaming mode?**

```
spark.readStream.table("silver.sales")
```

---

### **92. How to write a streaming Delta table?**

```
df.writeStream
  .format("delta")
  .outputMode("append")
  .table("silver.events")
```

---

### **93. When to use Append vs Merge in streaming?**

Append → inserts
Merge → updates/deletes (SCD2)

---

### **94. What is the Databricks Marketplace?**

Marketplace for:

* Datasets
* Models
* Dashboards
* Notebooks

---

### **95. How to publish a Dataset to Marketplace?**

Databricks workspace → Marketplace → Publish → Choose UC table.

---

### **96. What is Workflows Task Retry?**

Automatically retries tasks on failure.

---

### **97. What are Cluster Tags?**

Help track billing by:

* Department
* Cost center
* Project

---

### **98. What is Table Versioning?**

Each Delta commit increases version:

```
DESCRIBE HISTORY sales;
```

---

### **99. What is Delta Vacuum?**

Removes old data files.

```
VACUUM sales RETAIN 168 HOURS;
```

---

### **100. What is Enhanced Autoscaling?**

Adds/removes nodes dynamically for SQL Warehouse.

---

### **101. Explain Broadcast Hash Join**

Broadcasts small dataset to all nodes.

---

### **102. How to force broadcast join?**

```
SELECT /*+ BROADCAST(b) */ * FROM a JOIN b;
```

---

### **103. What is Shuffle Hash Join?**

Both tables are partitioned and shuffled before join.

---

### **104. What is Sort Merge Join?**

Default join for large tables.

---

### **105. How to view Spark UI?**

Cluster → Spark UI tab → Jobs, Stages, SQL, DAG visualization.

---

### **106. What is Job Run Trace?**

Shows lineage of:

* Notebooks
* Tables
* Tasks

---

### **107. What is DBFS?**

Databricks File System — abstraction over cloud storage.

---

### **108. How to list DBFS files?**

```
%fs ls /mnt/raw
```

---

### **109. How to mount ADLS in DBFS?**

(legacy mode — not recommended for UC)

```
dbutils.fs.mount()
```

---

### **110. What is Databricks Connect 2025?**

Run local PySpark code directly on Databricks compute.

---

### **111. What is Delta Cache?**

Caches frequently accessed data for faster reads.

---

### **112. Difference: Spark Cache vs Delta Cache**

| Spark Cache | Delta Cache  |
| ----------- | ------------ |
| Memory only | SSD + memory |
| Per cluster | Per node     |

---

### **113. How to cache a table?**

```sql
CACHE SELECT * FROM sales;
```

---

### **114. What is Materialized View (2025)?**

Automatically refreshed SQL objects.

---

### **115. What is Query Profile?**

Shows performance breakdown for SQL query.

---

### **116. What is System Tables (Databricks 2025)?**

Tables for:

* Cost usage
* Job audit
* Query history
* Cluster logs

Example:

```
SELECT * FROM system.access.audit;
```

---

### **117. How to enable Query Watchdog?**

Prevents long-running/expensive queries.

---

### **118. What is Grant Revoke in Databricks UC?**

```
GRANT SELECT ON TABLE sales TO user bob;
```

---

### **119. What is Tokenization in Databricks?**

Mask sensitive values by replacing them with tokens.

---

### **120. What is Data Masking with UDF?**

```
CREATE FUNCTION mask(a STRING)
RETURN regexp_replace(a, '.+@', 'xxxx@');
```

---

### **121. Explain Unity Catalog’s Column-Level Lineage (2025)**

Shows where each column originated in the entire ETL chain.

---

### **122. What is Full Clone vs Incremental Clone (2025)?**

Full Clone → deep clone
Incremental Clone → only changed data since last clone

---

### **123. How to migrate Hive Metastore to UC?**

Use **Upgrade to Unity Catalog** wizard.

---

### **124. What is Refactor Notebook?**

Databricks AI restructures notebook into modular scripts.

---

### **125. What is DBRX SQL Agent?**

AI agent that:

* Fixes SQL queries
* Optimizes queries
* Generates ETL code

---

