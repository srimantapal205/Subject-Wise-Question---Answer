#  **Azure Fabric Interview Questions & Answers (2025)**

---

## 🔵 **SECTION 1: Azure Fabric Basics (1–15)**

---

### **1. What is Microsoft Fabric?**

**Answer:**
Microsoft Fabric is an **end-to-end, unified analytics platform** that combines data engineering, data science, real-time analytics, data integration, BI, governance, and observability under a single SaaS umbrella.

It integrates multiple services:

* **Data Factory**
* **Synapse Data Engineering (Spark)**
* **Synapse Data Warehouse**
* **Lakehouse**
* **KQL Real-Time Analytics**
* **Power BI**
* **OneLake (storage)**
* **Data Activator**

**Example:**
A company ingests SAP + SQL + API data → transforms using Spark → stores in Lakehouse → builds semantic models → publishes Power BI dashboards.
All under one workspace.

---

### **2. What is OneLake in Microsoft Fabric?**

**Answer:**
OneLake is a **single, unified data lake storage** for Microsoft Fabric.
It is built on **ADLS Gen2** and provides:

* One logical lake across all regions.
* Automatic governance.
* Delta support.
* Direct access via shortcuts.

**Example:**
Fabric Lakehouse, Data Warehouse, and Power BI all store data inside **OneLake** without separate storage accounts.

---

### **3. What is a Lakehouse in Fabric?**

A Lakehouse is a hybrid of **Data Lake + Data Warehouse**, supporting:

* Files (Parquet, CSV)
* Tables (Delta tables)
* SQL analytics
* Spark processing
* Warehouse queries

**Example:**
You ingest CSVs → convert to Delta using Spark → query with SQL endpoint.

---

### **4. What is a Warehouse in Fabric?**

A **SQL-based fully managed data warehouse** that uses Delta tables in OneLake.

Key Features:

* T-SQL compatibility
* Compute + storage separation
* Auto-scaling
* Time-travel (Delta)

---

### **5. Difference between Lakehouse & Warehouse?**

| Feature  | Lakehouse               | Warehouse    |
| -------- | ----------------------- | ------------ |
| Engine   | Spark + SQL             | SQL only     |
| Storage  | Parquet/Delta + files   | Delta only   |
| Use Case | Data engineering        | BI/Reporting |
| API      | PySpark, notebooks, SQL | T-SQL        |

---

### **6. What are Shortcuts in OneLake?**

Shortcuts allow referencing external storage **without copying data**.

Supports:

* ADLS Gen2
* AWS S3
* Dataverse
* Other Fabric items

**Example:**
Create a shortcut to ADLS to read files in Spark instantly.

---

### **7. What is Delta Lake in Fabric?**

Fabric uses Delta Lake as the **transaction format** enabling:

* ACID transactions
* Schema enforcement
* Time travel
* MERGE operations

**Example:**

```
MERGE INTO sales AS t
USING updates AS s
ON t.id = s.id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
```

---

### **8. What is the SQL Endpoint of a Lakehouse?**

A built-in **read-only SQL engine** for querying Lakehouse tables.

---

### **9. What is the difference between SQL Endpoint vs Warehouse?**

* SQL Endpoint → **read-only**, cannot do DDL or DML.
* Warehouse → **full SQL engine**.

---

### **10. What is Direct Lake mode in Fabric?**

Power BI can query Delta tables **directly** from OneLake without:

* Import mode
* DAX engine load time

Super-fast because it skips refresh.

---

### **11. What is a Semantic Model?**

A unified BI model used by Power BI built on top of:

* Lakehouse tables
* Warehouse tables
* Direct Lake datasets

---

### **12. What is Data Factory in Fabric?**

ADF capabilities inside Fabric:

* Pipelines
* Dataflows Gen2
* 200+ connectors
* Pipeline orchestration

---

### **13. What is Dataflow Gen2?**

New Power Query based ETL tool supporting:

* Delta output
* Lakehouse/Warehouse as sink
* Large data scale
* Incremental refresh

---

### **14. What is Data Engineering in Fabric?**

Spark-based data processing using:

* Notebooks
* Spark jobs
* Delta Lake

---

### **15. What are Workspaces in Fabric?**

Logical containers for:

* Lakehouse
* Warehouse
* Notebooks
* Pipelines
* Power BI items

---

## 🔵 **SECTION 2: Ingestion & ETL (16–30)**

---

### **16. What are the ingestion options in Fabric?**

* Pipelines (ADF)
* Dataflows Gen2
* Spark notebooks
* Copy activity
* Shortcuts
* KQL ingestion

---

### **17. What is the Copy Activity in Fabric?**

A pipeline activity used to **copy data** between:

* SQL → Lakehouse
* ADLS → Lakehouse
* API → Lakehouse

---

### **18. How do you perform Incremental Load in Fabric?**

3 methods:

**Method 1 — Watermark column**

```
SELECT * FROM source WHERE ModifiedDate > @LastRunTime
```

**Method 2 — Delta MERGE**
**Method 3 — Dataflows Gen2 incremental refresh**

---

### **19. What is a Medallion Architecture in Fabric?**

Standard:

* **Bronze** → Raw
* **Silver** → Cleaned
* **Gold** → Business-level curated

Fabric supports this in Lakehouse using notebooks.

---

### **20. Example: Write data to Bronze in Spark**

```
df.write.format("delta").mode("append").save("/lakehouse/Files/Bronze/sales")
```

---

### **21. Example: Create a Silver Table**

```
CREATE TABLE Silver.sales
AS SELECT * FROM Bronze.sales
WHERE amount > 0
```

---

### **22. What are Data Pipelines in Fabric?**

Pipelines orchestrate:

* Ingestion
* Transformation
* Scheduling
* Error handling

---

### **23. What is a Notebook Job?**

A scheduled Spark notebook execution.

---

### **24. Explain Pipeline vs Notebook vs Dataflow Gen2.**

| Feature  | Pipeline      | Notebook  | Dataflow Gen2 |
| -------- | ------------- | --------- | ------------- |
| Best for | Orchestration | Transform | Simple ETL    |
| UI       | GUI           | Code      | Power Query   |
| Storage  | Any           | Delta     | Lakehouse     |

---

### **25. How do you schedule a Lakehouse Pipeline?**

Using pipeline **Triggers**:

* Scheduled
* Event-based
* Tumbling window

---

### **26. What is Auto Loader in Fabric?**

Continuous streaming ingestion for files arriving in a folder.

---

### **27. What is schema evolution in Lakehouse?**

Automatic handling when columns are added.

Example:

```
df.write.option("mergeSchema", "true")
```

---

### **28. How do you validate schema?**

Using Spark:

```
df.printSchema()
```

---

### **29. How to check data accuracy before load?**

* Data quality rules
* Null checks
* DQL (Data Quality Language)
* Expectations (similar to DLT)

---

### **30. How to handle CDC in Fabric?**

Use:

* Incremental load
* SQL CDC jobs
* Delta MERGE

---

## 🔵 **SECTION 3: Data Engineering / Spark (31–45)**

---

### **31. How to read files from Lakehouse?**

```
df = spark.read.format("delta").load("/lakehouse/default/sales")
```

---

### **32. How to write Delta table?**

```
df.write.format("delta").saveAsTable("Bronze.sales")
```

---

### **33. Example of PySpark transformation**

```
df2 = df.groupBy("category").agg(sum("amount"))
```

---

### **34. How to create a Gold table?**

```
CREATE TABLE Gold.sales_summary AS
SELECT category, SUM(amount) AS total
FROM Silver.sales
GROUP BY category
```

---

### **35. What is Spark Table vs SQL Table in Fabric?**

* Spark Table → created by notebooks
* SQL Table → created in Warehouse

Both stored as Delta.

---

### **36. What is Spark Compute Pool?**

Elastic processing power for Spark notebooks.

---

### **37. How does Fabric handle scaling?**

* Auto-scaling
* Pause-resume compute
* Elastic pools

---

### **38. What is Time Travel?**

Read old version of data:

```
SELECT * FROM sales VERSION AS OF 3
```

---

### **39. What is a Delta MERGE?**

Used for UPSERT operations.

---

### **40. Example MERGE**

```
MERGE INTO Silver.sales t
USING Bronze.sales s
ON t.id = s.id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
```

---

### **41. What is VACUUM in Delta?**

Clean old versions:

```
VACUUM sales RETAIN 7 HOURS;
```

---

### **42. Does Fabric support streaming?**

Yes, using:

* Auto Loader
* Eventstream (Real-time hub)

---

### **43. What is Eventstream?**

Real-time ingestion service for:

* Kafka
* Event Hub
* Pub/Sub

---

### **44. What is KQL database?**

Database used for **real-time analytics**.

Example query:

```
StormEvents | summarize count() by State
```

---

### **45. What is the difference between Spark and KQL?**

| Feature  | Spark           | KQL         |
| -------- | --------------- | ----------- |
| Type     | Batch/Streaming | Real-time   |
| Language | Python/SQL      | Kusto Query |
| Storage  | Delta           | KQL tables  |

---

## 🔵 **SECTION 4: Power BI + Direct Lake (46–60)**

---

### **46. What is Direct Lake Mode?**

Power BI queries **Delta tables** directly from OneLake.

No data import → no refresh required.

---

### **47. How is Direct Lake different from DirectQuery?**

| Feature       | Direct Lake | DirectQuery    |
| ------------- | ----------- | -------------- |
| Speed         | Very fast   | Slow           |
| Storage       | OneLake     | SQL DB         |
| Data movement | None        | Query pushdown |

---

### **48. When use Direct Lake Mode?**

* Large datasets
* Real-time dashboards
* Lakehouse/Warehouse sources

---

### **49. What is Semantic Model in Fabric?**

A Power BI dataset stored inside OneLake.

---

### **50. How to refresh a dataset?**

Direct Lake → **No refresh needed**
Import → Scheduled refresh

---

### **51. Can Power BI connect to Lakehouse?**

Yes using:

* Direct Lake
* SQL Endpoint
* Import mode

---

### **52. What is Power BI Report in Fabric?**

Visualization layer that uses semantic models.

---

### **53. What is a Datamart? (2025 update)**

In Fabric, replaced with:

* Warehouse
* Lakehouse
* Semantic models

Datamart is deprecated.

---

### **54. What is Data Activator?**

Automated action engine based on triggers from:

* KQL queries
* Power BI
* Warehouse

Example:
“Alert when sales drops below threshold.”

---

### **55. How to implement Row-Level Security (RLS)?**

Create roles:

```
[SalesRegion] = USERPRINCIPALNAME()
```

---

### **56. What is an Item in Fabric?**

Any object such as:

* Lakehouse
* Warehouse
* Pipeline
* Notebook
* Power BI report

---

### **57. How to share a workspace?**

Using Access control:

* Admin
* Member
* Contributor
* Viewer

---

### **58. What is Domain in Fabric?**

Logical grouping for governance.

Example:

* Sales Domain
* HR Domain
* Finance Domain

---

### **59. What is Data Product?**

A packaged asset containing:

* Data
* Model
* Documentation
* Pipelines

---

### **60. How to monitor Fabric usage?**

Using:

* Admin portal
* Real-time monitoring
* Fabric usage metrics

---

## 🔵 **SECTION 5: Governance, Security & Administration (61–80)**

---

### **61. What is the Fabric Admin Portal?**

It is the central place for managing:

* Capacity settings
* Workspace governance
* Data policies
* Security
* Monitoring
* Billing

**Example:**
You can allocate F64 capacity to a workspace from admin portal.

---

### **62. What is Fabric Capacity?**

Fabric capacity provides compute resources that power:

* Lakehouse
* Warehouse
* Data Engineering
* Power BI
* Real-time analytics

Fabric capacities come as:

* **F SKUs** (Fabric)
* **P SKUs** (Premium)
* **A SKUs** (Azure)

---

### **63. How is capacity consumption measured?**

Through **Capacity Units (CU)**.
Each operation (Spark query, SQL load, refresh) consumes CU.

---

### **64. What happens when capacity overloads?**

Fabric triggers:

* Throttling
* Slower job execution
* Temporary failures

You need to scale capacity or optimize workloads.

---

### **65. What is Data Lineage in Fabric?**

Fabric automatically tracks:

* Datasets
* Tables
* Pipelines
* Reports

Example:
Warehouse table → Semantic Model → Power BI report.

You can visualize dependencies.

---

### **66. What is Data Governance in Fabric?**

Fabric integrates with **Microsoft Purview**, supporting:

* Data classification
* Labeling
* End-to-end lineage
* Access control

---

### **67. What is Purview Integration?**

Purview provides:

* Data Catalog
* Data Sensitivity labels
* Access auditing

Fabric auto-scans metadata into Purview.

---

### **68. What are Sensitivity Labels?**

Labels that protect data:

* Confidential
* Highly Confidential
* Public

Used in Power BI datasets & Fabric items.

---

### **69. What is Workspace Role?**

Roles include:

* Admin
* Member
* Contributor
* Viewer

Each has different permissions.

---

### **70. What is Item-level Security?**

Allows securing:

* Specific tables
* Specific folders
* Specific columns

Example:
Finance table access only to accounting team.

---

### **71. What is Column-Level Security (CLS)?**

Restrict access to specific columns in semantic models.

**Example:**
Hide “Salary” for non-HR users.

---

### **72. What is Object-Level Security (OLS)?**

Restrict entire **tables** from being viewed.

---

### **73. What is Row-Level Security (RLS)?**

Filter row access based on user identity.

**Example:**

```
[Region] = USERPRINCIPALNAME()
```

---

### **74. What is Lakehouse Permission Model?**

It includes access to:

* Files folder
* Tables folder
* SQL endpoint
* Shortcut objects

---

### **75. What is Managed Identity in Fabric?**

Fabric pipelines and notebooks use managed identity to access:

* ADLS
* SQL Server
* Key Vault
* Dataverse

---

### **76. What is Tenant Setting?**

Admin configurations at tenant level for:

* Sharing
* Exporting
* Content creation
* Dataflows
* AI usage

---

### **77. What is Workspace-level Setting?**

Customization for:

* Region
* Default semantic model
* Permissions
* Linked connections

---

### **78. What is Capacity Metrics App?**

Used to analyze:

* Refresh failures
* Throttling
* Workload distribution
* Jobs’ resource usage

---

### **79. What security controls exist for OneLake?**

* Azure AD authentication
* RBAC
* Data encryption at rest
* Network isolation
* Sensitivity labels

---

### **80. How does Fabric handle backups?**

Fabric doesn’t require manual backups; it leverages:

* Delta versioning
* Soft deletion
* Workspace restore

---

## 🔵 **SECTION 6: Real-Time Analytics & Event Processing (81–95)**

---

### **81. What is Real-Time Analytics in Fabric?**

Powered by **KQL (Kusto Query Language)** for:

* Streaming data
* High-velocity logs
* IoT sensor ingestion

---

### **82. What is a KQL Database?**

A Fabric item used for streaming and log analytics.

---

### **83. What is Eventhouse?**

A container for KQL databases optimized for massive-scale real-time analytics.

---

### **84. What data formats does KQL support?**

* JSON
* CSV
* Parquet
* Avro
* Delta (via shortcuts)

---

### **85. What is a KQL Table?**

A table created using Kusto for real-time analytics.

Example:

```
.create table SalesEvents (SaleID:int, Amount:double, Timestamp:datetime)
```

---

### **86. How to ingest data into KQL?**

3 ways:

* Eventstream
* One-click ingestion
* KQL ingestion commands

---

### **87. What is Eventstream in Fabric?**

A real-time ingestion pipeline that supports:

* Kafka
* Event Hub
* IoT Hub
* REST events

---

### **88. What is the difference between Eventstream and Pipelines?**

| Feature | Eventstream         | Pipeline            |
| ------- | ------------------- | ------------------- |
| Type    | Streaming           | Batch               |
| Use     | IoT, logs           | ETL, batch loads    |
| Output  | KQL/Table/Lakehouse | Lakehouse/Warehouse |

---

### **89. What is a Real-Time Dashboard?**

A Power BI report connected to:

* Eventstreams
* KQL queries
* Real-time datasets

---

### **90. How to join streaming & static data?**

Using KQL:

```
StreamTable
| join kind=inner LookupTable on Key
```

---

### **91. How does Fabric handle late-arriving data?**

KQL supports:

* Ingestion-time policies
* Update policies
* Retention policies

---

### **92. What is retention policy in KQL?**

Automatically deletes data after a period:

```
.alter table Logs policy retention softdelete = 30d
```

---

### **93. What is batching policy?**

Controls data ingestion buffer size.

---

### **94. What is update policy?**

Defines how ingestion triggers downstream table updates.

---

### **95. Can KQL read Delta tables?**

Yes, KQL can read Delta using **OneLake shortcuts**.

---

## 🔵 **SECTION 7: Data Warehouse (SQL Analytics) (96–110)**

---

### **96. What is Data Warehouse in Fabric?**

A full T-SQL compatible Warehouse built on Delta format inside OneLake.

---

### **97. What is SQL Analytics Endpoint?**

Provides:

* Serverless SQL engine
* Query Lakehouse tables

SQL Endpoint is read-only.

---

### **98. How to create a Warehouse table?**

```
CREATE TABLE Sales(
  SaleID INT,
  Amount FLOAT,
  Region VARCHAR(20)
)
```

---

### **99. How does Fabric Warehouse store data?**

As **Delta Lake** tables inside OneLake.

---

### **100. How to load data into Warehouse?**

Using:

* COPY INTO
* Pipelines
* Dataflows
* Notebooks

Example:

```
COPY INTO Sales
FROM 'https://onelake/.../sales.csv'
FILE_FORMAT = 'CSV'
```

---

### **101. What is COPY INTO in Warehouse?**

High-speed ingestion command.

---

### **102. How to optimize Warehouse?**

* Use partitioning
* Use statistics
* Use Delta optimizations

---

### **103. How to check table statistics?**

```
SHOW STATS FOR Sales;
```

---

### **104. What is Query Acceleration?**

Automatic pushdown and parallelization.

---

### **105. How to implement Slowly Changing Dimensions (SCD) Type 2?**

Using Delta MERGE:

```
WHEN MATCHED AND s.hash<>t.hash THEN UPDATE SET EndDate = current_timestamp()
WHEN NOT MATCHED THEN INSERT (...)
```

---

### **106. How to schedule SQL tasks?**

Using **Warehouse SQL Jobs**.

---

### **107. What is Materialized View?**

Warehouse supports materialized view for performance.

---

### **108. What is a Data Warehouse Workload Group?**

Controls resource usage for Warehouse.

---

### **109. How to handle CDC from SQL Server?**

Use:

* ADF/Fabric Pipeline
* Watermark
* MERGE

---

### **110. What is the difference between Warehouse vs SQL Endpoint Lakehouse?**

| Feature     | Warehouse | SQL Endpoint  |
| ----------- | --------- | ------------- |
| Write       | Yes       | No            |
| Compute     | Dedicated | Serverless    |
| Performance | High      | Moderate      |
| DML         | Supported | Not Supported |

---

## 🔵 **SECTION 8: Advanced Fabric Concepts (111–120)**

---

### **111. What are Fabric Domains?**

Organize workspaces under business areas.

Example:

* HR Domain → HR workspaces
* Finance Domain → Finance workspaces

---

### **112. What are Data Products?**

Packaged set of:

* Lakehouse
* Pipelines
* Documentation
* Reports

---

### **113. What is a Notebook Job Definition?**

JSON representing a notebook job.

---

### **114. Difference between Default Lakehouse vs SQL Endpoint?**

* Default Lakehouse → Used for notebooks
* SQL Endpoint → Used for BI queries

---

### **115. What is Lakehouse ML?**

Machine learning using notebook-based MLflow integration.

---

### **116. What is MLflow in Fabric?**

Used for:

* Experiment tracking
* Model versioning
* Model registry

---

### **117. Does Fabric support Git Integration?**

Yes, Fabric integrates with GitHub and Azure DevOps for:

* Version control
* CI/CD pipelines

---

### **118. What is Workspace Git Sync?**

Automatically syncs:

* Notebooks
* Pipelines
* Dataflows
* Semantic models

---

### **119. How to deploy Fabric items to another environment?**

Use:

* Git branch → PR → Sync to Prod Workspace
* Deployment pipelines

---

### **120. What interview tasks can be expected for Fabric?**

Examples:

* Build Lakehouse
* Create Pipeline to ingest data
* Create Delta Table
* Apply SCD Type 2 logic
* Build Power BI report using Direct Lake
* Create Eventstream ingestion

---

Below is **Part 3** containing:

### ✅ **50 Advanced Azure Fabric Questions (2025)**

### ✅ **10 Real-World Scenario-Based Case Studies with Solutions**

All answers are detailed and suitable for **2–4 years Data Engineer experience**.

If you want, I can also give **Hands-on coding tasks**, **practical exercises**, and **End-to-end architecture diagrams**.

---

# ⭐ PART 3 — **ADVANCED AZURE FABRIC QUESTIONS (2025)**

---

## 🔵 **SECTION A — Advanced Architecture & Performance (1–15)**

---

### **1. How does Fabric unify compute for Lakehouse, Warehouse, and Power BI?**

Fabric uses **Shared Capacity** and “One Compute Engine” architecture:

* SQL Engine for Warehouse
* Spark Engine for Lakehouse
* DAX Engine for Power BI
* KQL Engine for Real-time Analytics

All workloads share **Capacity Units (CUs)** for distributed compute.

---

### **2. How does Delta Lake optimize read performance in Fabric?**

Fabric applies:

* File compaction
* Z-Ordering
* Auto Optimize
* Column pruning
* Data skipping
* Min/max index metadata

---

### **3. What is Z-Ordering in Fabric?**

Sorts Delta table files based on frequently filtered columns.

Example:

```
OPTIMIZE Sales ZORDER BY (CustomerID)
```

---

### **4. When should you use Warehouse vs Lakehouse for performance?**

**Warehouse** → BI workloads, many joins, high concurrency
**Lakehouse** → data engineering, streaming, ML

---

### **5. How does Fabric handle concurrency conflicts?**

Delta Lake uses:

* **Optimistic concurrency control**
* Automatic retries
* Conflict detection at commit time

---

### **6. What is Auto-Compaction in Fabric?**

Automatically merges small Delta files (small file problem).

---

### **7. What is scaling mode (elasticity) in Fabric?**

Fabric auto-scales compute during:

* Heavy SQL workloads
* Long-running Spark jobs
* High concurrency BI queries

---

### **8. What is Pushdown Optimization?**

Fabric pushes transformations:

* SQL queries → compute engine
* Power BI → Direct Lake storage engine
* Spark → data skipping

---

### **9. What is Query Folding in Fabric?**

Occurs mostly in **Dataflows Gen2**, automatically pushing steps to source DB.

---

### **10. What factors impact Warehouse performance?**

* Partitioning
* Materialized views
* Statistics
* Columnstore format
* Delta optimization

---

### **11. What is Lifecycle Management in Fabric?**

Manages retention & partition expiration:

* Bronze: 30–90 days
* Silver: 180 days
* Gold: Long-term curated

---

### **12. What is the difference between Delta CDF vs SQL CDC in Fabric?**

| Feature  | Delta CDF    | SQL CDC          |
| -------- | ------------ | ---------------- |
| Storage  | Delta Tables | SQL Logs         |
| Type     | File-based   | Log-based        |
| Best For | Lakehouse    | Warehouse / OLTP |

---

### **13. What is Vertical Partitioning in Warehouse?**

Split wide tables into multiple sub-tables to improve performance.

---

### **14. What is Horizontal Partitioning in Warehouse?**

Partition table by:

* Date
* Region
* Category

Improves query performance.

---

### **15. What is Load Balancing in Fabric?**

Workload Distribution among:

* Spark pools
* SQL compute
* KQL compute
* Power BI Service

---

## 🔵 **SECTION B — Real-Time Analytics & ETL Advanced (16–30)**

---

### **16. How does Fabric ensure Exactly-Once Processing?**

By using:

* Delta transactions
* Auto Loader checkpointing
* KQL ingestion batching
* Idempotent MERGE logic

---

### **17. What is Eventstream Routing?**

You can route events from a stream to:

* Lakehouse tables
* KQL databases
* Warehouse
* Custom endpoints

---

### **18. What type of serialization formats do Eventstreams support?**

* JSON
* AVRO
* Parquet
* Protobuf

---

### **19. How does KQL handle high-throughput ingestion?**

Using:

* Sharding
* Batching policies
* Hot-cache management

---

### **20. How does Fabric handle out-of-order streaming data?**

Using:

* Event timestamps
* Ingestion-time policies
* KQL reorder policies

---

### **21. How to convert Bronze → Silver in streaming mode?**

Use Auto Loader + Merge:

```
MERGE INTO Silver.Sales s
USING Streaming_Sales b
ON s.Id = b.Id
WHEN NOT MATCHED THEN INSERT *
```

---

### **22. What are Update Policies in KQL?**

Automatically apply transformations to incoming data.

---

### **23. What do Retention Policies do in KQL?**

Automatically delete expired data to save storage.

---

### **24. How to ingest 1TB data into Fabric?**

Use:

* COPY INTO with staging
* Partitioned folder ingestion
* Spark parallel ingestion

---

### **25. What is Auto-Sync for Delta + KQL?**

KQL can automatically sync data from Delta shortcuts.

---

### **26. How does Fabric manage schema drift in streaming?**

Supports:

* Auto-evolution
* Schema enforcement
* Warning logs

---

### **27. How do you handle incremental data for Warehouse?**

Use:

```
COPY INTO Table WITH (INCREMENTAL = TRUE)
```

---

### **28. What’s the best method to ingest API data into Fabric?**

* Pipelines REST connector
* Dataflows Gen2 Web connector
* Notebooks using Python requests

---

### **29. What is Unidentified Data Handling?**

Fabric auto-classifies unknown formats and suggests transformations.

---

### **30. How are secrets managed in Fabric?**

Using **Fabric Managed Identity** linked with **Azure Key Vault**.

---

## 🔵 **SECTION C — Fabric + Power BI Advanced (31–40)**

---

### **31. What is the difference between Import, DirectQuery, and Direct Lake?**

| Feature   | Import | DirectQuery | Direct Lake |
| --------- | ------ | ----------- | ----------- |
| Refresh   | Yes    | No          | No          |
| Storage   | PBIX   | DB          | OneLake     |
| Speed     | Fast   | Slow        | Fastest     |
| Data Size | Medium | Large       | Extra Large |

---

### **32. When is Direct Lake NOT recommended?**

* Too many small files (<10MB)
* Non-Delta datasets
* High-cardinality dimension tables

---

### **33. How does Direct Lake avoid refreshes?**

Reads Delta files directly using **VertiPaq acceleration**.

---

### **34. How do you handle relationships in large semantic models?**

Use:

* Surrogate keys
* Snowflake modeling
* Star schema

---

### **35. How do you optimize slow Direct Lake models?**

* Z-Order
* Compaction
* Add surrogate keys
* Reduce column cardinality

---

### **36. How does Fabric improve Power BI refresh?**

* Query caching
* Delta-based refresh
* Parallel partition updates

---

### **37. How to secure data in Direct Lake?**

Use:

* RLS
* OLS
* CLS
* Tenant-level policies

---

### **38. What is Data Activator?**

Real-time BI rules engine:

* Detect patterns
* Alert users
* Trigger Power Automate flows

---

### **39. What is a Real-Time Report vs Standard Report?**

Real-Time Report → observes streaming data
Standard Report → uses semantic model

---

### **40. What performance features does Power BI get from Fabric?**

* Direct Lake
* OneLake shortcuts
* Semantic models stored in lake
* Automatic optimization

---

## 🔵 **SECTION D — Admin, Governance, Reliability (41–50)**

---

### **41. How do you control costs in Fabric?**

* Monitor CU consumption
* Schedule compute pauses
* Limit parallel Spark jobs
* Optimize workloads
* Use lower F SKU

---

### **42. What is the Fabric "Soft Delete Policy"?**

Deleted items can be restored within **30 days**.

---

### **43. How does versioning work in Fabric?**

Fabric automatically versions:

* Delta Tables
* Pipelines
* Models
* Notebooks (via Git)

---

### **44. What is Workspace Restore?**

Allows restoring workspace from backup snapshots.

---

### **45. What is Tenant Isolation?**

Logical separation of Fabric tenants for:

* security
* data isolation
* governance

---

### **46. What is the Fabric Capacity Load Balancer?**

Distributes resources across workloads:

* SQL
* Spark
* Power BI
* KQL

---

### **47. What is Throttling in Fabric?**

Occurs when CU usage is above threshold.
Symptoms:

* Slow refresh
* Spark delays
* SQL query timeout

---

### **48. What is the difference between Cancel and Abort in Fabric Jobs?**

Cancel → Stops gracefully
Abort → Immediate termination

---

### **49. How to track Fabric changes?**

Using:

* Audit Logs
* Purview Lineage
* Git Version Control

---

### **50. What external tools can integrate with Fabric?**

* Databricks notebooks
* Azure ML
* Snowflake
* Power Automate
* Azure Functions

---

# ⭐ **PART 4 — REAL-WORLD SCENARIO CASE STUDIES WITH ANSWERS**

### (10 Scenarios, Architecture + Logic + Interview-grade explanations)

---

## 🔵 **SCENARIO 1 — Incremental Pipeline from SQL Server to Fabric Lakehouse**

**Problem:**
A SQL Server on-prem DB (200 tables) must be ingested daily into Lakehouse with incremental logic.

**Solution Architecture:**

1. Use **Fabric Pipelines** (Data Factory)
2. Create **SQL Server linked service** using gateway
3. Use **Get Metadata** to fetch table names
4. For each table:

   * Use **Watermark column** (ModifiedDate)
   * Use **Incremental query**
   * Write to **Bronze Delta**
5. Transform Bronze → Silver using MERGE
6. Create semantic model on Gold

**Why this works:**
Handles schema drift, easy monitoring, scalable, and versioning-enabled.

---

## 🔵 **SCENARIO 2 — Real-Time Sensor Data + Power BI Dashboard**

**Problem:**
IoT devices send 50,000 events/second. Need real-time dashboard.

**Solution:**

1. Ingest data via **Eventstream**
2. Route to:

   * KQL Database (Hot storage)
   * Lakehouse (Historical)
3. KQL → Real-time Power BI visual
4. Lakehouse → Gold table → Power BI Direct Lake

**Real-time latency:** <1 second

---

## 🔵 **SCENARIO 3 — SCD Type 2 Dimension Table using Fabric Lakehouse**

**Problem:**
Customer dimension requires history tracking.

**Solution (PySpark):**

```
MERGE INTO Silver.Customer tgt 
USING Bronze.NewCustomer src
ON tgt.CustomerID = src.CustomerID
WHEN MATCHED AND tgt.Hash <> src.Hash THEN
  UPDATE SET EndDate=current_timestamp(), IsActive=false
WHEN NOT MATCHED THEN
  INSERT (...)
```

---

## 🔵 **SCENARIO 4 — Multiple Finance Sources Consolidation**

**Problem:**
SAP + Oracle + CSV files must be combined.

**Solution:**

* Use Pipelines for SAP + Oracle ingestion
* Create shortcut to ADLS for CSV
* Use Spark for data unification
* Store curated Finance model in Gold
* Build Power BI semantic model on top

---

## 🔵 **SCENARIO 5 — 1 Billion Row Fact Table Optimization**

**Problem:**
Power BI refresh slow due to large fact table.

**Solution:**

* Switch to **Direct Lake**
* Partition by date
* Optimize with Z-Order
* Compact files
* Convert non-numeric keys → Surrogate Keys

---

## 🔵 **SCENARIO 6 — Cross-Tenant Data Sharing**

**Problem:**
Two companies want to share data securely.

**Solution:**

* Use **OneLake Shortcuts**
* Apply RLS
* Enable Cross-Tenant Share setting
* Provide governed access

---

## 🔵 **SCENARIO 7 — API Data Every 15 Minutes**

Requirements:

* Call API
* Load JSON to Lakehouse
* Transform and refresh model

**Solution:**

* Use Pipeline REST connector
* Parse using Dataflow Gen2
* Write to Bronze Delta
* Use job scheduler (15-minute trigger)

---

## 🔵 **SCENARIO 8 — Fabric with Databricks Migration**

**Problem:**
Databricks notebooks must be migrated to Fabric.

**Solution:**

* Use PySpark compatibility (80% same code)
* Create Lakehouse structure
* Migrate notebooks
* Replace DBFS with OneLake paths
* Test performance

---

## 🔵 **SCENARIO 9 — Power BI RLS for Multi-Region Sales**

**Problem:**
Restrict sales region data per regional manager.

**Solution:**
DAX rule:

```
Sales[Region] = LOOKUPVALUE(UserRegion[Region], UserRegion[Email], USERPRINCIPALNAME())
```

---

## 🔵 **SCENARIO 10 — End-to-End Fabric Medallion Architecture**

**Problem:**
Implement Bronze-Silver-Gold.

**Solution:**

* Bronze → Raw ingestion
* Silver → Clean, standardize, remove duplicates
* Gold → Business layer (facts + dimensions)
* Power BI: Direct Lake
* Lineage: Purview
* Governance: Sensitivity labels

---


