# End-to-end Azure data pipeline — design, patterns, and operational details

This document describes a comprehensive end-to-end design to ingest multiple on-premises sources to Azure, transform and serve data for analytics/BI, plus operational patterns (late data, retries, backfill, idempotency), file-format unification in a Lakehouse, near-real-time vs batch choices, PySpark/Spark performance patterns, Azure components, security, CI/CD, monitoring, and common troubleshooting patterns.

---

## 1. High-level architecture (end-to-end)

**Logical data flow**:

1. **Source systems (on-prem)** — OLTP databases, application logs, files, message queues.
2. **Secure transport** — VPN/ExpressRoute & service endpoints / private endpoints.
3. **Ingest layer** — Ingest to Azure Data Lake Storage Gen2 (ADLS Gen2) or a staging area:

   * Batch: Azure Data Factory (ADF) or AzCopy / SFTP gateway.
   * Real-time: Azure Event Hubs or Apache Kafka (Confluent / Event Hubs) or Azure IoT Hub for device telemetry.
4. **Stream processing (optional near-real-time)** — Azure Stream Analytics or Spark Structured Streaming on Azure Databricks / Synapse Spark.
5. **Landing zone (raw)** — ADLS Gen2 container `raw/` (immutable, partitioned by arrival date + source).
6. **Bronze (cleaned)** — Minimal parsing, validation, schema tagging (Delta tables if using Databricks / Delta Lake).
7. **Silver (enriched)** — Joins, deduplication, conforming schemas, derived fields.
8. **Gold (aggregates / BI)** — Tables optimized for BI queries (partitioned, compacted), Synapse Serverless / Dedicated SQL Pools or Azure Synapse Analytics / Power BI semantic models.
9. **Serving/consumption** — Synapse SQL, Databricks SQL, Power BI, ADLS for ad hoc queries.

**Chosen Azure services (recommended)**

* **Ingest & Orchestration**: Azure Data Factory (ADF) — batch orchestration, scheduling, triggers.
* **Real-time ingestion**: Azure Event Hubs or Kafka + Databricks Structured Streaming.
* **Processing/Transform**: Azure Databricks (preferred for Spark), or Synapse Spark Pools.
* **Storage**: Azure Data Lake Storage Gen2 (ADLS Gen2) in hierarchical namespace with Delta Lake (Lakehouse).
* **Query/Serving**: Azure Synapse (Serverless SQL, Dedicated SQL Pools) and Databricks SQL; Power BI for visualization.
* **Security & IAM**: Azure AD, RBAC, ACLs, Private Endpoints, Managed Identities.
* **Monitoring**: Azure Monitor, Log Analytics, ADF monitoring, Databricks job metrics.
* **CI/CD**: Azure DevOps / GitHub Actions for repo + ARM/Bicep or Terraform for infra + Azure Resource Manager templates or Synapse/ADF pipeline CI.

---

## 2. Ingestion patterns and late data handling

### 2.1 Arrival types & ingestion

* **Batch files (CSV, JSON, Avro)**: ADF Copy Activity → ADLS Gen2 `raw/source=<name>/date=YYYY-MM-DD/` with filename including `ingest_ts`.
* **Database transactional changes**: Use Change Data Capture (CDC) with Azure Data Factory + Logstash/Change Data Capture to Event Hubs or Databricks Auto Loader (or Azure Data Factory + Azure SQL CDC connector) to land into delta.
* **Streaming telemetry**: Event Hubs → Structured Streaming → Delta append.

### 2.2 Handling late-arriving data (delayed by a few hours)

Principles: avoid data loss, ensure correctness, minimize reprocessing cost.

**Techniques**

1. **Watermarking (for stream processing)**

   * Use event-time watermark in Structured Streaming (e.g., `withWatermark("eventTime", "2 hours")`) to accept late events within a window and drop-after threshold.
2. **Design for idempotent writes**

   * Use upserts (MERGE) into Delta tables keyed by a business key + event timestamp. That allows reprocessing older events safely (updates overwrite).
3. **Partition by event date and ingestion date**

   * Maintain `event_date` partition and `ingest_date` (or `_partition_time`) to allow efficient reprocessing for late partitions.
4. **Late-data queue / staging**

   * Detect late batches (based on `event_time` < `current_time - threshold`) and route them to a `late/` area and trigger specialized reconciliation jobs to re-MERGE only the affected partitions.
5. **Reconciliation & compaction**

   * Periodic data quality job: compute counts/checksums by business key/time to detect differences and trigger reprocess/backfills.

**Concrete pipeline behavior**

* Primary ingestion job writes to `raw/` and triggers a transform job to `bronze/` (append).
* If transform job sees records with event times older than the target partition’s current watermark, it writes them to `late/` and issues a `MERGE` into bronze/silver for affected partitions.
* Maintain an **ingest metadata table** in a control database with `file_name`, `ingest_ts`, `status`, `row_count`, `business_min_event_ts`, `business_max_event_ts`. This table is used for dedupe/retry/backfill decisions.

### 2.3 Retry handling

* **At transport level**: use ADF retry policies (configurable retry count & intervals) for transient errors.
* **At application level**: implement exponential backoff + jitter in custom connectors.
* **Idempotent ingestion**: Use unique file IDs or event IDs; if a file/event is re-sent, detect duplicates via control table or by deduping when merging into Delta using latest `ingest_ts` or event version.
* **Poison message handling**: For streaming, redirect problematic messages to a dead-letter queue (DLQ) for manual inspection.

### 2.4 Backfill

* **Backfill design**:

  * Use ADF pipeline or Databricks job to reprocess historical partitions/files and write to a `reprocessed/` staging directory.
  * Use `MERGE` into Delta tables by business key and event timestamp to avoid duplicates/overwrite logic.
* **Safe-backfill steps**:

  1. Mark backfill run id in control table.
  2. Run transformations writing to `temp/backfill/run_id/`.
  3. Validate row counts/checksums against expected.
  4. MERGE into target (idempotent).
  5. Update control table with success/failed rows.

### 2.5 Idempotency patterns

* **Idempotent writes**: Use MERGE INTO with a unique key. Example:

  ```sql
  MERGE INTO target t
  USING source s
  ON t.pk = s.pk
  WHEN MATCHED AND s.event_ts > t.event_ts THEN UPDATE ...
  WHEN NOT MATCHED THEN INSERT ...
  ```
* **Deduplication during ingestion**: Use window functions in Spark to keep latest per key:

  ```python
  from pyspark.sql.window import Window
  w = Window.partitionBy("pk").orderBy(col("event_ts").desc(), col("ingest_ts").desc())
  deduped = source_df.withColumn("rn", row_number().over(w)).filter("rn = 1")
  ```
* **Write atomicity**: Use Delta Lake/ACID support or Synapse table with transactional semantics to prevent partial states.

---

## 3. Multiple source formats → unify & Lakehouse storage

### 3.1 Parsing & normalization

* **Ingest raw, keep original**: Save raw payload (original file or message) in `raw/` for replay/debug.
* **Schema registry**:

  * Use a schema registry (e.g., Confluent Schema Registry if Kafka/Event Hubs with Avro) or central JSON schema store for evolving schemas.
* **Normalization logic**:

  * A transformation layer (Databricks / Synapse Spark) reads raw, parses by format (CSV/JSON/Avro).
  * Use a canonical schema (common column names & types) or a polymorphic schema (logical columns plus `payload` for unstructured fields).
  * Emit a normalized parquet/delta record with fields: `source_name`, `source_record_key`, `event_ts`, `ingest_ts`, `payload_*` (structured), `raw_payload`.

### 3.2 File formats & Lakehouse choice

* **Landing raw**: Keep raw files in original format OR convert to Avro/Parquet for compactness. Avro is useful for schema evolution and compact row-oriented write; Parquet for columnar queries.
* **Bronze/Silver/Gold**: Use **Delta Lake** (Delta tables on ADLS Gen2) to get:

  * ACID transactions (MERGE, UPSERT)
  * Time travel (commit history)
  * Fine-grained compaction and optimize operations
* **Schema evolution**: Delta supports adding columns; for type changes you can use `CAST` in transforms and create new columns or migrate.

### 3.3 Example zone layout (ADLS Gen2)

```
/data/
  raw/
    sourceA/
      YYYY=2025/MM=10/DD=03/ file1.json
  bronze/
    sourceA_delta/
      event_date=2025-10-03/ _delta_log/ ...
  silver/
    customer_enriched_delta/
  gold/
    sales_aggregates_delta/
```

---

## 4. Near real-time ingestion vs batch ingestion (service choices & why)

### 4.1 Near real-time (sub-second to minutes)

* **Use**: Event Hubs (or Kafka) + Databricks Structured Streaming (or Synapse Spark Structured Streaming).
* **Why**:

  * Event Hubs: high throughput, partitioning, retention, integrates with Azure ecosystem.
  * Structured Streaming: declarative stream processing, can do exactly-once semantics with Delta Sink.
  * Delta Lake provides transactional atomic writes and streaming upserts.
* **Pattern**: Event Hubs → Spark Structured Streaming + `writeStream.format("delta")` with `.trigger(availableNow()/processingTime)` as needed → update Silver.

### 4.2 Micro-batch / batch (minutes to hours)

* **Use**: Azure Data Factory / Databricks jobs on scheduled triggers.
* **Why**:

  * Simple scheduling, parity with ETL patterns, cost-effective for lower frequency ingest.
  * ADF supports many connectors, built-in mapping data flows (if no Spark coding desired).
* **Pattern**: ADF Copy Activity → raw → Databricks/ADF mapping flows → merge into Silver/Gold.

### 4.3 Hybrid approach

* Use streaming for near-real-time requirements (critical metrics) and batch for bulk processing: maintain a **merge window** where both modes can write to same Delta table; use `writeStream` with `checkpointLocation` and `merge` to handle late data and idempotency.

---

## 5. Data engineering / Spark performance

### 5.1 Broadcast join vs Shuffle join (PySpark)

* **Broadcast join**:

  * When one side is small enough to fit in driver/executor memory (commonly < 100–200MB depending on cluster).
  * Spark broadcasts the small table to all executors avoiding shuffle.
  * **Pros**: Avoids expensive shuffle; faster for small×large join.
  * **Cons**: Memory pressure; not usable if small table is actually large; can OOM executors.
  * **When to use**: Dimension table joins in star schema (lookup tables).
  * **How to force**: `broadcast(small_df)` or set `spark.sql.autoBroadcastJoinThreshold`.
* **Shuffle join**:

  * Default for large×large joins: both sides are partitioned by join key and shuffled across cluster.
  * **Pros**: Scales to large datasets.
  * **Cons**: Expensive network IO; can suffer from skew and many small files.
  * **When to use**: When neither side fits memory.

**Example**

```python
from pyspark.sql.functions import broadcast
result = large_df.join(broadcast(small_df), "id")
```

### 5.2 Handling skew in data (concrete examples)

Skew happens when a small subset of keys holds a large fraction of data.

**Detection**:

* Run `df.groupBy("key").count().orderBy(desc("count")).show(20)`

**Mitigation techniques**:

1. **Salting** (add random prefix to highly skewed key)

   * For join: add `salt = randInt(0, N)` to skewed key on both tables: `key_salted = concat(key, "_", salt)` and then join on salted keys, finally aggregate/summarize and remove salt.
2. **Broadcast smaller side**:

   * If small dimension exists, broadcast it to avoid shuffle.
3. **Skewed key split**:

   * Separate skewed keys and process them independently:

     * `skewed = df.filter(col("key").isin(skew_keys))` — process with different parallelism.
     * `normal = df.filter(~col("key").isin(skew_keys))` — use regular join.
4. **Increase parallelism**:

   * Repartition on join key: `df.repartition(n, "join_key")` with higher `n`.
5. **AQE (Adaptive Query Execution)**:

   * Enables dynamic reduce of stages and auto skew handling (see next section).

**Concrete salting example**

```python
import pyspark.sql.functions as F
N = 10
left_salted = left_df.withColumn("salt", F.floor(F.rand()*N)).withColumn("join_key_salt", F.concat_ws("_", F.col("key"), F.col("salt")))
right_expanded = right_df.withColumn("salt", F.explode(F.array([F.lit(i) for i in range(N)]))).withColumn("join_key_salt", F.concat_ws("_", F.col("key"), F.col("salt")))
joined = left_salted.join(right_expanded, "join_key_salt")
```

### 5.3 Adaptive Query Execution (AQE)

* **What is it**: AQE is a runtime optimization in Spark that dynamically adjusts query plans based on runtime statistics (e.g., actual partition sizes, skew detection). Enabled in Spark 3.x.
* **Key features**:

  * **Dynamic partition coalescing**: reduce number of reducers if partitions are small.
  * **Handling skew**: splits skewed partitions and handles them differently.
  * **Switch join strategies**: change a broadcast/hash join to sort-merge join or vice versa at runtime.
* **When to use**:

  * Enable when queries have variable data distribution or unknown cardinalities; helps with joins and shuffles.
* **Settings**:

  * `spark.sql.adaptive.enabled = true`
  * `spark.sql.adaptive.coalescePartitions.enabled = true`
  * `spark.sql.adaptive.skewJoin.enabled = true`
* **Tradeoffs**:

  * Slight overhead for collecting runtime metrics, but usually improves stability and performance for large workloads.

### 5.4 Partitioning strategy in Spark / data lake

**Why partition**:

* Reduce data scanned, prune partitions, speed up queries.

**How to partition**:

* Partition by **high-cardinality**? No — avoid too many small files.
* Partition by **date** (event_date, ingestion_date) is typical.
* For slow-changing high-cardinality columns (e.g., user_id) avoid partitioning by them; use bucketing instead for joins.
* Combine partition columns (e.g., `year/month/day`) to keep directories manageable.
* Limit total number of files in a partition — target file sizes (e.g., 128MB to 512MB) for parquet/delta.

**Bucketing (or Z-Ordering / clustering)**:

* Use bucketing to colocate related rows to speed up joins (supported by Spark SQL). Delta supports Z-ordering (Databricks) for data skipping improvements.

**Example partition layout**:

* Partition by `event_date=YYYY-MM-DD` and cluster by `customer_id` (or Z-ORDER by `customer_id`) for queries filtered by date and customer.

**Best practices**

* Use `OPTIMIZE` (Databricks Delta) or compaction jobs to merge small files.
* Auto compact small files after many small writes (using Delta `optimize` or `VACUUM`).
* Use `repartition()` before writing to control output file sizes.

---

## 6. Azure / Cloud services specifics

### 6.1 What is Azure Data Factory (ADF)?

ADF is a cloud-based data integration orchestration service for building ETL/ELT pipelines.

**Key components**

* **Pipelines**: orchestrations containing activities (Copy, Data Flow, Databricks, Stored Procedure).
* **Linked Services**: connection definitions to compute and storage (e.g., ADLS Gen2, SQL DB, REST).
* **Datasets**: metadata representation of data structures in linked services (e.g., table or file path).
* **Activities**: tasks executed in pipelines (Copy, Execute Pipeline, Databricks Notebook, Mapping Data Flow).
* **Triggers**: schedule/event triggers (scheduled, tumbling window, event-based).
* **Integration Runtime**: compute environment for data movement and execution (Azure, self-hosted for on-prem).
* **Monitoring**: built-in monitoring UI, integration with logs.

### 6.2 Incremental load in ADF — one approach

**Change tracking via watermark column (timestamp-based)**:

1. Maintain a `watermark` table storing the last processed `max_event_ts` per source.
2. ADF pipeline:

   * Lookup activity to get `last_watermark`.
   * Copy activity (or Query) using `WHERE event_ts > @last_watermark` to fetch incremental rows.
   * Write to staging/raw.
   * Transform & MERGE into target.
   * Update watermark to new `max(event_ts)` from the processed batch.

**Alternative**: Use CDC connectors (SQL Server CDC → Event Hubs), or log-based CDC for near-real-time.

### 6.3 What is Azure Synapse? vs Azure SQL Data Warehouse

* **Azure Synapse Analytics**: Integrated analytics service combining big-data (Spark), data integration (pipelines), serverless SQL, dedicated SQL pools (formerly SQL DW), Power BI integration. It is an analytics platform for both data warehousing and big data.
* **Azure SQL Data Warehouse** (legacy term) → **Azure Synapse Dedicated SQL Pool** is the MPP (distributed) data warehouse engine.
* **Differences**:

  * Synapse is a broader platform (serverless SQL, Spark pools, dedicated SQL pools, integrated pipelines).
  * Synapse offers analytics workloads and unified workspace; SQL DW was specifically the data warehouse engine.

### 6.4 ADLS Gen1 vs Gen2

* **Gen1**: older system; limited to HDFS-like store, no hierarchical namespace for blob-level operations.
* **Gen2**: Blob storage + hierarchical namespace; better performance for analytics, POSIX-style ACLs, recommended for new deployments.
* **Recommendation**: Use **ADLS Gen2** (hierarchical namespace) for Delta Lake and analytics workloads.

### 6.5 Securing data in ADLS

* **Authentication**: Azure AD + Managed Identities for services.
* **Authorization**:

  * **RBAC** for management operations.
  * **ACLs (POSIX-style)** on filesystem for fine-grained control.
* **Network**:

  * Private Endpoints, VNet service endpoints, firewall rules.
* **Encryption**:

  * Data-at-rest: Storage Service Encryption (SSE) with Microsoft-managed keys or bring-your-own-key (CMK) via Azure Key Vault.
  * Data-in-transit: TLS.
* **Auditing & logging**:

  * Azure Monitor diagnostic logs, Storage analytics, Sentinel for SIEM.

### 6.6 CI/CD / deployment for ADF & Synapse

* **Source control**: Git integration (Azure DevOps Git or GitHub) for ADF/Synapse workspace.
* **Dev/Test/Prod**: Branching strategy (feature branches → develop → main).
* **Deployment**:

  * Use ARM templates exported from ADF (or Synapse) via "Publish" to generate ARM JSON artifacts.
  * Use Azure DevOps Pipelines / GitHub Actions to deploy ARM templates to target environment.
  * Parameterize linked services secrets using Key Vault references.
* **Automation**:

  * Validate in staging, run integration tests (run pipeline test runs), smoke test outputs, then promote.

### 6.7 Monitoring pipelines in ADF — metrics/logs

* **ADF Monitor UI**: pipeline & activity run history, inputs/outputs.
* **Metrics to monitor**:

  * Pipeline success rate, failure count, latency (duration), data volume moved, throughput (MB/s).
  * Activity-level: retry counts, error messages, duration.
* **Logging**:

  * Enable diagnostic settings to send logs to Log Analytics or Storage Account.
  * Monitor stalled runs, long-running jobs, throttling errors from connectors.
* **Alerting**:

  * Create alerts on failures, long duration, or high retry rates.

---

## 7. Storage / file formats / schema

### 7.1 Parquet vs Avro — compare & choose

* **Parquet**:

  * Columnar storage, optimized for analytical reads, excellent compression for repeated column data, predicate pushdown.
  * Good for query/analytics (OLAP) and columnar scanning.
* **Avro**:

  * Row-oriented, schema embedded/serialized with data, efficient for write-heavy or streaming and for schema evolution.
  * Good for Kafka/Event Hubs messages, streaming ingestion and where schema registry is used.
* **When to choose**:

  * Use **Avro** or **JSON** in messaging and initial landing (streaming).
  * Convert to **Parquet** (or Parquet-backed Delta) for analytics / BI (Bronze->Silver->Gold).
  * If using Delta Lake, underlying format typically Parquet with Delta transaction logs.

### 7.2 Managing schema evolution

* **Approaches**:

  * Maintain a **schema registry** (e.g., Confluent or custom) to track versions.
  * Use schema-on-read for raw zone; explicit transforms to canonical schema.
  * Delta Lake supports adding columns; use `MERGE` and `ALTER TABLE ADD COLUMNS`.
  * For incompatible changes (type changes), create new columns (e.g., `col_v2`) and deprecate old ones after consumers migrate.
  * Automate compatibility checks in CI (validate that new schema is backward compatible).
* **Example**: When adding a new column: write transforms that `coalesce` or `cast` missing columns to `NULL`/default, update table schema via ALTER.

### 7.3 Role of partitioning / bucketing

* **Partitioning**: prune large data by directory — reduces data scanned (e.g., partition by `date`).
* **Bucketing**: helps with joins; colocates rows by hash on a bucket column; reduces shuffle for bucketed joins.
* **Combine**: Partition by date; bucket by `customer_id` within date partitions for faster joins on customer.

---

## 8. Troubleshooting & edge cases

### 8.1 Production pipeline failure diagnostics (downstream failure)

1. **Collect context**: pipeline run IDs, error messages, logs (ADF, Databricks driver/executor logs), time window.
2. **Reproduce locally**: run transformation on a smaller dataset and simulate input files.
3. **Inspect data**: check schema drift, corrupt files, nulls, unexpected values causing exceptions.
4. **Check dependencies**: missing credentials, resource quotas, storage permission changes.
5. **Roll forward/rollback**:

   * If bad release, rollback via CI/CD to previous commit.
   * If data issue, backfill corrected data for affected partitions.
6. **Root cause & fix**: implement better validation & test coverage, add defensive code.

### 8.2 Job runs fine on small data but fails at scale

**Strategies**

* **Resource scaling**: increase executors / worker size; but do targeted optimization first.
* **Optimize joins**: use broadcast for small side; ensure correct join keys and reduce data early via filters.
* **Reduce shuffle**: apply `filter` and `select` as early as possible; `repartition` thoughtfully.
* **Avoid wide transformations**: limit heavy groupBy wide keys; increase shuffle partitions: `spark.sql.shuffle.partitions`.
* **Memory tuning**: increase driver/executor memory or reduce memory pressure by caching less or tuning serialization.
* **File handling**: compact small files, increase parallelism for big partitions, optimize file size.

### 8.3 Concurrent writes to same partition/file

**Problem**: Two jobs writing same partition can cause file conflicts or duplicates.

**Solutions**

* **Use transactional storage**: Delta Lake provides ACID transactions and optimistic concurrency control → prevents conflicting writes by failing concurrent commits; you can retry.
* **Locking / coordination**:

  * Use a job coordinator (ADF/Webhook) to ensure only one writer per partition.
  * Use lease or blob lease to coordinate access.
* **Design write patterns**:

  * Use **append-only** with partition directories and unique filenames (ingest_ts + uuid) followed by periodic compaction.
  * For upserts, use MERGE operations with Delta which are atomic.
* **Deduplication**:

  * Deduplicate on `pk` with last `ingest_ts` during read or compaction job to remove duplicates from multiple writes.

---

## 9. Operational and governance considerations

* **Data catalog**: Use Azure Data Catalog / Purview for data discovery, lineage, and classification.
* **Data quality**: Implement checks with Great Expectations or custom rules; block promotions if QC fails.
* **Cost control**: Use autoscaling clusters, spot instances for non-critical jobs, monitor storage & compute usage.
* **Observability**: Centralized logs in Log Analytics, setup alerts for SLA breaches, use Power BI dashboards for pipeline metrics.
* **Retention & housekeeping**:

  * Use Delta VACUUM to remove old files and manage storage.
  * Lifecycle policies for raw zone (archive to cool/RA-GRS or delete after retention).

---

## 10. Quick checklist / best practices (summary)

* Use ADLS Gen2 + Delta Lake for lakehouse features (ACID, time travel).
* Keep raw immutable, transform through bronze→silver→gold.
* Use schema registry and canonical schema; store raw payloads for traceability.
* Implement idempotency: MERGE/upsert keyed by business key + event_ts.
* Handle late data with watermarking, `withWatermark`, and late partitions processing.
* Prefer broadcasting small tables; use shuffle joins for large joins, and enable AQE for dynamic adjustments.
* Partition by date; avoid high-cardinality partition keys; control file size (128–512 MB).
* Secure with Azure AD, RBAC, POSIX ACLs, Private Endpoints, and CMK for CMEK.
* CI/CD with Git, ARM/Bicep/Terraform and automated deployments via Azure DevOps/GitHub Actions.
* Monitor with Azure Monitor, Log Analytics, and set alerting for failures & SLA drift.

---

# ADF + Databricks Pipeline for Single On-Prem Source — Diagram + ADF JSON + Databricks Notebook

> Contents: architecture diagram (Mermaid), ADF pipeline JSON (copy + Databricks activity), Databricks PySpark notebook (ingest, normalize, dedupe, MERGE to Delta), deployment notes, parameter values.

---

## 1) Overview

This document shows a concrete end-to-end pattern for a single on-prem source (CSV files dropped to SFTP or network share) to Azure Data Lake Storage Gen2 via Azure Data Factory (ADF), and transformation/upsert into a Delta Lake table using Azure Databricks. The flow includes metadata tracking, idempotent MERGE (upsert), and a backfill path.

**High-level steps**

1. On-prem file lands on SFTP (or SMB) — Self-hosted Integration Runtime reads it.
2. ADF Copy Activity moves file to ADLS Gen2 `raw/` container.
3. ADF triggers a Databricks Notebook Activity passing parameters (input path, run_id).
4. Databricks notebook reads raw file, parses/validates, writes bronze delta and MERGEs into silver (idempotent upsert), updates control table in Azure SQL or a metadata Delta table.

---

## 2) Architecture diagram (Mermaid)

```mermaid
flowchart LR
  subgraph OnPrem
    SFTP["SFTP / File Share (CSV)"]
  end
  subgraph Azure
    ADF["Azure Data Factory"]
    ADLS["ADLS Gen2 - raw/container/"]
    DB["Azure Databricks (Jobs)\nSpark Structured Streaming / Batch"]
    DeltaBronze["Delta Bronze (raw parsed)"]
    DeltaSilver["Delta Silver (conformed)"]
    Meta["Control Table (Azure SQL / Delta)"]
    PowerBI["Power BI / Synapse / BI"]
  end

  SFTP -->|Copy (Self-hosted IR)| ADF
  ADF -->|Copy Activity| ADLS
  ADF -->|Databricks Notebook Activity| DB
  DB --> DeltaBronze
  DB --> DeltaSilver
  DB --> Meta
  DeltaSilver --> PowerBI
```

---

## 3) ADF Pipeline — components & JSON example

**Assumptions / placeholder names**

* Linked services:

  * `LS_SFTP_SHIR` — self-hosted IR for SFTP
  * `LS_ADLS_GEN2` — service principal connection to ADLS Gen2 (abfss://...)
  * `LS_AZURE_DATABRICKS` — Databricks linked service (token or MSI)
* Datasets:

  * `DS_SFTP_CSV` — dataset pointing to file on SFTP
  * `DS_ADLS_RAW` — dataset pointing to ADLS folder `raw/sourceA/{date}`

**Pipeline behavior**

1. Parameter `filePath` (SFTP path) and `runId` (GUID).
2. Copy Activity `CopyToRaw` — copies file from SFTP to ADLS under `raw/sourceA/ingest_date=<YYYY-MM-DD>/file_<runId>.csv`.
3. Databricks Notebook Activity `RunDatabricksTransform` — passes `input_path` and `runId`.

### Minimal ADF pipeline JSON (simplified)

> Replace placeholders (`<...>`) with values from your environment.

```json
{
  "name": "pip_Ingest_SFTP_to_Databricks",
  "properties": {
    "activities": [
      {
        "name": "CopyToRaw",
        "type": "Copy",
        "dependsOn": [],
        "policy": { "retry": 3, "retryIntervalInSeconds": 30 },
        "typeProperties": {
          "source": {"type": "FileServerSource"},
          "sink": {"type": "DelimitedTextSink","copyBehavior":"PreserveHierarchy"},
          "enableStaging": false
        },
        "inputs": [{"referenceName": "DS_SFTP_CSV","type": "DatasetReference"}],
        "outputs": [{"referenceName": "DS_ADLS_RAW","type": "DatasetReference"}]
      },
      {
        "name": "RunDatabricksTransform",
        "type": "DatabricksNotebook",
        "dependsOn": [ {"activity":"CopyToRaw","dependencyConditions":["Succeeded"]} ],
        "typeProperties": {
          "notebookPath": "/Repos/your-repo/ingest/transform_notebook",
          "baseParameters": {
            "input_path": "@activity('CopyToRaw').output.destination.path",
            "run_id": "@pipeline().RunId",
            "source_name": "sourceA"
          }
        },
        "linkedServiceName": {"referenceName": "LS_AZURE_DATABRICKS","type": "LinkedServiceReference"}
      }
    ],
    "parameters": {
      "filePath": {"type":"String"},
      "runId": {"type":"String"}
    }
  }
}
```

**Notes**

* The `Copy` activity uses the self-hosted IR to reach on-prem SFTP. Configure retry policy for transient network errors.
* The Databricks notebook receives the final ADLS path and `run_id`. You can pass more metadata (ingest_ts, source partitioning) if needed.

---

## 4) Databricks Notebook — PySpark (batch) (complete example)

Below is a single Python notebook designed to run in Databricks as a job. It:

* Accepts parameters: `input_path` (ADLS path to copied file), `run_id`, `source_name`.
* Reads CSV (schema provided), validates/cleans rows.
* Writes data to a Bronze Delta table (append) with metadata columns.
* Performs idempotent MERGE into Silver Delta table keyed by `business_id` using `event_ts` to maintain latest record.
* Updates a metadata control Delta table with run status/counts.

> **Prerequisites**: Databricks cluster with Spark 3.x, Delta Lake enabled; secrets configured for ADLS access (use credential passthrough or service principal with scope).

```python
# Databricks notebook source
from pyspark.sql import functions as F
from delta.tables import DeltaTable
import uuid

# --- Parameters passed from ADF activity ---
dbutils.widgets.text("input_path", "")
dbutils.widgets.text("run_id", "")
dbutils.widgets.text("source_name", "sourceA")

input_path = dbutils.widgets.get("input_path")
run_id = dbutils.widgets.get("run_id") or str(uuid.uuid4())
source_name = dbutils.widgets.get("source_name")

# --- Config / target paths ---
adls_raw_prefix = "abfss://datalake@<ADLS_ACCOUNT>.dfs.core.windows.net/raw/"  # if needed
bronze_path = f"abfss://datalake@<ADLS_ACCOUNT>.dfs.core.windows.net/bronze/{source_name}"
silver_path = f"abfss://datalake@<ADLS_ACCOUNT>.dfs.core.windows.net/silver/{source_name}"
meta_table_path = f"abfss://datalake@<ADLS_ACCOUNT>.dfs.core.windows.net/_metadata/{source_name}_control"

# --- Read CSV with explicit schema (example) ---
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, LongType, DoubleType

schema = StructType([
    StructField("business_id", StringType(), True),
    StructField("event_ts", TimestampType(), True),
    StructField("amount", DoubleType(), True),
    StructField("raw_json", StringType(), True)
])

print(f"Reading input: {input_path}")
raw_df = (spark.read
          .option("header", "true")
          .option("multiLine", "false")
          .schema(schema)
          .csv(input_path))

# --- Basic validation and enrichment ---
processed = (raw_df
             .withColumn("ingest_ts", F.current_timestamp())
             .withColumn("source_name", F.lit(source_name))
             .withColumn("_run_id", F.lit(run_id)))

# Example: drop rows without business_id
valid = processed.filter(F.col("business_id").isNotNull())
invalid = processed.filter(F.col("business_id").isNull())

# Write invalid rows to a quarantine path for later inspection
if invalid.count() > 0:
    invalid.write.mode("append").parquet(f"/mnt/datalake/quarantine/{source_name}/{run_id}")

# --- Write Bronze (append) as Delta ---
(spark
 .sql("CREATE DATABASE IF NOT EXISTS lakehouse")
 )

# Ensure bronze path exists as Delta table (first time)
from delta.tables import DeltaTable

try:
    DeltaTable.forPath(spark, bronze_path)
    bronze_exists = True
except Exception:
    bronze_exists = False

if not bronze_exists:
    valid.write.format("delta").mode("overwrite").option("overwriteSchema","true").save(bronze_path)
else:
    valid.write.format("delta").mode("append").save(bronze_path)

# --- Prepare MERGE into Silver table (idempotent upsert) ---
# Silver schema may include additional conformed columns
silver_table_exists = False
try:
    DeltaTable.forPath(spark, silver_path)
    silver_table_exists = True
except Exception:
    silver_table_exists = False

# create temp view for merge source
valid.createOrReplaceTempView("staging_batch")

# For MERGE use business_id as key and event_ts as ordering to keep latest
from pyspark.sql import SparkSession

merge_sql = f"""
MERGE INTO delta.`{silver_path}` t
USING (select business_id, event_ts, amount, ingest_ts, source_name, _run_id from staging_batch) s
ON t.business_id = s.business_id
WHEN MATCHED AND s.event_ts > t.event_ts THEN
  UPDATE SET *
WHEN NOT MATCHED THEN
  INSERT *
"""

if not silver_table_exists:
    # create silver by writing the initial dataset
    spark.sql("SELECT * FROM staging_batch").write.format("delta").mode("overwrite").save(silver_path)
else:
    spark.sql(merge_sql)

# --- Update metadata control table (Delta) ---
meta_schema = StructType([
    StructField("run_id", StringType(), False),
    StructField("source_name", StringType(), False),
    StructField("ingest_ts", TimestampType(), False),
    StructField("records_in", LongType(), False),
    StructField("records_bad", LongType(), False),
    StructField("status", StringType(), False)
])

meta_row = spark.createDataFrame([(
    run_id,
    source_name,
    spark.sql("select current_timestamp() as t").collect()[0][0],
    valid.count(),
    invalid.count(),
    "SUCCESS"
)], schema=meta_schema)

# Append to metadata Delta table (create if not exists)
try:
    DeltaTable.forPath(spark, meta_table_path)
    meta_exists = True
except Exception:
    meta_exists = False

if not meta_exists:
    meta_row.write.format("delta").mode("overwrite").save(meta_table_path)
else:
    meta_row.write.format("delta").mode("append").save(meta_table_path)

print(f"Run {run_id} completed. In: {valid.count()}, Bad: {invalid.count()}")

# Optionally, return output metrics as JSON for ADF to capture
output = {
    "run_id": run_id,
    "records_in": valid.count(),
    "records_bad": invalid.count(),
    "silver_path": silver_path
}

dbutils.notebook.exit(str(output))
```

**Notes on the notebook**

* For production, avoid calling `.count()` multiple times (expensive). Instead compute counts once into variables via `agg(count('*'))`.
* Use service principal credentials or cluster-managed identity to access ADLS (`abfss://`), or mount the filesystem with secrets.
* Replace `<ADLS_ACCOUNT>` with your storage account name or use workspace-backed mounts.
* Use Delta `VACUUM` and `OPTIMIZE` periodically for compaction.

---

## 5) Backfill & late-arrival handling (concrete)

1. When ADF Copy writes a file with `event_date` earlier than processed watermark, mark it with `late=true` in metadata and trigger a `Backfill` Data Factory pipeline passing `date_to_backfill`.
2. The backfill pipeline reuses the Databricks job but with `backfill_run_id` parameter; the notebook will write to a `temp/backfill/{run_id}/` path and MERGE into silver as usual.
3. Because MERGE is idempotent (based on `business_id` + `event_ts`), older events will update records if needed (or insert missing ones).

---

## 6) Deployment snippets & ADF <-> Databricks parameter mapping

* ADF CopyActivity outputs `destination.path` in the activity output. Use expression to pass it to Databricks: `@activity('CopyToRaw').output.destination.path`.
* Provision Databricks workspace linked service with Managed Identity or personal access token stored in Key Vault.
* Store secrets in Azure Key Vault and reference them in linked services for storage and Databricks.

---

## 7) Observability & retries

* ADF: set `retry` and `timeout` on activities. Configure alerts for pipeline failures.
* Databricks: capture stdout/stderr and job run output. Use newsroom to persist metrics (control table).
* Implement idempotency checks and dedup tests as part of the notebook.

---

## 8) Next steps / customization

* I can generate:

  * A full ARM template for the ADF pipeline and linked services (parameterized),
  * A Databricks Job JSON (jobs API) to run the notebook on schedule,
  * A more production-ready notebook with partitioning, compaction (`OPTIMIZE ZORDER` if on Databricks), and efficient counts.

---

Here’s a **concrete example** that ties Databricks (PySpark) + Delta Lake with an ADF pipeline for **incremental load**. I’ll show both parts:

---

## 1. Databricks PySpark code (Transform + Incremental MERGE into Delta)

This notebook assumes:

* **Bronze layer**: Raw ingestion from ADF copy activity into ADLS (e.g., `raw/source_table/`)
* **Silver layer**: Cleaned, deduplicated Delta table
* **Incremental column**: `last_updated` used for watermarking

```python
from pyspark.sql.functions import col, current_timestamp
from delta.tables import DeltaTable

# Paths
raw_path = "abfss://datalake@storageaccount.dfs.core.windows.net/raw/source_table/"
silver_path = "abfss://datalake@storageaccount.dfs.core.windows.net/silver/source_table/"

# Load raw data (incremental batch landed by ADF)
df_raw = spark.read.format("parquet").load(raw_path)

# Apply basic transformations (example: rename cols, cast types, add metadata)
df_transformed = (
    df_raw
    .withColumnRenamed("id", "record_id")
    .withColumn("ingest_ts", current_timestamp())
    .withColumn("amount", col("amount").cast("decimal(10,2)"))
    .dropDuplicates(["record_id"])  # dedup on business key
)

# Check if silver Delta table exists
if DeltaTable.isDeltaTable(spark, silver_path):
    delta_table = DeltaTable.forPath(spark, silver_path)
    
    # Perform Incremental MERGE
    (
        delta_table.alias("tgt")
        .merge(
            df_transformed.alias("src"),
            "tgt.record_id = src.record_id"
        )
        .whenMatchedUpdateAll()
        .whenNotMatchedInsertAll()
        .execute()
    )
else:
    # First load - write as Delta
    (
        df_transformed.write.format("delta")
        .mode("overwrite")
        .save(silver_path)
    )
```

Key points:

* **Idempotency**: `MERGE` ensures updates are applied and duplicates avoided.
* **Watermarking**: Use `last_updated` column filter for incremental batches in real-world jobs.
* **Schema evolution**: Enable with `.option("mergeSchema", "true")` if needed.

---

## 2. ADF Pipeline Template (Incremental Load)

This ADF JSON pipeline:

* Uses a **Lookup** activity to fetch the last watermark from metadata store.
* A **Copy Activity** pulls new data from on-prem/SQL using that watermark.
* A **Databricks Notebook Activity** transforms + merges data.

```json
{
  "name": "Incremental_Load_Pipeline",
  "properties": {
    "activities": [
      {
        "name": "Get_Watermark",
        "type": "Lookup",
        "dependsOn": [],
        "typeProperties": {
          "source": {
            "type": "SqlSource",
            "sqlReaderQuery": "SELECT MAX(watermark_value) AS last_watermark FROM WatermarkTable WHERE table_name = 'source_table'"
          },
          "dataset": {
            "referenceName": "MetadataDB_Dataset",
            "type": "DatasetReference"
          }
        }
      },
      {
        "name": "Copy_NewData",
        "type": "Copy",
        "dependsOn": [
          {
            "activity": "Get_Watermark",
            "dependencyConditions": ["Succeeded"]
          }
        ],
        "typeProperties": {
          "source": {
            "type": "SqlSource",
            "sqlReaderQuery": "SELECT * FROM source_table WHERE last_updated > @{activity('Get_Watermark').output.firstRow.last_watermark}"
          },
          "sink": {
            "type": "AzureBlobFSink"
          }
        },
        "inputs": [
          {
            "referenceName": "Source_SQL_Dataset",
            "type": "DatasetReference"
          }
        ],
        "outputs": [
          {
            "referenceName": "Raw_ADLS_Dataset",
            "type": "DatasetReference"
          }
        ]
      },
      {
        "name": "Transform_and_Merge",
        "type": "DatabricksNotebook",
        "dependsOn": [
          {
            "activity": "Copy_NewData",
            "dependencyConditions": ["Succeeded"]
          }
        ],
        "typeProperties": {
          "notebookPath": "/Shared/IncrementalMergeNotebook",
          "baseParameters": {
            "rawPath": "@dataset().Raw_ADLS_Dataset",
            "silverPath": "/mnt/datalake/silver/source_table/"
          }
        },
        "linkedServiceName": {
          "referenceName": "AzureDatabricks_LinkedService",
          "type": "LinkedServiceReference"
        }
      }
    ]
  }
}
```

---


