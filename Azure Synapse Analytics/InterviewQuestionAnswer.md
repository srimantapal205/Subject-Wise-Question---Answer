# <==== ::: Azure Synapse Analytics interview questions ::: ====>

---

### **1. What is Azure Synapse Analytics?**

Azure Synapse Analytics is an integrated analytics service that combines big data and data warehousing. It allows users to query data using serverless or dedicated resources and integrates deeply with other Azure services for data ingestion, preparation, management, and serving.

---

### **2. What are the key components of Synapse?**

* **Synapse SQL (Dedicated & Serverless pools)**
* **Apache Spark Pools**
* **Synapse Pipelines** (based on Azure Data Factory)
* **Synapse Studio**
* **Data Integration (Linked Services, Data Flows)**
* **Data Storage Integration (like ADLS Gen2)**

---

### **3. Difference between Dedicated and Serverless SQL Pools?**

| Feature          | Dedicated SQL Pool                | Serverless SQL Pool                      |
| ---------------- | --------------------------------- | ---------------------------------------- |
| **Provisioning** | Requires pre-provisioned capacity | On-demand, no setup needed               |
| **Billing**      | Based on reserved capacity (DWUs) | Pay-per-query (per TB of data processed) |
| **Performance**  | High, predictable                 | Best for ad-hoc querying                 |
| **Use case**     | Structured, large-scale DW        | Exploratory analytics, data lake queries |

---

### **4. What are the supported file formats in Synapse?**

* CSV
* Parquet
* JSON
* ORC
* Avro
* Delta (via Spark)

---

### **5. How does Synapse integrate with ADLS Gen2?**

Synapse integrates with Azure Data Lake Storage Gen2 through Linked Services, enabling direct querying, data movement, and Spark processing. You can mount storage accounts or access data using workspace credentials.

---

### **6. What is Synapse Studio?**

Synapse Studio is a unified web interface for developing, managing, and monitoring Synapse workloads. It allows you to build pipelines, run SQL or Spark queries, create notebooks, visualize data, and orchestrate analytics workflows.

---

### **7. How do you create a table in Synapse SQL pool?**

In a **dedicated SQL pool**:

```sql
CREATE TABLE dbo.Sales (
    SaleID INT,
    ProductName VARCHAR(100),
    Amount DECIMAL(10, 2)
)
WITH (
    DISTRIBUTION = ROUND_ROBIN,
    HEAP
);
```

In a **serverless SQL pool**:
You create external tables using `CREATE EXTERNAL TABLE`.

---

### **8. What is a Linked Service in Synapse?**

A Linked Service is a connection string-like object that defines how Synapse connects to external resources like Azure SQL, ADLS Gen2, Blob Storage, Dataverse, etc.

---

### **9. Explain the concept of Workspace in Synapse.**

A Synapse Workspace is a centralized environment that contains all analytics resources, including SQL/Spark pools, pipelines, notebooks, datasets, and connections. It simplifies management and collaboration for data analytics projects.

---

### **10. What are Notebooks in Synapse?**

Notebooks in Synapse are interactive documents where you can run code in various languages (e.g., PySpark, SQL, .NET, Scala) to analyze data, visualize results, and build data workflows.

---

### **11. What languages can be used in Synapse Notebooks?**

* PySpark (Python)
* Spark SQL
* Scala
* .NET for Spark (C#)

---

### **12. What is a Spark Pool in Synapse?**

A Spark Pool is a provisioned Apache Spark cluster within Synapse used for large-scale distributed data processing and machine learning workloads using notebooks or pipelines.

---

### **13. What is an Integration Runtime?**

Integration Runtime (IR) is the compute infrastructure used by Synapse Pipelines to perform data movement and transformation. There are three types:

* **Azure IR** (for cloud data)
* **Self-hosted IR** (for on-premise or VNet access)
* **Managed VNet IR** (secure data movement with enhanced isolation)

---

### **14. What are Data Flows in Synapse Pipelines?**

Data Flows are visual, code-free data transformation components that execute using Spark under the hood. You can perform operations like joins, aggregations, filters, and data type conversions within a pipeline.

---

### **15. How does Synapse handle data ingestion?**

Synapse supports multiple ingestion methods:

* **Synapse Pipelines** (Copy activity, Data Flows)
* **SQL Scripts** (from external tables in ADLS)
* **Spark jobs** (via Notebooks or Pipelines)
* **Event-based triggers** (from Event Grid or time-based triggers)

---
Here are **intermediate-level** answers (Q16–Q35) for your Azure Synapse Analytics interview preparation, especially for a **Data Engineer** role:

---

### **16. What is PolyBase and its use in Synapse?**

**PolyBase** allows Synapse SQL to query external data (like files in ADLS, Blob Storage, or Hadoop) using T-SQL. It enables **fast parallel loading** into dedicated SQL pools and helps build **external tables** over files like CSV, Parquet, and ORC.

---

### **17. What are external tables and why are they used?**

**External tables** allow querying data stored outside of Synapse (e.g., in ADLS Gen2) without physically loading it.
**Use cases:**

* Query raw data directly
* Perform ELT
* Save storage in SQL pool

---

### **18. How is data distributed in a dedicated SQL pool?**

Data in a dedicated pool is split across **60 distributions**. Each compute node processes a subset of the data to support parallelism. Distribution methods determine how rows are split across these distributions.

---

### **19. What is data movement and how to avoid it?**

**Data movement** occurs when rows need to be transferred between distributions during query execution (e.g., joins).
**To avoid it:**

* Use **hash distribution** on join keys
* Avoid joining large tables with different distribution methods
* Use **replicated** tables for small dimension tables

---

### **20. Explain Round-Robin, Hash, and Replicated distributions.**

| Type            | Description                                  | Use Case                                       |
| --------------- | -------------------------------------------- | ---------------------------------------------- |
| **Round-Robin** | Rows distributed evenly regardless of values | Default, when no good key exists               |
| **Hash**        | Rows distributed by hashing a column         | For large fact tables to enable parallel joins |
| **Replicated**  | Full copy to each distribution               | For small dimension tables used in joins       |

---

### **21. When would you use CTAS (Create Table As Select)?**

Use **CTAS** to:

* Create a new table based on a query
* Optimize data layout for performance
* Materialize transformed or aggregated data
  Example:

```sql
CREATE TABLE SalesSummary
WITH (DISTRIBUTION = HASH(CustomerID))
AS SELECT CustomerID, SUM(Amount) FROM Sales GROUP BY CustomerID;
```

---

### **22. What are materialized views in Synapse?**

Materialized views store **precomputed query results** for performance.
They auto-refresh (incrementally if possible) and improve performance for repetitive, complex queries.

---

### **23. How do you handle schema evolution in Synapse?**

* **Spark Pools**: Support schema evolution with Delta Lake.
* **Pipelines**: Use **mapping data flows** to handle changing columns.
* **External Tables**: Schema must match exactly—no evolution support.
  Best practices include:
* Storing raw data in Parquet/Delta
* Using metadata-driven pipelines

---

### **24. Explain the lifecycle of a pipeline in Synapse.**

1. **Design** – Create activities and data flows
2. **Publish** – Save pipeline changes to Synapse workspace
3. **Trigger** – Execute manually or via schedule/event
4. **Monitor** – Track execution, logs, and alerts
5. **Debug** – Test pipelines before full deployment

---

### **25. What is the use of staging in data transformation?**

Staging allows you to:

* Store **intermediate results**
* Break complex transformations into steps
* Improve performance and fault-tolerance
  Staging is typically implemented using temporary tables or storage locations in ADLS.

---

### **26. What monitoring tools are available in Synapse?**

* **Synapse Studio Monitor Hub**
* **Azure Monitor / Log Analytics**
* **Activity run and trigger run logs**
* **SQL and Spark job monitoring**
* **Alerts** using Action Groups or Logic Apps

---

### **27. What are the security features in Synapse?**

* **Azure AD Authentication**
* **RBAC (Role-Based Access Control)**
* **ACLs on ADLS Gen2**
* **Firewall rules and private endpoints**
* **Data encryption (at rest and in transit)**
* **Auditing & threat detection**

---

### **28. How does Synapse handle access control?**

* **RBAC** controls access at workspace and resource level.
* **Access Control Lists (ACLs)** manage permissions at file/folder level in ADLS.
* Use **Azure AD groups** for centralized permission management.

---

### **29. What is the difference between RBAC and ACL in Synapse?**

| Feature    | RBAC                                      | ACL                                   |
| ---------- | ----------------------------------------- | ------------------------------------- |
| Scope      | Azure resources (e.g., workspace)         | Files and folders in ADLS Gen2        |
| Purpose    | Controls Synapse Studio, pipelines, pools | Controls read/write access to storage |
| Managed By | Azure Portal                              | ADLS Gen2 or Azure Storage Explorer   |

---

### **30. How can you use Managed Identity in Synapse?**

Managed Identity allows Synapse to securely authenticate to other Azure services (like ADLS, Azure SQL) without storing credentials.
Steps:

* Enable Managed Identity
* Grant it required permissions (e.g., **Storage Blob Data Contributor**)

---

### **31. What are the types of authentication supported?**

* **Azure AD (Single Sign-On)**
* **SQL Authentication** (username/password)
* **Managed Identity** (for secure service-to-service)
* **MSI** (for pipelines, Spark jobs, linked services)

---

### **32. What is a pipeline trigger and its types?**

Triggers define **when** a pipeline should run. Types:

* **Manual**: Run on demand
* **Schedule**: Time-based execution (e.g., hourly)
* **Event-based**: File arrival in ADLS
* **Tumbling Window**: Repeating fixed intervals with state management

---

### **33. How is version control integrated into Synapse?**

Synapse integrates with **Azure DevOps Git** or **GitHub** for versioning artifacts (pipelines, notebooks, SQL scripts).
Benefits:

* Branching
* Collaboration
* CI/CD deployment pipelines

---

### **34. Can you explain how serverless SQL pricing works?**

Serverless SQL is **pay-per-query**, based on the **amount of data processed** (measured in TB).
Price factors:

* Query complexity
* File format (Parquet > CSV in performance)
* Use of **caching** and **data skipping**

---

### **35. What is Delta Lake and how is it used in Synapse Spark?**

**Delta Lake** is an open-source storage layer that enables **ACID transactions**, **schema enforcement**, and **time travel** on data lakes.
In Synapse Spark:

* Use Delta Lake for robust data pipelines
* Supports streaming and batch workloads
* Enables schema evolution and versioning

```python
df.write.format("delta").save("abfss://mydata@account.dfs.core.windows.net/delta/sales")
```

---

Here are **Advanced-Level (36–50+)** answers for Azure Synapse Analytics, ideal for senior data engineers, architects, or interview preparation:

---

### **36. What are DMVs and how are they used for performance tuning?**

**DMVs (Dynamic Management Views)** in Synapse provide real-time insights into system performance, query execution, and resource usage.
Common uses:

* Monitor query performance (`sys.dm_pdw_exec_requests`)
* Identify data skew (`sys.dm_pdw_nodes_db_partition_stats`)
* Analyze table size and distribution

---

### **37. Explain how to implement Slowly Changing Dimensions (SCD) in Synapse.**

For **SCD Type 2**:

* Use **Data Flows** to compare source and target (hashing helps)
* Mark changes (Insert, Update, No Change)
* Maintain historical records by versioning with surrogate keys, effective dates
  Can also use **MERGE** statements in T-SQL for SCD Type 1.

---

### **38. How do you optimize a large data load in Dedicated SQL Pool?**

* Use **PolyBase** for high-speed parallel loading
* Use **CTAS** to stage data
* Use **minimal logging** with `BATCHSIZE`, `TABLOCK`
* Avoid **small file loads**; combine files beforehand
* **Pause statistics update** during bulk load

---

### **39. What is the best way to manage metadata in a lakehouse architecture?**

* Use **Azure Purview** or **Microsoft Fabric** for data cataloging
* Store metadata in **Delta Lake log** or **Hive metastore**
* Maintain **schema registry** for schema enforcement
* Track lineage and classifications for governance

---

### **40. How would you implement Change Data Capture (CDC) in Synapse?**

* For **Azure SQL source**: Use built-in **CDC or Change Tracking**, then extract deltas using Data Flows or ADF Pipelines
* For file-based: Track **watermarks** (e.g., modified date or incremental file naming)
* Use **Delta Lake MERGE** for upserts in Spark

---

### **41. How do you join Spark and SQL data in Synapse?**

* Load SQL data into a **Spark DataFrame** using JDBC
* Register Spark DataFrames as **temporary views**
* Use `spark.sql()` to join across Spark and SQL sources
  Example:

```python
df_sql = spark.read.jdbc(jdbcUrl, "dbo.Customers", properties=props)
df_parquet = spark.read.parquet("abfss://...")
df_sql.join(df_parquet, "CustomerID")
```

---

### **42. Explain best practices for distributing large fact tables.**

* Use **HASH distribution** on frequently joined foreign key
* Ensure **join keys** match in both fact and dimension tables
* Avoid ROUND\_ROBIN for large facts
* Monitor skew using `dm_pdw_nodes_db_partition_stats`

---

### **43. How to design a hybrid ELT/ETL pipeline using Synapse?**

* **ETL**: Ingest and transform using **Data Flows or Spark**
* **ELT**: Load raw data into staging SQL tables, then use **stored procedures or CTAS** for transformations
* Use **Synapse Pipelines** for orchestration
* Store raw → staged → curated layers

---

### **44. What are the limitations of Serverless SQL?**

* No support for **INSERT/UPDATE/DELETE** (read-only)
* No **indexes**, **materialized views**
* Query performance depends on file size/format
* Limited to **external tables** and **views**
* File metadata caching delays changes for up to 1hr

---

### **45. When would you choose Apache Spark over SQL Pool in Synapse?**

Use **Spark** when:

* Working with **semi-structured** (JSON, XML) or streaming data
* Need **machine learning or advanced analytics**
* Require **schema evolution** (Delta Lake)
* Performing **complex transformations** not easily expressed in SQL

---

### **46. What is the difference between workspace DB and dedicated SQL DB in Synapse?**

| Feature     | Workspace DB        | Dedicated SQL DB                   |
| ----------- | ------------------- | ---------------------------------- |
| Type        | Serverless          | Pre-provisioned (dedicated)        |
| Performance | Pay-per-query       | Reserved compute (DWUs)            |
| Storage     | Data Lake           | Synapse-managed distributed tables |
| Use case    | Ad-hoc, exploration | High-performance warehousing       |

---

### **47. How to use Synapse for real-time analytics?**

* Use **Spark Structured Streaming** to process real-time data
* Ingest from **Event Hubs**, **Kafka**, or **IoT Hub**
* Write to Delta Lake or materialized views
* Use **Power BI DirectQuery** or external tables on fresh data

---

### **48. What is the role of partitioning in Synapse performance?**

* Improves query performance by **data pruning**
* Applies to **external tables** (on file paths) and **Spark** (e.g., `partitionBy`)
* Helps avoid full scans
* In SQL Pool, partitioning must be **manually managed** at ETL level

---

### **49. How to automate deployment of Synapse resources using CI/CD?**

* Use **Synapse Git Integration (GitHub or Azure DevOps)**
* Deploy using **ARM templates**, **Synapse Workspace Deployment Tool**, or **Azure CLI**
* Automate pipelines using **Azure DevOps Pipelines or GitHub Actions**

---

### **50. How does Synapse support a Lakehouse architecture?**

* Combines **data lake (ADLS)** and **SQL engine** access
* Supports **Delta Lake** with Spark
* Use **serverless SQL** for exploration and BI
* Integrates **structured and unstructured data**
* Layers: **Raw → Bronze → Silver → Gold**

---

### **51. What is a Data Explorer Pool in Synapse and when should it be used?**

**Data Explorer Pools** are optimized for:

* **Log and telemetry analytics**
* High ingestion throughput
* Time-series data
  Used when you need fast ingestion and ad-hoc analytics on semi-structured data (like JSON or CSV logs)

---

### **52. Explain columnstore vs rowstore indexes in Synapse.**

| Feature     | Columnstore Index          | Rowstore Index                         |
| ----------- | -------------------------- | -------------------------------------- |
| Storage     | Column-wise                | Row-wise                               |
| Compression | High                       | Low                                    |
| Query Type  | Analytical workloads       | Point lookups, updates                 |
| Usage       | Default in Dedicated Pools | Use `HEAP` or clustered index manually |

---

### **53. What is Result Set Caching in Serverless SQL?**

* Caches query results for **identical queries**
* Speeds up performance and reduces cost
* Automatically invalidated if underlying data changes
* Must be enabled with `SET RESULT_SET_CACHING ON`

---

### **54. How can you encrypt data in Synapse (TDE, BYOK)?**

* **TDE (Transparent Data Encryption)**: Encrypts data at rest by default
* **BYOK (Bring Your Own Key)**: Uses customer-managed keys in Azure Key Vault
* **In-transit encryption**: TLS/SSL
* **Column-level encryption**: Handled in SQL layer manually

---

### **55. Explain the use of Spark Structured Streaming in Synapse.**

* Processes real-time data in **micro-batches**
* Supports sources like Event Hubs, Kafka, ADLS
* Output can be written to Delta, Parquet, SQL, or Power BI
* Ensures **exactly-once** processing and **fault tolerance**

---

