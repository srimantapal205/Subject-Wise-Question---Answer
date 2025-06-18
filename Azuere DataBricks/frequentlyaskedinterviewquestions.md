Here are **frequently asked interview questions and answers on Databricks** tailored for a **Data Engineer** role. These questions cover practical scenarios, architecture, Spark optimizations, integrations, and real-world usage in a production environment.

---

### ✅ **Databricks Interview Questions & Answers for Data Engineers**

---

### **1. What is Databricks? How is it different from Apache Spark?**

**Answer:**
Databricks is a unified data analytics platform built on top of Apache Spark. It provides collaborative notebooks, optimized Spark engine, ML lifecycle management (MLflow), Delta Lake support, and native integrations with Azure, AWS, and GCP.
Unlike raw Spark, Databricks offers simplified cluster management, version control, security, and performance enhancements.

---

### **2. How do you ingest data into Databricks from various sources?**

**Answer:**
Databricks supports ingestion via:

* Mounting Azure Data Lake (ADLS Gen2) or S3
* Using Auto Loader for continuous ingestion
* REST APIs
* Structured streaming
* JDBC connectors
* Databricks connectors for Snowflake, Kafka, Event Hubs, etc.

---

### **3. What is Delta Lake and how does it enhance data reliability in Databricks?**

**Answer:**
Delta Lake is an open-source storage layer that brings **ACID transactions**, **schema enforcement**, **time travel**, and **data versioning** to data lakes. In Databricks, it helps maintain consistency, enables rollbacks, and supports efficient upserts and deletes using `MERGE INTO`.

---

### **4. How would you implement Slowly Changing Dimensions (SCD) Type 1/2 in Databricks?**

**Answer:**
Use **Delta Lake’s `MERGE INTO`** for SCD implementation:

* **Type 1**: Overwrite existing records using `UPDATE`.
* **Type 2**: Use `MERGE` with `INSERT` for new rows and `UPDATE` to mark existing rows as historical (`IsCurrent = false`, `EndDate` set).

---

### **5. Explain the differences between Databricks Jobs, Notebooks, and Workflows.**

**Answer:**

* **Notebooks**: Interactive development interface (supports Python, SQL, Scala).
* **Jobs**: Scheduled or triggered tasks that run Notebooks or JARs.
* **Workflows**: Orchestration feature (like Airflow) to chain multiple jobs with dependencies, parameters, and retries.

---

### **6. What are the benefits of using Databricks Auto Loader?**

**Answer:**

* Efficient incremental ingestion from cloud storage.
* Automatically detects and processes new files.
* Supports schema evolution and error handling.
* Scalable and fault-tolerant (uses checkpointing and file notification APIs).

---

### **7. How do you handle schema evolution in Delta Lake?**

**Answer:**
Use `MERGE` or `WRITE` options with:

```python
.option("mergeSchema", "true")
```

Or use `ALTER TABLE` to explicitly evolve schema. Delta ensures consistency and tracks changes.

---

### **8. What is Z-Ordering in Databricks Delta?**

**Answer:**
Z-Ordering is a multi-dimensional clustering technique that optimizes file layout to improve **query performance** by colocating related information in the same set of files. Use `OPTIMIZE ... ZORDER BY (col1, col2)`.

---

### **9. What are best practices for partitioning in Databricks?**

**Answer:**

* Partition by columns with **high cardinality but limited range** (e.g., `year`, `month`, `region`).
* Avoid too many small files (over-partitioning).
* Use `OPTIMIZE` and `VACUUM` for file management.

---

### **10. How do you tune Spark performance in Databricks?**

**Answer:**

* Use **Delta Lake** to reduce shuffling and optimize file sizes.
* Apply **caching** with `.cache()` or `.persist()`.
* Tune `spark.sql.shuffle.partitions` and `spark.executor.memory`.
* Use **broadcast joins** for small dimension tables.
* Monitor jobs in **Spark UI**.

---

### **11. What is the difference between a managed and unmanaged table in Databricks?**

**Answer:**

* **Managed table**: Databricks manages both data and metadata.
* **Unmanaged table**: Only metadata is managed; data stays at specified location (like ADLS or S3).

---

### **12. How do you perform streaming ETL in Databricks?**

**Answer:**
Use `readStream` and `writeStream` APIs with sources like Kafka, Event Hub, or Auto Loader, and sinks like Delta, Kafka, or SQL DB. Leverage watermarking, checkpointing, and structured streaming.

---

### **13. How does Databricks handle security and access control?**

**Answer:**

* Integration with **Azure Active Directory (AAD)**.
* Fine-grained **access control** on notebooks, clusters, tables.
* **Unity Catalog** for centralized data governance (RBAC, lineage).
* Token-based or OAuth 2.0 for secure API access.

---

### **14. What is Unity Catalog in Databricks?**

**Answer:**
Unity Catalog is a unified governance solution for all data and AI assets in Databricks. It enables centralized access control, data lineage, audit logging, and cross-workspace sharing.

---

### **15. How do you handle error logging and monitoring in Databricks jobs?**

**Answer:**

* Use `try-except` blocks in notebooks.
* Enable job-level **alerts** and **email notifications**.
* Monitor via **Databricks job logs**, **Spark UI**, and **Azure Monitor**.
* Push logs to **Log Analytics** or **Splunk**.

---

### **16. How can you schedule and orchestrate data pipelines in Databricks?**

**Answer:**

* Use **Databricks Jobs + Workflows**.
* Trigger from **Azure Data Factory**, **Airflow**, or **Event Grid**.
* Implement dependencies, retries, and parameter passing.

---

### **17. How do you join two large datasets in Spark efficiently?**

**Answer:**

* Use **broadcast join** when one dataset is small.
* Repartition on join keys to avoid shuffling.
* Filter early, cache intermediate results.
* Consider **bucketing** or **Z-ordering**.

---

### **18. What is the function of the `%run` command in Databricks?**

**Answer:**
`%run ./path/to/notebook` is used to **import and execute another notebook**, sharing variables and context across notebooks in the same job.

---

### **19. Explain how checkpointing works in streaming pipelines.**

**Answer:**
Checkpointing stores metadata and progress (offsets) of streaming jobs in a persistent location (e.g., DBFS or ADLS), enabling fault tolerance and recovery after failure.

---

### **20. How do you handle late-arriving data in streaming jobs?**

**Answer:**
Use **watermarks** to set event-time thresholds:

```python
.withWatermark("eventTime", "15 minutes")
```

Allows handling of late data up to defined time without unbounded state growth.

---



### **21. How does Delta Lake ensure data consistency in concurrent write scenarios?**

**Answer:**
Delta Lake uses **Optimistic Concurrency Control (OCC)** to manage concurrent writes:

* Each write operation reads the latest snapshot and attempts a transaction.
* Before committing, Delta checks whether the data it read has changed.
* If it has, the transaction fails and must be retried.

Internally, Delta maintains a **transaction log** (`_delta_log`) with **JSON and checkpoint files**. This log tracks every commit, schema changes, and file operations, ensuring **ACID compliance**.

---

### **22. Explain how Auto Loader works internally. When should you use it over Structured Streaming?**

**Answer:**
Auto Loader is a **Databricks-optimized structured streaming source** for files. It uses:

* **File notification mode** (preferred, using cloud APIs like Azure Blob storage events or S3 events) or
* **Directory listing mode** (less performant, scans all files in a directory).

Auto Loader supports:

* **Incremental ingestion**
* **Schema evolution**
* **Scalability** to millions of files

Use Auto Loader over raw `readStream` when:

* You’re ingesting **large-scale file-based data**
* Want **automated schema detection and evolution**
* Need **exact-once semantics** and **checkpointing**

---

### **23. What is the significance of checkpointing and watermarking in a structured streaming pipeline? How do you configure them in Databricks?**

**Answer:**

* **Checkpointing** persists the state of a streaming query (e.g., offsets, intermediate state, schema), so it can recover from failure.
* **Watermarking** is used for **late data handling**; it allows the engine to **discard old state** and limit memory usage.

**Configuration:**

```python
streamDF \
  .withWatermark("event_time", "10 minutes") \
  .groupBy(window("event_time", "5 minutes")) \
  .count() \
  .writeStream \
  .format("delta") \
  .option("checkpointLocation", "/mnt/checkpoints/stream1") \
  .start("/mnt/delta/output")
```

This configuration enables state cleanup for data that’s more than 10 minutes late.

---

### **24. What happens internally when you run `OPTIMIZE` on a Delta table with Z-Ordering?**

**Answer:**

`OPTIMIZE` in Delta:

* **Compacts small files** into larger ones to reduce I/O and improve scan performance.
* **Z-Ordering** organizes data on disk by sorting on the specified columns using a **space-filling curve (Z-order curve)**.

This helps:

* Minimize **data skipping**.
* Improve **query performance** on filter columns (especially nested or repeated queries).

Example:

```sql
OPTIMIZE sales ZORDER BY (customer_id, product_id)
```

Files are rewritten and sorted so queries on `customer_id` or `product_id` can skip irrelevant files.

---

### **25. How do you implement data deduplication in Delta Lake with upserts?**

**Answer:**

Use `MERGE INTO` with a unique key and deduplication logic.

Example:

```sql
MERGE INTO target_table AS target
USING (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY id ORDER BY updated_at DESC) as rn
  FROM staging_table
) AS source
ON target.id = source.id
WHEN MATCHED AND source.rn = 1 THEN
  UPDATE SET target.name = source.name, ...
WHEN NOT MATCHED AND source.rn = 1 THEN
  INSERT (id, name, ...) VALUES (source.id, source.name, ...)
```

Here, only the **latest version** of each record is considered (`rn = 1`), ensuring deduplication during the merge.

---

### **26. What is the Unity Catalog and how does it improve data governance compared to legacy approaches in Databricks?**

**Answer:**

**Unity Catalog** provides:

* Centralized **data governance and access control**
* **Data lineage** across tables, columns, and notebooks
* **Fine-grained permissions** (table, column, row level)
* Unified **catalog and schema management** across all Databricks workspaces

Key differences from legacy (Hive Metastore):

* Unity Catalog uses **3-level namespace**: `catalog.schema.table` (vs. just `database.table`)
* Supports **attribute-based access control (ABAC)** and **audit logs**
* Manages **data sharing** via Databricks Clean Rooms

---

### **27. How would you handle schema drift in a semi-structured ingestion pipeline using Databricks?**

**Answer:**

Approach:

* Ingest with Auto Loader using:

```python
.option("cloudFiles.schemaEvolutionMode", "addNewColumns")
```

* Use `mergeSchema = true` when writing:

```python
.write \
.format("delta") \
.option("mergeSchema", "true") \
.save("/mnt/delta/table")
```

* Maintain schema versions and changes via **Delta Lake schema tracking** or **Unity Catalog audit logs**.

For unknown schemas (e.g., JSON or XML):

* Parse with `from_json()` and use `schema_of_json()` for dynamic schema detection.

---

### **28. Describe a Databricks pipeline you built. How did you optimize it for performance and reliability?**

**Answer:**

✅ **Pipeline Overview:**

* Source: IoT sensor data from Event Hub → Raw Bronze Table (Delta)
* Transformation: Cleansing, parsing, deduplication → Silver Table
* Aggregation: Hourly summaries and anomaly detection → Gold Table
* Sink: Power BI and alerting via Azure Functions

✅ **Optimizations:**

* Used **Auto Loader** for incremental ingest with checkpointing
* Enforced schema with `DataFrameReader.schema()` to prevent drift
* Applied `OPTIMIZE ZORDER` on filter columns
* Cached small lookup tables
* Used **cluster pools** and **job clusters** to reduce spin-up cost
* Enabled **monitoring with job metrics** and alerting on failure

✅ **Reliability Measures:**

* Retry logic in jobs
* Delta ACID transactions to avoid duplicates
* Data quality checks in each layer

---

### **29. What are common causes of small files in Delta Lake, and how do you handle them?**

**Answer:**

**Causes:**

* Too many partitions
* Frequent streaming micro-batches with small writes
* Parallelism with small files
* Multiple jobs/appends without compaction

**Solutions:**

* Use `OPTIMIZE` regularly:

```sql
OPTIMIZE delta.`/mnt/delta/table`
```

* Batch writes instead of per-record inserts
* Tune micro-batch sizes for streaming
* Use Auto Loader’s `trigger=once` for large file loads
* Monitor file count per partition and adjust partition strategy

---

### **30. What’s the difference between `.cache()`, `.persist()`, and broadcast variables in Spark? How do you use them in Databricks?**

**Answer:**

| Feature      | Description                                                                |
| ------------ | -------------------------------------------------------------------------- |
| `.cache()`   | Stores RDD/DataFrame in memory (default storage level: MEMORY\_AND\_DISK)  |
| `.persist()` | Allows choosing storage level (e.g., disk-only, memory-only, etc.)         |
| `broadcast`  | Distributes a read-only variable across all workers for efficient join use |

**Use Cases:**

* Cache large intermediate DataFrames reused in multiple steps.
* Use `broadcast()` for small dimension tables in joins:

```python
broadcast_dim = broadcast(dim_df)
fact_df.join(broadcast_dim, "key")
```

---

### ✅ **Q31. What is Full Load in Databricks? When is it used?**

**Answer:**
A **full load** replaces the **entire target dataset** with new data every time. It truncates or overwrites the target table.

📌 **Used when:**

* Initial load of historical data
* Target data is small
* No change tracking or update timestamp is available

---

**💡 Example (PySpark):**

```python
df = spark.read.format("csv").option("header", True).load("/mnt/source/data.csv")

df.write.mode("overwrite").format("delta").save("/mnt/delta/full_load_table")
```

**OR (SQL):**

```sql
CREATE OR REPLACE TABLE full_load_table AS
SELECT * FROM parquet.`/mnt/source/data/`
```

**⚠️ Considerations:**

* Time-consuming on large datasets
* Not efficient for frequent refreshes

---

### ✅ **Q32. What is Incremental Load in Databricks? How do you implement it?**

**Answer:**
**Incremental load** extracts only **new or modified records** since the last load, using a **watermark** column (like `last_modified`, `updated_at`, `created_date`).

📌 **Used when:**

* Source data is large
* There’s a column to track changes (e.g., timestamp or sequence ID)

---

**💡 Example (Last N Days - Incremental by Date):**

```python
from datetime import datetime, timedelta

today = datetime.today()
last_n_days = today - timedelta(days=1)
formatted_date = last_n_days.strftime('%Y-%m-%d')

incremental_df = spark.read.format("parquet") \
  .load("/mnt/source/table/") \
  .filter(f"last_modified >= '{formatted_date}'")
```

**💡 Writing to Delta Lake:**

```python
incremental_df.write.mode("append").format("delta").save("/mnt/delta/incremental_table")
```

---

### ✅ **Q33. What is Delta Load in Databricks? How is it different from Incremental Load?**

**Answer:**
**Delta Load** = **Incremental Load + Merge (Upsert/Delete)**
It uses **MERGE INTO** with Delta Lake to apply:

* INSERT for new records
* UPDATE for modified records
* DELETE (optional, based on business logic)

📌 **Used when:**

* You need **Change Data Capture (CDC)** behavior
* Maintain latest record state in target
* Support Slowly Changing Dimensions (SCD)

---

**💡 Example (Delta Upsert using `MERGE INTO`):**

```python
source_df = spark.read.format("parquet").load("/mnt/source/incremental")

source_df.createOrReplaceTempView("source")

spark.sql("""
MERGE INTO delta.`/mnt/delta/target_table` AS target
USING source AS src
ON target.id = src.id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
""")
```

**OR using PySpark API:**

```python
from delta.tables import DeltaTable

delta_target = DeltaTable.forPath(spark, "/mnt/delta/target_table")

(delta_target.alias("target")
 .merge(
    source_df.alias("src"),
    "target.id = src.id"
 )
 .whenMatchedUpdateAll()
 .whenNotMatchedInsertAll()
 .execute()
)
```

---

### 🔁 **Comparison Table**

| Feature        | Full Load              | Incremental Load                 | Delta Load / Upsert               |
| -------------- | ---------------------- | -------------------------------- | --------------------------------- |
| Refresh Type   | Replace entire dataset | Append only new/changed data     | Upsert (Insert + Update + Delete) |
| Use Case       | Initial loads          | When change tracking is possible | CDC, data sync between systems    |
| Performance    | Slow on large datasets | Fast and efficient               | Efficient and consistent          |
| Complexity     | Low                    | Medium                           | High (requires `MERGE`)           |
| Storage Format | Any (CSV, Parquet)     | Prefer Delta                     | **Delta Lake required**           |
| Real-time Use  | ❌ Not suitable         | ✅ Often used                     | ✅ Enterprise-grade pipelines      |

---

### ✅ **Q34. How do you track the last successful load for incremental/delta loads?**

**Answer:**

Common approaches:

* **Metadata table** (store last load timestamp)
* **Checkpoint file** (in streaming or Auto Loader)
* **Workflow variables** (ADF/Databricks Jobs)

**Example:**

```python
# Load max date from target table
last_loaded = spark.sql("SELECT MAX(last_updated) FROM target_table").collect()[0][0]

# Use in filter for new data
incremental_df = source_df.filter(f"last_updated > '{last_loaded}'")
```

---

### ✅ **Q35. How do you handle deleted records from the source in Delta Load?**

**Answer:**

If the source tracks deletions (via a flag like `is_deleted = true`), use conditional logic in `MERGE`.

**Example with Delete Clause:**

```sql
MERGE INTO delta.`/mnt/delta/target_table` AS target
USING source AS src
ON target.id = src.id
WHEN MATCHED AND src.is_deleted = true THEN DELETE
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
```

---
Here is a structured Q\&A format with the main questions and their follow-ups, along with concise and technically sound answers. This will help you in interviews focused on Spark and Databricks:

---

### **1. Explain the architecture of Spark, including the roles of driver, executors, DAGs, and SparkContext.**

**Answer:**
Spark follows a master-slave architecture. The **Driver** is the master that orchestrates the execution of jobs. It maintains the **SparkContext**, which connects to the cluster manager. **Executors** are worker nodes that run tasks and store data. Spark breaks a job into **DAGs (Directed Acyclic Graphs)** representing stages and tasks for execution.

**Follow-ups:**

* **How does the driver program handle task scheduling?**
  The driver constructs a logical plan (DAG), breaks it into stages based on data shuffling, and schedules tasks using a cluster manager (YARN, Mesos, or Standalone).

* **What happens when an executor fails during a task execution?**
  Spark reassigns the failed task to another executor. If enough retries fail, the stage or job fails depending on configuration (`spark.task.maxFailures`).

---

### **2. What are the advantages and disadvantages of Delta Tables?**

**Answer:**
**Advantages:** ACID transactions, scalable schema evolution, time travel, optimized performance using Z-order and compaction.
**Disadvantages:** Requires Delta Lake engine support; limited multi-cloud compatibility; larger metadata overhead.

**Follow-ups:**

* **How do Delta Tables handle large-scale data updates efficiently?**
  Using **copy-on-write** mechanism and Delta Log for tracking metadata, combined with **OPTIMIZE** and **ZORDER** operations.

* **What limitations do you face in a multi-cloud environment?**
  Delta Tables may face compatibility and performance issues due to variations in cloud storage APIs and metadata handling.

---

### **3. Explain Delta Time Travel and the purpose of the vacuum command.**

**Answer:**
Delta Time Travel lets you query a Delta Table at a previous version or timestamp using `VERSION AS OF` or `TIMESTAMP AS OF`.
**VACUUM** removes old files no longer in the Delta log to save space.

**Follow-ups:**

* **What happens if the vacuum command is not run periodically?**
  Storage costs increase and performance degrades due to growing obsolete files.

* **How do you configure retention periods for Delta tables?**
  Set `delta.deletedFileRetentionDuration` (default is 7 days) to define how long to retain obsolete files before VACUUM deletes them.

---

### **4. Differentiate between Schema Enforcement and Schema Evolution.**

**Answer:**
**Schema Enforcement** prevents incompatible data from being written.
**Schema Evolution** allows compatible changes (e.g., adding columns) to the schema automatically or manually.

**Follow-ups:**

* **Can Schema Evolution lead to data inconsistencies?**
  Yes, if not managed properly. Different schema versions can lead to confusion in downstream systems.

* **What are the implications of enabling schema auto-detection?**
  Auto-detection may lead to implicit and undesired schema changes, especially in semi-structured formats like JSON or Parquet.

---

### **5. What is Secret Scope, and how is it used in Databricks?**

**Answer:**
Secret Scopes store credentials securely in Databricks. They can be **Databricks-backed** or **Azure Key Vault-backed**.

**Follow-ups:**

* **How do you handle expired secrets in a production environment?**
  Use Key Vault-backed scopes with automatic secret rotation and monitoring alerts.

* **What are the differences between Azure Key Vault-backed and Databricks-backed Secret Scopes?**
  Key Vault-backed secrets are managed externally (more secure, auto-rotation), while Databricks-backed secrets are managed within the workspace and are static.

---

### **6. How do you use Spark UI to debug stages, tasks, and performance issues?**

**Answer:**
Spark UI provides detailed info on **DAGs**, **tasks**, **stages**, **executors**, **storage**, and **environment**. You can spot slow stages, skewed tasks, GC time, and memory usage.

**Follow-ups:**

* **How would you identify and resolve a shuffle spill in Spark UI?**
  Look at shuffle read/write metrics and spill size. Use techniques like repartitioning, using broadcast joins, or increasing executor memory.

* **What insights can you gather from the DAG visualization in Spark UI?**
  You can see stage dependencies, narrow vs wide transformations, and potential optimization points in execution flow.

---

### **7. How do you handle bad data in Databricks?**

**Answer:**
Use options like `badRecordsPath`, schema validation, and try-catch logic in notebooks. Route invalid records to **quarantine tables** for review.

**Follow-ups:**

* **How do quarantine tables ensure data quality in downstream pipelines?**
  They isolate bad records, preventing them from corrupting business logic or analytics.

* **What are the best practices for logging and monitoring bad data?**
  Use structured logging, capture metadata (file name, record count, error type), and monitor with tools like Azure Monitor or custom dashboards.

---

## **Technical Round 2**

### **1. Explain how Adaptive Query Execution (AQE) works in Databricks.**

**Answer:**
AQE dynamically optimizes query plans at runtime based on actual data statistics. It can change join strategies, coalesce shuffle partitions, and optimize skew joins.

**Follow-ups:**

* **How does AQE optimize join operations dynamically?**
  By converting shuffle joins to broadcast joins if small tables are detected during runtime.

* **What configuration parameters are critical for enabling AQE?**
  `spark.sql.adaptive.enabled`, `spark.sql.adaptive.coalescePartitions.enabled`, `spark.sql.adaptive.skewJoin.enabled`.

---

### **2. Describe the role of Dynamic Resource Allocation in Databricks.**

**Answer:**
It enables Spark to scale executors based on workload. Executors are added when load increases and removed during idle time.

**Follow-ups:**

* **How does resource allocation adjust with load increase?**
  Spark requests more executors from the cluster manager based on backlogged tasks.

* **What are the potential downsides of enabling dynamic resource allocation?**
  Cold start delays, executor loss due to aggressive scale-in, and potential job failure if minimum executors are too low.

---

### **3. What is the usage of Optimize and REORG commands in Databricks?**

**Answer:**
`OPTIMIZE` compacts small files and improves read performance. `REORG` is used to reorder files for better data skipping and clustering.

**Follow-ups:**

* **How does Optimize command improve query latency in Delta tables?**
  By reducing file fragmentation and enabling efficient predicate pushdown.

* **What are the limitations of the REORG command with large datasets?**
  It can be time-consuming, expensive, and may not scale well without proper partitioning.

---

### **4. How is Git version control implemented in Databricks?**

**Answer:**
Databricks notebooks can be linked to a Git provider (GitHub, Azure DevOps). Changes can be committed and version-controlled.

**Follow-ups:**

* **What challenges do you face when managing multiple notebooks in Git?**
  Merge conflicts, non-standard notebook formats, difficulty in diffing large notebooks.

* **How do you resolve merge conflicts in Databricks notebooks?**
  Use the raw source view (JSON), resolve conflicts manually, or collaborate via Git branches.

---

### **5. What causes data skewness in Spark, and how can it be resolved?**

**Answer:**
Skewness is caused by uneven distribution of keys during shuffle operations. Solutions include **salting**, **broadcast joins**, and **AQE**.

**Follow-ups:**

* **How do you identify skewed partitions?**
  Use Spark UI to inspect task execution time and data volume in partitions.

* **What are the performance trade-offs of using salting?**
  It adds complexity and requires extra logic to de-salt post-processing.

---

### **6. How do you decide the number of partitions for repartitioning data in Spark?**

**Answer:**
Base it on input data size and cluster resources. A good rule of thumb is **1 partition per 100-200MB** of data per core.

**Follow-ups:**

* **What metrics would you analyze to determine if your partitioning is effective?**
  Task execution time, data skew, shuffle size, and stage duration in Spark UI.

* **How does improper partitioning affect job performance?**
  Too few partitions cause underutilization; too many cause overhead and memory issues.

---

### **7. What causes Out of Memory (OOM) issues in Databricks, and how do you resolve them?**

**Answer:**
OOM issues arise from large shuffles, wide transformations, or improper caching. Solutions include increasing executor memory, caching wisely, or repartitioning data.

**Follow-ups:**

* **How do caching strategies impact memory management?**
  Over-caching can fill memory and evict necessary data; cache only reused data.

* **What role does the executor heap size play in preventing OOM errors?**
  It determines memory available for computation and caching. Set using `spark.executor.memory`.

---
